#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/libperl-0.47.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
python3 build-libperl-fixture-047.py
confos_reserve_guest
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22464 user@127.0.0.1 "$@"; }
expected=$(sha256sum libperl-047-fixture/inputs/declaration.conf | cut -d' ' -f1)
ready(){
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 return 1
}
for boot in 1 2;do
 confos_boot_reserved images/libperl-047.qcow2 22464 3072 "logs/libperl-047-$boot.serial"
 ready
 guest 'python3 /usr/local/bin/embedded-perl-private-probe.py'
 if [ "$boot" = 1 ];then
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
 fi
done
guest "sudo -n sed -i '/^package libperl5.40 /d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/x86_64-linux-gnu/libperl.so.5.40.1 && python3 -c "import fcntl, math; print(123)"'
guest "perl -e 'print qq(STANDALONE PERL AFTER LIBRARY REMOVAL PASS\\n)'"
set +e
guest '/usr/local/bin/embedded-perl /usr/local/share/embedded-recorded.pl' >logs/libperl-removal-0.47.log 2>&1
result=$?
set -e
test "$result" = 3
grep -q 'dlopen:' logs/libperl-removal-0.47.log
echo 'CANONICAL47 LIBPERL TWO BOOTS AND REMOVAL PASS'
