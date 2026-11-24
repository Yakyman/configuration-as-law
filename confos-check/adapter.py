"""The thin adapter between the cases and the builder's ConfOS (build/INTERFACE.md, build/DECLARATION.md rev. 1).

The cases speak in semantic line specs (CASES.md, "Notation"). The adapter renders each spec into the builder's
syntax; a spec that has no kind in that syntax raises NotExpressible(spec). The person's lines are kept as specs
in a Declaration; every change re-renders the whole declaration.

Backends:
- ConfosBackend: write the declaration and its content files as root, `sudo confos apply`, wait for the reboot,
  reconnect, `confos status`, check `APPLIED SHA256` against the sha256 of the bytes written; power cut; link.
- StockBackend: a stock Debian 13 cloud image for testing the runner; every ConfOS operation raises NotAvailable.

Rendering (build/DECLARATION.md revision 1):
  base                              -> base VERSION (of the source's VERSION file)
  archive-state T                   -> snapshot T
  package NAME[=VERSION]            -> package NAME VERSION (VERSION from the Packages index of the snapshot)
  account NAME uid= gid= groups= shell= home=  -> account NAME UID GID GROUPS SHELL HOME (no uid/gid: NotExpressible)
  authorized-key NAME KEY           -> authorized-key NAME TYPE KEY   (@PERSON_KEY@ = the runner's public key)
  service NAME STATE EXE [ARG ...]  -> service NAME STATE EXE [ARG ...]
  service NAME TEXT [enabled]       -> service NAME enabled|disabled EXE ARGS (from ExecStart= of TEXT)
  firewall [NAME] TEXT              -> rule NAME TEXT
  setting NAME VALUE                -> setting NAME VALUE
  script PATH SHA256                -> file PATH 0755 SHA256 files/NAME (bytes from cases/declarations/)
  appimage PATH URL SHA256          -> file PATH 0755 SHA256 files/NAME (bytes fetched and checked)
  download PATH URL SHA256 [unpack=MEMBER] -> file PATH 0755 SHA256(MEMBER) files/NAME
  built PATH SOURCE CMD             -> file PATH 0755 SHA256 files/NAME (the person builds it: on the machine when
                                       one is given, else on the host from the known source)
  sudo RULE                         -> file /etc/sudoers.d/cases-H 0440 SHA256 files/NAME
  pip, npm, flatpak, user-unit, shell-startup, git-config, container-image -> NotExpressible
"""
import base64
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tarfile
import tempfile
import threading
import time
import urllib.request

from lib.common import RunnerError, utc, sha256_bytes, CASES_DIR, load_env, home_path

SNAPSHOT_URL = 'https://snapshot.debian.org/archive/debian/{t}/dists/trixie/main/binary-amd64/Packages.xz'
DECL_PATH = '/state/declaration.conf'
CONTENT_DIR = 'files'          # relative to the declaration: /state/files/NAME at runtime

# Sources of programs that the person builds (PROGRAMS.md, C7 and OW-7).
KNOWN_SOURCES = {
    'hello.c': ('https://raw.githubusercontent.com/docker-library/hello-world/'
                '522bcd2faf422c60b9d20e64d7cd6d56600aec97/hello.c',
                'cb95a0ed950c272471e7eb2a6b4261d857174bc3750874f538ac60e20af16d34'),
}

# Kinds of build/DECLARATION.md and the release that introduced each (INTERFACE.md / DECLARATION.md revisions
# 6-12). A spec of a channel is rendered in its native kind when the base release has it, else as before.
KIND_SINCE = {'pip': (0, 6), 'npm': (0, 6), 'compile': (0, 8), 'flatpak': (0, 9), 'appimage': (0, 10),
              'container': (0, 11), 'user-unit': (0, 12), 'linuxgsm': (0, 18)}
# The pinned inputs of those lines, made by tools/make-inputs.sh on the server from the upstream sources of
# PROGRAMS.md: KIND NAME FILE SHA256 EXTRA (EXTRA: version, image configuration digest or OSTree commit).
INPUTS_DIR = home_path(load_env().get('SERVER_DIR', 'VMs/confos/cases')) / 'inputs'


def version_tuple(v):
    try:
        return tuple(int(x) for x in str(v).split('.')[:2])
    except ValueError:
        return (0, 0)


