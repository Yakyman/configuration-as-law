# Independent final-2 carried-suite review

Review time: 2026-11-23T12:18:47Z

Scope: read-only review of the completed carried-suite tree in the candidate workspace, its controller summaries, source inventory, assembly log, channel records, readbacks, regression records, boot attempts, and independent comparisons. No guest, probe, or remote file was started or changed. The combined replay was still running, so this is preparatory carried-evidence review rather than final evidence acceptance.

## Controller and provenance

The carried controller completed at 2026-11-23T12:15:26Z with suite exit zero, an empty owned-machine list, all four channel suites tested, and the regression controller tested with an independent peer. Every recorded suite, metadata, readback, example-export, and regression-controller exit is zero. The regression summary likewise records suite exit zero, an empty machine list, and the same image SHA-256 as the carried summary.

The recipe inventory contains 65 source entries. The relevant frozen sources include the suite adapter, all four carried test suites, the transaction and boundary implementation, and the assembly program. The assembly log records 572 complete declaration rows, 19 exported channel rows, and hashes for the combined, channel, and factory artifacts. These figures describe assembly input; the final combined replay must still validate the assembled output.

## Channel assertions and readback

The four carried channel logs contain 301 result rows in total, with no false result:

- applications: 131 results;
- language: 79 results;
- ordinary: 59 results;
- system: 32 results.

The application and ordinary summaries report no failures. The other two logs match their source-shaped result inventories and their controllers return zero. Every-line readback contains 553 `OK` rows for applications, ordinary, and system, and 555 `OK` rows for language; there are no `FAIL` rows. Language has two additional declaration rows from its channel examples.

The adapter emitted 59 application, 55 language, 16 system, and 46 ordinary Bash-entry markers. For broker requests, the marker demonstrates that the declared installer frontend was invoked as an ordinary Bash command. For retained application launches, the adapter constructs a Bash command that invokes `stand-session`; those results remain sealed-launch compatibility evidence. They do not establish that saved shell input is safely executable, and they do not cancel the saved-code failures already retained by the new suites and supplement.

## Regression evidence

The carried regression logs contain:

- 35 transaction results, all passing;
- 9 power-cut results, all passing;
- 166 authority results, all passing;
- 133 code-boundary results, all passing.

The boot record contains 205 ordinary-login attempts explicitly marked before readiness; none succeeded. Across the complete 412-entry interleaved operator/ordinary record, the sole successful login is the final operator readiness observation. The original D01 through D09 operations and both D10 peer runs record exit zero, as do their creation, export, and cleanup operations.

The independent comparison reports declaration-byte equality and value equality. Both sides contain 557 successful rows. The separate independent comparison and original D10 comparison each contain 557 equal rows and no unequal row. The evidence therefore supports reproducible declaration and readback values for this carried replay, within the already documented scope of those tests.

## Material host-validator mismatch

The current carried evidence exposes one host-side summarizer defect. `ordinary.jsonl` contains 46 Bash-entry markers, but the reviewed `summarize-round1.py` currently plans only 45 because it derives markers only from baseline `expected` rows that contain a `command` field. The `DOWNLOAD` expected row has no command field. Its pinned suite source directly invokes `stand-session` with `curl` and a runtime-selected fixture port, and the adapter correctly emits the additional marker immediately after that expected row.

As written, the strict marker equality check will reject the complete carried tree even though the raw ordinary result passed. The correction should derive this one direct call from the pinned ordinary-suite source and validate its stable argument structure, placement, and fixture URL form while permitting only the source-selected decimal port. The exact observed payload may still be retained and hashed in metrics. This is a host validation contract correction and does not require another guest probe.

## Verdict

The completed carried raw evidence is internally consistent for the channel, readback, regression, boot-gate, and independent-comparison claims reviewed above. It preserves the distinction between Bash entry and sealed execution. It does not justify a final closure decision by itself.

Final metrics cannot yet be accepted because the ordinary dynamic-download marker is absent from the summarizer's planned transport contract. After that bounded correction, acceptance still depends on the completed combined replay, atomic export, a successful strict full-tree summary, and reconciliation with the publication manifests and independent final review. The overall outcome remains `?`.
