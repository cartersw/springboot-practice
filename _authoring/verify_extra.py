"""Regression, portability and grader failure-path execution."""
import contextlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import zipfile
import run_verification as v
import practice as p

def source_copy(assessment,name,private=True):
    source=v.ROOT/'_authoring'/p.SLUGS[assessment]/'reference'
    target=v.EVIDENCE/name
    ignored=['target','.git']+([] if private else ['*PrivateContractTest.java'])
    shutil.copytree(source,target,ignore=shutil.ignore_patterns(*ignored))
    return target

def grade_failure(target,assessment,label,status):
    os.environ.update(v.ENV)
    previous=set((v.ROOT/'.runs').iterdir())
    with (v.EVIDENCE/(label+'.log')).open('w',encoding='utf-8') as output,contextlib.redirect_stdout(output):
        code=p.grade_internal(target,assessment,v.ROOT)
    assert code==2
    current=set((v.ROOT/'.runs').iterdir())-previous
    report=next(p.read_json(x/'private-result.json') for x in current if (x/'private-result.json').is_file() and p.read_json(x/'private-result.json')['attempt']==str(target.relative_to(v.ROOT)))
    assert report['status']==status and report['score'] is None, report
    return report

def main(mode):
    if mode=='regressions':
        target=source_copy('03','alternate-payload')
        file=target/'src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java'
        text=file.read_text();old='mapper.writeValueAsString(List.of(customer,items.stream().map(i->List.of(i.sku(),i.quantity())).toList()))'
        assert old in text
        file.write_text(text.replace(old,'Base64.getEncoder().encodeToString('+old+'.getBytes(java.nio.charset.StandardCharsets.UTF_8))'),encoding='utf-8')
        v.assert_suite(v.maven('alternate-payload',target,['clean','test']),15,10)
        target=source_copy('01','string-id-regression')
        base=target/'src/main/java/dev/practice/assessment01'
        file=base/'dto/TicketResponse.java';file.write_text(file.read_text().replace('long id','String id'))
        file=base/'mapper/TicketMapper.java';file.write_text(file.read_text().replace('new TicketResponse(t.getId(),','new TicketResponse(t.getId().toString(),'))
        result=v.maven('string-id-regression',target,['clean','test'],1)
        assert any(t['method']=='a1_01' and t['result']=='failure' for t in result['tests'])
        assert all(t['result'] in ('passed','failure') for t in result['tests'])
        p.write_json(v.EVIDENCE/'test-quality-regressions.json',{'alternateCanonicalEncoding':'27/27 passed','wrongJsonIdType':'detected by scored assertions'})
    elif mode=='tooling':
        target=source_copy('01','protected-edit-source',False)
        file=target/'pom.xml';file.write_text(file.read_text()+'\n<!-- edit -->\n')
        before=p.hashes(target)
        try:p.grade_internal(target,'01',v.ROOT)
        except p.PracticeError as error:assert error.status=='INVALID_CONFIGURATION'
        else:raise AssertionError('Protected edit accepted')
        assert before==p.hashes(target)
        target=source_copy('01','compile-error-source',False)
        file=target/'src/main/java/dev/practice/assessment01/service/TicketService.java';file.write_text(file.read_text()+'\nINVALID JAVA\n')
        report=grade_failure(target,'01','compile-error-grade','BUILD_ERROR')
        # An editable MVC controller can make health fail without editing protected files.
        target=source_copy('01','smoke-error-source',False)
        file=target/'src/main/java/dev/practice/assessment01/controller/HealthInterceptor.java'
        file.write_text('''package dev.practice.assessment01.controller;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.*;
import org.springframework.web.servlet.HandlerInterceptor;
@Configuration public class HealthInterceptor implements WebMvcConfigurer {
 public void addInterceptors(InterceptorRegistry registry){registry.addInterceptor(new HandlerInterceptor(){
  public boolean preHandle(jakarta.servlet.http.HttpServletRequest req,jakarta.servlet.http.HttpServletResponse res,Object h)throws Exception{res.setStatus(503);return false;}
 }).addPathPatterns("/health");}
}''')
        grade_failure(target,'01','smoke-error-grade','APPLICATION_NOT_READY')
        p.write_json(v.EVIDENCE/'tooling-errors.json',{'protectedChanges':'rejected without changing source','compileFailure':'BUILD_ERROR / exit 2 / score null','smokeFailure':'APPLICATION_NOT_READY / exit 2 / score null'})
    elif mode=='portable':
        run=v.run('portable-export',[sys.executable,'tools/export_portable.py'])
        text=(v.EVIDENCE/'portable-export.log').read_text()
        destination=Path(re.search(r'Portable folder: (.+)',text).group(1).strip())
        archive=Path(re.search(r'Portable ZIP: (.+)',text).group(1).strip())
        with zipfile.ZipFile(archive) as z:
            assert all((i.external_attr>>16)&0o111 for i in z.infolist() if i.filename.endswith('/mvnw'))
        for assessment,slug in p.SLUGS.items():
            candidate=destination/'candidate'/slug
            p.verify_files(candidate,p.read_json(destination/'pack-manifest.json')['starterArchives'][assessment]['sourceHashes'])
            p.verify_protected(candidate,p.load_manifest(assessment,destination)[0])
        assert not list((destination/'candidate').rglob('*Private*'))
        assert not list(destination.rglob('SOLUTION.md'))
        assert not (destination/'_authoring/toolchain').exists()
        p.write_json(v.EVIDENCE/'portable-result.json',{'status':'PASS','zip':str(archive.relative_to(v.ROOT)),'sha256':p.digest(archive),'executableWrappers':True})
    elif mode=='bash':
        bash=Path('C:/Program Files/Git/bin/bash.exe')
        for assessment,slug in p.SLUGS.items():
            target=v.ROOT/'attempts'/slug/'verification with spaces'
            if not target.exists(): p.extract_archive(v.ROOT/'starter-archives'/(slug+'.zip'),target)
            # CMD and POSIX shells parse MAVEN_OPTS quoting differently. Pass the
            # already-selected cache as a quoted JVM option at the shell boundary.
            windows_opts=v.ENV['MAVEN_OPTS']
            v.ENV['MAVEN_OPTS']='-Dmaven.repo.local='+str(v.TOOLS/'repository').replace('\\','/')
            v.run(assessment+'-bash-version',[str(bash),'-c','./mvnw -v'],target)
            record=v.run(assessment+'-bash-test',[str(bash),'-c','./mvnw -o -B -ntp clean test'],target,1)
            v.assert_suite({'tests':v.cases(target)},15,failures=9 if assessment=='01' else 8)
            v.ENV['MAVEN_OPTS']=windows_opts
            v.run(assessment+'-spaces-grade',[sys.executable,'tools/practice.py','grade',assessment,'--attempt',str(target)],expected=1)
        p.write_json(v.EVIDENCE/'bash-result.json',{'status':'PASS','platform':'Git Bash on Windows','nativeMacLinuxVerified':False})
    elif mode=='instructions':
        guide=(v.ROOT/'START_HERE.md').read_text(encoding='utf-8')
        blocks=re.findall(r'```powershell\n(.*?)```',guide,re.S)
        # Exact setup and Windows commands from START_HERE; the server has its own live check.
        setup='\n'.join(line[3:] if line.startswith('   ') else line for line in blocks[0].splitlines())
        v.run('start-here-setup',['powershell','-NoProfile','-Command',setup])
        for assessment,slug in p.SLUGS.items():
            target=v.ROOT/'candidate'/slug
            cls={'01':'Ticket','02':'Catalog','03':'Reservation'}[assessment]+'PublicContractTest'
            v.maven(assessment+'-selected-test',target,[f'-Dtest={cls}#a{int(assessment)}_05','test'],1)
    elif mode=='git':
        # Restore verified archives as the normal user so Git ownership checks also
        # work outside the execution sandbox. Preserve the prior copies and outputs.
        previous=v.ROOT/'candidate'
        backup=v.EVIDENCE/'pre-git-candidate'
        assert p.within(previous,v.ROOT) and p.within(backup,v.ROOT)
        for assessment,slug in p.SLUGS.items():
            p.verify_files(previous/slug,p.read_json(v.ROOT/'pack-manifest.json')['starterArchives'][assessment]['sourceHashes'])
        if not backup.exists():
            previous.rename(backup)
            for assessment,slug in p.SLUGS.items():
                p.extract_archive(v.ROOT/'starter-archives'/(slug+'.zip'),previous/slug)
        for assessment,slug in p.SLUGS.items():
            target=v.ROOT/'candidate'/slug
            if not (target/'.git').exists():
                v.run(assessment+'-git-init',['git','init','-b','main'],target)
                v.run(assessment+'-git-longpaths',['git','config','core.longpaths','true'],target)
                v.run(assessment+'-git-add',['git','add','--all'],target)
                v.run(assessment+'-git-wrapper-mode',['git','update-index','--chmod=+x','mvnw'],target)
                v.run(assessment+'-git-commit',['git','-c','user.name=Practice Builder','-c','user.email=practice-builder@localhost','commit','-m','Unsolved practice starter'],target)
                v.run(assessment+'-git-tag',['git','tag','starter-v1'],target)
            clone=v.EVIDENCE/'clone with spaces'/slug
            if not clone.exists(): v.run(assessment+'-git-clone',['git','clone','--config','core.longpaths=true','--no-hardlinks',str(target),str(clone)])
            else:
                v.run(assessment+'-clone-longpaths',['git','config','core.longpaths','true'],clone)
                v.run(assessment+'-clone-checkout',['git','restore','--source=HEAD','--worktree','--','.'],clone)
            v.maven(assessment+'-clone-build',clone,['clean','-DskipTests','package'])
            v.assert_suite(v.maven(assessment+'-clone-public',clone,['test'],1),15,failures=9 if assessment=='01' else 8)
            tracked=subprocess_output(['git','ls-tree','-r','--name-only','HEAD'],target).splitlines()
            assert set(tracked)==set(p.read_json(v.ROOT/'pack-manifest.json')['starterArchives'][assessment]['sourceHashes'])
            assert subprocess_output(['git','rev-list','--count','HEAD'],target).strip()=='1'
            assert not subprocess_output(['git','status','--porcelain'],target).strip()
        p.write_json(v.EVIDENCE/'git-result.json',{'status':'PASS','commitsPerCandidate':1,'tag':'starter-v1','cleanCloneBuildAndPublicTests':True})
    else:raise ValueError(mode)

def subprocess_output(args,cwd):
    import subprocess
    return subprocess.check_output(args,cwd=cwd,env=v.ENV,text=True)

if __name__=='__main__':main(sys.argv[1])
