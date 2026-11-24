#!/usr/bin/env bash
# Shared runner; source from the six entry scripts. No action runs on sourcing.
# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html
# https://www.sudo.ws/docs/man/sudo.man/
set -euo pipefail
export LC_ALL=C TZ=UTC

root() {
    if [[ -n ${CAL_SUDO_PASSWORD:-} ]]; then
        # A here-string is authentication input, not the command's data input.
        command sudo -S -p '' -- "$@" <<< "$CAL_SUDO_PASSWORD"
    else
        command sudo -n -- "$@"
    fi
}

install_root_file() {
    root install -D -m "$3" -- "$1" "$2"
}

actions_main() {
    local name limit start finish rc failed=0 script
    script=$(readlink -f "$0")
    if [[ ${1:-} == --list ]]; then actions; return; fi
    [[ $(id -un) == user && $(id -u) != 0 ]] || {
        printf '%s\n' 'Run inside the disposable guest as user.' >&2; return 64;
    }
    if [[ ${1:-} == --action ]]; then
        [[ $# == 2 && ${CAL_ACTION_DISPATCH:-} == 1 ]] || return 64
        while read -r name limit; do
            if [[ $name == "$2" ]]; then
                # Called as a simple command: errexit is not disabled by an if test.
                "$name"
                return
            fi
        done < <(actions)
        return 64
    fi
    [[ $# == 0 ]] || return 64
    command -v timeout >/dev/null
    # Refuse a second attempt on the same guest; retain earlier evidence.
    (set -o noclobber; : > "$HOME/actions-status.tsv") || return 73
    mkdir -p "$HOME/actions-logs"
    while read -r name limit; do
        start=$(date +%s)
        set +e
        CAL_ACTION_DISPATCH=1 timeout --signal=TERM --kill-after=30s "${limit}s" \
            bash "$script" --action "$name" \
            > "$HOME/actions-logs/$name.log" 2> "$HOME/actions-logs/$name.stderr" < /dev/null
        rc=$?
        set -e
        finish=$(date +%s)
        printf '%s\t%d\t%d\n' "$name" "$rc" "$((finish-start))" >> "$HOME/actions-status.tsv"
        if (( rc != 0 )); then failed=1; fi
    done < <(actions)
    return "$failed"
}
