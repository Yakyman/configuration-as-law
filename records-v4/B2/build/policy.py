"""Guest policy support. Database agreement is not daemon-cache acknowledgement."""
import hashlib
import base64
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import time

POLICY = Path('/etc/fapolicyd')
RULES = '''# Stand owns this entire ruleset; first match wins.
allow perm=execute all : trust=1
deny_audit perm=execute all : all
deny_audit perm=open all : ftype=application/x-executable trust=0
deny_audit perm=open all : ftype=application/x-pie-executable trust=0
deny_audit perm=open all : ftype=application/x-sharedlib trust=0
deny_audit perm=open all : ftype=text/x-shellscript trust=0
deny_audit perm=open all : ftype=text/x-python trust=0
deny_audit perm=open all : ftype=text/x-script.python trust=0
deny_audit perm=open all : ftype=application/x-bytecode.python trust=0
allow perm=open all : all
'''

def _run(*args, timeout=60):
    if args[0]=='systemctl':args=('/usr/bin/systemctl',)+args[1:]
    return subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                          timeout=timeout).stdout

def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.stand-tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(text)
        stream.flush()
        os.fchmod(stream.fileno(), 0o644)
        os.fsync(stream.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def install_policy():
    """Install static configuration, without starting or reloading the daemon.

    Offline bootstrap order: install_policy, stage_trust, start daemon,
    refresh_trust. Caller records config and this module in its base manifest.
    """
    config_path = POLICY / 'fapolicyd.conf'
    config = config_path.read_text()
    desired = {'permissive':'0', 'trust':'file', 'integrity':'sha256', 'db_max_size':'128', 'allow_filesystem_mark':'1',
               'watch_fs':'ext2,ext3,ext4,tmpfs,overlay,xfs,btrfs'}
    output = []
    for line in config.splitlines():
        key = line.split('=', 1)[0].strip()
        if key not in desired and key != 'ignore_mounts':
            output.append(line)
    output.extend(key + ' = ' + value for key, value in desired.items())
    _write(config_path, '\n'.join(output) + '\n')
    rules_dir = POLICY / 'rules.d'
    rules_dir.mkdir(exist_ok=True)
    for path in rules_dir.glob('*.rules'):
        path.unlink()
    # A legacy file can shadow the compiled rules, so remove it explicitly.
    (POLICY / 'fapolicyd.rules').unlink(missing_ok=True)
    for path in (POLICY / 'trust.d').glob('*'):
        if path.is_file() or path.is_symlink():
            path.unlink()
    _write(rules_dir / '90-stand.rules', RULES)
    _write(POLICY / 'compiled.rules', RULES)
    _run('fapolicyd-cli', '--check-config')
    return {'installed':True, 'active_policy_acknowledged':False}

def _files(rows, declaration_dir):
    directory = Path(declaration_dir).resolve()
    for row in rows:
        if row.get('type', row.get('kind')) not in ('base','program','code'):
            continue
        if 'files' in row and 'files_manifest' in row:
            raise ValueError('use either files or files_manifest')
        if 'files_manifest' in row:
            path = (directory / row['files_manifest']).resolve()
            if not path.is_relative_to(directory):
                raise ValueError('manifest must remain in declaration directory')
            files = json.loads(path.read_text())
        else:
            files = row.get('files', [])
        if not isinstance(files, list):
            raise ValueError('file manifest must be a JSON list')
        yield from files

def stage_trust(rows, declaration_dir):
    """Validate and persist trust records; does not claim active enforcement."""
    records = {}
    for entry in _files(rows, declaration_dir):
        if entry.get('kind') == 'symlink':
            continue
        if entry.get('kind', 'file') != 'file':
            raise ValueError('unexpected manifest file kind')
        path = entry['path']
        if not path.startswith('/') or re.search(r'\s|%', path) or len(os.fsencode(path)) > 500:
            raise ValueError('prototype trust path must be absolute, short and contain no whitespace or percent')
        if 'content_b64' in entry:
            # The broker validates bytes before atomic publication. The existing
            # deny-open policy intentionally prevents reading an unadmitted ELF.
            # Trust the exact declared payload, then verify the installed file
            # after database convergence. This is not an atomic execute barrier.
            content = base64.b64decode(entry['content_b64'], validate=True)
            digest = hashlib.sha256(content).hexdigest()
            st = os.lstat(path)
            if not stat.S_ISREG(st.st_mode) or st.st_uid != entry['uid'] or st.st_gid != entry['gid'] or stat.S_IMODE(st.st_mode) != entry['mode']:
                raise ValueError('published file metadata differs: ' + path)
            if digest != entry['sha256'] or st.st_size != len(content):
                raise ValueError('declared payload differs: ' + path)
            records[path] = (len(content), digest)
            continue
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError('trust requires a regular file: ' + path)
            wanted_mode = int(entry['mode'], 8) if isinstance(entry['mode'], str) else entry['mode']
            if (stat.S_IMODE(before.st_mode), before.st_uid, before.st_gid) != (wanted_mode, entry['uid'], entry['gid']):
                raise ValueError('file permission or ownership mismatch: ' + path)
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            after = os.fstat(stream.fileno())
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise ValueError('file changed while hashing: ' + path)
        if digest != entry['sha256']:
            raise ValueError('file hash mismatch: ' + path)
        value = (before.st_size, digest)
        if path in records and records[path] != value:
            raise ValueError('conflicting trust records: ' + path)
        records[path] = value
    if not records:
        raise ValueError('refusing empty executable trust set')
    _write(POLICY / 'fapolicyd.trust', '# AUTOGENERATED FILE VERSION 2\n' + ''.join(
        path + ' ' + str(size) + ' ' + digest + '\n'
        for path, (size, digest) in sorted(records.items())))
    return records

def _dump_records(text):
    records = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 4 or not fields[1].startswith('/'):
            raise ValueError('unrecognized trust database output')
        source, path, size, digest = fields
        if source not in ('file','filedb'):
            raise ValueError('unexpected trust source: ' + source)
        if path in records:
            raise ValueError('duplicate trust database path: ' + path)
        records[path] = (int(size), digest)
    return records

def refresh_trust(rows, declaration_dir):
    """Wait for exact persisted database equality, explicitly flag cache uncertainty.

    A down daemon, mismatch, CLI failure or timeout raises; there is no offline
    success path. This return value alone MUST NOT be called a security barrier.
    """
    _run('systemctl', 'is-active', '--quiet', 'fapolicyd')
    expected = stage_trust(rows, declaration_dir)
    _run('fapolicyd-cli', '--update')
    deadline = time.monotonic() + 30
    last_error = 'database has not converged'
    while time.monotonic() < deadline:
        _run('systemctl', 'is-active', '--quiet', 'fapolicyd')
        try:
            if _dump_records(_run('fapolicyd-cli', '--dump-db')) == expected:
                check = _run('fapolicyd-cli', '--check-trustdb')
                _run('systemctl', 'is-active', '--quiet', 'fapolicyd')
                return {'database_matches':True, 'trusted_files':len(expected),
                        'check_trustdb':check, 'reload_acknowledged':False,
                        'limitation':'CLI confirms persisted database equality, not daemon decision-cache invalidation'}
        except (ValueError, subprocess.CalledProcessError) as error:
            last_error = str(error)
        time.sleep(0.1)
    raise RuntimeError('trust refresh failed: ' + last_error)
