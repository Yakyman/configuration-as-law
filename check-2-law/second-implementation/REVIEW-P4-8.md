VERDICT: AGREED

Reviewer: independent (RP4-8), 2026-11-19. Scope: the shared rules of the checks, PAPER §5/§9, `P/P4-8.md`, its analysis files and a sample of 5 claims checked against the cited raw evidence. No blocking defect. The findings below record what was checked; none changes an outcome.

1. **Fixed conditions (check 1): every outcome follows them.** The frozen oracle is `raw-P4-8/PROTOCOL.md` lines 91–103. The file's SHA256 is `3fe6a8a8…1f4b`, as the result claims. All 27 entries of `FROZEN.sha256` pass `sha256sum -c` from the root of the working directory. The freeze time (10:32:37, `frozen-at.json`) is before the first probe event (10:33:22, `server/results/control-small/events.json`).
   - Contract 0 applies the frozen rule "one acknowledged mismatch". `blocks` retry has `ack:true` and snapshot sha `197408ed…` ≠ declared `a2d60298…` (`analysis/matrix.json`). The replay shows the same.
   - P2 = `?`, P4/§9.3 = `?` and P7/§9.6 = `?` all follow §9.1: this is a prototype failure with no necessity proof. The executor did not infer hypothesis 0 from the added digest contract.
   - Minimal fix: none.
2. **Numbers (check 2): all match the data.** `analysis/summary.json` and `matrix.csv` give 15 attempts, 9 ACKs and 6 rejections. Among the ACKs, 7 launches have rc 0 and 2 have rc 126 (the `blocks` and `replay-blocks` retries). There are 818 checks with 0 failures. Read/wire integrity is 30/30 (`read-wire-final/integrity.json`). Export covers 725 files with 0 failures (`export-integrity.json`).
   - Every per-cell value in the result table matches `matrix.json`: write returns, ENOSPC/EROFS errors, modes 0644 and 0550, sizes 28,672 and 1,057,712, inodes 13/14, published entries and launch rc 0/126/127.
   - 11 cells have an existing snapshot and 4 have none, which matches the Bob endpoint count.
   - Controller hash `88ce1bad…0961ae` and policy hash `0778eb04…d3367f` match `source/`. The source line references 111–125, 164–165 and 170–173 match `source/cald.py`: `if not target.exists():` skips the write, chown and chmod.
   - Minimal fix: none.
3. **Invented rules (check 3): none found.** The source-path denial (rc 126) is kept as the existing hole. This matches the treatment accepted in `REVIEW-P3-6-2.md` item 9: even a literal reading gives `?` under §9.1, not 0.
   - The 0644 residue is excluded as a Unix-permission limb by the frozen protocol line 100, not by an after-the-fact rule.
   - Rejections are classed as "preserved rejection" by protocol line 94.
   - Minimal fix: none.
4. **Sample claim 1 (partial write): confirmed.** `server/results/blocks/controller.strace` shows:
   - line 1318: `openat(... O_WRONLY|O_CREAT|O_TRUNC ...) = 5` on the digest path;
   - line 1320: `write(..., 1057712) = 28672`;
   - line 1321: `write(..., 1029040) = -1 ENOSPC`;
   - line 1323: `{"error": "[Errno 28] No space left on device", "ok": false}`.
5. **Sample claim 2 (retry reuses the residue and publishes): confirmed.** In the same trace:
   - line 1856: `newfstatat` on the existing target returns ino 14, mode 0644, uid/gid 0. There is no target open or write afterwards.
   - The renames at lines 1862 (`pending.json`), 4952 (generation file) and 4959 (`current.json`) follow.
   - line 4980: `sendto` sends the effective document, which is the ACK.
6. **Sample claim 3 (residue identity): confirmed.** `blocks/first-snapshot.bin` and `blocks/retry-snapshot.bin` both hash to `197408ed3a6b77cd8a46b21720657b8a493d23febf301806f88bd8835d976905` and are 28,672 bytes. The fixture `padded` hashes to `a2d60298…` and is 1,057,712 bytes.
7. **Sample claim 4 (seven free blocks): confirmed.** `blocks/arm.json` gives `f_bfree` 8165 → 7 with `f_frsize` 4096, which is 28,672 bytes. That equals the partial write, so reserved blocks played no part (`f_bavail` = `f_bfree`).
8. **Sample claim 5 (promised launch fails): confirmed.** `blocks/retry-alice-confined-snapshot-exec.json` shows user alice, `cal-login -c <digest path>`, rc 126, empty stdout and stderr `Permission denied`.
9. **Nit, wording only.** The P4 row says the launch failure supplies the permission limb "independently of digest mismatch". Both observations come from the same partial-write residue: the mode is still 0644 because chmod was skipped together with the write. The limb is *measured* separately, but its cause is the same.
   - Minimal fix: replace "independently of" with "measured separately from". The outcome stays `?`.
