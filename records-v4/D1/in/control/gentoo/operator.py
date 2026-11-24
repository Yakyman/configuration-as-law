import subprocess as sp, pathlib, json, time, os, tarfile, io, base64
R=pathlib.Path.home()/'VMs/cal-1123'
D=R/'D1/gentoo'; D.mkdir(parents=True,exist_ok=True)
C=D/'control'; C.mkdir(exist_ok=True)
lab=str(R/'lab.sh'); vm='d1-gentoo'; statuses={}
def command(label,args,script=None):
    with (C/(label+'.out')).open('wb') as out,(C/(label+'.err')).open('wb') as err:
        p=sp.run(args,input=script,stdout=out,stderr=err,cwd=R)
    statuses[label]=p.returncode
    (C/'status.json').write_text(json.dumps(statuses,indent=2)+'\n')
    return p.returncode
try:
    if command('new',[lab,'new',vm,'gentoo']): raise RuntimeError('Fresh-machine creation failed')
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode='w:gz') as tf:
        tf.add(R/'D1/inputs/actions',arcname='actions')
    encoded=base64.b64encode(buf.getvalue()).decode()
    launch='''#!/bin/bash
set -eu
mkdir /tmp/d1-gentoo-operator
base64 -d <<'DATA' | tar xz -C /tmp/d1-gentoo-operator
'''+encoded+'''
DATA
cat > /tmp/d1-gentoo-operator/entry.sh <<'ENTRY'
#!/bin/bash
cd /tmp/d1-gentoo-operator/actions
bash gentoo.sh
rc=$?
printf '%s\\n' "$rc" > /tmp/d1-gentoo-operator/action-exit
ENTRY
setsid bash /tmp/d1-gentoo-operator/entry.sh > /tmp/d1-gentoo-operator/entry.out 2> /tmp/d1-gentoo-operator/entry.err < /dev/null &
'''
    if command('launch',[lab,'run',vm,'--timeout','120'],launch.encode()): raise RuntimeError('Action launch failed')
    i=0
    while True:
        time.sleep(30); i+=1
        rc=command('action-monitor-%03d'%i,[lab,'run',vm,'--timeout','120'],b'#!/bin/bash\ntest -f /tmp/d1-gentoo-operator/action-exit\n')
        if rc==0: break
        if rc!=1: raise RuntimeError('Action completion monitor failed')
    for leaf in ['actions-status.tsv','actions-logs']:
        if command('copy-'+leaf,[lab,'copy-out',vm,'/home/user/'+leaf,str(C)]): raise RuntimeError('Action evidence copy failed')
    if command('copy-operator',[lab,'copy-out',vm,'/tmp/d1-gentoo-operator',str(C)]): raise RuntimeError('Operator evidence copy failed')
    if command('cleanup-staging',[lab,'run',vm,'--timeout','120'],b'#!/bin/bash\nset -e\nrm -rf /tmp/d1-gentoo-operator "$HOME/actions-status.tsv" "$HOME/actions-logs"\n'): raise RuntimeError('Operator cleanup failed')
    env=os.environ.copy();env['LAB_ROOT']=str(R);env['C1_INPUTS_COMMIT']='b3c3c141c612b8d287c8058733141cb56d1c2431'
    with (C/'collector.out').open('wb') as out,(C/'collector.err').open('wb') as err:
        p=sp.run([str(R/'D1/inputs/collect.sh'),'--observe',vm,str(D/'raw')],env=env,stdout=out,stderr=err,cwd=R)
    statuses['collector']=p.returncode
except Exception as e:
    (C/'failure.txt').write_text(str(e)+'\n')
finally:
    command('destroy',[lab,'destroy',vm])
    (C/'status.json').write_text(json.dumps(statuses,indent=2)+'\n')
    (D/'DONE').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')
