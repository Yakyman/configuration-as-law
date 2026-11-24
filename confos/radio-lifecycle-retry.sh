#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/radio-lifecycle-retry-build.log 2>&1
python3 radio-lifecycle-retry.py
RADIO_PREBUILT=1 bash radio-lifecycle-private.sh
