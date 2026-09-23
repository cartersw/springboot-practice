"""Publish a report only after checking the recorded execution gates."""
from pathlib import Path
import json
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import practice as p
E=ROOT/'_authoring/verification'
for name in ('static-audit','git-result','bash-result','portable-result'):
    assert p.read_json(E/(name+'.json'))['status']=='PASS',name
assert 'Ran 43 tests' in (E/'utility-tests.log').read_text()
assert p.read_json(E/'doctor.json')['exitCode']==0
assert p.read_json(E/'start-here-setup.json')['exitCode']==0
assert p.read_json(E/'test-quality-regressions.json')['alternateCanonicalEncoding']=='27/27 passed'
assert p.read_json(E/'tooling-errors.json')['compileFailure']=='BUILD_ERROR / exit 2 / score null'
assessments={}
for aid,slug in p.SLUGS.items():
    ref=p.read_json(E/(aid+'-reference.json'))
    assert len(ref['tests'])==27 and all(t['result']=='passed' for t in ref['tests'])
    for seed in (1701,92837):
        assert p.read_json(E/(aid+f'-random-{seed}.json'))['exitCode']==0
    final=p.read_json(E/(aid+'-final-public.json'))
    assert len(final['tests'])==17 and all(t['result'] in ('passed','failure') for t in final['tests'])
    passing=sum(t['result']=='passed' and 'PublicContractTest' in t['class'] for t in final['tests'])
    assert passing==(6 if aid=='01' else 7)
    assert p.read_json(E/(aid+'-gates.json'))['status']=='PASS'
    assert p.read_json(E/(aid+'-mutations.json'))['status']=='PASS'
    assert p.read_json(E/('candidate-'+aid+'-startup.json'))['status']=='PASS'
    assert p.read_json(E/('reference-'+aid+'-startup.json'))['status']=='PASS'
    candidate=ROOT/'candidate'/slug
    p.verify_files(candidate,p.read_json(ROOT/'pack-manifest.json')['starterArchives'][aid]['sourceHashes'])
    p.verify_protected(candidate,p.load_manifest(aid)[0])
    assessments[aid]={'status':'STARTER_VERIFIED','referenceVisible':15,'referencePrivate':10,'smoke':2,'starterVisiblePassed':passing,'starterVisibleFailed':15-passing,'starterScore':40 if aid=='01' else 36,'mutationsDetected':7 if aid!='03' else 8,'unsolved':True,'instructionsVerified':True}
