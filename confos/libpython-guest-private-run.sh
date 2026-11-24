#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test ! -e libpython-guest-private
exec >logs/libpython-guest-private.log 2>&1
source slots.sh
cleanup(){
 local status=$?
 confos_stop_reserved
 python3 libpython-guest-private-cleanup.py "$status"
 exit "$status"
}
trap cleanup EXIT
python3 libpython-guest-private-build.py
confos_reserve_guest
confos_boot_reserved libpython-guest-private/disk.qcow2 22460 3072 logs/libpython-guest-private.serial
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -i private/login -p 22460 user@127.0.0.1 "$@"; }
expected=$(sha256sum libpython-guest-private/inputs/declaration.conf | cut -d' ' -f1)
ready=0
for attempt in {1..150};do
 if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
guest 'python3 /usr/local/bin/embedded-python-private-probe.py'
