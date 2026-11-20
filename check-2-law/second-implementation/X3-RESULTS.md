# X3 — second mechanism, 2026-11-19

**Checks 2 / 4 / 5: `? / ? / ?`.** A second disposable stand was built and measured: **Landlock ABI 2 + noexec/exec bind mounts**, with an independently implemented **SQLite** controller, replacing B's AppArmor/JSON controller. The paper's conditions and protocol stayed unchanged (hash verification). This collects evidence; it decides no open problem. B's prepared OS, catalog, fixture programs and externally assigned state ownership remain shared assumptions.

The complete requested **case → B result → X3 result → same/different** table is X3-COMPARISON.md, with both raw references on every row. B baseline preserves REVIEW-2's corrections. Stand and scope, [sources](X3-controller.py), source-review findings/dispositions. Independent review: **AGREED**, X3-REVIEW.md. Counts were independently reproduced and five empirical chains sampled; this accepts the reported evidence/attribution, not the hypothesis.

## Coverage and comparison

These are observations/controls, not independent security boundaries or property verdicts. Counts come from [comparison-counts.json](raw-X3/comparison-counts.json).

| B suite | B / X3 recorded cases | Comparison after repair |
|---|---:|---|
| Check 2 full list, including controls | 39 / 39 | 36 same effects; 1 different; 2 identity/audit adapters |
| FB1 build supplement | 9 / 9 commands | 6 same; 1 setup-residue difference; 2 identity/audit adapters; all 9 X3 command expectations met |
| Check 4 alpha/beta/shared, keep/delete | 102 / 102 assertions | All 102 agree and pass; this is the bounded fixture's `1`, not overall Check 4 |
| FB1 real Chromium lifecycle | 9 / 9 assertions | All agree: 7 pass, 2 home-state archival failures |
| FB1 Check 5 | 32 / 32 command events | All effects agree; one unmet Unix-execution expectation on each stand |

The build setup residue is disclosed: `built` already existed from X3's retained initial batch at `empty-no-exceptions`; the next event removes it before compile/deny/allow/revoke measurements. Likewise the final law build row demonstrates compiler denial, not absence of a pre-existing artifact. The original Python script remains denied, while Bash runs `USER_SCRIPT` on both stands; their O5 attribution is unresolved. Direct loader results differ numerically (B 126, X3 127), but both prevent the payload: X3's loader starts and noexec refuses its executable mapping. Chromium warnings differ, while the required DOM/extension markers succeed. The table compares those effects rather than interpreting unrelated warning text as failures.

## What repeated, what differed

| Case | B | X3 | Attribution under the unchanged paper |
|---|---|---|---|
| Undeclared native download, archive, AppImage; compiler and installed manager front doors | Tested attempts denied | Same tested attempts denied | Bounded gate evidence only; missing scheduler prerequisites are no enforcement credit |
| Explicit download home/tmp, build, then revoke | Allowed operations work; fresh revoked launches denied | Same, with broader home-directory build exception | Positive controls; no claim that every channel exception works |
| Personal hello apply **and run in the same shell** | Installs and prints hello | Installs successfully, then exec denied 126 | Different, X3 session-policy defect/limitation; a fresh session runs hello without another declaration change |
| Alpha/beta removal, saved-generation retention, shared consumer, rollback, keep/delete after GC | Fixture assertions pass | Same | Scoped lifecycle `1`; ownership was supplied, not discovered |
| Browser's new home `Crash Reports/settings.dat` after removal and GC | 40-byte file remains unarchived, both settings | Same, with hashes unchanged within each case | Repeated stand defect: shared directory-assignment/base-catalog design, not shown inherent in P6 |
| Own 0755 file, empty lists, same bytes/UID/GID/inode | Denied 126; root download exception makes it run | Same | Repeated P7/P4 boundary; both catalogs lack a personal-declaration route for arbitrary own executables. No contradiction decided |
| Root-version conflict, root fields, scope, allowlist/denylist; root manual write/DAC override | Rejections and positive controls succeed | Same | Scoped P7 behavior only, not a universal root-privilege proof |
| Initial X3 rollback | B rollback succeeds | Initial X3 fails when accumulated mounts exhaust kernel capacity; repaired rerun succeeds | X3-specific implementation failure, retained below; not property `0` |

Exact evidence for the differences and repeated failures:

