"""Local practice runner; Python standard library, Python 3.11+."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SLUGS = {'01':'01-incident-desk','02':'02-cached-catalog','03':'03-inventory-reservations'}
class PracticeError(Exception):
    def __init__(self, status, message):
        super().__init__(message); self.status=status
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def within(path, root):
    try: path.resolve().relative_to(root.resolve()); return True
    except ValueError: return False
def safe_files(root):
    for p in root.rglob('*'):
        if p.is_symlink() or not within(p,root):
            raise PracticeError('INVALID_CONFIGURATION',f'Symlink or escaping path: {p}')
        if p.is_file(): yield p
def hashes(root):
    return {p.relative_to(root).as_posix():digest(p) for p in safe_files(root)}
def select_target(assessment, attempt=None, root=ROOT):
    if assessment not in SLUGS: raise PracticeError('INVALID_CONFIGURATION','Unknown assessment ID')
    if attempt:
        target=Path(attempt)
        if not target.is_absolute(): target=root/target
        if not within(target,root/'attempts') or target.resolve()==(root/'attempts').resolve():
            raise PracticeError('INVALID_CONFIGURATION','Attempt must be inside this pack attempts tree')
    else: target=root/'candidate'/SLUGS[assessment]
    if not target.is_dir() or not within(target,root): raise PracticeError('INVALID_CONFIGURATION','Invalid target directory')
    if read_json(target/'assessment.json').get('id')!=assessment:
        raise PracticeError('INVALID_CONFIGURATION','Assessment ID mismatch')
    list(safe_files(target/'src'))
    return target.resolve()
def validate_manifest(m):
    if m.get('schemaVersion')!=1: raise PracticeError('INVALID_CONFIGURATION','Unsupported manifest schema')
    entries=m.get('tests',[])
    pairs=[(x['className'],x['methodName']) for x in entries]
    ids=[x['id'] for x in entries]
    if (len(entries)!=27 or len(set(pairs))!=27 or len(set(ids))!=27
        or sum(x['points'] for x in entries)!=100
        or sum(x['points']==4 for x in entries)!=25 or sum(x['points']==0 for x in entries)!=2
        or m.get('maxPoints')!=100 or m.get('expectedScoredTests')!=25 or m.get('expectedSmokeTests')!=2
        or sum(x['points']==4 and x.get('visibility')=='public' for x in entries)!=15
        or sum(x['points']==4 and x.get('visibility')=='private' for x in entries)!=10
        or {x['methodName'] for x in entries if x['points']==0}!={'contextStarts','healthResponds'}
        or any(x.get('visibility')!='public' for x in entries if x['points']==0)):
        raise PracticeError('INVALID_CONFIGURATION','Manifest test totals or identities are invalid')
    return entries
def verify_files(root, expected):
    bad=[]
    for name, expected_hash in expected.items():
        p=root/name
        if not within(p,root) or p.is_symlink() or not p.is_file() or digest(p)!=expected_hash: bad.append(name)
    if bad: raise PracticeError('INVALID_CONFIGURATION','Changed or missing protected/trusted files: '+', '.join(bad))
def verify_protected(target, manifest):
    verify_files(target,manifest['protectedFiles'])
    expected=set(manifest['protectedFiles'])
    extras=[]
    for tree in manifest.get('protectedTrees',[]):
        for path in safe_files(target/tree):
            rel=path.relative_to(target).as_posix()
            if rel not in expected: extras.append(rel)
    for name in ('.mvn/maven.config','.mvn/jvm.config','.mvn/extensions.xml'):
        if (target/name).exists() and name not in expected: extras.append(name)
    if extras: raise PracticeError('INVALID_CONFIGURATION','Unexpected protected files: '+', '.join(sorted(set(extras))))
def load_manifest(assessment, root=ROOT):
    index=read_json(root/'_authoring/authoritative-manifest.json')
    if index.get('schemaVersion')!=1: raise PracticeError('INVALID_CONFIGURATION','Unsupported author index schema')
    entry=index['assessments'][assessment]
    verify_files(root/'_authoring',{entry['path']:entry['sha256']})
    base=root/'_authoring'/SLUGS[assessment]
    m=read_json(root/'_authoring'/entry['path']); validate_manifest(m)
    if m['assessmentId']!=assessment: raise PracticeError('INVALID_CONFIGURATION','Trusted assessment ID mismatch')
    verify_files(base,m['trustedFiles'])
    actual={path.relative_to(base).as_posix() for folder in ('trusted-build','trusted-tests') for path in safe_files(base/folder)}
    if actual!=set(m['trustedFiles']):
        raise PracticeError('INVALID_CONFIGURATION','Trusted bundle has unexpected or missing files: '+', '.join(sorted(actual^set(m['trustedFiles']))))
    return m,base
def evaluate(report_dir, manifest, exit_code):
    expected=validate_manifest(manifest)
    known={(x['className'],x['methodName']):x for x in expected}
    found={}; issues=[]
    files=sorted(Path(report_dir).glob('TEST-*.xml'))
    if not files: return {'status':'BUILD_ERROR','score':None,'diagnostic':'No test reports in this run'}
    for path in files:
        try: tree=ET.parse(path)
        except ET.ParseError as e:
            return {'status':'INCOMPLETE_TEST_RUN','score':None,'diagnostic':f'Malformed XML {path}: {e}'}
        for case in tree.getroot().iter('testcase'):
            pair=(case.get('classname'),case.get('name'))
            if pair not in known: issues.append('Unexpected method '+str(pair)); continue
            if pair in found: issues.append('Duplicate method '+str(pair)); continue
            result='passed'; detail=''
            for tag in ('skipped','failure','error'):
                child=case.find(tag)
                if child is not None:
                    result=tag; detail=(child.get('message','')+'\n'+(child.text or '')).strip();break
            found[pair]={'result':result,'detail':detail}
            if result=='skipped': issues.append('Skipped method '+str(pair))
    for pair in known.keys()-found.keys(): issues.append('Missing method '+str(pair))
    if issues: return {'status':'INCOMPLETE_TEST_RUN','score':None,'diagnostic':'; '.join(issues)}
    results=[dict(x,**found[(x['className'],x['methodName'])]) for x in expected]
    if any(x['points']==0 and x['result']!='passed' for x in results):
        return {'status':'APPLICATION_NOT_READY','score':None,'diagnostic':'Smoke tests failed','results':results}
    score=sum(x['points'] for x in results if x['result']=='passed')
    if score==100 and exit_code!=0:
        return {'status':'BUILD_ERROR','score':None,'diagnostic':'Maven failed despite passing XML'}
    if score<100 and exit_code==0:
        return {'status':'BUILD_ERROR','score':None,'diagnostic':'Maven unexpectedly succeeded despite failed tests'}
    return {'status':'GRADED','score':score,'results':results,
            'publicPassed':sum(x['points']==4 and x['visibility']=='public' and x['result']=='passed' for x in results),
            'privatePassed':sum(x['points']==4 and x['visibility']=='private' and x['result']=='passed' for x in results),
            'smokePassed':2}
def snapshot(target, destination, base):
    if destination.exists(): raise PracticeError('INVALID_CONFIGURATION','Snapshot destination already exists')
    destination.mkdir(parents=True)
    for p in safe_files(target/'src/main/java'):
        rel=p.relative_to(target); out=destination/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
    for folder in ('trusted-build','trusted-tests'):
        for p in safe_files(base/folder):
            out=destination/p.relative_to(base/folder);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
def wrapper(target):
    return [str(target/'mvnw.cmd')] if os.name=='nt' else ['sh',str(target/'mvnw')]
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def tool_output(command, cwd=None):
    try:
        p=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',timeout=120)
        return {'command':command,'exitCode':p.returncode,'output':p.stdout}
    except (OSError,subprocess.TimeoutExpired) as e: return {'command':command,'exitCode':None,'output':str(e)}
def grade_internal(target,assessment,root=ROOT,details=False):
    m,base=load_manifest(assessment,root)
    verify_protected(target,m)
    before=hashes(target/'src')
    run=root/'.runs'/f'{assessment}-{dt.datetime.now().strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex[:10]}'
    snapshot(target,run,base)
    command=wrapper(run)+['-B','-ntp','clean','test']
    metadata={'command':command,'cwd':str(run),'start':utc(),'toolchain':[
        tool_output(['java','-version']),tool_output(['javac','-version']),tool_output(wrapper(run)+['-v'],run)]}
    with (run/'build.log').open('w',encoding='utf-8') as log:
        try:
            result=subprocess.run(command,cwd=run,stdout=log,stderr=subprocess.STDOUT,timeout=600)
            metadata['exitCode']=result.returncode
            report=evaluate(run/'target/surefire-reports',m,result.returncode)
        except subprocess.TimeoutExpired:
            metadata['exitCode']=None;report={'status':'BUILD_TIMEOUT','score':None,'diagnostic':'Build exceeded 600 seconds'}
        except OSError as e:
            metadata['exitCode']=None;report={'status':'BUILD_ERROR','score':None,'diagnostic':str(e)}
    metadata['end']=utc();write_json(run/'execution.json',metadata)
    if hashes(target/'src')!=before: report={'status':'INVALID_CONFIGURATION','score':None,'diagnostic':'Source changed during grading'}
    report.update({'assessmentId':assessment,'attempt':str(target.relative_to(root)),'time':utc()})
    write_json(run/'private-result.json',report)
    safe={k:v for k,v in report.items() if k!='results'}
    safe['buildLog']=str((run/'build.log').relative_to(root))
    safe['failedPublicIds']=[x['id'] for x in report.get('results',[]) if x['points'] and x['visibility']=='public' and x['result']!='passed']
    safe['failedPrivateIds']=[x['id'] for x in report.get('results',[]) if x['points'] and x['visibility']=='private' and x['result']!='passed']
    if details:
        print('Spoiler warning: detailed report contains private test failure information.')
        write_json(root/'reports'/(run.name+'-SPOILERS.json'),report)
    write_json(root/'reports'/(run.name+'.json'),safe)
    summary=f"Assessment {assessment}\nStatus: {safe['status']}\nScore: {str(safe['score'])+'/100' if safe['score'] is not None else 'ungraded'}\n"
    if safe['status']=='GRADED':
        summary+=f"Public: {safe['publicPassed']}/15 passed\nPrivate: {safe['privatePassed']}/10 passed\nSmoke: 2/2 passed\nFailed public IDs: {', '.join(safe['failedPublicIds'])}\nFailed private IDs: {', '.join(safe['failedPrivateIds'])}\n"
    else: summary+=safe.get('diagnostic','')+'\nBuild log (may contain private test details): '+safe['buildLog']+'\n'
    summary+='Attempt: '+safe['attempt']+'\n'
    (root/'reports'/(run.name+'.txt')).write_text(summary,encoding='utf-8');print(summary)
    return (0 if safe['score']==100 else 1) if safe['status']=='GRADED' else 2
def extract_archive(archive,destination):
    if destination.exists(): raise PracticeError('INVALID_CONFIGURATION','Extraction destination already exists')
    with zipfile.ZipFile(archive) as z:
        seen=set()
        for info in z.infolist():
            name=info.filename; parts=PurePosixPath(name).parts
            if ('\\' in name or ':' in name or name.startswith('/') or '..' in parts
                or stat.S_ISLNK(info.external_attr>>16) or name.casefold() in seen
                or not within(destination/name,destination)):
                raise PracticeError('INVALID_CONFIGURATION',f'Unsafe archive entry: {name}')
            if any(x in {'.git','target','_authoring','.runs'} for x in parts) or 'PrivateContractTest' in name or name.endswith(('SOLUTION.md','HINTS.md','.patch')):
                raise PracticeError('INVALID_CONFIGURATION',f'Noncandidate archive entry: {name}')
            seen.add(name.casefold())
        destination.mkdir(parents=True)
        z.extractall(destination)
    if os.name!='nt': (destination/'mvnw').chmod(0o755)
def new_attempt(assessment,name,root=ROOT):
    if assessment not in SLUGS: raise PracticeError('INVALID_CONFIGURATION','Unknown assessment ID')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}',name): raise PracticeError('INVALID_CONFIGURATION','Name must contain 1–60 letters, digits, hyphens or underscores')
    manifest=read_json(root/'pack-manifest.json');slug=SLUGS[assessment]
    entry=manifest['starterArchives'][assessment];archive=root/entry['path']
    verify_files(root,{entry['path']:entry['sha256']})
    destination=root/'attempts'/slug/(dt.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+name+'-'+uuid.uuid4().hex[:8])
    if not within(destination,root/'attempts'): raise PracticeError('INVALID_CONFIGURATION','Escaping attempt destination')
    extract_archive(archive,destination)
    verify_files(destination,entry['sourceHashes']);select_target(assessment,str(destination),root)
    print(str(destination))
    for action in ('test','grade'): print(f'python tools/practice.py {action} {assessment} --attempt "{destination.relative_to(root)}"')
    return destination
def doctor(root=ROOT):
    ok=sys.version_info>=(3,11);print('Python:',sys.version);print('OS:',platform.platform())
    for cmd in (['java','-version'],['javac','-version']):
        r=tool_output(cmd);print(r['output']);ok &= r['exitCode']==0 and bool(re.search(r'\b21(?:\.|\b)',r['output']))
    for i,slug in SLUGS.items():
        p=root/'candidate'/slug;print('Repository:',p)
        try:
            m,_=load_manifest(i,root);verify_files(p,m['protectedFiles'])
            r=tool_output(wrapper(p)+['-v'],p);print('Java actually used by Maven:\n'+r['output'])
            ok &= r['exitCode']==0 and 'Apache Maven 3.9.9' in r['output'] and bool(re.search(r'Java version: 21[.,]',r['output']))
        except (PracticeError,OSError,ValueError) as e: print(str(e));ok=False
    print('Prerequisites verified.' if ok else 'Setup incomplete. Use JDK 21 (JAVA_HOME points to its directory, not bin), Python 3.11+, and restore missing protected files from a fresh attempt. First wrapper run needs download access.')
    return 0 if ok else 2
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    for name in ('test','grade','new-attempt'):
        q=sub.add_parser(name);q.add_argument('assessment',choices=SLUGS)
        if name=='new-attempt':q.add_argument('--name',default='practice')
        else:q.add_argument('--attempt')
        if name=='grade':q.add_argument('--details',action='store_true')
    a=p.parse_args(argv)
    try:
        if sys.version_info<(3,11):raise PracticeError('INVALID_CONFIGURATION','Python 3.11+ required')
        if a.command=='doctor':return doctor()
        if a.command=='new-attempt':new_attempt(a.assessment,a.name);return 0
        target=select_target(a.assessment,a.attempt)
        if a.command=='test':return subprocess.run(wrapper(target)+['-B','-ntp','test'],cwd=target).returncode
        return grade_internal(target,a.assessment,details=a.details)
    except (PracticeError,OSError,ValueError,KeyError,zipfile.BadZipFile) as e:
        print(f'{getattr(e,"status","INVALID_CONFIGURATION")}: {e}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
