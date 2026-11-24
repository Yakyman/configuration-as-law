#!/bin/bash
set -u
cd "$(dirname "$0")/../../../.."
log=D1b/in/operator/gentoo
python3 - <<'SLOTS' > "$log/slots.txt"
import fcntl,pathlib
held=[]
for n in range(1,13):
 f=open(pathlib.Path('slots')/f'slot-{n}.lock','a')
 try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);held.append(f)
 except BlockingIOError:f.close()
print('free_slots='+str(len(held)))
assert len(held)>=4, 'Fewer than four shared VM slots free'
SLOTS
[ $? = 0 ] || exit 70
start=$(date +%s)
./lab.sh new d1b-gentoo gentoo > "$log/new.stdout" 2> "$log/new.stderr"
rc=$?
printf 'new\t%s\t%s\n' "$rc" "$(($(date +%s)-start))" > "$log/new.status"
