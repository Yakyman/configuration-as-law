#!/bin/bash
cd "$HOME/actions"
start=$(date +%s)
bash gentoo.sh
rc=$?
printf '%s\t%s\n' "$rc" "$(($(date +%s)-start))" > "$HOME/action-driver.status"
