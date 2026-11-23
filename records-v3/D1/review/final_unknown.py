import collections
import csv


def read(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t', quoting=csv.QUOTE_NONE))


joined = read('D1/compare/joined.tsv')
sources = {r['id']: r['source'] for r in read('D1/review/original-unknown.tsv')}
for r in read('D1/review/resolved-sample.tsv'):
    if r['review'] == 'NOT-ESTABLISHED':
        assert r['id'] not in sources
        sources[r['id']] = 'resolved sample: missing factual premise'
for r in read('D1/review/cards-1-4-extent.tsv'):
    if r['membership'] == 'UNKNOWN' and r['source_card'] in ('1', '2'):
        assert r['id'] not in sources
        sources[r['id']] = 'original card ' + r['source_card'] + ': whole-object facts unresolved'
for r in read('D1/review/card5-extent.tsv'):
    if r['original_card'] == '5' and r['extent_status'] == 'UNKNOWN':
        assert r['id'] not in sources
        sources[r['id']] = 'original card 5: whole-object facts unresolved'
assert len(sources) == 114
records = [dict(id=r['id'], machine=r['machine'], kind=r['kind'], name=r['name'], source=sources[r['id']])
           for r in joined if r['id'] in sources]
assert len(records) == 114
with open('D1/review/final-unknown.tsv', 'w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=['id', 'machine', 'kind', 'name', 'source'], delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
    writer.writeheader()
    writer.writerows(records)
print('Explicit review UNKNOWN:', len(records))
print('By machine:', dict(collections.Counter(r['machine'] for r in records)))
print('By kind:', dict(collections.Counter(r['kind'] for r in records)))
