runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'systemctl --user --no-pager --no-legend list-unit-files --type=service,timer'
