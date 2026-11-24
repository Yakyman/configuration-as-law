import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""List stored-outside-packages group rows: id, name, count, complete, persistence summary, first members.
argv[1]: 'summary' | 'members' (print all members of rows whose name starts with argv[2])."""
import csv
import json
import sys
from collections import Counter

csv.field_size_limit(10**9)
NIGHT = NIGHT_DIR + "A3/in/"
ROOT = NIGHT + "raw/server/"
rows = list(csv.DictReader(open(NIGHT + "part-server.tsv"), delimiter="\t"))


def members(r):
    m = json.loads(r['members'])
    if 'file' not in m:
        return None, m
    t = list(csv.DictReader(open(ROOT + m['file']), delimiter="\t"))
    return t, m


mode = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else ''
total = 0
for r in rows:
    if r['kind'] != '2:stored-outside-packages':
        continue
    if not r['name'].startswith(prefix):
        continue
    t, m = members(r)
    if t is None:
        print(r['id'], r['name'], 'NOFILE', json.dumps(m)[:200])
        continue
    total += len(t)
    pers = Counter(x['persistence'] for x in t)
    if mode == 'summary':
        print(r['id'][7:], r['name'], m['count'], m['complete'], dict(pers), sep='\t')
    else:
        print('==', r['id'], r['name'], m['count'], m['complete'])
        for x in t:
            print('   ', x['path'], x['type'], x['mode'], x['owner'], x['size'], x['mtime'][:19], x['executable'],
                  x['persistence'], sep=' ')
print('TOTAL members', total, file=sys.stderr)
