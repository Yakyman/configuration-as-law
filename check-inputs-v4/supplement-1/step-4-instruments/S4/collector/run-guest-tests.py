import base64,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parent.parent
parts=['set -eu','export DEBIAN_FRONTEND=noninteractive','apt-get -q update','apt-get -q -y install busybox toybox strace btrfs-progs','rm -rf /tmp/c1-tests; mkdir -p /tmp/c1-tests']
for source,target,zipped in [('probe-linux-amd64.gz','probe',True),('guest-tests.py','guest-tests.py',False),('talos.py','talos.py',False)]:
 data=base64.b64encode((root/'collector'/source).read_bytes()).decode();parts.append("printf %s '"+data+"' | base64 -d"+(' | gzip -d' if zipped else '')+' > /tmp/c1-tests/'+target)
parts+=['chmod 700 /tmp/c1-tests/probe','cd /tmp/c1-tests','python3 -B guest-tests.py']
p=subprocess.run([str(root/'lab.sh'),'run','col-debian','--root'],input=('\n'.join(parts)+'\n').encode(),timeout=600)
raise SystemExit(p.returncode)
