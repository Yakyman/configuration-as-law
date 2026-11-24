#!/bin/bash
# Future worker-only harness; caller supplies the independently sealed44 SHA256.
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.45
exec >logs/radio-recording-0.45.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
python3 build-radio-recording-045.py
confos_reserve_guest
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22458 user@127.0.0.1 "$@"; }
probe(){ guest "python3 /usr/local/bin/radio-recording-private-probe.py $*"; }
read_guest(){
 # Only callers below with explicitly read-only commands use this helper.
 # A guest assertion exits1 and is never retried; require SSH255 plus transport diagnostics.
 local attempt output status errors
 errors=radio-045-fixture/read-transport.stderr
 for attempt in 1 2 3;do
  if output=$(guest "$@" 2>"$errors");then
   cat "$errors" >&2
   printf '%s\n' "$output"
   return 0
  else status=$?;fi
  cat "$errors" >&2
  printf '%s\n' "$output" >&2
  if [ "$status" != 255 ] || ! grep -Eq 'kex_exchange_identification:|Connection reset by peer|Connection closed by|Connection timed out|Connection refused|Broken pipe' "$errors";then return "$status";fi
  echo "RADIO READ-ONLY SSH TRANSPORT255 RETRY $attempt: $*" >&2
  sleep 2
 done
 return 255
}
read_probe(){ read_guest "python3 /usr/local/bin/radio-recording-private-probe.py $*"; }
expected=$(sha256sum radio-045-fixture/inputs/declaration.conf | cut -d' ' -f1)
ready(){
 for attempt in {1..180};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 echo "RADIO READINESS FAILURE expected=$expected";return 1
}
boot_index=0
boot(){
 boot_index=$((boot_index+1))
 confos_boot_reserved images/radio-045.qcow2 22458 3072 "radio-045-fixture/boot-$boot_index.serial"
 echo "$confos_vm_pid" >radio-045-fixture/guest.pid
}
cut(){
 kill -KILL "$confos_vm_pid"
 wait "$confos_vm_pid" 2>/dev/null || true
 unset confos_vm_pid
 rm -f radio-045-fixture/guest.pid
}
boot;ready
stable=$(read_probe stable-hash)
[[ $stable =~ ^[0-9a-f]{64}$ ]]
probe authority
guest 'python3 /usr/local/bin/radio-mutation-probe.py'
guest 'sudo -n python3 /usr/local/bin/radio-mutation-probe.py'
prior=absent
for stage in add change remove;do
 case "$stage" in add) next=192.0.2.2;;change) next=192.0.2.3;;remove) next=absent;;esac
 desired=
 # Read the actual recorder stream; issue SIGKILL as soon as RECORDED arrives.
 while IFS= read -r line;do
  printf '%s\n' "$line"
  if [[ $line =~ ^RECORDED\ ([0-9a-f]{64})\;\ run\ confos\ apply$ ]];then
   desired=${BASH_REMATCH[1]}
   cut
   echo "RADIO IMMEDIATE RECORDED CUT $stage $desired"
   break
  fi
 done < <(probe request "$stage")
 test -n "$desired"
 boot;ready
 observed=$(read_guest 'sha256sum /state/declaration.conf')
 test "${observed%% *}" = "$desired"
 read_probe verify "$stage" "$prior" "$stable"
 probe repeat "$stage" "$prior"
 expected=$desired
 guest 'sudo -n confos apply' || true
 ready
 cut
 echo "RADIO IMMEDIATE APPLIED CUT $stage $expected"
 boot;ready
 read_probe verify "$stage" "$next" "$stable"
 probe repeat "$stage" "$next"
 prior=$next
done
guest 'sudo -n tar -cf - -C /state recorded-inputs' >radio-045-fixture/generated-inputs.tar
echo CANONICAL45 RADIO RECORDING SIX CUTS PASS
