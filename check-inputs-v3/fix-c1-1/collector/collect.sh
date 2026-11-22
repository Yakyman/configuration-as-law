#!/bin/sh
# Host-side controller. Guest collection uses only existing tools.
exec python3 - "$0" "$@" <<'PY'
import os,sys,pathlib,subprocess as sp,json,csv,hashlib,shlex,collections,datetime,re,tarfile,io,email
args=sys.argv[2:]
if len(args)!=3 or args[0] not in ('--instrument-test','--observe'):
 sys.exit('Usage: collect.sh --instrument-test|--observe VM OUTPUT_DIRECTORY')
mode,machine,out=args
if not re.fullmatch('[a-z][a-z0-9-]{0,39}',machine):sys.exit('Use a synthetic machine ID')
root=pathlib.Path(os.getenv('LAB_ROOT',pathlib.Path(sys.argv[1]).resolve().parent.parent))
lab=root/'lab.sh';meta=json.loads((root/'C1/vms'/machine/'meta.json').read_text())
if mode=='--instrument-test' and meta['system']!='debian':sys.exit('Instrument testing is restricted to Debian')
if mode=='--observe' and os.getenv('CAL_INPUTS_COMMIT','')=='':sys.exit('Set CAL_INPUTS_COMMIT to the committed input revision before observation')
if meta['system']=='talos':sys.exit('Use the documented Talos adapter; it has not been exercised on a check machine')
out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False);(out/'raw').mkdir()
objects=[];coverage=[];counter=0;installed_managers=set();parse_gaps=[]
fields=['id','machine','level','kind','name','members','evidence']
def obj(level,kind,name,members,evidence):
 ident=hashlib.sha256((machine+'\0'+str(level)+'\0'+kind+'\0'+name+'\0'+json.dumps(members,sort_keys=True,ensure_ascii=True)).encode()).hexdigest()[:24]
 objects.append([ident,machine,level,kind,name,json.dumps(members,ensure_ascii=True),evidence])
def query(label,script,as_user=None):
 global counter
 counter+=1
 if as_user:script='runuser -u '+shlex.quote(as_user)+' -- env HOME='+shlex.quote(users[as_user][1])+' XDG_RUNTIME_DIR=/run/user/'+users[as_user][0]+' sh -c '+shlex.quote(script)
 p=sp.run([str(lab),'run',machine,'--root'],input=('export LC_ALL=C TZ=UTC\n'+script+'\n').encode(),stdout=sp.PIPE,stderr=sp.PIPE)
 name=f'{counter:03d}-{label}';(out/'raw'/f'{name}.out').write_bytes(p.stdout);(out/'raw'/f'{name}.err').write_bytes(p.stderr)
 (out/'raw'/f'{name}.sh').write_text(script+'\n')
 coverage.append([label,str(p.returncode),str(len(p.stdout)),f'raw/{name}.out',f'raw/{name}.err'])
 return p.stdout,p.returncode,f'raw/{name}.out'
