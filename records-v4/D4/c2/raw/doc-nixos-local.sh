#!/bin/sh
# Reads installed official documentation (manual pages) of the exact release; no state change.
export MANWIDTH=110 PAGER=cat
echo "== nixos-rebuild(8): switch / boot / test"
man nixos-rebuild 2>/dev/null | col -b | awk '/^ +switch/{p=1} /^ +build-vm/{p=0} p' | head -n 40
echo "== configuration.nix(5): users.mutableUsers"
man configuration.nix 2>/dev/null | col -b | awk '/^ +users\.mutableUsers$/{p=1;n=0} p{print; if(++n>14) p=0}'
echo "== configuration.nix(5): users.users.<name>.initialPassword"
man configuration.nix 2>/dev/null | col -b | awk '/^ +users\.users\.<name>\.initialPassword$/{p=1;n=0} p{print; if(++n>14) p=0}'
echo "== configuration.nix(5): users.users.<name>.extraGroups"
man configuration.nix 2>/dev/null | col -b | awk '/^ +users\.users\.<name>\.extraGroups$/{p=1;n=0} p{print; if(++n>8) p=0}'
echo "== configuration.nix(5): environment.systemPackages"
man configuration.nix 2>/dev/null | col -b | awk '/^ +environment\.systemPackages$/{p=1;n=0} p{print; if(++n>12) p=0}'
echo "== nix-env(1) name/description"
man nix-env 2>/dev/null | col -b | sed -n '1,30p'
echo "== nix-env --install(1)"
man nix-env-install 2>/dev/null | col -b | sed -n '1,40p'
echo "== which useradd gpasswd nix-env nix"; command -v useradd gpasswd nix-env nix
