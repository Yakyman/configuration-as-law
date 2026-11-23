#!/usr/bin/env python3
"""Wait for the two corrected builds, record provenance, run the complete suite."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

root = Path(__file__).resolve().parent.parent
peer = root.parent/'round-4-peer'
raw = root/'raw'
units = ('bc4-final2-build-a.service', 'bc4-final2-build-b.service')
def state(unit):
    return dict(line.split('=', 1) for line in subprocess.check_output([
        'systemctl', '--user', 'show', unit, '--property=Result',
        '--property=ActiveState'], text=True).splitlines())
while any(state(unit)['ActiveState'] in ('active', 'activating') for unit in units):
    time.sleep(5)
assert all(state(unit)['Result'] == 'success' for unit in units)

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def normalized(value):
    if isinstance(value, dict):
        return {k:normalized(v) for k,v in value.items()}
    if isinstance(value, list):
        return [normalized(v) for v in value]
    if isinstance(value, str):
        return value.replace(str(root.parent), 'stand')
    return value

builds = {}
factory = {}
for directory,unit in zip((root,peer), units):
    image = directory/'base/stand.qcow2'
    builds[directory.name] = {
        'build_result': state(unit)['Result'],
        'image_sha256': digest(image),
        'image': normalized(json.loads(subprocess.check_output([
            'qemu-img', 'info', '--output=json', str(image)], text=True))),
        'recipe_files_sha256': {p.name:digest(p) for p in sorted((directory/'build').iterdir()) if p.is_file()},
        'recipe_log_sha256': digest(directory/'raw/recipe.log'),
    }
    factory[directory.name] = dict((name,sha) for sha,name in re.findall(
        r'^([a-f0-9]{64})  (/etc/stand/factory/(?:machine\.jsonl|base-files\.json)|/boot/initrd\.img-[^\s]+)$',
        (directory/'raw/rebuild-final.log').read_text(), re.M))
recipe_equal = builds[root.name]['recipe_files_sha256'] == builds[peer.name]['recipe_files_sha256']
provenance = {'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
              'builds':builds, 'recipe_files_equal':recipe_equal,
              'source_date_epoch':1794787200}
(raw/'final-build-provenance.json').write_text(json.dumps(provenance,indent=2,sort_keys=True)+'\n')
factory_equal = len(factory[root.name]) >= 3 and factory[root.name] == factory[peer.name]
comparison = {'expected':'both clean builds emit identical complete factory and initramfs hashes',
              'source_date_epoch':1794787200, 'files_sha256':factory,
              'passed':factory_equal, 'recipe_files_equal':recipe_equal}
(raw/'build-factory-comparison.json').write_text(json.dumps(comparison,indent=2,sort_keys=True)+'\n')
print(json.dumps(comparison,sort_keys=True),flush=True)
assert recipe_equal and factory_equal, 'corrected independent build requirements differ'
commands = [
    (['build/round4-driver.py','rebuilt','--regressions','--peer-root',str(peer)],'final-suite-console.jsonl'),
    (['build/assemble-channel-examples.py','raw/round-4/rebuilt','channel-example'],'assembly-final.json'),
    (['build/combined-selftest.py','combined','channel-example/combined','--peer-root',str(peer),'--reboot'],'combined-final-console.jsonl'),
]
for argv,filename in commands:
    with (raw/filename).open('wb') as stream:
        result = subprocess.run([sys.executable,*argv],cwd=root,stdout=stream,stderr=subprocess.STDOUT)
    print(json.dumps({'stage':argv[0],'exit':result.returncode}),flush=True)
    if result.returncode:
        sys.exit(result.returncode)
