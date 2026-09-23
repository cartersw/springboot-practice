import copy
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile
import practice as p

def manifest():
    tests=[dict(id=f'A1-{i:02}',className='example.PublicTest' if i<=15 else 'example.PrivateTest',methodName=f'a1_{i:02}',points=4,visibility='public' if i<=15 else 'private') for i in range(1,26)]
    tests += [dict(id='SMOKE-'+n,className='example.SmokeTest',methodName=n,points=0,visibility='public') for n in ('contextStarts','healthResponds')]
    return dict(schemaVersion=1,maxPoints=100,expectedScoredTests=25,expectedSmokeTests=2,tests=tests)

class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='practice tool tests ')
        self.root=Path(self.tmp.name);self.m=manifest();self.reports=self.root/'new run/reports';self.reports.mkdir(parents=True)
    def tearDown(self):self.tmp.cleanup()
    def xml(self,changes=None,nested=False,entries=None):
        changes=changes or {};outer=ET.Element('testsuites' if nested else 'testsuite');suite=ET.SubElement(outer,'testsuite') if nested else outer
        for entry in entries if entries is not None else self.m['tests']:
            node=ET.SubElement(suite,'testcase',classname=entry['className'],name=entry['methodName'])
            if entry['id'] in changes:ET.SubElement(node,changes[entry['id']],message='test detail').text='private content'
        ET.ElementTree(outer).write(self.reports/'TEST-suite.xml',encoding='utf-8')
    def evaluate(self,exit_code=0):return p.evaluate(self.reports,self.m,exit_code)
    def archive(self,names=None):
        archive=self.root/'starter.zip'
        with zipfile.ZipFile(archive,'w') as z:
            for name,body in (names or {'mvnw':'script','src/main/java/App.java':'starter','assessment.json':'{"id":"01"}'}).items():z.writestr(name,body)
        return archive
    def test_all_pass(self):self.xml();self.assertEqual(self.evaluate()['score'],100)
    def test_fixed_weight_mixture(self):self.xml({'A1-01':'failure','A1-16':'error'});r=self.evaluate(1);self.assertEqual((r['score'],r['publicPassed'],r['privatePassed']),(92,14,9))
    def test_smoke_failure(self):self.xml({'SMOKE-healthResponds':'failure'});self.assertEqual(self.evaluate(1)['status'],'APPLICATION_NOT_READY')
    def test_smoke_context_error(self):self.xml({'SMOKE-contextStarts':'error'});self.assertIsNone(self.evaluate(1)['score'])
    def test_skipped_invalid(self):self.xml({'A1-01':'skipped'});self.assertEqual(self.evaluate()['status'],'INCOMPLETE_TEST_RUN')
    def test_missing_invalid(self):self.xml(entries=self.m['tests'][1:]);self.assertIsNone(self.evaluate()['score'])
    def test_duplicate_invalid(self):self.xml(entries=self.m['tests']+[self.m['tests'][0]]);self.assertIsNone(self.evaluate()['score'])
    def test_unexpected_invalid(self):self.xml(entries=self.m['tests']+[dict(className='Other',methodName='other',id='other')]);self.assertIsNone(self.evaluate()['score'])
    def test_no_reports(self):self.assertEqual(self.evaluate(1)['status'],'BUILD_ERROR')
    def test_malformed_xml_path(self):path=self.reports/'TEST-bad.xml';path.write_text('<bad');self.assertIn(str(path),self.evaluate()['diagnostic'])
    def test_manifest_wrong_totals(self):self.m['maxPoints']=96;self.assertRaises(p.PracticeError,self.evaluate)
    def test_manifest_duplicate_id(self):self.m['tests'][1]['id']='A1-01';self.assertRaises(p.PracticeError,self.evaluate)
    def test_manifest_wrong_visibility_counts(self):self.m['tests'][0]['visibility']='private';self.assertRaises(p.PracticeError,self.evaluate)
    def test_manifest_wrong_smoke_identity(self):self.m['tests'][-1]['methodName']='otherSmoke';self.assertRaises(p.PracticeError,self.evaluate)
    def test_manifest_private_smoke(self):self.m['tests'][-1]['visibility']='private';self.assertRaises(p.PracticeError,self.evaluate)
    def test_manifest_unsupported_schema(self):self.m['schemaVersion']=2;self.assertRaises(p.PracticeError,self.evaluate)
    def test_nonzero_exit_all_pass(self):self.xml();self.assertEqual(self.evaluate(1)['status'],'BUILD_ERROR')
    def test_zero_exit_with_failure(self):self.xml({'A1-01':'failure'});self.assertEqual(self.evaluate()['status'],'BUILD_ERROR')
    def test_old_reports_ignored(self):self.xml();self.reports.rename(self.root/'old reports');self.reports.mkdir();self.assertIsNone(self.evaluate(1)['score'])
    def test_nested_xml(self):self.xml(nested=True);self.assertEqual(self.evaluate()['score'],100)
    def test_per_class_xml(self):
        for cls in {t['className'] for t in self.m['tests']}:
            self.xml(entries=[t for t in self.m['tests'] if t['className']==cls]);(self.reports/'TEST-suite.xml').rename(self.reports/f'TEST-{cls}.xml')
        self.assertEqual(self.evaluate()['score'],100)
    def test_protected_changes_preserved(self):
        f=self.root/'pom.xml';f.write_text('original');expected={'pom.xml':p.digest(f)};f.write_text('changed');self.assertRaises(p.PracticeError,p.verify_files,self.root,expected);self.assertEqual(f.read_text(),'changed')
    def test_missing_protected(self):self.assertRaises(p.PracticeError,p.verify_files,self.root,{'pom.xml':'none'})
    def test_added_protected_test_rejected(self):
        f=self.root/'src/test/ExtraTest.java';f.parent.mkdir(parents=True);f.write_text('extra');self.assertRaises(p.PracticeError,p.verify_protected,self.root,{'protectedFiles':{},'protectedTrees':['src/test']});self.assertEqual(f.read_text(),'extra')
    def test_added_maven_config_rejected(self):
        f=self.root/'.mvn/maven.config';f.parent.mkdir();f.write_text('-DskipTests');self.assertRaises(p.PracticeError,p.verify_protected,self.root,{'protectedFiles':{},'protectedTrees':[]})
    def test_snapshot_candidate_source(self):
        target=self.root/'candidate';base=self.root/'author'
        for file,body in [(target/'src/main/java/App.java','candidate'),(target/'src/test/java/FakeTest.java','untrusted'),(target/'target/surefire-reports/TEST-old.xml','stale'),(base/'reference/src/main/java/App.java','reference'),(base/'trusted-build/pom.xml','trusted pom'),(base/'trusted-tests/src/test/java/FullTest.java','trusted test')]:file.parent.mkdir(parents=True,exist_ok=True);file.write_text(body)
        dest=self.root/'new snapshot';p.snapshot(target,dest,base)
        self.assertEqual((dest/'src/main/java/App.java').read_text(),'candidate');self.assertEqual((dest/'pom.xml').read_text(),'trusted pom');self.assertFalse((dest/'target').exists());self.assertFalse((dest/'src/test/java/FakeTest.java').exists())
    def test_snapshot_existing_destination(self):self.assertRaises(p.PracticeError,p.snapshot,self.root,self.root,self.root)
    def test_attempt_id_mismatch(self):
        dest=self.root/'attempts/a';dest.mkdir(parents=True);(dest/'assessment.json').write_text('{"id":"02"}');self.assertRaises(p.PracticeError,p.select_target,'01','attempts/a',self.root)
    def test_attempt_path_escape(self):self.assertRaises(p.PracticeError,p.select_target,'01','../outside',self.root)
    def test_unknown_assessment(self):self.assertRaises(p.PracticeError,p.select_target,'99',None,self.root)
    def test_attempt_symlink_escape(self):
        external=self.root/'outside';external.mkdir();(external/'assessment.json').write_text('{"id":"01"}');attempts=self.root/'attempts';attempts.mkdir();link=attempts/'link'
        try:link.symlink_to(external,target_is_directory=True)
        except OSError:
            # Still exercise resolved-link rejection when OS disallows link creation.
            original=Path.resolve
            def resolve(path,*a,**kw):return external if path==link else original(path,*a,**kw)
            with patch.object(Path,'resolve',resolve):self.assertRaises(p.PracticeError,p.select_target,'01',str(link),self.root)
        else:self.assertRaises(p.PracticeError,p.select_target,'01',str(link),self.root)
    def test_zip_traversal(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'../escape':'x'}),self.root/'extract')
    def test_zip_absolute(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'/escape':'x'}),self.root/'extract')
    def test_zip_windows_drive(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'C:/escape':'x'}),self.root/'extract')
    def test_zip_backslash(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'..\\escape':'x'}),self.root/'extract')
    def test_zip_symlink(self):
        a=self.root/'link.zip'
        with zipfile.ZipFile(a,'w') as z:
            i=zipfile.ZipInfo('link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,'../escape')
        self.assertRaises(p.PracticeError,p.extract_archive,a,self.root/'extract')
    def test_zip_case_collision(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'App.java':'x','app.java':'y'}),self.root/'extract')
    def test_zip_existing_destination(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive(),self.root)
    def test_zip_private_rejected(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'src/test/ThingPrivateContractTest.java':'x'}),self.root/'extract')
    def test_zip_authoring_rejected(self):self.assertRaises(p.PracticeError,p.extract_archive,self.archive({'_authoring/reference':'x'}),self.root/'extract')
    def test_zip_paths_with_spaces(self):
        dest=self.root/'fresh attempt with spaces';p.extract_archive(self.archive(),dest);self.assertEqual((dest/'src/main/java/App.java').read_text(),'starter');self.assertEqual(set(p.hashes(dest)),{'mvnw','src/main/java/App.java','assessment.json'})
    def test_fresh_attempt_collision_safe(self):
        a=self.archive();entry={'path':a.name,'sha256':p.digest(a),'sourceHashes':{}}
        (self.root/'pack-manifest.json').write_text(json.dumps({'starterArchives':{'01':entry}}))
        first=p.new_attempt('01','same',self.root);second=p.new_attempt('01','same',self.root);self.assertNotEqual(first,second);self.assertTrue(first.exists());self.assertTrue(second.exists())
    def test_bad_attempt_name(self):self.assertRaises(p.PracticeError,p.new_attempt,'01','../bad',self.root)

if __name__=='__main__':unittest.main()
