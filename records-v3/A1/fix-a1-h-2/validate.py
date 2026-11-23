"""Check the correction delta and preservation; do not rerun unchanged work."""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / 'A1/fix-a1-h-1'

def read(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

manifest = json.loads((OUT / 'raw/frozen-input-sha256.json').read_text())
assert all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in manifest.items())
affected = {r['id'] for r in read(OUT / 'changes.tsv')}
assert len(affected) == 21
deltas = {}
for name in ('hole-1-extent.tsv', 'unit-file-reader-check.tsv', 'hole-1-scan.tsv'):
    old, new = read(OLD / name), read(OUT / name)
    assert [r['id'] for r in old] == [r['id'] for r in new]
    changed = {a['id'] for a, b in zip(old, new) if a != b}
    assert changed == affected, (name, changed ^ affected)
    deltas[name] = len(changed)
for sample in ('resolved', 'agreed'):
    rows = read(OLD / f'{sample}-audit.tsv')
    assert not affected.intersection(r['id'] for r in rows)
    original = read(ROOT / f'A1/review/{sample}-audit.tsv')
    assert [r['id'] for r in rows] == [r['id'] for r in original]
newcounts = json.loads((OUT / 'counts.json').read_text())
oldcounts = json.loads((OLD / 'counts.json').read_text())
for field in ('h1_confirmed_by_kind', 'h1_confirmed_total', 'original_card_1_status',
              'agreed_judgments', 'resolved_status', 'resolved_quote_support',
              'unit_rows_checked', 'unit_file_reading_second_applier_established', 'whole_table_rows'):
    assert newcounts[field] == oldcounts[field], field
badlinks = []
for path in [ROOT / 'A1/RESULT.md', ROOT / 'A1/FIX-A1-H-2.md', OUT / 'unit-boundaries.md']:
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' not in link and not (path.parent / link.split('#', 1)[0]).exists():
            badlinks.append(f'{path.relative_to(ROOT)}: {link}')
assert not badlinks, badlinks
quotes = {}
for name in ('A1/RESULT.md', 'A1/fix-a1-h-2/unit-boundaries.md'):
    proc = subprocess.run(['/usr/bin/python3', '-I', 'bin/check_quotes.py', name], cwd=ROOT,
                          text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    quotes[name] = proc.stdout.strip()
(OUT / 'raw/quote-check.log').write_text('\n'.join(f'{k}: {v}' for k, v in quotes.items()) + '\n')
summary = {'frozen_files_unchanged': len(manifest), 'changed_rows_per_output': deltas,
           'sample_ids_order_and_audits': 'unchanged; zero affected IDs in either sample',
           'other_count_fields': 'unchanged', 'local_links': 'all resolve', 'quote_checks': quotes}
(OUT / 'raw/validation.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
