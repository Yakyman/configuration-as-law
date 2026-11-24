#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
work="$PWD/interpreter-inputs/libperl-private"
exec >"$work/rebuild.log" 2>&1
python3 libperl-private-build-deps.py
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export DEB_CFLAGS_MAINT_APPEND="-ffile-prefix-map=$work=/usr/src/confos-libperl -I$work/dependencies/usr/include"
export DEB_LDFLAGS_MAINT_APPEND="-L$work/dependencies/usr/lib/x86_64-linux-gnu"
export LD_LIBRARY_PATH="$work/dependencies/usr/lib/x86_64-linux-gnu"
cd "$work/source"
bash debian/config.debian --shared
test -s build-shared/config.sh
cp confos-code-file-policy.h build-shared/
make -j2 -C build-shared libperl.so.5.40.1
cp build-shared/libperl.so.5.40.1 "$work/candidate.so"
cp build-shared/config.sh build-shared/config.h "$work/"
readelf -d "$work/candidate.so" >"$work/candidate-dynamic.txt"
nm -D --defined-only "$work/candidate.so" >"$work/candidate-symbols.txt"
sha256sum "$work/candidate.so"
echo 'PRIVATE LIBPERL CANDIDATE BUILT; ABI AND GUEST CONTROLS REQUIRED'
