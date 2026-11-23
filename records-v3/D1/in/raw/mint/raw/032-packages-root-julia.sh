runuser -u root -- env HOME=/root XDG_RUNTIME_DIR=/run/user/0 sh -c 'command -v julia >/dev/null 2>&1 || exit 127; julia --startup-file=no -e '"'"'using Pkg; Pkg.status()'"'"''
