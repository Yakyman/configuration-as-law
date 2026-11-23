import csv,json,collections
from pathlib import Path
KINDS={'L1:service','L1:timer','L1:unit-file','L1:user-service','L1:user-timer','L1:user-unit-file'}
rows=[r for r in csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t') if r['kind'] in KINDS]
header=['id','decision','sentences','what_it_does','basis','reason']
p=Path('D1/c1/part-fedora.units.tsv')
seen={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')} if p.exists() else set()
def group(r):
    if 'not-found' in r['members']:return 'absent'
    if ' alias ' in r['members']:return 'alias'
    if r['name'].endswith('.timer'):return 'timer'
    return 'service'
with p.open('a') as f:
    w=csv.writer(f,delimiter='\t',lineterminator='\n')
    if not p.stat().st_size:w.writerow(header)
    for r in rows:
        if r['id'] in seen:continue
        g=group(r)
        if g=='absent':
            d='NOT';what='Absent service reference; no loaded definition or running service.'
            reason='No service definition or running service exists; the represented absent service supplies no computer capability whose removal could change behavior.'
            doc='systemctl.html'
        elif g=='alias':
            d='MUST';what='Provides an alternate unit name for service or timer activation.'
            reason='Removing the alias removes activation through that name; this controls service execution beyond settings confined inside one program.'
            doc='systemd.unit.html'
        elif g=='timer':
            d='MUST';what='Schedules activation of a service through the service manager.'
            reason='Removing the timer removes its scheduled activation capability; its effects include starting another process, not merely internal program settings.'
            doc='systemd.timer.html'
        else:
            d='MUST';what='Defines or supplies service-manager activation and supervision of a process.'
            reason='Removing this service definition removes its managed activation capability; process execution is not a setting confined inside the service manager.'
            doc='systemd.service.html'
        out=[r['id'],d,'S2.2-1,S2.2-2',what,'doc:https://www.freedesktop.org/software/systemd/man/latest/'+doc,reason]
        assert len(what.split())<=15 and len(reason.split())<=30
        w.writerow(out);f.flush()
res=list(csv.DictReader(p.open(),delimiter='\t'))
assert len(res)==len(rows)==len({r['id'] for r in res})
assert {r['id'] for r in res}=={r['id'] for r in rows}
assert all(r['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'} for r in res)
print(collections.Counter(r['decision'] for r in res))
