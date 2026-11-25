#!/bin/bash
# Builder gate: the plan's game case on a clean installation of the case party's test
# declaration, built by the documented build command from the files that the source archive
# of this release will hold. The case party's adapter renders the declaration (read, not
# changed); test-game-sequence.sh then performs the sequence of the case.
set -euo pipefail
cd "$(dirname "$0")"
version=$(cat VERSION)
out=$PWD/game-sequence-build-$version
test ! -e "$out"
trap 'rm -rf "$out"' EXIT
mkdir "$out"
cases=../search/cases-copy
if [ -d ../cases/run/src11/declarations ] && [ -e ../cases/run/src11/adapter.py ]; then cases=../cases/run/src11; fi
if [ -d ../cases/declarations ] && [ -e ../cases/adapter.py ]; then cases=../cases; fi
python3 archive-members.py "$version" >"$out/members"
tar --no-recursion --null -T "$out/members" -czf "$out/candidate-source.tar.gz"
{
    echo "cases tree: $cases"
    python3 -B ../search/tools/build-clean.py "$cases" "$out/candidate-source.tar.gz" "$out/clean"
} >"logs/game-sequence-build-$version.log" 2>&1
bash test-game-sequence.sh "$version" "$out/clean/clean.qcow2" "$out/clean/key" "$out/clean/D-test" \
    "$out/clean/source" 22453 game-packages.conf ../cases/inputs/game
grep -qx "GAME SEQUENCE PASS ($version)" "logs/game-sequence-$version.log"
