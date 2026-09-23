# Repository map

`src/main/java/dev/practice/assessment01` contains the application.

TicketController → TicketService → TicketRepository → H2. TicketMapper builds response DTOs; TicketRequestValidator parses and checks inputs.

`dto/` defines input and output records. `model/` contains persistence entities.
`error/ApiExceptionHandler` translates application and framework errors into JSON.
Constructor injection connects Spring components. The application bootstrap,
health route and demo initializer are supplied infrastructure.

Public tests live in `src/test/java/dev/practice/assessment01/contract/`.
`support/ApiTestSupport` provides real MockMvc requests and database observations.
`support/Fixtures` resets committed fixture rows before each independent test.
Tests have no enclosing test transaction. Tests use their own fixture setup;
the `demo` profile seeds manual exploration data only. H2 data resets on restart.
The exact protected file list is in ASSESSMENT.md and assessment.json.
