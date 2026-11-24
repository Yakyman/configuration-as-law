#!/usr/bin/env python3
"""Find filesystem entries of the gaming inventory whose path contains any of the given substrings.
Prints path, type, target, ctime, persistence, package owner (aliases) and integrity. '@' stands for '/'."""
import json, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gcommon import RAW, owner

subs = [a.replace('@', '/') for a in sys.argv[1:]]
for line in open(RAW + 'raw/0004-filesystem.out', errors='replace'):
    if not any(s in line for s in subs):
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    p = d.get('path', '')
    if not any(s in p for s in subs):
        continue
    print(p, d.get('type'), d.get('target', ''), d.get('ctime', '')[:19], d.get('persistence'), owner(p), sep='\t')
