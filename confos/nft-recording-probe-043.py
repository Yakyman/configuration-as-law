import subprocess as s,hashlib,json,sys
from pathlib import Path
mode=sys.argv[1] if len(sys.argv)>1 else 'before'
def run(args,ok=True):
 p=s.run(args,text=True,capture_output=True);print('COMMAND',args,'EXIT',p.returncode,'STDOUT',p.stdout,'STDERR',p.stderr,flush=True)
 assert (p.returncode==0)==ok
 return p.stdout+p.stderr
def declaration():return Path('/state/declaration.conf').read_bytes()
def rules():return json.loads(run(['sudo','-n','nft','-j','-a','list','ruleset']))
def selected():return [e['rule'] for e in rules()['nftables'] if 'rule'in e and any(x.get('match',{}).get('right')==32124 for x in e['rule']['expr'])]
verdict=sys.argv[2] if len(sys.argv)>2 else 'accept'
assert verdict in ('accept','drop')
add=['nft','add','rule','inet','confos','input','tcp','dport','32124',verdict]
print('MODE',mode,flush=True)
status=run(['confos','status']).strip()
if mode!='before':assert status=='APPLIED '+hashlib.sha256(declaration()).hexdigest()
assert 'confos-session (enforce)' in run(['sudo','-n','cat','/proc/self/attr/current'])
if mode=='before':
 before=declaration();native=rules()
 run(['nft','--version']);run(['sudo','-n','nft','list','tables']);run(['nft','list','ruleset'],False)
 assert 'permission denied' in run(add,False)
 for args in (['sudo','-n','nft','add','rule','ip','other','input','accept'],['sudo','-n','nft','add','rule','inet','confos','input','tcp','dport','0','accept'],['sudo','-n','nft','delete','rule','inet','confos','input','handle','999999']):run(args,False)
 assert declaration()==before
 run(['sudo','-n',*add]);after=declaration();assert after!=before and ('add rule inet confos input tcp dport 32124 '+verdict).encode() in after
 run(['sudo','-n',*add]);assert declaration()==after and rules()==native
 run(['sudo','-n','/usr/sbin/nft','add','rule','inet','confos','input','tcp','dport','32125','accept'],False)
 assert rules()==native
elif mode=='applied':
 rule=selected();assert len(rule)==1 and rule[0]['expr'][-1]=={verdict:None}
 before=declaration()
 duplicate=before+("rule duplicate 'add rule inet confos input tcp dport 32124 "+verdict+"'\n").encode()
 p=s.run(['sudo','-n','tee','/state/declaration.conf'],input=duplicate,capture_output=True);assert p.returncode==0
 output=run(['sudo','-n','nft','delete','rule','inet','confos','input','handle',str(rule[0]['handle'])],False)
 assert 'ambiguous declaration rule ownership' in output and declaration()==duplicate
 p=s.run(['sudo','-n','tee','/state/declaration.conf'],input=before,capture_output=True);assert p.returncode==0
 assert declaration()==before
elif mode=='remove':
 rule=selected();assert len(rule)==1 and rule[0]['expr'][-1]=={verdict:None}
 args=['nft','delete','rule','inet','confos','input','handle',str(rule[0]['handle'])]
 before=declaration();run(args,False);assert declaration()==before
 run(['sudo','-n',*args]);after=declaration();assert after!=before and b'32124' not in after
 run(['sudo','-n',*args]);assert declaration()==after and len(selected())==1
elif mode=='verified':
 rule=selected();assert len(rule)==1 and rule[0]['expr'][-1]=={verdict:None}
 assert ('add rule inet confos input tcp dport 32124 '+verdict).encode() in declaration()
elif mode=='removed':assert not selected() and b'32124' not in declaration()
print('NFT',mode,'PASS DECLARATION',hashlib.sha256(declaration()).hexdigest(),flush=True)
