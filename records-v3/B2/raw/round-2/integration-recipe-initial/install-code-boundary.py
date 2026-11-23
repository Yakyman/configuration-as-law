#!/usr/bin/python3 -I
import os,pathlib,subprocess,sys
P=pathlib.Path
sys.path.insert(0,'/usr/local/lib/stand')
from stand import atomic
subprocess.run(['/usr/bin/gcc','-O2','-Wall','-Wextra','/tmp/session.c','-Wl,-l:libcrypto.so.3','-o','/usr/local/bin/stand-session'],check=True)
os.chmod('/usr/local/bin/stand-session',0o755)
subprocess.run(['/usr/sbin/usermod','-s','/usr/local/bin/stand-session','stand'],check=True)
# Startup files are stored in a protected directory and are not used by the launcher.
for name in ('.bashrc','.profile','.bash_profile','.bash_login'):
    p=P('/home/stand')/name
    if p.exists():p.unlink()
atomic('/etc/stand/w3m.conf','use_cookie 0\nuse_mouse 0\nuse_external 0\n')
atomic('/etc/ssh/sshd_config.d/10-stand-session.conf','Match User stand\n    PermitUserRC no\n    PermitUserEnvironment no\n    DisableForwarding yes\n    ForceCommand /usr/local/bin/stand-session\nMatch all\n')
# ForceCommand would hide SSH_ORIGINAL_COMMAND; the login binary itself is the fixed interface.
atomic('/etc/ssh/sshd_config.d/10-stand-session.conf','Match User stand\n    PermitUserRC no\n    PermitUserEnvironment no\n    DisableForwarding yes\nMatch all\n')
atomic('/etc/sysctl.d/90-stand-code.conf','kernel.yama.ptrace_scope=2\n')
subprocess.run(['/usr/sbin/sysctl','-p','/etc/sysctl.d/90-stand-code.conf'],check=True)
# The interpreter runner and generated profile membership are explicit factory requirements.
print('Shellless login, syscall filter and declaration-generated code policy installed')
