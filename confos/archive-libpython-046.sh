#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
grep -qx 'CANDIDATE46 LIBPYTHON AND REGRESSIONS PASS' logs/prepare-libpython-0.46.log
grep -qx 'CANONICAL46 LIBPYTHON TWO BOOTS AND REMOVAL PASS' logs/libpython-0.46.log
grep -qx 'SMOKE PASS' logs/smoke-0.46.log
grep -qx 'UPDATES PASS' logs/updates-0.46.log
python3 check-runtime-source-package.py 0.46 >logs/runtime-source-package-0.46.log
sha256sum releases/confos-0.45-source.tar.gz releases/inherited-0.45.sha256 >releases/inherited-0.46.sha256
bash archive-source.sh
sha256sum package-base.py optional_readers.py assemble.py VERSION interpreter-inputs/libpython-private/metadata.json >releases/source-0.46.sha256
sha256sum images/confos-0.46-clean.work/root.sqfs images/confos-0.46-clean.work/initramfs images/confos-0.46-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.46.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 bash verify-payload-inventory.sh 0.46 ../cases/inventory/inventory
