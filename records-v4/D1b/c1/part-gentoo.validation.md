# Gentoo c1 validation

2026-11-23 UTC.

Result: PASS. No concrete factual or mechanical error was found in the checked scope.

- `part-gentoo.tsv` has 32,775 data rows and 32,775 unique IDs. Its ID set exactly equals `D1b/in/part-gentoo.tsv`; there are no missing or extra IDs. The 1,210- and 1,633-row shard tables are disjoint subsets, and every merged row is byte-for-field identical to its shard row.
- Every row has the six required nonempty fields. Every decision is in the allowed vocabulary. Every cited sentence ID exists in `SENTENCES.md`; no citation list has a duplicate or whitespace defect. `what_it_does` is at most 15 words and `reason` at most 30 words in every row.
- All 861 homogeneous package-member groups were checked against their complete member files: 3,410 of 3,410 members join an `unchanged` package-file comparison after only the five recorded directory aliases. All 251 atomic alias cases also join an `unchanged` comparison. A ten-row sample covered `/sbin`, `/lib`, and `/lib64`; the raw filesystem record confirms each alias target.
- The supplemental member table has exactly one matching path entry for every member in all 901 groups it covers, and every aggregate decision agrees with the member decisions. Its 453 covered `MIXED` groups each contain at least two member decisions. The other 125 kernel `MIXED` groups were checked exhaustively: each has both unchanged package files and unmatched directory nodes, with no non-directory node in the unmatched partition.
- The two persistent-store `MIXED` rows were compared with all rows keyed to their raw object IDs in `store-members.tsv`. Their stated package, generated-state, configuration, and unresolved-content categories are present; no contradictory package comparison or persistence fact was found.
