#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/visudo-editor-0.44.log 2>&1
grep -qx 'CANONICAL44 VISUDO NINE CUTS AND SSH READERS PASS' logs/tools-0.44.log
if pgrep -f '(^|/)qemu-system-x86_64 .*images/tools-044.qcow2';then
 echo 'Refusing concurrent access to the canonical fixture';exit 1
fi
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved images/tools-044.qcow2 22455 3072 logs/visudo-editor-044.serial
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22455 user@127.0.0.1 "$@"; }
ready=0
for attempt in {1..150};do
 if guest 'confos status' 2>/dev/null;then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
guest 'sudo -n python3 -' <visudo-editor-fixture-044.py
expected=$(guest 'sha256sum /state/declaration.conf' | cut -d' ' -f1)
guest 'sudo -n confos apply' || true
ready=0
for attempt in {1..150};do
 if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then ready=1;break;fi
 sleep 2
done
test "$ready" = 1
guest 'sudo -n python3 -' <visudo-editor-controls-044.py
echo 'CANONICAL44 RECORDED VISUDO EDITOR PASS'
