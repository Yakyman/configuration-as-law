#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/prepare-solver-0.48.log 2>&1
python3 prepare-readers-048.py >logs/reader-inheritance-0.48.log
python3 package-base.py packages/confos-runtime_0.48_all.deb
python3 check-runtime-source-package.py 0.48
bash build.sh examples/development.conf images/confos-0.48-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.48.log
bash probe-solver-048.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.48.log
echo 'CANDIDATE48 SOLVER AND REGRESSIONS PASS'
