#!/usr/bin/python3 -B
"""Install and start the same declaration filesystem at all writable roots."""
import json, pathlib, subprocess, time
P=pathlib.Path
MOUNTS={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
store=P('/var/lib/stand-fs');store.mkdir(mode=0o700,exist_ok=True)
units=[]
for key,mount in MOUNTS.items():
    name='stand-files-'+key+'.service';units.append(name)
    extra=' --account-databases' if key=='etc' else ''
    unit=f'''[Unit]
Description=Primary declaration filesystem ({key})
After=local-fs.target stand-noexec.service
Requires=stand-noexec.service
Before=ssh.service stand-replay.service
[Service]
Type=simple
ExecStart=/usr/bin/python3 -B /usr/local/lib/stand/bc3_filesystem.py /var/lib/stand-fs/{key} {mount} --seed {mount}{extra}
ExecStartPost=/usr/bin/python3 -B /usr/local/lib/stand/bc3-ready.py {mount}
ExecStop=/usr/bin/umount {mount}
TimeoutStartSec=120
TimeoutStopSec=30
KillMode=control-group
Restart=no
[Install]
WantedBy=multi-user.target
'''
    (P('/etc/systemd/system')/name).write_text(unit)
P('/etc/stand/bc3-primary.json').write_text(json.dumps({
    'format':'bc3-primary-designation-v1',
    'primary_files':['/var/lib/stand/current/machine.jsonl']+
        ['/var/lib/stand-fs/'+key+'/current/declaration.json' for key in MOUNTS],
    'filesystem_mounts':MOUNTS,
    'semantics':'Filesystem declarations are desired namespace/inode/content state. System file operations apply prospective declarations before exposure; material is voluntarily recorded.'
},sort_keys=True,indent=2)+'\n')
subprocess.run(['/usr/bin/systemctl','daemon-reload'],check=True)
subprocess.run(['/usr/bin/systemctl','enable',*units],check=True)
# Start /etc last, after every unit and its enablement link already exists.
for unit in units:subprocess.run(['/usr/bin/systemctl','start',unit],check=True)
print('Five primary declaration filesystems mounted before factory capture')
