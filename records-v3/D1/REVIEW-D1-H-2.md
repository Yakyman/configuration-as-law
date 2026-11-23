VERDICT: DISAGREE

Review of `RESULT.md` after fix round 1 (check 1, Section 4.2), recorded 2026-11-22 UTC. Inputs read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4, `../SENTENCES.md`, (not published: orchestration and working notes), (not published: orchestration and working notes), `RESULT.md`, `FIX-D1-H-1.md`, `REVIEW.md`, `adjudication/HOLES.md`, and under `D1/fix-d1-h-1/`: `fix-d1-h-1/card-audit.md`, `fix-d1-h-1/sample-audit.md`, `recompute.py`, `summary.json`, `confirmed-rows.tsv`, `extent-search.tsv`, `final-unknown.tsv`, the two sample TSVs, `QUESTIONS.md`, `raw/`. For the sampled claims only: `compare/joined.tsv`, `adjudication/rows.tsv`, `compare/STATS.md`, `review/final-unknown.tsv`, `review/cards-5-8.md` (card 6), `review/cards14-raw/metadata-audit.tsv` and the saved Mint control records, `D1/review/raw/libreoffice-xslt.cxx`, `D1/review/raw/cockpit-development.html`.

`OUTCOME: 0` is correct and does not depend on any finding below: at least one gap (card 1, the Mint emoji font with empty maintainer scripts) holds under every reading considered here, and the per-machine adjudication outcomes are now reported as Section 4.1 gives them. The disagreement concerns the headline count and the stated extents.

1. **Card 6 is still refuted by the reading that finding 2 of the previous review rejected, and that card 3 now treats as undecided.**
   Where: `RESULT.md` line 90 ("Card 6 — REFUTED: the examples are established operational inputs under S2.2-1; automatic regeneration supplies no exemption"); `review/cards-5-8.md`, "Card 6 — REFUTED" ("so S2.2-1 decides MUST … the text does not say that every negative removal test is an exemption").
   Evidence: the card's premise (`adjudication/HOLES.md`, Hole 6) is that removal is undone by regeneration, "so the removal test is negative or only temporarily positive". The refutation decides MUST from S2.2-1 alone, against a negative or only temporary S2.2-2. Previous finding 2: "MUST follows only if S2.2-1 is read as a separate test, wider than the test S2.2-2 names. That is a choice between readings." The fix accepted that for card 3 (`fix-d1-h-1/card-audit.md`: "S2.2-1 can be read to include their selection behavior, while the designated removal test in S2.2-2 does not specify … No sentence chooses that scope"), but did not apply it to card 6. One reading is used to refute one card and called undecided for another.
   Minimal fix: mark card 6 CONFIRMED with its 20 rows, or record it as a question for the author, as was done for card 3. Update line 1 (5 confirmed holes, if confirmed) and the card dispositions.

