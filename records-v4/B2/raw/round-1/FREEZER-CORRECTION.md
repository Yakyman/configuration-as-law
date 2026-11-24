# General pause correction

Recorded 2026-11-23 UTC before the changed mechanism is exercised.

The first rebuilt candidate completed the editor installation at 09:14:25 UTC,
but the ordinary tool test timed out at 09:23:57 UTC. A subsequent removal also
completed. Root process inspection found its unconfined `runuser` parent in
state `T`, with the editor child a zombie, no pending/paused journal, and a
successful durable report. The SIGSTOP pause of the ordinary child reached the
caller's job-control handling; resuming only the confined child was insufficient.
See `final-1/editor-stall-process.txt`, (not published: direct evidence at least 2 MB) and
`final-1/interruption.json`. The incomplete candidate is not a whole-suite pass.

The [kernel cgroup v2 interface](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html#core-interface-files)
documents `cgroup.freeze`, asynchronous acknowledgement in `cgroup.events`,
and movement into and out of frozen groups. Its stated move-out effect is:
“If a process is moved out of a frozen cgroup, it becomes running.”
The revised mechanism uses that existing kernel facility. It creates a frozen,
root-controlled child beneath each original cgroup, journals its original and
destination paths before migration, and repeatedly gathers ordinary-domain
tasks until the kernel acknowledges freezing and none remain outside. Raced
privileged broker transitions are returned to the original group. Restoration
moves tasks back only after a durable success report or successful rollback.
No editor-specific exec substitution or caller exclusion is used.

Expected integration results: the existing concurrent heartbeat is frozen
through application and resumes afterwards in its original cgroup; new shell
entry is refused while pending; a retained ordinary Python subprocess caller
can install and remove through the broker without a stopped parent; the editor
installer uses the same path. Already job-stopped processes remain stopped.
The recipe will be rebuilt from scratch and the entire suite repeated on fresh
guests. Failures of saved-code provenance remain separately reported.

Source review tightened migration to check the numeric process start time and
source/destination cgroup around each write, inspect every thread's security
label, refuse threaded original cgroups, and refuse an unowned pre-existing
freezer child. Empty journal entries from an interrupted creation or completed
partial resume are pruned before a recovery census. The cgroup migration API
accepts numeric PIDs; these checks do not make that interface atomic. No
universal process-race closure is inferred from this finite integration test.
