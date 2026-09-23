# Private graded hints

Reveal only the requested level when explicitly asked.


## A1-D01

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/controller/TicketController.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: POST persists correctly but returns 200 instead of 201. Keep its response DTO and Location header otherwise correct. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/controller/TicketController.java):

```java
ResponseEntity.status(201)
```


## A1-D02

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: GET by a missing positive ID returns 200 with an empty body instead of a 404 error. Existing lookup remains correct. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
public TicketResponse get(long id){return mapper.response(find(id));}
```


## A1-D03

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: The service's duplicate-reference precheck is missing. Retain the database uniqueness constraint; a duplicate write reaches the constraint and is mapped to a 500 envelope by the generic handler instead of the required 409 domain response. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
if(repository.existsByExternalRef(ref))throw new DuplicateReferenceException();
```


## A1-D04

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: PUT applies title and priority but never applies the requested status. Validation of the status input remains correct. This is the first incomplete feature. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
t.setTitle(title);t.setPriority(priority);t.setStatus(status);
```


## A1-D05

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: List requests validate `status` but fail to apply the status filter. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
.filter(t->status==null||t.getStatus()==status)
```


## A1-D06

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: `priorityDesc` is implemented with priority ascending; its ID tie-breaker is ascending. Default `idAsc` remains correct. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
Comparator.comparing(Ticket::getPriority).reversed().thenComparing(Ticket::getId)
```


## A1-D07

1. Navigation: follow the request into `src/main/java/dev/practice/assessment01/service/TicketService.java`.

2. Concept: compare this component with the relevant endpoint contract and the public case topic; observe HTTP output and committed state separately.

3. Detailed repair: Deleting a nonexistent positive ID is treated as a successful no-op with 204. Existing deletion still works. The correct reference fragments below restore the published behavior.


Reference fragment in [source](reference/src/main/java/dev/practice/assessment01/service/TicketService.java):

```java
public void delete(long id){Ticket t=find(id);repository.delete(t);}
```
