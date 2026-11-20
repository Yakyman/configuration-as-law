VERDICT: AGREED

Independent review, 2026-11-19. Scope: X3-RESULTS.md, X3-PROTOCOL.md, cited data; checks (1)–(4) only. Paper §5 and §9 read from PAPER.html; protocol hash `d89ddfb1…` matches `raw-X3/protocol-fixed.sha256`, and `raw-X3/protocol-final-recheck.txt` records OK for protocol, shared rules, PAPER and the B inputs.

Summary: the outcomes `? / ? / ?` for Checks 2/4/5 follow §9.1. Every failure that fired is either specific to X3 (same-session exec, mount stacking, root noexec) or shared with B through the common catalog, base image and ownership assumptions. No inherent-property argument is given, so `0` is not available. Counts match the data. All 5 sampled claims match their evidence. The findings below are wording fixes and do not change any outcome.

1. **Counts match.** The RESULTS coverage table (39 = 36/1/2; 9 = 6/1/2; 102; 9 = 7 pass + 2 fail; 32) equals `raw-X3/comparison-counts.json`. X3-COMPARISON.md has 185 `| same` rows (36+6+102+9+32) and 2 `| different` rows. In `raw-X3/final/browser.jsonl`, `browser-assertion` has 7 `passed: true` and 2 `passed: false`. No fix needed.

2. **Sample 1 (same-session hello, pip/npm variants, old/fresh sessions) is confirmed.** `raw-X3/final/runtime.jsonl` shows:
   - line 12: rc 126 after a successful apply (generation 58);
   - line 13: `Hello, world!` rc 0;
   - lines 7–8: pip install rc 0 and `PYTHON_PACKAGE_EXECUTED`;
   - lines 9–10: npm `added 1 package` and `NODE_PACKAGE_EXECUTED`;
   - lines 18/19: `RC=126` / rc 0;
   - lines 22/23: `RC=126` / rc 126.

   No fix needed.

3. **Sample 2 (browser) is confirmed.** In `raw-X3/final/browser.jsonl`, lines 30 and 72 are `catalog removal archives new Chromium home files` with `passed: false`. Lines 41 and 82 show the 40-byte `Crash Reports/settings.dat` remaining under both `keep` and `delete`. No fix needed.

4. **Sample 3 (own 0755 file) is confirmed.** Lines 5–8 of both `raw-X3/final/authority.jsonl` and `B/raw/fb1/check-authority.jsonl` show the same hash `1aab5d66…`, mode 755, UID 1000, rc 126 without the exception, and rc 0 with it. Declaration hashes are unchanged across each command. No fix needed.

5. **Samples 4–5 (mount defect, root supplement) are confirmed.**
   - `raw-X3/mount-exhaustion-diagnosis.txt` shows 49174 mountinfo entries, a limit of 100000, and 13G available.
   - `tests-final-launch-ready.txt` shows 26 mounts at the start.
   - `raw-X3/root-noexec-supplement.txt` shows `BASELINE_ROOT_EXEC_RC=126`, `AFTER_MANUAL_ROOT_EXEC_RC=0` and 30 mounts at the end.

   No fix needed.

6. **Check 2: the pip/npm interpreter variants are filed only under "P3/O5 hole". The result does not say that the fixed clause fires on the stand.**
   - Where: X3-RESULTS.md, "Additional measurements", rows `python3 -m pip` and `Node invokes npm CLI`.
   - Evidence: runtime.jsonl lines 7–10. Only `python`/`node` are declared, yet an undeclared package is installed and its code runs.
   - Why it matters: §9.3 lists "programming language package managers (pip, npm)" as an installation channel in its own right, separate from "interpreters executing user scripts" (O5). Reading these rows only as O5 understates them. Unless the P3/O5 hole is resolved, Check 2 clause 1 ("a channel installs or launches a program although the declaration does not permit it") fires on the X3 stand.
   - The outcome stays `?`: this was seen on one stand only, B did not measure it, and no property argument is given.
   - Minimal fix: add one sentence saying that clause 1 fires on X3 for the pip/npm channel through the interpreter entry, unless P3/O5 classifies the package as a derivative of the declared runtime. The cause is attributed to the stand, so the outcome is `?`.

7. **Check 5: root's noexec denial is described as "not decided" rather than as the fixed clause firing.**
   - Where: X3-RESULTS.md, row "Root launches own native file on data mount", and X3-ROOT-SUPPLEMENT.md.
   - Evidence: `BASELINE_ROOT_EXEC_RC=126` for UID 0 with full CapEff.
   - Why it matters: clause 4 ("the system restricts root's own privileges") fires on the X3 stand because of its noexec design. The `?` is correct only because the cause is the hybrid stand, as the result itself says elsewhere. It is not correct on the ground that P7's scope is undecided.
   - Minimal fix: say that clause 4 fires on the X3 stand, is attributed to the X3 noexec design, and gives `?`. Keep the P7-scope sentence only as a separate hole note.

8. **The second mechanism is a hybrid, which departs from one sentence in the frozen protocol.**
   - Where: X3-PROTOCOL.md says "the selected second mechanism is Landlock itself". The final instrument is Landlock ABI 2 plus global noexec/exec bind mounts.
   - Evidence: X3-SOURCE-DISPOSITION.md, "Dynamic ELF smoke repair"; X3-STAND.md.
   - The change is disclosed, it is dated before any measurement, and no criterion was changed. No rule was invented. However, "protocol stayed unchanged" in RESULTS is true only of the file.
   - Minimal fix: add to RESULTS one clause naming this as a deviation of the instrument from the protocol's mechanism choice.

9. **Sub-scope outcome symbols could be misread as check outcomes.**
   - Where: X3-RESULTS.md, coverage table ("bounded fixture's `1`") and the differences table ("Scoped lifecycle `1`").
   - Under §9.1 an outcome belongs to a check, and Check 4 here is `?`.
   - Minimal fix: replace the `1` with "all bounded fixture assertions pass".

10. **No invented classification rule was found.**
    - The browser failure is reported under both base-present and catalog-only readings, and the condition fires under each; the remaining reading is left unresolved.
    - Own-file execution is recorded as "no contradiction decided".
    - Bash `USER_SCRIPT` stays an O5 hole.
    - O1/O2/O4/O6/O7/O9 keep their paper status.

    No fix needed.
