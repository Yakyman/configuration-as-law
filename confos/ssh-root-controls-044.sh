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
