#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.41
grep -qx 'CANDIDATE41 MPV AND REGRESSIONS PASS' logs/prepare-mpv-0.41.log
grep -qx 'CANONICAL41 MPV LUA JS AND INHERITED READERS PASS' logs/mpv-0.41.log
grep -qx 'SMOKE PASS' logs/smoke-0.41.log
python3 check-runtime-source-package.py 0.41 >logs/runtime-source-package-0.41.log
python3 interpreter-inputs/flatpak-mpv-js-integration41-draft/verify-component.py >logs/reader-inheritance-0.41.log
cmp packages/confos-code-readers_0.41_amd64.deb interpreter-inputs/flatpak-mpv-js-integration41-draft/confos-code-readers_0.41_amd64.deb
cp mpv-041-fixture/declaration.conf records/mpv-041-fixture.conf
sha256sum releases/confos-0.40-source.tar.gz releases/inherited-0.40.sha256 \
    logs/radio-0.40.log logs/radio-flatpak-0.40.log logs/flatpak-readers-0.39.log \
    logs/configuration-recording-0.38.log >releases/inherited-0.41.sha256
bash archive-source.sh
python3 - <<'PY' >releases/source-0.41.sha256
import hashlib, runpy
from pathlib import Path
names = set(runpy.run_path('package-base.py')['RUNTIME']) | {
    'package-base.py', 'package-initramfs.py', 'build.sh', 'boot.sh',
    'flatpak_readers.py', 'archive-source.sh', 'archive-mpv-041.sh',
    'flatpak-mpv-js-archive41-paths-draft.py', 'prepare-mpv-component-041.py'}
for name in sorted(names):
    print(hashlib.sha256(Path(name).read_bytes()).hexdigest(), name)
PY
sha256sum images/confos-0.41-clean.work/root.sqfs images/confos-0.41-clean.work/initramfs \
    images/confos-0.41-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.41.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
    bash verify-payload-inventory.sh 0.41 ../cases/inventory/inventory
