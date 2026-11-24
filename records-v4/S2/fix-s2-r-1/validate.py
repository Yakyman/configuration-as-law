"""Mechanical verification of FX-S2-R-1; not substantive acceptance."""
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('S2/fix-s2-r-1')
messages = [datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')]


def read(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def check(condition, description):
    assert condition, description
    messages.append('PASS: ' + description)


def outcome(r):
    if r['verdict'] == 'FACT-UNKNOWN' or r['verdict'] == 'AGREED' and r['c1'].startswith('UNKNOWN'):
        return '?'
    if r['verdict'] == 'GAP' or r['verdict'] == 'AGREED' and r['c1'].startswith('GAP'):
        return '0'
    return '1'


hashes = json.loads((OUT/'raw/input-sha256.json').read_text())
check(all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p,h in hashes.items()),
      f'All {len(hashes)} frozen input hashes unchanged, including text, protocol, review and original adjudications.')
report = Path('S2/RESULT.md').read_text()
before = (OUT/'RESULT.before.md').read_bytes()
check(hashlib.sha256(before).hexdigest() == 'bb4474fb19407dd297c36b49af0c6ef4b29733fe1a79754ab1637bb95e9d99dc',
      'Preserved pre-fix RESULT matches the original validation hash.')
old_rows = read('S2/adjudication/rows.tsv')
rows = read(OUT/'rows.tsv')
check(len(rows) == len(old_rows) == 105 and all(
      all(a[k] == b[k] for k in ('object','family','c1','c2')) for a,b in zip(rows,old_rows)),
      '105 original family rows and both original decision columns preserved in order.')
check(Counter(outcome(r) for r in rows) == {'0':17, '?':84, '1':4},
      'Revised object outcomes: 17 zero, 84 unknown, 4 one.')
changed_outcomes = [(a['object'],outcome(b),outcome(a)) for a,b in zip(rows,old_rows) if outcome(a)!=outcome(b)]
check(changed_outcomes == [('void-386e90812bdecbec21d0785c','0','?')],
      'The boot group is the only changed family-row outcome; the container remains zero with revised reasons.')
table = [line.split('|')[1:-1] for line in report.splitlines() if re.match(r'^\| \d+\. ',line)]
check(len(table) == 15, 'Report retains the 15 fixed families.')
family_results = []
for num,cells in enumerate(table,1):
    current = [r for r in rows if r['family'] == str(num)]
    grouped = {}
    for part in cells[2].split('<br>')[1:]:
        match = re.match(r'([01?]) \((\d+)\): (.*)', part.strip())
        assert match, part
        result, count, body = match.groups()
        ids = re.findall(r'`([^`]+)`',body)
        assert len(ids) == int(count)
        grouped.update({oid:result for oid in ids})
    check(grouped == {r['object']:outcome(r) for r in current},
          f'Family {num}: report IDs and per-row outcome buckets match revised rows.')
    results = list(grouped.values())
    result = '0' if '0' in results else '?' if '?' in results else '1'
    assert cells[1].strip() == result
    family_results.append(result)
check(Counter(family_results) == {'0':6, '?':9}, 'Family outcomes: six zero and nine unknown.')

a1 = {(r['source'],r['id']):r for r in read('S2/a1/sample.tsv')}
a2 = {(r['source'],r['id']):r for r in read('S2/a2/sample.tsv')}
check(len(a1) == len(a2) == 600 and a1.keys() == a2.keys()
      and all(a1[k]['agreed_decision'] == a2[k]['agreed_decision'] for k in a1)
      and Counter(k[0] for k in a1) == {'D1':300,'A3':300},
      'Sample retains 600 aligned original decisions: 300 D1 and 300 A3.')
sample = read(OUT/'sample-adjudication.tsv')
old_sample = {(r['source'],r['id']):r for r in read('S2/sample-adjudication.tsv')}
keys = {(r['source'],r['id']) for r in sample}
flagged = {(r['source'],r['id']) for r in read('S2/sample/flagged.tsv')}
challenged = {k for k in a1 if 'DOES-NOT-FOLLOW' in (a1[k]['finding'],a2[k]['finding'])}
check(keys == flagged == challenged and len(sample) == 8 and
      list(sample[0]) == ['id','source','a1','a2','verdict','sentences','reason'],
      'All eight original challenges adjudicated exactly once with the required header.')
cup = {'gaming-0b9c75abae9461b0be7b041d','gaming-7b8b804e906bab4f5a36ccf2'}
for r in sample:
    k = (r['source'],r['id'])
    assert (r['a1'],r['a2']) == (a1[k]['finding'],a2[k]['finding'])
    if r['id'] in cup:
        assert r['verdict'] == 'GAP'
    else:
        assert r == old_sample[k]
check(True, 'Only the two CUPS sample adjudications changed; all other six rows are exact copies.')
unreviewed_unknown = [k for k in a1 if k not in keys and (a1[k]['finding'],a2[k]['finding']) != ('FOLLOWS','FOLLOWS')]
both_follow = [k for k in a1 if a1[k]['finding'] == a2[k]['finding'] == 'FOLLOWS']
check(len(both_follow) == 582 and len(unreviewed_unknown) == 10 and
      Counter(r['verdict'] for r in sample) == {'GAP':2,'FACT-UNKNOWN':6},
      'Sample accounting: 582 follows + 2 gaps + (10 unchallenged + 6 challenged) unknown = 600; outcome zero.')
check(report.splitlines()[0] == 'STEP 2: 6 of 15 families with outcome 0; 9 with ?; sample outcome 0, 2 of 600 agreements do not follow',
      'First line matches recomputed family and sample outcomes.')

facts = read('S2/facts.tsv')
audit = read(OUT/'unknown-facts-audit.tsv')
audit_ids = {r['object'] for r in audit}
required_ids = {r['object'] for r in old_rows if r['family'] in {'7','8','10','12'}
                and r['verdict'] in {'AGREED','GAP'} and 'GAP' in r['c1']}
expected = {(r['object'],r['fact']):r['value'] for r in facts
            if r['object'] in required_ids and r['value'].startswith('UNKNOWN:')}
check(audit_ids == required_ids and len(audit_ids) == 11 and len(audit) == 23 and
      {(r['object'],r['fact']):r['saved_value'] for r in audit} == expected and
      all(r['sentences'] and r['evidence'] and r['reason'] for r in audit),
      'All 23 explicit UNKNOWN facts on all 11 challenged shared-gap rows preserved and individually explained.')
for r in audit:
    reference = next(i for i,f in enumerate(facts,2) if f['object']==r['object'] and f['fact']==r['fact'])
    assert str(reference) in r['evidence'], (r['object'],r['fact'])
check(True, 'Each audit entry cites its original fact line.')

c1 = {r['object']:r for r in read('S2/c1/decisions.tsv')}
c2 = {r['object']:r for r in read('S2/c2/decisions.tsv')}
signs = read(OUT/'signs.tsv')
for r in signs:
    a,b = c1[r['object']],c2[r['object']]
    assert all(r['c1_'+k]==a[k] and r['c2_'+k]==b[k] for k in ('by_meaning','without_forbidding'))
    if r['scope'] == 'family':
        exact = f"| {r['family']} / `{r['object']}` | {a['by_meaning']} | {b['by_meaning']} | {a['without_forbidding']} | {b['without_forbidding']} | {r['yes_no_reading']}; {r['full_answer_reading']} |"
        assert exact in report
active = [r for r in signs if r['scope']=='family']
check({r['object'] for r in active} == {r['object'] for r in rows if outcome(r)=='0'} and
      Counter(r['yes_no_reading'] for r in active) == {'both signs':14,'not both':3} and
      Counter(r['full_answer_reading'] for r in active) == {'both signs':11,'not both':6},
      'All 17 family-gap answer pairs are verbatim; conditional signs are 14/3 and 11/6; boot answers retained separately.')
b1 = {r['id']:r for r in read('S2/b1/answers.tsv')}
b2 = {r['id']:r for r in read('S2/b2/answers.tsv')}
for r in sample:
    a,b = b1[r['id']],b2[r['id']]
    assert f"| `{r['id']}` / {r['verdict']} | {a['by_meaning']} | {b['by_meaning']} | {a['without_forbidding']} | {b['without_forbidding']} |" in report
check(True, 'All eight sample answer pairs are verbatim and appear under their revised gap/unknown status.')

# Verify complete sentence quotations in the revised sample reasons.
sentences = {}
for line in Path('SENTENCES.md').read_text().splitlines():
    match = re.match(r'- \*\*(S[\d.]+-\d+)\*\* (.+)',line)
    if match:
        sentences[match[1]] = match[2].replace('**','')
quotes = 0
for r in sample:
    for sid,quote in re.findall(r'(S[\d.]+-\d+) “([^”]+)”',r['reason']):
        assert sentences[sid] == quote
        quotes += 1
check(quotes == 14, 'All 14 complete-sentence quotations in the revised sample reasons exactly match SENTENCES.md.')
for path in ['S2/RESULT.md','S2/FIX-S2-R-1.md',str(OUT/'FACT-AUDIT.md')]:
    command = ['/usr/bin/python3','-I','bin/check_quotes.py',path]
    result = subprocess.run(command, capture_output=True, text=True)
    messages.extend(['COMMAND: '+' '.join(command), result.stdout.strip(), 'Exit code: '+str(result.returncode)])
    assert result.returncode == 0, result.stderr

products = [Path('S2/RESULT.md'),Path('S2/FIX-S2-R-1.md')] + sorted(p for p in OUT.rglob('*') if p.is_file()
            and p.name not in {'validation.txt','output-sha256.json'})
check(all(not re.search(r'/(?:home|Users)/[A-Za-z0-9_.-]+', p.read_text()) for p in products),
      'New records contain no machine home paths.')
check(not list(OUT.rglob('__pycache__')), 'No generated bytecode/cache or disposable probe data retained.')
messages.append('Mechanical checks complete. Separate substantive acceptance remains pending.')
(OUT/'raw/validation.txt').write_text('\n'.join(messages)+'\n')
(OUT/'raw/output-sha256.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in products},indent=2)+'\n')
print('\n'.join(messages))
