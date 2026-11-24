#!/usr/bin/python3 -B
"""Compile only the builder's development fixtures, before factory enforcement."""
import base64, hashlib, json, pathlib, subprocess, tempfile
r=pathlib.Path('/usr/local/share/stand/dev');r.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as td:
    d=pathlib.Path(td)
    for v in (1,2,3):
        src='#include <stdio.h>\n#include <string.h>\n#include <unistd.h>\nint main(int n,char **a){if(n>1 && !strcmp(a[1],"--wait")){for(;;)pause();} puts("development-version-'+str(v)+'");return 0;}\n'
        (d/'worker.c').write_text(src)
        subprocess.run(['/usr/bin/gcc','-O2','-Wl,--build-id=none','-o',str(d/'worker'),str(d/'worker.c')],check=True)
        b=(d/'worker').read_bytes()
        row={'id':'dev-worker','type':'program','managed':True,'version':str(v),'source':'builder-source:development-worker',
             'source_sha256':hashlib.sha256(src.encode()).hexdigest(),
             'files':[{'path':'/opt/stand/pkgs/dev-worker/bin/worker','kind':'file','sha256':hashlib.sha256(b).hexdigest(),
                       'mode':493,'uid':0,'gid':0,'content_b64':base64.b64encode(b).decode()}]}
        (r/('worker-'+str(v)+'.json')).write_text(json.dumps(row,sort_keys=True)+'\n')
        (r/('worker-'+str(v)+'.c')).write_text(src)
unit='''[Unit]
Description=Declared development worker
[Service]
Type=simple
User=stand
ExecStart=/opt/stand/pkgs/dev-worker/bin/worker --wait
Restart=no
KillMode=control-group
TimeoutStopSec=5
MemoryDenyWriteExecute=yes
NoNewPrivileges=yes
ProtectSystem=strict
PrivateTmp=yes
[Install]
WantedBy=multi-user.target
'''
service={'id':'dev-service','type':'service','managed':True,'unit':'stand-development.service','enabled':'enabled','active':True,'unit_text':unit,'unit_sha256':hashlib.sha256(unit.encode()).hexdigest()}
rule={'id':'dev-rule','type':'rule','managed':True,'expression':'tcp dport 17777 drop'}
account={'id':'dev-account','type':'account','managed':True,'name':'fixture','uid':1200,'gid':1200,'groups':['fixture'],'shell':'/usr/sbin/nologin','home':'/home/fixture','gecos':'Development account'}
wifi={'id':'dev-wifi','type':'wifi','managed':True,'name':'development-network','ssid':'development-network','uuid':'<REDACTED>','autoconnect':False,'state':'saved'}
bt={'id':'dev-bluetooth','type':'bluetooth','managed':True,'adapter':'<MAC>','address':'<MAC>','name':'development-peer','trusted':False,'state':'prepared'}
for name,row in [('service',service),('rule',rule),('account',account),('wifi',wifi),('bluetooth',bt)]:
    (r/(name+'.json')).write_text(json.dumps(row,sort_keys=True)+'\n')
print('Development fixture artifacts prepared; no fixture executed')
