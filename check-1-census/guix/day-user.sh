#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
set -x
date -u --iso-8601=seconds
id
cp /mnt/taskshare/home.scm "$HOME/home.scm"
guix home reconfigure "$HOME/home.scm" --cores=2 --max-jobs=1
sha256sum /etc/config.scm "$HOME/home.scm" > /tmp/w1-declarations-before.sha256
cat /tmp/w1-declarations-before.sha256
guix install hello --cores=2 --max-jobs=1
"$HOME/.guix-profile/bin/hello"
guix package --list-installed
guix package --export-manifest
printf 'set number\n' > "$HOME/.vimrc"
mkdir -p "$HOME/Documents"
printf '# Day note\nI installed hello, adjusted my editor, and prepared a work note.\n' > "$HOME/Documents/day-note.md"
sha256sum -c /tmp/w1-declarations-before.sha256
readlink -f "$HOME/.guix-profile"
readlink -f "$HOME/.guix-home"
cat "$HOME/.config/w1/declared-note"
date -u --iso-8601=seconds
echo USER_DAY_DONE
