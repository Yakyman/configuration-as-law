"""Finite native exec/map boundary for the v4 shell; not a text provenance monitor."""
from pathlib import Path
import re, os, signal, time, json

PAUSED=Path('/run/stand-shell-paused.json')

def process(pid):
    try:
        p=Path('/proc',str(pid))
        if (p/'attr/current').read_text().strip()!='stand-shell (enforce)':return None
        fields=(p/'stat').read_text().split(') ',1)[1].split()
        return (fields[19],fields[0]) if fields[0]!='Z' else None
    except (OSError,IndexError):return None

def pause():
    """Exclusive apply lock is held; new shell entries cannot pass their gate.

    Stop every existing shell-domain task before any realization change. The
    authorized sudo broker has already left this domain. pidfds prevent reuse
    while signaling; the durable identity list also permits watchdog recovery.
    """
    from stand import atomic, canonical
    known=json.loads(PAUSED.read_text()) if PAUSED.exists() else {}
    deadline=time.monotonic()+10
    while time.monotonic()<deadline:
        active=False
        for p in Path('/proc').iterdir():
            if not p.name.isdigit():continue
            info=process(p.name)
            if info is None:continue
            identity,state=info
            if state in ('T','t'):
                # Do not resume a task that was stopped before this transaction.
                continue
            active=True
            try:
                fd=os.pidfd_open(int(p.name))
                try:
                    if process(p.name)!=(identity,state):continue
                    known[p.name]=identity
                    atomic(PAUSED,canonical(known)+'\n',mode=0o600)
                    signal.pidfd_send_signal(fd,signal.SIGSTOP)
                finally:os.close(fd)
            except ProcessLookupError:pass
        if not active:return
        time.sleep(.01)
    raise RuntimeError('ordinary shell tasks did not quiesce')

def resume():
    """Only after successful publication or successful restoration."""
    if not PAUSED.exists():return
    known=json.loads(PAUSED.read_text())
    for pid,identity in known.items():
        try:
            fd=os.pidfd_open(int(pid))
            try:
                info=process(pid)
                if info and info[0]==identity:signal.pidfd_send_signal(fd,signal.SIGCONT)
            finally:os.close(fd)
        except ProcessLookupError:pass
    PAUSED.unlink()

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
