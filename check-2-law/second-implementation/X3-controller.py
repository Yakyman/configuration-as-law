#!/usr/bin/python3
"""X3 disposable instrument: SQLite authority ledger and derivative reference counting."""
import grp
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import socket
import sqlite3
import stat
import struct
import subprocess
import tempfile

STORE = Path('/var/lib/cal')
CONSTITUTION = Path('/etc/cal/root.json')
ACCOUNTS = ('alice', 'bob')
PROGRAMS = frozenset(('alpha', 'beta', 'hello', 'figlet', 'python', 'node', 'browser'))
CHANNELS = frozenset(('package', 'pip', 'npm', 'flatpak', 'appimage', 'download', 'build', 'systemd', 'cron', 'interpreter'))
DB = None


def guard(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def object_fields(value, allowed, label):
    guard(type(value) is dict, label + ': expected object')
    guard(not (value.keys() - allowed), label + ': unsupported field')
    return value


def members(value, choices, label):
    guard(type(value) is list, label + ': expected list')
    guard(all(type(x) is str and x in choices for x in value), label + ': unsupported member')
    return sorted(set(value))


def version(value):
    guard(type(value) is str and re.fullmatch('[A-Za-z0-9._-]{1,40}', value), 'invalid program version')
    return value


def publish(path, value):
    # Export files are observations; SQLite is the committed authority.
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix='.x3-')
    try:
        with os.fdopen(handle, 'w') as stream:
            os.fchmod(stream.fileno(), 0o644)
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def latest():
    row = DB.execute('SELECT body FROM snapshots WHERE id=(SELECT snapshot FROM head WHERE singleton=1)').fetchone()
    return json.loads(row[0]) if row else {}


def load_personal(user):
    account = pwd.getpwnam(user)
    path = Path(account.pw_dir) / 'declaration.json'
    try:
        handle = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return {'programs': {}}
    with os.fdopen(handle, 'r') as stream:
        info = os.fstat(stream.fileno())
        guard(stat.S_ISREG(info.st_mode), 'personal declaration is not a regular file')
        guard(info.st_uid in (0, account.pw_uid), 'personal declaration has wrong owner')
        guard(info.st_size <= 65536, 'personal declaration exceeds bound')
        text = stream.read(65537)
        guard(len(text) <= 65536, 'personal declaration exceeds bound')
        return json.loads(text)


def compile_request(uid):
    root = json.loads(CONSTITUTION.read_text())
    object_fields(root, {'archive', 'programs', 'policies', 'allow_channels', 'shared', 'system_update'}, 'root')
    guard(root.get('archive') in ('keep', 'delete'), 'explicit archive choice required; O6 undecided')
    guard('system_update' not in root or type(root['system_update']) is str, 'system_update must be a string')
    catalog = root.get('programs', {})
    object_fields(catalog, PROGRAMS, 'root programs')
    resolved = {}
    for name, spec in catalog.items():
        object_fields(spec, {'version', 'scope', 'owners'}, name)
        scope = spec.get('scope', 'system')
        guard(scope in ('system', 'user'), 'invalid program scope')
        resolved[name] = {'version': version(spec.get('version', '1')), 'scope': scope,
                          'owners': members(spec.get('owners', []), ACCOUNTS, 'owners')}
    policies = object_fields(root.get('policies', {}), set(ACCOUNTS), 'policies')
    for user, policy in policies.items():
        object_fields(policy, {'allowlist', 'denylist'}, 'policy')
        for name, values in policy.items():
            members(values, PROGRAMS, name)
    channels = object_fields(root.get('allow_channels', {}), set(ACCOUNTS), 'channels')
    for user, values in channels.items():
        members(values, CHANNELS, 'channel list')
    shared = root.get('shared', {})
    guard(type(shared) is dict, 'shared must be an object')
    for name, owners in shared.items():
        guard(type(name) is str and re.fullmatch('[a-z][a-z0-9-]{0,39}', name), 'invalid shared identity')
        members(owners, PROGRAMS, 'shared owners')
    if uid == 0:
        personal = {user: load_personal(user) for user in ACCOUNTS}
    else:
        account = pwd.getpwuid(uid).pw_name
        guard(account in ACCOUNTS, 'account not enrolled')
        previous = latest()
        guard(previous.get('root') == root, 'unapplied root edit requires root')
        personal = previous.get('personal', {}).copy()
        personal[account] = load_personal(account)
    for user, document in personal.items():
        object_fields(document, {'programs'}, 'personal document')
        entries = object_fields(document.get('programs', {}), PROGRAMS, 'personal programs')
        limits = policies.get(user, {})
        for name, spec in entries.items():
            object_fields(spec, {'version'}, 'personal program')
            release = version(spec.get('version', '1'))
            guard(name not in limits.get('denylist', []), 'root denylist forbids program')
            guard('allowlist' not in limits or name in limits['allowlist'], 'root allowlist excludes program')
            if name in resolved:
                guard(resolved[name]['version'] == release, 'incompatible owner versions')
                resolved[name]['owners'] = sorted(set(resolved[name]['owners']) | {user})
            else:
                resolved[name] = {'version': release, 'scope': 'user', 'owners': [user]}
    return {'root': root, 'personal': personal, 'programs': resolved, 'shared': shared,
            'archive': root['archive'], 'allow_channels': channels}


