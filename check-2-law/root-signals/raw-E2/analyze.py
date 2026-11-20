#!/usr/bin/python3
from pathlib import Path
import collections,datetime,json,re
R=Path(__file__).resolve().parent;G=R/'guest'
audit=(G/'audit-final.log').read_text().splitlines(); journals=[json.loads(l) for l in (G/'journal-current.jsonl').read_text().splitlines()]
rows=[]; evidence=[]
for f in sorted((G/'probes').glob('*.json')):
 d=json.loads(f.read_text());t=d['target'];ts=datetime.datetime.fromisoformat(d['utc']).timestamp();sudo_pids={a['pid'] for a in d['ancestors'] if a.get('exe')=='/usr/bin/sudo'}
 auth=[];execs=[];markers=[]
 for lineno,line in enumerate(audit,1):
  event=re.search(r'msg=audit\(([0-9.]+):([0-9]+)\)',line);pid=re.search(r'\bpid=([0-9]+)',line)
  if not event or not pid:continue
  et=float(event[1]);pn=int(pid[1])
  if not ts-10<=et<=ts+2:continue
  ref={'line':lineno,'event':event[0],'text':line}
  if line.startswith('type=USER_AUTH ') and pn in sudo_pids:auth.append(ref)
  if line.startswith('type=SYSCALL ') and pn==t['pid']:
   if 'key="e2exec"' in line and 'success=yes' in line:execs.append(ref)
   if 'key="e2marker"' in line and 'success=yes' in line:markers.append(ref)
 messages=[]
 subjects=[f"unix-process:{a['pid']}:{a['starttime_ticks']}" for a in [t]+d['ancestors'] if a.get('starttime_ticks') and a['pid']!=1]
 for n,j in enumerate(journals,1):
  jt=int(j.get('__REALTIME_TIMESTAMP','0'))/1e6; msg=j.get('MESSAGE','')
  if isinstance(msg,str) and ts-10<=jt<=ts+2 and any(subject in msg for subject in subjects) and (('polkit' in j.get('SYSLOG_IDENTIFIER','') and ('authenticat' in msg.lower() or 'Executing command' in msg))):messages.append({'line':n,'message':msg,'pid':j.get('_PID')})
 row={'label':d['label'],'utc':d['utc'],'target_pid':t['pid'],'ruid':d['uids'][0],'euid':d['uids'][1],'loginuid':t['loginuid'],'audit_sessionid':t['audit_sessionid'],'tty_nr':t['tty_nr'],'dev_tty_open':d['controlling_tty']['open'],'stdin_isatty':d['fds']['0']['isatty'],'cgroup':t['cgroup'],'ancestry':[a['comm'] for a in d['ancestors']],'ancestry_executables':[a.get('exe') for a in d['ancestors']],'lsm':d['lsm'],'marker_ok':d['marker']['ok'],'sudo_USER_AUTH':auth,'target_exec_events':execs,'target_marker_events':markers,'polkit_journal_correlated':messages}
 rows.append(row)
 for k,entries in [('sudo_auth',auth),('target_exec',execs),('target_marker',markers)]:
  for e in entries:evidence.append(f"{d['label']} {k} audit-final.log:{e['line']} {e['text']}")
 for e in messages:evidence.append(f"{d['label']} polkit_journal journal-current.jsonl:{e['line']} pid={e['pid']} {e['message']}")
(R/'measurements.json').write_text(json.dumps(rows,indent=2)+'\n')
(R/'event-index.txt').write_text('\n'.join(evidence)+'\n')
cols=['label','target_pid','ruid','euid','loginuid','audit_sessionid','tty_nr','dev_tty_open','stdin_isatty','cgroup','marker_ok']
(R/'measurements.tsv').write_text('\t'.join(cols+['ancestry','sudo_auth_event_ids'])+'\n'+'\n'.join('\t'.join(str(x[k]) for k in cols)+'\t'+'>'.join(x['ancestry'])+'\t'+','.join(e['event'] for e in x['sudo_USER_AUTH']) for x in rows)+'\n')
fresh=next(x for x in rows if x['label']=='interactive-sudo-fresh')
criteria={'euid_root':fresh['euid']==0,'audit_login_user_set':fresh['loginuid']=='1102' and fresh['audit_sessionid']!='4294967295','controlling_tty':fresh['tty_nr']!=0 and fresh['dev_tty_open'],'fresh_successful_sudo_auth':any('res=success' in x['text'] for x in fresh['sudo_USER_AUTH']),'sshd_bash_sudo_ancestry':all(exe in fresh['ancestry_executables'] for exe in ['/usr/sbin/sshd','/usr/bin/bash','/usr/bin/sudo']),'logind_session_scope':bool(re.search(r'/session-\d+\.scope$',fresh['cgroup']))}
summary={'probe_count':len(rows),'euid0_count':sum(x['euid']==0 for x in rows),'marker_success_count':sum(x['marker_ok'] for x in rows),'audited_exec_count':sum(bool(x['target_exec_events']) for x in rows),'audited_marker_count':sum(bool(x['target_marker_events']) for x in rows),'joint_label':fresh['label'],'joint_criteria':criteria,'joint_satisfied':all(criteria.values()),'interpretation':'All samples automated. This only refutes sufficiency of the listed predicates as proof of a human; not a hypothesis verdict.'}
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for x in rows:
 if x['sudo_USER_AUTH'] or x['polkit_journal_correlated']:
  print(x['label'],'AUTH',[(e['line'],e['text']) for e in x['sudo_USER_AUTH']],'POLKIT',x['polkit_journal_correlated'])
