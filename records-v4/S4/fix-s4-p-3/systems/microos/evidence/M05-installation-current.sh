#!/bin/sh
find /var/log/zypp /var/log/YaST2 /var/log/transactional-update /var/log/combustion /var/lib/combustion -type f -size -16M -exec grep -aEn -- 'sudoers|visudo' {} +
rpm -q --scripts sudo
rpm -V sudo
for p in /etc/sudoers /usr/etc/sudoers /etc/sudoers.d/*; do test ! -f "$p" || sha256sum "$p"; done
