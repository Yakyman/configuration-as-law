#!/usr/bin/python3 -I
"""Install broker authority and remove caller access to original backends."""
import glob,json,os,pathlib,subprocess,sys
sys.path.insert(0,'/usr/local/lib/stand')
from guard import FRONTENDS
P=pathlib.Path
def write(path,text,mode=0o644):
    p=P(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);p.chmod(mode)
def call(*args):subprocess.run(args,check=True)

# The host-held operator key is external laboratory access, never an ordinary sudo grant.
P('/root/.ssh').mkdir(mode=0o700,exist_ok=True)
write('/root/.ssh/authorized_keys',P('/home/stand/.ssh/authorized_keys').read_text(),0o600)
write('/etc/ssh/sshd_config.d/00-stand.conf','PasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin prohibit-password\n')
call('/usr/sbin/usermod','-G','','stand')
for p in P('/etc/sudoers.d').iterdir():
    if p.is_file() and p.name!='README':p.unlink()
commands=', '.join('/usr/local/bin/'+n for n in FRONTENDS)
write('/etc/sudoers.d/stand','Defaults:stand env_reset, !setenv, secure_path="/usr/local/bin:/usr/bin:/usr/sbin"\nstand ALL=(root) NOPASSWD: NOSETENV: '+commands+'\n',0o440)
call('/usr/sbin/visudo','-cf','/etc/sudoers')
for name in FRONTENDS+['stand-replay']:
    p=P('/usr/local/bin')/name;p.unlink(missing_ok=True);p.symlink_to('/usr/local/lib/stand/stand.py')

# No automatic per-user manager or cron/at scheduler reads caller-controlled trees.
for name in ('user@.service','cron.service','atd.service'):
    subprocess.run(['/usr/bin/systemctl','mask',name],check=True)
write('/etc/cron.allow','root\n',0o600);write('/etc/at.allow','root\n',0o600)
for path in ('/var/spool/cron','/var/spool/cron/crontabs','/var/spool/cron/atjobs','/var/spool/cron/atspool'):
    P(path).mkdir(parents=True,exist_ok=True);P(path).chmod(0o700)

# Deny methods, not replies/signals. An explicit user rule wins over defaults.
# Read-only calls use stand-verify; broker/root services retain their bus access.
destinations=['org.freedesktop.systemd1','org.freedesktop.NetworkManager','org.bluez',
              'org.freedesktop.Accounts','org.freedesktop.hostname1','org.freedesktop.timedate1',
              'org.freedesktop.resolve1','org.freedesktop.network1','org.freedesktop.login1',
              'org.freedesktop.PolicyKit1','org.freedesktop.PackageKit']
rules='\n'.join('<deny send_destination="'+d+'" send_type="method_call"/>' for d in destinations)
text='<busconfig>\n<policy context="default">\n'+rules+'\n</policy>\n<policy user="root">\n'
text+='\n'.join('<allow send_destination="'+d+'"/>' for d in destinations)+'\n</policy>\n'
text+='<policy user="stand">\n'+rules+'\n</policy>\n</busconfig>\n'
write('/etc/dbus-1/system.d/zz-stand.conf',text)
write('/etc/polkit-1/rules.d/00-stand.rules','polkit.addRule(function(action, subject) { if (subject.user != "root") return polkit.Result.NO; });\n')

# Read AND execute denial prevents the original inode being copied or run by a loader.
names=('apt apt-get apt-cache apt-config apt-mark apt-key dpkg dpkg-deb dpkg-split dpkg-trigger dpkg-divert dpkg-statoverride '
       'update-alternatives useradd usermod userdel groupadd groupmod groupdel adduser deluser addgroup delgroup '
       'chfn chsh chage passwd gpasswd newgrp sg su runuser chpasswd newusers vipw vigr '
       'systemctl systemd systemd-run systemd-analyze systemd-mount systemd-umount run0 loginctl machinectl '
       'crontab cron at atq atrm batch atd nmcli nmtui nft iptables ip6tables iptables-restore '
       'bluetoothctl btmgmt hciconfig hcitool rfcomm pkexec mount umount').split()
paths=set()
for name in names:
    for prefix in ('/usr/bin','/usr/sbin','/usr/lib/systemd'):
        p=P(prefix)/name
        if p.exists() and p.is_file():paths.add(p.resolve())
for pattern in ('/usr/bin/dpkg-*','/usr/sbin/dpkg-*','/usr/bin/apt-*','/usr/bin/debconf*','/usr/sbin/debconf*','/usr/lib/dpkg','/usr/lib/apt','/usr/share/perl5/Dpkg*','/usr/share/debconf','/usr/lib/python3/dist-packages/apt*',
                '/usr/lib/*/libapt-pkg.so*','/usr/lib/*/libapt-private.so*'):
    for name in glob.glob(pattern):paths.add(P(name).resolve())
paths.discard(P('/usr/bin/dpkg-query'))
for p in paths:
    os.chown(p,0,0);p.chmod(0o700)
for path in ('/var/cache/apt/archives','/var/lib/stand/generations'):
    P(path).mkdir(parents=True,exist_ok=True);P(path).chmod(0o700)
write('/etc/stand/backend-paths.json',json.dumps(sorted(map(str,paths)),indent=2)+'\n')
call('/usr/bin/systemctl','daemon-reload')
call('/usr/bin/systemctl','reload','dbus')
call('/usr/bin/systemctl','reload','ssh')
print('Broker authority, backend DAC, bus policy and scheduler removal installed')
