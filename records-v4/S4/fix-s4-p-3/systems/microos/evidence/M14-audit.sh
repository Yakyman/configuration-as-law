#!/bin/sh
command -v ausearch || exit 127
ausearch --input-logs --file /var/lib/ca-certificates/openssl --interpret; printf "query_exit=%s\n" "$?"
ausearch --input-logs --file /etc/pki/trust --interpret; printf "query_exit=%s\n" "$?"
