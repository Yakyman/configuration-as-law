#!/bin/bash
# Builder regression for whole-system updates, not acceptance.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs images
exec >logs/test-updates.log 2>&1
unit=confos-updates-vm
image=images/updates.qcow2
cleanup() {
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -f "$image" examples/updates.conf
    rm -rf images/updates.work
}
trap cleanup EXIT
sed 's/^snapshot .*/snapshot 20260801T000000Z/' examples/development.conf >examples/updates.conf
# From 0.52: a package whose guarded reader was built from the release of the last
# archive state only (curl) goes through all three states with its own releases.
printf 'package curl 8.14.1-2+deb13u4\n' >>examples/updates.conf
check_curl() {
    guest "set -eu; test \"\$(dpkg-query -W -f='\${Version}' curl)\" = '$1'; curl --version | head -1; rm -f /tmp/inrelease; curl -fsSL -w 'HTTP %{http_code} after %{num_redirects} redirects\n' -o /tmp/inrelease http://snapshot.debian.org/archive/debian/20261123T000000Z/dists/trixie/InRelease; grep -m1 '^Origin: Debian' /tmp/inrelease"
    guest "printf 'output = /tmp/mark-curlrc\n' >/home/user/.curlrc; curl -fsSL http://snapshot.debian.org/archive/debian/20261123T000000Z/dists/trixie/InRelease >/dev/null 2>&1 || true; test ! -e /tmp/mark-curlrc; rm -f /home/user/.curlrc /tmp/inrelease"
    echo "PASS curl $1 runs and does not obey a saved configuration file"
}
./build.sh examples/updates.conf "$image"
systemd-run --user --unit="$unit" --property=MemoryMax=4G --working-directory="$PWD" ./boot.sh "$image" 22405 3072 logs/updates.serial
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22405 user@127.0.0.1 "$@"
}
wait_ready() {
    for attempt in $(seq 1 90); do
        if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $1" ]; then return; fi
        sleep 2
    done
    echo 'FAIL readiness timeout'; return 1
}
wait_ready "$(sha256sum examples/updates.conf | cut -d' ' -f1)"
check() {
    guest "uname -r; dpkg-query -W linux-image-amd64 libc6; test \"\$(uname -r)\" = '$1'; test \"\$(dpkg-query -W -f='\${Version}' libc6)\" = '$2'; sudo -n id; /home/user/bin/recorded.sh update"
    guest 'set -eu; generation=$(cat /etc/confos/identity); a=$(sha256sum /usr/lib/confos/initramfs/initramfs); b=$(sha256sum /system/generations/$generation/initramfs); test "${a%% *}" = "${b%% *}"; test "$(cat /usr/lib/confos/initramfs/kernel-release)" = "$(uname -r)"; dpkg-query -W confos-initramfs; sha256sum /system/generations/$generation/initramfs'
}
check 6.12.94+deb13-amd64 2.41-12+deb13u3
check_curl 8.14.1-2+deb13u4
echo 'PASS T0 clean installation and running kernel'
for stamp in 20261001T000000Z 20261123T000000Z; do
    if [ "$stamp" = 20261001T000000Z ]; then curl_release=8.14.1-2+deb13u5; else curl_release=8.14.1-2+deb13u7; fi
    guest "sudo -n sed -i -e 's/^snapshot .*/snapshot $stamp/' -e 's/^package curl .*/package curl $curl_release/' /state/declaration.conf"
    expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
    guest 'sudo -n confos apply' || true
    wait_ready "$expected"
    if [ "$stamp" = 20261001T000000Z ]; then
        check 6.12.107+deb13-amd64 2.41-12+deb13u4
    else
        check 6.12.118+deb13-amd64 2.41-12+deb13u5
    fi
    check_curl "$curl_release"
    guest 'test ! -e /state/staging; ls /system/generations; cat /system/boot.cfg'
    echo "PASS update $stamp and running kernel"
done
echo 'UPDATES PASS'
