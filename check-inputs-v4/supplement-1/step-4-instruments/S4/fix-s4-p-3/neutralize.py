#!/usr/bin/env python3
"""Copy an observation to a new handoff tree, mapping only listed literal fields."""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rules():
    with (HERE / 'neutral-literals.tsv').open(newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    seen = set()
    for row in rows:
        key = (row['file'], row['field'], row['old'])
        if key in seen or Path(row['file']).name != row['file']:
            raise ValueError('invalid or duplicate mapping')
        seen.add(key)
    return rows


def transform(path, entries):
    data = path.read_bytes()
    counts = collections.Counter()
    if path.suffix == '.tsv':
        rows = list(csv.reader(io.StringIO(data.decode('utf-8'), newline=''), delimiter='\t'))
        if not rows or len(rows[0]) != len(set(rows[0])):
            raise ValueError('missing or duplicate header: ' + path.name)
        header = rows[0]
        if any(entry['field'] not in header for entry in entries):
            raise ValueError('mapping field absent: ' + path.name)
        for number, row in enumerate(rows[1:], 2):
            if len(row) != len(header):
                raise ValueError('row width mismatch: ' + path.name + ':' + str(number))
            for entry in entries:
                index = header.index(entry['field'])
                if row[index] == entry['old']:
                    row[index] = entry['new']
                    counts[(entry['field'], entry['old'], entry['new'])] += 1
        if not counts:
            return data, counts
        output = io.StringIO(newline='')
        csv.writer(output, delimiter='\t', lineterminator='\n').writerows(rows)
        return output.getvalue().encode('utf-8'), counts
    value = json.loads(data)
    for entry in entries:
        parent = value
        for key in entry['field'].strip('/').split('/'):
            if not isinstance(parent, dict):
                raise ValueError('invalid summary container')
            parent = parent.get(key, {})
        if not isinstance(parent, dict):
            raise ValueError('invalid summary counters')
        if entry['old'] in parent:
            if entry['new'] in parent:
                raise ValueError('summary key collision')
            parent[entry['new']] = parent.pop(entry['old'])
            counts[(entry['field'], entry['old'], entry['new'])] += 1
    if not counts:
        return data, counts
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode('utf-8'), counts


def handoff(source, destination, report):
    source, destination, report = (Path(p).absolute() for p in (source, destination, report))
    # Reject links before resolution and never follow a file link out of the tree.
    if any(p.is_symlink() for target in (source, destination, report) for p in (target, *target.parents)):
        raise ValueError('linked paths are not accepted')
    source, destination, report = (p.resolve() for p in (source, destination, report))
    if not source.is_dir() or destination.exists() or report.exists():
        raise ValueError('source must exist; destination and report must be new')
    if any(a == b or a in b.parents for a, b in (
            (source, destination), (destination, source), (source, report), (destination, report))):
        raise ValueError('source, destination and report must be separate')
    paths = sorted(source.rglob('*'))
    if any(p.is_symlink() or not (p.is_dir() or p.is_file()) for p in paths):
        raise ValueError('source must contain only regular files and directories')
    files = [p for p in paths if p.is_file()]
    before = {p.relative_to(source).as_posix(): digest(p) for p in files}
    grouped = collections.defaultdict(list)
    for entry in rules():
        grouped[entry['file']].append(entry)
    # Validate all mapped tables before creating a deliverable tree.
    transformed = {}
    changes = []
    for name, entries in grouped.items():
        if name not in before:
            continue  # System-specific tables may be absent, including in partial observations.
        data, counts = transform(source / name, entries)
        if counts:
            transformed[name] = data
            changes.extend({'file': name, 'field': field, 'old': old, 'new': new, 'count': count}
                           for (field, old, new), count in sorted(counts.items()))
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for path in paths:
            name = path.relative_to(source).as_posix()
            target = destination / name
            if path.is_dir():
                target.mkdir(exist_ok=True)
            elif name in transformed:
                target.write_bytes(transformed[name])
            else:
                shutil.copyfile(path, target)
        after_paths = sorted(source.rglob('*'))
        if any(p.is_symlink() for p in after_paths) or after_paths != paths:
            raise ValueError('source tree changed during copy')
        if before != {p.relative_to(source).as_posix(): digest(p) for p in files}:
            raise ValueError('source bytes changed during copy')
        after = {name: digest(destination / name) for name in before}
        if any(before[name] != after[name] for name in before if name not in transformed):
            raise ValueError('unchanged-file verification failed')
        result = {'schema': 1, 'source_files': len(before),
                  'mapping_sha256': digest(HERE / 'neutral-literals.tsv'),
                  'source_unchanged': True, 'changes': changes,
                  'files': [{'path': name, 'source_sha256': before[name],
                             'handoff_sha256': after[name]} for name in sorted(before)]}
        with report.open('x') as stream:
            stream.write(json.dumps(result, indent=2) + '\n')
    except BaseException:
        shutil.rmtree(destination)
        raise
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--report', type=Path, required=True,
                        help='New audit report outside both trees; withheld from deciding parties')
    args = parser.parse_args()
    result = handoff(args.source, args.destination, args.report)
    print(json.dumps({'source_files': result['source_files'],
                      'mapped_fields': sum(row['count'] for row in result['changes']),
                      'source_unchanged': True}))
