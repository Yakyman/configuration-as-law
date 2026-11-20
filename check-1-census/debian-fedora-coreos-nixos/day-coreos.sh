#!/usr/bin/env bash
set -euxo pipefail
id
date -u --iso-8601=seconds
mkdir -p "$HOME/Documents"
printf 'export EDITOR=vi\n' > "$HOME/.bashrc"
printf '# Work note\n\nReview system logs and check available storage with tree.\n' > "$HOME/Documents/day-note.md"
sudo rpm-ostree install tree
rpm-ostree status
date -u --iso-8601=seconds
sudo systemctl reboot
