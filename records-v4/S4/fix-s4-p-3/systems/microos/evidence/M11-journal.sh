#!/bin/sh
journalctl --no-pager --all -o cat --grep='grubenv|grub2-editenv|grub-editenv|saved_entry|next_entry'
