#!/usr/bin/python3
"""Additional exact inputs and native recipes for the42 prebuilt component."""
from pathlib import Path
import subprocess
import sys

assert Path('VERSION').read_text().strip() in ('0.42', '0.43', '0.44', '0.45', '0.46','0.47','0.48','0.49')
subprocess.run(['python3', 'verify-curl-config-metadata-draft.py'], check=True, stdout=sys.stderr)
work = Path('interpreter-inputs/curl-config-draft')
assert not (work/'guest').exists()
assert not list(work.rglob('*.qcow2'))
names = ['advance-readers-release-042.py', 'prepare-readers-042.py', 'readers-archive-paths-042.py',
    'prepare-readers-042.sh', 'probe-readers-042.sh', 'check-reader-inheritance-042.py',
    'document-readers-042.py', 'archive-readers-042.sh', 'cleanup-readers-042.sh', 'sync-readers-042.sh',
    'patch-optional-identity-042.py', 'check-optional-identity-042.py', 'patch-native-config-draft.py',
    'build-readers-fixture-042.py', 'native-config-probe-042.py',
    'patch-pdb-gyp-draft.py', 'pdb-gyp-draft', 'pdb-gyp-patched-draft', 'pdb-gyp-evidence.tar.gz',
    'PDB-GYP-DRAFT.md', 'PDB-GYP-RESULTS.md', 'NATIVE-CONFIG-RESULTS.md', 'native-config-evidence.tar.gz',
    'curl-config-metadata-draft.json', 'verify-curl-config-metadata-draft.py',
    'prepare-curl-config-draft.py', 'patch-curl-config-draft.py', 'build-curl-config-draft.py',
    'probe-curl-config-draft.py', 'collect-curl-config-draft.py', 'curl-config-draft.md',
    'curl-config-draft-evidence', 'curl-config-guest-draft-evidence', str(work),
    'records/reader-inheritance-0.42.json',
    'packages/confos-code-readers_0.41_amd64.deb', 'packages/confos-code-readers_0.41_amd64.deb.sha256']
for name in names:
    assert Path(name).exists(), name
    sys.stdout.buffer.write(name.encode()+b'\0')
