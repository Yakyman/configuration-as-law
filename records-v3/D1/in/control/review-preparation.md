# Preparation review

Recorded 2026-11-22T07:00:19Z.

Verdict: **PASS for preparation; final acceptance pending.** The committed inputs,
ordinary-action wrappers, controller, and result-building logic passed the checks
listed below. Raw inventories, generated part tables, and `../READY.md` were not
available for this review and require a separate final audit.

## Committed inputs

Checked (not published: outside selected checks and direct evidence), Sections 4.1 and 4.2 of `../../../TEXT.md`,
`GATES/INPUTS-1-PUSHED`, (not published: outside selected checks and direct evidence),
(not published: outside selected checks and direct evidence), and
(not published: outside selected checks and direct evidence).

- PASS: `inputs-check-1.md` matches the SHA256 recorded by the gate.
- PASS: all 57 files named by `input-files.sha256.tsv` exist and match their
  recorded SHA256 values.
- PASS: all 44 paths selected by `selected-inputs.json` exist and occur exactly
  once in the checksum manifest.
- PASS: the required collector revision is
  `43594a47b72707f836953b6b39d5849d5513f61a`.

Collector interfaces and constraints were checked in
(not published: outside selected checks and direct evidence),
(not published: outside selected checks and direct evidence),
(not published: outside selected checks and direct evidence),
(not published: outside selected checks and direct evidence), and
(not published: outside selected checks and direct evidence).

- PASS: the general collector requires `--observe`, a VM name, a new output
  directory, and `CAL_INPUTS_COMMIT`; it records failed queries as coverage gaps.
- PASS: the Talos adapter requires a new output directory and the per-clone API
  environment; it records API failures and limitations rather than treating them
  as absent objects.
- PASS: the controller uses `opensuse` as the committed runner system identifier
  for clone `d1-tumbleweed`. The selected runner has no `tumbleweed` registry
  alias.

## Ordinary-action wrappers

Compared the selected sources (not published: outside selected checks and direct evidence),
(not published: outside selected checks and direct evidence), and (not published: outside selected checks and direct evidence) with
`../operator/actions-fedora.sh`, `../operator/actions-tumbleweed.sh`,
`../operator/actions-mint.sh`, and `control/actions-*.json`.

- PASS: Fedora has 15 commands, Tumbleweed has 15 commands, and Mint has 17
  commands in both the selected sources and wrappers.
- PASS: every stored base64 payload decodes byte-for-byte to the corresponding
  selected command, including complete here-documents.
- PASS: command order is unchanged; no command is missing, duplicated, repaired,
  or replaced.
- PASS: every command has one sequential begin marker and one exit marker.
- PASS: the privilege helper definitions are unchanged.
- PASS: wrapper-level errexit is disabled so a failed command is recorded and the
  next exact command is attempted, as required by the operator task.

## Controller

Checked (not published: orchestration helpers) and `operator-notes.md`.

- PASS: the task-local root is used consistently for `LAB_ROOT` and
  `CAL_LAB_ROOT`, and the exact gate revision is set in `CAL_INPUTS_COMMIT`.
- PASS: the checksum-pinned runner is addressed as task-local `lab.sh`, the exact
  filename hard-coded by the general collector.
- PASS: disposable VM state is task-local while clean bases and slot locks are
  shared through the documented links.
- PASS: a failed ordinary-action command does not prevent collection; collector
  failure is recorded; every created VM enters cleanup in a `finally` block.
- PASS: Talos endpoint, node, configuration, and tool path are derived from the
  fresh clone metadata before the host-side adapter runs.
- PASS: no classification or object-selection rule is present.

## Result builders

Checked the current (not published: orchestration helpers) and (not published: orchestration helpers).

- PASS: each part file starts with exactly
  `id\tpart\tmachine\tkind\tname\tmembers\tevidence`.
- PASS: the source header and row shape are validated before object mapping.
- PASS: parsed source rows are retained in source order; identifiers receive a
  machine prefix and repeated source identifiers receive an occurrence suffix
  without dropping a row.
- PASS: `level` is represented as `L<level>:` before the collector kind; source
  names and members are unchanged; evidence paths are made task-relative.
- PASS: absent inventories produce header-only part files.
- PASS: `../READY.md` begins with the required inventory fraction and reports each
  committed release, counts by emitted kind, exact ordinary-action statuses,
  collector coverage failures, unavailable-inventory reasons, deviations, and
  cleanup evidence.
- PASS: earlier ambiguous prose about command substitution was removed, destroy
  logs are cited only when present, and the no-repeat statement is limited to
  ordinary-action commands and collector observations.

## Scope limits

This was a read-only preparation review of committed files and local operator
logic. It did not contact a running VM, inspect live task processes, or probe a
remote environment. It did not validate raw collector output, object counts,
final identifier uniqueness, evidence-file existence, generated part-table row
preservation, action outcomes, cleanup outcomes, or the final `../READY.md`. Those
checks remain pending until all five raw inventories and final artifacts have
been copied into `D1/in/`.
