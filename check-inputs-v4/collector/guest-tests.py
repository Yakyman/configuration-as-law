"""Implementation validation only. Run on the disposable Debian guest."""
import hashlib,json,os,pathlib,subprocess,time
root=pathlib.Path('/tmp/c1-tests');probe=str(root/'probe');tree=root/'tree';tree.mkdir(exist_ok=True)
(tree/'script with spaces').write_bytes(b'#!/bin/sh\necho fixture\n');(tree/'.bashrc').write_text('true\n');(tree/'large').write_bytes(b'A'*8192)
(tree/'image.img').write_bytes(b'X'*10000);(tree/'proc-alias').symlink_to('/proc');os.mkfifo(tree/'fifo');(tree/'newline\nfile').write_bytes(b'X')
expected={str(p) for p in tree.iterdir()}|{str(tree)}
def scan(env=None):
 p=subprocess.run([probe,'scan',str(tree)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20);assert p.returncode==0,p.stderr
 rows=[json.loads(x) for x in p.stdout.splitlines()];assert rows[-1]['complete'];return {x['path']:x for x in rows if 'path' in x}
rows=scan();assert set(rows)==expected,(set(rows)-expected,expected-set(rows))
assert rows[str(tree/'script with spaces')]['shebang'];assert rows[str(tree/'.bashrc')]['startup']
assert rows[str(tree/'large')]['signature_bytes']==4096
assert rows[str(tree/'large')]['signature']=='sha256-prefix4096:'+hashlib.sha256(b'A'*4096).hexdigest()
assert rows[str(tree/'image.img')]['atomic']=='image';assert rows[str(tree/'image.img')]['signature_bytes']==4096
for kind in ('busybox','toybox'):
 target=root/kind;target.mkdir()
 for app in ('sh','find','stat','head','base64','gzip'): (target/app).symlink_to('/bin/'+kind)
 env={**os.environ,'PATH':str(target)}
 assert scan(env)==rows
for path in ('/proc/self/maps','/sys/kernel/uevent_seqnum','/dev/zero',str(tree/'proc-alias/self/maps'),str(tree/'fifo'),str(tree/'large')):
 p=subprocess.run([probe,'read',path,'4096'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=3);assert p.returncode!=0 and not p.stdout,(path,p.returncode)
request='\n'.join(json.dumps({'path':str(tree/'large'),'algorithm':a,'limit':16384}) for a in ('md5','sha1','sha256','sha384','sha512'))+'\n'
p=subprocess.run([probe,'digests'],input=request.encode(),stdout=subprocess.PIPE,timeout=10)
for row in map(json.loads,p.stdout.splitlines()):assert row['digest']==hashlib.new(row['algorithm'],b'A'*8192).hexdigest()
t0=time.monotonic();p=subprocess.run([probe,'run','1','sh','-c','sleep 20'],timeout=4);assert p.returncode==124 and time.monotonic()-t0<4
# Trace helper file opens separately: startup and traversal must not open pseudo contents.
trace=root/'trace.log';subprocess.run(['strace','-f','-e','trace=openat,open,read,readlink,getdents64','-o',str(trace),probe,'scan',str(tree)],stdout=subprocess.DEVNULL,check=True,timeout=20)
for line in trace.read_text().splitlines():
 if ('openat(' in line or 'open(' in line) and any('"'+p in line for p in ('/proc/','/sys/','/dev/')):raise AssertionError(line)
# Test genuine Btrfs snapshots and read-only mount flags, never a check system.
fs=root/'fs';fs.mkdir();image=root/'btrfs.img';subprocess.run(['truncate','-s','128M',str(image)],check=True)
subprocess.run(['mkfs.btrfs','-q','-f',str(image)],check=True)
subprocess.run(['mount','-o','loop',str(image),str(fs)],check=True)
try:
 subprocess.run(['btrfs','subvolume','create',str(fs/'live')],check=True,stdout=subprocess.DEVNULL)
 (fs/'live'/'kept').write_text('fixture');subprocess.run(['btrfs','subvolume','snapshot','-r',str(fs/'live'),str(fs/'old')],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['mount','-o','remount,ro',str(fs)],check=True)
 p=subprocess.run([probe,'scan',str(fs)],stdout=subprocess.PIPE,check=True,timeout=20);r={x['path']:x for x in map(json.loads,p.stdout.splitlines()) if 'path' in x}
 assert r[str(fs/'old')]['atomic']=='snapshot' and str(fs/'old'/'kept') not in r
 assert str(fs/'live'/'kept') in r and r[str(fs/'live'/'kept')]['readonly'] is True
finally:subprocess.run(['umount',str(fs)],check=True)
import talos
print(json.dumps({'passed':True,'checks':['GNU/busybox/toybox PATH independence','full names including newline','FIFO and pseudo aliases refused','4096 byte signature','all digest algorithms','timeout kills group','strace no pseudo-file opens','Btrfs snapshot opaque','read-only mount flag'],'talos':talos.fixture_check()}))
