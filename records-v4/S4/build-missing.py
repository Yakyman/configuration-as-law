#!/usr/bin/env python3
"""Build a lossless row-to-missing-fact index from the specified first-night tables."""
import csv
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
rows=[]
for name in ('unknown-rows.tsv','additional-unknown-rows.tsv'):
    for r in csv.DictReader((ROOT/'D1/review'/name).open(),delimiter='\t'):
        rows.append({k:r[k] for k in ('id','machine','kind','name','missing_facts')})
extra=[('alma-22d9524df6813c1275345f42','alma','/usr/lib/fontconfig/cache'),
       ('alma-d15f2f63f27850d00f28f708','alma','/home/user/.cache/fontconfig'),
       ('void-a861eb17053cb23311e16fcf','void','/home/user/.cache/fontconfig'),
       ('microos-230864c607d1cffde69583f3','microos','/.snapshots/1/snapshot/usr/lib/sysimage/rpm'),
       ('microos-7cc2a7c5eef50507eed81020','microos','/var/cache/zypp/solv/@System')]
for ident,machine,name in extra:
    rows.append(dict(id=ident,machine='d1-'+machine,kind='L2:stored-outside-packages' if machine=='microos' else 'L2:stored-ownership-unresolved',name=name,missing_facts='RESULT-only source/content fact'))
facts=[];links=[]
def add(machine,key,fact,predicate,why,how):
    selected=[r for r in rows if r['machine']=='d1-'+machine and predicate(r)]
    facts.append([machine,key+': '+fact,len(selected),why,how])
    links.extend([r['id'],machine,key] for r in selected)
