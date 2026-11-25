#!/bin/bash
# Read the stored root of a built disk from outside (no ConfOS record used) and check
# where the installer and configuration commands are. Byte equality with the packages
# is checked by compare-native-entries.py on builds that keep their work folder.
set -euo pipefail
cd "$(dirname "$0")"
disk=${1:?usage: check-dtest-disk-049.sh DISK.qcow2}
source slots.sh
confos_reserve_guest
tmp=$(mktemp -d images/.dtest-disk.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
export LIBGUESTFS_BACKEND=direct
generation=$(guestfish --ro -a "$disk" run : mount-ro /dev/sda2 / : ls /generations | head -1)
test -n "$generation"
guestfish --ro -a "$disk" run : mount-ro /dev/sda2 / : copy-out "/generations/$generation/root.sqfs" "$tmp"
unsquashfs -ll "$tmp/root.sqfs" >"$tmp/list.txt"
if grep -q ' squashfs-root/usr/lib/confos/native' "$tmp/list.txt";then echo 'relocated executables present';exit 1;fi
for path in usr/bin/apt usr/bin/apt-get usr/bin/pip3 usr/bin/flatpak usr/bin/podman usr/bin/systemctl \
  usr/bin/hostnamectl usr/bin/timedatectl usr/sbin/sysctl usr/sbin/useradd usr/sbin/usermod usr/sbin/userdel usr/sbin/visudo;do
 line=$(grep " squashfs-root/$path\$" "$tmp/list.txt" || true)
 case "$line" in
  -*) echo "PASS regular file /$path";;
  *) echo "FAIL /$path: ${line:-absent}";exit 1;;
 esac
 name=${path##*/}
 grep -q " squashfs-root/usr/local/bin/$name -> /usr/lib/confos/commands/$name\$" "$tmp/list.txt" || { echo "FAIL no entry link for $name";exit 1; }
done
grep -q ' squashfs-root/usr/bin/npm -> ../share/nodejs/npm/bin/npm-cli.js$' "$tmp/list.txt"
echo 'PASS /usr/bin/npm is the package link'
echo "STORED ROOT OF GENERATION $generation: COMMAND PATHS PASS"
