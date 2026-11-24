#!/usr/bin/env python3
"""Compare ed's dpkg maintainer-script files across saved observations and the two committed ed packages."""
import hashlib
import io
import json
import lzma
import sys
import tarfile

NAMES = ['/var/' + 'lib/dpkg/info/ed.' + x for x in ('postinst', 'prerm', 'list', 'md5sums')] + \
        ['/var/' + 'lib/dpkg/alternatives/editor', '/etc/alternatives/editor']


def deb_control(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'!<arch>\n'
    pos, out = 8, {}
    while pos < len(data):
        name = data[pos:pos + 16].decode().strip()
        size = int(data[pos + 48:pos + 58].decode().strip())
        body = data[pos + 60:pos + 60 + size]
        pos += 60 + size + (size % 2)
        if name.startswith('control.tar'):
            raw = lzma.decompress(body) if name.endswith('.xz') else body
            with tarfile.open(fileobj=io.BytesIO(raw)) as t:
                for m in t.getmembers():
                    if m.isfile():
                        out[m.name.lstrip('./')] = hashlib.sha256(t.extractfile(m).read()).hexdigest()
    return out


result = {'packages': {p: deb_control(p) for p in sys.argv[1:3]}, 'observations': {}}
for obs in sys.argv[3:]:
    with lzma.open(obs) as stream:
        o = json.load(stream)
    if 'disconnected_observation' in o:
        o = o['disconnected_observation']
    f = o['independent_census']['files']
    rel = o['p1_file_relations']
    result['observations'][obs] = {n: {k: f.get(n, {}).get(k) for k in ('kind', 'mode', 'sha256', 'target', 'st_mtime')}
                                   | {'claims': [c['line'] for c in rel.get(n, {}).get('own_line_comparisons', [])]}
                                   for n in NAMES}
    result['observations'][obs]['ed_dpkg_query'] = [x['stdout'] for x in o['independent_census']['queries'][:1]][0].count('\n')
print(json.dumps(result, indent=1))
