# Independent source review of the freezer gate

Reviewed at 2026-11-23T09:34:23Z.  The reviewed SHA-256 values are:

- `build/shell_boundary.py`: `acf6b0fca8307530f4adf4a0ff18d0480dfe6c4b749da76417144b36394e25d6`
- `build/v4-gate-selftest.py`: `c3d05c40e71652c84ff349792bad1ec2f28c4dc07400829419434462e1f047dc`
- `build/transactions.py`: `29647ca6f83d49d1844cf79eb34acf517d318f4cf07426455e8e013516cde469`
- `build/v4-editor.py`: `017d2d2344584533d8106421a15fcb6a206e1dc49cb0d6c58e36c51955da0177`

## Disposition

The changed source is suitable for a rebuilt bounded candidate.  The freezer
gate removes the demonstrated job-control deadlock without weakening the
before-report boundary.  Runtime evidence is still required; this review does
not reinstate C10.4 or close a general concurrency claim.

## Accepted properties

The implementation now scans labels per thread and migrates the whole process
when any thread remains in the shell domain.  It creates an already-frozen
private child beneath each original normal-domain cgroup, preserving the
original resource hierarchy and an unambiguous recovery destination.  The
group mapping is durably written before creation or migration.  Unowned name
collisions, noncanonical membership paths and threaded parent cgroups are
refused before realization.

Migration checks a captured start time and expected source membership, polls a
pidfd for exit before the numeric write, and verifies identity and destination
afterward.  A process that races into an allowed non-shell profile is returned
to the original group.  Completion requires every owned child to report
`frozen 1` and a new global census to find no shell-domain process outside the
owned children.  Resume enumerates current child membership, restores processes
while the child remains frozen, then relies on successful `rmdir` before
deleting the journal.  Existing job-stop state is left to the kernel freezer's
saved-state restoration; no `SIGCONT` is sent.

Recovery also handles both journal/child ordering gaps.  An entry whose child
was never created, or whose child was already removed by an interrupted
resume, is durably pruned before the freeze acknowledgement loop.  A surviving
owned child is reasserted frozen before membership is inspected.  This avoids
waiting forever for `frozen 1` on an absent, already empty child.

The gate test directly covers the earlier failure shape: an ordinary Python
parent uses synchronous `subprocess.run()` for two broker mutations, first
directly and then through the editor.  Each return requires exact declaration
and state readback, the successful report identity, restoration to the original
cgroup, child removal and journal removal.  The heartbeat case separately
requires kernel freeze acknowledgement throughout in-flight realization,
unchanged output, refusal of new shell admission, report-before-resume behavior
and final readback.

## Explicit limit

`cgroup.procs` accepts a numeric PID and has no pidfd-based migration API.  The
checks narrow the exit/reuse window and make ordinary disappearance harmless,
but they cannot make lookup and migration atomic.  A PID can theoretically be
reaped and reused between the last check and the kernel's numeric lookup.  A
post-write mismatch fails before realization, but cannot reconstruct the
unexpected process's former cgroup.  The source correctly avoids claiming that
a pidfd pins the numeric interface.

This residual kernel-interface race, deliberate refusal of threaded source
cgroups, and finite test coverage must remain stated limits.  The rebuilt run
can support the concrete normal-domain gate and C10.4 candidate; it cannot
support universal shell-freeze closure.  Outcome pending runtime evidence: `?`.
