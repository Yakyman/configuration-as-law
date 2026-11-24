#!/bin/bash
# Prints the state of a server-side run every 20 results and once when it ends. Usage: watch-run.sh NAME
. "$(dirname "$0")/../local.env"
name=$1; last=""
while true; do
  s=$(ssh -o ConnectTimeout=10 "$SERVER" "systemctl --user is-active cases-$name; wc -l < $SERVER_DIR/runs/$name/results.tsv 2>/dev/null; cut -f3 $SERVER_DIR/runs/$name/results.tsv 2>/dev/null | sort | uniq -c | tr '\n' ' '" 2>/dev/null | tr '\n' ' ')
  case "$s" in
    active*) n=$(echo "$s" | awk '{print $2}')
      if [ -n "$n" ] && [ "$n" != "$last" ] && [ $(( n % 20 )) -eq 0 ]; then echo "$name running: $s"; fi; last=$n ;;
    "") ;;
    *) echo "$name ended: $s"; exit 0 ;;
  esac
  sleep 60
done
