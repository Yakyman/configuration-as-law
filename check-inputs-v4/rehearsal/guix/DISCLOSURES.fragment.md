# Guix diagnostic disclosures

- `rehearsal/guix/diagnostics/fx1/transport-01.stderr`: read; only generic serial frame timeout, no machine contents.

Historical rounds 2 and 3 status/count records were copied from the lab host without reading any guest output. Round 2 failed create; round 3 booted but all 20 transport calls failed. Final kill/destroy cleanup succeeded for both.
- `rehearsal/guix/diagnostics/fx2/transport-03.stderr`: read; only the serial READY-stage timeout after the TTY handshake, no machine contents.
- `rehearsal/guix/diagnostics/serial-fixture-attempt1.stderr`: read; synthetic local PTY initialization failure before any protocol call completed, no guest facts; publication copy uses NIGHT_ROOT in the traceback.

Synthetic protocol tests use a local shell with startup files disabled and fixed exit commands only; all terminal transcripts are transient and discarded. Retained outputs contain numeric statuses and predetermined fault categories only.
- `rehearsal/guix/diagnostics/fx3-create.stderr`: read; generic boot/login timeout, no machine contents. Numeric metrics additionally locate the first failure at the initial TTY handshake.
- `rehearsal/guix/diagnostics/fx4-create.stderr`: read; generic boot/login timeout, no machine contents. Numeric metrics record shell-SYNC and wrapper-chunk timeouts during the boot-readiness attempts.
