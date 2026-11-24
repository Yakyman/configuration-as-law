import csv,json,collections,base64,glob
from pathlib import Path
csv.field_size_limit(10000000)
base=Path('D1/in/raw/alma'); out=Path('S2/a1/raw')
r=list(csv.DictReader(open('S2/sample/sample-D1.tsv'),delimiter='\t'))[:150]
o={x['id']:x for x in csv.DictReader(open(base/'objects.tsv'),delimiter='\t')}
p=collections.defaultdict(list)
for x in csv.DictReader(open(base/'package-files.tsv'),delimiter='\t'):p[x['path']].append(x)
fs={d['path']:d for l in open(base/'raw/0004-filesystem.out') if 'path' in (d:=json.loads(l))}
assert fs['/lib']['target']=='usr/lib'
pol={}
for f in glob.glob(str(base/'raw/*metadata-read*.out')):
 for l in open(f):
  try:d=json.loads(l);s=base64.b64decode(d['data']).decode()
  except:continue
  for x in r:
   if x['kind']=='L1:polkit-action' and 'id="'+x['name']+'"' in s:pol[x['id']]=(d['path'],f)
rows=[];rules=collections.defaultdict(list);evidence=[]
for x in r:
 a=o[x['id'][5:]];m=json.loads(a['members']);kind=a['kind'];name=a['name'];assert name==x['name'];assert kind==x['kind'].split(':',1)[1]
 finding='FOLLOWS';sent='S8.2-5';proof=a['evidence']; rule=kind
 if kind=='package':
  sent='S8.1-6,S8.2-7,S8.2-8,S8.2-16'
  if m['manager']=='rpm':
   assert m['reason']=='dependency' and x['decision']=='INSTALLED-DERIVED'
   reason='Installed package; retained dependency reason supports coverage by the recorded package from which installation obtained it.';rule='dependency-package'
  else:
   assert m['native_package_ids'] and x['decision']=='INSTALLED-PACKAGE'
   files=[v for k,v in p.items() if k.startswith(m['location']+'/')];assert files and all(z['integrity']=='unchanged' for v in files for z in v)
   code_root = {'python_linux_procfs-0.7.4.dist-info':'procfs', 'argcomplete-3.2.2.dist-info':'argcomplete', 'pip-23.3.2.dist-info':'pip'}.get(m['location'].rsplit('/',1)[-1])
   root=m['location'].rsplit('/',1)[0]+'/'+code_root if code_root else m['location']
   observed=[q for q,z in fs.items() if q.startswith(root+'/') and z['type']!='directory']
   assert observed and all(any(t['integrity']=='unchanged' and t['package'] in m['native_package_ids'] for t in p[q]) for q in observed)
   reason='Installed language package contents and metadata match unchanged native-package members; the containing package line can cover it.';rule='nested-package';proof+=';package-files.tsv;native_package_ids='+','.join(m['native_package_ids'])+';content_root='+root+';verified_content_files='+str(len(observed))
 elif kind=='process':reason='A process exists only during operation; its creating program determines the inherited decision, although its executable identity was not captured.'
 elif kind in ['driver','module-name']:reason='Kernel-created sysfs runtime representation; inherits the kernel program decision rather than requiring a separate line.';rule='sysfs-runtime'
 elif kind.startswith('firewall-'):reason='Live kernel ruleset object; inherits its creating firewall program or network setting decision rather than requiring a separate line.';rule='firewall-runtime'
 elif kind=='service':reason='The captured not-found inactive unit is service-manager runtime state; inherits the service manager decision.'
 elif kind=='polkit-action':
  path,doc=pol[x['id']];assert any(z['integrity']=='unchanged' for z in p[path]);sent='S8.2-6,S8.2-7,S8.2-8,S8.2-16';reason='The action occurs in a retained unchanged package policy; question one precedes access-setting classification.';proof=doc+';package-files.tsv:'+path
 elif kind in ['unit-file','user-unit-file','access-rule']:
  path=name if kind=='access-rule' else '/usr/lib/systemd/'+('user/' if kind=='user-unit-file' else 'system/')+name.removeprefix('user:')
  assert any(z['integrity']=='unchanged' for z in p[path]);sent='S8.2-6,S8.2-7,S8.2-8,S8.2-16';reason='Exact file is an unchanged package member; question one wins even when the file supplies settings or code.';rule='unchanged-file';proof+=';package-files.tsv:'+path
 elif kind=='stored-ownership-unresolved':
  members=list(csv.DictReader(open(base/m['file']),delimiter='\t'));assert len(members)==m['count'];proof+=';'+m['file']
  if x['decision']=='INSTALLED-PACKAGE':
   for child in members:
    cp=child['path'];cp=cp.removeprefix('/usr') if cp.startswith('/usr/lib/modules/') else cp
    assert any(z['integrity']=='unchanged' for z in p[cp]),cp
   sent='S8.2-6,S8.2-7,S8.2-8,S8.2-16';reason='All enumerated module files match unchanged package members through the captured lib symlink; the package line covers them.';rule='unchanged-module-group';proof+=';package-files.tsv;raw/0004-filesystem.out:lib-symlink'
  elif x['decision']=='RUNTIME':
   assert fs[name]['persistence']=='runtime' and all(z['persistence']=='runtime' for z in members)
   reason='Directory and all enumerated members have runtime persistence; their creating program or setting supplies the inherited decision.';rule='runtime-storage'
  elif x['decision']=='RECORD':
   sent='S8.2-6,S8.2-15,S8.2-2';rule='record-storage'
   if any(z['path'].endswith('.body') for z in members):
    finding='FACT-UNKNOWN';sent='S8.2-6,S8.2-9,S8.2-15';reason='Cached response body contents and executability are uncollected; a cache name and non-executable mode do not exclude question two.';rule='opaque-http-body'
   else:reason='Enumerated members are cache indexing directories, cache metadata, database state, or audit log records, without an earlier affirmative question.'
  else:raise ValueError(x)
 else:raise ValueError(x)
 assert len(reason.split())<=30
 rows.append(dict(id=x['id'],source='D1',agreed_decision=x['decision'],finding=finding,sentences=sent,reason=reason));rules[rule].append(x['id']);evidence.append((x['id'],rule,proof))
