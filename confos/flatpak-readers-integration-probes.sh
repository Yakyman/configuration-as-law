#!/bin/bash
set -euo pipefail
failures=0
ref=/usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08/df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c/files
objects=(
 /usr/lib/confos/flatpak/repo/objects/08/8ac0e78b5c58326c0b5f6f04ce48110e888e42c41f2ba6cf31f1589fdeb21b.file
 /usr/lib/confos/flatpak/repo/objects/9a/9a79a0a407476be156b7dd95932d9996782814a1cd7201be0d36bc3c3b636d.file
 /usr/lib/confos/flatpak/repo/objects/69/fbcba0a573b7b4570c7e2921656c1c257aef94d26051d4037bcd83a6579ffe.file
)
refuse() {
 local output status
 set +e
 output=$(timeout -k 2 20 "$@" 2>&1); status=$?
 set -e
 printf '\nALIAS/NAMESPACE COMMAND '; printf '%q ' "$@"; printf '\n%s\nEXIT %s\n' "$output" "$status"
 if [ "$status" = 0 ] || printf '%s\n' "$output" | grep -qx UNRECORDED-ALIAS-RAN || [[ "$output" != *denied* && "$output" != *permitted* && "$output" != *permission* && "$output" != *Permission* && "$output" != *'failed to map segment from shared object'* ]]; then failures=$((failures+1)); fi
}
cat /proc/self/attr/current
stat -c '%i %h %a %n' "$ref/bin/bash" "$ref/bin/python3.14" "$ref/lib/x86_64-linux-gnu/libpython3.14.so.1.0" "${objects[@]}"
sha256sum "$ref/bin/bash" "$ref/bin/python3.14" "$ref/lib/x86_64-linux-gnu/libpython3.14.so.1.0" "${objects[@]}"
for authority in user root; do
 prefix=(); [ "$authority" != root ] || prefix=(sudo -n)
 refuse "${prefix[@]}" "${objects[0]}" -c 'echo UNRECORDED-ALIAS-RAN'
 refuse "${prefix[@]}" "${objects[1]}" -c 'print("UNRECORDED-ALIAS-RAN")'
 for object in "${objects[@]:0:2}"; do
  refuse "${prefix[@]}" /lib64/ld-linux-x86-64.so.2 "$object" -c 'echo UNRECORDED-ALIAS-RAN'
 done
 refuse "${prefix[@]}" python3 -c 'import ctypes,sys; ctypes.CDLL(sys.argv[1]); print("UNRECORDED-ALIAS-RAN")' "${objects[2]}"
done
# In ordinary app view repository objects should not be bound. Preserve result
# as exposure evidence; absence is not an execution-policy refusal claim.
flatpak run --command=python3 io.mpv.Mpv -c 'import os,sys; print("APP ORIGINAL OBJECT EXPOSURE",[(p,os.path.exists(p)) for p in sys.argv[1:]])' "${objects[@]}"
flatpak run --command=python io.mpv.Mpv /home/user/bin/recorded-flatpak-python.py
flatpak run io.mpv.Mpv --version
# Native app Lua is deliberately still unpatched.
printf 'print("UNRECORDED-LUA-OPEN"); mp.commandv("quit", "0")\n' >/home/user/flatpak-open.lua
set +e
timeout -k 2 20 flatpak run --command=mpv io.mpv.Mpv --no-config --vo=null --ao=null --idle=yes --script=/home/user/flatpak-open.lua
echo "LUA DIAGNOSTIC EXIT $?"
set -e
command -v bwrap
command -v unshare
test -x /usr/bin/bwrap
test -x /usr/bin/unshare
printf 'echo UNRECORDED-ALIAS-RAN\n' >/home/user/ns-material.sh
cp /usr/bin/printf /home/user/ns-native
for authority in user root; do
 prefix=(); [ "$authority" != root ] || prefix=(sudo -n)
 for route in script native; do
  refuse "${prefix[@]}" bwrap --ro-bind / / --tmpfs /mnt --proc /proc /bin/bash -c '
   cat /proc/self/attr/current
   cp /home/user/ns-material.sh /mnt/material.sh
   cp /home/user/ns-native /mnt/native
   mount --bind /mnt /mnt
   mount -o remount,bind,ro /mnt
   if [ "$1" = script ]; then /bin/bash /mnt/material.sh; else /mnt/native "UNRECORDED-ALIAS-RAN\\n"; fi
  ' probe "$route"
  refuse "${prefix[@]}" unshare -rm /bin/bash -c '
   cat /proc/self/attr/current
   mount --make-rprivate /
   mount -t tmpfs tmpfs /mnt
   cp /home/user/ns-material.sh /mnt/material.sh
   cp /home/user/ns-native /mnt/native
   mount --bind /mnt /mnt
   mount -o remount,bind,ro /mnt
   if [ "$1" = script ]; then /bin/bash /mnt/material.sh; else /mnt/native "UNRECORDED-ALIAS-RAN\\n"; fi
  ' probe "$route"
 done
done
echo "ALIAS/NAMESPACE FAILURES $failures"
test "$failures" = 0
