"""Flatpak bundle request recording; native import only into isolated scratch."""
import configparser
import ctypes as C
import fcntl
import hashlib
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import language_recording

NATIVE = '/usr/bin/flatpak'
REF = re.compile(r'(?:app|runtime)/[A-Za-z0-9_.-]+/x86_64/[A-Za-z0-9_.-]+')
ID = re.compile(r'[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+')

class Repository:
    def __init__(self, path, create=False):
        self.lib = C.CDLL('libostree-1.so.1')
        self.gio = C.CDLL('libgio-2.0.so.0')
        self.obj = C.CDLL('libgobject-2.0.so.0')
        self.glib = C.CDLL('libglib-2.0.so.0')
        self.gio.g_file_new_for_path.argtypes = [C.c_char_p]
        self.gio.g_file_new_for_path.restype = C.c_void_p
        self.lib.ostree_repo_new.argtypes = [C.c_void_p]
        self.lib.ostree_repo_new.restype = C.c_void_p
        self.obj.g_object_unref.argtypes = [C.c_void_p]
        self.glib.g_free.argtypes = [C.c_void_p]
        self.lib.ostree_repo_create.argtypes = [C.c_void_p, C.c_int, C.c_void_p, C.c_void_p]
        self.lib.ostree_repo_open.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p]
        self.lib.ostree_repo_resolve_rev.argtypes = [C.c_void_p, C.c_char_p, C.c_int, C.POINTER(C.c_void_p), C.c_void_p]
        file = self.gio.g_file_new_for_path(os.fsencode(path))
        self.repo = self.lib.ostree_repo_new(file)
        self.obj.g_object_unref(file)
        # Public OSTreeRepoMode ARCHIVE=1; no private store-layout fabrication.
        valid = (self.lib.ostree_repo_create(self.repo, 1, None, None) if create else
                 self.lib.ostree_repo_open(self.repo, None, None))
        if not valid:
            self.close()
            raise ValueError('native OSTree repository create/open failed')

    def resolve(self, ref):
        output = C.c_void_p()
        if not self.lib.ostree_repo_resolve_rev(self.repo, ref.encode(), 0, C.byref(output), None):
            raise ValueError('native OSTree could not resolve imported ref')
        try:
            value = C.string_at(output).decode()
        finally:
            self.glib.g_free(output)
        if not re.fullmatch('[0-9a-f]{64}', value):
            raise ValueError('native OSTree returned invalid commit')
        return value

    def close(self):
        if self.repo:
            self.obj.g_object_unref(self.repo)
            self.repo = None

