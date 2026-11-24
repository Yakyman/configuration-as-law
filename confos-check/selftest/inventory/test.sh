#!/bin/sh
# Planted-object test of inventory and compare: copies the programs to the server, runs test.py there (detached,
# so that a lost connection does not stop it), waits for it, and fetches output.txt and the compare outputs.
# Exit status: that of test.py (0 only if every check passed).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cases=$(cd "$here/../.." && pwd)
. "$cases/local.env"
dir="$SERVER_DIR/inventory"
ssh "$SERVER" "mkdir -p $dir/selftest/inventory"
scp -q "$cases/inventory" "$cases/compare" "$cases/decide.tsv" "$SERVER:$dir/"
scp -q "$here/test.py" "$here/vm.py" "$SERVER:$dir/selftest/inventory/"
ssh "$SERVER" "cd $dir && rm -f selftest/inventory/exit && setsid nohup sh -c 'python3 selftest/inventory/test.py --stock \$HOME/$STOCK_IMAGE --slots \$HOME/$SLOTS_DIR > selftest/inventory/output.txt 2>&1; echo \$? > selftest/inventory/exit' < /dev/null > /dev/null 2>&1 &"
echo "started on the server; waiting"
while ! ssh "$SERVER" "test -e $dir/selftest/inventory/exit"; do sleep 20; done
mkdir -p "$here/out"
scp -q "$SERVER:$dir/selftest/inventory/output.txt" "$here/output.txt"
scp -q "$SERVER:$dir/selftest/inventory/out/*" "$here/out/"
rc=$(ssh "$SERVER" "cat $dir/selftest/inventory/exit")
tail -n 20 "$here/output.txt"
exit "$rc"
