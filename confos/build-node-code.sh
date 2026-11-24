#!/bin/bash
# Worker-only source build; all missing libraries are in the private dependency root.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/node-code-build.log 2>&1
sha256sum -c node-source.sha256
work="$PWD/interpreter-inputs/node/tree"
dependency_root="$PWD/interpreter-inputs/node/dependencies/root"
export SOURCE_DATE_EPOCH=1795392000 TZ=UTC LC_ALL=C
export PKG_CONFIG_SYSROOT_DIR="$dependency_root"
export PKG_CONFIG_LIBDIR="$dependency_root/usr/lib/x86_64-linux-gnu/pkgconfig:$dependency_root/usr/share/pkgconfig"
export LD_LIBRARY_PATH="$dependency_root/usr/lib/x86_64-linux-gnu"
export CFLAGS="-O2 -g0 -ffile-prefix-map=$work=/usr/src/confos-node"
export CXXFLAGS="$CFLAGS"
gcc --version | head -1
ld --version | head -1
cd "$work"
./configure --without-npm --without-corepack --shared --shared-zlib --shared-cares \
    --shared-ngtcp2 --shared-nghttp3 --shared-nghttp2 --shared-brotli --shared-simdjson \
    --shared-builtin-undici/undici-path=/usr/share/nodejs/undici/undici-fetch.js \
    --shared-builtin-acorn-path=/usr/share/nodejs/acorn/dist/acorn.js \
    --shared-builtin-acorn_walk-path=/usr/share/nodejs/acorn-walk/dist/walk.js \
    --shared-builtin-cjs_module_lexer/lexer-path=/usr/share/nodejs/cjs-module-lexer/lexer.js \
    --shared-builtin-cjs_module_lexer/dist/lexer-path=/usr/share/nodejs/cjs-module-lexer/dist/lexer.js \
    --shared-builtin-minimatch-path=/usr/share/nodejs/minimatch/dist/cjs/index.bundle.js \
    --shared-openssl --openssl-use-def-ca-store --with-intl=system-icu --shared-libuv \
    --prefix=/usr --arch-triplet=x86_64-linux-gnu \
    --node-relative-path=lib/x86_64-linux-gnu/nodejs:share/nodejs --dest-os=linux --dest-cpu=x64
cd ../../..
python3 prepare-node-build-tree.py
unshare --user --map-root-user --mount --propagation private bash node-build-inner.sh
cd "$work"
sha256sum out/Release/node out/Release/libnode.so.115
echo 'NODE CODE BUILD PASS'
