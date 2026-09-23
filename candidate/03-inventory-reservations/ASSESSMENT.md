# Inventory Reservations

Suggested time: 90 minutes after setup. Full score: 100 (25 tests × 4 points).

## Scenario

A small stock service lets teams reserve available parts. An existing implementation accepts requests, saves reservations, and produces inventory summaries, but it mishandles several edge cases. Repair it without replacing the supplied database or bypassing the audit collaborator.

This exercise is about **sequential requests in one application instance**. You are not being asked to implement distributed locks, concurrent overselling protection, event streaming, or a real external audit service. Nevertheless, each individual write workflow must be all-or-nothing when a business rule or the supplied audit operation fails.

### 10.2 Data and response shapes

Stock items have a normalized SKU, a display name, and a nonnegative available quantity. Reservations have an ID, request key, customer reference, status, and one or more item lines. The two statuses are `ACTIVE` and `CANCELLED`.

A reservation response contains exactly these fields; line items are always sorted by SKU ascending:

```json
{
  "id": 1000,
  "requestKey": "req-001",
  "customerRef": "team-a",
  "status": "ACTIVE",
  "items": [
    {"sku": "BOLT-M8", "quantity": 3},
    {"sku": "NUT-M8", "quantity": 2}
  ],
  "totalQuantity": 5
}
```

`totalQuantity` is the sum of the normalized, merged line quantities. Internal line IDs, database relationships, audit rows, and the stored canonical request representation must not appear in JSON.

### 10.3 POST `/api/reservations`

Request body:

```json
{
  "requestKey": "req-001",
  "customerRef": "team-a",
  "items": [
    {"sku": "BOLT-M8", "quantity": 3},
    {"sku": "NUT-M8", "quantity": 2}
  ]
}
```

Normalize and validate the request before applying idempotency or changing data:

| Field | Contract |
|---|---|
| `requestKey` | Required string. Strip; length 1–64; match `[A-Za-z0-9_-]+`. **Case-sensitive.** `r-Key` and `R-Key` are different keys. |
| `customerRef` | Required string. Strip; length 1–64; preserve case and internal spaces. Case-sensitive when comparing normalized requests. |
| `items` | Required nonnull array of 1–20 nonnull objects. |
| `items[].sku` | Required string. Strip + uppercase with `Locale.ROOT`; length 1–32; match `[A-Z0-9-]+`. |
| `items[].quantity` | Required integer, 1–100 inclusive **per input item**. Missing, null, fractional, or out-of-range quantities are invalid. |

Merge duplicate normalized SKUs by summing quantities. The merged quantity may exceed 100; the 100 limit applies to each input item, not to the merged total. The input limits naturally bound each merged total to at most 2,000. Sort merged lines by normalized SKU. Input item order and the way a quantity is split across duplicate SKUs must not affect the request's meaning.

Ignore unknown request fields, including attempted `id`, `status`, and `totalQuantity` overrides. A newly created reservation is always `ACTIVE`.

**Idempotency:** after validation/normalization, look up `requestKey` before checking current stock availability.

- A previously unused key with sufficient stock creates a reservation, subtracts every merged line quantity, and records one `CREATED` audit event. Return **201**, a `Location` header of `/api/reservations/{id}`, and the reservation DTO.
- An existing key with the same normalized customer reference and identical merged SKU/quantity lines returns **200** and the existing reservation's **current** DTO. Do not create another row, subtract stock again, or record another event. Item ordering, permitted SKU case differences, and duplicate partitioning do not make it a different request.
- An existing key with a different normalized customer reference or different merged lines returns **409 `IDEMPOTENCY_CONFLICT`**. Leave all state unchanged.
- A replay of a cancelled reservation returns that same reservation with status `CANCELLED`; it must not reserve stock again. Do not recheck availability on a valid replay.

For a new key, a referenced SKU that does not exist returns **404 `STOCK_NOT_FOUND`**. An existing SKU with insufficient available quantity returns **409 `INSUFFICIENT_STOCK`**. A quantity exactly equal to available stock is valid and leaves zero available.

**Atomicity:** stock deductions, the reservation header, lines, and its `CREATED` audit row must either all commit or none commit. Any failed attempt leaves the request key available for a later successful retry. A failure on a later line must not leave deductions from an earlier line.

The supplied audit collaborator may throw an availability exception. Map it to **503 `RESERVATION_UNAVAILABLE`**, with the shared error envelope, and roll back the entire workflow. This is a deterministic failure mode exercised by tests, not a requirement to connect to a network service.

