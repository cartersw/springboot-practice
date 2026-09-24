# macOS / Linux Setup

Install JDK 21 once, then use the **Install**, **Run**, and **Test** commands in each project's README. Maven and the H2 database are supplied by the project.

## Check your tools

```sh
java -version
javac -version
```

If both report **21.x**, skip installation and [open a project](#open-a-project).

## Install JDK 21

### macOS

With [Homebrew](https://brew.sh/) installed:

```sh
brew install --cask temurin@21
```

Select Java 21 in your current terminal:

```sh
export JAVA_HOME="$(/usr/libexec/java_home -v 21)"
export PATH="$JAVA_HOME/bin:$PATH"
```

To keep this selection in future terminals, add those two `export` lines once to your shell's startup file (`~/.zprofile` for the default macOS login shell). Reopen the terminal and check both version commands.

Source: [Homebrew's Temurin 21 package](https://formulae.brew.sh/cask/temurin%4021).

### Ubuntu 24.04

```sh
sudo apt update
sudo apt install openjdk-21-jdk curl
```

Select Java 21 in your current terminal:

```sh
export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-$(dpkg --print-architecture)"
export PATH="$JAVA_HOME/bin:$PATH"
```

To keep this selection in future Bash terminals, add those two `export` lines once to `~/.bashrc`. Reopen the terminal and check both version commands.

Source: [Ubuntu's supported Java versions](https://documentation.ubuntu.com/ubuntu-for-developers/reference/availability/java/).

## Open a project

Open `candidate/01-incident-desk` in your editor, then open a terminal in that folder, beside `pom.xml` and `mvnw`. Read `ASSESSMENT.md` for the problem.

| Action | Command from the project folder |
|---|---|
| **Install** | `./mvnw -DskipTests package` |
| **Run** | `./mvnw spring-boot:run -Dspring-boot.run.profiles=demo` |
| **Test** | `./mvnw test` |

Run Install first and wait for `BUILD SUCCESS`. Before starting the timer, run `./mvnw -Dtest=SmokeTest test`; both startup checks should pass.

If the wrapper says `Permission denied`, run `chmod +x mvnw` once or use `sh ./mvnw` in place of `./mvnw`.

Project 01 runs at `http://localhost:8081`. Stop it with Ctrl+C. Use a second terminal in the same folder to run tests while it is running. The project README has preview links and expected test results. Projects 02 and 03 use ports 8082 and 8083.

## Optional: Python for scoring and fresh attempts

These tools require Python 3.11 or later. Check `python3 --version` first.

**macOS with Homebrew:**

```sh
brew install python@3.13
export PATH="$(brew --prefix python@3.13)/libexec/bin:$PATH"
```

Add that `export` line to your shell's startup file if you want this version selected in future terminals.

**Ubuntu 24.04:**

```sh
sudo apt install python3
```

From the **pack root**, the folder containing `START_HERE.md`, run:

```sh
python3 tools/practice.py doctor
```

Expect `Prerequisites verified.` Use `python3` for the commands under [scoring and fresh attempts](START_HERE.md#score-or-start-another-attempt), including the printed `--attempt` commands for a fresh attempt.

Native macOS/Linux execution has not been tested for this pack. See [troubleshooting](SETUP.md#troubleshooting) for common issues.
