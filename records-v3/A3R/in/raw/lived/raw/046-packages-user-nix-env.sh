runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'command -v nix-env >/dev/null 2>&1 || exit 127; nix-env -q --out-path'
