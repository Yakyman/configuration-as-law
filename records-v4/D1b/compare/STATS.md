# Comparison of the two classifications (D1b)

- objects: 34708; with a valid decision from both: 34708
- matching decisions: 5074 of 34708 = 14.62 %
- Cohen's kappa: 0.08855
- rows for adjudication (different decisions, or a gap / MIXED from at least one): 30024

## Decisions (rows: c1, columns: c2)

| c1 \ c2 | GAP-TWO | INSTALLED-DERIVED | INSTALLED-OWN | INSTALLED-PACKAGE | MATERIAL | MIXED | PROGRAM-DERIVED | PROGRAM-OWN | RECORD | RUNTIME | SETTING-DEFAULT | SETTING-OWN | UNKNOWN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-TWO | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-DERIVED | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-OWN | 0 | 0 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-PACKAGE | 0 | 0 | 0 | 1895 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| MATERIAL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MIXED | 0 | 0 | 0 | 138 | 0 | 390 | 0 | 0 | 66 | 0 | 0 | 0 | 0 |
| PROGRAM-DERIVED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| PROGRAM-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| RECORD | 0 | 0 | 0 | 27 | 0 | 0 | 0 | 0 | 272 | 29 | 1 | 0 | 0 |
| RUNTIME | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 621 | 0 | 0 | 0 |
| SETTING-DEFAULT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SETTING-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| UNKNOWN | 7450 | 0 | 0 | 265 | 1 | 20378 | 1120 | 7 | 31 | 6 | 76 | 33 | 1880 |

## By kind (objects / matching)

| kind | objects | matching |
|---|---|---|
| L2:stored-ownership-unresolved | 31059 | 2782 |
| L2:code-ownership-unresolved | 1622 | 579 |
| L2:stored-outside-packages | 453 | 449 |
| L1:package | 440 | 387 |
| L1:unit-file | 246 | 242 |
| L1:module-name | 203 | 203 |
| L1:process | 159 | 159 |
| L1:driver | 127 | 127 |
| L1:group | 68 | 20 |
| L1:openrc-runlevel | 60 | 0 |
| L1:openrc-service | 47 | 0 |
| L1:firewall-ipv4 | 40 | 28 |
| L1:firewall-ipv6 | 29 | 21 |
| L1:access-rule | 29 | 27 |
| L1:account | 22 | 2 |
| L2:stored-ownership-unknown | 19 | 2 |
| L1:sudo-access | 14 | 5 |
| L1:user-unit-file | 14 | 13 |
| L1:container-image | 12 | 0 |
| L2:image | 11 | 8 |
| L2:executable-code-outside-packages | 10 | 10 |
| L2:opaque-directory | 6 | 3 |
| L2:code-ownership-unknown | 6 | 0 |
| L2:image-container-store | 5 | 3 |
| L1:port | 4 | 4 |
| L1:docker-container | 1 | 0 |
| L1:docker-image | 1 | 0 |
| L2:snapshot | 1 | 0 |

## Problems of form

- none
