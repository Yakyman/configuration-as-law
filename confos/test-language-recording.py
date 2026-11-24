#!/usr/bin/python3
"""Guest regression for the pip/npm request recorders, including power cuts."""
import hashlib
import importlib.util
from pathlib import Path
import shlex
import shutil

spec = importlib.util.spec_from_file_location('durability', 'test-durability.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
d.IMAGE = d.HERE/'images/language-recording.qcow2'
d.UNIT = 'confos-language-recording-vm'
d.SERIAL = d.HERE/'logs/language-recording.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')


def digest():
    return d.guest('sha256sum /state/declaration.conf').split()[0]


def record(command):
    output = d.guest('sudo -n '+command)
    expected = digest()
    assert output == 'RECORDED '+expected+'; run confos apply', output
    return expected


def cut(expected):
    d.qmp('quit')
    d.stop()
    d.boot()
    d.wait_ready(expected)


def apply(expected):
    d.guest('sudo -n confos apply', check=False)
    d.wait_ready(expected)
    cut(expected)


def main():
    assert not d.IMAGE.exists()
    shutil.copyfile(d.HERE/f'images/confos-{d.VERSION}-clean.qcow2', d.IMAGE)
    initial = hashlib.sha256((d.HERE/'examples/development.conf').read_bytes()).hexdigest()
    try:
        d.boot()
        d.wait_ready(initial)
        packages = [shlex.split(line) for line in Path('language-packages.conf').read_text().splitlines() if line.strip()]
        baseline = record('apt-get install '+shlex.join([row[1]+'='+row[2] for row in packages]))
        apply(baseline)
        d.guest('pip --version; pip3 --version; npm --version; test ! -e /usr/lib/confos/native; '
                'test ! -L /usr/bin/pip3; test "$(readlink /usr/bin/npm)" = ../share/nodejs/npm/bin/npm-cli.js')
        for command in ('pip install cowsay', 'npm install -g cowsay',
                        'sudo -n pip install --target /tmp/pip-bypass cowsay',
                        'sudo -n npm install -g --prefix /tmp/npm-bypass cowsay',
                        'sudo -n python3 /usr/bin/pip3 install cowsay',
                        'sudo -n /usr/bin/pip3 install cowsay', 'sudo -n /usr/bin/npm install -g cowsay',
                        'sudo -n node /usr/share/nodejs/npm/bin/npm-cli.js install -g cowsay'):
            d.guest('if '+command+'; then exit 73; fi')
            assert digest() == baseline
        for kind, install, repeat, remove, check, absent in (
                ('pip', 'pip3 install --break-system-packages cowsay==6.1',
                 'python3 -m pip install cowsay', 'python3 -m pip uninstall -y cowsay',
                 'cowsay -t recorded-pip; python3 -m pip show cowsay',
                 'test ! -e /usr/local/bin/cowsay'),
                ('npm', 'npm install --global cowsay@1.6.0',
                 'npm install -g cowsay', 'npm uninstall --global cowsay',
                 'npm-cowsay recorded-npm; npm ls --prefix /opt/confos/npm/cowsay',
                 'test ! -e /usr/local/bin/npm-cowsay && test ! -e /opt/confos/npm/cowsay')):
            added = record(install)
            assert added != baseline
            d.guest("grep '^"+kind+" cowsay ' /state/declaration.conf")
            d.guest(absent)
            assert d.guest('confos status') == 'APPLIED '+baseline
            assert record(repeat) == added
            cut(baseline)
            assert digest() == added
            d.guest(absent)
            apply(added)
            d.guest(check)
            assert record(repeat) == added
            removed = record(remove)
            assert removed == baseline
            d.guest(check)
            assert d.guest('confos status') == 'APPLIED '+added
            assert record(remove) == baseline
            cut(added)
            assert digest() == baseline
            apply(baseline)
            d.guest(absent)
            print('PASS', kind, 'native/module entry, add/repeat/remove, pre-apply state, record/apply cuts', flush=True)
        print('LANGUAGE RECORDING GUEST PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
