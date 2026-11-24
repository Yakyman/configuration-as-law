import pathlib,json,re,collections,csv,hashlib
R=pathlib.Path(__file__).resolve().parent;D=R/'transient';O=R/'raw'
def txt(n):return (D/(n+'.out')).read_text()
def seq(n):
 s=txt(n);d=json.JSONDecoder();out=[]
 while s.strip():x,i=d.raw_decode(s.lstrip());out.append(x);s=s.lstrip()[i:]
 return out
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
targets=json.loads((R/'targets.json').read_text());code=[x for x in targets if x['kind']=='L2:code-ownership-unknown']
s=json.loads(txt('spdx-document'));files=s.get('files',[]);packages=s.get('packages',[])
# SPDX file names are build inputs. Preserve schemas/counts, not the inventory.
save('spdx-diagnostic.json',{'document_keys':sorted(s),'package_rows':len(packages),'file_rows':len(files),'file_schema_counts':dict(collections.Counter(','.join(sorted(x)) for x in files)),'relationship_type_counts':dict(collections.Counter(x['relationshipType'] for x in s['relationships'])),'files_analyzed_values':dict(collections.Counter(str(x.get('filesAnalyzed')) for x in packages)),'file_name_categories':{'spdx_build_document':sum(x['fileName'].endswith('.spdx.json') for x in files),'go_mod':sum(x['fileName']=='go.mod' for x in files),'absolute_path':sum(x['fileName'].startswith('/') for x in files)},'checksummed_file_rows':sum(bool(x.get('checksums')) for x in files),'first_night_code_reference_matches':[{'first_id':x['id'],'path':x['name'],'exact_matches':sum(y['fileName'].lstrip('./')==x['name'].lstrip('/') for y in files),'basename_matches':sum(pathlib.PurePosixPath(y['fileName']).name==pathlib.PurePosixPath(x['name']).name for y in files)} for x in code]})
statuses=seq('etc-status');specs=seq('etc-spec');sm={x['metadata']['id']:x for x in specs}
save('controller-diagnostic.json',{'status_rows':len(statuses),'spec_rows':len(specs),'joined_rows':sum(x['metadata']['id'] in sm for x in statuses),'status_spec_schemas':dict(collections.Counter(','.join(sorted(x['spec'])) for x in statuses)),'spec_schemas':dict(collections.Counter(','.join(sorted(x['spec'])) for x in specs)),'status_owners':dict(collections.Counter(x['metadata'].get('owner','') for x in statuses)),'spec_owners':dict(collections.Counter(x['metadata'].get('owner','') for x in specs)),'metadata_created_min':min(x['metadata']['created'] for x in specs),'metadata_created_max':max(x['metadata']['created'] for x in specs),'matching_status_spec_versions':sum(str(x['spec']['specVersion'])==str(sm[x['metadata']['id']]['metadata']['version']) for x in statuses if x['metadata']['id'] in sm),'first_night_code_resource_matches':[{'first_id':x['id'],'path':x['name'],'matches':sum('/etc/'+y['metadata']['id']==x['name'] for y in specs)} for x in code]})
audit=txt('audit-history').splitlines();typed=[]
for line in audit:
 m=re.search(r' type=([^ ]+) msg=audit\(([^)]+)\): (.*)',line)
 if m:typed.append(m.groups())
save('audit-diagnostic.json',{'lines':len(audit),'parsed_records':len(typed),'unparsed_lines':len(audit)-len(typed),'record_types':dict(collections.Counter(x[0] for x in typed)),'event_ids':len(set(x[1] for x in typed)),'syscall_numbers':dict(collections.Counter(re.search(r'\bsyscall=(\d+)',x[2]).group(1) for x in typed if x[0]=='SYSCALL' and re.search(r'\bsyscall=(\d+)',x[2]))),'syscall_items':dict(collections.Counter(re.search(r'\bitems=(\d+)',x[2]).group(1) for x in typed if x[0]=='SYSCALL' and re.search(r'\bitems=(\d+)',x[2]))),'PATH_rows':sum(x[0]=='PATH' for x in typed),'first_night_code_path_mentions':[{'first_id':x['id'],'path':x['name'],'path_field_matches':sum(('path="'+x['name']+'"') in y[2] or ('name="'+x['name']+'"') in y[2] for y in typed)} for x in code]})
ev=txt('runtime-events').splitlines();types=collections.Counter();messages=[]
for i,l in enumerate(ev):
 m=re.search(r'talos/runtime/machine\.([A-Za-z]+Event)',l)
 if m:
  types[m[1]]+=1
  if m[1] in ('SequenceEvent','TaskEvent','PhaseEvent') and i+1<len(ev):messages.append({'type':m[1],'message':ev[i+1].strip()})
save('events-diagnostic.json',{'lines':len(ev),'event_types':dict(types),'sequence_phase_task_payloads':messages,'bounded_stream':True,'first_night_code_path_mentions':[{'first_id':x['id'],'path':x['name'],'literal_mentions':sum(x['name'] in l for l in ev)} for x in code]})
logs=txt('machined-history').splitlines();selected=[]
for line in logs:
 if any(marker in line for marker in ('machined logger initialized','install sequence:', '"volume": "STATE"','machine config loaded successfully','composed writable /etc overlay')):selected.append(re.sub(r'^\S+: ','',line))
save('history-diagnostic.json',{'lines':len(logs),'first_timestamp':re.search(r'\d{4}/\d\d/\d\d [\d:.]+',logs[0]).group(),'last_timestamp':re.search(r'\d{4}/\d\d/\d\d [\d:.]+',logs[-1]).group(),'selected_exact_diagnostics':selected,'first_night_code_path_mentions':[{'first_id':x['id'],'path':x['name'],'literal_mentions':sum(x['name'] in l for l in logs)} for x in code],'installer_error':re.sub(r'node [^: ]+:','node GUEST:',txt('installer-history')).strip()})
save('retained-reference-diagnostic.json',{'state_listing_exit_basis':'status.tsv:state-list','state_rows':txt('state-list').splitlines(),'boot_rows':txt('boot-list').splitlines(),'interpretation':'API namespace only; STATE was detached then unmounted in history-diagnostic.json. No assertion of empty backing storage.'})
# Retain only bounded transport failures, stripping endpoint identifiers.
errors={}
for p in D.glob('*.err'):
 if p.stat().st_size:errors[p.stem]=re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b','GUEST',p.read_text(errors='replace'))
save('query-errors.json',errors)
save('transient-integrity.json',{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.iterdir()) if p.is_file()})
