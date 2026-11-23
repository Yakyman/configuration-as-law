for c in nixos-rebuild nix-env nix-shell nix-channel nix systemctl useradd usermod userdel groupadd gpasswd passwd iptables nft ip loginctl crontab; do printf '%s ' "$c"; command -v "$c" || echo ABSENT; done
sha256sum /etc/nixos/configuration.nix /etc/nixos/hardware-configuration.nix
nix-channel --list; echo "nix-channel rc=$?"
nixos-version
