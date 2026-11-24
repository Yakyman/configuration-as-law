command -v python3 >/dev/null || exit 127
python3 - <<'ENDPY'
import subprocess,json,re
commands=[['journalctl','--no-pager','--all','-o','json','_COMM=useradd','+','_COMM=usermod','+','_COMM=groupadd','+','_COMM=gpasswd','+','_COMM=dnf','+','_COMM=anaconda','+','_COMM=systemctl','+','_COMM=setsebool'],['ausearch','-m','ADD_USER,DEL_USER,ADD_GROUP,DEL_GROUP,USER_MGMT,GRP_MGMT','--raw']]
for cmd in commands:
    try:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        total=0
        for raw in p.stdout:
            total+=len(raw)
            if total>16777216:
                p.kill();p.wait();print(json.dumps({'channel':cmd[0],'status':'output-cap'}));break
            text=raw.decode(errors='replace').strip()
            if cmd[0]=='journalctl':
                try:
                    r=json.loads(text);message=r.get('MESSAGE','')
                    if not isinstance(message,str): continue
                    # Only acquisition/account/configuration operations; never echo arbitrary journal events.
                    if not re.search(r'(?i)import|gpg|preset|disable|enable|created|useradd|usermod|groupadd|boolean|network|kickstart',message):continue
                    message=re.sub(r'(?i)(password|passwd|passphrase|psk|token|secret)([= :]+)\S+',r'\1\2[REDACTED]',message)
                    print(json.dumps({'channel':'journal','utc_usec':r.get('__REALTIME_TIMESTAMP'),'comm':r.get('_COMM'),'uid':r.get('_UID'),'message':message}))
                except ValueError: pass
            else:
                # Audit operation and result only; command/proctitle/payload fields are omitted.
                fields={}
                for key in ('type','msg','pid','uid','auid','ses','op','res'):
                    m=re.search(r'(?:^| )'+key+r'=([^ ]+)',text)
                    if m:fields[key]=m.group(1)
                if fields:print(json.dumps({'channel':'audit','fields':fields}))
        else:
            code=p.wait();print(json.dumps({'channel':cmd[0],'exit_status':code}))
    except FileNotFoundError: print(json.dumps({'channel':cmd[0],'status':'command-unavailable'}))
ENDPY

