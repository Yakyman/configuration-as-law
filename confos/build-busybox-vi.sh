#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/busybox-vi-build.log 2>&1
sha256sum -c busybox-source.sha256
work="$PWD/interpreter-inputs/busybox-vi"
test ! -e "$work"
dpkg-source --no-check -x interpreter-inputs/busybox/busybox_1.37.0-6.dsc "$work"
python3 patch-busybox-code.py "$work"
python3 patch-busybox-vi.py "$work"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-code-readers"
cd "$work"
cp debian/config/pkg/static .config
make oldconfig </dev/null
make -j2 "EXTRA_CFLAGS=$CFLAGS"
sha256sum busybox
echo 'BUSYBOX VI BUILD PASS'
