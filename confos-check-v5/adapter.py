"""The ONLY place for platform format, guest access, boot and build knowledge.

Pre-interface mode provides a strict transcript transport and stand command plans.
It intentionally cannot run host shell commands as a substitute for a guest.
See ASSUMPTIONS.md. Native execution is bound in part 2, after reading the release.
"""
import json
from pathlib import Path
from core import digest

class Unavailable(Exception):
    pass

class Transcript:
    def __init__(self, path):
        self.data=json.loads(Path(path).read_text())
        self.events=iter(self.data['events'])
        self.count=0
    def perform(self, request):
        try: event=next(self.events)
        except StopIteration: raise Unavailable('fixture exhausted')
        self.count+=1
        if event['request']!=request:
            raise ValueError('fixture request mismatch at event '+str(self.count))
        if 'unavailable' in event:
            raise Unavailable(event['unavailable'])
        reply=event['reply']
        if not isinstance(reply,dict): raise ValueError('adapter response must be an object')
        return reply
    def finish(self):
        if next(self.events,None) is not None:
            raise ValueError('unconsumed fixture events')

class StandPlan:
    """Inspection-only translations of the documented stand interface, not execution."""
    def render_line(self,line):
        k=line['kind']
        if k=='setting': return 'setting '+line['name']+' '+line['value']
        if k=='account':
            keys=('name','uid','gid','groups','shell','home')
            if not all(k in line for k in keys):
                raise Unavailable('stand account requires explicit identifiers')
            return 'account '+' '.join(str(line[k]) for k in keys)
        if k=='package': return 'package '+line['name']+' '+line['version']
        if k=='service': return 'service '+line['name']+' '+line['state']+' '+line['command']
        raise Unavailable('native line kind not documented: '+k)
    def plan(self,request):
        op=request['op']
        if op=='fresh': return {'argv':['./build.sh','DECLARATION','OUTPUT.qcow2'], 'scope':'owned-source-copy','assumption':'A01'}
        if op=='boot': return {'argv':['./boot.sh','DISK','SSH_PORT','MEMORY_MIB','SERIAL_LOG','QMP_SOCKET'],'scope':'confos.slice with external slot lock','assumption':'A02'}
        if op=='apply': return {'guest_role':'root','argv':['confos','apply'],'success_query':['confos','status'],'success_pattern':'^APPLIED [0-9a-f]{64}$','assumption':'A04'}
        if op=='read-law': return {'candidate':'/state/declaration.conf','committed':'/generations/SHA256/declaration.conf','reader':'external read-only disk','assumption':'A04/A05'}
        if op=='command': return {'guest_role':request.get('role','user'),'shell_text':request['command'],'transport':'SSH; root sudo -n','assumption':'A03/A11'}
        raise Unavailable('stand binding unavailable: '+op)
    def perform(self,request):
        raise Unavailable('no named source-built release/interface bound; '+request['op'])
    def finish(self): pass


def fixture_package_reader(root):
    """Test-only package container, NOT a specification of confpkg."""
    import tarfile, io
    root=Path(root).resolve()
    def read(line):
        path=(root/line['archive']).resolve()
        if not path.is_relative_to(root): raise ValueError('package input leaves input directory')
        data=path.read_bytes()
        if digest(data)!=line['archive_sha256']: raise ValueError('package archive hash mismatch')
        objects=[]; seen=set()
        with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as archive:
            for member in archive:
                parts=Path(member.name).parts
                if member.name.startswith('/') or '..' in parts or member.name in seen:
                    raise ValueError('unsafe or duplicate archive member')
                seen.add(member.name)
                value={'mode':format(member.mode,'04o'),'uid':member.uid,'gid':member.gid}
                if member.isfile():
                    value['sha256']=digest(archive.extractfile(member).read()); kind='file'
                elif member.isdir(): kind='dir'
                elif member.issym(): kind='symlink'; value['target']=member.linkname
                else: raise ValueError('unsupported fixture archive member')
                objects.append({'kind':kind,'id':'/'+member.name,'value':value})
        return objects
    return read


