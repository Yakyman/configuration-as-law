import csv,pathlib,re,collections
p=pathlib.Path('A1/c1/part-5.1.tsv'); rows=list(csv.DictReader(p.open(),delimiter='\t')); header=list(rows[0]); by={r['id']:r for r in rows}
inp=[r for r in csv.DictReader(open('A1/in/part-5.tsv'),delimiter='\t') if r['machine']=='ubuntu' and r['kind'] in ('stored','stored-directory-skeleton')]
def fix(i,**kw):by[inp[i]['id']].update(kw)
fix(19,decision='MUST',sentences='S2.2-1,S2.2-13',what_it_does='Selects distribution-specific package-build behavior and provenance.',basis='doc:https://manpages.debian.org/testing/dpkg-dev/deb-origin.5.en.html',reason='The selected vendor controls build-tool behavior as well as metadata; its effect extends beyond descriptive content.')
fix(26,decision='MUST',sentences='S2.2-1,S2.2-15',reason='Group membership and administration rights require recording; exempt password values do not remove that requirement.')
fix(66,decision='MUST',sentences='S2.2-1,S2.2-15',reason='Account expiration and password-login restrictions require recording; password values themselves remain exempt.')
fix(115,decision='MUST',sentences='S2.2-1,S2.2-2',reason='Removing the flag disables database rebuilding instead of merely slowing equivalent work; the functional cache exemption does not apply.')
for i in [2,4,5,6]:fix(i,basis='doc:https://manpages.debian.org/unstable/linux-base/linux-update-symlinks.1.en.html')
fix(3,basis='doc:https://kernel.org/doc/html/next/driver-api/early-userspace/early_userspace_support.html')
fix(33,basis='doc:https://www.gnu.org/software/bash/manual/html_node/Readline-Init-File.html')
fix(34,basis='doc:https://github.com/open-iscsi/open-iscsi')
fix(44,basis='doc:https://netplan.readthedocs.io/en/stable/netplan-tutorial/')
fix(45,basis='doc:https://manpages.ubuntu.com/manpages/jammy/man5/networks.5.html')
for i in [52,85,86,89,92,93]:fix(i,basis='doc:https://www.gnu.org/software/bash/manual/bash.html')
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
assert len(rows)==len(inp)==len(by)==150
assert set(by)=={r['id'] for r in inp}
for r in rows:
 assert r['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'}
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30
 assert all('\n' not in v and '\t' not in v for v in r.values())
notes=pathlib.Path('A1/c1/part-5.1.notes.md')
with notes.open('w') as f:
 f.write('# Part 5: stored-object classification notes\n\nScope: 150 rows selected by machine column ubuntu and kind stored or stored-directory-skeleton. No other classifications were read. Only supplied inventory rows and public documentation were used. No objects were removed.\n\nThe input uses members=1 even when evidence reports n>1. The evidence count is treated as an internal group count; partial samples never establish the omitted members. No raw machine files are available for this subset.\n\n## Governing sentences\n\n')
 ids={s for r in rows for s in r['sentences'].split(',')}
 for line in open('SENTENCES.md'):
  if any('**'+i+'**' in line for i in ids):f.write(line)
 f.write('\n## Scripted rules and manual checks\n\nRule U applies S3-1 and S3-2 only when the inventory explicitly reports more stored members than it identifies. It does not infer that a directory is homogeneous from sample names. Unknown member functions prevent a complete group decision, irrespective of familiar sampled files. Public documentation cannot recover this machine-specific membership.\n\nTen manually checked rows follow. Each has fewer named samples than its stated count.\n\n| ID | Reported count | Named samples |\n|---|---:|---:|\n')
 for i in [0,1,10,11,16,18,43,49,53,54]:
  r=inp[i];n=re.search(r'; n=(\d+);',r['evidence']).group(1);samples=r['evidence'].split('samples=')[1].split(' | ')
  f.write(f"| {r['id']} | {n} | {len(samples)} |\n")
 f.write('\nRule L applies S2.2-6 to fully enumerated log/history storage. It excludes configuration, control markers and incomplete journal groups. Ten manual checks identify the kind of past activity; all are records, not commands.\n\n| ID | Manual finding |\n|---|---|\n')
 for i,desc in [(130,'Alternatives log'),(131,'Crash-report log'),(132,'Three enumerated package logs'),(133,'Authentication log'),(134,'Failed-login history'),(135,'Cloud initialization output log'),(136,'Cloud initialization log'),(137,'Kernel message record'),(138,'Previous kernel message record'),(139,'Package operation log')]:f.write(f"| {inp[i]['id']} | {desc} |\n")
 f.write('\nAll other rows were considered individually; explicit calls in part-5.1.build.py preserve those decisions. Its initial provisional entries were corrected before completion as recorded below. The output TSV is authoritative.\n\n## Functional checks and corrections\n\n')
 f.write('The protected account files require their membership and login restrictions to be recorded; password values remain exempt. Declaration representation and secret protection are design matters, so their combined storage is not a HOLE. The manual-database auto-update flag controls whether rebuilding happens: despite being a cached value, it fails the functional cache exemption. The distribution-origin link selects package-build behavior, not only provenance content. These corrections changed rows '+', '.join(inp[i]['id'] for i in [19,26,66,115])+'.\n\n')
 f.write('Remaining HOLE rows concern explicit substantive overlaps: historical records also used to control future behavior, and the unspecified scope of settings inside one daemon. They do not concern storage layout, secret protection, or the design treatment of accumulated state.\n\n')
 f.write('UNKNOWN singleton cases are not classified from suggestive names. Searches for the image-version file, overlay-root local configuration, legal-display marker and snap section cache did not establish the actual contents and consumers on this machine. Secondary discussion of the legal marker was found, but no version-matched primary package source was established; its effect remains unconfirmed. PackageKit documentation shows proxy persistence as well as transaction history, so its missing database contents matter.\n\n## Documentation excerpts\n\nShort quotations below identify the documented functions. The TSV records the applied functional inference. Source-specific quotations remain below 25 words each.\n\n')
 f.write('REFERENCES_PLACEHOLDER\n')
 f.write('\n## Verification\n\nExactly 150 assigned IDs, one occurrence each, with no extras or omissions. All decisions are valid; word limits and single-line fields pass.\n\n')
 for k in ['MUST','NOT','HOLE','UNKNOWN','MIXED']:f.write(f'{k}: {sum(r["decision"]==k for r in rows)}\n\n')
print(collections.Counter(r['decision'] for r in rows))
