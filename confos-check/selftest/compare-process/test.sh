#!/bin/bash
# Fixture test of compare ([f7], 2026-11-25): a process is placed by the checksum of the file it executes, not by
# the name that file has in the process's mount namespace. Both directions: the process of a recorded application
# whose path exists only in its sandbox is placed; a process whose file is no stored object is reported; a process
# whose path equals a stored path while its file differs is not placed by that path (also not by a `service` line).
# The fixture is written by make.py. Usage: test.sh [COMPARE] (default: the compare of this tree).
cd "$(dirname "$0")" || exit 2
cmp_prog=${1:-../../compare}
python3 -I make.py || exit 2
python3 -I "$cmp_prog" --inventory inv --baseline base --decide ../../decide.tsv --out compare.tsv
rc=$?; [ "$rc" = 2 ] && { echo "RESULT: FAIL (compare error)"; exit 1; }
python3 -I "$cmp_prog" --inventory inv --derived derived.jsonl --declaration decl.conf --decide /dev/null \
  --out compare-derived.tsv
rc=$?; [ "$rc" = 2 ] && { echo "RESULT: FAIL (compare error)"; exit 1; }
python3 -I check.py compare.tsv compare-derived.tsv
