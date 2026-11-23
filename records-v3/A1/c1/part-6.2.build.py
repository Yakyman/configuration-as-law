import csv,json,pathlib,collections
base=pathlib.Path('A1/c1'); rows=[r for r in csv.DictReader(open('A1/in/part-6.tsv'),delimiter='\t') if r['kind']=='stored' and r['machine']=='freebsd' and r['name'].startswith(('/boot/','/etc/'))]
D={};rules=collections.defaultdict(list)
def url(p):
 q,s=p.rsplit('.',1);return f'https://man.freebsd.org/cgi/man.cgi?query={q}&sektion={s}&format=ascii'
def put(n,d,s,w,p,r):D[n]=(d,s,w,'doc:'+url(p) if p else 'evidence',r)
def must(n,w,p,r='Removing these definitions changes system capabilities or policy beyond a single program interface.'):
 put(n,'MUST','S2.2-1,S2.2-2',w,p,r)
def unknown(n,w='Complete contents and functions of this directory are not established.'):
 put(n,'UNKNOWN','S3-2',w,None,'Inventory supplies selected paths without complete contents; public documentation cannot identify every stored member.')
# R1: executable boot binaries, matched explicitly, not by broad directory prefix.
bootbins='boot boot0 boot0sio boot1 boot1.efi boot2 cdboot gptboot gptboot.efi gptzfsboot isoboot loader loader.efi loader_4th loader_4th.efi loader_ia32.efi loader_lua loader_lua.efi loader_simp loader_simp.efi mbr pmbr pxeboot zfsboot zfsloader'.split()
for n in bootbins:
 p='loader.8' if 'loader' in n else {'boot0':'boot0cfg.8','boot0sio':'boot0cfg.8','gptboot':'gptboot.8','gptzfsboot':'gptzfsboot.8','pxeboot':'pxeboot.8'}.get(n,'boot.8')
 put('/boot/'+n,'MUST','S2.2-1,S2.2-2,S2.2-9','Provides executable bootstrapping code for a supported boot method.',p,'Executable boot code provides boot capabilities; removal makes that code unavailable.');rules['R1'].append('/boot/'+n)
# R2: installed Forth programs and script entrypoints.
for r in rows:
 n=r['name']
 if n.startswith('/boot/') and (n.endswith('.4th') or n in ['/boot/loader.rc','/boot/menu.rc']):
  put(n,'MUST','S2.2-10,S2.2-13','Executes boot-loader commands controlling startup or its display.','loader_4th.8','These are executable loader scripts, including display scripts; execution as code prevails over their appearance as settings.');rules['R2'].append(n)
for n in ['loader.help.bios','loader.help.efi','loader.help.userboot']:
 put('/boot/'+n,'NOT','S2.2-3,S2.2-4','Supplies loader command help text.','loader.8','Removing help removes documentation content; the boot loader and its commands remain available.')
for n in ['defaults','efi','fonts','images','kernel','kernel.old','lua']:unknown('/boot/'+n)
must('/boot/device.hints','Passes driver resource hints and kernel tunables into the kernel.','device.hints.5')
must('/boot/loader.conf','Selects kernel, loaded modules, and kernel parameters.','loader.conf.5')
put('/boot/entropy','UNKNOWN','S3-2','Supplies saved entropy to seed randomness during startup.','save-entropy.8','Documentation establishes entropy seeding, but evidence does not establish whether removing this seed disables any capability or only changes random output.')
for n in ['userboot.so','userboot_4th.so','userboot_lua.so']:
 put('/boot/'+n,'MUST','S2.2-10','Provides a dynamically loaded boot-loader implementation used by the virtual-machine loading process.','bhyveload.8','This library executes in the host loading process; it is not the confined guest operating system.')
