#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/nft-recording-private.log 2>&1
if [ "${NFT_RECORDING_PREBUILT:-0}" != 1 ];then python3 nft-recording-private-build.py;fi
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved nft-recording-private/disk.qcow2 22449 3072 logs/nft-recording-private.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22449 user@127.0.0.1)
guest(){ ssh "${args[@]}" "$@"; }
expected=$(sha256sum nft-recording-private/inputs/declaration.conf | cut -d' ' -f1)
ready(){
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 return 1
}
ready
guest 'python3 -' <nft-recording-probe.py
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'python3 - applied' <nft-recording-probe.py
# Kill immediately after confirmed APPLIED, then boot exactly the same disk.
confos_stop_reserved
confos_boot_reserved nft-recording-private/disk.qcow2 22449 3072 logs/nft-recording-private.serial
ready
guest 'python3 - remove' <nft-recording-probe.py
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'python3 - removed' <nft-recording-probe.py
confos_stop_reserved
confos_boot_reserved nft-recording-private/disk.qcow2 22449 3072 logs/nft-recording-private.serial
ready
guest 'python3 - removed' <nft-recording-probe.py
echo 'NFT RECORDING PRIVATE MATRIX PASS'
