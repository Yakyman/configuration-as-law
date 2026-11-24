#!/usr/bin/env python3
"""Run the carried baseline without changing any self-test or installed mechanism."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'raw/round-0'
PEER = ROOT / 'peer'
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
steps = []

def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def save(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def run(root, argv, log):
    row = {'started_utc': utc(), 'root': str(root.relative_to(ROOT)) or '.',
           'argv': argv, 'log': log}
    print(json.dumps({'starting': row}), flush=True)
    with (OUT/log).open('wb') as stream:
        p = subprocess.run(argv, cwd=root, env=ENV, stdout=stream, stderr=subprocess.STDOUT)
    row.update(exit=p.returncode, ended_utc=utc())
    steps.append(row)
    save('steps.json', steps)
    print(json.dumps(row), flush=True)
    if p.returncode:
        raise RuntimeError('baseline stage failed: '+log)

def main():
    status = 1
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'steps.json').exists() or PEER.exists():
        raise RuntimeError('single-use controller: evidence or peer already exists')
    original = json.loads((OUT/'carried-recipe-sha256.json').read_text())
    current = {p.name:digest(p) for p in sorted((ROOT/'build').iterdir()) if p.is_file()}
    changed = [n for n in original if original[n] != current.get(n)]
    assert changed == ['lab.py'] and set(original) == set(current)
    save('recipe-provenance.json', {'utc':utc(), 'original_sha256':original,
        'relocated_sha256':current, 'changed_files':changed,
        'only_change':'lab.py: shared VM slot namespace cal-1122 -> cal-1123',
        'selftests_unchanged':all(original[n]==current[n] for n in original if 'test' in n)})
    try:
        PEER.mkdir()
        for name in ('build','downloads','keys'):
            shutil.copytree(ROOT/name, PEER/name)
        run(ROOT, ['python3','build/build.py','--server'], 'primary-build.log')
        run(PEER, ['python3','build/build.py','--server'], 'peer-build.log')
        save('build-identities.json', {'utc':utc(), 'independent_recipe_executions':True,
            'primary_image_sha256':digest(ROOT/'base/stand.qcow2'),
            'peer_image_sha256':digest(PEER/'base/stand.qcow2'),
            'recipe_inputs_equal':current == {p.name:digest(p) for p in (PEER/'build').iterdir() if p.is_file()}})
        run(ROOT, ['python3','build/round4-driver.py','baseline','--regressions','--peer-root','peer'], 'selftest-console.jsonl')
        run(ROOT, ['python3','build/assemble-channel-examples.py','raw/round-4/baseline','channel-example'], 'assembly.log')
        run(ROOT, ['python3','build/combined-selftest.py','combined','channel-example/combined','--peer-root','peer','--reboot'], 'combined-console.jsonl')
        status = 0
    except Exception as error:
        save('failure.json', {'utc':utc(), 'error_type':type(error).__name__,
                             'message':str(error).replace(str(ROOT),'[stand-root]')})
    finally:
        cleanup = []
        for root in (ROOT, PEER):
            for vm in sorted((root/'vms').glob('*')):
                if not vm.is_dir():
                    continue
                for op in ('destroy','kill','destroy'):
                    if not vm.exists():
                        break
                    with (OUT/'cleanup.log').open('ab') as stream:
                        p = subprocess.run(['python3',str(root/'lab.py'),op,vm.name], cwd=root,
                            env={**ENV,'STAND_ROOT':str(root)}, stdout=stream, stderr=subprocess.STDOUT)
                    cleanup.append({'root':str(root.relative_to(ROOT)), 'vm':vm.name, 'op':op, 'exit':p.returncode})
        for name in ('recipe.log','package-versions.txt','round-4','round-3'):
            path = ROOT/'raw'/name
            if path.exists():
                shutil.move(path, OUT/name)
        if (PEER/'raw').exists():
            shutil.copytree(PEER/'raw',OUT/'peer-build-raw')
        remaining = [str(v.relative_to(ROOT)) for root in (ROOT,PEER) for v in (root/'vms').glob('*')]
        if remaining:
            status = 1
        elif PEER.exists():
            shutil.rmtree(PEER)
        save('cleanup.json', {'utc':utc(), 'actions':cleanup, 'owned_vm_directories_remaining':remaining,
             'temporary_peer_removed':not PEER.exists(),
             'retained_image_sha256':digest(ROOT/'base/stand.qcow2') if (ROOT/'base/stand.qcow2').is_file() else None,
             'retained_image_mode':oct((ROOT/'base/stand.qcow2').stat().st_mode & 0o777) if (ROOT/'base/stand.qcow2').exists() else None})
        save('summary.json', {'utc':utc(), 'baseline_exit':status, 'steps':steps,
            'new_v4_mechanisms_built':False, 'hypothesis_outcome':'?',
            'note':'Unchanged version 3 baseline rerun; no version 4 acceptance.'})
    return status

if __name__ == '__main__':
    sys.exit(main())
