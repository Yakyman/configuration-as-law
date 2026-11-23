VERDICT: AGREED

# Review 3 of A1-H after fix round 2 (FX-A1-H-2)

Review date: 2026-11-22 UTC. Inputs read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4, `../SENTENCES.md`, `RESULT.md`,
`FIX-A1-H-2.md`, `REVIEW-A1-H-2.md`, `QUESTIONS.md` and the cited files in `A1/fix-a1-h-2/`. Counts were
recomputed with independent one-off commands from the TSV files. The verdict line `TRIAL: 2 confirmed holes`, the 114
established H1 occurrences and the H2 extent hold. Every finding of the previous review was handled. No blocking
defect remains. Finding 10 is a non-blocking nit.

1. **REVIEW-A1-H-2 finding 1 (21 disabled units, outside H1 under both readings): fixed.** Where: `RESULT.md`
   (hole 1, "Unit and file boundaries corrected"), `QUESTIONS.md`, `fix-a1-h-2/reading-outcomes.tsv`,
   `fix-a1-h-2/unit-boundaries.md`. Evidence: `fix-a1-h-2/reading-outcomes.tsv` has 21 rows, all `system-unit`, each giving the
   H1 outcome of both readings and `EXCLUDED-BOTH-READINGS`. All 21 `disabled_evidence` lines were checked against the
   saved inventory. Each cited line exists, names the unit and has state `disabled`. Example:
   `A1/in/raw/coreos/unit-files.txt:32` is `blk-availability.service disabled disabled`. In
   `A1/in/raw/debian/unit-files.txt:195` the state is `disabled` and the preset is `enabled`. `QUESTIONS.md` now keeps
   only 501 candidates open and says why the 21 do not depend on the choice. Minimal fix: none.

2. **The exclusion adds no rule and makes no reinterpretation.** Evidence: `A1/fix-a1-h-1/raw/systemctl-v260.xml:1116-1117`:
   "The unit file is not enabled, but contains an [Install] section with installation instructions."
   `A1/fix-a1-h-1/raw/systemd.unit-v260.xml:2241-2246`: the [Install] section "is not interpreted by systemd during
   runtime; it is used by the enable and disable commands of systemctl". So two programs read the file. That fails the
   premise of the existing H1 argument (S2.2-7, "in force only inside one program"). Round 1 applied the same exclusion
   (`EXCLUDED-MULTIPLE-READERS`), and review 2 accepted it. No object reading is chosen and no MUST/NOT is assigned.
   Minimal fix: none.

3. **Consistency check of the remaining 501.** Evidence: in `unit-file-reader-check.tsv`, none of the 501
   `READING-DEPENDENT` rows has an own state of `disabled`. The 11 text hits for "disabled" are preset values. Five rows
   have state `indirect`: `coreos-f2e614114f`, `coreos-f69f13e0a1`, `coreos-b6e47b5d3b`, `coreos-359942f31f` and
   `debian-502f1f48de`. The saved manual (`systemctl-v260.xml`, `indirect` row) also lets that state arise "through a
   symlink that is not specified in Also=". So the state alone does not establish an [Install] section. Keeping these
   rows open is consistent with the evidence standard. Minimal fix: none.

4. **REVIEW-A1-H-2 findings 2–3 (single-program check, object substitution): handled, still valid.** Evidence: the
   reader check keeps 598 rows: 501 READING-DEPENDENT, 76 FACTUAL-UNKNOWN and 21 EXCLUDED-BOTH-READINGS. All 21 rows
   whose `second_applier` begins with `ESTABLISHED` are exactly the 21 changed IDs. The other 501 are all
   `UNESTABLISHED`. Minimal fix: none.

5. **REVIEW-A1-H-2 finding 4 (sample counts): handled.** Evidence: none of the 21 IDs occurs in
   `review/resolved-sample.tsv` or `review/agreed-sample.tsv`. So the frozen audits and the counts in RESULT stay
   valid: agreed 48/1/8/3 and resolved 14 supported, 26 challenged (15/3/6/1/1). Minimal fix: none.

6. **REVIEW-A1-H-2 findings 5–6 (procps evidence, source provenance): handled.** Evidence: the round-1 files involved
   are in the frozen manifest, and their hashes are unchanged (finding 8). No H2 or provenance claim was edited.
   Minimal fix: none.

7. **Numbers match the data files.** Evidence: `fix-a1-h-2/hole-1-extent.tsv` has 914 unique IDs: 85
   CONFIRMED-STANDALONE, 29 CONFIRMED-CONSTITUENT, 243 FACTUAL-UNKNOWN, 501 READING-DEPENDENT, 21
   EXCLUDED-BOTH-READINGS and 15/5/15 earlier exclusions, so 56 exclusions in total. Confirmed rows by kind: 42
   system-closure, 40 stored, 31 package-owned-paths, 1 package (114). Compared with `fix-a1-h-1/hole-1-extent.tsv`,
   exactly 21 rows differ, all READING-DEPENDENT → EXCLUDED-BOTH-READINGS. No other column changed. `changes.tsv` has
   the same 21 IDs. `hole-1-scan.tsv` has 5,200 unique IDs. `counts.json` and (not published: external working record) agree.
   `compare/STATS.md` still gives 5,200 / 4,171 (80.21 %) / 0.48385 / 1,084. Minimal fix: none.

8. **Frozen inputs: unchanged.** Evidence: all 569 entries of `fix-a1-h-2/raw/frozen-input-sha256.json` re-hash to the
   recorded values (0 missing, 0 changed). Minimal fix: none.

9. **Scope and records: inside the task.** Evidence: no experiment, virtual machine, network lookup, new case or new
   sample. `recompute.py` reads only round-1 records and `A1/in/raw/`, and it writes only to `A1/fix-a1-h-2/`. It has
   no reference to the c1 or c2 folders. `bin/check_quotes.py A1/RESULT.md` reports 10 quotes checked, 0 not found.
   `unit-boundaries.md` has 2 quotes, 0 not found. The home paths in the extent are test-machine accounts from the
   inventory, not paths of our machines. The new files name no private tooling labels and no personal names. Minimal fix: none.

10. **Nit (non-blocking): stale pointers in the whole-table scan.** Where: `fix-a1-h-2/hole-1-scan.tsv`, column
    `scope_disposition`. Evidence: 893 rows (85 + 29 + 243 + 501 + 35) say "see A1/fix-a1-h-1/hole-1-extent.tsv".
    Only the 21 changed rows point to `fix-a1-h-2/hole-1-extent.tsv`. The statuses in the round-1 file are
    identical for those 893 rows, so no value is wrong, but the pointer names a superseded file. Minimal fix:
    optional. Point all rows to `fix-a1-h-2/hole-1-extent.tsv`.
