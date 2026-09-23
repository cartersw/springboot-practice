# Source-to-test traceability
All test expectations come from the published contract plus the specification test catalog. No hidden business rules are added.
| ID | Visibility | Topic | Test source |
|---|---|---|---|
| A1-01 | public | Existing ticket representation | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_01` |
| A1-02 | public | Default ordered collection | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_02` |
| A1-03 | public | Create and persist | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_03` |
| A1-04 | public | Normalize create and ignore read only input | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_04` |
| A1-05 | public | Missing ticket | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_05` |
| A1-06 | public | Duplicate reference | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_06` |
| A1-07 | public | Replace mutable fields | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_07` |
| A1-08 | public | Missing update | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_08` |
| A1-09 | public | Delete existing | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_09` |
| A1-10 | public | Missing delete | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_10` |
| A1-11 | public | Status filtering | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_11` |
| A1-12 | public | Priority ordering | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_12` |
| A1-13 | public | Filter and ordering | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_13` |
| A1-14 | public | Invalid create boundaries | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_14` |
| A1-15 | public | Invalid JSON and integer input | `reference/src/test/java/dev/practice/assessment01/contract/TicketPublicContractTest.java#a1_15` |
| A1-16 | private | Required create fields | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_16` |
| A1-17 | private | Normalized title limits | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_17` |
| A1-18 | private | Normalized uniqueness | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_18` |
| A1-19 | private | Reference boundaries | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_19` |
| A1-20 | private | Immutable update fields | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_20` |
| A1-21 | private | Invalid replacement preserves data | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_21` |
| A1-22 | private | Normalized and invalid status query | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_22` |
| A1-23 | private | Invalid sort and path IDs | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_23` |
| A1-24 | private | Empty filtered and empty collection | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_24` |
| A1-25 | private | Reference can be reused after deletion | `reference/src/test/java/dev/practice/assessment01/contract/TicketPrivateContractTest.java#a1_25` |
