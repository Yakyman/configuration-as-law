#!/usr/bin/env python3
"""Second-party, once-only step-6 procedure. The builder never invokes this file."""
import argparse,hashlib,importlib.util,json,pathlib,shlex,subprocess,sys,tarfile,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
APPLY='python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/'
QUERY='python3 -B /usr/local/lib/stand/bc4-compare.py '
WORKER='/opt/stand/pkgs/dev-worker/bin/worker'

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def stamp():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('case',choices=['1','2a','2b','3','4']);ap.add_argument('--publication',type=pathlib.Path,required=True);a=ap.parse_args()
    seal_path=ROOT/'raw/round-4-prep/inputs-seal.json';seal=json.loads(seal_path.read_bytes())
    publication=json.loads(a.publication.read_bytes())
    if not publication.get('public_record_url') or not publication.get('commit') or publication.get('inputs_seal_sha256')!=sha(seal_path):raise SystemExit('publication record must identify this exact seal before any attempt')
    for relative,digest in seal['files'].items():
        if sha(ROOT/relative)!=digest:raise SystemExit('sealed input mismatch: '+relative)
    if sha(ROOT/'base/stand.qcow2')!=seal['image_sha256']:raise SystemExit('frozen image mismatch')
    out=ROOT/'raw/round-4-second-party'/('case-'+a.case);out.mkdir(parents=True,exist_ok=False)
    (out/'publication.json').write_bytes(a.publication.read_bytes())
    (out/'started.json').write_text(json.dumps({'utc':stamp(),'case':a.case,'image_sha256':seal['image_sha256'],'inputs_seal_sha256':sha(seal_path)})+'\n')
    if a.case=='2b':
        (out/'not-expressible.json').write_text(json.dumps({'case':'2b','status':'not expressible on this testbed','reason':'Both the managed account row and the complete filesystem account database requirements state numeric identifiers. No omitted-identifier declaration is admitted.','outcome':'?','utc':stamp()})+'\n')
        return
    spec=importlib.util.spec_from_file_location('bc4_host_lab',ROOT/'lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
    owned=[];commands=[]
    def record(label,argv,data=None,required=True):
        commands.append({'label':label,'argv':[s.replace(str(ROOT),'[stand-root]').replace(str(pathlib.Path.home()),'[host-home]') for s in argv],'stdin':data,'utc':stamp()})
        (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        with (out/(label+'.stdout')).open('wb') as stdout,(out/(label+'.stderr')).open('wb') as stderr:
            r=subprocess.run(argv,input=data.encode() if data is not None else None,cwd=ROOT,stdout=stdout,stderr=stderr)
        (out/(label+'.exit')).write_text(str(r.returncode)+'\n')
        if required and r.returncode:raise RuntimeError('command failed: '+label)
        return r.returncode
    def guest(label,vm,script,root=True,required=True):
        return record(label,[sys.executable,'lab.py','run',vm]+(['--root'] if root else []),script,required)
    def create(suffix,names):
        vm='bc4-second-'+a.case+'-'+suffix
        if (ROOT/'vms'/vm).exists():raise RuntimeError('refuse existing guest: '+vm)
        owned.append(vm)
        record(suffix+'-new',[sys.executable,'lab.py','new',vm,'stand'])
        metadata=json.loads((ROOT/'vms'/vm/'meta.json').read_bytes())
        (out/(suffix+'-vm.json')).write_text(json.dumps({k:v for k,v in metadata.items() if k not in ('key',)},indent=2)+'\n')
        pid=int((ROOT/'vms'/vm/'qemu.pid').read_text());argv=pathlib.Path('/proc',str(pid),'cmdline').read_bytes().split(b'\0')
        clean=[x.decode().replace(str(ROOT),'[stand-root]') for x in argv if x]
        (out/(suffix+'-qemu-argv.json')).write_text(json.dumps(clean,indent=2)+'\n')
        guest(suffix+'-stage-directory',vm,'mkdir -p /var/lib/stand/bc4-inputs\n')
        with tempfile.TemporaryFile() as archive:
            with tarfile.open(fileobj=archive,mode='w') as tar:
                for name in names:tar.add(ROOT/'cases-6'/name,arcname=name)
            archive.seek(0)
            cmd=lab.ssh(ROOT/'vms'/vm,root=True)+['tar -xf - -C /var/lib/stand/bc4-inputs']
            with (out/(suffix+'-stage.stdout')).open('wb') as stdout,(out/(suffix+'-stage.stderr')).open('wb') as stderr:r=subprocess.run(cmd,stdin=archive,stdout=stdout,stderr=stderr)
            (out/(suffix+'-stage.exit')).write_text(str(r.returncode)+'\n')
            if r.returncode:raise RuntimeError('staging failed')
        guest(suffix+'-source-identities',vm,'sha256sum /var/lib/stand/bc4-inputs/*/declaration.json /var/lib/stand/bc4-inputs/*/blobs.json\n')
        return vm
    def snapshot(label,vm,name):guest(label,vm,QUERY+'snapshot --bundle /var/lib/stand/bc4-inputs/'+name+'/declaration.json\n')
    def apply(label,vm,name):guest(label,vm,APPLY+name+'\n')
    def package_state(label,vm):
        guest(label,vm,'set -e\n'+''.join(QUERY+'package '+p+'\n' for p in ['bc4-shared','bc4-owner-a','bc4-owner-b'])+'cat /var/lib/stand/objects.json\n')
    try:
        if a.case in ('1','2a'):
            name='case-'+a.case
            for side in ('left','right'):
                vm=create(side,[name])
                if a.case=='2a':
                    order=['alpha','beta'] if side=='left' else ['beta','alpha']
                    for index,pkg in enumerate(order,1):guest(side+'-install-'+str(index),vm,'stand-pkg install /usr/local/share/stand/bc4/package-'+pkg+'.json\n')
                    guest(side+'-accounts-before-final',vm,'getent passwd bc4alpha bc4beta\nid bc4alpha\nid bc4beta\ngetent group bc4alpha bc4beta\n')
                apply(side+'-apply',vm,name)
                guest(side+'-last-applied',vm,'cat /var/lib/stand/complete-last-success.json\npython3 -B /usr/local/lib/stand/bc3-state.py export\n')
                snapshot(side+'-snapshot',vm,name)
            record('pair-diff',[sys.executable,'-B','build/bc4-compare.py','diff',str(out/'left-snapshot.stdout'),str(out/'right-snapshot.stdout')])
        elif a.case=='3':
            vm=create('single',['case-3-before','case-3-after'])
            apply('before-apply',vm,'case-3-before');snapshot('before-snapshot',vm,'case-3-before')
            guest('before-launch',vm,WORKER+'\n',root=False)
            guest('before-service',vm,'/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath\n')
            guest('before-processes',vm,QUERY+'processes '+WORKER+'\n')
            apply('removal-apply',vm,'case-3-after')
            guest('after-processes',vm,QUERY+'processes '+WORKER+'\n')
            former=json.loads((out/'before-processes.stdout').read_bytes()).get('holders',[])
            identities=[{'pid':p['pid'],'starttime':p['starttime']} for p in former if 'starttime' in p]
            script="python3 -B - <<'PY'\nimport json,pathlib\nformer="+repr(identities)+"\nfor identity in former:\n p=pathlib.Path('/proc')/str(identity['pid'])/'stat'\n try:\n  fields=p.read_text().rsplit(') ',1)[1].split(); print(json.dumps({'former':identity,'exists':True,'same_starttime':fields[19]==identity['starttime'],'state':fields[0]}))\n except FileNotFoundError:print(json.dumps({'former':identity,'exists':False}))\nPY\n"
            guest('former-identities',vm,script)
            for label,script in [
              ('after-enabled','/usr/bin/systemctl is-enabled stand-development.service\n'),
              ('after-service','/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath\n'),
              ('after-rules-text','/usr/sbin/nft list table inet stand\n'),
              ('after-rules-json','/usr/sbin/nft -j list table inet stand\n'),
              ('after-executable','stat '+WORKER+'\n'),
              ('after-unit','stat /etc/systemd/system/stand-development.service\n')]:guest(label,vm,script,required=False)
            guest('after-launch',vm,WORKER+'\n',root=False,required=False)
            snapshot('after-snapshot',vm,'case-3-after')
        elif a.case=='4':
            vm=create('single',['case-4-both','case-4-one','case-4-none'])
            for stage,name in [('both','case-4-both'),('one','case-4-one'),('none','case-4-none')]:
                apply(stage+'-apply',vm,name);package_state(stage+'-packages',vm);snapshot(stage+'-snapshot',vm,name)
        (out/'completed.json').write_text(json.dumps({'utc':stamp(),'status':'commands completed','outcome':'requires independent judgment and separate review'})+'\n')
    except Exception as error:
        (out/'failure.json').write_text(json.dumps({'utc':stamp(),'error':str(error).replace(str(ROOT),'[stand-root]'),'outcome':'not inferred from command failure'})+'\n')
        raise
    finally:
        for vm in owned:
            if (ROOT/'vms'/vm).exists():
                guest(vm+'-final-reports',vm,'cat /var/lib/stand/complete-last-success.json /var/lib/stand/last-success.json\npython3 -B /usr/local/lib/stand/bc3-state.py export\n',required=False)
                record(vm+'-destroy',[sys.executable,'lab.py','destroy',vm],required=False)
        (out/'cleanup.json').write_text(json.dumps({'remaining_owned_guests':[v for v in owned if (ROOT/'vms'/v).exists()],'utc':stamp()})+'\n')
if __name__=='__main__':main()
