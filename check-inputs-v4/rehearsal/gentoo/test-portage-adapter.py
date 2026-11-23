#!/usr/bin/env python3
"""Synthetic records only: no guest or host inventory is queried."""
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('packages', Path(__file__).resolve().parents[2] / 'collector/packages.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class Context:
    def __init__(self):
        self.entries = {'/var/db/pkg/category/test-1/CONTENTS': {},
                        '/owned': {'type': 'directory'},
                        '/owned/link': {'type': 'symlink', 'target': 'target'},
                        '/owned/changed': {'type': 'symlink', 'target': 'other'},
                        '/owned/unreadable': {'type': 'symlink', 'target_error': 'denied'}}
        self.owned = {}; self.package_files = []; self._native_package_ids = set()
        self._package_digest_jobs = []; self.gaps = []; self.package_ownership_complete = True
    def add(self, *args, **kw): return 'package-id'
    def query(self, *args, **kw):
        return b'{"cpv":"category/test-1","reason":"explicit"}\n', 0, 'synthetic-reason'
    def safe_read(self, *args, **kw):
        return b'dir /owned\nsym /owned/link -> target 1\nsym /owned/changed -> target 1\nsym /owned/unreadable -> target 1\n', 0, 'synthetic-manifest'
c = Context(); m.portage(c)
assert c.owned['/owned'] == {'package-id'}
assert len(c.package_files) == 3
assert [r['integrity'] for r in c.package_files] == ['unchanged', 'changed', 'unknown']
assert not c.gaps
print('PASS: directory ownership retained; equal, changed and unreadable symlink targets handled distinctly.')
