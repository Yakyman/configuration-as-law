import csv, collections, sys
def rows(p):
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))
inp, out, done = sys.argv[1:4]
i = rows(inp); o = rows(out)
ii = [r['id'] for r in i]; oo = [r['id'] for r in o]
assert sorted(ii) == sorted(oo), 'id sets differ'
assert len(set(oo)) == len(oo), 'duplicate ids'
assert all(r['decision'] in {'MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED'} for r in o), 'bad decision'
with open(out, encoding='utf-8') as f:
    assert f.readline() == 'id\tdecision\tsentences\twhat_it_does\tbasis\treason\n', 'bad header'
c = collections.Counter(r['decision'] for r in o)
with open(done, 'w') as f:
    f.write(f"rows {len(o)} (input rows {len(i)})\n")
    for k in ['MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED']:
        f.write(f"{k} {c.get(k, 0)}\n")
print(open(done).read())
