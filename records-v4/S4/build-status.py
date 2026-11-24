#!/usr/bin/env python3
"""Render grouped instrument status; no object decisions are read or written."""
import csv
from pathlib import Path
R=Path(__file__).resolve().parent
recorded={'A02','A05','A08','A10','A12','A14','A15','V01','V04','V06','V08','M02','M04','M06','M08','M10','M12','M13','G01'}
partial={'A01','A06','A13','V05','M01','M07','M09','T01','T02','T04','T06'}
notes={
'A01':'41 cache-identity references verify bytes, but no original acquisition or installation receipt is thereby established.',
'A02':'Current content and sanitized installer/network directives are retained; they do not establish the chooser.',
'A03':'Three retained-evidence routes (recipe, operation history, package scriptlets) do not establish the complete creation/change event.',
'A04':'Current unit/preset evidence and retained operations do not establish the original disablement event.',
'A05':'All three inner-store scans completed with zero nested atomic boundaries; metadata and prefixes are recorded.',
'A06':'Inner metadata/prefixes are available; complete payload receipt and creator history are not established.',
'A07':'Current key metadata/DNF history is available; no explicit/dependency import cause is established.',
'A08':'Selected stored ALSA contents are retained in alma-facts.tsv.',
'A09':'Stored values and retained history do not establish their creator.',
'A10':'Read-only semanage query records persistent values.',
'A11':'The value query and retained script/history evidence do not establish who selected it.',
'A12':'Five isolated dconf database reads succeeded.',
'A13':'Schemas/profiles and current mapped readers are captured; complete actual historical or possible consumers are not enumerable from this snapshot.',
'A14':'All 24 cache queries decoded; source paths join to native package files.',
'A15':'41 cryptographically verified cache-reference archives, 459 equal complete member comparisons; cache identity is not installation provenance.',
'V01':'41 lock-addressed verified archives and 459 complete equal member comparisons; directory records assert membership only.',
'V02':'Installed, residual and cached receipt routes yielded zero unowned members with receipt; 6859 member paths lack one. Current-package duplicates are not old receipts.',
'V03':'Present account/group/sudo state has no retained causal event proving installation default versus later choice.',
'V04':'Three inner-store scans completed with no nested atomic boundaries; parent association is documented.',
'V05':'Metadata/prefixes do not establish complete image payload receipt or historical acquisition.',
'V06':'Selected configuration bytes and whole-file hashes are recorded; current equality is separate from creator.',
'V07':'Current text/key metadata/mount names do not establish a creation event.',
'V08':'Font-cache decoder sources join to exact native font package files.',
'M01':'Sysusers source files and RPM scriptlets are available, but a script is not proof that its branch executed for this object.',
'M02':'263 of 263 current unit selections recorded, with source files and enablement links.',
'M03':'Current links and script text do not establish the enablement actor/default event.',
'M04':'Sudo source bytes plus native full package-file comparisons permit source attribution where a receipt exists.',
'M05':'Source equality cannot prove whether a later actor selected the same default.',
'M06':'Active /etc traversed: 2219 descendants while the snapshot marker is retained.',
'M07':'Two snapshot-root manifests and 15837 complete comparisons recorded; generated members without a snapshot receipt remain unproved.',
'M08':'16177 of 16177 snapshot/current regular-file pairs have complete SHA256 comparisons.',
'M09':'Two SELinux store listings/checksums and full current/snapshot equality do not recover the original generated CIL/HLL receipt or event.',
'M10':'Complete bounded grubenv bytes retained, without executing configuration.',
'M11':'Current boot values do not establish who created or selected them.',
'M12':'Snapshot-root package set and database-file full comparisons are retained.',
'M13':'Host dumpsolv decoded the copied bounded cache stream; three cache/source files recorded.',
'T01':'Three current StaticPod image references are retained; they do not identify historical pull actor or every image source.',
'T02':'Six opaque roots and deeper target metadata are expanded; 18 pseudo-component boundaries remain after three distinct listing approaches.',
'T03':'No original complete installed-image manifest is exposed by these current-state API queries; current hashes/backing are not an installation receipt.',
'T04':'Complete API-daemon mountinfo is retained; namespace and stacked-overlay history prevent an unconditional per-object historical layer/persistence assertion.',
'T05':'Current content/listing/source references do not establish each historical creation/derivation event.',
'T06':'5940 of 5963 initial regular files yielded complete current hashes after Read, Copy and fresh-metadata Read; 23 remained not-found (9 containerd, 14 kubelet). Current absence is recorded, unavailable initial content is not inferred.',
'G01':'Fresh four-slot machine and two-level collector are exercised; unchanged browser and container actions fail in the final run, so full ordinary-action readiness is not certified.'}
evidence={'alma':'rehearsal/alma/round3','void':'rehearsal/void/round3','microos':'rehearsal/microos/round-3','talos':'rehearsal/talos/content-final','gentoo':'rehearsal/gentoo/round2'}
rows=list(csv.DictReader((R/'MISSING.tsv').open(),delimiter='\t'))
assert {r['fact'].split(':')[0] for r in rows}==set(notes)
with (R/'fact-status.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['machine','fact_id','status','evidence','reason_or_limit'])
 for r in rows:
  key=r['fact'].split(':')[0];status='recordable' if key in recorded else 'partial' if key in partial else 'not-obtainable'
  w.writerow([r['machine'],key,status,evidence[r['machine']],notes[key]])
print(f'{len(recorded)} of {len(rows)} fact groups recordable; {len(partial)} partial; {len(rows)-len(recorded)-len(partial)} not obtainable')
