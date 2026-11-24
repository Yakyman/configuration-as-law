if command -v semanage >/dev/null; then semanage boolean -l -C; else exit 127; fi