def lines(level,kind,label,command,user=None):
 data,rc,ev=query(label,command,user)
 if rc!=0:return data,rc,ev
 text=data.decode(errors='replace')
 if kind.startswith('package:'):
  manager=kind.split(':',1)[1];installed_managers.add(manager)
  prefix=(user+':' if user else '')
  records=[]
  if manager in ('pip','pip3','conda','mamba','npm','pnpm','composer','pipx'):
   try:
    parsed=json.loads(text)
    if manager in ('pip','pip3','conda','mamba'):records=[(r['name'],r) for r in parsed]
    elif manager in ('npm','pnpm'):
     def walk(deps,path=''):
      for name,rec in deps.items():
       records.append((path+name,rec));walk(rec.get('dependencies',{}),path+name+'/')
     for tree in parsed if isinstance(parsed,list) else [parsed]:walk(tree.get('dependencies',{}))
    elif manager=='composer':records=[(r['name'],r) for r in parsed.get('installed',[])]
    elif manager=='pipx':records=list(parsed.get('venvs',{}).items())
   except (ValueError,KeyError,TypeError,AttributeError):parse_gaps.append(label)
  elif manager=='nix':
   try:
    parsed=json.loads(text);elements=parsed.get('elements',parsed)
    records=list(elements.items()) if isinstance(elements,dict) else [(str(i),r) for i,r in enumerate(elements)]
   except (ValueError,TypeError,AttributeError):parse_gaps.append(label)
  elif manager=='yarn':
   try:
    def yarn_tree(nodes):
     for node in nodes:
      records.append((node['name'],node));yarn_tree(node.get('children',[]))
    for line in text.splitlines():
     row=json.loads(line)
     if row.get('type')=='tree':yarn_tree(row['data'].get('trees',[]))
     elif row.get('type')=='info':
      match=re.search(r'"([^" ]+@[^" ]+)"',str(row.get('data','')))
      if match:records.append((match.group(1),row))
   except (ValueError,TypeError,KeyError):parse_gaps.append(label)
  elif manager=='xbps-query':
   records=[(r.split()[1],r) for r in text.splitlines() if r.startswith(('ii ','hi ')) and len(r.split())>1]
  elif manager=='ghc-pkg':
   records=[(token.strip('(){}'),token) for token in text.split() if not token.endswith(':') and not token.startswith('/')]
  elif manager in ('cabal','opam','luarocks','dotnet'):
   for line in text.splitlines():
    parts=line.split()
    if len(parts)<2 or line.lstrip().startswith(('#','-')):continue
    if manager=='dotnet' and line.startswith('Package Id'):continue
    if re.match(r'^[0-9]',parts[1]):records.append((parts[0],line))
  elif manager=='R':
   for row in csv.reader(io.StringIO(text),delimiter='\t'):
    if row and row[0]!='Package':records.append((row[0],row))
  elif manager=='julia':
   for line in text.splitlines():
    match=re.search(r'\[([0-9a-f]+)\]\s+(\S+)(.*)',line)
    if match:records.append((match.group(2),line))
  elif manager=='cargo':
   records=[(line.split()[0],line) for line in text.splitlines() if line and not line[0].isspace()]
  elif manager=='go':
   records=[(line.strip().split()[1],line) for line in text.splitlines() if line.strip().startswith(('mod\t','dep\t'))]
  elif manager in ('dpkg-query','rpm','pacman','apk','opkg','flatpak','nix-env','guix','gem','snap','brew','rustup'):
   for line in text.splitlines():
    if not line.strip():continue
    if manager=='dpkg-query' and not line.split('\t')[-1].startswith('ii'):continue
    if manager=='snap' and line.startswith('Name '):continue
    records.append((line.split()[0],line))
  else:
   parse_gaps.append(label)
   obj(level,'unparsed-package-manager-evidence',prefix+manager,[text],ev)
  for name,record in records:obj(level,kind,prefix+str(name),[record],ev)
 elif kind=='firewall-nft':
  try:
   for record in json.loads(text).get('nftables',[]):
    if 'metainfo' in record:continue
    rkind=next(iter(record));rule=record[rkind]
    obj(level,'firewall-rule' if rkind=='rule' else 'firewall-'+rkind,label+':'+str(len(objects)),[rule],ev)
  except (ValueError,TypeError):parse_gaps.append(label)
 else:
  for i,line in enumerate(text.splitlines(),1):
   if not line.strip():continue
   name=line.split()[0]
   if kind in ('container','container-image','docker-container','docker-image') and name in ('CONTAINER','REPOSITORY','IMAGE'):continue
   if kind in ('timer','user-timer'):
    found=re.search(r'(?<!\S)(\S+\.timer)(?!\S)',line)
    if not found:continue
    name=found.group(1)
   elif kind in ('service','user-service'):
    found=re.search(r'(?<!\S)(\S+\.service)(?!\S)',line)
    if not found:continue
    name=found.group(1)
   elif kind in ('account','group'):name=line.split(':',1)[0]
   elif kind=='port':name=' '.join(line.split()[:5])
   elif kind=='sudo-access':
    if not line.lstrip().startswith('('):continue
    obj(level,'access-rule',label+':'+str(i),[line],ev+':'+str(i));continue
   elif kind=='ssh-access':
    obj(level,'access-rule',label+':'+name,[line],ev+':'+str(i));continue
   elif kind=='networkd':
    obj(level,'network-link',label+':'+name,[line],ev+':'+str(i));continue
   obj(level,kind,(user+':' if user else '')+name,[line],ev+':'+str(i))
 return data,rc,ev
