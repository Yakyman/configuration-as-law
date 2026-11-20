VERDICT: AGREED

# Review 2 of B (checks 2–5, after FB1), 2026-11-19

Scope: the shared rules of the checks; PAPER.html §5 and §9; B/RESULTS.md, B/STAND.md, B/FIX-1.md (newest FIX), B/PROTOCOL.md for the fixed conditions. Raw files opened only for counts and the 5-claim sample.

Agreed: all four outcomes are `?`, and each one follows from the fixed §9.3–9.6 conditions and the §9.1 attribution rule. The numbers match the data, and the failure conditions were not changed (hashes recomputed: PAPER.html `e6978714…`, the shared rules file `085e70fa…`, PROTOCOL.md `147b7be5…`, repro-root.json `e2de2505…` = `raw/protocol.sha256`). None of the findings below changes an outcome.

## Checked and consistent

- **Numbers.**
  - `law-v2/rows.json`: 39 rows; 33 have `met=true` (19 blocked, 14 works); 6 have `met=null` (O5×2, hardware×2, coverage defect, evidence).
  - `check-lifecycle-v2.jsonl`: 102 assertions, all true.
  - `fb1/check-authority.jsonl`: 32 command events. SUMMARY lists one failure, `no-lists-unix-execute-own-file`.
  - `fb1/check-build.jsonl`: 9 command events, 0 failures.
  - `fb1/check-browser-lifecycle.jsonl`: `failure_count` 2.
  - Check 3 inventories, A = B: 1101 packages (1100 installed), 31 accounts, 38 active units, 138 unit-file states, 51 modules, 7 PCI devices, 86 processes (18 userspace + 68 kernel). Machine IDs differ (`e5bbb653…` / `6b306b1d…`). `rules.txt` is byte-identical.
- **Sample (5 claims), all confirmed:**
  - (a) row 18: bash prints `USER_SCRIPT`, rc 0.
  - (b) row 35: root `/bin/sh` writes `/usr/local`, rc 0.
  - (c) Check 5 lines 5–8:
    - line 6: rc 126, `/home/alice/downloaded: Permission denied`.
    - line 8: rc 0, `Hello, world!`.
    - Lines 6–8: the `same_file` predicate (bytes, mode, uid, gid, inode; `src/check-authority.py:104`) is true.
    - Line 7: `policies: {}`.
  - (d) browser: `new_home_files` = `.config/chromium/Crash Reports/settings.dat`, 40 B. The sha256 is the same at creation and at `browser-case-end` under both settings.
  - (e) Check 3: only `kworker` comm labels differ (11 vs 11 records). `userspace_processes_equal: true`.
- **No invented classification rule.** O5 → `?` is required by §9.3. Absent radios → `?`: §9.3 assigns them to a real computer. The kworker granularity is recorded as a hole, and so is the P7-vs-P1/P4 case.

## Findings

1. **Check 4: the attribution understates what fired.** A fixed §9.5 clause fires in the stand under either reading of "present in the current generation".
   - Where: RESULTS.md, Check 4 ("we do **not** assert that §9.5's no-owner clause conclusively fired"); STAND.md §P6, last paragraph.
   - Reading A: base Chromium counts as present (`browser-owner-scope`: `chromium 156.0.8078.79-1~deb12u1` installed). Then under `delete` the assigned Chromium profile is deleted after GC while its program is still present. That is clause 1.
   - Reading B: base Chromium does not count. Then `settings.dat` stays active in home and is not archived. That is clause 2.
   - Evidence: `raw/fb1/check-browser-lifecycle.jsonl`, events `browser-owner-scope`, `browser-assertion` (passed=false, `surviving`), `browser-case-end`.
   - The outcome stays `?`: the cause is the stand's base/catalog split and untracked home state, which is not shown to follow from P6.
   - Minimal fix: replace the quoted sentence with "Under either reading of base presence a fixed §9.5 clause fires in the stand (clause 1 under `delete` if base Chromium counts; clause 2 if not). Attribution: stand defect (base/catalog split, untracked home state), not shown to follow from P6 → `?`."

2. **Check 5: the "unresolved for the author" framing leaves out a stand-side cause.**
   - Where: RESULTS.md Check 5, "Hole" paragraph; STAND.md §P7.
   - On the reading where P7's Unix permissions are exercised *through* the personal declaration, the case is decided by the user declaring their own file. The stand cannot represent that: personal declarations accept only catalog names (STAND §P7, "arbitrary user software … not implemented").
   - The only route that was tested is a root `allow_channels` line (line 7). That is root's line, not the user's.
   - So a `0` cannot follow from this stand alone. Only the definitional question (does P7 grant runtime execution outside any declaration?) is genuinely the author's.
   - `?` is correct.
   - Minimal fix: add one sentence. It should say that the personal-declaration route for a user's own executable cannot be represented in the stand, so on that reading the observation is a stand defect. Only on the runtime-Unix reading of P7 is it a §9.1 requirement contradiction.

3. **Check 2: pip and npm are blocked at their undeclared interpreter, not at the channel.**
   - Where: RESULTS.md Check 2, rows 03–06, and the summary "Tested prohibited channels were blocked".
   - Evidence: stderr `/usr/bin/pip3: /usr/bin/python3: bad interpreter` and `/usr/bin/npm: /usr/bin/env: bad interpreter`. In `00-reset` the effective `programs` are `{}`, so Python and Node are not declared.
   - The everyday case, a user with declared Python/Node running `pip install --user` or `npm install --prefix` and then the installed entry point, was not exercised.
   - `?` is unaffected.
   - Minimal fix: in rows 03–06, change "Blocked" to "Blocked at undeclared interpreter; pip/npm with declared Python/Node untested". Alternatively, rerun those four rows with Python/Node in the declaration.

4. **Check 3 (nit): "cannot support `1` without independent clean bootstraps" reads like an extra requirement.** §9.4 only says "two clean machines".
   - Where: RESULTS.md Check 3 (bold sentence); STAND.md §Machine.
   - The underlying point is sound. `src/repro-root.json` declares 4 programs, and most compared components come from the shared image, not from applying the declaration. That is "insufficient evidence" under PROTOCOL §Classification, not a new rule.
   - Minimal fix: reword to "this pair is insufficient evidence for `1`: most compared components are inherited from the common image rather than produced by applying the declaration".
