#!/bin/sh
command -v ausearch || exit 127
ausearch --input-logs --file /etc/sudoers --interpret; printf "query_exit=%s\n" "$?"
ausearch --input-logs --file /etc/sudoers.d --interpret; printf "query_exit=%s\n" "$?"
ausearch --input-logs --file /usr/etc/sudoers --interpret; printf "query_exit=%s\n" "$?"
