#!/usr/bin/env python3
"""Build a lossless row-to-missing-fact index from the specified first-night tables."""
import csv
import pathlib
import argparse
ROOT = pathlib.Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=pathlib.Path, help='New output directory; must not exist')
OUT = parser.parse_args().output
OUT.mkdir(parents=True, exist_ok=False)
rows = []
for name in ('unknown-rows.tsv', 'additional-unknown-rows.tsv'):
    for r in csv.DictReader((ROOT / 'D1/review' / name).open(), delimiter='\t'):
        rows.append({k: r[k] for k in ('id', 'machine', 'kind', 'name', 'missing_facts')})
extra = [('alma-22d9524df6813c1275345f42', 'alma', '/usr/lib/fontconfig/cache'), ('alma-d15f2f63f27850d00f28f708', 'alma', '/home/user/.cache/fontconfig'), ('void-a861eb17053cb23311e16fcf', 'void', '/home/user/.cache/fontconfig'), ('microos-230864c607d1cffde69583f3', 'microos', '/.snapshots/1/snapshot/usr/lib/sysimage/rpm'), ('microos-7cc2a7c5eef50507eed81020', 'microos', '/var/cache/zypp/solv/@System')]
extra += [('void-f2e5d5edfa5902c8aee7bace', 'void', '/etc/ssl/certs'), ('microos-dcce813055fa256ed012c87a', 'microos', '/var/lib/ca-certificates/openssl')]
for ident, machine, name in extra:
    rows.append(dict(id=ident, machine='d1-' + machine, kind='' if ident in {x[0] for x in extra[5:]} else 'L2:stored-outside-packages' if machine == 'microos' else 'L2:stored-ownership-unresolved', name=name, missing_facts='RESULT-only source/content fact'))
facts = []
links = []

def add(machine, key, fact, predicate, why, how):
    selected = [r for r in rows if r['machine'] == 'd1-' + machine and predicate(r)]
    facts.append([machine, key + ': ' + fact, len(selected), why, how])
    links.extend(([r['id'], machine, key] for r in selected))

def pathset(*names):
    return lambda r: r['name'] in names