def file_sha(v):
    """SHA256 of a content file held as bytes or as a path to a large input."""
    if isinstance(v, (bytes, bytearray)):
        return sha256_bytes(v)
    h = hashlib.sha256()
    with open(v, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def write_content(path, v):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(v, (bytes, bytearray)):
        path.write_bytes(v)
    else:
        try:
            if path.exists():
                path.unlink()
            os.link(v, path)
        except OSError:
            shutil.copyfile(v, path)


NO_KIND = {
    'pip': 'no kind for a package of a language package manager (pip) in the build/DECLARATION.md of this base release',
    'npm': 'no kind for a package of a language package manager (npm) in the build/DECLARATION.md of this base release',
    'flatpak': 'no kind for a Flatpak application in the build/DECLARATION.md of this base release',
    'user-unit': 'no kind for a user service or timer of an account in the build/DECLARATION.md of this base release',
    'shell-startup': 'no kind for a shell startup file of an account in the build/DECLARATION.md of this base release',
    'git-config': 'no kind for a program setting of an account in the build/DECLARATION.md of this base release',
    'container-image': 'no kind for a container image in the build/DECLARATION.md of this base release',
}

# Kinds of build/DECLARATION.md that a released version implements (build/STATE.md of that version). A line of
# another kind fails the whole application there, so it is left out of the rendered declaration and recorded.
IMPLEMENTED = {
    '0.1': {'kinds': {'base', 'snapshot', 'package', 'account', 'authorized-key', 'file', 'setting'},
            'settings': {'hostname': None, 'timezone': {'UTC'}}},
    # 0.2: sysctl settings, services, single input-chain rules (build/STATE.md, DECLARATION.md rev. 2/3)
    '0.2': {'kinds': {'base', 'snapshot', 'package', 'account', 'authorized-key', 'file', 'setting', 'service',
                      'rule'},
            'settings': {'hostname': None, 'timezone': {'UTC'}, 'sysctl:': None}},
    # 0.3: as 0.2; `file` targets only below /home/, /usr/local/, /etc/confos/user/ (DECLARATION.md rev. 3)
    '0.3': {'kinds': {'base', 'snapshot', 'package', 'account', 'authorized-key', 'file', 'setting', 'service',
                      'rule'},
            'settings': {'hostname': None, 'timezone': {'UTC'}, 'sysctl:': None},
            'file_prefixes': ('/home/', '/usr/local/', '/etc/confos/user/')},
}


class NotExpressible(Exception):
    label = 'not expressible'

    def __init__(self, spec, reason):
        super().__init__(f'{spec}: {reason}')
        self.spec = spec
        self.reason = reason


class NotImplementedKind(NotExpressible):
    """The kind exists in the builder's syntax, but the released version does not implement it."""
    label = 'not implemented'


class NotAvailable(Exception):
    """The operation exists only on ConfOS (stock backend)."""


# ---------------------------------------------------------------- specs

class Spec:
    def __init__(self, text):
        self.text = text.strip()
        self.fields = shlex.split(self.text)
        if not self.fields:
            raise ValueError('empty spec')
        self.kind = self.fields[0]
        self.args = self.fields[1:]

    def options(self):
        return dict(a.split('=', 1) for a in self.args[1:] if '=' in a)

    def key(self):
        """The identity of the recorded thing: a change (L~) replaces the spec with the same key."""
        k, a = self.kind, self.args
        if k in ('base', 'archive-state'):
            return (k,)
        if k == 'package' or k == 'account-package':
            return ('package', a[0].split('=')[0])
        if k in ('pip',):
            return (k, a[0].split('==')[0])
        if k in ('npm',):
            return (k, a[0].rsplit('@', 1)[0] if not a[0].startswith('@') else a[0])
        if k == 'container-image':
            return (k, a[0].split('@')[0].rsplit(':', 1)[0])
        if k in ('user-unit', 'shell-startup', 'git-config'):
            return (k, a[0], a[1])
        if k == 'firewall':
            return (k, a[0] if len(a) > 1 else firewall_name(a[0]))
        if k == 'sudo':
            return (k, a[0])
        if k in ('script', 'appimage', 'download', 'built', 'compile-from'):
            return ('path', a[0])
        return (k, a[0] if a else '')

    def __repr__(self):
        return self.text


def firewall_name(text):
    m = re.search(r'dport (\d+)', text)
    return 'cases-' + (m.group(1) if m else hashlib.sha256(text.encode()).hexdigest()[:8])


def read_spec_file(path):
    specs = []
    for line in Path(path).read_text().splitlines():
        if line.strip() and not line.strip().startswith('#'):
            specs.append(Spec(line))
    return specs


class Declaration:
    """The person's lines, as specs, in order."""

    def __init__(self, specs):
        self.specs = list(specs)

    def copy(self):
        return Declaration(self.specs)

    def add(self, spec):
        spec = Spec(spec) if isinstance(spec, str) else spec
        if any(s.key() == spec.key() for s in self.specs):
            raise RunnerError(f'add of an already recorded thing: {spec}')
        self.specs.append(spec)
        return spec

    def change(self, spec):
        spec = Spec(spec) if isinstance(spec, str) else spec
        for i, s in enumerate(self.specs):
            if s.key() == spec.key():
                self.specs[i] = spec
                return s, spec
        raise RunnerError(f'change of a thing that is not recorded: {spec}')

    def remove(self, key_spec):
        key_spec = Spec(key_spec) if isinstance(key_spec, str) else key_spec
        for i, s in enumerate(self.specs):
            if s.key() == key_spec.key():
                return self.specs.pop(i)
        raise RunnerError(f'removal of a thing that is not recorded: {key_spec}')

    def find(self, kind):
        return [s for s in self.specs if s.kind == kind]


# ---------------------------------------------------------------- rendering

class Rendered:
    def __init__(self):
        self.lines = []               # builder lines
        self.files = {}               # relative content path -> bytes
        self.not_expressible = []     # (spec text, reason)
        self.records = []             # notes: resolved versions, computed checksums
        self.line_of_spec = {}        # spec text -> builder line(s)

    def text(self):
        return ('\n'.join(self.lines) + '\n').encode()

    def sha256(self):
        return sha256_bytes(self.text())

    def write(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'declaration.conf').write_bytes(self.text())
        for rel, data in self.files.items():
            write_content(directory / rel, data)
        (directory / 'render.json').write_text(json.dumps({
            'sha256': self.sha256(), 'not_expressible': self.not_expressible, 'records': self.records,
            'lines_of_specs': self.line_of_spec}, indent=1, sort_keys=True) + '\n')
        return directory / 'declaration.conf'


def rendered_from_dir(directory):
    """A Rendered declaration read back from a directory: declaration.conf and every content file beside it (as
    written by Rendered.write or read from a disk by the runner), for a build of the same declaration."""
    directory = Path(directory)
    r = Rendered()
    r.lines = (directory / 'declaration.conf').read_bytes().decode().rstrip('\n').split('\n')
    for p in sorted(directory.rglob('*')):
        rel = str(p.relative_to(directory))
        if p.is_file() and rel not in ('declaration.conf', 'render.json'):
            r.files[rel] = p
    return r


class Renderer:
    _lock = threading.Lock()

    def __init__(self, cache_dir, base_version, person_key, ev=None):
        self.cache = Path(cache_dir)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.base_version = base_version
        self.person_key = person_key.strip()
        self.ev = ev
        self.indexes = {}
        self.built = {}            # spec text -> (bytes, note) of the last build by the person
        self._inputs = None
        self.homes = {}

    def has(self, kind):
        return version_tuple(self.base_version) >= KIND_SINCE[kind]

    def input(self, kind, name):
        """(path, sha256, extra) of a pinned input of the manifest; RunnerError if it was not made."""
        if self._inputs is None:
            self._inputs = {}
            mf = INPUTS_DIR / 'manifest.tsv'
            if mf.exists():
                for l in mf.read_text().splitlines():
                    f = l.split('\t')
                    if len(f) >= 4:
                        self._inputs[(f[0], f[1])] = (INPUTS_DIR / f[2], f[3], f[4] if len(f) > 4 else '')
        got = self._inputs.get((kind, name))
        if not got or not got[0].exists():
            raise RunnerError(f'the pinned input {kind} {name} is not made (tools/make-inputs.sh on the server)')
        path, sha, extra = got
        return path, sha, extra

    # -- inputs
    def fetch(self, url, sha256=None):
        """Fetch URL into the cache by checksum. A wrong checksum or an HTTP error is a RunnerError (unobserved)."""
        name = hashlib.sha256(url.encode()).hexdigest()
        path = self.cache / 'blobs' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            if not path.exists():
                start = utc()
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'cases-runner'})
                    with urllib.request.urlopen(req, timeout=300) as r:
                        data = r.read()
                        status = r.status
                except Exception as e:
                    if self.ev:
                        self.ev.record('H', f'fetch {url}', start, utc(), 1, b'', str(e).encode())
                    raise RunnerError(f'download failed: {url}: {e}')
                if self.ev:
                    self.ev.record('H', f'fetch {url}', start, utc(), 0, f'HTTP {status} {len(data)} bytes '
                                   f'sha256 {sha256_bytes(data)}\n'.encode(), b'')
                tmp = path.with_suffix('.tmp')
                tmp.write_bytes(data)
                os.replace(tmp, path)
        data = path.read_bytes()
        if sha256 and sha256 != '@SHA256@' and sha256_bytes(data) != sha256:
            raise RunnerError(f'checksum differs: {url}: {sha256_bytes(data)} != {sha256}')
        return data

    def packages_index(self, t):
        if t not in self.indexes:
            data = lzma.decompress(self.fetch(SNAPSHOT_URL.format(t=t)))
            index = {}
            for para in data.decode('utf-8', 'replace').split('\n\n'):
                fields = dict(re.findall(r'^([A-Za-z0-9-]+): (.*)$', para, re.M))
                if 'Package' in fields:
                    index[fields['Package']] = fields['Version']
            self.indexes[t] = index
        return self.indexes[t]

    # -- one spec
    def render_spec(self, spec, out, snapshot, machine=None):
        k, a = spec.kind, spec.args
        name_of = lambda path: CONTENT_DIR + '/' + re.sub(r'[^A-Za-z0-9._-]', '_', path.strip('/'))

        def file_line(path, mode, data, note):
            sha = sha256_bytes(data)
            rel = name_of(path)
            out.files[rel] = data
            out.records.append({'spec': spec.text, 'note': note, 'sha256': sha})
            owner = ''
            if version_tuple(self.base_version) >= (0, 21):
                # DECLARATION.md rev. 21: `file PATH MODE UID:GID SHA256 SOURCE`; a file in an account's home is the
                # account's, any other file root's
                own = next((ids for home, ids in sorted(self.homes.items(), key=lambda x: -len(x[0]))
                            if path.startswith(home.rstrip('/') + '/')), (0, 0))
                owner = f' {own[0]}:{own[1]}'
            return [f'file {shlex.quote(path)} {mode}{owner} {sha} {shlex.quote(rel)}']

        def input_rel(path):
            rel = CONTENT_DIR + '/' + path.name
            out.files[rel] = path
            return rel

        # native kinds of the channels (DECLARATION.md revisions 6-12), when the base release has them
        if k == 'pip' and self.has('pip'):
            name, _, version = a[0].partition('==')
            path, sha, ver = self.input('pip', name)
            if ver != version:
                raise RunnerError(f'pinned wheel of {name} is {ver}, the spec names {version}')
            out.records.append({'spec': spec.text, 'note': 'wheel from PyPI (tools/make-inputs.sh)', 'sha256': sha})
            return [f'pip {name} {version} {sha} {shlex.quote(input_rel(path))}']
        if k == 'npm' and self.has('npm'):
            name, _, version = a[0].rpartition('@')
            path, sha, ver = self.input('npm', name)
            if ver != version:
                raise RunnerError(f'pinned lock of {name} is for {ver}, the spec names {version}')
            out.records.append({'spec': spec.text, 'note': 'lock resolved by native npm (tools/make-inputs.sh)',
                                'sha256': sha})
            return [f'npm {name} {version} {sha} {shlex.quote(input_rel(path))}']
        if k == 'flatpak' and self.has('flatpak'):
            app = a[0]
            lines = []
            for ref in sorted(r for (kk, r) in (self.input_keys() or ()) if kk == 'flatpak'
                              and r.startswith('runtime/')):
                path, sha, commit = self.input('flatpak', ref)
                lines.append(f'flatpak {ref} {commit} {sha} {shlex.quote(input_rel(path))}')
            ref = f'app/{app}/x86_64/stable'
            path, sha, commit = self.input('flatpak', ref)
            lines.append(f'flatpak {ref} {commit} {sha} {shlex.quote(input_rel(path))}')
            out.records.append({'spec': spec.text, 'note': 'bundles exported by native flatpak build-bundle from '
                                'Flathub (tools/make-inputs.sh); the runtime line first'})
            return lines
        if k == 'appimage' and self.has('appimage'):
            path, url, sha = a[0], a[1], a[2]
            data = self.fetch(url, sha)
            rel = name_of(path)
            out.files[rel] = data
            out.records.append({'spec': spec.text, 'note': f'fetched: {url}', 'sha256': sha256_bytes(data)})
            return [f'appimage {shlex.quote(path)} 0755 {sha256_bytes(data)} {shlex.quote(rel)}']
        if k == 'linuxgsm' and self.has('linuxgsm'):
            # build/DECLARATION.md rev. 18+: `linuxgsm USER PATH RELEASE SHA256 BUNDLE`; the bundle is made by
            # tools/make-inputs.sh (step game) from the upstream archives and the defaults of the published release
            account, path, release = a[0], a[1], a[2]
            p, sha, _ = self.input('linuxgsm', release)
            rel = CONTENT_DIR + '/' + p.name
            out.files[rel] = p
            out.records.append({'spec': spec.text, 'note': f'bundle {p.name} (tools/make-inputs.sh game)',
                                'sha256': sha})
            return [f'linuxgsm {shlex.quote(account)} {shlex.quote(path)} {shlex.quote(release)} {sha} '
                    f'{shlex.quote(rel)}']
        if k == 'compile-from' and self.has('compile'):
            # REVIEW.md R2 (OW-7): the person records their own program by a compile line whose source is the file
            # they fetched and edited; the runner copies that file from the machine into the declaration's files
            path, source, flags = a[0], a[1], a[2:]
            if machine is not None:
                code, b64, _ = machine.u('base64 -w0 ' + shlex.quote(source), timeout=120)
                if code:
                    raise StepFailed(f'the person\'s source {source} could not be read')
                self.built[spec.text] = (base64.b64decode(b64), f'the person\'s source {source}, read from the machine')
            if spec.text not in self.built:
                raise NotExpressible(spec.text, 'the source of the program is read from the machine')
            src, note = self.built[spec.text]
            # one content file per line, named after the program it builds (the name of the source may be that of
            # another line's content file, for example D-test's files/hello.c)
            rel = CONTENT_DIR + '/compile_' + path.strip('/').replace('/', '_') + Path(source).suffix
            out.files[rel] = src
            out.records.append({'spec': spec.text, 'note': note, 'sha256': sha256_bytes(src)})
            return [f'compile {shlex.quote(path)} 0755 {sha256_bytes(src)} {shlex.quote(rel)}' +
                    ''.join(' ' + shlex.quote(f) for f in flags)]
        if k == 'built' and machine is None and self.has('compile'):
            path, source, command = a[0], a[1], a[2]
            known = KNOWN_SOURCES.get(Path(source).name)
            if not known:
                raise NotExpressible(spec.text, 'the source of the program is not available to the renderer')
            src = self.fetch(*known)
            words = shlex.split(command)
            flags = [w for w in words[1:] if w.startswith('-') and w != '-o' and not w.startswith('-o')]
            rel = CONTENT_DIR + '/' + Path(source).name
            out.files[rel] = src
            out.records.append({'spec': spec.text, 'note': f'source {known[0]}; compiled by the system (compile '
                                f'line), flags of the person\'s command: {flags}', 'sha256': sha256_bytes(src)})
            return [f'compile {shlex.quote(path)} 0755 {sha256_bytes(src)} {shlex.quote(rel)}' +
                    ''.join(' ' + shlex.quote(f) for f in flags)]
        if k == 'container-image' and self.has('container'):
            name = a[0].split('@')[0]
            path, sha, config = self.input('container', name)
            user = spec.options().get('user', 'person')
            out.records.append({'spec': spec.text, 'note': 'OCI archive saved by native podman (tools/make-inputs.sh)',
                                'sha256': sha})
            return [f'container {user} {name} {config.removeprefix("sha256:")} {sha} '
                    f'{shlex.quote(input_rel(path))}']
        if k == 'user-unit' and self.has('user-unit'):
            user, name, text = a[0], a[1], a[2].encode().decode('unicode_escape')
            state = 'enabled' if 'enabled' in a[3:] else 'disabled'
            data = text.encode()
            rel = CONTENT_DIR + '/user-units/' + user + '/' + name
            out.files[rel] = data
            out.records.append({'spec': spec.text, 'note': 'unit text of the spec', 'sha256': sha256_bytes(data)})
            return [f'user-unit {user} {name} {state} {sha256_bytes(data)} {shlex.quote(rel)}']
        if k == 'shell-startup' and version_tuple(self.base_version) >= (0, 7):
            # 0.7+: the startup files are empty immutable base files unless a file line supplies their bytes
            user, name, text = a[0], a[1], a[2]
            home = f'/home/{user}'
            return file_line(f'{home}/{name}', '0644', (text + '\n').encode(), 'the startup file, exact bytes')
        if k == 'git-config' and version_tuple(self.base_version) >= (0, 7):
            user, key, value = a[0], a[1], a[2]
            section, _, opt = key.partition('.')
            data = f'[{section}]\n\t{opt} = {value}\n'.encode()
            return file_line(f'/home/{user}/.gitconfig', '0644', data, 'the program setting, exact bytes')

        if k in NO_KIND:
            raise NotExpressible(spec.text, NO_KIND[k])
        if k == 'base':
            return [f'base {self.base_version}']
        if k == 'archive-state':
            return [f'snapshot {a[0]}']
        if k in ('package', 'account-package'):
            name, _, version = a[0].partition('=')
            if not version:
                if not snapshot:
                    raise NotExpressible(spec.text, 'no archive state in the declaration to resolve a version')
                version = self.packages_index(snapshot).get(name)
                if not version:
                    raise RunnerError(f'package {name} is not in the Packages index of {snapshot}')
                out.records.append({'spec': spec.text, 'note': f'version from Packages of {snapshot}',
                                    'version': version})
            return [f'package {name} {shlex.quote(version)}']
        if k == 'account':
            o = spec.options()
            if 'uid' not in o or 'gid' not in o:
                raise NotExpressible(spec.text, 'the `account` kind requires the numeric UID and GID')
            return [f"account {a[0]} {o['uid']} {o['gid']} {o.get('groups', '-')} "
                    f"{o.get('shell', '/bin/bash')} {o.get('home', '/home/' + a[0])}"]
        if k == 'authorized-key':
            key = ' '.join(a[1:]).replace('@PERSON_KEY@', self.person_key).split()
            return [f'authorized-key {a[0]} {key[0]} {key[1]}']
        if k == 'service':
            if len(a) >= 3 and a[1] in ('enabled', 'disabled'):
                return ['service ' + ' '.join(shlex.quote(x) for x in a)]
            text = a[1].encode().decode('unicode_escape')
            m = re.search(r'^ExecStart=(.*)$', text, re.M)
            if not m:
                raise NotExpressible(spec.text, 'no ExecStart= in the unit text')
            state = 'enabled' if 'enabled' in a[2:] else 'disabled'
            name = a[0][:-8] if a[0].endswith('.service') else a[0]
            return [f'service {name} {state} ' + ' '.join(shlex.quote(x) for x in shlex.split(m.group(1)))]
        if k == 'firewall':
            if len(a) == 1:
                name, text = firewall_name(a[0]), a[0]
            else:
                name, text = a[0], a[1]
            if not text.startswith('add '):
                text = 'add rule inet confos input ' + text
            return [f'rule {name} {shlex.quote(text)}']
        if k == 'setting':
            return [f'setting {a[0]} {shlex.quote(a[1])}']
        if k == 'script':
            path, sha = a[0], a[1]
            data = (CASES_DIR / 'declarations' / Path(path).name).read_bytes()
            if sha256_bytes(data) != sha:
                raise RunnerError(f'script {path}: checksum of cases/declarations differs')
            return file_line(path, '0755', data, 'the person\'s script from cases/declarations')
        if k == 'appimage':
            path, url, sha = a[0], a[1], a[2]
            data = self.fetch(url, sha)
            note = 'fetched; checksum computed at render time' if sha == '@SHA256@' else 'fetched and checked'
            return file_line(path, '0755', data, f'{note}: {url} sha256 {sha256_bytes(data)}')
        if k == 'download':
            path, url, sha = a[0], a[1], a[2]
            data = self.fetch(url, sha)
            member = spec.options().get('unpack')
            note = f'{url} sha256 {sha256_bytes(data)}'
            if member:
                with tarfile.open(fileobj=io.BytesIO(data)) as tf:
                    data = tf.extractfile(member).read()
                note += f', member {member}'
            return file_line(path, '0755', data, note)
        if k == 'built':
            path, source, command = a[0], a[1], a[2]
            if machine is not None or spec.text not in self.built:
                self.built[spec.text] = (self.build_on_machine(spec, machine) if machine is not None
                                         else self.build_on_host(spec))
            data, note = self.built[spec.text]
            return file_line(path, '0755', data, note)
        if k == 'sudo':
            rule = a[0]
            data = (rule + '\n').encode()
            return file_line('/etc/sudoers.d/cases-' + sha256_bytes(data)[:8], '0440', data, 'sudo rule')
        raise NotExpressible(spec.text, f'unknown spec kind {k}')

    def input_keys(self):
        try:
            self.input('none', 'none')
        except RunnerError:
            pass
        return list(self._inputs or {})

    def build_on_host(self, spec):
        path, source, command = spec.args[0], spec.args[1], spec.args[2]
        known = KNOWN_SOURCES.get(Path(source).name)
        if not known:
            raise NotExpressible(spec.text, 'the source of the program is not available to the renderer')
        src = self.fetch(*known)
        with tempfile.TemporaryDirectory(dir=self.cache) as d:
            (Path(d) / Path(source).name).write_bytes(src)
            argv = [x.replace(source, str(Path(d) / Path(source).name)).replace(path, str(Path(d) / 'out'))
                    for x in shlex.split(command)]
            start = utc()
            p = subprocess.run(argv, capture_output=True)
            if self.ev:
                self.ev.record('H', argv, start, utc(), p.returncode, p.stdout, p.stderr)
            if p.returncode:
                raise RunnerError('the build of the person\'s program failed on the host')
            cc = subprocess.run([argv[0], '--version'], capture_output=True, text=True).stdout.splitlines()[0]
            return (Path(d) / 'out').read_bytes(), f'built by the person from {known[0]} with {cc}'

    def build_on_machine(self, spec, machine):
        path, source, command = spec.args[0], spec.args[1], spec.args[2]
        code, out, err = machine.u(command, timeout=600)
        if code:
            raise StepFailed(f'the person\'s build command failed (exit {code})')
        code, out, err = machine.u('base64 -w0 ' + shlex.quote(path), timeout=120)
        if code:
            raise StepFailed('the built program could not be read back')
        return base64.b64decode(out), f'built by the person on the machine: {command}'

    # -- whole declaration
    def check_implemented(self, spec, lines):
        impl = IMPLEMENTED.get(self.base_version)
        if not impl:
            return
        for line in lines:
            f = shlex.split(line)
            if f[0] not in impl['kinds']:
                raise NotImplementedKind(spec.text, f'the kind `{f[0]}` is not implemented in ConfOS '
                                                    f'{self.base_version} (build/STATE.md); a line of it fails the '
                                                    f'whole application')
            if f[0] == 'file' and impl.get('file_prefixes') and not f[1].startswith(impl['file_prefixes']):
                raise NotImplementedKind(spec.text, f'a `file` target {f[1]} outside '
                                                    f'{", ".join(impl["file_prefixes"])} is refused by ConfOS '
                                                    f'{self.base_version} (build/DECLARATION.md)')
            if f[0] == 'setting':
                allowed = impl['settings']
                name = 'sysctl:' if f[1].startswith('sysctl:') else f[1]
                if name not in allowed or (allowed[name] is not None and f[2] not in allowed[name]):
                    raise NotImplementedKind(spec.text, f'the setting {f[1]}={f[2]} is not implemented in ConfOS '
                                                        f'{self.base_version} (build/STATE.md)')

    def render(self, declaration, machine=None, strict=False, machine_specs=None):
        """Render every spec. strict=False: NotExpressible / NotImplementedKind lines are recorded and left out
        (the D-test setup); strict=True: the first one is raised. machine_specs: the `built` specs that the person
        builds now on MACHINE (others reuse the earlier result)."""
        out = Rendered()
        self.homes = {}
        for sp in declaration.specs:
            if sp.kind == 'account':
                o = sp.options()
                if 'uid' in o and 'gid' in o:
                    self.homes[o.get('home', '/home/' + sp.args[0])] = (int(o['uid']), int(o['gid']))
        states = [s for s in declaration.specs if s.kind == 'archive-state']
        snapshot = states[0].args[0] if states else None
        for spec in declaration.specs:
            try:
                use = machine if (machine is not None and spec.text in (machine_specs or ())) else None
                lines = self.render_spec(spec, out, snapshot, use)
                self.check_implemented(spec, lines)
            except NotExpressible as e:
                if strict:
                    raise
                out.not_expressible.append([spec.text, f'{e.label}: {e.reason}'])
                for rel in list(out.files):
                    if rel not in {r for l in out.lines for r in shlex.split(l)}:
                        out.files.pop(rel)
                continue
            out.lines.extend(lines)
            out.line_of_spec[spec.text] = lines
        return out


