date -u +%FT%TZ
guix system reconfigure /etc/config.scm > /tmp/g1-apply.log 2>&1; rc=$?
tail -n 25 /tmp/g1-apply.log
echo "guix system reconfigure exit=$rc"
date -u +%FT%TZ
