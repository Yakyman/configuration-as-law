#!/usr/bin/python3
"""Run original private fault builder with PID-file trigger valid for either PID1."""
from pathlib import Path
import runpy

root = Path(__file__).resolve().parent
text = (root/'build-radio-fault-fixture-040.py').read_text()
old = "anchor='[ -f /run/confos-radio-ready.json ] || exec /bin/bash\\n'"
assert text.count(old) == 1
text = text.replace(old, "anchor='apparmor_parser -r /etc/confos/session.apparmor || exec /bin/bash\\n'")
old = ' kill -KILL "$radio_pid" || exit 1'
assert text.count(old) == 1
text = text.replace(old, ' radio_pid=$(cat /run/confos-radio.pid)\n'+old)
old = ' echo "RADIO TRUSTED FAULT INJECTED $radio_pid"'
assert text.count(old) == 1
text = text.replace(old, old+'''
 for fault_attempt in {1..20}; do
  if [ ! -e /run/confos-ready ] && [ ! -e /run/confos-radio-ready.json ] && [ ! -e /run/confos-radio.pid ]; then
   echo 'RADIO TRUSTED READINESS FILES REVOKED'
   exit 0
  fi
  sleep 1
 done
 echo 'RADIO TRUSTED READINESS REVOCATION FAILED'
''')
# Keep the existing isolated build procedure; save exact derivative recipe.
recipe = root/'radio-lifecycle-fault-recipe.py'
recipe.write_text(text)
runpy.run_path(str(recipe), run_name='__main__')