passwd,_,_=lines(1,'account','accounts','getent passwd')
users={}
for line in passwd.decode().splitlines():
 p=line.split(':')
 if len(p)==7 and (p[2]=='0' or int(p[2])>=1000) and p[6] not in ('/usr/sbin/nologin','/sbin/nologin','/bin/false'):users[p[0]]=(p[2],p[5])
lines(1,'group','groups','getent group')
managers={
 'dpkg-query':"dpkg-query -W -f='${binary:Package}\\t${Version}\\t${db:Status-Abbrev}\\n'",
 'rpm':"rpm -qa --qf '%{NAME}\\t%{VERSION}-%{RELEASE}\\t%{ARCH}\\n'",
 'pacman':'pacman -Q','apk':'apk info -v','opkg':'opkg list-installed','xbps-query':'xbps-query -l',
 'flatpak':'flatpak list --columns=ref,version,origin,installation --all', 'snap':'snap list',
 'nix-env':'nix-env -q --out-path', 'nix':'nix profile list --json','guix':'guix package --list-installed',
 'pip':'pip list --format=json','pip3':'pip3 list --format=json','pipx':'pipx list --json',
 'npm':'npm list -g --all --json','pnpm':'pnpm list -g --all --json','yarn':'yarn global list --json',
 'gem':'gem list --local','cargo':'cargo install --list','rustup':'rustup toolchain list',
 'go':'go version -m $(go env GOPATH)/bin/*','conda':'conda list --json','mamba':'mamba list --json',
 'composer':'composer global show --format=json','ghc-pkg':'ghc-pkg list --simple-output','cabal':'cabal list --installed --simple-output',
 'opam':'opam list --installed --columns=name,version','luarocks':'luarocks list --porcelain',
 'R':"R --vanilla --slave -e 'write.table(installed.packages()[,c(\"Package\",\"Version\",\"LibPath\")],row.names=FALSE,sep=\"\\t\")'",
 'julia':"julia --startup-file=no -e 'using Pkg; Pkg.status()'",'dotnet':'dotnet tool list --global','brew':'brew list --versions'}
# Discovery and query are combined; absence (127) is explicit, not an empty inventory.
for user in users:
 for manager,cmd in managers.items():
  lines(1,'package:'+manager,'packages-'+user+'-'+manager,'command -v '+manager+' >/dev/null 2>&1 || exit 127; '+cmd,user)
 for kind,cmd in [('service','list-units --all --type=service'),('timer','list-timers --all'),('unit-file','list-unit-files --type=service,timer')]:
  lines(1,'user-'+kind,'user-'+user+'-'+kind,'systemctl --user --no-pager --no-legend '+cmd,user)
for kind,cmd in [('service','list-units --all --type=service'),('timer','list-timers --all'),('unit-file','list-unit-files --type=service,timer')]:
 lines(1,kind,kind,'systemctl --no-pager --no-legend '+cmd)
for kind,cmd in [
 ('process',"for p in /proc/[0-9]*; do test -d \"$p\" || continue; printf '%s\\t' \"${p##*/}\"; readlink \"$p/exe\" || :; done"),
 ('module','cat /proc/modules'),('driver',"find /sys/devices -type l -name driver -exec sh -c 'for p do printf \"%s\\t%s\\n\" \"$p\" \"$(readlink \"$p\")\"; done' sh {} +"),
 ('port','ss -H -lntup'),('firewall-nft','nft -j -a list ruleset'),('firewall-ipv4','iptables-save'),('firewall-ipv6','ip6tables-save'),
 ('network','nmcli -t -f NAME,UUID,TYPE,DEVICE connection show'),('networkd','networkctl list --no-pager --no-legend'),
 ('ssh-access','sshd -T'),('sudo-access','sudo -l -U user'),('polkit-actions','pkaction'),
 ('container','podman ps -a --no-trunc'),('container-image','podman images --no-trunc'),
 ('docker-container','docker ps -a --no-trunc'),('docker-image','docker images --no-trunc')]:lines(1,kind,kind,cmd)
