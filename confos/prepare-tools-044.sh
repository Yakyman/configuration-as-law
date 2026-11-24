#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.44
test -s packages/confos-code-readers_0.44_amd64.deb
exec >logs/prepare-tools-0.44.log 2>&1
python3 package-base.py packages/confos-runtime_0.44_all.deb
python3 check-runtime-source-package.py 0.44
bash build.sh examples/development.conf images/confos-0.44-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.44.log
python3 build-tools-fixture-044.py
bash probe-tools-044.sh
bash probe-visudo-editor-044.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.44.log
python3 check-runtime-source-package.py 0.44
echo 'CANDIDATE44 VISUDO SSH AND REGRESSIONS PASS'
