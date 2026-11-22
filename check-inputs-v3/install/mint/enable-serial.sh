#!/bin/sh
# Installation instrument only; run after console login as user.
printf 'cal-test\n' | sudo -S -p '' sh -c 'printf '\''GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8"\n'\'' > /etc/default/grub.d/99-cal-console.cfg; update-grub >/dev/null 2>&1; systemctl enable --now serial-getty@ttyS0.service >/dev/null 2>&1'
printf 'serial-instrument-ready\n'
