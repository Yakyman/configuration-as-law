for p in /proc/[0-9]*; do test -d "$p" || continue; printf '%s\t' "${p##*/}"; readlink "$p/exe" || printf 'unknown\n'; done
