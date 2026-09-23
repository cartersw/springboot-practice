# Source ledger

The following source notes were supplied by specification v1.0. The builder did not copy external assessment code or tests. Dependency resolution and application behavior were verified locally; source-review dates below belong to the specification author.

Sources were reviewed for this specification on **2026-09-23**. Public repository contents and hosted documentation can change. These links establish the general format and framework behavior; the original assessment contracts above are not copied from them. The builder should preserve a concise source ledger in `_authoring/SOURCE_NOTES.md` without requiring these repositories as dependencies.

### S01 — HackerRank project configuration

HackerRank, **Configurations for Front-end, Back-end and Full stack Developer Questions**. Official documentation covering project scoring commands/results, test weights, read-only paths, and a Spring Boot configuration example.

https://support.hackerrank.com/articles/9443018671-configurations-for-front-end,-back-end-and-full-stack-developer-questions

### S02 — HackerRank candidate project workflow

HackerRank Candidate Support, **Taking Front-end, Back-end, Full-stack and Mobile Developer Assessments**. Official description of the project-based candidate environment and running tests.

https://candidatesupport.hackerrank.com/articles/8606305957-taking-front-end-back-end-full-stack-and-mobile-developer-assessments

### S03 — Repository feature and bug-fix format

HackerRank, **October 2025 Release Notes**. Official release notes discussing repository-based development questions, including framework-oriented feature and bug-fix work.

https://support.hackerrank.com/articles/8474307750-october-2025-release-notes

### S04 — Public interview exercise and author guidance

`agrison`, **springboot-backend-interview**. Public source repository and interviewer guide describing incomplete application code, tests, and a candidate's development process. Used for general exercise structure only; its optional performance tasks and dependencies are not copied.

https://github.com/agrison/springboot-backend-interview

https://raw.githubusercontent.com/agrison/springboot-backend-interview/master/Interviewer.md

### S05 — Public repository describing HackerRank provenance

`AfamO`, **hackerrank-spring-challenge**. The author's description mentions a HackerRank challenge, CRUD-style requirements, and H2. This is a third-party publication, not authenticated current employer material.

https://github.com/AfamO/hackerrank-spring-challenge

### S06 — Exposed tests illustrating the provenance/completeness limitation

The same repository's `SampleApplicationTests.java` contains greeting-endpoint tests that do not match its README CRUD scenario. This discrepancy is why no exact assessment content or expected outcomes were inferred from the repository.

https://raw.githubusercontent.com/AfamO/hackerrank-spring-challenge/main/src/test/java/com/hackerrank/sample/SampleApplicationTests.java

### S07 — Public Spring Boot take-home assignment

Crewmeister, **java-coding-challenge**. Public backend assignment with REST requirements and a simple persistence option. Its external data source and domain are not used in this pack.

https://github.com/crewmeister/java-coding-challenge

https://raw.githubusercontent.com/crewmeister/java-coding-challenge/master/README.md

### S08 — Spring Boot 3.5 compatibility baseline

Spring, **System Requirements — Spring Boot 3.5**. Official Java and Maven compatibility requirements. The page reviewed identified Boot 3.5.16; the builder still must resolve and verify the chosen patch in its own environment.

https://docs.spring.io/spring-boot/3.5/system-requirements.html

### S09 — Maven distribution pin

Apache Maven, **Maven 3.9.9 Release Notes**. Official record of the distribution pinned for this practice environment.

https://maven.apache.org/docs/3.9.9/release-notes.html

### S10 — Maven Wrapper generation and platform entry points

Apache Maven, **Maven Wrapper** and **wrapper:wrapper** plugin goal documentation. Official wrapper generation and configuration guidance; preserve the official scripts rather than writing lookalikes.

https://maven.apache.org/tools/wrapper/

https://maven.apache.org/tools/wrapper/maven-wrapper-plugin/wrapper-mojo.html

### S11 — HTTP-layer integration testing

Spring Framework 6.2, **MockMvc**. Official testing framework reference for exercising Spring MVC request handling without a running HTTP server.

https://docs.spring.io/spring-framework/reference/6.2/testing/mockmvc.html

### S12 — Database queries, sorting, and pagination

Spring Data JPA, **JPA Query Methods**, and Spring Data Commons, **Defining Query Methods**. Official repository-query and paging/sorting documentation. The literal search behavior and particular pagination response are specified by this pack, not assumed from framework defaults.

https://docs.spring.io/spring-data/jpa/reference/3.5/jpa/query-methods.html

https://docs.spring.io/spring-data/commons/reference/repositories/query-methods-details.html

### S13 — Application transaction boundaries

Spring Framework 6.2, **Using @Transactional**. Official explanation of declarative transactions and proxy-interception/self-invocation considerations.

https://docs.spring.io/spring-framework/reference/6.2/data-access/transaction/declarative/annotations.html

### S14 — Avoiding test-managed transaction masking

Spring Framework 6.2, **Transaction Management — TestContext Framework**. Official distinction between test-managed transactions and application transaction participation. This pack intentionally observes committed state without a test transaction.

https://docs.spring.io/spring-framework/reference/6.2/testing/testcontext-framework/tx.html

### S15 — Surefire test discovery and execution

Apache Maven Surefire, **Inclusions and Exclusions of Tests** and **surefire:test**. Official discovery and execution settings. This pack uses fixed method identities and XML results rather than display-name parsing or terminal grep.

https://maven.apache.org/surefire/maven-surefire-plugin/examples/inclusion-exclusion.html

https://maven.apache.org/surefire/maven-surefire-plugin/test-mojo.html

### S16 — Cache-key semantics

Spring Framework, **Declarative Annotation-based Caching**. Official discussion of cache keys and parameters. This assessment uses an explicit local adapter instead of asking the candidate to configure that annotation system or Redis.

https://docs.spring.io/spring-framework/reference/integration/cache/annotations.html

### S17 — Codex / agent instruction scoping

OpenAI, **Custom instructions with AGENTS.md**. Official instructions for scoped project guidance. Read the master specification explicitly and keep practice-folder instruction files short.

https://developers.openai.com/codex/guides/agents-md/

At review time this redirected to:

https://learn.chatgpt.com/docs/agent-configuration/agents-md

---
