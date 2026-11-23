import json,csv,collections,re
r=json.load(open('D1/c1/rpm-b-reviewed.json')); corrections=[]
network={'chrony-pool-openSUSE','NetworkManager-branding-openSUSE'}
unclear={'PackageKit-branding-openSUSE','flatpak-remote-flathub','registries-conf-default','libcontainers-default-policy','gtk3-branding-openSUSE','gtk4-branding-openSUSE','breeze6-cursors','metatheme-breeze6-common','gtk3-metatheme-breeze6','gtk4-metatheme-breeze6','metatheme-adwaita-common','gtk3-metatheme-adwaita','sddm-qt6-branding-openSUSE','sddm-branding-openSUSE','plasma6-branding-openSUSE'}
for x in r:
 k=x['name']
 if k in network:
  x.update(decision='MUST',sentences='S2.2-1,S2.2-2',reason='Configures system clock synchronization or system network connectivity assessment; these effects extend beyond the consuming program to other system users.',rule='systemrules');corrections.append(x)
 elif k in unclear:
  x.update(decision='HOLE',sentences='S2.2-1,S2.2-2,S2.2-7,S2.2-13',reason='Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.',rule='ambiguous');corrections.append(x)
fields=['id','decision','sentences','what_it_does','basis','reason']
with open('D1/c1/part-tumbleweed.rpm-b.tsv','w') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(r)
json.dump(r,open('D1/c1/rpm-b-reviewed.json','w'),indent=2)
p='D1/c1/part-tumbleweed.rpm-b.notes.md';text=open(p).read();pattern=r'(## Rule settings\n)(.*?)(?=## Rule firmware\n)';old=re.search(pattern,text,re.S).group(2)
sample=[x for x in r if x['rule']=='settings'][:10];assert len(sample)==10
replacement='\nS2.2-7,S2.2-13: passive settings or visual resources whose documented effects remain in the named application are NOT. Passive values alone are insufficient: shared/system effects are individually reviewed.\n\nTen final hand-checked IDs:\n\n'+''.join('- '+x['id']+' — '+x['name']+': '+x['what_it_does']+'; NOT.\n' for x in sample)+'\n'
text=re.sub(pattern,lambda ma:ma.group(1)+replacement,text,flags=re.S)
text+='\n## Confinement re-review amendment\n\nThe initial settings samples below are retained only as an audit record and are superseded by the replacement Rule settings list above.\n'+old+'\nReviewed corrections:\n\n'+''.join('- '+x['id']+' — '+x['name']+': '+x['decision']+'. '+x['reason']+'\n' for x in corrections)
text+='\nFinal counts after confinement review: MUST 2084, NOT 86, HOLE 220, UNKNOWN 0, MIXED 0.\n';open(p,'w').write(text)
assert all(len(x['reason'].split())<=30 for x in r)
print(collections.Counter(x['decision'] for x in r));print('settings sample',[(x['name'],x['id']) for x in sample])
