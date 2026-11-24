#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/make-code-build.log 2>&1
work="$PWD/interpreter-inputs/tools/trees/make"
rm -rf "$work"
dpkg-source --no-check -x interpreter-inputs/tools/make-dfsg_4.4.1-2.dsc "$work"
python3 patch-make-code.py "$work"
python3 normalize-reader-times.py "$work"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-make"
export CPPFLAGS=-D_GNU_SOURCE
cd "$work"
AUTOPOINT=true autoreconf -fi
./configure --prefix=/usr --disable-nls --without-guile
make -j2
sha256sum make
echo 'MAKE CODE BUILD PASS'
