#!/usr/bin/env bash
set -u
cd "$HOME/VMs/cal-1123"
w="$PWD/D1/void"
mkdir -p "$w/control"
exec >"$w/control/operator.stdout" 2>"$w/control/operator.stderr"
status() { printf '%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" >>"$w/control/lifecycle.tsv"; }
finish() { ./lab.sh destroy d1-void >"$w/control/destroy.stdout" 2>"$w/control/destroy.stderr"; status destroy "$?"; touch "$w/control/finished"; }
trap finish EXIT
./lab.sh new d1-void void >"$w/control/new.stdout" 2>"$w/control/new.stderr"
rc=$?; status new "$rc"; [ "$rc" = 0 ] || exit "$rc"
{
cat <<'GUEST'
#!/bin/bash
set -eu
mkdir -p /tmp/d1-void-actions
base64 -d <<'PAYLOAD' | tar -xz -C /tmp/d1-void-actions
GUEST
tar -cz -C D1/inputs/actions . | base64
cat <<'GUEST'
PAYLOAD
cat > /tmp/d1-void-actions/run.sh <<'RUN'
#!/bin/bash
cd /tmp/d1-void-actions
bash void.sh
rc=$?
printf '%s\n' "$rc" >/tmp/d1-void-actions/exit-status
RUN
setsid bash /tmp/d1-void-actions/run.sh > /tmp/d1-void-actions/entry.stdout 2>/tmp/d1-void-actions/entry.stderr < /dev/null &
GUEST
} >"$w/control/launch.sh"
./lab.sh run d1-void <"$w/control/launch.sh" >"$w/control/launch.stdout" 2>"$w/control/launch.stderr"
rc=$?; status launch "$rc"; [ "$rc" = 0 ] || exit "$rc"
while :; do
sleep 20
printf '%s\n' '#!/bin/sh' 'test -f /tmp/d1-void-actions/exit-status && cat /tmp/d1-void-actions/exit-status' | ./lab.sh run d1-void --timeout 120 >"$w/control/action-completion.stdout" 2>>"$w/control/action-completion.stderr"
rc=$?; status completion "$rc"
[ "$rc" = 0 ] && break
done
./lab.sh copy-out d1-void /home/user/actions-status.tsv "$w/control/actions-status.tsv"; status copy-status "$?"
./lab.sh copy-out d1-void /home/user/actions-logs "$w/control/actions-logs"; status copy-logs "$?"
./lab.sh copy-out d1-void /tmp/d1-void-actions/entry.stdout "$w/control/entry.stdout"; status copy-entry-stdout "$?"
./lab.sh copy-out d1-void /tmp/d1-void-actions/entry.stderr "$w/control/entry.stderr"; status copy-entry-stderr "$?"
printf '%s\n' '#!/bin/sh' 'rm -rf /tmp/d1-void-actions "$HOME/actions-status.tsv" "$HOME/actions-logs"' | ./lab.sh run d1-void >"$w/control/cleanup.stdout" 2>"$w/control/cleanup.stderr"
rc=$?; status cleanup "$rc"; [ "$rc" = 0 ] || exit "$rc"
LAB_ROOT="$PWD" C1_INPUTS_COMMIT=b3c3c141c612b8d287c8058733141cb56d1c2431 bash D1/inputs/collect.sh --observe d1-void "$w/raw" >"$w/control/collector.stdout" 2>"$w/control/collector.stderr"
status collector "$?"
