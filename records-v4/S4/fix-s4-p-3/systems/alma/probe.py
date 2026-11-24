#!/usr/bin/env python3
"""Rehearsal-only targeted diagnostic queries. Emits counts, never object decisions."""
import subprocess as sp,json,re,time,glob,gzip,pathlib
facts={
'A03': {'pattern':r'/boot/grub2|/boot/loader/entries|ens3\.nmconnection|/etc/NetworkManager/system-connections|/etc/firewalld/zones|/etc/kernel|/etc/sysconfig','paths':['/boot/grub2/grubenv','/boot/loader/entries','/etc/NetworkManager/system-connections/ens3.nmconnection','/etc/firewalld/zones','/etc/kernel','/etc/sysconfig'], 'logs':['/var/log/anaconda/*','/var/log/messages*'], 'operation':r'(?i)chose|chosen|default|kickstart|write|creat|chang'},
'A04': {'pattern':r'rpmdb-(?:migrate|rebuild)\.service','paths':['/etc/systemd/system/multi-user.target.wants/rpmdb-migrate.service','/etc/systemd/system/multi-user.target.wants/rpmdb-rebuild.service'],'logs':['/var/log/anaconda/*','/var/log/messages*'],'operation':r'(?i)disabl|preset|unlink|remov'},
'A07': {'pattern':r'(?i)c2a1e572|gpg-pubkey','paths':['/var/lib/rpm','/usr/lib/sysimage/rpm'],'logs':['/var/log/dnf*','/var/log/anaconda/*'],'operation':r'(?i)import|key.*install'},
'A09': {'pattern':r'/etc/alsa|asound\.state|alsactl','paths':['/etc/alsa/asound.state'],'logs':['/var/log/anaconda/*','/var/log/messages*'],'operation':r'(?i)store|write|creat'},
'A11': {'pattern':r'booleans\.local|setsebool|semanage.*boolean','paths':['/var/lib/selinux/targeted/active/booleans.local'],'logs':['/var/log/anaconda/*','/var/log/messages*'],'operation':r'(?i)set|write|creat|boolean'} }
def query(args):
 t=time.monotonic()
 try:
  p=sp.run(args,stdout=sp.PIPE,stderr=sp.PIPE,timeout=90)
  return p.stdout.decode(errors='replace'),{'command':args,'exit_status':p.returncode,'duration_seconds':round(time.monotonic()-t,3),'stderr_bytes':len(p.stderr),'stderr_no_matches':b'<no matches>' in p.stderr}
 except FileNotFoundError:return '',{'command':args,'exit_status':127,'duration_seconds':round(time.monotonic()-t,3)}
 except sp.TimeoutExpired:return '',{'command':args,'exit_status':124,'duration_seconds':round(time.monotonic()-t,3)}
def summarize(fact,method,data,diags,available):
 cfg=facts[fact]; lines=data.splitlines(); matched=[s for s in lines if re.search(cfg['pattern'],s)]
 operations=[s for s in matched if re.search(cfg['operation'],s)]
 # No inference from a matching phrase; retain only source/operation availability diagnostics.
 print(json.dumps({'fact_id':fact,'method':method,'source_available':available,'source_lines':len(lines),'target_matching_lines':len(matched),'target_operation_lines':len(operations),'target_path_counts':{p:sum(p in line for line in lines) for p in cfg['paths']},'choice_actor_marker_lines':sum(bool(re.search(r'(?i)chosen by|selected by|requested by|user choice|explicit choice|auid=|loginuid=',line)) for line in operations),'queries':diags,'payload_saved':False}),flush=True)
file_cache={}
journal_data,journal_diag=query(['journalctl','--no-pager','--all','-o','json'])
for fact,cfg in facts.items():
 data,diag=journal_data,journal_diag
 # Drop journal envelope; names, uid and timestamps are not by themselves provenance.
 messages=[]
 for line in data.splitlines():
  try:
   row=json.loads(line);m=row.get('MESSAGE',''); messages.append(m if isinstance(m,str) else '')
  except ValueError: pass
 summarize(fact,'journal-target-events','\n'.join(messages),[diag],diag['exit_status']==0)
 data_parts=[];diags=[]
 for path in cfg['paths']:
  data,diag=query(['ausearch','--input-logs','-f',path,'--raw']);data_parts.append(data);diags.append(diag)
 if fact=='A11':
  data,diag=query(['ausearch','--input-logs','-m','MAC_CONFIG_CHANGE','--raw']);data_parts.append(data);diags.append(diag)
 if fact in ('A04','A07','A09'):
  executable={'A04':'/usr/bin/systemctl','A07':'/usr/bin/rpm','A09':'/usr/sbin/alsactl'}[fact]
  data,diag=query(['ausearch','--input-logs','-x',executable,'--raw']);data_parts.append(data);diags.append(diag)
 summarize(fact,'audit-target-events','\n'.join(data_parts),diags,any(d['exit_status'] in (0,1) for d in diags))
 parts=[];diags=[]
 for path in sorted(set(p for pat in cfg['logs'] for p in glob.glob(pat))):
  if not pathlib.Path(path).is_file():continue
  if path not in file_cache:
   t=time.monotonic()
   try:
    with (gzip.open(path,'rt',errors='replace') if path.endswith('.gz') else open(path,errors='replace')) as f: data=f.read(32*1024*1024+1)
    rc=0 if len(data)<=32*1024*1024 else 75
   except (OSError,EOFError):data='';rc=1
   file_cache[path]=(data,{'source':path,'exit_status':rc,'bytes_read':len(data),'duration_seconds':round(time.monotonic()-t,3)})
  data,diag=file_cache[path];parts.append(data);diags.append(diag)
 if fact=='A07':
  data,diag=query(['dnf','-C','history','info','gpg-pubkey*']);parts.append(data);diags.append(diag)
 summarize(fact,'application-installer-event-records','\n'.join(parts),diags,any(d['exit_status']==0 for d in diags))
