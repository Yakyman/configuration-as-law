#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.45
exec >logs/prepare-radio-recording-0.45.log 2>&1
python3 prepare-readers-045.py >logs/reader-inheritance-0.45.log
python3 package-base.py packages/confos-runtime_0.45_all.deb
python3 check-runtime-source-package.py 0.45
bash build.sh examples/development.conf images/confos-0.45-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.45.log
bash probe-radio-recording-045.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.45.log
echo 'CANDIDATE45 RADIO RECORDING AND REGRESSIONS PASS'
