# Matching rule fixed before observation

The matching party uses only `id`, `machine`, `kind`, `name`, and raw inventory `level`. Neither the script nor its output uses the first night's decisions, verdicts, evidence, source or missing-fact explanations. Matching identifies the corresponding new row; it does not carry any conclusion or assert unchanged contents.

Run from the records root:

```sh
python3 S4/collector/match.py NEW_INVENTORY D1/review/unknown-rows.tsv \
  D1/review/additional-unknown-rows.tsv NEW_MATCH_DIRECTORY
```

`NEW_INVENTORY` is a combined TSV, a single collector directory containing `objects.tsv`, or a directory whose immediate system subdirectories contain `objects.tsv`. The output directory must not exist. Raw rows retain their original IDs. The two input tables provide 2,007 distinct first-night IDs; the seven additional source/content and trust-value candidates named only in D1/RESULT.md are documented in S4/MISSING.tsv but are outside these two fixed matching inputs.

Machine names `alma`, `void`, `gentoo`, `microos`, `talos` and the exact `d1-`/`d1b-` forms map to their system. Other machine names require an explicit `--machine-map EXACT=SYSTEM`; there is no substring guessing. Raw `level=1/2,kind=K` becomes `L1:K`/`L2:K`. Existing level-prefixed kinds are unchanged. No kind synonyms are used: a change from ownership-unresolved to outside-packages remains unmatched under this rule.

First match the exact case-sensitive `(machine, kind, name)` key. Both sides must have one row with that key. Duplicate first-night names, duplicate new names and collisions are left unmatched. IDs are not compared as content hashes or used as tie breakers.

For directory group rows, `name` is the exact parent directory. A group matches the new group for that directory and identical kind, even when its children changed. This is group-container identity only: member identities and missing members must be examined in the new inventory; no old member facts transfer. A separate executable row, atomic store row or snapshot row is matched only within its own kind. Paths are not normalized, resolved through symlinks, or shortened.

Version-bearing names retain the complete version: kernel release directories, package versions, image tags/digests and snapshot numbers are identity components. A different version or snapshot number gets no match. In particular the RPM `gpg-pubkey` version-like field is a key identifier and is never stripped. Random-looking strings, hashes, IDs, machine IDs, rescue names and temporary suffixes likewise remain literal; their changed spelling is not evidence of identity.

There is one explicit fallback for `L1:saved-network` only: a name ending in `NAME:UUID:TYPE:DEVICE` with a syntactically valid 8-4-4-4-12 hexadecimal UUID may match on `(NAME, TYPE, DEVICE)` when no exact name exists and this normalized key is unique on both sides. The UUID is the only removed component. No filename or directory uses this fallback. New IDs are used at most once; a collision remains unmatched.

`matched.tsv` columns: `first_id, new_id, machine, kind, first_name, new_name, match_rule`.
`unmatched.tsv` columns: `first_id, machine, kind, first_name, match_status, candidate_count`.
The latter status explains only the structural matching failure, never the earlier object's explanation. All files use UTF-8, tab delimiters and CSV quoting, preserving tabs/newlines in names. Invalid schemas, unknown machines, duplicate IDs or existing output directories fail with exit 2.

The runtime rule and its two input tables are unchanged. `S4/fix-s4-p-3/checks/match-scope.tsv` records dependency counts and structural eligibility only. M04 has seven duplicate-key IDs of eight; M05 has six of seven. Each has at most one structurally eligible ID. The seven RESULT-only IDs have no route in these matching inputs; their inclusion in a later decision scope remains an author question.
