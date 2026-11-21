# Manifest

This file maps every evidence key cited in the second paper to the files of this repository, and lists the
SHA-256 of every file. The column *Record* gives the identifier of each record in the working directory of
the test run (`night-1119/…`); the column *File* gives the file here, which is the file the paper links to.
The last column states the claim of the paper that the record supports; section numbers are those of the
second paper.

## 1. Evidence keys, records and claims

| Key | Record (`night-1119/…`) | File in this repository | Claim of the paper it supports |
|---|---|---|---|
| ev-v1-text | `PAPER.html` | [`first-paper/PAPER.html`](first-paper/PAPER.html) | §2, §3: the text of version 1 and the check conditions, fixed before the checks began. The file is byte-identical to the author's file `draft-v3-en.html`; the published PDF (`configuration-as-law-v1.pdf`, SHA-256 `fa2f7ce8d59f04d50f320e7c69d9d1c216e822af7ea0715ed60acbace17de160`) is byte-identical to the author's file `draft-v3-en.pdf` |
| ev-v-census | `V/RESULT.md` | [`check-1-census/debian-fedora-coreos-nixos/RESULT.md`](check-1-census/debian-fedora-coreos-nixos/RESULT.md) | §4.1: 398 rows, 63.32%, κ = 0.45480; outcome 0 for Debian, Fedora CoreOS and NixOS (kernel threads; the NixOS package profile); `.bashrc` and `.vimrc` unresolved; incompleteness of the inventory. §6.3: executable settings |
| ev-v-census | `V/REVIEW-2.md` | [`check-1-census/debian-fedora-coreos-nixos/REVIEW-2.md`](check-1-census/debian-fedora-coreos-nixos/REVIEW-2.md) | §3: numbers recomputed independently, a sample of the evidence checked; §4.1: outcomes 0/0/0 confirmed |
| ev-v-census | `V/METHOD.md` | [`check-1-census/debian-fedora-coreos-nixos/METHOD.md`](check-1-census/debian-fedora-coreos-nixos/METHOD.md) | §4.1: how the inventory was compiled and what it did not include |
| ev-w-census | `W/RESULT.md` | [`check-1-census/guix/RESULT.md`](check-1-census/guix/RESULT.md) | §4.1: 178 rows, 80.34%, κ = 0.63346; outcome 0 under the “two classes” branch (personal package selection); declaration files are present on the machine and their hashes did not change. §7.5: `guix install` by an ordinary user without changing the declaration files. §9, O11: access keys in root’s home directory as a borderline case |
| ev-w-census | `W/REVIEW.md` | [`check-1-census/guix/REVIEW.md`](check-1-census/guix/REVIEW.md) | §3, §4.1: outcome 0 and the numbers confirmed by an independent review |
| ev-w-census | `W/METHOD.md` | [`check-1-census/guix/METHOD.md`](check-1-census/guix/METHOD.md) | §4.1: the inventory method for Guix |
| ev-a-census | (records of the author's personal machines) | not published | §4.1: 695 rows (477 + 218), 215 exact matches (30.94%; κ = 0.27011), 391 by five categories (56.26%; κ = 0.30135); decisive case: an executable editor configuration. §6.3. The paper reports these machines only as aggregate numbers. |
| ev-def-analysis | `C/ATTACK.md` | [`definitions-analysis/documented-objects/ATTACK.md`](definitions-analysis/documented-objects/ATTACK.md) | §4.1: with an explicitly given recorded editor, the overlap of data and derivative is reproduced. §5.2: the other hard cases do not prove inevitable failure. §9, O10: an extension with an external program, a virtual-machine disk, containers; O11: UEFI variables |
| ev-def-analysis | `C/SOURCES.md` | [`definitions-analysis/documented-objects/SOURCES.md`](definitions-analysis/documented-objects/SOURCES.md) | same: the list of primary sources of the analysis |
| ev-def-analysis | `C/REVIEW-2.md` | [`definitions-analysis/documented-objects/REVIEW-2.md`](definitions-analysis/documented-objects/REVIEW-2.md) | same: review of the analysis |
| ev-samples | `E/E6C-RESULT.md` | [`check-1-census/samples/ubuntu-alpine/E6C-RESULT.md`](check-1-census/samples/ubuntu-alpine/E6C-RESULT.md) | §4.1: Ubuntu and Alpine, 262 rows, 29.77% by five categories, 6.11% by literal labels; outcome ? |
| ev-samples | `E/REVIEW-E6C.md` | [`check-1-census/samples/ubuntu-alpine/REVIEW-E6C.md`](check-1-census/samples/ubuntu-alpine/REVIEW-E6C.md) | §4.1: review of this sample |
| ev-samples | `X/X1C-RESULT.md` | [`check-1-census/samples/arch-silverblue-freebsd/X1C-RESULT.md`](check-1-census/samples/arch-silverblue-freebsd/X1C-RESULT.md) | §4.1: Arch Linux, Fedora Silverblue, FreeBSD, 510 rows, 12.94%; initial outcome 0 |
| ev-samples | `X/REVIEW-X1C.md` | [`check-1-census/samples/arch-silverblue-freebsd/REVIEW-X1C.md`](check-1-census/samples/arch-silverblue-freebsd/REVIEW-X1C.md) | §4.1: finding 5 — a refusal to classify was treated as a class |
| ev-samples | `X/X2C-RESULT.md` | [`check-1-census/samples/debian-desktop/X2C-RESULT.md`](check-1-census/samples/debian-desktop/X2C-RESULT.md) | §4.1: desktop Debian, 235 rows, 7.23%; outcome ? |
| ev-samples | `X/REVIEW-X2C.md` | [`check-1-census/samples/debian-desktop/REVIEW-X2C.md`](check-1-census/samples/debian-desktop/REVIEW-X2C.md) | §4.1: review of this sample |
| ev-report-fix | `REPORT-CHECK.md` | [`check-1-census/report-check/REPORT-CHECK.md`](check-1-census/report-check/REPORT-CHECK.md) | §4.1: the outcome of the Arch/Silverblue/FreeBSD sample under the literal condition is ? |
| ev-report-fix | `REPORT-FIX.md` | [`check-1-census/report-check/REPORT-FIX.md`](check-1-census/report-check/REPORT-FIX.md) | §4.1: correction of that outcome to ?; the overall outcome of check 1 remains 0 |
| ev-provenance | `X/X9-STATE.md` | [`check-1-census/provenance/X9-STATE.md`](check-1-census/provenance/X9-STATE.md) | §4.1: of 2058 created files, a single creating process was established for 2053 |
| ev-provenance | `X/REVIEW-X9.md` | [`check-1-census/provenance/REVIEW-X9.md`](check-1-census/provenance/REVIEW-X9.md) | §4.1: review of this experiment |
| ev-law-proto | `B/RESULTS.md` | [`check-2-law/stand/RESULTS.md`](check-2-law/stand/RESULTS.md) | §4.2: channels on the testbed; denial, permission and renewed denial of a launch. §4.4: the original derivative-lifecycle experiment (102 conditions), the 40-byte file |
| ev-law-proto | `B/REVIEW-2.md` | [`check-2-law/stand/REVIEW-2.md`](check-2-law/stand/REVIEW-2.md) | §4.2: review of the testbed outcomes |
| ev-law-proto | `B/Q-RESULTS.md` | [`check-2-law/stand/Q-RESULTS.md`](check-2-law/stand/Q-RESULTS.md) | §4.2: the everyday-work scenario, a package version change through the declaration, Wi-Fi and Bluetooth 2 of 2. §4.4: 94 conditions, withdrawal of the positive assessment |
| ev-law-proto | `B/Q-REVIEW-2.md` | [`check-2-law/stand/Q-REVIEW-2.md`](check-2-law/stand/Q-REVIEW-2.md) | §4.2: review of the additional runs |
| ev-channels | `D/RESULTS.md` | [`check-2-law/channels/RESULTS.md`](check-2-law/channels/RESULTS.md) | §4.2: 64 channels, 40 denials, 21 effects, 3 cases in which the required tools were absent; three installations through interpreters; execution continued after revocation. §6.3: 15 cases of open problem O5. §9, O12: an ordinary user wrote a shell startup file, which was then executed |
| ev-channels | `D/REVIEW.md` | [`check-2-law/channels/REVIEW.md`](check-2-law/channels/REVIEW.md) | §4.2: one denial concerns a recorded program; denials are attempts, not barriers |
| ev-channels | `D/raw/d2-classified-results.json` | [`check-2-law/channels/raw/d2-classified-results.json`](check-2-law/channels/raw/d2-classified-results.json) | §4.2: per-row results of the channels |
| ev-law-second | `X/X3-RESULTS.md` | [`check-2-law/second-implementation/X3-RESULTS.md`](check-2-law/second-implementation/X3-RESULTS.md) | §4.2: the second implementation of the testbed |
| ev-law-second | `X/REVIEW-X3.md` | [`check-2-law/second-implementation/REVIEW-X3.md`](check-2-law/second-implementation/REVIEW-X3.md) | §4.2: review |
| ev-law-second | `P/P3-1.md` | [`check-2-law/second-implementation/P3-1.md`](check-2-law/second-implementation/P3-1.md) | §4.2: 104 launches; a permission given before the file was created took effect in one implementation and not in the other |
| ev-law-second | `P/REVIEW-P3-1-2.md` | [`check-2-law/second-implementation/REVIEW-P3-1-2.md`](check-2-law/second-implementation/REVIEW-P3-1-2.md) | §4.2: review |
| ev-law-second | `P/P4-8.md` | [`check-2-law/second-implementation/P4-8.md`](check-2-law/second-implementation/P4-8.md) | §4.2: an incomplete copy of an executable was accepted, and the permitted launch failed twice |
| ev-law-second | `P/REVIEW-P4-8.md` | [`check-2-law/second-implementation/REVIEW-P4-8.md`](check-2-law/second-implementation/REVIEW-P4-8.md) | §4.2: review |
| ev-root-signals | `E/E2.md` | [`check-2-law/root-signals/E2.md`](check-2-law/root-signals/E2.md) | §4.2, §6.3: an automated command possessed all five indicators of a manual action |
| ev-root-signals | `E/REVIEW-E2.md` | [`check-2-law/root-signals/REVIEW-E2.md`](check-2-law/root-signals/REVIEW-E2.md) | same: review |
| ev-repro-proto | `B/Q-REPRO.md` | [`check-3-reproducibility/stand-pair/Q-REPRO.md`](check-3-reproducibility/stand-pair/Q-REPRO.md) | §4.3: 324/777/1101, 31, 43, 138, 52, 8, 20; 68 and 69 kernel tasks. §6.3: 68 and 69 would not violate any line. §9, O15: the package sources matched only in this run |
| ev-repro-proto | `B/raw/q/repro/summary.json` | [`check-3-reproducibility/stand-pair/raw/q/repro/summary.json`](check-3-reproducibility/stand-pair/raw/q/repro/summary.json) | §4.3: summary numbers of the comparison |
| ev-repro-proto | `B/raw/q/repro/comparison.txt` | [`check-3-reproducibility/stand-pair/raw/q/repro/comparison.txt`](check-3-reproducibility/stand-pair/raw/q/repro/comparison.txt) | §4.3: complete comparison of the inventories |
| ev-repro-pairs | `X/X5-REPRO.md` | [`check-3-reproducibility/clean-install-pairs/X5-REPRO.md`](check-3-reproducibility/clean-install-pairs/X5-REPRO.md) | §4.3: 580 and 353 store objects, 168 Debian packages; outcomes ?. §9, O15: pinned inputs |
| ev-repro-pairs | `X/REVIEW-X5.md` | [`check-3-reproducibility/clean-install-pairs/REVIEW-X5.md`](check-3-reproducibility/clean-install-pairs/REVIEW-X5.md) | §4.3: review |
| ev-repro-hw | `P/P6-3.md` | [`check-3-reproducibility/hardware-profiles/P6-3.md`](check-3-reproducibility/hardware-profiles/P6-3.md) | §4.3: 140 of 160 inventories, 14 of 16 final observations |
| ev-repro-hw | `P/REVIEW-P6-3-2.md` | [`check-3-reproducibility/hardware-profiles/REVIEW-P6-3-2.md`](check-3-reproducibility/hardware-profiles/REVIEW-P6-3-2.md) | §4.3: review |
| ev-repro-hw | `E/E4.md` | [`check-3-reproducibility/state-transfer/E4.md`](check-3-reproducibility/state-transfer/E4.md) | §4.3: transfer of application state with corrections of hardware addresses, database paths and encrypted credentials |
| ev-repro-hw | `E/REVIEW-E4.md` | [`check-3-reproducibility/state-transfer/REVIEW-E4.md`](check-3-reproducibility/state-transfer/REVIEW-E4.md) | §4.3: review |
| ev-lifecycle | `B/RESULTS.md` | [`check-2-law/stand/RESULTS.md`](check-2-law/stand/RESULTS.md) | §4.4: 102 conditions |
| ev-lifecycle | `B/Q-RESULTS.md` | [`check-2-law/stand/Q-RESULTS.md`](check-2-law/stand/Q-RESULTS.md) | §4.4: 94 conditions with the placement set by the test |
| ev-lifecycle | `B/Q-FIX-1.md` | [`check-4-lifecycle/stand/Q-FIX-1.md`](check-4-lifecycle/stand/Q-FIX-1.md) | §4.4: withdrawal of the positive assessment of the derivative lifecycle |
| ev-lifecycle | `X/X6-LIFECYCLE.md` | [`check-4-lifecycle/random-generations/X6-LIFECYCLE.md`](check-4-lifecycle/random-generations/X6-LIFECYCLE.md) | §4.4: 512 transitions, 253 deletions of generations, all 805 checkpoints passed |
| ev-lifecycle | `X/REVIEW-X6.md` | [`check-4-lifecycle/random-generations/REVIEW-X6.md`](check-4-lifecycle/random-generations/REVIEW-X6.md) | §4.4: review |
| ev-lifecycle | `X/raw-X6/coverage.json` | [`check-4-lifecycle/random-generations/raw-X6/coverage.json`](check-4-lifecycle/random-generations/raw-X6/coverage.json) | §4.4: coverage of the checkpoints |
| ev-lifecycle-stands | `P/P7-1.md` | [`check-4-lifecycle/stands/P7-1.md`](check-4-lifecycle/stands/P7-1.md) | §4.4: 48 sequences; state outside the archive survived the removal of the programs |
| ev-lifecycle-stands | `P/REVIEW-P7-1.md` | [`check-4-lifecycle/stands/REVIEW-P7-1.md`](check-4-lifecycle/stands/REVIEW-P7-1.md) | §4.4: review |
| ev-lifecycle-stands | `P/P7-3.md` | [`check-4-lifecycle/stands/P7-3.md`](check-4-lifecycle/stands/P7-3.md) | §4.4: 40 of 60 sequences lost access after restoration |
| ev-lifecycle-stands | `P/REVIEW-P7-3.md` | [`check-4-lifecycle/stands/REVIEW-P7-3.md`](check-4-lifecycle/stands/REVIEW-P7-3.md) | §4.4: review |
| ev-lifecycle-stands | `P/P4-3.md` | [`check-4-lifecycle/stands/P4-3.md`](check-4-lifecycle/stands/P4-3.md) | §4.4: on a storage fault, the reference from the generation was deleted before the deletion of the archive was refused |
| ev-lifecycle-stands | `P/REVIEW-P4-3.md` | [`check-4-lifecycle/stands/REVIEW-P4-3.md`](check-4-lifecycle/stands/REVIEW-P4-3.md) | §4.4: review |
| ev-rollback | `E/E3.md` | [`check-4-lifecycle/rollback/E3.md`](check-4-lifecycle/rollback/E3.md) | §4.4: older versions of the browser and of the synchronisation program did not start with the newer state |
| ev-rollback | `E/REVIEW-E3.md` | [`check-4-lifecycle/rollback/REVIEW-E3.md`](check-4-lifecycle/rollback/REVIEW-E3.md) | §4.4: review |
| ev-authority | `B/Q-AUTHORITY.md` | [`check-5-authority/stand/Q-AUTHORITY.md`](check-5-authority/stand/Q-AUTHORITY.md) | §4.5: 54 scenarios, 53 expectations met, one not |
| ev-authority | `B/Q-REVIEW-2.md` | [`check-2-law/stand/Q-REVIEW-2.md`](check-2-law/stand/Q-REVIEW-2.md) | §4.5: review |
| ev-authority | `B/raw/q/authority/final-owner-authority.jsonl` | [`check-5-authority/stand/raw/q/authority/final-owner-authority.jsonl`](check-5-authority/stand/raw/q/authority/final-owner-authority.jsonl) | §4.5: per-row events of the final run |
| ev-authority-stands | `P/P2-4.md` | [`check-5-authority/stands/P2-4.md`](check-5-authority/stands/P2-4.md) | §4.5: four cases in which access allowed by Unix permissions was refused |
| ev-authority-stands | `P/REVIEW-P2-4.md` | [`check-5-authority/stands/REVIEW-P2-4.md`](check-5-authority/stands/REVIEW-P2-4.md) | §4.5: review |
| ev-authority-stands | `P/P3-2.md` | [`check-5-authority/stands/P3-2.md`](check-5-authority/stands/P3-2.md) | §4.5: ten contradictions of the declarations, four lists not taking effect |
| ev-authority-stands | `P/REVIEW-P3-2-2.md` | [`check-5-authority/stands/REVIEW-P3-2-2.md`](check-5-authority/stands/REVIEW-P3-2-2.md) | §4.5: review |
| ev-authority-stands | `P/P8-1.md` | [`check-5-authority/stands/P8-1.md`](check-5-authority/stands/P8-1.md) | §4.5: the no-lists condition was violated, with 216 final observations per implementation |
| ev-authority-stands | `P/REVIEW-P8-1.md` | [`check-5-authority/stands/REVIEW-P8-1.md`](check-5-authority/stands/REVIEW-P8-1.md) | §4.5: review |
| ev-formal-lit | `X/X4-FORMAL.md` | [`definitions-analysis/formal-and-literature/X4-FORMAL.md`](definitions-analysis/formal-and-literature/X4-FORMAL.md) | §5.2: contradictions only under certain interpretations |
| ev-formal-lit | `X/REVIEW-X4-2.md` | [`definitions-analysis/formal-and-literature/REVIEW-X4-2.md`](definitions-analysis/formal-and-literature/REVIEW-X4-2.md) | §5.2: review |
| ev-formal-lit | `L/RESOLUTIONS.md` | [`definitions-analysis/formal-and-literature/RESOLUTIONS.md`](definitions-analysis/formal-and-literature/RESOLUTIONS.md) | §5.2: for five groups of cases the documented rules do not remove the ambiguity; outcome ? |
| ev-formal-lit | `L/REVIEW.md` | [`definitions-analysis/formal-and-literature/REVIEW.md`](definitions-analysis/formal-and-literature/REVIEW.md) | §5.2: review |
| ev-apply-crash | `P/P4-2.md` | [`open-problems/apply-crash/P4-2.md`](open-problems/apply-crash/P4-2.md) | §9, O14: after a successful apply response, an immediate stop lost the state in 6 of 6 experiments, and a stop after flushing to disk preserved it in 6 of 6 |
| ev-apply-crash | `P/REVIEW-P4-2.md` | [`open-problems/apply-crash/REVIEW-P4-2.md`](open-problems/apply-crash/REVIEW-P4-2.md) | §9, O14: review; which declaration is the primary one is an open question |

## 2. Supporting raw files and scripts by key

Raw files sit next to the records that cite them, under the same relative paths as in the records.

| Key | Folder(s) | Files |
|---|---|---|
| ev-v1-text | `first-paper/` | 1 |
| ev-v-census | `check-1-census/debian-fedora-coreos-nixos/` | 146 |
| ev-w-census | `check-1-census/guix/` | 123 |
| ev-def-analysis | `definitions-analysis/documented-objects/` | 3 |
| ev-samples | `check-1-census/samples/ubuntu-alpine/`<br>`check-1-census/samples/arch-silverblue-freebsd/`<br>`check-1-census/samples/debian-desktop/` | 16 + 13 + 14 |
| ev-report-fix | `check-1-census/report-check/` | 2 |
| ev-provenance | `check-1-census/provenance/` | 5 |
| ev-law-proto | `check-2-law/stand/` | 82 |
| ev-channels | `check-2-law/channels/` | 137 |
| ev-law-second | `check-2-law/second-implementation/` | 95 |
| ev-root-signals | `check-2-law/root-signals/` | 47 |
| ev-repro-proto | `check-3-reproducibility/stand-pair/`<br>`check-2-law/stand/src/ (inventory.py, compare-inventories.py)` | 3 + 16 |
| ev-repro-pairs | `check-3-reproducibility/clean-install-pairs/` | 14 |
| ev-repro-hw | `check-3-reproducibility/hardware-profiles/`<br>`check-3-reproducibility/state-transfer/` | 9 + 19 |
| ev-lifecycle | `check-4-lifecycle/stand/`<br>`check-4-lifecycle/random-generations/`<br>`check-2-law/stand/raw/ (check-lifecycle-v2.jsonl, fb1/check-browser-lifecycle.jsonl, q/main/lifecycle-v3.jsonl)` | 3 + 14 + 62 |
| ev-lifecycle-stands | `check-4-lifecycle/stands/` | 26 |
| ev-rollback | `check-4-lifecycle/rollback/` | 22 |
| ev-authority | `check-5-authority/stand/` | 5 |
| ev-authority-stands | `check-5-authority/stands/` | 53 |
| ev-formal-lit | `definitions-analysis/formal-and-literature/` | 33 |
| ev-apply-crash | `open-problems/apply-crash/` | 35 |

## 3. Numbers of the paper recounted from the files of this repository

Each value below was recounted from the published (cleaned) file named in the last column; all agree with the paper.

| Key | Quantity | Value | File |
|---|---|---|---|
| ev-v-census | rows compared | 398 | `check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/metrics.json` |
| ev-v-census | agreement % | 63.32 | `check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/metrics.json` |
| ev-v-census | kappa | 0.45480 | `check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/metrics.json` |
| ev-w-census | rows compared | 178 | `check-1-census/guix/raw/v3/stats.json` |
| ev-w-census | agreement % | 80.34 | `check-1-census/guix/raw/v3/stats.json` |
| ev-w-census | kappa | 0.63346 | `check-1-census/guix/raw/v3/stats.json` |
| ev-samples | Ubuntu+Alpine rows | 262 | `check-1-census/samples/ubuntu-alpine/E6C-statistics.json` |
| ev-samples | Ubuntu+Alpine five-category agreement % | 29.77 | `check-1-census/samples/ubuntu-alpine/E6C-statistics.json` |
| ev-samples | Ubuntu+Alpine literal agreement % | 6.11 | `check-1-census/samples/ubuntu-alpine/E6C-statistics.json` |
| ev-samples | Arch/Silverblue/FreeBSD rows | 510 | `check-1-census/samples/arch-silverblue-freebsd/raw-X1C/metrics.json` |
| ev-samples | Arch/Silverblue/FreeBSD exact agreement % | 12.94 | `check-1-census/samples/arch-silverblue-freebsd/raw-X1C/metrics.json` |
| ev-samples | desktop Debian rows | 235 | `check-1-census/samples/debian-desktop/raw-X2C/statistics.json` |
| ev-samples | desktop Debian exact agreement % | 7.23 | `check-1-census/samples/debian-desktop/raw-X2C/statistics.json` |
| ev-provenance | created paths (primary set) | 2058 | `check-1-census/provenance/X9-paths.tsv` |
| ev-provenance | paths with exactly one creator | 2053 | `check-1-census/provenance/X9-paths.tsv` |
| ev-provenance | created_unique_paths in analysis.json | 2058 | `check-1-census/provenance/raw-X9/analysis.json` |
| ev-channels | channels per system | 64 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-channels | stand denials (C) | 40 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-channels | stand observed effects (O) | 21 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-channels | stand prerequisites unavailable (U) | 3 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-channels | NixOS channels | 64 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-channels | stand rows left open as the O5 definition hole | 15 | `check-2-law/channels/raw/d2-classified-results.json` |
| ev-law-second | launches with permission changes/replacement | 104 | `check-2-law/second-implementation/raw-FX-P3-1-1/analysis/verification.json` |
| ev-law-second | accepted incomplete copy, permitted launch failed (times) | 2 | `check-2-law/second-implementation/raw-P4-8/analysis/summary.json` |
| ev-root-signals | automated command with all five signals | 5 signals, joint predicate satisfied | `check-2-law/root-signals/raw-E2/summary.json` |
| ev-law-proto/ev-lifecycle | lifecycle assertions passed (original fixture) | 102 | `check-2-law/stand/raw/check-lifecycle-v2.jsonl` |
| ev-law-proto/ev-lifecycle | lifecycle assertions passed (caller-placed state) | 94 | `check-2-law/stand/raw/q/main/lifecycle-v3.jsonl` |
| ev-law-proto | virtual Wi-Fi: IP replies received / sent | 2 / 2 | `check-2-law/stand/raw/q/main/radio-final.log` |
| ev-law-proto | virtual Bluetooth: L2CAP echo replies | 2 | `check-2-law/stand/raw/q/main/radio-final.log` |
| ev-law-proto/ev-lifecycle | size of the untracked browser crash-report settings file (bytes) | 40 | `check-2-law/stand/raw/fb1/check-browser-lifecycle.jsonl` |
| ev-repro-proto | baseline package records (both) | 324 / 324 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | added package records (each) | 777 / 777 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | packages equal | 1101 / 1101 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | accounts equal | 31 / 31 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | active_units equal | 43 / 43 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | unit_file_states equal | 138 / 138 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | modules equal | 52 / 52 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | pci equal | 8 / 8 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | userspace process records | 20 / 20 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-proto | kernel tasks | 68 / 69 | `check-3-reproducibility/stand-pair/raw/q/repro/summary.json` |
| ev-repro-pairs | NixOS pair: reachable store objects (a / b) | 580 / 580 | `check-3-reproducibility/clean-install-pairs/raw-X5/nixos/analysis-summary.json` |
| ev-repro-pairs | Guix pair: reachable store objects (a / b) | 353 / 353 | `check-3-reproducibility/clean-install-pairs/raw-X5/root-audit-guix.json` |
| ev-repro-pairs | Debian pair: package records (a / b, equal) | 168 / 168 / True | `check-3-reproducibility/clean-install-pairs/raw-X5/debian/comparison/supplement-summary.json` |
| ev-repro-hw | inventories obtained / planned | 140 / 160 | `check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/report-metrics.json` |
| ev-repro-hw | final observations obtained / planned | 14 / 16 | `check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/report-metrics.json` |
| ev-lifecycle | random generation transitions | 512 | `check-4-lifecycle/random-generations/raw-X6/coverage.json` |
| ev-lifecycle | deletions of saved generations (random GC) | 253 | `check-4-lifecycle/random-generations/raw-X6/coverage.json` |
| ev-lifecycle | checkpoints passed | 805 (no failures) | `check-4-lifecycle/random-generations/raw-X6/coverage.json` |
| ev-lifecycle-stands | ordinary-work sequences (primary) | 48 | `check-4-lifecycle/stands/raw-P7-1/post/execution-statistics.json` |
| ev-lifecycle-stands | sequences that lost access after restore / primary | 40 / 60 | `check-4-lifecycle/stands/raw-P7-3/analysis/final/summary.json` |
| ev-authority | scenarios / expectations met | 54 / 53 | `check-5-authority/stand/raw/q/authority/final-owner-authority.jsonl` |
| ev-authority-stands | Unix-allowed access rejected via personal declaration: cases x runs (original + replay) | 4 x 2 | `check-5-authority/stands/raw-P2-4/authority-matrix.json` |
| ev-authority-stands | contradictions to declared files (D/N primary endpoints) | 10 | `check-5-authority/stands/raw-FX-P3-2-1/run-1/matrix.csv` |
| ev-authority-stands | ineffective lists (forbidden program still runs) | 4 | `check-5-authority/stands/raw-FX-P3-2-1/run-1/matrix.csv` |
| ev-authority-stands | BQ: no-list Unix gap endpoints | 216 | `check-5-authority/stands/raw-P8-1/server/BQ/analysis/independent/summary.json` |
| ev-authority-stands | X3: no-list Unix gap endpoints | 216 | `check-5-authority/stands/raw-P8-1/server/X3/analysis/independent/summary.json` |
| ev-apply-crash | primary trials (immediate / after sync) | 6 / 6 | `open-problems/apply-crash/raw-P4-2/analysis.json` |
| ev-apply-crash | acknowledged state survived (summary) | 6 | `open-problems/apply-crash/raw-P4-2/analysis.json` |

## 4. SHA-256 of every file

`MANIFEST.md` itself is not listed.

```
5eebefd3682e32d661f307a28539b304e5e52fb1eb33ba214e61d7a57663e4f0  LICENSE
62191fd767a50c67dd9923e6c7407f9bbd07e5fd5412e0b200c341dc18b2f1ee  LICENSE-CODE
12dc9ae252b175bd2b69722a826939068d4990b050212be0bdab06c463ceaf93  README.md
e5db48196d5ba90107636e16d656cab5d747da0e1b8831119f84d190e5bfc3ea  check-1-census/debian-fedora-coreos-nixos/METHOD.md
5a184715436b5aa8ef48b3457d26170c6d4c9a22be4ac967eec1ece48703580b  check-1-census/debian-fedora-coreos-nixos/RESULT.md
4aac4b78585fd061f7d622e62b2225ac2057dd2c92e55003fe3128d97dc8293a  check-1-census/debian-fedora-coreos-nixos/REVIEW-2.md
3320402d92cd41a85b042fe456a515c7af78cae31d21df63830b2775f75a29c1  check-1-census/debian-fedora-coreos-nixos/c1-classes.tsv
6f14012b4c0e0dd3a663980f45f050ee81e97f33cf1d38a8fb1ede7f119e383e  check-1-census/debian-fedora-coreos-nixos/c2-classes.tsv
71519d1905bec9d7f430c9ce486d7e411be0661a7cf858f1d3927c999798b1cc  check-1-census/debian-fedora-coreos-nixos/collect.sh
80f094ad58e54f708f406d05d3a71a1ee7701d05f6efe5c3232a944b9d394629  check-1-census/debian-fedora-coreos-nixos/compare-adjudications.tsv
a971f6cfd06dc1ff274dc7ce739f2645b2bba6e5d91641a2fefc67060e366142  check-1-census/debian-fedora-coreos-nixos/compare.py
402447cf150bfafa4631748aca3b7ec3462ed6db9d906734ef93bd33f6efeeed  check-1-census/debian-fedora-coreos-nixos/day-coreos.sh
693d203d9add90624a9108f17cc17f1b2b738605d8c969974eb36199639fe463  check-1-census/debian-fedora-coreos-nixos/day-debian.sh
75b5e29f3f555396fafc602ebadfab787de8c53d9afe9c994046555f8f4d5680  check-1-census/debian-fedora-coreos-nixos/day-nixos.sh
8bd4cd78f57a4ef60c6296d210d635428f9d31a9a12739eed6e402f0b712ebc7  check-1-census/debian-fedora-coreos-nixos/inventory-stats.json
b3a7fca82a79fb1e949b3fa36c3a06f6b89bceece77986db72ca8d819982ff34  check-1-census/debian-fedora-coreos-nixos/nixos-outside-configuration.tsv
568932cf0dc0745d43ed18a4e2eb94c03d0863e632d81371053a3573fe8b3217  check-1-census/debian-fedora-coreos-nixos/preclass.py
88982b4de0ed18cdf087047d88ae39093dfe5104a2f0167abde47a853fb114db  check-1-census/debian-fedora-coreos-nixos/preclassified.tsv
64d66882c9ec9b07ccca959dbb602994be3080bab1189412bf1537c7439ea665  check-1-census/debian-fedora-coreos-nixos/raw/a1-preclass-reference.py
8700c084a48f784695d54b24c7e38e0e29413238fbac248c66f2925c087da818  check-1-census/debian-fedora-coreos-nixos/raw/coreos/accounts.txt
50734de417c588f6886dc29b72deb28fae8312c136128baf3c1fa539838660e2  check-1-census/debian-fedora-coreos-nixos/raw/coreos/checksum.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/debian-fedora-coreos-nixos/raw/coreos/collector-errors.txt
2d9d350ef5292b3d6500f5a1def06ddc106363a4718c3c2d03e800523cbaee60  check-1-census/debian-fedora-coreos-nixos/raw/coreos/day-after-reboot.log
f7dde0d4e99f44cd461c00fe62906da12c7161d1cf47947073729f37947b9216  check-1-census/debian-fedora-coreos-nixos/raw/coreos/day.log
14eb304ff3c2a17f8125b87ca1851160e91c6162d3ef19026b59d1f761c5ecc8  check-1-census/debian-fedora-coreos-nixos/raw/coreos/device-drivers.tsv
adf75aa8462bb03afd6ccf229e6c68bf77d64d97b4a1f17b8e988302cc2c59a5  check-1-census/debian-fedora-coreos-nixos/raw/coreos/directory-only-groups.json
66a255703843065f536618d9cff1ae945b2d98cc7152967028d18e3d78f0f472  check-1-census/debian-fedora-coreos-nixos/raw/coreos/end-time.txt
69d786547049af5cc6f08a8c5de066bd1ff97755c33908b1765b0590cbc437a8  check-1-census/debian-fedora-coreos-nixos/raw/coreos/files.tsv
46f20f05d86669ef1a133aeb59e705cf6ffe1a638e680f37a7248c070e1c2190  check-1-census/debian-fedora-coreos-nixos/raw/coreos/groups.txt
f619685d9ff342ed1c3974fd19f2dfa6f9f5ff89984e719a38188038ecf35876  check-1-census/debian-fedora-coreos-nixos/raw/coreos/image.sha256
6de32b94cd9c290bda443a3e7a86c08de052e56debf2d4ee4ddccbf2fd00f5a8  check-1-census/debian-fedora-coreos-nixos/raw/coreos/module-files.tsv
b633e670a9fe57bda3702948d8f40530e49c04100861a2a9d43d3773a7d0ee2b  check-1-census/debian-fedora-coreos-nixos/raw/coreos/modules.txt
d00a3902717a501fabc2f0629f211f07e0d5ec3e59a4af17ef1c048b50774c89  check-1-census/debian-fedora-coreos-nixos/raw/coreos/mounts.txt
ca50ff954e2e994ae35dc5e725f94ebc91621b697c759295fdc5d9b84143d125  check-1-census/debian-fedora-coreos-nixos/raw/coreos/os-release
bd59b71f0823e29d9ff3012fc774608cb79e621f7a961ca88ce08d1852c0829a  check-1-census/debian-fedora-coreos-nixos/raw/coreos/ostree-status.txt
4403e857e94b571eb4ea22aa8ae79166fc76d4522e0a6106f0f97edfe8ed2e5d  check-1-census/debian-fedora-coreos-nixos/raw/coreos/package-files.txt
c38a1fb400173e08b62e599613b8ae0ccc6cd75489013548ca5cd6fa14c6dd92  check-1-census/debian-fedora-coreos-nixos/raw/coreos/package-manager.txt
2879cb79456111046a403701e45e33d8cb90ed488e0ec332325d8e2decbcd9c9  check-1-census/debian-fedora-coreos-nixos/raw/coreos/packages.tsv
46700b2dcdd55b2c9c09238bc131856c0e8da7f26313d220b880f3fdcfb2792b  check-1-census/debian-fedora-coreos-nixos/raw/coreos/path-aliases.tsv
e2edda8b7cce5b044cbae567e8c9a4f4cda5c8c015ac7fc90f969c5bfbe1630c  check-1-census/debian-fedora-coreos-nixos/raw/coreos/process-executables.tsv
a5883d1d0e91c2a34c8bad035f27f652ad01ca2efcfd1f5ca0f258efa4fa6f6b  check-1-census/debian-fedora-coreos-nixos/raw/coreos/processes.txt
288d3549b402e034d70d5706411729eeaa22c8747d2acba80a3f7b2d5b804887  check-1-census/debian-fedora-coreos-nixos/raw/coreos/rpm-ostree-status.json
2f484fb18432ce2fa5ee983aafcdc7836cb19f9a515cd3c5fe21ef1f16d8a1ee  check-1-census/debian-fedora-coreos-nixos/raw/coreos/source.txt
7330881ea2db8cb9785709ca3f994d0eedbcf1ae22d20d88abb205b13327c1e5  check-1-census/debian-fedora-coreos-nixos/raw/coreos/time.txt
94e8c81f46cff11fddb03333a7a144423cdc124e4f87e5852f0dc8aa291ef326  check-1-census/debian-fedora-coreos-nixos/raw/coreos/timers.txt
1071004b8ae684761774522659a633b338e759751937ba5956b074b36cf1d818  check-1-census/debian-fedora-coreos-nixos/raw/coreos/uname.txt
8fa3112749996065b7e6a00786d5cccb2fb863d3c0fc3b33bd92e243a19c8be8  check-1-census/debian-fedora-coreos-nixos/raw/coreos/unit-files.txt
e34b194d86b32eb3671669cc1acff995f47a36e72662b85966c8a4210a163b99  check-1-census/debian-fedora-coreos-nixos/raw/coreos/unit-paths.txt
74815c2a38e0ceeed8024e34a64ab495285c65283113a0972fad097b0546fba9  check-1-census/debian-fedora-coreos-nixos/raw/coreos/unit-realpaths.tsv
e66a87dfc7aa7c78b115e212491720f160dddd6597ed61e2668408d5acee5de1  check-1-census/debian-fedora-coreos-nixos/raw/coreos/units.txt
488428000af6b33a040c3c6a030e7f9b4dacff2bd77aff136a9ed65190a50d23  check-1-census/debian-fedora-coreos-nixos/raw/coreos/unowned-groups.json
7cd12374e991ddea9778cdf0c85fcbc89c22920d647463d2c0efc73d602f7993  check-1-census/debian-fedora-coreos-nixos/raw/coreos/user-list-timers.txt
87df884c2f36fcf558647c75a6ddf133f2aa24a3ba8161e830c3c5c4d1f00ae3  check-1-census/debian-fedora-coreos-nixos/raw/coreos/user-list-unit-files.txt
cf34bdc20f8bf7acc6d35f74b913f7d40b64b7592dae5d6599bb9d2217f093a2  check-1-census/debian-fedora-coreos-nixos/raw/coreos/user-list-units.txt
505768371a38d104b6347b7a8251518914e3174451cdad3bb6003c132c1301c7  check-1-census/debian-fedora-coreos-nixos/raw/coreos/user-manager-state.txt
54289cb71b8bcbe4bf70f059fb85e33c827ec8803fee32023a0cc03fc21a0029  check-1-census/debian-fedora-coreos-nixos/raw/coreos/user-unit-paths.txt
a2b96e3ef201e09cd39988236571bc73f9849e90cf5326043267bd31fe765f7d  check-1-census/debian-fedora-coreos-nixos/raw/coreos/walk-roots.txt
5249ad82c162909dd41c231be2360306a999e0653623df8d9761367872987338  check-1-census/debian-fedora-coreos-nixos/raw/debian/account-definitions.txt
8fbd4a9e89530f64025126ecb62ff5849708930e0724203c2d48d48324b74db6  check-1-census/debian-fedora-coreos-nixos/raw/debian/accounts.txt
75424ceecadb5b74c6bca8a56c4b43134fd7ce655b40578cb4b3cdd959ddd570  check-1-census/debian-fedora-coreos-nixos/raw/debian/checksum.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/debian-fedora-coreos-nixos/raw/debian/collector-errors.txt
4e29cfd66542d9f3b5daa9361cc1a9f40f7752b3ac18c4f3bf2f0398f440d1c0  check-1-census/debian-fedora-coreos-nixos/raw/debian/conffiles.txt
947e7aa87bdbbbfe845cd24b1feabab769cd468cc10bfea3db312d1dcbce8942  check-1-census/debian-fedora-coreos-nixos/raw/debian/day.log
d7253ca0d988b7c826e487379905f5be8d6e08845353d99063f8195fe7a0a79e  check-1-census/debian-fedora-coreos-nixos/raw/debian/device-drivers.tsv
ea6f01eedba5a8239fcaeae230e67f893cf69af336b79dac0904d3b7ff7aa19a  check-1-census/debian-fedora-coreos-nixos/raw/debian/directory-only-groups.json
a9af69c66acd954a8d26f0570aeeabeaded316ef9f8b1b2b999f45ff1b88cd97  check-1-census/debian-fedora-coreos-nixos/raw/debian/end-time.txt
b8b3eb9e074c6bc8b511822fa9a67dc64e9813e8a2e4d6defa782fa6a9678bfd  check-1-census/debian-fedora-coreos-nixos/raw/debian/files.tsv
636cd19818afee61188eebe0d35c0edb144a4495d5366decd23ef11090889c51  check-1-census/debian-fedora-coreos-nixos/raw/debian/groups.txt
646700c853aa8505366f1d5dad71f2ba9b99b50fb09283a6e5cafb4e1c240ad2  check-1-census/debian-fedora-coreos-nixos/raw/debian/module-files.tsv
67da3fff32ace0b82404ed834419b68dc3e0880f6f31dc9ae5861ad89a1f32fe  check-1-census/debian-fedora-coreos-nixos/raw/debian/modules.txt
bff4050a111a765febdcedde1434fe98d338df8547cc309223b76d82e80ac5a9  check-1-census/debian-fedora-coreos-nixos/raw/debian/mounts.txt
59a77b5f2666d9c85c489bd1911a6eebbd91ef22fe48b90a3b75f1b21f3844d4  check-1-census/debian-fedora-coreos-nixos/raw/debian/os-release
a307b3153fee0ed1094107a2ebe537cdff4530cf75425ba3e3318d01ccdee760  check-1-census/debian-fedora-coreos-nixos/raw/debian/package-files.txt
d860f2ec4a2eef1f25479cea84e223dc43a18a955b2aea98f914dafaa2ba8bde  check-1-census/debian-fedora-coreos-nixos/raw/debian/package-manager.txt
35b9e627b7717cfd5518dea7071cbe7e38a3692b3bec9511f581d85cf7253204  check-1-census/debian-fedora-coreos-nixos/raw/debian/packages.tsv
5ab14e74ec173cf55c8708e81d055a908c304438f296a4cfa4cd017bd898a1b1  check-1-census/debian-fedora-coreos-nixos/raw/debian/path-aliases.tsv
bc231de6fe706d2203a3e0b22c05cff602735f8f1ce571bb51459bb62145b517  check-1-census/debian-fedora-coreos-nixos/raw/debian/process-executables.tsv
fde6e27b78f314a407f389fc2390ac4769de07cbf4f0d9dae78f022839963354  check-1-census/debian-fedora-coreos-nixos/raw/debian/processes.txt
b1804d8e45852be4c27c3f8c9e12b75159de6cc4a607abcc1416e98b6678b3c6  check-1-census/debian-fedora-coreos-nixos/raw/debian/source.txt
821f72f937d176ed844a1e6d0da95720195c9e4822dea37fb7150f024f138e78  check-1-census/debian-fedora-coreos-nixos/raw/debian/time.txt
b7b5c325c233e298ae048e563b80097ba2db5f0c70af6ea886050ed31a297d53  check-1-census/debian-fedora-coreos-nixos/raw/debian/timers.txt
216b726a16352aacd39f9a8ea80046b1531a5a700cb2a5d39ceaf5e3e187fda7  check-1-census/debian-fedora-coreos-nixos/raw/debian/uname.txt
58113e4a701c5890e4094aa2154319e25375273bf296a97fe8cc4173ceecd048  check-1-census/debian-fedora-coreos-nixos/raw/debian/unit-files.txt
a483320735e9d20da3412233d6296427a2c8a06208637e9148fced1dc8f17dea  check-1-census/debian-fedora-coreos-nixos/raw/debian/unit-paths.txt
340fc3180e0eeead41d0166fb0ec7042c7f067e8b449d371b359124f8c5bbece  check-1-census/debian-fedora-coreos-nixos/raw/debian/unit-realpaths.tsv
e0226de538a09dc4f1fe1843a46b69f8becf2c693ff2dbe504a3370cc8915287  check-1-census/debian-fedora-coreos-nixos/raw/debian/units.txt
e973ddb03304de11bfd1aa95f01e1802146c0c683a31e031b2b593159c0d583a  check-1-census/debian-fedora-coreos-nixos/raw/debian/unowned-groups.json
3a0c64056c3a604b51ec4c064f9d03e12978d94020dc1005fab89e0a77ae37bc  check-1-census/debian-fedora-coreos-nixos/raw/debian/user-list-timers.txt
bdc12e46bf82fe773108bda048f6dd0cf18960cccc94d0cb986c3f8e0ad68ec4  check-1-census/debian-fedora-coreos-nixos/raw/debian/user-list-unit-files.txt
53174ee5fca7db0a33459431ab3a7e4a4429f8b073e151ca5083984ed3eb4afe  check-1-census/debian-fedora-coreos-nixos/raw/debian/user-list-units.txt
505768371a38d104b6347b7a8251518914e3174451cdad3bb6003c132c1301c7  check-1-census/debian-fedora-coreos-nixos/raw/debian/user-manager-state.txt
acdd7080c389e2e148a6d55cc7d1f26e7698a6582375fb20b2cd5715450dd9b2  check-1-census/debian-fedora-coreos-nixos/raw/debian/user-unit-paths.txt
8ed37e4c3e9d490a50bf3a165b35d83055cf5b0932f7f45cca06a5a69745a2d1  check-1-census/debian-fedora-coreos-nixos/raw/debian/walk-roots.txt
af760afcf6e48fdc356647c8074b1d1cf4aa46f7311880c3e07f0521794cfcb9  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/agreed-holes.tsv
e73820ab7fe7206042da2132d401adb68398b9698797bc4ea8c11d1e8294e115  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/disagreements.tsv
f0833d95769b559e8d8e832b2cc985d1dc8d72254b5b0bd910d5974320dcb454  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/holes.tsv
cb1b40d0b0ed3d6aa37b125297490a6eb479e5037cd0954914f87867cf94762f  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/joined.tsv
18f583b236d8982f73dcc1349029eabfccaab7f2bc552ff186ff86d9faea209b  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/literal-disagreements.tsv
b9bd8d669de31aea7a1cd8fc5d28979052dd2a17013692e8fd69dbbfe282663f  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/metrics.json
56951ec2eaa07f954c6a787df4c360934618cff559d610615cbc33aa7037b5a6  check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/owner-disagreements.tsv
ed874ec363f75a053fce9ee4733426d9742997df050ee89e42504b859353b152  check-1-census/debian-fedora-coreos-nixos/raw/nixos/account-definitions.txt
20d9db3fcac5b78de48a54f2ef8187c92d3fed683b5cce05513cc976c93cd860  check-1-census/debian-fedora-coreos-nixos/raw/nixos/accounts.txt
bd4d64343254883801ee4fac331574fe1dbc4d60a82d18ec630f47a76ee84ecc  check-1-census/debian-fedora-coreos-nixos/raw/nixos/activation-script.txt
2c5edc000e08c10f43eb25241a5f75fbbcb9d44b4a0a0ba0dd1b568607738dfd  check-1-census/debian-fedora-coreos-nixos/raw/nixos/checksum.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/debian-fedora-coreos-nixos/raw/nixos/collector-errors.txt
1358f93aa54f9d0434c11251f7f4c688a9ea0b385abde9a3a268f3dab2565285  check-1-census/debian-fedora-coreos-nixos/raw/nixos/current-system.txt
c76ecfe4e03d450a7261825d166e015af8c3294b7faab005ec0e547963abd828  check-1-census/debian-fedora-coreos-nixos/raw/nixos/day.log
e399490ab87f4209882d9b2f915fc9faaddf7efa95803ab08f5f3ee1cce30500  check-1-census/debian-fedora-coreos-nixos/raw/nixos/device-drivers.tsv
b5a2ec0d7d270012af5f6cc409b306b6b14dfb8f80f788508638553dacd512d7  check-1-census/debian-fedora-coreos-nixos/raw/nixos/directory-only-groups.json
a99d1c6483b7b8ed986bb4648447bbd9489378a498c6550c0265c928246d86f8  check-1-census/debian-fedora-coreos-nixos/raw/nixos/end-time.txt
3b8e24766a615bea0d41232eed319da4ff7ef214978142bacd950eacafebe031  check-1-census/debian-fedora-coreos-nixos/raw/nixos/files.tsv
b0894ac134bae493e21eb7dea9ecc7785f1b8dc42edc29da015720b9fe429d3b  check-1-census/debian-fedora-coreos-nixos/raw/nixos/groups.txt
70bbf892e88e127b6046684425866102c839105806f1c7a3029394ce95ad4705  check-1-census/debian-fedora-coreos-nixos/raw/nixos/installed.txt
41a94fc0d50a30db74678b647306fccb936d160028f4ece62b11c4776389475a  check-1-census/debian-fedora-coreos-nixos/raw/nixos/module-files.tsv
86ac2fac5839c16aa112e5f8f1b0e6765b5efff809aac8c46b91f92ba5bf4271  check-1-census/debian-fedora-coreos-nixos/raw/nixos/modules.txt
48464dc68056e62f5e292ee23859e1b2bc0efe49b0d57bcc0c3c073aaaa7ebc0  check-1-census/debian-fedora-coreos-nixos/raw/nixos/mounts.txt
da1414c587f767e5ea601324e1cf571935bf9f76b57c077dffcb0932429f5608  check-1-census/debian-fedora-coreos-nixos/raw/nixos/nix-builder-accounts.txt
f125dfe6cb91d99d379371be660a99bf00dacd47f140967e0c195ffafdd099b3  check-1-census/debian-fedora-coreos-nixos/raw/nixos/nix-profiles.tsv
a45cf5f47790aec527d8dd1d2b80d18a443dd4998b8f3aa784c8979a3a6d9ca2  check-1-census/debian-fedora-coreos-nixos/raw/nixos/nixos-configuration/configuration.nix
68d9c33e354bc957f708b6b310a3b6376743d47cf9e98505f9eed8bf9d38e304  check-1-census/debian-fedora-coreos-nixos/raw/nixos/nixos-configuration/hardware-configuration.nix
7720f685675dfa775b698f45f9f38c29f420184c91f5cc3fd4ffbfbb62d16a25  check-1-census/debian-fedora-coreos-nixos/raw/nixos/os-release
21d2013e3081f1e455fdd5ba6230a8620c3cfc9a9c31981d857fe3891f79449e  check-1-census/debian-fedora-coreos-nixos/raw/nixos/package-manager.txt
38cd6b4a2f2c3ecc08ff892165e91c02936c937f9b4bf5f1e8706c5c9952afe6  check-1-census/debian-fedora-coreos-nixos/raw/nixos/packages.tsv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/debian-fedora-coreos-nixos/raw/nixos/path-aliases.tsv
02f32a621cdcc5031dbfb6750f16f6d6a87270dcd3b326d74b95761aa91e01e4  check-1-census/debian-fedora-coreos-nixos/raw/nixos/process-executables.tsv
e1a70f8aa402def31557dee1435dda54bbd497d3f64e11d25da7bc0407a364ec  check-1-census/debian-fedora-coreos-nixos/raw/nixos/processes.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/debian-fedora-coreos-nixos/raw/nixos/root-profile.txt
bfc07603134b0637149dec5746efae9a3215c501adb901cb934b6fd58fad6eb9  check-1-census/debian-fedora-coreos-nixos/raw/nixos/source.txt
606477036467a15e8d15633fa7534ef64f89430994feaf2ccaf062700e4cf25c  check-1-census/debian-fedora-coreos-nixos/raw/nixos/store-outside-system-closure.txt
38cd6b4a2f2c3ecc08ff892165e91c02936c937f9b4bf5f1e8706c5c9952afe6  check-1-census/debian-fedora-coreos-nixos/raw/nixos/store-top-level.txt
d88f81b6a7bba43c42299a2e952dbb90a09d4ec78849851c137fae3cbfa0fc87  check-1-census/debian-fedora-coreos-nixos/raw/nixos/system-closure.txt
e62b4ed324ef60c827e23c8300aa16bc16166af6b8b0a0520877e8afb7ff4364  check-1-census/debian-fedora-coreos-nixos/raw/nixos/time.txt
31a79e1bfb1a5ff09093ec96323b2ccef4166d3d8241eb757601c4357708f417  check-1-census/debian-fedora-coreos-nixos/raw/nixos/timers.txt
1acc13d7be5b3d8f6eaaf30db7efe6f94fcac33dbaedf530e79b5bef7ff91d7a  check-1-census/debian-fedora-coreos-nixos/raw/nixos/uname.txt
55b906bae963cebae369b587fc7347d196cc196c8f7ded06343b7dd4ba869a65  check-1-census/debian-fedora-coreos-nixos/raw/nixos/unit-files.txt
d9a9169cf9b1ff296c7bcae8ec87a2d3cab4c6515c17e101cba0b2a335d55d05  check-1-census/debian-fedora-coreos-nixos/raw/nixos/unit-paths.txt
668e4d81964c212f1e43c172634343a64657af7b6bfc614ef426df879cc7a992  check-1-census/debian-fedora-coreos-nixos/raw/nixos/unit-realpaths.tsv
d9d0d16ef46c28ff7855bea479b52605e436b491dadcc4870ecc893189c96307  check-1-census/debian-fedora-coreos-nixos/raw/nixos/units.txt
4a2b8e81df484d19751978020f60552d842e89bb074eb7648b8844698372fc42  check-1-census/debian-fedora-coreos-nixos/raw/nixos/unowned-groups.json
16ca56da312f0f1f7d443a6489bb671eca863c47686ca3a60067ae277d9ccdbc  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-closure-outside-system.txt
942a1ac76d40305f9b1fe4c31beb1f18f942fbacfff00d85fd082f5e5d2e6894  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-closure.txt
faf44d497e0868eaafc4608ce488966ed54466907ba6cc45d7d33a75c2308af2  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-list-timers.txt
8596932d0adb90c6c9d5245b98f8e0def4e501b2b70463cc18460fe51727c2da  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-list-unit-files.txt
7afdc538495c7508dbff1768ce8460241ee1d82cddb6f19a293c6fd3044b995b  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-list-units.txt
505768371a38d104b6347b7a8251518914e3174451cdad3bb6003c132c1301c7  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-manager-state.txt
9c3bc0b84f9fc9a9c7eea64ee206952b400b934c0b7da7e79a8d7bed765bb8d0  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-profile.txt
5a79124819cad1f59baeec381d2aec826285cf8f8f349ed85ffab581b454281b  check-1-census/debian-fedora-coreos-nixos/raw/nixos/user-unit-paths.txt
6a0aa235e835f82618d5e60dfe60e91181f7fa3b33eeb6c0ae03cc205307f092  check-1-census/debian-fedora-coreos-nixos/raw/nixos/walk-roots.txt
5e2b371d294cb8c1fde2aa86e5be94a5aff2d0daf5245a0a71da235ec8741b9f  check-1-census/debian-fedora-coreos-nixos/residual.tsv
aecbc9ce581d25d567d74cfd3be74d8a607daa2478c642506783f900acb47a6b  check-1-census/guix/METHOD.md
5624980d37663d19e9d96fe37a687e1d0c89d1ffef303f05534cf069b5ce3122  check-1-census/guix/RESULT.md
2ebb930b98f1b2daaa1d6bd522933d366b4c41e6ff1f5683c074a6deab353bb9  check-1-census/guix/REVIEW.md
5db3823120d97b617130d2f5204e0d0ba938a31236d08b109c2017b29ad2413b  check-1-census/guix/c1-classes.tsv
7619ba75fc5e5dd3701bb533184af495b3d9a7f1297c51f4333faf53a66e31d2  check-1-census/guix/c2-classes.tsv
45bbfb02f4a56d19864229fe6c1c2283bf7bc9a31192822082161aeb60041449  check-1-census/guix/collect.sh
b1b8dcc49e44b4d14cc17bcb809e6f33c052033f393827bd5725144c1f2cac82  check-1-census/guix/compare.py
5463a929a200d679368b3e3071c3542e99e6847ef06785bfe73fefa6b28653e2  check-1-census/guix/day-root.sh
9f6e5f1ce9873dd4318941d87286cb838d2827482eef3aa4c183a80e2b1edc7b  check-1-census/guix/day-user.sh
baf332ff2bbf3991f6880529d8585ceeea669141049c79bfe8c16f0b38ccb70c  check-1-census/guix/definition-audit.md
e3198ba1723503f4c5f2989d00b561d2440c9e319d4305f118066dc6454df05a  check-1-census/guix/definition-audit.tsv
2f9ebab38e690d1ed37b4ae8b77227da4fc1a23c25189c0eb2002007d6b7d0ac  check-1-census/guix/guix-outside-declaration.tsv
40e3bac799271cddd9de75fe689a4dae54e6a5864be0877ad261ec91637756fc  check-1-census/guix/home.scm
0ebbf2ce20bc1260fc20f93a420352ab482ffd3cc8da36cc9cdf66e023490b76  check-1-census/guix/inventory-stats.json
493c51e9b626483a26afc300b1a446d12738a47ef88311f18bfbf01cd09a98d0  check-1-census/guix/preclass.py
6765b453cf141cf0cfd44826e6ff0bb86dbcd26126127bc72bf748fd9c1047fe  check-1-census/guix/preclassified.tsv
cda51b387a0ed02fcb1dfce09a42a03fb2b3d341f84f96410c628a543cca65f1  check-1-census/guix/raw/a1-preclass-reference.py
b17d1a88a5080f1d246e88de0bf879a2fadc3ca2dd9f083c1cb6e92111ce2a5b  check-1-census/guix/raw/guix/accounts.txt
116125827890c06013f3dec217158d3faf2a178d16b0c4eb7e86ed227f21e6a2  check-1-census/guix/raw/guix/activation-source-paths.txt
0ac29a59b98b40638d8bccafafac0b6c8b597c2a34ba7e4f7936888869d6d21e  check-1-census/guix/raw/guix/census-user.txt
ec46d7375756b92972f08a22b1233dac9187000f0512d38b1905ed75607a1a0a  check-1-census/guix/raw/guix/checksum.txt
aeb8beebaa274284e902b5ee46a4b30449274185917eaec26919a638d759295c  check-1-census/guix/raw/guix/closure-comparison.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/collector-errors.txt
ecc16ad493c1ef27a6845554b0f6a57e295ecbfe72d1635a64597bcdeced944f  check-1-census/guix/raw/guix/command-status.tsv
e135e1e0aefbedfbe8e581c3900aaf215f14c720b1ba48d89108ae98614102a5  check-1-census/guix/raw/guix/configuration-paths.tsv
0b7ebfb365332db85816d02d6c1736ffbad49450029702bd6f9b45362197c8a3  check-1-census/guix/raw/guix/configuration/etc/config.scm
ef0a7f3818a8fbea186a48649e2972452d0668dbab6dcad9b2ee99cbf2605131  check-1-census/guix/raw/guix/configuration/etc/group
b17d1a88a5080f1d246e88de0bf879a2fadc3ca2dd9f083c1cb6e92111ce2a5b  check-1-census/guix/raw/guix/configuration/etc/passwd
724138dda292d1b7956c261f54e23f3db868706c50138c94a5fc2b5f3931ebe7  check-1-census/guix/raw/guix/configuration/etc/skel/.Xdefaults
0d833deed3e2c5aeeac2ca5bcaa3b1ebf3aeed320b41ad298751161fca91c928  check-1-census/guix/raw/guix/configuration/etc/skel/.bash_profile
eab40dd626d52ad1e1ff54431dcc7f75be4afe24070cffbda90aefbf3e96feaf  check-1-census/guix/raw/guix/configuration/etc/skel/.config/gdb/gdbinit
91f5421476f72d2c3290b4fa04d66300a70081897689328d4a049c25c486ab47  check-1-census/guix/raw/guix/configuration/etc/skel/.config/nano/nanorc
ea92c12bb1d48f8f0e183361493b0aac7509e6e3598c337818a890afffb1a85e  check-1-census/guix/raw/guix/configuration/etc/skel/.guile
2463ae208c212de5b59f8ac71af89e6b2e26626c3b1f3ddc0699a16366f3532b  check-1-census/guix/raw/guix/configuration/etc/skel/.zprofile
f207664b844b265cf50daf5d0e96399ff05810a9c4905fa6afc43e652f88b9ce  check-1-census/guix/raw/guix/configuration/etc/skel/guix-home-config.scm
3652c6c42fab841b5e02e34d5e14b5f80c52855557af8c14b5284e5770e64881  check-1-census/guix/raw/guix/configuration/home/guest/.guix-profile/manifest
40e3bac799271cddd9de75fe689a4dae54e6a5864be0877ad261ec91637756fc  check-1-census/guix/raw/guix/configuration/home/guest/home.scm
124e57fef78577d35a13dbab65a133028b753a1c8f1304be68915e12945c53df  check-1-census/guix/raw/guix/configuration/run/current-system/activate
0b7ebfb365332db85816d02d6c1736ffbad49450029702bd6f9b45362197c8a3  check-1-census/guix/raw/guix/configuration/run/current-system/configuration.scm
a27321308f06b194ac5f34ed90687c5d6bc0c8c6341fb56a64e9cd6a5f3a0c01  check-1-census/guix/raw/guix/configuration/run/current-system/parameters
a7f3a2660964cf2a1f568e00dcdaaa21de84f64f7198233fa4bdc33a66e82c4e  check-1-census/guix/raw/guix/configuration/run/current-system/profile/manifest
a3a36dfa130adff0fab22e8ce56775b7fd6346eb8f304cb1571d33a19103fbab  check-1-census/guix/raw/guix/current-system.txt
1917bee0a7d3412ab2c8cf9c44be3acf30a6e782d869dfa5ff2b742f0498232b  check-1-census/guix/raw/guix/day/user-day.log
7d975bffef60839af9209487751f3277868f76e67f04daba38047a9db92ead01  check-1-census/guix/raw/guix/device-drivers.tsv
741d8ac8f5aa784a13bc8203caf961a50b59edc7946e937afc6809ee014a79ce  check-1-census/guix/raw/guix/directory-only-groups.json
d3361e045948a5a5af047d30bd7d33986ebf59396277dd556094f22746881ce8  check-1-census/guix/raw/guix/end-time.txt
d876db6d095b682065ad217fba925ea4a67c30eadeedab69b15c3b64c658cfde  check-1-census/guix/raw/guix/files.tsv
c8c322ab81f58a100d4483c1e7c7584c5554d3339bf0a8a9843c06b17501a44b  check-1-census/guix/raw/guix/getent-path.txt
30d77055ad80d2c3f8c3964e395815fdf8d361364c509fa776ab73e7d7ffcc0f  check-1-census/guix/raw/guix/group-members.json
ef0a7f3818a8fbea186a48649e2972452d0668dbab6dcad9b2ee99cbf2605131  check-1-census/guix/raw/guix/groups.txt
f110f0d495e22273cdeca7f14491d3b8912f3f40f967954fdb14feae956a172c  check-1-census/guix/raw/guix/guix-builder-accounts.txt
db3b7953f6c628bb3c792e5639e37ae51427022de2de5dca1c62b219f7e5efc8  check-1-census/guix/raw/guix/guix-channels.scm
2ca525ef794b2870c6aa9d23ba489e0c5b9d9b8a476959d9a7c092703999d30e  check-1-census/guix/raw/guix/guix-profiles.tsv
6bd8f808a81577e14eb60900d551172a93e95f2c2ba8377de744c66db0ae959d  check-1-census/guix/raw/guix/guix-system-description.txt
a376d5a2a09685e12e136186a28266539c95f9ba248f676a7eb3ade802539e91  check-1-census/guix/raw/guix/guix-version.txt
4bf873a2b2b3b605c5b37eff63bd73240fd520b5a38ffc94cf8d092e351cffaf  check-1-census/guix/raw/guix/herd-all-service-status.txt
670ebdd7718e6a783c6766d204269f452936b91ed22741f736a01955e68cae98  check-1-census/guix/raw/guix/herd-detailed-status.txt
7e767676a2a16c967a9885e83248944d8a2703e63353c2a5f2322f18048e183b  check-1-census/guix/raw/guix/herd-log.txt
6a331f847b55d54143cd495726f3fa534cf391c6ef5cdafda85f44f27788dcf0  check-1-census/guix/raw/guix/herd-status.txt
cb1786445d4101b3623ae446d081ade3dce44a4d2d0ca61a31e52d74b9ccf744  check-1-census/guix/raw/guix/home-closure-outside-system-and-user.txt
cb1786445d4101b3623ae446d081ade3dce44a4d2d0ca61a31e52d74b9ccf744  check-1-census/guix/raw/guix/home-closure-outside-system.txt
3785080cb289572d531930e33c61d03ac835e038d10644bf46e826acb10c3441  check-1-census/guix/raw/guix/home-closure.txt
d27e2683632770904ca7f18b987aa2e1d88ebeaecc285c7dbfd6a3f3b50eb1a2  check-1-census/guix/raw/guix/home-description.txt
d27e2683632770904ca7f18b987aa2e1d88ebeaecc285c7dbfd6a3f3b50eb1a2  check-1-census/guix/raw/guix/home-generations.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/home-profile.txt
ddd9aeb83ffff59b6b530e44ca712e9bfb317397efaa74d443d62b8900356cec  check-1-census/guix/raw/guix/image-info.txt
ee8a39fab05612fc1c0d7299c5d174224ea4a34dca795857be1775831b7d40ac  check-1-census/guix/raw/guix/log-files.tsv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/mcron-schedule.txt
cc0c934faa08cdd980f473f4815e4257ad7246163a469bd1da21a6ed965597c6  check-1-census/guix/raw/guix/mcron-schedule.txt.stderr
c5752b2eb698657febbc789b49bc282a6b0a06c73804243139e44fde5039dac5  check-1-census/guix/raw/guix/module-files.tsv
b61d8f6bb43da8d767368831e3dcd5bb103f822dab43d86399ad046222f84b89  check-1-census/guix/raw/guix/modules.txt
7764429fdbaa34e99e5d11d01bddd7582e132771dcc03bb240b17ea6070892a3  check-1-census/guix/raw/guix/mounts.txt
d3ea841b7850dcf131c0859d024e7a107a66d9ba24a7a0cb325df29d6ab87691  check-1-census/guix/raw/guix/nsswitch.txt
138a194adeb2e44ba833463785e4f51df1eb3d30d5766996a42b120128618a8d  check-1-census/guix/raw/guix/os-release
b9f14046881ac1b835fe0d876dd7009af5de642f9b450cb0cd23c754e162bd78  check-1-census/guix/raw/guix/package-manager.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/path-aliases.tsv
7d9c8a48a97a115aa0a7cac5300a211c73231da3bf2baea0c35f736549476c34  check-1-census/guix/raw/guix/process-executables.tsv
8430517394d5b3a99b1e7c67620e43abb4d6d8c6a4f199de8c15daa7c75c24e6  check-1-census/guix/raw/guix/processes.txt
0b7ebfb365332db85816d02d6c1736ffbad49450029702bd6f9b45362197c8a3  check-1-census/guix/raw/guix/root-config.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/root-generations.txt
38770a951fe8a77b3407d99d6f7d5b90e662f1993d182ccce0438bcbe3d80861  check-1-census/guix/raw/guix/root-generations.txt.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/root-profile.txt
d094ac9ca317a5d19f96dbcecd0300a120f75822d13a24b8d3111c52c7f2b9cb  check-1-census/guix/raw/guix/service-provenance.tsv
e4c33a4bf7bca181fece87485aa3a9e3ac7170c9b35ea5f9edab9a4f933877fd  check-1-census/guix/raw/guix/service-source-paths.txt
2bcff7c679126829c28c25e9ea13d89e6fe09223134c74846f679ac4968d41e8  check-1-census/guix/raw/guix/sha256.txt
aae5417544ea9136f69fdf7878ac5526ea54bdb982b181327b82363bf3e0d5cb  check-1-census/guix/raw/guix/shepherd-probe.txt
ba8d458ca61cb85f17d34bdcda6d09679888c3f0602c87ea80a03413732a162d  check-1-census/guix/raw/guix/shepherd-timer-log-cleanup.txt
7a8e3ea7c0f378cbfe18e46af66f7cb6e5ad462258687e81ee6d4ee26ea019bb  check-1-census/guix/raw/guix/shepherd-timer-log-rotation.txt
a3a4d75008d2c26d66c25883f8a389b74d0e465602f6b46b9e3fbecaac0f8288  check-1-census/guix/raw/guix/source.txt
139b3e22c448ee2e19a5affa8651bb969152e1ccfc703c560f2d928b74f905e0  check-1-census/guix/raw/guix/store-outside-system-closure.txt
f92f4160fff6f9c4887e4c6ce6f589275963eb6d5c1e7f85eb7e592d07ed6fc9  check-1-census/guix/raw/guix/store-top-level.txt
0c9fa695b5054a71e04f15c3c53c5205e27c3b255997ebe57151d557c1b74a77  check-1-census/guix/raw/guix/supplementary-provenance.txt
a6eddaeeae9c105fb723ffa77840d5f5be877fda1a5a64a08d8b1afbb066d07b  check-1-census/guix/raw/guix/system-boot.scm
409f2b3ff73926a99ff357c24790bf2dccaef5054a73df58391709e6c1d5c59d  check-1-census/guix/raw/guix/system-closure.txt
0b7ebfb365332db85816d02d6c1736ffbad49450029702bd6f9b45362197c8a3  check-1-census/guix/raw/guix/system-config.txt
612cc8eca3291f75866c11a262103ce51ead1f46b78379015637223455da73f0  check-1-census/guix/raw/guix/system-generations.txt
ff63e29e92cefc0db7e6f3c44685fe4235e01c34fb02964e4c08500dd20c419f  check-1-census/guix/raw/guix/system-profile.txt
c856e5e9cb8b7cb7fea932ef83c674737ffc62403b03c435b02ebb994aba6088  check-1-census/guix/raw/guix/system-service-members.json
7777469b92465e1846f240847d780f469be1517ce0d605b38c961c76e92ee088  check-1-census/guix/raw/guix/time.txt
e02b698170f4ee1aaa5e84f891684447f655c656db74e55431f961f3451307aa  check-1-census/guix/raw/guix/uname.txt
1ce8a6b97c8c1adb388c2a61862e05c7a7b2a4d711015343acdfedf4144c1682  check-1-census/guix/raw/guix/unowned-groups.json
2318b9b764571ad480e3b41906f2d38a5bacca9cbb3a942f86a0820893c44e10  check-1-census/guix/raw/guix/user-closure-outside-system.txt
c9e12dca3d681f48c5ad88ccd6bc36210ec5b5bbc43f5700ad811ebbad555c68  check-1-census/guix/raw/guix/user-closure.txt
73898c5e75d596948871af7005b8f922c6b44f6c11ffc73652fba48179d8d1c7  check-1-census/guix/raw/guix/user-generations.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/user-herd-status.txt
56afa5bb50c9f753a06bcadb5070af0c77823769ac135ab8d2a3bc553dfbdacc  check-1-census/guix/raw/guix/user-herd-status.txt.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/user-mcron-schedule.txt
56afa5bb50c9f753a06bcadb5070af0c77823769ac135ab8d2a3bc553dfbdacc  check-1-census/guix/raw/guix/user-mcron-schedule.txt.stderr
9c3f4c41f95f3ce38ca507b34cc8628118b09c6de8669b1749e388c8bfcd7104  check-1-census/guix/raw/guix/user-profile-support-outside-system.txt
2b178075a37bc68f6c85b192895c3c0bcc70641212315f646cb2463f9a538e96  check-1-census/guix/raw/guix/user-profile.txt
37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570  check-1-census/guix/raw/guix/user-service-members.json
bb3a78eae7659b51f0b4be4c7eb3b970c317643e7b88ac8c311322ff57bcf60c  check-1-census/guix/raw/guix/user-settings.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  check-1-census/guix/raw/guix/walk-errors.txt
a3b5923f0cdea123001d6d8a87fd6ae7c39ef67c83e2a5e45cb203b7bcc6acd1  check-1-census/guix/raw/guix/walk-roots.txt
f19c7d18eb655318c886e89fe506d75e1cf4b04cde83e8337287752dafb2b18a  check-1-census/guix/raw/v3/disagreements.tsv
a11f6e8b27b2ecbadb7d54c19b4afd81ee26eb6912f2a0fae951281486a9fe52  check-1-census/guix/raw/v3/holes.tsv
b6f3f14fbb0d0120b11e514f44f1b183ed29828e54f987516b9ad131098925a4  check-1-census/guix/raw/v3/joined.tsv
04c47e3d214d424aadd26721104a4078acd871df7dbfc4763060ec468805c36c  check-1-census/guix/raw/v3/literal-disagreements.tsv
1a202fcc8151001e951c4ea1ddbcee6934a666a0ecc1fa2e48c4f9dd3661d4da  check-1-census/guix/raw/v3/owner-disagreements.tsv
ef7677b1df49292ea654ac54f369d01d9f16e16121ad3c37ba1d2b837bf27cfa  check-1-census/guix/raw/v3/stats.json
cd3754d1248e945cd3129ed7eaff799c51276351314ca88d6233a25a2717cb1d  check-1-census/guix/residual.tsv
51f6c8014d77aff7b73a058f0cc16006f2f6abe6dc7b3a7438d66287e9fc0dcd  check-1-census/guix/supplementary.sh
a2b8a79cb8762fffd012e2a7843b68edfb7a8807001b0e27dd22258e3da8ddfe  check-1-census/guix/write-outside-table.py
131a4dfc66a12996c36b2d130a575c59f5ac6e757e16f28d3b695404e10fcda2  check-1-census/provenance/REVIEW-X9.md
daa977a9321e636c0f7e536d1c800c2aa5a746ab94fd455d66d94785ba97d7bc  check-1-census/provenance/X9-STATE.md
74ad7e775b18c3eac072120941f9bc76e9652f15865c6d4a777cf1793f4f7fbd  check-1-census/provenance/X9-analyze.py
5dd72e42cee305d4b90e465dc067d54ea4987586ad37373e59c610bc204f2df3  check-1-census/provenance/X9-paths.tsv
8d0bf6f398b4aa5e495a7243a17286cc22bb7ab30fae00431600c69c718314e2  check-1-census/provenance/raw-X9/analysis.json
b2783d6ae50a86931f3ef938a7ba21564d90000c3115faf96761d8985f2fe20f  check-1-census/report-check/REPORT-CHECK.md
b1893bdc6d06103d3d8210dddc0c896eb9012ddcdd2ab8d0428ad03e3aa3acff  check-1-census/report-check/REPORT-FIX.md
179c155eac6fd7b87fa47e409450861f622c88a084c48051f5a2d06faa625dbf  check-1-census/samples/arch-silverblue-freebsd/REVIEW-X1C.md
1b21e28b3d6c1a9e886397735fdd0ee070e4eb9c621c12f8e638092eee279d6a  check-1-census/samples/arch-silverblue-freebsd/X1C-RESULT.md
90b35bea88a38d9a40644bf58bb88b63ceef6a8f11a213d0f89305d403e8db9b  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/compare.py
1d4c3843030a67d7657eb8f73af8ee2922eb5655c2f2ec579387260de0dc8bf5  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/disagreements.tsv
0ee35f947c5f635315d558c6bc3c8af64ba8abecea1b3774122b2bd237601c8f  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/holes.tsv
4969f1214a3ba8bdb4ec55f8404d35ec89db320c695173fa36f87cfc9f330e06  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/inputs/X/X1-c1-classes.tsv
e18e137fdbbe8fe3e06359d7c68bf8f428b7f866ff1de1e02a172f2813d45fcd  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/inputs/X/X1-c2-classes.tsv
4680701a7eb006ef68e5e2f7cef59e9cb20ffb4aa21f6d6f76be6d688728320a  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/inputs/X/X1-holes.tsv
3d453384f63019efc25563b41b0895abf64140c10e24d75a6ed6bc50693f76b4  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/inputs/X/X1-residual.tsv
0a5c15c353b21b73dac8f1ee4b3ec7b6d83b9eca922be9689522a9cd1fa2aeab  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/joined.tsv
8686d09b090ff571c4b0350d0282e9462b1cecf0b8eeb624292883ecd65b8622  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/metrics.json
5ec4a0a0cff5df619322dd5bf6029b92a43c882d5aa7f3bc141a3db85ec3fb77  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/section5-quotes.json
59ae7a537383c117ad52a67fc1e6ab91677ed820f6707058d13153e82eea85b7  check-1-census/samples/arch-silverblue-freebsd/raw-X1C/validation.json
3ff888ee1c4d70aa0f9af0ca3955b983090a5164f6ffe71496fcddb02a15defa  check-1-census/samples/debian-desktop/REVIEW-X2C.md
02475b4fb8a1b4156e2b6ff8cc1514ab22ab95acd79a8dc4f68e8228834f638a  check-1-census/samples/debian-desktop/X2C-RESULT.md
7259c1332b1e05b5a9195f9ec469f6b84a8bf3a4df3ba76963574ae32eacbc20  check-1-census/samples/debian-desktop/raw-X2C/compare.py
6e2b649211a6355a3218b6e9619b3c556db0bce680a88b93c2514ed90464c920  check-1-census/samples/debian-desktop/raw-X2C/decisive-evidence.json
5d8b85020a6622d631071dee614ba0bf70e506ae052c33f525ae605db3f39ef7  check-1-census/samples/debian-desktop/raw-X2C/disagreements.tsv
76d410417f84910e1e6fa3122a5dcd973acadba32f0320f443cc5c334806d73e  check-1-census/samples/debian-desktop/raw-X2C/holes.tsv
bd1bbe31ba72df4e8f7f33ace8b61fca8623e3e9caf508f2799a1acc3964f099  check-1-census/samples/debian-desktop/raw-X2C/inputs/X2-c1-classes.tsv
b3376651360185a892b37c61447ae4a2b1d4380a770a0c49ee09bc94af161645  check-1-census/samples/debian-desktop/raw-X2C/inputs/X2-c2-classes.tsv
fa32edeb8f2f8c7794e8dedbbfc40cb1d5e958057b19ba1b4966b8b8c7a8d278  check-1-census/samples/debian-desktop/raw-X2C/inputs/X2-hole-register.tsv
7b36d2e946de0495ef5ed285ec37a451f0e9fc6fe9409dd7fe60db20146b109a  check-1-census/samples/debian-desktop/raw-X2C/inputs/X2-residual.tsv
92972d940298bb0daba3219e168beb81f500fbd30588a40822d44c528b511074  check-1-census/samples/debian-desktop/raw-X2C/join-integrity.json
a7a4d5a3923f3b76305b798a6ebe2b89a6a3fe728089000abc354ac729275dff  check-1-census/samples/debian-desktop/raw-X2C/joined.tsv
d25636eaeaa9126babd8289deb76da532353b07f35d2e02054b946b3d66fa2ea  check-1-census/samples/debian-desktop/raw-X2C/section5-quotes.json
1d1a1d82bdb7a42bc52a2d81bfffd407c386470a8d288a63ceae7426552a7ad2  check-1-census/samples/debian-desktop/raw-X2C/statistics.json
1a9c27d166d012e81637da801694eb0b39aafd0551d1488d21af74e664dfb5fe  check-1-census/samples/ubuntu-alpine/E6C-RESULT.md
7456c3afb866741b37338635449f104bceb11417de6034a73e425137e189ac7d  check-1-census/samples/ubuntu-alpine/E6C-compare.py
216a750f732b95c375c3672a30a1e252749a0e9524a5847dc168f8afbed63b99  check-1-census/samples/ubuntu-alpine/E6C-coverage-gaps.tsv
21a9e70b7a1ed18e17590fa9a0b9b5ea32a32db61018fe69656ee017e187a192  check-1-census/samples/ubuntu-alpine/E6C-definition-audit.md
f0fe9a237e50d22d6ec205934f067d23fbe70d753f292fb481dbd71df7ad3c85  check-1-census/samples/ubuntu-alpine/E6C-disagreements.tsv
9239ea745dac15ed0944e1266c616312820c32922b1053fe62cdb36d2315c66a  check-1-census/samples/ubuntu-alpine/E6C-holes.tsv
e20c2c87d8b16b53062c8cd3e5b8166186fa581a22bfce4a23a4883d81c2fddb  check-1-census/samples/ubuntu-alpine/E6C-joined.tsv
5c9c41a2723e026af91ed34485036649c89173017945dabe59a95ebabdd94653  check-1-census/samples/ubuntu-alpine/E6C-raw/input-sha256.json
8acfb58718179b4b8eb9d183e2fb76e8ec1366fe40d975fe5529805093c5f994  check-1-census/samples/ubuntu-alpine/E6C-raw/inputs/E/E6-c1-classes.tsv
750618c18879f06110568daf2441655b230cd499eb6cc23730c303d56b041c38  check-1-census/samples/ubuntu-alpine/E6C-raw/inputs/E/E6-c2-classes.tsv
2a6e66e1b926379fa2dc41b77a959313d62e46d2f48838aa35247f1bc75d21b0  check-1-census/samples/ubuntu-alpine/E6C-raw/inputs/E/E6-preclassified.tsv
3afc19115326b231110a9716338a5b8f499a55d264350de1d1039358e1a40987  check-1-census/samples/ubuntu-alpine/E6C-raw/inputs/E/E6-residual.tsv
1fe9af38bf89d1a2a75277d3bf9b40b56f82639eab5713c65440a10186f04db2  check-1-census/samples/ubuntu-alpine/E6C-raw/inputs/E/raw-E6/holes.tsv
ba90f4a596e414415cd065793cd9e05f97a957491ff6a177b195e796ee68f1cd  check-1-census/samples/ubuntu-alpine/E6C-statistics.json
22f852e4e64e4ec2305a9842b7ac00f5265e03553de163717136a3aa633f7a68  check-1-census/samples/ubuntu-alpine/E6C-validation.json
35bf5dcc8bb6aa5abd518300e37351c4c2075c0fda157596dd6376cabf7b3590  check-1-census/samples/ubuntu-alpine/REVIEW-E6C.md
c8203755dbdbba5aea12bbe73d968875dba860943d55979f6a9bb3af5fd25624  check-2-law/channels/RESULTS.md
ae60cb8fccad3a6556027625c3589776c57b712227612b5803c1fad6776ddcfa  check-2-law/channels/REVIEW.md
315020096296091918326ee5326d60f0a5eedd0a90369ecd00ee39f6aa979fb0  check-2-law/channels/raw/d2-classified-results.json
2ff9226a18c0b558171c33765c326a28408a97da94680cd67a6313f6ab074935  check-2-law/channels/raw/d2-nixos/final-evidence/audit.txt
a30b4c84bab238be5fb9d7c6aa31b3d86b11e2b08838ca18715e2c6b8a973d85  check-2-law/channels/raw/d2-nixos/final-evidence/markers-and-network.txt
a4faf015c86ff089893eebb6a44033441a10035eff7a603dce281d77407a29f6  check-2-law/channels/raw/d2-nixos/results-adapters/bash-env.json
6d5fc665e8f64a6319ff9aac8f0f3ca3a26f5555ea71fceafa7986394a8dd427  check-2-law/channels/raw/d2-nixos/results-adapters/venv.json
c742517dcdca7cc5072555a6ed4c24fec902d78a398a8e0bd8107b26c674f4c3  check-2-law/channels/raw/d2-nixos/results-browser-retry/browser-extension.json
64d2d2e57cb9f598d08ff3da235d766adf7164fbbe3c70cfdbc709de15fa82cc  check-2-law/channels/raw/d2-nixos/results-browser-retry/native-host.json
d37c49f52e1f1a20b668fc02d9b7c17d3c81fd6992d9a61916a5e0ec019d9498  check-2-law/channels/raw/d2-nixos/results-browser-retry/network-browser.json
4abd09e50aea6ac3667b98ccff03b4d8ab53e71a3584f0075f5172fa777c61d6  check-2-law/channels/raw/d2-nixos/results-extra/continuation-revoke.json
07340f5ca04b0bfa794e230dfd8d41814f722871195aca80ab2bfa562726551f  check-2-law/channels/raw/d2-nixos/results-extra/cron-final-observation.json
e721101888dc9f5678aed1a02c941dc11474eb4c7cb797d5e25de6c1a3e1a614  check-2-law/channels/raw/d2-nixos/results-global-profile/system-package.json
8fd64c2cb20bde2d8bdc6a33529bf6481232042a3560f1eb1ced983cc971240c  check-2-law/channels/raw/d2-nixos/results-install-proof/npm-runtime-prefix.json
6b9e192bdbcb85ab6b66a7c4a4f29e7cc056c687d1d1d889e8807c00c9847a52  check-2-law/channels/raw/d2-nixos/results-install-proof/pip-module-user.json
104f23815f8804768a18f77e319d0ef56e747f14d448a875d46f1232d38a30be  check-2-law/channels/raw/d2-nixos/results-install-proof/pip-target.json
93eef42807e0cb12b34e134d134baa6ce28fe9798dff644099e5207d4f60b1f1  check-2-law/channels/raw/d2-nixos/results-library/library-path.json
5c53208692daba5c6dbd0216c4eafc6d7cc9b062962b8af912a98d01ba316a9c  check-2-law/channels/raw/d2-nixos/results-linger-final/systemd-linger.json
b3c898849897685ca466ddb9cf6010f64756d34c18d83cc6557dfbf8bdcbca6b  check-2-law/channels/raw/d2-nixos/results-main/archive.json
c9e8f69611589d5fe4b4262fb92df6fa5daaa0e5611d86e3f22789b9ea5e21c7  check-2-law/channels/raw/d2-nixos/results-main/at.json
30df467b58e044d7d33eff4007d346119190acc528ec53b84ceffb2eca549a35  check-2-law/channels/raw/d2-nixos/results-main/audit.json
a36f04afca86c7be9c200ff4acc8bd0746724b60d84ce518432a4d5a176264de  check-2-law/channels/raw/d2-nixos/results-main/build.json
5b6854607a4e94337bf6f670ef37ec3c022b6fa8675eb8f7b763e8f765351772  check-2-law/channels/raw/d2-nixos/results-main/bwrap.json
1736cef69b14e9de6092ecdc35928463108373f26d7ec02ac0c62e001ea1ee1e  check-2-law/channels/raw/d2-nixos/results-main/cargo-home.json
39840d386ed3b0c92ec32eb1c2f84f3078ef7cfc8d81beb3a9848098ebfb19c8  check-2-law/channels/raw/d2-nixos/results-main/cron.json
e7945f24205e4a8b3ab643529f3a05a6523ea9ea7ede6d2215972047a99dc0f5  check-2-law/channels/raw/d2-nixos/results-main/dbus-activation.json
bc8eb757baa29966b9a2937cf6a951ee579919a57039e7f7505a82047a7f18d5  check-2-law/channels/raw/d2-nixos/results-main/desktop-entry.json
40d77c26f290b2140128bc2cb4b4509fb590da741257812dc680bda06cada77e  check-2-law/channels/raw/d2-nixos/results-main/inline.json
b4bd5838cebf3a9a19c3c4f9f451ef9e8341ecca2a14aaefbe6135f007af860a  check-2-law/channels/raw/d2-nixos/results-main/ld-preload.json
c0bd0d9f31802ff5dcbd977641c795b9b783428938a11968f6d9476a4b69a971  check-2-law/channels/raw/d2-nixos/results-main/loader.json
733ac7b4111079bb857cc206b67589dd0a736f52d8ee5eada85f485a8e8548ce  check-2-law/channels/raw/d2-nixos/results-main/native-home.json
5f9fa4ca6ad103b84f1b682a69a73d58c1996d9f745fec6af821f028274ac7d3  check-2-law/channels/raw/d2-nixos/results-main/network-native.json
fbcca971b3191edb733df8fde22bfa042ba36a2c2266a6655d8425c72144d421  check-2-law/channels/raw/d2-nixos/results-main/network-shell.json
4b600f810c602284e1ff082309b3125ad6f75602873fea4b350b0b0e1d9893ca  check-2-law/channels/raw/d2-nixos/results-main/nix-env.json
583c5b085929e52510036a0200aefd5b1fa49c8c5271de3354cad0f49c7b36b9  check-2-law/channels/raw/d2-nixos/results-main/nix-profile.json
e99888cd7107016529a0f764e14c9c027a57d32b0bd0a53e79a952b82125a8d8  check-2-law/channels/raw/d2-nixos/results-main/nix-shell.json
dd0c5d717df533fad629ae9504815aa39fbbc6b80f1e094f9fb15c4be48d5e53  check-2-law/channels/raw/d2-nixos/results-main/node-file.json
1dfeaa9d63003ec86dc4b54e48c5492bef96ac4204f7faf8bbde7e324e58c1fb  check-2-law/channels/raw/d2-nixos/results-main/node-options.json
5c731280fc944546eed054ffe3c31f794d61697b37d13317d744969f42374dd5  check-2-law/channels/raw/d2-nixos/results-main/nohup.json
0643b025d254043708fa0c59039c749e29f30639be646a305bd1c01b6f7fa239  check-2-law/channels/raw/d2-nixos/results-main/npm-global.json
3b77fef43d3107f1e66970dff270ab2b844d64e5cacc27bd8e9779084c5a2a43  check-2-law/channels/raw/d2-nixos/results-main/npm-prefix.json
d4bc0c86323ed03b653d103f1367ec88c6bd9792c2053bf7a209a0dbbd185e43  check-2-law/channels/raw/d2-nixos/results-main/path-home.json
45badd511548cf0c2292a7e462bb57505e755d3c3a550fc6027fbbfb0c89aa9b  check-2-law/channels/raw/d2-nixos/results-main/pip-global.json
62892e962e3dc7ec74cad9cc59d0b095888692c6f2ca1d152393007a7cee0495  check-2-law/channels/raw/d2-nixos/results-main/pip-user.json
f11503dbdf2843c3fb382b2764a7b707baf2cf1a4dfd48051f17fc6d3e51bc23  check-2-law/channels/raw/d2-nixos/results-main/podman.json
fb79228aaba27310d311e27aa368ab2e5ab174e46ff235dc5fbc1c6536daf7a0  check-2-law/channels/raw/d2-nixos/results-main/python-file.json
211b8d61311a16b466f81c07bbd8940670baf5ed8420c44874572dad59e93ff8  check-2-law/channels/raw/d2-nixos/results-main/python-inline.json
33ec0016a82264b0d3b4398f91afa3d155f18c8eac4d5d6c85a5fe5d5b8bd60d  check-2-law/channels/raw/d2-nixos/results-main/pythonpath.json
75406c3df38e9cf4e7f678915740052ff7d8c5bec850a26ef1e242f51bc91613  check-2-law/channels/raw/d2-nixos/results-main/rc.json
669df5b13ae2bfc3f26d3196e7939bb93b77a99c462c07c4f930f2a219898a85  check-2-law/channels/raw/d2-nixos/results-main/setuid-existing.json
88521fe1a273ed49c47c7d2312cd1df6fa32ab139180cbc7404403db87fa6efc  check-2-law/channels/raw/d2-nixos/results-main/setuid-own.json
b1bb997272f4328d26c71dc7afea1a3fafe8daa1655e67b919ad3b6521021b2b  check-2-law/channels/raw/d2-nixos/results-main/shell-disown.json
5961e5e41555b5464846d8b5a2aa4ef4afe7405b2a3737e683c3dfb8ec56d8a4  check-2-law/channels/raw/d2-nixos/results-main/shell-file.json
a8e8194dfbf3b7eea4874d5ace7385e614a5cd4ecc65db833e1a89e4677b63c1  check-2-law/channels/raw/d2-nixos/results-main/shell-login.json
2b0d5f5a0d06bc5b240516145e53f7502a843120831f7c5840c4b101b1bf8784  check-2-law/channels/raw/d2-nixos/results-main/shell-profile.json
e019de9fce8ab338f8a01279090a8417893263075fd7cfc6c64b379a76c1ef9c  check-2-law/channels/raw/d2-nixos/results-main/sitecustomize.json
e72a25850c1e37679dfdf78a6da0a65ae193b8dc837fb4a0a5b5d9f23c15437e  check-2-law/channels/raw/d2-nixos/results-main/ssh-command.json
9e2987ad84198e1122309fdb6ff760ff545fd9d9277b7ac8eed6775a1417c1a9  check-2-law/channels/raw/d2-nixos/results-main/ssh-rc.json
ede5e74cef07d33c889e22db1bc5cb1af4ccfb407f3e752d3c0b9d4345d0cbb5  check-2-law/channels/raw/d2-nixos/results-main/systemd-path.json
c1f4f2ff26bc7e3c2aa458bf1f8dc5151fa49aeab145bea41ae5c7f14fbcc71e  check-2-law/channels/raw/d2-nixos/results-main/systemd-service.json
820d43e8c90dafe687d2b7d5024701a3ca7e6b52b87695bee8d38a9976ace0df  check-2-law/channels/raw/d2-nixos/results-main/systemd-socket.json
9f33eba4873ea1c08221ea7aa22fc59274e08922ae711607b5abfa45f65af170  check-2-law/channels/raw/d2-nixos/results-main/systemd-timer.json
c77fc401da06d452beee0613c256f2445bec02c0a802e8e872f85b14dac337b4  check-2-law/channels/raw/d2-nixos/results-main/systemd-transient.json
645eb093c09996a575a5f66ba054564c74bd236337bb4aaabe15647cfa034324  check-2-law/channels/raw/d2-nixos/results-main/tmp.json
cb969eaa0b44f7ecc708f65ada47c57fde8f48bf270f7b01e88362fe753b031f  check-2-law/channels/raw/d2-nixos/results-main/tmux.json
75478ecdd709a0bc24d91414a4d8c344d5335f2a811217fc725eb62cff831dbe  check-2-law/channels/raw/d2-nixos/results-main/userns.json
fa7273852757f4a51b36748ec9a620cbc5fa496fd5e8935075c42a04b281cdaf  check-2-law/channels/raw/d2-nixos/results-main/xdg-autostart.json
710a1637307cd75dbaa13d76ee37c34e011cbedb8a6e325f1bcec60da0324500  check-2-law/channels/raw/d2-nixos/results-packages/appimage.json
9d1b30a78dd7aa949cab494485ef4293a8dbc78c67ed6a287336bc777cae46d3  check-2-law/channels/raw/d2-nixos/results-packages/flatpak-system.json
81a99da9c5ea5e48a790b8a4f482b7490e94b129950781413bec151fc1ad7d3f  check-2-law/channels/raw/d2-nixos/results-packages/flatpak.json
d3ccfb5da77cb6042a467572fb040185e29dcedead7a73d162afe5a32c7394c2  check-2-law/channels/raw/d2-stand/final-denial-observations.txt
ddcc23974498561501c07d1175019e9af2072d560c6f22457b5d14ab7dc69e0e  check-2-law/channels/raw/d2-stand/results-browser-retry/browser-extension.json
115e278c4d696174ab0db39aa4d855ff4e865ce936950d08bba0734e82c5fa4c  check-2-law/channels/raw/d2-stand/results-browser-retry/native-host.json
6c0ba0d6a80503d855be9796142621555915e229ab716d9106e71cfc927283af  check-2-law/channels/raw/d2-stand/results-browser-retry/network-browser.json
2c275acd0e123b983de1e635599a235e1df1567e8ce319c1150e52703652e17e  check-2-law/channels/raw/d2-stand/results-extra/continuation-revoke.json
2111ef334946c339943ce98f1e70966ce41fd2586a04b55ae320abcb50154676  check-2-law/channels/raw/d2-stand/results-final/archive.json
5d40adf725cc7d7d0e78947486d70a6c85a5352ac41c1096820f877300bae52c  check-2-law/channels/raw/d2-stand/results-final/at.json
fe94a23e69cf98f330f68b2c8d6dc4dfff28a06ca365729a8c3fee3efcfd5e23  check-2-law/channels/raw/d2-stand/results-final/audit.json
9001d0c92db471d865c90a41ccee0e408e47f839f87acbdf74b056c1f3333f65  check-2-law/channels/raw/d2-stand/results-final/bash-env.json
1c664c7e048e98ab0930e9ca89493311f22590319aa4d6509bef22f6f67119bd  check-2-law/channels/raw/d2-stand/results-final/build.json
d1d1d70476bd081fee00eff14a4fd52cc13e798469b9073e7d97833e1019add7  check-2-law/channels/raw/d2-stand/results-final/bwrap.json
55818d39a2ad528f70e4b27842ab35a673d6a031bde0fc570f826ddfcb394a94  check-2-law/channels/raw/d2-stand/results-final/cargo-home.json
d762b608970876081785c8e2f8173e8f7ce27b4a062263d3fdd814b25dc09fbf  check-2-law/channels/raw/d2-stand/results-final/cron.json
42b95292b6a1567ed902bf67e112ec5de902d6024ca0d80fb34a3ee760ab4e70  check-2-law/channels/raw/d2-stand/results-final/dbus-activation.json
fbadd96b3732ec0632f62044d2e9565152891884a09c42b695c5dd1fd6940538  check-2-law/channels/raw/d2-stand/results-final/desktop-entry.json
dba0e9a54b07d0d197679be6ddcf05e49826facbde4c3c635f3c5ff1d215b1ce  check-2-law/channels/raw/d2-stand/results-final/inline.json
ab5f4e8648fd7feb725e58f3db7d47870a9c7b2108285763d80578446d5cb86a  check-2-law/channels/raw/d2-stand/results-final/ld-preload.json
056e8e5c947f161c9b55ae49a1bc083502a5f1f6712ea1c2c390af4282401148  check-2-law/channels/raw/d2-stand/results-final/loader.json
17eb62f29799a95e06b76a8945ebdeeacb210ba3e130ffeaacee486af98e194f  check-2-law/channels/raw/d2-stand/results-final/native-home.json
ac91f36638874c80bf7cb7498a3f9e987ebff3796eca1697ba5506a539a11734  check-2-law/channels/raw/d2-stand/results-final/network-native.json
99ce966231445334bb384db653de27e0ab99bed5cf38cb2e7ebbcf309057805c  check-2-law/channels/raw/d2-stand/results-final/network-shell.json
35f1879c56931b83cef6aa4d687adf5127743f42812ae55529df6f6532a112fe  check-2-law/channels/raw/d2-stand/results-final/nix-env.json
0d820659efbe758aebbcfb44439f0f8849d370602768897aab8e83e8e098263a  check-2-law/channels/raw/d2-stand/results-final/nix-profile.json
3ab3fa813d1e165b4bd0b51024d2bfa0817c75f7b6756150a1bb6d2bf453b45d  check-2-law/channels/raw/d2-stand/results-final/nix-shell.json
0b99a9ae5dd704719829abde8a994d945f917e700382cb72fc8557033fac1945  check-2-law/channels/raw/d2-stand/results-final/node-file.json
2d243aa7e55b37c26001fa57b82bc4cb69d1f057edbf53ed6c74afc0306d8ea9  check-2-law/channels/raw/d2-stand/results-final/node-options.json
f62b4fc70e218b6b2d08b652408c5c051fef88288cf5ca6652bd6798ecac6c9f  check-2-law/channels/raw/d2-stand/results-final/nohup.json
01e371d1b568fcea252221d21cdaa04250922181fa18214adee4a79106765535  check-2-law/channels/raw/d2-stand/results-final/npm-global.json
1d03abb88969d6ccfaa38d36cb3c0a7c1bb9b06bb46c34367989dad020bfce9b  check-2-law/channels/raw/d2-stand/results-final/npm-prefix.json
4070b8620517db392eb96313565be063e4b3dd38bdb1bdf245647df199ee3020  check-2-law/channels/raw/d2-stand/results-final/path-home.json
7fcd372164312f08fae075549d8b2fb2dd220ab4edfd16fef090b92f3799c517  check-2-law/channels/raw/d2-stand/results-final/pip-global.json
6acf544b8b78325da1527ff3d6d0953846281bf6f80cc85f5912ba77fd60f68f  check-2-law/channels/raw/d2-stand/results-final/pip-user.json
3ea572875be6518a3b88c16256e5d3f29273da675b4f04b326cced0462f5ee38  check-2-law/channels/raw/d2-stand/results-final/podman.json
dd994c28c10f11902e298fcf11b4aa37a42bfa2ee70d57398580304dd82da800  check-2-law/channels/raw/d2-stand/results-final/python-file.json
d8cbb656c21fb3310a11ccf0c7135229c11d3ff7dfcf509f4bdf871497283176  check-2-law/channels/raw/d2-stand/results-final/python-inline.json
94d646baedf720cb6dd6b7e96b908a65b2913936f8d44c80fa7999da6b1285ea  check-2-law/channels/raw/d2-stand/results-final/pythonpath.json
450a68d9e6832c21ab7a9371028697df0d44130e76e18f517aac79f4c6199971  check-2-law/channels/raw/d2-stand/results-final/rc.json
70a72f0b719a99dd0e528d824aec9c45980c400c8430b33e284c6d66b8fce50d  check-2-law/channels/raw/d2-stand/results-final/setuid-existing.json
c2ed649bb0da1deb65e7223db976297bc84f35c925013464790f7a8fa714a70b  check-2-law/channels/raw/d2-stand/results-final/setuid-own.json
d0b7a69edfdbfd889860ce598d7bf9bbcff2d794f666f4154b101a98a25f54e1  check-2-law/channels/raw/d2-stand/results-final/shell-disown.json
06c1af13d3b063ac762bb2735c67fe9bc43b074a04ea3dd83d2325d789d07b01  check-2-law/channels/raw/d2-stand/results-final/shell-file.json
6a696fc88f0acee9ceb8af5055d918621601334fb3c74f841c773acacd5c402d  check-2-law/channels/raw/d2-stand/results-final/shell-login.json
0ba54636202aad8ef4ec3a107459d58cbc691ebde7305099c2ca2bee06d225ac  check-2-law/channels/raw/d2-stand/results-final/shell-profile.json
e8f17bc0261f277bb5d1961dff0d643c71764f4ef9897248858bb21a6c518b41  check-2-law/channels/raw/d2-stand/results-final/sitecustomize.json
62b1a831b29c26d823e665cedd1131a4683e88c5c6f9745b62e6ae9e1f4e9e8a  check-2-law/channels/raw/d2-stand/results-final/ssh-command.json
3eeba318e8f8caf44429d3b26ff5d7bd372fb66594267b66c1602fb1972c74c6  check-2-law/channels/raw/d2-stand/results-final/ssh-rc.json
09d038fa4d80cd14d2771ed571fcc68cc46bca672ca7ba4084a0a4135e73b790  check-2-law/channels/raw/d2-stand/results-final/system-package.json
5de4b67a3707887d92de94a03427d47d445a01a01ad48b4e1fff7bd37bcb329a  check-2-law/channels/raw/d2-stand/results-final/systemd-linger.json
68f260858564f00ce6ccacd5c4c1782f82868fa6b528a78570049c21482be7a9  check-2-law/channels/raw/d2-stand/results-final/systemd-path.json
ec56c7093287c9504dc224aec23b2cb39c0616c5464f8f11178751381b1de999  check-2-law/channels/raw/d2-stand/results-final/systemd-service.json
16d2d6dcd7d483b093e5d635efc280b095e761e85b47d65ddba1708e16b9bf1a  check-2-law/channels/raw/d2-stand/results-final/systemd-socket.json
ae4a88fa2f3fbe854bafd1f4366a2bfbce987e0b0f27750bd9b4ff44dae60e9f  check-2-law/channels/raw/d2-stand/results-final/systemd-timer.json
714bd4179126ae2301492663e72fbafaf7d31d76a7d6caab0b13af91b2eb62e4  check-2-law/channels/raw/d2-stand/results-final/systemd-transient.json
cc7ab03655b804bccc68a31a2cd38aeed4b8d56fc335652dc32a1f601bb9d418  check-2-law/channels/raw/d2-stand/results-final/tmp.json
b96b35ecc5339000f8dbb61c835fd50f09a499dc49a207803b7b28e1f5567f4f  check-2-law/channels/raw/d2-stand/results-final/tmux.json
e785cfc050b7999bf240fbb1d34fb2f2168bdd1d8f71bdd177a0a72f3de3bd91  check-2-law/channels/raw/d2-stand/results-final/userns.json
29e0818a5520661e7a5456aab25c9c1e33e23af14c967bece97bab812fc50497  check-2-law/channels/raw/d2-stand/results-final/venv.json
a0772d18ebcf95c7461343eb9c6bf28652097f108db6f6d033eaabe89085bc2d  check-2-law/channels/raw/d2-stand/results-final/xdg-autostart.json
d8e3b7332f267fbc63a52e3198ef3f144f9eab315245d9e5117a854fd0e4725c  check-2-law/channels/raw/d2-stand/results-followup/appimage.json
f4bfe860bdb987bee8c3280eadc5da605a713aa0fd7ab27e3e4abe41ac9726c6  check-2-law/channels/raw/d2-stand/results-followup/flatpak-system.json
eaec2b365e2af163473a642da484cd9fa82bb0fa52df7774537a2eb1d2d8aac2  check-2-law/channels/raw/d2-stand/results-followup/flatpak.json
63a1fe0e30ca45b694a5603a0db8e2279ca48e0787eaa0d408c100339879d801  check-2-law/channels/raw/d2-stand/results-followup/library-path.json
99c73186129a00ff2f3f5ac0f8060e57acaeedc58773bfe1ebd646bbd301f907  check-2-law/channels/raw/d2-stand/results-followup/npm-runtime-prefix.json
d075873e8c18c2c4a26e55083a146de00b38af04fd89d62a7df6f8d3c11456a1  check-2-law/channels/raw/d2-stand/results-followup/pip-module-user.json
631aadb56a1a3f4f1b6f054b9a1d2515dd2915f36eff939eab03902cd379c552  check-2-law/channels/raw/d2-stand/results-followup/pip-target.json
bfc1cbf999c2dc01bb7885faba0ffa1ee58e08da365ac777c7d0b52135db960b  check-2-law/channels/raw/nixos-setup/configuration.nix
3bed0265cf4258c40910521be2a4159f9c2331e906d3098d8d1ac649d8bef03d  check-2-law/channels/raw/nixos-setup/hardware-configuration.nix
99cd780dd0547d85ec6093ec440922da0eb6f68f4a297185ee8496958d8a83ff  check-2-law/root-signals/E2.md
5a8473e165f9c328b5aba396edfb509503fdf447d43f6bf30c285242be4760c0  check-2-law/root-signals/REVIEW-E2.md
aaa20e0f74d80e138259aea6720b696264f1a1b4db20dd85da21782d72b06f7f  check-2-law/root-signals/raw-E2/analyze.py
8c4d3c76cc198163e90f253fa2ca9c9793df14bbdf08a80d3383e50998fff300  check-2-law/root-signals/raw-E2/commands.jsonl
ecf9eca507025270786ea0785921903c69ed58d9749c7b0d81c298344a80508d  check-2-law/root-signals/raw-E2/event-index.txt
e18e0c62b38da4add5eae2bb75406d0ce9658eb24d69e582ef4f8190b90a8c1e  check-2-law/root-signals/raw-E2/expect-polkit-success.txt
c8347408dec1b22bdfcca1209e2775c488b8afc531a403988ec85c8499aba6b2  check-2-law/root-signals/raw-E2/guest/audit-final-status.txt
be0d4788367ccd3b4f880b35d3d039a696c9c41a12edfed488a27256fe2e11af  check-2-law/root-signals/raw-E2/guest/immutable-rewrite-loginuid.json
1b36d09512ff0517abf2cc899dc044b34c4f021c4b5f4d756cdfdc8508286630  check-2-law/root-signals/raw-E2/guest/immutable-service-first-set-loginuid.json
924e28982678b0082636b81dd8eef689309672a60409e8566ac10a698c55d983  check-2-law/root-signals/raw-E2/guest/probes/authenticated-shell-child.json
ae5cefc9fa276ce714fd93ea624d60f7eeb8219113a6bf301d9d1d1aa12806c9  check-2-law/root-signals/raw-E2/guest/probes/cron-root.json
393ca2d950c09b61fb717fee3f7e4b183c5546245c26553a93720cd3899653b6  check-2-law/root-signals/raw-E2/guest/probes/cron-setuid.json
56205ffc0159f1da738ae6cf5075364d1d8d22c98e95fabcd5022145a07bbe39  check-2-law/root-signals/raw-E2/guest/probes/expect-sudo-fixed.json
2085d418b1fb13ae209bad361ece802dbca31693e313f50f8dee18af3cdb69a3  check-2-law/root-signals/raw-E2/guest/probes/immutable-inherited-setuid.json
372a4ccf4bd56fe48a566f110e3502e521c190dbac81ee1535ea2f7927524a89  check-2-law/root-signals/raw-E2/guest/probes/immutable-rewrite.json
332b743c3692b1665984d740eb3ef8a80d05f7d4c322b5799c7245f5e17958fc  check-2-law/root-signals/raw-E2/guest/probes/immutable-service-first-set.json
8f62a65ff1807052f1b7a8a22890854fb69da44ee63551852459b237903f9192  check-2-law/root-signals/raw-E2/guest/probes/interactive-sudo-cached.json
cd20789777ef301a941dd63ba75fbaf588794870b2f1cabe5c63fa0ce52fc03e  check-2-law/root-signals/raw-E2/guest/probes/interactive-sudo-fresh.json
125332a4f2a27591776b6885deefa3b7906c1028f35dbed22bec81afa106c362  check-2-law/root-signals/raw-E2/guest/probes/polkit-external-agent.json
be9769a44e8b36f405bd5ef506482a517d3d9492f7bbd7638a3f925ddff116e9  check-2-law/root-signals/raw-E2/guest/probes/root-rewrite-loginuid.json
2cd0d120ee6e0d9b558cc51cc451122fca6c8fd2d89c1ad33615eb238213dcf0  check-2-law/root-signals/raw-E2/guest/probes/root-service.json
a94a8183b41d9898f8669c4791fee43118752091eca53ff1ffe596e3951a25c5  check-2-law/root-signals/raw-E2/guest/probes/service-cgroup-move.json
7324e528d215cef11c2de34e6fe5a7ee5887fd781c558aa35a3a189be11e08a6  check-2-law/root-signals/raw-E2/guest/probes/service-from-interactive.json
572c07107b8069ea3a8e9ab7bcb2e7246ae0e6e8c30324ba487403b22b16bc8f  check-2-law/root-signals/raw-E2/guest/probes/service-loginuid.json
fb42504a9a7366b990cd5756259a51184ab7fc1c17611559288720db0373422f  check-2-law/root-signals/raw-E2/guest/probes/service-script-tty.json
13ba044a20b7eeb9c0da6c6c63e25ead77de489c29941d8a1a8302afd9666ec1  check-2-law/root-signals/raw-E2/guest/probes/setuid-no-tty.json
e6293a7adad0392f86fcc62939df17b20708841c0c41550f7ea29a76f0ed51b1  check-2-law/root-signals/raw-E2/guest/probes/setuid-tty.json
aa6932333727762f81d50ab670f356012883341d7ab18d2d2ab113869fbfa4df  check-2-law/root-signals/raw-E2/guest/probes/ssh-root-no-tty.json
d6dee62a9dca3922a96ccd9148add135601ce006bafc5c81e16761392ba514e8  check-2-law/root-signals/raw-E2/guest/probes/ssh-root-tty.json
036e74d8640a09597345679ec965236711e9e75e5da879515243db003cabb133  check-2-law/root-signals/raw-E2/guest/probes/sudo-nopasswd.json
77e07f69efc61a7107dc5f1ff5b832979b40fda8a4c18020d58e49a314766fef  check-2-law/root-signals/raw-E2/guest/root-rewrite-loginuid-loginuid.json
4802089efe523ee4395b11cf61f329a8352771233e607be9d75562684edd907f  check-2-law/root-signals/raw-E2/guest/service-cgroup-move-cgroup.json
9fa779bbb6337b432bbaa05e3371af745cc6a3944f65aa777bf0d858227beaed  check-2-law/root-signals/raw-E2/guest/service-loginuid-loginuid.json
4fad21c597f8a9bb684c40ef96bb1d74c9e6f924ef262daf3a18076578f21c40  check-2-law/root-signals/raw-E2/guest/sudoers-e2.txt
2a36a601d083b6215698f322ad3e6b24a4de4ac9ffdc2728db1b1db823d51d63  check-2-law/root-signals/raw-E2/guest/versions.txt
787b5a6735320cb1ec0744bd664ee77c890841a120c903da31903b6efbe80805  check-2-law/root-signals/raw-E2/interactive-sudo.txt
7489d5494182371fc949b9073beee5e5395bc1da783782039668cf26197132ec  check-2-law/root-signals/raw-E2/measurements.tsv
f47237cc328709206d4950686e6b2cada44772d1a548001a9b77574c01bf3470  check-2-law/root-signals/raw-E2/polkit-external-agent.sh
213054b4f9324c615641334e770c8021a63ec6299f2d9315ff6d587f179e7b9a  check-2-law/root-signals/raw-E2/polkit-external-agent.txt
9a19a721a92c0d4476e21ffcde45a5ee354fa980cf8d4dec1428be32690b2379  check-2-law/root-signals/raw-E2/probe.py
67ce735873c15e8a06c29a765c4c0f6f32d59cce76d3cee4f6bd270999b52666  check-2-law/root-signals/raw-E2/run-matrix.py
f2c5110403b6e876feee7e2ccd497afc261577b5bc8e329af0abf426eafb9b89  check-2-law/root-signals/raw-E2/run-supplement.py
1d026a1c1e7aa522d2e39255059e77332e8b49274984a77d2b8031b92e87f23f  check-2-law/root-signals/raw-E2/setup.sh
b503c779dde9b6dcf970de33c66d50ebdfbb2266637715508f60982f27212084  check-2-law/root-signals/raw-E2/sudo-negative.txt
41574f812389d64e1791cde2b770a2413f5319936bb4bff80b9cf47b0ef2f0e6  check-2-law/root-signals/raw-E2/sudo-nopasswd.txt
18a06b6d1b488a5d0214bb6da2e02d349cbf2eab8b2134b21a1a1264eb346f85  check-2-law/root-signals/raw-E2/suid-helper.c
3e688fad4ba1d159147fe28e395e407b01e64de19677fc2b9bdd0bb8167bd01f  check-2-law/root-signals/raw-E2/summary.json
cb0d21bcebeac32d2fa19bba7ada96707eaf2b7e08176641edaf562edd659faf  check-2-law/second-implementation/P3-1.md
fb45f45d5ef85577228e1b433a0c1a5581f5cd2c6f7242459c9d922f67f659d2  check-2-law/second-implementation/P4-8.md
eee0376090b2845535cab64447aacd4550dcdddfdf9f7cfc9f0bb53dd9beba45  check-2-law/second-implementation/REVIEW-P3-1-2.md
3130470e924636fcde7e162ab67f1eb2fdb3161de1df4c8a1c527cc2065b3139  check-2-law/second-implementation/REVIEW-P4-8.md
d1b0d6e64bef2346b1a4106eb70ffe716c781a83cab46966864d26b931620f90  check-2-law/second-implementation/REVIEW-X3.md
1de4146178018b4efa0635b43102e9591720175182484399c36825d46abaf461  check-2-law/second-implementation/X3-RESULTS.md
0a8ab3e30fac16cfc318ab14ce828bfeb22f64d522ca4c4eb16b60ae015f9c46  check-2-law/second-implementation/X3-controller.py
bc57940b785e0a838053af2e9e7b671fa9bda640bb137c057407522d870364b5  check-2-law/second-implementation/raw-FX-P3-1-1/MATRIX.md
33308da74eeaf2cbaf611a01b8edc0bd2dd9f21406c3a3d11bef2c4ce23e73d2  check-2-law/second-implementation/raw-FX-P3-1-1/adjudication.json
ebc4f7fbe0772efb81a45258bb055167825ad9131b3362a71ed279c59792085e  check-2-law/second-implementation/raw-FX-P3-1-1/analysis/bq-absent.json
833eb25a128f36136cd953f2ee68b0178010998cc28823cb513bd20734713caa  check-2-law/second-implementation/raw-FX-P3-1-1/analysis/verification.json
61a227da0d7f64bfd1338d4fb7ffb25db84cf76dd6bd906c1ce51819415f6899  check-2-law/second-implementation/raw-FX-P3-1-1/analysis/x3-absent.json
7d484fc59c66f6984f270cb449e4944af4b46663f0d212882c1b00d4dfd6c302  check-2-law/second-implementation/raw-P3-1/analysis/bq-absent.json
9e638f0a165938fa84c7f239c8adf50f8727595b58d2acb6e63affa93d3a7c29  check-2-law/second-implementation/raw-P3-1/analysis/bq-atomic.json
71df7d8e0556ea540b264f07c641b260f858a20cb7aad8a812cae12fac133a1e  check-2-law/second-implementation/raw-P3-1/analysis/bq-directory.json
cda6cb6cae0dd38223ce014e54b3c1da6524be238726c506b50d497addb19bc9  check-2-law/second-implementation/raw-P3-1/analysis/bq-existing-r1.json
a2497a8f935bf94bc3be0dea2c46ae2d690dede0c3a13602bbc09de654993216  check-2-law/second-implementation/raw-P3-1/analysis/bq-recreate.json
b24ae203694c42e802292517420830788a16e1156a72cbecc0007add0642770f  check-2-law/second-implementation/raw-P3-1/analysis/bq-rename.json
6809f8c49aa5641e3fde8512b3aa5ab9a885a0b7210fc0aaee59d0c6ed6b13a1  check-2-law/second-implementation/raw-P3-1/analysis/cells.json
8b1a31e591ad3a306557f7e44afd7e7816ef387c6bd289484b10898ade4eb369  check-2-law/second-implementation/raw-P3-1/analysis/runs.json
f1aa95fd3aaa7be9e3f87a02d3958e5c9a2dcc702b2188852e10282be65f1a52  check-2-law/second-implementation/raw-P3-1/analysis/verification.json
0e031b682e2cce2f1e919617b7c883c9a1a54980bc3894873d78b5c62b03f26a  check-2-law/second-implementation/raw-P3-1/analysis/x3-absent.json
0323f0a5b080e9012a791d6899aa1cbb34f508730b5b6ce95ccbacb8161203a2  check-2-law/second-implementation/raw-P3-1/analysis/x3-atomic.json
9b4d579b538c6f8237d1affd12a5db6c929e4b13a4de60805723d4da202a75e9  check-2-law/second-implementation/raw-P3-1/analysis/x3-directory-replay.json
8798ee0f7385e6c8051f91e5d8e00fd1fac1ccb269907d7ffc81b3557dcbb888  check-2-law/second-implementation/raw-P3-1/analysis/x3-directory.json
3274e7d0992e57842c197a10b572de1fda25dd04bf8b4e53e5a1afe7cc8b632e  check-2-law/second-implementation/raw-P3-1/analysis/x3-existing.json
ce025726c9f46dfb6a73371dd3c5c4edc7fad58a70c07be8a3b6e2ee01a897b7  check-2-law/second-implementation/raw-P3-1/analysis/x3-recreate.json
6f69b8b6d267c32ad1a8148145027345a94ee5bc40a0e7d3d5d748d762a32b01  check-2-law/second-implementation/raw-P3-1/analysis/x3-rename.json
54346baddeb5afaecaa5b4c9dfb9a024529817a8974d84cfea35224c30808c2f  check-2-law/second-implementation/raw-P3-1/inputs/X/X3-policy.py
0433e673164fb164e46de8d98f6cbe68b0b16f9bd99fb530b2f5be09a62eee8c  check-2-law/second-implementation/raw-P4-8/analysis/matrix.json
f63da4f389e4ea549dd4b4bf5cf5cd3b9d8ecc3135751aa7d040845402c7991f  check-2-law/second-implementation/raw-P4-8/analysis/summary.json
930351f7a075868f25a86dfbe19ae961e1da725964db500ae0271c23143312b4  check-2-law/second-implementation/raw-P4-8/fixture/identities.json
d55d458717f0ffb354ce3bd238d81809aa4288b688052add203fee8574d11af4  check-2-law/second-implementation/raw-P4-8/server/results/blocks/after-first-state.json
5c0ce24a0991962fdb0ff342a1aff277eea6233bf27bd02a18448b02ef65ab88  check-2-law/second-implementation/raw-P4-8/server/results/blocks/after-retry-state.json
bb48e16ad0252634aa142d3925d92bec0a2432ac9fe10b8c12ffe0e2486dfcff  check-2-law/second-implementation/raw-P4-8/server/results/blocks/arm.json
711e3df921a73b573e2352aa584e98068eaf40a38c2258a0d80584f43347a84b  check-2-law/second-implementation/raw-P4-8/server/results/blocks/before-first-state.json
b8b53e04986090f3c6e31ea99fa315a09a7ace1b138e1eb856a4294e67992f2a  check-2-law/second-implementation/raw-P4-8/server/results/blocks/retry-alice-baseline-exec.json
cc2b29da4c252f1d6a078097b63c2589817a8b938148ba3459025bea4922f8c7  check-2-law/second-implementation/raw-P4-8/server/results/blocks/retry-alice-confined-snapshot-exec.json
2a4231bfd98df8a830a484c39771f93205450ab6a168b6bf10a804a6d4ca60d3  check-2-law/second-implementation/raw-P4-8/server/results/blocks/retry-baseline-meta.json
7e59a2ed616c9fd53b8d690b4394da1906e7cb9fb2f3988d992378fa43272712  check-2-law/second-implementation/raw-P4-8/server/results/control-small/first-alice-confined-snapshot-exec.json
ebbb38a47ed2d1592a98d71358524aa733ede0e370ec53f394a701ff48a3787a  check-2-law/second-implementation/raw-P4-8/server/results/healthy/after-first-state.json
6c8af6858fe25507d62ea1e740d6a32a45155e24589ff586b033ea5067f33380  check-2-law/second-implementation/raw-P4-8/server/results/healthy/after-retry-state.json
6f2ce34dab13b8219909eeb61b4b725cd2947fc78f5e929bd2912c1234b5b231  check-2-law/second-implementation/raw-P4-8/server/results/healthy/first-alice-confined-snapshot-exec.json
67cc61fc1d6bd7dced642480a4762e948a274c770cae5af459f8fc7d13420559  check-2-law/second-implementation/raw-P4-8/server/results/inodes/after-first-state.json
c0413258a18e1ca1b87205b087d39a9b823ce499b6c61258f996cd90fe73ab16  check-2-law/second-implementation/raw-P4-8/server/results/inodes/after-retry-state.json
5eb1a956b102d31ccb52f42e6be1afdc13fa349004934d9e47c4353dd2289dfd  check-2-law/second-implementation/raw-P4-8/server/results/readonly/after-first-state.json
43ff9c59e360ea690cecc3779453dc66aa849e411e98f94631edfb9593026ae9  check-2-law/second-implementation/raw-P4-8/server/results/readonly/after-retry-state.json
664202d6025bc69031410af449a7da8e9aadf4a0d34163e02f27373459a74a67  check-2-law/second-implementation/raw-P4-8/src/payload.S
8942b346bb640599a785ce8f066e0a3b2c803b538dbee5edc92a46809c994cc9  check-2-law/second-implementation/raw-X3/comparison-counts.json
12cc67c0037d70004ecd182219e9fa25404283c829413675935a9d8cfe0b5e3c  check-2-law/second-implementation/raw-X3/final/authority.jsonl
3133063466c15e138f613dee1eff11b04dc3713291851f1a5ecb5b0bf9e09fb6  check-2-law/second-implementation/raw-X3/final/browser.jsonl
476c7feca4bdc078feacb1d91ec1228969ec94786540f19f06bcd895d50d768c  check-2-law/second-implementation/raw-X3/final/build.jsonl
282bbdced0ca74eb84966a6ca40d7b015fd2cc7c59c8d60f37d53ae6ecc44492  check-2-law/second-implementation/raw-X3/final/final-status.json
f785567b445d3486768c0d663d8ad596fcb111a20fed779685439a9ed32e3000  check-2-law/second-implementation/raw-X3/final/law/00-reset.json
aaf9e71adf9f8453b55dc4815dee9e9903a62cf4ffc8b15c1d42aee901ce9fff  check-2-law/second-implementation/raw-X3/final/law/01-identity.json
eba29cc4dfbcfeff947ff361eda70c7fe6c78f43b7c4aad4c45b9f1d35d0c909  check-2-law/second-implementation/raw-X3/final/law/02-system-package.json
02b1237621a09c3af268aede6a17810831af67683efb94314a4b6bf569a07878  check-2-law/second-implementation/raw-X3/final/law/03-pip-global.json
9e033b1bd5c4965084f028ad67913501e3e175cd2f40c2d4c57a42a493239d40  check-2-law/second-implementation/raw-X3/final/law/04-pip-user.json
f8c7a944f44f57d955ec34ebb87708e3e3809b2b41820e71803f6ce5c27ae70d  check-2-law/second-implementation/raw-X3/final/law/05-npm-global.json
58e394a2d28da6406b945acdc26f7229b64b18f47fe376205b3adc12aea23cdc  check-2-law/second-implementation/raw-X3/final/law/06-npm-user.json
3bb37f9d59560e4b6584d32700a43a69a7ae0d723e12e767d29574fc1c79a922  check-2-law/second-implementation/raw-X3/final/law/07-flatpak-system.json
2e907312b1eba2077fe6a1329407645d0b7721be6435aae01405bf88b44db671  check-2-law/second-implementation/raw-X3/final/law/08-flatpak-user.json
148710ded7c44d8f86536e63ba812b52da85d004db4011a8a33dbe03aa7fc3f3  check-2-law/second-implementation/raw-X3/final/law/09-appimage.json
5cbe9f371b3b926f19382f5e1103bce7cfbb0051cc6b56bbeabc3df574161211  check-2-law/second-implementation/raw-X3/final/law/10-download-home.json
07fff7008ca8ab7237117f627012cafac90599fd7f8c0b4b6dbdb4a2c8d302dc  check-2-law/second-implementation/raw-X3/final/law/11-download-tmp.json
41b32fe633a9e769d47854ccca11c987852774b69e1e36cdd01428764c7a3213  check-2-law/second-implementation/raw-X3/final/law/12-archive.json
16a2654796f0e11cdeccd6da1c7b66b1a37f455974d848948c7a31c8397a58a8  check-2-law/second-implementation/raw-X3/final/law/13-build.json
6eb7520a19d824e45455fdaf16cedd3b173909f67aae23801e86f345fe64b8ef  check-2-law/second-implementation/raw-X3/final/law/14-user-service.json
7c31e24bfc784d3af482c2a3ef1dde58c5bf68416eb19c898edf33137a0d2e9e  check-2-law/second-implementation/raw-X3/final/law/15-user-timer.json
90711095a2ff761849ac5fec838198d49c1de0febaaf8058c7dcc8479828e726  check-2-law/second-implementation/raw-X3/final/law/16-cron.json
3b1bc8644e72adc1e950e15afb31fe09675c24c0502ec87db04f94ca9678ac31  check-2-law/second-implementation/raw-X3/final/law/17-python-script.json
bf13046005edf60b052a4bbcdc0490948af8da00665c6822a476ff98eddd975d  check-2-law/second-implementation/raw-X3/final/law/18-shell-script.json
38d08e15d9286426331236b6ce9ce9617671e7a3fde2f9cd89b352e55d65754b  check-2-law/second-implementation/raw-X3/final/law/19-system-write.json
40d62d3e8094b35c9b0edbc717275d1dd76e34c54d0d838bfef5561b8be9f247  check-2-law/second-implementation/raw-X3/final/law/20-loader.json
90b3e406c01ac41af1c8fbad26cb198fcbe3c33b1d2d83ad2498c68aefd22f5e  check-2-law/second-implementation/raw-X3/final/law/21-allow-apply.json
98b76037983f425b1d3bb8933554875776436a586fa8536082b1a452bcc3266f  check-2-law/second-implementation/raw-X3/final/law/22-allow-home.json
d871e08db277ff243634d9fa92701ec0aed9770255c38a9ef54035550ae9ae1e  check-2-law/second-implementation/raw-X3/final/law/23-allow-tmp.json
fe9859e07c4a2d1b7d85feae6f5e352aa0b6df1bd9c0678e08898cbc28b1e430  check-2-law/second-implementation/raw-X3/final/law/24-revoke-apply.json
8188489a8e9b2e9e06d208d1a4d740d8b7eb20c197469898532b806329d52b1d  check-2-law/second-implementation/raw-X3/final/law/25-revoked.json
66f21efabdb2421fad386369ca3f570b958f2033979484b1023fe86df3530123  check-2-law/second-implementation/raw-X3/final/law/26-install.json
2892dbf7fdd53a60a1b6c21a94c08e8d2feed8570f60a3208f38c8aa09d929cb  check-2-law/second-implementation/raw-X3/final/law/27-network.json
7cc004c78530379699e29d5838e1314358bc362aa00e403f6b833e7a56580f8d  check-2-law/second-implementation/raw-X3/final/law/28-update.json
151df7145b92d98bb2906b522ae1e4a6ddfd153402f72cf7a710ca37d1192613  check-2-law/second-implementation/raw-X3/final/law/29-update-packages.json
f1b912737b4aa522b629594216885f34607887256b04244a457dbfde89366c51  check-2-law/second-implementation/raw-X3/final/law/30-browser-declare.json
24da811e3d8b001539ad359ae068994444261288f7cace7e908a3971a6b75146  check-2-law/second-implementation/raw-X3/final/law/31-browser.json
da1ae9eb499cc618e6b2cd3639e0fe8455c33a4e6118446950685af4fe4fddcd  check-2-law/second-implementation/raw-X3/final/law/32-extension-prepare.json
6b5f95dde31a0f571d3fc4b919e83919045d04b741e390c62505d21adb953802  check-2-law/second-implementation/raw-X3/final/law/33-extension.json
58f5c3622cde7d67b93f6dc8e844c8e099dee79bba24cb2fcc726c5b95a5ab70  check-2-law/second-implementation/raw-X3/final/law/34-root-managed.json
4a1f3f40034b6db85e5a404da4cf0b287893cec3767552f817af1c927933afc1  check-2-law/second-implementation/raw-X3/final/law/35-root-unconfined.json
cc7345d2f439ce12bda336a38c2578b6fda95d29bfd057ac89089ad7441af511  check-2-law/second-implementation/raw-X3/final/law/36-wifi.json
3c29433076afd2b28c8afa4c24c7cb642bb5754d865b0a679345233066256f75  check-2-law/second-implementation/raw-X3/final/law/37-bluetooth.json
1a3de96c3fc94bf1c518367ea180b3e2f7b3d571c3f20cc3d7c3f463c46072cd  check-2-law/second-implementation/raw-X3/final/law/38-audit.json
a79462e0ee8da8c68e6269ffedad5c3c52004c216fcc072bb2502eba0242fed6  check-2-law/second-implementation/raw-X3/final/law/rows.json
a1c4854e0e9c06c5098e6495a9c07a9b7b319d673c752537c4b7308bbe06b14f  check-2-law/second-implementation/raw-X3/final/runtime.jsonl
5c72a2964848966c675da25708b5dac8df02343cf8fb19dc19fbf9312ce7d738  check-2-law/second-implementation/raw-X3/root-noexec-supplement.txt
02b8f005454338e1ee268d519a56fc99be347b6bef3b6746833a3aa9aeba609a  check-2-law/stand/Q-RESULTS.md
0d6b657fdea56cd3bbf438a1c78526dd40d8e29a2cd90aefea0ccabcd0776dd8  check-2-law/stand/Q-REVIEW-2.md
47243c8fe9c696e3ebcbde8e58a3be698c285c015f82df1ff9ea028cf9216810  check-2-law/stand/RESULTS.md
be7eb4d73c2495d64127fbcb99871a23a3b6eb3982e9c2b90f88b5c157d990a3  check-2-law/stand/REVIEW-2.md
cf0ef86c3376406f1ddbbb128c60d788fddd1b0c5800bdb21d5516ef253fbb3c  check-2-law/stand/raw/check-lifecycle-v2.jsonl
6d04eb407ce7308709947fe7edfc6b0975076ad80ba893123409b30c9b3ccca0  check-2-law/stand/raw/fb1/check-authority.jsonl
b8c1074e2d358ad6da827d214481bae443c7554633d9bdbec40d129687927955  check-2-law/stand/raw/fb1/check-browser-lifecycle.jsonl
16d7b69b5a2c6c0baf125923541f16678f8e05b0ea632c8c296d326ac1193d09  check-2-law/stand/raw/fb1/check-build.jsonl
fc36aa2884d7612f671ddab8899a1dd94d9ed32b2a09453137af7fde28ce53a8  check-2-law/stand/raw/law-v2/00-reset.json
141ff64b71da7c1bbcb72d423089c4ac86c5152808e038c1a8aa6f8a56ed53cb  check-2-law/stand/raw/law-v2/01-identity.json
ba2067c78e7ef30268c6d00dfb9a438a865cb43e59eebbcd0c46e78e6ef8f899  check-2-law/stand/raw/law-v2/02-system-package.json
917a97bff5201db135cb431ec89d8c6488c554b8934d0d5a6c35fd6ca7028686  check-2-law/stand/raw/law-v2/03-pip-global.json
fd514079886cdb705718cf9703dbe66f7c2bf0b70fa33012a25bce03aab286cc  check-2-law/stand/raw/law-v2/04-pip-user.json
62ed1ecc85e9a8394aab00820bcde8c6ca30f40451c6e47527bd2d50734c777b  check-2-law/stand/raw/law-v2/05-npm-global.json
45d69f852bb475b644246577737ea4b8e9afe3f05ff07348e41d2e3ce6b96d82  check-2-law/stand/raw/law-v2/06-npm-user.json
da7c861b7999a5a55c5af9e9c332f0091fce57c417aae98d744d8d82d00aa53d  check-2-law/stand/raw/law-v2/07-flatpak-system.json
48a03b16b531a0153663cf4063414d8102c1cd7a767f2154a1f92b3fabb3851a  check-2-law/stand/raw/law-v2/08-flatpak-user.json
7e1dc4783b99ca995861bb5219f5b38a315e362ef35c2d37060b6885ec90b486  check-2-law/stand/raw/law-v2/09-appimage.json
6e804a094c608f45245da34459cd7c8af6cc97e5116746f0f80797d4b2300a55  check-2-law/stand/raw/law-v2/10-download-home.json
0b8805a7fc17d59eac1519e5162ba2835aeaa174c75054a4680ef16bb2c30527  check-2-law/stand/raw/law-v2/11-download-tmp.json
d7d929f732db9587ae8be59f749dd342b24338ffdd843d59d5ff61cf1ec6f2fc  check-2-law/stand/raw/law-v2/12-archive.json
2beb2b585a2707c2eefa28fd4febc102444f02bda8031c20edef99506bb86761  check-2-law/stand/raw/law-v2/13-build.json
a8d353a5df3920549daa9acc33c12f3322a54b6846813564e23748424b273fe9  check-2-law/stand/raw/law-v2/14-user-service.json
924855da1793d6e73f4140fed22a39e8bc5f8594782d5904cedb414525ee2606  check-2-law/stand/raw/law-v2/15-user-timer.json
9bd57c5a79efd852d4806d8e1138f2c3a51cd557e2dc47e4ec1ca0cf97f9561d  check-2-law/stand/raw/law-v2/16-cron.json
60322615916f586865dd15a187543e120dbf477ceb0edf3cfcaf85cee87253eb  check-2-law/stand/raw/law-v2/17-python-script.json
e6c105ba5716e49d57136c012aff5e898efda1f161f910c1f1617a5078b7b36c  check-2-law/stand/raw/law-v2/18-shell-script.json
31457e4bc091252b889e9d409f352bf1714f806e7b3945654adf45e68255a62c  check-2-law/stand/raw/law-v2/19-system-write.json
44e255a448cf6006cfff4c1d5318195038e04e29e21ea81db0cafeecd73af8c4  check-2-law/stand/raw/law-v2/20-loader.json
97c6881020de7da566c954ea6a3b57ac5371a6c778be338c96ce8b694f71191a  check-2-law/stand/raw/law-v2/21-allow-apply.json
b964b036929a96464a95cc2c1998fd8b3c417142047c8ddaaf12b448b1a619cd  check-2-law/stand/raw/law-v2/22-allow-home.json
c9617f443e6f7f5e6b67d5ed81461482d2eea73e41714b400ec06353529e6cd6  check-2-law/stand/raw/law-v2/23-allow-tmp.json
b3f0d6bfe4858a956b35e3d915a11cac36daae5191deda94ed4551d563908e30  check-2-law/stand/raw/law-v2/24-revoke-apply.json
f2f5afd96c64377280211642a8b08db4a11e9b3144d42af23ec26cc60c739392  check-2-law/stand/raw/law-v2/25-revoked.json
8ad029da88904814ed3fcd48db84523e7813bac40d068c58908b9d398870e27e  check-2-law/stand/raw/law-v2/26-install.json
687c0c86660b3a0d53ed52211595b2444f06f58378063bb3221e5f25da6a5a14  check-2-law/stand/raw/law-v2/27-network.json
a1626c98265edf1255b4b8230cd9e269643fcc8eaf138526768b82764dc13576  check-2-law/stand/raw/law-v2/28-update.json
8a226283ae784b8e96211b1bff3f82434586cacc8caf9a10db00e5d44caa439f  check-2-law/stand/raw/law-v2/29-update-packages.json
6157f510bdf669be14f0948243474a3ff0e0c0b2a2fd15362b8fb113b3b8ca3a  check-2-law/stand/raw/law-v2/30-browser-declare.json
4463db4649975b8be709d97dbe41a05efe591cadc2ca29604903da2b33485e35  check-2-law/stand/raw/law-v2/31-browser.json
2db8d2f8d01915b440a36ed5806e6cad322976ce6b740d08bedbefe4fe697cd6  check-2-law/stand/raw/law-v2/32-extension-prepare.json
76e7df0e70413329a31bf46c160436ccb12007bfe2857e2f02b926810c763267  check-2-law/stand/raw/law-v2/33-extension.json
97d4e1bbd53075fa99f9eaeab919d1c2793d5eb7469011f32d630e25be19450c  check-2-law/stand/raw/law-v2/34-root-managed.json
8cb345b02cf9fdad38ab528306a1008022667bc61407347275d11b4d07c2aa87  check-2-law/stand/raw/law-v2/35-root-unconfined.json
01fbf2557db84474c601305be75ea97560be61bcbf3267edcd42fff5e35dab68  check-2-law/stand/raw/law-v2/36-wifi.json
a5ba8bede21abb4ae5127ae579f91ee12d86ccc8dd5527711cd2b5e6cae0d028  check-2-law/stand/raw/law-v2/37-bluetooth.json
dc39a5bd505a9093ac353f1f9bfb107970cdc1c952b9a21c93ecd0702e1042c0  check-2-law/stand/raw/law-v2/38-audit.json
a85ab5a08c47168c77798e507af106fe88a854f1d88957410a8277286f3a0eab  check-2-law/stand/raw/law-v2/rows.json
56c94b9851c9e4c38d3903e9febb16bc448df7cd1e807f3e8b1b4b7bf05013cb  check-2-law/stand/raw/q/main/apply-policy.py
f0d0e89e765ee76e5851d8233f5d7213841dae4d6998b0a4a823b392faec08f5  check-2-law/stand/raw/q/main/cald.py
f35380a82d6acfd4df879d186487535e05df12b0c011055b4b5a6ba1026c03bd  check-2-law/stand/raw/q/main/check-day.py
f794fa49c8496b0ac8cb3e1e15d927c8879293fa6ccabd826862c64f15d8ba49  check-2-law/stand/raw/q/main/check-real-lifecycle.py
751a5ed97ec006479d22be873e2a66f0b4cd34ddcb5713cec66ee8633c58d4b1  check-2-law/stand/raw/q/main/check-supplement.py
cd37167536e3014b4df97e1b76912cc807a06bc2e82afa5a329c12aa209524df  check-2-law/stand/raw/q/main/day/22-pip-permitted.json
51a5907f64a116741550e62501cfd8d7f4e87e7a8f604fb054c8916c149e4eae  check-2-law/stand/raw/q/main/day/rows.json
8638312bce1c984d98834ee726a66ca6cd4c015fa1000771aa64fc4a557c3de1  check-2-law/stand/raw/q/main/lifecycle-v3.jsonl
8e5f353a2e74eadc9818502a15d0b09292fc3050221823ddad9dc81f258f866f  check-2-law/stand/raw/q/main/radio-final.log
1fde3e6546283b9819a13066df995e085478a4f5fb3a48ef31fe147362d9dc7c  check-2-law/stand/raw/q/main/radio-kernel.log
932b6b4b0bd61ac1f6cf7c6a9bbeec61402c9db442300ee2e7ef9fcd0820be20  check-2-law/stand/raw/q/main/radio-retry.log
cc66055d4ad75b59dbfe1a2bb8f954853982a3ecb87d3a878a0e7aa1c8184204  check-2-law/stand/raw/q/main/radios-modules.txt
3a93b84d298b946bda2c6426cdc54d2e1186aeec347e044f1f62d01062420143  check-2-law/stand/raw/q/main/supplement/00-actual-upgrade.json
ea8f744ace88acfaa5ec333325c5f0292570c40c9b544a77390f20a3ad194d82  check-2-law/stand/raw/q/main/supplement/01-upgrade-version.json
85ba8d0605ffefc8d91ae052563e0b1b73e4046319643285b107985a30f9771f  check-2-law/stand/raw/q/main/supplement/06-pip-import.json
36fde7b9acf16a848866d92fd554aab61032d30911046972b5c3ed0b0e9b4a84  check-2-law/stand/raw/q/main/supplement/10-node-installed-interpreted.json
57942cc370d089b845540b4365a1c70e680fb2dfe8cb4b2a9cf995688d3215af  check-2-law/stand/raw/q/main/supplement/rows.json
53b9935fdcbf8f060d5f8aed9f7de402bab8f498e6aa36248d7ca5f45d1e134f  check-2-law/stand/raw/q/main/upgrade-precondition.txt
27a0cdefaf443edb3bff77016440f00d31ee5394b52b6a0d3f8c804efd7a6705  check-2-law/stand/src/CONTROLLER.md
56c94b9851c9e4c38d3903e9febb16bc448df7cd1e807f3e8b1b4b7bf05013cb  check-2-law/stand/src/apply-policy.py
a056c3876c25d5f797ab2973710cbe1b4fab77255a8da10f7a34876414b800e5  check-2-law/stand/src/cal-login.c
3082b70b6a01b4e00cff042b45c68d722a1b012c49beefe57952db4d38b85994  check-2-law/stand/src/calctl.c
f0d0e89e765ee76e5851d8233f5d7213841dae4d6998b0a4a823b392faec08f5  check-2-law/stand/src/cald.py
1965ec4142a7c905acf037afd0d126ed9fb88db5129814229dabca14361d6f0c  check-2-law/stand/src/check-authority.py
c01158dc993247db33bdf58a482cd67ef3e32b01ba21e8a48fb0a92a1bbb174e  check-2-law/stand/src/check-browser-lifecycle-fb1.py
288b00aa104065904ed37eeaf7257ef781deda72103cc43d3b1b5fd9756febed  check-2-law/stand/src/check-build-fb1.py
69130b5525ad0c046f06333ec49324252b3aa64fe3b6e96f010e843e13e8a59f  check-2-law/stand/src/check-law.py
5012a6198d34f7d2dc9d715727488d6ed961e060b3308bfb5f1ae67bc2ff20d8  check-2-law/stand/src/check-lifecycle.py
17d1d72011b888de6133ec800d28c2d957ef5001c4d1c3a30f7829ba2b0115e0  check-2-law/stand/src/compare-inventories.py
7a083ac52a8b3c4001cf2997ebd7b37972a8d0ec5864e3c59c05b9e96942365e  check-2-law/stand/src/finalize-pristine.sh
610c4db62d57ea94c715b1522d3366dd0d92e5a60004bca218da293d24b00cff  check-2-law/stand/src/inventory.py
e2de2505c2de4e84b86ad9d3a6fd3660b7135e06b13753f0aa1d302463068278  check-2-law/stand/src/repro-root.json
89ec6d2cfd406dae92d8f632bb867b537f51d38f107f2e5dacf4502454b6af85  check-2-law/stand/src/setup-stand.sh
3ada2cfc8308f6c87e1c9ba2c3039f07465a5a9cb24acf5e439ae54414d44bce  check-2-law/stand/src/worker.c
6e3eb6df935bb0459fb76ba599ed3d939f366f99c3a4dcec32ca87c6abfc13d3  check-3-reproducibility/clean-install-pairs/REVIEW-X5.md
1231a1b4ac222faa5de8199d4a8f3b3868b55d1329c1de10bff7f7384d86c115  check-3-reproducibility/clean-install-pairs/X5-REPRO.md
d701b157e7761241d50f8e465d17f1a989001f40a5683900bd07383c0f01073a  check-3-reproducibility/clean-install-pairs/raw-X5/debian/comparison/projections-summary.json
bb8dc928fa8bb949f92df61c9771af63bb52920cf6c6331ad88d614a40f0d242  check-3-reproducibility/clean-install-pairs/raw-X5/debian/comparison/summary.json
757346aa8829c3cee72782cbf5788642c5e57ebb425adbc724cff3ee5556ba04  check-3-reproducibility/clean-install-pairs/raw-X5/debian/comparison/supplement-summary.json
7cbd0b0f379d244a1d54929858742514d23f5f0f8a0c6b003cdf7a5f898de3df  check-3-reproducibility/clean-install-pairs/raw-X5/guix/attempt-4/comparison-extra/summary.json
96b990afc73a498b1d932cfeb4e547f15cb10b90c370b0a1b07a16a9315bba57  check-3-reproducibility/clean-install-pairs/raw-X5/guix/attempt-4/comparison-native/summary.json
0400d1518dd130890d0d4f7f35cc38d8a5b81e09b57fad763473a63060953ea8  check-3-reproducibility/clean-install-pairs/raw-X5/guix/attempt-4/comparison/summary.json
853df879b0b30c9273bd35276f815b628c11f1fc8fe95cd30d39a1ba59d8f15c  check-3-reproducibility/clean-install-pairs/raw-X5/guix/attempt-4/offline-content-line-differences.json
fad126f1543ec2f8f3fe8dc7506f4121b2e1c989cde35051609ea381d20655d8  check-3-reproducibility/clean-install-pairs/raw-X5/nixos/analysis-summary.json
f55fa2b023b3e7adf901f83c0ff38d96e9ce5472ad6e67675be641888097a810  check-3-reproducibility/clean-install-pairs/raw-X5/nixos/generic-comparison/summary.json
dc6db8126363b60ac00bdffb41760b9c1dfe73f1f03d551a523ffd374c89af61  check-3-reproducibility/clean-install-pairs/raw-X5/root-audit-debian.json
2b43920141bff5c58ee713d756bee8168cbd0444633e88c6529828b52a267d4d  check-3-reproducibility/clean-install-pairs/raw-X5/root-audit-guix.json
84cb4de2f5c455d6eefb416100656b1225268690fdf6c6f73085a6d373001526  check-3-reproducibility/clean-install-pairs/raw-X5/root-audit-nixos.json
8d18e89fd9d4342432f0da608091c2d56beee82675be695005b7d4a23c41f107  check-3-reproducibility/hardware-profiles/P6-3.md
c1832b126c774e1195025bbec5037f742d658cb816751740bd539675b7915782  check-3-reproducibility/hardware-profiles/REVIEW-P6-3-2.md
de391f3523bf80a34b3d917ca9f6515b3d6a930812b755f09a2877b228521b36  check-3-reproducibility/hardware-profiles/raw-FX-P6-3-1/replay/correction-summary.json
3fe31902644775550954340c579e93bedd53574a5b9af0a1f234364a2e476825  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/blank-disk-per-window.json
1672b6659b3c0464097b2decd0bfc70ae5b9d8dd7c7815358e6aa8bcfc6f91dc  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/control-summary.json
63e8e2dc66ac77aafafb2b80411a1437214c138435a3c2cc38145907be3dc40e  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/independent-provisioning-summary.json
37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/observation-errors.json
16ca7085228dd3dc4b64ba0af8a70e8fc7df7e0ee9e6644a2ab0415bab63ccc5  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/pairs.json
e6c3f9990095d42b85dee6ac4d284bc27200ee98bdb64acf004ffa8a335db742  check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/report-metrics.json
d353c7f1924e7a2c23d0021ad1ac3e56cc7d4cb28b41749ea1c09f48cfaf4024  check-3-reproducibility/stand-pair/Q-REPRO.md
c7dcd7d50f03f4bb1ad7375503ed74fd125a5476afe4b92a1c54435dfc86c0d5  check-3-reproducibility/stand-pair/raw/q/repro/comparison.txt
9861591bef5c1267c78e6a851de996d4873caadf0ee1f0a7243bba7d3e1582f9  check-3-reproducibility/stand-pair/raw/q/repro/summary.json
4b30e56672a6b925eb9244a828dc615fb15d9645133f16f395a113db6b30a831  check-3-reproducibility/state-transfer/E4.md
0aa2f445fef5131514c7308c7571804475f44504f7397141392886a43bf28bf7  check-3-reproducibility/state-transfer/REVIEW-E4.md
3cc3d0482b5f099306c94598379877a545ec799d13fecc592ff3d3651b2c48b7  check-3-reproducibility/state-transfer/raw-E4/source-baseline.json
ab1fa059834a25b819d077775b6447811f6a608582743d90dee6ff252d860a08  check-3-reproducibility/state-transfer/raw-E4/source-ssh-auth-diagnosis-fix.json
ba59458f8613bd44980c1a6d948e9cf15863598b901839e4f9d71cce4e7f15f7  check-3-reproducibility/state-transfer/raw-E4/source-ssh-export-final.json
8d1ba3134db015320a2d5b91747e98de066b6d59bb89449b5f62a2b3c5bc4d1d  check-3-reproducibility/state-transfer/raw-E4/src/apply.sh
257920861d4296e2574173bb2911515de35aab62e942ef43e572f42d5d9457e2  check-3-reproducibility/state-transfer/raw-E4/src/declaration.json
51c71819e9fab284c7da2030bf69c95459bd21b6608228ec67efe06654fba4de  check-3-reproducibility/state-transfer/raw-E4/target-baseline.json
e122da5f82254333d294ae1f095716816fcd485fe2f955531164add882071b32  check-3-reproducibility/state-transfer/raw-E4/target-credential-matrix-complete.json
50b4c12caf87ea9af482838d5152c2c86c8547ecb684c9ebcb09931115f7f7a4  check-3-reproducibility/state-transfer/raw-E4/target-credential-matrix.json
8ba759e3e7fd73ffcf1f905fadd355b22bf4cd71f215ec6d4c25bc0d27d3c62c  check-3-reproducibility/state-transfer/raw-E4/target-credential-reencrypt.json
bde84c4e77546d508996e7fd43cafb7a178e671538e9c062a1c1aae434fc39d4  check-3-reproducibility/state-transfer/raw-E4/target-final-inventory.json
54a68f1e958cc9e6bb603a09153262104548882836fc770f0c770b828f98d685  check-3-reproducibility/state-transfer/raw-E4/target-import.json
ceaf587dd389e41d4e990cc78edae6ab03719466e0a67e89112d1635991d3f87  check-3-reproducibility/state-transfer/raw-E4/target-network-repair.json
30d5bb459bda2a3722e8c26799c33f1b66914a3cf81a94302ab28c8218ee3e63  check-3-reproducibility/state-transfer/raw-E4/target-postgres-path-repair.json
b3d1d3c5bbb81fd6870f516725220ac1f9974945fc121e4419270ed158dcaa6a  check-3-reproducibility/state-transfer/raw-E4/target-probes.json
22bb4c9e48f6f63e97fe6f4918d53e756400404f36189d403e81bfb62ec39186  check-3-reproducibility/state-transfer/raw-E4/target-ssh-source-pin-after-transfer.json
58b16a5480e051810ad043abadd6f4bf929490d3f5fce0c0a25bca163bc3e78b  check-3-reproducibility/state-transfer/raw-E4/target-ssh-source-pin-before-transfer.json
b909de405ba8426f0dd8efb237948da7d59f24f523b2ce84775211e97cfd6588  check-3-reproducibility/state-transfer/raw-E4/transfer-summary.json
7858b503c6007925cd0109219763f11acd877db4b5c0cfb560d39a954069f8c0  check-4-lifecycle/random-generations/REVIEW-X6.md
ac50be9d7442bd767692da6c92b93d87bc35be01afb2e496a9ccad8720fe05eb  check-4-lifecycle/random-generations/X6-LIFECYCLE.md
03d4f1e0fa983a525da127338e8334c5572f34093b015b5c16386bfbbac58b63  check-4-lifecycle/random-generations/X6-run.py
3de42a86694ef8f7ec632cec6959200784b38530e99db2da04f12364085c06dd  check-4-lifecycle/random-generations/raw-X6/coverage-command.txt
eaa5a3ceef6b9c02abd78e2fce4d694cc8790fd679f412dd67b1b2f64e1c1259  check-4-lifecycle/random-generations/raw-X6/coverage.json
56c94b9851c9e4c38d3903e9febb16bc448df7cd1e807f3e8b1b4b7bf05013cb  check-4-lifecycle/random-generations/raw-X6/instrument/apply-policy.py
3082b70b6a01b4e00cff042b45c68d722a1b012c49beefe57952db4d38b85994  check-4-lifecycle/random-generations/raw-X6/instrument/calctl.c
f0d0e89e765ee76e5851d8233f5d7213841dae4d6998b0a4a823b392faec08f5  check-4-lifecycle/random-generations/raw-X6/instrument/cald.py
3ada2cfc8308f6c87e1c9ba2c3039f07465a5a9cb24acf5e439ae54414d44bce  check-4-lifecycle/random-generations/raw-X6/instrument/worker.c
e494c1f670a591d42ac2e7aa5d63e3be905d77e8aedda0066839462d9bf2fff2  check-4-lifecycle/random-generations/raw-X6/results/seed-1119/summary.json
6de6ed6ec9b4d15f0454eac29d7cd42e4b190c5cbc163479d154839233ddd517  check-4-lifecycle/random-generations/raw-X6/results/seed-20261119/summary.json
c9a676ed0a8dcc41263ce085d1958e8a92be8e921d127aeb70b5981c1200dda3  check-4-lifecycle/random-generations/raw-X6/results/seed-42/summary.json
211d87625f942dcb2e33edef0db5492c0fb9780b81a88521860be54cd60dd18b  check-4-lifecycle/random-generations/raw-X6/results/seed-6/summary.json
505edb575005a4780a993897ac554691e4a9cc83f4f9b3def297a493078c3350  check-4-lifecycle/random-generations/raw-X6/results/summary.json
fc513477ab073758c0154514de9a4472a7c1464e5d6666df75adeed84e23e955  check-4-lifecycle/rollback/E3.md
ea5ccd177b61849d0d580f70164a4ebbc9fbfd2a11a04f97e2c228097017005f  check-4-lifecycle/rollback/REVIEW-E3.md
f339dbe63b95e2e5313452cf76fc0a6891adc31cc24ffc7f18ffb14703a8c536  check-4-lifecycle/rollback/raw-E3/event-index.json
040f9a9713614269842a043a069336086ae6049ecf8601cf2499a6acff39abb0  check-4-lifecycle/rollback/raw-E3/events.jsonl
aed54f2b8fc3eee1827a9790f100608d2023714a952eb67dc4b2073f172fca38  check-4-lifecycle/rollback/raw-E3/experiment.py
3de2700d56841232372bd7da8c345c53e09e485dd96d467d55e9f8d24950021f  check-4-lifecycle/rollback/raw-E3/ff-after-refusal-inspection.json
6bb49e175c199f1e7e4727ad039558142dc8ee9d878ad90daccf154e128abeea  check-4-lifecycle/rollback/raw-E3/ff-new-inspection.json
a47fd05957da63da39c159a55d17932afe46adc39f8902170fd0fed51f5f2148  check-4-lifecycle/rollback/raw-E3/ff-old-inspection.json
b11f2a6e10989895fa18e8b01d2f1d0362c6a01c89789dd56b2980a797064a9b  check-4-lifecycle/rollback/raw-E3/ff-recovery-inspection.json
08ff7dc63683bb29cf7b44f93df813a624ef7a82446901334c2240c978a8b52e  check-4-lifecycle/rollback/raw-E3/ff-restored-inspection.json
d2edaa615f46769d2920a6ff81a72b40077bd62d625b771ef11dc50ed696579f  check-4-lifecycle/rollback/raw-E3/measurements.json
d89171257d314753f3af9bf5e207fcf6084273ee0ac7fa29192a46ad7c5a7b6d  check-4-lifecycle/rollback/raw-E3/setup.sh
417e807a9db8ece9d62c37d219a0b56b773afe76ef5c4589a33e074473cb1e40  check-4-lifecycle/rollback/raw-E3/st-after-config-remedy-recovery-inspection.json
22723c63fa57d92764c5b0fea8b570463efb5b8a1e84de1d4a0e87fadd5a5934  check-4-lifecycle/rollback/raw-E3/st-archived-config-result-inspection.json
8cb80d87854b64d6058a5dab11046ee16bfe80b8358853194f4ae9b787ee3d4f  check-4-lifecycle/rollback/raw-E3/st-new-inspection.json
3e384c45b81f20d56770a70a74f7f39550a2a9a6fef2498abae4840c2eb6195e  check-4-lifecycle/rollback/raw-E3/st-old-archived-config.log
e96c125915c93736e800faabe9f591c44ff4dbc6e41c09a23b7cd94a6d180fa8  check-4-lifecycle/rollback/raw-E3/st-old-inspection.json
39d2e70f498c4fffd2158d27be36d46d6543542f9d0199b5f851e767669ce070  check-4-lifecycle/rollback/raw-E3/st-recovery-inspection.json
2a25e9808bfa16d1f40d80e8a9ede0a4bd0d02d697c2ab0a961b4988c8b02dd1  check-4-lifecycle/rollback/raw-E3/st-restored-inspection.json
bb276d1d83a93b4acef7587987edbf04f044cc0d0eb6c2f522a5a93371af2333  check-4-lifecycle/rollback/raw-E3/st-rollback-latest.log
9907a7588b7d69d8672afa8b7143d81a00eea0bcf3f83855662f968350379187  check-4-lifecycle/rollback/raw-E3/st-schema-diff.json
408c9ab6874fdd5ac1ab58c34331d4aaa905be32e4f6ce7ade392fc5817f1161  check-4-lifecycle/rollback/raw-E3/supplement.py
6a5c132d849fd6a011d6c512d362ff0a8ba050c6db7cb2fd23be3fb2675e5d07  check-4-lifecycle/stand/Q-FIX-1.md
3cf4c71cd6375d1d46c644173ff904696ed28710667dca5d82cacc19568ac075  check-4-lifecycle/stand/raw/q-fix-1/run-2/audit.json
f7066318ace66babf3e3395d75dcdd445e6b21b9658ed5091618bf347a31e73c  check-4-lifecycle/stand/raw/q-fix-1/run-2/lifecycle-adjudication.jsonl
04359adc321673addffa9ab0b62d9150c9640aea2f0bee4ccf32bef3b3b58a8f  check-4-lifecycle/stands/P4-3.md
4374ef03e73b04fbd7877b5ebca8a197b62929647a7acf364c8d40f11d0d5570  check-4-lifecycle/stands/P7-1.md
11f99bfffe1dd510ec2b68d3b0e6e47b9696bfaa27860e7f3317b19da1a9ef92  check-4-lifecycle/stands/P7-3.md
4d276c9e1e8d6edec1fd2bfad8f9da06ce1a3339c4b9b3ddb35ff18988b8ea00  check-4-lifecycle/stands/REVIEW-P4-3.md
5f044455c8f566b0c3911b6951a2d248e530ee4b500882b5c192d7481fad221e  check-4-lifecycle/stands/REVIEW-P7-1.md
88a67becdf55f3e8dcef0acdf1829c7eec5a97b0e400b867f8ca75e57f2abc62  check-4-lifecycle/stands/REVIEW-P7-3.md
2f1af6bc0ef71dbab2925090013261b81a6ca14596c2c793e9eae364b50e549e  check-4-lifecycle/stands/raw-P4-3/analysis-reproduced/matrix.csv
1e1cbe0318861bdc459a0f32515caeef9ff8f88bf2fd95faf186a8480eee9e9d  check-4-lifecycle/stands/raw-P4-3/apparmor-denials.txt
3c75afd70d38c45feb64ee6c9c250d82cb93d3d3d03dd6e88d3cf080afd12468  check-4-lifecycle/stands/raw-P4-3/declarations.json
73c8dbb0d4ef8e654fef91b9ca489e001cd2ac1aed49920eb845c9a081240a50  check-4-lifecycle/stands/raw-P4-3/guest/results/ro-saved-delete/after-retry.json
4a33543043685d8f0d15bc1546a67db356036e4b4c69fbd1f5c62f0bdd1663b1  check-4-lifecycle/stands/raw-P4-3/guest/results/ro-saved-delete/after-transition.json
23cf0654dcdf8d1cd39d1ccf19192d7109ad3ad9b7e01a8db7ebf5df2fc43469  check-4-lifecycle/stands/raw-P4-3/guest/results/ro-saved-delete/before-attempt.json
9970efd2d5d8230cb1daffc5008f12c956d73424817b9f2ec0c6b3ddaa2058f5  check-4-lifecycle/stands/raw-P4-3/guest/results/ro-saved-delete/meta.json
8fed20a21be9ed6285c2933b39913e45d2fffecd884f57b61bc46319112cd732  check-4-lifecycle/stands/raw-P4-3/guest/results/ro-saved-delete/transition.trace
18fddeedf7d50053f71a968a1155ff8cd5cfa396de8aed0c35ba9d6f8cadd301  check-4-lifecycle/stands/raw-P4-3/report-data/selected-matrix.csv
522e4df57470d31046fae29641fd26eabb2ed8498f67f601cb3dfa616042bd5e  check-4-lifecycle/stands/raw-P4-3/report-data/summary.json
47e425e9bccda107789bf929518fa63da1e238b559417f30691e3a3b61bb3396  check-4-lifecycle/stands/raw-P4-3/src/analyze.py
8d12a98e992ba4b8da5f788966da71f3a8d06f9c542608a847cbf30ae71c71f9  check-4-lifecycle/stands/raw-P4-3/src/payload.c
ff17f139394c9abaa160deadf03f2b5a4f65fb8afb6af4644f9413c382c54e17  check-4-lifecycle/stands/raw-P4-3/src/snapshot.py
faa14798c6ac8991134cbd4cf64339f4f903133e473e2b1ba142291516263d9f  check-4-lifecycle/stands/raw-P4-3/summarize.py
1a1a4e14aa3ad29ca76ec98baa712a94b2043bb5059da3ca9818b85d89fb9c0c  check-4-lifecycle/stands/raw-P7-1/post/execution-statistics.json
e4d7ca4ef37a5180955fb9b195b8f2a422d81be9e6c98ecd5563a45dd5361460  check-4-lifecycle/stands/raw-P7-1/post/execution-statistics.py
d8e630dca69be05dc22da86ea2e09e374cac422f9f562fb1472d0698af2e6ba8  check-4-lifecycle/stands/raw-P7-1/post/final-counts.json
ac98c531ac8e276d85cbee1a1bbb43670af43f67ea4c3f73ef950e43958af37f  check-4-lifecycle/stands/raw-P7-3/analysis/final/matrix.csv
bed70536409f4534f83c6ac9fef166bae5327ad919d7004e49bdb2f38af14d97  check-4-lifecycle/stands/raw-P7-3/analysis/final/rows.json
cfd525a2727198a79c12b9ff1afba341de6ac383e9bcf159c78eb898b495e28a  check-4-lifecycle/stands/raw-P7-3/analysis/final/summary.json
5ee60c9808002da38df26dcfb668ac6bb80d6727e448885d32e692a51e4a5b6c  check-5-authority/stand/Q-AUTHORITY.md
7a20d228ca8428306b310e400456df8fbe81a9d96e03ba00807af4e499465723  check-5-authority/stand/raw/q/authority/check-authority.py
0778eb046f74b6c5d2276e826415f20e2acbf4590ce6761e8f1feaaab1d3367f  check-5-authority/stand/raw/q/authority/final-owner-apply-policy.py
e1510fe7cb724edaff9ac52a8b59bde9b6ef7d5dd5d351a7c24141f3789f7f3d  check-5-authority/stand/raw/q/authority/final-owner-authority.jsonl
0eb1796f7ae636db4427801aab67c4ff335398b4a8f18aa251d7d4c3b6838722  check-5-authority/stand/raw/q/authority/final-owner-cald.py
eb636aa96d8e5f76720164272d9e84753ebabf3aadb5c89553ad0c1cbefccc61  check-5-authority/stands/P2-4.md
1c9052b7a7efdf55fc591aee42492664135cca260e54f267b3b09fe52c04ea12  check-5-authority/stands/P3-2.md
7d65649aa42af10c9d755f81c7f8128cb806a907b85670c5e8cfbd28faff6987  check-5-authority/stands/P8-1.md
fdff21b684549eece4558cfededd858813d79e95cb562e99348078cd26d3b0c3  check-5-authority/stands/REVIEW-P2-4.md
c363a970befa9441c32ceef5f3c10704caa2edf8d4487ab807796cd728d7e573  check-5-authority/stands/REVIEW-P3-2-2.md
115c47737c2837cad47412ac2b961e78239d829bb73ced3c195f52d71019a4fc  check-5-authority/stands/REVIEW-P8-1.md
0029f709cb9cf720cebec2ce952a1c204efa7cc6c57499198909f29906596086  check-5-authority/stands/raw-FX-P3-2-1/run-1/analysis.json
926af38a0d6e33ca762a988f1da6c042d20dae1f9e84b1df414405c9d91936ef  check-5-authority/stands/raw-FX-P3-2-1/run-1/matrix.csv
6a2310a6607fb0358ac62c59b2b9f6e47644b9f649390a893f271a496da0f1ee  check-5-authority/stands/raw-FX-P3-2-1/run-1/review-evidence.json
e0bf35f027beb50a0ff76b7e608f40a510f1f0034966fdf9c074bd4be4bd4083  check-5-authority/stands/raw-P2-4/analyze.py
f7d48e7383536b8c394311e54146bfc28c675e856008611b0baec90c8815d844  check-5-authority/stands/raw-P2-4/authority-matrix.json
f721a0d3eed6694d92a9d42434f2d326c46a34101780a1b719c2a0cf151bb42b  check-5-authority/stands/raw-P2-4/evidence/summary.json
55aa56b1ccec1282f2fd2b4e5a7daef0a757b7858055404b7652c086ace34b18  check-5-authority/stands/raw-P3-2/server/results/D-IP/meta.json
c46409390e175f2a7d30f2d323065d02cc405340159dc1830e6debe191d885aa  check-5-authority/stands/raw-P3-2/server/results/D-Qxy/meta.json
48a4d4d8b667091a7cad76f769c6d5c16c7e443a219475c07ebd4874c4fb9f6c  check-5-authority/stands/raw-P3-2/server/results/D-Qyx/meta.json
0e90cbf604c8b60e1b501396c0c45d227b9008a6a1a8edb0ef79a1cff16b402e  check-5-authority/stands/raw-P3-2/server/results/D-Sxy/meta.json
c2591d014e37620603351e04be96a4fb60874050b35eb1fab313ee8b4bf86870  check-5-authority/stands/raw-P3-2/server/results/D-Syx/meta.json
f8e0642a971d4a6902b8a64dfddaa93353aebadb3f057c24dac2125615d72298  check-5-authority/stands/raw-P3-2/server/results/F-IP/meta.json
3caff47615023648095ae4e8a03678e05924e79b5202a7d36b5b541049c14723  check-5-authority/stands/raw-P3-2/server/results/F-Qxy/meta.json
880fa7ba6d5d83c23208c07d930dd5478ab016b5f4393d7471dac50e9335346a  check-5-authority/stands/raw-P3-2/server/results/F-Qyx/meta.json
253fbf96fdb790be4b5320b9db3c30434aa0af12df173b180632d512ec44b2e0  check-5-authority/stands/raw-P3-2/server/results/F-Sxy/meta.json
6650ecb92de364d21ba54eaabf702ddeb0009d15a1fa79a8bb44990c49c924b8  check-5-authority/stands/raw-P3-2/server/results/F-Syx/meta.json
e33eca90047ff11ad634bdf2edc72be4ed946eb896c10f20317ccf5591f4bb16  check-5-authority/stands/raw-P3-2/server/results/I-IP/meta.json
8410baf66627e289b9a1a50dcc0cce324e1f7eacaa6eaaebfa628acd27f07b3c  check-5-authority/stands/raw-P3-2/server/results/I-Qxy/meta.json
9d2b2f0b6942eeecbf0fad815d7b6ad2ab93fca07326c6aba87cb970b443b53f  check-5-authority/stands/raw-P3-2/server/results/I-Qyx/meta.json
bc162afb04100d0cf423a2c5ff353e1ae242506784237802a3015d3988f873d0  check-5-authority/stands/raw-P3-2/server/results/I-Sxy/meta.json
a623d8d8a6482a4ddd56d9336f80b0203ac9220eb031551a236160eefb8e5b00  check-5-authority/stands/raw-P3-2/server/results/I-Syx/meta.json
25345ef80ab1aab08e90351874569bcb82246301ad2d13e0fd6316554854e924  check-5-authority/stands/raw-P3-2/server/results/N-IP/meta.json
7d079858870097f09e0b43eafb0391e9f070edd263223103fd567c281613b95b  check-5-authority/stands/raw-P3-2/server/results/N-Qxy/meta.json
9548646d8885d97bcd119f9924d157e6b2c873f5ae78d083c384b2d2e341dae6  check-5-authority/stands/raw-P3-2/server/results/N-Qyx/meta.json
5ca8e4168c637d3c47223da0a31d9e559b2c76281a40354586091eb8285680aa  check-5-authority/stands/raw-P3-2/server/results/N-Sxy/meta.json
579284d3417ea5a45546506a8d07f2fa6a30079b3621fbc3e5e758e080bd0ea4  check-5-authority/stands/raw-P3-2/server/results/N-Syx/meta.json
51ac26461844aa3f3661e64513a626405d515a13b61fee93f3eb1d2c85b8f7ed  check-5-authority/stands/raw-P3-2/server/results/control-D-Sxy/meta.json
d444fe947d57aa064a40b370424eef4fb2276dc408842e5bc7c7879283425148  check-5-authority/stands/raw-P3-2/server/results/control-D-Syx/meta.json
96c1cad700bb1691325d23e8b91aadbc12cafb09c58ece8cf87bc4227e103dc1  check-5-authority/stands/raw-P3-2/server/results/control-F-Sxy/meta.json
f39209c5e33c59ed2cb7e1a0bdb244dd629f62320503415a98f953964909f567  check-5-authority/stands/raw-P3-2/server/results/control-F-Syx/meta.json
4ed8d6bfa4b2773a1b4fa0558703773ca78294c7e4e314b00a8d0f51eb1503bb  check-5-authority/stands/raw-P3-2/server/results/control-I-Sxy/meta.json
72e1f149515b091fc59924aad76dea7b92e3a47baa11ac9b3f6f84cd0f4990c1  check-5-authority/stands/raw-P3-2/server/results/control-I-Syx/meta.json
c41a5890d6e5839c95567aecd0aae0ed02ae59282ae74777d1fab6c9b0b8ca1d  check-5-authority/stands/raw-P3-2/server/results/control-N-Sxy/meta.json
b2e8bd3b73df2ab653bb2af2a7f9f88caaaf7d222a6b8fac1c63d2f57dc2e536  check-5-authority/stands/raw-P3-2/server/results/control-N-Syx/meta.json
412fde77f5de16787505e90c9a1f132038209d42a0f01182ad0093dae06ef489  check-5-authority/stands/raw-P3-2/server/results/control-comparison.json
6fd022b9ea59029aabaa14550224d8758d5b64d4b42efda17a0b26d965e1a72b  check-5-authority/stands/raw-P3-2/server/results/replay-D-Qxy/meta.json
ea2bc36b2cb086cbf60375b6f59a979556ad5ccac41374d30eb576054ceb0bb4  check-5-authority/stands/raw-P3-2/server/results/replay-D-Qyx/meta.json
f250fbcf7ab71cab69d63976c684a7adcb297b4fd1172ee4e48d661a3afb7740  check-5-authority/stands/raw-P3-2/server/results/replay-F-Qxy/meta.json
db84a42a675edbdb86955a31e8fb5977e47b19b297325f563236a34f39d61ea7  check-5-authority/stands/raw-P3-2/server/results/replay-N-Qxy/meta.json
8753d3deaaf9207107dcb04c13c4310ea391798c07341dce9daa5cffbd9b3294  check-5-authority/stands/raw-P3-2/server/results/replay-N-Qyx/meta.json
8749416f11bceee7146490d50b0e1730488235f6b06570ca1e0b7020ebd48829  check-5-authority/stands/raw-P8-1/candidate-premises.json
ff7d96016fc2b931751e46c8407641981be0db78df0a3b7dd9c263e2cba1f4f0  check-5-authority/stands/raw-P8-1/matrix.json
fbedf3ef2ad0d18f8bb4970a1228daa8f0318f55830ff058c157c81840d7e6ee  check-5-authority/stands/raw-P8-1/server/BQ/analysis/independent/summary.json
a6dc4a8d2ecbf663afe056a8b6da1b3583e97a16a219bf10e65c72b622ec6ba6  check-5-authority/stands/raw-P8-1/server/BQ/analysis/summary.json
f416598e25096dc0d2116d8640c824c7589a8a56675e396c977f6b3281123545  check-5-authority/stands/raw-P8-1/server/X3/analysis/independent/summary.json
14b74566e8ccc9d74093722abdd220d6b93e7c22ed6dae31e0d2d833976b8395  check-5-authority/stands/raw-P8-1/server/X3/analysis/summary.json
0cc8da82193075676ce7bdf0407fa00a500cccdf5fc679c6669a63723139c395  check-5-authority/stands/raw-P8-1/timing.json
b4c9829d6e3ff95a40ef32d6a7f70ebad4762d929ba9dcfe72537ca46f5fdd8c  definitions-analysis/documented-objects/ATTACK.md
f463f263dc94c8169abd067e82a8cff3772fcd3f1d883465e9d332be929feb56  definitions-analysis/documented-objects/REVIEW-2.md
1c49c7dc7a3be70da98901999af4858ffe62ce6ccaf23c46ba2d50f6c00a5b72  definitions-analysis/documented-objects/SOURCES.md
b7cc72303e0ab7ac859c38c855cc24c46d3c15a487d6748b375393825642c08f  definitions-analysis/formal-and-literature/RESOLUTIONS.md
01fcc90f1ad14faa75a2b2a7040d15b9a0bd32bd9348951cee207df6aa2dab04  definitions-analysis/formal-and-literature/REVIEW-X4-2.md
6099e771b33733ea6647086ae3c0c12f67bb1bf461ced512ecb96a60f315d229  definitions-analysis/formal-and-literature/REVIEW.md
8302f824bdb83ab0f1111483f9ec61892836ff222ff4585ff6847f32fb12eef8  definitions-analysis/formal-and-literature/X4-FORMAL.md
a3e58a9e192e4ff2bfe285dc0d24d0a8ba405b9edb0cf8c221fea69da84200df  definitions-analysis/formal-and-literature/X4-model.py
4bb07f85bfdeaabba65e8deb117ecc222d748651ed5526284666f4bb3e6450bd  definitions-analysis/formal-and-literature/X4-requirements.txt
ef9ffb427e2b542c4bdca36be9bdbce44a5bda493c9ad06a289e0aa3bcf058dc  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/pair-matrix.md
b02deba2ed64b2726234c516dc3a26ed0070355b1bbefd0183910937160b0cfc  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/BRANCH-immediate-delete-saved-internal-P6-conflict.json
81ed2ca410a10d432271a1132b375ff87c13162646868eb48a84bb02b15fdce2  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-bypass-no-permission.json
6f750984eb49835ccc4929c11c025c69c2d34026c4c532abd1e95fecf7dffce6  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-historic-archive-historical-scope.json
7d93bc1c8dc4cf751cffb22b3eca0a9635e84b3c9e82d033da27ab5ef6bb42a5  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-historic-archive-joint.json
7489e3a9da45e0ae88a857690f5b6b7a5af26c9a60cafbca3654d8e0ece68631  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-ordinary-unix-joint.json
a5c06f7b27c195771ddd0eb8d5370a685c8cd7c1da5173a909f120d0c1f82c9a  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-overstrong-personal-joint.json
504f10c601321f7a311169bfbcad38c19112c997b0bc60a0e7986bf5e92cdf35  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-data-completion.json
2e1a00c97958c5183667592648f30fae1a63795f6f99a5f5926f46db1cb96ebc  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-derivative-completion.json
b3bd39ba289817c7723dad4b04cb0563581764bb93ae65d4e50f8619c8ec845d  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-no-attempt.json
97486513cfdc2de9fd52df198d3e056459ded55942ca050dd7c62c5c52a357a5  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-no-class-joint.json
b0aad24ec2fb750f80d3b902b22970d54c0b1fb3be9a0d9bb85e2612529a6c04  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-separately-recorded.json
ab3111298ab272418ef6e3666d812488451ab869fe9d3b2db936391c9addd290  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-launch-completed-delete-joint.json
02ae93a84b38e008b5b9243a15c58199e4ea5b7a32d4854c35ccc5150ee9aaaf  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-launch-delete-not-completed.json
5db751178e9f90c18feabb2c09c50e173fa9b055732cb573079da9b21af1f4f2  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-permitted-launch-keep-archive.json
3dd6e73e01a458f98f9d4fa237a4666ddd2bfb22007befa764bdc2388b047f7c  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-recorded-delete-joint.json
e4cfd33668a1c6a3806909a0308359795ebde115dbaf6d9546f23f233c513db7  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-root-program-joint.json
fbbe6862e36a70408a2e7764be77a59e5ce5bf135df35defb3ae5f04f8a86862  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-shared-needer-broad-eligibility-BRANCH.json
d558f739c5ad80aebbc7852b613cb04fba230d1424cab0c9a0e9257edf548e4f  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/canonical-shared-needer-direct-origin-eligibility.json
46da6e7d7357e7ceeada69681480e2702f191a8d0ae6ad1439b0665c65470573  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/class-conflict-retain_recorded_derivative-recorded-derivative.json
4a96665368c8601e9c6585b6693a9ef768040c9e000e64af5ccf44d0d83bbc3d  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/epistemic-editor-code-0.json
23b49a6a1407360c0bfe7d1c21993c811af6c1de978688c5bfdad8acd57628e7  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/epistemic-editor-code-1.json
fd063dec775df68faaa7b5d4b54ef4256b7f42634e6534a72af83a3205788e81  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/explicit-bypass-none-P1.json
392e4388522c910107772a84bba9cffaedefb8bdb5fa3cd331f641f75ae8e158  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/explicit-bypass-none-P3.json
a22adbfcb7d9a05ba9588269c49f6991932faf438e909018a92cbfbb3b710843  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/no-class-closed-predicates.json
06e180630e69f22465ac66b4d4770699f852a5ea2d8e5da3af711c10a66ae482  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/queries/overlap-derivative-data.json
93ecfcc8b5ee4bdab3e1feec162bb45daa59b34913c03971d786c372bad30415  definitions-analysis/formal-and-literature/raw-X4/fix-001/run-006/summary.json
e69787144830c2706952b1c29bd2a4297b0d03d8e302402826513d10865d93a1  first-paper/PAPER.html
c38f596c76f746010ecbc8b6c868f0159ea5f30e96d84031ec43f7f05baf8bfb  open-problems/apply-crash/P4-2.md
aa6081c1cbfffd859fe3dd6eb12e4ae3de5663bec17b665d2fc16388990aa77b  open-problems/apply-crash/REVIEW-P4-2.md
ca4c89fe6b6abb3f018146df6173ba771b8da302c1593fa38f3e70f6541e1075  open-problems/apply-crash/raw-P4-2/analysis.json
d8e7e3761602009545039c6954a5e52e3c827410b96314696b1282261d344eea  open-problems/apply-crash/raw-P4-2/matrix.csv
7597b1b1c8bb13cc083b8cd438e2ba0c8542077a9c161ffe4836547c3cf71a90  open-problems/apply-crash/raw-P4-2/recovery-facts.json
b994c7fda8f95c77b378b3eb4c87ae0f9829b24997fd7b9420d6e286ae9cf408  open-problems/apply-crash/raw-P4-2/server/results/B-delete-immediate/meta.json
9d18b9e9a078398f9845aa4170b6fd46b54b7fcd45bb64e81cd11ae00391c836  open-problems/apply-crash/raw-P4-2/server/results/B-delete-nocut/meta.json
16679b29a76eed26b74ccace7272ae60f16ca08184ed0d33dba48ea8e9e84ecd  open-problems/apply-crash/raw-P4-2/server/results/B-delete-reboot/meta.json
1ff7f54c75673df4ffb02dcd4f995e29f27fb27ce19ede46c15bb687e001daec  open-problems/apply-crash/raw-P4-2/server/results/B-delete-sync/meta.json
94cd6ddad217cfd26dba3f397229bce24c550303ff459880fe640b9ba88feb65  open-problems/apply-crash/raw-P4-2/server/results/B-keep-immediate/meta.json
7939ecb181503229815f8a648e92e38c3eb8965ad74e8044ce55efeec938869d  open-problems/apply-crash/raw-P4-2/server/results/B-keep-nocut/meta.json
15525dc98a06b9c0dc186b15e4a125af44d33060334d5560d031f0e4e1f88758  open-problems/apply-crash/raw-P4-2/server/results/B-keep-reboot/meta.json
54e3e5dee6f7b057ca488cc08126c5ae4e6aef89266eb0d3eb3f574cde64cb42  open-problems/apply-crash/raw-P4-2/server/results/B-keep-sync/meta.json
6678d91c9e0fe48fabdb5add39339cbe01094660b495bea9f35050e532cb2d07  open-problems/apply-crash/raw-P4-2/server/results/G-delete-immediate/meta.json
eb8e1fee784bc37439a4cca7b448ebd7089531986044b6e43f1ade7bce708dff  open-problems/apply-crash/raw-P4-2/server/results/G-delete-nocut/meta.json
db19578c840f468e6300b88d052b302d2c6e7f40916ada02e57d9ec7ca8673a2  open-problems/apply-crash/raw-P4-2/server/results/G-delete-reboot/meta.json
30d99e3de469587d2b4c14cbcb5b3b9e698135db7bbe962c31c0763987a86694  open-problems/apply-crash/raw-P4-2/server/results/G-delete-sync/meta.json
a7eef558b58368f8f03eecd38dd8a3853da39714fe717740f542573535cf7900  open-problems/apply-crash/raw-P4-2/server/results/G-keep-immediate/meta.json
7f188a934369a3c16670577ed8c7eacfe5d4a623fafbe81ff1c34d274b1ee2ea  open-problems/apply-crash/raw-P4-2/server/results/G-keep-nocut/meta.json
abaade17fa382815900ffeed3414611cd9b7aa686170103c312e6870f6e52ef2  open-problems/apply-crash/raw-P4-2/server/results/G-keep-reboot/meta.json
1de6420c7c598f6b7e02a52ea0761a9e1752e9a4b58c8d932232bcc798ec31f3  open-problems/apply-crash/raw-P4-2/server/results/G-keep-sync/meta.json
1c11ecfd8fdf9c6f924ddbf36a9ca814c1774af7e6a51c50b10499a6b7fb2cb0  open-problems/apply-crash/raw-P4-2/server/results/R-delete-immediate/meta.json
8e813bb33503056ba6d701dbb007cb89515cbc49b5dcc1f8da7720594009118f  open-problems/apply-crash/raw-P4-2/server/results/R-delete-nocut/meta.json
5e633a424221dae0404509f78834c486cda7094df2e478e83406eafa3b8a2e57  open-problems/apply-crash/raw-P4-2/server/results/R-delete-reboot/meta.json
972cdd7bb1f35babf8343109ab28daeb7b39bb1ef44fae97b98deddb21520b0a  open-problems/apply-crash/raw-P4-2/server/results/R-delete-sync/meta.json
0af1a1ac86beb85fb2798c1df2959bdc265ee2280baa1e8a709fadcc82a7b0a5  open-problems/apply-crash/raw-P4-2/server/results/R-keep-immediate/meta.json
2d33ad4285572385f664f067cd6750058aab1fc01752ec26e3c052656ff8147e  open-problems/apply-crash/raw-P4-2/server/results/R-keep-nocut/meta.json
1ac94343af0b876dbb45ba4256f915f5085837960fd0684c06e867ab8fa13c32  open-problems/apply-crash/raw-P4-2/server/results/R-keep-reboot/meta.json
39db5421e7cdde0ef6062bf71ee7f6cd93ce573814e79a47b937ce64bca016b2  open-problems/apply-crash/raw-P4-2/server/results/R-keep-sync/meta.json
8c569a2831383f9566c62dfa5674ee70246b773a37f37308c9d99ee188bc05b9  open-problems/apply-crash/raw-P4-2/server/results/replay-B-keep/meta.json
5e3198640a7751327f3fd460189fa4797e1f88eb2010571182485c33ba3f7ef5  open-problems/apply-crash/raw-P4-2/server/results/replay-G-delete/meta.json
6d30f8fd52b7165c74ba21fa364ecf74cf24754fcdde6e94d7f98613ab43da26  open-problems/apply-crash/raw-P4-2/server/results/replay-G-keep/meta.json
691eda83cb363611cd47cfd67c4da3ae3a1154af05a9f5430d310fc68fb13269  open-problems/apply-crash/raw-P4-2/server/results/replay-R-keep/meta.json
cb2e961c40bb003cbbf3e42c6ce4929331883d246fca16fa2de17fb94809f69a  open-problems/apply-crash/raw-P4-2/src/run.py
ce3b8e2ee4d203d3461994ab84a9d3633fc4711b8720b89d6bdf8179f3005108  open-problems/apply-crash/raw-P4-2/src/verify-evidence.py
f46ed090723ece8aa73c44ab4bd570e63a0cf4f2349b1618b7f05282cf36333f  preregistration-v3/configuration-as-law-v3.pdf
b0c9627bc35f2123e5fd880bb4f3b003bf775c411bd3a76f87ace481cf739532  preregistration-v3/prereg-en.md
```

Files listed: 925.
