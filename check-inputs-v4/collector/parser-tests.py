# Pure output normalization fixtures, executed on disposable Debian.
import json,main
class C:
 def __init__(self,data):self.data=data;self.rows=[];self.gaps=[]
 def query(self,*a,**k):return self.data,0,'fixture.out'
 def add(self,*a):self.rows.append(a)
c=C(b'[{"Id":"one"},{"Id":"two"}]');main.lines(c,'container','containers','unused');assert len(c.rows)==2 and not c.gaps
c=C(b'{"nftables":[{"metainfo":{}},{"rule":{"table":"filter","chain":"input","handle":1}},{"rule":{"table":"filter","chain":"input","handle":2}}]}');main.lines(c,'firewall-nft','firewall','unused');assert len(c.rows)==2 and all(r[1]=='firewall-rule' for r in c.rows)
c=C(b'not json');main.lines(c,'container','containers','unused');assert not c.rows and c.gaps
print(json.dumps({'passed':True,'checks':['container records separated','firewall rules separated','parse failure not empty success']}))
import pathlib,tempfile,types
with tempfile.TemporaryDirectory(prefix='c1-schema-') as tmp:
 c=main.Context(types.SimpleNamespace(machine='fixture',output=tmp+'/output'),[],{'system':'fixture'})
 ident=c.add(2,'stored-ownership-unknown','/etc','complete_immediate_listing=true','fixture')
 ref=c.write_members(ident,[{'path':'/etc/a','type':'file'}]);c.finish()
 assert json.loads(c.objects[0][5])['file']==ref and (pathlib.Path(tmp)/'output'/ref).is_file()
print(json.dumps({'member_reference':True}))
