# Source-to-test traceability
All test expectations come from the published contract plus the specification test catalog. No hidden business rules are added.
| ID | Visibility | Topic | Test source |
|---|---|---|---|
| A2-01 | public | Default page shape and totals | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_01` |
| A2-02 | public | Combined name and category filters | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_02` |
| A2-03 | public | Blank and unknown filters | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_03` |
| A2-04 | public | Normalized search text | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_04` |
| A2-05 | public | Inclusive price bounds | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_05` |
| A2-06 | public | Stock predicates | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_06` |
| A2-07 | public | Second page and metadata | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_07` |
| A2-08 | public | Descending price ties | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_08` |
| A2-09 | public | Name ordering | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_09` |
| A2-10 | public | Out of range page | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_10` |
| A2-11 | public | Empty search page | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_11` |
| A2-12 | public | Invalid searches have no effects | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_12` |
| A2-13 | public | Cache reuses populated and empty responses | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_13` |
| A2-14 | public | Successful writes refresh searches | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_14` |
| A2-15 | public | Failed writes preserve cache and rows | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPublicContractTest.java#a2_15` |
| A2-16 | private | Page and size cache separation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_16` |
| A2-17 | private | Search term cache separation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_17` |
| A2-18 | private | Stock cache separation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_18` |
| A2-19 | private | Sort cache separation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_19` |
| A2-20 | private | Price bound cache separation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_20` |
| A2-21 | private | Equivalent requests share entries | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_21` |
| A2-22 | private | Exact expiry without sliding reads | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_22` |
| A2-23 | private | Exact namespace invalidation | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_23` |
| A2-24 | private | Last and very distant pages | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_24` |
| A2-25 | private | Literal search and strict write boundaries | `reference/src/test/java/dev/practice/assessment02/contract/CatalogPrivateContractTest.java#a2_25` |
