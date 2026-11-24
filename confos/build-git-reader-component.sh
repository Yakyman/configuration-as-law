#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
version=${1:-$(cat VERSION)}
test -s packages/confos-code-readers_0.30_amd64.deb
sha256sum -c git-source.sha256
test ! -e interpreter-inputs/git/tree
dpkg-source -x interpreter-inputs/git/git_2.47.3-0+deb13u1.dsc interpreter-inputs/git/tree
bash build-git-code.sh
python3 package-git-readers.py "$version" packages/confos-code-readers_0.30_amd64.deb \
    interpreter-inputs/git/tree interpreter-inputs/git/git_2.47.3-0+deb13u1_amd64.deb \
    "packages/confos-code-readers_${version}_amd64.deb"
