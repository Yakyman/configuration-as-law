#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.44
exec >logs/tools-0.44.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
expected=$(sha256sum tools-044-fixture/inputs/declaration.conf | cut -d' ' -f1)
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22455 user@127.0.0.1 "$@"; }
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
 confos_boot_reserved images/tools-044.qcow2 22455 3072 "logs/tools-044-$boot_index.serial"
}
visudo_probe(){ guest "python3 - $1 ${2:-id}" <probe-visudo-044.py; }
ssh_probe(){
 guest 'python3 /usr/local/bin/probe-ssh-reader-guest-draft.py'
 guest 'bash -s' <ssh-root-controls-044.sh
}
apply_and_cut(){
 local stage=$1 program=${2:-id}
 expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
 guest 'sudo -n confos apply' || true
 for cycle in 1 2 3;do
  ready
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
  echo "TOOLS44 IMMEDIATE POST-APPLIED CUT $stage $cycle $expected"
  boot;ready
  if [ "$stage" = remove ];then visudo_probe removed "$program";else visudo_probe applied "$program";fi
  echo "TOOLS44 NATIVE STATE AFTER CUT PASS $stage $cycle"
 done
}
boot;ready
ssh_probe
guest 'sudo -n python3 -' <visudo-recording-include-probe.py
visudo_probe before
apply_and_cut add
visudo_probe change true
apply_and_cut change true
ssh_probe
visudo_probe remove true
apply_and_cut remove true
guest "sudo -n sed -i '/^package openssh-client /d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/bin/ssh && test ! -e /usr/bin/scp && test ! -e /usr/bin/sftp'
echo 'CANONICAL44 OPTIONAL SSH PACKAGE REMOVAL PASS'
echo 'CANONICAL44 VISUDO NINE CUTS AND SSH READERS PASS'
