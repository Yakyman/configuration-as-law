date -u +%FT%TZ
echo "== kernel params"; cat /proc/cmdline
echo "== time zone"; readlink -f /etc/localtime; date +%Z
echo "== locale"; cat /etc/locale.conf 2>/dev/null; grep -o 'LANG=[^ ]*' /etc/profiles/../set-environment 2>/dev/null | head -1; locale 2>/dev/null | head -1
echo "== dhcp"; systemctl is-enabled dhcpcd.service; systemctl is-active dhcpcd.service; ip -4 -o addr show | awk '{print $2, $4}'
echo "== account"; getent passwd user; id user; getent group wheel
echo "== root fs"; findmnt -n -o SOURCE,FSTYPE /; ls -l /dev/disk/by-uuid/ | grep 57eb3ffe
echo "== swap"; swapon --show; echo "swap lines=$(swapon --show --noheadings | wc -l)"
echo "== grub mbr"; dd if=/dev/vda bs=512 count=1 2>/dev/null | grep -a -c GRUB
echo "== platform"; uname -m
echo "== generation"; readlink /nix/var/nix/profiles/system; readlink /run/current-system; readlink /run/booted-system
