#!/usr/bin/env python3
"""Build final documents from retained numeric records and disclosed diagnostics."""
import csv,hashlib,json,pathlib,re,sys
C=pathlib.Path(__file__).resolve().parents[1]
SYSTEMS=['alma','void','gentoo','microos','talos','nixos','guix','fedora','mint','debian-server']
def rows(path):
 return list(csv.DictReader(path.open(),delimiter='\t')) if path.exists() else []
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
summary=[];history=[]
for system in SYSTEMS:
 d=C/'rehearsal'/system;ss=rows(d/'status.tsv');cc=rows(d/'counts.tsv')
 rounds=sorted({int(r['round']) for r in ss});last=rounds[-1] if rounds else 0
 if any(r>14 for r in rounds):raise SystemExit('Repair round outside four-round limit: '+system)
 completed_fx=[number for number in rounds if number>=11 and any(int(r['round'])==number and r['operation'] in ('destroy','destroy-fallback','destroy-interrupted','clone-absence-confirmed') and r['exit_status']=='0' for r in ss)]
 sr=[r for r in ss if int(r['round'])==last];cs={r['kind']:int(r['rows']) for r in cc if int(r['round'])==last and not r['kind'].startswith('lab:')}
 expected=9 if system in ('alma','void','gentoo','mint') else 13 if system in ('fedora','debian-server') else 0
 acts=[r for r in sr if re.fullmatch(r'action-(?:package_program|application_package|language_program|browser_extension|personal_setting|user_service|network_connection|home_script|container_run|developer_[a-z_]+|gaming_[a-z_]+|server_[a-z_]+)',r['operation'])]
 transports=[r for r in sr if re.fullmatch(r'transport-\d\d',r['operation'])]
 collect=[r for r in sr if r['operation']=='collector'];col=collect[-1] if collect else None
 whole=next((float(r['duration_seconds']) for r in sr if r['operation']=='whole-run'),None)
 action_ok=len(acts)==expected and all(r['exit_status']=='0' for r in acts)
 transport_ok=len(transports)==20 and len({r['operation'] for r in transports})==20 and all(r['exit_status']=='0' for r in transports)
 cleanup_ok=any(r['operation'] in ('destroy','destroy-fallback') and r['exit_status']=='0' for r in sr)
 query_failures=[r for r in sr if r['operation'].startswith('query-') and r['exit_status']!='0']
 limits=rows(d/'query-limitations.tsv');accepted=set();rejected=set()
 for r in limits:
  key=(int(r['round']),r['query'],r['exit_status'])
  diagnostic=C/r.get('diagnostic','')
  retained=diagnostic.is_file() and not diagnostic.is_symlink() and diagnostic.resolve().is_relative_to((d/'diagnostics').resolve())
  permitted=r.get('accepted')=='yes' and r.get('limitation_class') in {'unavailable-manager-record','missing-tool','inactive-user-manager','inaccessible-flatpak-scope','inactive-engine','nft-json-unavailable'} and retained and r.get('documentation')=='COLLECT.md#fx-repair-limitations-and-file-accounting'
  (accepted if permitted else rejected).add(key)
 accepted-=rejected
 unexplained=[r for r in query_failures if (last,r['operation'][6:],r['exit_status']) not in accepted]
 n=cs.get('packages:total',0);reason=cs.get('packages:reason-known',0);files=cs.get('package-files:total',0);known=cs.get('package-files:integrity-known',0);l2=cs.get('level:2',0)
 observed_reason=reason;reason_note=''
 if 'packages:reason-known-nonlanguage' not in cs:
  uncertain=sum(cs.get('reason:'+m+':'+v,0) for m in ('python','npm') for v in ('explicit','dependency'))
  if uncertain:
   reason=max(0,reason-uncertain)
   reason_note=f'; recorded {observed_reason}/{n} includes unseparated language-parent inference; established lower bound used'
 collect_ok=system in ('nixos','guix') or (len(collect)==1 and col['exit_status']=='0' and cs.get('collector:reduction-complete')==1 and l2>0 and n>0 and reason/n>.9 and files>0 and known/files>.9 and not unexplained)
 ready=last>=11 and action_ok and transport_ok and cleanup_ok and collect_ok and whole is not None and whole<1800
 failures=[]
 if not action_ok:failures += [f'{r["operation"][7:]} exit {r["exit_status"]}' for r in acts if r['exit_status']!='0'];failures += ['action batch incomplete'] if len(acts)<expected else []
 if not transport_ok:failures.append('transport sequence incomplete or failed')
 if not cleanup_ok:failures.append('cleanup not certified')
 if whole is None or whole>=1800:failures.append('whole-run 30-minute criterion not met')
 if system not in ('nixos','guix'):
  if cs.get('collector:reduction-complete')!=1:failures.append('collector numerical reduction incomplete')
  if not col:failures.append('collector not completed')
  elif col['exit_status']!='0':failures.append('collector exit '+col['exit_status'])
  if not l2:failures.append('second level has no rows')
  if not n or reason/n<=.9:failures.append(f'reason known {reason}/{n}')
  if not files or known/files<=.9:failures.append(f'integrity known {known}/{files} files')
  if unexplained:failures.append(f'{len(unexplained)} query failures lack documented limitation')
 ac='not assigned' if not expected else f'{sum(r["exit_status"]=="0" for r in acts)}/{expected} zero'
 coltext='not assigned (check 4)' if system in ('nixos','guix') else f'exit {col["exit_status"]}; {col["duration_seconds"]} s; L2 {l2}; reason {reason}/{n}{reason_note}; files {known}/{files}' if col else 'not completed'
 evidence=', '.join('`'+str((d/f).relative_to(C))+'`' for f in ('status.tsv','counts.tsv','query-limitations.tsv') if (d/f).exists())
 summary.append(dict(system=system,ready=ready,round=last,fx_rounds=len(completed_fx),fx_rounds_started=len([r for r in rounds if r>=11]),actions=ac,collector=coltext,transport=f'{sum(r["exit_status"]=="0" for r in transports)}/20 zero',whole=whole,failures=failures,evidence=evidence))
 for rno in rounds:
  rr=[r for r in ss if int(r['round'])==rno];rc={r['kind']:int(r['rows']) for r in cc if int(r['round'])==rno}
  def stage(name):
   matches=[r for r in rr if r['operation']==name]
   return '; '.join(f'{r["exit_status"]} / {r["duration_seconds"]} s' for r in matches) or 'not retained'
  cleanup='; '.join(f'{r["operation"]}: {r["exit_status"]} / {r["duration_seconds"]} s' for r in rr if r['operation'] in ('destroy','kill-fallback','destroy-fallback','kill-interrupted','destroy-interrupted','clone-absence-confirmed')) or 'not retained'
  history.append(f'| {system} | {rno} | {stage("actions")} | {stage("collector")} | {rc.get("level:1","not retained")} / {rc.get("level:2","not retained")} | {rc.get("packages:reason-known","not retained")} / {rc.get("packages:total","not retained")} | {rc.get("package-files:integrity-known","not retained")} / {rc.get("package-files:total","not retained")} | {cleanup} |')
