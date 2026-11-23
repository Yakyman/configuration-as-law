date -u +%FT%TZ
echo "== before"; getent group wheel; id -nG user
gpasswd -d user wheel; echo "gpasswd -d exit=$?"
echo "== after removal, no application"; getent group wheel; id -nG user
sleep 30; echo "== 30 s later"; date -u +%FT%TZ; getent group wheel; id -nG user
gpasswd -a user wheel; echo "gpasswd -a exit=$?"
echo "== after restore"; getent group wheel; id -nG user
date -u +%FT%TZ
