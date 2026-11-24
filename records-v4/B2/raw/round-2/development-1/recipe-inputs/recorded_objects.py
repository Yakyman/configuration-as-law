"""Finite installed-object provenance, with a census independent of declaration rows.

The installation ledger is written by activation, not reconstructed by inventory.
Only exact byte-copy derivations and one native sysctl reader are supported.
"""
import base64,importlib.util,json,pathlib,re
from importlib._bootstrap_external import _code_to_hash_pyc
LEDGER=pathlib.Path('/var/lib/stand/objects.json')

def derived_bytes(source_path,content,algorithm):
    if algorithm=='copy':return content
    if algorithm=='python-bytecode':
        code=compile(content,source_path,'exec',dont_inherit=True,optimize=0)
        return bytes(_code_to_hash_pyc(code,importlib.util.source_hash(content),checked=True))
    raise ValueError('unsupported derivation algorithm')

def validate(rows,d):
    import stand
    files={f['path']:f for r in rows if r['type'] in ('base','program','code') for f in stand.manifest(r,d)}
    identities={}
    settings=set()
    for r in rows:
        identity=r.get('package_identity')
        if identity is not None:
            if r['type'] not in ('program','code') or set(identity)!=({'backend','name','version','architecture'} if identity.get('backend')=='dpkg' else {'backend','name','version'}) or identity['backend'] not in ('stand','dpkg') or not re.fullmatch(r'[a-zA-Z0-9_.:+-]+',identity['name']) or identity['version']!=r['version']:
                raise ValueError('invalid exact package identity')
            if identity['backend']=='dpkg' and r.get('managed'):raise ValueError('native package identity is factory-only')
        for dependency in r.get('package_dependencies',[]):
            if not identity or set(dependency)!={'backend','name','version'} or dependency['backend']!='stand' or not re.fullmatch(r'[a-zA-Z0-9_.:+-]+',dependency['name']) or not isinstance(dependency['version'],str) or not dependency['version']:raise ValueError('unsupported exact dependency identity')
        for item in ([identity] if identity else [])+r.get('package_dependencies',[]):
            key=(item['backend'],item['name'])
            if key in identities and identities[key]!=item:raise ValueError('conflicting installed package identity')
            identities[key]=item
        for default in r.get('default_settings',[]):
            if not identity or set(default)!={'path'} or default['path'] not in {f['path'] for f in stand.manifest(r,d)}:raise ValueError('default requires own package member')
        for edge in r.get('derivations',[]):
            if set(edge)!={'path','source_path','algorithm'} or edge['algorithm'] not in ('copy','python-bytecode'):raise ValueError('unsupported derivation algorithm')
            own={f['path']:f for f in stand.manifest(r,d)}
            src=own.get(edge['source_path']);dst=own.get(edge['path'])
            if not src or not dst or src['kind']!='file' or dst['kind']!='file' or src['path']==dst['path']:raise ValueError('derivation requires distinct exact own source and output')
            if not r.get('managed'):raise ValueError('derivations require managed source payload')
            result=derived_bytes(src['path'],base64.b64decode(src['content_b64'],validate=True),edge['algorithm'])
            if stand.digest(result)!=dst['sha256']:raise ValueError('derived output differs from source algorithm')
        if r.get('derived_from'):
            edge=r['derived_from']
            if r['type'] not in ('service','timer','socket') or set(edge)!={'line','source_path','algorithm'} or edge['algorithm']!='copy':raise ValueError('unsupported unit derivation')
            owner=next((x for x in rows if x['id']==edge['line'] and x['type'] in ('program','code')),None)
            source=next((f for f in stand.manifest(owner,d) if f['path']==edge['source_path']),None) if owner else None
            if not source or source.get('sha256')!=r['unit_sha256']:raise ValueError('unit source must match exact declared source bytes')
        if r['type']=='setting':
            if r.get('name') in settings:raise ValueError('duplicate setting value')
            settings.add(r.get('name'))
            if set(r)!={'id','type','managed','reader','name','value'} or not r['managed'] or r['reader']!='sysctl' or r['name']!='kernel.printk':raise ValueError('unsupported setting reader')
            if not isinstance(r['value'],str) or not re.fullmatch(r'[0-9] [0-9] [0-9] [0-9]',r['value']):raise ValueError('kernel.printk requires four single-digit levels')

