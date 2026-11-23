#!/bin/sh
export LC_ALL=C
printf 'UTC='; date -u +%FT%TZ
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
nixos-rebuild switch
apply_rc=$?
printf 'APPLICATION_EXIT=%s\n' "$apply_rc"
[ "$apply_rc" = 0 ] || exit "$apply_rc"
printf 'before='; getent passwd user | cut -d: -f1,3,4
usermod -g wheel user
change_rc=$?
printf 'USERMOD_EXIT=%s\n' "$change_rc"
printf 'after='; getent passwd user | cut -d: -f1,3,4
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
usermod -g users user
printf 'CLEANUP_EXIT=%s\n' "$?"
printf 'UTC='; date -u +%FT%TZ
