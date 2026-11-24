#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/flatpak-bash-compatible-build.log 2>&1
source slots.sh
confos_reserve_guest
work="$PWD/interpreter-inputs/flatpak-bash-compatible"
test ! -e "$work"
mkdir "$work"
archive=interpreter-inputs/flatpak-readers/bash.tar.gz
printf '%s  %s\n' 91a4dcfbf1c170b0f8ed619e9625813b9301e5a8f79c710d4bebb30796d56bb8 "$archive" | sha256sum -c -
tar -xzf "$archive" --strip-components=1 -C "$work"
patchfile="$PWD/interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/bash/0001-bash-config.patch"
printf '%s  %s\n' e7a38fe0c52924d0b99c3d1bbde5e01e517e810ad4b20832b47ea81733d32719 "$patchfile" | sha256sum -c -
patch -d "$work" -p1 <"$patchfile"
python3 patch-flatpak-bash.py "$work"
sha256sum patch-flatpak-bash.py code-file-policy.h
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-flatpak-bash"
cd "$work"
./configure --prefix=/usr --with-curses --with-installed-readline=/usr --enable-job-control --without-bash-malloc CC_FOR_BUILD=/usr/bin/gcc ac_cv_rl_version=8.0 bash_cv_getcwd_malloc=yes bash_cv_job_control_missing=present bash_cv_termcap_lib=libtinfo bash_cv_dev_fd=standard bash_cv_dev_stdin=present
make -j2
./bash --version
readelf -d bash
readelf -V bash
sha256sum bash
echo 'BASH DYNAMIC BUILD COMPLETE; RUNTIME CHECK PENDING'

