#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.43
grep -qx 'CANDIDATE43 NFT ED AND REGRESSIONS PASS' logs/prepare-nft-ed-0.43.log
grep -qx 'CANONICAL43 NFT RECORDING NINE CUTS AND ED READERS PASS' logs/nft-ed-0.43.log
grep -qx 'SMOKE PASS' logs/smoke-0.43.log
grep -qx 'UPDATES PASS' logs/updates-0.43.log
python3 check-runtime-source-package.py 0.43 >logs/runtime-source-package-0.43.log
python3 check-reader-inheritance-043.py >logs/reader-inheritance-0.43.log
cp nft-ed-043-fixture/declaration.conf records/nft-ed-043-fixture.conf
sha256sum releases/confos-0.42-source.tar.gz releases/inherited-0.42.sha256 \
 logs/readers-0.42.log logs/mpv-0.41.log logs/radio-0.40.log >releases/inherited-0.43.sha256
bash archive-source.sh
python3 - <<'PY' >releases/source-0.43.sha256
import hashlib,runpy
from pathlib import Path
names=set(runpy.run_path('package-base.py')['RUNTIME'])|{
 'package-base.py','package-initramfs.py','build.sh','boot.sh','archive-source.sh',
 'archive-nft-ed-043.sh','prepare-nft-ed-component-043.py','nft-ed-archive-paths-043.py'}
for name in sorted(names):print(hashlib.sha256(Path(name).read_bytes()).hexdigest(),name)
PY
sha256sum images/confos-0.43-clean.work/root.sqfs images/confos-0.43-clean.work/initramfs \
 images/confos-0.43-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.43.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
 bash verify-payload-inventory.sh 0.43 ../cases/inventory/inventory
