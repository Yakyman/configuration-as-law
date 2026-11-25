#!/bin/bash
# Builder regression, not an acceptance: the sequence of declarations of the plan's game case
# (the test declaration; then the prerequisite packages and the launcher line 26.5.0, applied;
# then the line changed to 26.6.0, applied; then the person's own launcher), on an overlay of
# a clean installation, with the free space printed before and after every application and
# the lowest free space seen during each.
#
# usage: test-game-sequence.sh LABEL CLEAN.qcow2 LOGIN_KEY TEST_DECLARATION_DIR SOURCE_DIR SSH_PORT PACKAGE_LINES GAME_INPUTS
#   CLEAN.qcow2           a clean installation of the test declaration, account `person`
#   TEST_DECLARATION_DIR  holds declaration.conf (in force on CLEAN) and files/
#   SOURCE_DIR            holds boot.sh of the release under test
#   PACKAGE_LINES         the release's game-packages.conf (or a declaration of the case that
#                         has these lines); the package lines that the test declaration lacks
#                         are appended in their order, as the case does
#   GAME_INPUTS           holds linuxgsm-wet-26.5.0.tar and linuxgsm-wet-26.6.0.tar
# The log is logs/game-sequence-LABEL.log; its last line is GAME SEQUENCE PASS or FAIL.
set -euo pipefail
cd "$(dirname "$0")"
label=$1; clean=$(realpath "$2"); key=$(realpath "$3"); dtest=$(realpath "$4"); source_dir=$(realpath "$5"); port=$6
added=$(realpath "$7"); inputs=$(realpath "$8")
mkdir -p logs
exec >"logs/game-sequence-$label.log" 2>&1
work=$PWD/game-sequence-$label
test ! -e "$work"
mkdir "$work"
unit=confos-game-sequence-$label
result=FAIL
cleanup() {
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -rf "$work"
    echo "GAME SEQUENCE $result ($label)"
}
trap cleanup EXIT
date -u '+%Y-%m-%d %H:%M:%S UTC'
qemu-img info "$clean" | grep -E 'virtual size|disk size'
qemu-img create -q -f qcow2 -F qcow2 -b "$clean" "$work/disk.qcow2"
systemd-run --user --quiet --unit="$unit" --property=MemoryMax=6G --working-directory="$work" \
    "$source_dir/boot.sh" "$work/disk.qcow2" "$port" 4096 "$work/serial.log"
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
        -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -o IdentitiesOnly=yes \
        -i "$key" -p "$port" person@127.0.0.1 "$@"
}
wait_applied() {
    for attempt in $(seq 1 300); do
        if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $1" ]; then return 0; fi
        sleep 2
    done
    return 1
}
space() {
    echo "--- space: $1"
    guest 'df -m --output=target,size,used,avail /state /system | sed "s/^/    /"; sudo -n du -sm /state/files /state/staging /system/generations /system/base-packages /home /var 2>/dev/null | sed "s/^/    /"'
}
# Lowest free space of the data and system partitions while an application runs, with what held it.
watch_space() {
    local low_state=999999 low_system=999999 line
    while [ ! -e "$work/stop-watch" ]; do
        line=$(guest 'df -m --output=avail /state /system | tail -n +2 | tr -s " \n" " "' 2>/dev/null || true)
        set -- $line
        if [ "$#" = 2 ]; then
            if [ "$1" -lt "$low_state" ]; then
                low_state=$1
                guest 'sudo -n du -sm /state/files /state/staging/* 2>/dev/null | tr "\n" ";"' >"$work/low-state.txt" 2>/dev/null || true
            fi
            if [ "$2" -lt "$low_system" ]; then low_system=$2; fi
        fi
        sleep 3
    done
    echo "    lowest free space seen during the application: /state $low_state MiB, /system $low_system MiB"
    echo "    /state at that moment (MiB): $(cat "$work/low-state.txt" 2>/dev/null)"
}
apply_and_wait() {
    local expected
    expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
    space "before the application of $1"
    rm -f "$work/stop-watch"
    watch_space &
    local watcher=$!
    local status=0
    guest 'sudo -n confos apply' >"$work/apply.out" 2>"$work/apply.err" || status=$?
    echo "    confos apply ended with status $status (255: the connection closed at the restart)"
    grep -E 'No space left|Error|Traceback|REBOOTING' "$work/apply.out" "$work/apply.err" | tail -5 | sed 's/^/    /' || true
    local applied=0
    if grep -q '^REBOOTING' "$work/apply.out" && wait_applied "$expected"; then applied=1; fi
    touch "$work/stop-watch"
    wait "$watcher" || true
    if [ "$applied" != 1 ]; then
        echo "    NOT APPLIED: $1; status now: $(guest 'confos status' 2>&1 || true)"
        space "after the failed application of $1"
        return 1
    fi
    echo "    APPLIED $expected"
    space "after the application of $1"
}
put_file() {
    cat "$1" | guest "sudo -n sh -c 'mkdir -p /state/files && cat > /state/files/$2.new && mv /state/files/$2.new /state/files/$2'"
}
run_game() {
    guest 'bash /home/person/game/wetserver start' >"$work/game.out" 2>&1
    sleep 10
    guest 'sudo -n sh -c "ls -l /proc/[0-9]*/exe 2>/dev/null | grep etded"' | sed 's/^/    /'
    guest 'bash /home/person/game/wetserver stop' >>"$work/game.out" 2>&1 || true
    echo "    the game server of launcher $1 was started, seen running and stopped"
}
wait_applied "$(sha256sum "$dtest/declaration.conf" | cut -d' ' -f1)"
echo "clean installation in force: $(guest 'confos status')"
# The first declaration of the case: the package lines of PACKAGE_LINES that the test
# declaration lacks, in their order, then the launcher line.
first_tar=$(sha256sum "$inputs/linuxgsm-wet-26.5.0.tar" | cut -d' ' -f1)
second_tar=$(sha256sum "$inputs/linuxgsm-wet-26.6.0.tar" | cut -d' ' -f1)
cp "$dtest/declaration.conf" "$work/first.conf"
awk 'NR==FNR { if ($1=="package") have[$2]=1; next } NF==3 && $1=="package" && !($2 in have) { print }' \
    "$dtest/declaration.conf" "$added" >>"$work/first.conf"
