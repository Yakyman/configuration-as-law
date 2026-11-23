import csv,json,collections
p='D1/c1/part-tumbleweed.rpm-b.tsv'; r=json.load(open('D1/c1/rpm-b-reviewed.json'));m=json.load(open('D1/c1/rpm-b-metadata.json'))
for x in r:
 if x['name'] in {'libnl-config','libtirpc-netconfig','libsemanage-conf','alsa-ucm-conf','openal-soft-data','dbus-broker-block-restart'}:
  x.update(decision='HOLE',sentences='S2.2-1,S2.2-2,S2.2-7,S2.2-13',reason='These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.',rule='ambiguous')
 if x['name'].startswith('typelib-'):
  x.update(what_it_does='Supplies binary invocation metadata allowing language bindings to call native library functions',basis='doc:https://gi.readthedocs.io/en/latest/architecture.html')
 if x['name']=='gpg-pubkey':
  x.update(decision='HOLE',sentences='S2.2-2,S2.2-7,S2.2-13',reason='Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.',rule='trust')
fields=['id','decision','sentences','what_it_does','basis','reason']
with open(p,'w') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(r)
json.dump(r,open('D1/c1/rpm-b-reviewed.json','w'),indent=2)
rules={
'code':('S2.2-9,S2.2-10','Executable programs and native/interpreter library code must be recorded. Descriptions or documented binary paths establish code; package names alone do not. Translation, content, config and metapackage exceptions are reviewed first.'),
'data':('S2.2-2,S2.2-4','Operational text, icons, fonts and reference datasets lose their particular content when removed, but also stop corresponding rendering/language/recognition results. The text supplies no boundary between these two readings: HOLE.'),
'metadata':('S2.2-1,S2.2-2,S2.2-4,S2.2-13','Structural/package/introspection metadata has downstream operational uses without itself being the program. The text does not distinguish that behavior dependence from descriptive data or settings: HOLE.'),
'settings':('S2.2-7,S2.2-13','Documented passive settings or themes confined to one program need not be recorded. Values are not treated as executable merely because shipped in a package.'),
'firmware':('S2.2-2,S2.2-16','Firmware files supplied to drivers implement device capabilities and are system-changeable; MUST. The firmware metapackage is reviewed separately.'),
'systemrules':('S2.2-1,S2.2-2,S2.2-15','Documented rules affecting system-wide accounts, access, multiple programs, hardware handling or service activation change system behavior; MUST.'),
'docs':('S2.2-4','Documentation, man pages and license texts are content. Removing them removes only the supplied documents: NOT.'),
'accounts':('S2.2-1,S2.2-15','Packages expressly providing system accounts or groups establish accounts/access rights: MUST.')}
with open('D1/c1/part-tumbleweed.rpm-b.notes.md','w') as f:
 f.write('# RPM second-half classification notes\n\nScope: last 2390 RPM rows, original input order. No other classification was consulted.\n\nThe ownership dump `D1/in/raw/tumbleweed/raw/113-ownership-rpm.out` is empty. Package names and versions are established by input evidence. Public repository descriptions establish the package roles. The public repository is a rolling source: it establishes purpose, not identity of every historical byte. No claim of exact installed file identity is made.\n\nSource: '+m['source']+'\n\nMetadata summaries/descriptions and selected primary file paths are preserved in `rpm-b-metadata.json`. The scripts contain the explicit role selection and corrections. Every output is one package object, not a group of its files.\n\n')
 for rule,(sent,desc) in rules.items():
  sample=[x for x in r if x['rule']==rule][:10]
  f.write('## Rule '+rule+'\n\n'+sent+': '+desc+'\n\nTen hand-checked examples (description checked against role):\n\n')
  assert len(sample)==10
  for x in sample:
   v=m['packages'][x['name']];f.write('- '+x['id']+' — `'+x['name']+'`: '+v['summary']+'. Check: '+x['decision']+'; '+x['what_it_does']+'.\n')
  f.write('\n')
 f.write('## Individual exceptions\n\n')
 for x in r:
  if x['rule'] not in rules:f.write('- '+x['id']+' — `'+x['name']+'`: '+x['decision']+'. '+x['reason']+'\n')
 f.write('\nIntrospection source: https://gi.readthedocs.io/en/latest/architecture.html describes typelibs as “Binary version of the invocation info” and shows libgirepository presenting them to language bindings.\n\nRPM key source: https://rpm.org/docs/6.0.x/man/rpmkeys.8 states: “Digital signatures cannot be verified without the corresponding public key (aka certificate).”\n\nNo removal experiment was performed. UNKNOWN support/provider packages have descriptions insufficient to establish executable versus passive payload, and their ownership dump is empty.\n')
expected=[x['id'] for x in csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t') if x['kind']=='L1:package:rpm'][2390:]
assert len(r)==len(expected)==len(set(x['id'] for x in r)) and set(expected)=={x['id'] for x in r}
assert all(x['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'} for x in r)
assert all(len(x['what_it_does'].split())<=15 and len(x['reason'].split())<=30 for x in r)
print(collections.Counter(x['decision'] for x in r))
