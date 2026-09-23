# Incident Desk API

This is an unsolved repair assessment. Read ASSESSMENT.md, then use ARCHITECTURE.md
and QUICK_REFERENCE.md as navigation aids. Suggested time: 60 minutes after setup.
Verified starter baseline: **6/15 public scored tests pass;
9/15 fail; 2/2 smoke checks pass**. Normal Maven test execution
discovers 17 methods and exits nonzero because behavior failures are deliberate.
Compilation and startup failures are not intended. Full grading adds 10 private
input variants of published rules, for 25 scored tests × 4 points = 100.

## Windows PowerShell (tested on this machine)

From the pack root, follow START_HERE.md to select JDK 21 and Python 3.11+.
Then open this candidate or fresh-attempt folder in the same PowerShell window:

```powershell
java -version
javac -version
.\mvnw.cmd -v
.\mvnw.cmd -B -ntp '-DskipTests' package
.\mvnw.cmd -B -ntp '-Dtest=SmokeTest' test
.\mvnw.cmd -B -ntp test
.\mvnw.cmd '-Dtest=TicketPublicContractTest#a1_05' test
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.profiles=demo'
```

`-DskipTests package` is setup/compilation only, not test verification.
The demo listens on http://127.0.0.1:8081. Stop with Ctrl+C. Tests use MockMvc
and do not need that port. In-memory data resets at application restart. Tests
seed their own fixtures independently of demo data. Use response IDs in requests.http.

## macOS/Linux (instructions supplied; not executed here)

Install JDK 21 and Python 3.11+ using official distributions, then:

```sh
java -version
javac -version
./mvnw -v
./mvnw -B -ntp -DskipTests package
./mvnw -B -ntp -Dtest=SmokeTest test
./mvnw -B -ntp test
./mvnw '-Dtest=TicketPublicContractTest#a1_05' test
./mvnw spring-boot:run -Dspring-boot.run.profiles=demo
```

If archive extraction loses executable permissions, run `chmod +x mvnw` or
use `sh ./mvnw test`. Use `python3` instead of `python` where appropriate.

## Grading and fresh attempts

From the pack root (the folder containing START_HERE.md; fresh attempts may be deeper):

```powershell
python tools/practice.py doctor
python tools/practice.py test 01
python tools/practice.py grade 01
python tools/practice.py new-attempt 01 --name second-try
```

The fresh-attempt command prints its new path and exact `--attempt` commands.
It preserves existing work. Default grading reports counts and failed IDs;
`--details` opts into private failure details and may spoil practice.
Private files remain locally accessible to the owner; this is not a secure exam.

## Setup recovery

- `JAVA_HOME` must point to the JDK 21 directory, not `bin`; check both `javac -version`
  and the Java version printed by the wrapper. Changes to these environment variables affect this shell only.
- First builds normally require network downloads. Retry a failed download after restoring
  network/proxy access. An offline run after warm-up is `.\mvnw.cmd -o -B -ntp test`
  (Unix: `./mvnw -o -B -ntp test`); expected assertions still fail.
- If a port is occupied, stop the previous demo process or select a different local port
  for manual exploration. Do not change the test resources.
- In a synced OneDrive directory, read-only/locked generated `target` folders may prevent
  `clean`. Close processes holding them or use a fresh attempt; the grader uses new snapshots.
- Public assertion failures at the documented baseline mean the starter is running.
  Do not edit the POM or tests to hide failures.

Optional JDK vendor downloads: https://adoptium.net/temurin/releases/?version=21
