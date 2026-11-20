VERDICT: AGREED

Reviewer: independent of the executor, 2026-11-19. Scope:
- The shared rules of the checks, plus PAPER §5 and §9 (§9.1, §9.3).
- P/P3-1.md after fix round 1 and P/FIX-P3-1-1.md.
- The previous review P/REVIEW-P3-1.md.
- Data files cited from P/raw-FX-P3-1-1/ (ADJUDICATION.md, adjudication.json, MATRIX.md, analysis/cells.json, runs.json, verification.json, integrity.json, raw/protected-before.json).
- A sample of 5 claims from P/raw-P3-1/evidence/.

Headline: BQ stand `1`, X3 stand `0`, Check 2/P4 hypothesis `?`. It follows the fixed conditions.

1. **Previous finding 1 (x3-absent scored `?`) is handled.**
   - Where: P3-1.md row "Absent → A" now reads X3 `0`. ADJUDICATION.md and adjudication.json `rows` show x3-absent `0`.
   - Under §9.3 ("explicit permission through a line in the declaration does not take effect"), this is a stand trigger.
   - Under §9.1, the hypothesis stays `?`: the cause is an implementation gap, and there is no proof that it follows from the property.
   - The frozen protocol's `UNSUPPORTED` label was overridden in favour of the paper's own condition. That brings the result back into line with the fixed condition. It does not add a new rule.
   - No fix needed.

2. **Previous finding 2 (§9.3 clause 3 on the EBUSY rows) is handled.**
   - Where: P3-1.md, paragraph "The immediate post-directory denial…". adjudication.json `holes` has 3 entries, each with `ordinary_action_clause: "? — untested"`.
   - Evidence: in evidence/x3-atomic/events.jsonl:8 and evidence/x3-recreate/events.jsonl:8, the actor has euid 0 and errno 16. So these were root setup mutations, not an ordinary-person action. Recording "untested" rather than a decision is correct.
   - No fix needed.

3. **Previous findings 3–6 (confirmations) still hold, and the corrected texts do not contradict them.**

4. **Numbers match the data.**
   - I recomputed from analysis/cells.json: 104 cells (bq 48, x3 56 = 48 + 8 replay). All 104 have uid/euid 1000.
   - Every row in the P3-1 table matches cells.json: BQ and X3 S0/S1/fresh (=O0/O1/F), reapply R and revoke V, for all 6 trajectories.
   - BQ: 6 U + 2 ENOENT (bq-absent D, G) + 40 confined = 48 ✓.
   - runs.json `apply_ok`: everything is true except x3-directory and its replay (reapply/revoke false). This matches "both ACK false" and "All BQ reapply ACKs succeed".
   - verification.json: total_launches 104, audit_correlated_cells 104, all_assertions_passed true ✓.

5. **Integrity claim is independently confirmed.** I re-hashed all 3,388 files listed in raw-FX-P3-1-1/raw/protected-before.json: 0 mismatches. That list includes P/REVIEW-P3-1.md and the raw-P3-1 tree.

6. **Sample claim (a) is confirmed: the grant before creation is effective in the declaration.**
   - evidence/x3-absent/grant.ack.bin: `"ok": true`, effective `allow_channels: {alice: [download]}`, generation 2.
   - grant.request.bin and reapply.request.bin are byte-identical (`cmp`), so "reapply with the same declaration" holds.

7. **Sample claim (b) is confirmed: fresh F is denied while U runs the same A.**
   - F.launch.bin: `/home/alice/downloaded: Permission denied`, RC 126.
   - U.launch.bin: `P31_NATIVE_A … uid=1000 euid=1000 dev=65025 ino=131074`, RC 0.
   - F-before/snapshot.json: the object at /home/alice/downloaded has mode 0o100755 and ino 131074.

8. **Sample claim (c) is confirmed: the policy source omits the absent target.**
   - inputs/X/X3-policy.py:34 gates the exec mount on `os.path.exists(target)`.
   - :49–53 expand `'/home/*/downloaded'` through `glob.glob`, which returns nothing for a missing file. The comment on :52 says the opposite ("No file need exist yet").
   - The realized state agrees:
     - F-before/etc__cal__x3-exec-mounts.json is `[]`, and F-before/etc__cal__x3-alice.rules has only `x /tmp/downloaded`.
     - R-before rules add `x /home/alice/downloaded`.

9. **Sample claim (d) is confirmed: reapply restores execution.** evidence/x3-absent/R.launch.bin: `P31_NATIVE_A … uid=1000 euid=1000 ino=131074 exe=/home/alice/downloaded`, RC 0. So the `0` is an implementation defect in when the grant is realized, not syntax that is missing.

10. **Nit, not blocking.**
    - Where: P/P3-1.md:3 still pointed to the earlier review RP3-1 and called acceptance of this correction pending (that wording is not kept in this copy).
    - Minimal fix: point that sentence to `P/REVIEW-P3-1-2.md` (AGREED). No outcome changes.