class StepFailed(Exception):
    """A step of an ordinary action could not be performed on the machine."""


# ---------------------------------------------------------------- backends

class StockBackend:
    name = 'stock'
    firewall_fallback = None

    def __getattr__(self, attr):
        def unavailable(*a, **kw):
            raise NotAvailable(f'{attr}: no ConfOS operation on the stock image')
        return unavailable


class ConfosBackend:
    """ConfOS revision 1 through its documented interface only."""
    name = 'confos'
    # build/INTERFACE.md revision 3+: `sudo confos rules` runs the native read-only nftables query (build/confos,
    # rules(): /usr/sbin/nft list ruleset); the inventory uses it only when nft itself is refused to root
    firewall_fallback = 'confos rules'

    def __init__(self, source, apply_timeout=5400, reboot_timeout=900, status_timeout=180):
        self.source = Path(source)
        self.apply_timeout = apply_timeout
        self.reboot_timeout = reboot_timeout
        self.status_timeout = status_timeout

    def base_version(self):
        return (self.source / 'VERSION').read_text().strip()

    # -- clean installation
    def build_clean(self, rendered, directory, output, ev):
        """`./build.sh DECLARATION OUTPUT.qcow2` (build/INTERFACE.md) in our own copy of the published source."""
        decl = rendered.write(directory)
        # the host account's PATH may lack the system directories (depmod, mksquashfs live in /usr/sbin on Debian)
        env = dict(os.environ, PATH=os.environ.get('PATH', '/usr/bin:/bin') + ':/usr/local/sbin:/usr/sbin:/sbin')
        ev.note('build environment PATH=' + env['PATH'])
        code, out, err = ev.host([str(self.source / 'build.sh'), str(decl), str(output)], timeout=7200, env=env)
        work = Path(output).parent / (Path(output).stem + '.work')
        shutil.rmtree(work, ignore_errors=True)
        m = re.search(rb'^BUILT \S+ ([0-9a-f]{64})$', out, re.M)
        if code or not m:
            raise StepFailed(f'the clean build failed (exit {code})')
        digest = m.group(1).decode()
        if digest != rendered.sha256():
            raise StepFailed(f'the build reports {digest}, the declaration written is {rendered.sha256()}')
        return digest

    # -- the person writes the declaration
    def write(self, machine, rendered):
        """Write /state/declaration.conf and the content files beside it as root (file replacement)."""
        for rel, data in sorted(rendered.files.items()):
            target = '/state/' + rel
            want = file_sha(data)
            code, out, _ = machine.r(f'sha256sum {shlex.quote(target)} 2>/dev/null', timeout=600)
            if code == 0 and out.split()[:1] == [want.encode()]:
                continue  # the person's copy is already these bytes
            blob = data if isinstance(data, (bytes, bytearray)) else Path(data).read_bytes()
            code, _, _ = machine.r(f'mkdir -p {shlex.quote(str(Path(target).parent))} && '
                                   f'cat > {shlex.quote(target)}.new && mv {shlex.quote(target)}.new '
                                   f'{shlex.quote(target)}', stdin=blob, timeout=1800)
            if code:
                raise StepFailed(f'writing {target} as root failed (exit {code})')
        text = rendered.text()
        code, _, _ = machine.r(f'cat > {DECL_PATH}.new && mv {DECL_PATH}.new {DECL_PATH}', stdin=text)
        if code:
            raise StepFailed(f'writing {DECL_PATH} as root failed (exit {code})')
        code, out, _ = machine.r(f'sha256sum {DECL_PATH}')
        if code or out.split()[:1] != [rendered.sha256().encode()]:
            raise StepFailed('the declaration on the machine is not the bytes written')
        machine.written_sha = rendered.sha256()
        machine.written_text = text
        return rendered.sha256()

    def status(self, machine, record=True):
        code, out, err = machine.u('confos status', timeout=30, record=record)
        return code, out.decode(errors='replace').strip()

    def apply(self, machine, expected, cut=False, during=None):
        """APPLY of CASES.md: `sudo confos apply`, the reboot it makes, reconnect, `confos status`.

        cut=True: kill -9 of QEMU the instant `APPLIED EXPECTED` is read, then boot the same disk.
        during(machine, thread): called while the application runs (network loss cases).
        Returns a dict; 'applied' is True only when `confos status` printed exactly `APPLIED EXPECTED`."""
        ev = machine.ev
        res = {'expected': expected, 'cut': cut}
        old = machine.boot_id(record=True)
        res['old_boot_id'] = old
        holder = {}

        def go():
            holder['r'] = machine.r('confos apply', timeout=self.apply_timeout)

        t = threading.Thread(target=go, daemon=True)
        t.start()
        if during:
            during(machine, t)
        t.join()
        code, out, err = holder.get('r', (None, b'', b''))
        res['apply_exit'] = code
        text = out.decode(errors='replace')
        res['apply_stdout_tail'] = text[-2000:]
        rebooting = 'REBOOTING' in text or code == 255
        if not rebooting:
            bid = machine.boot_id(record=True)
            if bid == old and code != 0:
                res.update(applied=False, rebooted=False, reason=f'confos apply exited {code} before a reboot')
                c, s = self.status(machine)
                res['status'] = s
                return res
            if bid is None or bid != old:
                rebooting = True
        new = machine.wait_ssh(timeout=self.reboot_timeout, not_boot_id=old) if rebooting else old
        res['rebooted'] = rebooting
        res['new_boot_id'] = new
        if new is None:
            res.update(applied=False, reason='the machine did not answer after the reboot of the application')
            return res
        deadline = time.time() + self.status_timeout
        polls = 0
        status = ''
        while time.time() < deadline:
            polls += 1
            c, status = self.status(machine, record=False)
            if status == f'APPLIED {expected}':
                if cut:
                    machine.kill9()
                    res['cut_after_status'] = status
                break
            if status.startswith('APPLIED '):
                break
            time.sleep(0.2)
        ev.record('U', 'confos status (polled)', utc(), utc(), 0 if status.startswith('APPLIED') else 1,
                  status.encode() + b'\n', b'', {'polls': polls})
        res['status'] = status
        res['applied'] = status == f'APPLIED {expected}'
        if not res['applied']:
            res['reason'] = f'confos status printed {status!r}'
        if cut and res['applied']:
            machine.start()
            bid = machine.wait_ssh(timeout=self.reboot_timeout)
            res['after_cut_boot_id'] = bid
            if bid is None:
                res['after_cut'] = 'the machine did not answer after the power cut'
            else:
                c, s = self.status(machine)
                deadline = time.time() + self.status_timeout
                while not s.startswith('APPLIED') and time.time() < deadline:
                    time.sleep(1)
                    c, s = self.status(machine, record=False)
                res['after_cut_status'] = s
        return res

    # -- reading the declaration from outside
    def declaration_files_from_disk(self, machine, outdir):
        """Read /state/declaration.conf (partition 3) and the committed declaration of /system/current
        (partition 2) from the disk image with libguestfs, read-only (build/INTERFACE.md, Disk)."""
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        ev = machine.ev
        machine.r('sync')
        script = outdir / 'read-declaration.guestfish'
        script.write_text(
            'run\n'
            'mount-ro /dev/sda3 /\n'
            '-download /declaration.conf state-declaration.conf\n'
            'umount-all\n'
            'mount-ro /dev/sda2 /\n'
            '-download /current current\n'
            '-download /boot.cfg boot.cfg\n'
            'umount-all\n')
        code, out, err = ev.host(['guestfish', '--ro', '--format=qcow2', '-a', str(machine.disk), '-f', script.name], timeout=600, cwd=str(outdir))
        current = None
        if (outdir / 'boot.cfg').exists():
            # revision 5: `linux /generations/SHA256/vmlinuz ... confos.generation=SHA256`
            m = re.search(r'/generations/([0-9a-f]{64})/', (outdir / 'boot.cfg').read_text())
            current = m.group(1) if m else None
        elif (outdir / 'current').exists():
            current = (outdir / 'current').read_text().strip()
        if code or not current:
            raise RunnerError('the declaration could not be read from the disk: ' + err.decode(errors='replace'))
        script2 = outdir / 'read-generation.guestfish'
        script2.write_text('run\nmount-ro /dev/sda2 /\n'
                           f'download /generations/{current}/declaration.conf in-force.conf\n'
                           'umount-all\n')
        code, out, err = ev.host(['guestfish', '--ro', '--format=qcow2', '-a', str(machine.disk), '-f', script2.name], timeout=600, cwd=str(outdir))
        if code:
            raise RunnerError('the committed declaration could not be read: ' + err.decode(errors='replace'))
        result = {'current': current,
                  'in_force_sha256': hashlib.sha256((outdir / 'in-force.conf').read_bytes()).hexdigest()}
        sd = outdir / 'state-declaration.conf'
        result['state_sha256'] = hashlib.sha256(sd.read_bytes()).hexdigest() if sd.exists() else None
        return result

    def declaration_changed(self, machine, outdir):
        """DECL?: True if a declaration file differs from what the person (the runner) last wrote."""
        r = self.declaration_files_from_disk(machine, outdir)
        last = getattr(machine, 'written_sha', None) or getattr(machine, 'clean_sha', None)
        r['last_written'] = last
        r['changed'] = r['state_sha256'] != last or r['current'] != getattr(machine, 'in_force_sha', last)
        return r
