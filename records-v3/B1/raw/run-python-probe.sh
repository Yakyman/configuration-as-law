#!/bin/bash
# Execute on the server in the disposable-VM task directory, once only.
set -u
cd "$HOME/VMs/cal-1122/B1"
ssh -F /dev/null -i guest-key -o StrictHostKeyChecking=no -o UserKnownHostsFile=known_hosts -o LogLevel=ERROR -p 22382 root@127.0.0.1 'LC_ALL=C python3 -' < guest-probe.py
probe_rc=$?
printf 'PROBE_EXIT %s\n' "$probe_rc"
exit "$probe_rc"
