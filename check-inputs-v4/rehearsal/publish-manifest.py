#!/usr/bin/env python3
"""Build and validate an explicit credential-free publication allowlist."""
import csv,gzip,hashlib,pathlib,re,sys
C=pathlib.Path(__file__).resolve().parents[1]
files={'inputs-check-1.md','inputs-check-4.md','inputs-beyond-plan.md','DISCLOSURES.md','READY.md','CHOICES.md','releases.tsv','COLLECT.md','TALOS-COLLECT.md','LAB.md','collect.sh','lab.sh','install/materialize.py','PUBLISH.list','input-files.sha256.tsv','FIX-C1-REH-1.md','REVIEW.md','REVIEW-KIT.md','KIT-SHA256SUMS','rehearsal/REVIEW-FINAL.md'}
files.update((C/'rehearsal/recipe-paths.txt').read_text().splitlines())
files.update(p.relative_to(C).as_posix() for p in (C/'actions').glob('*') if p.is_file() and p.suffix in ('.sh','.py','.md'))
files.update(p.relative_to(C).as_posix() for p in (C/'collector').glob('*') if p.is_file() and (p.suffix in ('.py','.go','.sh','.md') or '.part-' in p.name))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*.py'))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/*.py'))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal/mint').glob('lived-gaming-fx[1-4]-staged.sh'))
files.add('rehearsal/fedora/homebrew-discovery.patch')
files.add('rehearsal/mint/operator-stop-fx2.sh')
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/sources/*') if p.is_file())
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*.md'))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/status.tsv'))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/counts.tsv'))
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/*.md'))
system_records={'CLEANUP.tsv','FX-RESULT.json','cleanup-final.tsv','cleanup-status.tsv','counts.tsv','deployed-source.tsv','firefox-bundled-release.json','fixture.json','gui-guard-verification.json','https-endpoints.tsv','old-action-status.tsv','portage-adapter-test.txt','portage-reasons-test.txt','query-limitations.tsv','serial-fixture-attempt1.json','serial-fixture-v2.json','serial-fixture-v3.json','serial-fixture.json','serial-fixture-sync.json','serial-sync-fixture.json','serial-wire-size.json','status.tsv'}
for p in (C/'rehearsal').glob('*/*'):
 if p.is_file() and (p.name in system_records or re.fullmatch(r'fx[1-4]-(?:collector-)?(?:deployed|local|source|staged)\.sha256',p.name) or re.fullmatch(r'fx[1-4]-process-control\.tsv',p.name)):
  files.add(p.relative_to(C).as_posix())
root_records={'key-material.sha256.tsv','language-reason-verification.txt','materialize-verification.json','probe-build.json','publication-builder-verification.json','recipe-paths.txt','final-summary.json','cleanup-final.tsv'}
files.update('rehearsal/'+name for name in root_records if (C/'rehearsal'/name).is_file())
# Retained permitted diagnostics only; never raw stdout, objects or members.
files.update(p.relative_to(C).as_posix() for p in (C/'rehearsal').glob('*/diagnostics/**/*') if p.is_file() and (p.name in ('coverage.tsv','collector.stderr') or (p.name.startswith(('action-','live-')) and p.suffix=='.stderr') or p.suffix=='.sha256' or (p.suffix in ('.err','.stderr') and p.stat().st_size>0)))
files.update(p.relative_to(C).as_posix() for p in (C/'raw/fx-release-evidence').glob('*') if p.is_file())
files.update(['raw/microos-kit2/verification.txt','raw/microos-kit2/appliances.html','collector/probe-build.json'])
# The kit-review checksum is retained; the primary final manifest covers revised kit docs.
files.update(p.relative_to(C).as_posix() for p in (C/'parts').glob('*.md'))
for table in (C/'rehearsal').glob('*/query-limitations.tsv'):
 for record in csv.DictReader(table.open(),delimiter='\t'):
  diagnostic=C/record['diagnostic']
  if (diagnostic.is_file() and not diagnostic.is_symlink()
      and diagnostic.resolve().is_relative_to((table.parent/'diagnostics').resolve())
      and diagnostic.suffix in ('.err','.stderr')):
   files.add(diagnostic.relative_to(C).as_posix())
# Provenance documents are public instrument records, never raw guest output.
files.update(['KIT-READY.md','KIT2-READY.md','COL-READY.md','ACT-READY.md'])
missing=[p for p in files if not (C/p).exists() and p not in ('PUBLISH.list','input-files.sha256.tsv')]
check_only='--check-only' in sys.argv
if missing and not check_only:raise SystemExit('Missing publication inputs: '+','.join(sorted(missing)))
if check_only:
 print('pending_publication_inputs',','.join(sorted(missing)))
 files={p for p in files if (C/p).exists()}
if not check_only:(C/'PUBLISH.list').write_text(''.join(p+'\n' for p in sorted(files)))
rows=[]
for name in sorted(files-{'input-files.sha256.tsv'}):
 p=C/name
 if p.stat().st_size>300000:raise SystemExit('Oversized publication file: '+name)
 if p.is_symlink() or not p.resolve().is_relative_to(C.resolve()):raise SystemExit('External publication path: '+name)
 if '.part-' not in name:
  s=p.read_text()
  bad=[label for label,rx in [('private-key',r'-----BEGIN [A-Z ]*(?:PRIVATE KEY|PUBLIC KEY|CERTIFICATE)-----'),('public-key-material',r'ssh-ed25519 [A-Za-z0-9+/=]{20,}'),('credential-yaml',r'^\s*(?:client-key-data|client-certificate-data):\s*\S+'),('personal-path',r'/home/(?!user/|linuxbrew/|calops/)[a-zA-Z][a-zA-Z0-9_-]*/')] if re.search(rx,s,re.M)]
  if bad:raise SystemExit('Publication scan failed: '+name+' '+','.join(bad))
 rows.append([name,hashlib.sha256(p.read_bytes()).hexdigest()])
if not check_only:
 with (C/'input-files.sha256.tsv').open('w',newline='') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['path','sha256']);w.writerows(rows)
parts=b''.join(p.read_bytes() for p in sorted((C/'collector').glob('probe-linux-amd64.gz.part-*')))
assert parts==(C/'collector/probe-linux-amd64.gz').read_bytes()
assert gzip.decompress(parts).startswith(b'\x7fELF')
assert (C/'input-files.sha256.tsv').stat().st_size<=300000
print('publication_files',len(files),'all_files_bounded',1,'chunks_match',1)
