#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
mkdir -p /tmp/w1-day
exec > >(tee /tmp/w1-day/day-root.log) 2>&1
set -x
date -u --iso-8601=seconds
if [ -f /tmp/w1-user-day.log ] && grep -qx USER_DAY_DONE /tmp/w1-user-day.log; then
  cp /tmp/w1-user-day.log /tmp/w1-day/user-day.log
else
  su - guest -c 'bash /mnt/taskshare/day-user.sh' > /tmp/w1-day/user-day.log 2>&1
fi
cat /tmp/w1-day/user-day.log
herd status > /tmp/w1-day/services-before-dwell.txt
date -u --iso-8601=seconds > /tmp/w1-day/dwell-start.txt
sleep 120
date -u --iso-8601=seconds > /tmp/w1-day/dwell-end.txt
herd status > /tmp/w1-day/services-after-dwell.txt
CENSUS_USER=guest bash /mnt/taskshare/collect.sh
cp /tmp/w1-declarations-before.sha256 /tmp/w1-day/
tar -C /tmp -czf /tmp/w1-day.tar.gz w1-day
echo DAY_AND_CENSUS_DONE
