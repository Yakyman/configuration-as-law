#!/usr/bin/python3
"""Resolve pinned base closures for the three published update snapshots.

Release preparation on the worker only; never writes a declaration.
"""
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
snapshots = ('20260801T000000Z', '20261001T000000Z', '20261123T000000Z')
names = sorted(set((HERE/'base-roots.txt').read_text().split()))
dest = HERE/'components'
dest.mkdir(exist_ok=True)
for stamp in snapshots:
    work = HERE/'locks.work'/stamp
    for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
        (work/sub).mkdir(parents=True, exist_ok=True)
    (work/'status').write_text('')
    (work/'etc/sources.list').write_text(
        f'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/{stamp}/ trixie main\n')
    opts = ['-o', f'Dir::State::status={work}/status', '-o', f'Dir::State::lists={work}/lists',
            '-o', f'Dir::Cache::archives={work}/archives', '-o', f'Dir::Etc::sourcelist={work}/etc/sources.list',
            '-o', 'Dir::Etc::sourceparts=-', '-o', 'APT::Install-Recommends=false',
            '-o', 'APT::Install-Suggests=false', '-o', 'APT::Sandbox::User=root',
            '-o', 'Acquire::Check-Valid-Until=false', '-o', 'Acquire::Retries=3',
            '-o', f'Dir::Log={work}/log', '-o', 'Dir::Cache::pkgcache=',
            '-o', 'Dir::Cache::srcpkgcache=', '-o', 'Acquire::Languages=none',
            '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-']
    subprocess.run(['apt-get', *opts, 'update'], check=True)
    result = subprocess.check_output(['apt-get', *opts, '--simulate', 'install', *names], text=True)
    (dest/(stamp+'.resolution.txt')).write_text(result)
    pins = re.findall(r'^Inst (\S+) \((\S+) ', result, re.M)
    if not set(names).issubset({name for name, _ in pins}):
        raise RuntimeError('resolution did not include all base components')
    pins.append(('confos-runtime', (HERE/'VERSION').read_text().strip()))
    pins.append(('confos-boot', (HERE/'VERSION').read_text().strip()))
    pins.append(('confos-code-readers', (HERE/'VERSION').read_text().strip()))
    pins.append(('confos-initramfs', (HERE/'VERSION').read_text().strip()+'+'+stamp))
    (dest/(stamp+'.txt')).write_text(''.join(name+'='+version+'\n' for name, version in sorted(pins)))
    print(stamp, len(pins), 'components', flush=True)
shutil.rmtree(HERE/'locks.work')
