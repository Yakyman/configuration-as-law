"""Changed extent/ledger accounting. Does not overwrite prior analysis or sample inputs."""
import csv,json,re
from collections import Counter
from pathlib import Path
OUT=Path('D1/fix-d1-h-2/raw')
csv.field_size_limit(10000000)
def read(p, raw=False):
    with Path(p).open() as f:return list(csv.DictReader(f,delimiter='\t',**({'quoting':csv.QUOTE_NONE} if raw else {})))
def write(name,rs):
    with (OUT/name).open('x') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs)
joined=read('D1/compare/joined.tsv',True); byid={r['id']:r for r in joined}
adj={r['id']:r for r in read('D1/adjudication/rows.tsv',True)}
scan=read(OUT/'whole-table-search.tsv'); candidates=read(OUT/'candidates.tsv')
tag_members={}
for t in read('D1/adjudication/raw/l2o_member_classes.tsv',True):
    if t['class']=='GAP:generated-list':tag_members.setdefault(t['id'],[]).append(t['path'])
micro_facts={(t['id'],t['path']):t['fact'] for t in read('D1/adjudication/raw/microos-members.tsv',True)}
# These rows do not establish the optional-record branch for all members.
limits={
'alma-caff428f8364f0a663721a85':('FACT_UNKNOWN','Contents/use of compiled dconf values: system/launch/access settings versus personal-program values.'),
'void-f2e5d5edfa5902c8aee7bace':('UNDECIDED:row-audit','The earlier certificate-setting inference was withdrawn; the role of the trust values is not established by generation alone.'),
'microos-7b851b26fa99c2a7ca64763f':('UNDECIDED:row-audit','Certificate bundle: generation alone does not establish the optional-record branch for its trust values.'),
'microos-dcce813055fa256ed012c87a':('UNDECIDED:row-audit','Certificate links/data: generation alone does not establish the optional-record branch for its trust values.'),
'microos-3aecc583b26d47be2c87f514':('UNDECIDED:row-audit','Certificate files: generation alone does not establish the optional-record branch for their trust values.'),
'microos-2ce40b9afb2194333071f853':('UNDECIDED:row-audit','Known policy values are access settings (S8.2-13); a row-wide optional record verdict is not established for this mixed policy store.'),
'microos-041c4df356de375ebbc7df6d':('UNDECIDED:row-audit','Policy module representations: no row-wide optional-record decision is established by their generation.'),
'microos-01b419c42b39b4d368973076':('UNDECIDED:row-audit','Compiled policy representations and unchanged package members: no row-wide optional-record decision is established.'),
}
extent=[]; original=[]
for s in scan:
    r=byid[s['id']]; a=adj.get(r['id'],{}); source=s['member_source']
    ms=read(source,True) if source else []
    regular=[m['path'] for m in ms if m['type']=='file']
    affected=[]; basis=''
    if a.get('hole')=='2' and r['id'] not in limits:
        affected=regular;basis='Existing generation facts: D1/adjudication/rows.tsv note; D1/adjudication/parts/l2-other.facts.md; D1/adjudication/raw/l2o_member_classes.tsv; member inventory. Confirmation concerns generated-list members, not every member of a mixed row.'
        if r['machine'] in ('d1-alma','d1-void'):affected=tag_members.get(r['id'],[])
        elif r['name'].endswith('/snapshot/etc'):affected=[p for p in regular if p.endswith('/ld.so.cache')]
        elif '/usr/lib/modules/' in r['name']:
            affected=[p for p in regular if '/modules.' in p and not micro_facts.get((r['id'],p),'').startswith('PKG-EQ')]
    if re.fullmatch(r'/var/cache/man(?:/[^/]+)?',r['name']):
        affected=[p for p in regular if p.endswith('/index.db')];basis='Same generated manual-page index family as D1/review/agreed-sample.md; actual index.db member required.'
    if re.fullmatch(r'/boot/grub2?/i386-pc',r['name']):
        affected=[p for p in regular if p.endswith('.lst')];basis='Copied GRUB lists from installed package: D1/adjudication/parts/l2-other.facts.md and D1/adjudication/rows.tsv note (MicroOS); S8.2-16 names built or obtained.'
    if r['name']=='/var/cache/ldconfig':
        affected=[p for p in regular if p.endswith('/aux-cache')];basis='Generated loader cache, same family as original card 2; member inventory establishes data file and persistence.'
    if r['id']=='void-db97bdf74065f7ecf12d337f':
        affected=[p for p in regular if p=='/etc/ld.so.cache'];basis='D1/adjudication/raw/l2o_member_classes.tsv marks this specific member generated from installed packages; other /etc members are not reclassified.'
    if affected:
        extent.append({k:r[k] for k in ('id','machine','kind','name')}|{'matching_members':' | '.join(affected),'member_source':source,'original_hole':a.get('hole',''),'original_verdict':a.get('verdict','agreement'),'status':'CONFIRMED:generated-list','evidence':basis})
    if a.get('hole')=='2':
        st,why=limits.get(r['id'],('CONFIRMED:generated-list',basis))
        original.append({k:r[k] for k in ('id','machine','kind','name')}|{'status':st,'reason':why,'member_source':source})