When several input fields are invalid, the tests do not require a particular validation message. When a new request simultaneously contains unknown and insufficient-stock lines, no relative precedence between those two business errors is graded; either applicable error is acceptable, but rollback is mandatory. The validation-before-idempotency and idempotency-before-availability ordering above **is** part of the contract.

### 10.4 GET `/api/reservations/{id}`

Existing positive ID: 200 and the complete reservation DTO, whether `ACTIVE` or `CANCELLED`. Missing positive ID: **404 `RESERVATION_NOT_FOUND`**. Invalid/nonpositive ID: 400 `INVALID_REQUEST`.

The response must reflect committed data and include merged, SKU-sorted item lines. This endpoint must work when the Open EntityManager in View feature is disabled, as it is in the supplied configuration.

### 10.5 POST `/api/reservations/{id}/cancel`

No request body is required.

- An active reservation becomes `CANCELLED`. Restore each reserved quantity to its stock item, record exactly one `CANCELLED` audit event, and return **200** with the updated DTO.
- Repeating cancellation on an already cancelled reservation returns **200** with the same current DTO. Do not restore stock again or add another audit event.
- A missing positive ID returns **404 `RESERVATION_NOT_FOUND`**. Invalid/nonpositive ID returns 400 `INVALID_REQUEST`.
- Cancellation must be atomic too. An audit failure returns **503 `RESERVATION_UNAVAILABLE`** and leaves stock quantities, status, and all audit rows as they were before the request. A subsequent successful cancellation restores stock exactly once.

### 10.6 GET `/api/inventory/summary`

Return 200 and an array sorted by SKU ascending. Include **every stock item**, even if it has never been reserved or has no active reservation. Each element contains exactly:

```json
{
  "sku": "BOLT-M8",
  "availableQuantity": 5,
  "reservedQuantity": 5,
  "activeReservations": 2
}
```

- `availableQuantity`: currently stored available quantity.
- `reservedQuantity`: sum of that SKU's line quantities in `ACTIVE` reservations only.
- `activeReservations`: count of **distinct active reservation IDs** containing that SKU, not the quantity sum and not a count of audit events.
- Cancelled reservations contribute zero to both aggregate values.
- Use numeric zero rather than null when no active reservation contributes.

There is no pagination, filtering, price calculation, stock-adjustment HTTP endpoint, or performance benchmark in this exercise.

### 10.7 Base stock fixture

Start each independent test with these rows and no reservations, lines, or audit events unless its setup says otherwise:

| SKU | Name | availableQuantity |
|---|---|---:|
| BOLT-M8 | M8 Bolt | 10 |
| NUT-M8 | M8 Nut | 8 |
| WASHER-M8 | M8 Washer | 0 |
| CLIP-S | Small Clip | 20 |

An initial summary has SKU order `[BOLT-M8, CLIP-S, NUT-M8, WASHER-M8]`, available quantities `[10,20,8,0]`, and zero reserved quantity and active reservation count in every row.

A reusable **active reservation fixture** has ID 701, key `fixture-701`, customer `team-a`, lines BOLT-M8 quantity 3 and NUT-M8 quantity 2, one `CREATED` event, available BOLT-M8=7 and NUT-M8=6. Its total quantity is 5. Build this directly in committed fixture setup, not by calling the creation endpoint.

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
  "code": "RESERVATION_NOT_FOUND",
  "message": "Reservation not found",
  "path": "/api/reservations/9999"
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
- `src/main/java/dev/practice/assessment03/InventoryReservationsApplication.java`
- `src/main/java/dev/practice/assessment03/audit/DatabaseReservationAudit.java`
- `src/main/java/dev/practice/assessment03/audit/ReservationAudit.java`
- `src/main/java/dev/practice/assessment03/config/DemoDataInitializer.java`
- `src/main/java/dev/practice/assessment03/health/HealthController.java`
- `src/main/resources/application.yml`
- `src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java`
- `src/test/java/dev/practice/assessment03/contract/SmokeTest.java`
- `src/test/java/dev/practice/assessment03/support/ApiTestSupport.java`
- `src/test/java/dev/practice/assessment03/support/AuditTestConfig.java`
- `src/test/java/dev/practice/assessment03/support/ControllableReservationAudit.java`
- `src/test/java/dev/practice/assessment03/support/Fixtures.java`
- `src/test/resources/application-test.yml`
- `src/test/resources/junit-platform.properties`
