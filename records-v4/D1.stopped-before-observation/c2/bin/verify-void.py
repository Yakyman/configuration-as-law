import csv, sys
from collections import Counter

inp_path, out_path, done_path = sys.argv[1:4]
inp = list(csv.reader(open(inp_path, encoding='utf-8'), delimiter='\t'))
out = list(csv.reader(open(out_path, encoding='utf-8'), delimiter='\t'))
assert out[0] == ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason'], out[0]
ii = [r[0] for r in inp[1:]]
oo = [r[0] for r in out[1:]]
assert sorted(ii) == sorted(oo), 'id sets differ'
assert len(oo) == len(set(oo)), 'duplicate ids'
W = ['INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED', 'PROGRAM-OWN', 'PROGRAM-DERIVED',
     'SETTING-OWN', 'SETTING-DEFAULT', 'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE',
     'GAP-TWO', 'UNKNOWN', 'MIXED']
c = Counter(r[1] for r in out[1:])
assert set(c) <= set(W), set(c) - set(W)
with open(done_path, 'w', encoding='utf-8') as f:
    f.write(f"rows\t{len(oo)}\tinput rows {len(ii)}; input is header-only, inventory not run\n")
    for w in W:
        f.write(f"{w}\t{c.get(w, 0)}\n")
print(open(done_path, encoding='utf-8').read())
