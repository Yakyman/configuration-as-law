#!/usr/bin/env python3
"""Deterministic A1 reduction. No manual class decisions live in this script.

Package database membership is the census's operational recorded proxy, not proof
of a person-designated declaration. Project/document roots use the census's data
convention. All other observations remain residual, including unreadable paths.
"""
import collections, csv, gzip, hashlib, json, os, pathlib, re, sys
BASE = pathlib.Path(__file__).resolve().parent
DOCS = {'Documents','Pictures','Photos','Music','Videos','Desktop','Документы','Изображения'}
ALIASES = []

def canon(p):
    p = os.path.normpath(p)
    for a,b in ALIASES:
        if p == a or p.startswith(a+'/'): return b+p[len(a):]
    return p

def group(path):
    parts = path.strip('/').split('/')
    if path == '/root' or path.startswith('/root/'):
        home = '/root'; rest = parts[1:]
    elif len(parts) >= 2 and parts[0] == 'home':
        home = '/'+ '/'.join(parts[:2]); rest = parts[2:]
    else:
        if len(parts) >= 3 and '/'.join(parts[:2]) in ('var/lib','var/cache','var/log','var/spool','usr/local'):
            return '/'+ '/'.join(parts[:3])
        return '/'+ '/'.join(parts[:2])
    if not rest: return home
    n = 1
    if rest[0] in ('.config','.cache','Projects') and len(rest)>1: n = 2
    if rest[0] == '.local' and len(rest)>1:
        n = 3 if rest[1] in ('share','state') and len(rest)>2 else 2
    return home+'/'+ '/'.join(rest[:n])

def is_data(path):
    parts = path.strip('/').split('/')
    rest = parts[2:] if len(parts)>2 and parts[0]=='home' else parts[1:] if parts[0]=='root' else []
    return bool(rest and rest[0] in DOCS | {'Projects'})

def write_tsv(name, fields, rows):
    with (BASE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)

