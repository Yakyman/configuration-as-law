import csv
import collections
import random


def read(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t', quoting=csv.QUOTE_NONE))


joined = read('D1/compare/joined.tsv')
adjudicated = read('D1/adjudication/rows.tsv')
ids = {r['id'] for r in adjudicated}
resolved_population = [r for r in adjudicated if r['verdict'].startswith('RESOLVED:')]
agreed_population = [r for r in joined if r['id'] not in ids and r['c1_decision'] == r['c2_decision']]
for name, population, seed, size in (
    ('resolved', resolved_population, 2026112201, 40),
    ('agreed', agreed_population, 2026112202, 60),
):
    expected = [r['id'] for r in random.Random(seed).sample(population, size)]
    sample = read(f'D1/review/{name}-sample.tsv')
    assert expected == [r['id'] for r in sample], name
    assert len(set(expected)) == size
    statuses = collections.Counter(r.get('review', r.get('assessment')) for r in sample)
    print(f'{name}: population {len(population)}, seed {seed}, {size} ordered ids verified; {dict(statuses)}')

assert sum(r['c1_decision'] == r['c2_decision'] for r in joined) == 15025
assert len(joined) == 16524 and len(adjudicated) == 1843
print('Inventory and comparison counts verified.')