- Same-shell apply/run: [B row 26](../stand/raw/law-v2/26-install.json), [X3 row 26](raw-X3/final/law/26-install.json); [runtime supplement](raw-X3/final/runtime.jsonl), lines 12–13: repeat denied 126, fresh-session `Hello, world!` rc 0. This preserves the original failed scenario; it does not claim ordinary installation is impossible by every non-bypass workflow.
- Browser: [X3 browser JSONL](raw-X3/final/browser.jsonl), lines 24–30, 39–41, 66–72, 81–82; [B browser JSONL](../stand/raw/fb1/check-browser-lifecycle.jsonl), same event labels. Under the base-present reading, `delete` removes assigned profile state while base Chromium remains present (failure clause 1); under the catalog-only reading, the home derivative remains active without an owner/archive (clause 2). The fixed condition fires in the stand under either reading for the delete sequence; **the cause is shared implementation scope**. The keep-only owner reading remains unresolved.
- Own file: [X3 authority JSONL](raw-X3/final/authority.jsonl), lines 5–8; [B authority JSONL](../stand/raw/fb1/check-authority.jsonl), lines 5–8. Same-file predicates remain true. Restricting P7 to non-execution file operations would change the fixed condition and is not done.

A failure seen with two enforcement mechanisms points toward examining the property question, but these two stands still share the catalog and ownership assumptions capable of causing it. There is no inherent-property argument for `0`. The observed same-session difference and repaired mount failure point directly to X3's mechanism/implementation.

## Additional measurements, with missing B baselines explicit

[Runtime supplement](raw-X3/final/runtime.jsonl) records the effective declaration and installed paths around each action. These rows do not replace B's original channel list.

| Case | B frozen baseline | X3 | Comparison/interpretation |
|---|---|---|---|
| Four pip/npm commands with Python/Node declared | Not measured there | Direct script entry points denied 126, lines 3–6 | Not comparable; declaration does not by itself allow installer scripts |
| `python3 -m pip` from writable offline source; import | Not measured there | Package installs, `PYTHON_PACKAGE_EXECUTED`, rc 0, lines 7–8 | Front-door denial is not closure of interpreter variants; P3/O5 attribution remains a hole |
| Node invokes npm CLI; runs installed package | Not measured there | Package installs, `NODE_PACKAGE_EXECUTED`, rc 0, lines 9–10 | Same attribution limit; installed files and actual code execution both recorded |
| Session predating download allowance | Not measured there | Old session target rc 126; fresh target rc 0, lines 18–19 | Landlock cannot relax that existing domain |
| Session predating revocation | Not measured there | Old and fresh target rc 126, lines 22–23 | Hybrid noexec revocation acts on subsequent path opens; no process-quiescence claim |
| Root launches own native file on data mount | Exact root/path pair not measured | Noexec denies 126; root manually adds exec bind and same file runs 0 | Prewritten supplement, [raw evidence](raw-X3/root-noexec-supplement.txt). Direct execution is restricted by mount policy, while manual mount authority remains. No blanket P7 pass or resolution of its scope follows |

The old-session wrapper itself returns 0 after printing `RC=126`; target exit status is taken from that printed field, not the wrapper status. Global mount behavior is attributed to the **hybrid stand**, never Landlock alone. Build allows execution throughout Alice's home; this is less narrow than B's `built` path. Wi-Fi/Bluetooth are absent, O4 root-program attribution remains open, and ABI 2 lacks separate truncate/ftruncate mediation. Full everyday work and exhaustive launch paths are not established. Hence Check 2 remains `?`, even where individual native attempts are blocked.

## Retained failures, repeat, and cleanup

Initial setup rejected ABI 2, then rejected Bash without ELF-loader permission. Both occurred before channel measurements; original sources/logs and repairs are in source dispositions. The initial measured batch is retained intact in raw-X3/initial/: law and build completed, lifecycle rollback failed, and later suites could not initialize. Diagnosis shows 49,174 mountinfo entries, mount limit 100,000, and 13 GiB free disk: this was mount accumulation, not storage exhaustion. The repaired implementation checks `/proc/self/mountinfo`, makes the disposable mount tree private, and repeats the entire suite after a guest reboot. The final suite starts at 26 mounts and ends at 30 after the supplementary control (start, [end](raw-X3/root-noexec-supplement.txt)). No failed evidence or criterion was removed.

Final raw data: [raw-X3/final/](raw-X3/final/). Source hashes: measured guest files, local final protocol/source. The VM is powered off and X3's server directory, disposable disk and key are deleted (cleanup); the queue unit is inactive. B's backing disk hash is unchanged and its files remain with their owner.
