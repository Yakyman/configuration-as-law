"""Check of run.form_routes: which interpreter routes a file's own form names (R1, Q12)."""
import importlib.machinery
import sys
from pathlib import Path

R = importlib.machinery.SourceFileLoader('runmod', str(Path(__file__).resolve().parents[2] / 'run')).load_module()
cases = [('/home/person/f.sh', 'sleep 86410 &', 'bash', True), ('/home/person/f.py', 'import x', 'python3', True),
         ('/home/person/f.py', 'import x', 'bash', False), ('/run/user/1000/x/events.log', '{"a":1}', 'python3', False),
         ('/home/person/hooks/pre-commit', '#!/bin/sh', 'sh', True), ('/home/person/c', '#!/usr/bin/env python3', 'python3', True),
         ('/home/person/doc.txt', 'A text', 'awk', False), ('/home/person/.bashrc', '# x', 'source', True),
         ('/home/person/jq', '\x7fELF', 'loader', True), ('/home/person/Makefile', 'all:', 'make', True)]
bad = 0
for path, l1, route, want in cases:
    got = route in R.form_routes(path, l1)
    print(f'{"PASS" if got == want else "FAIL"} {path} {l1!r} {route}: {got}')
    bad += got != want
print('RESULT:', 'PASS' if not bad else 'FAIL')
sys.exit(1 if bad else 0)
