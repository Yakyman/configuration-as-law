#!/bin/bash
set -u
export INPUTS_COMMIT=c62afbb5861fb038aa7da0aa00c0730ad140ec7c
export S4_INPUTS="$PWD/S4"
O=D1b/in/operator/microos
printf 'operation\texit_status\tduration_seconds\tstarted_utc\tfinished_utc\n' > "$O/status.tsv"
step() {
  local name=$1
  shift
  local before=$(date +%s) started=$(date -u +%FT%TZ)
  "$@" > "$O/$name.stdout" 2> "$O/$name.stderr"
  local status=$? after=$(date +%s)
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$status" "$((after-before))" "$started" "$(date -u +%FT%TZ)" >> "$O/status.tsv"
  return "$status"
}
if step new ./lab.sh new d1b-microos microos; then
  step collect env C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-microos D1b/raw/microos
fi
if ! step destroy ./lab.sh destroy d1b-microos; then
  step kill ./lab.sh kill d1b-microos
  step destroy-fallback ./lab.sh destroy d1b-microos
fi
date -u +%FT%TZ > "$O/completed.txt"
