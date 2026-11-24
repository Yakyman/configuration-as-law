"""Review recount of D1b/RESULT.md numbers from compare/joined.tsv and adjudication/rows.tsv.
Run from D1b/: /usr/bin/python3 -I review/count.py
"""
import collections
import csv

csv.field_size_limit(10**9)
J = {r['id']: r for r in csv.DictReader(open('compare/joined.tsv'), delimiter='\t')}
R = {r['id']: r for r in csv.DictReader(open('adjudication/rows.tsv'), delimiter='\t')}
print('joined', len(J), 'adjudicated', len(R), 'all-adjudicated-in-joined', all(i in J for i in R))
print('verdict x machine')
for k, v in sorted(collections.Counter((J[i]['machine'], r['verdict']) for i, r in R.items()).items()):
    print(' ', k, v)
print('machines', collections.Counter(r['machine'] for r in J.values()))
st = collections.Counter()
kinds = collections.Counter()
for i, r in J.items():
    if i in R:
        v = R[i]['verdict']
        s = 'GAP' if v == 'GAP' else ('UNK' if v == 'UNKNOWN' else 'RES')
    else:
        if r['c1_decision'] != r['c2_decision']:
            print('NOT ADJUDICATED BUT DIFFERENT', i)
        s = 'UNK' if r['c1_decision'] == 'UNKNOWN' else ('GAP' if r['c1_decision'] == 'GAP-TWO' else 'RES')
    st[(r['machine'], s)] += 1
    if s == 'UNK':
        kinds[(r['machine'], r['kind'])] += 1
print('status x machine')
for k, v in sorted(st.items()):
    print(' ', k, v)
print('unknown kinds')
for k, v in sorted(kinds.items()):
    print(' ', k, v)
print('hole column', collections.Counter(r['hole'] for r in R.values()))
print('GAP rows')
for i, r in R.items():
    if r['verdict'] == 'GAP':
        print(' ', i, J[i]['c1_decision'], J[i]['c2_decision'], r['hole'], J[i]['name'][:70])
print('matched-MIXED adjudicated rows by verdict',
      collections.Counter(R[i]['verdict'] for i in R if J[i]['c1_decision'] == J[i]['c2_decision']))
