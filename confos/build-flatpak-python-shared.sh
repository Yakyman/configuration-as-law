#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/flatpak-python-shared-build.log 2>&1
source slots.sh
confos_reserve_guest
work="$PWD/interpreter-inputs/flatpak-python-shared"
test ! -e "$work"
mkdir "$work"
archive=interpreter-inputs/flatpak-readers/python.tar.gz
printf '%s  %s\n' 653ee08c275a61b74e0d78e5d2d22a7be36b57dc4568fcdf7e20df3b0b417087 "$archive" | sha256sum -c -
tar -xzf "$archive" --strip-components=1 -C "$work"
patchfile="$PWD/interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/python3/python3-multiarch-include.patch"
printf '%s  %s\n' 0c23f1bbc4ddfe9a5836091f64ccf4f31e47c9e944e19c7d30db8c76c0fff271 "$patchfile" | sha256sum -c -
patch -d "$work" -p1 <"$patchfile"
python3 patch-flatpak-python.py "$work"
sha256sum patch-flatpak-python.py patch-python-code.py code-file-policy.h
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export CFLAGS="-O2 -pipe -g -Wp,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer -O3 -ffile-prefix-map=$work=/usr/src/confos-flatpak-python"
export LDFLAGS="-Wl,-z,relro,-z,now -Wl,--as-needed"
cd "$work"
./configure --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/bin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib/x86_64-linux-gnu --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/usr/com --mandir=/usr/share/man --infodir=/usr/share/info --disable-static --build=x86_64-unknown-linux-gnu --host=x86_64-unknown-linux-gnu lt_cv_sys_lib_dlsearch_path_spec=/usr/lib/x86_64-linux-gnu --enable-shared --without-ensurepip --with-system-expat --with-system-ffi --enable-loadable-sqlite-extensions --with-dbmliborder=gdbm --with-lto --with-conf-includedir=/usr/include/x86_64-linux-gnu --without-static-libpython --with-platlibdir=lib
make -j2
make -j2 regen-importlib
make -j2
sha256sum python libpython3.14.so.1.0
readelf -d python
readelf -d libpython3.14.so.1.0
readelf -V libpython3.14.so.1.0
echo 'SHARED CORE BUILD COMPLETE; ORIGINAL RUNTIME CHECKS PENDING'

