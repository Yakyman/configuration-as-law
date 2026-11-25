#!/usr/bin/python3
"""Text-level regression of the 0.50 recording requests (no machine): groupadd,
groupdel, modprobe, modprobe -r. The guest regression is test-tools-050.py."""
from pathlib import Path
import shlex
import configuration_recording as c

base = Path('examples/development.conf').read_bytes()


def rows(text):
    return [row for line in text.decode().splitlines() if (row := shlex.split(line, comments=True))]


def edit(text, tool, *arguments):
    return c.edit(text, rows(text), tool, list(arguments), {})


def refused(text, tool, *arguments):
    try:
        edit(text, tool, *arguments)
    except ValueError as error:
        print('REFUSED', tool, *arguments, '--', error)
        return
    raise AssertionError((tool, arguments))


one = edit(base, 'groupadd', 'project')
assert one == base+b'group project 1001\n', one[-60:]
assert edit(one, 'groupadd', 'project') == one
assert edit(one, 'groupadd', '-g', '1001', 'project') == one
refused(one, 'groupadd', '-g', '1002', 'project')
refused(base, 'groupadd', 'user')
refused(base, 'groupadd', 'wheel')
refused(base, 'groupadd', '-g', '1000', 'other')
refused(base, 'groupadd', '-r', 'other')
two = edit(one, 'groupadd', '-g', '2000', 'other')
assert two == one+b'group other 2000\n'
member = edit(two, 'usermod', '-aG', 'project', 'user')
assert b'account user 1000 1000 wheel,project /bin/bash /home/user\n' in member, member
refused(member, 'groupdel', 'project')
refused(base, 'usermod', '-aG', 'project', 'user')
assert edit(member, 'groupdel', 'other') == member.replace(b'group other 2000\n', b'')
back = edit(edit(member, 'usermod', '-G', 'wheel', 'user'), 'groupdel', 'project')
assert edit(back, 'groupdel', 'other') == base
assert edit(base, 'groupdel', 'project') == base
refused(base, 'groupdel', 'user')
commented = base+b'group project 1001  # shared work\n'
assert edit(commented, 'groupdel', 'project') == base+b'# shared work\n'

loaded = edit(base, 'modprobe', 'dummy')
assert loaded == base+b'setting module:dummy loaded\n', loaded[-60:]
assert edit(loaded, 'modprobe', 'dummy') == loaded
assert edit(loaded, 'modprobe', '-r', 'dummy') == base
assert edit(base, 'modprobe', '-r', 'dummy') == base
refused(base, 'modprobe', 'no_such_module_confos')
refused(base, 'modprobe', 'dummy', 'numdummies=2')
refused(base, 'modprobe', '-f', 'dummy')
refused(base, 'modprobe', '-a', 'dummy', 'loop')
try:
    c.validate(rows(base+b'setting module:dummy unloaded\n'))
except ValueError as error:
    print('REFUSED line', error)
else:
    raise AssertionError('invalid module value accepted')
print('CONFIGURATION EDIT 050 PASS')