for user in users:
 lines(1,'sudo-access','sudo-'+user,'sudo -l -U '+shlex.quote(user))
 lines(1,'container','containers-'+user,'podman ps -a --no-trunc',user)
 lines(1,'container-image','container-images-'+user,'podman images --no-trunc',user)
 lines(1,'cron','cron-'+user,'crontab -l',user)
# Container/image boundaries are discovered before filesystem-derived packages.
# Named volumes are host stored objects and are not beneath the pruned paths.
opaque_paths=set();engine_roots=[];boundary_gaps=[]
for engine in ('podman','docker'):
 for user in users if engine=='podman' else ['root']:
  template='{{.Store.GraphRoot}}' if engine=='podman' else '{{.DockerRootDir}}'
  rootdata,rc,rev=query('engine-root-'+engine+'-'+user,'command -v '+engine+' >/dev/null 2>&1 || exit 127; '+engine+' info --format '+shlex.quote(template),user)
  if rc==127:continue
  if rc:boundary_gaps.append(engine+':'+user+':root-query-failed');continue
  roots=rootdata.decode(errors='replace').splitlines()
  if not any(r.startswith('/') and os.path.normpath(r)!='/' for r in roots):boundary_gaps.append(engine+':'+user+':absolute-graph-root-unavailable')
  engine_roots.extend({'engine':engine,'user':user,'path':r,'evidence':rev} for r in roots if r.startswith('/'))
  for category,listcmd in [('image','images -q --no-trunc'),('container','ps -aq --no-trunc')]:
   command='ids=$('+engine+' '+listcmd+') || exit $?; test -n "$ids" || exit 0; '+engine+' '+category+' inspect --format '+shlex.quote('{{json .GraphDriver.Data}}')+' $ids'
   data,rc,iev=query('engine-layers-'+engine+'-'+user+'-'+category,command,user)
   if rc:boundary_gaps.append(engine+':'+user+':'+category+':inspect-failed');continue
   for line in data.decode(errors='replace').splitlines():
    try:record=json.loads(line)
    except ValueError:boundary_gaps.append(engine+':'+user+':'+category+':invalid-json');continue
    found=False
    for key in ('UpperDir','LowerDir','MergedDir','WorkDir','Dir'):
     value=record.get(key) if isinstance(record,dict) else None
     if not isinstance(value,str):continue
     for path in value.split(':') if key=='LowerDir' else [value]:
      if path.startswith('/') and os.path.normpath(path)!='/':opaque_paths.add(os.path.normpath(path));found=True
    if not found:boundary_gaps.append(engine+':'+user+':'+category+':driver-paths-unavailable')
# Resolve storage symlink aliases so find cannot enter a layer through its real path.
for i,path in enumerate(sorted(opaque_paths)):
 data,rc,pev=query('engine-layer-canonical-'+str(i),'readlink -m -- '+shlex.quote(path))
 if rc==0:
  resolved=data.decode(errors='replace').strip()
  if resolved.startswith('/') and resolved!='/':opaque_paths.add(resolved)
 else:boundary_gaps.append('canonical-path-query-failed')
def storage_prune(paths):
 def pattern(path):return ''.join('\\'+c if c in '\\*?[' else c for c in path)
 return '\\( '+ ' -o '.join('-path '+shlex.quote(pattern(path)) for path in ['/proc','/sys','/dev']+sorted(paths))+' \\) -prune -o'
# Full stored-files manifest. Pseudo-filesystem nodes are not stored objects.
prune=storage_prune(opaque_paths)
manifest,fs_rc,ev=query('filesystem',"find / "+prune+" -printf '%p\\0%y\\0%m\\0%U\\0%G\\0%l\\0'")
entries={};chunks=manifest.split(b'\0')
for i in range(0,len(chunks)-6,6):
 p,typ,modebits,uid,gid,target=[x.decode(errors='surrogateescape') for x in chunks[i:i+6]];entries[p]=(typ,modebits,uid,gid,target)
