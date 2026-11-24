#!/bin/bash
# Future worker-only gate. Persistent unit <=4G CPUQuota100; one shared slot.
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.40
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
port=22446
sshargs=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p "$port" user@127.0.0.1)
guest() { ssh "${sshargs[@]}" "set -eu; $*"; }
wait_ready() {
 local observed
 for attempt in {1..150}; do
  observed=$(guest 'confos status' 2>/dev/null || true)
  if [ "$observed" = "APPLIED $wanted" ]; then return; fi
  sleep 2
 done
 echo "READINESS FAILURE expected $wanted";return 1
}
controls() { guest 'python3 /usr/local/bin/radio-mutation-probe.py'; guest 'sudo -n python3 /usr/local/bin/radio-mutation-probe.py'; sleep 12; wait_ready; }
boot() {
 confos_boot_reserved "$disk" "$port" 3072 "$serial";wait_ready
 if [ "${radio_absent:-0}" = 1 ];then
  grep -q 'fixture-AP-ready; client absent' "$serial"
  grep -q '0 native saved bond(s)' "$serial"
 else
  grep -q 'WPA2-CCMP connected; AP traffic verified' "$serial"
  grep -q 'AUTHENTICATED BIDIRECTIONAL L2CAP PASS' "$serial"
 fi
 if [ "${radio_absent:-0}" = 1 ];then
  guest 'python3 - absent' <probe-radio-inspection.py
 else
  guest "python3 - present ${radio_expected_address:-192.0.2.2}" <probe-radio-inspection.py
 fi
}
power_cut() { kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid; }
for kind in normal systemd; do
 radio_absent=0
 disk="images/radio-040-$kind.qcow2";serial="logs/radio-040-$kind.serial"
 wanted=$(sha256sum "radio-040-fixture/$kind.conf" | cut -d' ' -f1)
 boot
 if guest 'confos radio-inspect bluetooth';then echo 'UNAUTHORIZED RADIO INSPECTION';exit 1;fi
 if guest 'sudo -n confos radio-inspect bluetooth extra';then echo 'UNVALIDATED RADIO INSPECTION';exit 1;fi
 if [ "$kind" = systemd ]; then guest 'test "$(cat /proc/1/comm)" = systemd';fi
 controls
 power_cut;boot;controls
 guest 'sudo -n cp /state/declaration.conf /state/radio-complete.conf; sudo -n cp /usr/local/share/radio-client-alt.json /state/client-alt.json'
 # Three cuts each after changing, removing and adding rows. Each readiness
 # requires native traffic (or explicit absent-client/bond status) at boot.
 for repetition in 1 2 3; do
  for phase in change remove add; do
   case "$phase" in
    change) radio_absent=0;radio_expected_address=192.0.2.3;alt=$(sha256sum radio-040-fixture/client-alt.json | cut -d' ' -f1);guest "sudo -n sed -i 's/^network .*/network saved $alt client-alt.json/' /state/declaration.conf";;
    remove) radio_absent=1;guest "sudo -n sed -i '/^network /d;/^bluetooth-pair /d' /state/declaration.conf";;
    add) radio_absent=0;radio_expected_address=192.0.2.2;guest 'sudo -n cp /state/radio-complete.conf /state/declaration.conf';;
   esac
   wanted=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
   guest 'sudo -n confos apply' || true # expected reboot disconnect; exact identity required next
   wait_ready;power_cut;boot
   if [ "$phase" != remove ];then controls;fi
   echo "RADIO CUT PASS $kind $repetition $phase"
  done
 done

 confos_stop_reserved
 echo "RADIO BOOT REBOOT CONTROLS CUTS REMOVAL RESTORE PASS $kind"
done
# A separately assembled clean disk from the exact same normal declaration.
radio_absent=0
disk=images/radio-040-replica.qcow2;serial=logs/radio-040-replica.serial
wanted=$(sha256sum radio-040-fixture/normal.conf | cut -d' ' -f1)
boot;controls
confos_stop_reserved
echo 'RADIO INDEPENDENT CLEAN NATIVE REPLAY PASS'
# Private fault images differ ONLY in a trusted boot trigger; no production escape.
for kind in normal systemd; do
 radio_absent=0
 disk="images/radio-040-fault-$kind.qcow2";serial="logs/radio-040-fault-$kind.serial"
 wanted=$(sha256sum "radio-040-fixture/$kind.conf" | cut -d' ' -f1)
 boot;controls
 guest 'sudo -n touch /run/radio-fault-request'
 for attempt in {1..25};do
  if grep -q 'RADIO TRUSTED READINESS FILES REVOKED' "$serial";then break;fi
  sleep 1
 done
 grep -q 'RADIO TRUSTED FAULT INJECTED' "$serial"
 grep -q 'RADIO TRUSTED READINESS FILES REVOKED' "$serial"
 if guest 'confos status' >"logs/radio-040-$kind-death.log" 2>&1;then
  echo "UNRESOLVED LIFECYCLE FAILURE $kind: status succeeded after radio supervisor death";exit 1
 fi
 confos_stop_reserved
 echo "RADIO SUPERVISOR DEATH READINESS REVOKED $kind"
done
echo 'CANONICAL40 RADIO GATES PASS' 
