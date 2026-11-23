#!/usr/bin/python3 -B
"""Factory inventory: executed once before the factory declaration is frozen."""
import grp, json, os, pathlib, pwd, re, sys
sys.path.insert(0,'/usr/local/lib/stand')
import stand
d=pathlib.Path('/etc/stand/factory');d.mkdir(parents=True,exist_ok=True)
excluded=('/etc/fapolicyd/fapolicyd.trust','/etc/stand/','/etc/passwd','/etc/group','/etc/shadow','/etc/gshadow',
          '/etc/passwd-','/etc/group-','/etc/shadow-','/etc/gshadow-','/etc/subuid','/etc/subgid','/etc/subuid-','/etc/subgid-','/etc/.pwd.lock','/etc/mtab','/etc/resolv.conf','/etc/hostname','/etc/hosts',
          '/etc/machine-id','/etc/NetworkManager/system-connections/','/etc/ssh/sshd_config.d/00-stand.conf',
          '/etc/sudoers.d/stand','/usr/local/lib/stand/__pycache__/','/etc/systemd/system/stand-',
          '/etc/NetworkManager/secret_key','/etc/apparmor.d/abstractions/stand-map','/etc/apparmor.d/abstractions/stand-read')
files=[]
for prefix in ('/usr','/boot','/etc','/bin','/sbin','/lib','/lib64'):
    p=pathlib.Path(prefix)
    paths=[p] if p.is_symlink() else p.rglob('*')
    for f in paths:
        name=str(f)
        if any(name==e or (e.endswith('/') and name.startswith(e)) or (e.endswith('-') and name.startswith(e)) for e in excluded):continue
        if f.is_symlink() or f.is_file():files.append(stand.filevalue(f))
files.append(stand.filevalue('/etc/stand/w3m.conf'))
files=sorted(files,key=lambda x:x['path'])
blob=(stand.canonical(files)+'\n').encode();stand.atomic(d/'base-files.json',blob)
packages=stand.run('dpkg-query','-W','-f=${binary:Package}\t${Version}\n').stdout
stand.atomic('/var/lib/stand/evidence/packages.tsv',packages)
rows=[{'id':'base','type':'base','managed':False,'version':'stand-0.1',
       'source':'https://cloud.debian.org/images/cloud/trixie/20261116-2664/debian-13-generic-amd64-20261116-2664.qcow2',
       'source_sha512':'e53a93ef33f828ceed0e7278c2cc2753bdc7d5098fbfae15bd64b6d878db350ea3744247763a1c8ecb6b4019a0f623c38caf6038ad6f9c357fb4e01493ddf1a3',
       'files_manifest':'base-files.json','manifest_sha256':stand.digest(blob)}]
# Make installed packages independently visible, with immutable image-backed contents.
by_path={f['path']:f for f in files}
for line in stand.run('dpkg-query','-W','-f=${binary:Package}\t${Version}\t${db:Status-Status}\n').stdout.splitlines():
    package,version,status=line.split('\t')
    if status!='installed':continue
    members=[]
    for name in stand.run('dpkg-query','-L',package).stdout.splitlines():
        if name in by_path:members.append(by_path[name])
    rows.append({'id':'package:'+package,'type':'program','managed':False,'version':version,
                 'source':'factory-image:'+rows[0]['source_sha512'],'files':sorted(members,key=lambda x:x['path'])})
# Explicit own-rights code inventory; no claim of complete semantic classification.
code=[]
for f in files:
    if f['kind']!='file':continue
    name=f['path']
    if name.endswith(('.py','.sh','.bash','.pl','.rb')):code.append(f);continue
    if f['mode'] & 0o111:
        try:
            with open(name,'rb') as stream:
                if stream.read(2)==b'#!':code.append(f)
        except OSError:pass
for name in ('/home/stand/.bashrc','/home/stand/.profile','/root/.bashrc','/root/.profile'):
    if pathlib.Path(name).is_file():code.append(stand.filevalue(name))
rows.append({'id':'code:factory','type':'code','managed':False,'version':'stand-0.1',
             'source':'factory-image:'+rows[0]['source_sha512'],'files':sorted(code,key=lambda x:x['path'])})
for p in pwd.getpwall():
    rows.append({'id':'account:'+p.pw_name,'type':'account','managed':False,**stand.account_value(p.pw_name)})
