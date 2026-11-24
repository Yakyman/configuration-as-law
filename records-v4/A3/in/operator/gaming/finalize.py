from pathlib import Path
import csv,json,collections,hashlib
csv.field_size_limit(64*1024*1024)
work=Path(__file__).resolve().parent
raw=work.parents[1]/'raw'
life=json.loads((work/'lifecycle.json').read_text())
actions=[]
for line in (work/'actions-status.tsv/actions-status.tsv').read_text().splitlines():
 name,rc,duration=line.split('\t'); actions.append({'action':name,'exit_status':int(rc),'duration_seconds':int(duration)})
status={'machine':'gaming','base':'mint','actions':actions,'lifecycle':life,'deviations':[], 'independent_acceptance':'not performed by operator'}
for label in ('gaming','gaming-base'):
 p=raw/label
 meta=json.loads((p/'metadata.json').read_text())
 with (p/'objects.tsv').open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
 status[label]={'objects':len(rows),'by_kind':dict(sorted(collections.Counter(r['level']+':'+r['kind'] for r in rows).items())),'collector_exit_status':life[label+'-collector']['exit_status'],'filesystem_complete':meta['filesystem_complete'],'package_ownership_complete':meta['package_ownership_complete'],'gaps':meta['gaps']}
 expected=json.loads((work/(label+'-remote-hashes.json')).read_text())
 actual={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
 assert actual==expected,label
 status[label]['transfer']={'files':len(actual),'all_hashes_match':True}
status['restart_boot_ids_differ']=(work/'boot-before.out').read_text().strip()!=(work/'boot-after.out').read_text().strip()
(work/'status.json').write_text(json.dumps(status,indent=2)+'\n')
lines=['# Gaming operator record','','All file references in this report are relative to `A3/in/operator/gaming/` unless stated otherwise. Beyond-plan TASK A3-I. Base: mint. Committed input marker: `3e0207b104f9718793c5b2678810936c7c3c14d2`.','','All staged input bytes matched the published checksums locally and after server transfer (`input-sha256.tsv`, `deployed-hashes.json`, `deployed-verification.txt`). The collector used the published compressed probe chunks.','','The lived script ran exactly once as the ordinary guest account through the documented session environment. Its four required input files were staged under `/run/user/1000/a3-inputs`; this runtime instrumentation disappeared on the one stop/start restart. No failed action was repaired or substituted. Action output is retained under `actions-logs/actions-logs/`; statuses are in `actions-status.tsv/actions-status.tsv`. Host lifecycle output replaces the actual host home and hostname with placeholders; guest action output and collector output are unchanged.','','| Action | Exit | Seconds |','|---|---:|---:|']
lines += [f"| {a['action']} | {a['exit_status']} | {a['duration_seconds']} |" for a in actions]
lines += ['', "The failed anonymous download reports `ERROR! Failed to install app '1110390' (Missing configuration)` in `actions-logs/actions-logs/gaming_anonymous_download.log`, after successful anonymous connection and user-info retrieval. Its stderr is retained alongside. No repair or retry was performed."]
lines+=['','Lifecycle exit statuses and UTC times: `lifecycle.json`; distinct boot identifiers: `boot-before.out`, `boot-after.out`. Both disposable clones were destroyed (`lived-destroy.out`, `base-destroy.out`, lifecycle statuses).','','| Inventory | Objects | Collector exit | Filesystem complete | Ownership complete |','|---|---:|---:|---|---|']
for label in ('gaming','gaming-base'):
 s=status[label]; lines.append(f"| {label} | {s['objects']} | {s['collector_exit_status']} | {s['filesystem_complete']} | {s['package_ownership_complete']} |")
lines+=['','Whole collector output: `../../raw/gaming/` and `../../raw/gaming-base/`. Every transferred file matched its remote SHA-256 manifest. Counts by level/kind and all collector gaps are retained in `status.json`; raw `metadata.json` and `coverage.tsv` are authoritative.','','Deviations from committed action/collector inputs: none. The published-list checksum discrepancy is recorded by the coordinating operator, separately from the matching executable inputs. No independent acceptance is asserted here.']
(work/'REPORT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:status[k]['objects'] for k in ('gaming','gaming-base')}))
