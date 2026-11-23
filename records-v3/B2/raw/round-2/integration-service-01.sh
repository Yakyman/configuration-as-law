#!/bin/sh
# Expected: the recorded native service starts in the generated boundary,
# MainPID has all uid/gid values 1000, and every candidate line verifies.
set -eu
python3 -B /usr/local/lib/stand/selftest.py add
/usr/bin/systemctl show stand-development.service -p MainPID -p User -p AppArmorProfile -p ExecStart
