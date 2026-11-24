#!/usr/bin/env python3
"""Pick 10 rows per script rule (seeded) from a built output and print them with their members for hand checking."""
import csv, json, random, re, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from members_rules import classify, load_shebang
from system_groups import member_rule
csv.field_size_limit(10**9)
IN = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/'
out = {r['id']: r for r in csv.DictReader(open(sys.argv[1]), delimiter='\t')}
rows = list(csv.DictReader(open(IN + 'part-developer.tsv'), delimiter='\t'))
load_shebang(rows)
mem = collections.defaultdict(list)
for m in csv.DictReader(open('/tmp/c2dev/members.tsv'), delimiter='\t'):
    mem[m['gid']].append(m)

RULES = [
    ('R1 rpm packages by dnf reason', lambda x: x['name'].startswith('rpm:')),
    ('R2 npm packages under bun global', lambda x: x['name'].startswith('npm:')),
    ('R3 rpm-shipped gems', lambda x: x['name'].startswith('gem:') and 'lefthook' not in x['name']),
    ('R4 processes', lambda x: x['kind'] == '1:process'),
    ('R5 netfilter rows', lambda x: 'firewall' in x['kind']),
    ('R6 Julia package trees', lambda x: x['kind'].startswith('2:') and '/.julia/juliaup/julia-' in x['name']),
    ('R7 bun global packages', lambda x: x['kind'].startswith('2:') and '/.bun/install/global/node_modules/' in x['name']),
    ('R8 bun cache', lambda x: x['kind'].startswith('2:') and '/.bun/install/cache' in x['name']),
    ('R9 Homebrew checkout', lambda x: x['kind'].startswith('2:') and '/linuxbrew/.linuxbrew/Homebrew' in x['name']),
    ('R10 Homebrew prefix and Cellar', lambda x: x['kind'].startswith('2:') and re.search(r'linuxbrew/\.linuxbrew/(Cellar|share|var|opt|etc|bin|lib)', x['name'])),
    ('R11 scc project tree', lambda x: x['kind'].startswith('2:') and '/Projects/scc' in x['name'] and '.cal-modcache' not in x['name']),
    ('R12 Go module cache', lambda x: x['kind'].startswith('2:') and '.cal-modcache' in x['name']),
    ('R13 Go build cache', lambda x: x['kind'].startswith('2:') and '/.cache/go-build' in x['name']),
    ('R14 runtime trees', lambda x: x['kind'].startswith('2:') and re.match(r'/(run|tmp|var/tmp)', x['name'])),
    ('R15 /var/cache records', lambda x: x['kind'].startswith('2:') and x['name'].startswith('/var/cache')),
    ('R16 SELinux module store', lambda x: x['kind'].startswith('2:') and x['name'].startswith('/var/lib/selinux/targeted')),
]
random.seed(20261123)
for title, sel in RULES:
    cand = [x for x in rows if sel(x)]
    pick = random.sample(cand, min(10, len(cand)))
    print('=' * 10, title, len(cand), 'rows')
    for x in pick:
        o = out[x['id']]
        print(x['id'], '|', x['name'][-90:], '|', o['decision'], '|', o['reason'][:160])
        if x['kind'] == '2:stored-ownership-unresolved':
            for m in mem[x['id']][:4]:
                r = classify(m) if x['name'].startswith('/home') else member_rule(x['name'], m)
                print('     ', m['path'][-70:], m['type'], m['exec'], m['ctime'][:19], '->', r[0])