def collect_tree(root):
    """External ordinary-directory fixture reader. Never follows a guest symlink."""
    import os, stat
    root=Path(root).resolve(); objects=[]; errors=[]
    def walk(directory):
        try: entries=sorted(os.scandir(directory),key=lambda e:e.name)
        except OSError as exc:
            errors.append({'kind':'stored','reason':str(exc)}); return
        for entry in entries:
            p=Path(entry.path)
            try:
                st=p.lstat(); value={'mode':format(stat.S_IMODE(st.st_mode),'04o'),'uid':st.st_uid,'gid':st.st_gid}
                if stat.S_ISLNK(st.st_mode): kind='symlink'; value['target']=os.readlink(p)
                elif stat.S_ISDIR(st.st_mode): kind='dir'
                elif stat.S_ISREG(st.st_mode): kind='file'; value['sha256']=digest(p.read_bytes())
                else: kind='special'; value['type']=stat.S_IFMT(st.st_mode)
                objects.append({'kind':kind,'id':'/'+str(p.relative_to(root)),'value':value})
                if kind=='dir': walk(p)
            except OSError as exc: errors.append({'kind':'stored','reason':str(exc)})
    walk(root)
    return {'objects':objects,'errors':errors,'coverage':{'stored':{'status':'complete' if not errors else 'incomplete','evidence':'external fixture tree scan'}}}

class StandTransport:
    """Executable transport for documented stand operations, without auto-start.

    Construction requires explicit private configuration. This is not selected by
    the part-1 CLI. It cannot create a VM or execute a guest command on the host.
    Build/boot/disk/new native grammar remain A01/A02/A05/A06 bindings.
    """
    def __init__(self, config):
        import os
        self.config=dict(config)
        for key in ('guest_host','guest_port','guest_user','ssh_key','known_hosts'):
            if not self.config.get(key): raise Unavailable('missing private transport field '+key)
        if self.config.get('release') in (None,'UNBOUND'):
            raise Unavailable('no named release')
    def command(self, command, role='user', stdin=None, timeout=60):
        import shlex, subprocess, time
        if role not in ('user','root'): raise ValueError('unknown guest role')
        remote=('sudo -n sh -c '+shlex.quote(command)) if role=='root' else ('sh -c '+shlex.quote(command))
        argv=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
              '-o','UserKnownHostsFile='+self.config['known_hosts'],
              '-o','ConnectTimeout=10','-i',self.config['ssh_key'],
              '-p',str(int(self.config['guest_port'])),'--',
              self.config['guest_user']+'@'+self.config['guest_host'],remote]
        start=time.monotonic()
        try:
            p=subprocess.run(argv,input=stdin,capture_output=True,timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise Unavailable('guest command timeout, not refusal: '+command) from exc
        if p.returncode==255: raise Unavailable('SSH transport failed, not policy refusal: '+p.stderr.decode(errors='replace'))
        return {'command':command,'role':role,'returncode':p.returncode,
                'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace'),
                'started_monotonic':start,'ended_monotonic':time.monotonic()}
    def status(self):
        import re
        result=self.command('confos status')
        value=result['stdout'].strip()
        if result['returncode'] or not re.fullmatch(r'APPLIED [0-9a-f]{64}',value):
            raise Unavailable('no exact successful committed status: '+repr(value))
        return dict(result,status=value,sha256=value.split()[1])
    def write_candidate(self, text):
        blob=text.encode()
        result=self.command('cat > /state/declaration.conf.new && mv /state/declaration.conf.new /state/declaration.conf',role='root',stdin=blob)
        if result['returncode']: return result
        actual=self.command('sha256sum /state/declaration.conf',role='root')
        if actual['returncode'] or actual['stdout'].split()[:1]!=[digest(blob)]:
            raise Unavailable('candidate bytes not verified after write')
        return dict(result,sha256=digest(blob))
    def perform(self,request):
        if request['op']=='command':
            if '@' in request['command']: raise Unavailable('unbound command token')
            return self.command(request['command'],request.get('role','user'))
        if request['op']=='read-boot':
            r=self.command('cat /proc/sys/kernel/random/boot_id')
            if r['returncode']: raise Unavailable('boot identity unreadable')
            return dict(r,boot_id=r['stdout'].strip())
        if request['op']=='query' and request['subject']=='status': return self.status()
        raise Unavailable('stand operation requires native lifecycle/disk binding: '+request['op'])
    def finish(self): pass
