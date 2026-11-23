runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'command -v pip >/dev/null 2>&1 || exit 127; pip list --format=json'
