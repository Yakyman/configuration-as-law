# Comparison of the two classifications (D1)

- objects: 16524; with a valid decision from both: 16524
- matching decisions: 15025 of 16524 = 90.93 %
- Cohen's kappa: 0.55586
- rows for adjudication (different decisions, or HOLE / MIXED from at least one): 1843

## Decisions (rows: c1, columns: c2)

| c1 \ c2 | HOLE | MIXED | MUST | NOT | UNKNOWN |
|---|---|---|---|---|---|
| HOLE | 306 | 0 | 142 | 28 | 3 |
| MIXED | 0 | 38 | 0 | 1 | 6 |
| MUST | 203 | 10 | 14073 | 235 | 344 |
| NOT | 103 | 3 | 219 | 550 | 13 |
| UNKNOWN | 10 | 1 | 102 | 76 | 58 |

## By kind (objects / matching)

| kind | objects | matching |
|---|---|---|
| L1:package:rpm | 8734 | 8146 |
| L1:package:dpkg-query | 1905 | 1760 |
| L1:unit-file | 1089 | 1089 |
| L1:polkit-actions | 982 | 982 |
| L1:service | 522 | 483 |
| L2:executable-code-outside-packages | 466 | 264 |
| L2:stored-outside-packages | 386 | 147 |
| L1:firewall-rule | 343 | 343 |
| L1:group | 278 | 148 |
| L1:user-unit-file | 232 | 225 |
| L1:firewall-chain | 223 | 223 |
| L1:module | 208 | 208 |
| L1:package:gem | 190 | 190 |
| L1:account | 168 | 168 |
| L1:process | 166 | 111 |
| L1:driver | 152 | 123 |
| L1:access-rule | 132 | 77 |
| L1:package:pip | 90 | 90 |
| L1:package:pip3 | 90 | 90 |
| L1:user-service | 65 | 60 |
| L1:timer | 28 | 28 |
| L1:port | 26 | 26 |
| L1:package:flatpak | 15 | 11 |
| L1:network | 10 | 9 |
| L1:user-timer | 8 | 8 |
| L1:network-link | 6 | 6 |
| L1:firewall-table | 2 | 2 |
| L1:container | 2 | 2 |
| L1:container-image | 2 | 2 |
| L1:firewall-ct helper | 1 | 1 |
| L1:package:system-image | 1 | 1 |
| L1:login-key | 1 | 1 |
| L1:saved-network | 1 | 1 |

## Problems of form

- none
