import csv,json,re
from pathlib import Path
p=Path('D1/c1/part-flatcar.stored.tsv'); note=Path('D1/c1/part-flatcar.stored.notes.md')
rows=[r for r in csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t') if r['kind']=='L2:stored-outside-packages']
out=list(csv.DictReader(p.open(),delimiter='\t')); byid={r['id']:r for r in out}; changed=[]
def fix(i,d,s,w,b,reason,why):
 r=byid[rows[i]['id']]; old=r.copy();r.update(decision=d,sentences=s,what_it_does=w,basis=b,reason=reason)
 assert len(w.split())<=15 and len(reason.split())<=30
 if r!=old:
  changed.append(r['id'])
  with note.open('a') as f:f.write('\n### Correction '+r['id']+'\n'+old['decision']+' → '+d+'. '+why+'\n')
def mix(i,groups,w,why,s='S2.2-1,S2.2-2,S2.2-4,S3-2',b='raw:flatcar/raw/105-filesystem.out'):
 ms=json.loads(rows[i]['members']);assign={j:d for d,idx in groups.items() for j in idx}
 assert set(assign)==set(range(1,len(ms)+1))
 text='; '.join(d+'='+','.join(map(str,idx)) for d,idx in groups.items())+'. '+why
 fix(i,'MIXED',s,w,b,text,why)
 with note.open('a') as f:
  f.write('Corrected complete member map (supersedes earlier map):\n')
  for j,m in enumerate(ms,1):f.write(f'- {j}: `{m}` — {assign[j]}\n')
G='doc:https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh'
mix(8,{'UNKNOWN':[1,3],'MUST':[2,4]},'Supply GRUB modules plus retained image-construction inputs.','Modules execute; separate memdisk/configuration inputs lack established later consumers.','S2.2-10,S3-2',G)
for i in [9,11]:
 groups={d:[] for d in ['MUST','NOT','HOLE','UNKNOWN']}
 for j,m in enumerate(json.loads(rows[i]['members']),1):
  name=Path(m).name
  d='MUST' if name.endswith('.mod') or name=='core.img' else ('NOT' if name.endswith('.lst') else ('HOLE' if name=='mbr.bin' else 'UNKNOWN'))
  groups[d].append(j)
 mix(i,{d:idx for d,idx in groups.items() if idx},'Supply loader code, module indexes, saved boot bytes and image-construction inputs.','Code requires recording; indexes are program-local values; saved boot bytes conflict with history exemption; construction-input consumers are unknown.','S2.2-1,S2.2-6,S2.2-7,S2.2-10,S2.2-13,S3-2',G)
fix(10,'UNKNOWN','S3-1,S3-2','Retain initial configuration embedded during boot-image construction.',G,'Documentation establishes embedding into another image, but no later consumption of this separate installed copy.','Inspected grub_install.sh: grub-mkimage consumes load.cfg with --config; the separately retained copy has no established runtime consumer.')
fix(68,'UNKNOWN','S3-1,S3-2','Supply files copied into newly created account home directories.','doc:https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml','Copying is documented, but contents and subsequent execution of these particular templates are not established.','useradd documents copying templates, not executing them. The inventory has no contents of these templates.')
# Retain known member decisions instead of letting an unknown subgroup erase them.
mix(18,{'MUST':[3,4,7],'UNKNOWN':[1,2,5,6]},'Configure kernel audit rules and audit-daemon event handling.','Kernel rules affect system auditing; plugin and daemon setting values remain unavailable.')
mix(52,{'MUST':[2,3,5],'UNKNOWN':[1,4]},'Supply SELinux policy trees and policy-selection settings.','Policy trees supply system access controls; uncaptured selection and management values remain unknown.')
mix(72,{'MUST':[1],'NOT':[4],'UNKNOWN':[2,3]},'Supply TLS trust certificates, a directory marker and cryptographic settings.','Trust store serves multiple programs; marker is bookkeeping; cryptographic configuration values are uncaptured.')
mix(79,{'MUST':[12],'NOT':[6,15],'UNKNOWN':[1,2,3,4,5,7,8,9,10,11,13,14,16]},'Configure services and provide timer activation plus marker-only directories.','Timer enablement affects execution; marker directories are bookkeeping; actual service-configuration values are uncaptured.')
# Repair aggregate /etc mapping to agree with directly inspected directory contents.
i=13;old=byid[rows[i]['id']]; oldgroups={}
for d,seq in re.findall(r'(MUST|NOT|UNKNOWN|HOLE)=([0-9,]+)',old['reason']):oldgroups[d]=set(map(int,seq.split(',')))
ms=json.loads(rows[i]['members']); names=[Path(x).name for x in ms]
for name,d in {'skel':'UNKNOWN','binfmt.d':'NOT','kernel':'NOT','modules-load.d':'NOT','pam.d':'NOT','pkcs11':'NOT','polkit-1':'NOT','security':'NOT','sudoers.d':'NOT','tmpfiles.d':'NOT','xdg':'NOT'}.items():
 j=names.index(name)+1
 for ss in oldgroups.values():ss.discard(j)
 oldgroups.setdefault(d,set()).add(j)
mix(i,{d:sorted(ss) for d,ss in oldgroups.items()},old['what_it_does'],'Account/code/system effects require recording; markers/history/content are exempt; other uncaptured effects remain unknown.','S2.2-1,S2.2-2,S2.2-4,S2.2-6,S2.2-10,S2.2-15,S3-2')
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
print('\n'.join(changed))
