#!/usr/bin/env bash
set -euo pipefail
cd "${CAL_LAB_ROOT:-$HOME/VMs/cal-1122}"
for slot in {1..12}; do
  exec {lock}>"slots/slot-$slot.lock"
  if flock -n "$lock"; then
    exec qemu-system-x86_64 -enable-kvm -cpu host -m 4096 -smp 2 -display none -monitor unix:install/guix/monitor.sock,server=on,wait=off -chardev socket,id=serial,path=install/guix/serial.sock,server=on,wait=off,logfile=install/guix/boot.log -serial chardev:serial -drive file=C1/base/guix.qcow2,if=virtio,format=qcow2 -drive file=images/guix.iso,media=cdrom,readonly=on -drive file=install/guix/input.iso,media=cdrom,readonly=on -kernel install/guix/bzImage -initrd install/guix/initrd -append 'root=31393730-3031-3031-3139-313133333833 gnu.system=/gnu/store/63qbjpi3vph650zyr1mayjpgh8h39vj3-system gnu.load=/gnu/store/63qbjpi3vph650zyr1mayjpgh8h39vj3-system/boot modprobe.blacklist=radeon,amdgpu console=tty0 console=ttyS0,115200n8' -netdev user,id=n0 -device virtio-net-pci,netdev=n0,mac=52:54:00:ca:10:01 -netdev user,id=n1 -device virtio-net-pci,netdev=n1,mac=52:54:00:ca:10:02
  fi
  exec {lock}>&-
done
exit 75
