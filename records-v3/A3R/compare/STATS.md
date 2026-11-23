# Comparison of the two classifications (A3R)

- objects: 5212; with a valid decision from both: 5212
- matching decisions: 3854 of 5212 = 73.94 %
- Cohen's kappa: 0.55445
- rows for adjudication (different decisions, or HOLE / MIXED from at least one): 2010

## Decisions (rows: c1, columns: c2)

| c1 \ c2 | HOLE | MIXED | MUST | NOT | UNKNOWN |
|---|---|---|---|---|---|
| HOLE | 73 | 10 | 830 | 18 | 1 |
| MIXED | 0 | 579 | 19 | 27 | 0 |
| MUST | 80 | 21 | 2606 | 24 | 11 |
| NOT | 2 | 37 | 173 | 591 | 3 |
| UNKNOWN | 1 | 3 | 86 | 12 | 5 |

## By kind (objects / matching)

| kind | objects | matching |
|---|---|---|
| stored-outside-packages | 1377 | 1168 |
| package-environment-evidence | 964 | 21 |
| executable-code-outside-packages | 955 | 951 |
| package:npm | 640 | 634 |
| stored-outside-packages:subtree | 223 | 179 |
| polkit-actions | 219 | 219 |
| python-distribution | 172 | 172 |
| access-rule | 145 | 89 |
| process | 88 | 66 |
| group | 68 | 29 |
| executable-code-outside-packages:subtree | 54 | 24 |
| user-unit-file | 51 | 51 |
| account | 40 | 40 |
| driver | 35 | 35 |
| port | 30 | 30 |
| firewall-rule | 21 | 21 |
| package:flatpak | 20 | 20 |
| service | 20 | 20 |
| user-service | 18 | 18 |
| firewall-chain | 16 | 16 |
| container-image | 12 | 12 |
| container | 8 | 8 |
| package:go | 6 | 6 |
| network | 6 | 6 |
| unit-file | 5 | 5 |
| network-link | 5 | 2 |
| firewall-table | 3 | 3 |
| saved-network | 3 | 3 |
| package:pipx | 2 | 2 |
| user-timer | 1 | 1 |
| timer | 1 | 0 |
| cron | 1 | 1 |
| package:cargo | 1 | 1 |
| package:cargo-record | 1 | 0 |
| login-key | 1 | 1 |

## Problems of form

- none
