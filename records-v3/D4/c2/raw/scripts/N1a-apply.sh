date -u +%FT%TZ
nixos-rebuild switch > /tmp/n1-apply.log 2>&1; rc=$?
tail -n 25 /tmp/n1-apply.log
echo "nixos-rebuild switch exit=$rc"
date -u +%FT%TZ
