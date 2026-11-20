#!/usr/bin/python3
"""Guest-only Landlock policy emitter; catalog is intentionally B-compatible."""
import glob,json,pathlib,subprocess,sys,os
D=json.load(open(sys.argv[1])); oldpath=pathlib.Path('/var/lib/cal/current.json')
old=json.loads(oldpath.read_text()) if oldpath.exists() else {}
if D['root'].get('system_update') and D['root'].get('system_update')!=old.get('root',{}).get('system_update'):
    subprocess.run(['apt-get','update'],check=True)
    subprocess.run(['apt-get','-y','upgrade'],check=True,env={**os.environ,'DEBIAN_FRONTEND':'noninteractive'})
for package in ('hello','figlet'):
    installed=subprocess.run(['dpkg-query','-W','-f=${db:Status-Status}',package],text=True,capture_output=True).stdout=='installed'
    if package in D['programs'] and not installed:
        candidates=list(pathlib.Path('/opt/cal-packages').glob(package+'_*.deb'))
        assert len(candidates)==1
        subprocess.run(['dpkg','-i',str(candidates[0])],check=True)
    elif package not in D['programs'] and installed: subprocess.run(['dpkg','--remove',package],check=True)
# Remove prior explicit executable mounts, then restore noexec data mounts.
mount_ledger=pathlib.Path('/etc/cal/x3-exec-mounts.json')
previous=json.loads(mount_ledger.read_text()) if mount_ledger.exists() else []
for target in reversed(previous):
    subprocess.run(['umount','--',target],check=True)
mount_ledger.write_text('[]')
subprocess.run(['mount','--make-rprivate','/'],check=True)
mountpoints={line.split()[4] for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines()}
for target in ['/home','/tmp','/var/tmp','/dev/shm','/var/lib/cal']:
    if target not in mountpoints: subprocess.run(['mount','--bind',target,target],check=True)
    subprocess.run(['mount','-o','remount,bind,noexec',target],check=True)
executable_mounts=[]
for user,allowed in D['allow_channels'].items():
    targets=[]
    if 'build' in allowed: targets.append('/home/'+user)
    if 'download' in allowed: targets += ['/home/'+user+'/downloaded','/tmp/downloaded']
    if 'appimage' in allowed: targets += glob.glob('/home/'+user+'/*.AppImage')
    for target in targets:
        if os.path.exists(target) and target not in executable_mounts:
            subprocess.run(['mount','--bind',target,target],check=True)
            subprocess.run(['mount','-o','remount,bind,exec',target],check=True)
            executable_mounts.append(target)
mount_ledger.write_text(json.dumps(executable_mounts))
tools='bash dash cat ls mkdir rmdir cp mv rm chmod touch date id sha256sum readlink head tail wc sort uniq tee printf env sleep true false timeout curl jq tar gzip unzip stat pwd dd tr'.split()
programs={'alpha':['/usr/local/lib/cal/alpha'],'beta':['/usr/local/lib/cal/beta'],'hello':['/usr/bin/hello'],'figlet':['/usr/bin/figlet'],'python':['/usr/bin/python3.11'],'node':['/usr/bin/node'],'browser':['/usr/bin/chromium','/usr/lib/chromium/chromium','/usr/lib/chromium/chrome_crashpad_handler']+['/usr/bin/'+s for s in 'dirname basename grep sed uname cut tr find xargs readlink getent expr'.split()]}
channels={'package':['/usr/bin/apt','/usr/bin/apt-get','/usr/bin/dpkg'],'pip':['/usr/bin/pip','/usr/bin/pip3','/usr/bin/python3.11'],'npm':['/usr/bin/npm','/usr/bin/node'],'flatpak':['/usr/bin/flatpak'],'appimage':['/home/*/*.AppImage'],'download':['/home/*/downloaded','/tmp/downloaded'],'build':['/usr/bin/gcc','/usr/bin/x86_64-linux-gnu-gcc-12','/usr/lib/gcc','/usr/bin/as','/usr/bin/ld','/home/USER'],'systemd':['/usr/bin/systemctl','/usr/bin/systemd-run','/usr/lib/systemd/systemd'],'cron':['/usr/bin/crontab'],'interpreter':['/usr/bin/python3.11','/usr/bin/node']}
def save(user,x,w):
    lines=['x '+str(pathlib.Path(p).resolve()) for p in sorted(x)]+['w '+p for p in w]
    target=pathlib.Path('/etc/cal/x3-'+user+'.rules');temp=target.with_suffix('.tmp');temp.write_text('\n'.join(lines)+'\n');temp.chmod(0o644);temp.replace(target)
for user in ('alice','bob'):
    x={'/usr/bin/'+t for t in tools}|{'/usr/local/bin/calctl','/lib64/ld-linux-x86-64.so.2'}
    for name,p in D['programs'].items():
        if p['scope']=='system' or user in p['owners']:x.update(programs[name])
    for name in D['allow_channels'].get(user,[]):
        for pattern in channels[name]:
            pattern=pattern.replace('USER',user)
            # No file need exist yet: the launcher resolves each rule at session start.
            x.update(glob.glob(pattern) if '*' in pattern else [pattern])
    w=['/home/'+user,'/tmp','/var/tmp','/dev/shm','/dev/null','/dev/zero','/dev/tty','/dev/pts','/var/lib/cal/active']
    if 'browser' in D['programs']:w+=['/proc']
    save(user,x,w)
save('root-worker',{'/usr/local/lib/cal/worker-body','/lib64/ld-linux-x86-64.so.2'},['/var/lib/cal/active','/dev/null','/dev/pts'])
print('X3 Landlock rules emitted; apply to NEW login sessions; build allows executable output in user home')