line=f'INPUTS: {sum(s["ready"] for s in summary[:5])} of 5 check-1 systems ready; check 4 {"ready" if all(s["ready"] for s in summary[5:7]) else "not ready"}; lived-in {sum(s["ready"] for s in summary[7:])} of 3 ready'
print(line)
print(json.dumps(summary,indent=2))
if '--preview' in sys.argv:sys.exit(0)
unfinished=[s['system'] for s in summary if not s['ready'] and s['fx_rounds']<4]
if unfinished:raise SystemExit('Refusing finalization before ready/four rounds: '+','.join(unfinished))
ready=line+'\n\n| System | Actions rehearsal | Collector rehearsal: duration and second level | Transport | What does not work and why |\n|---|---|---|---|---|\n'
for s in summary:
 failure='; '.join(s['failures']) or 'none; documented query limitations retained'
 whole_text=str(s['whole'])+' s' if s['whole'] is not None else 'not recorded'
 ready+=f'| {s["system"]} (FX{s["round"]-10}; round {s["round"]}) | {s["actions"]} | {s["collector"]}; whole {whole_text} | {s["transport"]} | {failure}. Evidence: {s["evidence"]} |\n'
(C/'READY.md').write_text(ready)
(C/'rehearsal/final-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
dis='''# Known before the first observation

Recorded 2026-11-23 UTC. These are instrument rehearsals on disposable clones, not hypothesis observations or outcomes. Collector objects, raw query stdout and member lists were reduced by software and deleted unread. The binding diagnostic exception permits collector/action stderr and coverage; every read is identified below. No unknown fact is relabelled merely to pass a threshold.

## Statuses and counts

FX1–FX4 use numeric round keys 11–14 and preserve historical first-pass rounds. Readiness uses the latest completed repair round, all actions, twenty transport calls, documented query limitations, nonzero second level, more than 90% package reasons and more than 90% packaged-file integrity, whole-run duration below 1800 seconds, and confirmed clone destruction. Directory entries establish ownership but are not files; symlinks remain in file accounting. Zero file denominators fail. Historical FX records produced before the language-reason correction retain their exact original counts; those counts are not validated facts. For acceptance, every historically known Python/npm reason is conservatively subtracted unless the new separating counters are present. This lower bound avoids reading deleted inventory, and the table below remains the original recorded counts, with invalidation explained in the system fragments. Gentoo FX1 additionally contains obsolete graph-derived reasons and is never accepted.

| System | Round | Actions exit / seconds | Collector exit / seconds | L1 / L2 | Known reasons / packages | Known integrity / files | Destroy exit / seconds |
|---|---|---|---|---|---|---|---|
'''+ '\n'.join(history)+'\n\n## Repairs, exposed diagnostics and replaced actions\n\n'
fragments=['rehearsal/FX-SCOPE.md','rehearsal/EXPOSURES.md','rehearsal/NOTES.md','rehearsal/SOURCE-ACCEPTANCE.md','rehearsal/REVIEW-EXPOSURES.md']
for system in SYSTEMS:
 d=C/'rehearsal'/system
 fragments += [p.relative_to(C).as_posix() for p in sorted(d.glob('*.md')) if p.name not in ('PLAN.md','FX-LOG.md','COLLECT-FRAGMENT.md','COLLECT.fragment.md')]
for name in dict.fromkeys(fragments):
 p=C/name
 if p.exists():dis+='### '+name+'\n\n'+p.read_text()+'\n'
dis+='## Installation choices\n\nThe complete fixed choice record is `CHOICES.md` (SHA256 `'+sha(C/'CHOICES.md')+'`). Its contents remain unchanged in this repair round and are reproduced exactly below. Active installation inputs, including the MicroOS KIT2 vendor image and Guix serial fallback, follow that record. Image-variant omissions identified in review finding 8 are disclosed in `FIX-C1-REH-1.md`; no new selection is made here.\n\n'+(C/'CHOICES.md').read_text()+'\n\n'
dis+='## Previously disclosed preparation content\n\nThe task required the previous disclosure record to be read. The following remains known; it is not a new observation and did not select new workloads. Paths inside this historical quotation are relative to the preceding night.\n\n'+(C.parent.parent/'night-1122/C1/fix-c1-2/DISCLOSURES.md').read_text()+'\n'
dis+='## Excluded access material\n\nGenerated key material and Talos credentials are excluded from publication. Their digests identify the exact preparation inputs.\n\n| File | SHA256 |\n|---|---|\n| `keys/lab` | `295e94b8759cb670b20d83c02f54d820327403adbec59c158be122d3124fae25` |\n| `keys/lab.pub` | `763ebc7bddd46b03ebfc01b1ac44b2cf72b80a8429d565ef3442d8a338e5fe72` |\n'
for p in [C/'install/access-key.pub']+sorted((C/'install/talos').rglob('talosconfig'))+sorted((C/'install/talos').rglob('controlplane.yaml')):
 if p.is_file():dis+=f'| `{p.relative_to(C)}` | `{sha(p)}` |\n'
dis+='\n`input-files.sha256.tsv` is the final checksum manifest; `PUBLISH.list` is the exact allowlist. Source and credential-free recipe inputs are regenerated after all writers stop. Independent review is retained under `rehearsal/`.\n'
(C/'DISCLOSURES.md').write_text(dis)
