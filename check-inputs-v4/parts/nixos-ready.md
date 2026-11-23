# NixOS readiness

- Image verified: yes; unchanged release 26.05.14979.94c3211b0ee8, reused verified ISO and copied original clean installation. Evidence: `C1/raw/reuse-checksums.txt` and `C1/install/nixos/README.md`.
- Clean installation boots: yes; fresh disposable clone returned 0 from `lab.sh new`.
- Lab run works: yes; ordinary and root scripts both returned their requested exit status 37 over SSH.
- Time spent adding and validating access: 2 minutes 49 seconds, 2026-11-23T06:17:27Z–06:20:16Z. Earlier release/image copying was performed separately.
- Failures: none during this access preparation.
- Final backing: `install/nixos/base.qcow2`, mode 0444; registered as `C1/base/nixos.qcow2` with SSH transport, user `user`, key `keys/lab`.
- Cleanup: both disposable overlays destroyed, both machines stopped. The original copied backing remains read-only. No guest output or inventory retained; no property assessment performed.

Exact declaration and access recipe: `C1/install/nixos/`. Exit-status evidence: `C1/raw/nixos/access-status.log`.
