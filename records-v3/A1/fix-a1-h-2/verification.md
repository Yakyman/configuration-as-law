# Independent verification of FX-A1-H-2

Date: 2026-11-22 UTC.

Scope: review finding 1 only. This verification checks the changed records, preserved inputs and samples, and consistency of the updated result. It does not select an object reading or determine an overall MUST/NOT result for any unit.

## Result

Pass. The correction consistently removes the 21 disabled-state inventory units from the open H1 reading boundary without changing established H1 membership, factual unknowns, samples, or frozen inputs.

| Check | Result | Evidence from independent inspection |
|---|---|---|
| Changed extent | Pass | Comparing the round-1 and round-2 extent TSVs gives 914 unique IDs in each and exactly 21 changed rows. Each changes from `READING-DEPENDENT` to `EXCLUDED-BOTH-READINGS`; no other row differs. The 21 IDs exactly equal `reading-outcomes.tsv` and `changes.tsv`. |
| Both recorded readings | Pass | `reading-outcomes.tsv` has 21 rows, all marked `EXCLUDED-BOTH-READINGS`. For each, the managed-unit reading identifies no settings-file H1 instance without substitution. The backing-file reading cites a matching disabled inventory line. The saved manual at `A1/fix-a1-h-1/raw/systemctl-v260.xml:1116-1117` defines disabled as an [Install] section with installation instructions, and `../fix-a1-h-1/raw/systemd.unit-v260.xml:2241-2246` assigns that section to the enable/disable commands. This supports failure of the single-program premise for the file reading. |
| Count partition | Pass | Direct TSV counts are 85 `CONFIRMED-STANDALONE`, 29 `CONFIRMED-CONSTITUENT`, 243 `FACTUAL-UNKNOWN`, 501 `READING-DEPENDENT`, 21 `EXCLUDED-BOTH-READINGS`, 15 `EXCLUDED-FACT`, 5 `EXCLUDED-MULTIPLE-READERS`, and 15 `EXCLUDED-STATE`: 914 total. Thus established H1 remains 114, factual unknowns remain 243, reading-dependent candidates change from 522 to 501, and exclusions total 56. These figures agree with `counts.json`, `unit-boundaries.md`, `../FIX-A1-H-2.md`, and `../RESULT.md`. |
| Other changed indices | Pass | The reader-check TSV retains 598 rows and has exactly the same 21 changed IDs, all with `EXCLUDED-BOTH-READINGS`. The whole-table scan retains 5,200 unique IDs and changes exactly those 21 scope dispositions. |
| Frozen material | Pass | Independent SHA-256 recomputation of all 569 entries in `raw/frozen-input-sha256.json` found zero mismatches. The manifest includes the original frozen inputs and round-1 records. |
| Samples and audits | Pass | The frozen resolved and agreed selections retain 40 and 60 IDs respectively; their hashes match the manifest. The round-1 resolved and agreed audit ID sequences match the corresponding selections in order. No changed ID occurs in either selection, so retaining the recorded sample dispositions and counts is consistent. |
| Result wording and quotations | Pass | `../RESULT.md` reports 501 reading-dependent candidates and 21 inventory units excluded under both readings, keeps 114 established H1 rows and 243 factual unknowns, and does not choose an object reading or an overall MUST/NOT result. `/usr/bin/python3 -I bin/check_quotes.py A1/RESULT.md` reports 10 quotations checked and zero absent. |

The corrected record resolves the reviewed counting defect. The remaining 501 managed-unit/backing-file cases remain unresolved, as required by the stated scope.
