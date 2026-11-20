#!/usr/bin/env bash
set -euxo pipefail
id
date -u --iso-8601=seconds
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
nix-env -f /nix/var/nix/profiles/per-user/root/channels/nixos -iA hello
"$HOME/.nix-profile/bin/hello"
mkdir -p "$HOME/Documents"
printf 'set number\n' > "$HOME/.vimrc"
printf '# Work note\n\nInstalled and ran hello from my user profile. Reviewed editor settings.\n' > "$HOME/Documents/day-note.md"
nix-env -q --installed --out-path
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
sudo loginctl enable-linger census
date -u --iso-8601=seconds
sleep 120
date -u --iso-8601=seconds
