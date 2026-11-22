#!/bin/bash
set -euo pipefail
cd "$HOME/VMs/cal-1122"
exec 9>slots/slot-11.lock
flock -n 9
exec qemu-system-x86_64 -enable-kvm -cpu host -m 4096 -smp 2 -display none -serial file:C1/install/talos/console.log -monitor unix:C1/install/talos/monitor.sock,server=on,wait=off -drive file=C1/base/talos.qcow2,if=virtio,format=qcow2 -cdrom images/talos-metal-amd64.iso -boot once=d -netdev user,id=n1,hostfwd=tcp:127.0.0.1:50111-:50000 -device virtio-net-pci,netdev=n1,mac=52:54:00:ca:10:01 -netdev user,id=n2,net=10.0.3.0/24 -device virtio-net-pci,netdev=n2,mac=52:54:00:ca:10:02
