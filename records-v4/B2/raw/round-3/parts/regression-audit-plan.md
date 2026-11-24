# Offline full-suite audit plan

Recorded 2026-11-23 UTC, before execution against final validation outputs.
Tool: `B2/tools/bc3-regression-audit.py`. Syntax parsed; the audit has not yet run.
No guest operation or frozen recipe modification is performed by this tool.

Invocation after final exports arrive:

```sh
python3 B2/tools/bc3-regression-audit.py --final B2/raw/round-3/final-1-validation --output B2/raw/round-3/regression-audit.json
```

Exit 0 means complete structurally checked evidence, including preserved real
failures. Exit 1 means malformed/inconsistent evidence. Exit 2 means required
outputs or assertion identities are absent. Neither exit 0 nor controller exit 0
is acceptance of the seventeen published cases.

Required controller records: `summary.json`, `steps.json`, `whole-suite-ledger.json`,
`lane-plan.json`; each referenced parent log must exist. The ledger contains
`components`, `round4`, `round3`; all exits are reported, including nonzero exits.
A parent success contradictory to its steps/lanes is inconsistent. Final cleanup
comes from the parent; concurrent child VM listings are not treated as leaks.

Required top-level component logs: cases and filesystem readback; objects and
objects-reboot; shell and shell-reboot; gate; tools; supplement-direct and
supplement-extra; final stand readbacks for all six component guests and pre-reboot
readbacks for objects/shell/supplement. Cases require precisely the fifteen fixture
IDs plus native account and ordinary work.

Required carried evidence: `carried-suite/{language,applications,system,ordinary}.jsonl`
and their readbacks/summary; `carried-suite/regressions/round{1,2,3}.jsonl`,
`powercuts.jsonl`, `boot-order.jsonl`, `boot-attempts.json`, inventory and summary.
Each of the nine powercuts requires expected, cut and result records. Native D01–D09
logs, both D10 peer logs and D10 summary/comparison are required, with original
controller completion and individual D01–D10 peer exit records. Independent peer
snapshot equality flags are checked against saved values, and declaration-byte
identity against exported original machine-declaration directories. This inherited comparison
covers the original machine declaration and its original reader rows only. It does
not compare the five BC3 filesystem declarations or the eight-file complete bundle.

Required combined evidence: summary, events, both snapshot exports, before/after
reboot readbacks, exact declaration hashes and schedule results for both sides,
and stand comparison. Snapshot ID inventories are matched to readbacks. Exact
machine declaration hashes must agree with `complete-example.json`. This inherited
combined example likewise covers the original combined machine declaration and
original reader rows only, not the five BC3 filesystem declarations or eight-file
complete bundle. Filesystem declarations include generation identities and timestamps;
no byte-equality claim for them follows from the inherited comparison.

Required provenance: image/build/peer identities, frozen input hash map,
recipe/controller snapshots, both recipe logs. Listed frozen file hashes are
recomputed. The separate retained-image publication audit remains responsible for
checking the actual final image and final declaration export checksums.

Historical Round-2 logs supply fixed assertion identities and multiplicities only.
Their truth values are never used as expected new truth values. Missing assertions
make the audit incomplete; new unexpected assertion identities require review.
Boolean counts are per top-level observation record, excluding summaries, without
double-counting nested fields. Explicit false verdicts, including failures counted
by a suite's exit code, remain listed. Required/implementation-exit metadata are
preserved where present; their absence is not guessed. Unavailable/untested states
are reported separately.

Concerns retained: historical saved-code and native-account checks only inspect the
old declaration model and can report false despite the added filesystem declaration.
Their raw verdicts remain false in this audit. Nonzero component exits do not excuse
omitted suites. Missing outputs after an early driver abort remain incomplete even
if a controller has already written a failure summary. This audit does not execute
or accept the second party's published cases and is not a complete semantic proof.

## Pre-execution amendment: dynamic reader identities

Recorded 2026-11-23 UTC, before the first full-audit execution. Source review found
that independent/combined/D10 stand-comparison rows use declaration object IDs,
not fixed test-case IDs. Those three logs now obtain their complete expected
inventories from their current saved reader snapshots. Independent and D10
snapshots are additionally checked against their current exported machine
 declarations. Each comparison payload and equality Boolean must match its saved
left/right reader rows. Missing current objects remain incomplete; duplicates,
foreign objects or contradictory values remain inconsistent. Combined snapshot
counts and complete before/after reboot readbacks retain their existing checks.

The exact deterministic factory ID delta was checked between:

- (not published: direct evidence at least 2 MB): 553 rows,
  SHA-256 `d046ab7b0e47dd88d0b49b83c34f14f4dcb2195a93aaf13df349c166bf218815`.
- (not published: direct evidence at least 2 MB): 559 rows,
  SHA-256 `ac7a53fb666fe6a3d7a53dec08e381ca36f385ec979fa54905c986da57d7285a`.

Added IDs: `package:libfuse2t64:amd64`, `package:python3-fusepy`,
`unit:stand-files-etc.service`, `unit:stand-files-home.service`,
`unit:stand-files-shm.service`, `unit:stand-files-tmp.service`,
`unit:stand-files-vartmp.service`. Removed ID: `unit:systemd-hostnamed.service`.
Seven additions and one removal account for the increase of six rows. The parser
does not special-case these names: it validates the actual current exported
inventories, including current fixture additions for each comparison.

Affected logs only: `carried-suite/regressions/independent-stand-compare.jsonl`,
`carried-suite/regressions/original/D10-compare.jsonl`,
`combined/stand-compare.jsonl`. Fixed historical case/assertion identity checks
remain unchanged, including the 60 missing observations in the aborted original
code/lifecycle suite. No observed pass, false or unavailable result is reclassified.
The audit has not been executed. The comparison scope remains original machine
 declarations and original reader rows, not the five filesystem declarations or
 eight-file complete bundle.

## First execution result and evidence review

Recorded 2026-11-23 UTC, after the final controller summary at 16:56:44 UTC.
The first full audit returned exit 2: `incomplete`, with no structural errors.
`B2/raw/round-3/regression-audit.json` contains exactly one missing-evidence entry:
60 assertion identities absent from the original aborted `round2.jsonl`. These
are SEALED-FIFO and the following 59 observations. They remain missing from that
original execution; the separate continuation is not merged into this audit.

Direct inspection of the raw component records confirms 19 false observations
and seven UNTESTED observations, exactly matching the audit's ID/file lists.
The false records remain historical false verdicts under their original readers.
The main controller exited 1, with components 0, round3 1 and round4 0; no owned
VM or peer remains. Nine powercuts have all expected/cut/result records and pass.
Combined replay has 24 passing assertion events and 584 original-reader rows on
both sides before and after reboot. These inherited comparisons do not establish
equality of the five filesystem declarations or eight-file complete bundle.

The separately saved continuation audit is complete without errors: original
73 plus 59 suffix observations yield 132 distinct passing observed assertions;
four successful setup operations are excluded. SEALED-FIFO is separately
NOT-TESTED after its known setup failure. Thus only the FIFO case remains
unavailable across the disclosed split execution, while 60 observations remain
missing from the original run. The seven UNTESTED observations in the primary
audit and the one FIFO continuation record are distinct counts, not substitutes.
The original controller failure and whole-suite incompleteness are unchanged.

No audit expectation, runtime, sealed input or saved evidence was changed during
this result review. This is internal engineering evidence review, not acceptance
of the second party's published cases. See `regression-final-review.md` alongside
this plan for the compact source/evidence map and reviewed audit hashes.
