#!/bin/bash
set -eu
systemctl --user stop cal-b1-vm.service
if systemctl --user is-active --quiet cal-b1-vm.service; then
    printf 'VM_STILL_ACTIVE\n'
    exit 1
fi
printf 'VM_INACTIVE\n'
flock -n "$HOME/VMs/cal-1122/slots/slot-2.lock" true
printf 'SLOT_2_UNLOCKED\n'
cd "$HOME/VMs/cal-1122/B1"
rm -f -- image.qcow2 SHA512SUMS image-hash.txt download-status.txt guest-key guest-key.pub user-data meta-data seed.iso serial.log known_hosts setup.log setup-status.txt backports.log backports-status.txt guest-probe.py
cd ..
rmdir B1
printf 'TASK_SERVER_DIRECTORY_REMOVED\n'
date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
