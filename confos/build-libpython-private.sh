#!/bin/bash
# Worker-only bounded shared-library candidate; never edits canonical components.
set -euo pipefail
cd "$(dirname "$0")"
work="$PWD/interpreter-inputs/libpython-private"
test ! -e "$work"
mkdir -p "$work"
exec >"$work/build.log" 2>&1
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
sha256sum -c interpreter-source.sha256
cp patch-python-code.py code-file-policy.h "$work/"
sha256sum patch-python-code.py code-file-policy.h >"$work/recipe.sha256"
dpkg-source --no-check -x interpreter-inputs/debian/python3.13_3.13.5-2+deb13u5.dsc "$work/source"
python3 patch-python-code.py "$work/source"
cd "$work/source"
./configure --prefix=/usr --enable-shared --without-static-libpython --with-ensurepip=no \
 --disable-test-modules CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-libpython"
make -j2 libpython3.13.so
cp libpython3.13.so.1.0 "$work/candidate.so"
cp pyconfig.h "$work/"
readelf -d "$work/candidate.so" >"$work/candidate-dynamic.txt"
nm -D --defined-only "$work/candidate.so" >"$work/candidate-symbols.txt"
sha256sum "$work/candidate.so"
echo 'PRIVATE LIBPYTHON CANDIDATE BUILT; ABI AND GUEST CONTROLS REQUIRED'