def unit_content(r):
    edge=r.get('derived_from')
    if not edge:return r['unit_text']
    content=pathlib.Path(edge['source_path']).read_text()
    if content!=r['unit_text']:raise ValueError('actual generated unit source differs')
    return content

def read_setting(r):
    return {'name':r['name'],'value':' '.join(pathlib.Path('/proc/sys/kernel/printk').read_text().split())}

def expected_entries(rows,d):
    import stand
    entries={}
    for r in rows:
        identity=r.get('package_identity')
        if identity:
            obj=('dpkg:' if identity['backend']=='dpkg' else 'package:stand:')+identity['name']
            value={**identity,'status':'installed'}
            origin={'line':r['id'],'relation':'own','required':value}
            if obj in entries:entries[obj]['origins'].append(origin)
            else:entries[obj]={'object':obj,'kind':'package','identity':identity,'facts':{'package_installed':True},'origins':[origin]}
        for dependency in r.get('package_dependencies',[]):
            obj='package:stand:'+dependency['name']
            required={**dependency,'status':'installed'}
            origin={'line':r['id'],'relation':'derived','required':required,'dependency_identity':dependency}
            existing=entries.get(obj)
            if existing and existing['identity']!=dependency:raise ValueError('conflicting dependency identity')
            if existing:existing['origins'].append(origin)
            else:entries[obj]={'object':obj,'kind':'package','identity':dependency,'facts':{'package_installed':True},'origins':[origin]}
        if r['type'] in ('base','program','code'):
            derived={e['path']:e for e in r.get('derivations',[])}
            defaults={e['path'] for e in r.get('default_settings',[])}
            for f in stand.manifest(r,d):
                if not identity and f['path'] not in derived:continue
                obj=f['path'];value=stand.desired_file(f)
                facts={'package_member':bool(identity),'package_installed':False,'remains_as_received':bool(identity)}
                e=entries.setdefault(obj,{'object':obj,'kind':'file','facts':facts,'origins':[]})
                origin={'line':r['id'],'relation':'derived' if obj in derived else 'package','required':value,'package_default':obj in defaults}
                if obj in derived:origin['derivation']=derived[obj]
                if identity:origin['package_identity']=identity
                e['origins'].append(origin)
        if r.get('derived_from'):
            edge=r['derived_from'];obj='/etc/systemd/system/'+r['unit']
            value={'path':obj,'kind':'file','sha256':r['unit_sha256'],'mode':0o644,'uid':0,'gid':0}
            entries[obj]={'object':obj,'kind':'file','facts':{'package_installed':False,'package_member':False,'executable':False,'setting':True},'origins':[{'line':r['id'],'relation':'own','required':value,'source_line':edge['line'],'derivation':{'path':obj,'source_path':edge['source_path'],'algorithm':'copy'}}]}
        if r['type']=='setting':
            obj='sysctl:'+r['name'];value={'name':r['name'],'value':r['value']}
            entries[obj]={'object':obj,'kind':'setting','facts':{'package_installed':False,'package_member':False,'executable':False,'setting':True,'chosen_value':True,'computer_obeys':True},'origins':[{'line':r['id'],'relation':'own','required':value}]}
    return list(entries.values())

