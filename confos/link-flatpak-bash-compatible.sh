#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/flatpak-bash-compatible-link.log 2>&1
source slots.sh
confos_reserve_guest
work="$PWD/interpreter-inputs/flatpak-bash-compatible"
runtime="$PWD/interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08/df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c/files"
libs="$runtime/lib/x86_64-linux-gnu"
sha256sum "$libs/libreadline.so.8" "$libs/libhistory.so.8" "$libs/libtinfo.so.6"
cd "$work"
# Host libc predates the target library's GLIBC_2.42 requirement. Defer only
# shared-dependency resolution to the original runtime; validate by executing
# there below. No RPATH or additional runtime library is installed.
make -j2 BASE_LDFLAGS="-rdynamic -Wl,-rpath-link,$libs -Wl,--allow-shlib-undefined" READLINE_LIB="$libs/libreadline.so.8" HISTORY_LIB="$libs/libhistory.so.8" TERMCAP_LIB="$libs/libtinfo.so.6"
sha256sum bash
readelf -d bash
readelf -V bash
bwrap --unshare-all --die-with-parent --clearenv --ro-bind "$runtime" /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu --ro-bind "$work/bash" /usr/bin/bash /usr/bin/bash -c 'printf "BASH RUNTIME CONTROL %s\\n" "$BASH_VERSION"; /usr/bin/sh -c "echo SH-ALIAS-PASS"; bind -l >/dev/null'
echo 'BASH EXACT RUNTIME DYNAMIC LINK CHECK PASS'
