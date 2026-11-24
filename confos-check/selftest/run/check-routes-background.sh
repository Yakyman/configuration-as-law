#!/bin/bash
# Check of [f5-b] of CORRECTIONS.md: the routes script of `run` ends when a route starts a background process, and
# writes the line of that route. Two files of the form of P4-C9-1 and P4-C9-2 of complete run 1: a shell script that
# starts `sleep 86417 &`, a Python file that starts `sleep 86418` in a session of its own. The script of the given
# `run` is given each file under `timeout 120`, as the account that runs this check, on a stock Debian system (where
# every route executes the file: the case that hung). The background processes are stopped at the end.
# Fails on the fourth freeze (the script is ended by the timeout and writes no line for the data routes).
# Usage: check-routes-background.sh PATH-OF-run
set -u
RUN=$1
HERE=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d)
status=0
python3 -I "$HERE/extract-routes.py" "$RUN" > "$T/routes.sh" || { echo "RESULT: FAIL (no routes script)"; exit 1; }
printf '#!/bin/bash\nsleep 86417 &\necho started\n' > "$T/f.sh"
printf 'import subprocess\nsubprocess.Popen(["sleep", "86418"], start_new_session=True)\n' > "$T/f.py"
for f in f.sh f.py; do
  start=$(date +%s)
  timeout 120 bash "$T/routes.sh" "$T/$f" > "$T/$f.out" 2> "$T/$f.err" < /dev/null
  code=$? took=$(( $(date +%s) - start ))
  lines=$(wc -l < "$T/$f.out")
  data=$(awk -F'\t' '$2 == "data"' "$T/$f.out" | cut -f3,4 | tr '\t\n' ': ')
  echo "file $f: exit $code after ${took}s, $lines route lines; data routes: $data"
  if [ "$code" = 124 ]; then echo "CHECK $f-ends FAIL (ended by the timeout of 120 s)"; status=1
  else echo "CHECK $f-ends PASS"; fi
  want=cat-pipe-bash; [ "$f" = f.py ] && want=python3-exec
  if awk -F'\t' -v w="$want" '$2 == "data" && $3 == w' "$T/$f.out" | grep -q .; then echo "CHECK $f-$want-recorded PASS"
  else echo "CHECK $f-$want-recorded FAIL (no line for the route $want)"; status=1; fi
done
pkill -f '^sleep 8641[78]$'; sleep 1
left=$(pgrep -fc '^sleep 8641[78]$'); echo "background processes left after the check: $left"
rm -f "$T"/*; rmdir "$T"
[ $status = 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL"
exit $status
