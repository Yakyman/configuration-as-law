# Transport rehearsal preparation

2026-11-23 UTC. Pending release by the coordinating task after check-1 work. The current fx-run.py creates a fresh overlay, runs 20 fixed `exit 0` calls, skips actions and collector for this system, and destroys the clone with kill/destroy fallback. Commands run in a durable user unit and the laboratory runner holds numbered slot locks.

Expected result before round 11: fresh boot succeeds; all 20 consecutive transport calls return 0 without timeout; cleanup removes the clone. No inventory command runs and no guest output is read.

Guix uses the registered original serial transport with passive_boot_login=true; no SSH reconfiguration is attempted. The KIT2 record documents that native stop may fail and kill/destroy fallback is authorized. Source: install/guix/KIT2.md, KIT2-READY.md and LAB.md; primary manual https://guix.gnu.org/manual/en/html_node/Base-Services.html documents serial agetty.

Round 11: boot succeeded; transport calls 01 and 03 failed with a framing timeout, call 02 succeeded. The old harness had not yet gained fail-fast, so it was stopped after failure; unit stop, explicit kill and destroy all returned 0. No whole-run success is claimed. The read diagnostic transport-01.stderr says only `lab: Serial timeout; VM retained`.

Before round 12: the serial wrapper now first disables terminal echo using a short unique handshake, then sends its long command. It preserves the authenticated login shell and waits for a final CLOSED marker after ACK and tty restoration, avoiding a close/logout race. The current harness aborts check-4 transport on its first failure. Expected result: all 20 calls complete without a framing/login timeout, followed by cleanup. Source: https://man7.org/linux/man-pages/man1/stty.1.html describes `[-]echo` as “echo input characters”; echo suppression cannot act retroactively on the already transmitted wrapper line. This is an instrument repair hypothesis, not an observed guest-content diagnosis.

Round 12 returned 0 on calls 01–02, then a READY-stage timeout on call 03; fail-fast aborted the sequence. Destroy returned 0; whole run 31.35 s. The short tty handshake had succeeded, so the long wrapper delivery remained the instrument failure point.

Before round 13: stage the wrapper through 128-character base64 chunks with individual acknowledgment; verify the entire encoded wrapper with SHA-256 before checked decoding and eval. Verify the encoded payload likewise before checked decoding and execution. A sentinel preserves trailing newlines through command substitution. Exact ACK and successful tty restoration gate CLOSED; initial stty success gates TTY. No file or package is created inside the guest. Bash's built-in `help eval` documents execution of the supplied argument as shell commands; checks precede that execution. Coreutils base64 and sha256sum are required transport tools, never installed by rehearsal. Offline synthetic fixtures test fixed exit statuses and corrupted protocol cases before the fresh round. Expected result: 20 consecutive calls return 0 and cleanup succeeds.

Before the final fixture rerun, the wrapper digest check and checked decode were split into separately acknowledged short commands; the final eval line is short. This preserves validation while removing the remaining long interactive setup line. The independent source review accepted this exact split. Synthetic expected results remain: 0/37/0/37 preserved, corrupt wrapper rejected at wrapper-hash, corrupt payload nonzero, wrong ACK no CLOSED, failed initial stty no TTY.

Exact final-source synthetic rerun passed all five scenarios (`serial-fixture.json`). Fresh round 13 launched after source review and fixture success; the deployed shared kit has only the serial branch repaired.

Round 13 boot's numeric metrics showed repeated login/password prompts and then a TTY-stage timeout. No console content was retained or read. Source investigation: QEMU's 16550A implementation defines `UART_FIFO_LENGTH 16` (https://qemu.googlesource.com/qemu/+/5d7a40b5b280cd82f24a9b4e5f4557e200111030/include/hw/char/serial.h). This makes reducing burst size a plausible transport repair, but does not establish that overflow caused this failure. The registered original guest declaration requests 115200 baud (`install/guix/original-config.scm`).

Before round 14: measured complete wire traffic for fixed normal calls is 2646–2648 bytes (`serial-wire-size.json`); this includes all chunk/handshake shell syntax. Slow serial writes to one byte every 10 ms (about 26.5 s transmission per call), leaving margin under the 60 s transport timeout and under 30 minutes for 20 calls. No extra retry or weakened certificate is introduced. Expected result: login and all 20 certified calls succeed without UART burst sensitivity; if not, retain exact failure and destroy the clone. Synthetic correctness rerun uses the actual slow pacing and the same five fixed cases.

Final source review also identified that a suffix ending `$` or `#` is only a candidate shell prompt. Before TTY setup, the transport now sends a short unique printf challenge and requires the exact SYNC line; echoed command syntax cannot satisfy the anchored line. A delta fixture is expected to preserve 0/37 and reject an intentionally suppressed SYNC. This does not claim the observed guest actually had a false prompt.

Round 13 cleanup completed: native destroy 1 after 165.246 s, kill-fallback 0, destroy-fallback 0. No whole-run success row is claimed after create failure. Evidence: status.tsv. The clone is removed before round 14.

Slow-pacing five-case fixture passed (`serial-fixture.json`); final SYNC delta fixture passed normal 0/37 and suppressed-SYNC rejection (`serial-sync-fixture.json`). Final wire totals are 2699/2701 bytes, nominally 27 s per call. All retained synthetic outputs are predetermined status/fault categories; terminal transcripts were discarded.

Round 14 create failed after 242.013 s. Numeric metrics include shell-SYNC and wrapper-chunk timeouts during boot readiness; the retained read create stderr is only a generic boot/login timeout. No 20-call sequence began. Four new fresh-clone rounds are exhausted; Guix is NOT READY. This is a transport readiness failure, not a hypothesis result. Cleanup is recorded separately when complete.

Reproduction entry points: `python3 C1/rehearsal/guix/serial-fixture.py` for the five protocol cases; `python3 C1/rehearsal/guix/serial-sync-fixture.py` for the exact two-case final SYNC delta. Both use only local synthetic PTYs with startup files disabled and fixed commands, never a VM inventory.

`deployed-source.tsv` records the final round-14 lab.sh hash after verifying local and deployed bytes match and that the source was unchanged since launch. Earlier round-specific source hashes were not captured; this final hash is not attributed to those earlier rounds. The chronological repair notes and synthetic result versions distinguish their source states.

Final round-14 cleanup completed: native destroy1 in153.003 s, kill-fallback0 in0.329 s, destroy-fallback0 in0.03 s. Explicit clone absence returned0 (`cleanup-final.tsv`). Final status/counts and diagnostic files synchronized; unread diagnostic replicas remain unread. The coordinating task was given phase GO immediately after confirmed removal.
