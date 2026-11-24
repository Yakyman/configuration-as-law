#!/bin/sh
journalctl --no-pager --all -o cat --grep='sudoers|visudo|sudo-access'
