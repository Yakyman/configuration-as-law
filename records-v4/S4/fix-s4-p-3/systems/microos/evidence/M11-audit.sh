#!/bin/sh
command -v ausearch || exit 127
ausearch --input-logs --file /boot/grub2/grubenv --interpret; printf "query_exit=%s\n" "$?"
