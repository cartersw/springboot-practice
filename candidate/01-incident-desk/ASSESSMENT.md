# Incident Desk

Complete a Spring Boot API for managing support tickets. A user should be able to report an incident, view open tickets, change a ticket's details, and delete a ticket.

The project is already set up and some functionality works. Fix the existing application so it behaves as described below and passes the tests.

## Requirements

Each ticket has an `id`, an `externalRef` such as `INC-200`, a `title`, a `priority` from 1 to 5, and a `status`. A higher priority number means a more urgent ticket. The supported statuses are `OPEN`, `IN_PROGRESS`, and `RESOLVED`.

### 1. Create a ticket

`POST /api/tickets`

The user supplies an external reference, title, and priority. Remove surrounding spaces from the reference and title, and convert the reference to uppercase. Save the ticket with a generated ID and status `OPEN`.

Return **201** with the saved ticket and a `Location` header pointing to it. If the reference is already used, return **409 `DUPLICATE_REFERENCE`**. For example, `inc-200` and `INC-200` refer to the same external reference.

### 2. View a ticket

`GET /api/tickets/{id}`

Return **200** with the ticket. If it does not exist, return **404 `NOT_FOUND`**.

### 3. List tickets

`GET /api/tickets`

Return **200** with a JSON array of tickets, ordered by ID from lowest to highest.

- Adding `status=OPEN` returns only open tickets. The other supported statuses work the same way.
- Adding `sort=priorityDesc` puts the highest-priority tickets first. Tickets with equal priority are ordered by ID, lowest first.
- `sort=idAsc` selects the default order. The status and sort options can be used together.
- If no tickets match, return an empty array: `[]`.

### 4. Update a ticket

`PUT /api/tickets/{id}`

The user supplies all three editable fields: `title`, `priority`, and `status`. Save the new values and return **200** with the updated ticket. Keep its original ID and external reference.

Return **404 `NOT_FOUND`** if the ticket does not exist. Invalid input must leave the saved ticket unchanged.

### 5. Delete a ticket

`DELETE /api/tickets/{id}`

Delete the ticket and return **204** with no response body. Return **404 `NOT_FOUND`** if it does not exist. After deletion, its external reference can be used for a new ticket.

Invalid fields, query options, and IDs return **400 `INVALID_REQUEST`**. The exact validation rules and error body are in [API_REFERENCE.md](API_REFERENCE.md); they are part of the assessment.

## Sample interaction

**Create a ticket.** Send `POST /api/tickets` with:

```json
{
  "externalRef": " inc-200 ",
  "title": " Scanner disconnected ",
  "priority": 4
}
```

Expected status: **201**. If the generated ID is `205`, the response body is:

```json
{
  "id": 205,
  "externalRef": "INC-200",
  "title": "Scanner disconnected",
  "priority": 4,
  "status": "OPEN"
}
```

The `Location` header is `/api/tickets/205`. Your application may generate a different ID.

**Resolve it.** Send `PUT /api/tickets/205` with:

```json
{
  "title": "Scanner repaired",
  "priority": 2,
  "status": "RESOLVED"
}
```

Expected status: **200**. The returned ticket has these new values, with the same ID and reference. It no longer appears in `GET /api/tickets?status=OPEN`.

**Delete it.** Send `DELETE /api/tickets/205`. Expect **204** and an empty body. A later `GET /api/tickets/205` returns **404 `NOT_FOUND`**.

## Working on the project

Edit application code under `src/main/java/`, except the [protected files](API_REFERENCE.md#files-you-may-change). Keep the tests and project configuration unchanged.

Run `.\mvnw.cmd test` from this folder. The unchanged starter has **9 failing tests out of 17**; your goal is to pass all 17. See [README.md](README.md) for running the app and checking your full score.
