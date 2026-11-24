VERDICT: DISAGREE

Review RR-S4-P-3 of S4-P after fix round 3 (FX-S4-P-3), 2026-11-23 UTC. Inputs read: (not published: orchestration or scratch); `TEXT.md` Sections 8, 9 and Appendix A; `SENTENCES.md`; `SUP1/step-4.md`; (not published: orchestration or scratch); (not published: orchestration or scratch); `S4/READY.md`; `S4/FIX-S4-P-3.md`; `S4/REVIEW-S4-P-3.md`; `S4/MISSING.tsv`; `S4/fact-status.tsv`; `S4/COLLECT.md`; `S4/MATCH.md`; `S4/HANDOFF.md`; `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md`; `S4/CLASSIFICATION-INPUTS.list`; `check-inputs-v4/supplement-1/step-4-instruments/S4/PUBLISH.list`; `check-inputs-v4/supplement-1/step-4-instruments/S4/input-files.sha256.tsv`; and the data files they cite (sample below). Paths are relative to the night folder.

1. **The deciding parties are given each object's first-night missing-fact explanation. This hints what the object is and passes on part of an earlier decision.** Where: `S4/CLASSIFICATION-INPUTS.list` lists `S4/MISSING.tsv`, `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/tables/missing-row-map.tsv` and `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/checks/match-scope.tsv`. `S4/HANDOFF.md` and `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` say to send these documents with the matching output. Evidence:
   - `missing-row-map.tsv` maps every first-night id to a fact group (`first_id, machine, fact_id`). `matched.tsv` maps `first_id` to `new_id` (`S4/MATCH.md`). Together they label every new object with its first-night fact group.
   - The fact groups are summaries of the `missing_facts` column of `D1/review/unknown-rows.tsv`. That column is first-night decision text. For example, row `alma-61c67b50…`, `source=agreement`, says "Listed as an installed package (Q1); … imported at a person's command (own line) or by dnf from repo configuration".
   - `MISSING.tsv` passes this on in group form. A07: "RPM key import had no explicit/dependency reason", which points to Q1 and to own line versus derived line. M05: "Sudo installation default versus later choice". V02: "Retained old-version package member origin and full receipt integrity". T03: "Original image membership and complete receipt integrity". "Receipt" appears in 7 rows; it is the word that RV-S4-P-3 finding 1 had removed from the handoff copy as an echo of S8.2-7.
   - `SUP1/step-4.md` part 4 has the parties decide "without seeing … any earlier decision about the same objects". `S4/MATCH.md` itself says the matching output carries no "missing-fact explanations". The allowlist puts them back next to that output.
   - The parties do not need these files to decide. The matching output already lists the objects to decide, and `COLLECT.md` documents where each fact is stored.
   
   Minimal fix: remove the three files from `CLASSIFICATION-INPUTS.list`. Name them among the materials withheld in `HANDOFF.md` and `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md`. Keep them in `check-inputs-v4/supplement-1/step-4-instruments/S4/PUBLISH.list` as instrument and operator inputs. Regenerate `check-inputs-v4/supplement-1/step-4-instruments/S4/input-files.sha256.tsv`.

2. **REVIEW-S4-P-3 finding 1 is handled as TASK-FX-S4-P-3 item 1 requires.** Evidence:
   - `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/neutral-literals.tsv` has 21 rows. They include `verified-archive:lock-receipt-reference`→`verified-archive:lock-reference`, `directory-receipt`→`directory-entry`, the `lock-receipt-reference` and `directory-receipt` counter keys, and all six `unowned-with-receipt-<status>` keys.
   - The six suffixes cover every value that `status` can take in `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extra_void.py` lines 274–285: `unknown`, `directory-receipt`, `equal`, `different-or-absent`, `different`, `absent`.
   - `HANDOFF.md` states that the file name `old-package-receipt-sources.tsv` is a name only.
   - `fix-s4-p-3/checks/handoff-tests.json` records 19 checks passed.

3. **REVIEW-S4-P-3 finding 2 is handled.** The two mapped values are `unknown:creator-field-empty` and `unknown:image-reference-field-empty` (`neutral-literals.tsv`), and `HANDOFF.md` describes them that way.

4. **REVIEW-S4-P-3 finding 3 is handled with the operator’s wording.**
   - The exact sentence ("If the handoff copy of a machine fails, nothing is repaired and no observation is repeated; the objects of that machine are listed by id as not delivered, receive no decision in this step, and the machine gives “?”.") appears in `S4/HANDOFF.md` and in `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` (last line).
   - No other procedure for that case remains in `COLLECT.md`, `HANDOFF.md`, `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md`, `MATCH.md` or `READY.md` (grep for withhold/fail/delivered).

5. **REVIEW-S4-P-3 finding 4 is handled. Each of the 14 groups ends under item 4 of TASK-S4-P.**
   - `fact-status.tsv` gives A03/A04/A07/A09/A11, V03/V07/V09, M03/M05/M11/M14 and T03/T05 `not-obtainable`.
   - `fix-s4-p-3/checks/attempt-basis.tsv` has exactly 42 `failed-to-record-complete-fact` rows, three per group. The rows marked `inconclusive-not-counted` and `supplementary-after-endpoint` are not counted.
   - Several groups share one probe run as a method. Each group still has three different methods, so this does not break the item.
   - Finding 8 of REVIEW-S4-P-3 is also handled: READY and FIX place the five handoff commands in `HANDOFF.md`.

