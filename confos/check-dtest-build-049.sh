#!/bin/bash
# Builder check, not an acceptance: the case party's test declaration, rendered by its
# own adapter, is built from the published 0.49 source archive with the search's tool
# (both read, neither changed). On 0.43 this build failed (Flatpak reader bundle
# checksum). Then the package objects of the recording tools are compared with the
# downloaded archives in that build. Throw-away output is removed at the end.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/dtest-build-0.49.log 2>&1
out=dtest-049
test ! -e "$out"
trap 'rm -rf "$out"' EXIT
sha256sum -c releases/release-0.49.sha256 2>/dev/null | grep 'source.tar.gz: OK'
cases=../search/cases-copy
if [ -d ../cases/declarations ] && [ -e ../cases/adapter.py ];then cases=../cases;fi
echo "cases tree: $cases"
python3 -B ../search/tools/build-clean.py "$cases" releases/confos-0.49-source.tar.gz "$out"
ls "$out" "$out/D-test" | head -40
test -s "$out/clean.qcow2"
# The first run of this script (22:33 UTC) built the disk and then stopped here: the
# build tool leaves no work folder. The stored root is therefore read from the disk.
work=$(find "$out" -maxdepth 3 -type d -name '*.work' | head -1)
if [ -n "$work" ];then
 python3 compare-native-entries.py "$work"
else
 bash check-dtest-disk-049.sh "$out/clean.qcow2"
fi
echo 'TEST DECLARATION OF THE CASE PARTY BUILDS FROM THE 0.49 SOURCE; PACKAGE OBJECTS IN PLACE PASS'
