#!/usr/bin/env python3
"""[f6]: every P4-S row that tools/make-search-cases.py writes (ROWS.md) is a row of CASES.md, in the same order.
usage: check-search-rows.py ROWS.md CASES.md   (exit 0 when they are)"""
import sys

rows = [l for l in open(sys.argv[1], encoding='utf-8').read().splitlines() if l.startswith('| P4-S-')]
md = open(sys.argv[2], encoding='utf-8').read().splitlines()
pos = [md.index(r) if r in md else -1 for r in rows]
ok = bool(rows) and -1 not in pos and pos == sorted(pos)
print(f'{len(rows)} rows, ' + ('all in CASES.md in order' if ok else 'NOT all in CASES.md in order'))
sys.exit(0 if ok else 1)
