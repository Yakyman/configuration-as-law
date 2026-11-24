#!/usr/bin/env python3
"""Show members of stored groups whose name matches arguments (exact) or prefix with --prefix."""
import csv, json, sys

IN = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/'
args = sys.argv[1:]
prefix = False
maxn = 400
if args and args[0] == '--prefix':
    prefix = True
    args = args[1:]
if args and args[0].startswith('--max='):
    maxn = int(args[0][6:])
    args = args[1:]
csv.field_size_limit(10**9)
r = csv.DictReader(open(IN + 'part-developer.tsv'), delimiter='\t')
for x in r:
    if not x['kind'].startswith('2:stored'):
        continue
    n = x['name']
    if (n in args) or (prefix and any(n.startswith(a) for a in args)):
        m = json.loads(x['members'])
        print('###', n, x['id'], m.get('count'))
        for l in list(open(IN + 'raw/developer/' + m['file']))[1:maxn + 1]:
            f = l.rstrip('\n').split('\t')
            print('  ', f[0], f[1], f[2], f[3], f[4], f[5][:19], f[6], f[8])
