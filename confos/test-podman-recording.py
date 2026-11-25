#!/usr/bin/python3
"""Guest OCI request recording with native run, removal and durable boundaries."""
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
d.IMAGE = d.HERE/'images/podman-recording.qcow2'
d.UNIT = 'confos-podman-recording-vm'
d.SERIAL = d.HERE/'logs/podman-recording.serial'
d.QMP = Path(str(d.SERIAL)+'.qmp')
name = 'docker.io/library/alpine:3.20.3'
declaration = Path('container-inputs/recorder-base.conf')
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
    base += ('package podman 5.4.2+ds1-2+b2\npackage uidmap 1:4.17.4-2\n'
             'package slirp4netns 1.2.1-1.1\npackage util-linux 2.41.5-0+deb13u1\n')
    declaration.write_text(base)
    shutil.copyfile('examples/recorded.sh', 'container-inputs/recorded.sh')
    baseline = hashlib.sha256(declaration.read_bytes()).hexdigest()
    try:
        subprocess.run(['./build.sh', str(declaration), str(d.IMAGE)], check=True)
        subprocess.run(['python3', 'compare-native-entries.py', 'images/podman-recording.work'], check=True)
        d.boot()
        d.wait_ready(baseline)
        for command in ('podman pull '+name, '/usr/bin/podman pull '+name,
                        'sudo -n /usr/bin/podman pull '+name,
                        'sudo -n podman --account root pull '+name,
                        'sudo -n podman pull alpine:3.20.3'):
            d.guest('if '+command+'; then exit 73; fi')
            assert digest() == baseline
        # 0.51: an account without recorded images, root included, has an empty list;
        # `image exists` answers from the declaration in force; an image that has no
        # /etc/mtab, /proc and /sys runs (the case party's X-REC-PODMAN on 0.43 ended
        # with status 126). First, so that a failure shows early.
        other = 'docker.io/library/busybox:1.36.1'
        d.guest('podman images; podman ps; sudo -n podman images; sudo -n podman ps')
        d.guest('if podman image exists '+other+'; then exit 73; fi')
        second = record('podman pull '+other)
        assert second != baseline
        d.guest('if podman image exists '+other+'; then exit 73; fi')
        # 0.55: between the recorded request and its application root's queries in JSON
        # form answer with the empty lists in force (up to 0.54 they ended with status 1).
        assert d.guest('sudo -n podman ps -a --format json') == '[]'
        assert d.guest('sudo -n podman images --format json') == '[]'
        apply(second)
        d.guest('podman image exists '+other+'; podman run --rm '+other+' true; '
                'test "$(podman run --rm '+other+' readlink /etc/mtab)" = /proc/mounts; '
                'podman run --rm '+other+' ls /proc/self/status /sys/kernel')
        assert record('podman rmi '+other) == baseline
        apply(baseline)
        d.guest('if podman image exists '+other+'; then exit 73; fi; podman images')
        print('PASS image without /etc/mtab, /proc and /sys runs; empty lists; image exists', flush=True)
        added = record('podman pull '+name)
        assert added != baseline
        d.guest("grep '^container user "+name+" ' /state/declaration.conf; test ! -e /usr/lib/confos/container-images; test ! -e /run/confos-container-ro")
        assert d.guest('confos status') == 'APPLIED '+baseline
        assert record('podman --account user pull '+name) == added
        cut(baseline)
        assert digest() == added
        apply(added)
        d.guest('podman images; podman image inspect '+name)
        assert d.guest('podman run --rm '+name+' cat /etc/alpine-release') == '3.20.3'
        assert record('podman pull '+name) == added
        removed = record('podman rmi '+name)
        assert removed == baseline
        d.guest('podman run --rm '+name+' cat /etc/alpine-release')
        assert record('podman --account user rmi '+name) == baseline
        cut(added)
        assert digest() == baseline
        apply(baseline)
        d.guest('test ! -e /run/confos-container-ro; test ! -e /usr/lib/confos/container-images; test ! -s /etc/subuid')
        d.guest('if podman run --rm '+name+' cat /etc/alpine-release; then exit 73; fi')
        print('PODMAN RECORDING GUEST PASS', flush=True)
    finally:
        d.stop()
        d.IMAGE.unlink(missing_ok=True)
        declaration.unlink(missing_ok=True)
        Path('container-inputs/recorded.sh').unlink(missing_ok=True)
        shutil.rmtree('images/podman-recording.work', ignore_errors=True)
if __name__ == '__main__':
    main()
