#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.41
exec >logs/prepare-mpv-0.41.log 2>&1
python3 prepare-mpv-component-041.py
bash build.sh examples/development.conf images/confos-0.41-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.41.log
python3 build-mpv-fixture-041.py
bash probe-mpv-041.sh
python3 check-runtime-source-package.py 0.41
echo 'CANDIDATE41 MPV AND REGRESSIONS PASS'
