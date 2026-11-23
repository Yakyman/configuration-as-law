"""Recount changed memberships and audit dispositions from frozen evidence; no probes."""
import collections
import csv
import hashlib
import json
import random
import re
from pathlib import Path

csv.field_size_limit(100000000)
out = Path('A3R/fix-a3r-h-1')
def read(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter='\t'))
def write(name, rows, fields=None):
    with (out / name).open('w') as f:
        w = csv.DictWriter(f, fields or list(rows[0]), delimiter='\t')
        w.writeheader()
        w.writerows(rows)

joined = read('A3R/compare/joined.tsv')
adj = read('A3R/adjudication/rows.tsv')
old_extent = read('A3R/review/code_extent.tsv')
data = Path('A3R/in/raw/lived/raw/160-filesystem.out').read_bytes().split(b'\0')
paths = {data[i].decode(): data[i+1].decode() for i in range(0, len(data)-1, 6)}
def members(row):
    if not row['kind'].startswith('stored'):
        return []
    if ':subtree' in row['kind']:
        return [row['name']]
    return [p for p in re.findall(r'/[^\\"\],]+', row['members']) if p != row['name']]
def represented(row, witnesses):
    mem = members(row)
    return [p for p in witnesses if any(p == m or p.startswith(m + '/') for m in mem)]

# Card 1 did not change: preserve its reviewed records byte-for-field.
extent = [r for r in old_extent if r['card'] == '1']
history = ['/home/user/.emacs.d/savefile/recentf', '/home/user/.emacs.d/savefile/savehist']
assert all(p in paths for p in history)
prefix = '/var/lib/systemd/deb-systemd-helper-enabled/'
markers = sorted(p for p, kind in paths.items()
                 if kind == 'f' and p.startswith(prefix) and not p.endswith('.dsh-also'))
assert all(p.rsplit('/', 1)[0].endswith('.wants') or '/' not in p[len(prefix):] for p in markers)
assert markers
write('helper-witnesses.tsv', [{'path': p, 'type': paths[p],
      'evidence': 'raw/helper-source.txt:354-375; A3R/in/raw/lived/raw/160-filesystem.out'}
      for p in markers])
search = []
for row in joined:
    for card, witnesses, reason, evidence in [
        ('7', history, 'History restored by executing saved editor code: ',
         'A3R/in/raw/lived/raw/160-filesystem.out; A3R/adjudication/rows.tsv:99b8709d5a3af244262c5442'),
        ('9', markers, 'Past enablement marker gates subsequent service-link creation: ',
         'A3R/in/raw/lived/raw/160-filesystem.out; A3R/fix-a3r-h-1/raw/helper-source.txt:354-375'),
    ]:
        hits = represented(row, witnesses)
        if card == '9' and (hits or 'deb-systemd-helper' in row['name']):
            search.append({'id': row['id'], 'kind': row['kind'], 'name': row['name'],
                           'member_witnesses': '|'.join(hits), 'confirmed': str(bool(hits)).lower()})
        if hits:
            extent.append({'id': row['id'], 'card': card, 'kind': row['kind'],
                           'name': row['name'], 'reason': reason + hits[0], 'evidence': evidence})
write('code_extent.tsv', extent)
write('helper-search.tsv', search)
removed = [r for r in old_extent if r['card'] == '7' and
           r['id'] not in {n['id'] for n in extent if n['card'] == '7'}]
write('removed-history-memberships.tsv', removed)
assert len(removed) == 3
assert [r for r in extent if r['card'] == '1'] == [r for r in old_extent if r['card'] == '1']

sentences = {}
for line in Path('SENTENCES.md').read_text().splitlines():
    m = re.match(r'- \*\*(S[\d.]+-\d+)\*\* (.*)', line)
    if m:
        sentences[m[1]] = m[2].replace('**', '')