6. **The numbers in the result files match the data.**
   - `fact-status.tsv` has 18 recordable, 12 partial and 15 not-obtainable (= 45). This matches the first line of READY ("18 of 45") and `checks/accounting.json`.
   - The 18 recordable ids are those READY lists per system.
   - For every group, the `objects` value in `MISSING.tsv` equals its row count in `missing-row-map.tsv` (G01 = 0, no rows), with 2,014 distinct ids.
   - Columns 1–4 of `MISSING.tsv` are unchanged from `fix-s4-p-2/tables/MISSING.tsv`. Column 5 changes only for A07, V09 and M14, as FIX row 6 says.
   - Columns 1–3 of `fact-status.tsv` change only for the 14 groups.
   - The map is byte-identical to the one from fix round 2.

7. **Sample of 8 claims: all supported by their cited evidence.**
   1. A04: "four application-log unit mentions but zero … operation matches". `systems/alma/raw/fact-diagnostics.jsonl`: `target_matching_lines 4`, `target_operation_lines 0`; journal and audit routes 0.
   2. V09: "126 processes, 430 fd links, 126 maps reads, zero certificate-path hits, 25 TLS-library mappings and one read error". `systems/void/diagnostics/04-trust-live-readers.json` matches exactly.
   3. V03/V07 retained logs. `01-retained-event-logs.json`: 8 absent roots, 0 files read, 0 matches.
   4. T05: "102 records and zero PATH records". `systems/talos/raw/audit-diagnostic.json`: `parsed_records 102`, `PATH_rows 0`.
   5. T05 replay: "163 events … status 124". `events-diagnostic.json` event types sum to 163, and `raw/status.tsv` has `runtime-events 124 10.113`.
   6. M05: "3,085 valid records; two source-sync messages". `followup-evidence/journal-diagnostics.json`: `records 3085`, `invalid_records 0`, M05 `message_hits 2` from `transactional-update-sync-etc-state`.
   7. Alma assembled run. `raw5/status.tsv`: `assembled-collector 0 114.397`, `actions 0 112.403`. `raw5/actions.tsv` has nine rows, all with exit 0.
   8. Cleanup. `checks/server-cleanup.json`: no remaining owned roots or units, 0 owned QEMU processes.

8. **Publication set: checksums and personal data.**
   - All 49 checksums in `check-inputs-v4/supplement-1/step-4-instruments/S4/input-files.sha256.tsv` match the files. The manifest equals `check-inputs-v4/supplement-1/step-4-instruments/S4/PUBLISH.list` without itself, and every listed file exists.
   - A grep of the listed files, and of the decompressed probe binary, finds no personal name, host name, home path of our machines, or mention of an automated assistant.
   - The `/home/user/…` and `/home/linuxbrew/…` strings in `seed-fixture.sh`, `validate-output.py` and `packages.py` are guest fixture and guest paths.
   - `man.archlinux.org` in `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/PACKAGES.md` is a documentation URL.

9. **The work stayed inside its task, apart from point 1.**
   - No observation, object decision or outcome is claimed.
   - No rehearsal inventory is kept. For example, `systems/alma/raw5/` holds statuses, coverage and stderr only, with no `objects.tsv` or member tables.
   - The new deviations are disclosed in READY and FIX: the fourth V09 probe, the MicroOS text-journal reduction, the Talos 64 MiB cap, and the rejected Alma launch name.
   - No published-text rule or failure condition was changed.

10. **Nit: the claim "every rehearsal inventory/event payload was deleted" is not exact.** Where: `S4/READY.md` paragraph "Only changed queries…"; `S4/FIX-S4-P-3.md` paragraph "The earlier preparation…". Evidence: `S4/fix-s4-p-3/systems/talos/raw/events-diagnostic.json` keeps 76 event message strings under `sequence_phase_task_payloads`. They are boot-sequence messages, not object rows. Minimal fix: reword to "inventories were deleted; diagnostic event messages are kept in `events-diagnostic.json`", or reduce that field to counts.

11. **Nit: the published adapter keeps an inactive rehearsal branch keyed to one first-night object.** Where: `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/key_events.py`, the `DIAGNOSTICS=False` branch filtering `key_id=='c2a1e572'`. Evidence: the branch never runs in observation mode, and it states no class. Minimal fix: note in `COLLECT.md` that the branch is inactive rehearsal code. Do not edit the tested file.

12. **Nit: the accounting check omits two newly created active files.** Where: `S4/fix-s4-p-3/checks/accounting.json` `allowed_active_files_changed`. Evidence: it does not list `S4/HANDOFF.md` and `S4/CLASSIFICATION-INPUTS.list`, which were created in this round (neither is in `fix-s4-p-3/raw/before.sha256.tsv`). Minimal fix: list them as added files.
