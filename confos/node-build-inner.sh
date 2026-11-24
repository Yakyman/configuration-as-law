#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
dependency_root="$PWD/interpreter-inputs/node/dependencies/root"
# Pinned external builtins must be visible at their final paths while snapshot
# tools run. This mount exists only in the private user/mount namespace.
mount --bind "$dependency_root/usr/share/nodejs" /usr/share/nodejs
mount -o remount,bind,ro /usr/share/nodejs
cd interpreter-inputs/node/tree
make -j2
