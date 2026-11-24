VERDICT: AGREED

# Review of S1-A after fix round 1 (`S1/ARGUMENT.md`, `S1/FIX-S1-A-1.md`)

Recorded 2026-11-23 UTC. Inputs read: (not published: orchestration or scratch), `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md`,
`SUP1/step-1.md`, (not published: orchestration or scratch), (not published: orchestration or scratch), `S1/REVIEW.md`, `S1/ARGUMENT.md`, `S1/QUESTIONS.md`,
`S1/FIX-S1-A-1.md`, everything under `S1/fix-s1-a-1/`, `S1/raw/input-hashes.tsv`, the "By kind" table of
`D1/compare/STATS.md`, the `id` and `kind` columns of `D1/compare/joined.tsv`, and the command lines of the performer's
run log for the fix round. Outcomes checked: Understanding 0; Reproducibility ?; Removal ?. All three follow the
published text and the committed outcome rule of `SUP1/step-1.md`. Findings 1–6 confirm this. Findings 7–9 are
minor record defects. None of them changes an outcome.

1. **Every finding of `S1/REVIEW.md` was handled, and each disposition is accurate.**
   *Where:* `S1/FIX-S1-A-1.md` table; `S1/ARGUMENT.md`; `S1/QUESTIONS.md`.
   *Evidence:* I checked each one against the current text and the pre-fix snapshot. The snapshot
   `S1/fix-s1-a-1/before/ARGUMENT.md` is the reviewed version: its lines 1, 118, 141, 143, 160, 201, 209, 213 and 260
   carry the passages that the previous review cites.
   - Finding 1: P4 row, line 141, now stipulates that "A subsequent installer request adds a line to D". Both
     observations precede any such request. The word "reject" no longer occurs in the file.
   - Finding 2: lines 116–118 and 139 record `alpha` and `beta` directly under the first clause of S8.2-17. The pair
     no longer rests on default coverage.
   - Finding 3: no change was needed, and none was made.
   - Finding 4: the first line reads `Removal ?`. Steps 2–5 of §5 are restricted to installed objects and settings.
     The `[L0, LS]` → `[L0]` pair is written out at lines 217–237, and Question 5 records both readings.
   - Finding 5: the blanket denial of a force criterion is withdrawn at line 213, and the last paragraph of
     `S1/QUESTIONS.md` is rewritten.
   - Findings 6, 8 and 10: no change was needed.
   - Finding 7: the D legend (line 256) and the account row (line 280) are made conditional.
   - Finding 9 (g, h): covered by the fixes for findings 4 and 5.
   *Minimal fix:* none.

2. **Removal "?" follows the text and the committed outcome rule. No rule was invented.**
   *Where:* `S1/ARGUMENT.md` §5; `S1/QUESTIONS.md` item 5.
   *Evidence:* The restricted derivation uses only sentences of the text: S8.3-1, S8.1-14, S8.2-16/17/18 and S8.3-4.
   The full consequence depends on two readings of S8.2-11 ("a value chosen by a person"), which `S1/REVIEW.md`
   finding 4 had already identified. `SUP1/step-1.md` says: "Where whether a consequence follows depends on a choice
   between two readings of a sentence, the readings are recorded as a question for the author and the consequence
   gives “?”". The fix adds two qualifications:
   - the narrow reading is not stated in S8.2-11 ("a person", not "the person of this computer");
   - the Section 8.5 exclusion is retained.

   Both are recorded as open, not decided. The Section 8.5 exclusion is not called a gap (line 235), which agrees with
   (not published: orchestration or scratch).
   *Minimal fix:* none.

3. **Understanding 0 stands, and the corrected P4 and temporal stipulations add no rule to the hypothesis.**
   *Where:* `S1/ARGUMENT.md` lines 141–145 and §3.
   *Evidence:* The new P4 stipulation is the one `S1/REVIEW.md` finding 1 proposed. It satisfies the stricter reading
   of S8.3-7, so the outcome no longer depends on how that sentence is read. Line 145 says the transition model is
   "a stipulation of this mathematical pair, not a rule added to the hypothesis". It is part of how the constructed
   system is specified, which is what the "two states" route of `SUP1/step-1.md` asks for. I tried to refute the pair
   on S8.1-12, S8.2-11 (granularity of the chosen object), S8.3-7 and identity of D. I found no sentence that defeats
   it. Each attempt is already answered at lines 158–162. A.4.4 lists an account's "numeric identifier" among what is
   in force under the account's line, which supports treating the UID as part of the account setting.
   *Minimal fix:* none.

