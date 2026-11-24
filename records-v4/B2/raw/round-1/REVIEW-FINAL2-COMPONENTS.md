# Independent final-2 component review

Review time: 2026-11-23T09:44:58Z

Scope: exported final-2 gate, ordinary-shell, shell-reboot, and gate-verification records. Full tool, carried-suite, and peer evidence was still pending. This note accepts only the observations described below and makes no final closure decision.

## Transaction gate

All nine recorded gate result rows pass, and the summary has no failure. The central concurrent row supplies the following concrete evidence:

- 456 heartbeat samples all retained the single value 28 while the private child cgroup reported `frozen=1` and `populated=1`.
- A new shell entry during the transaction was refused with exit 126 and `REFUSED declaration replay incomplete`.
- The existing shell resumed after successful application and was restored from `/user.slice/user-0.slice/session-2.scope/.stand-freeze` to its original cgroup.
- The fixture application produced 554 clean readback rows; removal returned to 553 clean rows.
- The freezer child and journal were absent after completion.

The ordinary Python `subprocess.run` caller completed both broker install and removal. Its cgroup before and after each call is identical, both reports are successful, application/removal readbacks are clean, and no freezer child or journal remains. The corresponding document-editor caller independently completes the same install/remove lifecycle with the same restoration properties. These rows directly address the earlier parent-stop deadlock shape.

The final gate restoration row confirms the original declaration bytes, 553 clean readback rows, successful report, and no journal. The separate gate verification contains 553 rows, all `OK`, and has SHA-256 `310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc`.

This evidence is sufficient to accept the tested gate lifecycle and the two nested caller shapes on this rebuilt image. It does not remove the documented numeric `cgroup.procs` PID-reuse race, prove every cgroup topology, or establish a universal process-freeze claim.

## Ordinary shell

The shell component establishes the intended positive baseline: enforcing shell profile, free ordinary commands, document editing, browser use, personal installer add/run/remove, and unsaved command execution. It also observes refusal of the tested unrecorded native executable, loader, recorded-path overwrite, persistence, raw-setting, user-namespace, and OCI-alternate paths. The component reports that all implemented checks behaved as asserted.

The same log honestly retains six saved-input boundary failures, all with exit zero and their effect output:

- `SAVED-SCRIPT`: `SAVED_CODE_RAN`
- `SAVED-PIPE`: `SAVED_CODE_RAN`
- `SAVED-SOURCE`: `SAVED_CODE_RAN`
- `STARTUP-ENV`: `SAVED_CODE_RAN`
- `PYTHON-IMPORT`: `IMPORTED_UNRECORDED`
- `PICKLE-CODE`: `PICKLE_EXECUTED`

The shell summary therefore records hypothesis outcome `?`, even though its implemented-check flag is true. The reboot row finds no matching unsaved process after reboot, preserves the payload identity, and reports unchanged declaration state. This supports the tested unsaved-process reboot behavior only; it does not cure the six saved-input counterexamples.

## Disposition

The final-2 records support component-level acceptance of the observed freezer gate, nested broker caller, nested editor caller, restoration, ordinary-shell positive baseline, tested denials, and unsaved-process reboot behavior. They do not justify variant closure or overall acceptance before the remaining suites and independent replay are reviewed. The current overall outcome remains `?`.
