# Executed version lock

Verified 2026-09-23 on Windows 11 AMD64.

- Eclipse Temurin JDK / javac 21.0.12.1; compile release 21, no previews.
- Spring Boot 3.5.16. No version substitution or SNAPSHOT dependency.
- Maven 3.9.9 through official wrapper 3.3.4 (only-script).
- Compiler plugin 3.14.1, Surefire 3.5.6, H2 2.3.232 (Boot-managed).
- Python 3.13.7, standard library only for tooling; minimum 3.11.
- Git 2.54.0.windows.1; Unix wrapper executed through Git Bash.

Tool binaries and dependency caches were restored from the original parent pack
into _authoring/toolchain. No global Maven or external runtime services required.
Exact output: verification/doctor.log, start-here-setup.log and *-reference.log.
Normal-user runs pass; sandbox Java filesystem access errors are recorded in
verification/01-clean-diagnostic.log. No global settings were changed.
