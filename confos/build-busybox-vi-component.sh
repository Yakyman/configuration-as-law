#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash build-busybox-vi.sh
python3 package-busybox-vi-readers.py "${1:-$(cat VERSION)}"
