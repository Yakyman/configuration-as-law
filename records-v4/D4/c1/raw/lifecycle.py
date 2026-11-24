from pathlib import Path
import datetime, subprocess, sys, re, os
root=Path(__file__).resolve().parent
system,action=sys.argv[1:]
name='d4c1-'+system
command='cd ~/VMs/cal-1123 && ./lab.sh '+action+' '+name+(' '+system if action=='new' else '')
t0=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(['ssh','-F',str(Path.home()/'.ssh/config'),os.environ['LAB_SSH_TARGET'],command],capture_output=True,text=True)
text=re.sub(r'/home/[^/\s]+','<host-home>',r.stdout+r.stderr)
record=root/(system+'-'+action+'.txt')
index=2
while record.exists():
 record=root/(system+'-'+action+'-'+str(index)+'.txt'); index+=1
record.write_text('start_utc='+t0+'\ncommand=lab.sh '+action+' '+name+(' '+system if action=='new' else '')+'\n'+text+'exit='+str(r.returncode)+'\nend_utc='+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
print(system,action,r.returncode,text)
