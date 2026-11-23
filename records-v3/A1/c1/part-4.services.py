import csv
from pathlib import Path
rows=list(csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t'))
p=Path('A1/c1/part-4.tsv');seen={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}
functions={
'avahi-daemon':'Starts and supervises multicast service discovery.',
'dbus-system':'Starts and supervises the system message bus.',
'elogind':'Starts and supervises login and session management.',
'file-systems':'Orders startup after required filesystems become available.',
'guix-daemon':'Starts and supervises the package build daemon.',
'guix-ownership':'Adjusts store ownership for the package build daemon.',
'host-name':'Sets the system network identity.',
'log-cleanup':'Schedules execution of old-log deletion code.',
'log-rotation':'Periodically executes log rotation code.',
'loopback':'Initializes the loopback network interface.',
'networking':'Starts and supervises DHCP network configuration.',
'nscd':'Starts and supervises name-service caching.',
'ntpd':'Starts and supervises network clock synchronization.',
'pam':'Provides the authentication-service dependency on login management.',
'root':'Runs the service manager and its administrative actions.',
'root-file-system':'Coordinates root-filesystem lifecycle and shutdown.',
'spice-vdagentd':'Starts and supervises desktop integration with the virtual-machine display client.',
'ssh-daemon':'Listens for SSH connections and launches session daemons.',
'sshd-9':'Runs an accepted SSH session service.',
'sysctl':'Applies kernel parameter settings.',
'system-log':'Collects system and kernel messages into log destinations.',
'term-console':'Provides console login service when its console is available.',
'timer':'Provides scheduling of timed service actions.',
'transient':'Provides dynamic spawning of transient services.',
'udev':'Starts and supervises device management.',
'upower-daemon':'Starts and supervises power-device monitoring.',
'urandom-seed':'Restores and saves random-generator seed across boots.',
'user-file-systems':'Coordinates unmounting manually mounted filesystems.',
'user-homes':'Initializes user home directories.',
'user-processes':'Orders user-process startup and shutdown after filesystem initialization.',
'virtual-terminal':'Sets kernel virtual terminals to UTF-8 mode.',
'x11-socket-directory':'Prepares the X11 socket directory.',
'xorg-server':'Starts and supervises the graphical login manager.'}
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for r in rows:
  if r['kind']!='system-service' or r['id'] in seen:continue
  n=r['name']
  if n.startswith('console-font-'):what='Loads a Unicode font into '+n.removeprefix('console-font-')+'.'
  elif n.startswith('term-tty'):what='Starts and supervises a login terminal on '+n.removeprefix('term-')+'.'
  elif n.startswith('file-system-'):what='Manages mounting and unmounting '+n.removeprefix('file-system-')+'.'
  else:what=functions[n]
  if n in ['root','sshd-9']:
   sentences='S2.2-9,S2.2-12';reason='The observed service runs a separate program process, explicitly required by these sentences.'
  else:
   sentences='S2.2-10';reason='Shepherd executes this service’s lifecycle procedures with its own rights; they are executable code, not confined application settings.'
  w.writerow([r['id'],'MUST',sentences,what,'raw:guix/herd-all-service-status.txt',reason]);f.flush()
