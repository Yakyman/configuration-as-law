# Reduction of the lived-in inventory before classification

The inventory taken with the final collector has 21278 rows ((not published: outside selected checks and direct evidence)). Most of them are
directories and code files inside a few dependency and cache trees. To keep the two classifications and
the adjudication within one night, rows of the two file kinds were collapsed to one row per subtree before
any of these objects was classified. Rule: the first 5 path components under a home directory and under
`/var/lib`, the first 4 elsewhere; a collapsed row has the kind `<kind>:subtree`, the prefix as its name
and the number of collapsed objects as `members`. All other kinds are kept row by row; nothing is dropped.
A classification may answer MIXED for a subtree and say which members differ. Script: (not published: orchestration and working notes).

Rows after the reduction: 5212.

| Kind | Rows |
|---|---:|
| stored-outside-packages | 1377 |
| package-environment-evidence | 964 |
| executable-code-outside-packages | 955 |
| package:npm | 640 |
| stored-outside-packages:subtree | 223 |
| polkit-actions | 219 |
| python-distribution | 172 |
| access-rule | 145 |
| process | 88 |
| group | 68 |
| executable-code-outside-packages:subtree | 54 |
| user-unit-file | 51 |
| account | 40 |
| driver | 35 |
| port | 30 |
| firewall-rule | 21 |
| package:flatpak | 20 |
| service | 20 |
| user-service | 18 |
| firewall-chain | 16 |
| container-image | 12 |
| container | 8 |
| package:go | 6 |
| network | 6 |
| unit-file | 5 |
| network-link | 5 |
| firewall-table | 3 |
| saved-network | 3 |
| package:pipx | 2 |
| user-timer | 1 |
| timer | 1 |
| cron | 1 |
| package:cargo | 1 |
| package:cargo-record | 1 |
| login-key | 1 |
