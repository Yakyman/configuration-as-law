#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.43
exec >logs/nft-ed-0.43.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
expected=$(sha256sum nft-ed-043-fixture/declaration.conf | cut -d' ' -f1)
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22450 user@127.0.0.1 "$@"; }
ready(){
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 echo "READINESS FAILURE $expected";return 1
}
boot_index=0
boot(){
 boot_index=$((boot_index+1))
 confos_boot_reserved images/nft-ed-043.qcow2 22450 3072 "logs/nft-ed-043-$boot_index.serial"
}
apply_and_cut(){
 local state=$1 verdict=${2:-accept}
 expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
 guest 'sudo -n confos apply' || true
 for cycle in 1 2 3;do
  ready
  # No guest assertion or inspection between APPLIED and the host power cut.
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
  echo "NFT43 IMMEDIATE POST-APPLIED CUT $state $cycle $expected"
  boot
  ready
  if [ "$state" = remove ];then nft_probe removed "$verdict";else nft_probe verified "$verdict";fi
  echo "NFT43 NATIVE STATE AFTER CUT PASS $state $cycle"
 done
 ready
}
nft_probe(){ guest "python3 - $1 ${2:-accept}" <nft-recording-probe-043.py; }
ed_probe(){
 guest 'rm -rf /home/user/ed-reader-material; python3 /usr/local/bin/probe-ed-reader-guest-draft.py'
 guest 'sudo -n python3 -' <ed-root-probe-043.py
}
boot;ready
ed_probe
nft_probe before accept
apply_and_cut add
nft_probe applied accept
nft_probe remove accept
nft_probe before drop
apply_and_cut change drop
nft_probe applied drop
ed_probe
nft_probe remove drop
apply_and_cut remove drop
nft_probe removed drop
guest "sudo -n sed -i '/^package ed /d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/bin/ed && test ! -e /usr/bin/red'
echo 'CANONICAL43 OPTIONAL ED RED REMOVAL PASS'
echo 'CANONICAL43 NFT RECORDING NINE CUTS AND ED READERS PASS'
