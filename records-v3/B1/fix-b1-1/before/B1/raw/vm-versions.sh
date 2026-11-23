#!/bin/sh
set -eu
date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
cat /etc/os-release
printf 'DEBIAN_POINT_RELEASE '
cat /etc/debian_version
uname -r
python3 --version
dpkg-query -W -f='${binary:Package}\t${Version}\n' base-files linux-base linux-image-7.3.4+deb13-amd64 systemd python3 python3.13 libpython3.13-minimal libc6
sha256sum /usr/bin/python3.13
printf 'SELECTED_KERNEL_CONFIG\n'
grep -E '^CONFIG_(SECURITY_SELINUX|DM_VERITY|CGROUPS|SECCOMP_FILTER|IMA|IMA_APPRAISE|EVM|SECURITY_IPE|SECURITY_LANDLOCK)=' /boot/config-7.3.4+deb13-amd64
