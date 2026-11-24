# Independent review of supplemental evidence

Reviewed at 2026-11-23T09:04:00Z.  The executed payload identities in
`final-1/supplement/input-sha256.json` match the frozen originals in
`supplement-inputs/` and `supplement-source-sha256.json`.

## Run integrity

`final-1/supplement/summary.json` records zero exit for every controller step,
successful guest destruction and no remaining owned guest.  Both verification
logs contain 553 `OK` rows and no failed row; their bytes are identical.  The
successful report is byte-identical before and after reboot.  These facts show
readback and reboot continuity, but do not turn the finite boundary attempts
into general closure.

## Actual observations

The direct suite first established exact fixture readiness and ordinary work.
Downloaded, nested-archive, compiled and prefix-selected native executables
were then refused with exit 126 and `Permission denied`.  The concrete compiler
plugin was refused with a failed-mapping diagnostic.  A directly executed saved
shell file was also refused.  In contrast, redirected shell input, an inherited
`/proc/self/fd` input, Python read/evaluation, an awk program file and a helper
launched saved shell input all executed their exact markers.  Declaration and
successful-report identity remained unchanged for every row.  These five are
real saved-input boundary failures, not setup failures.

The extra suite positively observed the enforcing shell domain, typed Python
input, an exported typed function and runtime-generated JIT code.  Saved Bash
startup code, saved editor commands, saved JIT instruction bytes and saved
instructions to the recorded custom dispatcher each emitted an exact effect
line with unchanged declaration/report identity.  They are real failures.
Preload, audit-library, FFI and saved-memfd attempts were refused or produced no
effect; binfmt registration was refused and left no entry.  Runtime memfd and
process-memory injection were restricted observations with no Boolean
hypothesis pass.  Git, make, foreign-interpreter, editor-plugin/modeline and
browser-extension shapes remain explicitly untested.

The original `SAVED-FFI` row is a detector false positive, not a mechanism
failure.  `supplement-marker-audit.json` shows that its marker occurs only in a
Python traceback reproducing the command source; stdout is empty and the
traceback says the shared object failed to map.  The exact-line audit confirms
the other four extra-suite failure markers as actual output.  The corrected
detector source was not executed and is not runtime evidence.

## Candidate implications

The evidence adds concrete support for denial of unrecorded native compiler and
download outputs, but C5.4 still depends on the final suite's separate exact
`recorded-native-overwrite` assertion.  Nothing here contradicts that bounded
candidate.

The saved-command failure in `ed` belongs to C7.10/C8.04.  It does not replace
or contradict the separate positive add/run/remove evidence required for the
recorded `v4-editor` installer functionality in C10.4.  C10.4 therefore remains
a bounded candidate, subject to the final suite evidence already specified in
the source review.

The additional failures reinforce the known saved-code provenance gap.  They
do not justify any broadened closure.  The reviewed supplemental outcome is
`?`.
