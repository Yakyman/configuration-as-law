# Postprocessing preparation review

Recorded 2026-11-22T08:23:59Z.

Verdict: **PASS for postprocessing preparation.** The earlier transfer and
cleanup findings were corrected and independently rechecked. Talos reporting in
(not published: orchestration helpers) also passes. This is not final acceptance of the
five-machine result.

## Transfer

Checked (not published: orchestration helpers).

- PASS: it requires all five lifecycle records to be finished and all five VM
  directories to be recorded as removed and absent before building the manifest.
- PASS: it scans owned process command lines and refuses to snapshot while a
  process still refers to task staging.
- PASS: it hashes every regular file selected under remote `raw/` and `control/`,
  rejects source symlinks, and prints a digest of the completed manifest through
  a separate connection.
- PASS: it stages the archive under a temporary directory, validates the manifest
  digest, rejects duplicate names, links, non-regular members, unsafe paths, and
  unexpected members, and requires exact manifest membership.
- PASS: every staged file is checked for byte length and SHA256 before any file
  is installed into the retained result directory. The verification record binds
  the installation to the manifest digest and records that verification preceded
  installation.
- PASS: temporary transfer material is removed automatically on success or
  failure.

## Cleanup

Checked (not published: orchestration helpers).

- PASS: the deletion target is fixed to the task's own staging directory and is
  asserted before deletion.
- PASS: all five lifecycle records must be finished, all five VM directories
  must be absent, and no owned process whose command line refers to task staging
  may remain.
- PASS: every remote manifest-listed retained file is rehashed immediately before
  deletion. `shutil.rmtree` unlinks directory symlinks rather than traversing
  their targets, so shared base and slot links are not followed.
- PASS: cleanup recomputes the local manifest digest, requires it to equal the
  transfer verification digest, and freshly rechecks every retained local file's
  byte length and SHA256 before contacting the remote environment.
- PASS: the remote manifest must have the same digest, and every remote retained
  file is rehashed again immediately before deletion.
- PASS: all symlinks below task staging are resolved before deletion, every target
  must be outside task staging, and every target must still exist after removal.
  The cleanup record reports the measured preservation result and target count.

## Talos and READY

Checked (not published: orchestration helpers) against the bounded Talos operational review.

- PASS: an absent Talos `objects.tsv` yields zero objects and the builder supplies
  a header-only part table.
- PASS: the termination reason and single-attempt execution deviation are read
  from saved evidence; the partial raw API files are retained and are not
  converted into an object table.
- PASS: the text cites the process observation, listing counts, termination
  record, and independent operational review, and it does not treat unavailable
  data as absent objects.
- PASS: collector nonzero status, VM cleanup, partial coverage, ordinary-action
  outcomes, and transport timeouts are reported separately.

The main scripts and their embedded remote programs both passed syntax parsing.
No transfer, cleanup, live-process query, VM query, or guest probe was executed
for this review.
