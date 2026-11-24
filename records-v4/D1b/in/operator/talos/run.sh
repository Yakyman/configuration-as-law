#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"
export LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
export S4_INPUTS="$PWD/S4" INPUTS_COMMIT=c62afbb5861fb038aa7da0aa00c0730ad140ec7c
mkdir -p D1b/in/operator/talos
logs=D1b/in/operator/talos
printf 'phase\texit_status\tduration_seconds\tstarted_utc\n' > "$logs/status.tsv"
phase() {
 local label=$1; shift
 local start finish rc stamp
 start=$(date +%s); stamp=$(date -u +%FT%TZ)
 "$@" > "$logs/$label.stdout" 2> "$logs/$label.stderr"
 rc=$?; finish=$(date +%s)
 printf '%s\t%s\t%s\t%s\n' "$label" "$rc" "$((finish-start))" "$stamp" >> "$logs/status.tsv"
 return "$rc"
}
phase new ./lab.sh new d1b-talos talos
boot=$?
if [ "$boot" -eq 0 ]; then
 phase collector env C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-talos D1b/raw/talos
fi
phase destroy ./lab.sh destroy d1b-talos
if [ "$?" -ne 0 ]; then
 phase kill ./lab.sh kill d1b-talos
 phase destroy-after-kill ./lab.sh destroy d1b-talos
fi
date -u +%FT%TZ > "$logs/complete"
