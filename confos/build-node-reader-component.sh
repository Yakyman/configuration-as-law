#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
version=${1:-$(cat VERSION)}
test -s packages/confos-code-readers_0.29_amd64.deb
sha256sum -c node-source.sha256
test ! -e interpreter-inputs/node/tree
dpkg-source -x interpreter-inputs/node/nodejs_20.19.2+dfsg-1+deb13u3.dsc interpreter-inputs/node/tree
python3 prepare-node-build-deps.py
python3 patch-node-code.py interpreter-inputs/node/tree
bash build-node-code.sh
python3 package-node-readers.py "$version" packages/confos-code-readers_0.29_amd64.deb \
    interpreter-inputs/node/tree "packages/confos-code-readers_${version}_amd64.deb"
