#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/visudo-recording-private.log 2>&1
if [ "${VISUDO_RECORDING_PREBUILT:-0}" != 1 ];then python3 visudo-recording-private-build.py;fi
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved visudo-recording-private/disk.qcow2 22449 3072 logs/visudo-recording-private.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22449 user@127.0.0.1)
guest(){ ssh "${args[@]}" "$@"; }
expected=$(sha256sum visudo-recording-private/inputs/declaration.conf | cut -d' ' -f1)
ready(){
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 return 1
}
ready
guest 'sudo -n python3 -' <visudo-recording-include-probe.py
guest 'python3 -' <visudo-recording-probe.py
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
# No intervening guest command between APPLIED and the abrupt cut.
kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
echo 'VISUDO IMMEDIATE POST-APPLIED CUT add'
confos_boot_reserved visudo-recording-private/disk.qcow2 22449 3072 logs/visudo-recording-private.serial
ready
guest 'python3 - applied' <visudo-recording-probe.py
guest 'python3 - remove' <visudo-recording-probe.py
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
echo 'VISUDO IMMEDIATE POST-APPLIED CUT remove'
confos_boot_reserved visudo-recording-private/disk.qcow2 22449 3072 logs/visudo-recording-private.serial
ready
guest 'python3 - removed' <visudo-recording-probe.py
echo 'VISUDO RECORDING PRIVATE MATRIX PASS'
