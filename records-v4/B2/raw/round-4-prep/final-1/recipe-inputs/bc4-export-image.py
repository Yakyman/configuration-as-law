#!/usr/bin/env python3
"""Read-only frozen-image declaration identity; no guest case is executed."""
import hashlib,json,os,pathlib,shlex,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1];OUT=ROOT/'raw/round-4-prep'/phase/'offline-declaration';OUT.mkdir(parents=True,exist_ok=False)
paths=['/var/lib/stand/current/machine.jsonl','/var/lib/stand/current/base-files.json','/etc/stand/bc3-primary.json']+['/var/lib/stand-fs/'+k+'/current/declaration.json' for k in ('home','tmp','vartmp','shm','etc')]
script='\n'.join('download '+shlex.quote(p)+' '+shlex.quote(str(OUT/(str(i)+'.json'))) for i,p in enumerate(paths))+'\n'
with (OUT/'guestfish.log').open('wb') as log:
    for n in range(1,13):
        r=subprocess.run(['flock','-n','-E','75',str(ROOT.parent/'slots'/('slot-'+str(n)+'.lock')),'guestfish','--ro','-a',str(ROOT/'base/stand.qcow2'),'-i'],input=script.encode(),stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LIBGUESTFS_MEMSIZE':'1024','LIBGUESTFS_BACKEND':'direct'})
        if r.returncode!=75:break
    else:raise RuntimeError('all slots occupied')
if r.returncode:raise RuntimeError('offline extraction failed')
files={p:(OUT/(str(i)+'.json')).read_text() for i,p in enumerate(paths)}
data=(json.dumps({'format':'bc3-complete-declaration-v1','files':files},sort_keys=True,separators=(',',':'))+'\n').encode()
(OUT/'declaration.json').write_bytes(data)
(OUT/'identity.json').write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'source':'frozen disk read-only without boot','files':{p:hashlib.sha256(t.encode()).hexdigest() for p,t in files.items()}},sort_keys=True,indent=2)+'\n')
print('Frozen complete declaration SHA-256 '+hashlib.sha256(data).hexdigest())
