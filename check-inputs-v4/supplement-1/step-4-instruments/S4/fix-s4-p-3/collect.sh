#!/bin/sh
# Host-side entry point for the fixed collector with the added event adapter.
collector_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
: "${LAB_ROOT:=$(CDPATH= cd -- "$collector_root/../.." && pwd)}"
export LAB_ROOT
exec python3 "$collector_root/assembled-main.py" "$@"
