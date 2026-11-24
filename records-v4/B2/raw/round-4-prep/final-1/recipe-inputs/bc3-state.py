#!/usr/bin/python3 -B
"""Read back designated filesystem requirements or export a complete description."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
P=pathlib.Path
MOUNTS={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('operation',choices=['verify','export']);a=ap.parse_args()
    description={'format':'bc3-complete-declaration-v1','files':{}}
    failures=[];count=0
    p=P('/var/lib/stand/current/machine.jsonl')
    description['files']['/var/lib/stand/current/machine.jsonl']=p.read_text()
    description['files']['/var/lib/stand/current/base-files.json']=(p.parent/'base-files.json').read_text()
    description['files']['/etc/stand/bc3-primary.json']=P('/etc/stand/bc3-primary.json').read_text()
    for key,mount in MOUNTS.items():
        base=(P('/var/lib/stand-fs')/key/'current').resolve()
        data=(base/'declaration.json').read_bytes();decl=json.loads(data)
        description['files']['/var/lib/stand-fs/'+key+'/current/declaration.json']=data.decode()
        if a.operation=='export':continue
        report=json.loads((base/'success.json').read_text())
        if report['declaration_sha256']!=sha(data):failures.append({'key':key,'error':'report identity'})
        for name,inode in decl['paths'].items():
            obj=decl['objects'][inode];path=P(mount+name);count+=1
            try:
                st=path.lstat()
                for attr in ('st_mode','st_uid','st_gid'):
                    if getattr(st,attr)!=obj[attr]:failures.append({'path':str(path),'field':attr,'expected':obj[attr],'actual':getattr(st,attr)})
                if stat.S_ISREG(st.st_mode):
                    actual=sha(path.read_bytes())
                    if actual!=obj['sha256']:failures.append({'path':str(path),'field':'sha256','expected':obj['sha256'],'actual':actual})
                elif stat.S_ISLNK(st.st_mode) and os.readlink(path)!=obj['target']:
                    failures.append({'path':str(path),'field':'link target'})
            except OSError as error:failures.append({'path':str(path),'error':type(error).__name__,'errno':error.errno})
        # A concurrent system mutation makes this census inconclusive, never a pass.
        if (P('/var/lib/stand-fs')/key/'current').resolve()!=base:
            failures.append({'key':key,'error':'declaration changed during readback'})
    if a.operation=='export':print(json.dumps(description,sort_keys=True,separators=(',',':')));return 0
    print(json.dumps({'filesystem_paths_checked':count,'passed':not failures,'failures':failures},sort_keys=True));return int(bool(failures))
if __name__=='__main__':raise SystemExit(main())
