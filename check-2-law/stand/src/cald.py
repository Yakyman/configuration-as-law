#!/usr/bin/python3
"""Disposable VM-only declaration controller; deliberately not a production daemon."""
import json, os, pathlib, pwd, grp, re, shutil, socket, struct, subprocess, time, tempfile

BASE = pathlib.Path('/var/lib/cal')
ROOT = pathlib.Path('/etc/cal/root.json')
SOCKET = '/run/cal.sock'
CATALOG = {'alpha', 'beta', 'hello', 'figlet', 'python', 'node', 'browser'}
USERS = ('alice', 'bob')
CHANNELS = {'package', 'pip', 'npm', 'flatpak', 'appimage', 'download', 'build', 'systemd', 'cron', 'interpreter'}

def require(ok, message):
    if not ok: raise ValueError(message)

def read(path, default=None):
    try:
        with open(path) as f: return json.load(f)
    except FileNotFoundError:
        if default is not None: return default
        raise

def atomic(path, value):
    fd, name = tempfile.mkstemp(prefix='.cal-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            os.fchmod(f.fileno(), 0o644)
            json.dump(value, f, sort_keys=True, indent=2)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

def mapping(value, label):
    require(isinstance(value, dict), label + ' must be an object')
    return value

def names(value, allowed, label):
    require(isinstance(value, list) and all(isinstance(x, str) and x in allowed for x in value), 'invalid ' + label)
    return value

def personal(username):
    # O_NOFOLLOW and bounded read prevent symlinks / unlimited input. Home's parent
    # components are trusted VM account setup; this is not a general secure resolver.
    account = pwd.getpwnam(username)
    path = pathlib.Path(account.pw_dir) / 'declaration.json'
    try: fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError: return {'programs': {}}
    try:
        import stat
        st = os.fstat(fd)
        require(stat.S_ISREG(st.st_mode) and st.st_uid in (0, account.pw_uid), 'personal declaration owner/type invalid')
        require(st.st_size <= 65536, 'personal declaration too large')
        with os.fdopen(fd, 'r') as f:
            fd = -1
            doc = json.loads(f.read(65537))
    finally:
        if fd >= 0: os.close(fd)
    mapping(doc, username)
    require(set(doc) <= {'programs'}, 'personal declaration cannot override root fields')
    return doc

def effective(uid):
    root = mapping(read(ROOT), 'root')
    require(set(root) <= {'archive', 'programs', 'policies', 'allow_channels', 'shared', 'system_update'}, 'unknown root key')
    require('system_update' not in root or isinstance(root['system_update'], str), 'system_update must be a request string')
    require(root.get('archive') in ('keep', 'delete'), 'explicit archive setting required (O6)')
    programs = {}
    for ident, item in mapping(root.get('programs', {}), 'programs').items():
        require(ident in CATALOG, 'unknown catalog program: ' + ident)
        mapping(item, ident)
        require(set(item) <= {'version', 'scope', 'owners'}, 'unknown program field')
        require(isinstance(item.get('version', '1'), str) and re.fullmatch(r'[A-Za-z0-9._-]{1,40}', item.get('version', '1')), 'invalid version')
        require(item.get('scope', 'system') in ('system', 'user'), 'invalid scope')
        owners = names(item.get('owners', []), USERS, 'owners')
        programs[ident] = dict(version=item.get('version', '1'), scope=item.get('scope', 'system'), owners=sorted(set(owners)))
    policies = mapping(root.get('policies', {}), 'policies')
    require(set(policies) <= set(USERS), 'unknown policy user')
    for user, policy in policies.items():
        mapping(policy, 'policy')
        require(set(policy) <= {'allowlist', 'denylist'}, 'unknown policy key')
        for key, values in policy.items(): names(values, CATALOG, key)
    allow = mapping(root.get('allow_channels', {}), 'allow_channels')
    require(set(allow) <= set(USERS), 'unknown allow_channels user')
    for user, channels in allow.items(): names(channels, CHANNELS, 'channels')
    # Non-root apply updates only its own declaration. Others retain their last
    # applied personal document, so editing a file alone has no live effect.
    old = read(BASE / 'current.json', {})
    docs = dict(old.get('personal', {}))
    if uid == 0:
        docs = {user: personal(user) for user in USERS}
    else:
        user = pwd.getpwuid(uid).pw_name
        require(user in USERS, 'account not enrolled')
        docs[user] = personal(user)
        require(root == old.get('root'), 'root declaration changed: root must apply first')
    for user, doc in docs.items():
        require(set(doc) <= {'programs'}, 'personal declaration cannot override root fields')
        for ident, item in mapping(doc.get('programs', {}), 'personal programs').items():
            require(ident in CATALOG, 'unknown catalog program: ' + ident)
            mapping(item, ident)
            require(set(item) <= {'version'}, 'personal scope/owners/other fields forbidden')
            version = item.get('version', '1')
            require(isinstance(version, str) and re.fullmatch(r'[A-Za-z0-9._-]{1,40}', version), 'invalid version')
            policy = policies.get(user, {})
            require(ident not in policy.get('denylist', []), 'root denylist forbids ' + ident)
            require('allowlist' not in policy or ident in policy['allowlist'], 'root allowlist forbids ' + ident)
            if ident in programs:
                require(programs[ident]['version'] == version, 'version conflicts with root/another owner')
                programs[ident]['owners'] = sorted(set(programs[ident]['owners'] + [user]))
            else: programs[ident] = dict(version=version, scope='user', owners=[user])
    shared = mapping(root.get('shared', {}), 'shared')
    for ident, owners in shared.items():
        require(isinstance(ident, str) and re.fullmatch(r'[a-z][a-z0-9-]{0,39}', ident), 'invalid shared ID')
        names(owners, CATALOG, 'shared owners')
    return dict(root=root, personal=docs, archive=root['archive'], programs=programs, shared=shared, allow_channels=allow)

def statekeys(doc):
    programs = set(doc.get('programs', {}))
    return programs | {'shared-' + key for key, owners in doc.get('shared', {}).items() if programs.intersection(owners)}

def sweep(doc):
    referenced = statekeys(doc)
    for path in (BASE / 'generations').glob('*.json'): referenced |= statekeys(read(path))
    if doc.get('archive') == 'delete':
        for path in (BASE / 'archive').iterdir():
            if path.name not in referenced: shutil.rmtree(path)

def apply(uid):
    doc = effective(uid) # validation precedes any mutation
    desired = statekeys(doc)
    pending = BASE / 'pending.json'
    atomic(pending, doc)
    hook = subprocess.run(['/usr/local/lib/cal/apply-policy', str(pending)], capture_output=True, text=True, timeout=120)
    require(hook.returncode == 0, 'policy hook failed (partial external mutation possible): ' + hook.stdout + hook.stderr)
    for path in (BASE / 'active').iterdir():
        if path.name not in desired:
            destination = BASE / 'archive' / path.name
            require(not destination.exists(), 'active/archive collision')
            path.rename(destination)
    for ident in desired:
        path = BASE / 'active' / ident
        archived = BASE / 'archive' / ident
        if not path.exists():
            if archived.exists(): archived.rename(path)
            else: path.mkdir(mode=0o755)
        if ident.startswith('shared-'):
            if not (path / 'cache').exists():
                with open(path / 'cache', 'x') as f: f.write('shared derivative\n')
        elif ident in ('alpha', 'beta'):
            env = dict(os.environ, CAL_VERSION=doc['programs'][ident]['version'])
            worker = subprocess.run(['/usr/local/lib/cal/worker', ident, str(path)], env=env, capture_output=True, text=True, timeout=10)
            require(worker.returncode == 0, 'worker failed: ' + worker.stderr)
        # Atomic replace avoids following a user-controlled metadata symlink.
        atomic(path / 'version', doc['programs'].get(ident, {}).get('version', 'shared'))
        item = doc['programs'].get(ident, {})
        owners = item.get('owners', [])
        if ident.startswith('shared-'):
            owners = sorted({user for owner in doc['shared'][ident[7:]] for user in doc['programs'].get(owner, {}).get('owners', [])})
        if (item.get('scope') == 'user' or ident.startswith('shared-')) and owners:
            if len(owners) == 1:
                account = pwd.getpwnam(owners[0]); owner_uid, owner_gid = account.pw_uid, account.pw_gid
            else:
                owner_uid, owner_gid = 0, grp.getgrnam('calusers').gr_gid
            os.chown(path, owner_uid, owner_gid); os.chmod(path, 0o770)
            # lchown only: derivatives may contain symlinks to unrelated files.
            for directory, subdirs, files in os.walk(path, followlinks=False):
                for name in subdirs + files:
                    os.chown(os.path.join(directory, name), owner_uid, owner_gid, follow_symlinks=False)
        else:
            os.chown(path, 0, 0); os.chmod(path, 0o755)
    generation = str(time.time_ns())
    doc['generation'] = generation
    atomic(BASE / 'generations' / (generation + '.json'), doc)
    atomic(BASE / 'current.json', doc)
    sweep(doc)
    return dict(ok=True, generation=generation, effective=doc, hook_stdout=hook.stdout, hook_stderr=hook.stderr)

def dispatch(uid, req):
    require(isinstance(req, dict), 'request must be object')
    action = req.get('action', 'status')
    if action == 'apply': return apply(uid)
    if action == 'rollback':
        require(uid == 0, 'only root may roll back generations')
        ids = req.get('generations', [])
        require(isinstance(ids, list) and len(ids) == 1 and isinstance(ids[0], str) and re.fullmatch(r'[0-9]+', ids[0]), 'rollback requires one generation ID')
        saved = read(BASE / 'generations' / (ids[0] + '.json'))
        atomic(ROOT, saved['root'])
        for user in USERS:
            path = pathlib.Path(pwd.getpwnam(user).pw_dir) / 'declaration.json'
            atomic(path, saved.get('personal', {}).get(user, {'programs': {}}))
            account = pwd.getpwnam(user)
            os.chown(path, account.pw_uid, account.pw_gid, follow_symlinks=False)
        return apply(0)
    if action == 'gc':
        require(uid == 0, 'only root may delete generations')
        generations = req.get('generations', [])
        require(isinstance(generations, list) and all(isinstance(x, str) and re.fullmatch(r'[0-9]+', x) for x in generations), 'invalid generation IDs')
        current = read(BASE / 'current.json', {})
        require(current.get('generation') not in generations, 'cannot delete current generation')
        for ident in generations: (BASE / 'generations' / (ident + '.json')).unlink(missing_ok=True)
        sweep(current)
    else: require(action == 'status', 'unknown action')
    return dict(ok=True, current=read(BASE / 'current.json', {}), generations=sorted(p.stem for p in (BASE / 'generations').glob('*.json')), active=sorted(p.name for p in (BASE / 'active').iterdir()), archive=sorted(p.name for p in (BASE / 'archive').iterdir()))

def main():
    require(os.geteuid() == 0, 'daemon requires root')
    BASE.mkdir(mode=0o755, parents=True, exist_ok=True)
    for name in ('active', 'archive', 'generations'): (BASE / name).mkdir(mode=0o755, exist_ok=True)
    try: os.unlink(SOCKET)
    except FileNotFoundError: pass
    server = socket.socket(socket.AF_UNIX)
    server.bind(SOCKET)
    os.chmod(SOCKET, 0o666)
    server.listen(16)
    while True:
        conn, _ = server.accept()
        with conn:
            conn.settimeout(5)
            try:
                _, uid, _ = struct.unpack('3i', conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')))
                data = b''
                while b'\n' not in data:
                    chunk = conn.recv(4096)
                    require(bool(chunk), 'request ended without newline')
                    data += chunk
                    require(len(data) <= 65536, 'request too large')
                result = dispatch(uid, json.loads(data.split(b'\n', 1)[0]))
            except Exception as exc: result = dict(ok=False, error=str(exc))
            try: conn.sendall((json.dumps(result, sort_keys=True) + '\n').encode())
            except (BrokenPipeError, TimeoutError): pass

if __name__ == '__main__': main()
