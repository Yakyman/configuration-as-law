KIT: 5 of 7 systems ready

Historical KIT snapshot; subsequent readiness and registration of the two late systems are reported in [KIT2-READY.md](KIT2-READY.md). The original first line and historical results are preserved.

Preparation closed at 2026-11-23T07:15:09Z. Readiness is an instrument result, not a check outcome.

| System | Image verified | Clean installation boots | lab.sh run works | Time and remaining work |
|---|---|---|---|---|
| AlmaLinux 10.3 | yes | yes | yes | 9m45s acquisition to cleanup; initial download resumed successfully. [Record](parts/alma-ready.md). |
| Void 20250202 | yes | yes | yes | About 9 min; corrected instrument sudo-rule ordering. [Record](parts/void-status.md). |
| Gentoo 20261122T164601Z | yes | yes | yes | 59m44s; source build, pinned repository update and final boot/access/shutdown tests passed; see corrected installer steps in the [record](parts/gentoo-ready.md). |
| MicroOS Snapshot20261121 | yes | no | no | 1h26m06s including cleanup and final revisit; corrected installer timed out (124) after 2400s. Internal cause unknown because output was discarded; no installed boot or login established. Failed disk removed. [Record](parts/microos-status.md). Later preparation: [KIT2-READY.md](KIT2-READY.md). |
| Talos 1.14.6 | yes | yes | yes | 14m41s across installation attempts; final signed digest-pinned installation and API run passed. [Record](parts/talos-ready.md). |
| NixOS 26.05 | yes | yes | yes | 2m49s for instrument access and fresh-clone tests; no failures. [Record](parts/nixos-ready.md). |
| GNU Guix System 1.5.0 | yes | yes | no | 1h12m34s including cleanup; copied original boots, but final access reconfiguration timed out (124) after 900s. Guest-side cause unknown because output was discarded. Failed candidates removed. [Record](parts/guix-status.md). Later preparation: [KIT2-READY.md](KIT2-READY.md). |

debian: ready; verified stable cloud image; create, run, root, output, timeout, copy-out, restart and cleanup checks passed ([validation](raw/debian/runner-validation.json)).

fedora: ready; previous read-only installation remains the direct backing; SSH/root and fresh-clone tests passed in 3m06s after correcting a host backing-link cycle ([record](install/fedora/README.md)).

mint: ready; previous read-only installation remains the direct backing; access setup, SSH/root and fresh-clone tests passed in 56 seconds ([record](install/mint/README.md)).

debian-server: ready; same verified cloud image, 8 GB / 4 vCPU / 40 GB; creation, exit 29 and destruction passed ([validation](raw/debian/runner-validation.json)).

Independent review has accepted the runner, the five ready check systems and all four auxiliary systems; the two failed preparations are documented separately in [REVIEW-KIT.md](REVIEW-KIT.md). Guix and MicroOS have no registered usable base.

Only installation, boot, login and selected exit statuses were tested on check systems. Installer and check-command output was discarded. No hypothesis property was assessed. The pre-observation repository commit remains a downstream gate, as described in [INPUTS.md](INPUTS.md).
