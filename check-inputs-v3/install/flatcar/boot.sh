#!/bin/bash
set -euo pipefail
cd "$HOME/VMs/cal-1122"
exec 9>slots/slot-9.lock
flock -n 9
exec qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -display none -serial file:C1/install/flatcar/console.log -monitor unix:C1/install/flatcar/monitor.sock,server=on,wait=off -drive file=C1/base/flatcar.qcow2,if=virtio,format=qcow2 -fw_cfg name=opt/org.flatcar-linux/config,file=C1/install/flatcar/ignition.json -netdev user,id=n1,hostfwd=tcp:127.0.0.1:2299-:22 -device virtio-net-pci,netdev=n1,mac=52:54:00:ca:10:01 -netdev user,id=n2,net=10.0.3.0/24 -device virtio-net-pci,netdev=n2,mac=52:54:00:ca:10:02
