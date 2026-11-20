#!/usr/bin/env python3
"""Compare frozen, independently supplied classifications; never reclassify.

Run: python compare.py [--output raw/<new-directory>]
Only the Python standard library is required. Outputs stay under this directory.
Literal labels and five-category class comparisons are BOTH reported. The
derivative's owner is a separate field, never silently used as a class label.
"""
import argparse
import csv
import hashlib
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parent
CATEGORIES = ('recorded', 'derivative', 'data', 'hole-none', 'hole-two')


def read_table(path, required):
    with path.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        if not set(required) <= set(reader.fieldnames or ()):
            raise ValueError(f'{path}: missing required columns')
        rows = list(reader)
    result = {}
    for line, row in enumerate(rows, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f'{path}:{line}: malformed row')
        if not row['id'] or row['id'] in result:
            raise ValueError(f'{path}:{line}: empty or duplicate id')
        result[row['id']] = row
    return result


def category(label):
    if label in ('recorded', 'recorded (works)'):
        return 'recorded'
    if label == 'derivative' or label.startswith('derivative of '):
        return 'derivative'
    if label in ('data', 'hole-none', 'hole-two'):
        return label
    raise ValueError(f'Unknown class: {label!r}')


def owner(row):
    label, field = row['class'], row['program_if_derivative']
    if category(label) != 'derivative':
        if field:
            raise ValueError(f"{row['id']}: non-derivative has an owner")
        return ''
    embedded = label.removeprefix('derivative of ') if label.startswith('derivative of ') else ''
    if embedded and field and embedded != field:
        raise ValueError(f"{row['id']}: conflicting derivative owner fields")
    if not (field or embedded):
        raise ValueError(f"{row['id']}: derivative owner is missing")
    return field or embedded


def metrics(left, right):
    if len(left) != len(right):
        raise ValueError('Metric vectors differ in length')
    n = len(left)
    a, b = Counter(left), Counter(right)
    equal = sum(x == y for x, y in zip(left, right))
    pe_numerator = sum(a[k] * b[k] for k in a.keys() | b.keys())
    po = Fraction(equal, n) if n else None
    pe = Fraction(pe_numerator, n*n) if n else None
    kappa = (po-pe)/(1-pe) if n and pe != 1 else None
    return {
        'n': n, 'identical': equal, 'different': n-equal,
        'agreement': float(po) if po is not None else None,
        'chance_agreement': float(pe) if pe is not None else None,
        'kappa': float(kappa) if kappa is not None else None,
        'kappa_exact': str(kappa) if kappa is not None else None,
        'undefined_reason': 'no pairs' if not n else 'chance agreement is one' if pe == 1 else None,
        'c1_counts': dict(sorted(a.items())), 'c2_counts': dict(sorted(b.items())),
        'confusion': {x: dict(sorted(Counter(y for u, y in zip(left, right) if u == x).items())) for x in sorted(a)},
    }


