for p in /sys/bus/*/drivers/*; do test -d "$p" && printf '%s\n' "$p"; done