npm = lambda r: '/node_modules/' in r['name']
store = lambda r: r['kind'] == 'L2:image-container-store'
a_inst = lambda r: r['kind'] in ('L1:saved-network', 'L1:saved-network-file') or r['name'] in ('/boot/grub2', '/boot/loader/entries', '/etc/NetworkManager/system-connections', '/etc/firewalld/zones', '/etc/kernel', '/etc/sysconfig')
add('alma', 'A01', 'npm original acquisition event and receipt records', npm, 'npm lacked a per-file manifest; the retained signature covered at most 4096 bytes', 'npm-archive-sources.tsv records cache references and reference type; no per-object acquisition event record is emitted')
add('alma', 'A02', 'Installer directives and current boot/network/firewall/kernel values', a_inst, 'Installer recipe and relevant current values were not captured', 'alma-facts.tsv current-content and installer-directives; saved-network credentials excluded')
add('alma', 'A03', 'Actual installer choice versus default or later change', a_inst, 'No chooser-linked creation/change event was recorded', 'alma-facts.tsv retains installer directives, bounded journal/audit extracts and scriptlets; no complete per-object choice/change event table is emitted')
add('alma', 'A04', 'Unit disablement history', lambda r: r['kind'] == 'L1:unit-file', 'No enablement-link history was retained', 'alma-facts.tsv retains current unit/preset and bounded operation extracts; no original disablement-event record is emitted')
add('alma', 'A05', 'Inner store member metadata', store, 'Engine and application stores were opaque', 'store-members.tsv and store-coverage.tsv; bounded inner traversal, nested boundaries explicit')
add('alma', 'A06', 'Complete store payload membership, receipt integrity and creator', store, 'Opaque storage did not provide per-member package or creator records', 'Inner metadata and prefix signatures recorded; no complete payload receipt or per-member creation-event table is emitted')
add('alma', 'A07', 'RPM key acquisition reason', lambda r: r['kind'] == 'L1:package', 'RPM key import had no explicit/dependency reason in the inventory', 'alma-facts.tsv records RPM key metadata and DNF history; no per-key import-reason field is emitted')
add('alma', 'A08', 'ALSA stored values', pathset('/etc/alsa'), 'File contents were not collected', 'alma-facts.tsv current-content')
add('alma', 'A09', 'ALSA value creator', pathset('/etc/alsa'), 'No reliable creation record', 'alma-facts.tsv current contents and bounded history extracts; no per-value creation-event record is emitted')
add('alma', 'A10', 'Persistent SELinux boolean values', pathset('/var/lib/selinux/targeted/active'), 'Boolean content/source was not retained', 'alma-facts.tsv s4-persistent-selinux-values, native read-only semanage query')
add('alma', 'A11', 'Persistent SELinux boolean chooser', pathset('/var/lib/selinux/targeted/active'), 'No chooser-linked event was recorded', 'alma-facts.tsv values, scriptlets and bounded history extracts; no per-value chooser-event record is emitted')
add('alma', 'A12', 'Compiled dconf values', pathset('/etc/dconf/db'), 'Binary database had no decoded values', 'alma-facts.tsv compiled-values; isolated dconf profile reads each existing system database')
add('alma', 'A13', 'dconf key meaning and actual consumers', pathset('/etc/dconf/db'), 'Neither decoded key meaning nor consumers were captured', 'Schemas, profiles and bounded current mapped-reader snapshot; no complete consumer history is emitted')
add('alma', 'A15', 'npm complete member equality to a verified reference archive', npm, 'No complete file/archive comparison was retained', 'npm-member-integrity.tsv complete byte/target comparisons against verified cache-reference archives; reference type retained separately')
add('alma', 'A14', 'Font cache source directories and font package provenance', lambda r: r['id'] in {x[0] for x in extra[:2]}, 'RESULT-only two caches retained metadata/prefixes, not decoded sources', 'font-cache-sources.tsv fc-cat decoding and font-source-packages.tsv package-file joins; 2 RESULT-only IDs, 0 IDs in fixed matching inputs')
add('void', 'V01', 'npm member receipt and full equality', npm, 'npm had no per-file unchanged-receipt evidence', 'npm-archive-sources.tsv and npm-member-integrity.tsv retain lock references, verified cached archives and complete member comparisons')
old = lambda r: 'Original old-package provenance' in r['missing_facts']
add('void', 'V02', 'Retained old-version package member origin and full receipt integrity', old, 'Current installed package manifest omitted retained old-kernel members', 'old-package-receipt-sources.tsv and old-package-member-integrity.tsv query installed, residual and cached manifests; missing references carry no-surviving-receipt')
add('void', 'V03', 'Account shell, memberships and sudo-rule creation history', lambda r: r['kind'] in ('L1:account', 'L1:group', 'L1:sudo-access', 'L1:access-rule'), 'No installation-default or later-choice event was recorded', 'Current account/group/sudo sources and package records; no per-object installation/choice event table is emitted')
add('void', 'V04', 'Inner store member metadata', lambda r: store(r) or r['name'] == '/home/user/.local/share', 'Three opaque stores and their parent lacked member inventories', 'store-members.tsv and store-coverage.tsv; parent joins to child store path')
add('void', 'V05', 'Complete store payload membership, receipt integrity and creator', lambda r: store(r) or r['name'] == '/home/user/.local/share', 'No complete inner payload/creator record', 'Bounded inner metadata and prefixes; no complete payload receipt or per-member creation-event table is emitted')
vconfig = pathset('/etc/default', '/etc/modules-load.d', '/etc/sudoers.d', '/var/db/xbps/keys')
add('void', 'V06', 'Stored configuration contents and whole-file hashes', vconfig, 'Values were not captured and longer files had only prefix signatures', 'void-configuration-facts.tsv selected file bytes and full-digests.tsv whole-file hashes')
add('void', 'V07', 'Stored configuration, trust-key and mount-entry creator', lambda r: vconfig(r) or r['name'] == '/mnt', 'No trustworthy creator/choice record was captured', 'Current configuration, key and mount records; historical_creator has an unknown marker, no creation event is emitted')
add('void', 'V08', 'Font cache source and installed-font provenance', lambda r: r['id'] == extra[2][0], 'RESULT-only cache lacked decoded sources', 'font-cache-sources.tsv, font-source-packages.tsv and package-files.tsv; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
add('microos', 'M01', 'Account/group creation source and event', lambda r: r['kind'] in ('L1:account', 'L1:group'), 'Creator/package-default event was unrecorded', 'Sysusers source files and RPM scriptlets; no per-account/group creation-event table is emitted')
add('microos', 'M02', 'Active unit definitions, overrides and enablement links', lambda r: r['kind'] in ('L1:unit-file', 'L1:user-unit-file'), 'Active /etc was pruned as a snapshot; basenames did not identify selected sources', 's4-microos-unit-selected.tsv, s4-microos-unit-links.tsv, s4-microos-sources.tsv and active /etc traversal')
add('microos', 'M03', 'Unit enablement actor/default history', lambda r: r['kind'] in ('L1:unit-file', 'L1:user-unit-file') and 'provenance' in r['missing_facts'], 'No creation event for seven alias/enablement links', 'Current links and package script text; no per-link enablement-event table is emitted')
add('microos', 'M04', 'Sudo supplying files and contents/integrity', lambda r: r['kind'] == 'L1:sudo-access', 'Active /etc and packaged /usr/etc source content were absent', 's4-microos-sources.tsv source bytes plus package-files.tsv; 8 dependent IDs, 7 duplicate-key IDs, at most 1 structurally matchable ID')
add('microos', 'M05', 'Sudo installation default versus later choice', lambda r: r['kind'] == 'L1:sudo-access' and 'provenance' in r['missing_facts'], 'No default-selection or later-choice event was recorded', 'Current source bytes and package-file comparisons; no per-rule choice-event table; 7 dependent IDs, 6 duplicate-key IDs, at most 1 structurally matchable ID')
add('microos', 'M06', 'Active /etc subvolume contents', lambda r: r['kind'] == 'L2:snapshot', 'Traversal stopped on active subvolume snapshot marker', 'objects/member tables traverse /etc while retaining expanded snapshot marker; full-digests.tsv and source sidecars')
snapshot = lambda r: r['name'].startswith('/.snapshots/') and r['id'] != extra[3][0]
add('microos', 'M07', 'Snapshot-root package membership and full package-file comparison', snapshot, 'No snapshot-root manifest or complete snapshot-file comparison was recorded', 's4-microos-snapshot-files.tsv snapshot RPM manifests and full hashes; absent manifest rows and unknown comparisons remain explicit')
add('microos', 'M08', 'Snapshot/current whole-file equality beyond digest prefix', snapshot, 'Only prefix equality was retained for long snapshot copies', 'full-digests.tsv and s4-microos-snapshot-current.tsv complete SHA256 pairs')
add('microos', 'M09', 'SELinux CIL/HLL copy derivation and original receipt records', lambda r: snapshot(r) and '/selinux/targeted/active/modules/' in r['name'], 'SELinux CIL/HLL copies lacked original package/derivation records', 'semodule format/checksum listings and full snapshot/current comparisons; no original per-copy receipt or derivation-event record is emitted')
add('microos', 'M10', 'Boot environment values', pathset('/boot/grub2'), 'grubenv content was not captured', 's4-microos-sources.tsv bounded complete bytes of grubenv')
add('microos', 'M11', 'Boot environment creator/chooser', pathset('/boot/grub2'), 'No event linked boot values to a person or program', 'Current grubenv bytes; no per-value creation/choice event table is emitted')
add('microos', 'M12', 'Inactive snapshot RPM database contents and package set', lambda r: r['id'] == extra[3][0], 'RESULT-only candidate lacked snapshot-root package inventory/full database equality', 'Snapshot-root RPM query, s4-microos-snapshot-files.tsv and full snapshot/current SHA256 pairs; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
add('microos', 'M13', 'System solver cache source package set', lambda r: r['id'] == extra[4][0], 'RESULT-only cache source/content was not decoded', 's4-microos-solver-cache.tsv bounded dumpsolv decoding, cookie/source bytes and full SHA256; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
add('talos', 'T01', 'Container image acquisition actor and recorded derivation', lambda r: r['kind'] == 'L1:container-image', 'Image list did not capture who obtained each image or its acquisition source', 'talos-image-sources.tsv current StaticPod image references; no historical pull-actor record is emitted')
opaque = lambda r: r['kind'] == 'L2:opaque-directory'
add('talos', 'T02', 'Unexpanded directory contents beyond original listing bounds', opaque, '64 directories, depth4 and4096 members plus opaque exclusions prevented enumeration', 'talos-expanded-members.tsv and talos-listing-coverage.tsv bounded API listings; proc/sys/dev component boundaries explicit')
stored = lambda r: r['kind'] in ('L2:stored-ownership-unknown', 'L2:code-ownership-unknown', 'L2:opaque-directory')
add('talos', 'T03', 'Original image membership and complete receipt integrity', stored, 'No complete original image manifest or overlay receipt comparison', 'Current listing, hashes and mount tables; no original installed-image member manifest or receipt comparison is emitted')
add('talos', 'T06', 'Complete exposed target file hashes and signatures', lambda r: stored(r) and r['name'].startswith(('/etc', '/opt', '/var/system', '/var/lib/containerd', '/var/lib/kubelet', '/var/log/containers')), 'The API listing retained no file contents or full hashes', 'talos-content.tsv and talos-content-attempts.tsv bounded Read, Copy and fresh-metadata Read hashes/signatures; per-file failures explicit')
add('talos', 'T04', 'Per-object backing, writable overlay origin and persistence', lambda r: stored(r) and any((w in r['missing_facts'].lower() for w in ('backing', 'overlay', 'upper', 'persistent', 'persistence', 'transient'))), 'No complete object-to-covering-mount map; /etc and /opt sources ambiguous', 'talos-mountinfo.tsv exact bounded API-daemon mount namespace; no per-object historical overlay-layer record is emitted')
add('talos', 'T05', 'Stored member creator and derivation history', lambda r: stored(r) and any((w in r['missing_facts'].lower() for w in ('creator', 'creation', 'provenance', 'derivation', 'who', 'person', 'generated', 'written', 'placed'))), 'No per-member creation or derivation event was retained', 'Current listing, content hashes and source references; no per-member creation/derivation-event record is emitted')
add('gentoo', 'G01', 'First two-level inventory after the committed actions', lambda r: False, 'First-night startup failed before any object was observed', 'Fresh four-slot boot and two inventory levels recorded; browser_extension and container_run each exited 1, so the full prescribed action sequence did not succeed; 0 first-night IDs')

add('void','V09','Trust-value choice events and actual consumer/use records',lambda r:r['id']==extra[5][0],
    'D1/RESULT.md Card 2 explicitly leaves the trust-value facts unrecorded',
    'No per-value historical choice or complete consumer/use record is emitted; current metadata/digests may be present, but those named records have no collection route; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
add('microos','M14','Trust-value choice events and actual consumer/use records',lambda r:r['id']==extra[6][0],
    'D1/RESULT.md Card 2 explicitly leaves the trust-value facts unrecorded',
    'No per-value historical choice or complete consumer/use record is emitted; current metadata/digests may be present, but those named records have no collection route; 1 RESULT-only ID, 0 IDs in fixed matching inputs')

covered = {r[0] for r in links}
assert {r['id'] for r in rows} == covered, sorted({r['id'] for r in rows} - covered)

def write(path, header, body):
    with path.open('w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(header)
        w.writerows(body)
facts.sort(key=lambda r: (['alma', 'void', 'microos', 'talos', 'gentoo'].index(r[0]), r[1].split(':')[0]))
write(OUT / 'MISSING.tsv', ['machine', 'fact', 'objects', 'why_not_recorded', 'how_recorded_now'], facts)
write(OUT / 'missing-row-map.tsv', ['first_id', 'machine', 'fact_id'], sorted(links))
print('facts=' + str(len(facts)) + ' original_rows=2007 result_only_rows=7 unique_rows=' + str(len(covered)))
