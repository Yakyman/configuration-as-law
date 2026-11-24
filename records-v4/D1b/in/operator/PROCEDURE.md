# Operator procedure

2026-11-23 UTC. Inputs gate: (not published: orchestration or scratch), commit
`c62afbb5861fb038aa7da0aa00c0730ad140ec7c`.

Before any machine was started, `/usr/bin/python3 -I S4/verify-inputs.py` returned
0 and reported that all 49 published inputs covered by the manifest matched.
The manifest excludes its own checksum. The verification output is retained in
`input-verification.stdout`; each machine operator also verifies the staged copy.
The local Git metadata directory is empty in this execution environment; the
named gate and checksum verification identify the supplied committed inputs.

The first ordinary host SSH invocation returned 255 with
`Bad owner or permissions on /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf`.
Explicitly selecting the existing user SSH configuration restored transport.
No host configuration was changed. This is a host transport invocation detail,
not a changed guest action, collector command, or observation retry.

The existing host Python and dumpsolv were found. The copied runner and existing
laboratory runner both had SHA256
`3402697b02c88449fd6ba41e7137c404185c43a2bcd45fa211623d0d7e349733`.
Task-local laboratory roots use the same registered read-only bases and shared
slot locks. The Gentoo operator starts first, after checking four free slots;
the other machine operators start only after its successful startup is recorded.
Each machine has one operator, with no nested operator work. The external step
review is responsible for acceptance.

Every machine is created once. The fixed action entry point is executed once
where assigned. Action failures remain failures and the fixed list continues.
The collector is invoked once; its output is preserved whole. Disposable VMs
are destroyed after collection. Each exact handoff command is subsequently run
once from its laboratory root, with a separate audit and exit status.

`build-inputs.py` reads delivered `objects.tsv` rows in their original order.
It adds only the required inventory ID prefix, `part`, and level prefix on
`kind`; the machine, name, members and evidence cells are preserved. No inventory
row is discarded, merged or deduplicated. `object-id-map.tsv` maps the prefixed
IDs to the unchanged raw IDs used by all handoff facts and matcher output.

The exact matcher is invoked separately for each machine, with both unchanged
first-night input tables. Its complete outputs remain in `match/MACHINE/`.
Since that invocation receives both complete old tables, its unmatched output
also contains the other machines. `match/unmatched-MACHINE.tsv` contains exactly
the rows for MACHINE; `match/matched-MACHINE.tsv` uses the same mechanical machine
selection. No matching rule is added. The headline unmatched total counts each
machine's rows once. Gentoo has no first-night input IDs.

For the four other systems, `part-MACHINE.tsv` contains exactly new rows whose
raw IDs occur in that machine's matched pairs. Gentoo's part contains every
delivered row. Missing or failed handoffs yield a header-only part and an explicit
list of any raw object IDs not delivered. No object decision is made here.

Final preservation verification completed after every original transfer. Its
record is `deliverable-verification.json`; it covers both originals and successful
handoffs, and separately verifies the AlmaLinux originals and not-delivered IDs.
`server-cleanup.json` records the absence of all five VMs and removal of temporary
server staging. Original observations, handoffs, audits and operator evidence
remain in the task directories.

The published AlmaLinux handoff failure traceback displays absolute task-root
paths as task-relative paths. Its diagnostic and stack line numbers are unchanged;
this display change is recorded in `D1b/handoff-audit/alma-failure.json`.
