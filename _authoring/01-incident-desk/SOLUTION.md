# Private solution notes

Do not read during an independent attempt. Each mutation below is independently verified; the combined candidate intentionally includes all of them.


## A1-D01

Root cause: POST persists correctly but returns 200 instead of 201. Keep its response DTO and Location header otherwise correct.

Designated detecting cases: A1-03. Observed failing cases: A1-03, A1-04, A1-17, A1-19, A1-25.

Author patch: [A1-D01](mutations/A1-D01.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/controller/TicketController.java):

```java
ResponseEntity.status(201)
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D01.json`.


## A1-D02

Root cause: GET by a missing positive ID returns 200 with an empty body instead of a 404 error. Existing lookup remains correct.

Designated detecting cases: A1-05. Observed failing cases: A1-05.

Author patch: [A1-D02](mutations/A1-D02.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
public TicketResponse get(long id){return mapper.response(find(id));}
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D02.json`.


## A1-D03

Root cause: The service's duplicate-reference precheck is missing. Retain the database uniqueness constraint; a duplicate write reaches the constraint and is mapped to a 500 envelope by the generic handler instead of the required 409 domain response.

Designated detecting cases: A1-06, A1-18. Observed failing cases: A1-06, A1-18.

Author patch: [A1-D03](mutations/A1-D03.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
if(repository.existsByExternalRef(ref))throw new DuplicateReferenceException();
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D03.json`.


## A1-D04

Root cause: PUT applies title and priority but never applies the requested status. Validation of the status input remains correct. This is the first incomplete feature.

Designated detecting cases: A1-07. Observed failing cases: A1-07.

Author patch: [A1-D04](mutations/A1-D04.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
t.setTitle(title);t.setPriority(priority);t.setStatus(status);
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D04.json`.


## A1-D05

Root cause: List requests validate `status` but fail to apply the status filter.

Designated detecting cases: A1-11, A1-13. Observed failing cases: A1-11, A1-13, A1-22, A1-24.

Author patch: [A1-D05](mutations/A1-D05.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
.filter(t->status==null||t.getStatus()==status)
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D05.json`.


## A1-D06

Root cause: `priorityDesc` is implemented with priority ascending; its ID tie-breaker is ascending. Default `idAsc` remains correct.

Designated detecting cases: A1-12. Observed failing cases: A1-12, A1-13.

Author patch: [A1-D06](mutations/A1-D06.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
Comparator.comparing(Ticket::getPriority).reversed().thenComparing(Ticket::getId)
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D06.json`.


## A1-D07

Root cause: Deleting a nonexistent positive ID is treated as a successful no-op with 204. Existing deletion still works.

Designated detecting cases: A1-10. Observed failing cases: A1-10.

Author patch: [A1-D07](mutations/A1-D07.patch) (reference → starter; reverse only in separate solution work).


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
public void delete(long id){Ticket t=find(id);repository.delete(t);}
```

The reference restores the operation, status, predicate, identity, or workflow boundary stated in ASSESSMENT.md; the private variants test the same published rule. Evidence is saved under `../verification/A1-D07.json`.


## Common incorrect repairs

Do not change test expectations or HTTP error handling to conceal behavioral differences. A repository-level save transaction is not a substitute for a complete workflow boundary. Tests deliberately observe committed state without `@Transactional` on test classes.

For catalog metadata, a page length is not the filtered total. Invalidating one concrete key cannot invalidate all result variants; clearing unrelated namespaces violates the contract. Cache hits are observed through the supplied gateway counter, not elapsed time.

Never verify rollback inside a test-managed transaction: that can mask missing application boundaries. Both creation and cancellation audit failures are tested independently. Exact generated sequence values are not part of the contract.
