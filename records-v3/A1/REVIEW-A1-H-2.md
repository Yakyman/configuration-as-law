VERDICT: DISAGREE

# Review 2 of A1-H after fix round 1 (FX-A1-H-1)

Review date: 2026-11-22 UTC. Inputs read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–5, `../SENTENCES.md`, (not published: orchestration and working notes),
(not published: orchestration and working notes), `RESULT.md`, `FIX-A1-H-1.md`, `REVIEW.md`, `QUESTIONS.md` and the cited files in
`A1/fix-a1-h-1/`. Counts were recomputed with independent scripts. The headline `TRIAL: 2 confirmed holes`, the 114
established H1 occurrences and the H2 extent hold. One classification defect stays open in the unresolved H1
candidates (finding 1).

1. **The 21 disabled-state inventory units are counted as reading-dependent, but under the record's own terms
   neither reading makes them H1 members.** Where: `RESULT.md` lines 32 and 48 ("522 inventory-unit candidates
   depend on an unresolved reading"), `FIX-A1-H-1.md` finding 2, `QUESTIONS.md`,
   `fix-a1-h-1/counts.json`. Evidence: in `unit-file-reader-check.tsv`, 21 rows have
   `second_applier` = "ESTABLISHED under file reading … file reading EXCLUDED-MULTIPLE-READERS" but
   `membership` = READING-DEPENDENT. The disabled states hold, for example `A1/in/raw/coreos/unit-files.txt:32`
   `blk-availability.service disabled disabled`. The saved manual, `raw/systemctl-v260.xml:1116-1117`, defines this
   state: "contains an [Install] section with installation instructions". So under the file reading these rows are
   out of H1. Under the unit reading they are out of H1 as well. The fix accepts REVIEW finding 2 that H1 fits these
   rows "only by taking the fragment file in place of the unit" (`unit-boundaries.md`: "The prior review silently
   selected the second"). Yet `QUESTIONS.md` says "H1 membership differs between these readings". For these 21 rows
   it does not differ. The record never states that the unit reading could give H1 membership. Minimal fix: state
   the H1 outcome of each reading. If the unit reading gives no membership, report the 21 as outside H1 under both
   readings and give 501 reading-dependent candidates in RESULT, FIX, `counts.json` and `QUESTIONS.md`. The
   established 114 does not change.

2. **REVIEW finding 1 (no single-program check on unit rows): handled.** Where: `fix-a1-h-1/unit-file-reader-check.tsv`,
   `hole-1-extent.tsv`. Evidence: 598 rows are checked (486 system-unit, 36 user-unit, 76 stored unit outputs). The old
   extent `review/hole-1-extent.tsv` changes in exactly three ways. 522 rows go from CONFIRMED-STANDALONE to
   READING-DEPENDENT. 76 rows go from CONFIRMED-STANDALONE to FACTUAL-UNKNOWN. 9 rows go from CONFIRMED-CONSTITUENT to
   FACTUAL-UNKNOWN. That gives 721 − 607 = 114 and 158 + 85 = 243. None of the 76 stored outputs has a `disabled`
   state in `in/raw/nixos/unit-files.txt`: 39 are enabled, 19 linked, 16 absent, 1 alias and 1 enabled-runtime.
   So none of them is a missed exclusion. Minimal fix: none.

3. **REVIEW finding 2 (unit replaced by its file): handled within COMMON.md.** Where: `QUESTIONS.md`,
   `unit-boundaries.md`. Evidence: the two readings of the object are written in plain words and left to the author.
   They are not turned into a factual ? and not counted as membership. Minimal fix: none, apart from finding 1.

4. **REVIEW finding 3 (sample counts): handled; the fix's dissent is supported.** Where: `fix-a1-h-1/agreed-audit.tsv`
   and `resolved-audit.tsv`. Evidence: agreed sample, 48 SUPPORTED (46 MUST, 1 NOT, 1 UNKNOWN), 1 CONFIRMED:H1,
   8 READING-DEPENDENT, 3 FACTUAL-UNKNOWN. Resolved sample (17 MUST, 23 NOT inputs): quote support 14 yes, 20 no,
   6 outside, and statuses 15 REFUTED (12 NOT, 1 MUST, 2 UNKNOWN), 3 FACT-WRONG, 6 OUTSIDE, 1 CONFIRMED:H1,
   1 FACTUAL-UNKNOWN. These match RESULT. None of the 8 agreed reading-dependent rows is among the 21 of finding 1.
   The saved unit manual (`raw/systemd.unit-v260.xml:2241-2246`) says the [Install] section "is not interpreted by
   systemd during runtime; it is used by the enable and disable commands of systemctl". So reading directives and
   following the resulting links are distinct acts. Leaving `coreos-4d2a7c7537` at ? (S3-2), rather than confirmed or
   excluded, adds no rule. Minimal fix: none.

5. **REVIEW finding 4 (templated procps evidence): handled.** Evidence: `A1/in/raw/nixos/system-closure.txt:142` is
   `/nix/store/…-procps-4.0.6` and `A1/in/raw/coreos/packages.tsv:397` is `procps-ng 4.0.6-1.fc44`, as cited
   per row. Minimal fix: none.

6. **REVIEW finding 5 (source origin): handled.** Evidence: the SHA-256 values of `(not published: adjudication scratch)`
   (2eb1c9b8…57ae, 42,569 bytes) and `guix-self.scm` (4cf00c3a…d044, 61,135 bytes) match the pinned-lookup records in
   `fix-a1-h-1/raw/provenance/`. The Guile release-archive member also matches. Lines 1209–1272 show the
   compiled-thunk / fallback / source order cited for H2. The mismatch with the inventoried channel revision is
   disclosed, not hidden. Minimal fix: none.

7. **Numbers: agreed apart from finding 1.** Evidence: `hole-1-extent.tsv` has 914 unique IDs: 85 standalone,
   29 constituent, 243 FACTUAL-UNKNOWN, 522 READING-DEPENDENT and 35 exclusions (15/15/5). Confirmed rows by kind
   are 42 system-closure, 40 stored, 31 package-owned-paths and 1 package. `hole-1-scan.tsv` has 5,200 unique IDs.
   `changes.tsv` has 614 records. `counts.json` and (not published: external working record) agree with all of these. The input figures
   (5,200 / 4,171 / 0.48385 / 1,084 / 127) and the card-1 split 86/8/3 are unchanged. Minimal fix: none.

8. **Frozen inputs and samples unchanged: agreed.** Evidence: all 531 entries of (not published: external working record)
   re-hash to the recorded values, including `../TEXT.md`, `../SENTENCES.md` and both sample files. The sample IDs and
   their order are unchanged. Minimal fix: none.

9. **Scope and records: agreed.** Evidence: no removal experiment, virtual machine, new sample or new case. Network
   use was limited to pinned source and documentation lookups. `recompute.py` reads only `compare/joined.tsv`, the
   adjudication rows, the frozen review records and `A1/in/raw/`. No fix file references the c1 or c2 folders.
   `bin/check_quotes.py A1/RESULT.md` reports 10 quotes checked, 0 not found. The new files contain no host names,
   personal names, home paths of our machines or forbidden system names. No change to the text is proposed.
   Minimal fix: none.
