"""Finite native exec/map boundary for the v4 shell; not a text provenance monitor."""
from pathlib import Path
import re

def generate(files, mapped):
    # Immutable admission was checked by codeboundary.generate. AppArmor's ix
    # keeps descendants in the shell's effective write and executable policy.
    rules = ['profile stand-shell /usr/local/bin/stand-shell flags=(attach_disconnected) {',
        '  #include <abstractions/stand-map>',
        '  /** r,',
        '  /var/lib/stand/apply.lock rk,',
        '  /home/stand/ rw,', '  /home/stand/** rwkl,',
        '  /tmp/ rw,', '  /tmp/** rwkl,',
        '  /var/tmp/ rw,', '  /var/tmp/** rwkl,',
        '  /dev/shm/ rw,', '  /dev/shm/** rwkl,',
        '  /dev/null rw,', '  /dev/tty rw,', '  /dev/pts/* rw,',
        '  network inet stream,', '  network inet6 stream,',
        '  network inet dgram,', '  network inet6 dgram,', '  network unix,',
        '  signal (send,receive) peer=stand-shell,',
        '  signal (receive) peer=unconfined,',
        '  /usr/bin/sudo Ux,',
        '  /usr/local/bin/stand-session Px -> stand-session,']
    for path in sorted(files):
        f = files[path]
        if path in ('/usr/bin/sudo','/usr/local/bin/stand-session'): continue
        if not f['mode'] & 0o111 or f['mode'] & 0o6000: continue
        # Do not grant execution of private manager backends, privileged helpers
        # or a separate namespace/authority mechanism merely because it is base.
        if not f['mode'] & 0o001: continue
        if not re.fullmatch(r'/[a-zA-Z0-9_./:+,@=-]+',path): continue
        if path in mapped or path.startswith(('/opt/stand/pkgs/','/usr/local/lib/stand/')):
            rules.append('  "'+path+'" ix,')
    rules.append('}')
    return '\n'.join(rules)+'\n'
