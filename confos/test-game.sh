#!/bin/bash
# Native launcher installation/update through person-authored package inputs.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/test-game.log 2>&1
image=images/game.qcow2
unit=confos-game-vm
cleanup() {
    result=$?
    if [ "$result" -ne 0 ] && [ "${KEEP_FAILED:-0}" = 1 ]; then
        echo 'FAILED game VM/worktree retained for immediate diagnosis'; return
    fi
    systemctl --user stop "$unit" 2>/dev/null || true
    rm -f "$image"
    rm -rf images/game.work game-test-inputs
}
trap cleanup EXIT
mkdir -p game-test-inputs
cp examples/development.conf game-test-inputs/declaration.conf
cp examples/recorded.sh game-test-inputs/recorded.sh
cat game-packages.conf >>game-test-inputs/declaration.conf
for release in 26.5.0 26.6.0; do
    ln -s "../game-inputs/linuxgsm-wet-$release.tar" "game-test-inputs/linuxgsm-wet-$release.tar"
done
first=$(sha256sum game-inputs/linuxgsm-wet-26.5.0.tar | cut -d' ' -f1)
second=$(sha256sum game-inputs/linuxgsm-wet-26.6.0.tar | cut -d' ' -f1)
printf 'linuxgsm user /home/user/game 26.5.0 %s linuxgsm-wet-26.5.0.tar\n' "$first" >>game-test-inputs/declaration.conf
./build.sh game-test-inputs/declaration.conf "$image"
systemd-run --user --unit="$unit" --property=MemoryMax=4G --working-directory="$PWD" ./boot.sh "$image" 22421 3072 logs/game.serial
guest() {
    ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22421 user@127.0.0.1 "$@"
}
wait_ready() {
    for attempt in $(seq 1 90); do
        if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $1" ]; then return; fi
        sleep 2
    done
    return 1
}
run_game() {
    guest 'cd /home/user/game; stat -c "%u:%g:%a %n" wetserver serverfiles/etded.x86; bash wetserver start; sleep 3; pgrep -a etded; bash wetserver stop'
}
wait_ready "$(sha256sum game-test-inputs/declaration.conf | cut -d' ' -f1)"
run_game
if guest 'touch /home/user/game/unrecorded-code'; then echo 'FAIL game code workspace writable'; exit 1; fi
echo 'PASS native game installation, ordinary-account start/stop and immutable code'
cat game-inputs/linuxgsm-wet-26.6.0.tar | guest 'sudo -n tee /state/linuxgsm-wet-26.6.0.tar >/dev/null'
guest "sudo -n sed -i 's/^linuxgsm .*/linuxgsm user \/home\/user\/game 26.6.0 $second linuxgsm-wet-26.6.0.tar/' /state/declaration.conf"
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
wait_ready "$expected"
run_game
echo 'PASS native launcher self-update in application and updated game start/stop'
guest 'cd /home/user/game; bash wetserver start; pgrep -a etded; sudo -n sed -i "/^linuxgsm /d" /state/declaration.conf'
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
wait_ready "$expected"
guest 'test ! -e /home/user/game/wetserver; test ! -e /home/user/game/serverfiles/etded.x86; test ! -e /run/confos-games; ! pgrep etded'
echo 'GAME REGRESSION PASS; direct mutable self-update and wider P4 are not acceptance passes'
