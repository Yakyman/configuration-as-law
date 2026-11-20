VERDICT: AGREED

Review of `X/X2C-RESULT.md` (sha256 bb3a82f9…37d1, matches `raw-X2C/validation.json`). Independent review, 2026-11-19.
Scope: the shared rules of the checks, PAPER.html §5 and §9; X2C-RESULT.md; X2-*.tsv/json; a sample of 5 claims. My recomputation scripts:
`X/raw-REVIEW-X2C/check.py`, `X/raw-REVIEW-X2C/dis.py` (run with `/usr/bin/python3 -I`).

What I checked, short version:
- (1) The `?` follows the fixed §9.2 condition plus §9.1 ("? = insufficient data"). No row has two different affirmative
  classes (recorded/derivative/data). The no-class and two-class limbs are not shown, because the premises are missing
  (no designated declaration, creator or authorship). That handling was set in `X2-PROTOCOL.md` before results ("Lack of
  provenance/designation evidence is an evidence gap…", "missing provenance … alone yields ?"). It was not added afterwards.
- (2) Every number matches the source TSVs. My own run gives: 235/235/235 IDs, all on debian-desktop; classification 1 223/11/1;
  Classification 2: 27 recorded, 152 derivative, 10 data, 7 hole-none, 39 hole-two; same=17; cross-product=2000; κ=0.0374823861;
  pair table 151/30/27/8/1/1/7/9/1 (sum 235); holes 234 / 46 / ∩46 / ∪234; only non-hole row is `efc18859d4`; proxies
  1,718 recorded + 3 data = 1,721. Frozen inputs in `raw-X2C/inputs/` are byte-identical to the live files, including PAPER.html and the shared rules of the checks.
  All row numbers in both result tables point to the stated IDs and classes.
- (3) I found no invented classification rule. No precedence, no directory rule, no declaration designated after the fact.
  The §5 quotes are verbatim.
- (4) Sample of 5 claims. All 5 hold: spool copy 138 B byte-identical (`raw-X2/spool-copy-check.json`); job `X2-Local-1`
  (`raw-X2/support/workload/print-submit.txt`); the three scripts each have `source /home/census/X2-desktop-env.sh` on line 3;
  row 36 `ps` pid 5455 is in `raw-X2/debian-desktop/processes.txt:202` and missing from `process-executables.tsv` (race);
  O2 in PAPER §8 really names person-written executed configuration as unresolved.

Findings. None of them changes the outcome.

1. **Most of the `?` is structural: more data from this stand cannot fix it.** Where: X2C-RESULT "Fixed condition",
   and the "Coverage" paragraph. Evidence: 149 rows say "described-owner/intent evidence gap", and 27 + 26 more rows
   have a designation gap as their main reason (`dis.py adj`). Stock Debian has no person-designated declaration, and X2-PROTOCOL forbids designating one after
   the fact. So no row can ever become `recorded` or `derivative of a described program` on this stand. Fix: add one
   sentence saying this `?` comes from the protocol design, not from too few observations. For a rerun, a hypothetical
   declaration (e.g. package selection + enabled units) has to be fixed before classification.
2. **The κ and the 7.2% agreement say almost nothing about agreement on classes.** Where: measurement table. Evidence:
   Classification 1's `hole-none` reasons say "No valid class established; not a proven no-class object"
   (`X2-c1-classes.tsv`, e.g. `54a0a0356a`). So classification 1 used `hole-none` to mean "not established", while classification 2 gave
   affirmative classes. Most of the 218 differences come from the two submissions using the labels differently. They are
   not substantive disagreements. The report says this in prose, but the table invites misreading. Fix: add a footnote
   under the κ row saying the two submissions use the labels differently, so κ cannot measure agreement on classes.
3. **The reading "a hole label is not a class" is correct, but the report does not anchor it in the protocol.** Where:
   "zero pairs assign different affirmative classes … cannot be substituted for §9.2's different-class-assignment limb".
   Evidence: X2-PROTOCOL lists `hole-none`/`hole-two` next to the classes as labels, and §5 defines only derivative and
   data, plus recorded through P1. The reading is literal, not invented. A reader still has to take it on trust. Fix: cite
   the protocol line "Classify every residual … `recorded (works)`, `derivative of <program>`, `data`, `hole-none`, or
   `hole-two`" and the §5.1 definitions next to the claim.
4. **Row 218: the spool evidence does not name the files it compares.** Where: "row 218 … specifically
   `d00001-001` … byte-identical 138-byte copy". Evidence: `raw-X2/spool-copy-check.json` has only byte counts and a
   sha256, with no original path and no spool member path. The link to `d00001-001` comes only from
   `X2-residual.tsv:218` samples. Fix: add `original_path` and `spool_path` to the check (or a sha256 of
   `/var/spool/cups/d00001-001` from `raw-X2/debian-desktop/files.tsv`).
5. **13 account rows: one adjudication reason does not engage the specific two-class claim.** Where: `raw-X2C/disagreements.tsv`,
   hole-none→hole-two rows (Debian-gdm, _apt, sshd …). Evidence: all 27 "candidate definition boundary" rows share one
   generic `why` ("program-generated origin does not establish described-owner status"). For accounts, §5.1 lists "users"
   as running components with no evidence needed. The factual gap is that the creator was the package maintainer script
   (adduser), not the program "itself". Fix: give the account family its own one-line reason that states this specific gap.
   The outcome stays `?`.
