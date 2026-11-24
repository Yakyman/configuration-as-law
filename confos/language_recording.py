"""Record explicit language installer requests; no application or installed-state scan."""
import email.parser
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import zipfile
from contextlib import contextmanager

PIP = ['/usr/bin/python3', '-IB', '/usr/bin/pip3']
NPM = ['/usr/bin/node', '/usr/share/nodejs/npm/bin/npm-cli.js']
NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]*')
VERSION = re.compile(r'[0-9][A-Za-z0-9.!+_-]*(?:\.[A-Za-z0-9!+_-]+)*')

def normalize(name):
    return re.sub('[-_.]+', '-', name).lower()

def request(kind, arguments):
    args = list(arguments)
    if kind == 'pip':
        args = [arg for arg in args if arg != '--break-system-packages']
    if kind == 'pip' and args and args[0] == 'uninstall':
        args = [arg for arg in args if arg not in ('-y', '--yes')]
    if kind == 'npm':
        global_flags = [x for x in args if x in ('-g', '--global')]
        if len(global_flags) != 1:
            raise ValueError('npm recording requires exactly one -g or --global')
        args = [x for x in args if x not in ('-g', '--global')]
    if len(args) < 2 or args[0] not in ('install', 'uninstall'):
        raise ValueError('supported requests: install NAME[==VERSION] or WHEEL (npm NAME[@VERSION]); uninstall NAME')
    operation, *tokens = args
    if kind == 'npm' and len(tokens) != 1:
        raise ValueError('npm records one root package per request')
    result = []
    seen = set()
    for token in tokens:
        if kind == 'pip' and operation == 'install' and token.endswith('.whl') and not token.startswith('-'):
            path = Path(token).absolute()
            if not path.is_file():
                raise ValueError('wheel input must be an existing local regular file')
            result.append((None, str(path)))
            continue
        separator = '==' if kind == 'pip' else '@'
        name, sep, version = token.partition(separator)
        if not NAME.fullmatch(name) or (operation == 'install' and sep and not VERSION.fullmatch(version)) or (operation == 'uninstall' and sep):
            raise ValueError('unsupported request; use an exact release or bare removal name: '+token)
        name = normalize(name) if kind == 'pip' else name
        if kind == 'npm' and name != name.lower():
            raise ValueError('npm requires lowercase unscoped package names')
        if name in seen:
            raise ValueError('duplicate language package request: '+name)
        seen.add(name)
        result.append((name, version if sep else None))
    return operation, result

