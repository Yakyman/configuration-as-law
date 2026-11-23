import csv,collections
from pathlib import Path
p=Path('D1/c1/part-flatcar.code.tsv'); rows=list(csv.DictReader(p.open(),delimiter='\t')); fields=list(rows[0])
inputs={r['id']:r for r in csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t') if r['kind']=='L2:executable-code-outside-packages'}
corrected=[]
for r in rows:
 leaf=inputs[r['id']]['name'].rsplit('/',1)[1]
 if leaf=='load.cfg':
  r.update(decision='UNKNOWN',sentences='S2.2-10,S2.2-13,S3-2',what_it_does='Supplies build-time GRUB script; installed-copy consumers are unestablished.',reason='The installer embeds this script into another object. No evidence establishes later execution or functional dependence on the separate installed source copy.')
 elif leaf=='grub.cfg.tar':
  r.update(decision='UNKNOWN',sentences='S2.2-10,S2.2-13,S3-2',what_it_does='Supplies build-time GRUB configuration archive; installed-copy consumers are unestablished.',reason='The installer embeds this archive into bootloader images. No evidence establishes later consumption or functional dependence on this separate installed archive.')
 elif leaf=='mbr.bin':
  r.update(decision='HOLE',sentences='S2.2-1,S2.2-2,S2.2-6',what_it_does='Preserves a snapshot of patched MBR boot code for restoration.',reason='Restoration uses saved boot code, while the snapshot records past bytes. The text does not define whether its records-of-the-past exemption includes functional recovery snapshots.')
 else:continue
 corrected.append(r['id'])
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
s=Path('D1/c1/part-flatcar.code.finish.py').read_text()
s=s.replace("'mbr.bin':('MUST','S2.2-1,S2.2-2','Preserves patched MBR boot code for restoration.','Removing the saved patched boot code removes the supplied exact boot-code restoration capability.')", "'mbr.bin':('HOLE','S2.2-1,S2.2-2,S2.2-6','Preserves a snapshot of patched MBR boot code for restoration.','Restoration uses saved boot code, while the snapshot records past bytes. The text does not define whether its records-of-the-past exemption includes functional recovery snapshots.')")
s=s.replace("'grub.cfg.tar':('MUST','S2.2-10,S2.2-13','Supplies archived GRUB boot script embedded into bootloader images.','The archive supplies boot script executed by GRUB with bootloader rights; packaging does not change its code function.')", "'grub.cfg.tar':('UNKNOWN','S2.2-10,S2.2-13,S3-2','Supplies build-time GRUB configuration archive; installed-copy consumers are unestablished.','The installer embeds this archive into bootloader images. No evidence establishes later consumption or functional dependence on this separate installed archive.')")
s=s.replace("d,s,what,why='MUST','S2.2-10,S2.2-13','Supplies initial GRUB commands locating the boot partition and embedded configuration.','GRUB executes the embedded search and set commands with its own rights; configuration syntax remains executable code.'", "d,s,what,why='UNKNOWN','S2.2-10,S2.2-13,S3-2','Supplies build-time GRUB script; installed-copy consumers are unestablished.','The installer embeds this script into another object. No evidence establishes later execution or functional dependence on the separate installed source copy.'")
Path('D1/c1/part-flatcar.code.finish.py').write_text(s)
n=Path('D1/c1/part-flatcar.code.notes.md');text=n.read_text();start=text.index('## Remaining rows: individual decisions');text=text[:start]+'''## Remaining rows: individual decisions

Each remaining row has an individual rationale and documentation URL in the TSV. No additional homogeneous rule is applied.

'''
for r in rows:
 leaf=inputs[r['id']]['name'].rsplit('/',1)[1]
 if leaf.endswith('.mod') or (leaf.endswith('.lst') and leaf!='menu.lst'):continue
 text+=f"- {r['id']} ({leaf}): {r['decision']}; {r['sentences']}.\n"
text+='''
## Correction audit

Review rechecked five objects after the initial 466-row completion. Their initial decisions were MUST. For load.cfg (three rows) and grub.cfg.tar, the initial rationale incorrectly transferred the embedded copy's execution to the distinct stored source object. They are now UNKNOWN: build-time use is documented, but no captured evidence establishes later consumers of the installed copies. For mbr.bin, the initial removal rationale assumed recovery capability alone decided the case. It is now HOLE: the snapshot also records past bytes, and S2.2-6 does not delimit whether recovery snapshots qualify. This is a scope question about the explicit exemption, not an invented precedence rule.

Corrected IDs:

'''
for i in corrected:text+=f"- {i}: MUST → {next(x['decision'] for x in rows if x['id']==i)}.\n"
text+='''
Additional exact sentence: S2.2-6: “records of the past—logs, history;”

## Validation

The finish script verifies 466 rows, equal input/output ID sets, uniqueness, permitted decisions, and field word limits. The correction script records the explicit five-row correction. Current totals: MUST 440; NOT 0; HOLE 19; UNKNOWN 7; MIXED 0. No group rows occur in this assigned kind.
'''
n.write_text(text)
print(corrected)
