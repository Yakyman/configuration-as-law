#!/usr/bin/env python3
"""Synthetic adapter checks only; no live target or observation."""
import csv
import hashlib
import json
import os
import subprocess
import pathlib
import sys
import tempfile
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'collector'))
import extra_talos
import talos

with patch.object(extra_talos,'collect',lambda ctx:None):
    legacy=talos.fixture_check()
assert legacy['passed']

MOUNT=b'10 0 7:0 / / ro - squashfs /dev/loop0 ro\n11 10 0:44 / /etc rw - overlay overlay rw,lowerdir=/base/etc,upperdir=/upper/etc\n'
HEADER=['NODE','MODE','UID','GID','SIZE(B)','LASTMOD','LABEL','NAME']
WIDTHS=[10,14,6,6,10,24,10,0]
def listing(entries):
    def line(items):return ''.join(str(x).ljust(w) for x,w in zip(items,WIDTHS))
    return (line(HEADER)+'\n'+''.join(line(['node',mode,0,0,size,'Nov 23 00:00:00','',name])+'\n' for name,mode,size in entries)).encode()
class Context:
    def __init__(self,path):
        self.out=path;self.calls=[]
        self.objects=[['group','test',2,'stored-ownership-unknown','/etc','{}','fixture'],['code','test',2,'code-ownership-unknown','/etc/tool','{}','fixture']]
    def query(self,label,args,timeout=0,**kw):
        self.calls.append((label,args,timeout,kw))
        if label=='s4-talos-mountinfo':
            assert args==['talosctl','read','/proc/self/mountinfo'] and kw['max_bytes']==1048576 and timeout==15
            return MOUNT,0,'fixture-mount'
        if label=='s4-talos-source-images':return b'{"resource_id":"pod","image":"registry.example/program:v1"}\n',0,'fixture-source'
        if label=='s4-talos-list':
            assert args[:4]==['talosctl','list','--depth','1']
            entries={'/etc':[('tool','-rwxr-xr-x',5)],'/var/lib/kubelet':[('workload','-rwxr-xr-x',4)],'/var/lib/containerd':[('large','-rw-r--r--',extra_talos.CONTENT_LIMIT+1)]}
            return listing(entries.get(args[-1],[])),0,'fixture-list'
        if label=='s4-talos-content':
            assert json.loads(args[-1])==[['/etc/tool',5],['/var/lib/kubelet/workload',4]]
            output=[]
            for path,payload,signature in [('/etc/tool',b'#!/sh','shebang'),('/var/lib/kubelet/workload',b'\x7fELF','ELF')]:
                output.append(json.dumps({'path':path,'status':'ok','bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest(),'prefix_hex':payload.hex(),'signature':signature,'query_exit':0}))
            return ('\n'.join(output)+'\n').encode(),0,'fixture-content'
        raise AssertionError(label)
with tempfile.TemporaryDirectory(prefix='talos-synthetic-',dir=ROOT/'rehearsal/talos') as name:
    ctx=Context(pathlib.Path(name));extra_talos.collect(ctx)
    summary=ctx.s4_summary['talos']
    assert summary['listing_failures']==0 and summary['boundaries']==0
    assert summary['mountinfo_status']=='ok' and summary['mountinfo_rows']==2
    assert summary['content_ok']==2 and summary['current_image_source_rows']==1
    assert summary['content_status_counts']=={'ok':2,'size-cap':1}
    assert summary['content_by_root']['/var/lib/kubelet']=={'ok':1}
    assert summary['content_by_root']['/var/lib/containerd']=={'size-cap':1}
    with (ctx.out/'talos-content.tsv').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    by_path={r['path']:r for r in rows}
    assert json.loads(by_path['/etc/tool']['object_ids'])==['group','code'] and by_path['/etc/tool']['signature']=='shebang'
    assert by_path['/var/lib/kubelet/workload']['signature']=='ELF'
    assert by_path['/var/lib/containerd/large']['status']=='size-cap' and by_path['/var/lib/containerd/large']['bytes']=='0'
    for payload,rc,expected in [(b'',0,'parser-failed'),(b'broken\n',0,'parser-failed'),(b'partial',75,'query-failed')]:
        with patch.object(ctx,'query',return_value=(payload,rc,'fixture-error')):
            assert extra_talos.mount_map(ctx)['mountinfo_status']==expected
# Exercise the concurrent stream reader with a disposable fake client, never an API.
with tempfile.TemporaryDirectory(prefix='talos-reader-fixture-',dir=ROOT/'rehearsal/talos') as name:
    directory=pathlib.Path(name);client=directory/'talosctl'
    client.write_text('#!'+sys.executable+'''
import sys,io,tarfile,posixpath
path=sys.argv[2]
if path.endswith('missing'):
 print('rpc error: code = Unknown desc = open '+path+': permission denied',file=sys.stderr);sys.exit(3)
payload=b"\\x7fELF" if path.endswith('elf') else b"#!/sh"
if sys.argv[1]=='copy':
 with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as archive:
  info=tarfile.TarInfo(posixpath.basename(path));info.size=len(payload);archive.addfile(info,io.BytesIO(payload))
else:sys.stdout.buffer.write(payload)
''')
    client.chmod(0o700)
    requested=[['fixture-elf',4],['fixture-script',5],['fixture-changing',9],['fixture-missing',0]]
    run=subprocess.run([sys.executable,'-c',extra_talos.READ_SCRIPT,json.dumps(requested)],capture_output=True,timeout=10,env={**os.environ,'PATH':str(directory.resolve())+os.pathsep+os.environ.get('PATH','')})
    assert run.returncode==0,run.stderr.decode()
    streams={r['path']:r for r in map(json.loads,run.stdout.splitlines())}
    assert streams['fixture-elf']['signature']=='ELF' and streams['fixture-elf']['sha256']==hashlib.sha256(b'\x7fELF').hexdigest()
    assert streams['fixture-script']['signature']=='shebang'
    assert streams['fixture-changing']['status']=='size-changed' and streams['fixture-changing']['sha256']==''
    assert streams['fixture-missing']['status']=='read-error' and streams['fixture-missing']['signature']=='unknown'
    copied=subprocess.run([sys.executable,'-c',extra_talos.COPY_SCRIPT,json.dumps(requested)],capture_output=True,timeout=10,env={**os.environ,'PATH':str(directory.resolve())+os.pathsep+os.environ.get('PATH','')})
    assert copied.returncode==0,copied.stderr.decode()
    copies={r['path']:r for r in map(json.loads,copied.stdout.splitlines())}
    assert copies['fixture-elf']['signature']=='ELF' and copies['fixture-elf']['sha256']==hashlib.sha256(b'\x7fELF').hexdigest()
    assert copies['fixture-script']['signature']=='shebang'
    assert copies['fixture-changing']['status']=='archive-error' and copies['fixture-changing']['sha256']==''
    assert copies['fixture-missing']['error_category']=='permission-denied'
    assert 'fixture-missing' not in copies['fixture-missing']['diagnostic'] and '<target>' in copies['fixture-missing']['diagnostic']
with tempfile.TemporaryDirectory(prefix='talos-refresh-fixture-',dir=ROOT/'rehearsal/talos') as name:
    directory=pathlib.Path(name);client=directory/'talosctl'
    client.write_text('#!'+sys.executable+'''
import sys,pathlib
state=pathlib.Path(__file__).with_name('changed')
if sys.argv[1]=='list':
 widths=[10,14,6,6,10,24,10,0]
 def line(items):return ''.join(str(x).ljust(w) for x,w in zip(items,widths))
 print(line(['NODE','MODE','UID','GID','SIZE(B)','LASTMOD','LABEL','NAME']))
 for name,mode,size in [('elf','-rwxr-xr-x',4),('script','-rwxr-xr-x',5),('unstable','-rw-r--r--',6 if state.exists() else 5),('link','Lrwxrwxrwx',5)]:
  print(line(['node',mode,0,0,size,'Nov 23 00:00:00','',name]))
else:
 if sys.argv[2].endswith('unstable'):state.touch()
 sys.stdout.buffer.write(b"\\x7fELF" if sys.argv[2].endswith('elf') else b"#!/sh")
''')
    client.chmod(0o700)
    requested=[['/fixture/elf',4],['/fixture/script',9],['/fixture/missing',0],['/fixture/link',5],['/fixture/unstable',5]]
    run=subprocess.run([sys.executable,'-c',extra_talos.REFRESH_SCRIPT,json.dumps(requested)],capture_output=True,timeout=15,env={**os.environ,'PATH':str(directory.resolve())+os.pathsep+os.environ.get('PATH','')})
    assert run.returncode==0,run.stderr.decode()
    rows={r['path']:r for r in map(json.loads,run.stdout.splitlines())}
    assert rows['/fixture/elf']['signature']=='ELF'
    assert rows['/fixture/script']['status']=='ok' and rows['/fixture/script']['original_listing_size']==9 and rows['/fixture/script']['before']['size']==5
    assert rows['/fixture/missing']['status']=='not-found'
    assert rows['/fixture/link']['status']=='nonregular-type'
    assert rows['/fixture/unstable']['status']=='metadata-changed' and rows['/fixture/unstable']['sha256']==''
print(json.dumps({'legacy_fixture':'passed; extension patched out; baseline only','extension_synthetic':'passed; bounded mount query, parser failures, source references, listing/content schemas, all-target content scope, concurrent bounded Read and Copy streams via fake client, fresh metadata before/after, absence, type and size changes, per-file/root cap counters, group/code joins','live_queries':0},sort_keys=True))
