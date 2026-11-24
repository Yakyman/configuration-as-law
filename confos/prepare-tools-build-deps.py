#!/usr/bin/python3
"""Private pinned libraries required by Debian's optional reader builds."""
from pathlib import Path
import hashlib
import subprocess
here = Path(__file__).resolve().parent
work = here/'interpreter-inputs/tools/dependencies'
apt, root = work/'apt', work/'root'
root.mkdir(parents=True, exist_ok=True)
for name in ('lists/partial', 'archives/partial', 'etc', 'log'):
    (apt/name).mkdir(parents=True, exist_ok=True)
(apt/'status').write_text('')
(apt/'etc/sources.list').write_text(
    'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20261123T000000Z/ trixie main\n')
options = ['-o', f'Dir::State::status={apt}/status', '-o', f'Dir::State::lists={apt}/lists',
    '-o', f'Dir::Cache::archives={apt}/archives', '-o', f'Dir::Etc::sourcelist={apt}/etc/sources.list',
    '-o', 'Dir::Etc::sourceparts=-', '-o', 'APT::Sandbox::User=root',
    '-o', 'Acquire::Check-Valid-Until=false', '-o', 'Acquire::Retries=3',
    '-o', f'Dir::Log={apt}/log', '-o', 'Dir::Cache::pkgcache=', '-o', 'Dir::Cache::srcpkgcache=',
    '-o', 'Acquire::Languages=none', '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-',
    '-o', 'APT::Install-Recommends=false', '-o', 'APT::Install-Suggests=false']
with (here/'logs/tools-build-deps.log').open('w') as log:
    subprocess.run(['apt-get', *options, 'update'], stdout=log, stderr=log, check=True)
    subprocess.run(['apt-get', *options, '--download-only', '-y', 'install',
        'libmpfr-dev', 'libgmp-dev', 'libsigsegv-dev', 'libreadline-dev', 'libselinux1-dev'],
        stdout=log, stderr=log, check=True)
    for archive in sorted((apt/'archives').glob('*.deb')):
        subprocess.run(['dpkg-deb', '-x', archive, root], check=True, stdout=log, stderr=log)
        log.write(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
    log.write('TOOLS PRIVATE BUILD DEPENDENCIES PASS\n')
