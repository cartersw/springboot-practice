# Parts Catalog

Complete a Spring Boot API that lets users search a parts catalog and update products. Searches should return the right products, and repeated searches should reuse saved results until those results expire or a product changes.

The project already includes the database, sample products, and an in-memory cache. Fix the existing application to meet the following requirements and pass the tests.

## Requirements

Each product has an `id`, `sku`, `name`, `category`, `priceCents`, and `stock`. Prices are whole-number cents: `2500` means 25.00. Stock is the number of available units.

### 1. Search products

`GET /api/products`

Support these optional filters. When several are supplied, a product must match all of them.

- `q`: the product name contains this text, ignoring case. Treat `%` and `_` as ordinary characters.
- `category`: the category matches this value, ignoring case.
- `minPrice` and `maxPrice`: the price falls within these inclusive bounds.
- `inStock=true`: stock is greater than zero. `inStock=false`: stock is zero.

Ignore surrounding spaces and case in `q` and `category`. A blank value for either means no filter.

### 2. Sort and return one page

Sort matching products before selecting the requested page.

- `sort=priceAsc`: lowest price first. This is the default.
- `sort=priceDesc`: highest price first.
- `sort=nameAsc`: alphabetical name order, ignoring case.

For every sort, break ties using ID from lowest to highest. `page` starts at **0**, and `size` defaults to **5**. Return **200** with the products on that page, the total number of matches, the total number of pages, and whether this is the first or last page. An empty result or a page beyond the results still returns **200**.

### 3. Reuse repeated searches

Save each successful search response, including empty pages, for **60 seconds**. Repeating an equivalent search before expiry must return that response without another database search. Reading a saved response does not extend its lifetime.

Different filters, pages, sizes, or sorts must have separate cache entries. Equivalent requests, such as omitted defaults versus explicit defaults, must share an entry. Use the supplied cache, clock, and database query gateway.

### 4. Update a product

`PUT /api/products/{id}`

The user supplies `name`, `category`, `priceCents`, and `stock`. Validate and save all four fields, then return **200** with the complete product. Keep its original ID and SKU.

After every successful update, including an update that leaves values the same, remove all product-search cache entries. The next search must see current data. Preserve unrelated cache entries.

Return **404 `NOT_FOUND`** for a missing product. Invalid requests return **400 `INVALID_REQUEST`**. Failed updates must leave products and valid cache entries unchanged; invalid searches must not query the database or create cache entries.

[API_REFERENCE.md](API_REFERENCE.md) contains the required field limits, page calculations, cache-key rules, and error format. These are part of the assessment. You do not need to install Redis or add other product endpoints.

## Sample interaction

**Search.** With the supplied sample data, send:

```http
GET /api/products?category=electronics&inStock=true&size=2
```

Expected status: **200**. Expected body:

```json
{
  "content": [
    {"id": 110, "sku": "CB-01", "name": "USB-C Cable", "category": "electronics", "priceCents": 1000, "stock": 12},
    {"id": 103, "sku": "MS-01", "name": "Wireless Mouse", "category": "electronics", "priceCents": 2500, "stock": 8}
  ],
  "page": 0,
  "size": 2,
  "totalElements": 4,
  "totalPages": 2,
  "first": true,
  "last": false
}
```

Four products match. The response contains the two cheapest. Mouse `103` comes before equally priced mouse `104` because its ID is lower.

**Repeat the search.** Send the same request within 60 seconds. Expect the same response and no new call to the database query gateway.

**Update a product.** Send `PUT /api/products/110` with:

```json
{
  "name": "USB-C Cable",
  "category": "electronics",
  "priceCents": 1000,
  "stock": 0
}
```

Expect **200**. Repeat the search: it must now query the database, report **3** matches, and return products **103** and **104** on the first page. Product `110` is out of stock.

## Working on the project

Edit application code under `src/main/java/`, except the [protected files](API_REFERENCE.md#files-you-may-change). Keep the tests, configuration, and supplied adapters unchanged.

Run `.\mvnw.cmd test` from this folder. The unchanged starter has **8 failing tests out of 17**; your goal is to pass all 17. See [README.md](README.md) for running the app and checking your full score.
