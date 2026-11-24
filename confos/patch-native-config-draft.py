#!/usr/bin/python3
"""Unintegrated draft: protect native configuration stores, preserving reads.

Only writes a new output directory; package/guest tests are still required.
"""
from pathlib import Path
import sys

def patched(text):
    anchor = '  /var/** rwkl,\n'
    assert text.count(anchor) == 1
    rules = ''.join('  deny '+prefix+path+'{,/**} wkl,\n'
                    for prefix in ('', '/run/host', '/proc/*/root')
                    for path in ('/var/lib/dpkg', '/var/lib/apt', '/var/spool/cron'))
    return text.replace(anchor, anchor+rules)

if __name__ == '__main__':
    source, output = map(Path, sys.argv[1:])
    prepared = {name: patched((source/name).read_text())
                for name in ('assemble.py', 'flatpak-profile.apparmor')}
    output.mkdir()
    for name, content in prepared.items():
        (output/name).write_text(content)
    print('NATIVE CONFIGURATION STORE DENIAL DRAFT; NO GUEST RESULT')
