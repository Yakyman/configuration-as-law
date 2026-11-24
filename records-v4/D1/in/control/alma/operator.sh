#!/bin/bash
set -u
cd "$HOME/VMs/cal-1123"
work="$PWD/D1/alma"
mkdir -p "$work/control"
exec >"$work/control/operator.log" 2>&1
record() { printf '%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" >> "$work/control/status.tsv"; }
finish() { ./lab.sh destroy d1-alma >"$work/control/destroy.out" 2>"$work/control/destroy.err"; record destroy "$?"; date -u +%FT%TZ > "$work/control/FINISHED"; }
trap finish EXIT
./lab.sh new d1-alma alma >"$work/control/new.out" 2>"$work/control/new.err"
rc=$?; record new "$rc"; [ "$rc" = 0 ] || exit "$rc"
python3 - "$work" <<'PY'
import base64,io,tarfile,pathlib,sys
work=pathlib.Path(sys.argv[1]); buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:gz') as tf: tf.add('D1/inputs/actions',arcname='actions')
payload=base64.b64encode(buf.getvalue()).decode()
script='''#!/bin/bash
set -e
mkdir -p /tmp/d1-alma-operator
base64 -d <<'PAYLOAD' | tar -xz -C /tmp/d1-alma-operator
'''+payload+'''
PAYLOAD
cat > /tmp/d1-alma-operator/run.sh <<'RUN'
#!/bin/bash
cd /tmp/d1-alma-operator/actions
bash alma.sh
rc=$?
printf '%s\\n' "$rc" > /tmp/d1-alma-operator/action-exit
RUN
chmod 700 /tmp/d1-alma-operator/run.sh
nohup setsid bash /tmp/d1-alma-operator/run.sh > /tmp/d1-alma-operator/entry.out 2> /tmp/d1-alma-operator/entry.err < /dev/null &
'''
(work/'control/stage.sh').write_text(script)
PY
./lab.sh run d1-alma < "$work/control/stage.sh" > "$work/control/stage.out" 2> "$work/control/stage.err"
rc=$?; record stage "$rc"; [ "$rc" = 0 ] || exit "$rc"
while true; do
 sleep 30
 printf '%s\n' 'if test -f /tmp/d1-alma-operator/action-exit; then cat /tmp/d1-alma-operator/action-exit; else echo running; fi' | ./lab.sh run d1-alma > "$work/control/action-state" 2>> "$work/control/action-state.err"
 rc=$?; record action-status-transport "$rc"
 if [ "$rc" = 0 ] && ! grep -qx running "$work/control/action-state"; then break; fi
done
for path in /home/user/actions-status.tsv /home/user/actions-logs /tmp/d1-alma-operator; do
 ./lab.sh copy-out d1-alma "$path" "$work/control" >> "$work/control/copy.out" 2>> "$work/control/copy.err"
 rc=$?; record copy-actions "$rc"; [ "$rc" = 0 ] || exit "$rc"
done
printf '%s\n' 'rm -rf /tmp/d1-alma-operator "$HOME/actions-logs" "$HOME/actions-status.tsv"' | ./lab.sh run d1-alma > "$work/control/cleanup.out" 2> "$work/control/cleanup.err"
rc=$?; record staging-cleanup "$rc"; [ "$rc" = 0 ] || exit "$rc"
LAB_ROOT="$PWD" C1_INPUTS_COMMIT=b3c3c141c612b8d287c8058733141cb56d1c2431 bash D1/inputs/collect.sh --observe d1-alma "$work/raw" > "$work/control/collector.out" 2> "$work/control/collector.err"
rc=$?; record collector "$rc"
exit "$rc"
