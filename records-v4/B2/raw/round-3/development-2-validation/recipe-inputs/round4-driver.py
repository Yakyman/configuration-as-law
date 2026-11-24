#!/usr/bin/env python3
"""Single-use sequential BC4 evidence driver; optional complete BC3 regression chain."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('phase')
parser.add_argument('--regressions', action='store_true')
parser.add_argument('--peer-root', type=Path)
args = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,39}', args.phase):
    parser.error('phase must be a fresh alphanumeric/hyphen label, at most 40 characters')
if args.peer_root and not args.regressions:
    parser.error('--peer-root requires --regressions')
peer = args.peer_root.resolve() if args.peer_root else None
if peer == ROOT:
    parser.error('independent peer must have a different build root')
OUT = ROOT / 'raw' / 'round-4' / args.phase
OUT.mkdir(parents=True, exist_ok=False)
events = (OUT / 'events.jsonl').open('w', buffering=1)
status = 0
owned = []
results = {}
regression_phase = 'bc4-' + args.phase
regression_started = False
regression_source = ROOT / 'raw' / 'round-3' / regression_phase


def event(**row):
    row['utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    line = json.dumps(row, sort_keys=True)
    events.write(line + '\n')
    print(line, flush=True)


def execute(argv, logfile, script=None, root=ROOT, timeout=14400):
    global status
    try:
        with (OUT / logfile).open('wb') as output:
            done = subprocess.Popen(list(map(str, argv)), cwd=root, stdin=subprocess.PIPE,
                                    stdout=output, stderr=subprocess.STDOUT, start_new_session=True,
                                    env={**os.environ, 'STAND_ROOT':str(root),
                                         'PYTHONDONTWRITEBYTECODE':'1'})
            try:
                done.communicate(script.encode() if isinstance(script, str) else script, timeout=timeout)
            except BaseException:
                # Stop nested controllers before removing their VM objects;
                # QEMU itself remains supervised by the lab's user service.
                try: os.killpg(done.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                done.wait()
                raise
        rc = done.returncode
    except subprocess.TimeoutExpired:
        rc = 124
        event(phase='error', log=logfile, error='controller timeout; cleanup required')
    except OSError as error:
        rc = 127
        # Do not publish host-specific paths from exception text.
        event(phase='error', log=logfile, error=type(error).__name__, errno=error.errno)
    event(phase='result', log=logfile, rc=rc)
    if rc:
        status = 1
    return rc


def lab(root, op, name, logfile, *extra, script=None):
    return execute([sys.executable, root/'lab.py', op, name, *extra], logfile,
                   script=script, root=root, timeout=7200 if op == 'run' else 360)


def reserve(root, name):
    if (root/'vms'/name).exists():
        raise RuntimeError('refusing collision with existing disposable VM name: '+name)
    owned.append((root, name))


def cleanup(root, name):
    if not (root/'vms'/name).exists():
        return
    label = ('peer-' if root != ROOT else '') + name
    event(phase='expected', id='CLEANUP-'+label, expected='owned disposable VM stopped and removed')
    if lab(root, 'destroy', name, label+'-destroy.log'):
        lab(root, 'kill', name, label+'-kill.log')
        lab(root, 'destroy', name, label+'-destroy-after-kill.log')


suites = [
    ('language', 'language-selftest.py /usr/local/share/stand/language /var/lib/stand/language-selftest.jsonl'),
    ('applications', 'app-selftest.py --output /var/lib/stand/app-selftest.jsonl'),
    ('system', 'system-selftest.py /var/lib/stand/system-selftest.jsonl'),
    ('ordinary', 'round4-selftest.py'),
]
try:
    event(phase='expected', id='BC4-SUITES',
          expected='four independent clean VMs; every suite exits zero after positive declaration paths and refusal attempts',
          source='B2/build/language-selftest.py; app-selftest.py; system-selftest.py; round4-selftest.py')
    for label, command in suites:
        if os.environ.get('STAND_V4_CHANNELS')=='1':
            command='v4-suite-adapter.py '+command
        name = 'bc4-'+args.phase+'-'+label
        reserve(ROOT, name)
        try:
            event(phase='expected', id='SUITE-'+label,
                  expected='fresh VM, installed test suite exit zero, then every-line verification',
                  guest_command='python3 -B /usr/local/lib/stand/'+command)
            if lab(ROOT, 'new', name, label+'-new.log', 'stand'):
                results[label] = {'new_exit':1, 'tested':False}
                continue
            rc = lab(ROOT, 'run', name, label+'.jsonl', '--root',
                     script='python3 -B /usr/local/lib/stand/'+command+'\n')
            metadata = 0
            if label == 'applications':
                event(phase='expected', id='FLATPAK-HELPER-AVAILABILITY',
                      expected='both native helper paths absent and system helper unit masked; saved beside the D-Bus refusal')
                metadata = lab(ROOT, 'run', name, 'applications-helper-availability.jsonl', '--root', script="""python3 -I - <<'META'
