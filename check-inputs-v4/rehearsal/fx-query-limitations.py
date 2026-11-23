#!/usr/bin/env python3
"""Identify only documented optional-interface limitations from retained diagnostics."""
import csv,pathlib,re
C=pathlib.Path(__file__).resolve().parents[1]
anchor='COLLECT.md#fx-repair-limitations-and-file-accounting'
for directory in sorted((C/'rehearsal').iterdir()):
 if not directory.is_dir():continue
 records=[];reads=[]
 for coverage in sorted(directory.glob('diagnostics/fx*/coverage.tsv')):
  number=int(coverage.parent.name[2:])+10
  rows=list(csv.DictReader(coverage.open(),delimiter='\t'))
  reads.append((coverage,'Query statuses, durations and numerical coverage only.'))
  for row in rows:
   if row['exit_status']=='0':continue
   path=coverage.parent/pathlib.Path(row['stderr']).name
   error=path.read_text(errors='replace') if path.is_file() else ''
   query=re.sub(r'packages-flatpak-user-[0-9]+-', 'packages-flatpak-user-',row['query'])
   code=row['exit_status'];kind='unexplained';why='Nonzero query remains unexplained and is not accepted.'
   if code=='127' and query=='package-selected-groups-dnf' and not error.strip():kind='unavailable-manager-record';why='The optional DNF4 history record is unreadable or absent; the source guard returns 127 before invoking the helper. No missing-command inference is made.'
   elif code=='127':kind='missing-tool';why='Optional command or interpreter is unavailable; the corresponding interface is not collected.'
   elif query in ('user-service','user-timer','user-unit-file') and re.search(r'Failed to connect to|Failed to (?:get|open).*bus|No medium found',error,re.I):kind='inactive-user-manager';why='The user manager or session bus is unavailable; its interface is not collected.'
   elif query.startswith('packages-flatpak-user-') and re.search(r'permission denied|unable to open|does not exist',error,re.I):kind='inaccessible-flatpak-scope';why='This optional user Flatpak installation scope cannot be opened; it is not collected.'
   elif query in ('container','container-image','docker-container','docker-image','containers','container-images','docker-containers','docker-images','user-containers','user-images') and re.search(r'cannot connect|connection refused|failed to connect|no such file or directory',error,re.I):kind='inactive-engine';why='The optional container engine socket or service is unavailable; its runtime interface is not collected.'
   elif query=='firewall-nft' and 'JSON support not compiled-in' in error:kind='nft-json-unavailable';why='The installed nft binary lacks JSON support; nft JSON rules are not collected.'
   records.append(dict(round=number,query=query,exit_status=code,accepted='yes' if kind!='unexplained' and path.is_file() else 'no',limitation_class=kind,diagnostic=str(path.relative_to(C)),documentation=anchor,explanation=why))
   if path.is_file():reads.append((path,why))
 if not records and not reads:continue
 with (directory/'query-limitations.tsv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=['round','query','exit_status','accepted','limitation_class','diagnostic','documentation','explanation'],delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(records)
 (directory/'AUTO-DIAGNOSTIC-READS.md').write_text('# Diagnostic reads for query acceptance\n\nThe classifier reads only coverage and retained stderr, never query stdout or object/member records. Every diagnostic read and its machine-level disclosure follows.\n\n'+'\n'.join('- `'+str(p.relative_to(C))+'`: '+why for p,why in reads)+'\n')
 print(directory.name, 'documented',sum(r['accepted']=='yes' for r in records),'unexplained',sum(r['accepted']=='no' for r in records))
