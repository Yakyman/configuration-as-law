"""Round 2: changed card dispositions, C3 scope, and C7 content evidence only.

Run: /usr/bin/python3 -I A3/fix-a3-h-2/recompute.py
All outputs are exclusively created. No probe, VM, sample draw, or input edit.
"""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
used = {}


def data(name):
    b = (ROOT / name).read_bytes()
    used[str(name)] = hashlib.sha256(b).hexdigest()
    return b


def read(name):
    return list(csv.DictReader(data(name).decode().splitlines(), delimiter='\t', quoting=csv.QUOTE_NONE))


def write(name, rows):
    with (OUT / name).open('x') as f:
        w = csv.DictWriter(f, list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


joined = read('A3/compare/joined.tsv')
adjudicated = {r['id']: r for r in read('A3/adjudication/rows.tsv')}
scope = read('A3/fix-a3-h-1/gap-scope.tsv')
for r in scope:
    if r['card'] == 'C6' and r['review_status'] == 'CONFIRMED':
        r['reason'] += ' configuration-origin.tsv says created=unknown for this member too; generation is a documentation-based inference, not a measured provenance fact. Confirmed count is a lower bound.'
        r['evidence'] += '; A3/in/raw/developer/configuration-origin.tsv; A3/fix-a3-h-1/raw/documentation.md'

# Whole joined table, both kind and name, including agreements and resolutions.
pattern = re.compile(r'/(?:var/lib/(?:docker|containerd|rancher/k3s/agent/containerd|kubelet/pods)|run/k3s/containerd)(?:/|$)')
candidates = []
for r in joined:
    if not (any(t in r['kind'] for t in ('docker', 'container', 'image')) or pattern.search(r['name']) or adjudicated.get(r['id'], {}).get('hole') == '3'):
        continue
    if r['kind'] == '1:docker-image':
        status = 'CONFIRMED'
        reason = 'Stored Docker image identity is established; whether documented build/pull/deploy/remove operations count as installation under S8.1-4/6 is a reading question, not a missing inventory fact.'
    elif r['kind'] == '1:docker-container':
        status = 'EXCLUDED'
        reason = 'Running process aspect follows S8.2-5/22, not a separate image. This does not certify the lifetime or class of stored container metadata.'
    elif r['name'] == '/home/user/.local/share/flatpak':
        status = 'EXCLUDED'
        reason = 'Flatpak deployment store, not the Docker engine image-installation case.'
    else:
        status = 'FACT_UNKNOWN'
        reason = 'Unexpanded store: member identities, image membership, received state and runtime-only versus persistent contents are unavailable; the whole directory is not promoted to a Docker image.'
    entry = dict(card='C3', id=r['id'], machine=r['machine'], kind=r['kind'], name=r['name'],
                 input_verdict=adjudicated.get(r['id'], {}).get('verdict', 'AGREED:'+r['c1_decision']),
                 review_status=status, reason=reason, evidence=r['evidence']+'; A3/fix-a3-h-2/raw/documentation.md')
    candidates.append(entry)
scope.extend(candidates)
write('gap-scope.tsv', scope)

cache = read('A3/fix-a3-h-1/cache-card.tsv')
for r in cache:
    if r['family'] in ('Go', 'Bun'):
        r['card_disposition'] = 'FACT-WRONG'
write('cache-card.tsv', cache)

# Recover literal here-doc bytes without executing any action script.
specs = [
    ('developer-e56b4f802a20335d455ecb3a', 'C1/actions/lived-developer.sh', "cat > lefthook.yml <<'EOF'", 'EOF', 'lefthook.yml'),
    ('developer-d916e8927ebf41371ab8dd1d', 'C1/actions/lived-developer.sh', "cat > Dockerfile <<'EOF'", 'EOF', 'Dockerfile'),
    ('server-c354536d6d9a738329571706', 'C1/actions/lived-server.sh', 'cat > "$work/cal-maintenance" <<\'CRON\'', 'CRON', 'cal-maintenance'),
]
published = {r['path']: r for r in read('A3/in/input-verification.tsv')}
content_checks = []
for rid, source, start, end, member in specs:
    b = data(source)
    expected = published[source.removeprefix('C1/')]['expected_sha256']
    assert hashlib.sha256(b).hexdigest() == expected
    lines = b.decode().splitlines(keepends=True)
    first = next(i for i, line in enumerate(lines) if line.strip() == start) + 1
    last = next(i for i in range(first, len(lines)) if lines[i].strip() == end)
    payload = ''.join(lines[first:last]).encode()
    machine, shortid = rid.split('-', 1)
    table = f'A3/in/raw/{machine}/members/{shortid}.tsv'
    match = next(r for r in read(table) if r['path'].endswith('/'+member))
    signature = 'sha256-prefix4096:'+hashlib.sha256(payload[:4096]).hexdigest()
    assert int(match['size']) == len(payload) and match['signature'] == signature
    with (OUT/'raw'/member).open('xb') as f:
        f.write(payload)
    content_checks.append(dict(id=rid, member=match['path'], source=source,
                               content_lines=f'{first+1}-{last}', script_sha256=expected,
                               bytes=len(payload), sha256_prefix4096=signature,
                               member_table=table, match='PASS'))
write('content-evidence.tsv', content_checks)

# Impact intersection only; do not redraw or re-audit the unchanged samples.
changed_ids = {r['id'] for r in cache if r['family'] in ('Go','Bun')}
changed_ids.update(r['id'] for r in candidates if r['review_status']=='CONFIRMED')
intersections = {}
for name in ('sample-resolved.tsv', 'sample-agreed.tsv'):
    intersections[name] = sorted(changed_ids & {r['id'] for r in read('A3/review/'+name)})
assert not any(intersections.values())

summary = dict(
    c3_search='All joined rows: kind contains docker/container/image OR engine-store path OR original hole 3; no classification filter.',
    c3_scope=[dict(status=s, machine=m, rows=n) for (s,m),n in sorted(Counter((r['review_status'],r['machine']) for r in candidates).items())],
    c3_original=[dict(status=s, rows=n) for s,n in sorted(Counter(r['review_status'] for r in candidates if adjudicated.get(r['id'],{}).get('hole')=='3').items())],
    card4=[dict(family=f, disposition=d, rows=n) for (f,d),n in sorted(Counter((r['family'],r['card_disposition']) for r in cache).items())],
    c6_extent='Lower bound: developer 2, gaming 0, server 0; 23 original candidate groups remain FACT_UNKNOWN.',
    content_checks=len(content_checks), sample_impacts=intersections,
)
with (OUT/'raw/recompute.json').open('x') as f:
    json.dump(summary,f,indent=2)
    f.write('\n')
with (OUT/'raw/consumed-inputs.sha256').open('x') as f:
    for path, digest in sorted(used.items()):
        f.write(digest+'  '+path+'\n')
print(json.dumps(summary,indent=2))
