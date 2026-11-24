#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
version=${1:-$(cat VERSION)}
test -s packages/confos-code-readers_0.31_amd64.deb
sha256sum -c nvim-source.sha256
test ! -e interpreter-inputs/nvim/tree
mkdir interpreter-inputs/nvim/tree
tar -xzf interpreter-inputs/nvim/neovim-v0.10.4.tar.gz --strip-components=1 -C interpreter-inputs/nvim/tree
bash build-nvim-code.sh
python3 package-nvim-readers.py "$version" packages/confos-code-readers_0.31_amd64.deb \
    interpreter-inputs/nvim/tree appimage-inputs/nvim.appimage \
    "packages/confos-code-readers_${version}_amd64.deb"
