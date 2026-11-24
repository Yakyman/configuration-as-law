import pathlib,subprocess as sp,time,os,json,re,hashlib,shutil,datetime
R=pathlib.Path(__file__).resolve().parent;O=R/'followup-evidence';O.mkdir(); name='fx-s4-p-3-microos-detail'; env={**os.environ,'LAB_SEPARATE_STDERR':'1'}
units=['dbus-org.freedesktop.nm-dispatcher.service','jeos-firstboot.service','network.service','NetworkManager-dispatcher.service','NetworkManager-wait-online.service','NetworkManager.service','mdcheck_continue.timer']
patterns={'M03':r'Created symlink|\benabl\w*|\bdisabl\w*|\bpreset\w*','M05':r'sudoers|visudo','M11':r'grubenv|grub2?-editenv|saved_entry|next_entry','M14':r'ca-certificates|p11-kit|trust anchor|openssl'}
def call(label,args,script=None):
 t=time.monotonic();p=sp.run(args,input=script,stdout=sp.PIPE,stderr=sp.PIPE,timeout=600,env=env)
 with (O/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.monotonic()-t:.3f}\n')
 err=re.sub(r'/home/[^/\s]+','HOST_HOME',p.stderr.decode(errors='replace'))
 (O/(label+'.stderr')).write_text(err)
 return p
(O/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
try:
 p=call('boot',[str(R/'lab.sh'),'new',name,'microos']);assert p.returncode==0
 script='journalctl --no-pager --all -o json\n';(O/'structured-journal.sh').write_text(script)
 p=call('structured-journal',[str(R/'lab.sh'),'run',name,'--root','--timeout','120'],script.encode())
 records=[];invalid=0
 for line in p.stdout.splitlines():
  try: records.append(json.loads(line))
  except ValueError:invalid+=1
 result={'query_exit':p.returncode,'records':len(records),'invalid_records':invalid,'units':{},'facts':{}}
 def msg(x):return str(x.get('MESSAGE',''))
 for unit in units:
  hits=[r for r in records if unit in msg(r)]
  result['units'][unit]={'message_hits':len(hits),'enablement_message_candidates':sum(bool(re.search(patterns['M03'],msg(r),re.I)) for r in hits)}
 for fact,pat in patterns.items():
  hits=[r for r in records if re.search(pat,msg(r),re.I)]
  result['facts'][fact]={'message_hits':len(hits),'audit_denials':sum('avc:' in msg(r) or 'AVC' in msg(r) for r in hits),'audit_success_yes':sum('success=yes' in msg(r) for r in hits),'explicit_command_fields':sum('COMMAND=' in msg(r) or 'proctitle=' in msg(r) for r in hits),'sender_uid_present':sum('_UID' in r for r in hits),'executable_basenames':sorted(set(pathlib.PurePosixPath(str(r.get('_EXE','unknown'))).name for r in hits)),'event_creation_terms':sum(bool(re.search(r'\b(created|changed|wrote|set|saved|installed|removed|anchor|added|imported)\b',msg(r),re.I)) for r in hits)}
 # Diagnostic event categories, no messages or values retained.
 (O/'journal-diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
 script="find /var/log/zypp /var/log/YaST2 -type f -printf 'SOURCE %p %s\\n' -exec grep -aEn 'NetworkManager|jeos-firstboot|mdcheck_continue|network.service|sudoers|visudo|grubenv|editenv|saved_entry|next_entry|ca-certificates|p11-kit|trust anchor' {} +\n"
 (O/'installation-records.sh').write_text(script)
 p=call('installation-records',[str(R/'lab.sh'),'run',name,'--root','--timeout','120'],script.encode())
 lines=p.stdout.decode(errors='replace').splitlines();sources=[x for x in lines if x.startswith('SOURCE ')];hits=[x for x in lines if not x.startswith('SOURCE ')]
 out={'query_exit':p.returncode,'source_files':len(sources),'source_bytes':sum(int(x.rsplit(' ',1)[1]) for x in sources),'matched_lines':len(hits),'units':{},'facts':{}}
 for unit in units:out['units'][unit]={'matching_lines':sum(unit in x for x in hits),'enablement_candidates':sum(unit in x and bool(re.search(patterns['M03'],x,re.I)) for x in hits)}
 for fact,pat in patterns.items():
  subset=[x for x in hits if re.search(pat,x,re.I)]
  out['facts'][fact]={'matching_lines':len(subset),'package_install_transaction_lines':sum('|install|' in x for x in subset),'package_remove_transaction_lines':sum('|remove|' in x for x in subset),'remaining_lines':sum('|install|' not in x and '|remove|' not in x for x in subset)}
 (O/'installation-diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
finally:
 p=call('destroy',[str(R/'lab.sh'),'destroy',name])
 if p.returncode:call('kill',[str(R/'lab.sh'),'kill',name]);call('destroy-again',[str(R/'lab.sh'),'destroy',name])
 (O/'cleanup.json').write_text(json.dumps({'vm_directories':len(list((R/'C1/vms').iterdir())),'raw_inventory_files':0,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
