"""Fallback native launch boundary. No interpreter or complete P4 claim."""
import pathlib,subprocess
PATHS=['/home','/tmp','/var/tmp','/dev/shm','/run']
def _run(*args):return subprocess.run(args,check=True,text=True,capture_output=True).stdout
def install_policy():
    for path in PATHS:
        pathlib.Path(path).mkdir(parents=True,exist_ok=True)
        if path in ('/tmp','/run','/dev/shm') and _run('/usr/bin/findmnt','-n','-o','FSTYPE','--target',path).strip()=='tmpfs':
            _run('/usr/bin/mount','-o','remount,size='+('1G' if path=='/tmp' else '256M'),path)
        if subprocess.run(['/usr/bin/mountpoint','-q',path]).returncode:
            _run('/usr/bin/mount','--bind',path,path)
        _run('/usr/bin/mount','-o','remount,bind,nosuid,nodev,noexec',path)
    return refresh_trust([],None)
def refresh_trust(rows,declaration_dir):
    mounts={}
    for path in PATHS:
        opts=_run('/usr/bin/findmnt','-n','-o','OPTIONS','--target',path).strip()
        if not {'noexec','nosuid','nodev'}.issubset(set(opts.split(','))):raise RuntimeError('missing mount gate '+path)
        mounts[path]=opts
    return {'mechanism':'noexec writable trees','mounts':mounts,'limitation':'file-read interpreters, memfd, anonymous code, other writable mounts, root backends remain open'}
