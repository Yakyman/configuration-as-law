#!/usr/bin/env python3
"""Assemble exact successful BC4 exports; no abbreviated or inferred rows."""
import argparse,hashlib,json,pathlib,shutil
P=pathlib.Path
p=argparse.ArgumentParser();p.add_argument('evidence',type=P);p.add_argument('output',type=P);a=p.parse_args()
if a.output.exists():raise SystemExit('refusing existing export directory')
summary=json.loads((a.evidence/'summary.json').read_text())
for name in ('language','applications','system','ordinary'):
    r=summary['suites'][name]
    if not r.get('tested') or any(r.get(k)!=0 for k in ('suite_exit','verify_exit','example_export_exit')):
        raise SystemExit('successful fresh-suite export required: '+name)
rows={};origins={}
for file in sorted(a.evidence.glob('*-examples/channel-examples/*.jsonl')):
    for line in file.read_text().splitlines():
        row=json.loads(line);ident=row['id']
        if ident in rows and rows[ident]!=row:raise SystemExit('conflicting exact exports: '+ident)
        rows[ident]=row;origins.setdefault(ident,[]).append(str(file.relative_to(a.evidence)))
required={'repository:hello','system:base-state','language:pip:development','language:npm:development',
          'language:pip:native-development','round4-flatpak','round4-appimage','round4-oci-image','round4-oci',
          'import:downloaded','source:source-example','import:source-example-built','dev-worker','dev-service',
          'round4-user-timer','schedule:scheduled-example:service','schedule:scheduled-example:timer','dev-wifi','dev-bluetooth'}
if set(rows)!=required:raise SystemExit('exact required export membership differs: '+str(set(rows)^required))
a.output.mkdir(parents=True)
shutil.copytree(a.evidence/'factory-export/factory',a.output/'factory')
shutil.copytree(a.evidence/'system-state/channel-system-state',a.output/'combined')
combined=a.output/'combined/machine.jsonl';base={r['id']:r for r in map(json.loads,combined.read_text().splitlines())}
for ident,row in rows.items():
    if ident in base and base[ident]!=row:raise SystemExit('conflicting system-state contribution: '+ident)
    base[ident]=row
canonical=lambda r:json.dumps(r,sort_keys=True,separators=(',',':'))+'\n'
combined.write_text(''.join(canonical(base[k]) for k in sorted(base)))
(a.output/'channels').mkdir();(a.output/'channels/machine.jsonl').write_text(''.join(canonical(rows[k]) for k in sorted(rows)))
manifest={str(f.relative_to(a.output)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.output.rglob('*')) if f.is_file()}
(a.output/'provenance.json').write_text(json.dumps({'image_sha256':summary['image_sha256'],'row_origins':origins,'files_sha256':manifest},indent=2,sort_keys=True)+'\n')
print(json.dumps({'exported_channel_rows':len(rows),'complete_declaration_rows':len(base),'files_sha256':manifest},sort_keys=True))