owned=set();ownership_complete=True
for manager,cmd in [('dpkg-query',"dpkg-query -W -f='${binary:Package}\\n' | xargs -r dpkg-query -L"),('rpm','rpm -qal'),('pacman','pacman -Qlq'),('apk','apk info | xargs -r apk info -L')]:
 data,rc,oev=query('ownership-'+manager,'command -v '+manager+' >/dev/null 2>&1 || exit 127; '+cmd)
 if rc==0:owned.update(x for x in data.decode(errors='surrogateescape').splitlines() if x.startswith('/'))
 elif rc!=127:ownership_complete=False
# Canonicalize usrmerge aliases based on the captured symlink manifest, without assuming a layout.
def canonical(p):
 for _ in range(20):
  parts=p.split('/');changed=False
  for i in range(1,len(parts)):
   prefix='/'.join(parts[:i+1]);entry=entries.get(prefix)
   if entry and entry[0]=='l':
    dest=entry[4] if entry[4].startswith('/') else str(pathlib.PurePosixPath(prefix).parent/entry[4]);p=os.path.normpath(dest+'/'+ '/'.join(parts[i+1:]));changed=True;break
  if not changed:return p
 return p
owned.update(canonical(p) for p in list(owned))
# Application deployments are owned by their Flatpak refs; retain refs and locations.
for user in users:
 data,rc,oev=query('flatpak-ownership-'+user,"command -v flatpak >/dev/null 2>&1 || exit 127; flatpak list --columns=ref | while IFS= read -r ref; do flatpak info --show-location \"$ref\"; done",user)
 if rc==0:
  locations=data.decode().splitlines()
  owned.update(p for p in entries if any(p==loc or p.startswith(loc+'/') for loc in locations))
 elif rc!=127:ownership_complete=False
# Parse distribution manifests as data on the host. Never execute a discovered
# interpreter: even -I does not prevent installed .pth startup code.
metadata_paths=sorted(p for p,e in entries.items() if e[0]=='f' and
 (('/.dist-info/' in p or '.dist-info/' in p) and pathlib.PurePosixPath(p).name in ('METADATA','RECORD') or
  '.egg-info/' in p and pathlib.PurePosixPath(p).name in ('PKG-INFO','installed-files.txt')))
if metadata_paths:
 import base64
 encoded=base64.b64encode(('\0'.join(metadata_paths)+'\0').encode(errors='surrogateescape')).decode()
 data,rc,oev=query('python-distribution-manifests','printf %s '+shlex.quote(encoded)+' | base64 -d | tar --null -T - -cf - 2>/dev/null')
 if rc==0:
  manifests={}
  try:
   with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for member in archive:
     if member.isfile():manifests['/'+member.name.lstrip('/')]=archive.extractfile(member).read().decode(errors='replace')
   for path,content in manifests.items():
    if pathlib.PurePosixPath(path).name not in ('METADATA','PKG-INFO'):continue
    info=email.message_from_string(content);distdir=str(pathlib.PurePosixPath(path).parent)
    obj(1,'python-distribution',distdir+':'+str(info.get('Name')),[info.get('Version')],oev)
    record=manifests.get(distdir+'/RECORD')
    if record is not None:
     for row in csv.reader(io.StringIO(record)):
      if row:owned.add(os.path.normpath(str(pathlib.PurePosixPath(distdir).parent/row[0])))
    elif distdir+'/installed-files.txt' in manifests:
     for file in manifests[distdir+'/installed-files.txt'].splitlines():owned.add(os.path.normpath(distdir+'/'+file))
    else:ownership_complete=False
  except (tarfile.TarError,ValueError,KeyError):ownership_complete=False
 else:ownership_complete=False
