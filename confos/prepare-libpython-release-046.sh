#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/prepare-libpython-0.46.log 2>&1
python3 prepare-libpython-046.py >logs/reader-inheritance-0.46.log
python3 package-base.py packages/confos-runtime_0.46_all.deb
python3 check-runtime-source-package.py 0.46
bash build.sh examples/development.conf images/confos-0.46-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.46.log
bash probe-libpython-046.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.46.log
echo 'CANDIDATE46 LIBPYTHON AND REGRESSIONS PASS'
