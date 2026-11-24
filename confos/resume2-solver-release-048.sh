#!/bin/bash
# Second resumption of the 0.48 gates. The clean image and the extended smoke of the
# first resumption stand (logs/smoke-0.48.log ends SMOKE PASS); only the solver probe,
# which ended on one reset SSH connection, and the update test are run again.
set -euo pipefail
cd "$(dirname "$0")"
test ! -e releases/confos-0.48-source.tar.gz
test -s images/confos-0.48-clean.qcow2
grep -qx 'SMOKE PASS' logs/smoke-0.48.log
if pgrep -f '(^|/)qemu-system-x86_64 .*images/solver-048\.qcow[2]';then exit 1;fi
attempt=second
if [ -e records/solver-048-second ];then attempt=third;fi
test ! -e "records/solver-048-$attempt"
mkdir -p "records/solver-048-$attempt"
cp logs/solver-0.48.log logs/prepare-solver-0.48.log "records/solver-048-$attempt/"
cp logs/solver-048-1.serial "records/solver-048-$attempt/" 2>/dev/null || true
rm -f images/solver-048.qcow2 logs/solver-048-*.serial logs/solver-048-*.serial.qmp
exec >>logs/prepare-solver-0.48.log 2>&1
echo 'RESUMED: THE PROBE SCRIPT ITSELF KILLED THE MACHINE (A FUNCTION NAMED cut); BUILD AND SMOKE ABOVE STAND'
bash probe-solver-048.sh
bash test-updates.sh
cp logs/test-updates.log logs/updates-0.48.log
echo 'CANDIDATE48 SOLVER AND REGRESSIONS PASS'
