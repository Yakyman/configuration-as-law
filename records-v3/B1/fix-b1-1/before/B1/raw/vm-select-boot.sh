#!/bin/sh
set -eu
# The cloud image's metapackage may install a cloud flavor too; select the target explicitly.
grep -F "menuentry 'Debian GNU/Linux, with Linux 7.3.4+deb13-amd64'" /boot/grub/grub.cfg
grub-reboot 'Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 7.3.4+deb13-amd64'
printf 'BOOT_SELECTED\n'
systemctl reboot
