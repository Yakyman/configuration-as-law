#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.42
exec >logs/prepare-readers-0.42.log 2>&1
python3 check-optional-identity-042.py
python3 prepare-readers-042.py
bash build.sh examples/development.conf images/confos-0.42-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.42.log
python3 build-readers-fixture-042.py
bash probe-readers-042.sh
python3 check-runtime-source-package.py 0.42
echo 'CANDIDATE42 NATIVE READERS STORES AND REGRESSIONS PASS'
