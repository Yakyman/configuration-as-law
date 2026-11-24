#!/usr/bin/python3
"""Recorded guest checks; native inspection uses existing fixed trusted queries."""
import hashlib,json,os,shlex,subprocess as sp,sys
from pathlib import Path
meta=json.loads(Path('/usr/local/share/radio-recording-expected.json').read_text())
assert os.geteuid()!=0 and Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
assert hashlib.sha256(Path('/usr/lib/confos/commands/nmcli').read_bytes()).hexdigest()==meta['draft_sha256']
assert Path('/usr/local/bin/nmcli').resolve()==Path('/usr/lib/confos/commands/nmcli')
def declaration():return Path('/state/declaration.conf').read_bytes()
def stable():return b''.join(line for line in declaration().splitlines(keepends=True) if shlex.split(line.decode(),comments=True)[:1]!=['network'])
def run(args,ok=True):
 p=sp.run(args,text=True,capture_output=True,timeout=25)
 print('RADIO COMMAND',args,'EXIT',p.returncode,'OUT',p.stdout,'ERR',p.stderr,flush=True)
 assert (p.returncode==0)==ok
 return p.stdout+p.stderr
def native(address):
 wifi=json.loads(run(['sudo','-n','confos','radio-inspect','wifi']))
 assert all(i['exit']==0 for i in wifi)
 assert ('Connected to ' in wifi[1]['stdout']) if address!='absent' else ('Not connected.' in wifi[1]['stdout'])
 assert 'type AP' in wifi[3]['stdout']
 ips=[a['local'] for i in json.loads(wifi[2]['stdout']) for a in i['addr_info'] if a['family']=='inet']
 assert ips==([] if address=='absent' else [address]),ips
 objects=json.loads(run(['sudo','-n','confos','radio-inspect','bluetooth']))
 adapters=[x['org.bluez.Adapter1']['Address'] for x in objects.values() if 'org.bluez.Adapter1' in x]
 assert sorted(adapters)==['00:AA:01:00:00:00','00:AA:01:01:00:01']
 assert len([x for x in objects.values() if x.get('org.bluez.Device1',{}).get('Paired')])==2
 files=json.loads(run(['sudo','-n','confos','radio-inspect','files']))
 infos=[i for i in files if i['path'].startswith('/var/lib/bluetooth/') and i['path'].endswith('/info')]
 assert len(infos)==2
 for i in infos:
  relative=i['path'].removeprefix('/var/lib/bluetooth/')
  expected=sp.check_output(['sudo','-n','sha256sum','/usr/lib/confos/radio/bluez/'+relative],text=True).split()[0]
  assert i['sha256']==expected
 print('RADIO_NATIVE_WIFI_BT_PASS',address,flush=True)
def request(stage):
 if stage=='add':return ['connection','add','type','wifi','ifname','wlan1','autoconnect','yes','con-name','wifi',
  'ssid',bytes.fromhex(meta['fixture']['wifi']['ssid_hex']).decode('ascii'),'wifi-sec.key-mgmt','wpa-psk',
  'wifi-sec.proto','rsn','wifi-sec.pairwise','ccmp','wifi-sec.group','ccmp','wifi-sec.psk',meta['fixture']['wifi']['psk'],
  'ipv4.method','manual','ipv4.addresses','192.0.2.2/24']
 if stage=='change':return ['connection','modify','id','wifi','ipv4.addresses','192.0.2.3/24']
 assert stage=='remove';return ['connection','delete','id','wifi']
def recorded(stage):
 rows=[r for line in declaration().decode().splitlines() if (r:=shlex.split(line,comments=True))]
 assert [' '.join(r) for r in rows if r[0] in ('radio-fixture','bluetooth-pair')]==meta['radio_rows']
 networks=[r for r in rows if r[0]=='network']
 if stage=='remove':assert not networks
 else:
  assert len(networks)==1 and networks[0][1]=='wifi'
  row=networks[0];source=Path('/state')/row[3]
  data=sp.check_output(['sudo','-n','cat',str(source)])
  assert hashlib.sha256(data).hexdigest()==row[2]
  obj=json.loads(data)
  assert obj=={'format':1,'fixture':'lab','ssid_hex':meta['fixture']['wifi']['ssid_hex'],'psk':meta['fixture']['wifi']['psk'],
               'address':'192.0.2.2/24' if stage=='add' else '192.0.2.3/24'}
  assert sp.check_output(['sudo','-n','stat','-c','%u %a',str(source)],text=True).strip()=='0 600'
  print('RADIO_EXACT_INPUT',row[3],repr(data),flush=True)
 print('RADIO_RECORDED_EXACT_PASS',stage,hashlib.sha256(declaration()).hexdigest(),flush=True)
mode=sys.argv[1]
if mode=='stable-hash':print(hashlib.sha256(stable()).hexdigest())
elif mode=='native':native(sys.argv[2])
elif mode=='request':
 # Inherit stdout: the worker cuts on the actual recorder's RECORDED line.
 raise SystemExit(sp.call(['sudo','-n','/usr/local/bin/nmcli',*request(sys.argv[2])]))
elif mode=='verify':
 recorded(sys.argv[2]);native(sys.argv[3]);assert hashlib.sha256(stable()).hexdigest()==sys.argv[4]
elif mode=='repeat':
 before=declaration();run(['sudo','-n','/usr/local/bin/nmcli',*request(sys.argv[2])]);assert declaration()==before
 recorded(sys.argv[2]);native(sys.argv[3])
elif mode=='authority':
 print('RADIO_CALLER',os.getuid(),os.geteuid(),Path('/proc/self/attr/current').read_text().strip(),flush=True)
 before=declaration()
 out=run(['/usr/local/bin/nmcli',*request('add')],False);assert 'permission denied' in out
 assert run(['sudo','-n','id','-u']).strip()=='0'
 assert declaration()==before
 for args in (['device','wifi','connect','unrepresented'],['connection','modify','id','absent','ipv4.method','auto']):
  run(['sudo','-n','/usr/local/bin/nmcli',*args],False);assert declaration()==before
 native('absent')
else:raise AssertionError(mode)
