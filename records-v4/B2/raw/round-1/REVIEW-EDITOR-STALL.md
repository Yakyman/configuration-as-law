# Review of the editor installer stall

Reviewed at 2026-11-23T09:25:00Z from frozen source and the reported failed-run
position.  No guest probe was performed.

The transaction mechanism used by the stalled assertion is the same mechanism
that completed direct ordinary mutations and the supplemental dispatcher
installation.  The unique process shape is in `build/v4-editor.py`: the editor
retains a Python parent in the `stand-shell` profile while
`subprocess.run()` waits for `stand-pkg`.  The child reaches the authorized
unconfined broker, whose transaction stops every task remaining in the shell
profile.  It therefore stops the Python waiter and its Bash ancestor while the
broker is their descendant.  Small inherited output is not by itself enough to
prove the precise observed wait, and an exact kernel wait cannot be assigned
without retained process-state evidence.  This retained-parent dependency is
nevertheless the only source-level process shape unique to the stalled case.

The minimal correction is an execution handoff:

```python
os.execv('/usr/local/bin/stand-pkg',
         ['/usr/local/bin/stand-pkg', action, target])
```

This makes the editor installer path identical to the already exercised direct
frontend-to-`sudo` transition.  It preserves arguments, output and exit status,
and leaves no intermediate editor process stopped while waiting for its broker.
The pause gate should not exempt the editor and paused processes should not be
resumed before durable transaction success or recovery.

Until a rebuilt disposable guest completes editor add, run, remove, refusal,
full readback and reboot continuity, C10.4 is not closed.  The retained failed
run is evidence of an implementation stall, not evidence against the fixed
hypothesis text.  Outcome: `?`.

## Later process evidence

The later read-only guest inspection (`final-1/editor-stall-process.txt`) showed
an unconfined `runuser` parent stopped after the transaction completed. The
implementation therefore uses the general cgroup freezer correction described
in `FREEZER-CORRECTION.md`, without the suggested editor-only exec change. This
source hypothesis is retained as history; the process evidence supersedes it.
