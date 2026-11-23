from pathlib import Path
import subprocess,json,hashlib
def run(args,**kw): return subprocess.run(['python3','lab.py',*args],check=True,**kw)
try:
 run(['new','bc3-metadata','stand'])
 with open('raw/factory-info.json','w') as out:
  run(['run','bc3-metadata','--root'],input="python3 -I - <<'GUEST'\n"+Path('raw/metadata-guest.py').read_text()+"\nGUEST\n",text=True,stdout=out)
 d=json.loads(Path('raw/factory-info.json').read_text())
 d['installed_source_equal']=all(h==hashlib.sha256((Path('build')/n).read_bytes()).hexdigest() for n,h in d['installed_hashes'].items())
 Path('raw/factory-info.json').write_text(json.dumps(d,indent=2)+'\n')
 run(['copy-out','bc3-metadata','/etc/stand/factory','raw/factory-export-final'])
finally:
 run(['destroy','bc3-metadata'])
