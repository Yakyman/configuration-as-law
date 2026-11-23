#!/usr/bin/env python3
"""Use only retained numerical rehearsal data to write the publication summary."""
import csv,hashlib,pathlib,re
C=pathlib.Path(__file__).resolve().parents[1]
systems=['alma','void','gentoo','microos','talos','nixos','guix','fedora','mint','debian-server']
def read(p):return list(csv.DictReader(p.open(),delimiter='\t')) if p.exists() else []
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
summary=[];dis=[]
for system in systems:
 d=C/'rehearsal'/system;rs=read(d/'status.tsv');cs=read(d/'counts.tsv')
 rounds=sorted(set(int(r['round']) for r in rs));latest=rounds[-1] if rounds else None
 rows=[r for r in rs if int(r['round'])==latest];counts={r['kind']:int(r['rows']) for r in cs if int(r['round'])==latest}
 action=[r for r in rows if re.fullmatch(r'action-(?:package_program|application_package|language_program|browser_extension|personal_setting|user_service|network_connection|home_script|container_run|developer_[a-z_]+|gaming_[a-z_]+|server_[a-z_]+)',r['operation'])]
 expected=9 if system in ('alma','void','gentoo','mint') else 13 if system in ('fedora','debian-server') else 0
 actions_ok=len(action)==expected and all(r['exit_status']=='0' for r in action)
 ac='not assigned' if not expected else f'{sum(r["exit_status"]=="0" for r in action)}/{expected} zero'
 transport=[r for r in rows if re.fullmatch(r'transport-\d\d',r['operation'])]
 transport_ok={r['operation'] for r in transport}=={f'transport-{i:02d}' for i in range(1,21)} and len(transport)==20 and all(r['exit_status']=='0' for r in transport)
 tr=f'{sum(r["exit_status"]=="0" for r in transport)}/20 zero' if transport else 'not reached'
 col=next((r for r in rows if r['operation']=='collector'),None)
 col_text='not assigned (check 4)' if system in ('nixos','guix') else 'not completed'
 n=counts.get('packages:total',0);reason=counts.get('packages:reason-known',0);anyknown=counts.get('packages:integrity-any-known',0);allknown=counts.get('packages:integrity-all-known',0)
 collect_ok=False
 latest_counts=[r for r in cs if int(r['round'])==latest and not r['kind'].startswith('lab:')]
 duplicate_counts=len({r['kind'] for r in latest_counts})!=len(latest_counts)
 duplicate_collectors=sum(r['operation']=='collector' for r in rows)>1
 if col:
  l2=counts.get('level:2',0);col_text=f'exit {col["exit_status"]}; {col["duration_seconds"]} s; L2 {l2} rows'
  queries_ok=all(r['exit_status']=='0' or r['exit_status']=='127' or (r['exit_status']=='75' and r['operation']=='query-filesystem') for r in rows if r['operation'].startswith('query-'))
  collect_ok=not duplicate_counts and not duplicate_collectors and counts.get('collector:reduction-complete')==1 and counts.get('collector:exit-success')==1 and queries_ok and col['exit_status']=='0' and float(col['duration_seconds'])<1800 and l2>0 and counts.get('collector:filesystem-complete',0)==1 and n>0 and reason/n>.9 and allknown/n>.9
 failures=[]
 if duplicate_counts or duplicate_collectors:failures.append('duplicate reduction or collector records; acceptance refused')
 failures += [f'{r["operation"][7:]} exit {r["exit_status"]}' for r in action if r['exit_status']!='0']
 if expected and len(action)<expected:failures.append('action batch incomplete')
 if not transport_ok:failures.append('twenty-call transport not passed')
 if system not in ('nixos','guix'):
  if not col:failures.append('collector not completed')
  elif col['exit_status']!='0':failures.append('collector incomplete or failed; see numeric status')
  if col and any(r['exit_status'] not in ('0','127') and not (r['exit_status']=='75' and r['operation']=='query-filesystem') for r in rows if r['operation'].startswith('query-')):failures.append('nonzero query causes not fully established from retained statuses')
  if n:
   failures.append(f'known reason {reason}/{n}; any-file integrity {anyknown}/{n}; all-file integrity {allknown}/{n}')
  if system=='talos':failures.append('bounded APIs do not supply complete L2, reason or image/file integrity')
  elif col and not counts.get('collector:filesystem-complete',0):failures.append('filesystem traversal incomplete')
  if col and not collect_ok:failures.append('package facts/completeness threshold not certified')
 if system=='guix':
  if any(r['operation']=='create' and r['exit_status']!='0' for r in rows):failures.append('boot/login failed; output unread, cause unresolved')
  if any(r['operation']=='destroy' and r['exit_status']!='0' for r in rows):failures.append('graceful shutdown failed; kill/destroy fallback recorded')
 if not rs:failures.append('no usable base/rehearsal completed by finalization')
 cleanup_ok=any(r['operation'] in ('destroy','destroy-fallback') and r['exit_status']=='0' for r in rows)
 ready=actions_ok and transport_ok and cleanup_ok and (system in ('nixos','guix') or collect_ok)
 summary.append((system,ready,ac,col_text,tr,'; '.join(failures) if failures else 'none',latest))
 for rno in rounds:
  rr=[r for r in rs if int(r['round'])==rno];cc={r['kind']:int(r['rows']) for r in cs if int(r['round'])==rno}
  actions=[r for r in rr if r['operation']=='actions'];cols=[r for r in rr if r['operation']=='collector']
  cleanup=[r for r in rr if r['operation'] in ('destroy','kill-fallback','destroy-fallback')]
  def fmt(rows):return ', '.join(f'{r["operation"]}: {r["exit_status"]} / {r["duration_seconds"]} s' for r in rows) or 'not reached'
  dis.append(f'| {system} | {rno} | {fmt(actions)} | {fmt(cols)} | {cc.get("level:1","not retained")} / {cc.get("level:2","not retained")} | {cc.get("packages:reason-known","not retained")} / {cc.get("packages:total","not retained")} | {cc.get("packages:integrity-any-known","not retained")} / {cc.get("packages:integrity-all-known","not retained")} | {fmt(cleanup)} |')
