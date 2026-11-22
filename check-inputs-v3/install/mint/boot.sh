#!/bin/bash
set -euo pipefail
cd "$HOME/VMs/cal-1122"
exec 9>slots/slot-10.lock
flock -n 9
exec qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -display none -serial file:C1/install/mint/console.log -monitor unix:C1/install/mint/monitor.sock,server=on,wait=off -drive file=C1/base/mint.qcow2,if=virtio,format=qcow2 -cdrom images/mint-linuxmint-22.3-cinnamon-64bit.iso -kernel C1/install/mint/vmlinuz -initrd C1/install/mint/initrd-seeded.lz -append 'boot=casper automatic-ubiquity noprompt noeject console=tty0 console=ttyS0,115200n8 locale=en_US.UTF-8 keyboard-configuration/layoutcode=us file=/preseed.cfg ---' -netdev user,id=n1 -device virtio-net-pci,netdev=n1,mac=52:54:00:ca:10:01 -netdev user,id=n2,net=10.0.3.0/24 -device virtio-net-pci,netdev=n2,mac=52:54:00:ca:10:02
