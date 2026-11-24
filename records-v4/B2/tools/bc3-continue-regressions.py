#!/usr/bin/env python3
"""Run only the unattempted carried regression suffix on the frozen BC3 image."""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'raw/round-3/final-1-continuation'
NAME = 'bc3-final-1-regression-suffix'
EXPECTED_IMAGE = '5641c3c34e08dba60ae7f97511fae33d4dde48dba0ef5d93db93ab6faeb3cb79'
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'STAND_ROOT': str(ROOT),
       'STAND_LEGACY': '1', 'LAB_RUN_TIMEOUT': '7200'}
steps = []


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run(args, name, script=None):
    record = {'started_utc': utc(), 'argv': [str(a).replace(str(ROOT), '[stand-root]') for a in args],
              'log': name, 'expected_exit': 0}
    print(json.dumps({'phase': 'expected', **record}), flush=True)
    with (OUT / name).open('wb') as output:
        result = subprocess.run(args, cwd=ROOT, env=ENV,
                                input=script.encode() if script is not None else None,
                                stdout=output, stderr=subprocess.STDOUT)
    record.update(ended_utc=utc(), exit=result.returncode)
    steps.append(record)
    save('steps.json', steps)
    print(json.dumps({'phase': 'result', **record}), flush=True)
    return result.returncode


def lab(operation, name, script=None, extra=()):
    return run([sys.executable, 'lab.py', operation, NAME, *extra], name, script)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    if (ROOT / 'vms' / NAME).exists():
        raise RuntimeError('continuation guest name already exists')
    image_hash = digest(ROOT / 'base/stand.qcow2')
    save('image.json', {'sha256': image_hash, 'expected_sha256': EXPECTED_IMAGE,
                        'unchanged': image_hash == EXPECTED_IMAGE})
    if image_hash != EXPECTED_IMAGE:
        raise RuntimeError('frozen image identity changed')
    sources = {
        'round2-continuation.py': ROOT / 'raw/round-3/parts/round2-continuation.py',
        'round2-selftest.py': ROOT / 'build/round2-selftest.py',
        'round2-probe.c': ROOT / 'build/round2-probe.c',
    }
    snapshot_sources = {**sources, 'host-controller.py': Path(__file__).resolve()}
    save('input-sha256.json', {name: digest(path) for name, path in snapshot_sources.items()})
    for name, path in snapshot_sources.items():
        (OUT / name).write_bytes(path.read_bytes())
    status = 1
    try:
        if lab('new', 'new.log', extra=['stand']):
            raise RuntimeError('fresh guest setup failed')
        copying = ['import base64,pathlib']
        for name, path in sources.items():
            if name != 'round2-continuation.py':
                continue
            data = base64.b64encode(path.read_bytes()).decode()
            copying.append('pathlib.Path(' + repr('/tmp/' + name) +
                           ').write_bytes(base64.b64decode(' + repr(data) + '))')
        if lab('run', 'copy.log', "python3 -I - <<'COPY'\n" + '\n'.join(copying) +
               '\nCOPY\n', extra=['--root']):
            raise RuntimeError('source delivery failed')
        status = lab('run', 'suffix.jsonl',
                     'python3 -B /tmp/round2-continuation.py\n', extra=['--root'])
        status |= lab('copy-out', 'export.log', extra=[
            '/var/lib/stand/bc3-round2-continuation', str(OUT / 'evidence')])
    finally:
        if (ROOT / 'vms' / NAME).exists():
            cleanup = lab('destroy', 'destroy.log')
            if cleanup:
                lab('kill', 'kill.log')
                cleanup = lab('destroy', 'destroy-after-kill.log')
            status |= cleanup
        save('summary.json', {
            'utc': utc(), 'controller_exit': status,
            'owned_guest_remaining': (ROOT / 'vms' / NAME).exists(),
            'steps': steps,
            'scope': 'unattempted suffix only; prior FIFO failure and original aborted suite remain',
            'hypothesis_outcome': '?',
        })
    return status


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        detail = str(error).replace(str(ROOT), '[stand-root]').replace(str(Path.home()), '[host-home]')
        if OUT.exists():
            save('failure.json', {'utc': utc(), 'error': detail})
        print(json.dumps({'phase': 'failure', 'error': detail}), flush=True)
        sys.exit(1)
