"""Step 10 of the self-test of derive: reader overrides of the release's own component (build/INTERFACE.md revision
29). check-overrides.py DERIVED.jsonl PUBLISHED_DIR. For every record of /usr/lib/confos/reader-overrides/manifest.json
of the component confos-code-readers (PUBLISHED_DIR/packages/) whose package is derived (selected), the target must be
derived with the record's mode and raw SHA256 and marked as its override; for a record whose package is not selected,
the target must not be taken from the record. Exit 0 if every record holds (or the release has no such manifest)."""
import glob
import io
import json
import os
import subprocess
import sys
import tarfile

objs = {(o['kind'], o['id']): o for o in map(json.loads, open(sys.argv[1]))}
debs = sorted(glob.glob(os.path.join(sys.argv[2], 'packages', 'confos-code-readers_*.deb')))
if not debs:
    print('no confos-code-readers package in this release: nothing to check')
    sys.exit(0)
data = subprocess.run(['dpkg-deb', '--fsys-tarfile', debs[-1]], capture_output=True, check=True).stdout
man = None
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    for m in t:
        if m.name.lstrip('.') == '/usr/lib/confos/reader-overrides/manifest.json':
            man = json.loads(t.extractfile(m).read())
if man is None:
    print('the component has no override manifest (a release before revision 29): nothing to check')
    sys.exit(0)
selected = {o['id'].split(':')[0] for o in objs.values() if o['kind'] == 'package' and o.get('value')}
bad = 0
for r in man:
    o = objs.get(('file', r['target']))
    v = (o or {}).get('value') or {}
    if r['package'] in selected:
        ok = v.get('sha256') == r['sha256'] and v.get('mode') == '%04o' % (r['mode'] & 0o7777) and \
            o.get('override_of') == r['package']
    else:
        ok = not (o and o.get('override'))
    bad += not ok
    print('OK ' if ok else 'BAD', r['package'], 'selected' if r['package'] in selected else 'not selected',
          r['target'], 'derived', v.get('mode'), v.get('sha256'), 'manifest', r['mode'], r['sha256'])
print(f'{len(man)} record(s), {bad} not as required')
sys.exit(1 if bad else 0)
