#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
grep -qx 'CANDIDATE48 SOLVER AND REGRESSIONS PASS' logs/prepare-solver-0.48.log
grep -qx 'CANONICAL48 SOLVER RECORDER DOCUMENT AND REMOVAL PASS' logs/solver-0.48.log
grep -qx 'SMOKE PASS' logs/smoke-0.48.log
grep -qx 'UPDATES PASS' logs/updates-0.48.log
python3 check-runtime-source-package.py 0.48 >logs/runtime-source-package-0.48.log
sha256sum releases/confos-0.47-source.tar.gz releases/inherited-0.47.sha256 >releases/inherited-0.48.sha256
bash archive-source.sh
sha256sum package-base.py optional_readers.py assemble.py recording.py VERSION SOLVER-PRIVATE.md >releases/source-0.48.sha256
sha256sum images/confos-0.48-clean.work/root.sqfs images/confos-0.48-clean.work/initramfs images/confos-0.48-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.48.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 bash verify-payload-inventory.sh 0.48 ../cases/inventory/inventory
