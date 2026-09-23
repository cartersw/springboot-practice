# Incident Desk API

Suggested time: 60 minutes after setup. Full score: 100 (25 tests × 4 points).

## Scenario

An internal incident-tracking backend was partially implemented during a handover. The application starts and some routes work, but its API does not consistently match the contract. Repair the existing implementation without changing the tests or build configuration.

Complete or fix ticket creation, lookup, updates, deletion, status filtering, and priority sorting. Preserve already working behavior. You do not need to build authentication, pagination, a frontend, or a new application.

Suggested time: **60 minutes**, starting after dependency installation and smoke checks. Full score: **100 points**.

### 6.2 Ticket model

The JSON representation is exactly:

```json
{
  "id": 101,
  "externalRef": "INC-101",
  "title": "Printer offline",
  "priority": 3,
  "status": "OPEN"
}
```

| Field | Rules |
|---|---|
| `id` | Generated positive long. Read-only. |
| `externalRef` | Required on create. Strip surrounding whitespace, uppercase with `Locale.ROOT`, then require 3–32 characters matching `[A-Z0-9-]+`. Unique across tickets. Immutable after creation. |
| `title` | Required. Strip surrounding whitespace; normalized length 1–120. Preserve internal spaces and case. |
| `priority` | Required JSON integer, 1 through 5 inclusive. Larger number means higher priority. |
| `status` | On creation always `OPEN`. For updates, required string normalized with strip + uppercase; one of `OPEN`, `IN_PROGRESS`, `RESOLVED`. |

No timestamps or additional success fields are required. POST input containing `id` or `status` must not override generated identity or the initial `OPEN` state.

### 6.3 Endpoints

#### POST `/api/tickets`

Request:

```json
{
  "externalRef": " inc-200 ",
  "title": " Scanner disconnected ",
  "priority": 4
}
```

On success, persist a ticket, return **201**, set `Location: /api/tickets/{generatedId}`, and return its complete representation with `externalRef="INC-200"`, `title="Scanner disconnected"`, `priority=4`, and `status="OPEN"`.

If a ticket already has the normalized external reference, return **409 `DUPLICATE_REFERENCE`**. Do not insert another row or modify the existing row. Invalid input returns **400 `INVALID_REQUEST`** and leaves state unchanged.

#### GET `/api/tickets/{id}`

Return **200** and the complete ticket when found. A valid but absent ID returns **404 `NOT_FOUND`**, not `200` with an empty body or `null`.

#### GET `/api/tickets`

Optional query parameters:

| Parameter | Omitted behavior | Accepted values |
|---|---|---|
| `status` | No status filter | After strip + uppercase: `OPEN`, `IN_PROGRESS`, `RESOLVED`. An explicitly blank value is invalid. |
| `sort` | `idAsc` | After strip: exactly `idAsc` or `priorityDesc`; values are case-sensitive. Blank or unknown values are invalid. |

Return **200** with a JSON array. Apply status filtering before sorting. `idAsc` sorts by ID ascending. `priorityDesc` sorts by priority descending, breaking every tie by ID ascending. No matches means `[]`, not `404`.

Invalid query values return **400 `INVALID_REQUEST`**. There is no pagination in this exercise.

#### PUT `/api/tickets/{id}`

This is a full replacement of the three mutable fields, not a partial PATCH:

```json
{
  "title": "Scanner connection repaired",
  "priority": 2,
  "status": " resolved "
}
```

All three fields are required and validated. Return **200** with the complete updated ticket. Preserve the existing `id` and `externalRef`, even when input includes additional properties with those names. Persist all three mutable fields. Missing ticket: **404 `NOT_FOUND`**. Invalid body: **400 `INVALID_REQUEST`**. Failed updates leave the row unchanged.

#### DELETE `/api/tickets/{id}`

Existing ticket: delete it, return **204**, and send an empty response body. Missing ticket: **404 `NOT_FOUND`**. A deleted external reference may subsequently be used by a new ticket.

### 6.4 Error summary

| Situation | HTTP | Code |
|---|---:|---|
| Invalid body, malformed JSON, bad query, invalid path ID | 400 | `INVALID_REQUEST` |
| Ticket absent | 404 | `NOT_FOUND` |
| Duplicate normalized external reference | 409 | `DUPLICATE_REFERENCE` |

A valid body with an absent ID receives 404. No relative precedence is required when both body and ID are invalid.

### 6.5 Base fixtures and examples

Each contract test starts with these rows unless its case explicitly says otherwise. Insert them in shuffled order, such as 104, 102, 103, 101, so tests do not accidentally depend on insertion order.

| id | externalRef | title | priority | status |
|---:|---|---|---:|---|
| 101 | INC-101 | Printer offline | 3 | OPEN |
| 102 | INC-102 | Scanner timeout | 1 | IN_PROGRESS |
| 103 | INC-103 | Label mismatch | 5 | OPEN |
| 104 | INC-104 | Dashboard delay | 3 | RESOLVED |

Expected IDs:

```text
GET /api/tickets                                    -> [101, 102, 103, 104]
GET /api/tickets?status=OPEN                        -> [101, 103]
GET /api/tickets?sort=priorityDesc                  -> [103, 101, 104, 102]
GET /api/tickets?status=OPEN&sort=priorityDesc       -> [103, 101]
```

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
  "message": "Ticket not found",
  "path": "/api/tickets/9999"
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
- `src/main/java/dev/practice/assessment01/IncidentDeskApplication.java`
- `src/main/java/dev/practice/assessment01/config/DemoDataInitializer.java`
- `src/main/java/dev/practice/assessment01/health/HealthController.java`
- `src/main/resources/application.yml`
- `src/test/java/dev/practice/assessment01/contract/SmokeTest.java`
- `src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java`
- `src/test/java/dev/practice/assessment01/support/ApiTestSupport.java`
- `src/test/java/dev/practice/assessment01/support/Fixtures.java`
- `src/test/resources/application-test.yml`
- `src/test/resources/junit-platform.properties`
