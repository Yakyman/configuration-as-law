#!/usr/bin/env python3
"""Once-only second-party controller. Preparation never invokes this entry point."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import time

P = pathlib.Path
ROOT = P(__file__).resolve().parent.parent
IMAGE = '1b581030629256ccc975950a2254572217e01a2474d2a07808a8e477ca980eca'
DECLARATION = '2e6946a893a04b121ef4687d82bc34fde2577e983ac0bfdc2ecf3ad4cdd79b4a'


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    with open(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('history', choices=['h1','h2','h3','h4'])
    parser.add_argument('--publication', type=P, required=True)
    args = parser.parse_args()
    os.chdir(ROOT)
    seal_path = ROOT/'cases-8/inputs-seal.json'
    publication = json.loads(args.publication.read_text())
    if not publication.get('public_record_url','').startswith('https://') or not publication.get('commit'):
        raise RuntimeError('An actual public record URL and commit are required before any attempt')
    if publication.get('inputs_seal_sha256') != sha(seal_path):
        raise RuntimeError('Publication seal identity differs')
    if publication.get('operator_verified_published_bytes') is not True:
        raise RuntimeError('The performing party must verify the public bytes independently')
    seal = json.loads(seal_path.read_text())
    for name, expected in seal['files'].items():
        path = ROOT/name
        if not path.resolve().is_relative_to(ROOT) or sha(path) != expected:
            raise RuntimeError('Sealed input differs: '+name)
    if sha(ROOT/'base/stand.qcow2') != IMAGE or sha(ROOT/'cases-8/declaration.json') != DECLARATION:
        raise RuntimeError('Final step-6 image or initial declaration differs')
    if (ROOT/'base/stand.qcow2').stat().st_mode & 0o222:
        raise RuntimeError('Base image must remain read-only')
    if (ROOT/'base/stand.json').read_bytes() != (ROOT/'cases-8/base-metadata.json').read_bytes():
        raise RuntimeError('Base launch metadata differs from the committed input')
    vm = 's8-second-'+args.history
    vm_dir = ROOT/'vms'/vm
    if vm_dir.exists():
        raise RuntimeError('Guest name already exists; do not reuse an attempted copy')
    out = ROOT/'raw/step-8-second-party'/args.history
    out.mkdir(parents=True, exist_ok=False)
    save(out/'publication.json', publication)
    save(out/'started.json', {'utc':utc(),'history':args.history,'image_sha256':IMAGE,
         'initial_declaration_sha256':DECLARATION,'inputs_seal_sha256':sha(seal_path)})
    spec = importlib.util.spec_from_file_location('s8_lab', ROOT/'lab.py')
    lab = importlib.util.module_from_spec(spec); spec.loader.exec_module(lab)
    commands = []
    observations = []

    def command(name, argv, stdin=None, timeout=1800):
        if any(x['name'] == name for x in commands):
            raise RuntimeError('Repeated command label refused: '+name)
        entry = {'name':name,'argv':[str(x).replace(str(ROOT),'<stand-root>') for x in argv],
                 'started_utc':utc(), 'stdin_sha256':hashlib.sha256(stdin).hexdigest() if stdin is not None else None}
        if stdin is not None:
            (out/(name+'.stdin')).write_bytes(stdin)
        with (out/(name+'.stdout')).open('wb') as stdout, (out/(name+'.stderr')).open('wb') as stderr:
            try:
                proc = subprocess.run([str(x) for x in argv], input=stdin, stdout=stdout, stderr=stderr,
                                      timeout=timeout, cwd=ROOT, env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                entry['exit'] = proc.returncode
            except subprocess.TimeoutExpired:
                entry.update(exit=None, error='TimeoutExpired')
            except OSError as e:
                entry.update(exit=None, error=type(e).__name__)
        entry['ended_utc'] = utc()
        commands.append(entry); save(out/'commands.json',commands)
        return entry

    def guest(name, source, root=False, trace=True):
        if isinstance(source, P):
            text = source.read_text()
        else:
            text = source
        if trace:
            # Preserve the interpreter shebang. EPOCHREALTIME is the Bash clock;
            # this adds diagnostics only, not a saved guest script or setting.
            lines = text.splitlines(keepends=True)
            if not lines or not lines[0].startswith('#!'):
                lines.insert(0, '#!/bin/bash\n')
            lines.insert(1, "PS4='+${EPOCHREALTIME} ${LINENO}: '; set -x\n")
            text = ''.join(lines)
        argv = [sys.executable, ROOT/'lab.py', 'run', vm] + (['--root'] if root else [])
        return command(name, argv, text.encode())

    def observe(label):
        entry = guest(label, ROOT/'cases-8/observe.py', root=True, trace=False)
        record = {'label':label, 'exit':entry['exit'], 'evidence':label+'.stdout',
                  'actions_record':'commands.json', 'status':'collected' if entry['exit']==0 else 'unavailable'}
        if entry['exit'] == 0:
            try:
                data = json.loads((out/(label+'.stdout')).read_text())
                if data.get('collection_error'):
                    record['status'] = 'partial'
                record['declaration_stable'] = data.get('declaration_stable')
                record['success_reports_stable'] = data.get('success_reports_stable')
            except (OSError,ValueError):
                record['status'] = 'unavailable: invalid JSON'
        observations.append(record); save(out/'observation-points.json', observations)
        return entry

    def boot_id(name):
        e = guest(name, 'cat /proc/sys/kernel/random/boot_id\n', root=True)
        return (out/(name+'.stdout')).read_text().strip() if e['exit']==0 else None

    def restart(number):
        before = boot_id('restart-'+str(number)+'-before-boot-id')
        request = guest('restart-'+str(number)+'-request', '/usr/bin/systemctl reboot\n', root=True)
        # The reboot command can close SSH before its status is delivered.
        status = {'before_boot_id':before, 'request_exit':request['exit'], 'started_utc':utc()}
        time.sleep(3)
        try:
            lab.ready(vm_dir)
            after = boot_id('restart-'+str(number)+'-after-boot-id')
            status.update(after_boot_id=after, done=bool(before and after and before != after))
        except Exception as e:
            status.update(done=False, error=str(e).replace(str(ROOT),'<stand-root>'))
        status['ended_utc'] = utc(); save(out/('restart-'+str(number)+'.json'),status)
        observe('h1-after-restart-'+str(number))
        return status['done']

    def interrupted(label, text, executable):
        folder = out/label
        entry = command(label+'-host-cut', [sys.executable,ROOT/'cases-8/h4/cut-action.py',vm,label,text,executable,
            '--observer',ROOT/'cases-8/observe.py','--output',folder],timeout=1750)
        record = {'label':'h4-'+label+'-disconnected','evidence':label+'/guest.json',
                  'status':'unavailable','actions_record':'commands.json'}
        try:
            data = json.loads((folder/'guest.json').read_text())
            record.update(status='collected' if 'disconnected_observation' in data else 'unavailable',
                          valid_cut=data.get('valid_cut',False))
            if data.get('disconnected_observation',{}).get('collection_error'):
                record['status'] = 'partial'
        except (OSError,ValueError):
            data = {}
        observations.append(record); save(out/'observation-points.json', observations)
        observe('h4-'+label+'-restored')
        if entry['exit'] != 0 or not data.get('valid_cut') or 'exit' not in data:
            return False
        if data['exit'] != 0:
            retry = guest(label+'-restored-retry', text+'\n')
            observe('h4-'+label+'-after-restored-retry')
            return retry['exit'] == 0
        return True

    created = False
    try:
        result = command('create', [sys.executable,ROOT/'lab.py','new',vm,'stand'],timeout=240)
        created = vm_dir.exists()
        if result['exit'] != 0:
            raise RuntimeError('Fresh guest creation/readiness failed')
        metadata = json.loads((vm_dir/'meta.json').read_text())
        pid = lab.live(vm_dir)
        argv = (P('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0') if pid else []
        save(out/'vm.json',{'metadata':metadata,'argv':[x.decode().replace(str(ROOT),'<stand-root>') for x in argv if x]})
        if args.history == 'h1':
            for number in (1,2):
                e = guest('h1-update-'+str(number), ROOT/('cases-8/h1/update-'+str(number)+'.sh'),root=True)
                if e['exit'] != 0 or not restart(number):
                    break
                guest('h1-after-restart-'+str(number)+'-package',
                      "/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\\n' ed\n",root=True)
        elif args.history == 'h2':
            guest('h2-development', ROOT/'cases-8/h2/history.sh')
        elif args.history == 'h3':
            e = guest('h3-prerequisites', ROOT/'cases-8/h3/prerequisites.sh',root=True)
            if e['exit'] == 0:
                guest('h3-launcher', ROOT/'cases-8/h3/history.sh')
        else:
            e = guest('h4-artifact-identity', "printf '%s\\n' 'cc7a77f4e8cb92e2db65c112f17cce425bf966980ff239772bf500599d1ff2ba  /usr/local/share/stand/dev/worker-1.json' | sha256sum -c -\n")
            if e['exit'] != 0:
                raise RuntimeError('Committed installation artifact differs')
            installed = interrupted('install','stand-pkg install /usr/local/share/stand/dev/worker-1.json','/usr/local/bin/stand-pkg')
            if installed:
                guest('h4-worker-run','/opt/stand/pkgs/dev-worker/bin/worker\n')
            # Development is a separate required part, even if installation failed.
            prefix = guest('h4-development-prefix',ROOT/'cases-8/h4/development-prefix.sh')
            if prefix['exit'] == 0:
                built = interrupted('development','stand-build build source:h2-hello','/usr/local/bin/stand-build')
                if built:
                    guest('h4-development-suffix',ROOT/'cases-8/h4/development-suffix.sh')
    except Exception as e:
        save(out/'failure.json',{'utc':utc(),'error':type(e).__name__,
                               'message':str(e).replace(str(ROOT),'<stand-root>')})
    finally:
        if created:
            observe(args.history+'-end')
            console = vm_dir/'console.log'
            if console.exists():
                (out/'console.log').write_bytes(console.read_bytes())
            stopped = command('stop',[sys.executable,ROOT/'lab.py','stop',vm],timeout=140)
            if stopped['exit'] != 0:
                command('cleanup-poweroff',[sys.executable,ROOT/'lab.py','kill',vm],timeout=30)
            command('destroy',[sys.executable,ROOT/'lab.py','destroy',vm],timeout=150)
        command('remaining-guests',[sys.executable,ROOT/'lab.py','list'],timeout=30)
        save(out/'cleanup.json',{'utc':utc(),'owned_guest_exists':vm_dir.exists(),
                               'base_sha256':sha(ROOT/'base/stand.qcow2'), 'outcome':'not assigned'})
        if vm_dir.exists():
            raise RuntimeError('Owned guest cleanup incomplete; retain evidence and remove that guest only')
    print('History commands finished; assign no outcome from controller exit alone.')


if __name__ == '__main__':
    main()
