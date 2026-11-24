import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""Lookup: for each path argument, print owning package(s), integrity, and package reason.
Use 'grep:REGEX' to search package-files paths by regex."""
import csv
import json
import re
import sys

csv.field_size_limit(10**9)
ROOT = NIGHT_DIR + "A3/in/raw/server/"
objs = {r['id']: r for r in csv.DictReader(open(ROOT + "objects.tsv"), delimiter="\t")}
pf = list(csv.DictReader(open(ROOT + "package-files.tsv"), delimiter="\t"))
bypath = {}
for r in pf:
    bypath.setdefault(r['path'], []).append(r)


def desc(pid):
    o = objs.get(pid)
    if not o:
        return pid
    try:
        m = json.loads(o['members'])
    except Exception:
        m = {}
    return f"{o['name']}[{m.get('reason')}]"


for a in sys.argv[1:]:
    if a.startswith('grep:'):
        rx = re.compile(a[5:])
        for p, lst in bypath.items():
            if rx.search(p):
                for r in lst:
                    print(p, desc(r['package']), r['integrity'], sep='\t')
        continue
    lst = bypath.get(a)
    if not lst:
        print(a, 'NO-PACKAGE', sep='\t')
    for r in lst or []:
        print(a, desc(r['package']), r['integrity'], r['rule'][:60], sep='\t')