def write_table(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out = (args.output or BASE / 'raw' / f'comparison-{stamp}').resolve()
    if not out.is_relative_to(BASE) or out == BASE:
        parser.error('Output must be a new subdirectory under this directory')
    out.mkdir(parents=True, exist_ok=False)
    inputs = out / 'inputs'
    inputs.mkdir()
    names = ['c1-classes.tsv', 'c2-classes.tsv', 'residual.tsv', 'preclassified.tsv', 'compare-adjudications.tsv']
    manifest = {}
    for name in names + ['PAPER.html', 'compare.py', 'METHOD.md']:
        source = BASE.parents[1] / 'first-paper' / name if name == 'PAPER.html' else BASE / name
        data = source.read_bytes()
        (inputs / name).write_bytes(data)
        manifest[name] = hashlib.sha256(data).hexdigest()
    r = read_table(inputs / 'residual.tsv', ('id', 'machine', 'kind', 'path_or_name', 'short_evidence'))
    a = read_table(inputs / 'c1-classes.tsv', ('id', 'class', 'program_if_derivative', 'reason'))
    b = read_table(inputs / 'c2-classes.tsv', ('id', 'class', 'program_if_derivative', 'reason'))
    p = read_table(inputs / 'preclassified.tsv', ('id', 'machine', 'class'))
    adjud = read_table(inputs / 'compare-adjudications.tsv', ('id', 'resolution', 'quote', 'why', 'open_problems', 'issue_type'))
    paper = (inputs / 'PAPER.html').read_text()
    section5 = paper.split('<h2>5.', 1)[1].split('<h2>6.', 1)[0]
    section5 = ' '.join(html.unescape(re.sub('<[^>]*>', '', section5)).split())
    if not r:
        raise ValueError('No residual rows supplied')
    if set(a) != set(b) or set(a) != set(r):
        raise ValueError('Classification and residual ID sets must match exactly (no rows dropped)')
    if set(p) & set(r):
        raise ValueError('Preclassified and residual IDs overlap')
    joined = []
    for ident in sorted(r):
        x, y = a[ident], b[ident]
        ca, cb = category(x['class']), category(y['class'])
        row = dict(r[ident], c1_raw=x['class'], c2_raw=y['class'],
                   c1_class=ca, c2_class=cb, c1_owner=owner(x), c2_owner=owner(y),
                   c1_reason=x['reason'], c2_reason=y['reason'],
                   literal_disagreement=x['class'] != y['class'], class_disagreement=ca != cb,
                   either_hole=ca.startswith('hole-') or cb.startswith('hole-'))
        row['owner_disagreement'] = ca == cb == 'derivative' and row['c1_owner'] != row['c2_owner']
        joined.append(row)
    relevant = {x['id'] for x in joined if x['class_disagreement'] or x['either_hole'] or x['owner_disagreement']}
    if set(adjud) != relevant:
        raise ValueError(f'Adjudication coverage mismatch: missing={sorted(relevant-set(adjud))}, extra={sorted(set(adjud)-relevant)}')
    for row in joined:
        if row['id'] in adjud:
            decision = adjud[row['id']]
            if decision['resolution'] not in ('resolved', 'not resolved', 'no disagreement'):
                raise ValueError('Invalid resolution status')
            if (row['class_disagreement'] or row['owner_disagreement']) and decision['resolution'] == 'no disagreement':
                raise ValueError('A disagreement lacks a decision')
            if decision['resolution'] == 'resolved' and not decision['quote']:
                raise ValueError('Resolution requires an exact section 5 quotation')
            if decision['resolution'] == 'resolved' and decision['quote'] not in section5:
                raise ValueError('Resolving quotation is not in section 5')
            row.update({k: v for k, v in decision.items() if k != 'id'})
        elif row['literal_disagreement']:
            row.update(resolution='same class after label normalization', quote='',
                       why='Only class serialization differs; the derivative owner, if any, is identical.',
                       open_problems='', issue_type='label-format')
    fields = list(joined[0]) if joined else list(r[next(iter(r))])
    fields += [x for x in ('resolution', 'quote', 'why', 'open_problems', 'issue_type') if x not in fields]
    selections = {
        'joined.tsv': joined,
        'disagreements.tsv': [x for x in joined if x['class_disagreement']],
        'literal-disagreements.tsv': [x for x in joined if x['literal_disagreement']],
        'owner-disagreements.tsv': [x for x in joined if x['owner_disagreement']],
        'holes.tsv': [x for x in joined if x['either_hole']],
        'agreed-holes.tsv': [x for x in joined if x['either_hole'] and not x['class_disagreement']],
    }
    for filename, rows in selections.items():
        write_table(out / filename, rows, fields)
    result = {'created_utc': stamp, 'inputs_sha256': manifest,
              'normalization': {'recorded (works)': 'recorded', 'derivative of <program>': 'derivative'},
              'scope': f'{len(joined)} residual paired rows only; common preclassification excluded from agreement/kappa',
              'groups': {}, 'output_rows': {k: len(v) for k, v in selections.items()}}
    machines = sorted({x['machine'] for x in joined})
    for machine in machines + ['overall']:
        rows = [x for x in joined if machine == 'overall' or x['machine'] == machine]
        pre = [x for x in p.values() if machine == 'overall' or x['machine'] == machine]
        pc = Counter(category(x['class']) for x in pre)
        result['groups'][machine] = {
            'class': metrics([x['c1_class'] for x in rows], [x['c2_class'] for x in rows]),
            'literal': metrics([x['c1_raw'] for x in rows], [x['c2_raw'] for x in rows]),
            'class_and_owner': metrics(
                [x['c1_class'] + (': ' + x['c1_owner'] if x['c1_class'] == 'derivative' else '') for x in rows],
                [x['c2_class'] + (': ' + x['c2_owner'] if x['c2_class'] == 'derivative' else '') for x in rows]),
            'either_hole': sum(x['either_hole'] for x in rows),
            'owner_disagreements': sum(x['owner_disagreement'] for x in rows),
            'resolutions': dict(Counter(x.get('resolution') for x in rows if x['class_disagreement'])),
            'disagreement_issue_types': dict(sorted(Counter(x['issue_type'] for x in rows if x['class_disagreement']).items())),
            'preclassified_counts': dict(pc),
            'census_counts_c1': dict(pc + Counter(x['c1_class'] for x in rows)),
            'census_counts_c2': dict(pc + Counter(x['c2_class'] for x in rows)),
        }
    (out / 'metrics.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'output': str(out), 'output_rows': result['output_rows'],
                      'agreement': {m: result['groups'][m]['class'] for m in machines + ['overall']}}, indent=2))


if __name__ == '__main__':
    main()
