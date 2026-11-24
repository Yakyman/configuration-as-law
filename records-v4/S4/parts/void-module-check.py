"""Synthetic npm archive equality and tamper checks; no machine inventory."""
import base64,hashlib,io,json,pathlib,sys,tarfile,tempfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'collector'))
import extra_void
class Context:
 def __init__(self,d):
  self.out=pathlib.Path(d);self.objects=[];self.owned={};self.users=[{'home':'/synthetic'}]
  archive=io.BytesIO()
  with tarfile.open(fileobj=archive,mode='w:gz') as tf:
   member=tarfile.TarInfo('package/a.js');member.size=4;tf.addfile(member,io.BytesIO(b'test'))
  archive=archive.getvalue();digest=hashlib.sha512(archive).digest();h=digest.hex();cache='/synthetic/.npm/_cacache/content-v2/sha512/'+h[:2]+'/'+h[2:4]+'/'+h[4:]
  self.entries={p:{'type':'file'} for p in ['/synthetic/package-lock.json','/synthetic/node_modules/a/package.json','/synthetic/node_modules/a/a.js',cache]}
  self.data={cache:archive,'/synthetic/package-lock.json':json.dumps({'packages':{'node_modules/a':{'integrity':'sha512-'+base64.b64encode(digest).decode(),'resolved':'https://example.invalid/a.tgz'}}}).encode()}
 def safe_read(self,p,limit):return (self.data[p],0,'synthetic') if p in self.data else (b'',75,'synthetic')
 def safe_reads(self,paths,limit):return {p:self.safe_read(p,limit) for p in paths}
 def digests(self,requests,max_bytes):return {(p,a):{'status':'ok','digest':hashlib.sha256(b'test').hexdigest(),'evidence':'synthetic'} for p,a in requests}
with tempfile.TemporaryDirectory() as d:
 ctx=Context(d);extra_void.collect_npm(ctx)
 assert ctx.s4_summary['npm']['verified_archives']==1
 assert ctx.s4_summary['npm']['equal']==1
 assert ctx.s4_summary['npm']['not-compared-to-archive']==1
with tempfile.TemporaryDirectory() as d:
 ctx=Context(d)
 for p in ctx.data:
  if '_cacache' in p:ctx.data[p]+=b'tamper'
 extra_void.collect_npm(ctx)
 assert ctx.s4_summary['npm'].get('verified_archives',0)==0
 assert ctx.s4_summary['npm'].get('equal',0)==0
print('synthetic archive verification: 2 cases passed')
for mode in ('installed-metadata','cache-index'):
 with tempfile.TemporaryDirectory() as d:
  ctx=Context(d);ctx.entries.pop('/synthetic/package-lock.json');ctx.data.pop('/synthetic/package-lock.json')
  contents={'package/a.js':b'test','package/package.json':b'{"name":"a","version":"1.0.0"}'}
  stream=io.BytesIO()
  with tarfile.open(fileobj=stream,mode='w:gz') as tf:
   for name,data in contents.items():
    member=tarfile.TarInfo(name);member.size=len(data);tf.addfile(member,io.BytesIO(data))
  archive=stream.getvalue();digest=hashlib.sha512(archive).digest();h=digest.hex();sri='sha512-'+base64.b64encode(digest).decode()
  cache='/synthetic/.npm/_cacache/content-v2/sha512/'+h[:2]+'/'+h[2:4]+'/'+h[4:]
  ctx.entries[cache]={'type':'file'};ctx.data[cache]=archive
  meta={'name':'a','version':'1.0.0'}
  if mode=='installed-metadata':meta['_integrity']=sri
  else:
   encoded=json.dumps({'key':'make-fetch-happen:request-cache:https://registry.npmjs.org/a/-/a-1.0.0.tgz','integrity':sri}).encode()
   path='/synthetic/.npm/_cacache/index-v5/aa/bb/cc';ctx.entries[path]={'type':'file'};ctx.data[path]=hashlib.sha1(encoded).hexdigest().encode()+b'\t'+encoded+b'\n'
  ctx.data['/synthetic/node_modules/a/package.json']=json.dumps(meta).encode()
  extra_void.collect_npm(ctx)
  assert ctx.s4_summary['npm']['verified_archives']==1
  key='installed-metadata-reference' if mode=='installed-metadata' else 'cache-identity-reference-not-install-receipt'
  assert ctx.s4_summary['npm'][key]==1
print('synthetic unlocked reference verification: 2 cases passed')
