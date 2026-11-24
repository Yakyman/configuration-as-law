"""Textual validation for FX-S3-A-2; run from the night folder."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import re
import subprocess

base = Path('S3/raw/fix-s3-a-2')
files = [Path('S3/ARGUMENT.md'), Path('S3/QUESTIONS.md'), Path('S3/FIX-S3-A-2.md')]
print('FX-S3-A-2 textual verification')
print('Recorded:', datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))
print('Operator checks only; independent acceptance pending. No empirical rerun.\n')

for p in files:
    cmd = ['/usr/bin/python3', '-I', 'bin/check_quotes.py', str(p)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print('Command:', ' '.join(cmd))
    print(result.stdout, end='')
    print('Exit code:', result.returncode)
    assert result.returncode == 0, result.stderr

sentences = dict(re.findall(r'^- \*\*(S\d\.\d-\d+)\*\* (.+)$', Path('SENTENCES.md').read_text(), re.M))
for p in files:
    pairs = re.findall(r'(S\d\.\d-\d+): “([^”]+)”', p.read_text())
    mismatches = [(sid, quote) for sid, quote in pairs if sentences.get(sid) != quote]
    print(f'{p}: exact ID–sentence pairs {len(pairs)}; distinct {len(set(pairs))}; mismatches {len(mismatches)}')
    assert not mismatches, mismatches

before = (base/'before/ARGUMENT.md').read_text()
after = files[0].read_text()
rows = lambda s: re.findall(r'^\| (?:A\d|I\d|B\d)\..*$', s, re.M)
assert len(rows(after)) == 16 and rows(before) == rows(after)
print('\nMoment rows: 16; all byte-identical to before-copy.')
assert before.split('## (b)')[1].split('## Separate gap lists')[0] == after.split('## (b)')[1].split('## Separate gap lists')[0]
print('Part (b): byte-identical to before-copy.')
assert after.splitlines()[0] == 'STEP 3: (a) ?; (b) ?'
print('First line:', after.splitlines()[0])
findings = re.findall(r'^\| (\d+)\.', files[2].read_text(), re.M)
assert findings == [str(i) for i in range(1, 8)]
print('Finding dispositions:', ', '.join(findings))
assert 'A-W2, candidate only, unless Section 8.5 covers it (question 2)' in after
assert 'on a third reading' in files[1].read_text()
print('A-W2 conditional status and third reading in question 2: present.')

manifest = json.loads((base/'frozen-inputs.json').read_text())
changed = [p for p, digest in manifest.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest() != digest]
print(f'Preserved inputs and historical evidence: {len(manifest)} files; mismatches {len(changed)}.')
assert not changed, changed

diff = ''
for name in ['ARGUMENT.md', 'QUESTIONS.md']:
    old = base/'before'/name
    current = Path('S3')/name
    diff += ''.join(difflib.unified_diff(old.read_text().splitlines(True), current.read_text().splitlines(True), fromfile=str(old), tofile=str(current)))
(base/'changes.diff').write_text(diff)
print('Complete diff written to', base/'changes.diff')
print('\nCurrent artifact SHA-256:')
for p in files + [base/'changes.diff', base/'verify.py', base/'frozen-inputs.json']:
    print(hashlib.sha256(p.read_bytes()).hexdigest(), p)
print('\nResult: PASS')
