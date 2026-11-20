#!/usr/bin/env python3
"""Guest component census; raw evidence and explicit exclusions accompany comparison data."""
import argparse
import json
import os
from pathlib import Path
import pwd
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory')
    args = parser.parse_args()
    out = Path(args.output_directory)
    out.mkdir(parents=True, exist_ok=True)
    raw = out / 'raw'
    raw.mkdir(exist_ok=True)
    errors = []

    def command(name, argv):
        try:
            p = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            record = dict(argv=argv, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)
        except OSError as e:
            record = dict(argv=argv, returncode=None, stdout='', stderr=str(e))
        (raw / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
        if record['returncode'] != 0:
            errors.append({'source': name, **record})
        return record['stdout']

    data = {}
    packages = command('dpkg', ['dpkg-query', '-W', '-f=${Package}\t${Version}\t${Architecture}\t${Status}\n'])
    data['packages'] = sorted([line.split('\t') for line in packages.splitlines()])
    data['accounts'] = sorted([dict(name=p.pw_name, uid=p.pw_uid, gid=p.pw_gid,
                                   home=p.pw_dir, shell=p.pw_shell) for p in pwd.getpwall()], key=lambda p: p['name'])
    (raw / 'passwd.txt').write_text(Path('/etc/passwd').read_text())
    # Include active timer waiting states, not merely SubState=running.
    units = command('active-units', ['systemctl', 'list-units', '--type=service,timer', '--state=active', '--no-legend', '--plain', '--no-pager'])
    data['active_units'] = sorted([line.split(None, 4)[:4] for line in units.splitlines() if line.strip()])
    files = command('unit-files', ['systemctl', 'list-unit-files', '--type=service,timer', '--no-legend', '--plain', '--no-pager'])
    # Preserve all enablement states; static, masked and disabled differences matter too.
    data['unit_file_states'] = sorted([line.split() for line in files.splitlines() if line.strip()])
    command('scopes-not-compared', ['systemctl', 'list-units', '--type=scope', '--all', '--no-legend', '--plain', '--no-pager'])

    processes = []
    excluded = []
    raw_processes = []
    for proc in sorted(Path('/proc').iterdir()):
        if not proc.name.isdigit():
            continue
        try:
            status = (proc / 'status').read_text()
            uid = int(re.search(r'^Uid:\s+(\d+)', status, re.M).group(1))
            argv = (proc / 'cmdline').read_bytes().split(b'\0')
            argv = [a.decode('utf-8', 'surrogateescape') for a in argv if a]
            try:
                exe = os.readlink(proc / 'exe')
            except FileNotFoundError:
                exe = None
            comm = (proc / 'comm').read_text().rstrip('\n')
            item = dict(pid=int(proc.name), exe=exe, uid=uid, args=argv, comm=comm)
            raw_processes.append(item)
            if item['pid'] == os.getpid():
                excluded.append(dict(reason='this inventory collector only', **item))
                continue
            # No general IP, PID, path, or arbitrary argument substitution.
            # Normalize only OpenSSH's explicit connection process-title tuple.
            norm = []
            for arg in argv:
                if exe and Path(exe).name in ('sshd', 'sshd-session'):
                    arg = re.sub(r'(?<=sshd: )([^ ]+) \[([0-9a-fA-F:.]+)\] port [0-9]+',
                                 r'\1 [<connection-address>] port <connection-port>', arg)
                norm.append(arg)
            processes.append(dict(exe=exe, uid=uid, args=norm, comm=comm))
        except (FileNotFoundError, ProcessLookupError):
            # Processes may exit during the census; retain the observation.
            excluded.append(dict(pid=int(proc.name), reason='exited during census'))
        except (PermissionError, AttributeError, ValueError) as e:
            errors.append(dict(source=str(proc), error=str(e)))
    sortkey = lambda value: json.dumps(value, sort_keys=True)
    data['processes'] = sorted(processes, key=sortkey)
    data['process_program_set'] = sorted({(p['exe'] or '[kernel] ' + p['comm']) for p in processes})
    (raw / 'processes.json').write_text(json.dumps(raw_processes, indent=2) + '\n')
    (raw / 'collector-and-races.json').write_text(json.dumps(excluded, indent=2) + '\n')

    modules = Path('/proc/modules').read_text()
    (raw / 'modules.txt').write_text(modules)
    data['modules'] = sorted([dict(name=s[0], size=int(s[1]), dependents=sorted(s[3].strip(',').split(',')) if s[3] != '-' else [])
                              for s in (line.split() for line in modules.splitlines())], key=lambda p: p['name'])
    data['pci'] = []
    for device in sorted(Path('/sys/bus/pci/devices').iterdir()):
        data['pci'].append(dict(address=device.name, vendor=(device / 'vendor').read_text().strip(),
                                device=(device / 'device').read_text().strip(),
                                driver=(device / 'driver').resolve().name if (device / 'driver').exists() else None))
    uname = os.uname()
    (raw / 'uname.json').write_text(json.dumps(dict(zip(uname._fields, uname)) if hasattr(uname, '_fields') else list(uname), indent=2) + '\n')
    data['kernel'] = dict(sysname=uname.sysname, release=uname.release, version=uname.version, machine=uname.machine)
    data['collection_errors'] = errors
    (out / 'inventory.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    (out / 'NORMALIZATION.md').write_text('''# Inventory scope and normalization

Raw command results include argv, exit status and stderr. Collection errors are retained as a compared category, not interpreted as absence.

Processes: raw records retain PID. Comparison omits PIDs (runtime identities), excludes only this collector PID, and retains multiplicity, executable symlink target, UID, comm and arguments. Exited processes are listed separately. The only argument normalization is an explicit sshd connection-address/port process-title pattern; arbitrary IPs, paths and numerical arguments remain unchanged. process_program_set is a separate executable set, not a substitute for the full process comparison. SSH server/session and parent test-harness processes remain visible. No claimed role is inferred from a binary name. Deleted executable suffixes remain visible.

Services/timers: all active units with load/active/sub states and all unit-file enablement/preset states are compared. Scope units (including transient session scopes) are outside this services/timers category and retained verbatim in raw/scopes-not-compared.json. No service/timer name is normalized or suppressed.

Kernel: uname hostname is a machine identity, preserved raw but excluded from kernel comparison. Module reference counts/load addresses/states are raw-only; name, size and named dependents are compared. PCI hardware addresses, vendor/device IDs and driver are compared without masking hardware differences. Accounts omit GECOS/password placeholders but retain name, UID, GID, home, shell; raw passwd is retained. Unix group memberships, ACLs and policy files need supplemental evidence for the full users-and-rules claim. No hypothesis outcome is assigned here.
''')
    print(json.dumps(dict(output=str(out), collection_errors=len(errors))))


if __name__ == '__main__':
    main()
