#!/usr/bin/env bash
set -euo pipefail
cd "${CAL_LAB_ROOT:?Set the laboratory root}"
new=C1/fix-c1-1/nixos
mkdir -p "$new/input" "$new/output"
# Copy the supplied declaration and install.sh to input/ and the launch/driver here first.
test ! -e "$new/base-attempt2.qcow2"
qemu-img create -f qcow2 "$new/base-attempt2.qcow2" 32G
systemd-run --user --quiet --collect --unit cal-fx-c1-nixos-install --working-directory="$PWD" bash "$new/launch.sh"
systemd-run --user --quiet --collect --unit cal-fx-c1-nixos-drive --working-directory="$PWD" python3 "$new/drive-install.py"
