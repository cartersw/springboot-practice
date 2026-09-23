# Cached Parts Catalog

Suggested time: 75 minutes after setup. Full score: 100 (25 tests × 4 points).

## Scenario

A parts-catalog API has inconsistent search results, pagination defects, and stale cached responses after product updates. Repair the existing backend. The repository already contains JPA entities, an H2 database, request parsing, a local cache adapter, and a query-observation helper.

You must make filtering, sorting, pagination, cache reuse, cache-key separation, and update invalidation conform to the contract. You are not being asked to install Redis or implement a cache server.

Suggested time: **75 minutes** after setup. Full score: **100 points**.

### 8.2 Product representation

```json
{
  "id": 101,
  "sku": "KB-01",
  "name": "Compact Keyboard",
  "category": "electronics",
  "priceCents": 5000,
  "stock": 5
}
```

Product IDs and SKUs are immutable. Prices use integer cents, not floating-point currency. Names are case-preserving, stripped strings. Categories are stripped lowercase strings using `Locale.ROOT`.

### 8.3 GET `/api/products`

The response is exactly this page envelope:

```json
{
  "content": [],
  "page": 0,
  "size": 5,
  "totalElements": 0,
  "totalPages": 0,
  "first": true,
  "last": true
}
```

Query parameters:

| Parameter | Default | Contract |
|---|---|---|
| `q` | Absent | Strip and lowercase. Absent/blank means no name filter. Otherwise literal case-insensitive substring match on `name` only. `%` and `_` are ordinary characters, not wildcards. Maximum normalized length 80. |
| `category` | Absent | Strip and lowercase. Absent/blank means no category filter. Otherwise case-insensitive exact category match, not a substring. Maximum normalized length 40. An unknown but valid category returns no matches. |
| `minPrice` | Absent | Integer cents, 0–1,000,000,000 inclusive. Product price must be greater than or equal to this bound. An explicitly blank value is invalid. |
| `maxPrice` | Absent | Integer cents, same range. Product price must be less than or equal to this bound. Explicit blank is invalid. |
| `inStock` | Absent | After strip + lowercase, exactly `true` or `false`. True means stock > 0; false means stock == 0; absent means either. Blank or another value is invalid. |
| `page` | 0 | Zero-based integer page number, 0–1,000,000 inclusive. Blank is invalid. |
| `size` | 5 | Integer, 1–50 inclusive. Blank is invalid. |
| `sort` | `priceAsc` | After strip: exactly `priceAsc`, `priceDesc`, or `nameAsc`. Case-sensitive. Blank is invalid. |

All active filters combine with **AND**. When both price bounds are supplied, `minPrice > maxPrice` is invalid.

Required operation order: **normalize/validate → filter → sort → paginate**. Search results must come from the database through the provided query gateway on a cache miss; do not hard-code the fixture rows or bypass that gateway.

Sorting:

- `priceAsc`: price ascending, then ID ascending.
- `priceDesc`: price descending, then ID ascending. The tie-breaker does **not** become descending.
- `nameAsc`: lowercase name ascending using ordinary lexicographic order, then ID ascending.

Pagination:

- `totalElements` is the number of filtered matches **before** taking the requested page.
- `totalPages` is 0 when there are no matches; otherwise it is ceiling(`totalElements / size`).
- `content` contains the slice starting at `page * size`, with at most `size` elements.
- An out-of-range page is a successful empty page. Preserve the requested page number and the correct filtered totals.
- `first` means `page == 0`.
- `last` means `totalPages == 0` or `page >= totalPages - 1`.
- Every valid search returns 200, even when empty. Invalid parameters return 400 `INVALID_REQUEST` before a query or cache entry is created.

### 8.4 Cache contract

A provided in-memory string key/value adapter stands in for the key-space behaviors commonly practiced with a cache. It is **not a Redis server or a Redis client implementation**. It stores immutable JSON strings and provides a clock-driven expiry mechanism. Its implementation is correct and protected.

The search cache must meet all these requirements:

