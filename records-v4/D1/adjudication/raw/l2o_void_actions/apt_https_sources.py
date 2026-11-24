#!/usr/bin/env python3
"""Use HTTPS for the same official APT coordinates in temporary action inputs."""
# https://manpages.ubuntu.com/manpages/noble/man1/apt-transport-https.1.html
# https://manpages.debian.org/trixie/apt/apt.conf.5.en.html
from pathlib import Path
import re
import sys

source = Path('/etc/apt')
target = Path.home() / '.cal-rehearsal-actions' / 'apt-https'
if not (target / '.complete').is_file():
    (target / 'sources.list.d').mkdir(parents=True, mode=0o700, exist_ok=True)
    target.chmod(0o700)
    inputs = [(source / 'sources.list', target / 'sources.list')]
    inputs += [(path, target / 'sources.list.d' / path.name)
               for path in sorted((source / 'sources.list.d').glob('*'))
               if path.suffix in ('.list', '.sources') and path.is_file()]
    replacements = 0
    pattern = re.compile(r'http://((?:[A-Za-z0-9-]+\.)*ubuntu\.com)(?=/)')
    for original, output in inputs:
        value = original.read_text() if original.is_file() else ''
        value, count = pattern.subn(r'https://\1', value)
        replacements += count
        output.write_text(value)
        output.chmod(0o600)
    (target / '.complete').write_text('prepared\n')
    print(f'APT transport: {replacements} official source URL occurrences switched to HTTPS', file=sys.stderr)
print(target)
