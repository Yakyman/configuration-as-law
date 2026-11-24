# Independent pre-run review of the supplemental probes

Reviewed at 2026-11-23T09:00:14Z, before the first supplemental guest run.
The reviewed payload hashes are those in
`raw/round-1/supplement-source-sha256.json`.

## Disposition

The frozen controller and both payloads are suitable for the planned single
fresh-overlay observation.  This is source review, not runtime evidence.  It
does not close any property row, and the Round 1 outcome remains `?` pending
the saved logs and their independent comparison with the preregistered
expectations.

## Checks accepted

- `tools/v4-direct-selftest.py` gates optional executables.  HTTP, archive,
  compiler, plugin and prefix fixtures have separate readiness observations;
  the native and prefix fixtures require exact hashes and the symlink target is
  checked.  A denial result additionally requires unchanged declaration/report
  identity, no effect marker, a nonzero exit, and a permission or mapping
  diagnostic.  Missing setup, a syntax error, or an unavailable program cannot
  therefore become a successful denial.  The fixture directory is explicitly
  removed on normal completion.
- `tools/v4-extra-selftest.py` distinguishes saved-input boundary observations,
  positive ordinary work, setup, and runtime-only memory.  Runtime-only rows
  have no Boolean hypothesis pass.  Optional editor, Git, make and compiler
  facilities are gated.  Git alias and filter consumers run only after exact
  configuration readback.  The binfmt command is setup-only and the exact
  effective entry decides its boundary row.  Temporary files are scoped to a
  temporary directory; the exact binfmt fixture and recorded dispatcher have
  explicit removal, followed by declaration-byte restoration and full
  readback verification.
- `tools/supplement1.py` saves source and image identities, retains nonzero
  payload exits, checks verification and exact report bytes across reboot, and
  destroys the owned disposable guest in `finally`.  Its completion status is
  not a universal boundary claim.

## Limits that must remain explicit

Each successful saved-input row describes only its concrete attempted route;
marker absence is not general closure.  The extra payload records that limit
as `ATTEMPT_REFUSED` or `NO_EFFECT_OBSERVED` and emits `closure_claim=false`.
The direct payload likewise retains every failed row and reports the overall
hypothesis outcome as `?`.  Browser extensions and foreign interpreters remain
untested when no supported concrete fixture exists.  Guest destruction is the
cleanup fallback if a payload aborts before its own cleanup.
