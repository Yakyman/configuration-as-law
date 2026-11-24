#!/bin/sh
set -u
PATH=/run/current-system/profile/bin:/run/current-system/profile/sbin:$PATH
echo "== date"; date -u +%FT%TZ
echo "== release"; guix --version | head -n 1; readlink /run/current-system
echo "== declaration line"; f=/etc/config.scm; [ -r "$f" ] || f=/run/current-system/configuration.scm; echo "$f"; grep -n 'supplementary-groups' "$f"
echo "== id before"; id -nG user
echo "== gpasswd -d user wheel"; command -v gpasswd; gpasswd -d user wheel; echo "status=$?"
echo "== id after gpasswd"; id -nG user
echo "== restore"; gpasswd -a user wheel; echo "status=$?"; id -nG user
echo "== date"; date -u +%FT%TZ
