VERDICT: AGREED

Review of `L/RESOLUTIONS.md` (2026-11-19, independent review). Read: the shared rules of the checks, `PAPER.html` §5 and §9 (plus O2/O5–O7 from §8),
`L/RESOLUTIONS.md`, and the decisive rows it cites in `A/RESULT.md` and `B/RESULTS.md`. Sample of 5 evidence sources opened:
`raw/settings/android.txt`, `raw/lifecycle/snap-snapshots.txt`, `raw/lifecycle/page6.txt`, `raw/lifecycle/apple-testing.txt`,
`raw/execution/fapolicyd-languages.txt` + `fapolicyd-shell.txt` (same pinned commit).

Results of the four checks:
- (1) Outcomes vs FIXED conditions: all five cases end in `?` for "does the literature resolve the §5 case". None changes a
  §9 outcome: O5 stays `?` exactly as §9.3 requires; the P7/P4 case keeps B's `?` (B/RESULTS.md:10, :147 — the §9.6
  condition fired on the stand, but §9.1 gives 0 only if it follows from the property, which B left unshown); case 1 states
  that A's editor-configuration collision stays decisive (RESOLUTIONS.md:7; A/RESULT.md:5 = 0). Consistent.
- (2) Numbers: API 23 (android.txt:479, :593), 31 days / auto snapshot on removal / Ubuntu Core off / 2.39+ / `--purge`
  (snap-snapshots.txt labels L338, L467, L487), SNAP_COMMON overwrite (L387), MSIX downgrade sentence (page6.txt label L61),
  Apple App Group + keychain exceptions (apple-testing.txt labels L51–L53), fapolicyd commit `b94857b4…` (fapolicyd-commit.txt).
  All match.
- (3) No invented rule: every semantic data/derivative/owner assignment is written as **unknown**; the two "Mechanism
  inference" notes (SELinux, AppArmor) are labelled as such and are not used to classify any case.
- (4) Sampled claims hold: Android "doesn't treat the configuration of components as user data" (android.txt:521);
  `text/x-shellscript` is absent from `%languages` and allowed by `72-shell.rules`; MSIX "When uninstalling or downgrading
  MSIX, MSIX preserves the user's appdata" is in the Downgrade section; Snap and Apple quotes verbatim; B's "denied with empty
  lists, allowed after explicit exception, same bytes/mode/owner/inode" matches B/RESULTS.md:80, :138, :147.

Findings (minor, none changes the verdict):

1. **Case-level `?` labels can be misread as §9 outcomes.** Where: RESOLUTIONS.md:26, :45, :63, :77, :102. Evidence: §9.1
   reserves 1/0/? for checks; case 1's "?" sits next to a census check whose outcome is 0 (A/RESULT.md:5). Minimal fix:
   write "Literature resolution: ?" and, in case 1, add "Check 1 outcome stays 0 (A/RESULT.md)".
2. **Line references use the `Lnn:` labels inside the evidence files, not file line numbers.** Where: RESOLUTIONS.md:91
   ("lines 51–55"), :94 ("line 61"), :97 ("lines 338, 380–403, 465–487"). Evidence: in page6.txt the cited sentence is file
   line 65 (label L61); in apple-testing.txt labels L51–L55 are file lines 55–59; snap-snapshots.txt is offset the same way.
   A reviewer using `sed -n 61p` lands on the wrong line. Minimal fix: write "label L61" (etc.) or cite file line numbers.
