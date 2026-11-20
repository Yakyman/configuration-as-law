#!/bin/bash
set -euxo pipefail
mkdir -p /srv/cal-web/python-package /srv/cal-web/node-package
printf 'from setuptools import setup\nsetup(name="cal-probe",version="1.0",py_modules=["calprobe"])\n' >/srv/cal-web/python-package/setup.py
printf 'print("PYTHON_PACKAGE_EXECUTED")\n' >/srv/cal-web/python-package/calprobe.py
printf '{"name":"cal-probe","version":"1.0.0","bin":{"cal-probe":"index.js"}}\n' >/srv/cal-web/node-package/package.json
printf '#!/usr/bin/node\nconsole.log("NODE_PACKAGE_EXECUTED");\n' >/srv/cal-web/node-package/index.js
mkdir -p /root/flatpak-app/files/bin
cp /srv/cal-web/downloaded /root/flatpak-app/files/bin/cal-probe
printf '[Application]\nname=org.cal.Probe\nruntime=org.freedesktop.Platform/x86_64/23.08\ncommand=cal-probe\n' >/root/flatpak-app/metadata
flatpak build-finish /root/flatpak-app
flatpak build-export /root/flatpak-repo /root/flatpak-app
flatpak build-bundle /root/flatpak-repo /srv/cal-web/probe.flatpak org.cal.Probe master
dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\n' | sort >/etc/cal/base-packages.tsv
systemctl list-unit-files --no-pager --no-legend >/etc/cal/base-units.txt
getent passwd >/etc/cal/base-accounts.txt
getent group >/etc/cal/base-groups.txt
uname -r >/etc/cal/base-kernel.txt
sha256sum /usr/local/sbin/cald /usr/local/lib/cal/apply-policy /usr/local/bin/cal-login /usr/local/bin/calctl /usr/local/lib/cal/worker /opt/cal-packages/*.deb >/etc/cal/base-artifacts.sha256
systemctl stop cald
rm -rf /var/lib/cal
rm -f /run/cal.sock
truncate -s 0 /etc/machine-id
rm -f /var/lib/dbus/machine-id
touch /etc/cloud/cloud-init.disabled
sync
poweroff
