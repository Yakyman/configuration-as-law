import csv,json,re,collections,pathlib,base64,plistlib
csv.field_size_limit(10000000)
base=pathlib.Path('S2/parts/d1'); out=[]; scoped=[]
titles={1:'a default value created during installation that no person of the computer chose',2:'a list the system generated from installed packages',3:'files left from an earlier version of a package that is still installed',4:'a stored archive whose contents are executed',5:"a package of a program's built-in installer whose code runs only inside that program"}
for f,chunk in enumerate(open('D1/adjudication/HOLES.md').read().split('\n## ')[1:],1):
 for ident in re.findall(r'^- ((?:alma|void|microos)-[a-f0-9]{24})',chunk,re.M):scoped.append((f,ident))
DB={}; FS={}; PK={}; packages={}
for m in ['alma','void','microos']:
 p=f'D1/in/raw/{m}'
 DB[m]={r['id']:r for r in csv.DictReader(open(p+'/objects.tsv'),delimiter='\t')}
 FS[m]={r['path']:r for r in map(json.loads,open(p+'/raw/0004-filesystem.out')) if 'path' in r}
 PK[m]=collections.defaultdict(list)
 for r in csv.DictReader(open(p+'/package-files.tsv'),delimiter='\t'):PK[m][r['path']].append(r)
 packages[m]=[r for r in DB[m].values() if r['kind']=='package']
def clean(s):return str(s).replace('/home/user','~').replace('/root','<root-home>').replace('\t','; ').replace('\n',' ')
def add(k,v,s=None):out.append(dict(family=f,object=ident,machine=m,name=clean(r['name']),fact=k,value=clean(v),source=s or source))
def unknown(k,reason,s=None):add(k,'UNKNOWN: '+reason,s)
def pkg(names):
 for x in packages[m]:
  if any(re.match(r'(rpm|xbps|npm):'+re.escape(n)+r'[@-]',x['name']) for n in names):add('related_package:'+clean(x['name']),x['name']+'; '+json.dumps({k:v for k,v in json.loads(x['members']).items() if k in ['version','manager','reason']}),p+'/objects.tsv#'+x['id'])
