#!/bin/bash
# Keeps running runs within the disk limit of COMMON.md (60 GB for the case party): every 10 minutes, the raw
# inventory files (inventory/*.jsonl, also of the reference installations) that are older than 20 minutes are gzipped
# in each named run, until none of the runs' units is active. `compare` reads a gzipped inventory as it is
# (load_jsonl: PATH.gz when PATH is absent); the runner reads a raw inventory only right after taking it.
# Runs on the server:  tools/compact-live.sh RUNS_DIR NAME...
set -u
runs=$1; shift
while :; do
  active=0
  for n in "$@"; do
    systemctl --user is-active --quiet "cases-$n" && active=1
    [ -d "$runs/$n" ] && find "$runs/$n" -path '*/inventory/*.jsonl' -type f -mmin +20 -print0 | \
      xargs -0 -r -P 4 -n 20 gzip -6
  done
  du -sh "$runs" 2>/dev/null | tail -1
  [ $active = 1 ] || break
  sleep 600
done
