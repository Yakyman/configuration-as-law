#!/usr/bin/env python3
"""History 4 action tables at its four observation points (OBSERVE-8 (c)), rendered offline from raw/h4."""
import json
import pathlib
import sys

d = pathlib.Path(sys.argv[1])
plan = json.load(open(sys.argv[2]))
out = pathlib.Path(sys.argv[3])
cmds = {c['name']: c for c in json.load(open(d / 'commands.json'))}
events = {e['event']: e['utc'] for e in json.load(open(d / 'install/host-events.json'))}
g = {'exit': 1, 'started_utc': '2026-11-23T19:00:50.353097+00:00', 'finished_utc': '2026-11-23T19:01:46.995419+00:00',
     'valid_cut': True, 'cut_seen_utc': '2026-11-23T19:00:50.374448+00:00',
     'stdout': 'FAILED recovery incomplete: readback mismatch: port:udp:1; restoration mismatch: port:udp:1'}
# values above are copied from install/guest.json (keys exit, started_utc, finished_utc, valid_cut, cut_seen_utc, stdout)
dev = plan['h2']
unavail = 'unavailable: guest session exited 255 (no login) at {}; see {}'
points = ['h4-install-disconnected', 'h4-install-restored', 'h4-install-after-restored-retry', 'h4-end']
for i, point in enumerate(points):
    t = []
    t.append({'action': 'h4.install', 'command_record': 'install-host-cut', 'started_utc': g['started_utc'],
              'ended_utc': g['finished_utc'], 'done': False, 'evidence': ['install/guest.json (exit, stdout)'],
              'reason': 'installer exit 1 while disconnected: ' + g['stdout']})
    t.append({'action': 'h4.install-network-down', 'command_record': 'install-host-cut', 'started_utc': events['cut-request'],
              'ended_utc': g['cut_seen_utc'], 'done': True,
              'evidence': ['install/host-events.json', 'install/guest.json (active_at_cut, carrier_at_cut, valid_cut=true)'],
              'reason': None})
    if i == 0:
        t.append(dict(action='h4.install-network-restored', command_record=None, started_utc=None, ended_utc=None,
                      done=False, evidence=[], reason='not yet reached'))
    else:
        t.append({'action': 'h4.install-network-restored', 'command_record': 'install-host-cut',
                  'started_utc': events['restore-request'], 'ended_utc': events['transport-finished'], 'done': True,
                  'evidence': ['install/host-events.json', 'install/guest.json (carrier_at_output ens3=1)'], 'reason': None})
    if i < 2:
        t.append(dict(action='h4.install-restored-retry-if-failed', command_record=None, started_utc=None, ended_utc=None,
                      done=False, evidence=[], reason='not yet reached'))
    else:
        c = cmds['install-restored-retry']
        t.append({'action': 'h4.install-restored-retry-if-failed', 'command_record': c['name'], 'started_utc': c['started_utc'],
                  'ended_utc': c['ended_utc'], 'done': False, 'evidence': [c['name'] + '.stdout', c['name'] + '.stderr'],
                  'reason': unavail.format(c['ended_utc'], 'commands.json')})
    t.append(dict(action='h4.worker-run', command_record=None, started_utc=None, ended_utc=None, done=False, evidence=[],
                  reason='not yet reached' if i < 3 else 'not reached: prerequisite failed (installation not done)'))
    for a in ['h4.development-network-down', 'h4.development-network-restored', 'h4.development-restored-retry-if-failed']:
        t.append(dict(action=a, command_record=None, started_utc=None, ended_utc=None, done=False, evidence=[],
                      reason='not yet reached' if i < 3 else 'not reached: prerequisite failed (development prefix unavailable)'))
    for a in dev:
        e = dict(action='h4.dev.' + a, command_record=None, started_utc=None, ended_utc=None, done=False, evidence=[],
                 reason='not yet reached')
        if i == 3:
            c = cmds['h4-development-prefix']
            if a in ('h2.1.fetch', 'h2.1.original.build'):
                e.update(command_record=c['name'], started_utc=c['started_utc'], ended_utc=c['ended_utc'],
                         evidence=[c['name'] + '.stdout', c['name'] + '.stderr'],
                         reason=unavail.format(c['ended_utc'], 'commands.json'))
            else:
                e['reason'] = 'not reached: prerequisite failed (development prefix unavailable)'
        t.append(e)
    (out / ('actions-' + point + '.json')).write_text(json.dumps(t, indent=1) + '\n')
print('written', len(points))
