#!/usr/bin/python3
"""Run ONLY as root in disposable VM after daemon/hook/worker installation.
Writes JSON-lines evidence to stdout; stops at first failed invariant with traceback.
Worker contract: worker --read-shared FILE prints file bytes and exits zero.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import pwd
import subprocess
import traceback

BASE = Path('/var/lib/cal')
ROOT = Path('/etc/cal/root.json')
IDS = ('alpha', 'beta', 'shared-cache')

def emit(event, **fields):
    print(json.dumps(dict(event=event, **fields), sort_keys=True), flush=True)

def check(condition, label, **fields):
    emit('assertion', label=label, passed=bool(condition), **fields)
    if not condition:
        raise AssertionError(label)

def ctl(*args):
    command = ['/usr/local/bin/calctl', *args]
    p = subprocess.run(command, capture_output=True, text=True, timeout=180)
    emit('command', argv=command, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)
    check(p.returncode == 0, 'calctl succeeded', argv=command)
    result = json.loads(p.stdout)
    check(result.get('ok') is True, 'daemon reports success', argv=command)
    return result

def write(path, doc):
    path.write_text(json.dumps(doc, sort_keys=True, indent=2) + '\n')
    emit('declaration-write', path=str(path), document=doc)

def declaration(mode, programs):
    return dict(archive=mode,
                programs={ident:dict(version='1', scope='system', owners=[]) for ident in programs},
                policies={}, allow_channels={}, shared={'cache':['alpha','beta']})

def configure(mode, programs):
    write(ROOT, declaration(mode, programs))
    return ctl('apply')

def snapshot(label):
    entries=[]
    for area in ('active','archive'):
        root=BASE/area
        for path in sorted(root.rglob('*')):
            st=path.lstat()
            entry=dict(path=str(path), inode=st.st_ino, mode=oct(st.st_mode), uid=st.st_uid, gid=st.st_gid)
            if path.is_symlink(): entry['link']=os.readlink(path)
            elif path.is_file():
                data=path.read_bytes()
                entry.update(size=len(data), sha256=hashlib.sha256(data).hexdigest(), bytes_base64=base64.b64encode(data).decode())
            entries.append(entry)
    emit('snapshot', label=label, entries=entries)
    return entries

def gc_saved():
    status=ctl('status')
    current=status['current']['generation']
    generations=[g for g in status['generations'] if g != current]
    # Log full generation contents before deletion, proving coverage of all owners.
    for generation in generations:
        emit('generation-before-gc', generation=generation, document=json.loads((BASE/'generations'/(generation+'.json')).read_text()))
    if generations: ctl('gc', *generations)
    return generations

def reset():
    for user in ('alice','bob'):
        account=pwd.getpwnam(user)
        write(Path(account.pw_dir)/'declaration.json', {'programs':{}})
    configure('delete', [])
    gc_saved()
    status=ctl('status')
    check(not status['active'] and not status['archive'], 'declarative reset left no active/archive state')

def read_shared(program, stage):
    path=BASE/'active'/'shared-cache'/'cache'
    command=['/usr/local/lib/cal/'+program,'--read-shared',str(path)]
    p=subprocess.run(command, capture_output=True, timeout=10)
    emit('shared-consumer', program=program, stage=stage, argv=command, returncode=p.returncode,
         stdout_base64=base64.b64encode(p.stdout).decode(), stderr=p.stderr.decode(errors='replace'),
         qualification='separately installed alpha/beta executables; common fixture implementation; root/system scope')
    check(p.returncode==0 and p.stdout==path.read_bytes(), 'shared derivative consumed successfully', program=program, stage=stage)

def run(mode):
    emit('case-start', archive=mode)
    reset()
    initial=configure(mode, ['alpha','beta'])
    generation=initial['generation']
    original={}
    for ident in IDS:
        path=BASE/'active'/ident
        check(path.is_dir(), 'declared state directory exists', ident=ident)
        original[ident]=dict(inode=path.stat().st_ino, cache=(path/'cache').read_bytes())
    snapshot(mode+' initial')
    read_shared('alpha','both-present'); read_shared('beta','both-present')

    configure(mode, ['beta'])
    snapshot(mode+' alpha-removed')
    check(not (BASE/'active'/'alpha').exists() and (BASE/'archive'/'alpha').is_dir(), 'removed alpha archived with saved generation')
    check((BASE/'archive'/'alpha'/'cache').read_bytes()==original['alpha']['cache'], 'archived alpha cache unchanged')
    check((BASE/'active'/'shared-cache').stat().st_ino==original['shared-cache']['inode'], 'shared state stays active with beta')
    read_shared('beta','alpha-removed')

    ctl('rollback', generation)
    snapshot(mode+' rollback')
    for ident in IDS:
        path=BASE/'active'/ident
        check(path.is_dir() and path.stat().st_ino==original[ident]['inode'], 'rollback restored same directory', ident=ident)
        check((path/'cache').read_bytes().startswith(original[ident]['cache']), 'rollback preserved cache prefix', ident=ident)
    check((BASE/'active'/'shared-cache'/'cache').read_bytes()==original['shared-cache']['cache'], 'rollback did not overwrite shared cache')

    configure(mode, ['beta'])
    read_shared('beta','alpha-removed-after-rollback')
    configure(mode, [])
    snapshot(mode+' all-removed-before-gc')
    for ident in IDS:
        check(not (BASE/'active'/ident).exists() and (BASE/'archive'/ident).is_dir(), 'all owner absence archives derivative before gc', ident=ident)
        check((BASE/'archive'/ident/'cache').read_bytes().startswith(original[ident]['cache']), 'saved generations retain program-created cache', ident=ident)
    gc_saved()
    snapshot(mode+' all-removed-after-gc')
    for ident in IDS:
        path=BASE/'archive'/ident
        check(path.exists()==(mode=='keep'), 'archive setting honored after last owning generation gc', ident=ident, archive=mode)
        if mode=='keep': check((path/'cache').read_bytes().startswith(original[ident]['cache']), 'keep retained program-created cache', ident=ident)
    emit('case-result', archive=mode, outcome='1')

if __name__=='__main__':
    try:
        check(os.geteuid()==0, 'guest root required')
        for mode in ('keep','delete'): run(mode)
        emit('check4-result', outcome='1', scope='worker-created alpha/beta cache; controller-created shared fixture consumed by both workers; ownership supplied externally')
    except Exception as exc:
        emit('check4-result', outcome='?', stand_failure=str(exc), traceback=traceback.format_exc())
        raise
