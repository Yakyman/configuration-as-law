#!/usr/bin/env python3
"""Match structural object keys only; never import prior decisions or explanations."""
import argparse
import collections
import csv
import pathlib
import re
import sys

SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')
UUID = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
NETWORK = re.compile(r'^(.*):(' + UUID + r'):([^:]*):([^:]*)$')


def read(path):
    with path.open(newline='', encoding='utf-8') as source:
        yield from csv.DictReader(source, delimiter='\t')


def canonical_machine(value, mappings):
    if value in mappings:
        return mappings[value]
    for system in SYSTEMS:
        if value in (system, 'd1-' + system, 'd1b-' + system):
            return system
    raise ValueError('Unmapped machine identifier; provide --machine-map for its exact value')


def row(source, mappings):
    kind = source['kind']
    if not re.match(r'^L[12]:', kind):
        level = str(source.get('level', ''))
        if level not in ('1', '2'):
            raise ValueError('A new raw inventory row requires level 1 or 2')
        kind = 'L' + level + ':' + kind
    # Intentionally do not access members, source, evidence or missing_facts.
    return (source['id'], canonical_machine(source['machine'], mappings), kind, source['name'])


def exact_key(item):
    return item[1:]


def normalized_key(item):
    ident, machine, kind, name = item
    if kind == 'L1:saved-network':
        match = NETWORK.fullmatch(name)
        if match:
            return (machine, kind, (match[1], '<connection-uuid>', match[3], match[4]))
    return None


def unique_rows(items):
    result = {}
    for item in items:
        if item[0] in result and result[item[0]] != item:
            raise ValueError('One id refers to different structural objects')
        if item[0] in result:
            raise ValueError('Duplicate object id in inventory')
        result[item[0]] = item
    return list(result.values())


def match_rows(old, new):
    old_exact = collections.defaultdict(list)
    new_exact = collections.defaultdict(list)
    old_normal = collections.defaultdict(list)
    new_normal = collections.defaultdict(list)
    for item in old:
        old_exact[exact_key(item)].append(item)
        if normalized_key(item) is not None: old_normal[normalized_key(item)].append(item)
    for item in new:
        new_exact[exact_key(item)].append(item)
        if normalized_key(item) is not None: new_normal[normalized_key(item)].append(item)
    matched, unmatched, used = [], [], set()
    for item in sorted(old):
        key=exact_key(item);candidates=new_exact[key];rule='exact-name'
        if len(old_exact[key]) != 1:
            unmatched.append([*item, 'ambiguous-first-night-key',len(candidates)]);continue
        if not candidates and normalized_key(item) is not None:
            key=normalized_key(item);candidates=new_normal[key];rule='saved-network-uuid'
            if len(old_normal[key]) != 1:
                unmatched.append([*item,'ambiguous-first-night-normalized-key',len(candidates)]);continue
        if len(candidates) != 1:
            unmatched.append([*item,'no-candidate' if not candidates else 'ambiguous-new-key',len(candidates)]);continue
        target=candidates[0]
        if target[0] in used:
            unmatched.append([*item,'new-id-already-matched',1]);continue
        used.add(target[0]);matched.append([item[0],target[0],item[1],item[2],item[3],target[3],rule])
    return matched, unmatched


def write(path, columns, rows):
    with path.open('w',newline='',encoding='utf-8') as output:
        writer=csv.writer(output,delimiter='\t',lineterminator='\n');writer.writerow(columns);writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory',type=pathlib.Path)
    parser.add_argument('unknown',type=pathlib.Path)
    parser.add_argument('additional_unknown',type=pathlib.Path)
    parser.add_argument('output',type=pathlib.Path)
    parser.add_argument('--machine-map',action='append',default=[],metavar='EXACT=SYSTEM')
    args=parser.parse_args();csv.field_size_limit(536870912)
    mappings={}
    for setting in args.machine_map:
        source,sep,target=setting.partition('=')
        if not sep or not source or target not in SYSTEMS:parser.error('Invalid --machine-map')
        if source in mappings and mappings[source]!=target:parser.error('Conflicting --machine-map')
        mappings[source]=target
    paths=[args.inventory]
    if args.inventory.is_dir():
        paths=[args.inventory/'objects.tsv'] if (args.inventory/'objects.tsv').is_file() else sorted(args.inventory.glob('*/objects.tsv'))
        if not paths:parser.error('No objects.tsv inputs found')
    try:
        old=unique_rows(row(item,mappings) for p in (args.unknown,args.additional_unknown) for item in read(p))
        new=unique_rows(row(item,mappings) for p in paths for item in read(p))
        matched,unmatched=match_rows(old,new)
        args.output.mkdir(parents=True,exist_ok=False)
        write(args.output/'matched.tsv',['first_id','new_id','machine','kind','first_name','new_name','match_rule'],matched)
        write(args.output/'unmatched.tsv',['first_id','machine','kind','first_name','match_status','candidate_count'],unmatched)
    except (ValueError,KeyError,OSError,csv.Error) as exc:
        parser.exit(2,'match: '+str(exc)+'\n')
    print(f'matched={len(matched)} unmatched={len(unmatched)}')

if __name__ == '__main__':
    main()
