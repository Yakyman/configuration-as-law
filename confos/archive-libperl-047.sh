#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
grep -qx 'CANDIDATE47 LIBPERL AND REGRESSIONS PASS' logs/prepare-libperl-0.47.log
grep -qx 'CANONICAL47 LIBPERL TWO BOOTS AND REMOVAL PASS' logs/libperl-0.47.log
grep -qx 'SMOKE PASS' logs/smoke-0.47.log
grep -qx 'UPDATES PASS' logs/updates-0.47.log
python3 check-runtime-source-package.py 0.47 >logs/runtime-source-package-0.47.log
sha256sum releases/confos-0.46-source.tar.gz releases/inherited-0.46.sha256 >releases/inherited-0.47.sha256
bash archive-source.sh
sha256sum package-base.py optional_readers.py assemble.py VERSION interpreter-inputs/libperl-private/metadata.json >releases/source-0.47.sha256
sha256sum images/confos-0.47-clean.work/root.sqfs images/confos-0.47-clean.work/initramfs images/confos-0.47-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.47.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 bash verify-payload-inventory.sh 0.47 ../cases/inventory/inventory
