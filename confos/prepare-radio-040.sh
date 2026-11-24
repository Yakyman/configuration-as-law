#!/bin/bash
# Parent starts in persistent worker unit <=8G CPUQuota100. Never auto-seal.
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.40
exec >logs/prepare-radio-0.40.log 2>&1
python3 prepare-radio-component-040.py
bash build.sh examples/development.conf images/confos-0.40-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.40.log
python3 build-radio-fixture-040.py
python3 build-radio-flatpak-fixture-040.py
bash probe-radio-flatpak-040.sh
python3 build-radio-lifecycle-fault-040.py
bash probe-radio-040.sh >logs/radio-0.40.log 2>&1
python3 check-runtime-source-package.py 0.40
echo 'CANDIDATE40 RADIO AND REGRESSIONS PASS'
