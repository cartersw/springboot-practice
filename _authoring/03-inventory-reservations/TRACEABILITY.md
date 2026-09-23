# Source-to-test traceability
All test expectations come from the published contract plus the specification test catalog. No hidden business rules are added.
| ID | Visibility | Topic | Test source |
|---|---|---|---|
| A3-01 | public | Create response and protected fields | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_01` |
| A3-02 | public | Committed creation workflow | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_02` |
| A3-03 | public | Unknown stock rolls back | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_03` |
| A3-04 | public | Insufficient stock rolls back | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_04` |
| A3-05 | public | Exact stock depletion | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_05` |
| A3-06 | public | Invalid requests never write | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_06` |
| A3-07 | public | Duplicate items merge | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_07` |
| A3-08 | public | Read committed reservation | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_08` |
| A3-09 | public | Missing and invalid lookup IDs | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_09` |
| A3-10 | public | Identical replay is read only | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_10` |
| A3-11 | public | Changed lines conflict | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_11` |
| A3-12 | public | Cancel restores inventory | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_12` |
| A3-13 | public | Repeated cancellation is read only | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_13` |
| A3-14 | public | Later line failure rolls back | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_14` |
| A3-15 | public | Initial complete inventory summary | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPublicContractTest.java#a3_15` |
| A3-16 | private | Normalized equivalent requests replay | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_16` |
| A3-17 | private | Different customer conflicts | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_17` |
| A3-18 | private | Business failure leaves key reusable | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_18` |
| A3-19 | private | Creation audit failure rolls back and retries | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_19` |
| A3-20 | private | Cancellation audit failure rolls back and retries | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_20` |
| A3-21 | private | Merged quantity uses stock limit | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_21` |
| A3-22 | private | Summary aggregates active reservations only | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_22` |
| A3-23 | private | Missing and invalid cancellation IDs | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_23` |
| A3-24 | private | Request keys retain case | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_24` |
| A3-25 | private | Cancelled replay does not check stock | `reference/src/test/java/dev/practice/assessment03/contract/ReservationPrivateContractTest.java#a3_25` |
