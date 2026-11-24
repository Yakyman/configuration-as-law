#!/usr/bin/env python3
"""Export exact frozen-disk primary declarations without booting that disk."""
import hashlib,json,os,pathlib,shlex,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1];OUT=ROOT/'raw/round-3'/phase/'offline-declaration'
OUT.mkdir(parents=True,exist_ok=False)
mounts={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
paths=['/var/lib/stand/current/machine.jsonl','/var/lib/stand/current/base-files.json','/etc/stand/bc3-primary.json']
paths+=['/var/lib/stand-fs/'+key+'/current/declaration.json' for key in mounts]
# /etc is a boot-time userspace mount. Its designation is also present in the
# underlying frozen /etc, created before that initial mount.
commands=[]
for i,path in enumerate(paths):commands.append('download '+shlex.quote(path)+' '+shlex.quote(str(OUT/(str(i)+'.json'))))
script='\n'.join(commands)+'\n'
slots=ROOT.parent/'slots'
with (OUT/'guestfish.log').open('wb') as log:
    for n in range(1,13):
        result=subprocess.run(['flock','-n','-E','75',str(slots/('slot-'+str(n)+'.lock')),
            'guestfish','--ro','-a',str(ROOT/'base/stand.qcow2'),'-i'],input=script.encode(),stdout=log,stderr=subprocess.STDOUT,
            env={**os.environ,'LIBGUESTFS_MEMSIZE':'1024','LIBGUESTFS_BACKEND':'direct'})
        if result.returncode!=75:break
    else:raise RuntimeError('all slots occupied')
if result.returncode:raise RuntimeError('offline declaration export failed')
bundle={'format':'bc3-complete-declaration-v1','files':{p:(OUT/(str(i)+'.json')).read_text() for i,p in enumerate(paths)}}
data=(json.dumps(bundle,sort_keys=True,separators=(',',':'))+'\n').encode()
(OUT/'declaration.json').write_bytes(data)
(OUT/'identity.json').write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),
    'source':'frozen disk read-only, without boot','files':{p:hashlib.sha256((OUT/(str(i)+'.json')).read_bytes()).hexdigest() for i,p in enumerate(paths)}},sort_keys=True,indent=2)+'\n')
print(json.dumps({'declaration_sha256':hashlib.sha256(data).hexdigest(),'files':len(paths)}))
