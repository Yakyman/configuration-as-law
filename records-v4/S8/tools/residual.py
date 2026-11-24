#!/usr/bin/env python3
"""Print the changed unclaimed entries of a summary outside runtime (/run) and the declaration machinery."""
import json
import sys

SKIP = ('/run/', '/var/' + 'lib/stand-fs/', '/var/' + 'lib/stand/generations')
s = json.load(open(sys.argv[1]))
for e in s['unclaimed_changed_outside_code_root_copies']:
    if not e['path'].startswith(SKIP):
        print(e['path'], e['kind'], 'exec' if e['executable_bit'] else '', 'dpkg-member' if e['dpkg_member_of'] else '')
