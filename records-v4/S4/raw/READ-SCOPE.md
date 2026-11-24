# Read scope and rehearsal handling

2026-11-23 UTC. The task's named common rules, fixed text sections, step inputs, result, two missing-fact tables, collector, documentation, rehearsal repair record and ordinary-action sources were read. No hypothesis text or C1 input was edited.

D1/RESULT.md names five further extent candidates beyond its 2,007-row count. To identify those named candidates exactly, its referenced `D1/fix-d1-h-2/generated/dispositions.tsv` and only the selected IDs/kinds/names from `D1/in/part-alma.tsv`, `part-void.tsv`, `part-microos.tsv` were consulted. No new classification was performed. These five rows are explicitly separated from the two matching tables; the matching script does not ingest those extent dispositions.

The system specialists and assembler inspected source, lifecycle/action status, bounded collector stderr, query coverage and numerical reductions only during rehearsals. Full query stdout, object rows and member inventories were transient and deleted unread after each run. The collector itself parses its own data to produce fact files and numerical diagnostics, as required for the instrument. The final observation operator will retain inventories separately under D1b.

The generic filesystem helper was built only on the server in a task-local build directory, with two compiler threads and a 2 GiB service memory limit. Rehearsal VMs used shared slot locks and durable user services. No local installation, sudo operation, service change, public upload or message to another party was made. The only deliberate collector termination by the assembler was the exact first Gentoo controller PID, after command-line identity verification, with SIGTERM to stop quadratic indexing; its harness then deleted the inventory and destroyed the VM. Alma's earlier SIGKILL was not issued by this task and its cause was not established.

Mechanical source/schema/matching checks by the assembler are not independent acceptance. RV-S4-P is the separate reviewer specified by the task. This workspace is not a Git worktree, so PUBLISH.list and the checksum manifest prepare the exact commit set; this task does not claim a commit or an observation.
