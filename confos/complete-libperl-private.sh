#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
work="$PWD/interpreter-inputs/libperl-private"
exec >"$work/rebuild-third.log" 2>&1
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export LD_LIBRARY_PATH="$work/dependencies/usr/lib/x86_64-linux-gnu"
cd "$work/source"
debian/gen-patchlevel -p DEBPKG: -v 5.40.1-6+deb13u1 debian/patches/series >patchlevel-debian.h
ln -s ../patchlevel-debian.h build-shared/patchlevel-debian.h
make -j2 -C build-shared 'SHRPLDFLAGS=$(LDDLFLAGS) -Wl,-soname,libperl.so.5.40' libperl.so.5.40.1
cp build-shared/libperl.so.5.40.1 "$work/candidate.so"
cp build-shared/config.sh build-shared/config.h "$work/"
readelf -d "$work/candidate.so" >"$work/candidate-dynamic.txt"
nm -D --defined-only "$work/candidate.so" >"$work/candidate-symbols.txt"
sha256sum "$work/candidate.so"
echo 'PRIVATE LIBPERL CANDIDATE BUILT; ABI AND GUEST CONTROLS REQUIRED'