# Supplemental, evidence-reviewed rows (if any) use the independent bounded note.
supp=Path('D1/fix-d1-h-2/generated/confirmed.tsv')
if supp.exists():
    for x in read(supp):
        if x['id'] not in {e['id'] for e in extent}:
            r=byid[x['id']];a=adj.get(x['id'],{})
            extent.append({k:r[k] for k in ('id','machine','kind','name')}|{'matching_members':x['matching_members'],'member_source':x['member_source'],'original_hole':a.get('hole',''),'original_verdict':a.get('verdict','agreement'),'status':'CONFIRMED:generated-list','evidence':x['evidence']})
write('card2-extent.tsv',extent);write('card2-original-rows.tsv',original)
card2={r['id'] for r in extent};card4={r['id'] for r in read(OUT/'card4-boot-extent.tsv')}
card5={r['id'] for r in read(OUT/'xpi-search.tsv') if r['name'].endswith('/cal-check/extensions')}
write('card5-extent.tsv',[r|{'status':'CONFIRMED:installed-contained-code'} for r in read(OUT/'xpi-search.tsv') if r['id'] in card5])
old=read('D1/fix-d1-h-1/raw/gap-row-dispositions.tsv')
ledger=[]
for r in old:
    r=dict(r); ids=r['id']
    if ids in card2: r.update(fix_status='CONFIRMED:generated-list',reason='Competing S8.2-15/2 and S8.2-16/1 readings; see card2-extent.tsv for affected members.')
    elif ids in card5:r.update(fix_status='CONFIRMED:installed-contained-code',reason='S8.2-1 versus S8.2-21 depends on unresolved archive/content boundary; Q1 does not settle recording obligation.')
    elif ids in limits:r.update(fix_status=limits[ids][0],reason=limits[ids][1])
    ledger.append(r)
write('gap-row-dispositions.tsv',ledger)
# Keep draw order and ids; replace only changed reasoning. No resampling.
sample_counts={}
for sample in ('agreed','resolved'):
    rs=read('D1/review/'+sample+'-sample.tsv')
    changed=[]
    for r in rs:
        if r['id'] in card2:
            r=dict(r);r['check_result']='CANDIDATE:CONFIRMED';r['reason']='Card 2: record under S8.2-15/2 versus installed generated list under S8.2-16/1; no priority supplied between these readings.';r['evidence']+='; D1/fix-d1-h-2/raw/card2-extent.tsv';changed.append(r['id'])
        elif r['id']=='microos-230864c607d1cffde69583f3':
            r=dict(r);r['check_result']='FACT_UNKNOWN';r['reason']='Inactive snapshot database: full contents/source package set not established by prefix hashes; cannot exclude card-2 membership. See generated/assessment.md.';r['evidence']+='; D1/fix-d1-h-2/generated/assessment.md';changed.append(r['id'])
        sample_counts.setdefault(sample,[]).append(r)
    write(sample+'-sample.tsv',sample_counts[sample]);sample_counts[sample]={'changed_ids':changed,'results':dict(Counter(r['check_result'] for r in sample_counts[sample]))}
summary={'searched':len(scan),'card2_rows':len(extent),'card2_by_machine':dict(Counter(r['machine'] for r in extent)),'card2_original_statuses':dict(Counter(r['status'] for r in original)),'card2_outside_original_hole2':sum(r['original_hole']!='2' for r in extent),'card4_boot_rows':len(card4),'card5_rows':len(card5),'exclusive_original_gap_ledger':dict(Counter(r['fix_status'] for r in ledger)),'confirmed_row_union':len(card2|card4|card5),'samples':sample_counts}
assert len(ledger)==len({r['id'] for r in ledger})==1364
assert {r['id'] for r in ledger}=={r['id'] for r in adj.values() if r['verdict']=='GAP'}
with (OUT/'changed-counts.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps(summary,indent=2))