units=set()
for line in stand.run('systemctl','list-unit-files','--type=service,timer','--state=enabled,enabled-runtime','--no-legend','--no-pager').stdout.splitlines():
    if line.strip():units.add(line.split()[0])
for line in stand.run('systemctl','list-units','--type=service,timer','--state=running,active','--no-legend','--plain','--no-pager').stdout.splitlines():
    if line.strip():units.add(line.split()[0])
units.update(p.name for p in pathlib.Path('/etc/systemd/system').glob('stand-*') if p.is_file() and p.suffix in ('.service','.timer','.socket'))
for unit in sorted(units):
    r={'id':'unit:'+re.sub(r'[^a-zA-Z0-9_.:@-]','_',unit),'type':'timer' if unit.endswith('.timer') else 'socket' if unit.endswith('.socket') else 'service','unit':unit,'managed':False}
    value=stand.service_value(r)
    if value['unit_sha256']:rows.append({**r,**value})
for line in stand.run('systemctl','--global','list-unit-files','--type=service,timer','--state=enabled','--no-legend','--no-pager').stdout.splitlines():
    if not line.strip():continue
    unit=line.split()[0];path=pathlib.Path('/usr/lib/systemd/user')/unit
    if path.is_file():
        r={'id':'user-unit:'+unit,'type':'timer' if unit.endswith('.timer') else 'socket' if unit.endswith('.socket') else 'service','unit':unit,'scope':'user-global','unit_path':str(path),'managed':False}
        rows.append({**r,**stand.service_value(r)})
rows.append({'id':'sudo:stand','type':'privilege','managed':False,'path':'/etc/sudoers.d/stand','text':pathlib.Path('/etc/sudoers.d/stand').read_text(),'mode':0o440,'uid':0,'gid':0})
rows.append({'id':'key:stand','type':'login-key','managed':False,'path':'/etc/stand/authorized_keys','text':pathlib.Path('/etc/stand/authorized_keys').read_text(),'mode':0o644,'uid':0,'gid':0})
rows.append({'id':'key:operator','type':'login-key','managed':False,'path':'/root/.ssh/authorized_keys','text':pathlib.Path('/root/.ssh/authorized_keys').read_text(),'mode':0o600,'uid':0,'gid':0})
rows.append({'id':'password-login','type':'password-login','allowed':False})
for protocol in ('tcp','udp'):
    for i,local in enumerate(stand.port_values(protocol)):
        rows.append({'id':'port:'+protocol+':'+str(i),'type':'port','protocol':protocol,'port':int(local.rsplit(':',1)[1]),'local':local,'listening':True})
rows.append({'id':'boot','type':'boot','order':['disk'],'guest_can_change':False})
for i,path in enumerate(['/home','/tmp','/var/tmp','/dev/shm','/run']):
    rows.append({'id':'mount:'+str(i),'type':'rule','backend':'mount','managed':False,'path':path,'required_options':['noexec','nosuid','nodev']})
rows.append({'id':'firewall:input','type':'rule','backend':'nft-chain','managed':False,
             'chain':{'family':'inet','table':'stand','name':'input','type':'filter','hook':'input','prio':0,'policy':'accept'}})
protected=json.loads(pathlib.Path('/etc/stand/backend-paths.json').read_text())
protected+=['/var/cache/apt/archives','/var/lib/stand/generations','/var/spool/cron','/var/spool/cron/crontabs','/var/spool/cron/atjobs','/var/spool/cron/atspool']
rows.append({'id':'authority:backend-dac','type':'rule','backend':'dac','managed':False,'paths':[stand.filevalue(p) for p in sorted(set(protected))]})
rows.append({'id':'code-boundary','type':'rule','backend':'code-boundary','managed':False,'required':'declared immutable exec/map; sealed read closure; fixed launch inputs; no writable executable memory; confined services; root setup launcher runs before no_new_privs, permanently drops all groups and uid/gid to 1000, then locks no_new_privs; immutable chroot input view; exact enforcing stand-format-parser and stand-build kernel policies from recorded sources'})
stand.atomic(d/'machine.jsonl',''.join(stand.canonical(r)+'\n' for r in rows))
print('FACTORY rows='+str(len(rows))+' files='+str(len(files)))
