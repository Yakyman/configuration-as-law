#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/nvim-code-build.log 2>&1
sha256sum -c nvim-source.sha256
if [ "${CONFOS_RESUME:-0}" != 1 ]; then
    python3 patch-nvim-code.py interpreter-inputs/nvim/tree
fi
work="$PWD/interpreter-inputs/nvim/tree"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C CMAKE_BUILD_PARALLEL_LEVEL=2
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-nvim"
export CXXFLAGS="$CFLAGS"
cd "$work"
make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX=/usr
sha256sum build/bin/nvim runtime/lua/vim/loader.lua
ldd build/bin/nvim
echo 'NEOVIM CODE BUILD PASS'
