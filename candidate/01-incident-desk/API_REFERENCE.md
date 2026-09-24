# Incident Desk: API Reference

Read [the problem statement](ASSESSMENT.md) first. This page contains the exact input limits, response fields, and edge cases used by the tests. These rules are required parts of the same assessment.

When implementing an endpoint, use its section below to check the details. For setup, running the app, and scoring, see [README.md](README.md).

## Ticket fields

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

## Required endpoints

### Task 1: Create a ticket: POST `/api/tickets`

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

### Task 2: View a ticket: GET `/api/tickets/{id}`

Return **200** and the complete ticket when found. A valid but absent ID returns **404 `NOT_FOUND`**, not `200` with an empty body or `null`.

### Task 3: List, filter, and sort tickets: GET `/api/tickets`

Optional query parameters:

| Parameter | Omitted behavior | Accepted values |
|---|---|---|
| `status` | No status filter | After strip + uppercase: `OPEN`, `IN_PROGRESS`, `RESOLVED`. An explicitly blank value is invalid. |
| `sort` | `idAsc` | After strip: exactly `idAsc` or `priorityDesc`; values are case-sensitive. Blank or unknown values are invalid. |

Return **200** with a JSON array. Apply status filtering before sorting. `idAsc` sorts by ID ascending. `priorityDesc` sorts by priority descending, breaking every tie by ID ascending. No matches means `[]`, not `404`.

Invalid query values return **400 `INVALID_REQUEST`**. There is no pagination in this exercise.

### Task 4: Update a ticket: PUT `/api/tickets/{id}`

This is a full replacement of the three mutable fields, not a partial PATCH:

```json
{
  "title": "Scanner connection repaired",
  "priority": 2,
  "status": " resolved "
}
```

All three fields are required and validated. Return **200** with the complete updated ticket. Preserve the existing `id` and `externalRef`, even when input includes additional properties with those names. Persist all three mutable fields. Missing ticket: **404 `NOT_FOUND`**. Invalid body: **400 `INVALID_REQUEST`**. Failed updates leave the row unchanged.

### Task 5: Delete a ticket: DELETE `/api/tickets/{id}`

Existing ticket: delete it, return **204**, and send an empty response body. Missing ticket: **404 `NOT_FOUND`**. A deleted external reference may subsequently be used by a new ticket.

## Error summary

| Situation | HTTP | Code |
|---|---:|---|
| Invalid body, malformed JSON, bad query, invalid path ID | 400 | `INVALID_REQUEST` |
| Ticket absent | 404 | `NOT_FOUND` |
| Duplicate normalized external reference | 409 | `DUPLICATE_REFERENCE` |

A valid body with an absent ID receives 404. No relative precedence is required when both body and ID are invalid.

## Supplied sample data and list examples

The supplied tests load these rows unless a test specifies different data. Their insertion order is deliberately shuffled, so the API must apply the requested sort. You do not need to create or edit these fixtures.

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
  "code": "NOT_FOUND",
  "message": "Ticket not found",
  "path": "/api/tickets/9999"
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
