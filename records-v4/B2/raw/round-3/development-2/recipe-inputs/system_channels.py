"""Finite trusted repository and base-transaction catalog admission.

Only catalog exact payloads may modify root paths. Catalog generation is an
image-build operation; ordinary tools only select a recorded complete state.
"""
import base64,copy,hashlib,json,os,pathlib,shutil,tempfile
P=pathlib.Path
CATALOG=P('/usr/local/share/stand/system/catalog.json')
def digest(b):return hashlib.sha256(b).hexdigest()
def catalog():return json.loads(CATALOG.read_bytes())
def update(rows):
    selected=[r for r in rows if r.get('channel')=='system-update']
    if len(selected)>1:raise ValueError('one complete base update state is allowed')
    if selected:validate(selected[0]);return selected[0]
def validate(row):
    c=catalog();channel=row.get('channel')
    if channel=='repository':expected=c['installs'].get(row.get('package'))
    elif channel=='system-update':expected=c['updates'].get(row.get('catalog_key'),{}).get('row')
    else:raise ValueError('unsupported system channel')
    if not expected or row!=expected:raise ValueError('system row differs from trusted exact catalog')
def prepare(tool,args):
    if tool not in ('apt','apt-get'):raise ValueError('unsupported system frontend')
    c=catalog()
    if len(args)==2 and args[0]=='install':
        for row in c['installs'].values():
            if args[1]==row['package']+'='+row['version']:return copy.deepcopy(row)
        raise ValueError('repository package/version is outside exact catalog')
    if len(args)==3 and args[:2]==['upgrade','--stand-catalog']:
        if args[2] not in c['updates']:raise ValueError('unknown exact base transaction')
        return copy.deepcopy(c['updates'][args[2]]['row'])
    raise ValueError('use install PACKAGE=VERSION or upgrade --stand-catalog KEY; alternate roots, hooks and overrides refused')
def cleanfile(f):return {k:v for k,v in f.items() if k!='content_b64'}
def expected_factory(rows,directory=None):
    from stand import load,manifest
    factory_dir=P('/etc/stand/factory');factory={r['id']:copy.deepcopy(r) for r in load(factory_dir,guarded=False)}
    row=update(rows)
    if not row:return factory
    change=catalog()['updates'][row['catalog_key']];new={f['path']:cleanfile(f) for f in change['after']};changed=set(change['paths'])
    original_files={f['path']:f for r in factory.values() if r['type'] in ('base','program','code') for f in manifest(r,factory_dir)}
    for key,r in factory.items():
        if r['type'] not in ('base','program','code'):continue
        fs=manifest(r,factory_dir);out=[new.get(f['path'],f) for f in fs if f['path'] not in changed or f['path'] in new]
        if r['type']=='base':
            existing={f['path'] for f in out}
            out += [f for p,f in new.items() if p not in existing and p.startswith(('/usr/','/etc/','/boot/'))]
            r['version']='system-state:'+row['version']
        if key.startswith('package:') and key[8:] in row['base_packages']:
            r['version']=row['base_packages'][key[8:]]
            if r.get('package_identity'):
                r['package_identity']['version']=r['version']
            artifact=next((a for a in row['artifacts'] if a['package']==key[8:] and a['version']==r['version']),None)
            if artifact:
                r['source']=artifact['source'];r['source_sha256']=artifact['sha256']
            if key[8:] in row['package_members']:
                lookup={p:f for p,f in original_files.items() if p not in changed};lookup.update(new)
                out=[lookup[p] for p in row['package_members'][key[8:]] if p in lookup]
        if out!=fs or 'files_manifest' in r:
            r.pop('files_manifest',None);r.pop('manifest_sha256',None);r['files']=sorted(out,key=lambda x:x['path'])
    return factory

def root_file_allowed(row,f):
    if row.get('channel')!='system-update':return False
    validate(row)
    return f in row['files']

