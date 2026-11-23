#!/usr/bin/env python3
"""Read Portage's selected records; never run an ebuild or infer history."""
import json
import portage
from portage._sets import load_default_config

settings = portage.settings
trees = portage.db[settings['EROOT']]
db = trees['vartree'].dbapi
sets = load_default_config(settings, trees)
selected = sets.getSetAtoms('selected')
explicit = set()
for atom in selected:
    matches = db.match(str(atom))
    # A version/slot-ambiguous selected atom does not prove every matching
    # installed version was directly selected.
    if len(matches) == 1:
        explicit.add(matches[0])

# --oneshot can install a direct request without recording it in selected.
# Current dependency edges likewise do not prove historical installation reason.
for cpv in sorted(db.cpv_all()):
    print(json.dumps({'cpv': cpv, 'reason': 'explicit' if cpv in explicit else 'unknown'}))
