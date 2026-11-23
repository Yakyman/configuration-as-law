import csv,json,pathlib,collections
base=pathlib.Path('D1/c1')
rows=[r for r in csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t') if r['kind'] in {'L1:user-service','L1:user-timer','L1:user-unit-file','L1:service','L1:timer','L1:unit-file'}]
out=base/'part-flatcar.units.tsv'
header=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(out.open(),delimiter='\t')) if out.exists() else []
seen={r['id'] for r in existing}
with out.open('a') as f:
 w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n')
 if not out.stat().st_size:w.writeheader()
 for r in rows:
  if r['id'] in seen:continue
  member=json.loads(r['members'])[0]
  if 'not-found' in member:
   decision='UNKNOWN';sent='S3-2';what='Unresolved inactive service reference; concrete definition and dependency effects unavailable.';basis='raw:D1/in/'+r['evidence'];reason='No unit definition was found; documentation explains missing-unit status but cannot establish this reference’s dependencies or behavioral effect.'
  else:
   decision='MUST';sent='S2.2-1,S2.2-2,S2.2-7,S2.2-13'
   if r['name'].endswith('.timer'):
    what='Schedules activation of a service through the service manager.';basis='doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html';reason='Removing this timer removes its service activation schedule; effects reach separate service processes, beyond settings only inside one program.'
   elif ' alias ' in member:
    what='Provides an alternative name through which a service can be activated.';basis='doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html';reason='Removing the alias removes activation through that name; the affected service runs beyond the manager, so the one-program exemption does not apply.'
   else:
    what='Defines manager-controlled activation and supervision of a separate service process.';basis='doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html';reason='Removing the service definition removes its managed activation capability; its effects extend to separate processes, so these settings are not confined inside one program.'
  w.writerow(dict(zip(header,[r['id'],decision,sent,what,basis,reason])));f.flush()
actual=list(csv.DictReader(out.open(),delimiter='\t'))
assert len(actual)==len(rows)==459
assert len({r['id'] for r in actual})==len(actual)
assert {r['id'] for r in actual}=={r['id'] for r in rows}
for r in actual:
 assert r['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'}
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30
print(dict(collections.Counter(r['decision'] for r in actual)))
