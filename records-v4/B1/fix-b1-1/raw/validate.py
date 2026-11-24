"""Mechanical audit of revised artifacts, not independent acceptance."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
import subprocess

F = Path(__file__).resolve().parents[1]
B = F.parent
N = B.parent

def read_rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))

old = read_rows(B / 'CHANNELS-V4.tsv')
new = read_rows(F / 'CHANNELS-V4.tsv')
assert len(new) == len(old) == 88
assert all(len(r) == 8 and None not in r and all(v is not None for v in r.values()) for r in new)
assert [r['variant'] for r in old] == [r['variant'] for r in new]
previous_names = []
for line in (N.parent / 'night-1122/B1/CHANNELS.md').read_text().splitlines():
    # Only the authorized first-column case identifiers/names enter this check.
    if re.match(r'^\| [CM]\d+\.\d+ ', line):
        previous_names.append(line.split('|')[1].strip())
assert previous_names == [r['variant'] for r in new]
assert len(set(previous_names)) == 88
assert sum(r['variant'].startswith('C') for r in new) == 76
assert sum(r['variant'].startswith('M') for r in new) == 12
assert all(len(r['reason'].split()) <= 40 for r in new)
print('PASS: 88 original identifiers/names in order; 76 C and 12 M; eight fields; reasons <=40 words.')

changed = {b['variant'].split()[0] for a, b in zip(old, new) if a != b}
expected = {'C3.5', 'C4.3', 'C5.1', 'C5.2', 'C5.3', 'C5.4', 'C5.5', 'C6.3',
            'C7.06', 'C7.07', 'C7.17', 'C7.19', 'C9.5'}
assert changed == expected
delta = json.loads((F / 'raw/changes.json').read_text())
assert set(delta) == changed
for a, b in zip(old, new):
    rid = b['variant'].split()[0]
    actual = {k: {'before': a[k], 'after': b[k]} for k in b if a[k] != b[k]}
    assert actual == delta.get(rid, {})
print('PASS: exactly 13 affected rows changed; 75 unchanged; every changed cell matches changes.json.')

counts = json.loads((F / 'raw/counts.json').read_text())
statuses = Counter(r['status'] for r in new)
assert statuses == counts['status']
assert statuses == {'DECIDED': 53, 'TWO_WAYS': 8, 'FACT_UNKNOWN': 27}
first_line = (B / 'RESULT.md').read_text().splitlines()[0]
assert first_line == 'CHANNELS: 53 decided, 0 not decided, 8 two ways, 27 fact unknown'
tags = ['INSTALLER', 'BUILTIN', 'GENERAL', 'BREAKING', 'UNKNOWN']
for tag, (name, members) in zip(tags, counts['routes'].items()):
    assert members == [r['variant'].split()[0] for r in new if f'[{tag}]' in r['route']]
baseline_kinds = json.loads((B / 'raw/counts.json').read_text())['kinds']
for name, members in counts['kinds'].items():
    expected_members = [x for x in baseline_kinds[name] if not (name == 'Installed object' and x == 'C7.07')]
    assert members == expected_members
    assert len(set(members)) == len(members)
    assert all(x.startswith('C') for x in members)
print('PASS: result status totals and all route/kind memberships reconcile; C7.07 installed-object exclusion verified.')

def norm(s):
    return re.sub(r'\s+', ' ', s.replace('**', '')).strip()
sentences = {}
for line in (N / 'SENTENCES.md').read_text().splitlines():
    m = re.match(r'- \*\*(S\d\.\d-\d+)\*\* (.*)', line)
    if m:
        sentences[m[1]] = norm(m[2])
quote_count = 0
for content in [r['law'] for r in new] + [(F / 'GAPS.md').read_text()]:
    for sid, quote in re.findall(r'(S\d\.\d-\d+): «([^»]+)»', content):
        assert norm(quote) == sentences[sid], sid
        quote_count += 1
text = norm((N / 'TEXT.md').read_text())
for r in new:
    for quote in re.findall(r'«([^»]+)»', r['law']):
        assert norm(quote) in text
gap_ids = set(re.findall(r'\b[CM]\d+\.\d+\b', (F / 'GAPS.md').read_text()))
assert gap_ids == {r['variant'].split()[0] for r in new if r['status'] in ['TWO_WAYS', 'NOT_DECIDED']}
print(f'PASS: {quote_count} numbered sentence quotations match their IDs; all law quotes match TEXT.md; gaps cover exactly eight rows.')

manifest = json.loads((F / 'inputs/manifest.json').read_text())
for relative, sha in manifest.items():
    path = F / 'inputs/RESULT-before.md' if relative == 'B1/RESULT.md' else N / relative
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, relative
print(f'PASS: {len(manifest)} baseline file hashes preserved, with the superseded result checked through its saved copy.')

command = ['/usr/bin/python3', '-I', 'bin/check_quotes.py', 'B1/fix-b1-1/GAPS.md']
completed = subprocess.run(command, cwd=N, capture_output=True, text=True)
(F / 'raw/check-quotes.txt').write_text('$ ' + ' '.join(command) + '\n' + completed.stdout + completed.stderr + f'exit_code: {completed.returncode}\n')
assert completed.returncode == 0
assert 'quotes checked: 17;' in completed.stdout
print('PASS: revised GAPS.md quotation checker: 17 checked, zero missing (raw/check-quotes.txt).')
print('No runtime probes were run. This log is mechanical verification, not independent acceptance.')
