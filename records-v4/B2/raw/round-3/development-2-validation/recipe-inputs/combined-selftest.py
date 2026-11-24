#!/usr/bin/env python3
"""Apply one exact combined BC4 declaration to two separately rebuilt images.

No VM is created by importing this module. Invoke on the server after both
recipe builds and the successful channel-export assembly have finished.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {'repository:hello','system:base-state','language:pip:development',
            'language:npm:development','language:pip:native-development',
            'round4-flatpak','round4-appimage','round4-oci-image','round4-oci',
            'import:downloaded','source:source-example','import:source-example-built',
            'dev-worker','dev-service','round4-user-timer',
            'schedule:scheduled-example:service','schedule:scheduled-example:timer',
            'dev-wifi','dev-bluetooth'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase')
    parser.add_argument('declaration', type=Path)
    parser.add_argument('--peer-root', type=Path, required=True)
    parser.add_argument('--reboot', action='store_true', help='also verify exact declaration after a clean reboot')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,39}', args.phase):
        parser.error('fresh alphanumeric/hyphen phase of at most 40 characters required')
    peer = args.peer_root.resolve()
    source = args.declaration.resolve()
    if peer == ROOT or (peer/'base/stand.qcow2').resolve() == (ROOT/'base/stand.qcow2').resolve():
        parser.error('peer must contain a separate independently rebuilt image')
    for root in (ROOT,peer):
        if not (root/'lab.py').is_file() or not (root/'base/stand.qcow2').is_file():
            parser.error('both roots must contain their lab and finished image')
    members = sorted(source.iterdir())
    if not members or any(p.is_symlink() or not p.is_file() or not re.fullmatch(r'[A-Za-z0-9_.-]+',p.name) for p in members):
        parser.error('declaration must contain only regular top-level files with safe names')
    payload = {p.name:p.read_bytes() for p in members}
    rows = [json.loads(line) for line in payload['machine.jsonl'].decode().splitlines() if line.strip()]
    ids = [row['id'] for row in rows]
    if len(ids)!=len(set(ids)) or not REQUIRED.issubset(ids):
        parser.error('complete assembled declaration must contain each required BC4 row exactly once')
    digests = {n:hashlib.sha256(b).hexdigest() for n,b in payload.items()}
    out = ROOT/'raw/round-4'/args.phase
    out.mkdir(parents=True,exist_ok=False)
    events = (out/'events.jsonl').open('w',buffering=1)
    status = 0
    owned = []
    snapshots = {}
    results = {}
    provenance = {'declaration_files_sha256':digests,'declaration_rows':len(rows),
                  'channel_row_ids':sorted(REQUIRED),'reboot_requested':args.reboot,
                  'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'images':{}}

    def event(**row):
        row['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        text=json.dumps(row,sort_keys=True)
        events.write(text+'\n');print(text,flush=True)

    def run(root,argv,log,script=None,timeout=3600):
        nonlocal status
        try:
            with (out/log).open('wb') as stream:
                process=subprocess.Popen(list(map(str,argv)),cwd=root,stdin=subprocess.PIPE,
                    stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,
                    env={**os.environ,'STAND_ROOT':str(root),'PYTHONDONTWRITEBYTECODE':'1'})
                try:
                    process.communicate(script.encode() if isinstance(script,str) else script,timeout=timeout)
                except BaseException:
                    try:os.killpg(process.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                    process.wait();raise
            rc=process.returncode
        except subprocess.TimeoutExpired:
            rc=124
        except OSError:
            rc=127
        if rc:status=1
        event(phase='result',log=log,rc=rc)
        return rc

    def lab(root,name,op,log,*extra,script=None):
        return run(root,[sys.executable,root/'lab.py',op,name,*extra],log,script,
                   timeout=3600 if op=='run' else 360)

    def guest(root,name,script,log):
        return lab(root,name,'run',log,'--root',script=script)

    def cleanup(root,name,label):
        if not (root/'vms'/name).exists():return
        if lab(root,name,'destroy',label+'-destroy.log'):
            lab(root,name,'kill',label+'-kill.log')
            lab(root,name,'destroy',label+'-destroy-after-kill.log')

    # No shell reconstructs or substitutes declaration bytes; both guests get
    # the same in-memory payload captured before the first VM starts.
    encoded={n:base64.b64encode(b).decode() for n,b in payload.items()}
    delivery="python3 -I - <<'DELIVER'\nimport base64,pathlib\np=pathlib.Path('/var/lib/stand/combined-input');p.mkdir()\n"
    delivery+='data='+repr(encoded)+'\n'
    delivery+="for name,text in data.items():(p/name).write_bytes(base64.b64decode(text,validate=True))\nDELIVER\n"
    exact="python3 -I - <<'EXACT'\nimport hashlib,json,pathlib\np=pathlib.Path('/var/lib/stand/current').resolve()\n"
    exact+='expected='+repr(digests)+'\n'
    exact+="actual={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}\nprint(json.dumps({'id':'COMBINED-EXACT-DECLARATION','passed':actual==expected,'files_sha256':actual},sort_keys=True))\nassert actual==expected\nEXACT\n"
    launches=[
        ('repository',['run','/opt/stand/pkgs/repository-hello/usr/bin/hello'],'Hello, world!'),
        ('updated-base',['run','/usr/bin/ed'],'GNU ed 1.21.1'),
        ('pip',['run','/opt/stand/pkgs/pip-development/main.py'],'PIP_POSITIVE 2026'),
        ('npm',['run','/opt/stand/pkgs/npm-development/main.js'],'NPM_POSITIVE true'),
        ('native-wheel',['run','/opt/stand/pkgs/pip-native-development/main.py'],'NATIVE_POSITIVE abc'),
        ('flatpak',['broker','flatpak','run','round4-flatpak'],'RECORDED_APPLICATION_OK'),
        ('appimage',['broker','stand-appimage','run','round4-appimage'],'RECORDED_APPLICATION_OK'),
        ('oci',['broker','podman','run','round4-oci'],'EXISTING_NONENTRY_EXEC_REFUSED'),
        ('download',['run','/opt/stand/pkgs/downloaded/bin/program'],'development-version-1'),
        ('source-build',['run','/opt/stand/pkgs/source-example-built/bin/program'],'BUILT_SOURCE_OK'),
        ('user-service-program',['run','/opt/stand/pkgs/dev-worker/bin/worker'],'development-version-1'),
    ]
    schedule="""python3 -I - <<'SCHEDULE'
