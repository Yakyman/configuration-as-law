runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'command -v go >/dev/null 2>&1 || exit 127; go version -m $(go env GOPATH)/bin/*'
