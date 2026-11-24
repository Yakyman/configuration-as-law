#!/usr/bin/env python3
"""Show members of stored groups of part-gaming. Args: [--prefix] [--max=N] names...
A leading '@' in a name stands for '/' (so that command lines need not contain system paths)."""
import csv, json, sys

IN = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/'
args = sys.argv[1:]
prefix = False
maxn = 60
while args and args[0].startswith('--'):
    if args[0] == '--prefix':
        prefix = True
    elif args[0].startswith('--max='):
        maxn = int(args[0][6:])
    args = args[1:]
args = [a.replace('@', '/') for a in args]
csv.field_size_limit(10**9)
for x in csv.DictReader(open(IN + 'part-gaming.tsv'), delimiter='\t'):
    if not x['kind'].startswith('2:stored'):
        continue
    n = x['name']
    if (n in args) or (prefix and any(n.startswith(a) for a in args)):
        m = json.loads(x['members'])
        print('###', n, x['id'], m.get('count'), m.get('complete'))
        for l in list(open(IN + 'raw/gaming/' + m['file']))[1:maxn + 1]:
            f = l.rstrip('\n').split('\t')
            print('  ', f[0], f[1], f[2], f[3], f[4], f[5][:19], f[6], f[7][:30], f[8] if len(f) > 8 else '')
