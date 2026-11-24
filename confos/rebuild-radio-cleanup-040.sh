#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.40
test ! -e releases/confos-0.40-source.tar.gz
test "$(systemctl --user show confos-radio-probes-040 -p ActiveState --value)" = failed
test ! -e logs/radio-0.40-before-readiness-fix.log
cp logs/radio-0.40.log logs/radio-0.40-before-readiness-fix.log
cp logs/prepare-radio-0.40.log logs/prepare-radio-0.40-before-readiness-fix.log
cp logs/radio-040-fault-normal.serial logs/radio-040-fault-normal-before-readiness-fix.serial
if pgrep -f '(^|/)qemu-system-x86_64 .*images/(confos-0.40-clean|radio-040-[a-z-]+)\.qcow2'; then
 echo 'Refusing to replace an open image'; exit 1
fi
rm -f images/confos-0.40-clean.qcow2 images/radio-040-normal.qcow2 images/radio-040-systemd.qcow2 \
 images/radio-040-replica.qcow2 images/radio-040-fault-normal.qcow2 images/radio-040-fault-systemd.qcow2
rm -rf images/confos-0.40-clean.work images/radio-040-normal.work images/radio-040-systemd.work \
 images/radio-040-replica.work images/radio-040-fault-normal.work images/radio-040-fault-systemd.work radio-040-fault-source
exec bash prepare-radio-040.sh
