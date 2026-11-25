#!/usr/bin/python3
"""For one declaration and each archive state: unpack the packages and compare every
reader override's `original_sha256` with the package file it would replace."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import assemble

declaration = Path(sys.argv[1]).resolve()  # the package tool needs absolute folders
original = declaration.read_text()
first = re.search(r'^snapshot (\S+)$', original, re.M).group(1)
states = [first]+[lock.stem for lock in sorted((assemble.HERE/'components').glob('*Z.txt')) if lock.stem != first]


def candidates(snapshot, names, work):
    """The release each named package has in this archive state."""
    apt = work/'apt-candidates'
    for sub in ('lists/partial', 'archives/partial', 'etc'):
        (apt/sub).mkdir(parents=True, exist_ok=True)
    (apt/'status').write_text('')
    (apt/'etc/sources.list').write_text(assemble.sources(snapshot))
    opts = ['-o', f'Dir::State::status={apt}/status', '-o', f'Dir::State::lists={apt}/lists',
            '-o', f'Dir::Cache::archives={apt}/archives', '-o', f'Dir::Etc::sourcelist={apt}/etc/sources.list',
            '-o', 'Dir::Etc::sourceparts=-', '-o', 'APT::Install-Recommends=false', '-o', 'APT::Sandbox::User=root',
            '-o', 'Acquire::Check-Valid-Until=false', '-o', 'Dir::Cache::pkgcache=', '-o', 'Dir::Cache::srcpkgcache=',
            '-o', 'Acquire::Languages=none', '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-']
    subprocess.run(['apt-get', *opts, 'update'], check=True, stdout=subprocess.DEVNULL)
    result = {}
    for name in names:
        output = subprocess.run(['apt-cache', *opts, 'policy', name], check=True, capture_output=True, text=True).stdout
        found = re.search(r'^\s+Candidate: (\S+)$', output, re.M)
        result[name] = found.group(1) if found else None
    return result


for snapshot in states:
    work = declaration.parent/('work-'+snapshot)
    work.mkdir()
    text = original.replace('snapshot '+first, 'snapshot '+snapshot)
    if snapshot != first:
        names = [shlex.split(line)[1] for line in text.splitlines() if line.startswith('package ')]
        wanted = candidates(snapshot, names, work)
        lines = []
        for line in text.splitlines():
            row = shlex.split(line, comments=True)
            if row[:1] == ['package'] and wanted.get(row[1]):
                line = shlex.join(['package', row[1], wanted[row[1]]])
            lines.append(line)
        text = '\n'.join(lines)+'\n'
    path = work/'declaration.conf'
    path.write_text(text)
    print('=== archive state', snapshot, flush=True)
    try:
        rows, parsed = assemble.parse(path)
        debs = assemble.packages(work, rows, parsed)
    except (ValueError, subprocess.CalledProcessError) as error:
        print('RESULT', snapshot, 'packages not resolved:', error, flush=True)
        shutil.rmtree(work, ignore_errors=True)
        continue
    root = work/'root'
    root.mkdir()
    assemble.payload(root, debs)
    versions = dict(re.findall(r'^Package: (\S+)\n(?:.*\n)*?Version: (\S+)$', (root/'var/lib/dpkg/status').read_text(), re.M))
    directory = root/'usr/lib/confos/reader-overrides'
    mismatched = 0
    for item in json.loads((directory/'manifest.json').read_text()):
        if item['package'] not in versions:
            continue
        target = root/item['target'].lstrip('/')
        expected = item.get('original_sha256')
        if not target.is_file() or target.is_symlink():
            state = 'TARGET ABSENT'
        elif expected is None:
            state = 'no original recorded (replaced whatever the release)'
        elif hashlib.sha256(target.read_bytes()).hexdigest() == expected:
            state = 'original matches'
        else:
            state = 'ORIGINAL DIFFERS'
        mismatched += state in ('ORIGINAL DIFFERS', 'TARGET ABSENT')
        print(f"{snapshot} {item['package']} {versions[item['package']]} built-from {item.get('source_version')} "
              f"{item['target']}: {state}", flush=True)
    print('RESULT', snapshot, 'overrides whose package file is not the one they were built from:', mismatched, flush=True)
    shutil.rmtree(work, ignore_errors=True)
