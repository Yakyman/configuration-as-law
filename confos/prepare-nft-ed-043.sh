#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.43
test -s packages/confos-code-readers_0.43_amd64.deb
exec >logs/prepare-nft-ed-0.43.log 2>&1
python3 package-base.py packages/confos-runtime_0.43_all.deb
python3 check-runtime-source-package.py 0.43
bash build.sh examples/development.conf images/confos-0.43-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.43.log
python3 build-nft-ed-fixture-043.py
bash probe-nft-ed-043.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.43.log
python3 check-runtime-source-package.py 0.43
echo 'CANDIDATE43 NFT ED AND REGRESSIONS PASS'