# R3: explicit shell startup/control programs.
shells={'csh.cshrc':'csh.1','csh.login':'csh.1','csh.logout':'csh.1','profile':'sh.1','netstart':'rc.8','network.subr':'rc.8','pccard_ether':'rc.8','rc':'rc.8','rc.bsdextended':'rc.8','rc.conf':'rc.conf.5','rc.firewall':'rc.8','rc.initdiskless':'rc.8','rc.resume':'rc.8','rc.shutdown':'rc.8','rc.subr':'rc.8','rc.suspend':'rc.8','locate.rc':'locate.updatedb.8'}
for n,p in shells.items():
 put('/etc/'+n,'MUST','S2.2-10,S2.2-13','Executes shell commands for startup, system management, or environment initialization.',p,'Shell execution gives these scripts the interpreter rights; code remains recordable even when it supplies settings.');rules['R3'].append('/etc/'+n)
# Individual system configuration and lookup objects.
specs={
'aliases':('Maps local mail recipients to delivery destinations or commands.','aliases.5'),
'auto_master':('Assigns automount filesystem paths to mount maps.','auto_master.5'),
'blacklistd.conf':('Sets connection blocking policy for repeated authentication failures.','blacklistd.8'),
'crontab':('Schedules commands executed under designated accounts.','crontab.5'),
'ddb.conf':('Provides commands configuring the kernel debugger.','ddb.8'),
'devd.conf':('Selects commands run in response to device events.','devd.conf.5'),
'devfs.conf':('Sets boot-time device ownership, permissions, and symbolic links.','devfs.conf.5'),
'dhclient.conf':('Controls acquired network addresses and DHCP negotiation.','dhclient.conf.5'),
'disktab':('Describes disk geometries and partition characteristics used to initialize disk labels.','disktab.5'),
'fbtab':('Controls device permissions associated with console login.','fbtab.5'),
'freebsd-update.conf':('Controls installation and removal of operating-system update files.','freebsd-update.conf.5'),
'fstab':('Defines filesystem mounts and mounting options.','fstab.5'),
'gettytab':('Defines terminal characteristics applied by the login-terminal process.','gettytab.5'),
'group':('Defines local groups and account memberships.','group.5'),
'hosts':('Maps network addresses to names for system name resolution.','hosts.5'),
'hosts.allow':('Controls access to network services through wrapper rules.','hosts.allow.5'),
'hosts.equiv':('Identifies trusted remote hosts and users for remote login.','hosts.equiv.5'),
'hosts.lpd':('Authorizes remote hosts to use local printing services.','hosts.lpd.5'),
'inetd.conf':('Configures listening sockets and programs serving incoming connections.','inetd.8'),
'libmap.conf':('Selects substitutions for dynamically loaded shared libraries.','libmap.conf.5'),
'login.access':('Accepts or rejects logins by user, origin, and terminal.','login.access.5'),
'login.conf':('Defines login classes, resource limits, environments, and authentication policy.','login.conf.5'),
'mac.conf':('Defines default security-label elements used across applications.','mac.conf.5'),
'master.passwd':('Defines local accounts and their authentication attributes.','passwd.5'),
'netconfig':('Defines transports and protocols available to RPC library clients.','netconfig.5'),
'networks':('Maps network names to network numbers for network applications.','networks.5'),
'newsyslog.conf':('Controls system log rotation and resulting file permissions.','newsyslog.conf.5'),
'nsmb.conf':('Specifies remote SMB computers, users, shares, and mounting parameters.','nsmb.conf.5'),
'nsswitch.conf':('Selects system-wide sources for account, host, and service lookups.','nsswitch.conf.5'),
'ntp.conf':('Selects time servers and system clock synchronization behavior.','ntp.conf.5'),
'passwd':('Defines local accounts visible through account lookup interfaces.','passwd.5'),
'pf.os':('Supplies operating-system fingerprints for firewall matching and packet analysis.','pf.os.5'),
'phones':('Supplies dialed phone numbers for remote connections.','phones.5'),
'printcap':('Defines printers and print-spooling capabilities.','printcap.5'),
'protocols':('Maps network protocol names to protocol numbers.','protocols.5'),
'pwd.db':('Supplies compiled account records for system account lookups.','pwd_mkdb.8'),
'regdomain.xml':('Defines wireless radio regulatory constraints applied to the system.','regdomain.5'),
'remote':('Defines connection parameters for remote terminal systems.','remote.5'),
'resolv.conf':('Specifies DNS servers and resolver search behavior across programs.','resolv.conf.5'),
'rpc':('Maps RPC program names to their protocol numbers.','rpc.5'),
'services':('Maps network service names to protocol and port numbers.','services.5'),
'shells':('Lists accepted login shells for account and service checks.','shells.5'),
'snmpd.config':('Configures the network management daemon and its modules.','bsnmpd.1'),
'spwd.db':('Supplies protected account records to system authentication routines.','pwd_mkdb.8'),
'sysctl.conf':('Sets kernel state defaults when entering multi-user operation.','sysctl.conf.5'),
'syslog.conf':('Routes system messages to destinations and configured actions.','syslog.conf.5'),
'termcap':('Defines terminal capabilities used by editors and terminal libraries.','termcap.5'),
'termcap.small':('Supplies a reduced terminal-capability database.','termcap.5'),
'ttys':('Configures terminal login processes and terminal access.','ttys.5')}
for n,(w,p) in specs.items():must('/etc/'+n,w,p)
for n in ['group','master.passwd','passwd','pwd.db','spwd.db','login.access','hosts.equiv','inetd.conf','blacklistd.conf']:
 d,s,w,b,r=D['/etc/'+n];D['/etc/'+n]=(d,s+',S2.2-15',w,b,r)
