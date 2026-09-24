# Inventory Reservations

Complete a Spring Boot API that lets teams reserve parts and cancel reservations. Reserving parts reduces available stock. Cancelling a reservation puts those parts back.

A user may send the same request more than once. Your application must handle these retries without taking or returning stock twice. Fix the existing project to meet the requirements below and pass the tests.

## Requirements

### 1. Create a reservation

`POST /api/reservations`

The user supplies a `requestKey`, a `customerRef`, and a list of items. Each item contains a `sku` and a `quantity`.

Remove surrounding spaces from the text fields and uppercase each SKU. Combine repeated SKUs into one line by adding their quantities. If all requested stock is available, save an `ACTIVE` reservation, deduct the quantities, and record one `CREATED` event using the supplied audit component.

Return **201** with the reservation and a `Location` header pointing to it. Return **404 `STOCK_NOT_FOUND`** for an unknown SKU, or **409 `INSUFFICIENT_STOCK`** when there are not enough parts. Reserving exactly the available quantity is allowed.

### 2. Handle the same request again

The request key identifies a reservation request. After validating the input, check whether the key has already been used, before checking available stock.

- Same key, same customer and items: return **200** with the existing reservation. Do not deduct stock or record an event again.
- Same key, different customer or item quantities: return **409 `IDEMPOTENCY_CONFLICT`** without changing data.
- Same request after cancellation: return **200** with the existing `CANCELLED` reservation. Do not reserve the parts again.

Item order does not matter. Two lines requesting 1 and 2 of the same SKU mean the same thing as one line requesting 3. Request keys and customer references remain case-sensitive.

### 3. View a reservation

`GET /api/reservations/{id}`

Return **200** with its current status, combined item lines sorted by SKU, and total quantity. Both active and cancelled reservations can be viewed. Return **404 `RESERVATION_NOT_FOUND`** if it does not exist.

### 4. Cancel a reservation

`POST /api/reservations/{id}/cancel`

No body is needed. Change an active reservation to `CANCELLED`, return its quantities to stock, record one `CANCELLED` event, and return **200** with the updated reservation.

If it is already cancelled, return **200** with the same reservation and make no further changes. A missing reservation returns **404 `RESERVATION_NOT_FOUND`**.

### 5. Leave data unchanged when a write fails

Creating or cancelling a reservation must either finish completely or leave all data as it was. A failure must not leave partial stock changes, reservation records, or audit events.

If the supplied audit component fails, return **503 `RESERVATION_UNAVAILABLE`** and undo the entire operation. A failed creation must leave its request key available for another attempt.

### 6. Show the inventory summary

`GET /api/inventory/summary`

Return **200** with every stock item, ordered by SKU. For each item, return its SKU, available quantity, quantity in active reservations, and number of distinct active reservations containing it. Cancelled reservations do not count. Include unused items with zero reserved quantity and zero active reservations.

Invalid input returns **400 `INVALID_REQUEST`**. [API_REFERENCE.md](API_REFERENCE.md) gives the required field limits, response shapes, and error format. Those rules are part of the assessment. Requests are tested sequentially; no external audit service or distributed locking is needed.

## Sample interaction

**Starting stock:** 10 bolts (`BOLT-M8`) and 8 nuts (`NUT-M8`).

**Reserve parts.** Send `POST /api/reservations` with:

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

Expect **201**. If the generated ID is `1000`, the response is:

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

Available stock is now **7 bolts and 6 nuts**. There is one `CREATED` event. Use your actual generated ID in later requests.

**Repeat the request.** Expect **200** with the same reservation. Stock stays at **7 bolts and 6 nuts**; no event is added.

**Cancel it.** Send `POST /api/reservations/1000/cancel`. Expect **200** with status `CANCELLED`. Stock returns to **10 bolts and 8 nuts**, and one `CANCELLED` event is added.

**Cancel it again.** Expect **200**, with no stock change and no additional event.

## Working on the project

Edit application code under `src/main/java/`, except the [protected files](API_REFERENCE.md#files-you-may-change). Keep the tests, configuration, and supplied audit adapter unchanged.

Run `.\mvnw.cmd test` from this folder. The unchanged starter has **8 failing tests out of 17**; your goal is to pass all 17. See [README.md](README.md) for running the app and checking your full score.
