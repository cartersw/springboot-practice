"""Execute every original mutation independently and check source traceability."""
import difflib
import json
from pathlib import Path
import shutil
import sys
import run_verification as v
import practice as p

def main(assessment,resume=False):
    base=v.ROOT/'_authoring'/p.SLUGS[assessment]
    manifest=p.read_json(base/'mutation-manifest.json')
    full=p.read_json(base/'grader-manifest.json')
    method_ids={(t['className'],t['methodName']):t['id'] for t in full['tests']}
    combined={f.relative_to(base/'reference').as_posix():f.read_text(encoding='utf-8') for f in (base/'reference/src/main/java').rglob('*.java')}
    records=[]
    for mutation in manifest['mutations']:
        destination=v.EVIDENCE/mutation['id']
        if not resume:
            shutil.copytree(base/'reference',destination,ignore=shutil.ignore_patterns('target','.git'))
            v.run(mutation['id']+'-apply',['git','apply','--unsafe-paths',str(base/mutation['patch'])],destination)
            result=v.maven(mutation['id'],destination,['clean','test'],1)
        else: result=p.read_json(v.EVIDENCE/(mutation['id']+'.json'))
        tests=result['tests']
        assert len(tests)==27 and all(t['result'] in ('passed','failure') for t in tests)
        assert sum(t['method'] in ('contextStarts','healthResponds') and t['result']=='passed' for t in tests)==2
        failed=[method_ids[t['class'],t['method']] for t in tests if t['result']=='failure']
        assert set(failed)&set(mutation['designatedDetectingIds']),mutation['id']
        records.append({'id':mutation['id'],'failedIds':failed,'smoke':2,'status':'PASS'})
        mutation['observedFailingIds']=failed
        mutation['buildExitCode']=1
        mutation['verificationEvidence']='../verification/'+mutation['id']+'.json'
        mutation.pop('patchCheck',None)
        for changed in mutation['files']:
            relative=changed['path'];reference=base/'reference'/relative;mutant=destination/relative
            changed['referenceSha256']=p.digest(reference);changed['starterSha256']=p.digest(mutant)
            changed['combinedStarterSha256']=p.digest(v.ROOT/'candidate'/p.SLUGS[assessment]/relative)
            original=reference.read_text(encoding='utf-8').splitlines(keepends=True)
            altered=mutant.read_text(encoding='utf-8').splitlines(keepends=True)
            # Individual patches intentionally have reference-only context. Compose their
            # disjoint changed lines, rather than trying to reapply overlapping context.
            for tag,i,j,k,l in difflib.SequenceMatcher(a=original,b=altered).get_opcodes():
                if tag=='equal': continue
                old=''.join(original[i:j]);new=''.join(altered[k:l])
                assert old and combined[relative].count(old)==1,(mutation['id'],relative)
                combined[relative]=combined[relative].replace(old,new,1)
        print(mutation['id'],'detected; smoke 2/2',flush=True)
    for relative,expected in combined.items():
        assert expected==(v.ROOT/'candidate'/p.SLUGS[assessment]/relative).read_text(encoding='utf-8'),relative
    p.write_json(base/'mutation-manifest.json',manifest)
    p.write_json(v.EVIDENCE/(assessment+'-mutations.json'),{'status':'PASS','individual':records,'exactCombinedSource':True})

if __name__=='__main__':main(sys.argv[1])
