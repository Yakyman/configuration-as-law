#!/usr/bin/python3
"""Actual guest settings/account/service recording and durable boundaries."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
spec = importlib.util.spec_from_file_location('durability', 'test-durability.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
native_guest = d.guest
def checked_guest(command, check=True):
    return native_guest('set -eu; '+command, check=check)
d.guest = checked_guest
d.IMAGE = d.HERE/'images/configuration-recording.qcow2'
d.UNIT = 'confos-configuration-recording-vm'
d.SERIAL = d.HERE/'logs/configuration-recording.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')
folder = Path('configuration-recording-inputs')
active = None
def digest():
    return d.guest('sha256sum /state/declaration.conf').split()[0]
def cut():
    d.qmp('quit')
    d.stop()
    d.boot()
    d.wait_ready(active)
def record(command):
    before = d.guest('confos status')
    output = d.guest('sudo -n '+command)
    expected = digest()
    assert output == 'RECORDED '+expected+'; run confos apply', output
    assert d.guest('confos status') == before == 'APPLIED '+active
    assert d.guest('sudo -n '+command) == output
    assert digest() == expected
    cut()
    assert digest() == expected
    return expected
def apply():
    global active
    active = digest()
    d.guest('sudo -n confos apply', check=False)
    d.wait_ready(active)
    cut()
def main():
    global active
    assert not d.IMAGE.exists() and not folder.exists()
    folder.mkdir()
    base = Path('examples/development.conf').read_text()
    base += 'setting timezone UTC\n'
    for name in ('cases-tick.service', 'cases-tick.timer'):
        data = Path('test-inputs', name).read_bytes()
        (folder/name).write_bytes(data)
        base += f'user-unit user {name} disabled {hashlib.sha256(data).hexdigest()} {name}\n'
    (folder/'declaration.conf').write_text(base)
    shutil.copyfile('examples/recorded.sh', folder/'recorded.sh')
    active = baseline = hashlib.sha256(base.encode()).hexdigest()
    try:
        subprocess.run(['./build.sh', str(folder/'declaration.conf'), str(d.IMAGE)], check=True)
        subprocess.run(['python3', 'compare-native-entries.py', 'images/configuration-recording.work'], check=True)
        d.boot()
        d.wait_ready(active)
        for command in ('hostnamectl set-hostname forbidden',
                        'sysctl -w net.ipv4.ip_forward=1',
                        'systemctl enable sleeper',
                        'systemctl --user enable cases-tick.timer',
                        'sudo -n /usr/lib/confos/systemctl-query enable sleeper',
                        'sudo -n /usr/lib/confos/systemctl-query --user enable cases-tick.timer',
                        'sudo -n timedatectl set-timezone Asia/Tokyo',
                        # From 0.49 the package executables keep their own paths; called there
                        # directly they are refused and record nothing.
                        'sudo -n /usr/bin/hostnamectl set-hostname forbidden',
                        'sudo -n /usr/sbin/sysctl -w net.ipv4.ip_forward=1',
                        'sudo -n /usr/bin/systemctl enable sleeper',
                        'sudo -n /usr/sbin/useradd -m forbidden'):
            d.guest('if '+command+'; then exit 73; fi')
            assert digest() == baseline
        d.guest("test \"$(hostname)\" = confos-test; test \"$(cat /proc/sys/net/ipv4/ip_forward)\" = 0; if grep -q '^forbidden:' /etc/passwd; then exit 73; fi; test ! -e /usr/lib/confos/native")
        record('hostnamectl set-hostname configured')
        record('timedatectl set-timezone Etc/UTC')
        record("sysctl -w 'kernel.printk=3 4 1 7'")
        record('systemctl disable sleeper')
        record('systemctl --user enable cases-tick.timer')
        record('useradd -m extra')
        d.guest("test \"$(hostname)\" = confos-test; test \"$(cat /etc/timezone)\" = UTC; grep -q '^4' /proc/sys/kernel/printk; if grep -q '^extra:' /etc/passwd; then exit 73; fi; confos services | grep -Eq '^sleeper enabled [0-9]+$'; test ! -e /home/user/timer-fired")
        apply()
        d.guest("test \"$(hostname)\" = configured; test \"$(cat /etc/timezone)\" = Etc/UTC; test \"$(hostnamectl --static)\" = configured; test \"$(timedatectl show -p Timezone)\" = Timezone=Etc/UTC; test \"$(sysctl -n kernel.printk | cut -c1)\" = 3; grep -q '^3' /proc/sys/kernel/printk; grep '^extra:x:1001:1001:extra:/home/extra:/bin/bash$' /etc/passwd; test \"$(confos services)\" = 'sleeper disabled -'; systemctl --user is-enabled cases-tick.timer")
        for attempt in range(20):
            if d.guest('test -e /home/user/timer-fired && echo fired', check=False) == 'fired':
                break
            import time
            time.sleep(1)
        d.guest('test -e /home/user/timer-fired; grep -q confos-session /home/user/timer-profile')
        record('usermod -s /bin/sh extra')
        record('usermod -aG wheel extra')
        record('systemctl enable sleeper')
        record('systemctl --user disable cases-tick.timer')
        d.guest("grep '^extra:x:1001:1001:extra:/home/extra:/bin/bash$' /etc/passwd; test \"$(confos services)\" = 'sleeper disabled -'")
        apply()
        d.guest("grep '^extra:x:1001:1001:extra:/home/extra:/bin/sh$' /etc/passwd; id -nG extra | grep -qw wheel; confos services | grep -Eq '^sleeper enabled [0-9]+$'; test \"$(systemctl --user is-enabled cases-tick.timer)\" = disabled")
        record('userdel extra')
        record('hostnamectl set-hostname confos-test')
        record('timedatectl set-timezone UTC')
        record("sysctl -w 'kernel.printk=4 4 1 7'")
        assert digest() == baseline
        apply()
        d.guest("if grep -q '^extra:' /etc/passwd; then exit 73; fi; test \"$(hostname)\" = confos-test; test \"$(cat /etc/timezone)\" = UTC; grep -q '^4' /proc/sys/kernel/printk")
        print('CONFIGURATION RECORDING GUEST PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)
        shutil.rmtree('images/configuration-recording.work', ignore_errors=True)
        shutil.rmtree(folder, ignore_errors=True)
if __name__ == '__main__':
    main()
