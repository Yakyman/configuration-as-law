# Independent review of the cgroup v2 freezer design

Reviewed at 2026-11-23T09:45:00Z from source and primary kernel
documentation.  No implementation was changed and no guest probe was run.

## Disposition

Replacing `SIGSTOP` with cgroup v2 freezing is the correct general direction.
The observed stopped `runuser` parent is a consequence of stop notification,
not an editor-specific transaction defect.  The editor-only `exec` handoff may
still simplify that frontend, but it cannot repair arbitrary callers that wait
for a broker child.

A frozen private child under each process's original cgroup is safer than one
global parking cgroup.  It preserves the original hierarchy, keeps the parent
cgroup structurally alive, gives every raced descendant an unambiguous restore
destination, and avoids relaxing inherited cgroup controls.  The design is
acceptable if the invariants below are implemented and exercised before a new
closure claim.

## Kernel facts used

The kernel's [cgroup v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html)
states that writing a PID to `cgroup.procs` migrates the whole process, a forked
child is born in its parent's current cgroup, zombies are absent from
`cgroup.procs`, and an empty cgroup can be removed.  It also states that moving
a process into a frozen cgroup stops it, moving it out makes it runnable, and a
frozen empty cgroup may be deleted.  Completion is the `frozen 1` field in
`cgroup.events`, not merely a successful write to `cgroup.freeze`.

The same documentation describes threaded topology: a new child begins as a
domain; below a threaded subtree it is `domain (invalid)` until changed to
`threaded`, and `cgroup.procs` in a threaded subtree has special read behavior.
The [kernel freezer source](https://github.com/torvalds/linux/blob/master/kernel/freezer.c)
uses `TASK_FROZEN` and saves the prior task state.  Thaw restores that saved
state, including an existing stopped or traced state.  This is the required
difference from externally visible `SIGSTOP`/`SIGCONT` job control.

## Required freeze algorithm

1. Require the unified cgroup v2 mount, a writable initial cgroup namespace,
   and the core `cgroup.freeze`, `cgroup.events`, `cgroup.procs` and
   `cgroup.type` files.  Compare the broker's cgroup namespace with PID 1 and
   fail before mutation if paths are namespace-relative or the hierarchy is
   unavailable.
2. Hold the exclusive application lock before discovery.  Recover any prior
   freezer journal before creating a new one.  Derive original cgroup paths
   only from the `0::` record in `/proc/PID/cgroup`; reject deleted paths,
   traversal, controls and ambiguous records.
3. For each newly observed original cgroup, durably record the exact original
   path, fixed private child path and required child type before `mkdir`.
   Refuse a pre-existing child unless the current durable journal owns it.
   Make the child root-owned and non-delegated.  Write `1` to its
   `cgroup.freeze` while it is empty, then require `frozen 1`.
4. Respect `cgroup.type`.  A normal domain parent may use the new domain child.
   Under `threaded` or `domain threaded` topology, change the child to
   `threaded` before population and use process-granularity migration only.
   If a whole thread group cannot be migrated, abort and restore before any
   realization change; never fall back to freezing selected threads.
5. Inspect every `/proc/PID/task/TID/attr/current`, because a thread's profile
   cannot safely be inferred only from the leader.  If any live thread has the
   exact enforcing shell profile, migrate the whole process.  Hold a pidfd,
   record TGID/start time/original group durably before the write, and recheck
   identity, profile and membership immediately around the `cgroup.procs`
   write.  A stale or exited process is skipped, never reassigned by numeric PID
   alone.
6. Iterate discovery and migration.  Existing shell tasks can fork during a
   scan, but a task moved into the already frozen child cannot run or fork, and
   a raced child inherits either the original group and is found by the next
   scan or the frozen child and is already contained.
7. Reconcile every child before declaring quiescence.  A member for which no
   thread still has the shell profile has raced through an allowed profile
   transition; move the whole process back to that child's recorded original
   group.  The child-to-original journal mapping is the recovery authority for
   inherited descendants, including a child not yet listed as an individual
   journal entry.
8. Require `frozen 1` for every child, then perform a complete global thread
   scan proving that no enforcing shell task remains outside the owned frozen
   children.  Repeat on any mismatch.  Only this state permits realization to
   begin.  A bounded failure to converge must restore and fail closed; it must
   not invoke `SIGSTOP` as a fallback.

## Recovery and resume ordering

The group mapping, rather than a saved PID list, is the durable recovery
authority.  PIDs and start times remain useful evidence and prevent a live
migration from targeting a reused number, but children may be born in the
frozen group and zombies are intentionally absent from `cgroup.procs`.

After a durable success report, or after restoration and full readback, keep
each child frozen while enumerating all of its live member processes and move
each whole process to the recorded parent.  Moving out makes it runnable; a
process that was job-stopped before freezing retains that saved stop state.
Do not thaw the populated child first, because resumed members could fork new
children into it during cleanup.  Once `cgroup.events` says `populated 0`,
remove the still-frozen child, then remove the durable journal.  A crash at any
point is idempotent: absent children are complete, existing children are
drained to their recorded parents, and the journal is deleted only after all
children are gone.

The recovery path must explicitly exclude itself, PID 1, the transaction
supervisor and its ancestors from selection.  Their unconfined profile should
already exclude them; the explicit check turns a surprising label or namespace
state into failure instead of freezing recovery.  The watchdog must recognize
a freezer journal even when no pending declaration remains.

## Remaining objections and evidence needed

- Systemd-managed cgroups and threaded subtrees make topology handling a real
  requirement.  Supporting only normal domain parents is acceptable only if
  the implementation detects other types and fails before mutation; silently
  creating `domain (invalid)` children is not acceptable.
- `frozen 1` proves the members of one child are frozen.  It does not prove the
  selector found every shell task.  The final global per-thread profile scan is
  independently required.
- A fatal signal can remove a frozen process, and privileged external code can
  migrate it.  Recovery must tolerate disappearance and verify actual child
  membership; ordinary callers must have no write access to the private child.
- Freeze convergence needs a bounded deadline within the transaction recovery
  budget.  Timeout before realization restores all groups and reports failure.

Evidence should show a Python parent waiting for its broker without a
`CLD_STOPPED`/job-control stall, an already job-stopped task remaining stopped
after restore, a fork/exec race captured or evicted, multiple original cgroups,
all children at `frozen 1` before the first realization checkpoint, no shell
profile outside them, report-before-resume ordering, crash recovery from each
journal phase, empty-child removal and journal absence.  Until that evidence
exists, C10.4 and the general transaction gate remain open.  Outcome: `?`.