def pathset(*names):return lambda r:r['name'] in names
npm=lambda r:'/node_modules/' in r['name']
store=lambda r:r['kind']=='L2:image-container-store'
a_inst=lambda r:r['kind'] in ('L1:saved-network','L1:saved-network-file') or r['name'] in ('/boot/grub2','/boot/loader/entries','/etc/NetworkManager/system-connections','/etc/firewalld/zones','/etc/kernel','/etc/sysconfig')
add('alma','A01','npm original acquisition and receipt provenance',npm,'npm lacked a per-file manifest; the retained signature covered at most 4096 bytes','PARTIAL: npm-archive-sources.tsv distinguishes cache-identity reference from installation receipt; verified current equality is A15, original acquisition remains unrecorded')
add('alma','A02','Installer directives and current boot/network/firewall/kernel values',a_inst,'Installer recipe and relevant current values were not captured','alma-facts.tsv current-content and installer-directives; saved-network credentials excluded')
add('alma','A03','Actual installer choice versus default or later change',a_inst,'No causal creation/change record established the chooser','NOT OBTAINABLE from present values alone; installer directives, restricted journal/audit and package scripts are supporting evidence, not proof of the event')
add('alma','A04','Unit disablement history',lambda r:r['kind']=='L1:unit-file','No enablement-link history was retained','NOT OBTAINABLE without a retained causal event; current unit/preset and bounded retained-history queries in alma-facts.tsv')
add('alma','A05','Inner store member metadata',store,'Engine and application stores were opaque','store-members.tsv and store-coverage.tsv; bounded inner traversal, with nested opaque boundaries explicit')
add('alma','A06','Complete store payload membership, receipt integrity and creator',store,'Opaque storage did not provide per-member package or creator records','PARTIAL: inner metadata and signatures recorded; archive/image payload identity and historical origin are not established by listing')
add('alma','A07','RPM key acquisition reason',lambda r:r['kind']=='L1:package','RPM key import had no explicit/dependency reason in the inventory','NOT OBTAINABLE without the import event; RPM key metadata and DNF history are recorded, no reason inferred from presence')
add('alma','A08','ALSA stored values',pathset('/etc/alsa'),'File contents were not collected','alma-facts.tsv current-content')
add('alma','A09','ALSA value creator',pathset('/etc/alsa'),'No reliable creation record','NOT OBTAINABLE from current content or timestamps alone; bounded retained-history routes preserve any evidence')
add('alma','A10','Persistent SELinux boolean values',pathset('/var/lib/selinux/targeted/active'),'Boolean content/source was not retained','alma-facts.tsv s4-persistent-selinux-values, native read-only semanage query')
add('alma','A11','Persistent SELinux boolean chooser',pathset('/var/lib/selinux/targeted/active'),'No event establishes who chose the values','NOT OBTAINABLE without a retained causal event; native values, scriptlets and restricted history stay separate')
add('alma','A12','Compiled dconf values',pathset('/etc/dconf/db'),'Binary database had no decoded values','alma-facts.tsv compiled-values; isolated dconf profile reads each existing system database')
add('alma','A13','dconf key meaning and actual consumers',pathset('/etc/dconf/db'),'Neither decoded key meaning nor consumers were captured','PARTIAL: schemas, profiles and current mapped readers; a point-in-time snapshot cannot establish every historical or possible consumer')
add('alma','A15','npm complete member equality to a verified reference archive',npm,'No complete file/archive comparison was retained','npm-member-integrity.tsv records complete byte/target equality to a cryptographically verified cache reference; cache-only references do not establish installation receipt')
add('alma','A14','Font cache source directories and font package provenance',lambda r:r['id'] in {x[0] for x in extra[:2]},'RESULT-only two caches retained metadata/prefixes, not decoded sources','font-cache-sources.tsv raw fc-cat decoding and font-source-packages.tsv join to package IDs and package-files.tsv')
add('void','V01','npm member receipt and full equality',npm,'npm had no per-file unchanged-receipt evidence','npm-archive-sources.tsv and npm-member-integrity.tsv verify lock-addressed cached archive and complete installed file digests')
old=lambda r:'Original old-package provenance' in r['missing_facts']
add('void','V02','Retained old-version package member origin and full receipt integrity',old,'Current installed package manifest omitted retained old-kernel members','old-package-receipt-sources.tsv and old-package-member-integrity.tsv: installed, residual and cached package receipts; NOT OBTAINABLE for members with no surviving old receipt')
add('void','V03','Account shell, memberships and sudo-rule creation history',lambda r:r['kind'] in ('L1:account','L1:group','L1:sudo-access','L1:access-rule'),'Current values do not establish installer default versus later choice','NOT OBTAINABLE from present state; current source contents and surviving package records do not prove the actor or installation event')
add('void','V04','Inner store member metadata',lambda r:store(r) or r['name']=='/home/user/.local/share','Three opaque stores and their parent lacked member inventories','store-members.tsv and store-coverage.tsv; parent joins to child store path')
add('void','V05','Complete store payload membership, receipt integrity and creator',lambda r:store(r) or r['name']=='/home/user/.local/share','No complete inner payload/creator record','PARTIAL: bounded metadata listing; neither nested opaque payloads nor original acquisition established by listing')
vconfig=pathset('/etc/default','/etc/modules-load.d','/etc/sudoers.d','/var/db/xbps/keys')
add('void','V06','Stored configuration contents and whole-file hashes',vconfig,'Values were not captured and longer files had only prefix signatures','void-configuration-facts.tsv and full-digests.tsv; current receipt equality stays separate from historical choice')
add('void','V07','Stored configuration, trust-key and mount-entry creator',lambda r:vconfig(r) or r['name']=='/mnt','No trustworthy creator/choice record was captured','NOT OBTAINABLE from current contents, directory names or timestamps; missing retained causal event')
add('void','V08','Font cache source and installed-font provenance',lambda r:r['id']==extra[2][0],'RESULT-only cache lacked decoded sources','font-cache-sources.tsv, font-source-packages.tsv and package-files.tsv')
add('microos','M01','Account/group creation source and event',lambda r:r['kind'] in ('L1:account','L1:group'),'Creator/package-default event was unrecorded','PARTIAL: sysusers source files and RPM scriptlets; NOT OBTAINABLE historical event without retained causal evidence')
add('microos','M02','Active unit definitions, overrides and enablement links',lambda r:r['kind'] in ('L1:unit-file','L1:user-unit-file'),'Active /etc was pruned as a snapshot; basenames did not identify selected sources','s4-microos-unit-selected.tsv, s4-microos-unit-links.tsv, s4-microos-sources.tsv and active /etc traversal')
add('microos','M03','Unit enablement actor/default history',lambda r:r['kind'] in ('L1:unit-file','L1:user-unit-file') and 'provenance' in r['missing_facts'],'No creation event for seven alias/enablement settings','NOT OBTAINABLE from current links or package script text alone; stored sources do not prove execution')
add('microos','M04','Sudo supplying files and contents/integrity',lambda r:r['kind']=='L1:sudo-access','Active /etc and packaged /usr/etc source content were absent','s4-microos-sources.tsv plus package-files.tsv; full source content retained for per-line attribution')
add('microos','M05','Sudo installation default versus later choice',lambda r:r['kind']=='L1:sudo-access' and 'provenance' in r['missing_facts'],'No causal event established default versus later choice','NOT OBTAINABLE solely from current packaged-file equality and source text')
add('microos','M06','Active /etc subvolume contents',lambda r:r['kind']=='L2:snapshot','Traversal stopped on active subvolume snapshot marker','objects/member tables now traverse /etc while retaining expanded snapshot marker; full-digests.tsv and source sidecars')
snapshot=lambda r:r['name'].startswith('/.snapshots/') and r['id']!=extra[3][0]
add('microos','M07','Snapshot-root package membership and full package-file comparison',snapshot,'Current-root ownership and 4096-byte prefix equality did not establish snapshot-specific receipt','s4-microos-snapshot-files.tsv queries snapshot RPM database and full hashes; records without a snapshot receipt stay unknown')
add('microos','M08','Snapshot/current whole-file equality beyond digest prefix',snapshot,'Only prefix equality was retained for long snapshot copies','full-digests.tsv and s4-microos-snapshot-current.tsv full SHA256 pairs; equality is not receipt provenance')
add('microos','M09','Generated SELinux CIL/HLL derivation and original receipt',lambda r:snapshot(r) and '/selinux/targeted/active/modules/' in r['name'],'Generated representation lacked a full original package/derivation record','PARTIAL: semodule format/checksum and full snapshot/current comparison; absent original generated receipt cannot be reconstructed from equality')
add('microos','M10','Boot environment values',pathset('/boot/grub2'),'grubenv content was not captured','s4-microos-sources.tsv bounded complete bytes of grubenv')
add('microos','M11','Boot environment creator/chooser',pathset('/boot/grub2'),'No event linked boot values to a person or program','NOT OBTAINABLE from current values alone')
add('microos','M12','Inactive snapshot RPM database contents and package set',lambda r:r['id']==extra[3][0],'RESULT-only candidate lacked snapshot-root package inventory/full database equality','Snapshot-root RPM query, s4-microos-snapshot-files.tsv and full snapshot/current SHA256 pairs')
add('microos','M13','System solver cache source package set',lambda r:r['id']==extra[4][0],'RESULT-only cache source/content was not decoded','s4-microos-solver-cache.tsv: read-only dumpsolv plus cookie/source bytes and full SHA256; unavailable decoder stays unknown')
add('talos','T01','Container image acquisition actor and recorded derivation',lambda r:r['kind']=='L1:container-image','Image list did not capture who obtained each image or its acquisition source','talos-image-sources.tsv retains current StaticPod image references; NOT OBTAINABLE historical pull actor from current presence/configuration alone')
opaque=lambda r:r['kind']=='L2:opaque-directory'
add('talos','T02','Unexpanded directory contents beyond original listing bounds',opaque,'64 directories, depth4 and4096 members plus opaque exclusions prevented enumeration','PARTIAL: talos-expanded-members.tsv and talos-listing-coverage.tsv target the documented API; conservative proc/sys/dev component boundaries remain explicit after three listing methods')
stored=lambda r:r['kind'] in ('L2:stored-ownership-unknown','L2:code-ownership-unknown','L2:opaque-directory')
add('talos','T03','Original image membership and complete receipt integrity',stored,'No complete original image manifest or overlay receipt comparison','NOT OBTAINABLE original image receipt from API listing/hash alone; no complete original manifest is exposed, readonly backing is not unchanged receipt')
add('talos','T06','Complete exposed target file hashes and signatures',lambda r:stored(r) and r['name'].startswith(('/etc','/opt','/var/system','/var/lib/containerd','/var/lib/kubelet','/var/log/containers')),'The API listing retained no file contents or full hashes','PARTIAL: talos-content.tsv and talos-content-attempts.tsv retain bounded Read, Copy and fresh-metadata Read hashes/signatures; absent/unstable paths remain explicit after three methods; no installation receipt inferred')
add('talos','T04','Per-object backing, writable overlay origin and persistence',lambda r:stored(r) and any(w in r['missing_facts'].lower() for w in ('backing','overlay','upper','persistent','persistence','transient')),'No complete object-to-covering-mount map; /etc and /opt sources ambiguous','talos-mountinfo.tsv records exact bounded API-daemon mount namespace; joins and namespace/overlay limitations documented, no historical layer attribution inferred')
add('talos','T05','Stored member creator and derivation history',lambda r:stored(r) and any(w in r['missing_facts'].lower() for w in ('creator','creation','provenance','derivation','who','person','generated','written','placed')),'No causal creation record distinguishes original image, generated or later-written members','NOT OBTAINABLE from current listing alone; original event may have no retained API record')
add('gentoo','G01','First two-level inventory after the committed actions',lambda r:False,'First-night startup failed before any object was observed','Fresh four-slot boot, unchanged actions and extended collector rehearsal; zero first-night rows, no invented object count')
covered={r[0] for r in links}
assert {r['id'] for r in rows}==covered,sorted({r['id'] for r in rows}-covered)
def write(path,header,body):
    with path.open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(header);w.writerows(body)
facts.sort(key=lambda r: (['alma','void','microos','talos','gentoo'].index(r[0]), r[1].split(':')[0]))
write(ROOT/'S4/MISSING.tsv',['machine','fact','objects','why_not_recorded','how_recorded_now'],facts)
write(ROOT/'S4/missing-row-map.tsv',['first_id','machine','fact_id'],sorted(links))
print('facts='+str(len(facts))+' original_rows=2007 result_only_rows=5 unique_rows='+str(len(covered)))
