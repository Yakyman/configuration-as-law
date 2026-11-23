from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import difflib, hashlib, json, re

base = Path('B1')
out = base / 'fix-b1-1'
errors = []
text = (base/'CHANNELS.md').read_text()
rows = [[c.strip() for c in re.split(r'(?<!\\)\|', line)[1:-1]] for line in text.splitlines() if re.match(r'^\| [CM]\d', line)]
ids = [row[0].split()[0] for row in rows]
if any(len(row) != 6 for row in rows): errors.append('Table width')
if len(ids) != len(set(ids)): errors.append('Duplicate variant IDs')
counts = Counter(row[2] for row in rows)
expected = f"CHANNELS: {counts['CLOSABLE']} closable, {counts['CLOSABLE-ONLY-BY-REMOVAL']} closable only by removal, {counts['NOT-CLOSABLE']} not closable, {counts['TEXT-OPEN']} text-open, {counts['UNKNOWN']} unknown"
if text.splitlines()[0] != expected: errors.append('Header counts')
if json.loads((out/'variant-inventory.json').read_text()) != rows: errors.append('JSON inventory differs')
index = {r[0].split()[0]: r for r in rows}
required = {
    'C10.4':'TEXT-OPEN', 'C8.07':'UNKNOWN', 'C7.08':'CLOSABLE',
    'C7.24':'CLOSABLE', 'C7.25':'UNKNOWN',
    **{k:'UNKNOWN' for k in 'C7.03 C7.04 C7.05 C7.06 C7.17 C8.03 C8.06 C1.1 C1.2 C1.4 C1.5 C3.1 C6.2 C6.3 C9.1 C9.5 C10.1 C10.2'.split()}
}
for key, verdict in required.items():
    if index[key][2] != verdict: errors.append('Required correction: '+key)
design = (base/'DESIGN-INPUT.md').read_text()
design_list = dict(re.findall(r'^- \*\*([CM]\d+\.\d+) — ([A-Z-]+):\*\*',design,re.M))
expected_list = {k:r[2] for k,r in index.items() if r[2]!='CLOSABLE'}
if design_list != expected_list: errors.append('Non-CLOSABLE design list mismatch')
original = json.loads((out/'input-manifest.json').read_text())['inputs']
changed = []
frozen = []
for entry in original:
    p = Path(entry['path'])
    saved = out/'before'/p
    if hashlib.sha256(saved.read_bytes()).hexdigest() != entry['sha256']:
        errors.append('Snapshot changed: '+str(p))
    if hashlib.sha256(p.read_bytes()).hexdigest() != entry['sha256']:
        changed.append(str(p))
        if str(p) not in ['B1/CHANNELS.md','B1/DESIGN-INPUT.md']:
            errors.append('Frozen input changed: '+str(p))
    else:
        frozen.append(str(p))
reports = [base/'CHANNELS.md',base/'DESIGN-INPUT.md',base/'FIX-B1-1.md']
new_md = sorted(out.glob('*.md'))
diff=''
for p in reports[:2]:
    diff+=''.join(difflib.unified_diff((out/'before'/p).read_text().splitlines(True),p.read_text().splitlines(True),fromfile='before/'+str(p),tofile=str(p)))
(out/'reports.diff').write_text(diff)
checked_links = 0
for p in reports+new_md:
    s=p.read_text()
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if '://' in target or target.startswith('#'): continue
        target=target.split('#',1)[0]
        resolved=p.parent/target
        # This report is written at the end of this invocation.
        generated_validation=resolved.resolve()==(out/'validation.json').resolve()
        if target and not generated_validation and not resolved.exists(): errors.append('Missing link: '+str(p)+' -> '+target)
        checked_links+=1
sentences={}
for line in Path('SENTENCES.md').read_text().splitlines():
    m=re.match(r'- \*\*(S\d+(?:\.\d+)?-\d+)\*\* (.*)',line)
    if m: sentences[m[1]]=m[2]
quotations=0
for match in re.finditer(r'(S\d+(?:\.\d+)?-\d+)(?: says exactly)?: “([^”]+)”',text):
    if match[1] not in sentences or match[2] != sentences[match[1]]:
        errors.append('Non-exact sentence quote: '+match[1])
    quotations+=1
for phrase in ['C7.03 stays CLOSABLE', 'not a fourth hole', '### T2 — Browser extension', 'does not compel accepting that algorithm', 'a cooperative evaluator checking every file']:
    if phrase in text or phrase in design: errors.append('Stale conclusion: '+phrase)
if 'S2.2-15' not in text.split('**R** in each channel row means',1)[1].split('\n',1)[0]: errors.append('R misses port requirement')
if len(re.findall(r'^\| \d+\.',(base/'FIX-B1-1.md').read_text(),re.M)) != 12: errors.append('Finding count')
result={
 'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Changed report consistency checks only; no probe and no independent acceptance',
 'status':'PASS' if not errors else 'FAIL', 'errors':errors,
 'row_count':len(rows), 'counts':dict(counts), 'header':expected,
 'required_corrections_checked':len(required),
 'design_nonclosable_exact_match':design_list==expected_list,
 'design_nonclosable_count':len(design_list),
 'local_links_checked':checked_links, 'exact_sentence_quotes_checked':quotations,
 'finding_dispositions':12, 'snapshots_checked':len(original),
 'original_files_changed':changed, 'frozen_original_files_unchanged':len(frozen),
 'fixed_text_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['TEXT.md','SENTENCES.md']},
 'empirical_reruns':0
}
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
