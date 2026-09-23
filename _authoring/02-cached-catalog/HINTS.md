# Private graded hints

Reveal only the requested level when explicitly asked.


## A2-D01

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: When both q and category are supplied, their two predicates combine with OR instead of AND. Other filters still combine with the resulting predicate using AND. A single q or category predicate behaves correctly. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
filters.add("("+q+" and "+category+")")
```


## A2-D02

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Minimum price uses `>` instead of `>=`. Maximum price remains inclusive. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
p.priceCents >= :min
```


## A2-D03

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Database page selection uses `max(0, requestedPage - 1)`, treating positive page numbers as one-based. Keep the response's `page` field equal to the originally requested value. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
int selectedPage=c.page();
```


## A2-D04

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: priceDesc sorts by price descending **and ID descending**, incorrectly reversing its tie-breaker. Other sort modes remain correct. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
p.priceCents desc, p.id asc
```


## A2-D05

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Response totalElements is set to current content length and totalPages is derived from that incorrect number. Keep `page` and `size` as requested; first/last derive from the supplied metadata. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/repository/ProductSearchRepository.java):

```java
long total=count.getSingleResult();
```


## A2-D06

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/cache/SearchKeyFactory.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Cache key includes category, minPrice, and maxPrice, but omits q, inStock, page, size, and sort. The key prefix is correct. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/cache/SearchKeyFactory.java):

```java
Arrays.asList(c.q(),c.category(),c.minPrice(),c.maxPrice(),c.inStock(),c.page(),c.size(),c.sort())
```


## A2-D07

1. Navigation: follow the request into `src/main/java/dev/practice/assessment02/cache/SearchCacheInvalidator.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: SearchCacheInvalidator calls exact-key `delete("products:search:v1:")` once instead of deleting matching keys. This is the incomplete invalidation feature. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment02/cache/SearchCacheInvalidator.java):

```java
for(String key:store.keys())if(key.startsWith("products:search:v1:"))store.delete(key);
```
