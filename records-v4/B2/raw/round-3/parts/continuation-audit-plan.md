# Separate offline continuation audit plan

Recorded 2026-11-23 UTC, before running the audit against continuation evidence.
Tool: `B2/tools/bc3-continuation-audit.py`. Static syntax checked; not executed.
No guest operations and no original or continuation evidence changes are made.
The primary `bc3-regression-audit.py` still reports the 60 absent original suffix
observations; it does not absorb the continuation. Its separate current-row
inventory amendment is recorded in `regression-audit-plan.md`.

Run after exports and original controller evidence arrive:

```sh
python3 B2/tools/bc3-continuation-audit.py --output B2/raw/round-3/continuation-audit.json
```

Defaults: continuation root `B2/raw/round-3/final-1-continuation`, original prefix
`B2/raw/round-3/final-1-validation/carried-suite/regressions/round2.jsonl`, historic
133-observation inventory `B2/raw/round-2/final-1/carried-suite/regressions/round2.jsonl`,
and fixed plan `B2/raw/round-3/parts/round2-continuation.json`. If the original raw
folder has not yet been relocated, `--original` may name that exact saved log;
this changes no inventory or truth requirement.

Required continuation artifacts: source snapshots `round2-continuation.py`,
`round2-selftest.py`, `round2-probe.c`, `host-controller.py`, `input-sha256.json`,
`image.json`, `suffix.jsonl`, `steps.json`, `summary.json`, referenced controller
logs, and `evidence/bc3-round2-continuation/{provenance.json,round2-selftest.py,round2-probe.c,observations.jsonl}`.

The audit checks:

- Fixed source/probe/continuation hashes, embedded original bytes and manifest,
  byte-exact source suffix hash, exported guest originals/provenance, and equality
  of stdout/exported JSON observation records.
- Exactly the planned 59 suffix IDs in order, no duplicate or earlier test ID,
  four separately identified setup results without assertion `passed` fields,
  and one explicit SEALED-FIFO NOT-TESTED record without a pass or fresh attempt.
- Original 73 IDs against the beginning of the historic 133-ID inventory; the
  historic remainder must be SEALED-FIFO plus the fixed 59 suffix IDs. Setup
  repetitions are excluded. When all available observations exist, the union
  contains 132 distinct IDs and one unavailable FIFO case.
- Every false original/suffix assertion, failed setup and nonzero controller step
  remains reported. A failed assertion is not by itself structural corruption.
  Completion counts, inventory flags and suffix exit must match observed records.
- Frozen image identity against the copied host controller's fixed expected hash,
  input hashes, controller step ledger, referenced logs, exit consistency and
  owned-guest cleanup. A failed initial destroy followed by successful fallback
  is retained but does not become a spurious inconsistent-success claim.

Exit 0 means complete, structurally consistent continuation evidence, including
any preserved false observations. Exit 1 means inconsistency; exit 2 means missing
required evidence. Every outcome explicitly states that the original whole suite
remains incomplete. Neither a successful continuation nor 132 observed distinct
assertions converts the FIFO setup failure or original controller exit into a pass.
