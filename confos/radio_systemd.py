"""Deterministic optional PID1 supervision for the declared radio runtime."""
from pathlib import Path

def configure(root):
    directory = Path(root)/'etc/confos/systemd-system'
    if not directory.is_dir():
        return
    service = directory/'confos-radio.service'
    if service.exists():
        raise ValueError('radio service ownership conflict')
    service.write_text('[Unit]\nDefaultDependencies=no\n[Service]\n'
        'Type=notify\nNotifyAccess=main\n'
        'ExecStart=/usr/bin/python3 /usr/lib/confos/radio_runtime.py\n'
        'AppArmorProfile=confos-radio\n'
        'Environment=PATH=/usr/bin:/usr/sbin LC_ALL=C.UTF-8\n'
        'KillMode=control-group\nTimeoutStartSec=120\nTimeoutStopSec=30\n'
        'ExecStopPost=/usr/bin/rm -f /run/confos-ready /run/confos-radio-ready.json /run/confos-radio.pid\n'
        'StandardOutput=tty\nStandardError=tty\nTTYPath=/dev/console\n')
    service.chmod(0o644)
    # BindsTo+After also stops a readiness task already running when the
    # supervisor dies; its StopPost then revokes any late readiness write.
    for unit in [directory/'confos-ready.service', *sorted(directory.glob('confos-user-*.service'))]:
        if not unit.is_file():
            raise ValueError('missing readiness unit: '+unit.name)
        dropin = directory/(unit.name+'.d')/'90-radio.conf'
        if dropin.exists():
            raise ValueError('radio dependency ownership conflict')
        dropin.parent.mkdir(exist_ok=True)
        text = '[Unit]\nBindsTo=confos-radio.service\nAfter=confos-radio.service\n'
        if unit.name == 'confos-ready.service':
            text += '[Service]\nExecStopPost=/usr/bin/rm -f /run/confos-ready\n'
        dropin.write_text(text)
        dropin.chmod(0o644)
