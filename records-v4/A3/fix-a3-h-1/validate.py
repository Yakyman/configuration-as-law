"""Mechanical checks of the changed artifacts, without rerunning frozen analyses."""
from pathlib import Path
import csv
import hashlib
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]

def read(path):
    with (ROOT/path).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

with (OUT/'raw/validation.txt').open('x') as log:
    def report(s):
        print(s)
        log.write(s+'\n')

    report('Mechanical validation, '+datetime.now(timezone.utc).isoformat())
    for f in ['A3/RESULT.md', 'A3/FIX-A3-H-1.md']:
        cmd = ['/usr/bin/python3', '-I', 'bin/check_quotes.py', f]
        p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        report('Command: '+' '.join(cmd))
        report(p.stdout.strip())
        assert p.returncode == 0, p.stderr
    frozen = (OUT/'raw/frozen-inputs.sha256').read_text().splitlines()
    for line in frozen:
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    report(f'Frozen-input checksum verification: {len(frozen)} unchanged files.')

    g = read('A3/fix-a3-h-1/gap-scope.tsv')
    assert len({(r['card'], r['id']) for r in g}) == len(g)
    c = Counter((r['card'], r['machine']) for r in g if r['review_status']=='CONFIRMED')
    assert c == {('C2','developer'):7, ('C6','developer'):2, ('C7','developer'):2, ('C7','server'):1}
    report('Confirmed scopes: '+str(dict(c)))
    ctime = read('A3/fix-a3-h-1/ctime-unknown.tsv')
    assert len(ctime)==467 and len({r['id'] for r in ctime})==467
    report('Ctime impacts: '+str(dict(Counter(r['input_verdict'] for r in ctime))))
    cache = read('A3/fix-a3-h-1/cache-card.tsv')
    assert Counter(r['family'] for r in cache)=={'Go':986,'Bun':344,'uv':5,'RubyGems':1}
    report('Card 4 family counts: '+str(dict(Counter(r['family'] for r in cache))))

    # Only effect intersections are checked; no draws or old audits are rerun.
    changed = {r['id'] for r in g if r['review_status'] in ['CONFIRMED','FACT_UNKNOWN']}
    for name in ['sample-resolved.tsv', 'sample-agreed.tsv']:
        sample = read('A3/review/'+name)
        assert not changed.intersection(r['id'] for r in sample)
    sample = read('A3/review/sample-resolved.tsv')
    overlap = [r for r in sample if r['id'] in {x['id'] for x in ctime}]
    assert len(overlap)==9 and all(r['audit']=='FACT_UNKNOWN' for r in overlap)
    report('Sample impacts: no changed gap candidate overlaps either sample; 9 ctime overlaps already FACT_UNKNOWN. No sample rerun.')

    docs = [ROOT/'A3/RESULT.md', ROOT/'A3/FIX-A3-H-1.md', OUT/'raw/documentation.md']
    for p in docs:
        text = p.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' not in target:
                assert (p.parent/target.split('#')[0]).exists(), (p.name, target)
    report('Relative links in updated reports and documentation: all targets exist.')
    report('Result first line: '+(ROOT/'A3/RESULT.md').read_text().splitlines()[0])
    report('Mechanical checks passed. Independent acceptance is not asserted.')
