#!/usr/bin/env python3
"""Render the cumulative ordinary-action table (OBSERVE-8 (c)) for one observation point, offline.

usage: actions.py HISTORY_DIR PLAN_JSON HISTORY POINT_LABEL [extra.json]
An action is done only if an ACTION_DONE marker for it appears in a guest session that ended before the
observation of POINT_LABEL began (or, for restarts, restart-N.json says done). extra.json may supply
special entries (history 4 interruption actions) as {action: {done, evidence, reason, started_utc, ended_utc}}.
"""
import json
import pathlib
import re
import sys

d = pathlib.Path(sys.argv[1])
plan = json.load(open(sys.argv[2]))
history, point = sys.argv[3], sys.argv[4]
extra = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
commands = json.load(open(d / 'commands.json'))
cut = next((c['started_utc'] for c in commands if c['name'] == point), None)
if cut is None:  # disconnected h4 points are recorded inside the cut command
    cut = extra.get('_point_utc', {}).get(point)
before = [c for c in commands if cut is None or c['ended_utc'] <= cut]
marks = {}
failed = []
for c in before:
    out = d / (c['name'] + '.stdout')
    if not out.exists():
        continue
    text = out.read_text(errors='replace')
    for m in re.finditer(r'^ACTION_(BEGIN|DONE|FAILED) (\S+)', text, re.M):
        marks.setdefault(m.group(2), {})[m.group(1)] = c
    for m in re.finditer(r'^ACTION_FAILED (.*)$', text, re.M):
        failed.append({'command_record': c['name'], 'marker': m.group(1)})
names = plan[history] if history != 'h4' else extra.get('_order', plan['h4'])
table = []
prior_failed = False
for name in names:
    e = {'action': name, 'command_record': None, 'started_utc': None, 'ended_utc': None,
         'done': False, 'evidence': [], 'reason': 'not yet reached'}
    if name in extra:
        e.update(extra[name])
    elif re.match(r'h1\.restart-(\d)', name):
        n = name[-1]
        p = d / ('restart-' + n + '.json')
        c = next((c for c in before if c['name'] == 'restart-' + n + '-request'), None)
        if p.exists() and c:
            r = json.load(open(p))
            e.update(command_record='restart-' + n + '-request', started_utc=r['started_utc'], ended_utc=r['ended_utc'],
                     done=bool(r.get('done')), evidence=['restart-' + n + '.json'],
                     reason=None if r.get('done') else 'boot id unchanged or access not regained')
    elif name in marks:
        m = marks[name]
        c = m.get('DONE') or m.get('BEGIN')
        e.update(command_record=c['name'], started_utc=c['started_utc'], ended_utc=c['ended_utc'],
                 evidence=[c['name'] + '.stdout', c['name'] + '.stderr'])
        if 'DONE' in m:
            e.update(done=True, reason=None)
        else:
            e['reason'] = 'ACTION_BEGIN without ACTION_DONE (command failed, exit %s)' % c.get('exit')
            prior_failed = True
    elif prior_failed or failed:
        e['reason'] = 'not reached: prerequisite failed'
    table.append(e)
print(json.dumps(table, indent=1))
