command -v runuser >/dev/null 2>&1 || exit 127; runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'systemctl --user cat --no-pager systemd-nspawn@.service'
