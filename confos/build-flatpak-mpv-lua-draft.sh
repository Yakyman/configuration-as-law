#!/bin/bash
# Worker-only private candidate build. No runtime integration or image mutation.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/flatpak-mpv-lua-draft-build.log 2>&1
work="$PWD/interpreter-inputs/flatpak-mpv-lua-candidate"
test ! -e "$work"
mkdir -p "$work/mpv" "$work/luajit" "$work/candidate"
printf '%s  %s\n' \
  48c4704dd6b93279e93a7f3ba48d1bab444b15d9196e400db11ea362069a891f interpreter-inputs/flatpak-readers/mpv.tar.gz \
  718f9ebb54b715ec4cd86ef1605177a9a2c1c80a0b6de4c26f3e1ccc8e5fd327 interpreter-inputs/flatpak-readers/luajit.tar.gz | sha256sum -c -
tar -xzf interpreter-inputs/flatpak-readers/mpv.tar.gz --strip-components=1 -C "$work/mpv"
tar -xzf interpreter-inputs/flatpak-readers/luajit.tar.gz --strip-components=1 -C "$work/luajit"
python3 patch-mpv-lua-stream-draft.py "$work/mpv"
python3 patch-luajit-code.py "$work/luajit"
sha256sum patch-mpv-lua-stream-draft.py patch-luajit-code.py code-file-policy.h
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
make -C "$work/luajit" -j2 BUILDMODE=dynamic PREFIX=/app \
  CC=gcc XCFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-flatpak-mpv-lua"
cp "$work/luajit/src/libluajit.so" "$work/candidate/libluajit-5.1.so.2.1.1781966178"
sha256sum "$work/candidate/libluajit-5.1.so.2.1.1781966178"
readelf -d "$work/candidate/libluajit-5.1.so.2.1.1781966178"
readelf -V "$work/candidate/libluajit-5.1.so.2.1.1781966178"
echo 'LUAJIT CANDIDATE BUILT; ABI AND CONFINED PROBES PENDING'
python3 check-flatpak-mpv-dependencies-draft.py
