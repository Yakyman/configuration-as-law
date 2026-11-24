import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""Print rows of the server part filtered by kind (argv[1], comma list or 'small') with truncated members."""
import csv
import sys

csv.field_size_limit(10**9)
BASE = NIGHT_DIR + "A3/in/"
rows = list(csv.DictReader(open(BASE + "part-server.tsv"), delimiter="\t"))
BIG = {'2:stored-outside-packages', '1:firewall-ipv4', '1:firewall-rule', '1:firewall-chain', '1:firewall-ipv6',
       '2:executable-code-outside-packages', '1:process', '1:module-name', '1:port'}
sel = sys.argv[1]
width = int(sys.argv[2]) if len(sys.argv) > 2 else 300
for r in rows:
    k = r['kind']
    if sel == 'small':
        if k in BIG:
            continue
    elif k not in sel.split(','):
        continue
    print(r['id'], k, r['name'], r['members'][:width], r['evidence'][:120] if width > 300 else '', sep=' | ')
