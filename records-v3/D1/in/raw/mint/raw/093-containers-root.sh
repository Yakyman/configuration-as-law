runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'podman ps -a --no-trunc'