with open(out/'d1-first.tsv','w') as f:
 w=csv.DictWriter(f,fieldnames=['id','source','agreed_decision','finding','sentences','reason'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
notes='''# Review notes: first 150 D1 sample rows

Every sampled ID was matched, without its source prefix, to `D1/in/raw/alma/objects.tsv`. The two submitted sentence sets were read but not used as proof. All member files were opened and every immediate member checked. No recursive group membership was invented. All references below are relative to `D1/in/raw/alma/` unless already prefixed D1.

## Literal rules and evidence

- Dependency packages: S8.2-7 and S8.2-8 decide the kind; S8.2-16 explicitly permits dependency coverage. The retained reason is dependency, including weak dependency. This tests the permissible recording route, not whether an existing declaration actually covers it.
- Nested packages: Exact native manifests establish package provenance for both metadata and actual content; all observed non-directory content paths were joined and are unchanged. native_package_ids alone is not used as containment proof. Question one decides because these are installed packages. S8.2-16 permits their native package line.
- Unchanged files and module groups: S8.2-7/8/16. Exact manifest integrity is unchanged. Module paths require the observed `/lib` symlink target `usr/lib` in `raw/0004-filesystem.out`; this is an observed alias, not guessed path equivalence.
- Policy actions: decoded retained metadata contains the exact action ID inside an unchanged package policy. S8.2-6 prevents replacing the first question with the later access-setting question.
- Processes, sysfs representations, live firewall rules, service-manager state, and runtime storage: S8.2-5 precedes the four questions. A missing executable name does not alter RUNTIME, because all possible creator identities give that label. Creator decisions are inherited rather than independently reconstructed here.
- Records: S8.2-15, after earlier questions, covers metadata/indexing directory objects, databases and logs. An immediate child directory is not silently expanded into its descendants. Four groups include actual opaque HTTP body files; their contents were not captured, so question two cannot be excluded from mode bits or names. These are FACT-UNKNOWN, not a text gap.

## Public documentation consulted

- https://docs.kernel.org/filesystems/sysfs.html : “sysfs is a RAM-based filesystem initially based on ramfs.” The captured query scripts list sysfs directories, not stored module binaries.
- https://docs.npmjs.com/cli/commands/npm-cache/ : “npm stores cache data in an opaque directory within the configured `cache`, named `_cacache`.” This identifies cache layout but does not prove opaque payload executability.
- https://pip.pypa.io/en/stable/topics/caching/ : “This cache functions like a web browser cache.” Its HTTP-response section and version-23.3 http-v2 description identify the layout; exact response contents remain unavailable.
- https://github.com/linux-audit/audit-userspace/blob/master/init.d/auditd.conf : “log_file = /var/log/audit/audit.log”. Retained members identify the log, not executable material.

`D1/in/control/alma/actions-logs/language_program.log` documents successful npm installation during the captured cache creation interval. No actual payload contents were inferred from that temporal correspondence.

## Manual checks per homogeneous rule

The source rows, member lists and relevant integrity joins were visually inspected before applying these rules. Lists below contain ten IDs or the whole rule when smaller.

'''
for rule,ids in rules.items():notes+='- '+rule+' ('+str(len(ids))+' rows): '+', '.join(ids[:10])+'.\n'
notes+='\n## Per-row evidence index\n\n| ID | Rule | Evidence |\n|---|---|---|\n'
for ident,rule,proof in evidence:notes+='| '+ident+' | '+rule+' | '+proof+' |\n'
notes+='\nCounts: '+str(dict(collections.Counter(x['finding'] for x in rows)))+'\n'
(out/'d1-first-notes.md').write_text(notes)
print(collections.Counter(x['finding'] for x in rows))