def native(argv, directory):
    env = {'PATH': '/usr/bin:/usr/sbin:/bin', 'HOME': str(directory), 'LC_ALL': 'C.UTF-8',
           'PYTHONDONTWRITEBYTECODE': '1', 'PIP_CONFIG_FILE': '/dev/null'}
    outcome = subprocess.run(argv, cwd=directory, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    if outcome.returncode:
        raise ValueError('native resolver failed:\n'+outcome.stdout)
    return outcome.stdout

def wheel_metadata(path):
    with zipfile.ZipFile(path) as wheel:
        records = [p for p in wheel.namelist() if p.endswith('.dist-info/METADATA')]
        if len(records) != 1:
            raise ValueError('wheel requires exactly one METADATA object')
        meta = email.parser.BytesParser().parsebytes(wheel.read(records[0]))
    name, version = normalize(meta.get('Name', '')), meta.get('Version', '')
    if not NAME.fullmatch(name) or not VERSION.fullmatch(version):
        raise ValueError('unsupported wheel identity')
    return name, version

def prepare_pip(requests, rows, directory, declaration=None):
    existing = {normalize(r[1]): r[2] for r in rows if r[0] == 'pip'}
    wanted = {}
    wheel_inputs = {}
    for name, value in requests:
        if name is None:
            identity, version = wheel_metadata(Path(value))
            if identity in wanted:
                raise ValueError('duplicate wheel identity')
            wanted[identity] = version
            wheel_inputs[identity] = value
        else:
            if name in wanted:
                raise ValueError('duplicate wheel/package identity')
            wanted[name] = value or existing.get(name)
    roots = existing | wanted
    # Reuse the exact already-declared wheels instead of resolving their release anew.
    if declaration is not None:
        for row in rows:
            if row[0] != 'pip' or (normalize(row[1]) in wanted and wanted[normalize(row[1])] != row[2]):
                continue
            source = Path(row[4])
            if source.is_absolute() or '..' in source.parts:
                raise ValueError('existing wheel input escapes declaration directory')
            path = declaration.parent/source
            if hashlib.sha256(path.read_bytes()).hexdigest() != row[3]:
                raise ValueError('existing wheel input checksum mismatch')
            if wheel_metadata(path) != (normalize(row[1]), row[2]):
                raise ValueError('existing wheel input identity mismatch')
            wheel_inputs.setdefault(normalize(row[1]), str(path))
    output = directory/'wheels'
    output.mkdir()
    native([*PIP, '--isolated', '--disable-pip-version-check', 'download',
            '--only-binary=:all:', '--no-cache-dir', '--index-url', 'https://pypi.org/simple',
            '--dest', str(output), *[wheel_inputs.get(name, name+('=='+version if version else '')) for name, version in sorted(roots.items())]], directory)
    prepared = {}
    for path in sorted(output.iterdir()):
        if path.suffix != '.whl':
            raise ValueError('native pip returned a non-wheel input')
        name, version = wheel_metadata(path)
        if name in prepared or (roots.get(name) is not None and roots[name] != version):
            raise ValueError('duplicate or conflicting resolved wheel')
        prepared[name] = (version, path.name, path.read_bytes())
    if not roots.keys() <= prepared.keys():
        raise ValueError('native pip omitted a requested package')
    return prepared

def prepare_npm(requests, directory):
    name, version = requests[0]
    manifest = {'name': 'confos-recorded-request', 'version': '1.0.0', 'private': True}
    (directory/'package.json').write_text(json.dumps(manifest, sort_keys=True)+'\n')
    (directory/'empty-npmrc').write_text('')
    native([*NPM, 'install', '--package-lock-only', '--save-exact', '--ignore-scripts', '--no-audit', '--no-fund',
            '--logs-max=0', '--cache', str(directory/'cache'), '--userconfig', str(directory/'empty-npmrc'),
            '--globalconfig', '/dev/null', '--registry', 'https://registry.npmjs.org/',
            name+('@'+version if version else '')], directory)
    data = (directory/'package-lock.json').read_bytes()
    lock = json.loads(data)
    resolved = lock.get('packages', {}).get('node_modules/'+name, {}).get('version', '')
    if not VERSION.fullmatch(resolved) or (version is not None and resolved != version):
        raise ValueError('npm did not resolve the requested exact release')
    version = resolved
    validate_npm(data, name, version)
    if (directory/'node_modules').exists():
        raise ValueError('native lock-only npm unexpectedly installed packages')
    return {name: (version, 'package-lock.json', data)}

def validate_npm(data, name, version):
    lock = json.loads(data)
    packages = lock.get('packages', {})
    if lock.get('lockfileVersion') not in (2, 3) or packages.get('', {}).get('dependencies') != {name: version}:
        raise ValueError('native npm lock has unexpected root')
    if packages.get('node_modules/'+name, {}).get('version') != version:
        raise ValueError('npm resolved a different root release')
    for path, package in packages.items():
        if path and (not path.startswith('node_modules/') or '..' in Path(path).parts or
                     not package.get('resolved', '').startswith('https://') or
                     not package.get('integrity', '').startswith(('sha256-', 'sha512-'))):
            raise ValueError('npm lock includes unsupported source or lacks integrity')

def input_name(filename, data):
    return 'recorded-inputs/'+hashlib.sha256(data).hexdigest()+'/'+filename

def edit(original, kind, removals, prepared):
    output = []
    pending = dict(prepared)
    canonical = normalize if kind == 'pip' else lambda s: s
    for line in original.decode().splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        name = canonical(row[1]) if len(row) > 1 and row[0] == kind else None
        if name in removals:
            continue
        if name in prepared:
            version, filename, data = pending.pop(name)
            replacement = [kind, name, version, hashlib.sha256(data).hexdigest(), input_name(filename, data)]
            output.append(line if row == replacement else shlex.join(replacement)+'\n')
        else:
            output.append(line)
    for name, (version, filename, data) in sorted(pending.items()):
        if output and not output[-1].endswith('\n'):
            output[-1] += '\n'
        output.append(shlex.join([kind, name, version, hashlib.sha256(data).hexdigest(), input_name(filename, data)])+'\n')
    return ''.join(output).encode()

def persist_inputs(parent, prepared, created=None):
    # Inputs become durable before text can refer to them; never replace existing bytes.
    created = [] if created is None else created
    for _, filename, data in prepared.values():
        target = parent/input_name(filename, data)
        for folder in (target.parent.parent, target.parent):
            if folder.is_symlink():
                raise ValueError('recorded input directories cannot be symlinks')
            if not folder.exists():
                folder.mkdir(mode=0o755)
                created.append((folder, folder.stat().st_ino, True))
        if target.exists() or target.is_symlink():
            if target.is_symlink() or target.read_bytes() != data:
                raise ValueError('content-addressed input collision')
        else:
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
            created.append((target, os.fstat(fd).st_ino, False))
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        with target.open('rb') as stream:
            os.fsync(stream.fileno())
        for folder in (target.parent, target.parent.parent, parent):
            fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)

