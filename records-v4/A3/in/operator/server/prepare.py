import pathlib,csv,hashlib,tarfile,subprocess,base64
p=pathlib.Path('A3/in/operator/server'); c=pathlib.Path('C1')
manifest={r['path']:r['sha256'] for r in csv.DictReader((c/'input-files.sha256.tsv').open(),delimiter='\t')}
files=[x for x in (c/'PUBLISH.list').read_text().splitlines() if x.startswith('collector/') or x in ['collect.sh','actions/lived-server.sh','actions/lib.sh']]
with tarfile.open(p/'inputs.tar','w') as tf:
 for f in files:
  assert hashlib.sha256((c/f).read_bytes()).hexdigest()==manifest[f],f
  tf.add(c/f,arcname='inputs/'+f)
(p/'verified-inputs.tsv').write_text('path\tsha256\n'+''.join(f'{f}\t{manifest[f]}\n' for f in files))
stage='#!/bin/bash\nset -e\nmkdir /tmp/a3-actions\n'
for f in ['lived-server.sh','lib.sh']:
 stage+=f"printf %s '{base64.b64encode((c/'actions'/f).read_bytes()).decode()}' | base64 -d > /tmp/a3-actions/{f}\n"
stage+='cd /tmp/a3-actions\nbash lived-server.sh\n'
(p/'guest-actions.sh').write_text(stage)
