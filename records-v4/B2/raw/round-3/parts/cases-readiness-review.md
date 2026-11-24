# Case-document readiness audit

Recorded 2026-11-23 UTC. Scope: static audit of `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md` against
`B2/build/bc3-selftest.py`, `B2/build/bc3-fixtures.json` and `B2/build/lab.py`.
No guest was started and no case was attempted. This is a builder-side document
audit, not the required independent case performance or acceptance review.

## Findings checked

- All fifteen displayed attempt commands and all fifteen displayed permitted
  commands match the manifest strings exactly, including the pickle trailing
  space and multiline JIT quoting. The manifest's original-evidence paths remain
  available. Working directories match the controller; direct supplemental cases
  retain their separate directory prefix.
- The ordinary-work fenced command matches the frozen controller's literal
  one-session command. Package executable path, script path, fixed HTTP URL,
  browser configuration and document edit/readback match.
- Both source SHA-256 values printed at the document's end match the current
  controller and fixture manifest. No implementation source was edited by this
  audit. The pending image and complete-declaration identity placeholders were
  preserved for final sealing.
- `lab.py new NAME stand` creates an overlay against `base/stand.qcow2` and starts
  it. Its existing shared lock/service code supplies VM resource coordination.
  The displayed `run NAME --root` syntax is accepted by the parser and invokes
  the guest root controller. That controller sends ordinary commands through the
  ordinary account and applies the original command strings.
- `copy-out NAME /var/lib/stand/bc3-evidence DEST` extracts the basename into DEST.
  The document now names the resulting `DEST/bc3-evidence/snapshots/` path exactly.
  Destroying each copy follows the export; no account reset or second native
  account invocation is prescribed.
- Each numbered case is selected separately with `--case`, so it gets its own
  newly created copy. The account case tests the full original tuple and an exact
  matching own-line filesystem account row; the document does not describe an
  alias as the native tool.
- The host network service uses a user service and fixed relative document root.
  Its exact page content matches the controller's expected marker. The guest URL
  addresses the host through the virtual Ethernet network. Setup/readiness and
  cleanup instructions are separate from the ordinary-work attempt.

## Document corrections made

The common replay block now refuses to overwrite an existing case JSONL, stops
when fresh-copy creation fails, and captures a failed controller status inside an
`if` so a shell's errexit setting does not silently skip export/cleanup. A failed
copy-out is reported. Network fixture readiness commands were added before any
attempt. The controller's fixed `builder self-test only` and `?` summary labels
are explained: independent observation and review, rather than that hardcoded
label, determine the case outcome. No original attempt or permitted command was
changed.

## Known limitations and sealing prerequisites

The document remains a draft until the builder inserts the final image and complete
declaration hashes and commits the frozen inputs to the public records. This
static audit does not establish public commitment. It does not prove that the
installed guest copies equal the working recipe; image sealing must bind those
identities. A missing laboratory directory, key, image metadata, occupied network
port or unavailable VM slot is a setup issue, not a successful refusal.

Coverage-after-execution alone is insufficient temporal evidence. Review must
check the prospective filesystem publication mechanism, generation reports and
source hashes; the document states this explicitly. The fixed controller has
finite observations, not a proof of all system behavior. Ordinary-work marker
success alone also does not replace checking package/script rows and the actual
saved document in the exported snapshots/audit. No additional case attempts are
authorized by this document audit.

The common replay snippet creates one fresh copy per selected ID and requires
manual progression through all seventeen listed IDs; it is not a batch loop.
A failed export can leave incomplete evidence and must be reported as such. The
second-party process must preserve stdout/stderr and all successful exports even
when a case fails. A source edit after this audit requires refreshing source
identities before sealing, never after the first second-party attempt.
