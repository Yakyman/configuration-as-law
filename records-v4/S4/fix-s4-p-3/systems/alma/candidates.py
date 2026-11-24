#!/usr/bin/env python3
import pathlib,glob,gzip,re,json,time
specs={
'A07':{'globs':['/var/log/dnf*','/var/log/anaconda/*'], 'patterns':{
'generic_key':r'(?i)gpg-pubkey|c2a1e572',
'exact_key':r'(?i)c2a1e572',
'exact_key_import':r'(?i)(?:import.*c2a1e572|c2a1e572.*import)',
'exact_key_reason':r'(?i)(?:c2a1e572.*(?:reason|depend|explicit|request|repository)|(?:reason|depend|explicit|request|repository).*c2a1e572)',
'direct_import_command':r'(?i)rpm\s+(?:[^\n]*\s)?--import\s+',
'generic_key_import':r'(?i)(?:gpg-pubkey.*import|import.*gpg-pubkey)',
}},
'A11':{'globs':['/var/log/anaconda/*','/var/log/messages*'], 'patterns':{
'generic_boolean_tool':r'(?i)booleans\.local|setsebool|semanage.*boolean',
'persistent_setsebool_command':r'(?i)setsebool[^\n]*\s-P(?:\s|$)',
'semanage_boolean_modification':r'(?i)semanage\s+boolean[^\n]*\s(?:-[ma]|--modify|--add)(?:\s|$)',
'boolean_local_path':r'booleans\.local',
'generic_boolean_audit_event':r'type=MAC_CONFIG_CHANGE.*(?:bool=|boolean=)',
}}}
cache={}
for fact,spec in specs.items():
 for path in sorted(set(x for pat in spec['globs'] for x in glob.glob(pat))):
  if not pathlib.Path(path).is_file():continue
  if path not in cache:
   t=time.monotonic()
   try:
    with (gzip.open(path,'rt',errors='replace') if path.endswith('.gz') else open(path,errors='replace'))as f:data=f.read(32*1024*1024+1)
    rc=0 if len(data)<=32*1024*1024 else 75
   except (OSError,EOFError):data='';rc=1
   cache[path]=(data,rc,round(time.monotonic()-t,3))
  data,rc,dur=cache[path];lines=data.splitlines()
  print(json.dumps({'fact_id':fact,'source':path,'exit_status':rc,'duration_seconds':dur,'source_lines':len(lines),'bytes_read':len(data),'counts':{k:sum(bool(re.search(p,line))for line in lines)for k,p in spec['patterns'].items()},'payload_saved':False}),flush=True)