def doc(k,v,url,q):add(k,v,url+'; quote: "'+q+'"')
for f,ident in scoped:
 m,oid=ident.split('-',1);p=f'D1/in/raw/{m}';r=DB[m][oid]; source=p+'/objects.tsv#'+oid; data=json.loads(r['members']); n=r['name']
 add('presence','Present in retained inventory; observation '+json.load(open(p+'/metadata.json'))['utc'])
 add('object_scope','Immediate-child group of '+str(data['count'])+' entries; not a recursive union or the entire directory contents with packaged entries restored' if 'file'in data else ('Stored file, archive contents not expanded' if 'metadata'in data else 'One recorded account or service entry'))
 if 'record'in data:add('recorded_value',data['record'],p+'/'+r['evidence'])
 members=list(csv.DictReader(open(p+'/'+data['file']),delimiter='\t')) if 'file'in data else ([data['metadata']] if 'metadata'in data else [])
 if members:
  add('member_list',json.dumps([x['path'] for x in members]),p+'/'+data.get('file','raw/0004-filesystem.out'))
  for x in members:
   path=x['path']; y=FS[m].get(path,x)
   add('member_metadata:'+clean(path),json.dumps({k:y[k] for k in ['type','mode','uid','gid','owner','size','mtime','ctime','persistence','executable','signature','target'] if k in y}),p+'/raw/0004-filesystem.out#'+clean(path))
   if m=='microos' and path.startswith('/.snapshots/1/snapshot/'):
    active=path.removeprefix('/.snapshots/1/snapshot')
    if active in FS[m]:
     a=FS[m][active]
     add('active_counterpart_metadata_comparison:'+clean(path),json.dumps({k:y.get(k)==a.get(k) for k in ['inode','ctime','size','mode','mtime','signature']}),p+'/raw/0004-filesystem.out#'+active)
     for q in PK[m].get(active,[]):add('active_counterpart_manifest:'+clean(path)+':'+q['package'],DB[m][q['package']]['name']+'; integrity='+q['integrity']+'; counterpart='+active,p+'/package-files.tsv#'+active)
   matches=PK[m].get(path,[])
   if m=='alma' and path.startswith('/usr/lib/'):matches+=PK[m].get(path[4:],[])
   if matches:
    for match in matches:
     z=DB[m][match['package']]
     add('member_package_record:'+clean(path),z['name']+'; integrity='+match['integrity']+'; '+match['rule'],p+'/package-files.tsv#'+clean(path))
   else:add('member_package_record:'+clean(path),'No matching file entry in retained native package-files table; directory entries are omitted by that table; absence alone is not proof of never having been supplied by a package',p+'/package-files.tsv')
 unknown('recorded_description_source','No primary-description designation or successful application record for this object was captured by these inventories; installation inputs do not identify a recording line',source)
 if f==1:
  if n in ['root','tss','systemd-oom']:
   doc('documented_record_format','Account fields describe system login identities and numeric IDs; x indicates shadow password storage, not a visible password','https://man7.org/linux/man-pages/man5/passwd.5.html','Each line of the file describes a single user')
   for q in PK[m].get('/etc/passwd',[]):add('account_container_file_package',DB[m][q['package']]['name']+'; /etc/passwd; integrity='+q['integrity'],p+'/package-files.tsv#/etc/passwd')
   add('execution','Account database fields are read as identity values; the record is not itself executed')
   add('effect_scope','System identity, UID/GID and login-shell lookup; not limited to a personal application')
   if n!='root':doc('documented_login_shell','nologin denies login when invoked as an account login shell','https://man7.org/linux/man-pages/man8/nologin.8.html','deny login access to an account.')
   add('login_shell',data['record'].split(':')[-1])
   add('account_uid',data['record'].split(':')[2])
   add('account_primary_gid',data['record'].split(':')[3])
   if n=='root':add('launch_or_access','UID 0/GID 0 account has /bin/bash as its login shell. The passwd row does not contain an authentication credential or prove an enabled remote/password login route')
   else:add('launch_or_access','Account has a nologin login shell, which refuses login when invoked. This does not prevent a privileged service from using the account UID without an interactive login')
   related={'root':['system-user-root'],'tss':['tpm2-tss'],'systemd-oom':['systemd']}[n];pkg(related)
   recipe={'root':'/usr/lib/sysusers.d/system-user-root.conf','tss':'/usr/lib/sysusers.d/tpm2-tss.conf','systemd-oom':'/usr/lib/sysusers.d/systemd.conf'}[n]
   for z in PK[m].get(recipe,[]):add('generation_recipe_package',DB[m][z['package']]['name']+'; '+recipe+'; integrity='+z['integrity'],p+'/package-files.tsv#'+recipe)
   doc('producer_mechanism','systemd-sysusers can create accounts from sysusers descriptions; a recipe match alone does not timestamp or prove the historical invocation','https://www.freedesktop.org/software/systemd/man/latest/systemd-sysusers.html','systemd-sysusers creates system users and groups')
   unknown('producer_and_creation_time','The inventory records current account fields and packaged recipes, not the first account-creation transaction; fresh installation cannot recover that historical transaction')
   unknown('person_choice_and_time','No retained first-creation operator record identifies who chose these account values or when; matching distribution defaults does not establish a personal choice')
   unknown('package_as_received','An individual account is not independently hashed in the package manifest; current /etc/passwd and recipe ownership do not prove that this entry was delivered verbatim')
  elif n.endswith('.service'):
   doc('documented_service_behavior','Enabling creates links for later activation; starting a service spawns a daemon process. Preset applies distribution enable/disable defaults','https://www.freedesktop.org/software/systemd/man/latest/systemctl.html','Starting actually spawns the daemon process')
   unit='/usr/lib/systemd/system/'+('gdm.service' if n=='display-manager.service' else n)
   for z in PK[m].get(unit,[]):add('unit_file_package',DB[m][z['package']]['name']+'; '+unit+'; integrity='+z['integrity'],p+'/package-files.tsv#'+unit)
   links=[(a,b) for a,b in FS[m].items() if b.get('type')=='symlink' and a.startswith('/etc/systemd/') and (a.endswith('/'+n) or ('avahi' in a if n.startswith('avahi') else False))]
   for a,b in links:add('service_link',json.dumps(b),p+'/raw/0004-filesystem.out#'+a)
   add('execution','Service definition and links are read by systemd; enabled service can cause service executable(s) to start as separate host processes')
   add('effect_scope','System service manager, not a program launched solely for one user')
   pkg(['avahi' if n.startswith('avahi') else 'gdm','systemd'])
   unknown('person_choice_and_time','Link timestamps and preset state show current result, not a logged personal selection; no first installation operator event retained')
   unknown('producer_transaction','No retained log identifies the exact process that created each enablement/alias link; timestamps are not process attribution')
   recovered_name='gdm.service' if n=='display-manager.service' else 'avahi-daemon.service'
   recovered=(base/'raw'/recovered_name).read_text()
   recsrc='S2/parts/d1/raw/'+recovered_name+'; S2/parts/d1/raw/service-content-recovery.json; '+p+'/raw/0019-package-files-rpm.out; '+p+'/package-files.tsv'
   add('recovered_unit_identity','Exact-version official repository RPM unit bytes have full SHA-256 equal to original retained RPM digest; original inventory marks this unit unchanged',recsrc)
   add('unit_ExecStart',next(x.split('=',1)[1] for x in recovered.splitlines() if x.startswith('ExecStart=')),recsrc)
   add('unit_User','No User= directive in exact matched unit',recsrc)
   add('unit_Group','No Group= directive in exact matched unit',recsrc)
   add('unit_dropins','Retained complete filesystem traversal contains no avahi-daemon.service.d, avahi-.service.d, gdm.service.d, display-manager.service.d, or generic service.d directory; account for enabled alias link separately',p+'/raw/0004-filesystem.out')
   doc('execution_rights','For system services, absent User=/Group= means system-manager default root at process launch. This states launch credentials, not every credential transition inside the daemon','https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html','the default is "root"')
  elif n.startswith('/var/service/'):
   leaf=n.rsplit('/',1)[1];path='/etc/runit/runsvdir/default/'+leaf
   if path in FS[m]:add('service_link_metadata',json.dumps(FS[m][path]),p+'/raw/0004-filesystem.out#'+path)
   pkg(['runit-void','acpid'])
   doc('launch_or_access','A service-directory symlink enables runit supervision and service process startup','https://docs.voidlinux.org/config/services/index.html','To enable a service on a booted system, create a symlink to the service directory in /var/service')
   add('execution','The link is followed to a service directory; runit executes its run script as a host process')
   add('effect_scope','Booted system service supervision')
   unknown('person_choice_and_time','Link metadata identifies time of filesystem change, not the person choosing the service; image build/first enabling transaction not retained')
   unknown('producer_transaction','No exact link-creation process invocation retained; package update timestamps support timing but not individual writer identity')
   unknown('execution_rights','Effective run-script credentials not retained')
  else:
   if m=='void' and n=='/usr/bin':
    for line in open(p+'/raw/0011-metadata-read-0.out'):
     z=json.loads(line)
     if 'pkgdb' not in z.get('path',''):continue
     d=plistlib.loads(base64.b64decode(z['data']))
     for pn,pv in d.items():
      if not isinstance(pv,dict):continue
      for group,entries in pv.get('alternatives',{}).items():
       for ent in entries:
        link,target=ent.split(':',1)
        if '/'not in link:link='/usr/bin/'+link
        if link in [v['path'] for v in members] and FS[m].get(link,{}).get('target')==target:add('alternative_registration:'+link,pv['pkgver']+'; group='+group+'; target='+target,p+'/raw/0011-metadata-read-0.out#'+z['path'])
   doc('documented_link_behavior','A symbolic link stores another pathname; executing through it uses its target rather than treating the pathname text as source code','https://man7.org/linux/man-pages/man7/symlink.7.html','Symbolic links are files that act as pointers to other files.')
   add('execution','Symbolic links select command/manual targets; links contain target names rather than instructions. A command link can be followed when a caller executes its target')
   add('execution_rights','Command target runs with caller credentials unless its target applies a privilege transition; link mode alone grants no elevated execution')
   add('launch_or_access','Command links expose target programs; manual-page links select documents. None of these links is itself an authentication credential')
   add('effect_scope','System command selection' if not n.startswith('/home/') else 'Command lookup in the user npm installation')
   if '.bin' in n:
    pkg(['cowsay']);add('producer','npm during the successful language_program ordinary action', 'C1/actions/ordinary.sh#language_program; D1/in/control/void/actions-logs/actions-logs/language_program.log')
    add('person_choice','Operator requested cowsay installation; the two command link targets were selected by npm from package metadata','C1/actions/ordinary.sh#language_program')
   else:unknown('person_choice_and_producer','Alternative links and package tables expose the selected targets; retained data do not identify all historical selections, first writers, or their times')
   unknown('package_as_received','Links are not covered by file digests establishing original delivered bytes; a package-triggered creation differs from an observed package payload copy')
 elif f==2:
  familytools={
   '/usr/share/mime':('update-mime-database','shared-mime-info','MIME identifiers, suffixes and sniffing rules consumed by applications'),
   '/usr/share/mime/application':('update-mime-database','shared-mime-info','MIME descriptions consumed by applications'),
   '/etc/ssl/certs':('update-ca-certificates','ca-certificates','Certificate trust lookup by TLS applications'),
   '/var/lib/ca-certificates/openssl':('update-ca-certificates','ca-certificates','Certificate trust lookup by TLS applications'),
   '/var/cache/ldconfig':('ldconfig','glibc','Shared library lookup/cache construction'),
   '/etc/dconf/db':('dconf update','dconf','Desktop and login-manager values read through dconf'),
  }
  tool,package,effect=familytools.get(n, ('depmod','kernel-modules-core','Kernel module dependency lookup') if '/usr/lib/modules/'in n else (('semodule','selinux-policy-targeted','SELinux policy loaded and enforced by kernel') if n.endswith('/active') else ('ldconfig','glibc','Snapshot etc includes shared-library cache and many other files')))
  pkg([package]);add('named_member_function',effect)
  if tool=='update-mime-database':doc('documented_derivation','Scans packages/*.xml and combines them into generated MIME lookup files','https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html','It scans all the XML files in the packages subdirectory')
  elif tool=='update-ca-certificates':
   if m=='microos':doc('documented_derivation','The distribution update-ca-certificates script calls update hooks with statedir=/var/lib/ca-certificates; this documents a generation mechanism, not a historical input list','https://raw.githubusercontent.com/openSUSE/ca-certificates/master/update-ca-certificates',"statedir='/var/lib/ca-certificates'")
   else:doc('documented_derivation','update-ca-certificates updates certificate directory and generates concatenated certificate bundle','https://manpages.debian.org/bookworm/ca-certificates/update-ca-certificates.8.en.html','generates ca-certificates.crt, a concatenated single-file list of certificates')
  elif tool=='ldconfig':doc('documented_derivation','ldconfig constructs cache from shared libraries in specified/configured/trusted directories; ld.so consumes it','https://man7.org/linux/man-pages/man8/ldconfig.8.html','The cache is used by the run-time linker')
  elif tool=='depmod':doc('documented_derivation','depmod reads kernel modules to generate dependency and symbol lists','https://raw.githubusercontent.com/kmod-project/kmod/master/man/depmod.8.scd','Generate modules.dep and map files.')
  elif tool=='dconf update':doc('documented_derivation','dconf update compiles keyfile directories into dconf databases','https://wiki.gnome.org/Projects/dconf/SystemAdministrators','This directory contains keyfiles in a special format that can be compiled into the dconf database.')
  elif tool=='semodule':doc('documented_derivation','semodule manages SELinux policy modules and can rebuild the policy from its store','https://raw.githubusercontent.com/SELinuxProject/selinux/master/policycoreutils/semodule/semodule.8','force a rebuild of policy')
  add('generation_mechanism',tool+' is associated with the named database/cache; the historical invocation and exact input closure require a retained log, not just this filename')
  unknown('historical_producer_inputs_choice','The retained inventory has names, metadata and package manifests but no complete generation transaction/input set or personal override history for all members; a fresh run cannot establish old inputs')
  if 'selinux' in n or n.endswith('/snapshot/etc'):
   unknown('member_content_execution_and_effects','This aggregate includes multiple files/directories and its complete stored values are not dumped; cannot assert every member is only values or exclude launch/access entries')
  else:add('execution','Named database/cache/certificate entries are consumed as lookup or value data; execute-permission metadata for directories/symlinks is not evidence of code execution')
  if '/usr/lib/modules/'in n:
   add('additional_executable_member','The group also includes vmlinuz, a kernel boot image owned by kernel-core; the depmod-generated modules.* subset does not describe every group member',p+'/members/'+oid+'.tsv; '+p+'/package-files.tsv')
   add('additional_execution_context','vmlinuz is loaded for execution as the kernel by the boot path; this is host kernel execution, not a personal application process',p+'/members/'+oid+'.tsv; https://www.kernel.org/doc/html/latest/filesystems/ramfs-rootfs-initramfs.html')
  if 'cert' in n:add('launch_or_access','CA trust data affects acceptance of remote TLS peer identities; it is not evidence of a means of login to this computer')
  elif n=='/etc/dconf/db':unknown('launch_or_access','Exact dconf keys and effective profile/lock selection were not dumped, so launch/access effects of every stored value cannot be excluded')
  else:add('launch_or_access','Named generated index does not directly start a standalone process; consumers use its lookup information. Other aggregate members are separately bounded by member_content_execution_and_effects when present')
  unknown('package_as_received','Current generated member bytes are not certified as original delivered payload bytes; package table matches and integrity results above retain their limited scope')
 elif f==3:
  pkg(['linux6.12']);add('earlier_package_version','linux6.12 changed from 6.12.11_1 to 6.12.118_1 in package_program','D1/in/control/void/actions-logs/actions-logs/package_program.log:316')
  doc('retention_mechanism','Void intentionally retains previous kernel versions during updates','https://docs.voidlinux.org/config/kernel.html','When updating the kernel, old versions are left behind')
  add('execution','The named directory entry is traversed, not executed. Descendant .ko.zst files contain compressed kernel-module code; modules.* files contain lookup tables')
  doc('documented_execution','Module loader puts ELF code into kernel space, relocates it and calls its initialization function; the operation needs privilege','https://man7.org/linux/man-pages/man2/init_module.2.html','This system call requires privilege.')
  add('execution_rights','Loadable modules execute in kernel context, not as a standalone user process; loading requires a compatible kernel and permitted module-loading operation')
  unknown('current_loadability','No retained module vermagic/signature, running-kernel compatibility, or complete module-loading restriction check establishes which old modules can load on the observed machine')
  unknown('package_as_received','Old version payload/full digests not retained in current XBPS manifest; prefix hashes cannot certify unchanged old files')
  add('person_choice','Operator invoked package_program; individual retained module bytes were not authored by that action','C1/actions/ordinary.sh#package_program; D1/in/control/void/actions-logs/actions-logs/package_program.log:316')
  unknown('original_writer_and_time','Old file mtimes survive but first installation transaction is not retained; mtime is not the time a person brought the file')
  add('launch_or_access','Kernel modules can affect kernel behavior when loaded; directory entries and dependency lists do not grant authentication access themselves')
 elif f==4:
  pkg(['dracut','kernel-core','kernel-default','linux6.12','linux6.18'])
  doc('documented_generator_purpose','dracut generates an initramfs/initrd image for a kernel version from system inputs','https://raw.githubusercontent.com/dracut-ng/dracut/main/man/dracut.8.adoc','low-level tool for generating an initramfs/initrd image')
  doc('archive_execution_sequence','Kernel unpacks initramfs into rootfs and executes contained /init as PID 1; archive bytes are first parsed/unpacked, then contained code runs','https://www.kernel.org/doc/html/latest/filesystems/ramfs-rootfs-initramfs.html','it executes it as PID 1')
  add('execution_rights','Early boot init runs as a host PID 1 process with system startup authority; archive mode 0600/0644 is not a denial of contained-code execution')
  add('launch_or_access','Contained startup programs can load drivers, mount root and start system processes; this is not confined to a personal browser or virtual guest')
  if m=='void':add('producer','dracut run by kernel update for 6.12.118_1 and 6.18.64_1; GRUB found those initrds and the older 6.12.11_1 image','D1/in/control/void/actions-logs/actions-logs/package_program.stderr:2-89')
  else:unknown('historical_producer','Inventory stores opaque archive metadata, not its generating process; dracut package presence does not prove its exact historical invocation')
  unknown('archive_contents_and_input_versions','Archive contents were not expanded or hashed per member, so exact executable members and their source package/version/modifiedness are unavailable')
  unknown('package_as_received','No whole-image original package digest or generation input manifest certifies the archive as received; metadata prefix hashes are insufficient')
  unknown('person_choice_and_time','Filesystem mtimes are known but precise earlier build choices and person selecting each boot/archive parameter were not retained')
 elif f==5:
  pkg(['firefox'])
  doc('documented_install_remove_unit','Browser Addons API installs an XPI by file path and uninstalls by add-on ID; temp=False selects non-temporary installation','https://firefox-source-docs.mozilla.org/python/marionette_driver.html','Install a Firefox addon, which can be used right away.')
  add('installation_action','Operator browser_extension action downloaded ClearURLs via add-on service API, checked advertised payload hash, then invoked Addons.install(temp=False); action returned zero','C1/actions/firefox-addon.py; C1/actions/ordinary.sh#browser_extension; '+('D1/in/control/alma/actions-status.tsv' if m=='alma' else 'D1/in/control/void/actions-status.tsv/actions-status.tsv'))
  add('person_choice','Operator requested ClearURLs; script requested the then-current API release, without specifying a release number','C1/actions/firefox-addon.py')
  add('producer','Browser AddonManager through Marionette wrote installed XPI into the persistent profile; client quit/cleanup after installation','C1/actions/firefox-addon.py')
  add('execution','XPI archive is handled by Firefox; extension JavaScript is run by browser execution contexts, not by invoking the XPI as a native executable','C1/actions/firefox-addon.py; https://raw.githubusercontent.com/ClearURLs/Addon/master/manifest.json; quote: "background"')
  add('authoritative_candidate_prefix_match','One AMO candidate, advertised version 1.28.0, has size 1226057 and prefix4096 SHA-256 af66ff20482b867da5f670e384f9f3ec025ffeddec6a269a5ae7c315c4a8f036, matching both retained installed files. This proves only the matched 4096-byte range, not whole-archive identity','S2/parts/d1/raw/amo-candidate.json; S2/parts/d1/raw/amo-prefix-check.json; '+p+'/members/'+oid+'.tsv')
  add('candidate_manifest_byte_range','Candidate manifest.json compressed bytes occupy [14952,16628), with local ZIP header at 14909, entirely outside the retained first 4096 bytes','S2/parts/d1/raw/amo-prefix-check.json; https://addons.mozilla.org/firefox/downloads/file/5286652/clearurls-1.28.0.xpi')
  unknown('installed_version_and_permissions','Installed manifest and clearurls-source.json contents were not collected. The one authoritative AMO candidate matches size/prefix, but manifest bytes [14952,16628) lie beyond saved prefix4096; this cannot certify historical installed version or permissions','S2/parts/d1/raw/amo-prefix-check.json; '+p+'/members/'+oid+'.tsv')
  unknown('package_as_received','Download was hash-checked at retrieval, but installed XPI has only a 4096-byte prefix hash; neither retained full installed digest nor payload comparison proves unchanged installed bytes')
  unknown('execution_rights_and_launch_access_capability','Historical manifest/effective permissions and browser policy were not retained; cannot prove inability to launch external programs or alter host settings from current upstream manifest')
  add('permission_documentation','downloads.open requires both downloads.open and downloads permissions; this conditional API fact does not establish actual installed permissions','https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/open; quote: "as well as the \"downloads\" permission"')
