#!/bin/sh
journalctl --no-pager --all -o cat --grep='systemctl|preset|enable|disable|symlink'