4. **The numbers in the result files match the data files.**
   *Where:* `S1/ARGUMENT.md` §7; `S1/fix-s1-a-1/raw/validation.txt`; `S1/fix-s1-a-1/raw/output-hashes.tsv`.
   *Evidence:* I recounted from `D1/compare/joined.tsv` independently:
   - 16,375 data rows in 45 kinds.
   - All 45 kind and count pairs of §7 equal the "By kind" table of `D1/compare/STATS.md` (`diff` is empty).
   - All 45 example IDs exist in `joined.tsv` with the stated kind.
   - The counts sum to 16,375.

   I recomputed the SHA-256 fingerprints, and every listed file matches: the 7 in `S1/raw/input-hashes.tsv`, the 17 in
   `S1/fix-s1-a-1/raw/preserved-input-hashes.tsv` and the 10 in `output-hashes.tsv`. The frozen inputs, the previous
   review and the original raw evidence are therefore unchanged.
   *Minimal fix:* none.

5. **Sample of cited evidence (8 claims): all 8 hold.**
   *Evidence:*
   - (a) Rerunning `/usr/bin/python3 -I (not published: orchestration or scratch) S1/ARGUMENT.md` gives "quotes checked: 50; not found in
     TEXT.md: 0", as `S1/fix-s1-a-1/raw/quote-check.txt` states.
   - (b) "45 exact matches" between sentence IDs and quotations: every `- S8.x-n: «…»` line equals `SENTENCES.md`.
     The validation script asserts this, and the quote check confirms it.
   - (c) Kind counts and IDs: see finding 4.
   - (d) "17 fingerprints unchanged": see finding 4.
   - (e) Line 233: "S8.2-11 says “a person”, not “the person of this computer”". This is true of S8.2-11 as published.
   - (f) Line 213: S8.1-11 gives accounts and services force criteria "without an explicit classification
     restriction". This is true of S8.1-11 ("A service is in force if it is enabled; an account, if it exists.").
   - (g) Line 150: A.4.4 "includes an account's numeric identifier". The A.4.4 passage quoted at line 188 is exact.
   - (h) "No behavioural experiments or machines run in this fix round". The fix-round command lines contain only
     local reads (`cat`, `sed`, `rg`), local Python edits and validation under `S1/`. There is no remote login,
     download or virtual machine.
   *Minimal fix:* none.

6. **The work stayed inside its task.**
   *Evidence:* The fix round read only (not published: orchestration or scratch), (not published: orchestration or scratch), `S1/ARGUMENT.md`, `S1/REVIEW.md`,
   `SUP1/step-1.md`, `SENTENCES.md`, `S1/QUESTIONS.md`, `TEXT.md`, `S1/raw/input-hashes.tsv`,
   `S1/raw/validation.txt`, (not published: orchestration or scratch) and the F1/F10/F11 passages of `OP/OPINION.md`. All of these are
   named by its task or by the original task. It wrote only under `S1/`. Its outputs went to a new directory,
   `S1/fix-s1-a-1/`, created with `exist_ok=False`, and nothing frozen was overwritten. No other task folder and no
   classification decision was read. The new Removal pair is the reviewer's logical case, written out on request.
   It is not an added experiment or machine case.
   *Minimal fix:* none.

7. **A record of the fix round was deleted.**
   *Where:* `S1/fix-s1-a-1/`. The editing script (not published: record outside selected evidence) was created, run and then removed by the
   final command (`Path('S1/fix-s1-a-1/revise.py').unlink()`).
   *Evidence:* A.4.1: "All records of the checks are dated, never deleted". The effect of the script is preserved
   exactly in `S1/fix-s1-a-1/raw/changes.diff`, and its text survives in the run log, so nothing is lost. The deletion
   is still not mentioned in `S1/FIX-S1-A-1.md`.
   *Minimal fix:* restore the script text from the run log into `S1/fix-s1-a-1/`, or add one line to
   `S1/FIX-S1-A-1.md` saying it was a temporary editing script whose full effect is `raw/changes.diff`.

8. **One sentence of the disposition has no evidence in this round.**
   *Where:* `S1/FIX-S1-A-1.md`, first paragraph: "Separate reasoning for the three consequences informed the
   corrections."
   *Evidence:* The fix-round command lines show no parallel parts and no new per-consequence notes. The only
   per-consequence notes are the original `S1/raw/understanding.md`, `reproducibility.md` and `removal.md` from before
   the review.
   *Minimal fix:* delete the sentence, or point it to the files it means.

9. **A legend sentence can be read as contradicting S8.2-19. The wording predates the fix.**
   *Where:* `S1/ARGUMENT.md` line 258: "S8.2-2/19 permits no mandatory line or voluntary recording".
   *Evidence:* S8.2-19: «What need not be recorded may also be recorded in the declaration.» The sentence can be read
   as "permits neither a mandatory line nor voluntary recording". The intended meaning, "no line is mandatory, and
   voluntary recording is permitted", is the one the rest of the file uses (lines 96–97).
   *Minimal fix:* "S8.2-2: no line is mandatory; S8.2-19: voluntary recording is permitted."
