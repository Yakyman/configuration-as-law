#!/usr/bin/python3 -I
"""Install the finite channel adapters and isolated inactive format parsers."""
import os,pathlib,shutil,subprocess
P=pathlib.Path
def write(path,text,mode=0o644):
    p=P(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);p.chmod(mode)
private=P('/usr/local/lib/stand/format-tools');private.mkdir(mode=0o700,exist_ok=True)
if not P('/usr/bin/ostree').is_symlink():
    shutil.move('/usr/bin/ostree',private/'ostree')
os.chmod(private/'ostree',0o700)
shutil.copyfile('/usr/bin/unsquashfs',private/'unsquashfs');os.chmod(private/'unsquashfs',0o700)
# The public manager cannot mutate a deployment, even when invoked directly as
# superuser. The private parser is an attached mandatory domain with only an
# inactive temporary output tree; it cannot deploy into a live root.
for name in ('ostree','flatpak','apt','apt-get','npm','pip','pip3','podman','corepack'):
    p=P('/usr/bin')/name
    if p.exists() or p.is_symlink():p.unlink()
    p.symlink_to('/usr/local/lib/stand/stand.py')
for name in ('/usr/libexec/flatpak-system-helper','/usr/lib/flatpak/flatpak-system-helper','/usr/share/nodejs/corepack'):
    p=P(name)
    if p.is_dir():shutil.rmtree(p)
    else:p.unlink(missing_ok=True)
subprocess.run(['/usr/bin/systemctl','mask','flatpak-system-helper.service'],check=True)
write('/etc/apparmor.d/stand-format-parser','''profile stand-format-parser /usr/local/lib/stand/format-tools/* {
  /usr/** r,
  /etc/** r,
  /lib/** r,
  /lib64/** r,
  /usr/lib/** m,
  /lib/** m,
  /lib64/** m,
  /proc/*/mountinfo r,
  /proc/*/mounts r,
  /proc/filesystems r,
  /proc/sys/kernel/random/boot_id r,
  /proc/*/status r,
  /dev/urandom r,
  /dev/null rw,
  /tmp/stand-flatpak-*/ rw,
  /tmp/stand-flatpak-*/** rwkl,
  /tmp/stand-appimage-*/ rw,
  /tmp/stand-appimage-*/** rwkl,
  signal (receive) peer=unconfined,
}
''')
write('/etc/apparmor.d/stand-build','''profile stand-build {
  /usr/** r,
  /etc/** r,
  /lib/** r,
  /lib64/** r,
  /usr/lib/** m,
  /lib/** m,
  /lib64/** m,
  /usr/bin/*gcc* ix,
  /usr/lib/gcc/** ix,
  /usr/libexec/gcc/** ix,
  /usr/bin/*as ix,
  /usr/bin/*ld* ix,
  /opt/stand/pkgs/*/src/input.c r,
  /var/lib/stand/stand-build-*/ rw,
  /var/lib/stand/stand-build-*/** rwk,
  /dev/null rw,
  /dev/urandom r,
  /proc/*/stat r,
  /proc/*/status r,
  /proc/meminfo r,
  /proc/sys/vm/overcommit_memory r,
  signal (send,receive) peer=stand-build,
  signal (receive) peer=unconfined,
}
''')
for profile in ('stand-format-parser','stand-build'):
    subprocess.run(['/usr/sbin/apparmor_parser','-r','-T','/etc/apparmor.d/'+profile],check=True)
print('Declaration frontends, inactive parser domain and fixed compiler domain installed')
