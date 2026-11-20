VERDICT: AGREED

Reviewer: independent (RP8-1), 2026-11-19. Scope: the shared rules of the checks, PAPER §5 and §9, `P/P8-1.md`, the analysis files it cites, and 5 sampled raw claims. Locators below are relative to `P/raw-P8-1/`.

None of the findings below changes an outcome. BQ auxiliary contract **0**, X3 auxiliary contract **1**, and PAPER **?** everywhere all follow the frozen contract and the unchanged §9.1/§9.6 text. Findings 1–2 are wording/labeling fixes. Finding 3 is a clarity nit.

1. **A01's "ineligible → ?" rule was written after the cases it reclassifies had been observed, but P8-1.md presents it as part of the contract.**
   - Where: P8-1.md, outcome definition ("? for … ineligible preservation comparisons") and the "BQ adjudicated" trajectory table.
   - Evidence: the frozen protocol (l.60) defines `?` only as missing observations. `amendments/A01-verification.receipt.json` is dated 13:12:03 UTC. By then 9 of the 12 BQ `same-*` trajectories had run: their step-03 snapshots are dated 13:07:21–13:11:46 (`server/BQ/evidence/primary/same-*/03-root-fixed/event.json`). A01 moves exactly these trajectories from frozen `1` to `?` (`server/BQ/analysis/summary.json` trajectory 0:18/1:18 vs `independent/summary.json` 0:18/1:6/?:12).
   - Why `?` is still right: the frozen text cannot decide whether a rejected request "changes previously committed rights" when the peer's pre-state already differs from the committed rights. That makes these cases a definitional hole, and the shared rules of the checks say a hole is recorded, not settled by a new rule. Headline outcomes are unaffected: BQ's 0 rests on 18 corroborated events that both counts share, and X3 has 0 ineligible edges.
   - Minimal fix: in P8-1.md, call these 42 events / 12 trajectories "hole in the frozen auxiliary contract (pre-divergent peer edge)", not a contract category. Show the frozen per-layout trajectory counts (same-AB/BA = 1) next to the A01 column. State that A01 postdates 9 of the affected trajectories.

2. **The §9.6 no-list limb has no stand-level 1/0/? outcome.**
   - Where: P8-1.md §9.6 table, row "No lists: ordinary Unix permissions".
   - Evidence: `independent/summary.json` gives `no_list_unix_gaps` = 216 for both stands, and `p2.unix_native_success` = 1440/1440. The literal stand failure condition ("in the absence of lists, the user cannot do what ordinary Unix permissions allow") is therefore met on both stands. The row says only "Conditional literal no-list restriction observation".
   - Minimal fix: write "stand limb **0** (literal, 216 endpoints per stand); PAPER **?** (§9.1 necessity / P4-vs-P7 scope unresolved)". No outcome changes.

3. **Two different metrics are both 60 and read as one quantity (nit).**
   - Where: P8-1.md, A01 paragraph ("60 rejected-peer edges" → "42 `?`") and the BQ paragraph ("60 divergent post-response slots, including 24 own-request").
   - Evidence: `independent/summary.json` has separate keys: `ineligible_rejected_peer_edges` = 60 and `runtime_current_divergent_slots` = 60. 42 events = 12 at step 03 + 30 at step 04 (`report-counts.json` steps).
   - Minimal fix: one sentence saying 60 edges fall in 42 events (step 03: 12, step 04: 30), and that the divergent-slot 60 is a separate metric.

**Checked and confirmed (no finding):**
- Counts match the data files:
  - BQ events 18/342 (frozen) and 18/300/42 (A01).
  - ACKs: BQ 36 (all at step 01, rollback 0/36); X3 240/120.
  - Composition table: all 6 rows.
  - P2: BQ 1440/360/420; X3 1440/570/570.
  - Candidate conflicts: BQ 96, X3 108. List grants: BQ 36, X3 60. No-list gaps: 216 per stand.
  - Old/fresh session differences: X3 120, BQ 0.
  - Active queries 10,800 per stand, 300 per trajectory, minimum 30.03 s per trajectory. Active time 1081.513 + 1081.495 = 2163.008 s.
  - Timing 40.557 min.
  - Export 1,474 / 1,243 files, 0 mismatches.
  - Control ACK/error patterns.
- Sampled raw claims (5), all confirmed:
  - BQ `mixed-AB-r1` step 02: refusal "version conflicts with root/another owner"; Bob alpha rc 126.
  - BQ step 03: worker-failure refusal; generation stays 1795094032522431857; Bob alpha execute 126→0 with version/cache reads rc 1; mapped exe SHA cd4a6f94…; peer uid 0. This corroborates the BQ auxiliary 0.
  - BQ step 04: Bob 0→126. BQ step 10: refusal; generation S1; Alice version "1".
  - X3 `mixed-AB-r1`: ledger head 2→3→4→7; step 10 ACK, generation 7 matches the saved S1 document; at step 04 old Bob session rc 0 vs fresh 126.
  - Root mode-000 control: rc 0, unconfined (`server/BQ/evidence/controls/root-unix/result.json`).
- Not checked: raw dumps beyond these 5 samples; replay events; source code at `src/BQ-policy.py:46` and `src/BQ-controller.py:175`.
