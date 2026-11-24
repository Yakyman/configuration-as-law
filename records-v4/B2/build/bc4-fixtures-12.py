#!/usr/bin/python3 -B
"""Prepare two exact account-creating package artifacts; never install them."""
import argparse
import base64
import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n'


def fixture(label, uid):
    name = 'bc4' + label
    account = dict(id='bc4-account-' + label, type='account', managed=True,
                   name=name, uid=uid, gid=uid, groups=[name],
                   shell='/usr/sbin/nologin', home='/home/' + name,
                   gecos='BC4 ' + label + ' account')
    payload = canonical(account).encode()
    package = dict(id='bc4-package-' + label, type='program', managed=True,
                   version='1', source='builder-source:bc4-account-' + label,
                   package_identity=dict(backend='stand', name='bc4-account-' + label, version='1'),
                   package_contribution_ids=[account['id']],
                   files=[dict(path='/opt/stand/pkgs/bc4-account-' + label + '/share/account.json',
                               kind='file', mode=0o444, uid=0, gid=0,
                               sha256=hashlib.sha256(payload).hexdigest(),
                               content_b64=base64.b64encode(payload).decode())])
    return dict(format='stand-package-bundle-v1', package=package, rows=[account])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs='?', default='/usr/local/share/stand/bc4')
    args = parser.parse_args()
    directory = Path(args.output)
    directory.mkdir(parents=True, exist_ok=True)
    combined = []
    for label, uid in [('alpha', 2201), ('beta', 2202)]:
        artifact = fixture(label, uid)
        (directory / ('package-' + label + '.json')).write_text(canonical(artifact))
        rows = [artifact['package']] + artifact['rows']
        (directory / ('rows-' + label + '.jsonl')).write_text(''.join(map(canonical, rows)))
        combined.extend(rows)
    (directory / 'case-2a-rows.jsonl').write_text(''.join(map(canonical, combined)))
    print('BC4 account package artifacts prepared; no package installed')


if __name__ == '__main__':
    main()