put('/etc/dumpdates','NOT','S2.2-3,S2.2-6','Records dates and levels of previous filesystem dumps.','dump.8','It records past backups; records of the past are explicitly exempt.')
for n in ['motd','motd.template']:
 put('/etc/'+n,'NOT','S2.2-3,S2.2-4','Supplies announcement text displayed after login.','motd.5','Removing announcement content leaves login and other computer capabilities available.')
put('/etc/login.conf.db','NOT','S2.2-3,S2.2-5','Caches login capabilities in a hashed lookup database.','cap_mkdb.1','The hashed database accelerates lookup of the available text database; the cache exemption applies.')
put('/etc/nscd.conf','NOT','S2.2-3,S2.2-7,S2.2-13','Sets internal name-service cache sizes, lifetimes, and worker counts.','nscd.conf.5','Values configure caching inside one daemon; they do not constitute the cached accounts or network definitions.')
put('/etc/os-release','NOT','S2.2-3,S2.2-4','Describes operating-system identity and attributes as informational values.','os-release.5','This is descriptive content; removing it removes identification content rather than the operating system capabilities.')
put('/etc/rmt','MUST','S2.2-2,S2.2-9','Provides an executable path to the remote tape protocol service.','rmt.8','Removing this executable entrypoint prevents invoking the remote tape service through that path.')
for n in ['autofs','bluetooth','cron.d','defaults','devd','dma','gss','kyua','mail','mtree','newsyslog.conf.d','ntp','pam.d','periodic','pkg','ppp','rc.d','security','ssh','ssl','syslog.d','unbound']:unknown('/etc/'+n)
put('/etc/mail','MIXED','S2.2-2,S2.2-4,S2.2-10,S3-2','Contains mail control files, build instructions, and documentation.',None,'README: NOT content; Makefile: MUST executable build commands; aliases: MUST delivery routing. Unlisted members cannot be classified from samples.')
put('/etc/pam.d','MIXED','S2.2-2,S2.2-4,S2.2-15,S3-2','Contains authentication policies and documentation.',None,'README: NOT documentation; atrun, cron, ftp: MUST authentication policy. Unlisted members cannot be identified from the abbreviated inventory.')
put('/etc/hostid','MUST','S2.2-1,S2.2-2','Supplies the saved UUID used to set kernel identity.',None,'The startup script uses the saved value for kernel identity; removal permits a different generated identity.')
put('/etc/machine-id','MUST','S2.2-1,S2.2-2','Defines the local system UUID required by the message bus.',None,'Documented as required for the message bus, this identity participates in system communication rather than descriptive content.')
put('/etc/ftpusers','MUST','S2.2-1,S2.2-2,S2.2-15','Restricts accounts permitted to log into the FTP service.','ftpd.8','Account login authorization is explicitly recordable; this access restriction affects service access.')
put('/etc/libalias.conf','UNKNOWN','S3-2','Configuration path associated with network address translation; actual instructions remain unestablished.',None,'The library purpose is known, but available evidence does not establish this file format, contents, or use.')
put('/etc/mail.rc','UNKNOWN','S3-2','Startup input for the mail command; actual settings or executable commands are unavailable.','mail.1','The startup language permits commands; missing contents prevent distinguishing internal preferences from executable actions.')
assert set(D)=={r['name'] for r in rows},(set(r['name'] for r in rows)-set(D),set(D)-set(r['name'] for r in rows))
# Append completed records, preserving any prior completed rows.
out=base/'part-6.2.tsv';header=['id','decision','sentences','what_it_does','basis','reason']
seen=set()
if out.exists():seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')}
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not out.stat().st_size:w.writerow(header);f.flush()
 for r in rows:
  if r['id'] in seen:continue
  d=D[r['name']];assert len(d[2].split())<=15,(r['name'],d[2]);assert len(d[4].split())<=30,(r['name'],d[4]);w.writerow([r['id'],*d]);f.flush()
