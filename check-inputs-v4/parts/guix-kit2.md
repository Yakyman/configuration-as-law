# Guix KIT2 readiness

Ready: yes, using the explicitly permitted serial fallback.

- Release: unchanged GNU Guix System 1.5.0; verified image evidence remains in
  `C1/raw/reuse-checksums.txt` and `C1/raw/guix/signature-status.txt`.
- Reuse: byte-for-byte host comparison of the retained original copy against
  the preceding clean backing returned 0. Registration returned 0; see
  `C1/raw/guix-kit2/reuse-status.txt`. The preceding laboratory is unchanged.
- Access: existing `user`/password serial login from the original declaration;
  no additional guest configuration or reconfiguration. SSH was not enabled
  and no lab-key login is claimed. This is the task's explicit fallback.
- Instrument change: the Guix registry requests passive boot/login. The
  runner restores the selected preceding recipe's passive startup, avoiding
  Ctrl-C before the login prompt. See `C1/install/guix/kit2-passive.patch` and
  preceding `C1/fix-c1-1/LAB.md`. Independent static review preceded execution.
- Fresh boot/login returned 0; `lab.sh run` returned exactly 37 for the user
  script and 0 for the privileged script. All command output was discarded.
  Status evidence: `C1/raw/guix-kit2/status.txt`.
- Cleanup: native stop returned 1; the bounded shutdown did not establish
  QEMU exit. Forced stop and destroy returned 0. Disposable absence, read-only
  base and serial registration checks each returned 0; see
  `C1/raw/guix-kit2/cleanup-status.txt`. No guest-side cause is inferred.
- Smoke elapsed 2026-11-23T07:22:00Z–07:24:29Z, 2m29s; including reading,
  registration and cleanup, about 8 minutes of this follow-up task.
- Current recipe: `C1/install/guix/KIT2.md`, `kit2-reuse.sh`,
  `kit2-base.json`, and `kit2-smoke.sh`; the original installation inputs
  remain `original-config.scm` and `original-install.sh`.

Previous failure: SSH reconfiguration ultimately exceeded its 900-second
limit (124); the guest-side cause remains unknown because output was
intentionally discarded. Those failed attempts were read and not repeated.
KIT2 uses the original installation and the task's permitted serial access.
The only new host preparation error was a service invocation with a relative
script path, corrected before any VM or guest probe started; see
`C1/raw/guix-kit2/host-launch-note.md`.

No hypothesis property was assessed and no check-system inventory was read.
