#!/usr/bin/env python3
"""Compare the submitted labels, never replace them with adjudicated labels.

Run: python compare.py
Only the standard library is required. Outputs are confined to raw/v3/.
"""
import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASSES = ('recorded', 'derivative', 'data', 'hole-none', 'hole-two')


def read_table(path):
    with path.open(newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    indexed = {}
    for line, row in enumerate(rows, 2):
        key = row.get('id')
        if not key or key in indexed:
            raise ValueError(f'{path}:{line}: missing or duplicate id {key!r}')
        indexed[key] = row
    return indexed


def category(label):
    # Explicit format equivalence, not a new rule about objects.
    if label == 'recorded (works)':
        return 'recorded'
    if label.startswith('derivative of '):
        return 'derivative'
    if label not in CLASSES:
        raise ValueError(f'Unknown class label: {label!r}')
    return label


def owner(row):
    if category(row['class']) != 'derivative':
        return ''
    return row['program_if_derivative'] or (
        row['class'][len('derivative of '):] if row['class'].startswith('derivative of ') else '')


def agreement(left, right):
    if len(left) != len(right):
        raise ValueError('Unequal paired lengths')
    n = len(left)
    a, b = Counter(left), Counter(right)
    matches = sum(x == y for x, y in zip(left, right))
    po = Fraction(matches, n) if n else None
    pe = Fraction(sum(a[k] * b[k] for k in a.keys() | b.keys()), n*n) if n else None
    kappa = (po-pe)/(1-pe) if n and pe != 1 else None
    return {'n': n, 'matches': matches,
            'agreement': float(po) if po is not None else None,
            'expected_agreement': float(pe) if pe is not None else None,
            'kappa': float(kappa) if kappa is not None else None,
            'kappa_exact': str(kappa) if kappa is not None else None}


def write_table(path, rows, fields):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    paths = {name: ROOT/name for name in
             ('c1-classes.tsv', 'c2-classes.tsv', 'residual.tsv', 'preclassified.tsv')}
    a, b, inventory, automatic = [read_table(p) for p in paths.values()]
    if set(automatic) & (set(a) | set(b) | set(inventory)):
        raise ValueError('Automatic and manually classified ids overlap')
    unknown = (set(a) | set(b)) - set(inventory)
    if unknown:
        raise ValueError(f'No VM/object metadata for ids: {sorted(unknown)}')
    decisions_path = ROOT/'definition-audit.tsv'
    decisions = read_table(decisions_path) if decisions_path.exists() else {}
    rows = []
    for key in sorted(set(inventory) | set(a) | set(b)):
        item = inventory[key]
        row = {'id': key, 'machine': item['machine'], 'kind': item['kind'],
               'path_or_name': item['path_or_name'], 'evidence': item['short_evidence']}
        for prefix, source in [('c1', a), ('c2', b)]:
            entry = source.get(key)
            for field in ('class', 'program_if_derivative', 'reason'):
                row[prefix+'_'+field] = entry[field] if entry else ''
            row[prefix+'_category'] = category(entry['class']) if entry else ''
            row[prefix+'_owner'] = owner(entry) if entry else ''
        paired = key in a and key in b
        row['paired'] = int(paired)
        row['literal_disagreement'] = int(paired and a[key]['class'] != b[key]['class'])
        row['class_disagreement'] = int(paired and row['c1_category'] != row['c2_category'])
        row['owner_disagreement'] = int(paired and row['c1_category'] ==
            row['c2_category'] == 'derivative' and row['c1_owner'] != row['c2_owner'])
        row['either_hole'] = int(any(row[p+'_category'].startswith('hole-') for p in ('c1', 'c2')))
        decision = decisions.get(key, {})
        for field in ('resolution', 'quote', 'why', 'open_problems', 'issue_type'):
            row[field] = decision.get(field, '')
        # Literal spelling differences do not need an object reclassification.
        if paired and not row['class_disagreement'] and not row['owner_disagreement'] and not row['either_hole']:
            row['resolution'] = 'same class; notation only' if row['literal_disagreement'] else 'same class'
        rows.append(row)

    scopes = sorted({r['machine'] for r in rows})
    stats = {}
    for scope in scopes + ['overall']:
        selected = [r for r in rows if scope == 'overall' or r['machine'] == scope]
        pairs = [r for r in selected if r['paired']]
        auto = [r for r in automatic.values() if scope == 'overall' or r['machine'] == scope]
        counts = {p: dict(Counter(r[p+'_category'] for r in selected if r[p+'_category']))
                  for p in ('c1', 'c2')}
        auto_counts = Counter(category(r['class']) for r in auto)
        stats[scope] = {
            'inventory_rows': len(selected), 'paired_rows': len(pairs),
            'missing_c1': [r['id'] for r in selected if not r['c1_class']],
            'missing_c2': [r['id'] for r in selected if not r['c2_class']],
            'class_counts': counts, 'automatic_class_counts': dict(auto_counts),
            'full_census_class_counts': {p: dict(Counter(counts[p])+auto_counts) for p in counts},
            'class': agreement([r['c1_category'] for r in pairs], [r['c2_category'] for r in pairs]),
            'literal': agreement([r['c1_class'] for r in pairs], [r['c2_class'] for r in pairs]),
            'class_and_owner': agreement([(r['c1_category'], r['c1_owner']) for r in pairs],
                                         [(r['c2_category'], r['c2_owner']) for r in pairs]),
            'class_disagreements': sum(r['class_disagreement'] for r in pairs),
            'owner_disagreements': sum(r['owner_disagreement'] for r in pairs),
            'hole_counts': {p: sum(r[p+'_category'].startswith('hole-') for r in selected) for p in counts},
            'union_holes': sum(r['either_hole'] for r in selected),
            'confusion': {x: {y: sum(r['c1_category'] == x and r['c2_category'] == y for r in pairs)
                              for y in CLASSES} for x in CLASSES}}
    output = ROOT/'raw/v3'
    output.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ['id']
    write_table(output/'joined.tsv', rows, fields)
    for filename, flag in [('disagreements.tsv', 'class_disagreement'),
                           ('literal-disagreements.tsv', 'literal_disagreement'),
                           ('owner-disagreements.tsv', 'owner_disagreement'),
                           ('holes.tsv', 'either_hole')]:
        write_table(output/filename, [r for r in rows if r[flag]], fields)
    (output/'stats.json').write_text(json.dumps(stats, indent=2, sort_keys=True)+'\n')
    hash_paths = list(paths.values()) + [ROOT.parents[1]/'first-paper'/'PAPER.html', Path(__file__)]
    if decisions_path.exists():
        hash_paths.append(decisions_path)
    (output/'input-hashes.json').write_text(json.dumps({str(p.relative_to(ROOT.parents[1])):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in hash_paths}, indent=2)+'\n')
    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
