#!/usr/bin/env python3
"""Writes the fixture of test.sh ([f7]): two inventories (base/, inv/) that hold the same stored files, the machine
inventory with processes, ports and login scopes besides; a derivation with two `service` lines.

Stored files (equal in both inventories, so every one of them follows from what the baseline has):
  /usr/bin/sleep (A), /usr/bin/tail (E), /usr/bin/cat (F), /opt/unread (U),
  /usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/active/files/bin/mpv (B).
Processes of the machine:
  /app/bin/mpv            file B   path not stored, file stored and recorded   -> placed by the checksum
  /tmp/ns-planted         file C   path not stored, file not stored             -> reported
  /usr/bin/tail           file D   path stored with E, file not stored          -> reported (not placed by the path)
  /usr/bin/sleep          file A   path stored with A                           -> placed by the path
  /opt/unread             file unreadable (both ways)                           -> reported (not placed by its path)
  /usr/bin/sleep (deleted) file A, but deleted                                  -> reported (no stored object)
  /usr/bin/cat#sha256=F   file F   split object: same path, two files           -> placed
  /usr/bin/cat#sha256=G   file G                                                -> reported
Ports: one held by /app/bin/mpv (placed), one by /tmp/ns-planted (reported).
Scopes: session-8 with member /app/bin/mpv (placed), session-9 with member /usr/bin/tail (reported).
Service lines (derived mode): sleep (its process runs the stored file: matched), tail (its process runs another
file than the stored one: not placed by the path, MISSING), unreader (its process file could not be read: UNVERIFIED).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def h(c):
    return c * 64


MPV = '/usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/active/files/bin/mpv'
STORED = [('/usr/bin/sleep', h('a')), ('/usr/bin/tail', h('e')), ('/usr/bin/cat', h('f')), ('/opt/unread', h('1')),
          (MPV, h('b'))]


def stored():
    out = [{'kind': 'meta', 'id': 'meta', 'value': {}}]
    for p, s in STORED:
        out.append({'kind': 'file', 'id': p, 'mode': '0755', 'uid': 0, 'gid': 0, 'size': 1000, 'sha256': s,
                    'exec': True, 'exec_reason': 'elf', 'fs': '@part1'})
    return out


def proc(oid, exe, sha, args):
    v = {'users': ['root'], 'count': 1, 'args': [args]}
    if exe is not None:
        v['exe'] = exe
        v['exe_sha256'] = sha
    return {'kind': 'process', 'id': oid, 'value': v}


def force():
    return [
        proc('/app/bin/mpv', '/app/bin/mpv', h('b'), '/app/bin/mpv --idle'),
        proc('/tmp/ns-planted', '/tmp/ns-planted', h('c'), '/tmp/ns-planted 86403'),
        proc('/usr/bin/tail', '/usr/bin/tail', h('d'), '/usr/bin/tail 86404'),
        proc('/usr/bin/sleep', '/usr/bin/sleep', h('a'), '/usr/bin/sleep infinity'),
        proc('/opt/unread', '/opt/unread', '', '/opt/unread --serve'),
        proc('/usr/bin/sleep (deleted)', '/usr/bin/sleep (deleted)', h('a'), 'sleep 77'),
        proc('/usr/bin/cat#sha256=' + h('f'), '/usr/bin/cat', h('f'), 'cat'),
        proc('/usr/bin/cat#sha256=' + h('9'), '/usr/bin/cat', h('9'), 'cat -'),
        {'kind': 'port', 'id': 'tcp/0.0.0.0:7001', 'value': {'exe': ['/app/bin/mpv']}},
        {'kind': 'port', 'id': 'tcp/0.0.0.0:7002', 'value': {'exe': ['/tmp/ns-planted']}},
        {'kind': 'unit', 'id': 'system/session-8.scope',
         'value': {'enabled': 'transient', 'active': 'active', 'transient': True, 'members': ['/app/bin/mpv']}},
        {'kind': 'unit', 'id': 'system/session-9.scope',
         'value': {'enabled': 'transient', 'active': 'active', 'transient': True, 'members': ['/usr/bin/tail']}},
    ]


def write(path, objs):
    with open(path, 'w', encoding='utf-8') as f:
        for o in objs:
            f.write(json.dumps(o, sort_keys=True) + '\n')


def main():
    for d in ('base', 'inv'):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    write(os.path.join(HERE, 'base', 'stored.jsonl'), stored())
    write(os.path.join(HERE, 'base', 'force.jsonl'), [])
    write(os.path.join(HERE, 'inv', 'stored.jsonl'), stored())
    write(os.path.join(HERE, 'inv', 'force.jsonl'), force())
    write(os.path.join(HERE, 'derived.jsonl'), [
        {'kind': 'unit', 'id': 'service:sleeper', 'line': 'd:1',
         'value': {'name': 'sleeper', 'enabled': True, 'argv': ['/usr/bin/sleep', 'infinity']}},
        {'kind': 'unit', 'id': 'service:unreader', 'line': 'd:3',
         'value': {'name': 'unreader', 'enabled': True, 'argv': ['/opt/unread', '--serve']}},
        {'kind': 'unit', 'id': 'service:tailer', 'line': 'd:2',
         'value': {'name': 'tailer', 'enabled': True, 'argv': ['/usr/bin/tail', '86404']}}])
    with open(os.path.join(HERE, 'decl.conf'), 'w') as f:
        f.write('service sleeper /usr/bin/sleep infinity\nservice tailer /usr/bin/tail 86404\nservice unreader /opt/unread --serve\n')


if __name__ == '__main__':
    main()
