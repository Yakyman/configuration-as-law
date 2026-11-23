import sys, collections
names = {'PKG': 'R-PKG', 'KMOD': 'R-KMOD', 'SERVICE': 'R-SERVICE', 'PROC': 'R-PROC', 'ACCT': 'R-ACCT'}
by = collections.OrderedDict()
for l in open(sys.argv[1], encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) < 4 or p[1] == 'row':
        continue
    by.setdefault(p[1], []).append((p[0], p[2]))
for rule, items in by.items():
    label = names.get(rule, rule[:60])
    print(f'- `{label}` ({len(items)} rows): ' + ', '.join(f'{i} ({n[:28]})' for i, n in items[:10]))
