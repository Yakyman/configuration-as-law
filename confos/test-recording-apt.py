#!/usr/bin/python3
"""Builder regression: explicit APT requests, unchanged applied state, durable apply."""
import hashlib
import importlib.util
from pathlib import Path
import shutil

spec = importlib.util.spec_from_file_location('durability', 'test-durability.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
d.IMAGE = d.HERE/'images/recording-apt.qcow2'
d.UNIT = 'confos-recording-apt-vm'
d.SERIAL = d.HERE/'logs/recording-apt.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')


def digest():
    return d.guest('sha256sum /state/declaration.conf').split()[0]


def cut(expected):
    d.qmp('quit')
    d.stop()
    d.boot()
    d.wait_ready(expected)


def record(command, expected):
    output = d.guest('sudo -n '+command)
    assert output == 'RECORDED '+expected+'; run confos apply', output
    assert digest() == expected


def main():
    assert not d.IMAGE.exists()
    shutil.copyfile(d.HERE/f'images/confos-{d.VERSION}-clean.qcow2', d.IMAGE)
    original = (d.HERE/'examples/development.conf').read_bytes()
    initial = hashlib.sha256(original).hexdigest()
    candidate = original+b'package tree 2.2.1-1\n'
    added = hashlib.sha256(candidate).hexdigest()
    try:
        d.boot()
        d.wait_ready(initial)
        d.guest('uname -r; dpkg-query -W linux-image-amd64; apt-get --version')
        d.guest('test ! -e /usr/bin/tree')
        for command in ('apt-get install tree', 'sudo -n apt-get install tree -o APT::Update::Post-Invoke::=false',
                        'sudo -n apt-get install tree=0.0-confos-missing',
                        'sudo -n apt-get remove bash',
                        'sudo -n /usr/bin/apt-get install tree', 'sudo -n /bin/apt install tree',
                        '/usr/bin/apt-get install tree'):
            d.guest('if '+command+'; then exit 71; fi')
            assert digest() == initial
            d.guest('test ! -e /usr/bin/tree')
        print('PASS unauthorized/unsupported/unavailable/base/native requests leave declaration and machine unchanged', flush=True)
        # From 0.49 every package file keeps its own path and bytes; the recording entries
        # are reached by name through /usr/local/bin.
        d.guest('test ! -e /usr/lib/confos/native && test ! -L /usr/bin/apt-get && test ! -L /usr/bin/apt '
                '&& test "$(readlink /usr/local/bin/apt-get)" = /usr/lib/confos/commands/apt-get '
                '&& test "$(command -v apt-get)" = /usr/local/bin/apt-get '
                '&& test "$(sudo -n sh -c "command -v apt-get")" = /usr/local/bin/apt-get')
        print('PASS package installer files in place; recording entry first in the ordinary and sudo paths', flush=True)
        for index, (install, remove) in enumerate((
                ('apt-get -y install tree=2.2.1-1', 'apt-get -y remove tree'),
                ('apt install -y tree', 'apt purge -y tree'),
                ('apt-get install tree:amd64=2.2.1-1', 'apt-get purge tree')), 1):
            record(install, added)
            d.guest('test ! -e /usr/bin/tree')
            assert d.guest('confos status') == 'APPLIED '+initial
            record(install, added)
            # Recorder success is durable even before application, without changing
            # the identity that status reports for the machine.
            cut(initial)
            assert digest() == added
            d.guest('test ! -e /usr/bin/tree')
            d.guest('sudo -n confos apply', check=False)
            d.wait_ready(added)
            cut(added)
            d.guest('/usr/bin/tree --version; dpkg-query -W tree')
            record(install, added)
            record(remove, initial)
            d.guest('/usr/bin/tree --version')
            assert d.guest('confos status') == 'APPLIED '+added
            record(remove, initial)
            cut(added)
            assert digest() == initial
            d.guest('sudo -n confos apply', check=False)
            d.wait_ready(initial)
            cut(initial)
            d.guest('test ! -e /usr/bin/tree; if tree --version; then exit 72; fi')
            print('PASS recorder add/removal, idempotence, pending/apply power cuts', index, flush=True)
        print('APT RECORDING PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
