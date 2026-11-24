#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >interpreter-inputs/ssh-reader-draft/guest-build-run.log 2>&1
python3 build-ssh-reader-guest-draft.py
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved interpreter-inputs/ssh-reader-draft/guest/disk.qcow2 22454 3072 interpreter-inputs/ssh-reader-draft/guest.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -i private/login -p 22454 user@127.0.0.1)
expected=$(sha256sum interpreter-inputs/ssh-reader-draft/guest/inputs/declaration.conf | cut -d' ' -f1)
ready=0
for attempt in {1..150};do
 if [ "$(ssh "${args[@]}" 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
ssh "${args[@]}" 'python3 /usr/local/bin/probe-ssh-reader-guest-draft.py'
echo SSH_READER_PRIVATE42_PIPELINE_PASS
