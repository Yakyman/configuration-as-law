#!/usr/bin/python3
"""Build development artifacts from genuine Flatpak/OCI/SquashFS formats inside builder VM."""
import hashlib, io, json, pathlib, subprocess, sys, tarfile, tempfile, shutil
sys.path.insert(0,'/usr/local/lib/stand')
from app_channels import PERMISSIONS
P=pathlib.Path
out=P('/usr/local/share/stand/channels');out.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(*args):
    result=subprocess.run(list(map(str,args)),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if result.returncode:raise RuntimeError('artifact builder failed '+str(args[0])+': '+result.stdout)
    return result.stdout.strip()
def tar(files):
    b=io.BytesIO()
    with tarfile.open(fileobj=b,mode='w') as t:
        for n,(data,mode) in sorted(files.items()):
            info=tarfile.TarInfo(n);info.size=len(data);info.mode=mode;info.mtime=0;t.addfile(info,io.BytesIO(data))
    return b.getvalue()
def save(kind,blob,spec):
    p=out/(kind+'.artifact');p.write_bytes(blob)
    spec.update(id='round4-'+kind,artifact=str(p),sha256=sha(blob),permissions=PERMISSIONS)
    (out/(kind+'.json')).write_text(json.dumps(spec,sort_keys=True)+'\n')
with tempfile.TemporaryDirectory(prefix='app-fixtures-') as td:
    td=P(td)
    src=td/'probe.c';src.write_text('''#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
int main(void){
 if(getuid()!=1000||getgid()!=1000){puts("UID_BYPASS");return 13;}
 int net=socket(AF_INET,SOCK_STREAM,0);if(net>=0){close(net);puts("NETWORK_BYPASS");return 14;}
 if(access("/usr/bin/python3",F_OK)!=0)puts("IMAGE_ROOT_ONLY");
 int fd=open("/new-code",O_WRONLY|O_CREAT,0700);
 if(fd>=0){close(fd);puts("WRITE_BYPASS");return 11;}
 int exists=access("/unrecorded",F_OK)==0;
 char *a[]={"/unrecorded",NULL};execv(a[0],a);
 if(exists){if(errno!=EACCES&&errno!=EPERM)return 12;puts("EXISTING_NONENTRY_EXEC_REFUSED");}
 else if(errno!=ENOENT&&errno!=EACCES&&errno!=EPERM)return 12;
 puts("RECORDED_APPLICATION_OK WRITE_REFUSED EXEC_REFUSED");
 if(access("/hold",F_OK)==0){
  fflush(stdout);pid_t child=fork();if(child<0){puts("FORK_FAILED");return 15;}
  if(child==0){puts("CONTAINER_CHILD_READY");fflush(stdout);for(;;)pause();}
  puts("CONTAINER_HOLDER_READY");fflush(stdout);for(;;)pause();
 }
 return 0;}
''')
    binary=td/'probe';run('/usr/bin/gcc','-static','-O2','-o',binary,src);code=binary.read_bytes()
    for kind,hold in [('oci',False),('oci-hold',True)]:
        layer_files={'bin/probe':(code,0o755),'unrecorded':(code,0o755)}
        if hold:layer_files['hold']=(b'hold until declaration removal\n',0o444)
        layer=tar(layer_files)
        config={'architecture':'amd64','os':'linux','config':{'Entrypoint':['/bin/probe'],'Cmd':[],'Env':[],'User':'1000:1000','WorkingDir':'/'},'rootfs':{'type':'layers','diff_ids':['sha256:'+sha(layer)]}}
        blobs={}
        def desc(data,media):
            if not isinstance(data,bytes):data=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
            dg=sha(data);blobs['blobs/sha256/'+dg]=(data,0o644)
            return {'mediaType':media,'digest':'sha256:'+dg,'size':len(data)}
        manifest={'schemaVersion':2,'mediaType':'application/vnd.oci.image.manifest.v1+json','config':desc(config,'application/vnd.oci.image.config.v1+json'),'layers':[desc(layer,'application/vnd.oci.image.layer.v1.tar')]}
        md=desc(manifest,'application/vnd.oci.image.manifest.v1+json')
        blobs['oci-layout']=(b'{"imageLayoutVersion":"1.0.0"}',0o644)
        blobs['index.json']=(json.dumps({'schemaVersion':2,'manifests':[md]}).encode(),0o644)
        save(kind,tar(blobs),{'digest':md['digest'],'entrypoint':'bin/probe','configuration':{'image':md['digest'],'entrypoint':'/bin/probe','uid':1000,'gid':1000,'read_only':True,'network':'none','mounts':[],'capabilities':[],'hooks':[]}})
    app=td/'app';(app/'files/bin').mkdir(parents=True);(app/'export').mkdir();shutil.copy2(binary,app/'files/bin/probe')
    (app/'metadata').write_text('[Application]\nname=org.stand.Probe\nruntime=org.stand.Runtime/x86_64/stable\ncommand=probe\n')
    runtime=td/'runtime';(runtime/'usr').mkdir(parents=True);(runtime/'files').mkdir()
    (runtime/'usr/identity').write_text('Static development runtime; no external shared libraries.\n')
    (runtime/'metadata').write_text('[Runtime]\nname=org.stand.Runtime\n')
    repo=td/'repo'
    run('/usr/bin/flatpak','build-export','--timestamp=2026-11-22T00:00:00Z','--no-update-summary','--runtime','--arch=x86_64',repo,runtime,'stable')
    run('/usr/bin/flatpak','build-export','--timestamp=2026-11-22T00:00:00Z','--no-update-summary','--arch=x86_64',repo,app,'stable')
    commit=run('/usr/bin/ostree','--repo='+str(repo),'rev-parse','app/org.stand.Probe/x86_64/stable')
    rc=run('/usr/bin/ostree','--repo='+str(repo),'rev-parse','runtime/org.stand.Runtime/x86_64/stable')
    save('flatpak',tar({str(p.relative_to(repo)):(p.read_bytes(),0o644) for p in repo.rglob('*') if p.is_file()}),{'application':'org.stand.Probe','runtime':'org.stand.Runtime/x86_64/stable','commit':commit,'runtime_commit':rc,'entrypoint':'files/bin/probe'})
    appdir=td/'AppDir';appdir.mkdir();shutil.copy2(binary,appdir/'AppRun')
    (appdir/'probe.desktop').write_text('[Desktop Entry]\nType=Application\nName=Recorded probe\nExec=probe\nIcon=probe\nCategories=Utility;\n')
    (appdir/'probe.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>\n')
    squash=td/'root.squashfs';run('/usr/bin/mksquashfs',appdir,squash,'-noappend','-processors','1','-all-root','-no-xattrs','-mkfs-time','0','-all-time','0','-quiet')
    # Official Type-2 runtime input is cached and checksum-verified by the image recipe.
    runtime_bytes=(out/'appimage-runtime').read_bytes()
    if sha(runtime_bytes)!='617aa77314d57c8b8e4fae9c3f0b35af7b30d5529cb69e98f64f92510ed98a46':raise ValueError('official AppImage runtime checksum mismatch')
    if runtime_bytes[:4]!=b'\x7fELF' or runtime_bytes[8:11]!=b'AI\x02':raise ValueError('official AppImage runtime format mismatch')
    save('appimage',runtime_bytes+squash.read_bytes(),{'entrypoint':'AppRun','squashfs_offset':len(runtime_bytes),'runtime_sha256':sha(runtime_bytes)})
print('Application-format development fixtures built')
