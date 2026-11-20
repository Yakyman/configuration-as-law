#!/usr/bin/env bash
set -euxo pipefail
id
date -u --iso-8601=seconds
sudo cloud-init status --wait
sudo apt-get update
sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y jq
mkdir -p "$HOME/Documents" "$HOME/.config/nano"
printf 'set tabsize 4\n' > "$HOME/.nanorc"
printf '# A day of work\n\nPrepared a short inventory note and reviewed a JSON task list.\n' > "$HOME/Documents/day-note.md"
printf '{"tasks":["write note","review configuration"]}\n' > "$HOME/Documents/tasks.json"
jq '.tasks[]' "$HOME/Documents/tasks.json"
sudo loginctl enable-linger census
date -u --iso-8601=seconds
sleep 120
date -u --iso-8601=seconds
