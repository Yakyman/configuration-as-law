#!/usr/bin/env python3
"""VM-only real-browser supplement to fixed Check 4, both archive settings.
Records browser-created files outside assigned state instead of ignoring them.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import runpy

assert os.geteuid()==0 and Path('/run/cal.sock').exists(), 'disposable VM only'
helpers=runpy.run_path(str(Path(__file__).with_name('check-lifecycle.py')))
emit,ctl,reset=helpers['emit'],helpers['ctl'],helpers['reset']
failures=[]

def check(ok,label,**fields):
    if not ok: failures.append(label)
    emit('browser-assertion',label=label,passed=bool(ok),**fields)

def files(root):
    result={}
    if not root.exists(): return result
    for p in sorted(root.rglob('*')):
        if p.is_symlink(): result[str(p.relative_to(root))]={'link':os.readlink(p)}
        elif p.is_file(): result[str(p.relative_to(root))]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    return result

for mode in ('keep','delete'):
    emit('browser-case-start',archive=mode)
    reset()
    emit('browser-owner-scope',base_browser_packages=[line for line in Path('/etc/cal/base-packages.tsv').read_text().splitlines() if line.split('\t')[0].startswith('chromium')],
         qualification='Removing the catalog browser entry does not uninstall base Chromium. Empty catalog programs alone does not prove all program owners absent under the full declaration; this is an archival coverage probe, not an automatic fixed-condition verdict.')
    doc=dict(archive=mode,programs={'browser':dict(version='1',scope='user',owners=['alice'])},policies={},allow_channels={},shared={})
    Path('/etc/cal/root.json').write_text(json.dumps(doc))
    initial=ctl('apply')
    home=Path('/home/alice')
    before=files(home)
    command=['runuser','-u','alice','--','/usr/local/bin/cal-login','-c',
        '/usr/lib/chromium/chromium --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=/var/lib/cal/active/browser --dump-dom http://127.0.0.1:8080/']
    p=subprocess.run(command,capture_output=True,text=True,timeout=60)
    emit('browser-command',argv=command,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    if p.returncode!=0 or 'CAL browser fixture' not in p.stdout: raise RuntimeError('browser setup failed')
    managed=files(Path('/var/lib/cal/active/browser'))
    managed.pop('version',None)
    after=files(home)
    outside={key:value for key,value in after.items() if key not in before}
    changed={key:value for key,value in after.items() if key in before and value!=before[key]}
    emit('browser-created-files',archive=mode,managed=managed,new_home_files=outside,changed_home_files=changed)
    check(bool(managed),'browser produced managed derivatives',archive=mode)
    doc['programs']={}
    Path('/etc/cal/root.json').write_text(json.dumps(doc))
    ctl('apply')
    archived=files(Path('/var/lib/cal/archive/browser'))
    archived.pop('version',None)
    check(not Path('/var/lib/cal/active/browser').exists() and archived==managed,'managed derivatives archived intact with saved generation',archive=mode)
    surviving={key:files(home).get(key) for key in outside if (home/key).exists() or (home/key).is_symlink()}
    # Test catalog archival coverage, preserving the base-vs-catalog owner boundary.
    # Do not infer owner absence under the full declaration from the empty map.
    check(not surviving,'catalog removal archives new Chromium home files',archive=mode,surviving=surviving,
          current=json.loads(Path('/var/lib/cal/current.json').read_text()))
    helpers['gc_saved']()
    check(Path('/var/lib/cal/archive/browser').exists()==(mode=='keep'),'browser archive setting honored after gc',archive=mode)
    if mode=='keep':
        retained=files(Path('/var/lib/cal/archive/browser'));retained.pop('version',None)
        check(retained==managed,'kept browser archive bytes unchanged',archive=mode)
    emit('browser-case-end',archive=mode,remaining_home_files={key:files(home).get(key) for key in outside})
    # Only fresh files generated in this disposable probe; evidence precedes cleanup.
    for key in outside:
        (home/key).unlink(missing_ok=True)
    emit('fixture-cleanup',removed_new_home_files=sorted(outside))
emit('browser-SUMMARY',failures=failures,failure_count=len(failures),note='Catalog archival coverage observations. Base Chromium remains installed/recorded; full-declaration owner absence is not established. Not a property-inherent counterexample.')
raise SystemExit(bool(failures))
