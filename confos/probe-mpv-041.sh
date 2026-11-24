#!/bin/bash
# Canonical future41 guest checks; caller owns a bounded persistent worker unit.
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.41
exec >logs/mpv-0.41.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
disk=images/mpv-041.qcow2
expected=$(sha256sum mpv-041-fixture/declaration.conf | cut -d' ' -f1)
guest() { ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22450 user@127.0.0.1 "$@"; }
ready() {
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then return;fi
  sleep 2
 done
 echo "READINESS FAILURE $expected";return 1
}
for cycle in 1 2;do
 confos_boot_reserved "$disk" 22450 3072 "logs/mpv-041-$cycle.serial"
 ready
 guest 'sudo -n python3 -' <<'PY'
import hashlib,json,os
from pathlib import Path
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
path=Path('/run/confos-radio-ready.json')
before=path.read_bytes();json.loads(before)
try:
 fd=os.open(path,os.O_WRONLY)
except PermissionError as error:
 assert error.errno==13
else:
 os.close(fd);raise AssertionError('root can write radio readiness')
assert path.read_bytes()==before
print('RADIO READY ROOT READ ALLOWED WRITE DENIED',hashlib.sha256(before).hexdigest())
PY
 guest 'flatpak run --command=python3 io.mpv.Mpv /home/user/bin/mpv41-app-probe.py'
 guest 'python3 -' <mpv41-original-alias-probe.py
 if [ "$cycle" = 1 ];then
  guest 'BINARY=/usr/bin/bash bash -s' <flatpak-bash-compatible-probes.sh
  guest 'BINARY=/usr/bin/sh bash -s' <flatpak-bash-compatible-probes.sh
  guest 'bash -s' <flatpak-python-shared-probes.sh
  kill -KILL "$confos_vm_pid";wait "$confos_vm_pid" 2>/dev/null || true;unset confos_vm_pid
 fi
 echo "MPV41 BOOT INPUTS ALIASES PASS $cycle"
done
# Removing the app rebuilds the native store without all three app contributions.
guest 'nohup flatpak run io.mpv.Mpv --no-config --vo=null --ao=null --idle=yes --load-scripts=no </dev/null >/home/user/mpv41-running.log 2>&1 &'
guest 'python3 -' <<'PY'
from pathlib import Path
import time
for attempt in range(50):
 found=[]
 for path in Path('/proc').glob('[0-9]*/cmdline'):
  try: args=path.read_bytes().split(b'\0')
  except OSError: continue
  if args[0] in (b'mpv',b'/app/bin/mpv') and b'--idle=yes' in args: found.append(str(path))
 if found: break
 time.sleep(.1)
assert found,'live native mpv removal subject missing'
print('MPV41 LIVE REMOVAL SUBJECT',found)
PY
guest "sudo -n sed -i '\\|^flatpak app/io.mpv.Mpv/|d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/confos/flatpak/app/io.mpv.Mpv && test -f /usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08/active/files/bin/bash'
guest 'python3 -' <<'PY'
import json
from pathlib import Path
items=json.loads(Path('/usr/lib/confos/flatpak-reader-overrides/manifest.json').read_text())
for item in items:
 if item['ref'].startswith('app/io.mpv.Mpv/'):
  for relative in item['objects']: assert not (Path('/usr/lib/confos/flatpak')/relative).exists(),relative
for path in Path('/proc').glob('[0-9]*/cmdline'):
 try: args=path.read_bytes().split(b'\0')
 except OSError: continue
 assert args[0] not in (b'mpv',b'/app/bin/mpv'),path
print('MPV41 APP REMOVAL ORIGINAL AND REPLACEMENT PASS')
PY
guest "sudo -n sed -i '\\|^flatpak runtime/org.freedesktop.Platform/|d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/confos/flatpak/runtime/org.freedesktop.Platform && echo MPV41_LAST_RUNTIME_REMOVAL_PASS'
echo 'CANONICAL41 MPV LUA JS AND INHERITED READERS PASS'
