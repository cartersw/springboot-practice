# Start after pulling the repo: macOS / Ubuntu

Open one candidate folder and read README.md, then ASSESSMENT.md. Finish setup
and smoke checks before timing your attempt. The three independent exercises
progress from REST (60 minutes), to catalog queries/cache (75 minutes), to
reservations (90 minutes). Behavior failures are deliberate; startup/build failures
are not the exercise. Solutions and private variants of the published rules stay
outside candidate folders; avoid authoring files during practice.

1. **Install tools.** Run the block for your OS in Terminal, from any folder.

   **macOS:** If Homebrew is missing, install it from [brew.sh](https://brew.sh/)
   and follow its printed PATH instructions first.

   ```sh
   brew install --cask temurin@21
   brew install python@3.13
   export JAVA_HOME="$(/usr/libexec/java_home -v 21)"
   export PATH="$JAVA_HOME/bin:$(brew --prefix python@3.13)/libexec/bin:$PATH"
   ```

   **Ubuntu 24.04:**

   ```sh
   sudo apt update
   sudo apt install openjdk-21-jdk python3 curl
   export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-$(dpkg --print-architecture)"
   export PATH="$JAVA_HOME/bin:$PATH"
   ```

2. **In that Terminal, enter the folder containing `START_HERE.md`.**
   Replace the path below. This is the **project folder**.

   ```sh
   cd "/path/to/spring-boot-practice"
   ```

3. **Check setup.** Run in the project folder.

   ```sh
   python3 tools/practice.py doctor
   ```

   Continue when it says `Prerequisites verified.` No separate Maven install.

4. **Run the first assessment's tests.** Start in the project folder.

   ```sh
   cd candidate/01-incident-desk
   chmod +x mvnw
   ./mvnw -v
   ./mvnw -B -ntp -DskipTests package
   ./mvnw -B -ntp -Dtest=SmokeTest test
   ./mvnw -B -ntp test
   cd ../..
   ```

   Packaging with `-DskipTests` is setup only. If executable permissions are lost,
   use `sh ./mvnw` in place of `./mvnw`. The README includes demo startup commands.

   Expected: **2 smoke passes; 6 public passes and 9 public failures.**

5. **Start working.** Open `candidate/01-incident-desk` in your editor.
   Read `README.md`, then `ASSESSMENT.md`, then edit its application code. Repeat step 4 to test.

6. **Get your score.** Run in the project folder.

   ```sh
   python3 tools/practice.py grade 01
   ```

7. **Start fresh when needed.** Run in the project folder.

   ```sh
   python3 tools/practice.py new-attempt 01 --name retry
   ```

   Open the folder it prints. Run its printed test/grade commands from the
   project folder, replacing `python` with `python3`. Keep the `--attempt` path.

For the next assessments, replace `01` and its folder:

| Assessment | Folder | Expected public tests | Smoke |
|---|---|---|---|
| 02 | `candidate/02-cached-catalog` | 7 pass, 8 fail | 2 pass |
| 03 | `candidate/03-inventory-reservations` | 7 pass, 8 fail | 2 pass |

macOS/Linux execution has not been tested by the builder.
