# Comparison of the two classifications (A3)

- objects: 24249; with a valid decision from both: 24249
- matching decisions: 3007 of 24249 = 12.40 %
- Cohen's kappa: 0.11479
- rows for adjudication (different decisions, or a gap / MIXED from at least one): 21251

## Decisions (rows: c1, columns: c2)

| c1 \ c2 | ACTION | GAP-TWO | INSTALLED-DERIVED | INSTALLED-OWN | INSTALLED-PACKAGE | MATERIAL | MIXED | PROGRAM-DERIVED | PROGRAM-OWN | RECORD | RUNTIME | SETTING-DEFAULT | SETTING-OWN | UNKNOWN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACTION | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GAP-TWO | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-DERIVED | 0 | 0 | 115 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-OWN | 0 | 0 | 0 | 451 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-PACKAGE | 0 | 0 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 |
| MATERIAL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MIXED | 0 | 0 | 0 | 0 | 1 | 0 | 9 | 0 | 0 | 6 | 1 | 0 | 0 | 0 |
| PROGRAM-DERIVED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 69 | 2 | 0 | 0 | 0 | 0 | 0 |
| PROGRAM-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| RECORD | 31 | 0 | 0 | 0 | 2 | 69 | 1 | 0 | 0 | 384 | 20 | 0 | 1 | 0 |
| RUNTIME | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1880 | 0 | 0 | 0 |
| SETTING-DEFAULT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SETTING-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14 | 0 |
| UNKNOWN | 0 | 14918 | 96 | 7 | 2462 | 276 | 582 | 337 | 947 | 1389 | 10 | 61 | 20 | 61 |

## By kind (objects / matching)

| kind | objects | matching |
|---|---|---|
| 2:code-ownership-unresolved | 14672 | 140 |
| 2:stored-ownership-unresolved | 6805 | 447 |
| 1:package | 734 | 566 |
| 1:firewall-rule | 469 | 469 |
| 2:stored-outside-packages | 366 | 279 |
| 1:firewall-ipv4 | 288 | 267 |
| 1:firewall-chain | 271 | 271 |
| 1:process | 230 | 230 |
| 1:firewall-ipv6 | 106 | 91 |
| 2:executable-code-outside-packages | 80 | 71 |
| 1:module-name | 53 | 53 |
| 1:port | 44 | 44 |
| 1:timer | 28 | 18 |
| 1:service | 25 | 10 |
| 1:unit-file | 16 | 13 |
| 1:firewall-table | 14 | 14 |
| 2:image-container-store | 8 | 5 |
| 1:group | 6 | 2 |
| 1:user-service | 5 | 2 |
| 1:user-unit-file | 5 | 2 |
| 1:docker-container | 4 | 3 |
| 1:docker-image | 4 | 0 |
| 1:user-timer | 4 | 4 |
| 1:saved-network | 3 | 0 |
| 1:sudo-access | 3 | 1 |
| 1:access-rule | 3 | 3 |
| 1:account | 2 | 1 |
| 1:firewall-ct helper | 1 | 1 |

## Problems of form

- none
