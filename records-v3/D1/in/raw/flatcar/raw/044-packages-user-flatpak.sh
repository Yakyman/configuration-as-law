runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'command -v flatpak >/dev/null 2>&1 || exit 127; flatpak list --columns=ref,version,origin,installation --all'
