#!/usr/bin/python3
"""Guest regression of 0.50: groupadd/groupdel and modprobe record lines; the queries
repaired in 0.50 answer. Every recorded request is repeated and followed by a power
cut; every application is followed by a power cut right after the report of success."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
spec = importlib.util.spec_from_file_location('durability', 'test-durability.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
native_guest = d.guest
def checked_guest(command, check=True):
    return native_guest('set -eu; '+command, check=check)
d.guest = checked_guest
d.IMAGE = d.HERE/'images/tools-050.qcow2'
d.UNIT = 'confos-tools-050-vm'
d.SERIAL = d.HERE/'logs/tools-050.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')
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
ABSENT = ("if getent group project; then exit 73; fi; test ! -d /sys/module/dummy; "
          "if grep -qw '^dummy' /proc/modules; then exit 73; fi; "
          "test \"$(id -nG user)\" = 'user wheel'")
def main():
    global active
    assert not d.IMAGE.exists()
    shutil.copyfile(d.HERE/f'images/confos-{d.VERSION}-clean.qcow2', d.IMAGE)
    base = (d.HERE/'examples/development.conf').read_bytes()
    active = baseline = hashlib.sha256(base).hexdigest()
    try:
        d.boot()
        d.wait_ready(active)
        assert d.guest('timedatectl show -p Timezone') == 'Timezone=UTC'
        assert d.guest('timedatectl show -p Timezone --value') == 'UTC'
        assert d.guest('timedatectl show --property=Timezone --value') == 'UTC'
        assert d.guest('systemctl is-enabled sleeper') == 'enabled'
        assert d.guest('systemctl is-active sleeper.service') == 'active'
        assert d.guest('systemctl is-enabled no-such-unit-050 || true') != 'enabled'
        print('PASS timezone and declared-service queries', flush=True)
        for command in ('groupadd project', 'groupdel wheel', 'modprobe dummy', 'modprobe -r virtio_net',
                        'sudo -n /usr/sbin/groupadd project', 'sudo -n /usr/sbin/modprobe dummy',
                        'sudo -n groupadd -r project', 'sudo -n modprobe dummy numdummies=3',
                        'sudo -n modprobe no_such_module_confos', 'sudo -n groupadd user',
                        'sudo -n usermod -aG project user'):
            d.guest('if '+command+'; then exit 73; fi')
            assert digest() == baseline
        d.guest(ABSENT)
        print('PASS unauthorized, full-path and unsupported requests record nothing and change nothing', flush=True)
        record('groupadd project')
        record('usermod -aG project user')
        record('modprobe dummy')
        d.guest("grep -qx 'group project 1001' /state/declaration.conf; "
                "grep -qx 'setting module:dummy loaded' /state/declaration.conf; "
                "grep -q '^account user 1000 1000 wheel,project ' /state/declaration.conf; "+ABSENT)
        print('PASS lines recorded; nothing in force before the application', flush=True)
        apply()
        d.guest("test \"$(getent group project)\" = 'project:x:1001:user'; id -nG user | grep -qw project; "
                "test -d /sys/module/dummy; grep -qw '^dummy' /proc/modules; "
                "test \"$(cat /etc/confos/modules.json)\" = '[\"dummy\"]'")
        print('PASS group, membership and module in force after the application and a power cut', flush=True)
        d.guest('if sudo -n groupdel project; then exit 73; fi')
        record('usermod -G wheel user')
        record('groupdel project')
        record('modprobe -r dummy')
        assert digest() == baseline
        d.guest("test \"$(getent group project)\" = 'project:x:1001:user'; test -d /sys/module/dummy")
        apply()
        d.guest(ABSENT+'; test ! -e /etc/confos/modules.json')
        print('PASS removal requests remove the lines and the things', flush=True)
        print('TOOLS 050 GUEST PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)
if __name__ == '__main__':
    main()
