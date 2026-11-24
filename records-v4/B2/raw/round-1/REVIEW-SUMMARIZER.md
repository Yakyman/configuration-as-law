# Independent strict-summarizer review

Review time: 2026-11-23T10:54:44Z

Scope: bounded source audit and read-only checks of `summarize-round1.py`. No guest was started or changed, no metrics file was written, and no closure decision is made.

## Confirmed corrections

The parser now requires strict UTF-8, nonempty newline-terminated inputs, one JSON object per declared JSONL line, unique JSON keys, and finite JSON values. Malformed records are rejected rather than skipped. Verification logs require exactly four TAB-separated fields per row, unique IDs, valid status/digest fields, all-`OK` status, and an exact declaration-derived ID/type inventory.

Each of the six new-suite logs is tied to a pinned source SHA-256 and an embedded exact ordered phase/ID/mode/schema contract. Read-only evaluation of the current local records produced:

- shell: 28 result rows, 6 false observations;
- shell reboot: 1 result row, 0 false observations;
- gate: 9 result rows, 0 false observations;
- tools: 86 result rows, 1 false observation;
- direct supplement: 17 result rows, 5 false observations;
- extra supplement: 21 result rows, 4 false observations.

All six current source hashes and record contracts match. The total remains 16 false observations; passing summaries do not remove them. The source also reconciles suite failure lists, counts, runtime observations, and untested lists where those fields exist.

The carried baseline contracts are SHA-pinned, result contracts compare ordered record signatures, adapter transport is explicitly parsed, powercut/readback transport has dedicated parsers, and combined assertions and comparisons are separately validated. The mandatory lists contain 123 unique carried paths and 50 unique combined paths. A local `--check-only` run stopped immediately on the first missing carried artifact, confirming that missing required evidence is no longer silently omitted.

## Material findings

### 1. Main controller cleanup state is not validated

`controller()` checks `owned_vms_remaining`, `vms_remaining`, and `remaining_owned_vm` when present. The main final summary uses `remaining_vms` and `peer_remaining`, neither of which is checked. It also treats a missing `steps` field as an empty successful sequence.

The summarizer can therefore produce validated metrics from a main summary that reports a remaining machine or peer, or from a stripped summary with no controller steps. Export/adoption have separate checks, but the metrics validator must not describe such evidence as complete.

Required correction: for the main controller require the exact expected summary schema, `controller_exit == 0`, `remaining_vms == []`, `peer_remaining is False`, a nonempty exact step inventory, and every step exit equal to its expected exit. Reconcile the separate controller steps record if that is the authoritative inventory.

### 2. Required carried and combined paths are minimum sets, not exact inventories

`require_files()` verifies that every listed path exists and is a regular non-symlink, but it never compares the complete recursive regular-file set with the 123/50 contracts. An additional assertion-bearing or failure-bearing file can therefore be present yet omitted from parsing and `all_false_observations` while validation still succeeds.

Required correction: compare the complete relative regular-file set under each carried and combined root with an exact reviewed inventory. If some unparsed logs are intentionally allowed, classify them in a separate exact allowlist and state why they cannot contain assertion results. Reject unknown extra files.

### 3. Carried shell transport payloads are not tied to expected commands

`adapted_rows()` requires each `v4-shell-entry` marker to have the wrapper shape and checks the total marker count. It does not compare the `actual_command` payload string with the corresponding expected carried command, and it removes all markers before metrics are formed. Any payload strings with the right wrapper and count satisfy this check.

This is insufficient for the claim that every compatible carried frontend was actually routed through the ordinary shell. The result schema can match the baseline even when a marker names a different command.

Required correction: derive the exact expected adapted payload sequence from the pinned baseline commands and the reviewed adapter transformation, including the documented extra holder, then compare marker order and complete payload bytes. Retain a marker count and SHA-256 or the normalized marker sequence in metrics so the routing evidence remains auditable.

## Additional bounded observation

Malformed standalone JSON documents still fail validation, although some paths may surface a raw parse exception rather than the summarizer's concise evidence-error message. This does not hide a failure and is not release-blocking.

## Verdict

The rewrite fixes the original silent malformed-line, permissive readback, missing required-file, and new-suite undercount defects. It is not yet acceptable for final metrics because main cleanup can be ignored, extra carried/combined evidence can be omitted from aggregation, and carried shell markers are not linked to their expected commands. These are host-side validation defects and require no guest rerun. After bounded corrections, re-review can focus on those three paths. Current overall outcome remains `?`.