1. Cache the complete successful search response, including metadata and empty pages.
2. Every search key begins with the exact prefix `products:search:v1:`.
3. The key must distinguish all normalized request dimensions: q, category, minPrice, maxPrice, inStock, page, size, and sort. Null/absent values must not collide with supplied string values. Do not rely on map iteration order, ambiguous concatenation, or a truncated hash.
4. Semantically equivalent spelling covered by the normalization rules must share an entry: surrounding whitespace, permitted case differences, blank q/category versus absent, omitted pagination/sort versus explicit defaults, and query-parameter ordering.
5. A cache hit must not call the provided database query gateway. A miss must call it exactly once. The gateway's counter measures logical search evaluations, **not the number of SQL statements**.
6. Entries expire 60 seconds after insertion. A read at 59 seconds is a hit; a read exactly at 60 seconds is a miss. Reads do not extend expiry. Use the supplied clock; do not sleep in tests or call an independent system clock.
7. After a successful product update, invalidate **all and only** keys whose names start with `products:search:v1:`. Search results may have changed membership, ordering, pages, and counts.
8. Do not clear the entire cache. Keys such as `products:search:v10:keep`, `products:detail:103`, and `orders:search:v1:keep` must survive.
9. Failed updates do not invalidate successful search entries. Invalid searches must not be cached.

The exact suffix encoding is an implementation choice; tests verify identity and separation behavior, not a secret string formula. This problem intentionally uses explicit cache orchestration rather than requiring Spring cache annotations.

### 8.5 PUT `/api/products/{id}`

Request body requires all four mutable fields:

```json
{
  "name": "Wireless Mouse",
  "category": "accessories",
  "priceCents": 3000,
  "stock": 0
}
```

| Field | Validation/normalization |
|---|---|
| `name` | Strip; length 1–100; preserve case and internal spaces. |
| `category` | Strip + lowercase; length 1–40; match `[a-z][a-z0-9-]*`. |
| `priceCents` | Required integer, 0–1,000,000,000 inclusive. |
| `stock` | Required integer, 0–1,000,000 inclusive. |

Success: persist changes, invalidate the search namespace, return 200 and the complete product DTO. Extra body fields `id` and `sku` must not change identity. Even a valid no-op update counts as a successful update and invalidates search entries.

Missing positive ID: 404 `NOT_FOUND`. Invalid body/ID: 400 `INVALID_REQUEST`. A failed write leaves all product data and valid search-cache entries unchanged.

There is no product creation, deletion, or individual GET requirement in this assessment. Do not add those endpoints as candidate tasks.

### 8.6 Base fixtures

Seed exactly these rows; insert in deliberately non-sorted order. Product IDs are fixture-assigned because the API does not create products.

| id | sku | name | category | priceCents | stock |
|---:|---|---|---|---:|---:|
| 101 | KB-01 | Compact Keyboard | electronics | 5000 | 5 |
| 102 | KB-02 | Mechanical Keyboard | electronics | 9000 | 0 |
| 103 | MS-01 | Wireless Mouse | electronics | 2500 | 8 |
| 104 | MS-02 | Travel Mouse | electronics | 2500 | 2 |
| 105 | NT-01 | Grid Notebook | stationery | 700 | 20 |
| 106 | NT-02 | Plain Notebook | stationery | 700 | 0 |
| 107 | PN-01 | Gel Pen | stationery | 200 | 50 |
| 108 | DK-01 | Standing Desk | furniture | 20000 | 3 |
| 109 | CH-01 | Office Chair | furniture | 15000 | 0 |
| 110 | CB-01 | USB-C Cable | electronics | 1000 | 12 |
| 111 | ST-01 | Monitor Stand | furniture | 5000 | 4 |
| 112 | KB-03 | Keyboard Cover | accessories | 500 | 10 |

Independent expected orders:

```text
All, priceAsc:             [107,112,105,106,110,103,104,101,111,102,109,108]
All, nameAsc:              [101,107,105,112,102,111,109,106,108,104,110,103]
Electronics, priceAsc:     [110,103,104,101,102]
Electronics, priceDesc:    [102,101,103,104,110]
Electronics, nameAsc:      [101,102,104,110,103]
Electronics, inStock=true: [110,103,104,101]
Electronics, inStock=false:[102]
All, price 2500..5000:     [103,104,101,111]
```

