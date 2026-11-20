#!/usr/bin/env python3
"""A1 deterministic reduction, adapted to dpkg, rpm-ostree and Nix.

Imports only A1's pure grouping helpers from the saved exact source snapshot.
Package membership is the census's operational proxy, not proof of a declaration.
Nix store membership is split into system closure and other paths; the latter
are NOT automatically called recorded. No manual classifications live here.
"""
import ast, collections, csv, hashlib, json, os, pathlib, re
BASE = pathlib.Path(__file__).resolve().parent
source=ast.parse((BASE/'raw/a1-preclass-reference.py').read_text())
helpers=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in {'canon','group','is_data'}]
helpers += [n for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'DOCS','ALIASES'} for t in n.targets)]
exec(compile(ast.Module(body=helpers,type_ignores=[]),'a1-helpers','exec'))
a1_group=group; a1_is_data=is_data
def normalize_home(p):
    return '/home/'+p[len('/var/home/'):] if p.startswith('/var/home/') else p
def group(p):
    if p.startswith('/nix/var/nix/'):
        parts=p.strip('/').split('/')
        return '/nix/var/nix' if len(parts)==4 and parts[3].endswith('.lock') else '/'+ '/'.join(parts[:4])
    if p.startswith('/nix/var/log/nix'):return '/nix/var/log/nix'
    # CoreOS /home is /var/home; retain real pathname in output.
    q=a1_group(normalize_home(p))
    return '/var'+q if p.startswith('/var/home/') and q.startswith('/home/') else q
def is_data(p):return a1_is_data(normalize_home(p))
def write(name,fields,rows):
    with (BASE/name).open('w') as f:
        w=csv.DictWriter(f,fields,delimiter='\t');w.writeheader();w.writerows(rows)
