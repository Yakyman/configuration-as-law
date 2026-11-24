#!/usr/bin/env python3
"""Check which Wine-prefix code files have a file of the same basename, size and 4096-byte signature
under Wine's package directories (/usr/lib/*-linux-gnu/wine/*-windows/). Output: A3/c2/raw/gaming-wine-copies.tsv"""
import json, os, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gcommon import RAW, NIGHT

pre = '/home/user/Games/wine-tools/drive_c/'
pk, px = {}, []
for line in open(RAW + 'raw/0004-filesystem.out', errors='replace'):
    if '/wine/' not in line and pre not in line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    p = d.get('path', '')
    if d.get('type') != 'file':
        continue
    if p.startswith('/usr/lib/') and '/wine/' in p and '-windows/' in p:
        pk[(os.path.basename(p).lower(), d.get('size'), d.get('signature'))] = p
    elif p.startswith(pre):
        px.append((p, d.get('size'), d.get('signature')))
out = open(NIGHT + 'A3/c2/raw/gaming-wine-copies.tsv', 'w')
out.write('path\tmatch\n')
n = 0
for p, s, g in px:
    mt = pk.get((os.path.basename(p).lower(), s, g), '')
    out.write('%s\t%s\n' % (p, mt))
    n += bool(mt)
print('prefix files', len(px), 'matching package file', n)
