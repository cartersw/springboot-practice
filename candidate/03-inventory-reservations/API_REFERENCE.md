# Inventory Reservations: API Reference

Read [the problem statement](ASSESSMENT.md) first. This page contains the exact input limits, response fields, and edge cases used by the tests. These rules are required parts of the same assessment.

When implementing an endpoint, use its section below to check the details. For setup, running the app, and scoring, see [README.md](README.md).

## Reservation fields

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

## Task 1: Create a reservation and handle retries: POST `/api/reservations`

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

### Decide whether this is a new request or a retry

Validate and normalize the request first. Then look up `requestKey` before checking current stock availability:

- A previously unused key with sufficient stock creates a reservation, subtracts every merged line quantity, and records one `CREATED` audit event. Return **201**, a `Location` header of `/api/reservations/{id}`, and the reservation DTO.
- An existing key with the same normalized customer reference and identical merged SKU/quantity lines returns **200** and the existing reservation's **current** DTO. Do not create another row, subtract stock again, or record another event. Item ordering, permitted SKU case differences, and duplicate partitioning do not make it a different request.
- An existing key with a different normalized customer reference or different merged lines returns **409 `IDEMPOTENCY_CONFLICT`**. Leave all state unchanged.
- A replay of a cancelled reservation returns that same reservation with status `CANCELLED`; it must not reserve stock again. Do not recheck availability on a valid replay.

For a new key, a referenced SKU that does not exist returns **404 `STOCK_NOT_FOUND`**. An existing SKU with insufficient available quantity returns **409 `INSUFFICIENT_STOCK`**. A quantity exactly equal to available stock is valid and leaves zero available.

### Keep creation all-or-nothing

Stock deductions, the reservation header, lines, and its `CREATED` audit row must either all commit or none commit. Any failed attempt leaves the request key available for a later successful retry. A failure on a later line must not leave deductions from an earlier line.

The supplied audit collaborator may throw an availability exception. Map it to **503 `RESERVATION_UNAVAILABLE`**, with the shared error envelope, and roll back the entire workflow. This is a deterministic failure mode exercised by tests, not a requirement to connect to a network service.

When several input fields are invalid, the tests do not require a particular validation message. When a new request simultaneously contains unknown and insufficient-stock lines, no relative precedence between those two business errors is graded; either applicable error is acceptable, but rollback is mandatory. The validation-before-idempotency and idempotency-before-availability ordering above **is** part of the contract.

## Task 2: View a reservation: GET `/api/reservations/{id}`

Existing positive ID: 200 and the complete reservation DTO, whether `ACTIVE` or `CANCELLED`. Missing positive ID: **404 `RESERVATION_NOT_FOUND`**. Invalid/nonpositive ID: 400 `INVALID_REQUEST`.

The response must reflect committed data and include merged, SKU-sorted item lines. This endpoint must work when the Open EntityManager in View feature is disabled, as it is in the supplied configuration.

## Task 3: Cancel a reservation: POST `/api/reservations/{id}/cancel`

No request body is required.

- An active reservation becomes `CANCELLED`. Restore each reserved quantity to its stock item, record exactly one `CANCELLED` audit event, and return **200** with the updated DTO.
- Repeating cancellation on an already cancelled reservation returns **200** with the same current DTO. Do not restore stock again or add another audit event.
- A missing positive ID returns **404 `RESERVATION_NOT_FOUND`**. Invalid/nonpositive ID returns 400 `INVALID_REQUEST`.
- Cancellation must be atomic too. An audit failure returns **503 `RESERVATION_UNAVAILABLE`** and leaves stock quantities, status, and all audit rows as they were before the request. A subsequent successful cancellation restores stock exactly once.

## Task 4: Report inventory: GET `/api/inventory/summary`

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

## Supplied sample stock and test data

The supplied tests start with the following stock and no reservations, lines, or audit events unless a test specifies different data. Test setup is already provided; you do not need to write it:

| SKU | Name | availableQuantity |
|---|---|---:|
| BOLT-M8 | M8 Bolt | 10 |
| NUT-M8 | M8 Nut | 8 |
| WASHER-M8 | M8 Washer | 0 |
| CLIP-S | Small Clip | 20 |

An initial summary has SKU order `[BOLT-M8, CLIP-S, NUT-M8, WASHER-M8]`, available quantities `[10,20,8,0]`, and zero reserved quantity and active reservation count in every row.

A reusable **active reservation fixture** has ID 701, key `fixture-701`, customer `team-a`, lines BOLT-M8 quantity 3 and NUT-M8 quantity 2, one `CREATED` event, available BOLT-M8=7 and NUT-M8=6. Its total quantity is 5. The tests can load this reservation directly as committed starting data, independently of the creation endpoint. You do not need to create or modify this fixture.

## Request validation and error responses

These rules apply to every endpoint in this assessment:

- Use JSON request and response bodies. Return exactly the success fields specified above. JSON object field order does not matter; array order does.
- IDs are positive Java `long` values represented as JSON integers. A nonpositive or nonnumeric path ID returns **400 `INVALID_REQUEST`**. Use generated IDs rather than hard-coding expected values.
- When a rule says to strip text, use Java `String.strip()`. Apply case changes only where specified, using `Locale.ROOT`. Check length after normalization. Tests use ASCII boundary values; Unicode normalization and grapheme counting are outside scope.
- A required field cannot be missing or `null`. A required string also cannot be empty after normalization. Numeric request fields use boxed types so a missing value remains distinguishable from zero.
- Reject fractional values for integer fields. Nonnumeric values in numeric JSON fields or query parameters return **400**. Numeric strings are not a separately scored coercion case.
- Ignore unknown JSON fields, including attempts to override read-only fields. Ignore unknown query parameter names. Repeated query parameters and malformed JSON with duplicate keys are outside scope.
- Return DTOs with the documented fields. Do not rely on ORM entity serialization or expose JPA relationships, internal fingerprints, or audit internals.
- Unsupported HTTP methods, unknown routes, CORS, authentication, and arbitrary malformed URLs are outside scope.

Every scored error response must use this shape:

```json
{
  "status": 404,
  "code": "RESERVATION_NOT_FOUND",
  "message": "Reservation not found",
  "path": "/api/reservations/9999"
}
```

`status` must match the HTTP status. `code` must match the relevant error below or in the endpoint requirements. `message` must be nonblank, but its exact wording is your choice. `path` is the request URI without its query string. No timestamps, stack traces, or SQL messages are required.

If several request fields are invalid, any applicable **400 `INVALID_REQUEST`** message is acceptable. Follow any error-ordering rules explicitly stated for an endpoint; otherwise, no particular precedence is required.

## Files you may change

**Make your solution changes under `src/main/java/`, except for the protected Java files listed below.** You may edit existing classes or add classes there. Preserve behavior that already works.

Keep the build files, tests, fixtures, resources, and protected adapters unchanged. Do not hard-code sample data, special-case test inputs, bypass observation interfaces, or suppress tests. Full grading checks protected files and runs against pristine tests and build configuration in an isolated snapshot.

Protected files:

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
