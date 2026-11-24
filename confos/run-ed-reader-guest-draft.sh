#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >interpreter-inputs/ed-reader-draft/guest-build-run.log 2>&1
python3 build-ed-reader-guest-draft.py
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved interpreter-inputs/ed-reader-draft/guest/disk.qcow2 22453 3072 interpreter-inputs/ed-reader-draft/guest.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22453 user@127.0.0.1)
expected=$(sha256sum interpreter-inputs/ed-reader-draft/guest/inputs/declaration.conf | cut -d' ' -f1)
ready=0
for attempt in {1..150};do
 if [ "$(ssh "${args[@]}" 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
ssh "${args[@]}" 'python3 /usr/local/bin/probe-ed-reader-guest-draft.py'
echo ED_READER_PRIVATE41_PIPELINE_PASS