def native(arguments, directory):
    env = {'PATH': '/usr/bin:/usr/sbin', 'HOME': str(directory), 'LC_ALL': 'C', 'TMPDIR': str(directory),
           'XDG_CACHE_HOME': str(directory/'cache'), 'XDG_CONFIG_HOME': str(directory/'config'),
           'XDG_DATA_HOME': str(directory/'data'), 'FLATPAK_USER_DIR': str(directory/'user'),
           'FLATPAK_SYSTEM_DIR': str(directory/'system')}
    result = subprocess.run([NATIVE, *arguments], cwd=directory, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    if result.returncode:
        raise ValueError('native Flatpak metadata operation failed:\n'+result.stderr)
    return result.stdout

def request(arguments):
    args = [a for a in arguments if a not in ('-y', '--assumeyes', '--system')]
    if not args:
        raise ValueError('Flatpak request is missing')
    operation, *tail = args
    if operation == 'install':
        if tail.count('--bundle') != 1:
            raise ValueError('only install --bundle LOCALFILE is representable; named remotes are unsupported')
        tail.remove('--bundle')
        if len(tail) != 1 or tail[0].startswith('-'):
            raise ValueError('only one bundle file and -y/--system are supported')
        path = Path(tail[0]).absolute()
        if not path.is_file():
            raise ValueError('bundle must be an existing local file')
        return operation, path
    if operation == 'uninstall':
        if len(tail) != 1 or not (REF.fullmatch(tail[0]) or ID.fullmatch(tail[0])):
            raise ValueError('uninstall requires one complete REF or declared ID')
        return operation, tail[0]
    raise ValueError('request has no current declaration form; remote-add and other mutations are refused')

def inspect_bundle(path, directory):
    directory.mkdir(exist_ok=True)
    repository = directory/'repo'
    repo = Repository(repository, create=True)
    repo.close()
    native(['build-import-bundle', str(repository), str(path)], directory)
    branches = native(['repo', '--branches', str(repository)], directory)
    refs = [token for token in branches.split() if REF.fullmatch(token)]
    if len(refs) != 1:
        raise ValueError('bundle must import exactly one supported x86_64 application/runtime ref')
    ref = refs[0]
    repo = Repository(repository)
    try:
        commit = repo.resolve(ref)
    finally:
        repo.close()
    text = native(['repo', '--metadata='+ref, str(repository)], directory)
    config = configparser.RawConfigParser()
    config.read_string(text)
    section = 'Application' if ref.startswith('app/') else 'Runtime'
    if config.get(section, 'name', fallback='') != ref.split('/')[1]:
        raise ValueError('bundle metadata identity differs from imported ref')
    dependency = None
    if section == 'Application':
        dependency = 'runtime/'+config.get(section, 'runtime', fallback='')
        if not REF.fullmatch(dependency):
            raise ValueError('application must name a supported exact runtime ref')
    return ref, commit, dependency

def dependency_check(rows, inspection):
    refs = {r[1] for r in rows if r[0] == 'flatpak'}
    for ref, _, dependency in inspection:
        if dependency is not None and dependency not in refs:
            raise ValueError('declare required runtime first: '+dependency)

def existing_input(declaration, row):
    source = Path(row[4])
    if source.is_absolute() or '..' in source.parts:
        raise ValueError('existing bundle input escapes declaration directory')
    path = declaration.parent/source
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != row[3]:
        raise ValueError('existing bundle checksum mismatch')
    with path.open('rb') as stream:
        os.fsync(stream.fileno())
    folder = path.parent
    while True:
        fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        if folder == declaration.parent:
            break
        folder = folder.parent
    return data

def edit(original, replacement=None, remove=None):
    output = []
    found = False
    target = (replacement[1].split('/')[1] if replacement else remove.split('/')[1] if '/' in remove else remove)
    for line in original.decode().splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        if len(row) > 1 and row[0] == 'flatpak' and row[1].split('/')[1] == target:
            if remove is not None and '/' in remove and row[1] != remove:
                raise ValueError('requested full ref differs from the recorded branch')
            found = True
            if replacement:
                output.append(line if row == replacement else shlex.join(replacement)+'\n')
        else:
            output.append(line)
    if replacement and not found:
        if output and not output[-1].endswith('\n'):
            output[-1] += '\n'
        output.append(shlex.join(replacement)+'\n')
    return ''.join(output).encode()

def record(arguments):
    import assemble
    import recording
    if os.geteuid() != 0:
        raise ValueError('permission denied: this account may not change /state/declaration.conf; use an authorized root invocation')
    operation, value = request(arguments)
    declaration = recording.DECLARATION
    with open('/run/confos-apply.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if declaration.is_symlink():
            raise ValueError('declaration must be a regular primary text file')
        original = declaration.read_bytes()
        with tempfile.TemporaryDirectory(prefix='confos-flatpak-record-', dir='/run') as temporary:
            directory = Path(temporary)
            captured = directory/'declaration.conf'
            captured.write_bytes(original)
            rows, _ = assemble.parse(captured)
            prepared = {}
            if operation == 'install':
                # Freeze bytes before native import; inspect exactly what will be recorded.
                data = value.read_bytes()
                source = directory/'input.flatpak'
                source.write_bytes(data)
                ref, commit, dependency = inspect_bundle(source, directory/'requested')
                filename = value.name
                replacement = ['flatpak', ref, commit, hashlib.sha256(data).hexdigest(), language_recording.input_name(filename, data)]
                # Preserve equivalent person-written source paths and comments.
                existing = next((r for r in rows if r[:4] == replacement[:4]), None)
                if existing:
                    if existing_input(declaration, existing) != data:
                        raise ValueError('existing bundle input changed or escapes declaration directory')
                    replacement = existing
                else:
                    prepared[ref] = (commit, filename, data)
                candidate = edit(original, replacement=replacement)
            else:
                candidate = edit(original, remove=value)
            captured.write_bytes(candidate)
            candidate_rows, _ = assemble.parse(captured)
            inspections = []
            for index, row in enumerate(r for r in candidate_rows if r[0] == 'flatpak'):
                if operation == 'install' and row[1] == ref:
                    inspections.append((ref, commit, dependency))
                    continue
                data = existing_input(declaration, row)
                frozen = directory/f'existing-{index}.flatpak'
                frozen.write_bytes(data)
                inspected = inspect_bundle(frozen, directory/f'existing-{index}')
                if inspected[:2] != tuple(row[1:3]):
                    raise ValueError('existing bundle ref/commit mismatch')
                inspections.append(inspected)
            dependency_check(candidate_rows, inspections)
            with language_recording.input_transaction(declaration, candidate, prepared):
                recording.commit(declaration, original, candidate)
