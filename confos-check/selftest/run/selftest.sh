#!/bin/bash
# Self-test of the runner. Runs ON THE SERVER from the copy of cases/ (lib/remote.sh selftest does it from the
# laptop). At most 2 machines at once, 2 GB and 2 vCPU each, on the stock Debian 13 cloud image.
set -u
cd "$(dirname "$0")/../.."
CASES=$PWD
. ./local.env
BASE="$HOME/$SERVER_DIR/run"
NAME=selftest-stock
status=0
echo "selftest of the runner, start $(date -u +%FT%TZ)"

echo "== 1. machinery"
python3 -I selftest/run/machinery.py || status=1

echo "== 2. run --backend stock on a subset"
./run --backend stock --name "$NAME" --only P4-SHELL,P4-C9-4,P4-PIPE-1,P1-0,OW-1,OW-10 --max-vms 2 --vm-mem 2048 \
  || status=1
RUNDIR="$HOME/$SERVER_DIR/runs/$NAME"
echo "-- results.tsv"
cat "$RUNDIR/results.tsv"
python3 -I selftest/run/check-results.py "$RUNDIR" || status=1

echo "== 3. cleanup"
ours=$(pgrep -a qemu | grep -F "$BASE/work/$NAME/" || true)
echo "qemu processes with our work folder: ${ours:-none}"
[ -z "$ours" ] || status=1
echo "ls of our work folder:"
ls -1A "$BASE/work/$NAME" 2>&1
left=$(find "$BASE/work/$NAME" -name '*.qcow2' 2>/dev/null)
echo "disks left: ${left:-none}"
[ -z "$left" ] || status=1
held=0
for n in 1 2 3 4 5 6; do
  if ! flock -n "$HOME/$SLOTS_DIR/slot-$n.lock" true; then
    holder=$(fuser "$HOME/$SLOTS_DIR/slot-$n.lock" 2>/dev/null)
    for p in $holder; do grep -qF "$BASE/work/$NAME/" "/proc/$p/cmdline" 2>/dev/null && held=1; done
    echo "slot $n held by another party (pids:$holder)"
  fi
done
echo "slots held by our processes: $held"
[ "$held" = 0 ] || status=1

echo "== 3b. a run stopped by a signal while a case is in progress"
STOP=selftest-stop
STOPDIR="$HOME/$SERVER_DIR/runs/$STOP"
rm -rf "$STOPDIR" "$BASE/work/$STOP"
# P4-PIPE-1: on the stock image it runs commands in the guest (OW-1 ends at once there: no ConfOS operation), so
# the signal arrives while the case is in progress
./run --backend stock --name "$STOP" --only P4-PIPE-1 --max-vms 1 --vm-mem 2048 > "$BASE/selftest-stop.out" 2>&1 &
rpid=$!
for i in $(seq 1 180); do
  grep -qs 'U\$' "$STOPDIR/P4-PIPE-1/log.txt" && break
  kill -0 "$rpid" 2>/dev/null || break
  sleep 5
done
if kill -0 "$rpid" 2>/dev/null; then
  sleep 5
  echo "sending SIGTERM to the runner (pid $rpid) at $(date -u +%FT%TZ)"
  kill -TERM "$rpid"
else
  echo "CHECK stop-during-case FAIL (the runner ended before a guest command of the case: nothing to stop)"; status=1
fi
wait "$rpid"; echo "runner exit $?"
python3 -I selftest/run/check-stop.py "$STOPDIR" || status=1
python3 -I selftest/run/check-stop-row.py ./run || status=1
ours=$(pgrep -a qemu | grep -F "$BASE/work/$STOP/" || true)
echo "qemu processes with the stopped run's work folder: ${ours:-none}"
[ -z "$ours" ] || status=1
left=$(find "$BASE/work/$STOP" -name '*.qcow2' 2>/dev/null)
echo "disks left by the stopped run: ${left:-none}"
[ -z "$left" ] || status=1
rm -rf "$STOPDIR" "$BASE/work/$STOP" "$BASE/keys/$STOP"

echo "== 4. run --list against CASES.md"
./run --list > "$BASE/list.txt"
python3 -I selftest/run/extract-ids.py CASES.md > "$BASE/cases-ids.txt"
if diff "$BASE/cases-ids.txt" "$BASE/list.txt"; then
  echo "CHECK list-matches-CASES.md PASS $(wc -l < "$BASE/list.txt") IDs"
else
  echo "CHECK list-matches-CASES.md FAIL"; status=1
fi

echo "== 5. the repairs of the fifth freeze ([f5-a], [f5-b], [f5-c] of CORRECTIONS.md; each fails on the fourth)"
python3 -I selftest/run/check-before-record.py ./run || status=1
bash selftest/run/check-routes-background.sh ./run || status=1
REL=${CASES_RELEASE:-$HOME/$SERVER_BUILD_DIR/releases/confos-0.43-source.tar.gz}
RELDIR=$(mktemp -d)
if tar -xzf "$REL" -C "$RELDIR" assemble.py archive_sources.py archive-sources.json 2>/dev/null || \
   tar -xzf "$REL" -C "$RELDIR"; then
  python3 -I selftest/run/check-repro2-accounts.py ./run "$RELDIR" || status=1
else
  echo "CHECK repro2-accounts FAIL (the release $REL could not be unpacked)"; status=1
fi
rm -rf "$RELDIR"

echo "end $(date -u +%FT%TZ)"
if [ "$status" = 0 ]; then echo "SELFTEST PASS"; else echo "SELFTEST FAIL"; fi
exit "$status"
