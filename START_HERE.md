# Start here - Windows PowerShell

1. **Open PowerShell - pack root.**
   Open a terminal in the folder containing this file, `candidate`, and `tools`.

2. **Install prerequisites - new machines only.**
   Install Git, [JDK 21](https://adoptium.net/temurin/releases/?version=21) with `JAVA_HOME` and `bin` on PATH, and [Python 3.11+](https://docs.python.org/3/using/windows.html) on PATH, then reopen PowerShell.

3. **Check setup - pack root, each new terminal.**
   This selects bundled tools when present and must finish with `Prerequisites verified.`

   ```powershell
   $practiceTools = Join-Path (Get-Location) '_authoring/toolchain'
   if (Test-Path -LiteralPath $practiceTools) {
       $env:JAVA_HOME = (Get-ChildItem -LiteralPath $practiceTools -Directory -Filter 'jdk-*' | Select-Object -First 1).FullName
       $env:PATH = "$practiceTools/python;$env:JAVA_HOME/bin;$env:PATH"
       $env:MAVEN_USER_HOME = Join-Path $practiceTools 'maven-home'
       $practiceRepository = Join-Path $practiceTools 'repository'
       $env:MAVEN_OPTS = '-Dmaven.repo.local="' + $practiceRepository + '"'
   }
   python tools/practice.py doctor
   ```

4. **Choose an assessment - open its folder in your editor.**
   Read `README.md`, then `ASSESSMENT.md`; the commands below use `01`, so substitute the ID and folder for other assessments.

   | ID | Folder | Time | Starter public tests |
   |---|---|---|---|
   | 01 | `candidate/01-incident-desk` | 60 min | 6 pass, 9 fail |
   | 02 | `candidate/02-cached-catalog` | 75 min | 7 pass, 8 fail |
   | 03 | `candidate/03-inventory-reservations` | 90 min | 7 pass, 8 fail |

5. **Build and check startup - start at pack root.**
   Packaging must succeed and both smoke tests must pass before you start the timer.

   ```powershell
   cd candidate/01-incident-desk
   .\mvnw.cmd -B -ntp '-DskipTests' package
   .\mvnw.cmd -B -ntp '-Dtest=SmokeTest' test
   cd ../..
   ```

6. **Practice - edit the assessment's `src/main/java`; run tests at pack root.**
   Make the permitted source changes and repeat this command; starter behavior failures are expected.

   ```powershell
   python tools/practice.py test 01
   ```

7. **Get your score - pack root.**
   This runs full grading and saves results in `reports/`.

   ```powershell
   python tools/practice.py grade 01
   ```

8. **Start fresh, optional - pack root.**
   Open the printed attempt folder and use its printed test/grade commands, including `--attempt`.

   ```powershell
   python tools/practice.py new-attempt 01 --name retry
   ```

