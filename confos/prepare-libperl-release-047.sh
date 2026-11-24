#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/prepare-libperl-0.47.log 2>&1
python3 prepare-libperl-047.py >logs/reader-inheritance-0.47.log
python3 package-base.py packages/confos-runtime_0.47_all.deb
python3 check-runtime-source-package.py 0.47
bash build.sh examples/development.conf images/confos-0.47-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.47.log
bash probe-libperl-047.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.47.log
echo 'CANDIDATE47 LIBPERL AND REGRESSIONS PASS'
