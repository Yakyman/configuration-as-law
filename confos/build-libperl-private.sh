#!/bin/bash
# Worker-only repair candidate, using the package's native shared-build configuration.
set -euo pipefail
cd "$(dirname "$0")"
work="$PWD/interpreter-inputs/libperl-private"
test ! -e "$work"
mkdir -p "$work"
exec >"$work/build.log" 2>&1
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export DEB_CFLAGS_MAINT_APPEND="-ffile-prefix-map=$work=/usr/src/confos-libperl"
sha256sum -c interpreter-source.sha256
cp patch-perl-code.py code-file-policy.h "$work/"
dpkg-source --no-check -x interpreter-inputs/debian/perl_5.40.1-6+deb13u1.dsc "$work/source"
python3 patch-perl-code.py "$work/source"
cd "$work/source"
bash debian/config.debian --shared
cp confos-code-file-policy.h build-shared/
make -j2 -C build-shared libperl.so.5.40.1
cp build-shared/libperl.so.5.40.1 "$work/candidate.so"
cp build-shared/config.sh build-shared/config.h "$work/"
readelf -d "$work/candidate.so" >"$work/candidate-dynamic.txt"
nm -D --defined-only "$work/candidate.so" >"$work/candidate-symbols.txt"
sha256sum "$work/candidate.so"
echo 'PRIVATE LIBPERL CANDIDATE BUILT; ABI AND GUEST CONTROLS REQUIRED'
