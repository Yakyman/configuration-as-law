#!/bin/bash
# Builder regression, not an acceptance: the superuser reads which file every process
# executes (a recorded Flatpak application in its sandbox included); `flatpak list` with
# its options; root's container queries in JSON form.
# usage: test-queries-055.sh LABEL readable|unreadable SSH_PORT
#   readable     the repaired release: every check of process-exe-probe.sh holds
#   unreadable   control on a release before the repair: the report is reproduced
# The log is logs/queries-LABEL.log; its last line is PROCESS QUERIES PASS or FAIL.
set -euo pipefail
cd "$(dirname "$0")"
label=$1; expect=$2; port=$3
mkdir -p logs
exec >"logs/queries-$label.log" 2>&1
work=$PWD/queries-$label
test ! -e "$work"
mkdir -p "$work/inputs"
unit=confos-queries-$label
result=FAIL
cleanup() {
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -rf "$work"
    echo "PROCESS QUERIES $result ($label, expected: $expect)"
}
trap cleanup EXIT
date -u '+%Y-%m-%d %H:%M:%S UTC'
decl=$work/inputs/declaration.conf
grep -E '^(base|snapshot|account|authorized-key) ' examples/development.conf >"$decl"
printf 'package flatpak 1.16.6-1~deb13u3\npackage util-linux 2.41.5-0+deb13u1\npackage gpg 2.4.7-21+deb13u1+b5\npackage gpg-agent 2.4.7-21+deb13u1+b5\n' >>"$decl"
printf 'package podman 5.4.2+ds1-2+b2\npackage uidmap 1:4.17.4-2\npackage slirp4netns 1.2.1-1.1\n' >>"$decl"
ln flatpak-inputs/runtime.flatpak flatpak-inputs/mpv.flatpak "$work/inputs/"
printf 'flatpak runtime/org.freedesktop.Platform/x86_64/26.08 df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c %s runtime.flatpak\n' "$(sha256sum flatpak-inputs/runtime.flatpak | cut -d' ' -f1)" >>"$decl"
printf 'flatpak app/io.mpv.Mpv/x86_64/stable 13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc %s mpv.flatpak\n' "$(sha256sum flatpak-inputs/mpv.flatpak | cut -d' ' -f1)" >>"$decl"
cp process-exe-probe.sh "$work/inputs/process-exe-probe.sh"
printf 'file /usr/local/bin/process-exe-probe.sh 0755 0:0 %s process-exe-probe.sh\n' \
    "$(sha256sum process-exe-probe.sh | cut -d' ' -f1)" >>"$decl"
cat "$decl"
./build.sh "$decl" "$work/disk.qcow2" >"$work/build.log" 2>&1 || { tail -30 "$work/build.log"; exit 1; }
grep -n 'ptrace' "$work/disk.work/root/etc/confos/session.apparmor" | head -12
systemd-run --user --quiet --unit="$unit" --property=MemoryMax=5G --working-directory="$work" \
    "$PWD/boot.sh" "$work/disk.qcow2" "$port" 4096 "$work/serial.log"
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
        -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p "$port" user@127.0.0.1 "$@"
}
expected=$(sha256sum "$decl" | cut -d' ' -f1)
ready=0
for attempt in $(seq 1 150); do
    if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ]; then ready=1; break; fi
    sleep 2
done
test "$ready" = 1
guest "/usr/local/bin/process-exe-probe.sh $expect"
result=PASS