def observed(e):
    import stand
    if e['kind']=='file':return stand.filevalue(e['object'])
    if e['kind']=='setting':return read_setting({'name':e['object'].split(':',1)[1]})
    i=e['identity']
    if i['backend']=='stand':
        installed=json.loads(LEDGER.read_text()) if LEDGER.exists() else []
        registered=next((x for x in installed if x['object']==e['object'] and x['kind']=='package'),None)
        return {**registered['identity'],'status':'installed'} if registered else {'status':'absent'}
    result=stand.run('/usr/bin/dpkg-query','-W','-f=${Version}\t${Architecture}\t${db:Status-Status}',i['name'],check=False)
    parts=result.stdout.strip().split('\t')
    return {'backend':'dpkg','name':i['name'],'version':parts[0] if len(parts)==3 else None,'architecture':parts[1] if len(parts)==3 else None,'status':parts[2] if len(parts)==3 else 'absent'}

def census():
    if not LEDGER.exists():return []
    result=[]
    entries=json.loads(LEDGER.read_text())
    package_states={e['object']:observed(e) for e in entries if e['kind']=='package'}
    for e in entries:
        try:value=observed(e)
        except (OSError,ValueError):value={'unknown':True}
        facts=dict(e['facts'])
        if e['kind']=='file':
            packages=[o['package_identity'] for o in e['origins'] if o.get('package_identity')]
            installed=[i for i in packages if package_states.get(('dpkg:' if i['backend']=='dpkg' else 'package:stand:')+i['name'],{}).get('status')=='installed']
            facts['package_member']=bool(installed)
            facts['remains_as_received']=any(value==o['required'] and o.get('package_identity') in installed for o in e['origins'] if o.get('package_identity'))
        if e['kind']=='package':facts['package_installed']=value.get('status')=='installed'
        result.append({**e,'observed':value,'facts':facts})
    return result

def claims(rows,d,items):
    import stand
    proposed={e['object']:e for e in expected_entries(rows,d)};out={}
    ledger={e['object']:e for e in census()}
    for e in items:
        for origin in ledger.get(e['object'],{}).get('origins',[]):
            candidates=proposed.get(e['object'],{}).get('origins',[])
            if origin not in candidates:continue
            valid=True
            edge=origin.get('derivation')
            if edge:
                src=stand.filevalue(edge['source_path']);dst=stand.filevalue(edge['path'])
                try:valid=src.get('sha256') is not None and stand.digest(derived_bytes(edge['source_path'],pathlib.Path(edge['source_path']).read_bytes(),edge['algorithm']))==dst.get('sha256')
                except (OSError,ValueError,SyntaxError):valid=False
            out.setdefault(e['object'],[]).append({**origin,'provenance_verified':valid})
    return out

def activate(rows,d,old,olddir):
    import stand
    # State readers are the OS interfaces. The ledger records installation
    # provenance only, never substitutes for a file or setting observation.
    for r in rows:
        if r['type']=='setting':pathlib.Path('/proc/sys/kernel/printk').write_text(r['value']+'\n')
    for r in rows:
        for edge in r.get('derivations',[]):
            target=next(f for f in stand.manifest(r,d) if f['path']==edge['path'])
            result=derived_bytes(edge['source_path'],pathlib.Path(edge['source_path']).read_bytes(),edge['algorithm'])
            if stand.digest(result)!=target['sha256']:raise ValueError('actual source differs from declared derivation')
            stand.atomic(edge['path'],result,target['mode'],target['uid'],target['gid'])
    wanted=expected_entries(rows,d)
    existing=json.loads(LEDGER.read_text()) if LEDGER.exists() else []
    keys={e['object'] for e in wanted}
    for e in existing:
        if e['object'] in keys:continue
        # Keep residual provenance until actual removal. Native package state
        # is queried independently and cannot disappear by dropping a line.
        if e['kind']=='file' and stand.filevalue(e['object']).get('missing'):continue
        if e['kind']=='package' and e['identity']['backend']=='dpkg' and observed(e).get('status')!='installed':continue
        if e['kind']=='package' and e['identity']['backend']=='stand':
            prior=next((r for r in old if r['id'] in {o['line'] for o in e['origins']}),None)
            if prior and not any(pathlib.Path(f['path']).exists() for f in stand.manifest(prior,olddir)):continue
        wanted.append(e)
    stand.atomic(LEDGER,stand.canonical(wanted)+'\n',0o600)
