#!/bin/bash
set -euo pipefail
# Invoke from the server laboratory root through a persistent user service.
cd "${LAB_ROOT:?}"
d=fix-c1-1/opensuse
iso=images/openSUSE-Tumbleweed-DVD-x86_64-Snapshot20261120-Media.iso
xorriso -osirrox on -indev "$iso" -extract /boot/x86_64/loader/linux "$d/linux" -extract /boot/x86_64/loader/initrd "$d/initrd" >/dev/null 2>&1
test ! -e "$d/installation.qcow2"
qemu-img create -q -f qcow2 "$d/installation.qcow2" 40G
for slot in {1..12}; do
  exec {slotfd}>"slots/slot-$slot.lock"
  if flock -n "$slotfd"; then
    exec qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -cpu host -display none \
      -kernel "$d/linux" -initrd "$d/initrd" \
      -append 'console=ttyS0,115200n8 textmode=1 install=cd:/ language=en_US' \
      -drive file="$d/installation.qcow2",format=qcow2,if=virtio \
      -drive file="$iso",media=cdrom,readonly=on \
      -netdev user,id=n0 -device virtio-net-pci,netdev=n0,mac=52:54:00:ca:10:01 \
      -serial unix:"$d/install.sock",server=on,wait=off \
      -qmp unix:"$d/qmp.sock",server=on,wait=off -monitor none -no-reboot
  fi
  exec {slotfd}>&-
done
exit 75
