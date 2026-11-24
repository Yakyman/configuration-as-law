#!/usr/bin/env python3
"""Run each exact committed copier once, retrieve copies, and verify audit hashes."""
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tarfile
import time

ROOT = Path(__file__).resolve().parents[3]
SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ssh = ['ssh', '-F', os.environ['LAB_SSH_CONFIG'], '-o', 'BatchMode=yes', os.environ['LAB_SSH_TARGET']]
    operator = ROOT / 'D1b/in/operator'
    report = operator / 'handoff-status.tsv'
    checks = []
    with report.open('x', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=['machine', 'utc', 'exit_status', 'duration_seconds', 'command'], delimiter='\t', lineterminator='\n')
        writer.writeheader()
        output.flush()
        for machine in SYSTEMS:
            lab = 'VMs/cal-1123/d1b-operator-' + machine
            command = ('python3 "$S4_INPUTS/fix-s4-p-3/neutralize.py" D1b/raw/' + machine +
                       ' D1b/handoff/' + machine + ' --report D1b/handoff-audit/' + machine + '.json')
            script = 'cd\ncd ' + lab + '\nS4_INPUTS="$PWD/S4"\nmkdir -p D1b/handoff-audit\n' + command
            start = time.monotonic()
            run = subprocess.run(ssh + ['systemd-run --user --quiet --wait --pipe --collect --unit=d1b-handoff-' + machine + ' bash -ec ' + shlex.quote(script)], capture_output=True)
            (operator / ('handoff-' + machine + '.stdout')).write_bytes(run.stdout)
            (operator / ('handoff-' + machine + '.stderr')).write_bytes(run.stderr)
            writer.writerow(dict(machine=machine, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                 exit_status=run.returncode, duration_seconds=round(time.monotonic()-start, 3), command=command))
            output.flush()
            print(machine + ' handoff exit ' + str(run.returncode), flush=True)
            if run.returncode:
                continue
            assert not (ROOT / 'D1b/handoff' / machine).exists()
            command = 'cd ' + lab + '/D1b && tar -cf - handoff/' + machine + ' handoff-audit/' + machine + '.json'
            with (operator / ('handoff-transfer-' + machine + '.stderr')).open('wb') as err:
                process = subprocess.Popen(ssh + [command], stdout=subprocess.PIPE, stderr=err)
                with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
                    archive.extractall(ROOT / 'D1b', filter='data')
                transfer_rc = process.wait()
            if transfer_rc:
                raise RuntimeError('Handoff transfer failed for ' + machine)
            audit = json.loads((ROOT / 'D1b/handoff-audit' / (machine + '.json')).read_text())
            assert audit['source_unchanged'] is True
            mismatches = []
            for row in audit['files']:
                for tree, field in (('handoff', 'handoff_sha256'),):
                    path = ROOT / 'D1b' / tree / machine / row['path']
                    if not path.is_file() or digest(path) != row[field]:
                        mismatches.append(tree + '/' + row['path'])
            expected = {row['path'] for row in audit['files']}
            for tree in ('handoff',):
                base = ROOT / 'D1b' / tree / machine
                assert {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()} == expected
            check = dict(machine=machine, transfer_exit=transfer_rc, files=len(expected), source_unchanged=audit['source_unchanged'],
                         mapped_fields=sum(c['count'] for c in audit['changes']), mismatches=mismatches,
                         local_raw_verification='deferred until all original transfers complete')
            checks.append(check)
            (operator / 'handoff-local-verification.json').write_text(json.dumps(checks, indent=2) + '\n')
            assert not mismatches, 'Local copy differs from committed handoff audit'
            print(machine + ' local handoff hashes verified: ' + str(len(expected)) + ' files', flush=True)


if __name__ == '__main__':
    main()