import json,pathlib,subprocess
paths={p:pathlib.Path(p).exists() or pathlib.Path(p).is_symlink() for p in ('/usr/libexec/flatpak-system-helper','/usr/lib/flatpak/flatpak-system-helper')}
q=subprocess.run(['/usr/bin/systemctl','is-enabled','flatpak-system-helper.service'],capture_output=True,text=True)
mask=pathlib.Path('/etc/systemd/system/flatpak-system-helper.service')
target=str(mask.readlink()) if mask.is_symlink() else None
ok=not any(paths.values()) and q.stdout.strip()=='masked' and target=='/dev/null'
print(json.dumps({'id':'FLATPAK-HELPER-AVAILABILITY','passed':ok,'paths_present':paths,'is_enabled_output':q.stdout,'is_enabled_exit':q.returncode,'unit_link':target},sort_keys=True))
assert ok
META
""")
            verify = lab(ROOT, 'run', name, label+'-verify.jsonl', '--root',
                         script='/usr/local/bin/stand-verify\n')
            exported = lab(ROOT, 'copy-out', name, label+'-examples-export.log',
                           '/var/lib/stand/channel-examples', OUT/(label+'-examples'))
            if label == 'system':
                exported |= lab(ROOT, 'copy-out', name, 'system-state-export.log',
                                '/var/lib/stand/channel-system-state', OUT/'system-state')
            if label == 'language':
                exported |= lab(ROOT, 'copy-out', name, 'factory-export.log',
                                '/etc/stand/factory', OUT/'factory-export')
            results[label] = {'tested':True, 'suite_exit':rc, 'verify_exit':verify, 'example_export_exit':exported, 'metadata_exit':metadata}
        finally:
            cleanup(ROOT, name)
    if args.regressions:
        # The existing controller already covers development D01–D10, BC1–BC3,
        # inventory, boot admission, nine power cuts and an optional clean peer.
        # Keep its nonzero missing-peer disposition: absence is not a pass.
        if regression_source.exists():
            raise RuntimeError('regression evidence phase already exists')
        names = ['dev','peer-a','peer-b','cut','bc3-'+regression_phase,
                 'bc3-inventory-'+regression_phase,
                 'bc3-regression1-'+regression_phase,'bc3-regression2-'+regression_phase]
        if peer:
            names.append('bc3-peer-a')
        for name in names:
            reserve(ROOT, name)
        if peer:
            reserve(peer, 'bc3-peer-b')
        event(phase='expected', id='PRIOR-SUITES',
              expected='complete existing BC3 controller including prior suites, boot gate, power cuts and independent peer comparison',
              independent_peer_requested=bool(peer),
              missing_peer_disposition='not tested; existing controller returns nonzero')
        argv = [sys.executable, ROOT/'build/round3-driver.py', regression_phase]
        if peer:
            argv += ['--peer-root', peer]
        regression_started = True
        rc = execute(argv, 'regressions-console.jsonl', timeout=21600)
        results['regressions'] = {'tested':True, 'controller_exit':rc,
                                  'independent_peer_requested':bool(peer)}
    else:
        event(phase='not-tested', id='PRIOR-SUITES', reason='--regressions not requested')
except BaseException as error:
    status = 1
    event(phase='error', error=type(error).__name__)
    raise
finally:
    for root, name in reversed(owned):
        try:
            cleanup(root, name)
        except BaseException as error:
            status = 1
            event(phase='cleanup-error', vm=name, error=type(error).__name__)
    # Move the complete child evidence tree, including original failed outputs,
    # beneath this round's raw directory. No test output is reclassified.
    if regression_started and regression_source.exists():
        shutil.move(str(regression_source), str(OUT/'regressions'))
    image = ROOT/'base/stand.qcow2'
    image_sha = None
    if image.exists():
        with image.open('rb') as stream:
            image_sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    else:
        status = 1
    recipe = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((ROOT/'build').iterdir()) if p.is_file()}
    (OUT/'recipe-sha256.json').write_text(json.dumps(recipe, indent=2, sort_keys=True)+'\n')
    remaining = [('peer:' if root != ROOT else '')+name
                 for root, name in owned if (root/'vms'/name).exists()]
    if remaining:
        status = 1
    summary = {'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'suite_exit':status, 'image_sha256':image_sha, 'suites':results,
               'regressions_requested':args.regressions,
               'independent_peer_requested':bool(peer),
               'owned_vms_remaining':remaining}
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    event(phase='summary', **{k:v for k,v in summary.items() if k!='utc'})
    events.close()
sys.exit(status)
