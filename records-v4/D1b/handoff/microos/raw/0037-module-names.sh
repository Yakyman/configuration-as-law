for p in /sys/module/*; do test -d "$p" && printf '%s\n' "${p##*/}"; done
