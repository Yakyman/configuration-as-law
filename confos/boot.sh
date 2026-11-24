#!/bin/bash
set -euo pipefail
if [ "$#" -lt 4 ] || [ "$#" -gt 5 ]; then echo 'usage: boot.sh DISK SSH_PORT MEMORY_MIB SERIAL_LOG [QMP_SOCKET]' >&2; exit 2; fi
disk=$(realpath "$1")
port=$2
memory=$3
log=$(realpath -m "$4")
qmp=$(realpath -m "${5:-$4.qmp}")
[[ $port =~ ^[0-9]+$ && $memory =~ ^[0-9]+$ && $memory -le 8192 && $memory -ge 512 ]]
mkdir -p "$HOME/VMs/confos/slots"
launch() {
        exec qemu-system-x86_64 -enable-kvm -machine q35 -cpu host -smp 2 -m "$memory" \
          -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
          -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_VARS_4M.fd \
          -drive "file=$disk,format=qcow2,if=virtio,cache=none" \
          -netdev "user,id=n,hostfwd=tcp:127.0.0.1:$port-:22" -device virtio-net-pci,netdev=n \
          -display none -serial "file:$log" -monitor none -qmp "unix:$qmp,server=on,wait=off"
}
if [ -n "${CONFOS_SLOT_FD:-}" ]; then
    [[ $CONFOS_SLOT_FD =~ ^[0-9]+$ && $CONFOS_SLOT_FD -ge 3 ]]
    held=$(readlink "/proc/self/fd/$CONFOS_SLOT_FD")
    [[ $held == "$HOME/VMs/confos/slots/slot-"[1-6]'.lock' ]]
    flock -n "$CONFOS_SLOT_FD"
    launch
fi
attempt=0
while true; do
for slot in {1..6}; do
    exec {lock}>"$HOME/VMs/confos/slots/slot-$slot.lock"
    if flock -n "$lock"; then
        launch
    fi
    exec {lock}>&-
done
if [ "$((attempt % 6))" = 0 ]; then echo 'Waiting for a shared VM slot' >&2; fi
attempt=$((attempt + 1))
sleep 5
done
