VERDICT: AGREED

Review 2 of `C/ATTACK.md` after FC1 (2026-11-19). Scope: (1) outcomes against the fixed §9.1/§9.2 conditions, (2) numbers against the data files, (3) invented rules, (4) an evidence sample of 5 claims. The headline **0** follows from H1 (rows 01, 09) under the fixed condition "belongs to two classes with different consequences" (§9.2) and the §9.1 counterexample clause. All six REVIEW.md findings were handled. The two findings below are nits and do not change any outcome.

1. **Some evidence locators are still ambiguous, the same defect as REVIEW.md finding 6, but on other entries** (nit; check 2). `SOURCES.md` E19 (`raw/host-details.txt` L23–35), E20 (L26–31) and E21 (L17–30) cite embedded page labels. `raw/host-details.txt` contains 4 documents (`grep -c '^L1: '` = 4), so each label occurs more than once. For example, L26–31 appears at file line 29 (BlueZ storage), 118 (crontab), 209 (systemd-coredump) and 249 (capabilities). The coredump text E20 needs is at file lines 209–214 ("an image of the memory contents of the process", L30). Minimal fix: give the section name or the physical file lines, as was already done for E13, E14 and E24.

2. **Row 09's wording says more than the text supports** (nit; check 3). The row says "§5's code clause imposes derivative status" on an interpreter-run script. §9.3 (PAPER.html L226) explicitly calls script execution by an interpreter an O5 case, so the text does not decide whether the script is code "within" the interpreter. The outcome is unaffected. If the script is "within", it is data plus derivative, which is the dual class with different consequences. If O5 is undecided, the classification is undecided, which also gives 0 under §9.1. Minimal fix: replace "imposes" with "under the 'within' reading imposes; otherwise the O5 boundary leaves the class undecided — 0 either way".

Checked and found correct:
- **REVIEW.md findings 1–6 were all handled** (FIX-1.md table vs ATTACK.md rows):
  - Findings 1 and 2: rows 04, 06, 07, 11, 17, 33, 18 (installer branch) and 36 (rewritten branch) now have classification 0, as do rows 10 and 13–16. The rescue rules (decomposition, suite-as-program, output-as-need) were removed.
  - Row 20 was deliberately not set to 0. The exception quotes §5.1 L133 as REVIEW.md finding 1 allowed. Its evidence holds: `raw/hardware/web3.json` L91–92 says that KeyMint refuses use with `KEY_REQUIRES_UPGRADE` and that `IKeyMintDevice::upgradeKey` "generate[s] a new keyblob". Keystore makes the call and deletes the old blob. Even if Keystore is read as a co-owner, P6's shared-derivative clause covers that, so no second class with different consequences arises. Classification 1 / lifecycle ? is consistent.
  - Finding 3: H3 / row 03 is now 1, with scope ? and law ?.
  - Finding 4: H2 / row 02 is now explicitly conditional on the archive staying on the computer.
  - Finding 5: row 10 now has classification 0.
  - Finding 6: the E13, E14 and E24 locators were fixed. Physical file line 911 is L16 "Users can create or modify the keyfile connection files manually".
- **Outcomes follow the fixed conditions**:
  - Every 0 in the table cites an undecided or dual classification (§9.1 "cannot classify", §9.2 "two classes with different consequences" / "text … does not resolve").
  - Every ? is missing evidence (row 05), law/lifecycle/scope (O4, O5, O9 per §9.3), or an unproven impossibility.
  - Interpreter law stays ? as §9.3 requires.
  - Row 24 (unlisted microcode, O9 scope ?) is treated the same way as the accepted H3 treatment.
- **Numbers match the data files**:
  - The table has 42 rows.
  - The classification-0 set {01, 04, 06, 07, 09, 10, 11, 13, 14, 15, 16, 17, 18, 33, 36} plus conditional 02 matches `fix-1/raw/document-validation.json` and `fix-1/raw/final-audit.md`, and the FIX-1 listing totals 15.
  - The paper SHA-256 `e6978714…5d93a1` matches, and `paper_unchanged` is true.
  - `broken_local_links` is empty in the 08:39 UTC rerun.
  - PAPER.html L133, 134, 135, 145, 205, 226, 237 and 238 contain the quoted text.
- **No invented classification rule** was found in rows 01–42 or H1–H4. Row 20 rests on L133 only.
- **Evidence sample (5 claims)**:
  - E26 KeyMint upgrade (`web3.json` L91–92): confirmed.
  - E14 manual keyfile editing (`raw/network.txt` file line 911): confirmed.
  - E18 DKMS generates its own signing key and uses it for builds (`raw/dkms-timers.txt` L247–249, L256), which supports row 40: confirmed.
  - E02 `places.sqlite` holds bookmarks and history (`raw/applications/web-emacs-firefox.txt` file line 115, L109), which supports row 06: confirmed.
  - E20 coredump stores "an image of the memory contents of the process" (`raw/host-details.txt` file line 213): confirmed, but see finding 1 on the locator.
