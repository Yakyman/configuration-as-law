#!/usr/bin/env python3
"""Subtract only base objects with identical identity and recorded facts."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

csv.field_size_limit(1024 * 1024 * 1024)
HEADER = ['id', 'part', 'machine', 'kind', 'name', 'members', 'evidence']

def read_tsv(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def encoded(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))

class Inventory:
    def __init__(self, directory):
        self.directory = directory
        self.rows = read_tsv(directory / 'objects.tsv')
        self.identities = {r['id']: [r['level'], r['kind'], r['name']] for r in self.rows}
        if len(self.identities) != len(self.rows):
            raise ValueError('Duplicate source object ID')
        self.package_files = collections.defaultdict(list)
        for row in read_tsv(directory / 'package-files.tsv'):
            self.package_files[row['package']].append({k: v for k, v in row.items() if k not in ('package', 'evidence')})

    def facts(self, row):
        value = json.loads(row['members'])
        # A member-file locator encodes a machine-dependent ID, not a fact.
        if isinstance(value, dict) and isinstance(value.get('file'), str) and value['file'].startswith('members/'):
            value = dict(value)
            relative = value.pop('file')
            member_path = (self.directory / relative).resolve()
            if not member_path.is_relative_to((self.directory / 'members').resolve()):
                raise ValueError('Member reference outside members directory')
            value['member_rows'] = sorted(read_tsv(member_path), key=encoded)
        # Native package IDs likewise name objects rather than facts. Resolve only
        # this documented field, leaving every other string/field untouched.
        if isinstance(value, dict) and 'native_package_ids' in value:
            value = dict(value)
            value['native_package_ids'] = sorted([self.identities[i] for i in value['native_package_ids']], key=encoded)
        return {'members': value, 'package_files': sorted(self.package_files.get(row['id'], []), key=encoded)}

    def key(self, row):
        return encoded([row['level'], row['kind'], row['name'], self.facts(row)])

def write_tsv(path, header, rows):
    with path.open('w', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)

def reduce(root, machine):
    lived = Inventory(root / 'raw' / machine)
    base = Inventory(root / 'raw' / (machine + '-base'))
    matches = collections.defaultdict(list)
    for row in base.rows:
        matches[base.key(row)].append(row['id'])
    output, audit = [], []
    before, after = collections.Counter(), collections.Counter()
    for row in lived.rows:
        kind = row['level'] + ':' + row['kind']
        before[kind] += 1
        key = lived.key(row)
        equal = matches.get(key, [])
        audit.append([row['id'], 'drop' if equal else 'keep', ';'.join(equal), hashlib.sha256(key.encode()).hexdigest()])
        if equal:
            continue
        after[kind] += 1
        # Preserve source fields verbatim; evidence adds an unambiguous source
        # row and inventory root for all original relative references.
        evidence = 'raw/' + machine + '/objects.tsv#' + row['id'] + '; inventory_root=raw/' + machine + '; ' + row['evidence']
        output.append([machine + '-' + row['id'], 'A3', machine, kind, row['name'], row['members'], evidence])
    write_tsv(root / ('part-' + machine + '.tsv'), HEADER, output)
    write_tsv(root / ('reduction-' + machine + '.tsv'), ['source_id', 'decision', 'matching_base_ids', 'facts_sha256'], audit)
    result = {'machine': machine, 'base_objects': len(base.rows), 'before': len(lived.rows), 'after': len(output), 'dropped': len(lived.rows) - len(output), 'by_kind': {kind: {'before': before[kind], 'after': after[kind]} for kind in sorted(before)}}
    (root / ('counts-' + machine + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('machines', nargs='*', choices=['developer', 'gaming', 'server'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    for machine in args.machines or ['developer', 'gaming', 'server']:
        print(json.dumps(reduce(args.root, machine), sort_keys=True))
