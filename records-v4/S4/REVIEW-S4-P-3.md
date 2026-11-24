VERDICT: DISAGREE

Review RV-S4-P-3 of S4-P after fix round 2 (FX-S4-P-2), 2026-11-23 UTC. Inputs read: (not published: orchestration or scratch); `TEXT.md` Sections 8, 9 and Appendix A; `SENTENCES.md`; (not published: orchestration or scratch); (not published: orchestration or scratch); `SUP1/step-4.md`; `S4/READY.md` (byte-identical to `S4/fix-s4-p-2/READY.md`); `S4/FIX-S4-P-2.md`; `S4/REVIEW-S4-P-2.md`; and the data files they cite. Paths are relative to the night folder.

1. **The new handoff map leaves the positive "receipt" labels in place. Only their negated forms were changed (REVIEW-S4-P-2 finding 3 is only partly handled).** Where: `S4/fix-s4-p-2/neutral-literals.tsv` (11 rows); `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extra_void.py` lines 143–144, 276, 285 and 291. Evidence:
   - When a record has no other provenance, the collector writes the default `lock-receipt-reference`. That gives the status `verified-archive:lock-receipt-reference` in `npm-archive-sources.tsv` and a counter key in `fact-summary.json`. `S4/rehearsal/void/round3/fact-summary.json` shows `adapters.npm."lock-receipt-reference": 41`.
   - `old-package-member-integrity.tsv` uses the status `directory-receipt`: 4,294 rows in the same summary. The `unowned-with-receipt-*` counter keys are also unmapped.
   - `grep -c lock-receipt` returns 0 for both `neutralize.py` and `test-handoff.py`.
   
   So the Void handoff copy still labels lock references as receipts. That is the wording of S8.2-7 ("Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?"). Meanwhile the Alma counterpart has been neutralized to `cache-identity-reference`. The result is asymmetric: after the copy, "receipt" survives only on the lock-based references. Minimal fix: add map rows such as `verified-archive:lock-receipt-reference`→`verified-archive:lock-reference`, `directory-receipt`→`directory-entry`, and the `lock-receipt-reference` and `unowned-with-receipt-<status>` counter keys. Add them to `HANDOFF.md` and to the synthetic tests. In `HANDOFF.md`, note that the file name `old-package-receipt-sources.tsv` is a name only.

2. **The handoff map removes two `unknown` markers, although READY and HANDOFF say unknown fields are preserved.** Where: `neutral-literals.tsv` maps `unknown: no creation event established by current file`→`creator-field-empty` and `unknown:no-original-image-manifest`→`image-reference-field-empty`. Evidence:
   - READY says "Neutralization preserves every measured value and unknown/failure field". `HANDOFF.md` says "Unknown facts and failed reads retain their status".
   - `S4/fix-s4-p-2/tables/MISSING.tsv` row V07 is itself a classification input. It still says "historical_creator has an unknown marker", but the handoff copy no longer carries that marker.
   - Under COMMON, an object whose deciding fact is not held gets FACT_UNKNOWN, and this marker is the inventory's signal for that.
   - The previous review's example name `creator-field-empty` contributed to this. It is still a defect against the fix's own stated invariant.
   
   Minimal fix: keep the prefix (`unknown:creator-field-empty`, `unknown:image-reference-field-empty`), and update `HANDOFF.md` and the tests.

