for c in guix herd useradd usermod userdel groupadd gpasswd passwd ip iptables nft loginctl systemctl crontab; do printf '%s ' "$c"; command -v "$c" || echo ABSENT; done
sha256sum /etc/config.scm
guix --version | head -1
