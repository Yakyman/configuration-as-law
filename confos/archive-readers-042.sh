#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.42
grep -qx 'CANDIDATE42 NATIVE READERS STORES AND REGRESSIONS PASS' logs/prepare-readers-0.42.log
grep -qx 'CANONICAL42 NATIVE READERS AND CONFIGURATION STORES PASS' logs/readers-0.42.log
grep -qx 'SMOKE PASS' logs/smoke-0.42.log
python3 check-runtime-source-package.py 0.42 >logs/runtime-source-package-0.42.log
python3 check-reader-inheritance-042.py >logs/reader-inheritance-0.42.log
cp readers-042-fixture/declaration.conf records/readers-042-fixture.conf
sha256sum releases/confos-0.41-source.tar.gz releases/inherited-0.41.sha256 \
 logs/mpv-0.41.log logs/radio-0.40.log logs/configuration-recording-0.38.log \
 >releases/inherited-0.42.sha256
bash archive-source.sh
python3 - <<'PY' >releases/source-0.42.sha256
import hashlib,runpy
from pathlib import Path
names=set(runpy.run_path('package-base.py')['RUNTIME'])|{
 'package-base.py','package-initramfs.py','build.sh','boot.sh','archive-source.sh',
 'archive-readers-042.sh','prepare-readers-042.py','readers-archive-paths-042.py'}
for name in sorted(names):print(hashlib.sha256(Path(name).read_bytes()).hexdigest(),name)
PY
sha256sum images/confos-0.42-clean.work/root.sqfs images/confos-0.42-clean.work/initramfs \
 images/confos-0.42-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.42.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
 bash verify-payload-inventory.sh 0.42 ../cases/inventory/inventory
