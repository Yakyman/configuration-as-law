#!/usr/bin/env python3
"""Server-only stand image recipe; explicit invocation is required."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'build'
RAW = ROOT / 'raw'
LOG = None

def sanitize(text):
    text = text.replace(str(ROOT), '[stand-root]')
    text = text.replace(str(Path.home()), '[host-home]')
    return re.sub(r'/home/[^/\s]+', '[host-home]', text)

def record(text):
    text = sanitize(text)
    print(text, flush=True)
    if LOG:
        LOG.write(text + '\n')
        LOG.flush()

def run(args, *, data=None, output=None):
    record('RUN ' + Path(str(args[0])).name)
    result = subprocess.run([str(x) for x in args], cwd=ROOT, input=data,
                            stdout=output if output is not None else subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if output is None and result.stdout:
        record(result.stdout.decode(errors='replace'))
    if result.stderr:
        record(result.stderr.decode(errors='replace'))
    if result.returncode:
        raise RuntimeError(Path(str(args[0])).name + ' exited ' + str(result.returncode))
    return result.stdout

def lab(*args, script=None, output=None):
    return run([sys.executable, ROOT / 'lab.py', *args],
               data=script.encode() if isinstance(script, str) else script, output=output)

def verify_cache(cache):
    manifest = ROOT / 'downloads' / 'packages.sha256'
    files = sorted(cache.glob('*.deb'))
    if not files and not manifest.exists():
        return False
    if not files or not manifest.is_file():
        raise RuntimeError('incomplete package cache; require .deb files and packages.sha256')
    expected = {}
    for line in manifest.read_text().splitlines():
        fields = line.split()
        if len(fields) != 2 or not re.fullmatch('[a-f0-9]{64}', fields[0]):
            raise RuntimeError('invalid package checksum manifest')
        name = fields[1].removeprefix('*')
        if Path(name).name != name or not name.endswith('.deb') or name in expected:
            raise RuntimeError('unsafe or duplicate package checksum filename')
        expected[name] = fields[0]
    if set(expected) != {p.name for p in files}:
        raise RuntimeError('package cache membership differs from checksum manifest')
    for path in files:
        with path.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != expected[path.name]:
                raise RuntimeError('package checksum mismatch: ' + path.name)
    record('Verified all cached package checksums before bootstrap')
    return True

def scp_to_builder(path, destination='/tmp/stand-packages.tar'):
    info = json.loads((ROOT / 'vms/builder/meta.json').read_text())
    run(['scp', '-F', '/dev/null', '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes',
         '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
         '-o', 'GlobalKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
         '-i', ROOT / 'keys/guest', '-P', str(info['port']), path,
         'stand@127.0.0.1:'+destination])

def package_cache_export(cache):
    archive = ROOT / 'downloads/packages-export.tar'
    try:
        with archive.open('wb') as out:
            lab('run', 'builder', '--root', script='set -eu\ncd /var/cache/apt/archives\ntar -cf - -- *.deb\n', output=out)
        cache.mkdir(exist_ok=True)
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                if not member.isfile() or Path(member.name).name != member.name or not member.name.endswith('.deb'):
                    raise RuntimeError('unexpected package archive member')
            tar.extractall(cache, filter='data')
        lines = []
        for path in sorted(cache.glob('*.deb')):
            with path.open('rb') as stream:
                lines.append(hashlib.file_digest(stream, 'sha256').hexdigest() + '  ' + path.name)
        if not lines:
            raise RuntimeError('no package archives retained; cannot freeze reproducible package inputs')
        (ROOT / 'downloads/packages.sha256').write_text('\n'.join(lines) + '\n')
        verify_cache(cache)
    finally:
        archive.unlink(missing_ok=True)

def main():
    global LOG
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='store_true', help='confirm execution on the VM server')
    parser.add_argument('--replace', action='store_true', help='explicitly replace an existing frozen base')
    args = parser.parse_args()
    if not args.server:
        parser.error('--server is required; do not run heavy work on the laptop')
    if not Path('/dev/kvm').exists() or not os.access('/dev/kvm', os.R_OK | os.W_OK):
        raise RuntimeError('accessible KVM is required')
    if any((ROOT / 'vms').glob('*')):
        raise RuntimeError('existing VM directories must be destroyed before building or replacing the base')
    for name in ('base','downloads','keys','raw'):
        (ROOT / name).mkdir(exist_ok=True)
    base = ROOT / 'base/stand.qcow2'
    metadata = ROOT / 'base/stand.json'
    if (base.exists() or base.is_symlink() or metadata.exists()) and not args.replace:
        raise RuntimeError('existing base requires --replace; nothing overwritten')
    LOG = (RAW / 'recipe.log').open('a')
    cache = ROOT / 'downloads/packages'
    cached = verify_cache(cache)
    for binary in ('qemu-img','qemu-system-x86_64','systemd-run','ssh','scp','flock','cloud-localds','curl','ssh-keygen'):
        if not shutil.which(binary):
            raise RuntimeError('missing server prerequisite: ' + binary)
    record('Recipe started; no property outcome inferred from building')
    shutil.copy2(BUILD / 'lab.py', ROOT / 'lab.py')
    run(['sh', BUILD / 'fetch.sh'])
    run([sys.executable, BUILD / 'seed.py'])
    backup_base = ROOT / 'base/stand-previous.qcow2'
    backup_metadata = ROOT / 'base/stand-previous.json'
    if backup_base.exists() or backup_base.is_symlink() or backup_metadata.exists():
        raise RuntimeError('previous interrupted replacement artifacts require explicit recovery')
    if base.exists() or base.is_symlink():
        base.rename(backup_base)
    if metadata.exists():
        metadata.rename(backup_metadata)
    base.symlink_to('../downloads/source.qcow2')
    metadata.write_text(json.dumps({'system':'stand','transport':'ssh','user':'stand','key':'keys/guest',
        'qemu_args':['-drive','file=build/seed.iso,format=raw,if=virtio,readonly=on']}) + '\n')
    committed = False
    try:
        lab('new', 'builder', 'stand')
        lab('run', 'builder', '--root', script='set -eu\ncloud-init status --wait\n')
        bootstrap = (BUILD / 'bootstrap.sh').read_text()
        if cached:
            archive = BUILD / 'packages.tar'
            try:
                with tarfile.open(archive, 'w') as tar:
                    for path in sorted(cache.glob('*.deb')):
                        tar.add(path, arcname=path.name)
                    tar.add(ROOT / 'downloads/packages.sha256', arcname='packages.sha256')
                scp_to_builder(archive)
            finally:
                archive.unlink(missing_ok=True)
            prefix = '''#!/bin/bash
set -eu
mkdir -p /tmp/stand-packages
tar -xf /tmp/stand-packages.tar -C /tmp/stand-packages
cd /tmp/stand-packages
sha256sum -c packages.sha256
apt-get() {
  if [ "$1" = update ]; then return 0; fi
  /usr/bin/dpkg -i /tmp/stand-packages/*.deb
}
'''
        else:
            prefix = '''#!/bin/bash
set -eu
cat > /etc/apt/apt.conf.d/99stand-retain <<'EOF'
APT::Keep-Downloaded-Packages "true";
Binary::apt::APT::Keep-Downloaded-Packages "true";
#clear DPkg::Post-Invoke;
EOF
'''
        lab('run', 'builder', '--root', script=prefix + bootstrap)
        if not cached:
            package_cache_export(cache)
        with (RAW / 'package-versions.txt').open('wb') as out:
            lab('run','builder','--root', script="dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n'\n", output=out)
        source_files = ['stand.py','noexec.py','capture.py','selftest.py','policy.py','dev-inputs.py','install-noexec.sh','guard.py','install-guard.py','round1-selftest.py','codeboundary.py','codeverify.py','session.c','sha256.h','install-code-boundary.py','round2-selftest.py','round2-probe.c','transactions.py','inventory.py','round3-selftest.py','round3-inventory-test.py','install-transactions.py','normalize.py','language_channels.py','language-fixtures.py','language-native-fixture.py','language-selftest.py','app_channels.py','app-fixtures.py','app-selftest.py','system_channels.py','system-fixtures.py','system-selftest.py','import_channels.py','job_channels.py','install-channels.py','round4-selftest.py','../keys/host_ed25519','../keys/host_ed25519.pub']
        # External channel inputs are separately frozen; fetched only on server.
        run([sys.executable,BUILD/'language-fixtures.py',ROOT/'downloads/language'])
        run([sys.executable,BUILD/'system-fixtures.py','fetch',ROOT/'downloads/system'])
        runtime=ROOT/'downloads/channels/appimage-runtime';runtime.parent.mkdir(exist_ok=True)
        if not runtime.exists():run(['curl','--fail','--location','--output',runtime,'https://github.com/AppImage/type2-runtime/releases/download/continuous/runtime-x86_64'])
        if hashlib.sha256(runtime.read_bytes()).hexdigest()!='617aa77314d57c8b8e4fae9c3f0b35af7b30d5529cb69e98f64f92510ed98a46':raise RuntimeError('AppImage runtime checksum mismatch')
        archive=BUILD/'channel-inputs.tar'
        try:
            with tarfile.open(archive,'w') as tar:
                for folder,relative in [('language','language'),('system','system-inputs'),('channels','channels')]:
                    for path in sorted((ROOT/'downloads'/folder).iterdir()):
                        if path.is_file():tar.add(path,arcname=relative+'/'+path.name)
            scp_to_builder(archive,'/tmp/channel-inputs.tar')
        finally:archive.unlink(missing_ok=True)
        run([sys.executable, BUILD / 'deploy.py', *source_files])
        lab('run','builder','--root', script='''set -eu
install -m 755 /tmp/stand.py /tmp/noexec.py /tmp/capture.py /tmp/selftest.py /tmp/policy.py /tmp/guard.py /tmp/round1-selftest.py /tmp/codeboundary.py /tmp/codeverify.py /tmp/round2-selftest.py /tmp/round2-probe.c /tmp/transactions.py /tmp/inventory.py /tmp/round3-selftest.py /tmp/round3-inventory-test.py /usr/local/lib/stand/
install -m 755 /tmp/language_channels.py /tmp/language-selftest.py /tmp/app_channels.py /tmp/app-selftest.py /tmp/system_channels.py /tmp/system-selftest.py /tmp/import_channels.py /tmp/job_channels.py /tmp/round4-selftest.py /usr/local/lib/stand/
mkdir -p /usr/local/share/stand
tar -xf /tmp/channel-inputs.tar -C /usr/local/share/stand
/usr/bin/python3 -B /tmp/language-native-fixture.py /usr/local/share/stand/language
/usr/bin/python3 -B /tmp/dev-inputs.py
/usr/bin/python3 -B /tmp/app-fixtures.py
/usr/bin/python3 -B /tmp/system-fixtures.py catalog /usr/local/share/stand/system-inputs
rm -rf /usr/local/share/stand/system-inputs /tmp/channel-inputs.tar
rm -rf /tmp/stand-packages /tmp/stand-packages.tar
rm -f /etc/apt/apt.conf.d/99stand-retain
/usr/bin/python3 -I /tmp/install-guard.py
/usr/bin/python3 -I /tmp/install-channels.py
/usr/bin/python3 -I /tmp/install-code-boundary.py
/usr/bin/python3 -I /tmp/normalize.py
/usr/bin/python3 -I /tmp/install-transactions.py
sh /tmp/install-noexec.sh
rm -f /tmp/stand.py /tmp/noexec.py /tmp/capture.py /tmp/selftest.py /tmp/policy.py /tmp/dev-inputs.py /tmp/install-noexec.sh /tmp/guard.py /tmp/install-guard.py /tmp/round1-selftest.py /tmp/codeboundary.py /tmp/codeverify.py /tmp/round2-selftest.py /tmp/session.c /tmp/sha256.h /tmp/round2-probe.c /tmp/install-code-boundary.py /tmp/transactions.py /tmp/inventory.py /tmp/round3-selftest.py /tmp/round3-inventory-test.py /tmp/install-transactions.py /tmp/normalize.py
rm -f /tmp/language_channels.py /tmp/language-fixtures.py /tmp/language-native-fixture.py /tmp/language-selftest.py /tmp/app_channels.py /tmp/app-fixtures.py /tmp/app-selftest.py /tmp/system_channels.py /tmp/system-fixtures.py /tmp/system-selftest.py /tmp/import_channels.py /tmp/job_channels.py /tmp/install-channels.py /tmp/round4-selftest.py
sync
sha256sum /etc/stand/factory/machine.jsonl /etc/stand/factory/base-files.json /boot/initrd.img-*
''')
        lab('stop','builder')
        final = ROOT / 'base/stand-new.qcow2'
        if final.exists():
            raise RuntimeError('stand-new.qcow2 already exists; inspect interrupted build')
        run(['qemu-img','convert','-O','qcow2',ROOT / 'vms/builder/disk.qcow2',final])
        with final.open('rb') as stream:
            os.fsync(stream.fileno())
        final.chmod(0o444)
        final.replace(base)
        metadata.write_text(json.dumps({'system':'stand','transport':'ssh','user':'stand','key':'keys/guest','operator_user':'root'}) + '\n')
        lab('destroy','builder')
        committed = True
        backup_base.unlink(missing_ok=True)
        backup_metadata.unlink(missing_ok=True)
        record('Frozen standalone stand image built; package cache retained; property tests are separate')
    finally:
        if not committed:
            if (ROOT / 'vms/builder').exists():
                try:
                    lab('stop','builder')
                except Exception:
                    lab('kill','builder')
                lab('destroy','builder')
            base.unlink(missing_ok=True)
            metadata.unlink(missing_ok=True)
            if backup_base.exists() or backup_base.is_symlink():
                backup_base.rename(base)
            if backup_metadata.exists():
                backup_metadata.rename(metadata)
            (ROOT / 'base/stand-new.qcow2').unlink(missing_ok=True)
        for name in ('seed.iso','user-data','meta-data','packages.tar'):
            (BUILD / name).unlink(missing_ok=True)
        (ROOT / 'downloads/source.qcow2').unlink(missing_ok=True)
        (ROOT / 'downloads/source.qcow2.part').unlink(missing_ok=True)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        record('BUILD FAILED: ' + str(error))
        raise SystemExit(1)
