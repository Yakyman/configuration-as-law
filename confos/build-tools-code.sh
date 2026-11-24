#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/tools-code-build.log 2>&1
work="$PWD/interpreter-inputs/tools/trees"
sha256sum -c tools-source.sha256
rm -rf "$work/dash" "$work/mawk" "$work/gawk" "$work/sed"
bash extract-tools-sources.sh
python3 patch-tools-code.py "$work"
python3 normalize-reader-times.py "$work/dash" "$work/mawk" "$work/gawk" "$work/sed"
dependency_root="$PWD/interpreter-inputs/tools/dependencies/root"
test -f "$dependency_root/usr/include/mpfr.h"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-tools -ffile-prefix-map=$dependency_root=/usr/src/confos-tools-deps"
export CPPFLAGS="-D_GNU_SOURCE -I$dependency_root/usr/include -I$dependency_root/usr/include/x86_64-linux-gnu"
export LDFLAGS="-L$dependency_root/usr/lib/x86_64-linux-gnu"
export LD_LIBRARY_PATH="$dependency_root/usr/lib/x86_64-linux-gnu"
export PKG_CONFIG_SYSROOT_DIR="$dependency_root"
export PKG_CONFIG_LIBDIR="$dependency_root/usr/lib/x86_64-linux-gnu/pkgconfig:$dependency_root/usr/share/pkgconfig"
for name in dash mawk gawk sed; do
    (cd "$work/$name"; if [ "$name" = dash ]; then autoreconf -fi; fi
     flags=()
     case "$name" in
         dash) flags=(--disable-fnmatch --disable-lineno --disable-glob);;
         gawk) flags=(--disable-rpath);;
         sed) flags=(--with-packager=Debian --without-included-regex);;
     esac
     ./configure --prefix=/usr --libdir=/usr/lib/x86_64-linux-gnu --disable-nls "${flags[@]}"
     case "$name" in
         gawk) make -j2 -C support; make -j2 gawk;;
         sed) make -j2 sed/sed;;
         *) make -j2;;
     esac)
done
sha256sum "$work/dash/src/dash" "$work/mawk/mawk" "$work/gawk/gawk" "$work/sed/sed/sed"
echo 'TOOLS CODE BUILD PASS'
