#!/bin/sh
set -eu
cd /usr/local/lib/stand
chmod 755 stand.py
for name in stand-apply stand-verify stand-inventory stand-compare stand-replay stand-pkg stand-line apt apt-get pip pip3 npm flatpak podman crontab systemd-run systemctl nmcli nft useradd usermod userdel groupadd groupdel bluetoothctl; do
  ln -sfn /usr/local/lib/stand/stand.py /usr/local/bin/"$name"
done
/usr/bin/systemctl disable --now fapolicyd || true
/usr/bin/systemctl mask fapolicyd
cat > /etc/systemd/system/stand-noexec.service <<'EOF'
[Unit]
Description=Native execution gate for writable data mounts
After=local-fs.target
Before=ssh.service stand-replay.service
[Service]
Type=oneshot
ExecStart=/usr/bin/python3 -B -c "import sys; sys.path.insert(0,'/usr/local/lib/stand'); import noexec; noexec.install_policy()"
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF
cat > /etc/systemd/system/stand-replay.service <<'EOF'
[Unit]
Description=Replay the last completed finite declaration
After=local-fs.target NetworkManager.service stand-noexec.service ssh.service systemd-resolved.service systemd-networkd.service
ConditionPathExists=/var/lib/stand/current
[Service]
Type=oneshot
ExecStart=/usr/local/bin/stand-replay
TimeoutStartSec=300
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable stand-replay.service stand-noexec.service
/usr/bin/systemctl start stand-noexec.service
/usr/bin/systemctl stop user@1000.service || true
python3 -B /tmp/install-bc3.py
python3 -B capture.py
stand-apply /etc/stand/factory
