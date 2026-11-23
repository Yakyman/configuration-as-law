"""Draw the sample of agreed objects for step 2 of Supplement 1.

Usage: python3 -I s2_sample.py JOINED.tsv OUT.tsv
JOINED.tsv is a comparison table of two classifications (columns id, machine, kind, name, members, evidence,
c1_decision, c1_sentences, ..., c2_decision, c2_sentences, ...). The sample holds 300 rows on which both
classifications gave the same decision other than a gap, a mixed group or an unknown fact, allocated to the kinds of objects in
proportion to their numbers (largest remainders), drawn with the seed 20261123 from the rows sorted by id.
"""
import csv
import random
import os
import sys
from collections import defaultdict

SEED, SIZE = 20261123, 300
csv.field_size_limit(sys.maxsize)
EXCLUDED = {'GAP-NONE', 'GAP-TWO', 'MIXED', 'UNKNOWN'}


def main(source, target):
    with open(source, encoding='utf-8', newline='') as handle:
        rows = [r for r in csv.DictReader(handle, delimiter='\t')
                if r['c1_decision'] == r['c2_decision'] and r['c1_decision'] not in EXCLUDED]
    rows.sort(key=lambda r: r['id'])
    by_kind = defaultdict(list)
    for row in rows:
        by_kind[row['kind']].append(row)
    size = min(SIZE, len(rows))
    exact = {kind: size * len(group) / len(rows) for kind, group in by_kind.items()}
    quota = {kind: int(value) for kind, value in exact.items()}
    rest = sorted(exact, key=lambda kind: (-(exact[kind] - quota[kind]), kind))
    for kind in rest[:size - sum(quota.values())]:
        quota[kind] += 1
    rng = random.Random(SEED)
    chosen = []
    for kind in sorted(by_kind):
        chosen += rng.sample(by_kind[kind], quota[kind])
    chosen.sort(key=lambda r: r['id'])
    fields = ['id', 'machine', 'kind', 'name', 'members', 'evidence', 'decision', 'c1_sentences', 'c2_sentences']
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    with open(target, 'w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
        writer.writerow(fields)
        for row in chosen:
            writer.writerow([row['id'], row['machine'], row['kind'], row['name'], row['members'], row['evidence'],
                             row['c1_decision'], row['c1_sentences'], row['c2_sentences']])
    print(f'agreed rows: {len(rows)}; kinds: {len(by_kind)}; sampled: {len(chosen)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
