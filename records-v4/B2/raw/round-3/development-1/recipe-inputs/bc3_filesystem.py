#!/usr/bin/python3
"""Declaration-first filesystem for the bounded build-3 image.

API reference: https://github.com/fusepy/fusepy/blob/master/fuse.py
Run as root: bc3_filesystem.py STORE MOUNT [--seed DIRECTORY]
The operator designates STORE/current/declaration.json as primary declaration.
Immutable blobs implement its exact content requirements; callbacks publish only
complete generations. No read-time discovery/recording or interpreter detection.

Limits: whole-file writes and whole-state generations, serialized callbacks;
no writable mmap, special nodes, ACLs, locks or extended allocation operations.
Direct-I/O + zero cache TTLs are intentional. This is not a general POSIX FS.
"""
import argparse
import base64
import copy
import errno
import hashlib
import json
import os
from pathlib import Path
import stat
import time
import uuid
try:
    from fuse import FUSE, FuseOSError, Operations, fuse_get_context
except ImportError:
    from fusepy import FUSE, FuseOSError, Operations, fuse_get_context


def syncdir(path):
    fd = os.open(path, os.O_DIRECTORY | os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def durable(path, data):
    with open(path, 'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


class DeclaredFS(Operations):
    def __init__(self, store, seed=None, uid=0, gid=0, mode=0o755, account_databases=False):
        self.account_databases = account_databases
        self.store = Path(store).resolve()
        self.store.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.store, 0o700)
        self.blobs = self.store / 'blobs'
        self.generations = self.store / 'generations'
        self.blobs.mkdir(exist_ok=True)
        self.generations.mkdir(exist_ok=True)
        self.handles = {}
        self.next_handle = 0
        self.failed = False
        self.previous = None
        self.previous_directory = None
        if (self.store / 'current').exists():
            self.state = json.loads((self.store / 'current/declaration.json').read_bytes())
            current_directory = (self.store / 'current').resolve()
            older = sorted(d for d in self.generations.iterdir() if d != current_directory)
            if older:
                self.previous_directory = older[-1]
                self.previous = json.loads((older[-1] / 'declaration.json').read_bytes())
            # No handles survive a daemon restart. Retire previously open,
            # unlinked objects through a new declaration before serving.
            candidate = copy.deepcopy(self.state)
            self.collect(candidate)
            if candidate != self.state:
                self.commit(candidate, 'recovery-retire-unlinked')
        else:
            self.state = {'format': 'bc3-declared-filesystem-v1', 'generation': 0,
                          'next_inode': 2, 'paths': {'/': '1'},
                          'objects': {'1': self.node(stat.S_IFDIR | mode, uid, gid)}}
            if seed:
                self.import_tree(Path(seed))
            self.commit(self.state, 'initial-application')
        self.validate()

    def node(self, mode, uid, gid):
        now = time.time()
        n = dict(st_mode=mode, st_uid=uid, st_gid=gid, st_atime=now,
                 st_mtime=now, st_ctime=now, st_size=0, xattrs={})
        if stat.S_ISREG(mode):
            n['sha256'] = self.put_blob(b'')
        return n

    def put_blob(self, data):
        digest = hashlib.sha256(data).hexdigest()
        dest = self.blobs / digest
        if not dest.exists():
            durable(dest, data)
            os.chmod(dest, 0o400)
            syncdir(self.blobs)
        return digest

    def import_tree(self, root):
        # Seed copying is an explicit initial declaration application, never a
        # running-session inventory. Hard links are preserved.
        seen = {}
        def add(source, target):
            st = source.lstat()
            typ = stat.S_IFMT(st.st_mode)
            if typ not in (stat.S_IFREG, stat.S_IFDIR, stat.S_IFLNK):
                raise RuntimeError('unsupported seed node: ' + str(source))
            key = (st.st_dev, st.st_ino)
            if key in seen:
                self.state['paths'][target] = seen[key]
                return
            ino = '1' if target == '/' else str(self.state['next_inode'])
            if target != '/':
                self.state['next_inode'] += 1
            seen[key] = ino
            n = self.node(st.st_mode, st.st_uid, st.st_gid)
            for field in ('st_atime', 'st_mtime', 'st_ctime', 'st_size'):
                n[field] = getattr(st, field)
            if typ == stat.S_IFREG:
                n['sha256'] = self.put_blob(source.read_bytes())
            elif typ == stat.S_IFLNK:
                n['target'] = os.readlink(source)
            self.state['objects'][ino] = n
            self.state['paths'][target] = ino
            if typ == stat.S_IFDIR:
                for child in sorted(source.iterdir()):
                    add(child, target.rstrip('/') + '/' + child.name)
        add(root, '/')

    def validate(self):
        for ino in self.state['paths'].values():
            if ino not in self.state['objects']:
                raise RuntimeError('missing declared inode')
        for n in self.state['objects'].values():
            if 'sha256' in n:
                data = (self.blobs / n['sha256']).read_bytes()
                if len(data) != n['st_size'] or hashlib.sha256(data).hexdigest() != n['sha256']:
                    raise RuntimeError('declared content mismatch')

    def commit(self, candidate, operation):
        if self.failed:
            raise FuseOSError(errno.EIO)
        candidate = copy.deepcopy(candidate)
        candidate['generation'] = self.state.get('generation', 0) + 1
        if self.account_databases:
            from bc3_account_rows import account_rows, database_rows
            snapshot = {}
            for basename in ('passwd', 'group', 'shadow', 'gshadow', 'subuid', 'subgid'):
                ino = candidate['paths'].get('/' + basename)
                if ino is not None:
                    node = candidate['objects'][ino]
                    if 'sha256' in node:
                        snapshot['/etc/' + basename] = (self.blobs / node['sha256']).read_bytes()
            try:
                candidate['account_rows'] = account_rows(snapshot)
                candidate.pop('account_parse_error', None)
            except (ValueError, UnicodeError, KeyError) as error:
                # A direct privileged malformed edit remains possible breaking;
                # it must not leave stale semantic account claims in force.
                candidate['account_rows'] = database_rows(snapshot)
                candidate['account_parse_error'] = str(error)
        name = '%020d-%s' % (candidate['generation'], uuid.uuid4().hex)
        directory = self.generations / name
        previous_name = (self.store / 'current').resolve().name if (self.store / 'current').exists() else None
        switched = False
        try:
            directory.mkdir(mode=0o700)
            data = encoded(candidate)
            durable(directory / 'declaration.json', data)
            # This report becomes authoritative only through the same current
            # pointer as the declaration. It is not a premature public report.
            durable(directory / 'success.json', encoded({
                'status': 'success', 'operation': operation,
                'declaration_sha256': hashlib.sha256(data).hexdigest(),
                'generation': candidate['generation'], 'utc_epoch': time.time()}))
            syncdir(directory)
            syncdir(self.generations)
            temporary = self.store / ('next-' + uuid.uuid4().hex)
            os.symlink('generations/' + name, temporary)
            os.replace(temporary, self.store / 'current')
            switched = True
            syncdir(self.store)
            old_state = self.state
            old_directory = self.previous_directory
            retired = self.previous
            self.previous = old_state
            self.previous_directory = (self.generations / previous_name) if previous_name else None
            self.state = candidate
            # The immutable generation is the primary report. A compact audit
            # survives retirement, retaining every changed path and content ID.
            changes = []
            for path in sorted(set(old_state['paths']) | set(candidate['paths'])):
                before_id = old_state['paths'].get(path)
                after_id = candidate['paths'].get(path)
                before = old_state['objects'].get(before_id)
                after = candidate['objects'].get(after_id)
                if before_id != after_id or before != after:
                    changes.append({'path': path, 'inode': after_id,
                                    'sha256': after.get('sha256') if after else None,
                                    'present': after_id is not None})
            event = encoded({'generation': candidate['generation'], 'operation': operation,
                             'declaration_sha256': hashlib.sha256(data).hexdigest(),
                             'changes': changes, 'status': 'success', 'utc_epoch': time.time()})
            with open(self.store / 'audit.jsonl', 'ab') as audit:
                audit.write(event)
                audit.flush()
                os.fsync(audit.fileno())
            # Retain current + preceding generation only. Blob retention follows
            # their complete objects maps, including all open-unlinked inodes.
            if old_directory and old_directory != self.previous_directory:
                for item in old_directory.iterdir():
                    item.unlink()
                old_directory.rmdir()
            retained = {n['sha256'] for state in (candidate, old_state)
                        for n in state['objects'].values() if 'sha256' in n}
            if retired:
                displaced = {n['sha256'] for n in retired['objects'].values() if 'sha256' in n}
                for digest in displaced - retained:
                    (self.blobs / digest).unlink(missing_ok=True)
            syncdir(self.generations)
        except Exception:
            # Do not serve the previous in-memory state after uncertain commit.
            # A restart validates the authoritative pointer before mounting.
            if switched:
                self.failed = True
            raise

    def __call__(self, op, *args):
        if self.failed:
            raise FuseOSError(errno.EIO)
        try:
            return getattr(self, op)(*args)
        except OSError as e:
            raise FuseOSError(e.errno or errno.EIO)

    def inode(self, path, fh=None, state=None):
        s = self.state if state is None else state
        if fh is not None:
            if fh not in self.handles:
                raise FuseOSError(errno.EBADF)
            return self.handles[fh]['inode']
        if path not in s['paths']:
            raise FuseOSError(errno.ENOENT)
        return s['paths'][path]

    def parent(self, path, state):
        if path == '/':
            raise FuseOSError(errno.EBUSY)
        p = path.rsplit('/', 1)[0] or '/'
        n = state['objects'][self.inode(p, state=state)]
        if not stat.S_ISDIR(n['st_mode']):
            raise FuseOSError(errno.ENOTDIR)

    def allocate(self, state, path, mode):
        self.parent(path, state)
        if path in state['paths']:
            raise FuseOSError(errno.EEXIST)
        uid, gid, _ = fuse_get_context()
        ino = str(state['next_inode'])
        state['next_inode'] += 1
        state['paths'][path] = ino
        state['objects'][ino] = self.node(mode, uid, gid)
        return ino

    def collect(self, state):
        live = set(state['paths'].values()) | {h['inode'] for h in self.handles.values()}
        state['objects'] = {i: n for i, n in state['objects'].items() if i in live}

    def getattr(self, path, fh=None):
        ino = self.inode(path, fh)
        n = self.state['objects'][ino]
        out = {k: v for k, v in n.items() if k.startswith('st_')}
        out['st_ino'] = int(ino)
        links = sum(i == ino for i in self.state['paths'].values())
        if stat.S_ISDIR(n['st_mode']):
            if path is None:
                path = next((p for p, i in self.state['paths'].items() if i == ino), None)
            links = 2 + sum(stat.S_ISDIR(self.state['objects'][i]['st_mode'])
                            for p, i in self.state['paths'].items()
                            if p != '/' and (p.rsplit('/', 1)[0] or '/') == path)
        out['st_nlink'] = links
        out['st_blocks'] = (n['st_size'] + 511) // 512
        return out

    def opendir(self, path):
        ino = self.inode(path)
        if not stat.S_ISDIR(self.state['objects'][ino]['st_mode']):
            raise FuseOSError(errno.ENOTDIR)
        return self.make_handle(ino, os.O_RDONLY)

    def releasedir(self, path, fh):
        return self.release(path, fh)

    def readdir(self, path, fh):
        if path is None:
            ino = self.inode(path, fh)
            path = next((p for p, i in self.state['paths'].items() if i == ino), None)
            if path is None:
                return ['.', '..']
        if not stat.S_ISDIR(self.state['objects'][self.inode(path)]['st_mode']):
            raise FuseOSError(errno.ENOTDIR)
        return ['.', '..'] + [p.rsplit('/', 1)[1] for p in self.state['paths']
                             if p != '/' and (p.rsplit('/', 1)[0] or '/') == path]

    def make_handle(self, ino, flags):
        self.next_handle += 1
        self.handles[self.next_handle] = dict(inode=ino, flags=flags)
        return self.next_handle

    def open(self, path, flags):
        ino = self.inode(path)
        if not stat.S_ISREG(self.state['objects'][ino]['st_mode']):
            raise FuseOSError(errno.EISDIR)
        if flags & os.O_TRUNC:
            self.truncate(path, 0)
        return self.make_handle(ino, flags)

    def create(self, path, mode, fi=None):
        state = copy.deepcopy(self.state)
        ino = self.allocate(state, path, stat.S_IFREG | mode)
        self.commit(state, 'create')
        return self.make_handle(ino, os.O_RDWR)

    def read(self, path, size, offset, fh):
        n = self.state['objects'][self.inode(path, fh)]
        with open(self.blobs / n['sha256'], 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def change_data(self, path, fh, transform, operation):
        state = copy.deepcopy(self.state)
        n = state['objects'][self.inode(path, fh)]
        if not stat.S_ISREG(n['st_mode']):
            raise FuseOSError(errno.EINVAL)
        data = transform((self.blobs / n['sha256']).read_bytes())
        n.update(sha256=self.put_blob(data), st_size=len(data),
                 st_mtime=time.time(), st_ctime=time.time())
        # Kernel normally clears these on an unprivileged write; never retain
        # privilege bits when replacing bytes through this ordinary filesystem.
        n['st_mode'] &= ~(stat.S_ISUID | stat.S_ISGID)
        self.commit(state, operation)

    def write(self, path, data, offset, fh):
        h = self.handles[fh]
        if h['flags'] & os.O_APPEND:
            offset = self.state['objects'][h['inode']]['st_size']
        self.change_data(path, fh, lambda old: old[:offset].ljust(offset, b'\0') + data + old[offset + len(data):], 'write')
        return len(data)

    def truncate(self, path, length, fh=None):
        if length < 0:
            raise FuseOSError(errno.EINVAL)
        self.change_data(path, fh, lambda old: old[:length].ljust(length, b'\0'), 'truncate')
        return 0

    def flush(self, path, fh):
        return 0

    def fsync(self, path, datasync, fh):
        syncdir(self.store)
        return 0

    def release(self, path, fh):
        self.handles.pop(fh, None)
        state = copy.deepcopy(self.state)
        self.collect(state)
        if state != self.state:
            self.commit(state, 'release-unlinked')
        return 0

    def mkdir(self, path, mode):
        state = copy.deepcopy(self.state)
        self.allocate(state, path, stat.S_IFDIR | mode)
        self.commit(state, 'mkdir')
        return 0

    def unlink(self, path):
        state = copy.deepcopy(self.state)
        ino = self.inode(path)
        if stat.S_ISDIR(state['objects'][ino]['st_mode']):
            raise FuseOSError(errno.EISDIR)
        del state['paths'][path]
        self.collect(state)
        self.commit(state, 'unlink')
        return 0

    def rmdir(self, path):
        state = copy.deepcopy(self.state)
        self.parent(path, state)
        ino = self.inode(path)
        if not stat.S_ISDIR(state['objects'][ino]['st_mode']):
            raise FuseOSError(errno.ENOTDIR)
        if any(p.startswith(path + '/') for p in state['paths']):
            raise FuseOSError(errno.ENOTEMPTY)
        del state['paths'][path]
        self.collect(state)
        self.commit(state, 'rmdir')
        return 0

    def rename(self, old, new):
        state = copy.deepcopy(self.state)
        self.parent(old, state)
        self.parent(new, state)
        ino = self.inode(old)
        if old == new:
            return 0
        isdir = stat.S_ISDIR(state['objects'][ino]['st_mode'])
        if isdir and new.startswith(old + '/'):
            raise FuseOSError(errno.EINVAL)
        if new in state['paths']:
            target = state['paths'][new]
            if target == ino:
                return 0
            targetdir = stat.S_ISDIR(state['objects'][target]['st_mode'])
            if isdir != targetdir:
                raise FuseOSError(errno.ENOTDIR if isdir else errno.EISDIR)
            if targetdir and any(p.startswith(new + '/') for p in state['paths']):
                raise FuseOSError(errno.ENOTEMPTY)
            del state['paths'][new]
        moved = {p: i for p, i in state['paths'].items() if p == old or p.startswith(old + '/')}
        for p in moved:
            del state['paths'][p]
        for p, i in moved.items():
            state['paths'][new + p[len(old):]] = i
        self.collect(state)
        self.commit(state, 'rename')
        return 0

    def link(self, target, source):
        # fusepy translates kernel (old, new) into Operations(new, old).
        state = copy.deepcopy(self.state)
        self.parent(target, state)
        ino = self.inode(source)
        if stat.S_ISDIR(state['objects'][ino]['st_mode']):
            raise FuseOSError(errno.EPERM)
        if target in state['paths']:
            raise FuseOSError(errno.EEXIST)
        state['paths'][target] = ino
        self.commit(state, 'link')
        return 0

    def symlink(self, target, source):
        state = copy.deepcopy(self.state)
        ino = self.allocate(state, target, stat.S_IFLNK | 0o777)
        state['objects'][ino].update(target=source, st_size=len(os.fsencode(source)))
        self.commit(state, 'symlink')
        return 0

    def readlink(self, path):
        return self.state['objects'][self.inode(path)]['target']

    def metadata(self, path, operation, update):
        state = copy.deepcopy(self.state)
        n = state['objects'][self.inode(path)]
        update(n)
        n['st_ctime'] = time.time()
        self.commit(state, operation)
        return 0

    def chmod(self, path, mode):
        return self.metadata(path, 'chmod', lambda n: n.update(st_mode=stat.S_IFMT(n['st_mode']) | mode))

    def chown(self, path, uid, gid):
        def update(n):
            if uid != -1:
                n['st_uid'] = uid
            if gid != -1:
                n['st_gid'] = gid
            n['st_mode'] &= ~(stat.S_ISUID | stat.S_ISGID)
        return self.metadata(path, 'chown', update)

    def utimens(self, path, times=None):
        atime, mtime = times if times is not None else (time.time(), time.time())
        return self.metadata(path, 'utimens', lambda n: n.update(st_atime=atime, st_mtime=mtime))

    def getxattr(self, path, name, position=0):
        attrs = self.state['objects'][self.inode(path)]['xattrs']
        if name not in attrs:
            raise FuseOSError(errno.ENODATA)
        return base64.b64decode(attrs[name])

    def listxattr(self, path):
        return list(self.state['objects'][self.inode(path)]['xattrs'])

    def setxattr(self, path, name, value, options, position=0):
        if not name.startswith('user.'):
            raise FuseOSError(errno.ENOTSUP)
        attrs = self.state['objects'][self.inode(path)]['xattrs']
        if options & 1 and name in attrs:
            raise FuseOSError(errno.EEXIST)
        if options & 2 and name not in attrs:
            raise FuseOSError(errno.ENODATA)
        return self.metadata(path, 'setxattr', lambda n: n['xattrs'].update({name: base64.b64encode(value).decode()}))

    def removexattr(self, path, name):
        if name not in self.state['objects'][self.inode(path)]['xattrs']:
            raise FuseOSError(errno.ENODATA)
        return self.metadata(path, 'removexattr', lambda n: n['xattrs'].pop(name))

    def statfs(self, path):
        s = os.statvfs(self.store)
        return {k: getattr(s, k) for k in ('f_bsize', 'f_frsize', 'f_blocks', 'f_bfree', 'f_bavail', 'f_files', 'f_ffree', 'f_favail', 'f_namemax')}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('store')
    p.add_argument('mount')
    p.add_argument('--seed')
    p.add_argument('--uid', type=int, default=0)
    p.add_argument('--gid', type=int, default=0)
    p.add_argument('--mode', type=lambda x: int(x, 8), default=0o755)
    p.add_argument('--initialize-only', action='store_true')
    p.add_argument('--account-databases', action='store_true')
    a = p.parse_args()
    fs = DeclaredFS(a.store, a.seed, a.uid, a.gid, a.mode, a.account_databases)
    if not a.initialize_only:
        FUSE(fs, a.mount, foreground=True, nothreads=True, allow_other=True,
             default_permissions=True, direct_io=True, attr_timeout=0,
             entry_timeout=0, negative_timeout=0, use_ino=True,
             nosuid=True, nodev=True, noexec=True, nonempty=True, fsname='bc3-declared-filesystem')


if __name__ == '__main__':
    main()
