#!/bin/bash
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
python3 - <<'PY'
import json,subprocess
d=json.load(open('/root/e4/declaration.json'))
subprocess.run(['apt-get','install','-y','--no-install-recommends',*d['packages']],check=True)
PY
mkdir -p /srv/e4 /etc/NetworkManager/conf.d
cat >/etc/NetworkManager/conf.d/90-e4.conf <<'EOF'
[keyfile]
unmanaged-devices=interface-name:ens3
[main]
no-auto-default=*
EOF
systemctl restart NetworkManager
cat >/etc/systemd/system/e4-web.service <<'EOF'
[Unit]
Description=E4 local browser fixture
[Service]
ExecStart=/usr/bin/python3 /root/e4/web.py
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now e4-web redis-server postgresql
dpkg-query -W -f='${Package}\t${Version}\n' network-manager openssh-server chromium chromium-driver redis-server postgresql-15 systemd
sha256sum /root/e4/declaration.json
date -Is
touch /root/e4/APPLIED
