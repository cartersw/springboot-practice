# Repository map

`src/main/java/dev/practice/assessment02` contains the application.

ProductSearchController → SearchRequestParser → ProductSearchService → SearchKeyFactory / KeyValueStore. Cache misses go through the protected ProductQueryGateway and QueryProbe to ProductSearchRepository. The repository applies database pagination and constructs CatalogPageResponse metadata. ProductWriteController → ProductWriteService → ProductRepository / SearchCacheInvalidator. The protected ClockConfig and cache adapter provide expiration.

`dto/` defines input and output records. `model/` contains persistence entities.
`error/ApiExceptionHandler` translates application and framework errors into JSON.
Constructor injection connects Spring components. The application bootstrap,
health route and demo initializer are supplied infrastructure.

Public tests live in `src/test/java/dev/practice/assessment02/contract/`.
`support/ApiTestSupport` provides real MockMvc requests and database observations.
`support/Fixtures` resets committed fixture rows before each independent test.
Tests have no enclosing test transaction. Tests use their own fixture setup;
the `demo` profile seeds manual exploration data only. H2 data resets on restart.
The exact protected file list is in ASSESSMENT.md and assessment.json.
