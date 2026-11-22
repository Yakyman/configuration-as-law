#!/usr/bin/env bash
set -euo pipefail
exec >/dev/null 2>&1
status=/run/install-output/install-status.txt
trap 'rc=$?; printf "installation_exit=%s\n" "$rc" >> "$status"' EXIT
printf 'stage=partition\n' >> "$status"
parted -s /dev/vda -- mklabel msdos mkpart primary ext4 1MiB 100% set 1 boot on
printf 'stage=format\n' >> "$status"
mkfs.ext4 -F -L nixos /dev/vda1
printf 'stage=mount\n' >> "$status"
udevadm settle
mount /dev/vda1 /mnt
printf 'stage=generate\n' >> "$status"
nixos-generate-config --root /mnt
cp /mnt/etc/nixos/hardware-configuration.nix /run/install-output/hardware-configuration.nix
printf 'hardware_capture_before_install=0\n' >> "$status"
cp /run/install-input/configuration.nix /mnt/etc/nixos/configuration.nix
printf 'stage=install\n' >> "$status"
nixos-install --no-root-passwd
printf 'nixos_install_exit=0\n' >> "$status"
sync
poweroff
