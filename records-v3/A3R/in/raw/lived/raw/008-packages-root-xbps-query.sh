runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'command -v xbps-query >/dev/null 2>&1 || exit 127; xbps-query -l'
