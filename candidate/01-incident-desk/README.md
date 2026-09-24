# Incident Desk API

Fix the app using the rules in [ASSESSMENT.md](ASSESSMENT.md).
Suggested practice time: **60 minutes**, starting after setup.

## Set up and practice - Windows PowerShell

1. **Prepare your terminal - main folder.**
   Follow `START_HERE.md` in the folder containing `candidate` and `tools`.

2. **Open this project - same terminal.**
   Enter this folder, or the folder printed when you created a fresh attempt.

   ```powershell
   cd candidate/01-incident-desk
   ```

3. **Read the task - your editor.**
   Read [ASSESSMENT.md](ASSESSMENT.md) for the requirements and allowed changes; [ARCHITECTURE.md](ARCHITECTURE.md) and [QUICK_REFERENCE.md](QUICK_REFERENCE.md) help you find things.

4. **Check your tools - project folder.**
   These commands show the Java and build-tool versions; both Java commands should report version 21.

   ```powershell
   java -version
   javac -version
   .\mvnw.cmd -v
   ```

5. **Build the app - project folder.**
   This checks that the code builds successfully without running the tests.

   ```powershell
   .\mvnw.cmd -B -ntp '-DskipTests' package
   ```

6. **Check that the app starts - project folder.**
   This runs two basic checks that the app starts and responds; both must pass.

   ```powershell
   .\mvnw.cmd -B -ntp '-Dtest=SmokeTest' test
   ```

7. **Work on the task and check progress - project folder.**
   Edit the allowed files in `src/main/java` and repeat this command to see which tests now pass.

   ```powershell
   .\mvnw.cmd -B -ntp test
   ```

   Before you make changes, expect **6 passing and 9 failing task tests**, plus **2 passing startup checks**.

## Get a score or start again - main folder

Return to the folder containing `START_HERE.md` before running these commands.

**Get your score:** runs the task tests plus additional checks of the same requirements and gives a score out of 100.

```powershell
python tools/practice.py grade 01
```

**Start again:** creates a fresh copy and keeps your existing work.

```powershell
python tools/practice.py new-attempt 01 --name second-try
```

Open the printed folder and use its printed test and grade commands, including `--attempt`, to check that copy.

## Other useful commands - project folder

```powershell
# Run just one test while working on a specific problem.
.\mvnw.cmd '-Dtest=TicketPublicContractTest#a1_05' test

# Run the tests without downloading anything; requires a previous successful download.
.\mvnw.cmd -o -B -ntp test

# Start the app with sample data so you can try requests yourself.
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.profiles=demo'
```

Open http://127.0.0.1:8081/health and try the examples in `requests.http`.
Stop the app with **Ctrl+C**; restarting clears its data.
The tests do not need this demo running.

## macOS/Linux

Follow `START_HERE_MAC_LINUX.md` in the main folder, then use `./mvnw` instead of `.\mvnw.cmd` and `python3` instead of `python`.
If you get `Permission denied`, run `chmod +x mvnw` in the project folder.

## If a command fails

- **Wrong Java version:** set `JAVA_HOME` to your JDK 21 folder and repeat Step 3 of `START_HERE.md`.
- **Download failed:** check your internet connection and rerun the command.
- **Address already in use:** stop the previous demo with Ctrl+C.
- **Files locked or access denied:** close the running app and retry, or create a fresh attempt.
- **Task tests fail:** use the failures to guide your fixes; leave the tests and build settings unchanged.
