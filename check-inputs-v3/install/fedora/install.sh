#!/bin/bash
set -euo pipefail
# Run from the laboratory root on the server after image verification.
cd "$(dirname "$0")/../../.."
root=$PWD
mkdir -p C1/base slots
[ -f C1/fedora/squashfs.img ] || xorriso -osirrox on -indev images/Fedora-Workstation-Live-45-1.4.x86_64.iso -extract /LiveOS/squashfs.img C1/fedora/squashfs.img
qemu-img create -f qcow2 C1/base/fedora.qcow2 40G
for slot in {1..12}; do
  exec {slotfd}>"slots/slot-$slot.lock"
  if flock -n "$slotfd"; then
    exec qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -cpu host -display none \
      -kernel C1/fedora/vmlinuz -initrd C1/fedora/initrd.img \
      -append 'console=ttyS0,115200n8 inst.text inst.profile=fedora-workstation inst.ks=http://10.0.2.2:18081/fedora/ks.cfg inst.stage2=https://dl.fedoraproject.org/pub/fedora/linux/releases/45/Everything/x86_64/os/ ip=dhcp' \
      -drive file=C1/base/fedora.qcow2,format=qcow2,if=virtio \
      -netdev user,id=n0 -device virtio-net-pci,netdev=n0,mac=52:54:00:ca:10:01 \
      -serial file:C1/fedora/install-console.log -monitor none -no-reboot
  fi
  exec {slotfd}>&-
done
printf '%s\n' 'No free VM slot' >&2
exit 75