print(collections.Counter(d[0] for d in D.values()))
# Build notes with exact text citations and concise documentary excerpts.
notes=['# Part 6: boot and system configuration subset','', 'Decisions use Section 2.2 and S3-2. No removal test was run. Inventory file contents are unavailable; listed paths establish roles only where standard documentation identifies them. Evidence n counts sometimes exceed the members field; partial directory inventories are not assumed homogeneous.','', '## Rules','', 'R1: explicitly enumerated boot executables are MUST under S2.2-1, S2.2-2 and S2.2-9. Their removal eliminates the corresponding available boot code.','', 'R2: Forth scripts and their entrypoints are MUST under S2.2-10 and S2.2-13. The loader executes them; display-producing code remains code.','', 'R3: explicitly enumerated shell scripts and shell-sourced files are MUST under S2.2-10 and S2.2-13. Shell rights are not restricted to a program interface.','']
for rule,names in rules.items():
 notes.append(rule+' hand checks (path and inventory identity checked individually):')
 for n in names[:10]:notes.append('- '+next(r['id'] for r in rows if r['name']==n)+' — '+n+' — '+D[n][2])
 notes.append('')
notes+=['All other mappings are individual decisions. Unknown directory contents are not assigned a homogeneous classification. MIXED identifies already established different members while explicitly leaving unlisted members unresolved.','', '## Numbered sentences','']
used=set(s for d in D.values() for s in d[1].split(','))
for line in pathlib.Path('SENTENCES.md').read_text().splitlines():
 if any('**'+s+'**' in line for s in used):notes.append(line)
notes+=['','## Documentation','']
sources=json.load(open(base/'part-6.2.sources.json'))
for k,x in sources.items():
 if not x['excerpt'].startswith('Sorry'):
  notes+=['- '+x['url']+' — "'+x['excerpt']+'"']
notes+=['','Additional primary sources:','- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/man/man7/hier.7 — "defines the UUID for the local system, required for dbus"; "configuration files for the Pluggable Authentication Modules (PAM) library".','- https://raw.githubusercontent.com/freebsd/freebsd-src/main/stand/forth/Makefile — "FILES+= beastie.4th" and "FILES+= loader.4th" identify installed loader script names (whitespace normalized).','- https://raw.githubusercontent.com/freebsd/freebsd-src/main/libexec/rc/rc.d/hostid — "If ${hostid_file} already exists, we take UUID from there."','- https://raw.githubusercontent.com/freebsd/freebsd-src/main/usr.bin/locate/locate/updatedb.sh — ". $LOCATE_CONFIG" demonstrates shell sourcing of locate settings.','', 'Boot script execution, system configuration effects, and directory membership are distinct facts. A documented general directory role does not establish the complete collection actually stored on the inventoried machine.','']
(base/'part-6.2.notes.md').write_text('\n'.join(notes))
