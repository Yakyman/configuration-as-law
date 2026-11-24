#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/solver-0.48.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
test ! -e images/solver-048.qcow2
cp --reflink=auto images/confos-0.48-clean.qcow2 images/solver-048.qcow2
mkdir -p solver-048-fixture/inputs
cp examples/development.conf solver-048-fixture/inputs/declaration.conf
confos_reserve_guest
guest_once(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22466 user@127.0.0.1 "$@"; }
# A connection-level failure (ssh status 255) is retried; every request below is idempotent.
# Gate runs 2 and 3 of 0.48 ended right after the first recorded request because the
# power-cut function was named `cut` and replaced the cut command in the next pipeline,
# killing the machine (records/solver-048-second/, records/solver-048-third/).
guest(){
 local attempt status
 for attempt in 1 2 3 4 5;do
  status=0
  guest_once "$@" || status=$?
  if [ "$status" != 255 ];then return "$status";fi
  sleep 2
 done
 return 255
}
initial=$(sha256sum examples/development.conf | cut -d' ' -f1)
expected=$initial
ready(){
 for attempt in {1..180};do
  if [ "$(guest_once 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 return 1
}
boot_index=0
boot(){
 boot_index=$((boot_index+1))
 confos_boot_reserved images/solver-048.qcow2 22466 4096 "logs/solver-048-$boot_index.serial"
 ready
}
power_cut(){ kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid; }
boot
guest 'test ! -e /usr/bin/libreoffice'
request='sudo -n apt-get install libreoffice-writer=4:25.2.3-2+deb13u9'
reply=$(guest "$request");printf '%s\n' "$reply"
desired=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
test "$reply" = "RECORDED $desired; run confos apply"
test "$(guest "$request")" = "$reply"
guest "grep -qx 'package libreoffice-writer 4:25.2.3-2+deb13u9' /state/declaration.conf && test ! -e /usr/bin/libreoffice"
test "$(guest 'confos status')" = "APPLIED $initial"
power_cut;boot
test "$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)" = "$desired"
guest 'test ! -e /usr/bin/libreoffice'
expected=$desired
guest_once 'sudo -n confos apply' || true
ready;power_cut;boot
versions=$(guest 'dpkg-query -W libreoffice-writer libreoffice-core');printf '%s\n' "$versions"
printf '%s\n' "$versions" | grep -qx $'libreoffice-writer\t4:25.2.3-2+deb13u9'
printf '%s\n' "$versions" | grep -qx $'libreoffice-core\t4:25.2.3-2+deb13u9'
for content in FIRST-DOCUMENT SECOND-DOCUMENT;do
 guest "printf '%s\\n' '$content' > /home/user/solver-document.txt; timeout 45 libreoffice --headless --convert-to odt --outdir /home/user /home/user/solver-document.txt"
 guest "timeout 25 libreoffice --headless --cat /home/user/solver-document.odt | grep -q '$content'"
done
test "$(guest "$request")" = "$reply"
remove='sudo -n apt-get remove libreoffice-writer'
reply=$(guest "$remove");printf '%s\n' "$reply"
test "$reply" = "RECORDED $initial; run confos apply"
test "$(guest "$remove")" = "$reply"
guest 'test -e /usr/bin/libreoffice'
power_cut;boot
test "$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)" = "$initial"
expected=$initial
guest_once 'sudo -n confos apply' || true
ready;power_cut;boot
guest 'test ! -e /usr/bin/libreoffice && test ! -e /usr/lib/libreoffice/program/soffice.bin'
echo 'CANONICAL48 SOLVER RECORDER DOCUMENT AND REMOVAL PASS'