all_rows=[]; all_stats={}
for machine in ('laptop','server'):
    raw=BASE/'raw'/machine
    read=lambda name: (raw/(name+'.stdout')).read_text(errors='replace') if (raw/(name+'.stdout')).exists() else ''
    alias_rows = [json.loads(line) for line in read('path-aliases').splitlines()]
    ALIASES = sorted([(r['path'],r['realpath']) for r in alias_rows if r.get('realpath') and r['path'] != r['realpath']],key=lambda t:-len(t[0]))
    owned={canon(p) for p in read('package-paths').splitlines() if p.startswith('/')}
    pending=[]
    def add(kind,path,evidence,cls=None,count=1):
        pending.append(dict(machine=machine,kind=kind,path_or_name=path,evidence=evidence,classification=cls,count=count))
    for line in read('packages').splitlines():
        fields=line.split('\t')
        if len(fields)>1 and fields[1]!='installed': continue
        add('package',fields[0],f'raw/{machine}/packages.stdout: {line}','recorded (works)')
    groups={}; owned_groups=collections.Counter(); stats=collections.Counter(); errors=[]; meta=[]
    if '--reuse-stored' in sys.argv:
        groups=json.loads((raw/'stored-groups.json').read_text())
        stats=collections.Counter(json.loads((BASE/'inventory-stats.json').read_text())[machine])
        errors=json.loads((raw/'walk-errors.json').read_text())
        meta=json.loads((raw/'walk-meta.json').read_text())
        for r in csv.DictReader((BASE/'preclassified.tsv').open(),delimiter='\t'):
            if r['machine']==machine and r['kind']=='package-owned-paths': owned_groups[r['path_or_name']]=int(r['member_count'])
    else:
        with gzip.open(raw/'unowned.jsonl.gz','wt') as uf, gzip.open(raw/'walk.jsonl.gz','rt') as source:
            for line in source:
                row=json.loads(line)
                if row['kind']=='entry':
                    stats['entries']+=1; stats[row['type']]+=1
                    path=row['path']; key=group(path)
                    if canon(path) in owned:
                        stats['owned_entries']+=1;owned_groups[key]+=1;continue
                    stats['unowned_entries']+=1
                    row['group']=key;uf.write(json.dumps(row,ensure_ascii=True)+'\n')
                    g=groups.setdefault(key,{'count':0,'types':collections.Counter(),'samples':[]})
                    g['count']+=1;g['types'][row['type']]+=1
                    if len(g['samples'])<4 and row['type']!='directory':g['samples'].append(path)
                elif row['kind']=='error': errors.append(row)
                else: meta.append(row)
    (raw/'walk-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
    (raw/'walk-meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    (raw/'stored-groups.json').write_text(json.dumps(groups,indent=2)+'\n')
    for key,g in sorted(groups.items()):
        evidence=f"raw/{machine}/unowned.jsonl.gz group={key}; n={g['count']}; types={dict(g['types'])}; samples="+' | '.join(g['samples'])
        add('stored',key,evidence,'data' if is_data(key) else None,g['count'])
    for key,n in sorted(owned_groups.items()):
        add('package-owned-paths',key,f'raw/{machine}/walk.jsonl.gz intersect package-paths.stdout; observed package-owned entries={n}','recorded (works)',n)
    unreadable_seen=set()
    for e in errors:
        # Access failures are evidence limitations, not invented stored contents.
        if e['operation']=='lstat': continue
        k=group(e['path'])
        if k in groups or k in unreadable_seen or canon(e['path']) in owned: continue
        unreadable_seen.add(k)
        add('unreadable-directory',k,f"raw/{machine}/walk-errors.json: {e['path']}: {e['error']}")
    for scope in ('system','user'):
        name=scope+'-unit-paths-retry' if (raw/(scope+'-unit-paths-retry.stdout')).exists() else scope+'-unit-paths'
        unitmap={}
        for block in (read(scope+'-installed-unit-paths')+'\n\n'+read(name)).strip().split('\n\n'):
            props=dict(line.split('=',1) for line in block.splitlines() if '=' in line)
            if props.get('Id'):unitmap[props['Id']]=props
        for line in read(scope+'-template-unit-paths').splitlines():
            r=json.loads(line)
            if r.get('kind')=='template': unitmap.setdefault(r['unit'],dict(Id=r['unit'],FragmentPath=r.get('selected',''),SourcePath='',DropInPaths='',UnverifiedTemplateDropins='yes'))
        dynamic=collections.defaultdict(list)
        seen_units=set()
        for line in read(scope+'-units').splitlines():
            fields=line.split()
            if not fields:continue
            unit=fields[0];seen_units.add(unit);props=unitmap.get(unit,{});frag=props.get('FragmentPath','');source=props.get('SourcePath','')
            ev=f'raw/{machine}/{scope}-units.stdout: {line}; {name}.stdout: '+json.dumps(props,sort_keys=True)
            drops=props.get('DropInPaths','').split()
            if frag and canon(frag) in owned and all(canon(d) in owned for d in drops):
                add(scope+'-unit',unit,ev,'recorded (works)')
            elif unit.endswith(('.device','.scope','.mount','.automount','.slice','.target','.socket','.path')):
                dynamic[(unit.rsplit('.',1)[1],frag,source,props.get('DropInPaths',''))].append(dict(unit=unit,properties=props))
            else:add(scope+'-unit',unit,ev)
        for (typ,frag,source,drops),items in sorted(dynamic.items()):
            provenance=';'.join((frag,source,drops))
            suffix=hashlib.sha256(provenance.encode()).hexdigest()[:8]
            dest=f'{scope}-unpackaged-{typ}-{suffix}.json';(raw/dest).write_text(json.dumps(items,indent=2)+'\n')
            add(scope+'-units',f'unpackaged *.{typ} [{provenance}]',f'raw/{machine}/{dest}; count={len(items)}; examples='+', '.join(i['unit'] for i in items[:5]),count=len(items))
        for line in read(scope+'-unit-files').splitlines():
            f=line.split()
            if not f or f[0] in seen_units:continue
            unit=f[0];props=unitmap.get(unit,{});frag=props.get('FragmentPath','');drops=props.get('DropInPaths','').split()
            cls='recorded (works)' if frag and canon(frag) in owned and all(canon(d) in owned for d in drops) and not props.get('UnverifiedTemplateDropins') else None
            add(scope+'-unit-file',unit,f'raw/{machine}/{scope}-unit-files.stdout: {line}; installed/template-unit-paths.stdout: '+json.dumps(props,sort_keys=True),cls)
    exes={r['pid']:r.get('exe') for r in map(json.loads,read('process-exes').splitlines())}
    procs=collections.defaultdict(list)
    for line in read('process-pids').splitlines()[1:]:
        f=line.split(None,3)
        if len(f)<4:continue
        pid=int(f[0]);exe=exes.get(pid);key=exe or f[2]
        # Kernel workers are one program family; preserve all members in raw.
        if not exe and f[3].startswith('['):key='kernel threads'
        procs[key].append({'pid':pid,'user':f[1],'comm':f[2],'args':f[3],'exe':exe})
    for key,items in sorted(procs.items()):
        exe=items[0]['exe'];n=len(items)
        add('process',key,f'raw/{machine}/process-pids.stdout and process-exes.stdout; count={n}; pids='+','.join(str(i['pid']) for i in items), 'recorded (works)' if exe and canon(exe.removesuffix(' (deleted)')) in owned and not exe.endswith(' (deleted)') else None,n)
    for line in read('accounts').splitlines():
        f=line.split(':'); add('account',f[0],f'raw/{machine}/accounts.stdout: uid={f[2]} gid={f[3]} home={f[5]} shell={f[6]}')
    paths={}
    for line in read('module-paths').splitlines():
        f=line.replace('\\t','\t').split('\t',1)
        if len(f)==2:paths[f[0]]=f[1]
    for line in read('modules').splitlines()[1:]:
        f=line.split();path=paths.get(f[0],'')
        add('kernel-module',f[0],f'raw/{machine}/modules.stdout: {line}; module-paths.stdout: {path}','recorded (works)' if path and canon(path) in owned else None)
    stats['walk_errors']=len(errors);stats['package_path_set']=len(owned);all_stats[machine]=dict(stats)
    # Bounded grouping, before any manual classification. Membership retains
    # every original row; no observations are discarded to meet the row cap.
    reduced={}; memberships={}
    for r in pending:
        key=None
        if r['classification'] is None:
            if r['kind']=='process': key=('processes','processes with unverified package-owned executable')
            elif r['kind']=='account': key=('accounts','all enumerated accounts')
            elif r['kind'] in ('system-unit','user-unit','system-unit-file','user-unit-file'):
                key=(r['kind']+'s','unpackaged or overridden '+r['kind']+' inventory')
            elif r['kind'] in ('system-units','user-units') and '/run/systemd/generator/' in r['path_or_name'] and ';/etc/fstab;' in r['path_or_name']:
                key=(r['kind'],'generated mount units from /etc/fstab')
            elif r['kind']=='stored':
                path=r['path_or_name']; leaf=path.rsplit('/',1)[-1]
                if '/.cache/' in path and re.match(r'^(?:[abefilmnr]\d|re\d|lighta-export|lp-burst|lp2s)',leaf) and groups[path]['types'].get('directory',0):
                    key=('stored',path.split('/.cache/')[0]+'/.cache/{project-worktrees}')
                elif '/.cache/' in path and leaf.startswith('n81') and leaf.endswith('.log'):
                    key=('stored',path.split('/.cache/')[0]+'/.cache/{n81-build-logs}')
                elif path.startswith('/var/log/') and re.match(r'^(boot.log|btmp|snapper.log)',leaf):
                    key=('stored','/var/log/'+re.split(r'(?<=log)[.-]|(?<=btmp)\.',leaf)[0]+'{rotations}')
                elif re.match(r'^/etc/(?:passwd|group|shadow|gshadow|subuid|subgid)-$',path):
                    key=('stored','/etc/{account-database-backups}')
        if key is None: key=(r['kind'],r['path_or_name'])
        if key not in reduced: reduced[key]=dict(r,kind=key[0],path_or_name=key[1],count=0)
        reduced[key]['count']+=r['count'];memberships.setdefault(key,[]).append(r)
    member_output={}
    for key,items in memberships.items():
        if len(items)>1 or (items[0]['kind'],items[0]['path_or_name']) != key:
            label=key[0]+'::'+key[1];member_output[label]=items
            reduced[key]['evidence']=f'raw/{machine}/group-members.json key={label}; original rows={len(items)}; member count={reduced[key]["count"]}'
    (raw/'group-members.json').write_text(json.dumps(member_output,indent=2)+'\n')
    pending=list(reduced.values())
    for r in sorted(pending,key=lambda r:(r['kind'],r['path_or_name'])):
        r['id']=('L' if machine=='laptop' else 'S')+'-'+hashlib.sha256((r['kind']+'\0'+r['path_or_name']).encode()).hexdigest()[:10]
        all_rows.append(r)
res=[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],short_evidence=r['evidence']) for r in all_rows if r['classification'] is None]
write_tsv('residual.tsv',['id','machine','kind','path_or_name','short_evidence'],res)
write_tsv('preclassified.tsv',['id','machine','kind','path_or_name','class','member_count','evidence'],[dict(id=r['id'],machine=r['machine'],kind=r['kind'],path_or_name=r['path_or_name'],**{'class':r['classification']},member_count=r['count'],evidence=r['evidence']) for r in all_rows if r['classification'] is not None])
(BASE/'inventory-stats.json').write_text(json.dumps(all_stats,indent=2)+'\n')
print(json.dumps({'residual_rows':len(res),'preclassified_rows':len(all_rows)-len(res),'stats':all_stats},indent=2))
if len(res)>700: raise SystemExit('Residual exceeds 700: refine documented grouping, do not truncate.')