audit = read('A3R/review/sample_audit.tsv')
scope_unknown = {
    '852fec2bc63d3ac71655249a': 'The inventory identifies stream metadata files but not their saved fields or exact removal effects. Program state alone is not a NOT decision.',
    '4223394cc494d974882ce847': 'A staged os-release copy and the retained source do not establish this copy\'s consumer or removal effect. No unchanged-capability exemption is demonstrated.',
    'lived-tec6e90176f': 'The subtree includes runtime configuration, lock, secret directories and control endpoints. Their exact contents/roles and whole-row removal effects are not established; regeneration alone is not an exemption.',
}
for row in audit:
    if row['sample'] == 'resolved' and row['order'] in {'4', '12', '15', '16'}:
        row['candidate_verdict'] = 'UNKNOWN'
        row['reason'] += ' S3-2 supplies an evidential outcome, not a recording decision or a refutation.'
    if row['id'] in scope_unknown:
        row.update(candidate='yes', candidate_verdict='UNKNOWN', review_decision='UNKNOWN',
                   sentence_ids='S3-1,S3-2', reason=scope_unknown[row['id']])
    if row['id'] == 'e6c7b500df6175d8c883f1e4':
        row.update(candidate='yes', candidate_verdict='CONFIRMED', review_decision='HOLE',
                   sentence_ids='S2.2-1,S2.2-6',
                   reason='Card 9: helper records earlier enablement, then checks these exact markers before creating service links. History exemption and behavioural dependence collide. See scope-review.md and raw/helper-source.txt:354-375; no next-upgrade claim is needed.')
    if row['id'] == 'e2107a3dd8d91a0eef56dac4':
        row.update(candidate='no', candidate_verdict='SUPPORTED', review_decision='MUST',
                   sentence_ids='S2.2-1,S2.2-2',
                   reason='Recorded device-link arbitration function supports the original MUST under its cited rules. S2.5-1 provides no literal NOT decision. Broader proposed state-wide exemption remains an author question; see QUESTIONS.md.')
    row['exact_sentences'] = ' | '.join(sentences[s] for s in row['sentence_ids'].split(','))
write('sample_audit.tsv', audit)
adj_by_id = {r['id']: r for r in adj}
mixed_sample = [dict(sample_order=r['order'], id=r['id'], name=r['name'],
                    original_verdict=adj_by_id[r['id']]['verdict'],
                    corrected_disposition=r['candidate_verdict'])
                for r in audit if r['sample'] == 'resolved'
                and adj_by_id[r['id']]['verdict'] == 'RESOLVED:MIXED']
write('mixed-sample.tsv', mixed_sample)

# Retain and verify the original selections; no new random draw of cases.
adj_ids = {r['id'] for r in adj}
for sample, seed, n, pool in [
    ('resolved', 2026112201, 40, [r for r in adj if r['verdict'].startswith('RESOLVED:')]),
    ('agreed', 2026112202, 60, [r for r in joined if r['same'] == 'yes' and r['id'] not in adj_ids]),
]:
    expected = random.Random(seed).sample(sorted(pool, key=lambda r: r['id']), n)
    selected = json.loads(Path(f'A3R/review/{sample}_sample.json').read_text())
    actual = [r for r in audit if r['sample'] == sample]
    assert [r['id'] for r in selected] == [r['id'] for r in expected] == [r['id'] for r in actual]

sets = {c: {r['id'] for r in extent if r['card'] == c} for c in ['1', '7', '9']}
summary = {
    'card_rows': {c: len(s) for c, s in sets.items()},
    'card_1_7_overlap': len(sets['1'] & sets['7']),
    'card_1_7_distinct': len(sets['1'] | sets['7']),
    'card_9_overlap_with_1_7': len(sets['9'] & (sets['1'] | sets['7'])),
    'distinct_rows_all_cards': len(set.union(*sets.values())),
    'helper_markers': len(markers),
    'sampled_mixed_rows': len(mixed_sample),
    'sampled_mixed_partial_citations': sum(r['corrected_disposition'] == 'REFUTED' for r in mixed_sample),
    'samples': {s: dict(collections.Counter(r['candidate_verdict'] for r in audit if r['sample'] == s))
                for s in ['resolved', 'agreed']},
    'original_card_dispositions': {'CONFIRMED': 2, 'REFUTED': 5, 'UNKNOWN': 1, 'FACT-WRONG': 0, 'OUTSIDE': 0},
    'sample_quote_defects': sum(r['original_quote_is_full_sentence'] == 'false' for r in audit),
}
for filename, digest in json.loads((out / 'frozen-inputs.sha256.json').read_text()).items():
    assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == digest, filename
summary['frozen_inputs_unchanged'] = True
(out / 'counts.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
