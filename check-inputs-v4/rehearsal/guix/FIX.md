# Guix transport repair result

NOT READY after four new fresh-clone rounds (11–14). No hypothesis outcome is assigned. This check-4 rehearsal ran no actions or collector and read no guest inventory.

| Round | Create | Transport sequence | Cleanup | Whole run |
|---|---|---|---|---|
| 11 | 0, 26.165 s | calls 1/3 failed, call 2 passed; old sequence interrupted | explicit kill0/destroy0 | not claimed |
| 12 | 0, 9.42 s | first 2 passed, call 3 READY timeout; fail-fast | destroy0 | 31.35 s, failed readiness |
| 13 | 1, 242.241 s | no sequence; initial TTY timeout in boot readiness | native destroy1; kill0/destroy0 | not claimed |
| 14 | 1, 242.013 s | no sequence; shell-SYNC and wrapper-chunk timeouts in boot readiness | native destroy1; kill0/destroy0; clone absent | not claimed |

Evidence: status.tsv and counts.tsv; every diagnostic read is named in DISCLOSURES.fragment.md. Historical rounds 2/3 were synchronized as numeric records; their final kill/destroy cleanup succeeded.

The original serial transport had inconsistent frame/login timeouts. Repairs now require an exact unique shell SYNC challenge after a candidate prompt, certify echo suppression, stage the receiver in short acknowledged chunks, check complete receiver and payload SHA-256 plus decoder status, preserve trailing newlines, require the exact final ACK, and certify tty restoration before CLOSED. Input is paced one byte every 10 ms; complete fixed-call wire traffic is 2699–2701 bytes (about 27 s nominal transmission under the 60 s timeout). No guest configuration, installed software or frozen choice changed.

Independent source review accepted the complete repair. The five slow-pacing synthetic PTY scenarios passed: exact 0/37 status preservation, corrupt receiver rejection, corrupt payload nonzero, wrong ACK rejection and initial stty-failure rejection. The final shell-SYNC delta preserved 0/37 and rejected a suppressed challenge. Evidence: serial-fixture.json, serial-sync-fixture.json, and FX-INSTRUMENT-REVIEW.md. These establish protocol correctness on the synthetic fixture, not readiness on the real guest.

What remains: live guest serial login/delivery is unreliable. Numeric metrics locate failures, but do not establish an underlying UART, shell, terminal or guest-service cause. No raw console was read. No fifth round was run and no ready claim is made. LAB.fragment.md describes the repaired protocol for the shared kit documentation.

Final round-14 cleanup completed: native destroy1 after153.003 s; kill-fallback0, destroy-fallback0. `cleanup-final.tsv` explicitly confirms the clone is absent. All four fresh Guix clones have been removed.
