#!/usr/bin/python3 -I
import os,pathlib,subprocess,sys,shutil
P=pathlib.Path
sys.path.insert(0,'/usr/local/lib/stand')
from stand import atomic
subprocess.run(['/usr/bin/gcc','-O2','-Wall','-Wextra','/tmp/session.c','-static','-o','/usr/local/bin/stand-session'],check=True)
os.chmod('/usr/local/bin/stand-session',0o4755)
shutil.copy2('/usr/local/bin/stand-session','/usr/local/lib/stand/service-launch.new')
os.chmod('/usr/local/lib/stand/service-launch.new',0o755)
os.replace('/usr/local/lib/stand/service-launch.new','/usr/local/lib/stand/service-launch')
subprocess.run(['/usr/bin/gcc','-O2','-Wall','-Wextra','/tmp/shell.c','-static','-o','/usr/local/bin/stand-shell'],check=True)
os.chmod('/usr/local/bin/stand-shell',0o755)
subprocess.run(['/usr/sbin/usermod','-s','/usr/local/bin/stand-shell','stand'],check=True)
# Startup files are stored in a protected directory and are not used by the launcher.
for name in ('.bashrc','.profile','.bash_profile','.bash_login'):
    p=P('/home/stand')/name
    if p.exists():p.unlink()
key=P('/home/stand/.ssh/authorized_keys')
if key.exists():
    atomic('/etc/stand/authorized_keys',key.read_text());os.chmod('/etc/stand/authorized_keys',0o644);key.unlink()
atomic('/etc/stand/w3m.conf','use_cookie 0\nuse_mouse 0\nuse_external 0\n')
atomic('/etc/ssh/sshd_config.d/10-stand-session.conf','PermitUserEnvironment no\nMatch User stand\n    AuthorizedKeysFile /etc/stand/authorized_keys\n    PermitUserRC no\n    DisableForwarding yes\nMatch all\n')
atomic('/etc/sysctl.d/90-stand-code.conf','kernel.yama.ptrace_scope=2\n')
subprocess.run(['/usr/sbin/sysctl','-p','/etc/sysctl.d/90-stand-code.conf'],check=True)
# The interpreter runner and generated profile membership are explicit factory requirements.
print('Bash login, declaration-generated native policy and sealed compatibility launcher installed')