now=p.utc()
report='''# Final verification report

**Overall: PASS on Windows 11, JDK 21.** Verified on 2026-09-23. The Unix wrapper
was also executed under Git Bash on Windows. Native macOS/Linux is unverified.

| Assessment | Clean build | Startup | Reference visible | Reference private | Smoke | Starter visible passing / failing | Unsolved | Instructions |
|---|---|---|---|---|---|---|---|---|
| 1: Incident Desk | PASS | PASS | 15/15 | 10/10 | 2/2 | 6 / 9 | YES | YES |
| 2: Cached Catalog | PASS | PASS | 15/15 | 10/10 | 2/2 | 7 / 8 | YES | YES |
| 3: Inventory Reservations | PASS | PASS | 15/15 | 10/10 | 2/2 | 7 / 8 | YES | YES |

## Workspace tooling

| Check | Result |
|---|---|
| Fresh-attempt generation and archive replay | PASS; existing attempts preserved |
| Grader | PASS; references 100/100 each; starters 40/100, 36/100, 36/100 |
| Solution isolation | PASS; no solution code or history in candidate repositories |
| Hidden-test isolation | PASS; candidate tests and archives contain only visible tests and smoke checks |
| Maven Wrapper | PASS; mvnw.cmd and ./mvnw, including paths with spaces |
| Utility tests | 43/43 passed |
| Clean Git clones | PASS; one unsolved commit and starter-v1 tag per candidate |
| Offline tests after dependency warm-up | PASS; only expected starter assertion failures |
| Test isolation | PASS; references passed default order and random seeds 1701 and 92837 |

All 22 prescribed defects were tested independently: each is detected and still
passes both smoke checks. Their combined source changes exactly reproduce the
candidate application source. No unintended application defect was found.
Candidate application code and runtime configuration are byte-for-byte unchanged
from the original unsolved starters. Demo startup used real HTTP and H2, including
successful and error requests. All verification servers were stopped.

## Defects corrected and maintenance completed

1. Removed README commands for an environment script absent from the portable
   pack. Added directly executable PowerShell setup, with restored local tools in
   this workspace and official installation guidance for exports. No global
   environment, Git, or execution-policy settings were changed.
2. Completed the entry-point instructions: read README before ASSESSMENT, compile
   before the timer, distinguish expected failures, launch the demo, and use the
   pack root correctly when working in a deeper fresh-attempt folder.
3. Corrected copied error examples in Assessments 2 and 3 and removed residual
   instructions addressed to the assessment builder.
4. Tightened JSON assertions to reject wrong primitive types and objects where
   arrays are required. A separate invalid JSON-ID implementation was executed
   and correctly rejected by the scored tests.
5. Removed reservation test assumptions about the internal request encoding.
   Equivalent replay is checked through the documented workflow. A separate
   reference using a different encoding passed all 27 tests.
6. Hardened manifest validation for the 15-visible/10-private split, named smoke
   tests, and smoke visibility. Added three regression tests. Ungradable reports
   now identify their build log; actual compilation and smoke failures return
   exit 2 and no score. Protected edits are rejected without changing source.
7. Preserved Unix executable permissions for mvnw in regenerated starter and
   portable ZIPs; refreshed every affected archive and integrity hash.
8. Restored the author-only references, explanations and mutation records omitted
   by the incoming portable export. Rebuilt current verification records and
   corrected author evidence links. Portable exports still omit solutions/tools.
9. Restored starter-only Git repositories omitted by ZIP transfer. Verified clean
   clones, using repository-local long-path support for deeply nested Windows
   paths. Preserved the previous candidate copies in author-only evidence.

## Remaining limits

- Native macOS/Linux execution and installing prerequisites on a completely clean
  operating system were not performed. Git Bash execution is not a substitute
  for those platform checks.
- Dependencies were already cached; this verifies clean source builds and
  offline reuse, not downloading every dependency into an empty cache again.
- Initial sandbox runs hit Java filesystem access errors. The same builds passed
  with normal user permissions. Git long-path support was scoped to verification
  clones/repositories; no global settings were changed.
- Private material is excluded from ordinary practice, not access-controlled
  against the owner of the local workspace.

Assessment 1 is ready. Follow [START_HERE.md](START_HERE.md). The final candidate
folders are unsolved, and normal public tests end with the expected failures.
'''
(ROOT/'VERIFICATION_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
author=report+'''
## Author evidence and contract review

Actual logs and JSON execution records are under `verification/`. Each command
record includes command, cwd, start/end times, exit code and observed test cases.
Surefire XML is retained in the executed reference/mutation/clone/snapshot folders.
`verification/initial-candidate-hashes.json` records the incoming candidate bytes;
`verification/static-audit.json` records the final source/isolation comparison.

| Assessment | Reference compiled | Reference scored /25 | Smoke /2 | Starter public /15 | Starter full /25 | Individual mutations detected | Archive replay | Grader |
|---|---|---|---|---|---|---|---|---|
| 01 | PASS | 25 | 2 | 6 | 10 | 7/7 | PASS | PASS |
| 02 | PASS | 25 | 2 | 7 | 9 | 7/7 | PASS | PASS |
| 03 | PASS | 25 | 2 | 7 | 9 | 8/8 | PASS | PASS |

Key record patterns: `01-reference.json`, `01-random-1701.json`,
`01-random-92837.json`, `01-candidate-build.json`, `candidate-01-startup.json`,
`reference-01-startup.json`, `reference-01-default-startup.json`,
`01-candidate-grade.log`, `01-reference-grade.log`, `01-fresh-*.json`,
`01-bash-*.json`, `01-clone-*.json`, and `01-final-public.json`; repeat for 02/03.
Every individual mutation has `A1-D01.json` etc., with its observed failing IDs
indexed by `01-mutations.json` etc. Grader snapshots and private XML are in `.runs`
at the pack root. Candidate-safe report summaries are in `reports`.

Reviewed all 75 scored methods, smoke helpers, configuration and fixtures against
the full specification and candidate instructions. HTTP codes and JSON envelopes,
normalization, boundary validation, filtering, stable sorting, pagination totals,
cache identity/invalidation/expiry, committed persistence, cancellation, replay,
and rollback are covered by the published contracts. Independent fixture resets
use JDBC; tests have no enclosing transaction. Clock/cache/probe/audit controls
reset between methods. No timing sleeps, network services, exact generated IDs,
test-order dependencies, or hidden business rules were found.

Contract fairness adjustment: A3-02 now observes public persisted fields rather
than requiring one canonical serialization. A3-25 creates and cancels through the
API before checking cancelled replay, removing its dependency on a fixture's
specific internal encoding. It still asserts replay status, identity, quantities,
audit counts, availability independence and no database changes. The 25 scored
test identities remain unchanged. `test-quality-regressions.json` proves the
alternate encoding passes while `string-id-regression.json` proves wrong JSON
types fail. A1-24 now explicitly requires empty arrays, not merely empty nodes.

All spoiler-search occurrences in candidate materials were reviewed: practice
assistance notices, public behavior descriptions, generic debug guidance, and
official wrapper credential-variable support are appropriate. No repair comments,
solution fragments, private payloads, mutation descriptions or answer keys occur
in candidate source, archives or their single-commit Git history.

Verification harness retries are retained. The initial compiler/clean failures
were sandbox AccessDenied errors; normal-user runs pass. Standalone mutation
patches are relative to the reference, so their overlapping context is not
stacked; verified changed lines were composed and compared exactly to starters.
CMD's quoted MAVEN_OPTS was adjusted at the Git Bash test boundary. An initial
deep Git clone required repository-local core.longpaths=true. These harness/setup
issues did not require changing assessment application code or expected outcomes.
'''
(ROOT/'_authoring/VALIDATION_REPORT.md').write_text(author,encoding='utf-8',newline='\n')
for slug in p.SLUGS.values():
    file=ROOT/'_authoring'/slug/'SOLUTION.md'
    text=file.read_text(encoding='utf-8')
    text=re.sub(r'`evidence/(a[123]-d\d\d)`',lambda m:'`../verification/'+m.group(1).upper()+'.json`',text)
    file.write_text(text,encoding='utf-8',newline='\n')
state={'status':'VERIFIED','phase':'FINAL_VERIFICATION_COMPLETE','completedAt':now,'assessments':assessments,'nextAction':'Begin Assessment 1 using START_HERE.md; leave candidate source unsolved.','evidence':'_authoring/verification','report':'VERIFICATION_REPORT.md','platform':'Windows 11 AMD64; Git Bash for Unix wrapper','nativeMacLinuxVerified':False,'utilityTests':43}
p.write_json(ROOT/'_authoring/build-state.json',state)
(ROOT/'_authoring/BUILD_STATE.md').write_text('# Final verification complete\n\nPASS. All three references: 27/27; starters: 6/15, 7/15, 7/15 visible; all smoke checks pass. All 22 individual mutations detected.\n\nRead VALIDATION_REPORT.md and verification/*.json for current evidence. Candidate applications remain byte-identical to original unsolved source. No unfinished verification gate on Windows. Native macOS/Linux and clean-OS installation unverified.\n',encoding='utf-8')
(ROOT/'_authoring/VERSION_LOCK.md').write_text('''# Executed version lock

Verified 2026-09-23 on Windows 11 AMD64.

- Eclipse Temurin JDK / javac 21.0.12.1; compile release 21, no previews.
- Spring Boot 3.5.16. No version substitution or SNAPSHOT dependency.
- Maven 3.9.9 through official wrapper 3.3.4 (only-script).
- Compiler plugin 3.14.1, Surefire 3.5.6, H2 2.3.232 (Boot-managed).
- Python 3.13.7, standard library only for tooling; minimum 3.11.
- Git 2.54.0.windows.1; Unix wrapper executed through Git Bash.

Tool binaries and dependency caches were restored from the original parent pack
into _authoring/toolchain. No global Maven or external runtime services required.
Exact output: verification/doctor.log, start-here-setup.log and *-reference.log.
Normal-user runs pass; sandbox Java filesystem access errors are recorded in
verification/01-clean-diagnostic.log. No global settings were changed.
''',encoding='utf-8')
pack=p.read_json(ROOT/'pack-manifest.json');pack['status']='VERIFIED';pack['lastVerifiedAt']=now
p.write_json(ROOT/'pack-manifest.json',pack)
print('Published PASS report after checking all execution gates.')
