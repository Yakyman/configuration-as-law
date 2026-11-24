# Native SSH configuration reader, 2026-11-24 UTC

Hypothesis outcome: `?`. These are builder development controls, not independent acceptance or universal reader closure.

The private candidate extends sealed42 source `38a9ff3f01eaf5fec7b818a9ab305988321fa1a39890012d41170e7aa35f3137`.
Native candidate SHA256: `6eed3f62ba9e292b9498c640066fae650f3adec67833555adecbdcb3ccf18377`.
Portable metadata: `interpreter-inputs/ssh-reader-draft/metadata.json`, SHA256
`0fa9a006b9103f742c8245a1083914036cb89436142cd54bd306b6c39b651099`.
That file pins source archives, original package, build dependencies, licences, policy header, source patch, recipes,
candidate and native comparison/provenance. The original and candidate agree in version, dynamic dependencies,
symbol versions, exported symbols and native algorithm queries; the confined guest checks exact installed hashes.

Observed command outputs:

- `run-ssh-reader-guest-draft.sh`: `SSH_READER_PRIVATE42_GUEST_MATRIX_PASS 22`, `SSH_READER_PRIVATE42_PIPELINE_PASS`.
- Original `-F` ProxyCommand and Match exec created their marker; candidate refused both with exit255 and no marker.
- Candidate refused symlink, regular-file fd0 aliases via `/proc/self/fd/0` and `/dev/fd/0`, and regular stdin configs.
  The original accepted both fd aliases and executed their Match control.
- Explicit typed/data-produced config pipes and typed ProxyCommand retained their marker-producing behavior (R4).
- Recorded Match, ProxyCommand and nested includes executed; a recorded include of a mutable config was refused.
- Original and candidate ordinary localhost connections each returned exit0 and exact `SSH_READER_CONNECTION_OK`.
- `run-ssh-reader-root-draft.sh`: `SSH_READER_ROOT_PRIVATE_MATRIX_PASS`; sudo uid0 refused mutable Match/Proxy
  with exit255 and no marker, accepted recorded Match (exit0) and recorded Proxy (marker, expected exit255).

Automatic user configuration creation returned EROFS (30): the mount prevented saving it. This is a mount refusal;
the native automatic-reader path was not observed. Match as a command-line option remains natively unsupported.
The guard applies to opened config files before their contents are interpreted; this report makes no claim about
other SSH input readers.

Fixture failures are retained, not counted as successes: unsupported supplementary group `users` (changed to `-`);
an fd3 alias that native SSH closes (replaced by fd0 with original positives); attempted creation in the read-only
automatic-config directory; missing ephemeral mutable files after reboot (root harness now creates its own controls).
The earlier build failure is `records/ssh-reader-private-build-failure.log`. Other normalized logs, composition
records and native metadata are retained under `interpreter-inputs/ssh-reader-draft/` on the worker.

All private units ended, their guests stopped, and their fixture disk, disposable key, extracted source/build and
dependency trees were removed by `cleanup-ssh-reader-draft.py` (`SSH_READER_PRIVATE_SCRATCH_REMOVED`). Exact source
and dependency archives, licence copies, generated config header, original and candidate binaries remain.

Release44 integration is separate: `prepare-ssh-component-044.py` extends sealed43 exact bytes, modes and links with
one SSH manifest entry and the component version change. `check-reader-inheritance-044.py` checks that composition;
`build-tools-fixture-044.py` prepares the combined SSH/visudo fixture after the runtime is packaged.
`ssh-archive-paths-044.py` lists portable inputs and evidence while excluding guest disks and connection keys.
Canonical44 guest controls and independent review remain required before acceptance.
