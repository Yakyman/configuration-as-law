#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/radio-lifecycle-private.log 2>&1
if [ "${RADIO_PREBUILT:-0}" != 1 ];then python3 radio-lifecycle-private.py;fi
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved radio-lifecycle-private/disk.qcow2 22447 3072 logs/radio-lifecycle-private.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22447 user@127.0.0.1)
guest() { ssh "${args[@]}" "$@"; }
wanted=$(sha256sum radio-lifecycle-private/inputs/declaration.conf | cut -d' ' -f1)
ready=0
for attempt in {1..150};do
 if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $wanted" ];then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
guest 'test "$(cat /proc/1/comm)" = systemd; python3 /usr/local/bin/radio-mutation-probe.py; sudo -n python3 /usr/local/bin/radio-mutation-probe.py'
grep -q 'WPA2-CCMP connected; AP traffic verified' logs/radio-lifecycle-private.serial
grep -q 'AUTHENTICATED BIDIRECTIONAL L2CAP PASS' logs/radio-lifecycle-private.serial
echo 'PRIVATE SYSTEMD RADIO READY AND CONTROLS PASS'
guest 'sudo -n touch /run/radio-fault-request'
sleep 5
grep -q 'RADIO TRUSTED FAULT INJECTED' logs/radio-lifecycle-private.serial
if guest 'confos status';then echo 'FAIL: READY AFTER RADIO DEATH';exit 1;fi
grep -q 'RADIO TRUSTED READINESS FILES REVOKED' logs/radio-lifecycle-private.serial
echo 'PRIVATE SYSTEMD RADIO DEATH REVOKES READY PASS'