printf 'linuxgsm person /home/person/game 26.5.0 %s files/linuxgsm-wet-26.5.0.tar\n' "$first_tar" >>"$work/first.conf"
echo "lines added by the case: $(($(wc -l <"$work/first.conf") - $(wc -l <"$dtest/declaration.conf")))"
put_file "$inputs/linuxgsm-wet-26.5.0.tar" linuxgsm-wet-26.5.0.tar
cat "$work/first.conf" | guest 'sudo -n sh -c "cat > /state/declaration.conf.new && mv /state/declaration.conf.new /state/declaration.conf"'
echo "first declaration of the case: $(sha256sum "$work/first.conf" | cut -d' ' -f1)"
apply_and_wait 'the launcher line 26.5.0'
run_game 26.5.0
sed "s|^linuxgsm person /home/person/game 26.5.0 .*|linuxgsm person /home/person/game 26.6.0 $second_tar files/linuxgsm-wet-26.6.0.tar|" "$work/first.conf" >"$work/second.conf"
put_file "$inputs/linuxgsm-wet-26.6.0.tar" linuxgsm-wet-26.6.0.tar
cat "$work/second.conf" | guest 'sudo -n sh -c "cat > /state/declaration.conf.new && mv /state/declaration.conf.new /state/declaration.conf"'
echo "second declaration of the case: $(sha256sum "$work/second.conf" | cut -d' ' -f1)"
apply_and_wait 'the launcher line 26.6.0'
run_game 26.6.0
# The person's own launcher, as the case performs it at its end; its result does not decide.
guest 'mkdir -p ~/game-direct && cd ~/game-direct && curl -fsSLo linuxgsm.sh https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/50dc4e551b661b9d1fa39c291068a16a66056aff/linuxgsm.sh' || echo '    the direct download ended with a failure status'
direct=0
guest 'cd ~/game-direct && bash linuxgsm.sh wetserver' >"$work/direct.out" 2>&1 || direct=$?
echo "    the person's own launcher (saved, not recorded) ended with status $direct"
space 'at the end of the case'
result=PASS