@contextmanager
def input_transaction(declaration, candidate, prepared):
    created = []
    try:
        persist_inputs(declaration.parent, prepared, created)
        yield
    except BaseException:
        # A commit may have replaced text before its final fsync/report failed.
        # Never remove input that the current declaration actually references.
        try:
            committed = declaration.read_bytes() == candidate
        except OSError:
            committed = True  # Cannot prove rollback is safe.
        if not committed:
            for path, inode, is_dir in reversed(created):
                try:
                    if path.lstat().st_ino != inode or path.is_symlink():
                        continue
                    if is_dir:
                        path.rmdir()
                    else:
                        path.unlink()
                    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
                    try:
                        os.fsync(fd)
                    finally:
                        os.close(fd)
                except FileNotFoundError:
                    pass
                except OSError as error:
                    if not (is_dir and error.errno == errno.ENOTEMPTY):
                        raise
        raise

def validate_existing(rows, declaration, directory):
    wheels = []
    identities = set()
    for row in rows:
        if row[0] not in ('pip', 'npm'):
            continue
        kind, name, version, digest, source_text = row
        identity = (kind, normalize(name) if kind == 'pip' else name)
        if identity in identities:
            raise ValueError('duplicate normalized language identity')
        identities.add(identity)
        source = Path(source_text)
        if source.is_absolute() or '..' in source.parts:
            raise ValueError('existing language input escapes declaration directory')
        path = declaration.parent/source
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('existing language input checksum mismatch')
        if kind == 'pip':
            if wheel_metadata(path) != (normalize(name), version):
                raise ValueError('existing wheel input identity mismatch')
            wheels.append(str(path))
        else:
            validate_npm(data, name, version)
    if wheels:
        output = directory/'validate-wheels'
        output.mkdir()
        native([*PIP, '--isolated', '--disable-pip-version-check', 'download', '--no-index',
                '--only-binary=:all:', '--no-cache-dir', '--dest', str(output), *wheels], directory)

def already_recorded(kind, requests, rows, declaration):
    existing = {(normalize(row[1]) if kind == 'pip' else row[1]): row
                for row in rows if row[0] == kind}
    for name, version in requests:
        wheel = None
        if name is None:
            wheel = Path(version)
            name, version = wheel_metadata(wheel)
        row = existing.get(name)
        if row is None or (version is not None and row[2] != version):
            return False
        source = Path(row[4])
        if source.is_absolute() or '..' in source.parts:
            raise ValueError('recorded language input escapes declaration directory')
        data = (declaration.parent/source).read_bytes()
        if hashlib.sha256(data).hexdigest() != row[3]:
            raise ValueError('recorded language input checksum mismatch')
        if wheel is not None and wheel.read_bytes() != data:
            return False
        with (declaration.parent/source).open('rb') as stream:
            os.fsync(stream.fileno())
        folder = (declaration.parent/source).parent
        while True:
            fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
            if folder == declaration.parent:
                break
            folder = folder.parent
    return True

def record(kind, arguments):
    import recording
    if kind not in ('pip', 'npm'):
        raise ValueError('unsupported language installer')
    if os.geteuid() != 0:
        raise ValueError('permission denied: this account may not change /state/declaration.conf; use an authorized root invocation')
    operation, requests = request(kind, arguments)
    import assemble
    with open('/run/confos-apply.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        declaration = recording.DECLARATION
        if declaration.is_symlink():
            raise ValueError('declaration must be a regular primary text file')
        original = declaration.read_bytes()
        with tempfile.TemporaryDirectory(prefix='confos-language-record-', dir='/run') as temporary:
            directory = Path(temporary)
            capture = directory/'declaration.conf'
            capture.write_bytes(original)
            rows, _ = assemble.parse(capture)
            validate_existing(rows, declaration, directory)
            if operation == 'install' and already_recorded(kind, requests, rows, declaration):
                # Keep the original exact dependency resolution on repeated requests.
                recording.commit(declaration, original, original)
                return
            removals = {name for name, _ in requests} if operation == 'uninstall' else set()
            if removals and kind == 'pip':
                # Resolve remaining roots to reject removal of a still-required wheel.
                remaining = [row for row in rows if not (row[0] == 'pip' and normalize(row[1]) in removals)]
                if any(row[0] == 'pip' for row in remaining):
                    required = prepare_pip([], remaining, directory, declaration)
                    if removals & required.keys():
                        raise ValueError('removed wheel is required by remaining pip lines')
            prepared = {} if removals else (prepare_pip(requests, rows, directory, declaration) if kind == 'pip' else prepare_npm(requests, directory))
            for row in rows:
                if row[0] != kind:
                    continue
                name = normalize(row[1]) if kind == 'pip' else row[1]
                if name in prepared:
                    version, filename, data = prepared[name]
                    if version == row[2] and hashlib.sha256(data).hexdigest() == row[3]:
                        del prepared[name]  # Preserve a person's existing equivalent line.
            candidate = edit(original, kind, removals, prepared)
            capture.write_bytes(candidate)
            assemble.parse(capture)
            with input_transaction(declaration, candidate, prepared):
                recording.commit(declaration, original, candidate)
