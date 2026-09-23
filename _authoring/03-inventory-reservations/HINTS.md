# Private graded hints

Reveal only the requested level when explicitly asked.


## A3-D01

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/service/AvailabilityChecker.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Availability rejects `available <= requested` instead of only rejecting `available < requested`, so exact depletion incorrectly fails. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/AvailabilityChecker.java):

```java
available < requested
```


## A3-D02

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Duplicate normalized SKUs overwrite the earlier quantity with the last input quantity instead of summing. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
merged.merge(sku,item.quantity(),Integer::sum);
```


## A3-D03

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: SKU normalization strips whitespace but omits uppercase conversion. Keep syntactic validation case-permissive long enough that this produces an ordinary incorrect unknown-SKU response, not an unexpected parsing exception. The correct implementation normalizes before applying the uppercase SKU pattern. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
required(item.sku(),32).toUpperCase(Locale.ROOT)
```


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
sku.matches("[A-Z0-9-]+")
```


## A3-D04

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/service/ReservationService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Remove the workflow transaction from `ReservationService.create`, while leaving each Spring Data repository save operational. Individual saves can commit before a later failure. Keep DTO loading and repository queries valid so this causes partial persistence, not a startup or lazy-loading failure. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/ReservationService.java):

```java
@Transactional
 public CreateReservationOutcome create
```


## A3-D05

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/controller/ReservationController.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Creation controller always responds 201, ignoring the correct service outcome's `isNew` flag. A replay should instead be 200. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/controller/ReservationController.java):

```java
ResponseEntity.status(outcome.isNew()?201:200)
```


## A3-D06

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Existing-key comparison checks normalized items but not customerRef. A different customer with the same key/items is wrongly accepted as a replay. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
public boolean samePayload(String saved,String incoming){return saved.equals(incoming);}
```


## A3-D07

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/service/ReservationService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Cancellation lacks the already-cancelled early return; it restores quantities and records another cancellation event on every call. Keep cancellation's transaction intact. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/ReservationService.java):

```java
if(r.getStatus()==ReservationStatus.CANCELLED)return response(r);
```


## A3-D08

1. Navigation: follow the request into `src/main/java/dev/practice/assessment03/repository/InventorySummaryRepository.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Summary uses inner joins from stock to lines/reservations, includes cancelled reservations, uses COUNT(line.id) for reservedQuantity, and counts reservation rows rather than the required distinct active reservation IDs. This deliberately incorrect aggregate query is the incomplete summary feature. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/repository/InventorySummaryRepository.java):

```java
select s.sku,s.available_quantity,coalesce(sum(case when r.status='ACTIVE' then l.quantity else 0 end),0) reserved_quantity,count(distinct case when r.status='ACTIVE' then r.id end) active_reservations from stock_items s left join reservation_lines l on l.sku=s.sku left join reservations r on r.id=l.reservation_id group by s.sku,s.available_quantity order by s.sku
```
