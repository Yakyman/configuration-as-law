#!/bin/sh
command -v ausearch || exit 127
ausearch --input-logs --file /etc/systemd/system --interpret; printf "query_exit=%s\n" "$?"
