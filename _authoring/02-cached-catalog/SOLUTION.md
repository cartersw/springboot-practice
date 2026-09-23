# Private solution notes

Do not read during an independent attempt. Each mutation below is independently verified; the combined candidate intentionally includes all of them.


## A2-D01

Root cause: When both q and category are supplied, their two predicates combine with OR instead of AND. Other filters still combine with the resulting predicate using AND. A single q or category predicate behaves correctly.

Designated detecting cases: A2-02. Observed failing cases: A2-02, A2-04, A2-17, A2-21.

Author patch: [A2-D01](mutations/A2-D01.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
filters.add("("+q+" and "+category+")")
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D01.json`.


## A2-D02

Root cause: Minimum price uses `>` instead of `>=`. Maximum price remains inclusive.

Designated detecting cases: A2-05. Observed failing cases: A2-05, A2-20.

Author patch: [A2-D02](mutations/A2-D02.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
p.priceCents >= :min
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D02.json`.


## A2-D03

Root cause: Database page selection uses `max(0, requestedPage - 1)`, treating positive page numbers as one-based. Keep the response's `page` field equal to the originally requested value.

Designated detecting cases: A2-07, A2-16. Observed failing cases: A2-07, A2-16, A2-24.

Author patch: [A2-D03](mutations/A2-D03.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
int selectedPage=c.page();
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D03.json`.


## A2-D04

Root cause: priceDesc sorts by price descending **and ID descending**, incorrectly reversing its tie-breaker. Other sort modes remain correct.

Designated detecting cases: A2-08. Observed failing cases: A2-08, A2-19.

Author patch: [A2-D04](mutations/A2-D04.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
p.priceCents desc, p.id asc
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D04.json`.


## A2-D05

Root cause: Response totalElements is set to current content length and totalPages is derived from that incorrect number. Keep `page` and `size` as requested; first/last derive from the supplied metadata.

Designated detecting cases: A2-01, A2-10, A2-24. Observed failing cases: A2-01, A2-07, A2-10, A2-24.

Author patch: [A2-D05](mutations/A2-D05.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
long total=count.getSingleResult();
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D05.json`.


## A2-D06

Root cause: Cache key includes category, minPrice, and maxPrice, but omits q, inStock, page, size, and sort. The key prefix is correct.

Designated detecting cases: A2-16, A2-17, A2-18, A2-19. Observed failing cases: A2-16, A2-17, A2-18, A2-19.

Author patch: [A2-D06](mutations/A2-D06.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/cache/SearchKeyFactory.java):

```java
Arrays.asList(c.q(),c.category(),c.minPrice(),c.maxPrice(),c.inStock(),c.page(),c.size(),c.sort())
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D06.json`.


## A2-D07

Root cause: SearchCacheInvalidator calls exact-key `delete("products:search:v1:")` once instead of deleting matching keys. This is the incomplete invalidation feature.

Designated detecting cases: A2-14, A2-23. Observed failing cases: A2-14, A2-23.

Author patch: [A2-D07](mutations/A2-D07.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/cache/SearchCacheInvalidator.java):

```java
for(String key:store.keys())if(key.startsWith("products:search:v1:"))store.delete(key);
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A2-D07.json`.


## Common incorrect repairs

Do not change test expectations or HTTP error handling to conceal behavioral differences. A repository-level save transaction is not a substitute for a complete workflow boundary. Tests deliberately observe committed state without `@Transactional` on test classes.

For catalog metadata, a page length is not the filtered total. Invalidating one concrete key cannot invalidate all result variants; clearing unrelated namespaces violates the contract. Cache hits are observed through the supplied gateway counter, not elapsed time.

Never verify rollback inside a test-managed transaction: that can mask missing application boundaries. Both creation and cancellation audit failures are tested independently. Exact generated sequence values are not part of the contract.
