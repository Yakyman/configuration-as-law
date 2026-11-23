runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'command -v go >/dev/null 2>&1 || exit 127; go version -m $(go env GOPATH)/bin/*'
