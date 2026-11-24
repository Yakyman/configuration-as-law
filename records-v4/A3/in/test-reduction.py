#!/usr/bin/env python3
"""Small synthetic regression checks; never interrogates a guest."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('reduction', Path(__file__).with_name('reduce.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def write(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    module.write_tsv(path, header, rows)

with tempfile.TemporaryDirectory(prefix='a3-reduction-') as temporary:
    root = Path(temporary)
    for base in (True, False):
        directory = root / 'raw' / ('server-base' if base else 'server')
        prefix = 'base-' if base else 'lived-'
        rows = []
        for name, kind, facts in [
            ('equal', 'package', {'reason': 'explicit', 'manager': 'test', 'large_fact': 'x' * 200000}),
            ('changed-reason', 'package', {'reason': 'explicit' if base else 'dependency'}),
            ('changed-integrity', 'package', {'reason': 'unknown'}),
            ('group-equal', 'stored', {'file': 'members/' + prefix + 'group-equal.tsv', 'count': 1, 'complete': True}),
            ('group-changed', 'stored', {'file': 'members/' + prefix + 'group-changed.tsv', 'count': 1, 'complete': True}),
            ('language', 'package', {'native_package_ids': [prefix + 'equal'], 'reason': 'unknown'}),
            ('runtime', 'process', {'record': 'same PID, different state ' + str(base)}),
        ]:
            rows.append([prefix + name, 'test-machine', '1', kind, name, json.dumps(facts), 'raw/' + prefix + 'query.out'])
        if not base:
            rows.extend([['new-1', 'test-machine', '1', 'package', 'new', '{}', 'raw/query.out'], ['new-2', 'test-machine', '1', 'package', 'new', '{}', 'raw/query.out']])
        write(directory / 'objects.tsv', ['id', 'machine', 'level', 'kind', 'name', 'members', 'evidence'], rows)
        write(directory / 'package-files.tsv', ['package', 'path', 'integrity', 'evidence', 'rule'], [[prefix + 'changed-integrity', '/test', 'unchanged' if base else 'changed', 'raw/query.out', 'full digest']])
        for name in ('group-equal', 'group-changed'):
            timestamp = '2026-11-23T00:00:00Z' if base or name == 'group-equal' else '2026-11-23T00:00:01Z'
            write(directory / 'members' / (prefix + name + '.tsv'), ['path', 'mtime', 'persistence'], [['/entry', timestamp, 'persistent']])
    counts = module.reduce(root, 'server')
    result = module.read_tsv(root / 'part-server.tsv')
    assert counts['before'] == 9 and counts['after'] == 6 and counts['dropped'] == 3, counts
    assert [r['name'] for r in result] == ['changed-reason', 'changed-integrity', 'group-changed', 'runtime', 'new', 'new']
    assert all(r['id'].startswith('server-') for r in result)
    assert list(result[0]) == module.HEADER
    # Referenced membership evidence must fail closed when missing.
    (root / 'raw/server-base/members/base-group-equal.tsv').unlink()
    try:
        module.reduce(root, 'server')
    except FileNotFoundError:
        pass
    else:
        raise AssertionError('Missing member table was silently accepted')
print('PASS: equal facts across IDs, native-owner references, reason/integrity/member/runtime changes, duplicate retention, schema, missing evidence refusal')
