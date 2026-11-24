#!/usr/bin/python3 -I
"""Install boot admission and supervisor recovery using existing PAM/systemd."""
import pathlib,subprocess,sys
sys.path.insert(0,'/usr/local/lib/stand')
from stand import atomic
P=pathlib.Path
atomic('/etc/systemd/system/stand-watchdog.service','''[Unit]
Description=Recover abandoned declaration transactions
[Service]
Type=oneshot
ExecStart=/usr/local/bin/stand-watchdog
TimeoutStartSec=300
''')
atomic('/etc/systemd/system/stand-watchdog.timer','''[Unit]
Description=Independent declaration silence watchdog
[Timer]
OnBootSec=10s
OnUnitActiveSec=5s
AccuracySec=1s
[Install]
WantedBy=timers.target
''')
P('/usr/local/bin/stand-watchdog').symlink_to('/usr/local/lib/stand/stand.py')
# Account checks precede session creation even while sshd is listening (the
# listener itself is a recorded runtime object verified during replay).
p=P('/etc/pam.d/common-account')
atomic(p,'account requisite pam_exec.so quiet /usr/bin/test -f /run/stand-ready\n'+p.read_text())
for unit in ('getty@.service','serial-getty@.service','systemd-user-sessions.service','systemd-logind.service'):
    atomic(P('/etc/systemd/system')/(unit+'.d')/'50-stand-replay.conf',
           '[Unit]\nRequires=stand-replay.service\nAfter=stand-replay.service\n')
subprocess.run(['/usr/bin/systemctl','daemon-reload'],check=True)
subprocess.run(['/usr/bin/systemctl','enable','--now','stand-watchdog.timer'],check=True)
print('PAM/launcher admission gate and independent watchdog installed')
