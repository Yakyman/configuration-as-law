# Transport rehearsal preparation

2026-11-23 UTC. Pending release by the coordinating task after check-1 work. The current fx-run.py creates a fresh overlay, runs 20 fixed `exit 0` calls, skips actions and collector for this system, and destroys the clone with kill/destroy fallback. Commands run in a durable user unit and the laboratory runner holds numbered slot locks.

Expected result before round 11: fresh boot succeeds; all 20 consecutive transport calls return 0 without timeout; cleanup removes the clone. No inventory command runs and no guest output is read.

NixOS uses the registered SSH transport and retained clean installation described in LAB.md and KIT-READY.md.

Round 11 passed: create 0 in 23.469 s; all 20 consecutive calls returned 0 in approximately 0.19 s each; destroy 0 in 1.533 s; whole run 28.814 s. No actions or collector ran. No stderr file or guest output was read. Evidence: status.tsv.
