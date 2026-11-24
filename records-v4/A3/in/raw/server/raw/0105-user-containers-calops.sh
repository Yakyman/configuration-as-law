command -v runuser >/dev/null 2>&1 || exit 127; runuser -u calops -- env HOME=/home/calops XDG_RUNTIME_DIR=/run/user/1001 sh -c 'podman ps -a --no-trunc --format json'
