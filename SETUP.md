# One-time Windows Setup

Set up Java once for your Windows account. After that, every project can use it from a new terminal.

## 1. Check Java

Open PowerShell and run:

```powershell
java -version
javac -version
```

Both should report **21.x**. If they do, continue to [open a project](START_HERE.md#open-a-project). If a command is missing or reports another version, use the steps below.

## 2. Install or select JDK 21

If JDK 21 is not installed, download **Temurin 21, JDK, Windows** from [Adoptium](https://adoptium.net/temurin/releases/?version=21). In the MSI installer's Custom Setup, enable **Add to PATH** and **Set JAVA_HOME**. These options are described in the [official installer instructions](https://adoptium.net/installation/windows).

If JDK 21 is already installed, configure it once:

1. Find its installation folder. Common locations are `C:\Program Files\Eclipse Adoptium` and `%LOCALAPPDATA%\Programs\Eclipse Adoptium`. Select the `jdk-21...` folder containing `bin\java.exe` and `bin\javac.exe`.
2. Open Start and search for **Edit environment variables for your account**.
3. Under **User variables**, create or edit `JAVA_HOME`. Set its value to the full JDK folder path, without quotes and without `\bin` at the end.
4. Edit the user `Path`, click **New**, and add `%JAVA_HOME%\bin`. Keep the existing entries.
5. Save, close your terminal and editor, then reopen them. Run the two version commands again.

You do not need to paste `$env:JAVA_HOME` commands into each project. Changes made through Windows Environment Variables persist for future terminals. If Java still selects another version, check `where.exe java` and correct the earlier Java entry on your `Path`.

## 3. Optional: set up the scoring tools

Building, running, and testing the Java projects works without Python. Full scoring, prerequisite checks, and creating fresh attempts require **Python 3.11 or later**.

Check your Python command:

```powershell
python --version
```

If needed, install a supported version using [Python's Windows instructions](https://docs.python.org/3/using/windows.html). Reopen the terminal and check again. If your installation uses a command such as `py -3.13`, use that command wherever the practice instructions say `python`.

From the **pack root** (the folder containing `START_HERE.md`), run:

```powershell
python tools/practice.py doctor
```

Expect `Prerequisites verified.` The first wrapper check may download Maven.

Return to [START_HERE.md](START_HERE.md) and open a project.

## Troubleshooting

| What you see | What to do |
|---|---|
| `java` or `javac` is not recognized | Follow step 2, then restart your terminal and editor. |
| Maven uses a different Java version | Check `JAVA_HOME`, then run `.\mvnw.cmd -v` from the project folder. It must show Java 21. |
| `mvnw.cmd` is not found | Open the folder containing `pom.xml` and `mvnw.cmd`. The command is `.\mvnw.cmd`, with no backslash before `.cmd`. |
| A dependency download fails | Restore network/proxy access and rerun Install. |
| The browser cannot connect | Keep Run active and wait for the server to finish starting. Use your project's port: 8081, 8082, or 8083. |
| The port is already in use | Stop your previous demo with Ctrl+C before running another copy. |
| Tests report `BUILD FAILURE` | Compare the counts with the README's starter baseline. Expected assertion failures are part of the exercise; keep the tests and POM unchanged. |
| `clean` cannot remove `target` files | Stop processes holding those files. OneDrive may also lock them. A fresh attempt is another option; grading uses fresh snapshots. |
| Git reports a path-length error | Use a shorter checkout path, or clone with `git clone --config core.longpaths=true SOURCE DESTINATION`. ZIP extraction does not require Git. |

After dependencies are cached, an offline test run is `.\mvnw.cmd -o -B -ntp test` (macOS/Linux: `./mvnw -o -B -ntp test`). Tests still report any unfinished behavior.

The project runs with the included in-memory H2 database. You do not need to install a database server, Redis, or global Maven.

Windows project execution has been verified. Clean-machine installation and native macOS/Linux execution have not been tested for this pack.
