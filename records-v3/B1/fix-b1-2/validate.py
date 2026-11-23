from pathlib import Path
import collections,datetime,hashlib,json,re,sys
root=Path('B1'); out=root/'fix-b1-2'; errors=[]
def check(ok,msg):
 if not ok: errors.append(msg)
def parse(s):
 rows=[]
 for line in s.splitlines():
  if re.match(r'^\| [CM]\d',line):
   cells=[v.strip() for v in re.split(r'(?<!\\)\|',line.strip('|'))]
   check(len(cells)==6,'Malformed table row')
   rows.append(cells)
 return rows
text=(root/'CHANNELS.md').read_text(); before=(out/'before/B1/CHANNELS.md').read_text()
rows=parse(text); old=parse(before); byid={r[0].split()[0]:r for r in rows}; oldbyid={r[0].split()[0]:r for r in old}
check(len(rows)==88 and len(byid)==88,'Variant count or uniqueness')
check(set(byid)==set(oldbyid),'Added or removed variant IDs')
counts=collections.Counter(r[2] for r in rows)
check(counts=={'CLOSABLE':8,'TEXT-OPEN':3,'UNKNOWN':77},'Verdict totals')
expected=f"CHANNELS: {counts['CLOSABLE']} closable, 0 closable only by removal, 0 not closable, {counts['TEXT-OPEN']} text-open, {counts['UNKNOWN']} unknown"
check(text.splitlines()[0]==expected,'Header mismatch')
for rid,r in byid.items():
 check(r[1]==oldbyid[rid][1],'Changed requirement: '+rid)
 if rid.startswith('C'): check(r[2]!='CLOSABLE','Full-R row still CLOSABLE: '+rid)
 else: check(r==oldbyid[rid],'Mechanic row changed: '+rid)
check(next(x for x in text.splitlines() if x.startswith('**R**'))==next(x for x in before.splitlines() if x.startswith('**R**')),'R changed')
for start,end in [('## TEXT-OPEN cards','## Q1'),('## Q2','## Q3')]:
 check(text[text.index(start):text.index(end)]==before[before.index(start):before.index(end)],'Accepted text readings changed: '+start)
check('E1,E2,E12,E16' in byid['C7.05'][4],'C7.05 E12 missing')
check(all(t in byid['C7.24'][3] for t in ['File-open route','non-file route','stdin','argv/environment','inherited FDs','socket/IPC']),'C7.24 missing input routes')
check(all(byid[r][2]=='UNKNOWN' and 'mandatory' in byid[r][3] for r in ['C2.6','C4.4','C7.01','C7.07','C7.08','C7.09','C7.23','C7.24','C8.01','C8.02']),'D coverage claims')
q3=text[text.index('## Q3'):]
check('whole session' in q3 and 'editor inherits' in q3,'Q3 editor inheritance cost')
check(q3.count('stdin, argv/environment, inherited descriptors and socket/IPC input')==2,'Q3 non-file inputs')
design=(root/'DESIGN-INPUT.md').read_text()
actual=[(m[0],m[1],m[2]) for m in re.findall(r'^- \*\*([CM]\d+\.\d+) — ([A-Z-]+):\*\* (.*)\.$',design,re.M)]
nonclosable=[(r[0].split()[0],r[2],r[0].split(' ',1)[1]) for r in rows if r[2]!='CLOSABLE']
check(actual==nonclosable,'Design non-CLOSABLE inventory mismatch')
keys=['variant','requirement','verdict','mechanism','evidence','cost']
check(json.loads((out/'variant-inventory.json').read_text())==[dict(zip(keys,r)) for r in rows],'JSON inventory mismatch')
changes=[{'id':r[0].split()[0],'before':oldbyid[r[0].split()[0]],'after':r} for r in rows if r!=oldbyid[r[0].split()[0]]]
check(changes==json.loads((out/'row-changes.json').read_text()),'Row changes mismatch')
verdict_changes=[x['id'] for x in changes if x['before'][2]!=x['after'][2]]
check(len(verdict_changes)==31,'Verdict change count')
manifest=json.loads((out/'input-manifest.json').read_text())['sha256']
changed=[]
for name,digest in manifest.items():
 p=Path(name)
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: changed.append(name)
check(sorted(changed)==['B1/CHANNELS.md','B1/DESIGN-INPUT.md'],'Frozen inputs changed')
for p in (out/'before').rglob('*'):
 if p.is_file(): check(hashlib.sha256(p.read_bytes()).hexdigest()==manifest[str(p.relative_to(out/'before'))],'Snapshot mismatch')
# Exact sentence quotations in the edited report.
sentences=dict(re.findall(r'^- \*\*(S[23][\d.]*-\d+)\*\* (.*)$',Path('SENTENCES.md').read_text(),re.M))
quotes=re.findall(r'(S[23][\d.]*-\d+)(?: says exactly:?| explicitly says:|:)? “([^”]+)”',text)
for sid,quote in quotes: check(sentences.get(sid)==quote,'Sentence quote mismatch: '+sid)
check(len(quotes)>=18,'Too few checked exact quotations')
fix=(root/'FIX-B1-2.md').read_text()
check(len(re.findall(r'^\| [1-8]\. ',fix,re.M))==8,'Finding dispositions missing')
files=[root/'CHANNELS.md',root/'DESIGN-INPUT.md',root/'FIX-B1-2.md',out/'evidence-audit.md',out/'WORKLOG.md',out/'REVIEW.md']
links=0
for p in files:
 check(p.exists(),'Missing record: '+str(p))
 if not p.exists(): continue
 s=p.read_text()
 for target in re.findall(r'\]\(([^)]+)\)',s):
  if target.startswith(('http:','https:','#')): continue
  target=target.split('#')[0];links+=1
  check((p.parent/target).exists(),'Broken local link: '+str(p)+' -> '+target)
 check(not re.search(r'/home/|<HOST>|\b(?:independent reviewer|independent reviewer|independent reviewer|independent reviewer|independent reviewer|<USER>)\b',s,re.I),'Publication hygiene: '+str(p))
review=(out/'REVIEW.md').read_text() if (out/'REVIEW.md').exists() else ''
check(review.startswith('VERDICT: AGREE'),'Separate review not AGREE')
result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Changed report consistency and input preservation; no empirical rerun','status':'PASS' if not errors else 'FAIL','errors':errors,'row_count':len(rows),'counts':dict(counts),'header':expected,'verdict_change_count':len(verdict_changes),'changed_row_count':len(changes),'requirements_unchanged':True if not any('requirement' in e or 'R changed' in e for e in errors) else False,'design_nonclosable_count':len(actual),'exact_sentence_quotes_checked':len(quotes),'local_links_checked':links,'original_files_changed':sorted(changed),'frozen_original_files_unchanged':len(manifest)-len(changed),'fixed_text_sha256':{n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in ['TEXT.md','SENTENCES.md']},'empirical_reruns':0,'independent_review':review.splitlines()[0] if review else 'pending'}
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
