#!/bin/bash
# Builder regression, not an acceptance: saved Basic libraries of the office suite.
# usage: test-basic-macros.sh LABEL SOURCE_DIR ran|refused SUITE_RELEASE SSH_PORT
#   SOURCE_DIR     the source of the release under test (build.sh, boot.sh, examples/)
#   ran|refused    what basic-macro-probe.py must observe
#   SUITE_RELEASE  the release of libreoffice-writer that the declaration names
# The log is logs/basic-macros-LABEL.log; its last line is BASIC MACROS PASS or FAIL.
set -euo pipefail
cd "$(dirname "$0")"
label=$1; source_dir=$(realpath "$2"); expect=$3; release=$4; port=$5
mkdir -p logs
exec >"logs/basic-macros-$label.log" 2>&1
work=$PWD/basic-macros-$label
test ! -e "$work"
mkdir -p "$work/inputs"
unit=confos-basic-macros-$label
result=FAIL
cleanup() {
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -rf "$work"
    echo "BASIC MACROS $result ($label, libreoffice-writer $release, expected: $expect)"
}
trap cleanup EXIT
date -u '+%Y-%m-%d %H:%M:%S UTC'
grep -E '^(base|snapshot|account|authorized-key) ' "$source_dir/examples/development.conf" >"$work/inputs/declaration.conf"
printf 'package libreoffice-writer %s\n' "$release" >>"$work/inputs/declaration.conf"
cp basic-macro-probe.py "$work/inputs/basic-macro-probe.py"
printf 'file /usr/local/bin/basic-macro-probe.py 0644 0:0 %s basic-macro-probe.py\n' \
    "$(sha256sum basic-macro-probe.py | cut -d' ' -f1)" >>"$work/inputs/declaration.conf"
cat "$work/inputs/declaration.conf"
"$source_dir/build.sh" "$work/inputs/declaration.conf" "$work/disk.qcow2" >"$work/build.log" 2>&1 || { tail -30 "$work/build.log"; exit 1; }
grep -E 'reader (override|guard)|^BUILT' "$work/build.log" || true
echo "core library in the built root: $(sha256sum "$work/disk.work/root/usr/lib/libreoffice/program/libmergedlo.so" | cut -d' ' -f1)"
systemd-run --user --quiet --unit="$unit" --property=MemoryMax=5G --working-directory="$work" \
    "$source_dir/boot.sh" "$work/disk.qcow2" "$port" 4096 "$work/serial.log"
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
        -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p "$port" user@127.0.0.1 "$@"
}
expected=$(sha256sum "$work/inputs/declaration.conf" | cut -d' ' -f1)
ready=0
for attempt in $(seq 1 150); do
    if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ]; then ready=1; break; fi
    sleep 2
done
test "$ready" = 1
guest "python3 /usr/local/bin/basic-macro-probe.py $expect"
result=PASS
