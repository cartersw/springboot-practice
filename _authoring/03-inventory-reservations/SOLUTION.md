# Private solution notes

Do not read during an independent attempt. Each mutation below is independently verified; the combined candidate intentionally includes all of them.


## A3-D01

Root cause: Availability rejects `available <= requested` instead of only rejecting `available < requested`, so exact depletion incorrectly fails.

Designated detecting cases: A3-05. Observed failing cases: A3-05.

Author patch: [A3-D01](mutations/A3-D01.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/AvailabilityChecker.java):

```java
available < requested
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D01.json`.


## A3-D02

Root cause: Duplicate normalized SKUs overwrite the earlier quantity with the last input quantity instead of summing.

Designated detecting cases: A3-07, A3-21. Observed failing cases: A3-07, A3-16, A3-21.

Author patch: [A3-D02](mutations/A3-D02.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
merged.merge(sku,item.quantity(),Integer::sum);
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D02.json`.


## A3-D03

Root cause: SKU normalization strips whitespace but omits uppercase conversion. Keep syntactic validation case-permissive long enough that this produces an ordinary incorrect unknown-SKU response, not an unexpected parsing exception. The correct implementation normalizes before applying the uppercase SKU pattern.

Designated detecting cases: A3-16. Observed failing cases: A3-16.

Author patch: [A3-D03](mutations/A3-D03.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
required(item.sku(),32).toUpperCase(Locale.ROOT)
```


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
sku.matches("[A-Z0-9-]+")
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D03.json`.


## A3-D04

Root cause: Remove the workflow transaction from `ReservationService.create`, while leaving each Spring Data repository save operational. Individual saves can commit before a later failure. Keep DTO loading and repository queries valid so this causes partial persistence, not a startup or lazy-loading failure.

Designated detecting cases: A3-14, A3-19. Observed failing cases: A3-03, A3-04, A3-14, A3-18, A3-19, A3-21.

Author patch: [A3-D04](mutations/A3-D04.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/ReservationService.java):

```java
@Transactional
 public CreateReservationOutcome create
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D04.json`.


## A3-D05

Root cause: Creation controller always responds 201, ignoring the correct service outcome's `isNew` flag. A replay should instead be 200.

Designated detecting cases: A3-10. Observed failing cases: A3-10, A3-16, A3-24, A3-25.

Author patch: [A3-D05](mutations/A3-D05.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/controller/ReservationController.java):

```java
ResponseEntity.status(outcome.isNew()?201:200)
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D05.json`.


## A3-D06

Root cause: Existing-key comparison checks normalized items but not customerRef. A different customer with the same key/items is wrongly accepted as a replay.

Designated detecting cases: A3-17. Observed failing cases: A3-17.

Author patch: [A3-D06](mutations/A3-D06.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/normalization/ReservationRequestNormalizer.java):

```java
public boolean samePayload(String saved,String incoming){return saved.equals(incoming);}
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D06.json`.


## A3-D07

Root cause: Cancellation lacks the already-cancelled early return; it restores quantities and records another cancellation event on every call. Keep cancellation's transaction intact.

Designated detecting cases: A3-13. Observed failing cases: A3-13.

Author patch: [A3-D07](mutations/A3-D07.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/service/ReservationService.java):

```java
if(r.getStatus()==ReservationStatus.CANCELLED)return response(r);
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D07.json`.


## A3-D08

Root cause: Summary uses inner joins from stock to lines/reservations, includes cancelled reservations, uses COUNT(line.id) for reservedQuantity, and counts reservation rows rather than the required distinct active reservation IDs. This deliberately incorrect aggregate query is the incomplete summary feature.

Designated detecting cases: A3-15, A3-22. Observed failing cases: A3-15, A3-22.

Author patch: [A3-D08](mutations/A3-D08.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment03/repository/InventorySummaryRepository.java):

```java
select s.sku,s.available_quantity,coalesce(sum(case when r.status='ACTIVE' then l.quantity else 0 end),0) reserved_quantity,count(distinct case when r.status='ACTIVE' then r.id end) active_reservations from stock_items s left join reservation_lines l on l.sku=s.sku left join reservations r on r.id=l.reservation_id group by s.sku,s.available_quantity order by s.sku
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A3-D08.json`.


## Common incorrect repairs

Do not change test expectations or HTTP error handling to conceal behavioral differences. A repository-level save transaction is not a substitute for a complete workflow boundary. Tests deliberately observe committed state without `@Transactional` on test classes.

For catalog metadata, a page length is not the filtered total. Invalidating one concrete key cannot invalidate all result variants; clearing unrelated namespaces violates the contract. Cache hits are observed through the supplied gateway counter, not elapsed time.

Never verify rollback inside a test-managed transaction: that can mask missing application boundaries. Both creation and cancellation audit failures are tested independently. Exact generated sequence values are not part of the contract.
