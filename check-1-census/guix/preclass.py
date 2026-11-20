#!/usr/bin/env python3
"""Guix reduction: current-system closure membership is an INVENTORY PROXY
ONLY, never proof of person designation/P1/P4. Exact A1 helpers reused.
No manual classifications imported. Full store file walk is unnecessary.
"""
import ast, collections, csv, hashlib, json, os, pathlib, re
BASE = pathlib.Path(__file__).resolve().parent
source=ast.parse((BASE/'raw/a1-preclass-reference.py').read_text())
helpers=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in {'canon','group','is_data'}]
helpers += [n for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'DOCS','ALIASES'} for t in n.targets)]
exec(compile(ast.Module(body=helpers,type_ignores=[]),'a1-helpers','exec'))
a1_group=group; a1_is_data=is_data
def group(p):
    parts=p.strip('/').split('/')
    if p.startswith('/var/guix/profiles/per-user/'):
        if len(parts)>=6:
            family=re.sub(r'-[0-9]+-link$', '', parts[5])
            return '/'+ '/'.join(parts[:5]+[family])
        return p
    if p.startswith('/var/db/'):
        return '/'+ '/'.join(parts[:3])
    if p.startswith('/var/run/') and len(parts)>2 and parts[2] in {'dhcpcd','nscd','ntpd','shepherd','sshd','udisks2','dbus'}:
        return '/'+ '/'.join(parts[:3])
    if p.startswith('/var/guix/'):
        return '/'+'/'.join(p.strip('/').split('/')[:3])
    return a1_group(p)
def is_data(p):return a1_is_data(p)
def write(name,fields,rows):
    with (BASE/name).open('w') as f:
        w=csv.DictWriter(f,fields,delimiter='\t');w.writeheader();w.writerows(rows)
