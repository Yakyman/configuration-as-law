import csv,pathlib,collections
p=pathlib.Path('A1/c1/part-3.stored.tsv')
rows=list(csv.DictReader(p.open(),delimiter='\t'));header=list(rows[0])
updates={
'nixos-bfd49e603a':dict(decision='MIXED',sentences='S2.2-4,S3-1,S3-2',reason='The nixos-rebuild and nixos-version manual-page documents: NOT. All other listed store objects: UNKNOWN; names alone do not establish every operational role.'),
'nixos-76634f69cd':dict(decision='MIXED',sentences='S2.2-1,S2.2-4,S2.2-10,S3-2',reason='Loadable modules and their containing directories: MUST; font, translations, and their directories: NOT; all remaining members: UNKNOWN without contents or established use.'),
'nixos-0075a76d48':dict(decision='MIXED',sentences='S2.2-1,S2.2-15,S3-2',reason='Authorized login key and its containing directories: MUST. Other keys, moduli, known hosts, and configuration members: UNKNOWN without local role or contents evidence.'),
'nixos-b86fee9a16':dict(decision='MIXED',sentences='S2.2-1,S2.2-9,S2.2-10,S3-2',reason='Environment generator and its containing directories: MUST. Remaining service trees, presets, and daemon settings: UNKNOWN because local contents and effective behavior are absent.')}
for r in rows:
 if r['id'] in updates:r.update(updates[r['id']])
 assert len(r['reason'].split())<=30
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
p=pathlib.Path('A1/c1/part-3.stored.build.py');lines=p.read_text().splitlines()
for r in rows:
 if r['id'] not in updates:continue
 prefix="add('"+r['id'].removeprefix('nixos-')+"',"
 replacement='add('+','.join(repr(x) for x in [r['id'].removeprefix('nixos-'),r['decision'],r['sentences'],r['what_it_does'],r['basis'],r['reason']])+')'
 indices=[i for i,l in enumerate(lines) if l.startswith(prefix)];assert len(indices)==1
 lines[indices[0]]=replacement
p.write_text('\n'.join(lines)+'\n')
p=pathlib.Path('A1/c1/part-3.stored.notes.md');s=p.read_text()
s=s.replace('A group decision remains UNKNOWN when the available inventory and documentation do not support a complete member partition.','A group uses MIXED when its members receive different decisions, including explicitly identified UNKNOWN members. Missing knowledge is retained at member level when other members have established decisions.')
p.write_text(s)
print(collections.Counter(r['decision'] for r in rows))
