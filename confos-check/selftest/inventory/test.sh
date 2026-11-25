#!/bin/sh
# Planted-object test of inventory and compare: copies the programs to the server, runs test.py there (detached,
# so that a lost connection does not stop it), waits for it, and fetches output.txt and the compare outputs.
# Exit status: that of test.py (0 only if every check passed).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cases=$(cd "$here/../.." && pwd)
. "$cases/local.env"
# INVENTORY_PROG / COMPARE_PROG: other programs to test (e.g. those of an earlier freeze); TEST_TAG: a separate
# folder on the server, so that two tests can run at once
dir="$SERVER_DIR/inventory${TEST_TAG:+-$TEST_TAG}"
ssh "$SERVER" "mkdir -p $dir/selftest/inventory"
scp -q "${INVENTORY_PROG:-$cases/inventory}" "$SERVER:$dir/inventory"
scp -q "${COMPARE_PROG:-$cases/compare}" "$SERVER:$dir/compare"
scp -q "$cases/decide.tsv" "$SERVER:$dir/"
scp -q "$here/test.py" "$here/vm.py" "$SERVER:$dir/selftest/inventory/"
ssh "$SERVER" "cd $dir && rm -f selftest/inventory/exit && setsid nohup sh -c 'python3 selftest/inventory/test.py --stock \$HOME/$STOCK_IMAGE --slots \$HOME/$SLOTS_DIR > selftest/inventory/output.txt 2>&1; echo \$? > selftest/inventory/exit' < /dev/null > /dev/null 2>&1 &"
echo "started on the server; waiting"
while ! ssh "$SERVER" "test -e $dir/selftest/inventory/exit"; do sleep 20; done
out="$here/out${TEST_TAG:+-$TEST_TAG}"; mkdir -p "$out"
scp -q "$SERVER:$dir/selftest/inventory/output.txt" "$here/output${TEST_TAG:+-$TEST_TAG}.txt"
scp -q "$SERVER:$dir/selftest/inventory/out/*" "$out/"
rc=$(ssh "$SERVER" "cat $dir/selftest/inventory/exit")
tail -n 25 "$here/output${TEST_TAG:+-$TEST_TAG}.txt"
exit "$rc"
