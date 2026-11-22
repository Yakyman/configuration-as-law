#!/usr/bin/env bash
set -euo pipefail
cd "${CAL_LAB_ROOT:-$HOME/VMs/cal-1122}"
for slot in {1..12}; do
  exec {lock}>"slots/slot-$slot.lock"
  if flock -n "$lock"; then
    exec qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -display none -monitor none -serial unix:C1/fix-c1-1/nixos/serial.sock,server=on,wait=off -drive file=C1/fix-c1-1/nixos/base-attempt2.qcow2,if=virtio,format=qcow2 -cdrom images/nixos.iso -kernel install/nixos/boot/store/klj5d351lajhxbajijm835lj9cqsgw0j-linux-6.18.64/bzImage -initrd install/nixos/boot/store/q7qxm83pxydvy7p105vvsjvqh4bnl0js-initrd-linux-6.18.64/initrd -append 'init=/nix/store/93qkxicg8zs65a674p005s2wkdf5cg0y-nixos-system-nixos-26.05.14979.94c3211b0ee8/init nohibernate root=fstab loglevel=3 console=ttyS0,115200n8' -netdev user,id=n0 -device virtio-net-pci,netdev=n0,mac=52:54:00:ca:10:01 -netdev user,id=n1 -device virtio-net-pci,netdev=n1,mac=52:54:00:ca:10:02 -virtfs local,path=C1/fix-c1-1/nixos/input,mount_tag=input,security_model=none,readonly=on -virtfs local,path=C1/fix-c1-1/nixos/output,mount_tag=output,security_model=none
  fi
  exec {lock}>&-
done
exit 75
