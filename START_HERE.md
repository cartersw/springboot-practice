# Spring Boot Practice

Choose a project, open its folder, and use **Install**, **Run**, and **Test** in its README.

## Software requirements

**JDK 21** is required. Maven and the database are supplied by the project. **Python 3.11+** is needed only for the scoring and fresh-attempt tools.

Already able to run `java -version` and `javac -version` with version 21? Continue below. Otherwise, follow [one-time Windows setup](SETUP.md) or [macOS/Linux setup](START_HERE_MAC_LINUX.md).

## Open a project

| Project | Practice | Suggested time | Instructions |
|---|---|---|---|
| 01 - Incident Desk | Ticket creation, updates, filtering, and sorting | 60 minutes | [Open README](candidate/01-incident-desk/README.md) |
| 02 - Parts Catalog | Search, pagination, and caching | 75 minutes | [Open README](candidate/02-cached-catalog/README.md) |
| 03 - Inventory Reservations | Stock, repeated requests, and cancellation | 90 minutes | [Open README](candidate/03-inventory-reservations/README.md) |

For your first attempt, open `candidate/01-incident-desk` in your editor. Open its terminal beside `pom.xml` and `mvnw.cmd`. If your terminal is currently in the folder containing this document, enter:

```powershell
cd candidate/01-incident-desk
```

Read `ASSESSMENT.md` for the problem. Use `API_REFERENCE.md` for exact requirements. Work inside the candidate folder to keep private tests and authoring materials out of your independent attempt.

## Install, Run, Test

From the selected project folder, use these Windows PowerShell commands. The project README also lists macOS/Linux commands.

**Install** - download dependencies and build the project without running tests:

```powershell
.\mvnw.cmd '-DskipTests' package
```

Wait for `BUILD SUCCESS`. The first run needs internet access. Check that the application can start before beginning the timer:

```powershell
.\mvnw.cmd '-Dtest=SmokeTest' test
```

Expect **2 passing tests**.

**Run** - start the API with sample data:

```powershell
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.profiles=demo'
```

The project README links to its local API. Keep this terminal open while exploring. Stop with Ctrl+C; restart after code changes. For tests, use a second terminal in the same project folder or stop the app first.

**Test** - check your work:

```powershell
.\mvnw.cmd test
```

The unchanged projects intentionally fail some tests:

| Project | Tests run | Pass | Fail | Errors | Skipped |
|---|---:|---:|---:|---:|---:|
| 01 | 17 | 8 | 9 | 0 | 0 |
| 02 | 17 | 9 | 8 | 0 | 0 |
| 03 | 17 | 9 | 8 | 0 | 0 |

`BUILD FAILURE` at this baseline is expected. Your target is **17 passing tests**. Compilation failures and failing startup checks are setup problems.

## Score or start another attempt

These optional tools use **Python 3.11+**. Open a terminal in the **pack root**, the folder containing this document and `tools`. From an original `candidate/01-incident-desk`, `02-cached-catalog`, or `03-inventory-reservations` folder, `cd ../..` returns there. From a fresh attempt, open the pack root directly.

| Action | Command from the pack root |
|---|---|
| Check prerequisites | `python tools/practice.py doctor` |
| Run project 01's public tests | `python tools/practice.py test 01` |
| Get project 01's full score | `python tools/practice.py grade 01` |
| Create another attempt | `python tools/practice.py new-attempt 01 --name second-try` |

Replace `01` with `02` or `03` for another project. On macOS/Linux, use `python3`. If your Windows Python command is `py -3.13`, use that instead of `python`.

Full grading checks **25 scored cases at 4 points each**, including 10 private variants of the published requirements. The 2 startup checks are not scored. Grading verifies protected files and uses pristine tests and build configuration in an isolated snapshot. The default report lists counts and failed IDs; `--details` reveals private failure details and may spoil practice. Private files remain locally accessible to the owner.

A fresh attempt preserves your existing work. Open the new folder and use the exact `--attempt` commands printed by the tool. Default grading commands target the original candidate folder.

Need help? See [setup and troubleshooting](SETUP.md).
