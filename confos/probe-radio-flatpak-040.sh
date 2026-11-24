#!/bin/bash
# Explicit worker gate; reserve one guest, run inside persistent bounded unit.
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.40
exec >logs/radio-flatpak-0.40.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
serial=logs/radio-flatpak-0.40.serial
confos_boot_reserved images/radio-040-flatpak.qcow2 22448 3072 "$serial"
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22448 user@127.0.0.1)
guest() { ssh "${args[@]}" "$@"; }
wanted=$(sha256sum radio-040-flatpak-fixture/declaration.conf | cut -d' ' -f1)
ready() {
 for attempt in {1..150};do
  if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $wanted" ];then return;fi
  sleep 2
 done
 return 1
}
ready
# Positive host radio proof and actual host native controls. These are not
# inferred from missing Flatpak executables or hidden private mount points.
grep -q 'WPA2-CCMP connected; AP traffic verified' "$serial"
grep -q 'AUTHENTICATED BIDIRECTIONAL L2CAP PASS' "$serial"
guest 'python3 /usr/local/bin/radio-mutation-probe.py'
guest 'flatpak run --command=cat io.mpv.Mpv /proc/self/attr/current' | grep -Fx 'confos-flatpak (enforce)'
guest 'flatpak run io.mpv.Mpv --version' | tee logs/radio-flatpak-mpv-0.40.log
grep -q '^mpv ' logs/radio-flatpak-mpv-0.40.log
guest 'flatpak run --command=python3 io.mpv.Mpv /home/user/bin/radio-flatpak-positive.py' | grep -Fx 'RECORDED-RADIO-FLATPAK-PYTHON-PASS'
guest 'flatpak run --command=bash io.mpv.Mpv /home/user/bin/radio-flatpak-entry.sh' | tee logs/radio-flatpak-controls-0.40.log
grep -Fxq 'RECORDED-RADIO-FLATPAK-BASH-PASS' logs/radio-flatpak-controls-0.40.log
grep -q '^FLATPAK RADIO CONTROL PROBE PASS blocked-sockets=2 ' logs/radio-flatpak-controls-0.40.log
before=$(grep -c 'RADIO VERIFIED ' "$serial")
# Supervisor rechecks exact saved bonds and Wi-Fi association every10 seconds.
for attempt in {1..30};do
 if [ "$(grep -c 'RADIO VERIFIED ' "$serial")" -gt "$before" ];then break;fi
 sleep 1
done
test "$(grep -c 'RADIO VERIFIED ' "$serial")" -gt "$before"
ready
echo 'CANONICAL40 FLATPAK RADIO CONTROLS PASS'
