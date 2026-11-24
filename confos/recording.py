"""Record an invoked tool's explicit request; never infer lines from installed state."""
import fcntl
import hashlib
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
from archive_sources import sources

HERE = Path(__file__).resolve().parent
DECLARATION = Path('/state/declaration.conf')
NATIVE_APT = '/usr/bin/apt-get'
PACKAGE = re.compile(r'[a-z0-9](?:[a-z0-9+.-]*[a-z0-9])?(?::(?:amd64|all))?')
RELEASE = re.compile(r'[0-9][A-Za-z0-9.+:~_-]*')


def configure(root):
    """Every package file keeps its path and bytes; nothing is moved or relinked.

    The recording entries are files of the runtime package in /usr/lib/confos/commands,
    reached through its /usr/local/bin links, which precede /usr/bin and /usr/sbin in
    every session and sudo path. Up to 0.48 this function moved the package's own
    executables to /usr/lib/confos/native; an outside comparison then found the package
    files missing at the paths their lines require.
    """
    for name in ('apt', 'apt-get', 'pip', 'pip3', 'flatpak', 'podman', 'npm', 'hostnamectl', 'timedatectl',
                 'systemctl', 'sysctl', 'useradd', 'usermod', 'userdel', 'visudo'):
        for directory in ('usr/bin', 'usr/sbin'):
            entry = root/directory/name
            if entry.is_symlink() and os.readlink(entry).startswith('/usr/lib/confos/commands/'):
                raise ValueError('a package path is linked to a recording entry: /'+directory+'/'+name)
    if (root/'usr/lib/confos/native').exists():
        raise ValueError('relocated package executables are not part of this release')


def apt_request(arguments):
    args = [arg for arg in arguments if arg not in ('-y', '--yes', '--assume-yes', '-q', '-qq')]
    if len(args) < 2 or args[0] not in ('install', 'remove', 'purge'):
        raise ValueError('supported requests: install NAME[=VERSION]...; remove/purge NAME...')
    operation, *tokens = args
    requests = {}
    for token in tokens:
        name, separator, release = token.partition('=')
        if not PACKAGE.fullmatch(name) or (separator and (operation != 'install' or not RELEASE.fullmatch(release))):
            raise ValueError('unsupported package request or option: '+token)
        name = name.split(':')[0]
        if name in requests:
            raise ValueError('duplicate package request: '+name)
        requests[name] = release if separator else None
    return operation, requests


