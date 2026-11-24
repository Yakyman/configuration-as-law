"""Apply only the two documented rules and explicitly listed individual decisions."""
import base64
import collections
import csv
import io
import json
from pathlib import Path
import tarfile

csv.field_size_limit(10000000)
BASE = Path(__file__).resolve().parents[2]
HANDOFF = BASE / 'D1b/handoff/void'
OUT = BASE / 'D1b/c1/part-void.tsv'
HEADER = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']

def table(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def decode(value):
    while isinstance(value, str):
        value = json.loads(value)
    return value

rows = table(BASE / 'D1b/in/part-void.tsv')
objects = table(HANDOFF / 'objects.tsv')
members = {}
for row in rows:
    meta = decode(row['members'])
    if 'file' in meta:
        listed = table(HANDOFF / meta['file'])
        assert meta['complete'] and len(listed) == meta['count']
        members[row['id']] = listed
    elif 'path' in meta:
        members[row['id']] = [meta]

npm = {r['path']: r for r in table(HANDOFF / 'npm-member-integrity.tsv')}
archives = {r['package_root']: r for r in table(HANDOFF / 'npm-archive-sources.tsv')}
packages = {}
for row in objects:
    if row['kind'] == 'package':
        meta = decode(row['members'])
        if meta.get('manager') == 'npm' and meta.get('location'):
            packages[meta['location']] = (row, meta)
old = collections.defaultdict(list)
for row in table(HANDOFF / 'old-package-member-integrity.tsv'):
    old[row['path']].append(row)
provided = collections.defaultdict(list)
for row in table(HANDOFF / 'package-files.tsv'):
    provided[row['path']].append(row)

archive_names = {}
for root, source in archives.items():
    assert source['status'] == 'verified-archive:lock-reference'
    for filename in source['evidence'].split(';'):
        for line in (HANDOFF / filename).read_text().splitlines():
            obj = json.loads(line)
            if obj.get('path') == source['cache'] and obj.get('status') == 'ok':
                with tarfile.open(fileobj=io.BytesIO(base64.b64decode(obj['data']))) as archive:
                    archive_names[root] = [m.name.removeprefix('package/').rstrip('/') for m in archive.getmembers()]
    assert root in archive_names

previous = table(OUT) if OUT.exists() else []
done = {r['id'] for r in previous}
assert len(done) == len(previous)
stream = OUT.open('a', encoding='utf-8', newline='')
writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
if not previous and OUT.stat().st_size == 0:
    writer.writerow(HEADER)
    stream.flush()

def append(row, decision, sentences, what, basis, reason):
    if row['id'] in done:
        return
    fields = [row['id'], decision, sentences, what, basis, reason]
    assert len(what.split()) <= 15 and len(reason.split()) <= 30
    assert all('\t' not in f and '\n' not in f for f in fields)
    writer.writerow(fields)
    stream.flush()
    done.add(row['id'])

# Explicit individual decisions: these rows contain installer-created dependency
# containers or actual dependency package roots, not just archive payload files.
individual_npm = {
    '1d3093e090ec37303afa298b': ('MIXED', 'cliui payload files and its dependency container', 'node_modules: RECORD, created by npm for dependencies; all five files: INSTALLED-PACKAGE, unchanged cliui archive payload.'),
    '891ba9e7d2557d2187c34f3e': ('MIXED', 'wrap-ansi payload files and its dependency container', 'node_modules: RECORD, created by npm for dependencies; all four files: INSTALLED-PACKAGE, unchanged wrap-ansi archive payload.'),
    'a397c6c5091c03df1faba489': ('MIXED', 'yargs payload and its dependency container', 'node_modules: RECORD, npm dependency container; remaining members: INSTALLED-PACKAGE, unchanged yargs files and archive payload directories.'),
    'a74472d9bb92730824ba2b8e': ('INSTALLED-DERIVED', 'Four nested npm dependency packages of cliui', 'All four members are installed dependency packages; their lock dependency relationships cover them through cliui and its requesting package.'),
    '2671e0c8194a80cfbd661158': ('INSTALLED-DERIVED', 'Four nested npm dependency packages of wrap-ansi', 'All four members are installed dependency packages; their lock dependency relationships cover them through wrap-ansi and its requesting package.'),
    '7d33ae31b2b79c994ad2c971': ('INSTALLED-DERIVED', 'Four nested npm dependency packages of yargs', 'All four members are installed dependency packages; their lock dependency relationships cover them through yargs and its requesting package.'),
}

for row in rows:
    raw_id = row['id'].removeprefix('d1b-void-')
    if '/.local/node_modules/' in row['name']:
        listed = members[row['id']]
        assert all(m['persistence'] == 'persistent' for m in listed)
        if raw_id in individual_npm:
            decision, what, reason = individual_npm[raw_id]
            if decision == 'INSTALLED-DERIVED':
                assert len(listed) == 4
                assert all(packages[m['path']][1]['reason'] == 'dependency' for m in listed)
            else:
                assert any(m['path'].endswith('/node_modules') for m in listed)
                for m in listed:
                    if m['type'] == 'file':
                        fact = npm[m['path']]
                        assert fact['status'] == 'equal' and fact['expected'] == fact['actual']
            append(row, decision, 'S8.1-6,S8.2-6,S8.2-7,S8.2-8,S8.2-15,S8.2-16', what,
                   'raw:D1b/handoff/void/npm-member-integrity.tsv', reason)
            continue
        for member in listed:
            fact = npm[member['path']]
            root = fact['package_root']
            assert root in packages
            if member['type'] == 'file':
                assert fact['status'] == 'equal' and fact['expected'] == fact['actual']
            else:
                assert member['type'] == 'directory'
                relative = member['path'][len(root) + 1:]
                assert any(name == relative or name.startswith(relative + '/') for name in archive_names[root])
                assert '/node_modules' not in relative
        append(row, 'INSTALLED-PACKAGE', 'S8.2-6,S8.2-7,S8.2-8,S8.2-16',
               'Unchanged npm package payload files or their archive directories',
               'raw:D1b/handoff/void/npm-member-integrity.tsv',
               'Every member belongs to an installed npm package and matches its verified archive payload; the package line covers it before later questions.')
    elif row['name'].startswith('/usr/lib/modules'):
        listed = members[row['id']]
        for member in listed:
            assert member['persistence'] == 'persistent'
            assert member['path'] == '/usr/lib/modules/6.12.11_1' or member['path'].startswith('/usr/lib/modules/6.12.11_1/')
            assert not provided[member['path']]
            assert old[member['path']] and all(f['status'] == 'no-reference-found' for f in old[member['path']])
        append(row, 'UNKNOWN', 'S8.2-6,S8.2-7,S8.2-9,S8.2-15,S8.2-16',
               'Stored files or directories of the older kernel module tree',
               'raw:D1b/handoff/void/old-package-member-integrity.tsv',
               'Original package provenance and reference comparison are missing; current metadata cannot establish unchanged package membership or the source line that obtained these members.')

stream.close()
print(collections.Counter(r['decision'] for r in table(OUT)))
print('Saved', len(done), 'of', len(rows))