2. **The S2.2-10 maintainer-script exclusion is applied to four Mint packages only. The fix's statement about shell requirements contradicts the rpm documentation.**
   Where: `RESULT.md` line 59 ("Three original rows with actual maintainer-script evidence are excluded by S2.2-10. A requirement for a shell is not itself evidence of a shell script."); `fix-d1-h-1/recompute.py` (`controls={'dmz-cursor-theme','fonts-noto-cjk','wamerican','yaru-theme-icon'}`, the only script check).
   Evidence: the rpm scriptlet manual (https://rpm.org/docs/latest/man/rpm-scriptlets.7) says: "The scriptlet interpreter dependency is automatically added by RPM". `/bin/sh` is the default scriptlet interpreter. Example: `tumbleweed-25d4e59fef6a08262890c4c4` (google-roboto-fonts, a card-1 example) requires "/bin/sh; /bin/sh; aaa_base; coreutils; coreutils; perl" (`review/cards14-raw/metadata-audit.tsv` line 431). Its adjudication note, "no code (repo filelist)", rests on a file list, and file lists do not contain scriptlets. Joining `confirmed-rows.tsv` with `review/cards14-raw/metadata-audit.tsv`: 110 rows in the established card-1/card-2 extent carry a `/bin/sh` requirement (Tumbleweed 74 + 6, Fedora 28 + 2). Their scriptlets were never examined. The fix excludes Mint rows by S2.2-10 when a script is seen, so these rows fail the fix's own test for "established".
   Minimal fix: apply the S2.2-10 ground everywhere or nowhere. If it is applied, move rows whose scriptlets are unexamined out of "established" (into unresolved membership) until their scripts are checked. Correct the quoted sentence for RPM packages.

3. **19 Mint rows moved from UNKNOWN into the established extents without the fact the fix's own ground needs.**
   Where: `RESULT.md` line 35 ("remove 19 Mint rows whose supposed missing fact was only the discarded metadata criterion"); `fix-d1-h-1/final-unknown.tsv` compared with `review/final-unknown.tsv`.
   Evidence: all 19 are now CONFIRMED in `confirmed-rows.tsv` (cards 1 and 2: e.g. tzdata, tzdata-legacy, cups-common, cups-server-common, mint-themes, libsnmp-base). Their earlier reason was "whole-object facts unresolved". Whether a maintainer script is present is a whole-object fact, and under finding 2's ground it decides the row. Saved control records exist for only two of the 19 (`mint-fonts-ubuntu-control.json`, `mint-mint-translations-control.json`, both with empty scripts). For the other 17 nothing establishes that scripts are absent.
   Minimal fix: keep the 17 rows without script evidence out of the established extent (as UNKNOWN or as unresolved membership), and recount 97 and the card-1/card-2 extents.

4. **The reported "number of rows" per hole is a lower bound, not the exact extent the task asks for.**
   Where: `RESULT.md` lines 59, 65, 71, 77 ("Established extent: N rows"), the "Verification confirmed rows" column, and line 81.
   Evidence: (not published: orchestration and working notes) step 1: "For a confirmed hole establish its exact extent". `fix-d1-h-1/extent-search.tsv` leaves 920 row/card memberships unresolved: card 1 has 359, card 2 206, card 3 46, card 5 309. Line 81 says this openly, but the per-card counts and the machine column are presented as the hole sizes.
   Minimal fix: label each per-card count and the machine column as "at least", and give the unresolved membership count beside each. The alternative is to resolve the memberships.

5. **Card 5 was widened beyond its card, but the sample table reports no new gap type.**
   Where: `RESULT.md` line 73 (title "Absent hardware and alternative execution environments") and line 108 ("New gap types 0").
   Evidence: Hole 5 in `adjudication/HOLES.md` is "support for hardware that is absent but could be attached". The 197 rows added from `review/card5-extent.tsv` are 192 Xen PV GRUB modules, `/boot/boot` and four CPU-microcode rows. These concern another hypervisor or boot platform, or present hardware under a hypervisor, not attachable devices. Recount: 58 original card-5 rows + 192 + 1 + 4 = 255, which matches the result.
   Minimal fix: state that card 5 was widened in verification, or count the boot-environment scope as a separate gap type, in line 108 and line 111.

6. **A stale sentence from the previous version remains.**
   Where: `RESULT.md` line 137 ("The confirmed Mint counterexample independently sets the overall outcome to 0.").
   Evidence: the result now has four confirmed gaps across Fedora, Tumbleweed, Mint and Flatcar, and the per-machine outcomes come from the adjudication (line 6).
   Minimal fix: replace it with a reference to the confirmed gaps and the adjudication outcomes.

7. **Handling of the previous review's findings (checked one by one).**
   - Finding 1: fixed. The outcome table now carries the adjudication case outcomes (Fedora/Tumbleweed/Mint/Flatcar 0, Talos ?), and the verification is labelled separately.
   - Finding 2: fixed for metadata as a MUST ground everywhere (no metadata-based MUST was found in `recompute.py` or in the samples). The S2.2-1-as-wider-test reading is still used for card 6 (finding 1 above).
   - Finding 3: fixed (card 3 CONFIRMED; both readings in `QUESTIONS.md`).
   - Finding 4: fixed (card 5 CONFIRMED; both alsa-sof-firmware rows removed from UNKNOWN and present in card 5).
   - Finding 5: fixed. All ten Xen/menu sample rows and microcode_ctl moved to card 5, and the seeds and ordered ids are unchanged (asserted in `recompute.py`).
   - Finding 6: fixed through the alternative the review offered (metadata ground dropped everywhere). Keeping guest-only ROMs NOT under S2.2-11/12 is literal.
   - Finding 7: the deviation is recorded at line 119. `recompute.py` reads only `compare/joined.tsv`, `adjudication/rows.tsv` and the verification's own earlier files.
   - Finding 8: recounted, but see findings 1–3 above.

8. **Verified without defect: numbers, sampled claims, scope.**
   - Unchanged metrics match `compare/STATS.md` (16524 objects, 15025 matching, 90.93 %, κ 0.55586). The per-machine rows equal the recount in the previous review.
   - Recomputed from `confirmed-rows.tsv`: card 1 410 (196/166/48), card 2 151 (48/54/49; 145 adjudicated + 6 added), card 3 319 (127 + 176 joined-account rows + 15 + 1 sample-linked rows), card 5 255. 1135 distinct ids, disjoint across cards. Per machine 496/314/132/193.
   - `final-unknown.tsv`: 97 rows (Fedora 11, Tumbleweed 5, Mint 13, Flatcar 68). Kinds 67/13/12/3/2. The decomposition 114 − 2 − 19 + 4 holds.
   - Sample counts: resolved 10 UPHELD / 20 CONFIRMED / 7 OUTSIDE / 3 UNKNOWN; agreed 57 / 3. These match the sample TSVs.
   - Sampled claims confirmed:
     - the notes of the named examples of cards 1, 2, 3 and 5 in `adjudication/rows.tsv`;
     - the agreed NOT/NOT dependency-only accounts behind the card-3 additions (`compare/joined.tsv`, e.g. `fedora-edac0a2e03ebf8334e8d8461`);
     - `libreoffice-xslt.cxx` lines 328–334 forbid writes, directory creation and network operations while allowing file reads;
     - `cockpit-development.html` around line 933 places the bridge on the server side.
   - `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`: 12 quotes checked, 0 not found.
   - No probe, VM or read of `D1/c1/`, `D1/c2/` or `(not published: adjudication scratch)` in this round. No new rule or failure condition was asserted.
