# Independent verification of `RESULT.md`

The conclusion is accepted: one textual gap is confirmed, in the two competing branches of S8.2-15 for fetched Git repository objects and references. The rejected-card reasoning is supported. In particular, Card 5 is resolved because Q2 decides PROGRAM and S8.2-16 always permits an own line without requiring a unique line form. Card 6 correctly applies the person-chosen condition of Q3, treats the two documented Docker-generated firewall files as RECORD, excludes runtime firewall objects under S8.2-5, and retains missing origins as factual unknowns.

The scope builder reproduces byte-for-byte. There are 117 exact level-two `.git` rows: 29 code rows and 88 stored rows. The scope table now selects 67, marks two FACT_UNKNOWN, and excludes 48. For the original Card 2 population, the arithmetic is 67 selected, fourteen executable Homebrew hooks and their immediate hook group excluded, and two commit-graph groups marked FACT_UNKNOWN, totaling 84. The builder also scans 129 paths containing `.github` because its initial substring test is broad; all are excluded, so this does not change the confirmed set.

The commit-graph correction has been applied. `developer-4fbf65b1725f19d2f17c9c20` (`.git/objects/info`) and `developer-419b511cc8523c257792bd83` (`.git/objects/info/commit-graphs`) are marked FACT_UNKNOWN in the reproducible ledger. `RESULT.md` reports the supported 67-row extent, removes the metadata example from the confirmed examples, and explicitly explains both exclusions. This correction does not change the report's one-gap conclusion.

The two `.git` root group rows remain properly included because their complete immediate-member lists contain the confirmed `objects` and `refs` groups; the report consistently counts inventory rows, including groups, rather than unique files.

Final status: accepted with no remaining issue from this correction.
