runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'systemctl --user --no-pager --no-legend list-unit-files --type=service,timer'