def references(document):
    installed = set(document.get('programs', {}))
    return installed | {'shared-' + key for key, owners in document.get('shared', {}).items() if installed.intersection(owners)}


def trim_archive(document):
    if document.get('archive') != 'delete':
        return
    retained = references(document)
    for row in DB.execute('SELECT body FROM snapshots'):
        retained.update(references(json.loads(row[0])))
    for directory in (STORE / 'archive').iterdir():
        if directory.name not in retained:
            shutil.rmtree(directory)


def materialize(document):
    pending = STORE / 'pending.json'
    publish(pending, document)
    hook = subprocess.run(['/usr/local/lib/cal/apply-policy', str(pending)], capture_output=True, text=True, timeout=120)
    guard(hook.returncode == 0, 'external policy failure (may partially mutate): ' + hook.stdout + hook.stderr)
    desired = references(document)
    for directory in (STORE / 'active').iterdir():
        if directory.name not in desired:
            target = STORE / 'archive' / directory.name
            guard(not target.exists(), 'derivative identity collision')
            directory.rename(target)
    for name in sorted(desired):
        active, archived = STORE / 'active' / name, STORE / 'archive' / name
        if not active.exists():
            if archived.exists():
                archived.rename(active)
            else:
                active.mkdir(mode=0o755)
        item = document['programs'].get(name, {})
        if name.startswith('shared-'):
            if not (active / 'cache').exists():
                (active / 'cache').write_text('X3 shared derivative\n')
            owners = sorted({user for owner in document['shared'][name[7:]]
                             for user in document['programs'].get(owner, {}).get('owners', [])})
            user_scope = True
        else:
            owners, user_scope = item['owners'], item['scope'] == 'user'
            if name in ('alpha', 'beta'):
                run = subprocess.run(['/usr/local/lib/cal/worker', name, str(active)],
                                     env={**os.environ, 'CAL_VERSION': item['version']},
                                     capture_output=True, text=True, timeout=10)
                guard(run.returncode == 0, 'worker failed: ' + run.stderr)
        publish(active / 'version', item.get('version', 'shared'))
        if user_scope and owners:
            if len(owners) > 1:
                owner_uid, owner_gid = 0, grp.getgrnam('calusers').gr_gid
            else:
                account = pwd.getpwnam(owners[0])
                owner_uid, owner_gid = account.pw_uid, account.pw_gid
            os.chown(active, owner_uid, owner_gid)
            os.chmod(active, 0o770)
            for directory, subdirs, files in os.walk(active, followlinks=False):
                for entry in subdirs + files:
                    os.chown(Path(directory) / entry, owner_uid, owner_gid, follow_symlinks=False)
        else:
            os.chown(active, 0, 0)
            os.chmod(active, 0o755)
    with DB:
        number = DB.execute('INSERT INTO snapshots(body) VALUES (?)', ('{}',)).lastrowid
        document['generation'] = str(number)
        DB.execute('UPDATE snapshots SET body=? WHERE id=?', (json.dumps(document, sort_keys=True), number))
        DB.execute('INSERT OR REPLACE INTO head(singleton,snapshot) VALUES (1,?)', (number,))
    publish(STORE / 'generations' / (str(number) + '.json'), document)
    publish(STORE / 'current.json', document)
    trim_archive(document)
    return {'ok': True, 'generation': str(number), 'effective': document,
            'hook_stdout': hook.stdout, 'hook_stderr': hook.stderr}


