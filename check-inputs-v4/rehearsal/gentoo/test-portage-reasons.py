#!/usr/bin/env python3
"""Synthetic native API fixture: distinguish selection evidence from graph guesses."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import types

portage = types.ModuleType('portage')
portage.settings = {'EROOT': '/'}
class Database:
    def match(self, atom):
        return {'category/chosen': ['category/chosen-1'],
                'category/slots': ['category/slots-1', 'category/slots-2']}[atom]
    def cpv_all(self):
        return ['category/chosen-1', 'category/slots-1', 'category/slots-2',
                'category/oneshot-1', 'category/possible-dependency-1']
portage.db = {'/': {'vartree': types.SimpleNamespace(dbapi=Database())}}
sets = types.ModuleType('portage._sets')
sets.load_default_config = lambda settings, trees: types.SimpleNamespace(
    getSetAtoms=lambda name: ['category/chosen', 'category/slots'])
sys.modules['portage'] = portage
sys.modules['portage._sets'] = sets
output = io.StringIO()
with contextlib.redirect_stdout(output):
    runpy.run_path(str(Path(__file__).resolve().parents[2] / 'collector/portage-reasons.py'))
rows = [json.loads(line) for line in output.getvalue().splitlines()]
assert len(rows) == 5
assert [r['cpv'] for r in rows if r['reason'] == 'explicit'] == ['category/chosen-1']
assert sum(r['reason'] == 'unknown' for r in rows) == 4
assert all(r['reason'] != 'dependency' for r in rows)
print('PASS: unique selection explicit; ambiguous slots, unrecorded direct requests and graph-only relationships unknown')
