#!/usr/bin/python3
"""Canonical root-session mutation probes; no private pre-seeded store fixtures."""
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp

assert os.geteuid() == 0
assert Path('/proc/self/attr/current').read_text().strip() == 'confos-session (enforce)'
def snapshot():
    result = {}
    for root in map(Path, ('/var/lib/dpkg', '/var/lib/apt', '/var/spool/cron')):
        assert root.is_dir(), root
        for path in [root, *sorted(root.rglob('*'))]:
            stat = path.lstat()
            result[str(path)] = [stat.st_mode, stat.st_uid, stat.st_gid,
                os.readlink(path) if path.is_symlink() else
                hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None]
    result['declaration'] = hashlib.sha256(Path('/state/declaration.conf').read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
commands = {}
for name in ('apt-mark', 'crontab', 'dpkg'):
    commands[name] = next(str(path) for path in (Path('/usr/lib/confos/native')/name, Path('/usr/bin')/name)
                          if path.is_file() and path.read_bytes()[:4] == b'\x7fELF')
def invoke(args, data=None, denial=False):
    before = snapshot()
    result = sp.run(args, input=data, text=True, stdout=sp.PIPE, stderr=sp.STDOUT, timeout=20)
    after = snapshot()
    print('NATIVE42 CONFIG', args, 'EXIT', result.returncode, 'OUTPUT', result.stdout,
          'BEFORE', before, 'AFTER', after, flush=True)
    assert before == after
    if denial:
        assert result.returncode != 0
        assert any(word in result.stdout.lower() for word in
                   ('permission denied', 'operation not permitted', 'do not have permission to lock'))
    return result.returncode, result.stdout
queries = [[commands['apt-mark'], option] for option in ('showhold', 'showauto', 'showmanual')]
queries += [[commands['dpkg'], '--get-selections', 'cron'], [commands['crontab'], '-u', 'user', '-l']]
before = [invoke(args) for args in queries]
assert all(item[0] == 0 for item in before[:-1])
# No claim of changing an existing crontab: the canonical image has no such row.
assert before[-1][0] == 1 and 'no crontab' in before[-1][1].lower()
request = Path('/tmp/native42-request.cron')
request.write_text('* * * * * /usr/bin/touch /tmp/native42-forbidden-marker\n')
invoke([commands['apt-mark'], 'hold', 'cron'], denial=True)
invoke([commands['apt-mark'], 'auto', 'cron'], denial=True)
invoke([commands['crontab'], '-u', 'user', str(request)], denial=True)
invoke([commands['dpkg'], '--set-selections'], 'cron hold\n', denial=True)
assert [invoke(args) for args in queries] == before
print('NATIVE42 FOUR MUTATIONS REFUSED QUERIES STORES DECLARATION UNCHANGED')
