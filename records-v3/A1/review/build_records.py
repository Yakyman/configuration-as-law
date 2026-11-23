"""Reproduce the sampling and write the review's row-level records."""
import csv, re, random, collections
from pathlib import Path

def read(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
def write(path, rows):
    with open(path, 'w') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t');w.writeheader();w.writerows(rows)
j=read('A1/compare/joined.tsv'); a=read('A1/adjudication/rows.tsv'); jm={r['id']:r for r in j}; am={r['id']:r for r in a}
for label,seed,pool,n in [('resolved',112221,[r for r in a if r['verdict'].startswith('RESOLVED:')],40),('agreed',112222,[r for r in j if r['same']=='yes' and r['id'] not in am],60)]:
    picked=random.Random(seed).sample(sorted(pool,key=lambda r:r['id']),n)
    assert [r['id'] for r in picked]==[r['id'] for r in read(f'A1/review/{label}-sample.tsv')]

confirmed={'guix-084d6fb332':'User auto-compilation cache; source home.scm is retained.',
'guix-033f2e4eef':'Root auto-compilation cache; source config.scm is retained.',
'guix-eaca1bed67':'system-boot.scm sets paired source and compiled load paths.',
'guix-5e84abb70c':'Captured activation script sets paired source and compiled load paths.'}
copied_nodes={'guix-ba6bc2924d','guix-8fd6717fba','guix-9e2b09e306','guix-d6f4da0567','guix-9849b393fe','guix-0c0c8b4f78'}
aggregates={'guix-25ad6943ae':'Home group contains p6c84... and pb4v... module-import-compiled outputs and their sources; whole-group removal is not speed-only.'}
uncertain={r['id'] for r in j if r['kind']=='system-closure-store-object' and r['name'].endswith('-module-import-compiled')} - set(confirmed)
uncertain.add('guix-da5f01a3ef')
rows=[]
for r in j:
    rid=r['id']
    if rid not in set(confirmed)|set(aggregates)|uncertain|copied_nodes:continue
    status='CONFIRMED-STANDALONE' if rid in confirmed else 'CONFIRMED-CONSTITUENT' if rid in aggregates else 'FACT-WRONG' if rid=='guix-2b6eee2e59' or rid in copied_nodes else 'FACTUAL-UNKNOWN'
    note=confirmed.get(rid,aggregates.get(rid,'The saved inventory names the compiled output but does not map this exact hash to retained source and a fallback loader. Not counted as confirmed.'))
    if rid=='guix-2b6eee2e59':note='Exact substitute archive decodes to a 96-byte empty-directory NAR; its SHA256 matches narinfo. There is no executable code. See extent-evidence-limit.md.'
    if rid=='guix-da5f01a3ef':note='Exact 7684-member list excludes all Home/user/system closure members. Its 18 other compiled-import outputs have no established source/loader mapping; do not count the Home objects a second time. See final-boundaries.md.'
    if rid in copied_nodes:note='guix-self.scm built-modules copies these build inputs into a final module union with #:copy? #t. Runtime paths point to the copied union, not this exact store object; deleting this input does not trigger source fallback there. FACT-WRONG as an H4 instance; see final-boundaries.md.'
    rows.append(dict(id=rid,kind=r['kind'],name=r['name'],extent_status=status,note=note,evidence=r['evidence']))
write('A1/review/hole-4-extent.tsv',rows)
# Search the complete table, including rows agreed by the classifications.
pattern=re.compile(r'compiled|guile|guix|shepherd|cache|\.go(?:$|\b)|\.pyc|__pycache__|python|pypy|javascript|mozilla|firefox|thunderbird|shader|emacs|\.eln',re.I)
search=[dict(id=r['id'],kind=r['kind'],name=r['name'],extent_status=next((x['extent_status'] for x in rows if x['id']==r['id']),'SCREENED-NOT-ESTABLISHED'),evidence=r['evidence']) for r in j if pattern.search(r['name']) or r['kind']=='store-group']
write('A1/review/hole-4-search.tsv',search)

out=[]
for r in read('A1/review/resolved-sample.tsv'):
    x=jm[r['id']]; rid=r['id']; status='SUPPORTED'; dec=r['verdict'].split(':')[1]; ids=r['sentence_id']; note=r['note']; support='yes'
    if r['verdict']=='RESOLVED:NOT' and r['sentence_id']=='S2.2-2':
        status='REFUTED';support='no';ids='S2.2-1,S2.2-2';note='The quoted positive removal implication alone does not prove NOT. The established absence of any behavioural contribution places this object outside the scope of S2.2-1, and no explicit must-record category applies. '+r['note']
    if r['sentence_id']=='S2.5-1':
        status='OUTSIDE';support='outside';dec='OUTSIDE';note='The stated treatment of program state is outside the definition under S2.5-1 and COMMON.md; this is not a blanket textual exemption from recording every state-related object. '+r['note']
    if rid in ['debian-9e34733f17','guix-68f88fa3ed','ubuntu-b20e807939']:
        status='FACT-WRONG';support='no';dec='MUST';ids='S2.2-2';note='The asserted absence of a capability loss, or speed-only regeneration, is contradicted by available program capabilities; see resolved-fact-challenges.md.'
    if rid=='guix-0abb5d3f0a':
        status='REFUTED';support='no';dec='UNKNOWN';ids='S3-2';note='Absence of matching hardware does not establish lack of topology-compilation capability. Exact compiler availability is not established; factual UNKNOWN, not a wording hole. See resolved-fact-challenges.md.'
    if rid=='debian-desktop-2a6c5aa500':
        status='REFUTED';support='no';ids='S2.2-4,S2.2-6,S2.2-7';note='The quoted settings exemption decides preferences, but not the entire profile. Messages are content; telemetry/session records are past records or program state. The note itself identifies these distinct members. Together the cited exemptions resolve the candidate; no collision.'
    if rid=='ubuntu-869a3e13d4':
        status='REFUTED';support='no';ids='S2.2-5,S2.5-1';note='S2.2-5 covers cached package data, not the recreated lock member. The lock is transient coordination state whose treatment is outside under S2.5-1; the composite candidate is therefore resolved by the two clauses, not by the cache quotation alone.'
    if rid=='guix-30d7041bdd':
        status='REFUTED';support='no';ids='S2.2-1,S2.2-2';note='The object is a profile link tree, not itself the program named by the quotation. Removing the documented PATH profile makes programs unreachable; the behavioural/removal rule decides MUST.'
    if rid in ['ubuntu-89ce5c5668','arch-89ce5c5668']:
        status='OUTSIDE';support='outside';dec='OUTSIDE';ids='S2.5-1';note='The quotation records the kernel program, not separately every runtime thread instance. The treatment of these runtime kernel-state instances is outside under S2.5-1, consistently with original card 5; this does not exempt kernel code itself.'
    if rid=='debian-4a04681652':
        status='REFUTED';support='no';dec='UNKNOWN';ids='S3-2';note='The row contains the package-owned directory alone, not past log files, so S2.2-6 does not decide it. APT 2.6.1 recreates this directory before logging; exact installed 2.6.2 source was not retrieved. Keep factual UNKNOWN rather than infer a new wording hole; see resolved-fact-challenges.md.'
    if rid=='nixos-6cad6264ed':
        status='CONFIRMED:H1';support='no';dec='HOLE';ids='S2.2-1,S2.2-2,S2.2-7,S2.2-13';note='The ssh client applies the value settings but their connection/authentication effects reach beyond it. S2.2-7 does not define whether in force inside means the applying program or effect scope. See final-boundaries.md.'
    if rid=='coreos-4d2a7c7537':
        status='CONFIRMED:H1';support='no';dec='HOLE';ids='S2.2-1,S2.2-2,S2.2-7';note='Manager enablement directories/links select which other processes start. They are settings of one manager with external effects; the removal quotation states only the mandatory side of H1. Constituent occurrence; see final-boundaries.md.'
    if rid=='debian-c366c1919d':
        note+=' The overall MUST is supported by the explicit server-login rule, but the note separately calls ssh_config NOT without resolving H1; record that constituent in the H1 extent without changing this row-level supported MUST.'
    out.append(dict(id=rid,name=x['name'],original_verdict=r['verdict'],sentence_id=r['sentence_id'],quote=r['quote'],quote_support=support,review_status=status,review_decision=dec,deciding_sentences=ids,review_note=note,evidence=x['evidence']))
write('A1/review/resolved-audit.tsv',out)
print('extent',dict(collections.Counter(r['extent_status'] for r in rows)),'search',len(search))
print('sample',dict(collections.Counter(r['review_status'] for r in out)))
