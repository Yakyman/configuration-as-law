#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/flatpak-readers-0.39.log 2>&1
source slots.sh
private=.
test "$(cat VERSION)" = 0.39
image="$private/images/flatpak-readers-039.qcow2"
cleanup() { confos_stop_reserved; rm -f "$image"; }
trap cleanup EXIT
expected=$(sha256sum "$private/examples/flatpak-readers-039.conf" | cut -d' ' -f1)
guest() {
 ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22450 user@127.0.0.1 "$@"
}
ready() {
 for attempt in $(seq 1 120); do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ]; then return; fi
  sleep 2
 done
 return 1
}
confos_reserve_guest
confos_boot_reserved "$image" 22450 3072 logs/flatpak-readers-integration.serial
ready
for cycle in 1 2; do
 echo "INTEGRATION BOOT CYCLE $cycle"
 guest 'flatpak run --command=cat io.mpv.Mpv /proc/self/attr/current'
 guest 'BINARY=/usr/bin/bash bash -s' <flatpak-bash-compatible-probes.sh
 guest 'BINARY=/usr/bin/sh bash -s' <flatpak-bash-compatible-probes.sh
 guest 'bash -s' <flatpak-python-shared-probes.sh
 guest 'bash -s' <flatpak-readers-integration-probes.sh
 if [ "$cycle" = 1 ]; then
  confos_stop_reserved
  confos_boot_reserved "$image" 22450 3072 logs/flatpak-readers-integration-restart.serial
  ready
 fi
done
# Remove app line first: runtime and its guarded reader remain while named.
guest "sudo -n sed -i '\\|^flatpak app/io.mpv.Mpv/|d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/confos/flatpak/app/io.mpv.Mpv && test -f /usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08/active/files/bin/bash && echo APP_REMOVED_RUNTIME_RETAINED'
# Last runtime line removed: original and replacement contributions disappear.
guest "sudo -n sed -i '\\|^flatpak runtime/org.freedesktop.Platform/|d' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready
guest 'test ! -e /usr/lib/confos/flatpak/runtime/org.freedesktop.Platform && test ! -e /usr/lib/confos/flatpak/repo/objects/08/8ac0e78b5c58326c0b5f6f04ce48110e888e42c41f2ba6cf31f1589fdeb21b.file && echo LAST_RUNTIME_REMOVAL_PASS'
echo 'CANONICAL39 FLATPAK READER INTEGRATION TEST PASS'

