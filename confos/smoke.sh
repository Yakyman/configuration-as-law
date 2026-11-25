#!/bin/bash
# Builder regression only. Run on the worker, under a user service for persistence.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs images
stamp=$(date -u +%Y%m%dT%H%M%SZ)
exec > >(tee "logs/smoke-$stamp.log" smoke.log) 2>&1
image=images/smoke.qcow2
unit=confos-smoke-vm
port=22402
cleanup() {
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -f "$image"
    rm -rf images/smoke.work
}
trap cleanup EXIT
declaration=${DECLARATION:-examples/development.conf}
test -f "$declaration"
test ! -e "$image"
./build.sh "$declaration" "$image"
systemd-run --user --unit="$unit" --property=MemoryMax=3G --working-directory="$PWD" \
    ./boot.sh "$image" "$port" 2048 "logs/smoke-$stamp.serial"
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
        -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p "$port" user@127.0.0.1 "$@"
}
wait_status() {
    local expected=$1
    for attempt in $(seq 1 90); do
        if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ]; then return 0; fi
        sleep 2
    done
    echo 'FAIL: readiness timeout'
    return 1
}
initial=$(sha256sum "$declaration" | cut -d' ' -f1)
wait_status "$initial"
echo 'PASS clean build, disk boot and SSH'
guest 'dpkg-query -W confos-runtime; test "$(stat -c %a /usr/lib/confos/assemble.py)" = 644; test "$(stat -c %a /usr/lib/confos/components/20261123T000000Z.txt)" = 644; version=$(cat /usr/lib/confos/VERSION); test -r "/system/base-packages/confos-runtime_${version}_all.deb"'
echo 'PASS genuine runtime package and fixed installed source modes'
guest 'dpkg-query -W confos-boot; version=$(cat /usr/lib/confos/VERSION); test -r "/system/base-packages/confos-boot_${version}_amd64.deb"; test -r /usr/lib/confos/boot/BOOTX64.EFI'
echo 'PASS named boot package and retained apply archive'
guest 'set -eu; dpkg-query -W confos-initramfs; version=$(cat /usr/lib/confos/VERSION); for stamp in 20260801T000000Z 20261001T000000Z 20261123T000000Z; do test -r "/system/base-packages/confos-initramfs_${version}+${stamp}_amd64.deb"; done; generation=$(cat /etc/confos/identity); a=$(sha256sum /usr/lib/confos/initramfs/initramfs); b=$(sha256sum /system/generations/$generation/initramfs); test "${a%% *}" = "${b%% *}"; test "$(cat /usr/lib/confos/initramfs/kernel-release)" = "$(uname -r)"'
echo 'PASS packaged initramfs bytes, running kernel and all retained update archives'
guest 'sudo -n id'
guest 'test "$(stat -c %u:%g:%a /usr/sbin/unix_chkpwd)" = 0:42:2755'
echo 'PASS native package numeric ownership and mode'
guest 'sudo -n -i id; test "$(hostname)" = confos-test; sudo -n mkdir -p /state/files; printf regression | sudo -n tee /state/files/sudo-check.new; sudo -n mv /state/files/sudo-check.new /state/files/sudo-check; sudo -n rm /state/files/sudo-check'
echo 'PASS sudo and sudo login shell with cron and declared hostname'
guest 'cat /proc/self/attr/current; sudo -n cat /proc/self/attr/current'
guest '/home/user/bin/recorded.sh ordinary-work'
if guest 'mv /home/user/bin /home/user/moved-bin'; then
    echo 'FAIL declared directory moved'; exit 1
fi
if guest 'printf "touch /home/user/startup-marker\n" >> /home/user/.bashrc'; then
    echo 'FAIL unrecorded automatic startup changed'; exit 1
fi
guest '/home/user/bin/recorded.sh after-refusal; test ! -e /home/user/startup-marker'
echo 'PASS declared path and automatic startup protected'
guest 'confos services; sudo -n confos rules; cat /proc/sys/kernel/printk'
guest 'sudo -n nft list ruleset'
guest 'test "$(sudo -n nft list ruleset | sed -n "/tcp dport 32123/p" | xargs)" = "tcp dport 32123 accept"; test "$(stat -c %a /run)" = 755; test "$LC_ALL" = C.UTF-8; cat <(printf "process-substitution-ok\n")'
echo 'PASS exact rule text, runtime mode, UTF-8 session and process substitution'
guest 'sudo -n sh -c "printf '\''package tree 2.2.1-1\n'\'' >> /state/declaration.conf"'
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || result=$?
wait_status "$expected"
guest '/usr/bin/tree --version'
echo 'PASS package line added and applied'
if guest 'cp /usr/bin/busybox /home/user/busybox; chmod +x /home/user/busybox; /home/user/busybox true'; then
    echo 'FAIL saved native executable started'
    exit 1
fi
echo 'PASS undeclared native executable refused'
guest 'printf "echo UNRECORDED-SHELL\\n" >/home/user/unrecorded.sh; printf "print(12345)\\n" >/home/user/unrecorded.py; printf "print 67890;\\n" >/home/user/unrecorded.pl'
for command in 'bash /home/user/unrecorded.sh' 'sh /home/user/unrecorded.sh' 'python3 /home/user/unrecorded.py' 'perl /home/user/unrecorded.pl'; do
    if guest "$command"; then
        echo "FAIL saved interpreter input: $command"; exit 1
    fi
done
echo 'PASS undeclared Bash sh Python Perl inputs refused'
for mutation in 'sudo -n hostname unrecorded' 'sudo -n mount -o remount,bind,exec /home' 'sudo -n /usr/sbin/nft flush ruleset' 'sudo -n /usr/local/bin/nft flush ruleset'; do
    if guest "$mutation"; then
        echo "FAIL privileged mutation: $mutation"
        exit 1
    fi
done
echo 'PASS privileged hostname, mount and firewall changes refused'
if [ "${EXTENDED:-0}" = 1 ]; then
    guest 'sudo -n sed -i "s/^package tree 2.2.1-1$/package ed 1.21.1-1/" /state/declaration.conf'
    expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
    guest 'sudo -n confos apply' || true
    wait_status "$expected"
    guest 'test ! -e /usr/bin/tree && /usr/bin/ed --version'
    echo 'PASS package line changed (tree to ed)'
    guest 'sudo -n sed -i "/^package ed /d" /state/declaration.conf'
    expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
    guest 'sudo -n confos apply' || true
    wait_status "$expected"
    guest 'test ! -e /usr/bin/ed && test ! -e /usr/bin/tree && test ! -e /state/staging'
    guest 'ls /system/generations'
    echo 'PASS package line removed and staging absent'
    guest 'sudo -n sed -i "/^service sleeper /d; /^rule development /d" /state/declaration.conf'
    expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
    guest 'sudo -n confos apply' || true
    wait_status "$expected"
    guest 'test -z "$(confos services)" && ! sudo -n confos rules | grep -q 32123'
    guest 'python3 -c '\''from pathlib import Path; assert not any(p.read_bytes().split(bytes([0]))[:2] == [b"/usr/bin/sleep", b"30000"] for p in Path("/proc").glob("[0-9]*/cmdline"))'\'''
    echo 'PASS service process and effective rule removed'
fi
echo 'SMOKE PASS'
