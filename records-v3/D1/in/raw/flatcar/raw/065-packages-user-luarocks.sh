runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'command -v luarocks >/dev/null 2>&1 || exit 127; luarocks list --porcelain'
