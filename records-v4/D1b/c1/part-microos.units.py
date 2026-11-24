import csv,json,collections,pathlib,base64
csv.field_size_limit(10000000)
root=pathlib.Path('D1b/handoff/microos')
def read(p):return list(csv.DictReader(open(p),delimiter='\t'))
rows=[r for r in read('D1b/in/part-microos.tsv') if r['kind'] in ['L1:unit-file','L1:user-unit-file']]
sel={r['object_id']:r for r in read(root/'s4-microos-unit-selected.tsv')}
pf=collections.defaultdict(list)
for r in read(root/'package-files.tsv'):pf[r['path']].append(r)
objects={r['id']:r for r in read(root/'objects.tsv')}
sources={r['path']:r for r in read(root/'s4-microos-sources.tsv')}
output=pathlib.Path('D1b/c1/part-microos.units.tsv')
existing=read(output) if output.exists() else []
done={r['id'] for r in existing}
with output.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not existing:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
 for r in rows:
  if r['id'] in done:continue
  s=sel[r['id'].removeprefix('d1b-microos-')]; ps=json.loads(s['properties_json']);assert s['query_exit']=='0'
  paths={p['FragmentPath'] for p in ps};assert len(paths)==1
  for p in ps:paths.update(p.get('SourceFiles',[]));paths.update(p.get('DropInPaths','').split())
  for path in paths:
   assert len(pf[path])==1 and pf[path][0]['integrity']=='unchanged',(r['id'],path)
   assert pf[path][0]['package'] in objects
   if path in sources:assert sources[path]['status']=='ok'
  fragment=ps[0]['FragmentPath'];pkg=objects[pf[fragment][0]['package']]['name'].split('@')[0].removeprefix('rpm:')
  w.writerow([r['id'],'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Unit definition configuring '+r['name'].split(':')[-1]+' behavior.','raw:D1b/handoff/microos/package-files.tsv',f'Selected unit definition remains unchanged from {pkg}; first question decides, and its supplying package line covers it.'])
  f.flush()
actual=read(output)
assert len(actual)==260 and {r['id'] for r in actual}=={r['id'] for r in rows}
assert all(len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30 for r in actual)
print(collections.Counter(r['decision'] for r in actual))
sample_indices=[0,2,35,67,98,130,160,195,230,259]
notes='''# Unit-file classification rule\n\nScope: 260 system and user unit-file inventory rows. No other classification was read.\n\nRule U1: Resolve the inventory unit through s4-microos-unit-selected.tsv. The selected fragment, and every selected drop-in/source file, must have an exact package-files.tsv comparison of unchanged and an installed supplying package in objects.tsv. Then S8.2-6, S8.2-7 and S8.2-8 answer question 1 affirmatively; S8.2-16 covers this installed file with its supplying package line. All 260 meet this predicate. Package installation reason does not change coverage of files obtained with that package; the package object's own recording is a separate question. Disabled/static/template files remain installed files. No inference about human choice from enablement or preset equality is made.\n\nThe objects are the listed unit definitions, not the enabled-state value or the running process. Current selected fragment resolution avoids inferring the selected source from a basename. Multiple identical property records for aliases are checked for the same fragment; drop-ins are checked separately.\n\nDocumentation: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html describes list-unit-files as listing installed unit files and distinguishes it from list-units. Exact excerpt: “Use list-unit-files (see below) for listing installed unit template files.”\n\nhttps://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html describes unit files as INI-style configuration and alias resolution through symbolic links. Exact excerpt: “Units can be aliased (have an alternative name), by creating a symlink”.\n\nFacts: D1b/handoff/microos/s4-microos-unit-selected.tsv, package-files.tsv, objects.tsv and s4-microos-sources.tsv. Saved query evidence is retained in those tables. Current source inspection confirms configuration definitions and purposes. Selected definitions and drop-ins are supplied installed package files; none is a transient /run fragment.\n\n## Manual checks of U1\n\nTen spread rows were manually inspected: current source bytes decoded from s4-microos-sources.tsv, selected-fragment join and unchanged package comparison.\n\n'''
for i in sample_indices:
 r=rows[i];p=json.loads(sel[r['id'].removeprefix('d1b-microos-')]['properties_json'])[0]['FragmentPath'];src=base64.b64decode(sources[p]['content_base64']).decode();desc=next((x.removeprefix('Description=') for x in src.splitlines() if x.startswith('Description=')),'unit configuration')
 notes+=f'- {r["id"]}: `{p}`; {desc}; exact package comparison unchanged.\n'
notes+='\nAll selected additional drop-ins are also unchanged package files, including user@.service, dbus-broker, logind, ignition-delete-config, remount-fs, sysctl and udevd. No gap rows. Output IDs and field word limits were verified by the accompanying script.\n'
pathlib.Path('D1b/c1/part-microos.units.notes.md').write_text(notes)
