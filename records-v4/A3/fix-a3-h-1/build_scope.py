"""Recompute only changed review scopes and evidence-rule impacts; inputs are read-only.

Run from any directory. Outputs are exclusive-created beside this script.
No probes, new samples, inventory collection or classification reruns.
"""
from pathlib import Path
import csv
import re
import json
from collections import Counter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]

def read(path):
    with (ROOT / path).open() as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))

def write(name, fields, rows):
    with (OUT / name).open('x') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

J = read('A3/compare/joined.tsv')
R = {x['id']: x for x in read('A3/adjudication/rows.tsv')}
old = {(x['card'], x['id']): x for x in read('A3/review/gap-scope.tsv')}
scope = []

def add(card, x, status, reason, evidence=''):
    scope.append(dict(card=card, id=x['id'], machine=x['machine'], kind=x['kind'],
                      name=x['name'], input_verdict=R.get(x['id'], {}).get('verdict', 'AGREED:'+x['c1_decision']),
                      review_status=status, reason=reason, evidence=evidence))

c7_confirmed = {'server-c354536d6d9a738329571706',
                'developer-e56b4f802a20335d455ecb3a',
                'developer-d916e8927ebf41371ab8dd1d'}
member_pattern = re.compile(r'/(?:Dockerfile(?:\.[^/]*)?|[^/]*\.Dockerfile|lefthook(?:-local)?\.ya?ml|crontab)$', re.I)
member_search = []
for x in J:
    n, k, rid = x['name'], x['kind'], x['id']
    if k.startswith('2:') and '/.git' in n:
        inside = bool(re.search(r'/\.git(?:/(?:objects|refs)(?:/|$)|$)', n))
        status = 'CONFIRMED' if inside else 'EXCLUDED'
        reason = 'Fetched project objects/references; competing branches of S8.2-15.' if inside else 'Hooks reach Q2; operational metadata is not fetched history; .github substring matches are not .git.'
        if '/.git/objects/info' in n:
            status, reason = 'FACT_UNKNOWN', 'Commit-graph provenance (fetched or locally generated) and received-state membership are not established.'
        elif inside and '/Homebrew/.git' in n:
            status, reason = 'FACT_UNKNOWN', 'Homebrew documents self-installation/update/removal; Q1 cannot be skipped. Inventory lacks received-content comparison and per-member installation provenance.'
        add('C2', x, status, reason, 'raw documentation excerpts in raw/documentation.md; '+x['evidence'])
    if k.startswith('1:firewall') or (k.startswith('2:') and any(p in n for p in ['/etc/firewalld', '/system.control', '/.config/pulse', '/etc/rancher', '/var/lib/rancher'])):
        prev = old[('C6', rid)]
        status, reason = prev['review_status'], prev['reason']
        if n in ['/etc/firewalld/policies', '/etc/firewalld/zones']:
            status, reason = 'CONFIRMED', 'Documented runtime-generated Docker access-rule member: chosen-value condition versus categorical settings list. Other group members are not promoted.'
        elif '/.config/pulse' in n:
            status, reason = 'FACT_UNKNOWN', 'Cookie origin is unknown in configuration-origin.tsv; the S8.2-14 versus S8.2-11 reading choice is not used to infer origin.'
        add('C6', x, status, reason, x['evidence'])
    if not k.startswith('2:'):
        continue
    p = Path('A3/in/raw') / x['machine'] / 'members' / (rid.split('-', 1)[1]+'.tsv')
    hits = []
    if (ROOT / p).exists():
        for m in read(p):
            if member_pattern.search(m['path']) or '/etc/cron.d/' in m['path']:
                hits.append(m)
    # Search all joined row names and kinds as well as their immediate-member names.
    name_hit = bool(member_pattern.search(n) or n == '/etc/cron.d' or '/etc/cron.d/' in n)
    if hits or name_hit:
        for m in hits:
            member_search.append(dict(id=rid, member=m['path'], type=m['type'], executable=m['executable'], evidence=str(p)))
        status, reason = 'FACT_UNKNOWN', 'Candidate file name only: command-bearing contents/capability and any prior Q1 package membership/integrity are not established.'
        if rid in c7_confirmed:
            status, reason = 'CONFIRMED', 'Established command-bearing value file: scope of file executed as code versus parsed values is undecided. Ordinary siblings retain their classes.'
        elif hits and all(m['path'].endswith('/bin/crontab') for m in hits):
            status, reason = 'EXCLUDED', 'crontab executable tool, not a crontab value file; Q2 applies to the tool.'
        add('C7', x, status, reason, str(p))

write('gap-scope.tsv', list(scope[0]), scope)
write('command-file-members.tsv', list(member_search[0]), member_search)

ctime = []
cache = []
for x in J:
    r = R.get(x['id'], {})
    if r.get('verdict', '').startswith('RESOLVED:') and 'ctime' in r['note'].lower():
        ctime.append(dict(id=x['id'], machine=x['machine'], kind=x['kind'], name=x['name'],
                          input_verdict=r['verdict'], review_status='FACT_UNKNOWN', original_note=r['note'],
                          missing_fact='Received-content comparison for the relevant member(s); ctime alone does not establish identity or unchanged contents.'))
    if r.get('hole') == '4':
        n = x['name']
        group = 'Go' if '/.cal-modcache' in n else 'Bun' if '/.bun/' in n else 'uv' if '/uv/' in n else 'RubyGems'
        status = 'FACT-WRONG' if group == 'uv' else 'REFUTED' if group in ['Go', 'Bun'] else 'FACT_UNKNOWN'
        cache.append(dict(id=x['id'], machine=x['machine'], kind=x['kind'], name=n, family=group, card_disposition=status))
write('ctime-unknown.tsv', list(ctime[0]), ctime)
write('cache-card.tsv', list(cache[0]), cache)
summary = dict(
    scope=[dict(card=c, status=s, machine=m, rows=n) for (c,s,m),n in sorted(Counter((x['card'],x['review_status'],x['machine']) for x in scope).items())],
    ctime=dict(Counter(x['input_verdict'] for x in ctime)),
    cache=dict(Counter(x['family'] for x in cache)),
    c6_original=[dict(status=s, machine=m, rows=n) for (s,m),n in sorted(Counter((x['review_status'],x['machine']) for x in scope if x['card']=='C6' and R.get(x['id'],{}).get('hole')=='6').items())],
    command_file_rows=sum(x['card']=='C7' for x in scope),
)
with (OUT/'raw/recompute.json').open('x') as f:
    json.dump(summary, f, indent=2)
    f.write('\n')
print(json.dumps(summary, indent=2))