rows=[];stats={}
for machine in ('guix',):
    raw=BASE/'raw'/machine
    if not (raw/'files.tsv').exists():raise SystemExit('Missing raw/guix/files.tsv; collect first.')
    def read(name):return (raw/name).read_text(errors='replace') if (raw/name).exists() else ''
    manager=read('package-manager.txt').strip()
    if manager!='guix':raise SystemExit('Expected Guix package-manager marker')
    ALIASES=sorted([tuple(l.split('\t',1)) for l in read('path-aliases.tsv').splitlines() if '\t' in l],key=lambda x:-len(x[0]))
    owned=set()
    closure=set(read('system-closure.txt').splitlines())
    def recorded_path(p):
        if manager=='guix':
            return '/'.join(p.split('/')[:4]) in closure if p.startswith('/gnu/store/') else False
        return canon(p) in owned
    def add(kind,path,evidence,cls=None,count=1):
        uid=machine+'-'+hashlib.sha256((kind+'\0'+path).encode()).hexdigest()[:10]
        rows.append(dict(id=uid,machine=machine,kind=kind,path_or_name=path,evidence=evidence,classification=cls,count=count))
    for path in sorted(closure):
        if not path.startswith('/gnu/store/'):
            raise SystemExit('Unexpected system closure entry: '+repr(path))
        add('system-closure-store-object',path,f'raw/{machine}/system-closure.txt: {path}; CURRENT-SYSTEM CLOSURE INVENTORY PROXY ONLY','recorded (works)')
    if manager=='guix':
        user_extra=set(read('user-closure.txt').splitlines())-closure
        home_outside=set(read('home-closure.txt').splitlines())-closure
        (raw/'home-closure-outside-system.txt').write_text('\n'.join(sorted(home_outside))+'\n')
        home_extra=home_outside-user_extra
        other=sorted(set(read('store-top-level.txt').splitlines())-closure-user_extra-home_extra)
        (raw/'home-closure-outside-system-and-user.txt').write_text('\n'.join(sorted(home_extra))+'\n')
        if home_extra:add('store-group','Guix Home closure outside current system and user-package closures',f'raw/{machine}/home-closure-outside-system-and-user.txt; n={len(home_extra)}; home declaration captured under configuration/',count=len(home_extra))
        (raw/'user-closure-outside-system.txt').write_text('\n'.join(sorted(user_extra))+'\n')
        profile_links=dict(line.split('\t',1) for line in read('guix-profiles.tsv').splitlines() if '\t' in line)
        user=read('census-user.txt').strip()
        profile='/home/'+user+'/.guix-profile'
        for _ in range(12):
            if profile not in profile_links: break
            target=profile_links[profile]
            profile=os.path.normpath(target if target.startswith('/') else os.path.join(os.path.dirname(profile),target))
        package_paths={line.split('\t')[-1].strip() for line in read('user-profile.txt').splitlines() if '\t' in line}
        split=set()
        if profile in user_extra:
            add('user-profile-state',profile,f'raw/{machine}/configuration/home/{user}/.guix-profile/manifest; raw/{machine}/guix-profiles.tsv; raw/{machine}/day/user-day.log: Guix generated persistent selection manifest after ordinary-user guix install; both declaration hashes unchanged')
            split.add(profile)
        for path in sorted(package_paths & user_extra):
            add('user-profile-package',path,f'raw/{machine}/user-profile.txt; raw/{machine}/day/user-day.log: installed and executed by ordinary user; outside current system closure; compare raw/{machine}/home-closure.txt')
            split.add(path)
        support=sorted(user_extra-split)
        (raw/'user-profile-support-outside-system.txt').write_text('\n'.join(support)+'\n')
        if support:add('store-group','user profile support outside current system closure',f'raw/{machine}/user-profile-support-outside-system.txt; n={len(support)}; package/profile objects retained in separate rows',count=len(support))
        (raw/'store-outside-system-closure.txt').write_text('\n'.join(other)+'\n')
        if other:add('store-group','/gnu/store outside current system closure',f'raw/{machine}/store-outside-system-closure.txt; n={len(other)}; profiles in user-profile.txt/root-profile.txt',count=len(other))
    unowned=collections.defaultdict(list);own_groups=collections.Counter();ftypes=collections.Counter()
    for line in read('files.tsv').splitlines():
        f=line.split('\t')
        if len(f)!=4:raise SystemExit('Malformed filesystem row; no silent dropping: '+repr(line))
        typ,path,target,size=f;ftypes[typ]+=1
        if recorded_path(path):own_groups[group(path)]+=1
        else:unowned[group(path)].append(dict(type=typ,path=path,target=target,size=int(size)))
    (raw/'unowned-groups.json').write_text(json.dumps(unowned,indent=2)+'\n')
    directories={k:v for k,v in unowned.items() if all(r['type']=='d' for r in v)}
    (raw/'directory-only-groups.json').write_text(json.dumps(directories,indent=2)+'\n')
    if directories:add('stored-directory-skeleton','directory-only remainder',f'raw/{machine}/directory-only-groups.json; directory groups={len(directories)}; all members retained; no content-bearing group merged',count=sum(map(len,directories.values())))
    for key,items in sorted(unowned.items()):
        if key in directories:continue
        samples=[r['path']+(' -> '+r['target'] if r['target'] else '') for r in items if r['type']!='d'][:4]
        add('stored',key,f'raw/{machine}/unowned-groups.json group={key}; n={len(items)}; samples='+ ' | '.join(samples),'data' if is_data(key) else None,len(items))
    for key,n in sorted(own_groups.items()):add('package-owned-paths',key,f'raw/{machine}/files.tsv intersect current-system closure; INVENTORY PROXY ONLY; n={n}','recorded (works)',n)
    # Status alone is insufficient to infer service provenance.
    for scope,filename in [('system','herd-status.txt'),('user','user-herd-status.txt')]:
        service_rows=[]
        for line in read(filename).splitlines():
            match=re.match(r'^\s*[+*−-]\s+(.+?)\s*$',line)
            if match:
                name=match.group(1)
                service_rows.append(dict(name=name,line=line))
                add(scope+'-service',name,f'raw/{machine}/{filename}: {line}; generated definitions in configuration/; provenance not inferred from status')
        if read(filename).strip() and not service_rows:
            add(scope+'-service-inventory','Shepherd status (unparsed)',f'raw/{machine}/{filename}; all output preserved; parsing limit')
        (raw/(scope+'-service-members.json')).write_text(json.dumps(service_rows,indent=2)+'\n')
    exes={}
    for line in read('process-executables.tsv').splitlines():
        f=line.split('\t');
        if len(f)==3:exes[f[0]]=f[2]
    procs=collections.defaultdict(list)
    for line in read('processes.txt').splitlines()[1:]:
        f=line.split(None,4)
        if len(f)<5:continue
        exe=exes.get(f[0],'');key=exe or ('kernel threads' if f[4].startswith('[') else f[3]);procs[key].append((f,exe))
    for key,items in sorted(procs.items()):
        exe=items[0][1]
        add('process',key,f'raw/{machine}/processes.txt + process-executables.tsv; closure labels are INVENTORY PROXY ONLY; pids='+','.join(i[0][0] for i in items),'recorded (works)' if exe and not exe.endswith(' (deleted)') and recorded_path(exe) else None,len(items))
    builders=[]
    for line in read('accounts.txt').splitlines():
        if re.match(r'^guixbuilder\d+:',line):builders.append(line);continue
        f=line.split(':');add('account',f[0],f'raw/{machine}/accounts.txt: uid={f[2]} gid={f[3]} home={f[5]} shell={f[6]}')
    if builders:
        (raw/'guix-builder-accounts.txt').write_text('\n'.join(builders)+'\n')
        add('account-group','Guix build users',f'raw/{machine}/guix-builder-accounts.txt; n={len(builders)}; generated configuration under configuration/',count=len(builders))
    paths=dict(l.split('\t',1) for l in read('module-files.tsv').splitlines() if '\t' in l)
    for line in read('modules.txt').splitlines()[1:]:
        f=line.split();path=paths.get(f[0],'');add('kernel-module',f[0],f'raw/{machine}/modules.txt: {line}; path={path}; closure labels are INVENTORY PROXY ONLY','recorded (works)' if path and recorded_path(path) else None)
    stats[machine]=dict(package_manager=manager,file_entries=sum(ftypes.values()),file_types=ftypes,package_owned_entries=sum(own_groups.values()),unowned_entries=sum(map(len,unowned.values())),unowned_groups=len(unowned),accounts=len(read('accounts.txt').splitlines()),processes=len(read('processes.txt').splitlines())-1,loaded_modules=len(read('modules.txt').splitlines())-1,driver_bindings=len(read('device-drivers.tsv').splitlines()))
# All observation memberships/cardinalities, including service and process rows.
(BASE/'raw/guix/group-members.json').write_text(json.dumps(rows,indent=2)+'\n')
rows.sort(key=lambda r:(r['machine'],r['kind'],r['path_or_name']))
res=[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],short_evidence=r['evidence']) for r in rows if r['classification'] is None]
write('residual.tsv',['id','machine','kind','path_or_name','short_evidence'],res)
write('preclassified.tsv',['id','machine','kind','path_or_name','class','member_count','evidence'],[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],**{'class':r['classification']},member_count=r['count'],evidence=r['evidence']) for r in rows if r['classification'] is not None])
(BASE/'inventory-stats.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(dict(residual=len(res),preclassified=len(rows)-len(res),stats=stats),indent=2))
if len(res)>400:raise SystemExit('Residual >400; regroup explicitly, never truncate.')