def handle(uid, request):
    guard(type(request) is dict, 'request must be object')
    action = request.get('action', 'status')
    if action == 'apply':
        return materialize(compile_request(uid))
    if action in ('gc', 'rollback'):
        guard(uid == 0, 'only root controls saved generations')
        ids = request.get('generations', [])
        guard(type(ids) is list and all(type(x) is str and re.fullmatch('[0-9]+', x) for x in ids), 'invalid generation IDs')
        if action == 'rollback':
            guard(len(ids) == 1, 'rollback needs exactly one generation')
            row = DB.execute('SELECT body FROM snapshots WHERE id=?', (ids[0],)).fetchone()
            guard(row is not None, 'unknown generation')
            saved = json.loads(row[0])
            publish(CONSTITUTION, saved['root'])
            for user in ACCOUNTS:
                account = pwd.getpwnam(user)
                path = Path(account.pw_dir) / 'declaration.json'
                publish(path, saved.get('personal', {}).get(user, {'programs': {}}))
                os.chown(path, account.pw_uid, account.pw_gid, follow_symlinks=False)
            return materialize(compile_request(0))
        guard(latest().get('generation') not in ids, 'cannot discard current generation')
        with DB:
            DB.executemany('DELETE FROM snapshots WHERE id=?', [(number,) for number in ids])
        for number in ids:
            (STORE / 'generations' / (number + '.json')).unlink(missing_ok=True)
        trim_archive(latest())
    else:
        guard(action == 'status', 'unsupported action')
    return {'ok': True, 'current': latest(),
            'generations': [str(row[0]) for row in DB.execute('SELECT id FROM snapshots ORDER BY id')],
            'active': sorted(p.name for p in (STORE / 'active').iterdir()),
            'archive': sorted(p.name for p in (STORE / 'archive').iterdir())}


def main():
    global DB
    guard(os.geteuid() == 0, 'disposable guest root required')
    for area in ('active', 'archive', 'generations'):
        (STORE / area).mkdir(parents=True, exist_ok=True)
    DB = sqlite3.connect(STORE / 'x3-ledger.sqlite')
    DB.executescript('CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY AUTOINCREMENT,body TEXT NOT NULL); CREATE TABLE IF NOT EXISTS head(singleton INTEGER PRIMARY KEY CHECK(singleton=1),snapshot INTEGER NOT NULL);')
    os.chmod(STORE / 'x3-ledger.sqlite', 0o600)
    # Repair observational exports from the committed ledger after a daemon restart.
    for row in DB.execute('SELECT id,body FROM snapshots'):
        publish(STORE / 'generations' / (str(row[0]) + '.json'), json.loads(row[1]))
    if latest():
        publish(STORE / 'current.json', latest())
    endpoint = Path('/run/cal.sock')
    endpoint.unlink(missing_ok=True)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(endpoint))
        os.chmod(endpoint, 0o666)
        server.listen(16)
        while True:
            client, _ = server.accept()
            with client:
                client.settimeout(5)
                try:
                    credentials = client.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i'))
                    uid = struct.unpack('3i', credentials)[1]
                    buffer = bytearray()
                    while b'\n' not in buffer:
                        chunk = client.recv(4096)
                        guard(chunk, 'incomplete request')
                        buffer.extend(chunk)
                        guard(len(buffer) <= 65536, 'request exceeds bound')
                    reply = handle(uid, json.loads(buffer.split(b'\n', 1)[0]))
                except Exception as error:
                    reply = {'ok': False, 'error': str(error)}
                try:
                    client.sendall((json.dumps(reply, sort_keys=True) + '\n').encode())
                except (OSError, TimeoutError):
                    pass


if __name__ == '__main__':
    main()