3. **"A failed handoff is withheld" adds a way to lose objects, and no rule covers it.** Where: `S4/fix-s4-p-2/HANDOFF.md` ("A failed handoff is withheld, never repaired by recollecting an observation"); `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` line 66 ("the partial copy is not delivered"). Evidence: `SUP1/step-4.md` part 4 has the two parties decide every object of the new inventories. Part 3 says only what happens to first-night objects with no match. Neither part says what the objects of a successfully collected machine receive when the copier fails on it. The fix fills that hole with a procedure of its own. Minimal fix: record it as an author question in `S4/fix-s4-p-2/QUESTIONS.md` (for example: deliver the original, or report the machine's objects by id without a decision), and do not settle it in HANDOFF.

4. **Item 4 of TASK-S4-P is still unfinished for 14 groups, which are spread over all four systems counted as ready.** Where: `S4/fix-s4-p-2/tables/fact-status.tsv`:
   - 12 groups `attempt evidence incomplete`: A03/A04/A07/A09/A11, V03/V07, M03/M05/M11, T03/T05;
   - 2 groups `not rehearsed`: V09, M14.
   
   READY's header says "4 of 5 systems ready". Evidence: the relabelling itself is correct (findings 5–6 below). But item 4 says to rehearse "until … it … records the facts of `MISSING.tsv`, or until three different attempts on a fact have failed". None of the 14 groups reached either end. READY admits this ("not certification that item 4 is complete"). `SUP1/step-4.md` part 2 freezes the collector and fact list at commit ("None of them changes after that"). Committing now would freeze those 14 groups unrehearsed. Minimal fix: either do the item-4 rehearsals for the 14 groups before the commit, or record committing them unrehearsed as a question for the author in `QUESTIONS.md`, and make the first paragraph of READY point to that question.

5. **REVIEW-S4-P-2 findings 1, 2 and 4 are handled.** Evidence:
   - Finding 1: V09/M14 are `not rehearsed` and excluded from k (`fact-status.tsv`; `checks/status-basis.tsv`).
   - Finding 2: `STATUS.md` restores item 1/item 4 as the only grounds for `not-obtainable`. `status-basis.tsv` audits all 15 earlier labels. Only V02 keeps the label, based on three distinct routes: installed manifests, residual metadata and cached archives (`S4/parts/void.md` line 16). `S4/rehearsal/void/round3/coverage.tsv` lines 136–144 show nine cache-manifest queries with exit 0, and `fact-summary.json` shows `no-surviving-receipt` 6,859 and `equal` 22,282.
   - Finding 4: READY attributes the Void action exits to `actions.tsv`: 12 rows, all exit 0. In `status.tsv`, the three exit-1 rows (`action-language_install_node`, `action-language_npm_install`, `action-language_cowsay`) are `cat` reads of stderr logs (`S4/rehearsal/void/run-round3.py` lines 39–42).
   - Finding 3 is handled only in part (findings 1–2 above).
   - Findings 5 and 6 of REVIEW-S4-P-2 recorded no defect. G01 remains `partial`: `S4/rehearsal/gentoo/round2/actions.tsv` shows `browser_extension 1` and `container_run 1`.

6. **The numbers in the result files match the data.**
   - Status counts in `fact-status.tsv`: 18 recordable, 12 partial, 1 not-obtainable, 12 attempt evidence incomplete, 2 not rehearsed (= 45). They equal READY, `STATUS.md` and `checks/accounting.json`.
   - Exactly the 14 former `not-obtainable` groups changed status between the fix-1 and fix-2 tables.
   - `missing-row-map.tsv` is byte-identical to fix-1 and has 2,014 distinct IDs. Every `objects` value in `MISSING.tsv` equals its count in the map (G01 = 0, no map rows). Columns 1–3 of `MISSING.tsv` are unchanged from fix-1.
   - `checks/sudo-scope.tsv` supports 8 M04 / 7 M05 IDs, of which 7 and 6 have duplicate keys.
   - `checks/handoff-tests.json` lists 17 passed checks.

7. **The work stayed inside its task.**
   - Preservation: all 540 files in `S4/fix-s4-p-2/raw/before.sha256.tsv` still match, except the declared `S4/READY.md`. Nothing under `check-inputs-v4`, `D1/`, `check-inputs-v4/supplement-1/step-4-instruments/S4/collector`, `S4/rehearsal/` or `S4/fix-s4-p-1/` changed.
   - No machine run, observation, object decision or outcome is claimed.
   - Publication files: all 46 hashes in `fix-s4-p-2/input-files.sha256.tsv` verify, and the manifest equals `check-inputs-v4/supplement-1/step-4-instruments/S4/PUBLISH.list` minus itself. The listed files, READY and FIX contain no host name, personal name, host home path or mention of an automated system.
   - No rule was added to the published text and no failure condition was touched. The decision scope of the seven RESULT-only IDs stays an author question.

8. **Nit: FIX row 3 says "`HANDOFF.md` and `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` give all five commands".** Where: `S4/FIX-S4-P-2.md` row 3. Evidence: `S4/fix-s4-p-2/COMMANDS.md` contains no `neutralize` command; line 66 points to `HANDOFF.md`. Minimal fix: say the commands are in `HANDOFF.md`, and that `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` refers to them.
