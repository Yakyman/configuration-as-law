# X6 — Check 4 under random generations

2026-11-19. **Bounded alpha/beta lifecycle experiment: 1. General P6 / Check 4: ?.** Four fixed seeds completed **512 random generation transitions**, with no observed invariant failures. This is additional evidence for the known-owner B fixture; no open problem is decided and B's broader Check 4 result is not upgraded. Independent audit: X6-INDEPENDENT-REVIEW.md — **AGREE**, with all 805 checkpoints independently reconstructed and checked.

## Fixed measurement and instrument

Protocol was written and hashed before experiment execution. Its SHA-256 remains `a2a62bcd46d274c11c970eff241b0ce0743f7578366a3857015b508d16375881`; the fixed §9.5 failure condition and §9.1 attribution were unchanged. Evidence: pre-run hashes, freeze time, post-run verification.

The unmodified B controller/policy ran in a fresh overlay of stopped `B/clean-a.qcow2` on `<HOST>`, 2 GiB / 2 vCPU. Runtime controller and policy hashes match `B/src`; alpha, beta and worker binaries have the same recorded hash. The independent oracle maintained its own declaration/generation ledger and expected cache contents; it did not import controller code. Evidence: image chain and backing hash, [runtime sources](raw-X6/instrument/), source hashes, runtime preflight, completion/resource log.

## Coverage and results

Every generation apply and every generation-GC operation was checked immediately. Counts below exclude declarative resets; the 32 tail operations and four initial fixture applies are additional to the random workload. Full operation streams, replies, before/after inventories, saved declarations, raw cache bytes, hashes and logical-to-actual generation handles are retained under [raw-X6/results/](raw-X6/results/).

| Seed | Add | Remove | Upgrade | Rollback | Toggle | Random generations | Random GC | Checked operations* | Fixture outcome |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [6](raw-X6/results/seed-6/summary.json) | 20 | 20 | 35 | 16 | 37 | 128 | 68 | 205 | 1 |
| [42](raw-X6/results/seed-42/summary.json) | 25 | 24 | 27 | 12 | 40 | 128 | 69 | 206 | 1 |
| [1119](raw-X6/results/seed-1119/summary.json) | 26 | 32 | 22 | 15 | 33 | 128 | 57 | 194 | 1 |
| [20261119](raw-X6/results/seed-20261119/summary.json) | 22 | 20 | 21 | 33 | 32 | 128 | 59 | 196 | 1 |
| **Total** | **93** | **96** | **105** | **76** | **142** | **512** | **253** | **801** | **1** |

\* Random generation steps + random GC + eight tail operations + one initial apply per seed. There are 805 successful checkpoints including four reset endpoints. The harness recorded 9,278 checks tagged P6 and 8,572 instrument checks, zero failures. Tags are diagnostic counts, not independent experiments or a broader definition of P6. Coverage totals and exact event-line index: [coverage.json](raw-X6/coverage.json); reproducible count command: `python X/X6-summarize.py`, [saved output](raw-X6/coverage-command.txt).

| Measured invariant | Observed evidence |
|---|---|
| Current owner → active; absent current owner → archive while any saved owner survives | Placement and cache continuity checked at every checkpoint. Seed 6 event line 115 shows no current programs and archived state with surviving owner references. |
| Shared state survives removal of one owner and stays accessible | 309 single-owner checkpoints; 993 successful shared-consumer reads overall. Seed 6 line 72 has alpha current, beta archived and shared active; lines 1487 and 1512 cover both removal orders. |
| Rollback restores programs, versions, policy and extant derivatives | 76 rollbacks; 19 program-reactivation occurrences, 18 downward version changes and 32 rollbacks changing archive policy. Each is checked against the selected saved declaration and pre-transition cache contents. Seed 6 line 294 is one rollback checkpoint. |
| Keep after deleting every owning saved generation | All four keep tails retain alpha, beta and shared caches after GC leaves only the empty current generation. Seed 6 lines 1494 → 1498 show protected archives before GC and retained archives afterward. |
| Delete preserves referenced archives, then removes unreferenced ones | All four delete tails preserve all three caches before GC and remove them afterward. Seed 6 lines 1519 → 1523 show the reference transition; 80 authorized derivative-incarnation deletions occur across the full corpus. |
| No silent loss/recreation | Every extant alpha/beta cache preserves its previous prefix and receives only the fixture's expected append; shared bytes stay identical. After authorized deletion a later creation starts a new incarnation. Full pre/post bytes are retained in every checkpoint. |

All seed-6 line references above are literal JSONL line numbers in seed-6/events.jsonl; [coverage.json](raw-X6/coverage.json) provides equivalent tail evidence for every seed. These repeated observations do not establish a statistical failure-rate bound.

## Failures, attribution and holes

**Failing experimental sequences: 0.** Therefore no sequence required minimization or failure reruns. The harness includes dependency-valid delta reduction, single-operation deletion checks and two final reruns for any failure, but that path was not exercised by this corpus. No stand failure was attributed to P6 and no hypothesis `0` is asserted. Evidence: [aggregate summaries](raw-X6/results/summary.json), each seed's `events.jsonl`, successful process exit.

The measured objects are append-only alpha/beta caches and B's controller-created shared fixture consumed by both programs. Owner relations are supplied; alpha/beta executables remain installed fixture infrastructure. Upgrades change catalog version labels and the workers' emitted records; they do not test historical distribution-package payloads. The experiment therefore establishes assigned-state lifecycle behavior under the stated catalog interpretation, not full-system owner absence. These boundaries follow the frozen protocol and B stand input.

General derivative discovery/ownership and data boundaries (O1/O2), missing archive instructions (O6), incompatible derivative formats or historical-byte rollback (O7), transfer (O8), installed-versus-running/base presence (O9), arbitrary out-of-tree derivatives, concurrent writers, crash consistency and per-user isolation remain uncovered or undecided. The prior Chromium coverage defect remains; see B Check 4 input. A case not decided by the paper remains a hole, not a new rule.

Two preflight issues were recovered before experiments: default SSH configuration failed its ownership check, so the existing user SSH config was selected explicitly; an initial source probe guessed `cald.py`, then the service unit identified `/usr/local/sbin/cald`. No host configuration was changed. Both original outputs are retained in server-preflight.txt and guest-preflight.txt; the source-location correction is in daemon-provenance.txt.

## Reproduction and cleanup

[Harness](X6-run.py) supports fixed-seed generation and exact recorded-stream replay. In another disposable B copy as root:

```sh
python3 X6-run.py --output /root/X6-results-new
python3 X6-run.py --output /root/X6-replay-new --replay /path/to/seed-6/operations.json
```

Each output directory must be new. The second command executes the recorded logical operation stream, translating generation labels to that run's fresh IDs. This report records one execution of each seed, not an unperformed second run. Source hashes were frozen before execution and verified afterward: harness-before.sha256, harness-after-check.txt, guest-final.txt.

The VM stopped with exit status 0; its disposable disk and server working directory were removed, and no X6 QEMU process remained. The B backing overlay's SHA-256 was unchanged. Evidence: cleanup-before-delete.txt, cleanup.txt. Only the records remain locally.
