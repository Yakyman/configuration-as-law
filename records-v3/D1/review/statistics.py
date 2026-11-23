import csv
import collections
import hashlib
import json
from pathlib import Path


def read(path):
    with open(path, newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle, delimiter='\t', quoting=csv.QUOTE_NONE))


joined = read('D1/compare/joined.tsv')
adjudicated = read('D1/adjudication/rows.tsv')
adjudication = {r['id']: r for r in adjudicated}
stats = {}
unknown = []
for machine in ('fedora', 'tumbleweed', 'mint', 'flatcar', 'talos', 'TOTAL'):
    rows = [r for r in joined if machine == 'TOTAL' or r['machine'] == machine]
    n = len(rows)
    match = sum(r['c1_decision'] == r['c2_decision'] for r in rows)
    first = collections.Counter(r['c1_decision'] for r in rows)
    second = collections.Counter(r['c2_decision'] for r in rows)
    expected = sum(first[k] * second[k] for k in first) / n**2 if n else None
    adjud = [adjudication[r['id']] for r in rows if r['id'] in adjudication]
    undecided = [r for r in rows if (
        adjudication.get(r['id'], {}).get('verdict') == 'UNKNOWN'
        or (r['id'] not in adjudication and r['c1_decision'] == r['c2_decision'] == 'UNKNOWN'))]
    if machine != 'TOTAL':
        unknown.extend(dict(id=r['id'], machine=machine, kind=r['kind'], name=r['name'],
                            source='adjudication' if r['id'] in adjudication else 'agreed UNKNOWN')
                       for r in undecided)
    stats[machine] = dict(objects=n, matching=match, matching_share=match/n if n else None,
                          kappa=(match/n-expected)/(1-expected) if n and expected != 1 else None,
                          adjudicated=len(adjud), verdicts=dict(collections.Counter(r['verdict'] for r in adjud)),
                          unknown=len(undecided), unknown_kinds=dict(collections.Counter(r['kind'] for r in undecided)))

Path('D1/review/statistics.json').write_text(json.dumps(stats, indent=2)+'\n')
with open('D1/review/original-unknown.tsv', 'w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=['id', 'machine', 'kind', 'name', 'source'], delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
    writer.writeheader()
    writer.writerows(unknown)
hashes = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (
    'COMMON.md', 'TEXT.md', 'SENTENCES.md', 'D1/compare/STATS.md', 'D1/compare/joined.tsv',
    'D1/adjudication/HOLES.md', 'D1/adjudication/rows.tsv', 'D1/in/READY.md')}
Path('D1/review/input-sha256.json').write_text(json.dumps(hashes, indent=2)+'\n')
print(json.dumps(stats['TOTAL']))
