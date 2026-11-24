#!/bin/bash
set -u
cd "$HOME/VMs/cal-1123" || exit 90
mkdir -p D1/talos/control
exec >D1/talos/control/run.out 2>D1/talos/control/run.err
printf 'started=%s\n' "$(date -u +%FT%TZ)" >D1/talos/control/status.txt
./lab.sh new d1-talos talos >D1/talos/control/new.out 2>D1/talos/control/new.err
new_rc=$?
printf 'new_rc=%s\n' "$new_rc" >>D1/talos/control/status.txt
if [ "$new_rc" -eq 0 ]; then
  LAB_ROOT="$PWD" C1_INPUTS_COMMIT=b3c3c141c612b8d287c8058733141cb56d1c2431 D1/inputs/collect.sh --observe d1-talos D1/talos/output >D1/talos/control/collect.out 2>D1/talos/control/collect.err
  printf 'collect_rc=%s\n' "$?" >>D1/talos/control/status.txt
fi
./lab.sh destroy d1-talos >D1/talos/control/destroy.out 2>D1/talos/control/destroy.err
printf 'destroy_rc=%s\nfinished=%s\n' "$?" "$(date -u +%FT%TZ)" >>D1/talos/control/status.txt
