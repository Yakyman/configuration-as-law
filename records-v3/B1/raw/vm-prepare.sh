#!/bin/bash
set -eu
cd "$HOME/VMs/cal-1122/B1"
expected=$(awk '$2 ~ /debian-13-genericcloud-amd64.qcow2$/ {print $1}' SHA512SUMS)
actual=$(sha512sum image.qcow2 | cut -d ' ' -f1)
test -n "$expected"
test "$expected" = "$actual"
printf 'IMAGE_SHA512 %s\n' "$actual"
ssh-keygen -q -t ed25519 -N '' -C task-probe -f guest-key
pubkey=$(cat guest-key.pub)
cat > user-data <<EOF
#cloud-config
hostname: probe
manage_etc_hosts: true
disable_root: false
ssh_pwauth: false
users:
  - name: root
    ssh_authorized_keys:
      - $pubkey
EOF
printf 'instance-id: b1-probe-01\nlocal-hostname: probe\n' > meta-data
cloud-localds seed.iso user-data meta-data
qemu-img resize image.qcow2 8G
systemd-run --user --unit=cal-b1-vm --property=MemoryMax=4G --property=CPUQuota=200% /usr/bin/flock -n "$HOME/VMs/cal-1122/slots/slot-2.lock" /usr/bin/qemu-system-x86_64 -enable-kvm -cpu host -smp 2 -m 3072 -nographic -monitor none -serial "file:$HOME/VMs/cal-1122/B1/serial.log" -drive "file=$HOME/VMs/cal-1122/B1/image.qcow2,format=qcow2,if=virtio" -drive "file=$HOME/VMs/cal-1122/B1/seed.iso,format=raw,if=virtio,readonly=on" -netdev user,id=n1,hostfwd=tcp:127.0.0.1:22382-:22 -device virtio-net-pci,netdev=n1