def apply_selection(tool,args):
    import stand
    if args==['remove','system:base-state']:return remove_update()
    row=prepare(tool,args)
    if row['channel']=='repository':return stand.candidate_edit(add=row)
    with stand.transaction():
        current=stand.current_dir();rows=stand.load(current)
        rows=[r for r in rows if r.get('channel')!='system-update']+[row]
        expected=expected_factory(rows)
        rows=[expected.get(r['id'],r) for r in rows]
        with tempfile.TemporaryDirectory(prefix='system-edit-',dir=stand.ROOT) as directory:
            for f in current.iterdir():shutil.copyfile(f,P(directory)/f.name)
            stand.atomic(P(directory)/'machine.jsonl',''.join(stand.canonical(r)+'\n' for r in rows))
            return stand.apply(directory)

def restore_factory_manifests(directory,expected):
    """Carry trusted manifest inputs when returning from inline updated rows."""
    factory=P('/etc/stand/factory')
    for row in expected.values():
        name=row.get('files_manifest')
        if name is None:continue
        if not isinstance(name,str) or P(name).name!=name or name in ('.','..'):
            raise ValueError('invalid trusted factory manifest name')
        data=(factory/name).read_bytes()
        if digest(data)!=row['manifest_sha256']:
            raise ValueError('trusted factory manifest checksum differs')
        (P(directory)/name).write_bytes(data)

def remove_update():
    import stand
    with stand.transaction():
        current=stand.current_dir();rows=[r for r in stand.load(current) if r.get('channel')!='system-update']
        expected=expected_factory(rows)
        rows=[expected.get(r['id'],r) for r in rows]
        with tempfile.TemporaryDirectory(prefix='system-remove-',dir=stand.ROOT) as directory:
            for f in current.iterdir():shutil.copyfile(f,P(directory)/f.name)
            restore_factory_manifests(directory,expected)
            stand.atomic(P(directory)/'machine.jsonl',''.join(stand.canonical(r)+'\n' for r in rows))
            return stand.apply(directory)

def activate(rows,d,old,olddir):
    """Run after quiesce/revocation and before code-policy regeneration."""
    import stand
    current=update(rows);previous=update(old)
    if not current and not previous:return
    c=catalog();selected=current or previous;entry=c['updates'][selected['catalog_key']]
    wanted=entry['after'] if current else entry['before']
    values={f['path']:f for f in wanted}
    for p in entry['paths']:
        if p not in values:
            target=P(p)
            if target.is_file() or target.is_symlink():target.unlink();stand.syncdir(target.parent)
    for f in wanted:
        p=P(f['path']);p.parent.mkdir(parents=True,exist_ok=True)
        if f['kind']=='symlink':
            if p.is_symlink() and os.readlink(p)==f['target']:continue
            p.unlink(missing_ok=True);p.symlink_to(f['target']);stand.syncdir(p.parent)
        else:
            if p.is_symlink():p.unlink()
            stand.atomic(p,base64.b64decode(f['content_b64']),f['mode'],f['uid'],f['gid'])

def observe(row):
    import stand
    validate(row)
    actual=dict(line.split('\t') for line in stand.run('/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\n').stdout.splitlines())
    if row['channel']=='repository':
        files=[stand.filevalue(f['path']) for f in row['files']]
        dependencies={n:{'version':actual.get(n),'declaration_line':v['declaration_line'],'files':[stand.filevalue(f['path']) for f in v['files']]} for n,v in row['dependency_states'].items()}
        return files==[cleanfile(f) for f in row['files']] and dependencies==row['dependency_states'],{'files':files,'dependencies':dependencies}
    # Complete exact map is the required new base state, not an update request.
    files=[stand.filevalue(f['path']) for f in row['files']]
    absent=[p for p in row['absent'] if P(p).exists() or P(p).is_symlink()]
    value={'base_packages':actual,'files':files,'unexpected_present':absent}
    return actual==row['base_packages'] and files==[cleanfile(f) for f in row['files']] and not absent,value
