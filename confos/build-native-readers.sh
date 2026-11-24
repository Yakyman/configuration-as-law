#!/bin/bash
# Worker-only. Build from authenticated Debian source archives, never a live root.
set -euo pipefail
cd "$(dirname "$0")"
version=${1:-$(cat VERSION)}
mkdir -p logs
exec >"logs/native-readers-$version.log" 2>&1
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
work="$PWD/interpreter-inputs/native-$version"
mkdir -p "$work"
cleanup() { rm -rf "$work"; }
trap cleanup EXIT
sources="$PWD/interpreter-inputs/debian"
sha256sum -c interpreter-source.sha256
sha256sum -c busybox-source.sha256
gcc --version | head -1
ld --version | head -1
for pair in 'bash bash_5.2.37-2.dsc' 'python python3.13_3.13.5-2+deb13u5.dsc' 'perl perl_5.40.1-6+deb13u1.dsc'; do
    read -r name dsc <<<"$pair"
    dpkg-source --no-check -x "$sources/$dsc" "$work/$name"
done
dpkg-source --no-check -x interpreter-inputs/busybox/busybox_1.37.0-6.dsc "$work/busybox"
python3 patch-bash-code.py "$work/bash"
python3 patch-python-code.py "$work/python"
python3 patch-perl-code.py "$work/perl"
python3 patch-busybox-code.py "$work/busybox"
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-code-readers"
(cd "$work/bash"; ./configure --without-bash-malloc --disable-nls --without-installed-readline; make -j2)
(cd "$work/python"; ./configure --prefix=/usr --with-ensurepip=no --disable-test-modules; make -j2)
(cd "$work/perl"; sh Configure -des -Dprefix=/usr -Dman1dir=none -Dman3dir=none \
    -Dprivlib=/usr/share/perl/5.40 -Darchlib=/usr/lib/x86_64-linux-gnu/perl/5.40 \
    -Dotherlibdirs=/usr/lib/x86_64-linux-gnu/perl-base -Dusethreads -Duse64bitall \
    "-Doptimize=$CFLAGS"; make -j2)
(cd "$work/busybox"; cp debian/config/pkg/static .config; make oldconfig </dev/null; make -j2 "EXTRA_CFLAGS=$CFLAGS")
python3 package-code-readers.py "$version" "$work" "packages/confos-code-readers_${version}_amd64.deb"
echo 'NATIVE READERS PACKAGE PASS'
