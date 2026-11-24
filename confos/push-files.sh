#!/bin/bash
# Copy the named source files to the build folder on the worker.
set -euo pipefail
cd "$(dirname "$0")"
source ./local.env
scp -q -r -F "$SSH_CONFIG" "$@" "$WORKER:$REMOTE_BUILD/"
