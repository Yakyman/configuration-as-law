#!/bin/bash
# Laptop side: copy cases/ to the server, start the self-test or a run there, copy results back.
#   lib/remote.sh push
#   lib/remote.sh selftest            # push, run selftest/run/selftest.sh on the server, copy its output back
#   lib/remote.sh pull NAME           # copy runs/NAME (without raw inventories) into ../runs/NAME
#   lib/remote.sh list NAME [--stop-at ID]  # print the list of cases of runs/NAME that did not pass
#   lib/remote.sh compact NAME        # shrink a finished run on the server (gzip inventories, hard-link copies)
set -euo pipefail
CASES=$(cd "$(dirname "$0")/.." && pwd)
. "$CASES/local.env"
SRC="$SERVER_DIR/${REMOTE_SRC:-run/src}"   # REMOTE_SRC=run/src2 while a run uses run/src
push() {
  ssh "$SERVER" "mkdir -p $SRC"
  scp -q -r "$CASES"/* "$SERVER:$SRC/"
}
case "${1:-}" in
  push) push ;;
  selftest)
    push
    ssh "$SERVER" "cd $SRC && bash selftest/run/selftest.sh > ../selftest-output.txt 2>&1; echo exit=\$?" || true
    scp -q "$SERVER:$SERVER_DIR/run/selftest-output.txt" "$CASES/selftest/run/output.txt"
    tail -n 5 "$CASES/selftest/run/output.txt" ;;
  specificity)
    # [n2-7]: the latest release of build/STATE.md, its checksum checked on the server
    push
    V=$(sed -n 's/^## Current released version: *\([0-9.]*\).*/\1/p' "$CASES/../build/STATE.md" | head -1)
    WANT=$(grep -A8 '^## Current released version' "$CASES/../build/STATE.md" | grep -A1 "confos-$V-source.tar.gz" | grep -o '[0-9a-f]\{64\}' | head -1)
    TAR="$SERVER_BUILD_DIR/releases/confos-$V-source.tar.gz"
    HAVE=$(ssh "$SERVER" "sha256sum $TAR" | cut -c1-64)
    [ -n "$WANT" ] && [ "$HAVE" = "$WANT" ] || { echo "release $V: checksum $HAVE, build/STATE.md says ${WANT:-nothing}" >&2; exit 1; }
    ssh "$SERVER" "cd $SRC && bash selftest/specificity/test.sh \$HOME/$TAR > ../specificity-output.txt 2>&1; echo exit=\$?" || true
    scp -q "$SERVER:$(dirname "$SRC")/specificity-output.txt" "$CASES/selftest/specificity/output.txt"
    tail -n 25 "$CASES/selftest/specificity/output.txt" ;;
  pull)
    # everything of the run except the raw inventories (several GB per run; they stay on the server)
    mkdir -p "$CASES/../runs/$2"
    ssh "$SERVER" "cd $SERVER_DIR/runs && tar -cf - --exclude='*/inventory' --exclude='*/declaration-from-disk' \
      --exclude='*/derived.jsonl' --exclude='*/compare.tsv' --exclude='*/compare-excluded.tsv' --exclude='*/attempt-delta.tsv' '$2'" | tar -xf - -C "$CASES/../runs" ;;
  list)
    # the list of cases that did not pass (tools/failing-list.py), made on the server where the comparisons are
    scp -q "$CASES/tools/failing-list.py" "$SERVER:$SERVER_DIR/failing-list.py"
    ssh "$SERVER" "python3 -I $SERVER_DIR/failing-list.py $SERVER_DIR/runs/$2 ${3:-} ${4:-} ${5:-} ${6:-}" ;;
  compact)
    # after a run has ended and its list is made: raw inventories gzipped, identical files (declaration payloads read
    # back from every disk) hard-linked; a full run shrinks from ~30 GB to a few GB (COMMON.md: at most 60 GB)
    ssh "$SERVER" "cd $SERVER_DIR/runs && find '$2' -path '*/inventory/*.jsonl' -type f -print0 | xargs -0 -r -P 8 -n 20 gzip -6 && hardlink -q -c '$2'; du -sh '$2' ~/$SERVER_DIR" ;;
  *) echo "usage: remote.sh push|selftest|pull NAME|list NAME [--stop-at ID]|compact NAME" >&2; exit 2 ;;
esac
