#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
python3 -B selftest/test_checks.py
python3 -B selftest/test_cli.py
python3 -B selftest/test_payloads.py
python3 -B run --validate
python3 -B tools/check_catalogue.py
printf 'SELFTEST PASS (fixtures only; no operating-system run)\n'
