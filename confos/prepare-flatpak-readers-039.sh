#!/bin/bash
# Parent launches through persistent systemd-run only after38 is sealed.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/prepare-flatpak-readers-0.39.log 2>&1
test "$(cat VERSION)" = 0.39
python3 prepare-flatpak-readers-component-039.py
./build.sh examples/development.conf images/confos-0.39-clean.qcow2
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.39.log
python3 build-flatpak-readers-fixture-039.py
bash probe-flatpak-readers-039.sh
python3 check-runtime-source-package.py 0.39
python3 check-flatpak-readers-inheritance.py
echo 'CANDIDATE39 FLATPAK READERS AND REGRESSIONS PASS'
