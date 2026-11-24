#!/bin/sh
find /var/log/zypp /var/log/YaST2 /var/log/transactional-update /var/log/combustion /var/lib/combustion -type f -size -16M -exec grep -aEn -- 'NetworkManager|jeos-firstboot|mdcheck_continue|network.service' {} +
systemctl show dbus-org.freedesktop.nm-dispatcher.service jeos-firstboot.service network.service NetworkManager-dispatcher.service NetworkManager-wait-online.service NetworkManager.service mdcheck_continue.timer -p Id -p UnitFileState -p UnitFilePreset
rpm -q --scripts systemd NetworkManager mdadm jeos-firstboot
