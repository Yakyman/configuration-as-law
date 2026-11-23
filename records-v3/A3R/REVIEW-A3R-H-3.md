VERDICT: AGREED

Review of `RESULT.md` after fix round 2, 2026-11-22 UTC. Read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4,
`../SENTENCES.md`, (not published: orchestration and working notes), (not published: orchestration and working notes), `RESULT.md`, `FIX-A3R-H-2.md`,
`REVIEW-A3R-H-2.md`, all files under `A3R/fix-a3r-h-2/`, `compare/STATS.md`, `adjudication/rows.tsv`,
`fix-a3r-h-1/code_extent.tsv`, and selected rows or lines of (not published: outside selected checks and direct evidence),
`in/raw/lived/raw/003-packages-root-dpkg-query.out` and (not published: over 20 MB: raw trace, snapshot, index or operational log). No raw dump
was read beyond the sample listed below.

## Findings

None. No blocking or minor defect was found within the four points checked. The checks below record what was
verified and how.

## Handling of the previous review (`REVIEW-A3R-H-2.md`)

1. **Finding 1 (card 9 omitted the user-instance markers): handled.** The corrected search covers both roots.
   Evidence: `fix-a3r-h-2/raw/helper-source.txt` lines 100–110 now include
   `USER_INSTANCE_ENABLED_STATE_DIR => '/var/lib/systemd/deb-systemd-user-helper-enabled'`, and lines 576–580 select
   it for user units. An independent parse of `160-filesystem.out` gives 142 regular files under the two roots: 75
   `.dsh-also` lists and 67 markers (56 system, 11 user). That matches `helper-witnesses.tsv`. An independent
   whole-table search of `joined.tsv` finds exactly 29 rows whose name is an ancestor of a marker. Of these, `/`,
   `/var` and `/var/lib` do not list the helper directories among their members. The other 26 equal card 9 in
   `fix-a3r-h-2/code_extent.tsv`. `fix-a3r-h-2/added-memberships.tsv` holds exactly the five IDs the previous review named. Card 9
   now has 26 rows (19 system groups, 4 user groups, 2 parents, `/var/lib/systemd`), and the distinct total is 142.
   The card-9 disposition rests on the same source facts as before: the S2.2-6 and S2.2-1 sentences are quoted
   unchanged, and no rule was added.
2. **Finding 2 (S2.5-1 listed among supporting sentences): handled.** The introduction to "Cards that did not
   survive" now limits support to the Section 2.2 and Section 3 sentences. It says S2.5-1 is quoted only to explain
   why the cards are not OUTSIDE. No disposition changed (`fix-a3r-h-2/raw/result.diff`).

## Checks without finding

3. **Text and failure conditions (point 1).** The result keeps "no published-check outcome" and proposes no change to
   the text. It keeps the undecided overlap as a hole. Card 6 and the sample unknowns stay "? under S3-2". S2.5-1 is
   not used as an exemption. A regenerated `diff -u` of `fix-a3r-h-2/RESULT.before.md` against `RESULT.md` is
   byte-identical to `raw/result.diff`. The changes are limited to card 9's extent and source citation, derived
   totals and links, and the S2.5-1 sentence.
4. **Numbers (point 2).** These figures match their data files:
   - `compare/STATS.md`: 5,212 objects; 3,854 = 73.94 %; kappa 0.55445; 2,010 adjudicated.
   - `adjudication/rows.tsv`: 681 / 226 / 441 / 621 / 41.
   - `code_extent.tsv`: card 1 has 115 rows (69 + 45 + 1), card 7 has 4, 3 overlap, 116 distinct, card 9 has 26, no
     overlap with cards 1 and 7, 142 overall.
   - `counts.json` and (not published: external working record) agree with all of the above.
   - Cards 1 and 7 equal the round-1 ledger field for field.
5. **Sampled evidence (point 3), 8 claims:**
   - (a) `003-…dpkg-query.out` line 227 reads `init-system-helpers 1.69~deb13u1 ii`.
   - (b) Every numbered line of (not published: external working record) (100–113, 341–379, 568–580) matches the cited primary-source
     URL exactly. Line 360 `next if -e $statefile;` comes before link creation, and lines 369–370 carry the
     "Store the fact that we ran enable" comment.
   - (c) `joined.tsv` row `60af4555f895a621f8fdd8b5` has the single member `…/default.target.wants/pulseaudio.service`,
     which is a regular file in `160-filesystem.out`.
   - (d) The user groups hold 1, 1, 1 and 8 markers, as the round-2 independent review states.
   - (e) The members of `/var/lib/systemd` (`9a8b54a65f2c0b01ccabcf0e`) include both helper directories.
   - (f) All `.wants` entries under both roots are regular files. The 23 groups plus 2 roots account for all 25
     directories, so the example groups hold markers, not service symlinks.
   - (g) All 1,066 digests in `frozen-inputs.sha256.json` match the current files.
   - (h) `bin/check_quotes.py A3R/RESULT.md` reports 14 quotations checked and 0 missing.
6. **Scope (point 4).**
   - Round 2 wrote only `RESULT.md`, `FIX-A3R-H-2.md` and the new folder `A3R/fix-a3r-h-2/`, and frozen
     inputs are unchanged.
   - It ran no probe, VM, sample draw or classification. Its only external read was the primary-source documentation
     of the installed helper version.
   - No other task folder is cited.
   - The files contain no host names, no home paths of the host and no private labels. Object names found on the
     guest and listed in `helper-search.tsv` are inventory data and not statements by the writer.