exec((base/'normalize.py').read_text())
docs={}
for row in out:
 if '; quote: ' in row['source']:
  def replace_quote(match):
   u,q=match.group(1),match.group(2)
   key=(u,q)
   if key not in docs:docs[key]='doc-'+str(len(docs)+1)
   return 'S2/parts/d1/DOCUMENTATION.md#'+docs[key]+'; '+u
  row['source']=re.sub(r'(https://[^; ]+); quote: (\".*?\")(?=; |$)',replace_quote,row['source'])
with open(base/'DOCUMENTATION.md','w') as h:
 h.write('# Documentation evidence\n\nRetrieved 2026-11-23 UTC. These describe tool behavior, not historical guest bytes or invocation history.\n')
 for (u,q),label in docs.items():h.write('\n## '+label+'\n\n'+u+'\n\nQuote: '+q+'\n')
with open(base/'facts.tsv','w') as h:
 w=csv.DictWriter(h,fieldnames=['family','object','machine','name','fact','value','source'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
with open(base/'FACTS.md','w')as h:
 unknowns=[x for x in out if x['value'].startswith('UNKNOWN:')]
 h.write(f'D1 collector facts: {len(scoped)} objects of families 1–5; {len(unknowns)} unknown fact rows.\n\n')
 h.write('Facts are indexed in facts.tsv. Directory rows retain the original immediate-child scope, not an inferred recursive replacement. Prefix digests are not full-file integrity checks for files larger than 4096 bytes. Times are UTC; ctime/mtime do not identify a writer. No new probes were run: remaining absences concern historical transactions/bytes that a fresh machine cannot recover. General documented behavior is distinguished from proof about an old invocation.\n')
 for f in range(1,6):
  h.write(f'\n## {f}. {titles[f]}\n\n')
  for _,ident in [x for x in scoped if x[0]==f]:
   rows=[x for x in out if x['object']==ident];h.write(f"- `{ident}` — `{rows[0]['name']}`.\n")
   for x in rows:
    if x['value'].startswith('UNKNOWN:'):h.write(f"  - {x['fact']}: {x['value'][9:]}\n")
print(len(scoped),len(out),len(unknowns))
