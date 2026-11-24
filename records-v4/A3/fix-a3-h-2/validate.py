"""Mechanical checks of round 2 artifacts; no repeat of unchanged analyses."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


with (OUT/'raw/validation.txt').open('x') as log:
    def report(s):
        print(s)
        log.write(s+'\n')

    report('Mechanical validation, '+datetime.now(timezone.utc).isoformat())
    for name in ('A3/RESULT.md', 'A3/FIX-A3-H-2.md'):
        cmd = ['/usr/bin/python3', '-I', 'bin/check_quotes.py', name]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        report('Command: '+' '.join(cmd))
        report(p.stdout.strip())
        assert p.returncode == 0, p.stderr

    frozen = {}
    for manifest in ('frozen-inputs.sha256', 'consumed-inputs.sha256'):
        for line in (OUT/'raw'/manifest).read_text().splitlines():
            digest, name = line.split('  ',1)
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
            if name in frozen:
                assert frozen[name] == digest
            frozen[name] = digest
    report(f'Frozen and consumed inputs: {len(frozen)} distinct files unchanged; prior correction artifacts included.')

    old = rows(ROOT/'A3/fix-a3-h-1/gap-scope.tsv')
    new = rows(OUT/'gap-scope.tsv')
    key = lambda r: (r['card'],r['id'],r['review_status'])
    assert {key(r) for r in old} == {key(r) for r in new if r['card']!='C3'}
    assert len({(r['card'],r['id']) for r in new}) == len(new)
    c3 = [r for r in new if r['card']=='C3']
    assert Counter(r['review_status'] for r in c3) == {'CONFIRMED':4,'FACT_UNKNOWN':7,'EXCLUDED':5}
    assert Counter(r['machine'] for r in c3 if r['review_status']=='CONFIRMED') == {'developer':1,'server':3}
    report('C3: 4 confirmed (developer 1, server 3), 7 FACT_UNKNOWN, 5 excluded; prior C2/C6/C7 statuses preserved.')

    cache = rows(OUT/'cache-card.tsv')
    assert Counter((r['family'],r['card_disposition']) for r in cache) == {
        ('Go','FACT-WRONG'):986, ('Bun','FACT-WRONG'):344, ('uv','FACT-WRONG'):5, ('RubyGems','FACT_UNKNOWN'):1}
    report('Card 4: Go 986, Bun 344, uv 5 FACT-WRONG; RubyGems 1 FACT_UNKNOWN.')
    summary = json.loads((OUT/'raw/recompute.json').read_text())
    assert not any(summary['sample_impacts'].values())
    report('Saved impact intersections are empty; samples were not redrawn or re-audited.')

    checks = rows(OUT/'content-evidence.tsv')
    assert len(checks) == 3
    for r in checks:
        b = (OUT/'raw'/Path(r['member']).name).read_bytes()
        assert len(b) == int(r['bytes']) < 4096
        assert 'sha256-prefix4096:'+hashlib.sha256(b).hexdigest() == r['sha256_prefix4096']
        m = next(m for m in rows(ROOT/r['member_table']) if m['path']==r['member'])
        assert m['size'] == r['bytes'] and m['signature'] == r['sha256_prefix4096']
    report('Three recovered content blocks match inventory sizes and full-file hashes: 80, 143, 145 bytes.')

    brew = json.loads((OUT/'raw/homebrew-source.json').read_text())
    assert re.fullmatch('[0-9a-f]{40}',brew['commit']) and brew['commit'] in brew['url']
    excerpt = {r['line']:r['text'] for r in brew['excerpt']}
    assert 'HOMEBREW_PREFIX}/Homebrew' in excerpt[340] and 'sudo_removal_paths' in excerpt[342]
    steam = (ROOT/'A3/adjudication/raw/steam-bootstrap/steam.sh').read_text().splitlines()
    assert 'reset_steam' in steam[532] and steam[610] == '}'
    report('Homebrew citation pinned to immutable commit, lines 340–342; Steam closing brace is line 611.')

    documents = [ROOT/'A3/RESULT.md',ROOT/'A3/FIX-A3-H-2.md',OUT/'raw/documentation.md',OUT/'QUESTIONS.md']
    for p in documents:
        content = p.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' not in target:
                assert (p.parent/target.split('#')[0]).exists(), (p.name,target)
        assert not re.search(r'/home/(?!user(?:/|\b)|linuxbrew(?:/|\b))',content), p.name
    result = documents[0].read_text()
    assert result.splitlines()[0] == 'LIVED-IN: 4 confirmed gaps'
    assert result.count('## Confirmed gap:') == 4
    assert 'lower bound, not an exact total extent' in result
    report('Relative links, result first line, four gap sections and C6 lower-bound disclosure checked.')
    report('All mechanical checks passed. Independent acceptance remains pending review.')
