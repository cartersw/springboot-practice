# Start after pulling the repo: macOS / Ubuntu

Use JDK 21 and Python 3.11+ to run the assessments.
Finish setup before starting the timer; some task tests will fail until you fix the app.

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
   Replace the path below. This is the **main folder**.

   ```sh
   cd "/path/to/spring-boot-practice"
   ```

3. **Check setup.** Run in the main folder.

   ```sh
   python3 tools/practice.py doctor
   ```

   Continue when it says `Prerequisites verified.` No separate Maven install.

4. **Build and test Assessment 1.** Start in the main folder.

   ```sh
   cd candidate/01-incident-desk
   # Allow the build command to run.
   chmod +x mvnw
   # Show the Java and build-tool versions.
   ./mvnw -v
   # Build the app without running tests.
   ./mvnw -B -ntp -DskipTests package
   # Check that the app starts and responds.
   ./mvnw -B -ntp -Dtest=SmokeTest test
   # Run the task tests to see what needs fixing.
   ./mvnw -B -ntp test
   # Return to the main folder.
   cd ../..
   ```

   To try the app yourself with sample data, follow the demo command in its README.

   Before any changes: **2 startup checks pass; 6 task tests pass and 9 fail.**

5. **Start working.** Open `candidate/01-incident-desk` in your editor.
   Read `README.md`, then `ASSESSMENT.md`, then edit its application code. Repeat step 4 to test.

6. **Get your score.** Run in the main folder.

   ```sh
   python3 tools/practice.py grade 01
   ```

7. **Start fresh when needed.** Run in the main folder.

   ```sh
   python3 tools/practice.py new-attempt 01 --name retry
   ```

   Open the folder it prints. Run its printed test/grade commands from the
   main folder, replacing `python` with `python3`. Keep the `--attempt` path.

For the next assessments, replace `01` and its folder:

| Assessment | Folder | Task tests before changes | Startup checks |
|---|---|---|---|
| 02 | `candidate/02-cached-catalog` | 7 pass, 8 fail | 2 pass |
| 03 | `candidate/03-inventory-reservations` | 7 pass, 8 fail | 2 pass |
