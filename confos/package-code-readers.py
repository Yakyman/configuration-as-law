#!/usr/bin/python3
"""Package original source-built code readers with fixed native paths and metadata."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

version, work_name, output_name = sys.argv[1:]
here = Path(__file__).resolve().parent
work = Path(work_name)
output = Path(output_name).resolve()
output.parent.mkdir(parents=True, exist_ok=True)
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='reader-package-', dir=output.parent) as temp:
    root = Path(temp)/'root'
    def copy(source, target, mode=0o644):
        p = root/target.lstrip('/')
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, p)
        p.chmod(mode)
        return p
    for source, target in [('bash/bash', 'bash'), ('python/python', 'python3.13'), ('perl/perl', 'perl'), ('busybox/busybox', 'busybox')]:
        executable = copy(work/source, '/usr/bin/'+target, 0o755)
        subprocess.run(['strip', '--strip-unneeded', executable], check=True)
    (root/'usr/bin/perl5.40.1').symlink_to('perl')
    # Debian builds several modules into its executable that upstream builds as
    # extensions (fcntl among them). Ship this build's matching extension set.
    extensions = sorted((work/'python/build').glob('lib.*/*.so'))
    if not any(p.name.startswith('fcntl.') for p in extensions):
        raise ValueError('Python build has no fcntl extension')
    for source in extensions:
        target = copy(source, '/usr/lib/python3.13/lib-dynload/'+source.name, 0o644)
        subprocess.run(['strip', '--strip-unneeded', target], check=True)
    copy(work/'python/Lib/importlib/_bootstrap_external.py', '/usr/lib/python3.13/importlib/_bootstrap_external.py')
    for source, label in [('bash/COPYING', 'bash'), ('python/LICENSE', 'python'),
                          ('perl/Copying', 'perl-gpl'), ('perl/Artistic', 'perl-artistic'),
                          ('busybox/LICENSE', 'busybox')]:
        copy(work/source, '/usr/share/doc/confos-code-readers/'+label+'-license')
    for name in ('code-file-policy.h', 'patch-bash-code.py', 'patch-python-code.py',
                 'patch-perl-code.py', 'patch-busybox-code.py', 'interpreter-source.sha256', 'busybox-source.sha256'):
        copy(here/name, '/usr/share/doc/confos-code-readers/'+name)
    control = root/'DEBIAN/control'
    control.parent.mkdir(parents=True)
    control.write_text('Package: confos-code-readers\nVersion: '+version+'\nArchitecture: amd64\n'
        'Maintainer: ConfOS project\nSection: interpreters\nPriority: required\n'
        'Replaces: bash, python3.13-minimal, libpython3.13-stdlib, perl-base, busybox-static\n'
        'Description: ConfOS Bash, Python, Perl and BusyBox code-input enforcement\n'
        ' Source-built Debian readers check opened code inputs in confined sessions.\n')
    for p in [*root.rglob('*'), root]:
        if p.is_dir(): p.chmod(0o755)
        elif not p.is_symlink() and not p.stat().st_mode & 0o111: p.chmod(0o644)
        os.utime(p, (epoch, epoch), follow_symlinks=False)
    artifact = Path(temp)/'payload.deb'
    subprocess.run(['dpkg-deb', '--root-owner-group', '--uniform-compression', '-Zgzip', '-z9',
                    '--build', root, artifact], check=True,
                    env=dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), TZ='UTC', LC_ALL='C'))
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    os.replace(artifact, output)
    output.with_suffix('.deb.sha256').write_text(digest+'\n')
    print(digest, output.name)
