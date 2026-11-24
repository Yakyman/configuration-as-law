#!/usr/bin/python3 -B
"""Prepare step-6 removal inputs; never install them or perform a case."""
import argparse
import hashlib
import json
from pathlib import Path


def rows(dev_dir=Path('/usr/local/share/stand/dev')):
    """Return existing case-3 rows and two dependency-only case-4 packages."""
    dev_dir = Path(dev_dir)
    case3 = [json.loads((dev_dir / name).read_bytes()) for name in
             ('worker-1.json', 'service.json', 'rule.json')]
    if [row['id'] for row in case3] != ['dev-worker', 'dev-service', 'dev-rule']:
        raise ValueError('unexpected inherited fixture identities')
    case4 = []
    for suffix in ('a', 'b'):
        case4.append({
            'id': 'bc4:owner-' + suffix,
            'type': 'program',
            'managed': True,
            'version': '1',
            'source': 'fixture:supplement-1-step-6-owner-' + suffix,
            'package_identity': {
                'backend': 'stand', 'name': 'bc4-owner-' + suffix, 'version': '1'},
            'files': [],
            'package_dependencies': [
                {'backend': 'stand', 'name': 'bc4-shared', 'version': '1'}],
        })
    return {'case3': case3, 'case4': case4}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dev-dir', type=Path,
                        default=Path('/usr/local/share/stand/dev'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    fixtures = rows(args.dev_dir)
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {}
    for case, values in fixtures.items():
        manifest[case] = []
        for row in values:
            filename = row['id'].replace(':', '-') + '.json'
            data = (json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode()
            (args.output / filename).write_bytes(data)
            manifest[case].append({'id': row['id'], 'file': filename,
                                   'sha256': hashlib.sha256(data).hexdigest()})
    (args.output / 'fixtures-34.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print('Removal fixture inputs prepared; no package installed and no case performed')


if __name__ == '__main__':
    main()
