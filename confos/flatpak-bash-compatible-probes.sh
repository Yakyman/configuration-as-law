#!/bin/bash
# Run inside a prepared guest after recording the prototype binary and script.
# This never changes the app bundle or chooses an unrecorded interpreter.
set -euo pipefail
binary=${BINARY:-/usr/bin/bash}
recorded=/home/user/bin/recorded-flatpak-bash.sh
failures=0
check() {
    local expected=$1 output status
    shift
    set +e
    output=$(timeout -k 2 20 flatpak run --command="$binary" io.mpv.Mpv "$@" 2>&1)
    status=$?
    set -e
    printf 'COMMAND '; printf '%q ' "$@"; printf '\n%s\nEXIT %s\n' "$output" "$status"
    if [ "$expected" = refuse ]; then
        if [[ $output != *'Permission denied'* || $output == *UNRECORDED-BASH-RAN* ]]; then failures=$((failures+1)); fi
    elif [ "$status" != 0 ] || [[ $output != *RECORDED-BASH-RAN* ]]; then
        failures=$((failures+1))
    fi
}
printf 'echo UNRECORDED-BASH-RAN\n' >/home/user/flatpak-bash-material.sh
for directory in /home/user /tmp /dev/shm; do
    file="$directory/flatpak-bash-material.sh"
    # /tmp and /dev/shm are private per app invocation. Create and consume within
    # the same sandbox; home already contains host material in a read-only view.
    check refuse -c 'if [[ $1 != /home/user/* ]]; then printf "echo UNRECORDED-BASH-RAN\n" >"$1"; fi; exec "$0" "$1"' "$binary" "$file"
    check refuse -c 'if [[ $1 != /home/user/* ]]; then printf "echo UNRECORDED-BASH-RAN\n" >"$1"; fi; . "$1"' "$binary" "$file"
    check refuse -c 'if [[ $1 != /home/user/* ]]; then printf "echo UNRECORDED-BASH-RAN\n" >"$1"; fi; exec "$0" <"$1"' "$binary" "$file"
done
check recorded "$recorded"
check recorded -c '. "$1"' prototype "$recorded"
check recorded -c 'printf "RECORDED-BASH-RAN\n"'
check recorded -c 'printf "echo RECORDED-BASH-RAN\n" | "$0"' "$binary"
check recorded -c 'printf "RECORDED-BASH-RAN\n" >/tmp/data; read -r value </tmp/data; printf "%s\n" "$value"'
if [ "$binary" = /usr/bin/bash ]; then
    check recorded -c 'BASH_ENV="$1" "$0" -c :' "$binary" "$recorded"
    check refuse -c 'BASH_ENV=/home/user/flatpak-bash-material.sh "$0" -c :' "$binary"
    # Config patch specifically affects argv[0] leading "-", not merely --login.
    check recorded -c 'export HOME=/home/user/bin/login; exec -a -bash /usr/bin/bash -c :'
    check refuse -c 'mkdir -p /tmp/login; printf "echo UNRECORDED-BASH-RAN\n" >/tmp/login/.bash_profile; export HOME=/tmp/login; exec -a -bash /usr/bin/bash -c :'
fi
echo "FLATPAK BASH FAILURES $failures"
test "$failures" = 0
