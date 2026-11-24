for p in /var/service/* /run/runit/service/* /etc/service/*; do test -e "$p" || continue; printf '%s\t' "$p"; readlink "$p" || :; done
