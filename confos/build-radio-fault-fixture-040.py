#!/usr/bin/python3
"""Private fault-injection derivative only; never replace canonical runtime package."""
from pathlib import Path
import shutil, subprocess as sp, runpy
root=Path.cwd();assert (root/'VERSION').read_text()=='0.40\n'
work=root/'radio-040-fault-source'
assert not work.exists(), 'inspect/remove previous fault source first'
work.mkdir()
# Source files are small. Large dependency input trees stay read-only references.
for source in root.iterdir():
    if source.is_file() and (source.suffix in ('.py','.sh','.json','.txt','.apparmor') or source.name in ('VERSION','confos','runtime-init','early-init','installer-chroot','apt-command','language-query','flatpak-command','podman-command','nft-query','systemctl-query','configuration-command')):
        shutil.copy2(source,work/source.name)
for name in runpy.run_path(str(root/'package-base.py'))['RUNTIME']:
    shutil.copy2(root/name,work/name)
for name in ('components','examples'): shutil.copytree(root/name,work/name)
for name in ('interpreter-inputs','appimage-inputs','flatpak-inputs'):
    if (root/name).exists(): (work/name).symlink_to(root/name,target_is_directory=True)
(work/'packages').mkdir()
for source in (root/'packages').iterdir():
    if source.name not in ('confos-runtime_0.40_all.deb','confos-runtime_0.40_all.deb.sha256'):
        (work/'packages'/source.name).symlink_to(source)
p=work/'runtime-init';s=p.read_text();anchor='[ -f /run/confos-radio-ready.json ] || exec /bin/bash\n';assert s.count(anchor)==1
inject='''# PRIVATE TEST ONLY: trusted fault injector, absent from canonical package.
(
 while [ ! -f /run/radio-fault-request ]; do sleep 1; done
 kill -KILL "$radio_pid" || exit 1
 echo "RADIO TRUSTED FAULT INJECTED $radio_pid"
) &
'''
p.write_text(s.replace(anchor,anchor+inject))
sp.run(['python3','package-base.py','packages/confos-runtime_0.40_all.deb'],cwd=work,check=True)
for kind in ('normal','systemd'):
    sp.run(['bash','build.sh',str(root/'radio-040-fixture'/(kind+'.conf')),str(root/'images'/('radio-040-fault-'+kind+'.qcow2'))],cwd=work,check=True)
print('PRIVATE FAULT IMAGES BUILT; canonical runtime untouched')
