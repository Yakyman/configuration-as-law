#!/usr/bin/env bash
set -eu
export LC_ALL=C
printf 'Supplementary read-only provenance capture: '; date -u --iso-8601=seconds
printf '\nStock skeleton comparisons\n'
for home in /home/guest /root; do
  for rel in .Xdefaults .bash_profile .guile .zprofile guix-home-config.scm .config/gdb/gdbinit .config/nano/nanorc; do
    if [ -f "$home/$rel" ] && [ -f "/etc/skel/$rel" ]; then
      sha256sum "$home/$rel" "/etc/skel/$rel"
      if cmp -s "$home/$rel" "/etc/skel/$rel"; then printf 'MATCH %s\n' "$home/$rel"; else printf 'DIFFER %s\n' "$home/$rel"; fi
    fi
  done
done
printf '\nSystem etc source comparisons\n'
for rel in hosts sudoers mtab ssl; do
  ls -ld "/etc/$rel" "/run/current-system/etc/$rel" 2>&1 || true
  [ ! -f "/etc/$rel" ] || cat "/etc/$rel"
  if [ -f "/etc/$rel" ] && [ -f "/run/current-system/etc/$rel" ]; then
    sha256sum "/etc/$rel" "/run/current-system/etc/$rel"
  fi
done
printf '\nProfile manifests\n'
cat /home/guest/.guix-profile/manifest
cat /home/guest/.guix-home/profile/manifest
printf '\nHome declaration snapshot\n'
cat /home/guest/.guix-home/configuration.scm
printf '\nBoot/current system\n'
readlink -f /run/booted-system /run/current-system
printf '\nNSS\n'
cat /etc/nsswitch.conf
