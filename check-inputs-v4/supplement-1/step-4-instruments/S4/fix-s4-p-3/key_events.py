"""Retain DNF key event fields; no object classification or inferred import reason."""
import json
GUEST_SCRIPT = r'''#!/usr/bin/env python3
import glob,gzip,json,re,shlex,pathlib
DIAGNOSTICS=False
rows=[];coverage=[]
safe_flags={'-y','--assumeyes','-q','--quiet','-v','--verbose','-C','--cacheonly'}
for path in sorted(glob.glob('/var/log/dnf.log*')):
 if not pathlib.Path(path).is_file():continue
 try:
  with (gzip.open(path,'rb') if path.endswith('.gz') else open(path,'rb'))as f:raw=f.read(32*1024*1024+1)
  if len(raw)>32*1024*1024:
   coverage.append({'source':path,'status':'size-cap','bytes':len(raw)});continue
  data=raw.decode(errors='replace')
 except (OSError,EOFError):coverage.append({'source':path,'status':'read-failed'});continue
 lines=data.splitlines();command='unknown:command-field-empty';command_line=0;segment=0;event=None
 for lineno,line in enumerate(lines,1):
  if '--- logging initialized ---' in line:
   command='unknown:command-field-empty';command_line=0;segment+=1;event=None
  if re.search(r'\bCommand:\s',line):
   event=None
   text=re.split(r'\bCommand:\s*',line,1)[1].strip()
   try:words=shlex.split(text)
   except ValueError:words=[]
   if words and pathlib.PurePosixPath(words[0]).name in ('dnf','dnf-3') and len(words)>2 and next((w for w in words[1:] if w not in safe_flags),'')=='install' and all(w in safe_flags or re.fullmatch(r'[A-Za-z0-9_+][A-Za-z0-9_.+*-]*',w) for w in words[1:]):
    command=text;command_line=lineno
   else:command='unknown:command-outside-allowlist';command_line=lineno
  match=re.search(r'Importing GPG key 0x([0-9a-fA-F]+):',line)
  if match:
   event={'key_id':match.group(1).lower(),'source_file':path,'event_line':lineno,'log_segment':segment,'import_timestamp':line.split()[0],'preceding_command':command,'command_line':command_line,'fingerprint':'unknown:fingerprint-field-empty','key_source':'unknown:source-field-empty','success_timestamp':'unknown:success-field-empty','success_line':0}
   rows.append(event)
   continue
  if event:
   m=re.match(r'\s*Fingerprint:\s*([0-9A-Fa-f ]+)$',line)
   if m:event['fingerprint']=m.group(1).replace(' ','').lower()
   m=re.match(r'\s*From\s*:\s*(\S+)\s*$',line)
   if m and m.group(1).startswith('/etc/pki/rpm-gpg/'):
    event['key_source']=m.group(1)
   if 'Key imported successfully' in line:
    event['success_timestamp']=line.split()[0];event['success_line']=lineno;event=None
 coverage.append({'source':path,'status':'read','lines':len(lines),'bytes':len(raw)})
for r in rows:
 r['status']='fields-recorded' if all(not str(r[k]).startswith('unknown:') for k in ('preceding_command','fingerprint','key_source','success_timestamp')) and r['fingerprint'].endswith(r['key_id']) else 'unknown:event-fields-incomplete'
if DIAGNOSTICS:
 target=[r for r in rows if r['key_id']=='c2a1e572']
 print(json.dumps({'event_count':len(rows),'target_event_count':len(target),'target_complete_fields':sum(r['status']=='fields-recorded'for r in target),'target_command_present':sum(not r['preceding_command'].startswith('unknown:')for r in target),'target_command_outside_allowlist':sum(r['preceding_command']=='unknown:command-outside-allowlist'for r in target),'target_fingerprint_present':sum(not r['fingerprint'].startswith('unknown:')for r in target),'target_source_present':sum(not r['key_source'].startswith('unknown:')for r in target),'target_success_present':sum(not r['success_timestamp'].startswith('unknown:')for r in target),'coverage':coverage,'payload_saved':False}))
else:
 for r in rows:print(json.dumps({'event':r}))
 for c in coverage:print(json.dumps({'coverage':c}))
'''
def collect(ctx):
 from main import write_tsv
 data,rc,ev=ctx.query('s4-alma-dnf-key-events',"python3 - <<'S4_KEY_EVENTS'\n"+GUEST_SCRIPT+"\nS4_KEY_EVENTS\n",120)
 rows=[];coverage=[['','query-completed' if rc==0 else 'unknown:query-failed',0,0,rc,ev]]
 for line in data.splitlines():
  try:r=json.loads(line)
  except ValueError:continue
  if 'coverage' in r:
   c=r['coverage'];coverage.append([c.get('source',''),c.get('status',''),c.get('lines',0),c.get('bytes',0),rc,ev]);continue
  r=r.get('event',{})
  if rc!=0:r['status']='unknown:query-failed'
  key=r.get('key_id','')
  matches=[obj for obj in ctx.objects if key and obj[3]=='package' and obj[4].startswith('rpm:gpg-pubkey@'+key+'-')]
  if rc==0 and len(matches)>1:r['status']='unknown:multiple-package-key-matches'
  for obj in matches:
    rows.append([obj[0]]+[r.get(k,'') for k in ['key_id','fingerprint','key_source','import_timestamp','success_timestamp','preceding_command','source_file','log_segment','command_line','event_line','success_line','status']]+[ev])
 write_tsv(ctx.out/'alma-key-events.tsv',['object_id','key_id','fingerprint','key_source','import_timestamp','success_timestamp','preceding_command','source_file','log_segment','command_line','event_line','success_line','status','evidence'],rows)
 write_tsv(ctx.out/'alma-key-event-coverage.tsv',['source','status','lines','bytes','query_exit_status','evidence'],coverage)
 if not hasattr(ctx,'s4_summary'):ctx.s4_summary={}
 ctx.s4_summary['alma_key_events']={'query_exit_status':rc,'rows':len(rows),'complete_field_rows':sum(r[-2]=='fields-recorded'for r in rows)}
