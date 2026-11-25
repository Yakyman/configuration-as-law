#!/bin/bash
# [f6]: casedefs_search.py and the rows of section P4-S of CASES.md are exactly what tools/make-search-cases.py writes
# from the tables and scripts of the search and the builder's finding; and every P4-S case of casedefs.py is in the
# order of CASES.md. Runs where the folders of the search and of the builder are next to cases/.
# usage: bash selftest/run/check-search-cases.sh [SEARCH_DIR BUILD_DIR]
set -u
C=$(cd "$(dirname "$0")/../.." && pwd)
S=${1:-$C/../search}
B=${2:-$C/../build}
T=$(mktemp -d)
trap 'rm -f "$T"/casedefs_search.py "$T"/search-cases.md "$T"/ids-md "$T"/ids-run; rmdir "$T"' EXIT
fail=0
python3 -I "$C/tools/make-search-cases.py" "$S" "$B" "$T" > /dev/null || { echo "FAIL: the program stopped"; exit 1; }
# the cases (every line but the comments of the head, which record the checksums of the inputs) must be equal; an
# input that changed since the file was written is reported, and counts only if the cases changed with it
if cmp -s <(grep -v '^#' "$T/casedefs_search.py") <(grep -v '^#' "$C/casedefs_search.py"); then
  echo "ok: the cases of casedefs_search.py are the program's output"
else echo "FAIL: the cases of casedefs_search.py differ from the program's output"; fail=1; fi
diff <(grep '^#   ' "$C/casedefs_search.py") <(grep '^#   ' "$T/casedefs_search.py") | sed -n 's/^> #   /note: input changed since the freeze: /p'
# every row the program writes is a row of CASES.md, in its order
if python3 -I "$C/selftest/run/check-search-rows.py" "$T/search-cases.md" "$C/CASES.md" > /dev/null
then echo "ok: the $(grep -c '^| P4-S-' "$T/search-cases.md") rows are in CASES.md, in order"
else echo "FAIL: a row of the program is not in CASES.md, or not in order"; fail=1; fi
python3 -I "$C/selftest/run/extract-ids.py" "$C/CASES.md" > "$T/ids-md"
(cd "$C" && ./run --list) > "$T/ids-run" 2>&1
if cmp -s "$T/ids-md" "$T/ids-run"; then echo "ok: run --list = the IDs of CASES.md ($(wc -l < "$T/ids-md"))"
else echo "FAIL: run --list differs from CASES.md"; fail=1; fi
[ $fail = 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL"
exit $fail
