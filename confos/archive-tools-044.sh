#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.44
grep -qx 'CANDIDATE44 VISUDO SSH AND REGRESSIONS PASS' logs/prepare-tools-0.44.log
grep -qx 'CANONICAL44 VISUDO NINE CUTS AND SSH READERS PASS' logs/tools-0.44.log
grep -qx 'SMOKE PASS' logs/smoke-0.44.log
grep -qx 'UPDATES PASS' logs/updates-0.44.log
grep -qx 'CANONICAL44 RECORDED VISUDO EDITOR PASS' logs/visudo-editor-0.44.log
python3 check-runtime-source-package.py 0.44 >logs/runtime-source-package-0.44.log
python3 check-reader-inheritance-044.py >logs/reader-inheritance-0.44.log
cp tools-044-fixture/inputs/declaration.conf records/tools-044-fixture.conf
sha256sum releases/confos-0.43-source.tar.gz releases/inherited-0.43.sha256 \
 logs/nft-ed-0.43.log logs/readers-0.42.log logs/mpv-0.41.log >releases/inherited-0.44.sha256
bash archive-source.sh
python3 - <<'PY' >releases/source-0.44.sha256
import hashlib,runpy
from pathlib import Path
names=set(runpy.run_path('package-base.py')['RUNTIME'])|{
 'package-base.py','package-initramfs.py','build.sh','boot.sh','archive-source.sh',
 'archive-tools-044.sh','prepare-ssh-component-044.py','tools-archive-paths-044.py','ssh-archive-paths-044.py'}
for name in sorted(names):print(hashlib.sha256(Path(name).read_bytes()).hexdigest(),name)
PY
sha256sum images/confos-0.44-clean.work/root.sqfs images/confos-0.44-clean.work/initramfs \
 images/confos-0.44-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.44.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
 bash verify-payload-inventory.sh 0.44 ../cases/inventory/inventory
