#!/usr/bin/env python3
"""List process rows of part-gaming with their executable's package and integrity."""
import collections, csv, json, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gcommon import IN, owner

ex = collections.Counter()
for x in csv.DictReader(open(IN + 'part-gaming.tsv'), delimiter='\t'):
    if x['kind'] == '1:process':
        e = json.loads(x['members'])['record'].split('\t')[1]
        ex[e] += 1
for e, n in sorted(ex.items()):
    print(n, e, owner(e))
