#!/usr/bin/python3
"""Native Flatpak bundle recording, separate application, removal and power cuts."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess

spec = importlib.util.spec_from_file_location('durability', 'test-durability.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
d.IMAGE = d.HERE/'images/flatpak-recording.qcow2'
d.UNIT = 'confos-flatpak-recording-vm'
d.SERIAL = d.HERE/'logs/flatpak-recording.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')
runtime = 'runtime/org.freedesktop.Platform/x86_64/26.08'
application = 'app/io.mpv.Mpv/x86_64/stable'
declaration = Path('flatpak-inputs/recorder-base.conf')

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
    base = Path('examples/development.conf').read_text()
    base += ('package flatpak 1.16.6-1~deb13u3\n'
             'package gpg 2.4.7-21+deb13u1+b5\npackage gpg-agent 2.4.7-21+deb13u1+b5\n')
    runtime_hash = hashlib.sha256(Path('flatpak-inputs/runtime.flatpak').read_bytes()).hexdigest()
    base += f'flatpak {runtime} df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c {runtime_hash} runtime.flatpak\n'
    declaration.write_text(base)
    shutil.copyfile('examples/recorded.sh', 'flatpak-inputs/recorded.sh')
    baseline = hashlib.sha256(declaration.read_bytes()).hexdigest()
    try:
        subprocess.run(['./build.sh', str(declaration), str(d.IMAGE)], check=True)
        subprocess.run(['python3', 'compare-native-entries.py', 'images/flatpak-recording.work'], check=True)
        d.boot()
        d.wait_ready(baseline)
        with open('flatpak-inputs/mpv.flatpak', 'rb') as source:
            subprocess.run(['ssh', '-F', '/dev/null', '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
                '-i', 'private/login', '-p', '22406', 'user@127.0.0.1',
                'tee /home/user/mpv.flatpak >/dev/null'], stdin=source, check=True)
        for command in ('flatpak install --bundle /home/user/mpv.flatpak',
                        'sudo -n flatpak remote-add extra https://example.invalid/repo',
                        'sudo -n flatpak install flathub io.mpv.Mpv',
                        'sudo -n /usr/bin/flatpak install --bundle /home/user/mpv.flatpak'):
            d.guest('if '+command+'; then exit 73; fi')
            assert digest() == baseline
        added = record('flatpak install -y --system --bundle /home/user/mpv.flatpak')
        assert added != baseline
        d.guest("grep '^flatpak "+application+" ' /state/declaration.conf; test ! -e /usr/lib/confos/flatpak/app/io.mpv.Mpv")
        assert d.guest('confos status') == 'APPLIED '+baseline
        assert record('flatpak install --bundle /home/user/mpv.flatpak') == added
        cut(baseline)
        assert digest() == added
        apply(added)
        d.guest('flatpak info io.mpv.Mpv; flatpak run --command=mpv io.mpv.Mpv --version')
        assert record('flatpak install --bundle /home/user/mpv.flatpak') == added
        d.guest('if sudo -n flatpak uninstall org.freedesktop.Platform; then exit 73; fi')
        assert digest() == added
        removed = record('flatpak uninstall io.mpv.Mpv')
        assert removed == baseline
        d.guest('flatpak info io.mpv.Mpv')
        assert record('flatpak uninstall '+application) == baseline
        cut(added)
        assert digest() == baseline
        apply(baseline)
        d.guest('test ! -e /usr/lib/confos/flatpak/app/io.mpv.Mpv; flatpak info org.freedesktop.Platform')
        print('FLATPAK RECORDING GUEST PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)
        declaration.unlink(missing_ok=True)
        Path('flatpak-inputs/recorded.sh').unlink(missing_ok=True)
        shutil.rmtree('images/flatpak-recording.work', ignore_errors=True)

if __name__ == '__main__':
    main()
