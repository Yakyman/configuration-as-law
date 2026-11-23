#!/bin/sh
# Host-side controller. No local-machine inventory mode is provided.
collector_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
: "${LAB_ROOT:=$(dirname -- "$collector_root")}"
export LAB_ROOT
exec python3 "$collector_root/collector/main.py" "$@"
