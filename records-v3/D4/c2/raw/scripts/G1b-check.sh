date -u +%FT%TZ
echo "== host name"; cat /proc/sys/kernel/hostname
echo "== time zone"; readlink -f /etc/localtime; date +%Z; echo "TZ=$TZ"
echo "== locale"; echo "LANG=$LANG"; grep -h -o 'LANG=[^ ]*' /etc/profile 2>/dev/null | head -2
echo "== kernel params"; cat /proc/cmdline
echo "== grub mbr"; dd if=/dev/vda bs=512 count=1 2>/dev/null | grep -a -c GRUB
echo "== root fs"; grep ' / ' /proc/mounts; ls -l /dev/disk/by-label/ 2>/dev/null | grep root; blkid -s LABEL -s TYPE /dev/vda1 2>/dev/null
echo "== account"; getent passwd user; id user; getent group wheel netdev users
echo "== password hash equal to declared"; [ "$(getent shadow user | cut -d: -f2)" = '$6$cal1122$ZIs03fvnBPSkasZ1B2RLSUt5dtUPGWVefzUbzC/CFnMSXK4xzJO5MQW1e3hyUIucJpFf/YLlootGG36zQ6EqB0' ] && echo equal || echo different
echo "== services"; herd status 2>&1 | head -60
echo "== dhcp address"; ip -4 -o addr show | awk '{print $2, $4}'
echo "== generation"; readlink /var/guix/profiles/system; readlink /run/current-system; readlink /run/booted-system
