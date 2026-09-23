"""Evidence runner. Invoke with the pack-local Python or another Python 3.11+."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'_authoring'))
sys.path.insert(0, str(ROOT/'tools'))
import practice as p
TOOLS = ROOT/'_authoring/toolchain'
EVIDENCE = ROOT/'_authoring/verification'
ENV = os.environ.copy()
ENV['JAVA_HOME'] = str(next(TOOLS.glob('jdk-*')))
ENV['PATH'] = str(TOOLS/'python')+os.pathsep+str(Path(ENV['JAVA_HOME'])/'bin')+os.pathsep+ENV['PATH']
ENV['MAVEN_USER_HOME'] = str(TOOLS/'maven-home')
ENV['MAVEN_OPTS'] = '-Dmaven.repo.local="'+str(TOOLS/'repository')+'"'

def cases(target):
    result = []
    for path in (target/'target/surefire-reports').glob('TEST-*.xml'):
        for c in ET.parse(path).getroot().iter('testcase'):
            result.append({'class':c.get('classname'), 'method':c.get('name'), 'result':next((t for t in ('failure','error','skipped') if c.find(t) is not None),'passed')})
    return result

def run(name, command, cwd=ROOT, expected=0):
    log = EVIDENCE/(name+'.log')
    record = {'command':list(map(str, command)), 'cwd':str(cwd), 'start':p.utc(), 'expectedExit':expected}
    with log.open('w',encoding='utf-8') as output:
        result = subprocess.run(command,cwd=cwd,env=ENV,stdout=output,stderr=subprocess.STDOUT,timeout=600)
    record.update(exitCode=result.returncode,end=p.utc(),log=str(log.relative_to(ROOT)))
    if any('mvnw' in str(x) for x in command): record['tests']=cases(cwd)
    p.write_json(EVIDENCE/(name+'.json'), record)
    print(name, 'exit', result.returncode, 'expected', expected, flush=True)
    if result.returncode != expected: raise RuntimeError(f'{name}: unexpected exit; see {log}')
    return record

def maven(name,target,args,expected=0):
    return run(name,p.wrapper(target)+['-B','-ntp']+args,target,expected)

def assert_suite(record, public, private=0, failures=0):
    tests=record['tests']
    assert len(tests)==public+private+2, record
    assert sum(t['result']=='failure' for t in tests)==failures, record
    assert all(t['result'] in ('passed','failure') for t in tests), record
    assert sum(t['method'] in ('contextStarts','healthResponds') and t['result']=='passed' for t in tests)==2, record

def startup(assessment,target,label,demo=True):
    port=8080+int(assessment)
    command=p.wrapper(target)+['-B','-ntp','spring-boot:run']
    if demo: command+=['-Dspring-boot.run.profiles=demo']
    log=EVIDENCE/(label+'-startup.log')
    record={'command':command,'cwd':str(target),'start':p.utc(),'responses':[]}
    def request(path,body=None,method=None):
        url='http://127.0.0.1:'+str(port)+path
        data=None if body is None else json.dumps(body).encode()
        req=urllib.request.Request(url,data=data,method=method,headers={'Content-Type':'application/json'})
        try: response=urllib.request.urlopen(req,timeout=3)
        except urllib.error.HTTPError as error: response=error
        with response:
            raw=response.read();result={'path':path,'status':response.status,'body':json.loads(raw) if raw else None}
        record['responses'].append(result)
        return result
    # Refuse to accidentally inspect another process on the expected port.
    import socket
    with socket.socket() as sock:
        assert sock.connect_ex(('127.0.0.1',port))!=0, f'Port {port} occupied'
    with log.open('w',encoding='utf-8') as output:
        process=subprocess.Popen(command,cwd=target,env=ENV,stdout=output,stderr=subprocess.STDOUT,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            deadline=time.monotonic()+90
            while True:
                if process.poll() is not None: raise RuntimeError(f'Application exited: {log}')
                try:
                    health=request('/health')
                    if health['status']==200 and health['body']=={'status':'UP'}: break
                except (OSError,ValueError): pass
                if time.monotonic()>deadline: raise TimeoutError(str(log))
                time.sleep(.25)
            if assessment=='01':
                if demo:
                    result=request('/api/tickets/101');assert result['status']==200 and result['body']['externalRef']=='INC-101'
                else: assert request('/api/tickets')['body']==[]
                error=request('/api/tickets?sort=unknown');assert error['status']==400 and error['body']['code']=='INVALID_REQUEST'
                created=request('/api/tickets',{'externalRef':'MANUAL-900','title':'Verification','priority':2})
                assert created['status']==(201 if label.startswith('reference') else 200)
                assert request('/api/tickets/'+str(created['body']['id']))['body']==created['body']
            elif assessment=='02':
                result=request('/api/products?category=electronics&size=50')
                assert result['status']==200
                assert [x['id'] for x in result['body']['content']]==([110,103,104,101,102] if demo else [])
                error=request('/api/products?size=0');assert error['status']==400 and error['body']['code']=='INVALID_REQUEST'
            else:
                if demo:
                    body={'requestKey':'manual-900','customerRef':'verify','items':[{'sku':'BOLT-M8','quantity':3},{'sku':'NUT-M8','quantity':2}]}
                    created=request('/api/reservations',body);assert created['status']==201
                    assert request('/api/reservations/'+str(created['body']['id']))['body']==created['body']
                else: assert request('/api/inventory/summary')['body']==[]
                error=request('/api/reservations/0');assert error['status']==400 and error['body']['code']=='INVALID_REQUEST'
            record.update(status='PASS',end=p.utc())
        finally:
            if os.name=='nt': subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else: process.terminate()
            process.wait(timeout=20)
    p.write_json(EVIDENCE/(label+'-startup.json'),record)
    print(label,'startup PASS',flush=True)

def assessment_gates(assessment,skip_reference=False):
    slug=p.SLUGS[assessment];reference=ROOT/'_authoring'/slug/'reference';candidate=ROOT/'candidate'/slug
    for seed in (() if skip_reference else (1701,92837)):
        args=['-Djunit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random',
              '-Djunit.jupiter.testclass.order.default=org.junit.jupiter.api.ClassOrderer$Random',
              f'-Djunit.jupiter.execution.order.random.seed={seed}','test']
        assert_suite(maven(assessment+f'-random-{seed}',reference,args),15,10)
    if not skip_reference:
        maven(assessment+'-reference-package',reference,['-DskipTests','package'])
        startup(assessment,reference,'reference-'+assessment)
        startup(assessment,reference,'reference-'+assessment+'-default',False)
    # Same grading path as candidate CLI, without exposing a restore-solution CLI.
    os.environ.update(ENV)
    grade_source=EVIDENCE/(assessment+'-reference-grade-source')
    shutil.copytree(reference,grade_source,ignore=shutil.ignore_patterns('target','.git','*PrivateContractTest.java'))
    with (EVIDENCE/(assessment+'-reference-grade.log')).open('w',encoding='utf-8') as output:
        import contextlib
        with contextlib.redirect_stdout(output): code=p.grade_internal(grade_source,assessment,ROOT)
    assert code==0
    print(assessment,'reference grade 100/100',flush=True)
    maven(assessment+'-candidate-build',candidate,['clean','-DskipTests','package'])
    assert_suite(maven(assessment+'-candidate-smoke',candidate,['-Dtest=SmokeTest','test']),0)
    expected_failures=9 if assessment=='01' else 8
    assert_suite(maven(assessment+'-candidate-public',candidate,['test'],1),15,failures=expected_failures)
    assert_suite(maven(assessment+'-candidate-offline',candidate,['-o','test'],1),15,failures=expected_failures)
    startup(assessment,candidate,'candidate-'+assessment)
    run(assessment+'-candidate-grade',[sys.executable,'tools/practice.py','grade',assessment],expected=1)
    run(assessment+'-new-attempt',[sys.executable,'tools/practice.py','new-attempt',assessment,'--name','final-verification'])
    attempt=Path((EVIDENCE/(assessment+'-new-attempt.log')).read_text().splitlines()[0])
    maven(assessment+'-fresh-build',attempt,['clean','-DskipTests','package'])
    assert_suite(maven(assessment+'-fresh-smoke',attempt,['-Dtest=SmokeTest','test']),0)
    run(assessment+'-fresh-test',[sys.executable,'tools/practice.py','test',assessment,'--attempt',str(attempt)],expected=1)
    assert_suite({'tests':cases(attempt)},15,failures=expected_failures)
    run(assessment+'-fresh-grade',[sys.executable,'tools/practice.py','grade',assessment,'--attempt',str(attempt)],expected=1)
    p.verify_files(attempt,p.read_json(ROOT/'pack-manifest.json')['starterArchives'][assessment]['sourceHashes'])
    p.write_json(EVIDENCE/(assessment+'-gates.json'),{'status':'PASS','attempt':str(attempt.relative_to(ROOT)),'completed':p.utc()})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode');ap.add_argument('assessment',nargs='?');a=ap.parse_args()
    if a.mode=='reference':
        target=ROOT/'_authoring'/p.SLUGS[a.assessment]/'reference'
        maven(a.assessment+'-reference',target,['clean','test'])
    elif a.mode=='tools':
        run('utility-tests',[sys.executable,'-m','unittest','discover','-s','tools','-v'])
        run('doctor',[sys.executable,'tools/practice.py','doctor'])
    elif a.mode=='gates': assessment_gates(a.assessment)
    elif a.mode=='starter-gates': assessment_gates(a.assessment,True)
    elif a.mode=='mutations':
        import verify_mutations
        verify_mutations.main(a.assessment)
    elif a.mode=='mutation-summary':
        import verify_mutations
        verify_mutations.main(a.assessment,True)
    elif a.mode=='extra':
        import verify_extra
        verify_extra.main(a.assessment)
    elif a.mode=='final-public':
        target=ROOT/'candidate'/p.SLUGS[a.assessment]
        assert_suite(maven(a.assessment+'-final-public',target,['clean','test'],1),15,failures=9 if a.assessment=='01' else 8)
    else: raise ValueError(a.mode)
if __name__=='__main__': main()
