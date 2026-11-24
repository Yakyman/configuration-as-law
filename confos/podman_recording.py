"""Record an explicit OCI image request without loading the active store."""
import fcntl
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tarfile
import tempfile

NATIVE = '/usr/bin/podman'
HEX = re.compile(r'[0-9a-f]{64}')
ACCOUNT = re.compile(r'[a-z_][a-z0-9_-]*')
IMAGE = re.compile(r'(?P<registry>[a-z0-9]+(?:[.-][a-z0-9]+)*(?::[0-9]+)?)/[a-z0-9]+(?:[._-][a-z0-9]+)*(?:/[a-z0-9]+(?:[._-][a-z0-9]+)*)*(?::[a-z0-9_][a-z0-9_.-]*)?')

def request(arguments, sudo_user=None):
    args = list(arguments)
    account = None
    if '--account' in args:
        if args.count('--account') != 1:
            raise ValueError('exactly one --account is supported')
        index = args.index('--account')
        if index+1 >= len(args):
            raise ValueError('--account requires a declared ordinary account')
        account = args[index+1]
        del args[index:index+2]
    if len(args) != 2 or args[0] not in ('pull', 'rmi'):
        raise ValueError('supported: [--account USER] pull/rmi REGISTRY/NAME[:TAG]')
    match = IMAGE.fullmatch(args[1])
    if not match or not ('.' in match['registry'] or ':' in match['registry'] or match['registry'] == 'localhost'):
        raise ValueError('image must be fully qualified; transports, digests and other options are unsupported')
    name = args[1]
    if ':' not in name.rsplit('/', 1)[-1]:
        name += ':latest'
    account = account or sudo_user
    if not account or not ACCOUNT.fullmatch(account) or account == 'root':
        raise ValueError('root requires --account USER or a validated ordinary sudo-origin account')
    return args[0], account, name

def account_check(rows, account):
    matches = [r for r in rows if r[0] == 'account' and r[1] == account]
    if len(matches) != 1 or not 1 <= int(matches[0][2]) <= 60000:
        raise ValueError('container target must be one declared ordinary account with UID <= 60000')

def validate_oci(data, expected_name=None):
    """Verify original archive blobs without extracting paths or running code."""
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        members = {}
        for member in archive.getmembers():
            name = member.name.rstrip('/')
            if name in members or name.startswith('/') or '..' in Path(name).parts or not (member.isfile() or member.isdir()):
                raise ValueError('unsafe or duplicate OCI archive member')
            members[name] = member
        def read(name):
            member = members.get(name)
            if member is None or not member.isfile():
                raise ValueError('missing OCI object: '+name)
            return archive.extractfile(member).read()
        if json.loads(read('oci-layout')).get('imageLayoutVersion') != '1.0.0':
            raise ValueError('unsupported OCI layout')
        index = json.loads(read('index.json'))
        if index.get('schemaVersion') != 2 or len(index.get('manifests', [])) != 1:
            raise ValueError('require one OCI image manifest')
        def blob(descriptor):
            digest = descriptor.get('digest', '')
            if not digest.startswith('sha256:') or not HEX.fullmatch(digest[7:]):
                raise ValueError('require SHA256 OCI descriptors')
            value = read('blobs/sha256/'+digest[7:])
            if hashlib.sha256(value).hexdigest() != digest[7:] or descriptor.get('size') != len(value):
                raise ValueError('OCI descriptor hash/size mismatch')
            return value
        descriptor = index['manifests'][0]
        if expected_name is not None and descriptor.get('annotations', {}).get('org.opencontainers.image.ref.name') != expected_name:
            raise ValueError('OCI archive name differs from the requested image')
        if descriptor.get('mediaType') != 'application/vnd.oci.image.manifest.v1+json':
            raise ValueError('require an OCI image manifest')
        manifest = json.loads(blob(descriptor))
        if manifest.get('schemaVersion') != 2 or manifest['config'].get('mediaType') != 'application/vnd.oci.image.config.v1+json':
            raise ValueError('unsupported OCI image configuration')
        config = json.loads(blob(manifest['config']))
        if config.get('os') != 'linux' or config.get('architecture') != 'amd64':
            raise ValueError('require Linux amd64 image')
        layers = manifest.get('layers', [])
        diff_ids = config.get('rootfs', {}).get('diff_ids', [])
        if config.get('rootfs', {}).get('type') != 'layers' or len(layers) != len(diff_ids):
            raise ValueError('inconsistent OCI layer configuration')
        for layer, diff_id in zip(layers, diff_ids):
            raw = blob(layer)
            media = layer.get('mediaType')
            if media == 'application/vnd.oci.image.layer.v1.tar+gzip':
                raw = gzip.decompress(raw)
            elif media != 'application/vnd.oci.image.layer.v1.tar':
                raise ValueError('unsupported layer encoding; require tar or gzip')
            if 'sha256:'+hashlib.sha256(raw).hexdigest() != diff_id:
                raise ValueError('OCI uncompressed layer hash mismatch')
        return manifest['config']['digest'][7:]