rows=[];stats={}
for machine in ('debian','coreos','nixos'):
    raw=BASE/'raw'/machine
    if not (raw/'files.tsv').exists():continue
    def read(name):return (raw/name).read_text(errors='replace') if (raw/name).exists() else ''
    manager=read('package-manager.txt').strip()
    ALIASES=sorted([tuple(l.split('\t',1)) for l in read('path-aliases.tsv').splitlines() if '\t' in l],key=lambda x:-len(x[0]))
    owned={canon(p) for p in read('package-files.txt').splitlines() if p.startswith('/')}
    closure=set(read('system-closure.txt').splitlines())
    def recorded_path(p):
        if manager=='nix':
            return '/'.join(p.split('/')[:4]) in closure if p.startswith('/nix/store/') else False
        return canon(p) in owned
    def add(kind,path,evidence,cls=None,count=1):
        uid=machine+'-'+hashlib.sha256((kind+'\0'+path).encode()).hexdigest()[:10]
        rows.append(dict(id=uid,machine=machine,kind=kind,path_or_name=path,evidence=evidence,classification=cls,count=count))
    for line in read('packages.tsv').splitlines():
        f=line.split('\t')
        if manager=='dpkg' and (len(f)<3 or not f[2].startswith('ii')):continue
        if manager=='nix':
            if f[0] not in closure:continue
            kind='system-closure-store-object'
        else:kind='package'
        add(kind,f[0],f'raw/{machine}/packages.tsv: {line}','recorded (works)')
    if manager=='nix':
        user_extra=set(read('user-closure.txt').splitlines())-closure
        other=sorted(set(read('store-top-level.txt').splitlines())-closure-user_extra)
        (raw/'user-closure-outside-system.txt').write_text('\n'.join(sorted(user_extra))+'\n')
        if user_extra:add('store-group','user profile closure outside current system closure',f'raw/{machine}/user-closure-outside-system.txt; n={len(user_extra)}; user-profile.txt identifies installed program',count=len(user_extra))
        (raw/'store-outside-system-closure.txt').write_text('\n'.join(other)+'\n')
        if other:add('store-group','/nix/store outside current system closure',f'raw/{machine}/store-outside-system-closure.txt; n={len(other)}; profiles in user-profile.txt/root-profile.txt',count=len(other))
    unowned=collections.defaultdict(list);own_groups=collections.Counter();ftypes=collections.Counter()
    for line in read('files.tsv').splitlines():
        f=line.split('\t')
        if len(f)!=4:continue
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
    for key,n in sorted(own_groups.items()):add('package-owned-paths',key,f'raw/{machine}/files.tsv intersect package-files.txt; n={n}','recorded (works)',n)
    unit_real=dict(l.split('\t',1) for l in read('unit-realpaths.tsv').splitlines() if '\t' in l)
    for scope,filename in [('system','units.txt'),('user','user-list-units.txt')]:
        unitmap={}
        for block in read('unit-paths.txt' if scope=='system' else 'user-unit-paths.txt').split('\n\n'):
            props=dict(l.split('=',1) for l in block.splitlines() if '=' in l)
            if props.get('Id'):unitmap[props['Id']]=props
        dyn=collections.defaultdict(list)
        for line in read(filename).splitlines():
            f=line.split()
            if len(f)<4 or '.' not in f[0] or f[1] not in {'loaded','not-found','masked','error','bad-setting'}:continue
            unit=f[0];props=unitmap.get(unit,{});frag=props.get('FragmentPath','')
            checks=[frag]+props.get('DropInPaths','').split()
            if frag and all(recorded_path(p) or recorded_path(unit_real.get(p,'')) for p in checks):add(scope+'-unit',unit,f'raw/{machine}/{filename}: {line}; fragment={frag}; dropins='+props.get('DropInPaths',''),'recorded (works)')
            elif f[1]=='not-found':dyn['not-found'].append(unit)
            elif unit.endswith(('.device','.scope','.mount','.automount','.slice','.target','.socket','.path')):dyn[unit.rsplit('.',1)[1]].append(unit)
            else:add(scope+'-unit',unit,f'raw/{machine}/{filename}: {line}; properties='+json.dumps(props,sort_keys=True))
        for typ,items in sorted(dyn.items()):add(scope+'-units','unpackaged *.'+typ,f'raw/{machine}/{filename}; members='+','.join(items),count=len(items))
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
        add('process',key,f'raw/{machine}/processes.txt + process-executables.tsv; pids='+','.join(i[0][0] for i in items),'recorded (works)' if exe and recorded_path(exe) else None,len(items))
    builders=[]
    for line in read('accounts.txt').splitlines():
        if machine=='nixos' and re.match(r'^nixbld\d+:',line):builders.append(line);continue
        f=line.split(':');add('account',f[0],f'raw/{machine}/accounts.txt: uid={f[2]} gid={f[3]} home={f[5]} shell={f[6]}')
    if builders:
        (raw/'nix-builder-accounts.txt').write_text('\n'.join(builders)+'\n')
        add('account-group','Nix build users (nixbld1..nixbld32)',f'raw/{machine}/nix-builder-accounts.txt; n={len(builders)}; evaluated declaration in account-definitions.txt',count=len(builders))
    paths=dict(l.split('\t',1) for l in read('module-files.tsv').splitlines() if '\t' in l)
    for line in read('modules.txt').splitlines()[1:]:
        f=line.split();path=paths.get(f[0],'');add('kernel-module',f[0],f'raw/{machine}/modules.txt: {line}; path={path}','recorded (works)' if path and recorded_path(path) else None)
    stats[machine]=dict(package_manager=manager,file_entries=sum(ftypes.values()),file_types=ftypes,package_owned_entries=sum(own_groups.values()),unowned_entries=sum(map(len,unowned.values())),unowned_groups=len(unowned),accounts=len(read('accounts.txt').splitlines()),processes=len(read('processes.txt').splitlines())-1,loaded_modules=len(read('modules.txt').splitlines())-1,driver_bindings=len(read('device-drivers.tsv').splitlines()))
rows.sort(key=lambda r:(r['machine'],r['kind'],r['path_or_name']))
res=[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],short_evidence=r['evidence']) for r in rows if r['classification'] is None]
write('residual.tsv',['id','machine','kind','path_or_name','short_evidence'],res)
write('preclassified.tsv',['id','machine','kind','path_or_name','class','member_count','evidence'],[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],**{'class':r['classification']},member_count=r['count'],evidence=r['evidence']) for r in rows if r['classification'] is not None])
(BASE/'inventory-stats.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(dict(residual=len(res),preclassified=len(rows)-len(res),stats=stats),indent=2))
if len(res)>400:raise SystemExit('Residual >400; regroup explicitly, never truncate.')
