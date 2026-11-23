#!/usr/bin/env python3
"""Synthetic source check: native provenance must never supply language reason."""
import json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'collector'))
import packages
class Context:
 def __init__(self):
  self.data={
   '/python/a.dist-info/METADATA':'Name: a\nVersion: 1\n',
   '/python/b.dist-info/METADATA':'Name: b\nVersion: 1\n',
   '/python/old.egg-info':'Name: old\nVersion: 1\n',
   '/work/package-lock.json':json.dumps({'packages':{'':{'dependencies':{'wanted':'1'}},'node_modules/wanted':{'version':'1'},'node_modules/transitive':{'version':'1'}}}),
   '/work/node_modules/wanted/package.json':'{"name":"wanted"}',
   '/work/node_modules/transitive/package.json':'{"name":"transitive"}',
   '/native/node_modules/unmatched/package.json':'{"name":"unmatched"}',
  }
  self.entries={p:{'type':'file'} for p in self.data};self.entries['/python/b.dist-info/REQUESTED']={'type':'file'}
  self.owned={p:{'native-explicit'} for p in self.data};self._native_package_ids={'native-explicit'}
  self.gaps=[];self.package_files=[];self._package_digest_jobs=[];self.package_ownership_complete=True;self.objects=[]
 def safe_read(self,path,limit):return (self.data[path].encode(),0,'fixture') if path in self.data else (b'',2,'fixture-missing')
 def add(self,level,kind,name,facts,evidence):self.objects.append((name,facts));return str(len(self.objects))
c=Context();packages.language(c)
facts={name.split(':',1)[1].split('@',1)[0]:fact for name,fact in c.objects}
assert facts['a']['reason']=='unknown' and facts['a']['native_package_ids']==['native-explicit']
assert facts['b']['reason']=='explicit' and facts['b']['reason_source']=='python-requested'
assert facts['old']['reason']=='unknown'
assert facts['wanted']['reason']=='explicit' and facts['wanted']['reason_source']=='npm-lock-top-level'
assert facts['transitive']['reason']=='dependency' and facts['transitive']['reason_source']=='npm-lock-transitive'
assert facts['unmatched']['reason']=='unknown' and facts['unmatched']['native_package_ids']==['native-explicit']
assert all(f.get('reason_source')!='native-owner' for f in facts.values())
print('PASS: synthetic native provenance does not transfer reason; own REQUESTED and npm lock evidence remain usable.')
