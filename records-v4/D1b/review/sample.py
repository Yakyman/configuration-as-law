"""Review sample: notes of example ids cited in D1b/RESULT.md and the size of group G2.
Run from D1b/: /usr/bin/python3 -I review/sample.py
"""
import csv

csv.field_size_limit(10**9)
J = {r['id']: r for r in csv.DictReader(open('compare/joined.tsv'), delimiter='\t')}
R = {r['id']: r for r in csv.DictReader(open('adjudication/rows.tsv'), delimiter='\t')}


def status(i):
    if i in R:
        v = R[i]['verdict']
        return 'GAP' if v == 'GAP' else ('UNK' if v == 'UNKNOWN' else 'RES')
    return 'UNK' if J[i]['c1_decision'] == 'UNKNOWN' else 'RES'


g2 = [i for i, r in J.items() if r['machine'] == 'd1b-gentoo' and status(i) == 'UNK'
      and r['name'].startswith('/var/db/repos')]
print('gentoo UNK under /var/db/repos:', len(g2))
prof = [i for i in g2 if i in R and R[i]['note'].startswith('Profile values')]
print('  of which notes starting "Profile values":', len(prof))
v1 = [i for i, r in J.items() if r['machine'] == 'd1b-void' and status(i) == 'UNK' and i not in R]
print('void matching UNKNOWN outside adjudication:', len(v1))
for i in ['d1b-gentoo-4fdc4b1911980b52450bbf10', 'd1b-gentoo-d1a1869b5087cbcc4f6df688',
          'd1b-gentoo-d4bcdd8be82152fedbb1c210', 'd1b-void-14aecb121740cea2d41bda86',
          'd1b-gentoo-b92d06df7c2cb763db610d04', 'd1b-talos-3da20a4239d2bce2616f4852',
          'd1b-void-5933a7ab38ed2c6e261307b0', 'd1b-gentoo-2546496f6d830f0509d2db6c']:
    r = J[i]
    print('==', i, r['kind'], r['name'][:80], 'status', status(i))
    print('  c1', r['c1_decision'], '|', r['c1_reason'][:300])
    print('  c2', r['c2_decision'], '|', r['c2_reason'][:300])
    if i in R:
        print('  adj', R[i]['verdict'], R[i]['sentence_id'], '|', R[i]['note'][:400])
