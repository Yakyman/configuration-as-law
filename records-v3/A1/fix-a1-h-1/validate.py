"""Validate this correction without regenerating frozen inputs or samples."""
import csv,hashlib,json,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]; out=root/'A1/fix-a1-h-1'
def read(p):
 with (root/p).open() as f:return list(csv.DictReader(f,delimiter='\t'))
frozen=json.loads((out/'raw/frozen-input-sha256.json').read_text())
changed=[p for p,h in frozen.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
for sample,n in [('agreed',60),('resolved',40)]:
 old=read(f'A1/review/{sample}-audit.tsv');new=read(f'A1/fix-a1-h-1/{sample}-audit.tsv')
 assert len(new)==n and [r['id'] for r in old]==[r['id'] for r in new]
checks=read('A1/fix-a1-h-1/unit-file-reader-check.tsv')
assert len(checks)==598
for r in checks:
 if r['kind']=='system-unit':assert 'user-list-unit-files' not in r['available_inventory_matches']
 if r['kind']=='user-unit':assert 'unit-files.txt:' not in r['available_inventory_matches'].replace('user-list-unit-files.txt:','')
assert sum(r['second_applier'].startswith('ESTABLISHED') for r in checks)==21
badlinks=[]
for p in [root/'A1/RESULT.md',root/'A1/FIX-A1-H-1.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link:continue
  if not (p.parent/link.split('#',1)[0]).exists():badlinks.append(str(p.relative_to(root))+': '+link)
assert not badlinks,badlinks
proc=subprocess.run(['/usr/bin/python3','-I','bin/check_quotes.py','A1/RESULT.md'],cwd=root,text=True,capture_output=True)
assert proc.returncode==0,proc.stdout+proc.stderr
(out/'raw/quote-check.log').write_text(proc.stdout+proc.stderr)
summary={'frozen_files_unchanged':len(frozen),'sample_ids_and_order':'unchanged (40 resolved; 60 agreed)','checked_unit_rows':len(checks),'conditional_file_second_applier':21,'local_result_fix_links':'all resolve','quote_check':proc.stdout.strip()}
(out/'raw/validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
