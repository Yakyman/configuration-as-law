#!/usr/bin/python3
import json, pathlib, subprocess, sys
doc=json.load(open(sys.argv[1]))
oldpath=pathlib.Path('/var/lib/cal/current.json')
old=json.loads(oldpath.read_text()) if oldpath.exists() else {}
if doc['root'].get('system_update') and doc['root'].get('system_update')!=old.get('root',{}).get('system_update'):
    subprocess.run(['apt-get','update'],check=True)
    subprocess.run(['apt-get','-y','upgrade'],check=True,env={**__import__('os').environ,'DEBIAN_FRONTEND':'noninteractive'})
for package in ('hello','figlet'):
    wanted=package in doc['programs']
    result=subprocess.run(['dpkg-query','-W','-f=${db:Status-Status}',package],capture_output=True,text=True)
    present=result.stdout=='installed'
    if wanted and not present:
        archives=list(pathlib.Path('/opt/cal-packages').glob(package+'_*.deb'))
        if len(archives)!=1: raise RuntimeError('expected one offline package '+package)
        subprocess.run(['dpkg','-i',str(archives[0])],check=True)
    elif present and not wanted:
        subprocess.run(['dpkg','--remove',package],check=True)
tools='bash dash cat ls mkdir rmdir cp mv rm chmod touch date id sha256sum readlink head tail wc sort uniq tee printf env sleep true false timeout curl jq tar gzip unzip stat pwd dd tr'.split()
programs={'alpha':['/usr/local/lib/cal/alpha'],'beta':['/usr/local/lib/cal/beta'], 'hello':['/usr/bin/hello'], 'figlet':['/usr/bin/figlet'], 'python':['/usr/bin/python3.11'], 'node':['/usr/bin/node'], 'browser':['/usr/bin/chromium','/usr/lib/chromium/chromium','/usr/lib/chromium/chrome_crashpad_handler','/usr/bin/dirname','/usr/bin/basename','/usr/bin/grep','/usr/bin/sed','/usr/bin/uname','/usr/bin/cut','/usr/bin/tr','/usr/bin/find','/usr/bin/xargs','/usr/bin/readlink','/usr/bin/getent','/usr/bin/expr']}
channels={'package':['/usr/bin/apt','/usr/bin/apt-get','/usr/bin/dpkg'], 'pip':['/usr/bin/pip','/usr/bin/pip3','/usr/bin/python3.11'], 'npm':['/usr/bin/npm','/usr/bin/node'], 'flatpak':['/usr/bin/flatpak'], 'appimage':['/home/*/*.AppImage'], 'download':['/home/*/downloaded','/tmp/downloaded'], 'build':['/usr/bin/gcc','/usr/bin/x86_64-linux-gnu-gcc-12','/usr/lib/gcc/**','/usr/bin/as','/usr/bin/ld','/home/*/built'], 'systemd':['/usr/bin/systemctl','/usr/bin/systemd-run','/usr/lib/systemd/systemd'], 'cron':['/usr/bin/crontab'], 'interpreter':['/usr/bin/python3.11','/usr/bin/node']}
profiles=[]
for user in ('alice','bob'):
    paths={'/usr/bin/'+x for x in tools}|{'/usr/local/bin/calctl'}
    for ident, item in doc['programs'].items():
        if item['scope']=='system' or user in item['owners']: paths.update(programs[ident])
    for channel in doc['allow_channels'].get(user,[]): paths.update(channels[channel])
    lines=[f'profile cal-{user} flags=(attach_disconnected) {{','  / r,','  /** r,','  /usr/lib/** mr,','  /lib/** mr,',f'  owner /home/{user}/** rwkl,','  owner /tmp/** rwkl,','  owner /var/tmp/** rwkl,','  owner /dev/shm/** rwkl,','  /dev/null rw,','  /dev/zero rw,','  /dev/urandom r,','  /dev/random r,','  /dev/tty rw,','  /dev/pts/** rw,','  /run/cal.sock rw,','  network inet stream,','  network inet6 stream,','  network inet dgram,','  network inet6 dgram,','  network unix,','  signal (receive),','  signal (send) peer=cal-'+user+',','  ptrace (read,trace) peer=cal-'+user+',']
    for ident,item in doc['programs'].items():
        if user in item['owners']:
            lines += [f'  owner /var/lib/cal/active/{ident}/** rwkl,',f'  /var/lib/cal/active/{ident}/ rw,']
    if 'browser' in doc['programs'] and (doc['programs']['browser']['scope']=='system' or user in doc['programs']['browser']['owners']):
        lines += ['  /proc/*/oom_score_adj w,','  /proc/*/task/*/comm rw,']
    # AppArmor checks the resolved target (e.g. Debian's figlet alternative).
    paths |= {str(pathlib.Path(path).resolve()) for path in paths if '*' not in path}
    for path in sorted(paths): lines.append('  '+path+' mrix,')
    lines.append('}')
    profiles.append('\n'.join(lines))
# Managed root program is confined by executable attachment, not by uid.
profiles.append('''profile cal-root-program /usr/local/lib/cal/worker flags=(attach_disconnected) {
  /** r,
  /usr/lib/** mr,
  /lib/** mr,
  /var/lib/cal/active/** rwk,
  /dev/null rw,
  /dev/pts/** rw,
  /usr/local/lib/cal/worker mrix,
}''')
path=pathlib.Path('/etc/apparmor.d/cal-stand')
path.write_text('\n\n'.join(profiles)+'\n')
subprocess.run(['apparmor_parser','-r',str(path)],check=True)
print('Loaded enforcing profiles for alice, bob, and the managed root worker')
