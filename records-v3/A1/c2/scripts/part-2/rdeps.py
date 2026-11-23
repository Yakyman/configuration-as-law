"""Run on the server: for target packages, list installed packages (names.txt) whose Depends/Recommends name them."""
import re, sys
names = set(l.strip().split(':')[0] for l in open('names.txt') if l.strip())
targets = sys.argv[1:]
pk = None; deps = {}
for line in open('Packages', encoding='utf-8', errors='replace'):
    if line.startswith('Package: '):
        pk = line[9:].strip()
    elif pk in names and (line.startswith('Depends: ') or line.startswith('Pre-Depends: ') or line.startswith('Recommends: ')):
        kind = line.split(':')[0]
        for d in re.split(r'[,|]', line.split(':', 1)[1]):
            d = d.strip().split(' ')[0].split(':')[0]
            deps.setdefault(d, set()).add(pk + ('' if kind != 'Recommends' else '(R)'))
for t in targets:
    print(t, '<-', ' '.join(sorted(deps.get(t, []))))
