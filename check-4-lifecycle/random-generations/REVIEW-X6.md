VERDICT: AGREED

Review of X6 (Check 4 under random generations), 2026-11-19. Reviewer: independent of the executor and of the earlier auditor. Scope: (1) outcomes against the fixed PAPER §9.5/§9.1 conditions; (2) numbers against the data files; (3) rules invented to classify cases; (4) at most 5 sampled claims against the cited evidence. No raw dump was read beyond the sample.

What I checked and found correct:
- The outcomes "bounded fixture experiment 1, general P6 / Check 4 ?" follow §9.5 (quoted unchanged in X6-PROTOCOL.md) and §9.1. No `0` is asserted. Holes O1/O2/O6–O9 remain open.
- The protocol SHA-256 recomputes to `a2a62bcd…6375881`, which matches protocol-before/at-run/after-check. The freeze (08:44:06 UTC) comes before the first seed starts (08:48:44, exercise-completion.txt).
- The harness edit after the freeze (`1eb239…` → `03d4f1…`) happened before the run and is disclosed in raw-X6/PREPARATION.md.
- Every number in both tables of X6-LIFECYCLE.md matches the seed summaries and results/summary.json:
  - per-seed kinds sum to 128;
  - checked operations = 128 + GC + 8 + 1;
  - totals: 93/96/105/76/142/512/253/801;
  - checks: P6 9,278 and instrument 8,572;
  - counts: single-owner 309, shared reads 993, rollback 19/18/32, deletions 80.
- grep over the four events.jsonl files gives:
  - 206+207+195+197 = 805 `checkpoint-pass` events;
  - 0 `failure` events;
  - 0 `command-error` events;
  - 0 commands with a nonzero return code.
- operations.json is byte-identical to plan-<seed>.json for all four seeds.
- I replayed the operation streams through the harness's own Model (no controller code). This independently gives 63 last-reference-GC deletions + 17 policy-switch deletions = 80 authorized deletions, which matches the summary.
- Sampled claims (seed-6 events.jsonl), all as stated:
  - L72: alpha current, beta archived, shared active.
  - L115: no current programs, all three archived, alpha still referenced.
  - L294: rollback r023→r021 checkpoint.
  - L1494→1498: keep, 4→1 generations, all three archives retained.
  - L1519→1523: delete, all archived while referenced, then none.
  - L1487/L1512 also show both removal orders.

Findings (none changes the outcome):

1. **The "currently applied setting" rule is new relative to B and is not counted.**
   - Where: X6-PROTOCOL.md invariant 5 ("Explicit switching is measured against the currently applied setting. This is the same interpretation already used by B Check 4"); X6-LIFECYCLE.md does not mention it.
   - Evidence: 17 of the 80 authorized deletions come from a random keep→delete toggle on an archive that was already unreferenced under keep. Per seed: 6:3, 42:5, 1119:8, 20261119:1, from my replay of operations.json through X6-run.py's Model. B Check 4 never switched the setting: B/RESULTS.md:107-115 runs keep and delete separately. Only B's controller semantics (B/STAND.md:33) encode it.
   - Assessment: I do not treat it as an invented rule. It was frozen before the results. PAPER §5.2 P6 says the keep/delete choice "is a setting recorded in the declaration", and the declaration in force is the only source of truth, so deleting after a switch to delete matches "the setting" in §9.5. Under the opposite reading (the setting at archival time governs), these 17 cases would be holes, and the protocol would then require `?`.
   - Minimal fix: in X6-LIFECYCLE.md, add one line with the 17-case count and the textual basis (P6 "setting recorded in the declaration"). Change "same interpretation already used by B Check 4" to "B controller semantics (B/STAND.md:33), not exercised by B Check 4".

2. **The oracle cannot detect deletion and recreation of the shared cache while it is referenced.**
   - Where: X6-run.py `verify` (shared-continuity checks bytes only); X6-LIFECYCLE.md row "No silent loss/recreation … shared bytes stay identical".
   - Evidence: the controller always writes the constant bytes `shared derivative\n` (raw-X6/instrument/cald.py:147). Byte identity therefore cannot distinguish preservation from delete+recreate, which is a §9.5 clause ("a shared derivative is … deleted … while a program that needs it is present"). By protocol invariant 6, inode identity is diagnostic only. In my sample the inode is continuous (33316 at L72/L115/L294; 33159 at L1487–L1519), so I saw no sign of a real failure.
   - Minimal fix: in X6-summarize.py, check post hoc that the shared-cache inode stays the same across consecutive checkpoints of one incarnation; the snapshots already hold the inodes. Otherwise, reword the row to say "shared bytes identical; recreation not detectable by bytes".

3. **(nit) The "P6" tag covers checks stricter than §9.5.**
   - Where: X6-run.py `check(...)` with the default category 'P6', for own-cache `readable:*`, re-add reactivation with prefix, and the no-duplicate-copy check.
   - Evidence: §9.5 names inaccessibility only for shared derivatives. This cannot inflate a `1`, because stricter checks only add possible failures. The headline "9,278 checks tagged P6" still reads as P6 coverage.
   - Minimal fix: keep the existing disclaimer and append "includes stricter-than-§9.5 diagnostics" next to the count.

4. **(nit) The independence of the audit cannot be confirmed from the files.**
   - Where: X6-LIFECYCLE.md line 3; X6-PROTOCOL.md line 3.
   - Evidence: the files name the executor and the auditor only by internal labels, so their independence is asserted rather than documented.
   - Minimal fix: state the identities of the executor and the auditor.
