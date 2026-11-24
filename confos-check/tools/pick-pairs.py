#!/usr/bin/env python3
"""Find in a Debian Packages file: two small packages sharing one non-base dependency (Removal, shared object)."""
import re, sys
pk = {}
cur = {}
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    if line == '\n':
        if 'Package' in cur:
            pk[cur['Package']] = cur
        cur = {}
        continue
    m = re.match(r'([A-Za-z-]+): (.*)', line)
    if m:
        cur[m.group(1)] = m.group(2).strip()
def deps(p):
    d = pk[p].get('Depends', '') + ',' + pk[p].get('Pre-Depends', '')
    return {x.split('|')[0].split('(')[0].split(':')[0].strip() for x in d.split(',') if x.strip()}
for want in sys.argv[2:]:
    a, b = want.split(',')
    if a in pk and b in pk:
        shared = deps(a) & deps(b)
        print(a, pk[a]['Version'], b, pk[b]['Version'], 'shared:', sorted(shared))
        for s in sorted(shared):
            if s in pk:
                print('  ', s, pk[s]['Version'], pk[s].get('Priority'), pk[s].get('Installed-Size'))
    else:
        print('missing', want)