def private_native(directory):
    directory = directory.resolve()
    env = {'PATH': '/usr/bin:/usr/sbin:/bin', 'HOME': str(directory/'home'),
           'XDG_CONFIG_HOME': str(directory/'config'), 'XDG_RUNTIME_DIR': str(directory/'run'),
           'TMPDIR': str(directory/'images-tmp'), 'LC_ALL': 'C.UTF-8',
           'CONTAINERS_CONF': str(directory/'containers.conf'), 'REGISTRY_AUTH_FILE': str(directory/'auth.json')}
    command = [NATIVE, '--root', str(directory/'store'), '--runroot', str(directory/'run/store'),
        '--tmpdir', str(directory/'tmp'), '--storage-driver', 'vfs', '--cgroup-manager', 'cgroupfs',
        '--events-backend', 'none', '--hooks-dir', str(directory/'hooks'),
        '--network-config-dir', str(directory/'networks'), '--volumepath', str(directory/'volumes')]
    def native(args):
        result = subprocess.run([*command, *args], env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=240)
        if result.returncode:
            raise ValueError('private Podman request failed:\n'+result.stdout+result.stderr)
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        return result.stdout.strip()
    return native

def prepare(name, directory):
    directory = directory.resolve()
    for sub in ('home', 'config', 'run', 'store', 'tmp', 'images-tmp', 'hooks', 'networks', 'volumes'):
        (directory/sub).mkdir(mode=0o700)
    (directory/'auth.json').write_text('{}\n')
    (directory/'containers.conf').write_text('[engine]\nruntime="crun"\n')
    native = private_native(directory)
    try:
        native(['pull', '--platform', 'linux/amd64', '--tls-verify=true', '--authfile', str(directory/'auth.json'), name])
        image_id = native(['image', 'inspect', '--format', '{{.Id}}', name]).removeprefix('sha256:')
        if not HEX.fullmatch(image_id):
            raise ValueError('unexpected native image configuration identity: '+repr(image_id))
        archive = directory/'image.oci.tar'
        native(['save', '--format', 'oci-archive', '--output', str(archive), name])
        data = archive.read_bytes()
        saved_id = validate_oci(data, name)
        if saved_id != image_id:
            raise ValueError('saved OCI config '+saved_id+' differs from requested native image '+image_id)
        return image_id, data
    finally:
        # Native documented migrate retires the rootless pause namespace too.
        # This command has precisely the same private roots and environment.
        try:
            native(['rmi', '--all'])
        finally:
            native(['system', 'migrate'])

def existing(rows, account, name, declaration):
    matches = [r for r in rows if r[:3] == ['container', account, name]]
    if len(matches) > 1:
        raise ValueError('duplicate container identity')
    if not matches:
        return None
    row = matches[0]
    source = Path(row[5])
    if source.is_absolute() or '..' in source.parts:
        raise ValueError('existing container source escapes declaration directory')
    path = declaration.parent/source
    if not path.resolve().is_relative_to(declaration.parent.resolve()):
        raise ValueError('existing container source resolves outside declaration directory')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != row[4] or validate_oci(data, name) != row[3]:
        raise ValueError('existing container archive identity mismatch')
    return row[3], data

def edit(original, account, name, prepared):
    import language_recording
    replacement = None
    if prepared is not None:
        config, data = prepared
        replacement = ['container', account, name, config, hashlib.sha256(data).hexdigest(),
                       language_recording.input_name('image.oci.tar', data)]
    output, found = [], False
    for line in original.decode().splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        if row[:3] == ['container', account, name]:
            if found:
                raise ValueError('duplicate container identity')
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

def record(arguments, sudo_user=None):
    import assemble
    import language_recording
    import recording
    if os.geteuid() != 0:
        raise ValueError('permission denied: this account may not change /state/declaration.conf; use an authorized root invocation')
    operation, account, name = request(arguments, sudo_user)
    with open('/run/confos-apply.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        declaration = recording.DECLARATION
        if declaration.is_symlink():
            raise ValueError('declaration must be a regular primary text file')
        original = declaration.read_bytes()
        with tempfile.TemporaryDirectory(prefix='confos-podman-record-', dir='/run') as temporary:
            directory = Path(temporary)
            capture = directory/'declaration.conf'
            capture.write_bytes(original)
            rows, _ = assemble.parse(capture)
            account_check(rows, account)
            prepared = None
            if operation == 'pull':
                prepared = existing(rows, account, name, declaration)
                if prepared is not None:
                    # Preserve manual source paths/comments and stable existing pins.
                    with language_recording.input_transaction(declaration, original, {}):
                        with (declaration.parent/next(r[5] for r in rows if r[:3] == ['container', account, name])).open('rb') as stream:
                            os.fsync(stream.fileno())
                        folder = Path(stream.name).parent
                        while True:
                            fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY)
                            try:
                                os.fsync(fd)
                            finally:
                                os.close(fd)
                            if folder == declaration.parent:
                                break
                            folder = folder.parent
                        recording.commit(declaration, original, original)
                    return
                workspace = directory/'resolver'
                workspace.mkdir()
                prepared = prepare(name, workspace)
            candidate = edit(original, account, name, prepared)
            capture.write_bytes(candidate)
            assemble.parse(capture)
            inputs = {} if prepared is None else {name: (prepared[0], 'image.oci.tar', prepared[1])}
            with language_recording.input_transaction(declaration, candidate, inputs):
                recording.commit(declaration, original, candidate)