check=sum(x[1] for x in summary[:5]);check4=all(x[1] for x in summary[5:7]);lived=sum(x[1] for x in summary[7:])
line=f'INPUTS: {check} of 5 check-1 systems ready; check 4 {"ready" if check4 else "not ready"}; lived-in {lived} of 3 ready'
ready=line+'\n\n| System | Actions rehearsal | Collector rehearsal: duration and second level | Transport | What does not work and why |\n|---|---|---|---|---|\n'
for system,ok,ac,col,tr,fail,r in summary:
 ready+=f'| {system}'+(f' (round {r})' if r else '')+f' | {ac} | {col} | {tr} | {fail}; evidence: `rehearsal/{system}/status.tsv`, `counts.tsv` |\n'
(C/'READY.md').write_text(ready)
s='# Known before the first observation\n\nRecorded 2026-11-23 UTC. This is preparation evidence only. Every guest used for these rehearsals is a throwaway clone; command and collector output is deleted unread. The retained per-system `status.tsv` and `counts.tsv` contain only exit statuses, elapsed seconds, byte sizes and row counts labelled by fixed operation/kind. Missing results are not zero or successful absence. Counts from nonzero/incomplete collector runs are partial and do not certify coverage.\n\n'
s+='## Rehearsal statuses and counts\n\nPackage integrity is reported two ways: at least one known file, and every listed file known. The first does not establish whole-package completeness. Directory/symlink and unsupported-manager facts remain unknown. Readiness uses the conservative complete-facts reading; no unknown fact is relabelled to pass a threshold.\n\n| System | Round | Actions: exit / duration | Collector: exit / duration | L1 / L2 rows | Known reasons / packages | Integrity any / all known packages | Cleanup: exit / duration |\n|---|---|---|---|---|---|---|---|\n'+'\n'.join(dis)+'\n\n'
s+='Every query status and byte size and every object-kind count is retained in the tables below, without object names or file contents.\n\n'
paths=[]
for system in systems:
 for name in ('status.tsv','counts.tsv'):
  p=C/'rehearsal'/system/name
  if p.exists():paths.append(p.relative_to(C).as_posix())
s+='| File | SHA256 |\n|---|---|\n'+''.join(f'| `{p}` | `{digest(C/p)}` |\n' for p in paths)
s+='\n## Instrument repairs, procedural deviations and exposed content\n\n'
for name in ['rehearsal/NOTES.md','rehearsal/SCOPE.md','rehearsal/EXPOSURES.md']+[f'rehearsal/{x}/NOTES.md' for x in systems]:
 p=C/name
 if p.exists():s+='### '+name+'\n\n'+p.read_text()+'\n'
s+='## Installation choices\n\nThe following is the complete prepared choice record, including superseded attempts and active late-system replacements. They were established before any retained observation.\n\n'+(C/'CHOICES.md').read_text()+'\n'
s+='## Prior preparation disclosures read for this task\n\nThe task explicitly required the preceding input records and disclosure document to be read. Thus the following previously exposed facts also became known during preparation; they are not new observations and do not select new actions. File paths in this quoted historical record are relative to its original night folder.\n\n'+(C.parent.parent/'night-1122/C1/fix-c1-2/DISCLOSURES.md').read_text()+'\n'
s+='## Generated access material excluded from publication\n\nGenerated laboratory keys and credential-bearing Talos configurations are never published. Their SHA256 digests identify the exact preparation inputs without exposing key material. Fixed synthetic guest passwords in authored recipes are isolated laboratory parameters, not personal credentials.\n\n| Excluded laboratory file | SHA256 |\n|---|---|\n| `keys/lab` | `295e94b8759cb670b20d83c02f54d820327403adbec59c158be122d3124fae25` |\n| `keys/lab.pub` | `763ebc7bddd46b03ebfc01b1ac44b2cf72b80a8429d565ef3442d8a338e5fe72` |\n'
s+=f'| `install/access-key.pub` | `{digest(C/"install/access-key.pub")}` |\n'
for p in sorted((C/'install/talos').rglob('*')):
 if p.name in ('talosconfig','controlplane.yaml') and p.is_file():s+=f'| `{p.relative_to(C)}` | `{digest(p)}` |\n'
s+='\nInput-file checksums are supplied by `input-files.sha256.tsv`; `PUBLISH.list` is the exact publication allowlist. It excludes generated credentials, raw guest output, transient disks and the oversized unsplit helper. The checksum manifest excludes its own digest to avoid a self-reference. A final independent source/document review is recorded separately.\n'
(C/'DISCLOSURES.md').write_text(s)
print(line)
