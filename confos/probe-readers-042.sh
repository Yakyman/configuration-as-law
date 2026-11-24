#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.42
exec >logs/readers-0.42.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
expected=$(sha256sum readers-042-fixture/declaration.conf | cut -d' ' -f1)
guest() { ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22450 user@127.0.0.1 "$@"; }
ready() {
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 echo "READINESS FAILURE $expected";return 1
}
readers() {
 guest 'rm -rf /home/user/pdb-gyp-material; python3 /usr/local/bin/pdb-gyp-native-probe.py'
 guest 'python3 /usr/local/bin/probe-curl-config-guest-draft.py'
 guest 'sudo -n python3 -' <native-config-probe-042.py
}
for cycle in 1 2;do
 confos_boot_reserved images/readers-042.qcow2 22450 3072 "logs/readers-042-$cycle.serial"
 ready
 readers
 echo "CANONICAL42 READERS AND STORES BOOT PASS $cycle"
 if [ "$cycle" = 1 ];then
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
 fi
done
guest 'test ! -e /usr/bin/ed; sudo -n apt-get install ed=1.21.1-1; test ! -e /usr/bin/ed'
test "$(guest 'confos status')" = "APPLIED $expected"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'ed --version'
guest 'sudo -n python3 -' <native-config-probe-042.py
echo 'CANONICAL42 CONFIG POLICY PRESERVES RECORDER APPLY PASS'
guest "sudo -n sed -i -e '/^package curl /d' -e '/^package gyp /d' -e '/^package libcurl4t64 /d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/bin/curl && test ! -e /usr/bin/gyp && test ! -e /usr/lib/python3/dist-packages/gyp/input.py && test -f /usr/lib/python3.13/pdb.py'
echo 'CANONICAL42 OPTIONAL PACKAGE REMOVAL PASS'
echo 'CANONICAL42 NATIVE READERS AND CONFIGURATION STORES PASS'
