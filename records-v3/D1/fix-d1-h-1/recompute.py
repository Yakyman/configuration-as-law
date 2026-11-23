"""Recompute only the verification decisions changed in fix round 1. No probes."""
import collections, csv, hashlib, json, random, re
from pathlib import Path
P = Path('D1/fix-d1-h-1')
def read(path, frozen=False):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE if frozen else csv.QUOTE_MINIMAL))
def write(name, rows, fields):
    with (P/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter='\t'); w.writeheader();w.writerows(rows)
J=read('D1/compare/joined.tsv',True); A=read('D1/adjudication/rows.tsv',True)
by={r['id']:r for r in J}; adj={r['id']:r for r in A}
old14={r['id']:r for r in read('D1/review/cards-1-4-extent.tsv')}
old5={r['id']:r for r in read('D1/review/card5-extent.tsv')}
def name(r):return re.sub(r'^(root|user):','',r['name'])
# Revised samples retain every ordered id; no redraw and no new case.
samples={}; changed={}
for label,size,seed,pop in [('resolved',40,2026112201,[r for r in A if r['verdict'].startswith('RESOLVED:')]),('agreed',60,2026112202,[r for r in J if r['id'] not in adj and r['c1_decision']==r['c2_decision']])]:
    records=read('D1/review/'+label+'-sample.tsv')
    assert [r['id'] for r in records]==[r['id'] for r in random.Random(seed).sample(pop,size)]
    out=[]
    for r in records:
        old=r.get('review',r.get('assessment')); card=''; reason='Unchanged; see original row evidence.'
        if old in ('CORRECTED','CANDIDATE:REFUTED'):
            status='CONFIRMED';card='3';reason='Dependency selection versus removal scope is undecided; dependency field alone is not a MUST sentence.'
        elif label=='resolved' and ('x86_64-xen' in r['name'] or r['name']=='/boot/boot' or name(r)=='microcode_ctl'):
            status='CONFIRMED';card='5';reason='Known inactive platform support; text does not select fixed-environment or changed-environment removal scope.'
        else:status={'NOT-ESTABLISHED':'UNKNOWN'}.get(old,old)
        if card:changed[r['id']]=card
        out.append(dict(index=r.get('sample_index',r.get('order')),id=r['id'],machine=r['machine'],kind=r['kind'],name=r['name'],previous=old,status=status,card=card,reason=reason,evidence='D1/review/'+label+'-sample.tsv#'+r['id']+'; D1/fix-d1-h-1/sample-audit.md'))
    write(label+'-sample.tsv',out,list(out[0]));samples[label]=dict(population=len(pop),seed=seed,counts=dict(collections.Counter(r['status'] for r in out)));samples[label]['rows']=out
# Confirmed membership uses established payload facts, never a name match alone.
M={}; exclusions={}; uncertain={}
def put(r,card,reason,source):M[(r['id'],card)]=dict(id=r['id'],machine=r['machine'],kind=r['kind'],name=r['name'],card=card,status='CONFIRMED',reason=reason,evidence=source)
controls={'dmz-cursor-theme','fonts-noto-cjk','wamerican','yaru-theme-icon'}
trust={'gpg-pubkey','ca-certificates-mozilla','libtirpc-common','/etc/ssl'}
for r in J:
    a=adj.get(r['id'],{});h=a.get('hole','');n=name(r)
    if h in ('1','2'):
        if r['machine']=='mint' and n in controls:
            exclusions[(r['id'],h)]='Direct maintainer-script evidence, S2.2-10: D1/review/cards14-raw/mint-'+n+'-control.json'
        elif n in trust:
            exclusions[(r['id'],h)]='Established trust/transport policy function, S2.2-1; original rows.tsv note and cards-1-4.md.'
        elif n=='/etc/udev':uncertain[(r['id'],h)]='Actual mixed hwdb contents not inventoried; retained factual UNKNOWN.'
        else:put(r,h,a['note'],'D1/adjudication/rows.tsv#'+r['id'])
    if h=='3':put(r,'3',a['note'],'D1/adjudication/rows.tsv#'+r['id'])
    if h=='5':put(r,'5',a['note'],'D1/adjudication/rows.tsv#'+r['id'])
    prior=old5.get(r['id'],{})
    if prior.get('reason','').startswith(('Different boot-platform','Existing adjudication')) or r['name']=='/boot/boot':
        put(r,'5','Known boot/firmware support for a different environment; no sentence selects the environment scope.','D1/review/card5-extent.tsv#'+r['id']+'; D1/adjudication/rows.tsv#'+r['id'])
    # Same installed package in root/user collections has the same package-level facts.
    same_sample=[s for s,c in changed.items() if c=='3' and by[s]['machine']==r['machine'] and name(by[s])==n]
    if same_sample:put(r,'3','Nondeciding payload plus established dependency relationship; same installed package as affected sample.','D1/review/'+('agreed' if same_sample[0] not in {x['id'] for x in samples['resolved']['rows']} else 'resolved')+'-sample.tsv#'+same_sample[0])
    # Additional dependency-only packages: both recorded functional accounts support the premise.
    if r['kind'].startswith('L1:package') and 'Metapackage: dependency record' in r['c2_what'] and ('Selects dependencies without' in r['c1_what'] or 'empty-payload dependency target' in r['c1_what']):
        put(r,'3','Both recorded factual accounts identify a dependency-only package with no executable runtime payload.','D1/compare/joined.tsv#'+r['id'])
    # Previously checked extra data-only roles, beyond the original adjudicated cards.
    if (r['machine']=='fedora' and n=='glibc-all-langpacks') or (r['machine']=='mint' and n in {'liblouis-data','libthai-data','libx11-data','libopenal-data'}):
        put(r,'2','Established shared locale/translation/dictionary/rendering values; content versus capability boundary.','D1/compare/joined.tsv#'+r['id']+'; D1/review/cards14-raw/'+n+'.txt' if r['machine']=='mint' else 'D1/compare/joined.tsv#'+r['id'])