A default GET returns IDs `[107,112,105,106,110]`, page 0, size 5, totalElements 12, totalPages 3, first true, last false.

## Shared request and error rules



- Request and response bodies use JSON. Successful response field names and types are explicitly defined below. JSON object property order does not matter; array order does.
- IDs are positive Java `long` values represented as JSON integers. Nonpositive or nonnumeric path IDs receive `400 INVALID_REQUEST`. Do not hard-code generated IDs in tests or application code.
- Text normalization means Java `String.strip()`. Case folding explicitly described below uses `Locale.ROOT`. Length bounds refer to normalized values. Tests use ASCII boundary data; Unicode normalization and grapheme counting are not assessment topics.
- Required means a field cannot be omitted or `null`. Required string fields also cannot normalize to empty. Numeric fields use boxed request types so omission is distinguishable from zero.
- Reject fractional numbers for integer request fields. Nonnumeric JSON/query inputs receive `400`. Numeric strings are not a separate scored coercion edge case.
- Unknown JSON properties are ignored, including attempts to set read-only fields. DTOs must keep those properties from mutating stored identity fields. Unknown query parameter names are ignored. Repeated instances of the same query parameter and malformed JSON with duplicate keys are out of scope.
- Unsupported HTTP methods, unknown routes, CORS, authentication, and arbitrary malformed URLs are out of scope. 
- Do not depend on ORM entity serialization. Return DTOs with exactly the declared success fields. Do not expose JPA relationships, internal fingerprints, or audit internals in JSON.
- All scored error responses use the error envelope below. An explanatory message must be nonempty but its precise English wording is not scored.

```json
{
  "status": 404,
  "code": "NOT_FOUND",
  "message": "Product not found",
  "path": "/api/products/9999"
}
```

`status` matches the HTTP status; `code` is the endpoint-specific value; `message` is a nonblank string; `path` is the request URI without its query string. No exact error-message text matching. No timestamps, stack traces, or SQL messages are required.

When multiple independent request defects coexist, any applicable `400 INVALID_REQUEST` message is acceptable. Where business-error precedence is specified, follow it. Otherwise no relative precedence is required.

## Allowed work and protected files

Edit or add files under `src/main/java/**`, except the concrete protected application files below. Keep existing working behavior. Do not modify build files, tests, fixtures, resources or protected adapters; do not hard-code fixtures, bypass observation interfaces, special-case test inputs, or suppress tests. Full grading verifies protected files and uses pristine tests/build configuration in a new isolated snapshot.

- `.mvn/wrapper/maven-wrapper.properties`
- `mvnw`
- `mvnw.cmd`
- `pom.xml`
- `src/main/java/dev/practice/assessment02/CachedCatalogApplication.java`
- `src/main/java/dev/practice/assessment02/cache/InMemoryKeyValueStore.java`
- `src/main/java/dev/practice/assessment02/cache/KeyValueStore.java`
- `src/main/java/dev/practice/assessment02/config/ClockConfig.java`
- `src/main/java/dev/practice/assessment02/config/DemoDataInitializer.java`
- `src/main/java/dev/practice/assessment02/health/HealthController.java`
- `src/main/java/dev/practice/assessment02/observation/ProductQueryGateway.java`
- `src/main/java/dev/practice/assessment02/observation/QueryProbe.java`
- `src/main/resources/application.yml`
- `src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java`
- `src/test/java/dev/practice/assessment02/contract/SmokeTest.java`
- `src/test/java/dev/practice/assessment02/support/ApiTestSupport.java`
- `src/test/java/dev/practice/assessment02/support/ClockTestConfig.java`
- `src/test/java/dev/practice/assessment02/support/Fixtures.java`
- `src/test/java/dev/practice/assessment02/support/MutableClock.java`
- `src/test/resources/application-test.yml`
- `src/test/resources/junit-platform.properties`
