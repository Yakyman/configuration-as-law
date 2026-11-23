#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y --no-install-recommends install python3 fapolicyd nftables network-manager bluez w3m ed gcc libc6-dev nodejs flatpak ostree squashfs-tools
systemctl disable --now apt-daily.timer apt-daily-upgrade.timer || true
systemctl disable --now fapolicyd.service || true
systemctl mask apt-daily.service apt-daily-upgrade.service
touch /etc/cloud/cloud-init.disabled
mkdir -p /usr/local/lib/stand /var/lib/stand/generations /opt/stand/pkgs /etc/stand /var/lib/stand/evidence
printf '%s\n' 'stand ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/stand
chmod 440 /etc/sudoers.d/stand
rm -f /etc/sudoers.d/90-cloud-init-users
printf '%s\n' 'PasswordAuthentication no' 'KbdInteractiveAuthentication no' > /etc/ssh/sshd_config.d/00-stand.conf
systemctl reload ssh
printf '%s\n' 'stand prototype bootstrap complete'
