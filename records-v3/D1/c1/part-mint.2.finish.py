import csv,json,re,collections
r=[r for r in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if r['kind']=='L1:package:dpkg-query'][635:1270]; byname={x['name'].split(':')[1]:x for x in r}
p='D1/c1/part-mint.2.tsv';existing={x['id'] for x in csv.DictReader(open(p),delimiter='\t')}
extra={
'libllvm20':('Provides executable compiler and toolchain library routines.','https://packages.ubuntu.com/noble-updates/libllvm20','Modular compiler and toolchain technologies, runtime library'),
'libmuffin0':('Provides native window-management and compositing routines.','https://raw.githubusercontent.com/linuxmint/muffin/master/debian/control','window and compositing manager (shared library)'),
'libpam-fingwit':('Selects when fingerprint authentication may be used by login services.','https://github.com/xapp-project/fingwit','Fingwit uses two PAM modules:')}
with open(p,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for n,(what,url,quote) in extra.items():
  if byname[n]['id'] not in existing:w.writerow([byname[n]['id'],'MUST','S2.2-1,S2.2-2,S2.2-10',what,'doc:'+url,'The native module executes with its calling program’s rights and supplies system capabilities.'])
rows=list(csv.DictReader(open(p),delimiter='\t'));m=json.load(open('D1/c1/part-mint.2.metadata.json'));fl=json.load(open('D1/c1/part-mint.2.filelists.json'));ind=json.load(open('D1/c1/part-mint.2.individual.json'))
notes=['# Classification c1: package slice 2','', 'Scope: package-kind indices 635 through 1269 inclusive. Installation identity comes from the assigned inventory; operational function comes from the cited public package descriptions and file lists. No removal or execution probe was performed. Package contents are considered together as the single inventoried package object; this is not a grouped directory row.','', '## Exact deciding sentences','']
ids=['S2.2-1','S2.2-2','S2.2-3','S2.2-4','S2.2-7','S2.2-9','S2.2-10','S2.2-11','S2.2-13','S2.2-15','S3-1','S3-2']
for line in open('SENTENCES.md'):
 if any(line.startswith('- **'+s+'**') for s in ids):notes.append(line.strip())
notes += ['', '## Public documentation and method','', 'The primary package-index sources are https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz and https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz . Selected Description fields are retained in `part-mint.2.metadata.json`. Per-package URLs and exact description quotations appear below. Base-release documentation establishes package function, not an assertion that an installed update has the base version. Additional source URLs cover packages absent from the base indexes.', '', 'Shared-library semantics: https://www.debian.org/doc/debian-policy/ch-sharedlibs.html : “the dynamic linker knows that library must be loaded at runtime.” Native library routines execute in the caller, rather than a confined web-page or virtual-machine interface.', '', 'Rule E (homogeneous executable packages): a documented native runtime library, interpreter module, or executable utility supplies runnable operations. S2.2-10 requires caller-rights library/module code; S2.2-9 requires standalone programs; S2.2-1 and S2.2-2 independently cover their removed capabilities. This rule is applied only after reading each package description. Data, development, common, theme, documentation and transitional packages were withheld and inspected individually. The same semantic rule covers libraries and utilities; their sentence fields distinguish the relevant explicit clause.', '', 'Ten manually checked Rule E rows (id, package, checked role):']
checks=['libefiboot1t64','libelf1t64','libencode-locale-perl','libexpat1','libfdisk1','libgdk-pixbuf2.0-bin','libglib2.0-bin','libgtk-3-bin','libimobiledevice-utils','libjxl-tools']
for n in checks:notes.append(f'- {byname[n]["id"]}: {n}; “{m[n]["Description"].splitlines()[0]}”. This is executable runtime/module/utility functionality, not passive package data.')
notes += ['', 'Additional manual utility checks to make both executable forms independently auditable:']
for n in ['libgsf-bin','libgtk2.0-bin','liblcms2-utils','liblouisutdml-bin','libmbim-proxy','libmtp-runtime','libnotify-bin','libpam-modules-bin','libpaper-utils','libqmi-proxy']:
 notes.append(f'- {byname[n]["id"]}: {n}; “{m[n]["Description"].splitlines()[0]}”. Executable utility or helper.')
notes += ['', '## Individual exceptions','', 'Every entry below was decided after inspecting its own published file list; similar wording is not a rule inferred from package suffixes. File-list evidence is retained in `part-mint.2.filelists.json`. Quotes identify representative actual contents, excluding routine package documentation where operational files exist. Documentation-only lists were inspected completely.','']
for n,v in ind.items():
 files=fl[n]['files'];oper=[f for f in files if not f.startswith('/usr/share/doc/')];quote='; '.join((oper or files)[:2]);notes.append(f'- {byname[n]["id"]}, {n}: {v[0]}. {v[4]} Source: {fl[n]["url"]}; file-list quote: “{quote}”.')
notes += ['', 'MathJax execution uncertainty is supported by https://docs.mathjax.org/en/v2.7/ : “MathJax on NodeJS” and “works in all modern browsers.” The installed inventory does not select the execution context. Interpreter initialization resources likewise do not establish their installed confinement mode merely by their presence.', '', 'HOLE rows concern the actual classification boundary for operational location databases; they do not ask how a system should transfer or preserve state. The text supplies no boundary between geographical database content and capability-defining lookup data.', '', '## Per-package function quotations','']
for x in r:
 n=x['name'].split(':')[1]
 if n in extra:url,quote=extra[n][1:]
 else:
  url='https://packages.ubuntu.com/noble/'+n;quote=m[n]['Description'].splitlines()[0]
  if n=='libnewt0.52':quote='text mode windowing with slang'
 notes.append(f'- {x["id"]}: {url} — “{quote}”.')
counts=collections.Counter(x['decision'] for x in rows)
assert len(rows)==len(r)==635
assert {x['id'] for x in rows}=={x['id'] for x in r}
assert len({x['id'] for x in rows})==635
for x in rows:
 assert x['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'}
 assert len(x['what_it_does'].split())<=15,(x['id'],'what')
 assert len(x['reason'].split())<=30,(x['id'],'reason')
notes += ['', '## Mechanical verification','', 'Exactly 635 assigned ids, each once; no additions or omissions; all decisions valid; field word limits verified.', '', ', '.join(f'{k}: {counts[k]}' for k in ['MUST','NOT','HOLE','UNKNOWN','MIXED'])+'.']
open('D1/c1/part-mint.2.notes.md','w').write('\n'.join(notes)+'\n')
print(dict(counts))
