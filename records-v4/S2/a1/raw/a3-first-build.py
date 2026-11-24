import csv,json,collections
from pathlib import Path
csv.field_size_limit(10000000)
root=Path('.')
sample=list(csv.DictReader(open(root/'S2/sample/sample-A3.tsv'),delimiter='\t'))[:150]
inventories={m:{r['id']:r for r in csv.DictReader(open(root/f'A3/in/raw/{m}/objects.tsv'),delimiter='\t')} for m in ('developer','gaming')}
rows=[]; evidence=[]; rules=collections.defaultdict(list)
for n,s in enumerate(sample,1):
 m=s['machine']; oid=s['id'].split('-',1)[1]; r=inventories[m][oid]; obj=json.loads(r['members'])
 assert r['name']==s['name'].replace(chr(92)*2,chr(92)) and r['kind']==s['kind'].split(':',1)[1]
 members=[]
 if 'file' in obj:
  members=list(csv.DictReader(open(root/f'A3/in/raw/{m}'/obj['file']),delimiter='\t'))
  assert obj['complete'] and len(members)==obj['count']
 f='FOLLOWS'; sent='S8.2-5'; rule=''; reason=''
 if r['kind'].startswith('firewall'):
  rule='live-firewall';reason='Live kernel firewall state is not a separate object; it belongs to the firewall program or access-rule setting under S8.2-5.'
 elif r['kind']=='process':
  rule='process'; exe=obj['record'].split('\\t')[-1]
  if exe.endswith('unknown'):reason='Observed process exists only during execution. Its executable identity is unknown, but every possible identity leaves the sampled decision RUNTIME.'
  else:reason=f'Observed {exe.rsplit("/",1)[-1]} process belongs to its executable, covered as INSTALLED-PACKAGE; the process is not a separate object.'
 elif r['kind']=='module-name':
  rule='loaded-module';reason='Loaded kernel module instance exists during execution and belongs to the installed kernel module; S8.2-5 removes separate-object status.'
 elif r['kind']=='port':
  rule='open-port';reason='Observed listening TCP port is explicitly a runtime object under S8.2-5, belonging to its creating service or program.'
 elif r['kind']=='timer':
  rule='live-timer';reason='The next/last activation observation is runtime scheduling state, belonging to the timer service setting rather than a separate stored unit file.'
 elif r['kind']=='package':
  sent='S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16'
  if obj['reason']=='explicit':
   assert s['decision']=='INSTALLED-OWN';rule='explicit-package';reason='Installer inventory identifies an explicitly installed package. Question one decides installed object; its own declaration line records that package.'
  else:
   assert obj['reason']=='dependency' and s['decision']=='INSTALLED-DERIVED';rule='dependency-package';reason='Installer records dependency installation. Question one decides installed object; S8.2-16 expressly covers a dependency through its recorded parent package.'
 elif s['decision']=='RUNTIME':
  if n==20:rule='rpc-pseudo';reason='Observed filesystem magic identifies RPC pipefs, a kernel communication filesystem; its objects exist during execution and belong to the RPC subsystem.'
  elif n==73:rule='namespace';reason='The member has NSFS filesystem magic: a live network namespace handle, not persistent file contents; it belongs to the container network program.'
  else:
   assert all(a['persistence']=='runtime' for a in members);rule='volatile-group';reason='Every listed immediate member is on a runtime filesystem. These transient objects belong to the creating service/program, not separate persistent objects.'
 elif n in (105,144):
  rule='cups-hardlink';sent='S8.2-7,S8.2-8,S8.2-16';reason='Device/inode matches unchanged package-owned backend-available files. These are the same received package objects; their package line covers them.'
 elif n in (128,130):
  rule='compiled-python';sent='S8.2-9,S8.2-10,S8.2-16,S8.2-23';reason='Bytecode members correspond to installed source modules; saved package post-installation script compiles them. Executable compiled copies are covered by the source package line.'
 elif n==122:
  rule='archive-unresolved';f='FACT-UNKNOWN';sent='S8.2-7,S8.2-9,S8.2-15';reason='Missing: whether this updater archive is part of an installed package, and whether its contents are executed. Download logging alone does not establish RECORD.'
 elif '.bun/install/cache/' in r['name']:
  rule='manifest-cache';sent='S8.2-15,S8.2-23';reason='These hashed .npm files are binary registry-response metadata, read as values. They are cache records, despite the collector shebang flag.'
 elif n==3:
  rule='go-action-index';sent='S8.2-15,S8.2-23';reason='All five members are 175-byte Go action-index files ending -a, containing output hashes and metadata rather than executable build outputs; program records.'
 elif n in (17,26):
  rule='reflog';sent='S8.2-15';reason='Immediate members are local reference-update logs written by Git, not fetched repository objects or executable hooks; program records.'
 elif n==136:
  rule='execution-log';sent='S8.2-15';reason='All eighteen members are captured standard-output/error execution logs, corroborated by saved action logs; program records.'
 else:
  assert n in (9,27,33,55,65,69,89)
  rule='cache-structure';sent='S8.2-15,S8.2-23';reason='Listed immediate members are cache directories, metadata markers, locks or indexes created by their programs. Descendant files are not members of this group.'
 assert reason and len(reason.split())<=30,(n,reason)
 rows.append([s['id'],'A3',s['decision'],f,sent,reason]);rules[rule].append(s['id'])
 refs=[f'A3/in/raw/{m}/objects.tsv#{oid}']
 if members:refs.append(f'A3/in/raw/{m}/'+obj['file'])
 refs.extend(f'A3/in/raw/{m}/'+p for p in r['evidence'].split(';'))
 evidence.append(f'| {n} | {s["id"]} | {rule} | '+ '; '.join('`'+z+'`' for z in refs)+' |')
with open(root/'S2/a1/raw/a3-first.tsv','w') as o:
 w=csv.writer(o,delimiter='\t',lineterminator='\n');w.writerow(['id','source','agreed_decision','finding','sentences','reason']);w.writerows(rows)
with open(root/'S2/a1/raw/a3-first-evidence.md','w') as o:
 o.write('# Evidence index\n\nEvery assigned row was matched to its original inventory ID; all referenced group member tables were read completely.\n\n| Row | ID | Rule | Evidence |\n| --- | --- | --- | --- |\n'+'\n'.join(evidence)+'\n')
print(collections.Counter(r[3] for r in rows))
print('\n'.join(k+': '+', '.join(v[:10]) for k,v in rules.items()))