# Search the whole table by kind and name; record uncertain additional matches separately.
rx={
 '1':re.compile(r'font|theme|lang|l10n|i18n|wallpaper|artwork|sound|branding|locale|translation',re.I),
 '2':re.compile(r'data|dict|terminfo|ncurses-base|poppler|netconfig|gpg-pubkey|colo[u]?r|zone|database|hwdata|cmap|suffix|locale',re.I),
 '3':re.compile(r'pattern|meta|default-font|langpacks|firmware-all|^grub2$|^dbus|^kernel$|^linux-|^xorg$|^xserver-xorg-|^libvirt-|^qemu-|^passwdqc$',re.I),
 '5':re.compile(r'firmware|ucode|microcode|wireless|wacom|media-player|usb|alsa|hwdata|hwdb|xen|grub|boot|modem',re.I)}
scan=[]
for r in J:
    for h,pattern in rx.items():
        key=(r['id'],h)
        match=bool(pattern.search(r['name'])) and (r['kind'].startswith(('L1:package','L2:')) or h=='5')
        if key not in M and key not in exclusions and key not in uncertain and not match:continue
        if key in M:status='CONFIRMED';reason=M[key]['reason']
        elif key in exclusions:status='EXCLUDED';reason=exclusions[key]
        elif key in uncertain:status='UNRESOLVED_MEMBERSHIP';reason=uncertain[key]
        elif r['id'] in old5 and h=='5' and old5[r['id']]['extent_status']=='EXCLUDED' and not re.search(r'metadata|requirements|requires|recommends|boot-platform|microcode',old5[r['id']]['reason'],re.I):
            status='EXCLUDED';reason=old5[r['id']]['reason']
        else:
            status='UNRESOLVED_MEMBERSHIP';reason='Kind/name match alone does not establish this gap or a deciding independent function; not an object UNKNOWN verdict.'
        scan.append(dict(id=r['id'],machine=r['machine'],kind=r['kind'],name=r['name'],card=h,status=status,reason=reason))
write('extent-search.tsv',scan,list(scan[0]))
rows=list(M.values());write('confirmed-rows.tsv',rows,list(rows[0]))
# Remove metadata-only information gaps; retain actual missing facts and add QML facts.
unknown={r['id']:r for r in read('D1/review/original-unknown.tsv',True)}
for r in samples['resolved']['rows']:
    if r['status']=='UNKNOWN':unknown[r['id']]=dict(source='Resolved sample: missing factual premise.')
unknown['flatcar-776158c873d0ec65315d36b4']=dict(source='Actual mixed hwdb contents not inventoried.')
for r in J:
    if adj.get(r['id'],{}).get('hole')=='7' and name(r) in {'plasma6-theme-openSUSE','plasma6-sddm-theme-openSUSE'}:
        unknown[r['id']]=dict(source='Card 7: actual script authority/confinement not established; metadata MUST withdrawn.')
u=[dict(id=r['id'],machine=r['machine'],kind=r['kind'],name=('[guest account home directory]' if r['id']=='flatcar-e25481968473168cc22e8706' else r['name']),source=unknown[r['id']]['source']) for r in J if r['id'] in unknown]
assert not ({r['id'] for r in rows}&set(unknown))
write('final-unknown.tsv',u,list(u[0]))
# Only outcome column and verification counts change; comparison metrics are frozen.
summary=dict(confirmed_cards=['1','2','3','5'],confirmed_unique_rows=len({r['id'] for r in rows}),
 by_card={h:dict(collections.Counter(r['machine'] for r in rows if r['card']==h)) for h in ('1','2','3','5')},
 confirmed_by_machine=dict(collections.Counter(by[i]['machine'] for i in {r['id'] for r in rows})),
 extent_search=dict(collections.Counter(r['status'] for r in scan)),
 unknown_total=len(u),unknown_by_machine=dict(collections.Counter(r['machine'] for r in u)),unknown_by_kind=dict(collections.Counter(r['kind'] for r in u)),
 samples={k:{a:b for a,b in v.items() if a!='rows'} for k,v in samples.items()},
 outcomes={m:'?' if m=='talos' else '0' for m in ['fedora','tumbleweed','mint','flatcar','talos']})
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
# Input integrity verification covers all frozen material read during this fix.
hashes=json.loads((P/'input-sha256.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in hashes.items())
print('Frozen input hashes unchanged:',len(hashes));print('Ordered samples unchanged; no new inventory/removal probe.')
