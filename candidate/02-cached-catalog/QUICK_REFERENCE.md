# Java and Spring quick reference

| Familiar .NET concept | Spring/Java concept here |
|---|---|
| API controller and route attributes | `@RestController`, `@GetMapping`, `@PostMapping`, `@PutMapping` |
| Constructor dependency injection | Spring injects beans into a constructor. `@Service`, `@Repository`, and `@Component` register common roles. |
| HTTP result objects | `ResponseEntity` controls status, headers and a DTO body. |
| Immutable data carrier | Java `record`; accessors use `value.name()`. |
| Persistence context / repository | JPA entities and Spring Data repositories. Entities have a no-argument constructor and accessors. |
| Request validation and central errors | Jakarta validation or explicit checks; `@RestControllerAdvice` translates exceptions. |
| Integration tests | JUnit Jupiter with MockMvc and H2; requests exercise actual MVC handling. |

Read the controller route first, then follow its injected service into persistence.
Use your IDE's Go to Definition on a type or method, Find References for callers,
and search for a route or public test method name. `import` lines show where a type lives.
Java generics use `List<T>` and `Optional<T>`; a missing Optional must be handled.
Use `.equals()` for value equality; `==` compares object identity (and primitive values).
DTOs are the API boundary. Entity persistence does not imply that arbitrary entity
fields belong in JSON. Integer cents avoid floating-point currency calculations.

Run one public test while investigating: `./mvnw '-Dtest=CLASS#METHOD' test`, or
PowerShell `.\mvnw.cmd '-Dtest=CLASS#METHOD' test`, substituting names from
`public-tests.json`. Normal `test` discovers all public tests and smoke checks.

Maven prints compilation diagnostics before test execution. A compilation error,
dependency download error or failed context smoke check is a setup/readiness
problem. A JUnit assertion shows expected versus actual application behavior.
Read its first relevant public test stack frame and its surrounding assertions.
`Tests run`, `Failures`, `Errors`, and `Skipped` describe execution, not the full
practice score. Full grading always uses 25 scored tests worth four points each.
`-DskipTests package` only checks setup and compilation; it is not test verification.

Fixtures reset independently before each test, so requests in different tests do
not share a scenario. Debug one test with its own fixtures. Use returned IDs in
manual requests; database sequences need not be gap-free.

General references: [Spring MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html),
[Spring Data JPA](https://docs.spring.io/spring-data/jpa/reference/),
[JUnit](https://junit.org/junit5/docs/current/user-guide/).
These are framework references, not exercise solutions.
