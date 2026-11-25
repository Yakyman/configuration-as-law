#!/usr/bin/python3
"""Fetch every release of the office suite's core package that the pinned archive states offer and
extract the merged core library that holds its Basic interpreter.

Usage: fetch-basic-library.py OUT_DIR
Writes OUT_DIR/RELEASE/libmergedlo.so, OUT_DIR/RELEASE/archive.sha256 and OUT_DIR/releases.json
(release -> states that offer it, archive name and checksum, library checksum).
Runs on the build host; needs apt-get, dpkg-deb and network access to the pinned archive.
"""
import hashlib
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import archive_sources  # noqa: E402

PACKAGE = 'libreoffice-core'
MEMBER = './usr/lib/libreoffice/program/libmergedlo.so'
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
states = sorted(json.loads((HERE/'archive-sources.json').read_text()))
found = {}
for state in states:
    apt = out/('apt-'+state)
    for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
        (apt/sub).mkdir(parents=True, exist_ok=True)
    (apt/'status').write_text('')
    (apt/'etc/sources.list').write_text(archive_sources.sources(state))
    opts = ['-o', f'Dir::State::status={apt}/status', '-o', f'Dir::State::lists={apt}/lists',
            '-o', f'Dir::Cache::archives={apt}/archives', '-o', f'Dir::Etc::sourcelist={apt}/etc/sources.list',
            '-o', 'Dir::Etc::sourceparts=-', '-o', 'APT::Sandbox::User=root', '-o', 'APT::Architecture=amd64',
            '-o', 'Acquire::Check-Valid-Until=false', '-o', 'Acquire::Retries=3', '-o', f'Dir::Log={apt}/log',
            '-o', 'Dir::Cache::pkgcache=', '-o', 'Dir::Cache::srcpkgcache=', '-o', 'Acquire::Languages=none',
            '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-']
    subprocess.run(['apt-get', *opts, 'update'], check=True, stdout=subprocess.DEVNULL)
    listing = subprocess.check_output(['apt-cache', *opts, 'madison', PACKAGE], text=True)
    for release in sorted({line.split('|')[1].strip() for line in listing.splitlines() if '|' in line}):
        entry = found.setdefault(release, {'states': []})
        entry['states'].append(state)
        if 'library_sha256' in entry:
            continue
        subprocess.run(['apt-get', *opts, 'download', PACKAGE+'='+release], check=True, cwd=apt/'archives',
                       stdout=subprocess.DEVNULL)
        archive = next(p for p in (apt/'archives').glob(PACKAGE+'_*.deb')
                       if subprocess.check_output(['dpkg-deb', '-f', str(p), 'Version'], text=True).strip() == release)
        folder = out/re.sub(r'[^A-Za-z0-9.+~-]', '_', release)
        folder.mkdir(exist_ok=True)
        process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(archive)], stdout=subprocess.PIPE)
        with tarfile.open(fileobj=process.stdout, mode='r|') as stream:
            for member in stream:
                if member.name == MEMBER:
                    (folder/'libmergedlo.so').write_bytes(stream.extractfile(member).read())
        process.wait()
        entry['archive'] = archive.name
        entry['archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        entry['library_sha256'] = hashlib.sha256((folder/'libmergedlo.so').read_bytes()).hexdigest()
        (folder/'archive.sha256').write_text(entry['archive_sha256']+'  '+archive.name+'\n')
        archive.unlink()
(out/'releases.json').write_text(json.dumps(found, indent=1, sort_keys=True)+'\n')
print(json.dumps(found, indent=1, sort_keys=True))
