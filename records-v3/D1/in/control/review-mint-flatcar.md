# Mint and Flatcar inventory review

Recorded 2026-11-22T08:01:06Z.

Verdict: **PASS for the Mint and Flatcar table mappings and retained records,
with a material Mint coverage limitation.** This is a bounded review of two
completed machines. It is not acceptance of the five-machine inventory.

## Files and method

Compared `../raw/mint/objects.tsv` with `../part-mint.tsv` and
`../raw/flatcar/objects.tsv` with `../part-flatcar.tsv`, row by row and in order.
Also checked `object-counts.json`, both `raw/<machine>/coverage.tsv`
files, both `raw/<machine>/metadata.json` files, every evidence path referenced
by the two part tables and coverage tables, and both
`control/<machine>/status.json` lifecycle records. The Mint ordinary-action
statuses were checked in `mint/actions.log`.

The subset interface in (not published: orchestration helpers) was also checked. It accepts
only unique names from the fixed five-machine set, rebuilds only the requested
parts, and retains prior count records for machines outside the requested
subset.

## Table mapping

- PASS: both part files have exactly the required header:
  `id\tpart\tmachine\tkind\tname\tmembers\tevidence`.
- PASS: Mint retains all 2,031 source rows in source order. Flatcar retains all
  1,827 source rows in source order.
- PASS: every emitted `name` and `members` value is byte-for-byte equal to its
  source value.
- PASS: every Mint row has `part=mint` and `machine=mint`; every Flatcar row has
  `part=flatcar` and `machine=flatcar`. The source machine values are
  `d1-mint` and `d1-flatcar`, respectively.
- PASS: every emitted kind is exactly `L<source level>:<source kind>`.
- PASS: every identifier is unique and begins with its machine prefix.
  Mint has no repeated source identifier. Flatcar has eight source identifiers
  that each occur twice; all eight second occurrences have the required
  `-occurrence-2` suffix, and no row is removed.
- PASS: every referenced evidence file exists. All 126 Mint and 963 Flatcar
  numeric line references are within their referenced files.
- PASS: total object counts, per-kind counts, and duplicate-occurrence counts
  exactly match `object-counts.json`.
- PASS: the collector's `level-1.tsv` and `level-2.tsv` row totals reconcile
  with `objects.tsv`: Mint has 2,031 level-1 rows and no level-2 rows; Flatcar
  has 975 level-1 rows and 852 level-2 rows.

## Provenance and execution records

- PASS: both metadata files record observation mode and input revision
  `43594a47b72707f836953b6b39d5849d5513f61a`.
- PASS: both collector stages exited 0 and retained the collector completion
  message. The outputs use the expected fresh-clone machine and system names.
- PASS: all 17 Mint ordinary-action commands have one recorded exit status and
  all exited 0. Flatcar has no ordinary actions under the committed inputs.
- PASS: both lifecycle records show successful `new`, collector, and `destroy`
  stages; Mint additionally shows a successful action stage. Both record the VM
  directory as removed. The destroy logs are present and empty, consistent with
  successful silent cleanup.

## Collector coverage

Flatcar records 124 coverage queries: 40 exited 0, 81 exited 127 for unavailable
tools, and 3 exited 1. Its filesystem traversal exited 0, package ownership is
recorded as complete, all coverage stdout/stderr paths exist, and no container
boundary gap is recorded.

Mint records 110 coverage queries: 4 exited 0, 10 exited 127, and 96 exited 1.
The saved error for the filesystem traversal and most later queries is
`lab: Serial login timeout`. `metadata.json` therefore records
`filesystem_status` 1, incomplete ownership queries, and three container-engine
boundary gaps. The resulting table contains the successfully collected account,
group, and native-package rows, but no level-2 filesystem rows. These failures
are retained in `../raw/mint/coverage.tsv` and `../raw/mint/metadata.json`; they are
coverage gaps and do not establish absence of the uncollected objects.

The Mint limitation does not alter the lossless table-mapping verdict: the part
file retains every object that the committed collector emitted. It must remain
explicit in `../READY.md` and in any assessment of whether the five-machine data
are sufficient.

## Scope limits

This review read only the saved Mint and Flatcar artifacts. It did not classify,
filter, merge, or select objects; run a probe; contact a VM; or independently
observe cleanup. Cleanup findings are limited to internal consistency of the
saved lifecycle records. Fedora, Tumbleweed, Talos, the final combined counts,
and final `../READY.md` remain unreviewed.
