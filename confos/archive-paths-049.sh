#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/archive-paths-0.49.log 2>&1
grep -qx 'CANDIDATE49 PACKAGE PATHS AND REGRESSIONS PASS' logs/prepare-paths-0.49.log
grep -qx 'SMOKE PASS' logs/smoke-0.49.log
grep -qx 'UPDATES PASS' logs/updates-0.49.log
grep -qx 'APT RECORDING PASS' logs/recording-apt-0.49.log
grep -qx 'CONFIGURATION RECORDING GUEST PASS' logs/configuration-recording-0.49.log
grep -qx 'LANGUAGE RECORDING GUEST PASS' logs/language-recording-0.49.log
grep -qx 'PODMAN RECORDING GUEST PASS' logs/podman-recording-0.49.log
grep -qx 'FLATPAK RECORDING GUEST PASS' logs/flatpak-recording-0.49.log
grep -qx 'OTHER EXPORT OF THE PINNED FLATPAK COMMITS BUILDS; READER REPLACEMENTS IN PLACE PASS' logs/other-export-0.49.log
python3 check-runtime-source-package.py 0.49 >logs/runtime-source-package-0.49.log
sha256sum releases/confos-0.48-source.tar.gz releases/inherited-0.48.sha256 >releases/inherited-0.49.sha256
bash archive-source.sh
sha256sum package-base.py optional_readers.py flatpak_readers.py assemble.py recording.py VERSION >releases/source-0.49.sha256
sha256sum images/confos-0.49-clean.work/root.sqfs images/confos-0.49-clean.work/initramfs images/confos-0.49-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.49.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 bash verify-payload-inventory.sh 0.49 ../cases/inventory/inventory
