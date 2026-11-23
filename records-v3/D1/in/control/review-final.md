# Final inventory artifact review

Recorded 2026-11-22T09:08:02Z.

Verdict: **PASS for the completed D1-I operator artifacts.** Four collector
inventories are present and Talos is correctly recorded as unavailable after one
terminated, non-completing attempt. The retained inventories contain 16,524
objects in total. This review accepts record integrity and reporting; it does not
classify any object or decide a hypothesis outcome.

## Inputs and execution records

- PASS: `input-verification.json` records the required revision
  `43594a47b72707f836953b6b39d5849d5513f61a`; every recorded expected and actual
  input hash matches. The earlier preparation review independently checked all
  57 checksum-manifest files and all 44 selected paths.
- PASS: `remote-instrument-hashes.json` records exact matches for the
  selected runner, general collector, and Talos adapter.
- PASS: Fedora, Tumbleweed, Mint, and Flatcar have successful `new`, collector,
  and `destroy` stages. The three desktop action stages also succeeded. Talos has
  successful `new` and `destroy` stages and the recorded collector termination
  status `-15`. All five lifecycle records finish with the VM directory removed.
- PASS: all 47 exact desktop commands have one recorded exit marker, all exited
  0, and the previously reviewed wrappers preserve source order and command
  bodies.

## Object tables

Every `part-<machine>.tsv` has exactly the required header
`id\tpart\tmachine\tkind\tname\tmembers\tevidence`.

| Machine | Source rows retained | Emitted level 1 | Emitted level 2 | Repeated source-ID occurrences |
|---|---:|---:|---:|---:|
| Fedora | 5,887 | 5,887 | 0 | 0 |
| Tumbleweed | 6,779 | 6,779 | 0 | 0 |
| Mint | 2,031 | 2,031 | 0 | 0 |
| Flatcar | 1,827 | 975 | 852 | 8 |
| Talos | 0, header only | 0 | 0 | 0 |

- PASS: all 16,524 source rows are retained in their original order. Every name
  and members value is unchanged. The emitted part and machine values use the
  requested machine names, and every kind is exactly
  `L<source level>:<source kind>`.
- PASS: all 16,524 emitted identifiers are globally unique and machine-prefixed.
  Flatcar's eight repeated source identifiers retain both rows; each second
  occurrence has an `-occurrence-2` suffix.
- PASS: every object evidence file exists. All numeric evidence line references
  are within their referenced files.
- PASS: per-machine totals, per-kind totals, and duplicate counts exactly match
  `object-counts.json` and the tables in `../READY.md`. The collector's
  level files reconcile exactly with each available `objects.tsv`.

## Coverage and unavailable inventory

- Fedora records 118 coverage queries, 74 nonzero statuses,
  `filesystem_status` 1, one serial-login timeout, two serial-command timeouts,
  and no level-2 rows.
- Tumbleweed records 118 coverage queries, 72 nonzero statuses,
  `filesystem_status` 1, two serial-command timeouts, and no level-2 rows.
- Mint records 110 coverage queries, 106 nonzero statuses,
  `filesystem_status` 1, 96 serial-login timeouts, and no level-2 rows.
- Flatcar records 124 coverage queries, 84 nonzero statuses,
  `filesystem_status` 0, complete recorded ownership coverage, and 852 level-2
  rows.

All coverage stdout and stderr pointers exist. `../READY.md` explicitly states that
the three missing desktop level-2 inventories are coverage gaps and do not prove
absence.

Talos has no `objects.tsv`; `../part-talos.tsv` contains only the required header.
The saved termination, process, and listing records agree: the first pagemap read
had transferred more than 137 GB after 1,112 seconds, while 359 pagemap paths and
114,323 regular paths were listed for unbounded full reads before output-table
creation. The whole collector attempt was terminated once with no repair,
selective continuation, rerun, or synthesized object table. `../READY.md` gives this
precise reason, labels the termination as an execution deviation, and cites the
retained partial evidence.

## READY, transfer, and cleanup

- PASS: the first line of `../READY.md` is exactly
  `INVENTORY: 4 of 5 machines`.
- PASS: it reports all five committed releases, exact per-kind object counts, all
  47 action results, collector and transport coverage gaps, the Talos unavailable
  reason, the deployment adaptations, the Talos execution deviation, and all five
  cleanup results.
- PASS: the transfer manifest contains 1,517 unique regular files totaling
  38,075,595 bytes. Fresh local hashing matched every recorded byte length and
  SHA256. The manifest digest is
  `f03a071059a503a5795094dba1193f6f8de7b9808e4ad28396c9af64bcdd7269`,
  matching `transfer-verification.json`.
- PASS: transfer verification records exact archive membership and verification
  before installation. `server-cleanup.json` binds cleanup to the same
  manifest digest, records 1,517 reverified retained files, no remaining task
  process, all five VM directories absent, task staging removed, and all four
  shared symlink targets preserved.

## Scope

This review used only the committed inputs and saved operator artifacts. It did
not run or repeat a guest query, repair an input, select or discard a collector
object, infer an unobserved object, or classify whether any object must be
recorded. The substantial documented coverage gaps remain limitations of the
inventory data and belong to later sufficiency and classification work.
