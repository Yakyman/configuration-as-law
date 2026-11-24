INVENTORY: 0 of 5 machines

Recorded UTC: 2026-11-23T11:12:11.526695+00:00

Input gate: `3e0207b104f9718793c5b2678810936c7c3c14d2 2026-11-23T11:10:54Z 1017 files`.

Pre-observation input verification stopped: check-inputs-v4/PUBLISH.list does not match its entry in C1/input-files.sha256.tsv. No machine was created and no action or collector was run.

Verification evidence: `control/input-verification.tsv` and `control/input-verification.json`. Of 1020 manifest entries, 1019 match. Collector files, action scripts/helpers and installation recipes match. The publication list itself fails:

- File: `check-inputs-v4/PUBLISH.list`
- Expected SHA-256: `63801d3b7bd13b1c5335d9dede8b6135b7e8506953aa93425aa06cabcda78660`
- Actual SHA-256: `4569378038e1142d9519dd9cd49e6e40575cce030fe1b3f835768943c1cd89b6`

The manifest itself is listed for publication but has no self-checksum. This is reported separately and is not counted as a checksum failure. The commit identifier is taken from the supplied gate; the current workspace is not a Git worktree, so commit-tree identity was not independently verified.

| Machine | Committed release | Objects by kind | Second level obtained | Known package reasons | Known packaged-file integrity | Ordinary actions | Missing-inventory evidence |
|---|---|---|---|---|---|---|---|
| alma | 10.3 | 0 total; no observed kinds | No; 0 rows | N/A (no inventory) | N/A (no inventory) | Not attempted (input verification stop) | `raw/alma/NOT-RUN.md` |
| void | 20250202 (rolling-release installation image) | 0 total; no observed kinds | No; 0 rows | N/A (no inventory) | N/A (no inventory) | Not attempted (input verification stop) | `raw/void/NOT-RUN.md` |
| gentoo | stage3-amd64-openrc-20261122T164601Z | 0 total; no observed kinds | No; 0 rows | N/A (no inventory) | N/A (no inventory) | Not attempted (input verification stop) | `raw/gentoo/NOT-RUN.md` |
| microos | Snapshot20261121 plain x86_64 KVM/XEN image | 0 total; no observed kinds | No; 0 rows | N/A (no inventory) | N/A (no inventory) | Not prescribed | `raw/microos/NOT-RUN.md` |
| talos | 1.14.6 | 0 total; no observed kinds | No; 0 rows | N/A (no inventory) | N/A (no inventory) | Not prescribed | `raw/talos/NOT-RUN.md` |

Deviations: no execution deviations; no commands were substituted, inputs repaired, cases retried, or objects selected. The input publication-list checksum mismatch above prevented all five prescribed runs. All part files contain only the required header. No hypothesis outcome is assigned by this operator record.
