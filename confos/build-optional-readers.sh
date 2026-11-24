#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
version=${1:-$(cat VERSION)}
test -s packages/confos-code-readers_0.28_amd64.deb
sha256sum -c tools-source.sha256
python3 prepare-tools-build-deps.py
bash build-tools-code.sh
bash build-make-code.sh
python3 package-optional-readers.py "$version" packages/confos-code-readers_0.28_amd64.deb \
    interpreter-inputs/tools/trees "packages/confos-code-readers_${version}_amd64.deb"
