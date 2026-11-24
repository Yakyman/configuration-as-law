"""Review RV-S3-A-3: independent recomputation of FX-S3-A-2 records. Run from the night folder. Writes nothing."""
import json, hashlib, re, difflib
from pathlib import Path

m = json.load(open('S3/raw/fix-s3-a-2/frozen-inputs.json'))
bad = [p for p, d in m.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest() != d]
print('frozen manifest files', len(m), 'mismatches', bad)
s = dict(re.findall(r'^- \*\*(S\d\.\d-\d+)\*\* (.+)$', Path('SENTENCES.md').read_text(), re.M))
for f in ['S3/ARGUMENT.md', 'S3/QUESTIONS.md', 'S3/FIX-S3-A-2.md']:
    t = Path(f).read_text()
    pairs = re.findall(r'(S\d\.\d-\d+): “([^”]+)”', t)
    print(f, 'pairs', len(pairs), 'distinct', len(set(pairs)), 'mismatch', sum(1 for a, b in pairs if s.get(a) != b))
b = Path('S3/raw/fix-s3-a-2/before/ARGUMENT.md').read_text()
a = Path('S3/ARGUMENT.md').read_text()
rows = lambda x: re.findall(r'^\| (?:A\d|I\d|B\d)\..*$', x, re.M)
print('moment rows', len(rows(a)), 'identical to before', rows(a) == rows(b))
seg = lambda x: x.split('## (b)')[1].split('## Separate gap lists')[0]
print('part (b) identical', seg(a) == seg(b))
diff = ''
for n in ['ARGUMENT.md', 'QUESTIONS.md']:
    o = Path('S3/raw/fix-s3-a-2/before') / n
    c = Path('S3') / n
    diff += ''.join(difflib.unified_diff(o.read_text().splitlines(True), c.read_text().splitlines(True), fromfile=str(o), tofile=str(c)))
print('changes.diff reproduces', diff == Path('S3/raw/fix-s3-a-2/changes.diff').read_text())
for n in ['ARGUMENT.md', 'QUESTIONS.md']:
    print('before', n, hashlib.sha256((Path('S3/raw/fix-s3-a-2/before') / n).read_bytes()).hexdigest())
print('first line', a.splitlines()[0])
