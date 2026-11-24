# Unexecuted carried-suite suffix: fixed continuation plan

Recorded 2026-11-23 UTC. Prepared only; no continuation has been executed.
Inputs: `round2-continuation.py` and `round2-continuation.json` in this directory.
The JSON manifest fixes source/probe/suffix/script hashes and all expected IDs.

## Scope and separation

Run once on a fresh disposable copy of the unchanged final image, after the host
controller verifies its frozen image SHA-256. Do not run on the partially exercised
original guest. Keep new logs under `B2/raw/round-3/final-1-continuation/`; preserve
all original full-suite logs, summaries, failures and incomplete status unchanged.
This completes available previously unexecuted work; it is not a retry of failed
fixture creation, a rerun of the first 73 observations, or published-case acceptance.

The standalone script embeds the original source and native probe byte-for-byte.
At execution it checks both hashes, saves those exact bytes beneath the guest's
`/var/lib/stand/bc3-round2-continuation/`, and checks the original suffix hash.
Creation of that directory is exclusive: a second invocation on the same guest
fails before fixture construction. No recipe source, runtime, image, CASES file,
or existing test is edited.

## Exact source extraction

Original `B2/build/round2-selftest.py`:

- Lines 1–43 supply unchanged imports, helpers and original result calculation.
- Line 45 and lines 49–110 supply fixture construction through ADMIT. The first
  three service assertions on lines 46–48 are omitted.
- Lines 111–174 are omitted entirely. No prior positive, admission, interpreter,
  saved-source, argument or stdin assertion is repeated.
- Line 175 supplies the original hostile environment mapping needed by the suffix.
- Lines 176–177, FIFO creation and SEALED-FIFO invocation, are omitted. One explicit
  `NOT-TESTED` record explains the known original EROFS; no pass is assigned.
- Lines 178 through the original main body's end are retained byte-for-byte,
  including socketpair, PTY, all assertions, cleanup, VERIFY and original summary.

Fixture commands FIXTURE-COMPILE, FIXTURE-LIBRARY, FIXTURE-HOLDER and ADMIT run as
setup only. Their `passed` field is renamed `setup_passed`, their phases are
`setup_expected`/`setup_result`, and `continuation_scope` is `setup`. They never
contribute suffix assertion counts. Any setup failure aborts before suffix entry;
there is no weakening of their original success calculation.

## Expected observations fixed before execution

The companion JSON lists 59 Boolean suffix result IDs, in original execution order,
from SEALED-SOCKET through VERIFY. The script checks exact order and completeness
after the unchanged suffix returns. SEALED-FIFO is one separate NOT-TESTED record.
The original suffix's summary remains a summary of executed assertions; added
fields state `whole_original_suite_complete=false` and identify SEALED-FIFO.
Continuation exit 0 would mean these 59 assertions completed without an original
assertion failure; it would not make the original 133-observation suite complete.
A setup error or later exception leaves the remaining continuation suffix missing.
All false results must remain false and no stage is retried.

The original 73 observations already include the four setup assertions. Their new
setup records must not be counted again. If all 59 suffix observations pass, the
combined distinct result inventory is 132 observed assertions plus one unavailable
FIFO case, with the original failed controller run still reported separately.

## State preservation and limitations

Fixture construction reproduces the declaration row, exact interpreter programs,
native probe/library/holder, source inputs, configuration fixtures and filenames
used by the suffix. Earlier omitted assertions are predominantly attempted reads
and denied launches/admissions; their successful no-change expectations are not
necessary mutations for the suffix. The suffix itself creates its editor/browser
inputs and native copies, then installs/removes its lifecycle fixtures exactly as
before. `old-copy`, used by a removal assertion, is created by the unchanged suffix.
The socketpair and PTY operations do not require creating a named FIFO file.

This is a separate fresh-guest continuation with reconstructed setup, not proof
that the aborted original guest could have resumed at the same instruction. Its
source and state preparation are disclosed so review can judge that distinction.
The FUSE special-node limitation remains. The full original suite remains
incomplete and cannot be relabeled a complete pass.

## Host controller handoff

After source review, copy the standalone script to the fresh guest and execute
`python3 -B` on that script as root once. No probe or source sidecars are required:
they are embedded with their original hashes. Save stdout, stderr and exit status,
export `/var/lib/stand/bc3-round2-continuation/` including the exact original source,
probe, manifest and observation log, then destroy the disposable copy. Record the
image hash and cleanup in the separate continuation evidence folder.
