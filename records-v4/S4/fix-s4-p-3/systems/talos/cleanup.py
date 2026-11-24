import pathlib,json,shutil,hashlib,subprocess as sp
from runner import R,L,D,O,N,run
sources=['runner.py','probe.py','reduce.py','cleanup.py','targets.json','expectations.md']
(O/'source-hashes.json').write_text(json.dumps({n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in sources},indent=2)+'\n')
rc=run('destroy',[str(L/'lab.sh'),'destroy',N],limit=180)
if rc:
 run('kill',[str(L/'lab.sh'),'kill',N],limit=60)
 rc=run('destroy-after-kill',[str(L/'lab.sh'),'destroy',N],limit=180)
assert rc==0
shutil.rmtree(D)
shutil.rmtree(L)
for p in R.glob('__pycache__'):shutil.rmtree(p)
(O/'cleanup.json').write_text(json.dumps({'destroy_exit':rc,'throwaway_disk_absent':not (L/'C1/vms'/N/'disk.qcow2').exists(),'isolated_runner_absent':not L.exists(),'transient_inventory_absent':not D.exists(),'qemu_process_matches':sum(N in x and 'qemu-system' in x for x in sp.check_output(['ps','-eo','args'],text=True).splitlines()),'no_object_decisions':True},indent=2)+'\n')
