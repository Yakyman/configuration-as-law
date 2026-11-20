#!/bin/bash
set -u
agent_dir=$(mktemp -d)
mkfifo "$agent_dir/ready"
pkttyagent --process "$$" --notify-fd 3 3>"$agent_dir/ready" &
agent=$!
trap 'kill "$agent" 2>/dev/null; wait "$agent" 2>/dev/null; rm -rf "$agent_dir"' EXIT
read -r ignored <"$agent_dir/ready" || true
pkexec --disable-internal-agent /usr/bin/python3 /usr/local/lib/e2/probe.py polkit-external-agent
rc=$?
exit "$rc"
