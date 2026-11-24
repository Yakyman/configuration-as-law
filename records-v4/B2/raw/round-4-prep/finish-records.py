#!/usr/bin/env python3
"""Offline input audit and full-text publication formatting; no VM operations."""
import base64,hashlib,json,pathlib,runpy
ROOT=pathlib.Path(__file__).resolve().parents[2]
CASES=ROOT/'cases-6'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(path,data):path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
def machine(bundle):return bundle['files']['/var/lib/stand/current/machine.jsonl'].splitlines(keepends=True)
names=['case-1','case-2a','case-3-before','case-3-after','case-4-both','case-4-one','case-4-none']
bundles={};identities={}
for name in names:
    directory=CASES/name;bundle=json.loads((directory/'declaration.json').read_bytes());bundles[name]=bundle
    assert bundle['format']=='bc3-complete-declaration-v1' and len(bundle['files'])==8
    payloads=json.loads((directory/'blobs.json').read_bytes())
    for digest,value in payloads.items():assert sha(base64.b64decode(value,validate=True))==digest
    (directory/'files').mkdir(exist_ok=True);identity={}
    for source,text in bundle['files'].items():
        if source.endswith('/machine.jsonl'):filename='machine.jsonl'
        elif source.endswith('/base-files.json'):filename='base-files.json'
        elif source.endswith('/bc3-primary.json'):filename='designation.json'
        else:filename='filesystem-'+source.split('/')[4]+'.json'
        (directory/'files'/filename).write_bytes(text.encode());identity[source]={'sha256':sha(text.encode()),'full_text':'files/'+filename}
        if filename.startswith('filesystem-'):
            state=json.loads(text)
            assert set(state['paths'].values())==set(state['objects'])
            for node in state['objects'].values():
                if 'sha256' in node:assert node['sha256'] in payloads
    rows=[json.loads(s) for s in machine(bundle)]
    assert len(rows)==len({r['id'] for r in rows})
    for row in rows:
        if 'files_manifest' in row:assert sha(bundle['files']['/var/lib/stand/current/'+row['files_manifest']].encode())==row['manifest_sha256']
    identities[name]={'sha256':sha((directory/'declaration.json').read_bytes()),'blobs_sha256':sha((directory/'blobs.json').read_bytes()),'files':identity,'machine_rows':len(rows)}
write(CASES/'declarations.json',identities)
assert (CASES/'case-1/declaration.json').read_bytes()==(CASES/'case-3-before/declaration.json').read_bytes()

removed={};deltas={}
for before,after,ids in [('case-3-before','case-3-after',['dev-worker','dev-service','dev-rule']),('case-4-both','case-4-one',['bc4:owner-a']),('case-4-one','case-4-none',['bc4:owner-b'])]:
    old,new=bundles[before],bundles[after];oldlines=machine(old);newlines=machine(new)
    assert [s for s in oldlines if json.loads(s)['id'] not in ids]==newlines
    removed[before+' -> '+after]=[{'id':json.loads(s)['id'],'sha256':sha(s.encode()),'full_text':s} for s in oldlines if json.loads(s)['id'] in ids]
    changes={}
    for path in old['files']:
        if old['files'][path]==new['files'][path]:continue
        entry={'before_sha256':sha(old['files'][path].encode()),'after_sha256':sha(new['files'][path].encode())}
        if '/stand-fs/' in path:
            a,b=json.loads(old['files'][path]),json.loads(new['files'][path]);paths={}
            for name in sorted(set(a['paths'])|set(b['paths'])):
                ai,bi=a['paths'].get(name),b['paths'].get(name)
                av,bv=a['objects'].get(ai),b['objects'].get(bi)
                if ai==bi and av==bv:continue
                fields=sorted(k for k in set(av or {})|set(bv or {}) if (av or {}).get(k)!=(bv or {}).get(k))
                paths[name]={'before_inode':ai,'after_inode':bi,'changed_fields':fields,'before':av,'after':bv}
            entry['paths']=paths
            entry['other_fields']={k:{'before':a.get(k),'after':b.get(k)} for k in set(a)|set(b) if k not in ('paths','objects') and a.get(k)!=b.get(k)}
        changes[path]=entry
    deltas[before+' -> '+after]={'removed_machine_ids':ids,'surviving_machine_lines_byte_identical':True,'constituent_changes':changes}
