"""Remove only the task's disposable resources after evidence transfer."""
import datetime,json,pathlib,shutil,subprocess
root=pathlib.Path(__file__).resolve().parent.parent
assert root.name=='c1-col'
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
p=subprocess.run([str(root/'lab.sh'),'destroy','col-debian'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=160)
record['debian_destroy_exit']=p.returncode;record['debian_destroyed']=not (root/'C1/vms/col-debian').exists()
cmd=['podman','--root',str(root/'podman-root'),'--runroot',str(root/'podman-run'),'--storage-driver','vfs']
record['containers']={}
for name in ('c1-col-rocky','c1-col-rocky-ro'):
 r=subprocess.run(cmd+['rm','-f',name],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 record['containers'][name]=r.returncode==0
r=subprocess.run(cmd+['rmi','--all','--force'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30);record['images_removed']=r.returncode==0
if not record['debian_destroyed'] or not all(record['containers'].values()):
 (root/'cleanup.json').write_text(json.dumps(record,indent=2)+'\n');raise SystemExit('Cleanup incomplete; retained task directory')
for p in root.iterdir():
 if p.name=='cleanup.json':continue
 if p.is_symlink() or p.is_file():p.unlink()
 else:shutil.rmtree(p)
record['task_artifacts_removed']=True;record['shared_slot_directory_preserved']= (root.parent/'slots').is_dir()
(root/'cleanup.json').write_text(json.dumps(record,indent=2)+'\n')