# Missing file manifests use the binding conservative ownership fallback.
unsupported_ownership=installed_managers-{'dpkg-query','rpm','pacman','apk','flatpak','pip','pip3'}
if unsupported_ownership:ownership_complete=False
metadata_names={'package.json','composer.lock','Cargo.lock','conda-meta','METADATA','installed.packages','Project.toml','Manifest.toml','packages.config','Gemfile.lock','opam'}
for p,e in entries.items():
 if pathlib.PurePosixPath(p).name in metadata_names:obj(1,'package-environment-evidence',p,[e],ev)
# Installed npm package trees, including project-local environments.
node_meta=[p for p,e in entries.items() if e[0]=='f' and '/node_modules/' in p and p.endswith('/package.json')]
if node_meta:
 import base64
 encoded=base64.b64encode(('\0'.join(node_meta)+'\0').encode(errors='surrogateescape')).decode()
 data,rc,nev=query('npm-package-records','printf %s '+shlex.quote(encoded)+' | base64 -d | tar --null -T - -cf - 2>/dev/null')
 if rc==0:
  with tarfile.open(fileobj=io.BytesIO(data)) as archive:
   for member in archive:
    if not member.isfile():continue
    path='/'+member.name.lstrip('/');tree=str(pathlib.PurePosixPath(path).parent)
    try:rec=json.loads(archive.extractfile(member).read())
    except (ValueError,UnicodeError):ownership_complete=False;continue
    obj(1,'package:npm',tree,[rec.get('name'),rec.get('version')],nev)
    owned.update(p for p in entries if p==tree or p.startswith(tree+'/'))
 else:ownership_complete=False
if meta['system']=='flatcar':
 data,rc,iev=query('system-image','cat /etc/os-release; printf "\\nMOUNTS\\n"; findmnt -rn -o TARGET,OPTIONS /usr')
 text=data.decode(errors='replace');obj(1,'package:system-image','flatcar-system-image',[text],iev)
 if rc==0 and '\nMOUNTS\n' in text:
  for line in text.split('\nMOUNTS\n',1)[1].splitlines():
   columns=line.split()
   if len(columns)==2 and 'ro' in columns[1].split(','):
    mount=columns[0];owned.update(p for p in entries if p==mount or p.startswith(mount+'/'))
 else:ownership_complete=False
# Discover local language installation records beyond login-user PATH.
# Reading manifests as data avoids executing package startup hooks.
local_records=[p for p,e in entries.items() if e[0]=='f' and
 (p.endswith('/.crates2.json') or p.endswith('/.crates.toml') or
 ('/specifications/' in p and p.endswith('.gemspec')) or
 ('/pkg/mod/' in p and p.endswith('/go.mod')))]
for i,path in enumerate(local_records):
 data,rc,lev=query('local-language-record-'+str(i),'cat -- '+shlex.quote(path))
 if rc:continue
 if path.endswith('.gemspec'):
  obj(1,'package:gem',path,[data.decode(errors='replace')],lev)
 elif path.endswith('/go.mod'):
  obj(1,'package:go',path,[data.decode(errors='replace')],lev)
 elif path.endswith('.crates2.json'):
  try:
   crates=json.loads(data).get('installs',{})
   for name,record in crates.items():obj(1,'package:cargo',path+':'+name,[record],lev)
  except (ValueError,TypeError):obj(1,'package-record-unparsed',path,[data.decode(errors='replace')],lev)
 else:obj(1,'package:cargo-record',path,[data.decode(errors='replace')],lev)
# Filesystem metadata and explicit startup/shebang candidates are independent of executable bits.
codes,crc,cev=query('code-candidates',"find / "+prune+" -type f -exec sh -c 'for f do case \"$f\" in */.bashrc|*/.bash_profile|*/.bash_login|*/.bash_logout|*/.profile|*/.zshrc|*/.zshenv|*/.zprofile|*/.zlogin|*/.zlogout|*/.kshrc|*/.cshrc|*/.tcshrc|*/.login|*/.logout|*/.xsession|*/.xinitrc|*/config.fish|*/fish/conf.d/*|/etc/profile|/etc/bash.bashrc|/etc/bashrc|/etc/profile.d/*|/etc/zsh/*) printf \"%s\\0\" \"$f\"; continue;; esac; if test -x \"$f\" || test \"$(head -c 2 -- \"$f\" 2>/dev/null)\" = \"#!\"; then printf \"%s\\0\" \"$f\"; fi; done' sh {} +")
code=set(x.decode(errors='surrogateescape') for x in codes.split(b'\0') if x)
groups=collections.defaultdict(list)
for p,e in entries.items():
 if p in owned or canonical(p) in owned:continue
 groups[str(pathlib.PurePosixPath(p).parent)].append(p)
 if p in code:obj(2,'executable-code-outside-packages' if ownership_complete else 'executable-code-outside-packages',p,[e],cev)
