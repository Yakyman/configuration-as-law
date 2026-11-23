#!/bin/sh
export LC_ALL=C
printf 'UTC='; date -u +%FT%TZ
nixos-version
nix --version
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
command -v nixos-rebuild nix-env useradd usermod
printf 'account uid/gid/shell: '; getent passwd user | cut -d: -f1,3,4,7
getent group users wheel | cut -d: -f1,3
printf 'mutableUsers='; nix-instantiate --eval '<nixpkgs/nixos>' -A config.users.mutableUsers
printf 'declared primary group='; nix-instantiate --eval '<nixpkgs/nixos>' -A config.users.users.user.group
MANWIDTH=80 man usermod | col -b | sed -n '/^NAME/,/^OPTIONS/p'
MANWIDTH=80 man usermod | col -b | sed -n '/-g, --gid/,/-G, --groups/p'
