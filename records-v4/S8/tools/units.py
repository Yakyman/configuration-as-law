#!/usr/bin/env python3
"""For enabled/alias units without a unit row: list their enablement links in the census and whether each link
has an own claim (machine file or filesystem object) that matches (S8 reading aid; offline)."""
import json
import sys

o = json.load(open(sys.argv[1]))
s = json.load(open(sys.argv[2]))
files = o['independent_census']['files']
rel = o['p1_file_relations']
units = [u for u, _ in s['enabled_units_without_unit_row']]
out = {}
for u in units:
    links = []
    for p, st in files.items():
        if st.get('kind') != 'symlink':
            continue
        if p.startswith(('/etc/systemd/', '/usr/lib/systemd/')) and (p.endswith('/' + u) or st.get('target', '').endswith('/' + u)):
            comps = rel.get(p, {}).get('own_line_comparisons', [])
            links.append({'path': p, 'target': st.get('target'),
                          'claims': [c['line'] for c in comps],
                          'matching': any(c['state_matches'] for c in comps)})
    # the unit file itself
    unit_files = []
    for p, st in files.items():
        if p in ('/usr/lib/systemd/system/' + u, '/etc/systemd/system/' + u, '/lib/systemd/system/' + u):
            comps = rel.get(p, {}).get('own_line_comparisons', [])
            unit_files.append({'path': p, 'kind': st.get('kind'), 'claims': [c['line'] for c in comps],
                               'matching': any(c['state_matches'] for c in comps)})
    out[u] = {'links': links, 'unit_files': unit_files}
print(json.dumps(out, indent=1))
