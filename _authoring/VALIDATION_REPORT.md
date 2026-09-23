# Final verification report

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
