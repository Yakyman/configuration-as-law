#!/usr/bin/python3
"""Host-context original-object assertions, including explicit root invocation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

root = Path('/usr/lib/confos/flatpak')
items = json.loads(Path('/usr/lib/confos/flatpak-reader-overrides/manifest.json').read_text())
items = [item for item in items if item['ref'].startswith('app/io.mpv.Mpv/')]
assert len(items) == 3
for item in items:
    target = root/item['ref']/item['commit']/'files'/item['target']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256']
    for relative in item['objects']:
        original = root/relative
        assert original.is_file() and not original.is_symlink()
        assert hashlib.sha256(original.read_bytes()).hexdigest() == item['original_sha256']
        assert not os.path.samefile(target, original)
        if item['target'] == 'bin/mpv':
            attempts = [[str(original), '--version'], ['/lib64/ld-linux-x86-64.so.2', str(original), '--version']]
        else:
            attempts = [['python3', '-c', 'import ctypes,sys; ctypes.CDLL(sys.argv[1]); print("ORIGINAL-ALIAS-RAN")', str(original)]]
        attempts.append(['python3', '-c',
            'import mmap,sys; f=open(sys.argv[1],"rb"); mmap.mmap(f.fileno(),0,flags=mmap.MAP_PRIVATE,prot=mmap.PROT_READ|mmap.PROT_EXEC); print("ORIGINAL-ALIAS-RAN")', str(original)])
        for prefix in ([], ['sudo', '-n']):
            for command in attempts:
                stdout = ''
                try:
                    result = subprocess.run(prefix+command, capture_output=True, text=True, timeout=15)
                    stdout = result.stdout
                    output = result.stdout+result.stderr
                    assert result.returncode != 0, output
                except PermissionError as error:
                    output = str(error)
                print('ORIGINAL ALIAS', prefix+command, output, flush=True)
                # Python tracebacks quote source containing the marker string;
                # only the actual stdout line would establish its execution.
                assert 'ORIGINAL-ALIAS-RAN' not in stdout.splitlines()
                assert any(value in output.lower() for value in ('permission denied', 'operation not permitted', 'failed to map segment')), output
print('MPV41 ORIGINAL OBJECT ALIASES PASS', flush=True)
