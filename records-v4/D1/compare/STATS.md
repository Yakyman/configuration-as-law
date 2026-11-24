# Comparison of the two classifications (D1)

- objects: 16375; with a valid decision from both: 16375
- matching decisions: 8677 of 16375 = 52.99 %
- Cohen's kappa: 0.45940
- rows for adjudication (different decisions, or a gap / MIXED from at least one): 7708

## Decisions (rows: c1, columns: c2)

| c1 \ c2 | GAP-NONE | GAP-TWO | INSTALLED-DERIVED | INSTALLED-OWN | INSTALLED-PACKAGE | MATERIAL | MIXED | PROGRAM-DERIVED | PROGRAM-OWN | RECORD | RUNTIME | SETTING-DEFAULT | SETTING-OWN | UNKNOWN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-NONE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| GAP-TWO | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-DERIVED | 0 | 0 | 1703 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |
| INSTALLED-OWN | 0 | 0 | 0 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| INSTALLED-PACKAGE | 0 | 0 | 0 | 0 | 1605 | 0 | 0 | 8 | 0 | 0 | 5 | 160 | 0 | 2 |
| MATERIAL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MIXED | 0 | 3 | 0 | 0 | 96 | 0 | 10 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| PROGRAM-DERIVED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 101 | 0 | 0 | 0 | 0 | 2 | 0 |
| PROGRAM-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| RECORD | 0 | 30 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1078 | 38 | 0 | 0 | 6 |
| RUNTIME | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3497 | 0 | 0 | 0 |
| SETTING-DEFAULT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 |
| SETTING-OWN | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 13 | 0 |
| UNKNOWN | 0 | 1117 | 301 | 2 | 4838 | 4 | 82 | 172 | 5 | 204 | 320 | 226 | 36 | 587 |

## By kind (objects / matching)

| kind | objects | matching |
|---|---|---|
| L2:stored-ownership-unresolved | 3676 | 1916 |
| L2:stored-outside-packages | 3174 | 603 |
| L1:package | 2484 | 2020 |
| L2:executable-code-outside-packages | 1874 | 10 |
| L1:process | 1574 | 1468 |
| L1:module-name | 610 | 610 |
| L1:unit-file | 559 | 179 |
| L1:polkit-action | 455 | 455 |
| L1:service | 331 | 167 |
| L1:driver | 303 | 303 |
| L1:firewall-rule | 206 | 206 |
| L1:access-rule | 155 | 153 |
| L1:group | 130 | 25 |
| L1:firewall-chain | 127 | 127 |
| L1:user-unit-file | 121 | 75 |
| L1:socket | 66 | 66 |
| L1:account | 58 | 6 |
| L2:image | 48 | 27 |
| L2:code-ownership-unresolved | 46 | 11 |
| L1:network-state | 42 | 42 |
| L1:firewall-ipv4 | 40 | 28 |
| L1:sudo-access | 36 | 12 |
| L2:stored-ownership-unknown | 35 | 3 |
| L1:firewall-ipv6 | 29 | 21 |
| L1:timer | 19 | 19 |
| L1:user-service | 18 | 7 |
| L1:mount-resource | 18 | 18 |
| L1:port | 17 | 13 |
| L1:runit-service | 15 | 0 |
| L1:container-image | 14 | 12 |
| L1:saved-network | 13 | 8 |
| L1:mount | 13 | 13 |
| L1:network-configuration | 11 | 11 |
| L2:opaque-directory | 11 | 6 |
| L1:kernel-module | 10 | 10 |
| L1:saved-network-file | 7 | 7 |
| L2:code-ownership-unknown | 7 | 6 |
| L2:image-container-store | 6 | 3 |
| L1:container | 4 | 2 |
| L1:block-device | 4 | 4 |
| L1:user-timer | 3 | 3 |
| L1:firewall-table | 2 | 2 |
| L2:snapshot | 2 | 0 |
| L1:docker-container | 1 | 0 |
| L1:docker-image | 1 | 0 |

## Problems of form

- none
