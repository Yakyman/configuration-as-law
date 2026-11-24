"""Finite native exec/map boundary for the v4 shell; not a text provenance monitor."""
from pathlib import Path
import re, os, select, time, json

PAUSED=Path('/run/stand-shell-paused.json')

def identity(pid):
    try:
        fields=Path('/proc',str(pid),'stat').read_text().rsplit(') ',1)[1].split()
        return (fields[19],fields[0]) if fields[0]!='Z' else None
    except (OSError,IndexError):return None

def process(pid):
    try:
        # Labels are per-thread. Freezing/migration is per process and therefore
        # covers every thread when any thread retains the ordinary domain.
        tasks=Path('/proc',str(pid),'task').iterdir()
        for task in tasks:
            try:
                if (task/'attr/current').read_text().strip()=='stand-shell (enforce)':
                    return identity(pid)
            except OSError:continue
    except OSError:pass
    return None

CGROUP=Path('/sys/fs/cgroup')
FREEZE_NAME='.stand-freeze'

def membership(pid):
    try:
        for line in Path('/proc',str(pid),'cgroup').read_text().splitlines():
            if line.startswith('0::'):
                value=line[3:]
                if not value.startswith('/') or '..' in value.split('/') or str(Path(value))!=value or value.endswith(' (deleted)'):
                    raise RuntimeError('invalid unified cgroup path')
                return value
    except OSError:pass
    return None

def members(group):
    try:return (CGROUP/group.lstrip('/')/'cgroup.procs').read_text().split()
    except FileNotFoundError:return []

def move(pid,target,expected_source,expected_start):
    # cgroup.procs is a numeric-PID API, not a pidfd API. Check both sides and
    # fail closed on an identity mismatch; this does not claim atomic migration.
    try:
        fd=os.pidfd_open(int(pid))
        try:
            info=identity(pid)
            if select.select([fd],[],[],0)[0] or info is None:return False
            if info[0]!=expected_start or membership(pid)!=expected_source:return False
            (CGROUP/target.lstrip('/')/'cgroup.procs').write_text(str(pid)+'\n')
            info=identity(pid)
            if info is None:return False
            if info[0]!=expected_start or membership(pid)!=target:
                raise RuntimeError('cgroup migration identity changed')
            return True
        finally:os.close(fd)
    except ProcessLookupError:return False

def frozen(group):
    try:return 'frozen 1' in (CGROUP/group.lstrip('/')/'cgroup.events').read_text().splitlines()
    except FileNotFoundError:return False

def pause():
    """Freeze shell-domain tasks without job-control stop notifications.

    A private child under each original cgroup preserves its resource ancestry.
    The exclusive apply lock and pending journal block new shell admission.
    Each destination is frozen before migration. Repeat the census after all
    freeze acknowledgements; raced sudo transitions return to the original
    group. No realization changes start until every shell task is frozen.
    """
    from stand import atomic, canonical
    state=json.loads(PAUSED.read_text()) if PAUSED.exists() else {'groups':{}}
    groups=state['groups']
    # A crash may occur before mkdir, or after one child was removed during
    # resume. An absent child contains no tasks; discard that completed entry.
    for original,child in list(groups.items()):
        directory=CGROUP/child.lstrip('/')
        if not directory.exists():
            del groups[original]
            atomic(PAUSED,canonical(state)+'\n',mode=0o600)
        else:(directory/'cgroup.freeze').write_text('1\n')
    deadline=time.monotonic()+10
    while time.monotonic()<deadline:
        for p in Path('/proc').iterdir():
            if not p.name.isdigit() or process(p.name) is None:continue
            original=membership(p.name)
            if original is None or original in groups.values():continue
            child=original.rstrip('/')+'/'+FREEZE_NAME
            directory=CGROUP/child.lstrip('/')
            if original not in groups:
                origin=CGROUP/original.lstrip('/')
                if original!='/' and (origin/'cgroup.type').read_text().strip()!='domain':
                    raise RuntimeError('threaded cgroup migration unsupported')
                if directory.exists():raise RuntimeError('unowned freezer child already exists')
                groups[original]=child
                # Recovery must know the destination before it can contain tasks.
                atomic(PAUSED,canonical(state)+'\n',mode=0o600)
            directory=CGROUP/child.lstrip('/')
            directory.mkdir(exist_ok=True)
            (directory/'cgroup.freeze').write_text('1\n')
            # A task may exit or cross into sudo between census and migration.
            # The next frozen-group census returns non-shell tasks to origin.
            info=process(p.name)
            if info is not None:move(p.name,child,original,info[0])
        if not all(frozen(group) for group in groups.values()):
            time.sleep(.01);continue
        for original,child in groups.items():
            for pid in members(child):
                info=identity(pid)
                if info and process(pid) is None:move(pid,original,child,info[0])
        # A migrated process cannot fork/exec after frozen=1. Once all ordinary
        # tasks are in acknowledged destinations, the census is stable.
        outside=any(process(p.name) is not None and membership(p.name) not in groups.values()
                    for p in Path('/proc').iterdir() if p.name.isdigit())
        if not outside and all(frozen(group) for group in groups.values()):return
        time.sleep(.01)
    raise RuntimeError('ordinary shell tasks did not quiesce')

def resume():
    """Return tasks to their original groups only after report/restoration.

    Moving out of a frozen group resumes execution without SIGCONT, so tasks
    that were already job-stopped remain job-stopped. The pending marker stays
    until every move is complete. Recovery can repeat an interrupted resume.
    """
    if not PAUSED.exists():return
    state=json.loads(PAUSED.read_text())
    for original,child in state['groups'].items():
        directory=CGROUP/child.lstrip('/')
        if not directory.exists():continue
        for pid in members(child):
            info=identity(pid)
            if info:move(pid,original,child,info[0])
        directory.rmdir()
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
