"""Recompute only H1 membership and affected audits from frozen review inputs."""
import csv, collections, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'A1/fix-a1-h-1'
def read(path):
    with (ROOT/path).open() as f: return list(csv.DictReader(f,delimiter='\t'))
def write(name,rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def counts(rows,key):return dict(sorted(collections.Counter(r[key] for r in rows).items()))
joined=read('A1/compare/joined.tsv'); byid={r['id']:r for r in joined}
adj={r['id']:r for r in read('A1/adjudication/rows.tsv')}
old=read('A1/review/hole-1-extent.tsv'); revised=[]; checks=[]; changes=[]
notes='A1/fix-a1-h-1/unit-boundaries.md'
for prev in old:
    r=dict(prev); id=r['id']; j=byid[id]; original=r['extent_status']
    unit=original.startswith('CONFIRMED') and (r['kind'] in ('system-unit','user-unit') or (r['kind']=='system-closure-store-object' and '-unit-' in r['name']))
    if unit:
        inventory=r['kind'] in ('system-unit','user-unit')
        unitname=r['name'] if inventory else r['name'].split('-unit-',1)[1]
        machine=id.split('-',1)[0]
        if id.startswith('debian-desktop-'):machine='debian-desktop'
        files=(['unit-files.txt','unit-realpaths.tsv','unit-paths.txt'] if r['kind']=='system-unit' else ['user-list-unit-files.txt','user-unit-paths.txt'] if r['kind']=='user-unit' else ['unit-realpaths.tsv'])
        hits=[]; disabled_evidence=[]
        for name in files:
            p=ROOT/'A1/in/raw'/machine/name
            if p.exists():
                for n,line in enumerate(p.read_text().splitlines(),1):
                    # Exact unit basename; do not confuse an instantiated unit with its template.
                    if line.split() and (line.split()[0]==unitname or any(x.rstrip('/').split('/')[-1]==unitname for x in line.split())):
                        hits.append(f'{p.relative_to(ROOT)}:{n}: {line}')
                        if name in ('unit-files.txt','user-list-unit-files.txt') and len(line.split())>1 and line.split()[0]==unitname and line.split()[1]=='disabled':
                            disabled_evidence.append(f'{p.relative_to(ROOT)}:{n}')
        status='READING-DEPENDENT' if inventory else 'FACTUAL-UNKNOWN'
        why=('The inventory object is a managed unit; replacing it by its fragment file chooses an unstated object reading. That reading remains unresolved, not refuted. ' if inventory else 'Stored unit configuration remains a candidate. ')
        why+='Available row/fragment and unit-file-state evidence does not establish the exact file section contents and all applying programs. [Install] can be applied by systemctl; no claim that every file has operative [Install] values. No confirmed single-program premise.'
        if disabled_evidence:
            why='The inventory object is a managed unit, not silently substituted by its fragment file. Under the hypothetical file reading, saved disabled state establishes [Install] instructions applied by systemctl in addition to runtime manager values; that file reading is EXCLUDED-MULTIPLE-READERS, not a confirmed H1 example. Actual inventory-object reading remains unresolved. Evidence: '+', '.join(disabled_evidence)+'.'
        r.update(extent_status=status,qualification=why,evidence=prev['evidence']+'; '+notes)
        checks.append({'id':id,'kind':r['kind'],'name':r['name'],'row_evidence':j['evidence'],'available_inventory_matches':' | '.join(hits) or 'No exact matching saved unit-file/path line; joined-row evidence only.','second_applier':('ESTABLISHED under file reading: disabled state entails installation instructions for systemctl; file reading EXCLUDED-MULTIPLE-READERS' if disabled_evidence else 'UNESTABLISHED: neither presence nor absence established for the exact file'),'membership':status})
    if id in ('nixos-ee908f90c5','nixos-b9f001fe55'):
        r.update(extent_status='FACTUAL-UNKNOWN',qualification='Aggregate of native unit files; no constituent with an established single-program premise remains demonstrated by the former unit-only rationale.',evidence=prev['evidence']+'; '+notes)
    if original.startswith('CONFIRMED') and r['name']=='/etc/systemd':
        if id in ('nixos-b86fee9a16','arch-b86fee9a16'):
            r['qualification']=('Confirmed only for the separately identified non-unit settings: journald/logind configuration and generator environment.' if id.startswith('nixos-') else 'Confirmed only for the identified 80-dhcp.network configuration consumed by systemd-networkd.')+' Enablement links and unit-file members do not contribute to the confirmed count; their single-program premise remains unresolved.'
        else:
            r.update(extent_status='FACTUAL-UNKNOWN',qualification='Former confirmation depended on enablement links/unit configuration. systemctl creates links and the manager follows them; creation alone does not prove a second applier of the same value. Exact one-program premise and alternative qualifying constituents are not established. Retain candidate, not confirmed or refuted.')
        r['evidence']=prev['evidence']+'; '+notes
    if id in ('nixos-4d1b734b98','nixos-2009ac3ba5','nixos-8d44cbf2f9','nixos-7ab5b73f41','coreos-29d771e7fa'):
        source='A1/in/raw/coreos/packages.tsv:397 (procps-ng 4.0.6-1.fc44)' if id.startswith('coreos-') else 'A1/in/raw/nixos/system-closure.txt:142 (procps 4.0.6)'
        r['evidence']=source+'; https://man7.org/linux/man-pages/man8/sysctl.8.html; '+j['evidence']
    if r != prev:
        changes.append({'id':id,'kind':r['kind'],'name':r['name'],'before':original,'after':r['extent_status'],'reason':r['qualification'],'evidence':r['evidence']})
    revised.append(r)
write('hole-1-extent.tsv',revised);write('unit-file-reader-check.tsv',checks);write('changes.tsv',changes)
newby={r['id']:r for r in revised}
scan=read('A1/review/hole-1-scan.tsv')
for r in scan:
    if r['id'] in newby:r['scope_disposition']=newby[r['id']]['extent_status']+'; see A1/fix-a1-h-1/hole-1-extent.tsv'
write('hole-1-scan.tsv',scan)
agreed=read('A1/review/agreed-audit.tsv')
for r in agreed:
    if r['judgment']=='CONFIRMED:H1' and not newby[r['id']]['extent_status'].startswith('CONFIRMED'):
        new=newby[r['id']];r['judgment']=new['extent_status'];r['review_reason']=new['qualification'];r['evidence']+='; '+notes
        # A reading question is not a factual ? under S3-2.
        if new['extent_status']=='FACTUAL-UNKNOWN':
            r['deciding_sentences']='S3-2';r['exact_quotes']='If what the object does remains unknown, the case yields ?.'
write('agreed-audit.tsv',agreed)
resolved=read('A1/review/resolved-audit.tsv')
for r in resolved:
    if r['id']=='coreos-4d2a7c7537':
        r.update(review_status='FACTUAL-UNKNOWN',review_decision='UNKNOWN',deciding_sentences='S3-2',review_note=newby[r['id']]['qualification'],evidence=r['evidence']+'; '+notes)
write('resolved-audit.tsv',resolved)
confirmed=[r for r in revised if r['extent_status'].startswith('CONFIRMED')]
anchors=[r for r in revised if adj.get(r['id'],{}).get('hole')=='1']
summary={'h1_status':counts(revised,'extent_status'),'h1_confirmed_by_kind':counts(confirmed,'kind'),'h1_confirmed_total':len(confirmed),'original_card_1_status':counts(anchors,'extent_status'),'agreed_judgments':counts(agreed,'judgment'),'resolved_status':counts(resolved,'review_status'),'resolved_quote_support':counts(resolved,'quote_support'),'unit_rows_checked':len(checks),'unit_file_reading_second_applier_established':sum(r['second_applier'].startswith('ESTABLISHED') for r in checks),'membership_changes':sum(r['before']!=r['after'] for r in changes),'all_changed_records':len(changes),'whole_table_rows':len(scan)}
assert len(scan)==5200 and len(checks)==598
assert len(agreed)==60 and len(resolved)==40
assert [r['id'] for r in agreed]==[r['id'] for r in read('A1/review/agreed-audit.tsv')]
assert [r['id'] for r in resolved]==[r['id'] for r in read('A1/review/resolved-audit.tsv')]
assert len(confirmed)==114
(OUT/'counts.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
