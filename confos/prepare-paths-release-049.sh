#!/bin/bash
# Gates of 0.49. Sequential: the recorder tests share one guest port.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/prepare-paths-0.49.log 2>&1
test "$(cat VERSION)" = 0.49
python3 test-flatpak-readers-module.py
python3 prepare-readers-049.py >logs/reader-inheritance-0.49.log
python3 package-base.py packages/confos-runtime_0.49_all.deb
python3 check-runtime-source-package.py 0.49
bash build.sh examples/development.conf images/confos-0.49-clean.qcow2
python3 compare-native-entries.py images/confos-0.49-clean.work
EXTENDED=1 bash smoke.sh
cp smoke.log logs/smoke-0.49.log
bash check-other-export-049.sh
python3 test-recording-apt.py >logs/recording-apt-0.49.log 2>&1
python3 test-configuration-recording.py >logs/configuration-recording-0.49.log 2>&1
python3 test-language-recording.py >logs/language-recording-0.49.log 2>&1
python3 test-podman-recording.py >logs/podman-recording-0.49.log 2>&1
python3 test-flatpak-recording.py >logs/flatpak-recording-0.49.log 2>&1
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.49.log
echo 'CANDIDATE49 PACKAGE PATHS AND REGRESSIONS PASS'