for directory,paths in sorted(groups.items()):obj(2,'stored-outside-packages' if ownership_complete else 'stored-outside-packages',directory,sorted(paths),ev)
# Rules are captured without password databases or private keys.
rulepaths=[p for p,e in entries.items() if e[0]=='f' and (p=='/etc/sudoers' or p.startswith(('/etc/sudoers.d/','/etc/polkit-1/rules.d/','/usr/share/polkit-1/rules.d/','/etc/security/access.d/','/etc/pam.d/')) or p in ('/etc/security/access.conf','/etc/pam.d/sudo','/etc/pam.d/sshd'))]
for i,p in enumerate(rulepaths):
 data,rc,rev=query('access-rule-'+str(i),'cat -- '+shlex.quote(p))
 if rc==0:obj(1,'access-rule',p,[data.decode(errors='replace')],rev)
# Public login-key fingerprints, never private key material.
keypaths=[p for p,e in entries.items() if e[0]=='f' and pathlib.PurePosixPath(p).name in ('authorized_keys','authorized_keys2')]
for i,p in enumerate(keypaths):
 data,rc,kev=query('login-keys-'+str(i),'ssh-keygen -lf '+shlex.quote(p))
 if rc==0:obj(1,'login-key',p,[data.decode(errors='replace')],kev)
# Saved connection metadata only, never secret values.
networkpaths=[p for p,e in entries.items() if e[0]=='f' and (p.startswith(('/etc/NetworkManager/system-connections/','/etc/systemd/network/','/var/lib/iwd/')) or p in ('/etc/network/interfaces','/etc/wpa_supplicant/wpa_supplicant.conf'))]
for i,p in enumerate(networkpaths):
 cmd="awk 'BEGIN{IGNORECASE=1} /^[[:space:]]*($|#|;)/ {next} /^[[:space:]]*\\[/ {print;next} /^[[:space:]]*(id|uuid|type|interface-name|ssid|key-mgmt|autoconnect|Name|MACAddress|DHCP|Address|Gateway|DNS|NamePolicy|auto|iface)[[:space:]=]/ {print}' "+shlex.quote(p)
 data,rc,nev=query('saved-network-'+str(i),cmd)
 if rc==0:obj(1,'saved-network',p,[data.decode(errors='replace')],nev)
with (out/'objects.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(fields);w.writerows(objects)
for level in (1,2):
 with (out/f'level-{level}.tsv').open('w',newline='') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(fields);w.writerows(x for x in objects if x[2]==level)
with (out/'coverage.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['query','exit_code','bytes','stdout','stderr']);w.writerows(coverage)
(out/'metadata.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'machine':machine,'system':meta['system'],'mode':mode,'inputs_commit':os.getenv('CAL_INPUTS_COMMIT'),'filesystem_status':fs_rc,'engine_graph_roots':engine_roots,'opaque_storage_paths':sorted(opaque_paths),'container_boundary_gaps':boundary_gaps,'ownership_queries_complete':ownership_complete,'package_parse_gaps':parse_gaps,'unsupported_ownership_managers':sorted(unsupported_ownership),'limitations':['Ownership not established by any queried record is listed as belonging to no package, per the binding input decision.','Failed queries and inaccessible paths are coverage gaps, not evidence of absence.','Container and VM image contents are not expanded.']},indent=2)+'\n')
print('Collection produced; inspect coverage.tsv and metadata.json for failures and limitations.')
PY
