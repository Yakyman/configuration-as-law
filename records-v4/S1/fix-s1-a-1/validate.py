from pathlib import Path
import csv
import difflib
import hashlib
import re
import subprocess

out=Path('S1/fix-s1-a-1/raw')
argument=Path('S1/ARGUMENT.md').read_text()
checks=[]
expected='STEP 1: Understanding 0; Reproducibility ?; Removal ?'
assert argument.splitlines()[0]==expected
assert Path('S1/FIX-S1-A-1.md').read_text().splitlines()[0]==expected
checks.append('Outcome lines: Understanding 0; Reproducibility ?; Removal ?.')
command=['/usr/bin/python3','-I','bin/check_quotes.py','S1/ARGUMENT.md']
result=subprocess.run(command,text=True,capture_output=True)
(out/'quote-check.txt').write_text('Command: '+' '.join(command)+'\n'+result.stdout+result.stderr+f'Exit status: {result.returncode}\n')
assert result.returncode==0,result.stdout
checks.append(result.stdout.strip())
numbered={}
for line in Path('SENTENCES.md').read_text().splitlines():
    m=re.match(r'- \*\*(S\d\.\d-\d+)\*\* (.+)$',line)
    if m: numbered[m[1]]=m[2]
quotes=re.findall(r'^- (S\d\.\d-\d+): «([^»]+)»$',argument,re.M)
for sid,quote in quotes:
    assert numbered[sid]==quote,(sid,quote)
checks.append(f'Sentence-ID/quotation correspondence: {len(quotes)} exact matches.')
before=Path('S1/fix-s1-a-1/before/ARGUMENT.md').read_text()
def table_identity(text):
    return [tuple(part.strip() for part in line.split('|')[1:4]) for line in text.splitlines() if re.match(r'\| L[12]:',line)]
assert table_identity(argument)==table_identity(before)
checks.append(f'Crosswalk kind/count/example-ID columns: all {len(table_identity(argument))} rows unchanged from pre-fix argument. No inventory recount performed.')
rows=list(csv.DictReader((out/'preserved-input-hashes.tsv').open(),delimiter='\t'))
for row in rows:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
checks.append(f'Preserved inputs and original evidence: {len(rows)} fingerprints unchanged.')
for row in csv.DictReader(Path('S1/raw/input-hashes.tsv').open(),delimiter='\t'):
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
checks.append('Original seven input fingerprints still match.')
fix=Path('S1/FIX-S1-A-1.md').read_text()
findings=re.findall(r'^\| (\d+)\.',fix,re.M)
assert findings==[str(i) for i in range(1,11)]
checks.append('Disposition covers all ten review findings.')
for filename in ('S1/ARGUMENT.md','S1/QUESTIONS.md','S1/FIX-S1-A-1.md'):
    value=Path(filename).read_text()
    assert not re.search(r'/home/|<HOST>',value,re.I),filename
    assert 'awaiting RV-S1' not in value,filename
checks.append('Updated result documents: no local home paths, machine identifiers ; no stale pre-review status.')
diff=''
for name in ('ARGUMENT.md','QUESTIONS.md'):
    diff+=''.join(difflib.unified_diff((Path('S1/fix-s1-a-1/before')/name).read_text().splitlines(True),(Path('S1')/name).read_text().splitlines(True),fromfile='before/'+name,tofile='S1/'+name))
(out/'changes.diff').write_text(diff)
checks.append('Exact argument/questions diff saved as changes.diff.')
checks.append('No behavioural experiments or machines run in this fix round; revised reasoning awaits separate acceptance.')
(out/'validation.txt').write_text('Recorded 2026-11-23 UTC.\nCommand: /usr/bin/python3 -I S1/fix-s1-a-1/validate.py\n'+'\n'.join(checks)+'\n')
print('\n'.join(checks))