write(CASES/'removed-lines.json',removed);write(CASES/'removal-deltas.json',deltas)

explanations={
 'base':'Exact image identity and referenced file manifest with digest, explicit file bytes/metadata.',
 'program':'Exact version/source, file requirements and any package/dependency identity; content is fixed, no moving resolver.',
 'code':'Exact source/version and every code file requirement.',
 'account':'Explicit name, numeric UID/GID, groups, shell, home and GECOS.',
 'group':'Explicit group name, numeric GID and members.',
 'service':'Explicit unit identity, enabled state, unit checksum; managed unit text and active state when present.',
 'timer':'Explicit timer identity, enablement, unit checksum and any declared activity.',
 'socket':'Explicit socket identity, enablement, unit checksum and any declared activity.',
 'privilege':'Exact configuration text and mode/UID/GID.',
 'login-key':'Exact authorization text and mode/UID/GID.',
 'password-login':'Explicit disallowed password authentication.',
 'port':'Explicit protocol, local address, port and listening requirement.',
 'boot':'Explicit disk boot and guest_can_change:false; actual host launch evidence is required.',
 'rule':'Exact backend and stated required values; backend mapping is fixed in the pinned implementation.',
 'setting':'Explicit reader/path/name and exact stated value.'}
audit=[]
for line in machine(bundles['case-1']):
    row=json.loads(line);entry={'id':row['id'],'type':row['type'],'line_sha256':sha(line.encode()),'fields':sorted(row),'reason':explanations[row['type']]}
    if row.get('backend')=='code-boundary':entry['verification_limit']='The broad prose predicates are preserved literally. Exact implementation policy/configuration can be compared; these queries do not prove every possible execution satisfies the prose. Any unavailable required observation remains unresolved, not a pass.'
    audit.append(entry)
write(CASES/'case-1-lines.json',audit)

artifacts=CASES/'artifacts';artifacts.mkdir(exist_ok=True)
fixture=runpy.run_path(str(ROOT/'build/bc4-fixtures-12.py'))['fixture']
for label,uid in [('alpha',2201),('beta',2202)]:
    (artifacts/('package-'+label+'.json')).write_text(json.dumps(fixture(label,uid),sort_keys=True,separators=(',',':'))+'\n')
rows={json.loads(s)['id']:json.loads(s) for s in machine(bundles['case-3-before'])}
for identity,name in [('dev-worker','worker-1.json'),('dev-service','service.json'),('dev-rule','rule.json')]:
    (artifacts/name).write_text(json.dumps(rows[identity],sort_keys=True)+'\n')
rows={json.loads(s)['id']:json.loads(s) for s in machine(bundles['case-4-both'])}
for identity in ('bc4:owner-a','bc4:owner-b'):(artifacts/(identity.replace(':','-')+'.json')).write_text(json.dumps(rows[identity],sort_keys=True,separators=(',',':'))+'\n')
base=json.loads(bundles['case-1']['files']['/var/lib/stand/current/base-files.json']);base_by_path={f['path']:f for f in base}
am={}
for p in artifacts.iterdir():
    if p.name.startswith('package-'):installed='/usr/local/share/stand/bc4/'+p.name
    elif p.name.startswith('bc4-owner'):installed='/usr/local/share/stand/bc4/removal/'+p.name
    else:installed='/usr/local/share/stand/dev/'+p.name
    digest=sha(p.read_bytes());assert digest==base_by_path[installed]['sha256']
    am[p.name]={'sha256':digest,'installed_source':installed,'matches_frozen_image_manifest':True}
write(CASES/'artifacts.json',am)
write(ROOT/'raw/round-4-prep/input-audit.json',{'complete_bundles':len(bundles),'machine_counts':{n:x['machine_rows'] for n,x in identities.items()},'all_blob_digests_match':True,'all_manifest_digests_match':True,'case1_equals_case3before':True,'removal_deltas_exact':True,'artifact_source_hashes_match_image':True,'case_execution':'none'})
print(json.dumps({'bundles':len(bundles),'artifact_count':len(am),'removal_machine_deltas':'exact'}))
