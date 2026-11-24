#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.39
grep -qx 'CANDIDATE39 FLATPAK READERS AND REGRESSIONS PASS' logs/prepare-flatpak-readers-0.39.log
grep -qx 'CANONICAL39 FLATPAK READER INTEGRATION TEST PASS' logs/flatpak-readers-0.39.log
grep -qx 'SMOKE PASS' logs/smoke-0.39.log
python3 check-runtime-source-package.py 0.39 >logs/runtime-source-package-0.39.log
python3 check-flatpak-readers-inheritance.py >logs/reader-inheritance-0.39.log
sha256sum releases/confos-0.38-source.tar.gz releases/inherited-0.38.sha256 \
    logs/flatpak-recording-0.36.log logs/podman-recording-0.37.log \
    logs/configuration-recording-0.38.log >releases/inherited-0.39.sha256
# Keep the fixture recipe and result; avoid duplicate bundle copies in examples.
if [ -f examples/flatpak-readers-039.conf ];then
    cp examples/flatpak-readers-039.conf records/flatpak-readers-039-fixture.conf
fi
test -s records/flatpak-readers-039-fixture.conf
rm -f examples/flatpak-readers-039.conf examples/runtime.flatpak examples/mpv.flatpak \
    examples/recorded-flatpak-bash.sh examples/recorded-flatpak-python.py examples/recorded_flatpak_module.py
bash archive-source.sh
python3 - <<'PY' >releases/source-0.39.sha256
import hashlib, runpy
from pathlib import Path
names = set(runpy.run_path('package-base.py')['RUNTIME']) | {
    'package-base.py', 'package-initramfs.py', 'build.sh', 'boot.sh',
    'flatpak_readers.py', 'package-flatpak-reader-overrides.py', 'archive-source.sh',
    'flatpak-readers-archive-paths.py', 'check-flatpak-readers-inheritance.py'}
for name in sorted(names):
    print(hashlib.sha256(Path(name).read_bytes()).hexdigest(), name)
PY
sha256sum images/confos-0.39-clean.work/root.sqfs images/confos-0.39-clean.work/initramfs \
    images/confos-0.39-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.39.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
    bash verify-payload-inventory.sh 0.39 ../cases/inventory/inventory
