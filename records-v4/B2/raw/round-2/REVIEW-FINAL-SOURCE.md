# Final source review before rebuilt-image observation

Recorded 2026-11-23 UTC. Reviewed the source identified by
`FINAL-INPUT-CHANGES.md`; no machine observation was performed by review.

No critical pre-launch defect was found.

- Native package membership without independent receipt remains
  `FACT_UNKNOWN`; exact installer artifacts remain the only finite received
  package provenance. Claim matching consumes the already collected census
  snapshot.
- The received default now has a concrete value-only reader in the recorded
  source and bytecode fixture. The fixture verifies the exact observed value
  without treating it as executable configuration.
- The alternate-root fixture creates its destination and preserves the actual
  package database/content/report observations. Its result is not treated as a
  successful refusal merely because a setup error occurred.
- The derived unit is source-hash-bound at admission and `unit_content()` is
  used at activation. It is independently read back.
- The final controller builds primary and peer images before three distinct
  validation lanes, joins all lanes before moving child evidence or assembling
  the complete example, and retains the child records unchanged. The extra
  complete-example rows are the four target-interpreter object rows and two
  generated-unit rows; the worker row already belongs to the carried example.

Static syntax parsing passed for `recorded_objects.py`,
`v4-object-fixtures.py`, `v4-objects-selftest.py`, and `tools/round2.py`.
This review does not close an owner. The final self-test evidence and rebuilt
recipe still require an independent evidence review. All nine Round 2 owners
remain NOT CLOSED.
