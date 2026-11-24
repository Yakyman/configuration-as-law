#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/git-code-build.log 2>&1
sha256sum -c git-source.sha256
if [ "${CONFOS_RESUME:-0}" != 1 ]; then
    python3 prepare-git-build-deps.py
    python3 patch-git-code.py interpreter-inputs/git/tree
fi
tree="$PWD/interpreter-inputs/git/tree"
dependency_root="$PWD/interpreter-inputs/git/dependencies/root"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export LD_LIBRARY_PATH="$dependency_root/usr/lib/x86_64-linux-gnu"
cd "$tree"
make -j2 all NO_OPENSSL=1 USE_LIBPCRE2=1 prefix=/usr gitexecdir=/usr/lib/git-core \
    NO_CROSS_DIRECTORY_HARDLINKS=1 NO_INSTALL_HARDLINKS=1 NO_PERL_CPAN_FALLBACKS=1 \
    PYTHON_PATH=/usr/bin/python3 DEFAULT_PAGER=pager DEFAULT_EDITOR=editor \
    CFLAGS="-O2 -g0 -I. -ffile-prefix-map=$tree=/usr/src/confos-git -I$dependency_root/usr/include -I$dependency_root/usr/include/x86_64-linux-gnu" \
    LDFLAGS="-L$dependency_root/usr/lib/x86_64-linux-gnu -Wl,-rpath-link,$dependency_root/usr/lib/x86_64-linux-gnu" \
    CURL_CFLAGS="-I$dependency_root/usr/include/x86_64-linux-gnu" CURL_LDFLAGS=-lcurl
sha256sum git git-remote-http git-http-push git-imap-send
echo 'GIT CODE BUILD PASS'
