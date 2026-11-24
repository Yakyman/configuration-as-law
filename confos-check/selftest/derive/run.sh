#!/bin/bash
# Run the self-test of `derive`: copy the program and the test to the server, run selftest/server.sh there, and
# keep its full output (output.txt), the derivation (derived.jsonl), the base derivation (base.jsonl) and the log
# of what derive read (derive-reads.log) here. Exit status is that of the test.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
CASES=$(cd "$HERE/../.." && pwd)
. "$CASES/local.env"
D="$SERVER_DIR/derive"
ssh "$SERVER" "mkdir -p $D/selftest/decl $D/published" || exit 2
scp -q "$CASES/derive" "$SERVER:$D/derive" || exit 2
scp -q "$CASES/local.env" "$SERVER:$D/local.env" || exit 2
scp -q "$HERE/server.sh" "$HERE/check.py" "$HERE/check-overrides.py" "$HERE/guest.sh" "$SERVER:$D/selftest/" || exit 2
scp -q "$HERE/decl/"* "$SERVER:$D/selftest/decl/" || exit 2
# The component list of the base, as published by the builder (read, never changed).
# The component lock of the base as published: from the source archive of the latest released version
# (build/STATE.md, "Current released version"), not from the builder's working folder.
V=$(sed -n 's/^## Current released version: *//p' "$CASES/../build/STATE.md" | head -1)
[ -n "$V" ] || { echo "no released version in build/STATE.md"; exit 2; }
ssh "$SERVER" "rm -rf $D/published && mkdir -p $D/published && tar -xzf \$HOME/$SERVER_BUILD_DIR/releases/confos-$V-source.tar.gz -C $D/published --wildcards --no-anchored VERSION components.txt 'components/*' 'packages/*'" || exit 2
ssh "$SERVER" "cd $D/published && d=\$(dirname \$(find . -name components.txt | head -1)) && [ \"\$d\" = . ] || { cp -r \$d/* . ; }; ls; cat VERSION" || exit 2
ssh "$SERVER" "bash $D/selftest/server.sh" > "$HERE/output.txt" 2>&1
rc=$?
for f in derived.jsonl base.jsonl base-t0.jsonl unknown.jsonl derive-reads.log; do
  scp -q "$SERVER:$D/results/$f" "$HERE/$f"
done
# The log names directories of the server; keep it relative to the test folder.
sed -i "s|\"/[^\"]*/$D/|\"\$DIR/|g; s|'/[^']*/$D/|'\$DIR/|g" "$HERE/derive-reads.log"
tail -n 16 "$HERE/output.txt"
exit $rc
