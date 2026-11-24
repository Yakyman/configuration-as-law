#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
work="$PWD/interpreter-inputs/libpython-private"
exec >"$work/rebuild.log" 2>&1
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
python3 libpython-debian-modules-private.py
cd "$work/source"
make -j2 libpython3.13.so
cp libpython3.13.so.1.0 "$work/candidate.so"
readelf -d "$work/candidate.so" >"$work/candidate-dynamic.txt"
nm -D --defined-only "$work/candidate.so" >"$work/candidate-symbols.txt"
sha256sum "$work/candidate.so"
echo 'PRIVATE LIBPYTHON DEBIAN MODULES CANDIDATE BUILT'
