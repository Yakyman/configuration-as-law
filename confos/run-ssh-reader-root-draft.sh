#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >interpreter-inputs/ssh-reader-draft/root-controls.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
confos_reserve_guest
confos_boot_reserved interpreter-inputs/ssh-reader-draft/guest/disk.qcow2 22454 3072 interpreter-inputs/ssh-reader-draft/root.serial
args=(-F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -i private/login -p 22454 user@127.0.0.1)
ready=0
for attempt in {1..100}; do
 if ssh "${args[@]}" 'confos status' 2>/dev/null; then ready=1; break; fi
 sleep 2
done
test "$ready" = 1
ssh "${args[@]}" 'bash -s' <<'ROOT_CONTROLS'
set -euo pipefail
test "$(sudo id -u)" = 0
mkdir -p /home/user/ssh-reader-material
printf 'Match exec "touch /tmp/ssh-reader-marker"\n' >/home/user/ssh-reader-material/match.conf
printf 'Host ssh-reader-test\n ProxyCommand touch /tmp/ssh-reader-marker\n' >/home/user/ssh-reader-material/proxy.conf
for kind in match proxy; do
 for origin in material recorded; do
  sudo rm -f /tmp/ssh-reader-marker
  config=/home/user/ssh-reader-material/$kind.conf
  if [ "$origin" = recorded ]; then config=/usr/local/share/ssh-reader-draft/$kind.conf; fi
  query=()
  if [ "$kind" = match ]; then query=(-G); fi
  set +e
  output=$(sudo /usr/bin/ssh -F "$config" -o ConnectTimeout=1 -o BatchMode=yes "${query[@]}" ssh-reader-test 2>&1)
  status=$?
  set -e
  marker=no
  if test -e /tmp/ssh-reader-marker; then marker=yes; fi
  printf 'SSH ROOT %s %s EXIT %s MARKER %s\n%s\n' "$kind" "$origin" "$status" "$marker" "$output"
  if [ "$origin" = material ]; then
   test "$status" != 0
   test "$marker" = no
   [[ "$output" == *'ConfOS: Permission denied for saved code input'* ]]
  else
   test "$marker" = yes
   if [ "$kind" = match ]; then test "$status" = 0; else test "$status" = 255; fi
  fi
 done
done
sudo rm -f /tmp/ssh-reader-marker
echo SSH_READER_ROOT_PRIVATE_MATRIX_PASS
ROOT_CONTROLS
