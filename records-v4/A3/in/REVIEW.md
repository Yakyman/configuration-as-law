# Independent review

Review ran from 2026-11-23T11:19:53Z through 2026-11-23T11:28:22Z. Status: complete for the A3-I operator inventory.

## Reduction method

`reduce.py`, `REDUCTION.md`, `FACTS.md`, `INPUTS.md`, the committed collector contract, and all three machine evidence sets were reviewed. The reducer removes a lived-in row only when a base row has the same level, kind, name and all compared facts. It compares the complete decoded `members` value, every row of a referenced member table, and every package-file path, integrity value and rule. It retains duplicate fact rows and retained source rows, and it supplies no missing or unknown fact. The only normalizations replace machine-specific member filenames and native-package object IDs with the evidence they locate. These are locator normalizations, not object selections.

The one-gibibyte CSV field limit prevents truncation or failure on a recorded fact larger than the library default. The existing synthetic test passed, including a 200,000-character fact, equal facts with different source IDs, native-package references, changed installation reason, changed package integrity, changed member facts, changed runtime facts, duplicate retention, exact output schema, and refusal when referenced membership evidence is missing.

For the server data, all 753 lived-in and 591 base member references exist. All referenced native-package IDs resolve. All 25,166 lived-in and 21,659 base package-file rows join to source object IDs. The reduction audit has 3,287 rows: 1,962 drops and 1,325 keeps. The derived table has exactly 1,325 data rows, the required seven-column header, unique `server-`-prefixed IDs, part `A3`, machine `server`, level-prefixed kinds, and valid preserved JSON members. The reported counts agree with the audit and table.

## Server operation and evidence

The committed server script defines the same 13 actions named by the status table. The lifecycle contains one action execution step, exactly one restart stop/start pair, different before/after boot IDs, one lived-in collection, one lived-in destruction, one untouched-base creation and collection, and one base destruction. Every recorded lifecycle exit is zero. All 13 action statuses are zero, with separate saved output for each action.

The copy manifest independently verifies all 2,015 files in the two server raw directories without mismatch. Both collector metadata files retain `ready_for_observation=false`; the lived-in inventory records six gaps and the base records three. The reports distinguish filesystem and implemented ownership flags from universal fact completeness and do not state a hypothesis outcome.

## Developer operation and evidence

The developer reduction audit has 11,852 rows: 5,443 drops and 6,409 keeps. The derived table has exactly 6,409 data rows, the required header, unique `developer-`-prefixed IDs, part `A3`, machine `developer`, level-prefixed kinds and valid preserved JSON members. The untouched base has 5,966 objects. Reported overall and per-kind counts agree with the audit and table.

All 6,214 lived-in and 1,483 base member references exist and are unique within their inventories. All 82 native-package references in each inventory resolve. All 169,962 lived-in and 158,405 base package-file rows join to source object IDs. Each inventory contains seven `members` fields larger than 131,072 characters, with a maximum of 590,951; the raised field limit reads these facts and the reduction audit accounts for every source row.

The committed developer script names the same 13 actions as the saved action table. All ran exactly once and exited zero. The lifecycle records successful removal of the instrument-only input staging directory before restart, exactly one successful stop/start pair, distinct before/after boot IDs, two successful collector calls, and successful destruction of both disposable machines. Two supplemental status reads failed while the machine was restarting; the required status copy had already succeeded, and neither failure reran an action or collector.

The lived-in and base raw manifests independently verify all 7,163 and 2,411 copied files without mismatch. The operator manifest verifies all 56 files it names, and every staged input digest matches its committed source. Developer metadata retains `ready_for_observation=false`: filesystem traversal is marked complete, package ownership is incomplete, and the lived-in/base inventories record 304/220 gaps and 114/116 nonzero queries. `READY.md` reports those limits and makes no complete-package or hypothesis claim.

## Gaming operation and evidence

The gaming reduction audit has 24,243 rows: 7,728 drops and 16,515 keeps. The derived table has exactly 16,515 data rows, the required header, unique `gaming-`-prefixed IDs, part `A3`, machine `gaming`, level-prefixed kinds and valid preserved JSON members. The untouched base has 8,312 objects. Reported overall and per-kind counts agree with the audit and table.

All 4,810 lived-in and 3,169 base member references exist and are unique within their inventories. All 101 lived-in and 98 base native-package references resolve. All 449,205 lived-in and 444,199 base package-file rows join to source object IDs. The largest `members` field in each source inventory is 517,167 characters; the raised field limit reads it, and the reduction audit accounts for every source row.

The committed gaming script names the same nine actions as the saved action table. It ran once. Eight actions exited zero; `gaming_anonymous_download` exited 8 with the recorded message `Missing configuration`. Its output is retained, later actions continued once, and no repair, replacement or retry is recorded. The lifecycle has one action-script invocation, exactly one successful restart stop/start pair, distinct before/after boot IDs, two successful collector calls and successful destruction of both disposable machines. The instrument inputs were staged in a runtime directory that did not persist through the restart.

The lived-in and base raw manifests independently verify all 6,230 and 4,541 copied files without mismatch or omission. The operator transfer manifest verifies all 47 files it names; all 44 deployed inputs match both their transfer manifest and committed local bytes. Gaming metadata retains `ready_for_observation=false`: filesystem traversal is marked complete, package ownership is incomplete, and the lived-in/base inventories record 196/200 gaps and 109/111 nonzero queries. `READY.md` preserves the failed action and these coverage limits.

## Final reconciliation and conclusion

Two preliminary wording findings were corrected during review. `FACTS.md` now limits its raw-output statement to each completed machine and describes whole collector output without implying universal fact coverage. `READY.md` now states that paths inside a reproduced operator record are relative to that operator record's directory.

The final synthetic test passed with bytecode writing disabled. All three derived tables have the exact required schema. Their row counts, audit decisions, overall counts and every level/kind count agree with source data and `counts-MACHINE.json`. `READY.md` begins exactly `INVENTORY: 3 of 3 machines`; its three overall summaries and all 79 per-kind rows agree with the count files. Required method, fact, input, readiness, review and machine-table artifacts exist.

The A3-I operator inventory is accepted as complete: developer 11,852 before and 6,409 after; gaming 24,243 before and 16,515 after; server 3,287 before and 1,325 after. This accepts execution, retained evidence and exact base subtraction only. It supplies no classification or hypothesis outcome, and all unknown or incomplete facts remain recorded as such.
