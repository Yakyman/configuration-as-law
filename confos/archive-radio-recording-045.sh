#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
grep -qx 'CANDIDATE45 RADIO RECORDING AND REGRESSIONS PASS' logs/prepare-radio-recording-0.45.log
grep -qx 'CANONICAL45 RADIO RECORDING SIX CUTS PASS' logs/radio-recording-0.45.log
grep -qx 'SMOKE PASS' logs/smoke-0.45.log
grep -qx 'UPDATES PASS' logs/updates-0.45.log
python3 check-runtime-source-package.py 0.45 >logs/runtime-source-package-0.45.log
sha256sum releases/confos-0.44-source.tar.gz releases/inherited-0.44.sha256 >releases/inherited-0.45.sha256
bash archive-source.sh
sha256sum nmcli-command package-base.py radio_declaration.py radio_runtime.py recording.py assemble.py VERSION >releases/source-0.45.sha256
sha256sum images/confos-0.45-clean.work/root.sqfs images/confos-0.45-clean.work/initramfs images/confos-0.45-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.45.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 bash verify-payload-inventory.sh 0.45 ../cases/inventory/inventory
