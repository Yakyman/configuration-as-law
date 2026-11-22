#!/bin/sh
set -eu
parted -s /dev/vda -- mklabel msdos mkpart primary ext4 1MiB 100% set 1 boot on
mkfs.ext4 -F -L root /dev/vda1
mount /dev/vda1 /mnt
herd start cow-store /mnt
mkdir -p /mnt/etc
cp /run/install-input/config.scm /mnt/etc/config.scm
guix system init /mnt/etc/config.scm /mnt
sync
herd power-off shepherd
