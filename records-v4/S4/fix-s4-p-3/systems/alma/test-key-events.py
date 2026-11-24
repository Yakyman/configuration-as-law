import pathlib,tempfile,runpy,subprocess,json
R=pathlib.Path(__file__).resolve().parent
source=runpy.run_path(str(R/'key_events.py'))['GUEST_SCRIPT']
base='''2026-11-23T00:00:00+0000 DDEBUG --- logging initialized ---
2026-11-23T00:00:01+0000 DDEBUG Command: dnf -y install tree
2026-11-23T00:00:02+0000 CRITICAL Importing GPG key 0xc2a1e572:
 Userid     : "Example"
 Fingerprint: 0000 0000 0000 0000 0000 0000 0000 0000 c2a1 e572
 From       : /etc/pki/rpm-gpg/TEST-KEY
2026-11-23T00:00:03+0000 INFO Key imported successfully
'''
cases={'complete':(base,'fields-recorded'),'missing_success':(base.rsplit('2026-11-23T00:00:03',1)[0],'unknown:event-fields-incomplete'),'different_command':(base.replace('2026-11-23T00:00:03','2026-11-23T00:00:02+0000 DDEBUG Command: dnf -y install git\n2026-11-23T00:00:03'),'unknown:event-fields-incomplete'),'rejected_command':(base.replace('dnf -y install tree','dnf --setopt=proxy_password=EXAMPLE install tree'),'unknown:event-fields-incomplete'),'general_safe_package':(base.replace('install tree','install qemu-guest-agent sudo'),'fields-recorded')}
results=[]
with tempfile.TemporaryDirectory(dir=R)as tmp:
 p=pathlib.Path(tmp)/'dnf.log'
 for name,(fixture,expected)in cases.items():
  p.write_text(fixture)
  program=source.replace("glob.glob('/var/log/dnf.log*')",'glob.glob('+repr(str(p))+')')
  proc=subprocess.run(['python3','-c',program],capture_output=True,text=True,check=True)
  rows=[json.loads(l)['event']for l in proc.stdout.splitlines()if '"event"'in l]
  assert len(rows)==1 and rows[0]['status']==expected,(name,rows)
  assert 'Userid' not in proc.stdout and 'proxy_password' not in proc.stdout
  results.append({'case':name,'passed':True})
# The bounded read counts bytes even when decoding would produce fewer characters.
with tempfile.TemporaryDirectory(dir=R)as tmp:
 p=pathlib.Path(tmp)/'dnf.log';p.write_bytes(('é'*17).encode())
 program=source.replace("glob.glob('/var/log/dnf.log*')",'glob.glob('+repr(str(p))+')').replace('32*1024*1024','32')
 proc=subprocess.run(['python3','-c',program],capture_output=True,text=True,check=True)
 records=[json.loads(l)for l in proc.stdout.splitlines()]
 assert records==[{'coverage':{'source':str(p),'status':'size-cap','bytes':33}}]
 results.append({'case':'multibyte_byte_cap','passed':True})
# Partial stdout from a failed transport cannot become a complete recorded field row.
import sys,types
module=runpy.run_path(str(R/'key_events.py'));tables={}
sys.modules['main']=types.SimpleNamespace(write_tsv=lambda path,header,rows:tables.update({path.name:(header,rows)}))
class Context:
 out=R
 objects=[['synthetic-id','alma',1,'package','rpm:gpg-pubkey@c2a1e572-00000000.(none)']]
 def query(self,*args):
  return (json.dumps({'event':{'key_id':'c2a1e572','status':'fields-recorded'}})+'\n').encode(),7,'raw/synthetic.out'
ctx=Context();module['collect'](ctx)
assert tables['alma-key-events.tsv'][1][0][-2]=='unknown:query-failed'
assert tables['alma-key-event-coverage.tsv'][1][0][1]=='unknown:query-failed'
assert tables['alma-key-event-coverage.tsv'][1][0][-2]==7
assert ctx.s4_summary['alma_key_events']['complete_field_rows']==0
results.append({'case':'partial_stdout_nonzero_query','passed':True})
(R/'raw/key-parser-tests.json').write_text(json.dumps(results,indent=2)+'\n')
print('Seven synthetic key-event cases passed.')