def resolve(roots, snapshot, directory):
    """Ask native APT for a plan using empty status and the declaration's archive."""
    for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
        (directory/sub).mkdir(parents=True, exist_ok=True)
    (directory/'status').write_text('')
    (directory/'etc/sources.list').write_text(sources(snapshot))
    options = ['-o', f'Dir::State::status={directory}/status',
        '-o', f'Dir::State::lists={directory}/lists', '-o', f'Dir::Cache::archives={directory}/archives',
        '-o', f'Dir::Etc::sourcelist={directory}/etc/sources.list',
        '-o', 'Dir::Etc::sourceparts=-', '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-',
        '-o', 'Dir::Etc::preferences=-', '-o', 'Dir::Etc::preferencesparts=-',
        '-o', 'APT::Install-Recommends=false', '-o', 'APT::Install-Suggests=false',
        '-o', 'APT::Sandbox::User=root', '-o', 'Acquire::Check-Valid-Until=false',
        '-o', 'Acquire::Retries=3', '-o', 'Acquire::http::Timeout=30',
        '-o', 'Acquire::Languages=none', '-o', f'Dir::Log={directory}/log',
        '-o', 'Dir::Cache::pkgcache=', '-o', 'Dir::Cache::srcpkgcache=']
    for operation in (['update'], ['--simulate', 'install', *[
            name+('='+release if release else '') for name, release in sorted(roots.items())]]):
        result = subprocess.run([NATIVE_APT, *options, *operation], text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode and operation[0] == '--simulate':
            result = subprocess.run([NATIVE_APT, *options, '--solver', '3.0',
                                     '--no-strict-pinning', *operation], text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode:
            raise ValueError('native APT resolution failed:\n'+result.stdout)
    resolved = dict(re.findall(r'^Inst (\S+?)(?::amd64)? \((\S+) ', result.stdout, re.M))
    if not resolved or not set(roots) <= resolved.keys():
        raise ValueError('APT did not resolve every named package to an exact release')
    if any(release and resolved[name] != release for name, release in roots.items()):
        raise ValueError('native dependency resolution changed an explicit package request')
    return resolved


def edit_packages(original, rows, snapshot, operation, requests, directory):
    components = dict(line.split('=', 1) for line in (HERE/'components'/(snapshot+'.txt')).read_text().split())
    roots = {name: release for name, release in components.items() if not name.startswith('confos-')}
    explicit = {row[1].split(':')[0]: row[2] for row in rows if row[0] == 'package'}
    if len(explicit) != sum(row[0] == 'package' for row in rows):
        raise ValueError('ambiguous package identities with architecture aliases')
    for name, release in explicit.items():
        if name in roots and roots[name] != release:
            raise ValueError('package release conflicts with base: '+name)
        roots[name] = release
    if operation == 'install':
        for name, release in requests.items():
            if name in components and release and release != components[name]:
                raise ValueError('request conflicts with the base component release: '+name)
            roots[name] = release or roots.get(name)
    else:
        for name in requests:
            if name in components:
                raise ValueError('cannot remove a base component with a package line: '+name)
            roots.pop(name, None)
    resolved = resolve(roots, snapshot, directory)
    if operation != 'install' and set(requests) & resolved.keys():
        raise ValueError('removal is still required by remaining package lines: '+', '.join(sorted(set(requests) & resolved.keys())))
    output = []
    pending = dict(requests)
    for line in original.decode().splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        name = row[1].split(':')[0] if len(row) > 1 and row[0] == 'package' else None
        if name not in requests:
            output.append(line)
        elif operation == 'install':
            output.append(line if row[2] == resolved[name] else shlex.join(['package', name, resolved[name]])+'\n')
        pending.pop(name, None)
    if operation == 'install':
        for name in sorted(pending):
            if output and not output[-1].endswith('\n'):
                output[-1] += '\n'
            output.append(shlex.join(['package', name, resolved[name]])+'\n')
    return ''.join(output).encode()


def commit(path, original, candidate):
    """Durable atomic text replacement. The immutable applied declaration is untouched."""
    if path.is_symlink() or path.read_bytes() != original:
        raise ValueError('declaration changed during request; retry')
    if candidate == original:
        # Earlier manual edits may not have been flushed yet.
        with path.open('rb') as stream:
            os.fsync(stream.fileno())
    else:
        metadata = path.stat()
        fd, temporary = tempfile.mkstemp(prefix='.record-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                os.fchmod(stream.fileno(), metadata.st_mode & 0o777)
                os.fchown(stream.fileno(), metadata.st_uid, metadata.st_gid)
                stream.write(candidate)
                stream.flush()
                os.fsync(stream.fileno())
            if path.read_bytes() != original:
                raise ValueError('declaration changed during request; retry')
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    print('RECORDED '+hashlib.sha256(candidate).hexdigest()+'; run confos apply', flush=True)


def apt(arguments):
    if os.geteuid() != 0:
        raise ValueError('permission denied: this account may not change /state/declaration.conf; use an authorized root invocation')
    operation, requests = apt_request(arguments)
    import assemble
    with open('/run/confos-apply.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if DECLARATION.is_symlink():
            raise ValueError('declaration must be a regular primary text file')
        original = DECLARATION.read_bytes()
        with tempfile.TemporaryDirectory(prefix='confos-record-', dir='/run') as temporary:
            directory = Path(temporary)
            captured = directory/'declaration.conf'
            captured.write_bytes(original)
            rows, snapshot = assemble.parse(captured)
            candidate = edit_packages(original, rows, snapshot, operation, requests, directory/'apt')
            captured.write_bytes(candidate)
            assemble.parse(captured)
            commit(DECLARATION, original, candidate)
