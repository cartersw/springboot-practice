# Incident Desk

[Problem statement](ASSESSMENT.md) | [API requirements](API_REFERENCE.md) | [Code map](ARCHITECTURE.md) | [Java/Spring reference](QUICK_REFERENCE.md)

**Time:** 60 minutes after setup. **Score:** 100 points.

## Software requirements

- **JDK 21** to build, run, and test. [Set up Java once](../../SETUP.md) if needed.
- **Maven 3.9.9** is downloaded by the included wrapper. The H2 database is included too.
- **Python 3.11+** is needed only for the optional scoring and fresh-attempt tools.

## Project commands

Open a terminal in **this folder**, beside `pom.xml` and `mvnw.cmd`. Run **Install** first and wait for `BUILD SUCCESS`. Then use **Run** to explore the API or **Test** to check your work.

| Action | Windows PowerShell | macOS / Linux |
|---|---|---|
| **Install** - download dependencies and build | `.\mvnw.cmd '-DskipTests' package` | `./mvnw -DskipTests package` |
| **Run** - start with sample data | `.\mvnw.cmd spring-boot:run '-Dspring-boot.run.profiles=demo'` | `./mvnw spring-boot:run -Dspring-boot.run.profiles=demo` |
| **Test** - run the public tests | `.\mvnw.cmd test` | `./mvnw test` |

Install skips tests. Before starting the timer, check startup with `.\mvnw.cmd '-Dtest=SmokeTest' test` (`./mvnw -Dtest=SmokeTest test` on macOS/Linux). Expect **2 passing tests**.

## Preview the API

After **Run** finishes starting the server, open:

- [Health check](http://localhost:8081/health)
- [Example GET request](http://localhost:8081/api/tickets)

Use `requests.http` with your editor's HTTP client, or Postman, for requests with a body. Use IDs returned by the app.

**Stop:** Ctrl+C in the running terminal. **Reload code changes:** stop and run again. Restarting resets the sample data. To run tests while the app is running, open a second terminal in this folder; tests do not need the server.

## Test results

Before you change any code, **Test** should report:

```text
Tests run: 17, Failures: 9, Errors: 0, Skipped: 0
BUILD FAILURE
```

This is the expected starting point: 2 startup checks and 6 scored tests pass; 9 scored tests fail. Your goal is **17 passing tests**.

To run one test in PowerShell:

```powershell
.\mvnw.cmd '-Dtest=TicketPublicContractTest#a1_05' test
```

Use `./mvnw` on macOS/Linux. Choose other test names from `public-tests.json`. Failure details are in `target/surefire-reports`.

## Full score

From the **pack root** (the folder containing `START_HERE.md`), run:

```powershell
python tools/practice.py grade 01
```

This checks 25 scored cases worth 4 points each: 15 public cases and 10 private variants. Startup checks are not scored. For a fresh attempt, use its printed `--attempt` command.

[Fresh attempts and grading](../../START_HERE.md#score-or-start-another-attempt) | [Setup and troubleshooting](../../SETUP.md#troubleshooting) | [macOS/Linux setup](../../START_HERE_MAC_LINUX.md)