import json,subprocess,time
end=time.monotonic()+15
while True:
    p=subprocess.run(['/usr/bin/journalctl','-u','stand-scheduled-example.service','--no-pager','-o','cat'],capture_output=True,text=True)
    if 'BUILT_SOURCE_OK' in p.stdout or time.monotonic()>=end:break
    time.sleep(.2)
print(json.dumps({'id':'COMBINED-SCHEDULE','passed':p.returncode==0 and 'BUILT_SOURCE_OK' in p.stdout,'journal':p.stdout},sort_keys=True))
assert p.returncode==0 and 'BUILT_SOURCE_OK' in p.stdout
SCHEDULE
"""
    try:
        for label,root in [('a',ROOT),('b',peer)]:
            name='bc4-combined-'+args.phase+'-'+label
            if (root/'vms'/name).exists():raise RuntimeError('disposable name collision')
            owned.append((root,name,label))
            with (root/'base/stand.qcow2').open('rb') as stream:
                image_sha=hashlib.file_digest(stream,'sha256').hexdigest()
            provenance['images'][label]={'sha256':image_sha,
                'recipe_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted((root/'build').iterdir()) if p.is_file()}}
            event(phase='expected',id='COMBINED-'+label,
                  expected='fresh image accepts the same complete BC4 declaration; all lines verify and every channel launches',
                  declaration_files_sha256=digests,image_sha256=image_sha)
            try:
                if lab(root,name,'new',label+'-new.log','stand'):continue
                if guest(root,name,delivery,label+'-deliver.log'):continue
                if guest(root,name,'/usr/local/bin/stand-apply /var/lib/stand/combined-input\n',label+'-apply.log'):continue
                guest(root,name,exact,label+'-exact.jsonl')
                guest(root,name,'/usr/local/bin/stand-verify\n',label+'-verify.jsonl')
                for test,fields,marker in launches:
                    event(phase='expected',id=label+'-'+test,expected='recorded ordinary launch succeeds',marker=marker)
                    log=label+'-launch-'+test+'.log'
                    rc=lab(root,name,'run',log,script='\t'.join(fields)+'\n')
                    output=(out/log).read_text(errors='replace') if (out/log).exists() else ''
                    ok=rc==0 and (marker is None or marker in output)
                    if not ok:status=1
                    event(phase='assertion',id=label+'-'+test,passed=ok)
                event(phase='expected',id=label+'-schedule',expected='recorded scheduled command appears in actual service journal')
                guest(root,name,schedule,label+'-schedule.jsonl')
                if args.reboot:
                    event(phase='expected',id=label+'-reboot',expected='exact combined declaration and all required values survive a clean reboot')
                    lab(root,name,'stop',label+'-stop.log')
                    lab(root,name,'start',label+'-start.log')
                    guest(root,name,exact,label+'-reboot-exact.jsonl')
                    guest(root,name,'/usr/local/bin/stand-verify\n',label+'-reboot-verify.jsonl')
                log=label+'-snapshot.json'
                rc=guest(root,name,'/usr/local/bin/stand-compare --snapshot -\n',log)
                if rc==0:
                    values=json.loads((out/log).read_text())
                    if {r['id'] for r in values}!=set(ids) or not all(r['ok'] for r in values):
                        status=1
                    else:snapshots[label]=values
                results[label]={'snapshot_exit':rc,'snapshot_complete':label in snapshots}
                if label=='b' and set(snapshots)=={'a','b'}:
                    event(phase='expected',id='COMBINED-COMPARE',expected='installed stand-compare reports equal for every combined declaration line')
                    script="python3 -I - <<'SNAPSHOTS'\nimport base64,pathlib\n"
                    for side in ('a','b'):
                        data=base64.b64encode((out/(side+'-snapshot.json')).read_bytes()).decode()
                        script+="pathlib.Path('/var/lib/stand/combined-"+side+".json').write_bytes(base64.b64decode('"+data+"'))\n"
                    script+="SNAPSHOTS\n/usr/local/bin/stand-compare /var/lib/stand/combined-a.json /var/lib/stand/combined-b.json\n"
                    guest(root,name,script,'stand-compare.jsonl')
                    left={r['id']:r for r in snapshots['a']};right={r['id']:r for r in snapshots['b']}
                    same=left==right
                    if not same:status=1
                    event(phase='assertion',id='COMBINED-VALUES-EQUAL',passed=same,compared_rows=len(left))
            finally:
                cleanup(root,name,label)
        if set(snapshots)!={'a','b'}:status=1
        recipes_equal=(set(provenance['images'])=={'a','b'} and
                       provenance['images']['a']['recipe_sha256']==provenance['images']['b']['recipe_sha256'])
        if not recipes_equal:status=1
        event(phase='assertion',id='COMBINED-RECIPES-EQUAL',passed=recipes_equal)
    except BaseException as error:
        status=1
        event(phase='error',error=type(error).__name__)
        raise
    finally:
        for root,name,label in reversed(owned):
            try:cleanup(root,name,label)
            except BaseException as error:
                status=1;event(phase='cleanup-error',side=label,error=type(error).__name__)
        remaining=[label for root,name,label in owned if (root/'vms'/name).exists()]
        if remaining:status=1
        provenance['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        (out/'provenance.json').write_text(json.dumps(provenance,indent=2,sort_keys=True)+'\n')
        summary={'suite_exit':status,'results':results,'snapshot_sides':sorted(snapshots),
                 'owned_vms_remaining':remaining,'declaration_rows':len(rows),
                 'independent_build_origin':'two supplied separate roots; recipe-build provenance must additionally establish separate rebuilds'}
        (out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
        event(phase='summary',**summary);events.close()
    return status


if __name__=='__main__':
    sys.exit(main())
