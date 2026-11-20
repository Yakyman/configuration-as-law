#!/bin/bash
set -euxo pipefail
cd /root/stand-src
install -d /etc/cal /usr/local/lib/cal
install -d /opt/cal-packages /srv/cal-web
cd /opt/cal-packages
apt-get download hello figlet
test -e /srv/cal-web/downloaded || cp /usr/bin/hello /srv/cal-web/downloaded
tar -C /srv/cal-web -czf /srv/cal-web/program.tar.gz downloaded
cd /root/stand-src
gcc -O2 -Wall -o /usr/local/bin/cal-login cal-login.c
gcc -O2 -Wall -o /usr/local/bin/calctl calctl.c
gcc -O2 -Wall -o /usr/local/lib/cal/worker worker.c
cp /usr/local/lib/cal/worker /usr/local/lib/cal/alpha
cp /usr/local/lib/cal/worker /usr/local/lib/cal/beta
install -m 755 cald.py /usr/local/sbin/cald
install -m 755 apply-policy.py /usr/local/lib/cal/apply-policy
groupadd -f calusers
for u in alice bob; do
 usermod -a -G calusers "$u"
 printf '{"programs":{}}\n' >"/home/$u/declaration.json"
 chown "$u:$u" "/home/$u/declaration.json"
done
printf '{"archive":"keep","programs":{},"policies":{},"allow_channels":{},"shared":{}}\n' >/etc/cal/root.json
cat >/etc/systemd/system/cald.service <<'EOF'
[Unit]
After=apparmor.service
[Service]
ExecStart=/usr/local/sbin/cald
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now cald
for i in {1..30}; do calctl status >/dev/null 2>&1 && break; sleep 1; done
calctl apply
for u in alice bob; do usermod -s /usr/local/bin/cal-login "$u"; done
systemctl disable --now cron
systemctl mask cron user@.service
printf 'root\n' >/etc/cron.allow
cat >/etc/systemd/system/cal-web.service <<'EOF'
[Service]
ExecStart=/usr/bin/python3 -m http.server 8080 --bind 127.0.0.1 --directory /srv/cal-web
[Install]
WantedBy=multi-user.target
EOF
printf '<html><body><h1>CAL browser fixture</h1></body></html>\n' >/srv/cal-web/index.html
systemctl daemon-reload
systemctl enable --now cal-web
systemctl disable --now apt-daily.timer apt-daily-upgrade.timer man-db.timer fstrim.timer
# All infrastructure and tool packages are a pinned base part of the declaration.
dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\n' | sort >/etc/cal/base-packages.tsv
sha256sum /etc/cal/base-packages.tsv >/etc/cal/base-packages.sha256
cat /sys/module/apparmor/parameters/enabled
aa-status
