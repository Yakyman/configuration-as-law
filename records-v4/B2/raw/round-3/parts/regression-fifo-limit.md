# Carried regression stopped at named FIFO setup

Recorded 2026-11-23 UTC. Source-only analysis; no guest operation, retry, new case,
runtime edit or sealed-input change was performed.

The builder reported that the final carried `round2.jsonl` stopped at 16:33:38 UTC,
after 73 passing Boolean observations, with `OSError: [Errno 30] Read-only file system`
at `round2-selftest.py` line 176, `os.mkfifo(WORK/'fifo')`. These observed details
are attributed to the builder's report; this component inspected source only.
The eventual exported raw log is the authority for final counts and exact traceback.

## Source finding

`B2/build/round2-selftest.py` creates the FIFO before invoking the `SEALED-FIFO`
case. There is no surrounding exception handler in `main()`. Failure of `os.mkfifo`
therefore prevents even that case's expected/result records from being emitted.
It then prevents the subsequent socket/PTY, environment/preload/startup, typed
legacy-launcher requests, editor/document, browser, native-location, login-key,
service/timer lifecycle, removal/profile cleanup and final `VERIFY` observations.
The suite's final summary is also not reached. Those are unexecuted observations,
not failed refusal assertions and not passes.

`B2/build/bc3_filesystem.py` explicitly documents special nodes as unsupported.
Its initial import accepts only regular files, directories and symlinks, and its
operation implementation provides no named-FIFO creation callback. The reported
failure is consistent with that declared implementation limit. Source inspection
alone does not establish which library/kernel layer selected errno 30; no new
probe is warranted to restate the observed failure.

## Reporting consequence

Use: “73 observed assertions passed; the carried code/lifecycle suite exited 1
while creating its named-FIFO fixture; the remaining suffix did not run.” Final
counts must be checked against exported evidence. Do not report a complete pass,
count absent observations as passing, or convert this abort into an expected
successful refusal. The operation was fixture setup, not the tested refusal.

The parent driver continuing with peer comparison cannot complete the omitted
suffix. Later successful peer or combined checks remain separate results.
The requested complete regression execution is not achieved by this run. Retain
the nonzero suite, lane and controller statuses and identify the incomplete suffix
in BUILD-3/SELFTEST, even if every directly targeted case passes.

The existing offline audit semantics are appropriate: the old fixed assertion
inventory detects absent suffix identities and returns `incomplete` (exit 2),
unless an independent structural inconsistency also requires exit 1. It retains
all existing true/false observations and nonzero controller results. No audit
truth semantics or expected inventories should be weakened to obtain exit 0.

## Relation to the seventeen target cases

The named-FIFO limitation does not by itself negate the separate observed results
for the fifteen saved-code ways, native account change and listed ordinary work.
An ordinary shell pipeline is an unnamed pipe and does not require a FIFO node
in this filesystem. The target list does not require creating a named FIFO.
However, the result demonstrates an additional ordinary filesystem operation
that this implementation does not support; it limits any general-purpose or
whole-system claim. The seventeen finite results must therefore be reported
alongside the incomplete required regression run, not as completion of the full
build task or independent published-case acceptance.

This is an implementation limitation. There is no argument here from Section 8
alone that every system having P1, P2 and P4 must fail, so it supplies no
hypothesis-outcome 0 and no new refusal closure.
