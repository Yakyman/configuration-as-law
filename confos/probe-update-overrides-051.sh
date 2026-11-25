#!/bin/bash
# Builder diagnostic for the failure of complete run 2 on 0.49 (OW-2, OW-3): the
# declaration of the first update state names `curl` of the archive state
# 20260801T000000Z and does not build, `reader override original checksum mismatch:
# /usr/bin/curl`. This lists, for the case party's declaration of that state (a copy,
# read from its run folder) and for the two later archive states, every reader
# override whose package file is not the one the override was built from. Build
# stage only (packages unpacked, overrides checked); no machine is started.
set -uo pipefail
cd "$(dirname "$0")"
exec >logs/update-overrides-0.51.log 2>&1
fixture=update-overrides-051
test ! -e "$fixture" || exit 1
mkdir "$fixture"
trap 'rm -rf "$fixture" images/update-overrides-*.work images/update-overrides-*.qcow2' EXIT
source_decl=../cases/run/work/run-2/vms/OW-2-m/decl
cp -r "$source_decl"/. "$fixture/"
sed -i 's/^base 0\.49$/base 0.51/' "$fixture/declaration.conf"
grep -n '^base \|^snapshot \|^package curl\|^package ed\|^package openssh\|^package gyp\|^package git \|^package nodejs\|^package python3 \|^package make' "$fixture/declaration.conf"
python3 probe-update-overrides-051.py "$fixture/declaration.conf"
echo 'UPDATE OVERRIDES PROBE END'
