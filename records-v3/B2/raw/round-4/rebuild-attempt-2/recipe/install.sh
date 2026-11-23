#!/bin/sh
set -eu
cd /usr/local/lib/stand
chmod 755 stand.py
for name in stand-apply stand-verify stand-compare stand-replay stand-pkg stand-line apt apt-get pip pip3 npm flatpak podman crontab systemd-run systemctl nmcli nft useradd usermod userdel groupadd groupdel bluetoothctl; do
  ln -sfn /usr/local/lib/stand/stand.py /usr/local/bin/"$name"
done
cat > /etc/systemd/system/stand-replay.service <<'EOF'
[Unit]
Description=Replay the last completed finite declaration
After=local-fs.target NetworkManager.service fapolicyd.service ssh.service
ConditionPathExists=/var/lib/stand/current
[Service]
Type=oneshot
ExecStart=/usr/local/bin/stand-replay
TimeoutStartSec=180
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable stand-replay.service fapolicyd.service
python3 -B -c 'import policy; print(policy.install_policy())'
fagenrules
python3 -B capture.py
fapolicyd-cli --delete-db
/usr/bin/systemctl start fapolicyd
stand-apply /etc/stand/factory
