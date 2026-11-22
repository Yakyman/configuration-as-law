#!/bin/bash
set -euo pipefail
cd "${LAB_ROOT:?}"
d=fix-c1-1/opensuse
# Call only after installer power-off/reboot and successful QEMU exit.
! systemctl --user is-active --quiet cal-fx1-opensuse-install
test -f "$d/installation.qcow2"
test ! -e C1/base/opensuse-fx-c1.qcow2
test ! -e C1/base/opensuse-fx-c1.json
chmod 444 "$d/installation.qcow2"
ln -s ../../fix-c1-1/opensuse/installation.qcow2 C1/base/opensuse-fx-c1.qcow2
printf '%s\n' '{"transport":"serial","user":"user","password":"cal-test"}' > C1/base/opensuse-fx-c1.json
printf 'registry_created=yes\nbacking_read_only=yes\n' > "$d/registry-status.txt"
