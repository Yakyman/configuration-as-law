#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/libpython-0.46.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
python3 build-libpython-fixture-046.py
confos_reserve_guest
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -i private/login -p 22461 user@127.0.0.1 "$@"; }
expected=$(sha256sum libpython-046-fixture/inputs/declaration.conf | cut -d' ' -f1)
ready(){
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 return 1
}
for boot in 1 2;do
 confos_boot_reserved images/libpython-046.qcow2 22461 3072 "logs/libpython-046-$boot.serial"
 ready
 guest 'python3 /usr/local/bin/embedded-python-private-probe.py'
 guest 'python3 /usr/local/share/probe-recorded-filename-reader.py'
 if [ "$boot" = 1 ];then
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
 fi
done
guest "sudo -n sed -i '/^package libpython3.13 /d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0 && python3 -c "import fcntl, math; print(123)"'
set +e
guest '/usr/local/bin/embedded-python file /usr/local/share/embedded-recorded.py' >logs/libpython-removal-0.46.log 2>&1
result=$?
set -e
test "$result" = 3
grep -q 'dlopen:' logs/libpython-removal-0.46.log
echo 'CANONICAL46 LIBPYTHON TWO BOOTS AND REMOVAL PASS'
