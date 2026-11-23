import csv,re,collections
from pathlib import Path
rows=list(csv.DictReader(open('A1/compare/joined.tsv'),delimiter='\t'))
adj={r['id']:r for r in csv.DictReader(open('A1/adjudication/rows.tsv'),delimiter='\t')}
out={}
def add(r,status,why,source):
 out[r['id']]={'id':r['id'],'kind':r['kind'],'name':r['name'],'extent_status':status,'qualification':why,'evidence':source,'same':r['same']}
# Every original anchor is inspected, preserving any constituent limitation.
for r in rows:
 a=adj.get(r['id'],{})
 if a.get('hole')=='1':
  n=a['note'];status='CONFIRMED-CONSTITUENT' if any(x in n for x in ['HOLE A:','HOLE:','MEMBERS','MUST:','NOT:']) else 'CONFIRMED-STANDALONE'
  add(r,status,n,'A1/adjudication/rows.tsv; '+r['evidence'])
  if r['id'] in ['nixos-a332c16c0a','nixos-334b6692d5']:
   add(r,'FACTUAL-UNKNOWN','nix.conf is used by both CLI and daemon according to adjudication evidence; whether these constitute one executing program is not established. Not counted as a one-program setting.','A1/adjudication/rows.tsv')
# Exact additional rows: known one-program value input, with a stated external effect.
adds={
'coreos-29d771e7fa':'Configuration-only sysctl package: systemd-sysctl applies kernel.yama.ptrace_scope to kernel cross-process tracing policy.',
'debian-6551aee88e':'Configuration-only session bus package; session.conf is read by the session bus and governs communication/activation of other applications.',
'debian-446f7db4a6':'mke2fs reads filesystem feature defaults that govern the filesystems it creates, matching the CoreOS mke2fs anchor.',
'debian-9cf6463675':'update-ca-certificates reads the CA selector and builds the trust bundle used by TLS applications.',
'ubuntu-9cf6463675':'update-ca-certificates reads the CA selector and builds the trust bundle used by TLS applications.',
'debian-bbe4c8f871':'netplan reads the saved YAML and produces interface configuration; same named configuration as original package-owned netplan anchor.',
'ubuntu-bbe4c8f871':'netplan reads saved YAML and produces backend network interface configuration.',
'debian-f4c9cf7ef7':'systemd-tmpfiles reads screen directory rules; creates /run/screen with mode1777 for another program.',
'ubuntu-f4c9cf7ef7':'systemd-tmpfiles reads screen runtime-directory cleanup/creation rules affecting the filesystem used by screen.',
'nixos-7ab5b73f41':'sysctl.d links contain the separately inventoried sysctl rules applied by systemd-sysctl to kernel parameters.',
'ubuntu-7ab5b73f41':'systemd-sysctl applies the inventoried IPv6 parameter values to the kernel.',
'nixos-16e3948c30':'install-grub reads grub-config.xml as values to generate bootloader configuration.',
'guix-669b5718ae':'udevd reads udev.conf selecting the active device-rules directory; determines device management outside the daemon.',
'guix-f7c3371071':'sysctl reads sysctl.conf values to set kernel operating parameters.',
'guix-806b5ff18e':'Single account-creation tool PAM service; matching Guix rootok service rule and fallback other/pam_deny documented in facts-K2.',
'guix-16d77a812e':'PAM service read by chfn for permission to change account information; effects concern account records, not only chfn.',
'alpine-46b7935e7d':'mkinitfs reads feature lists to select modules included in generated boot images.',
'freebsd-9a8da13e5c':'newsyslog reads rotation values controlling rotation and permissions of other programs log files.',
'freebsd-1166c4aa4a':'mtree reads base-hierarchy specifications as values and creates the filesystem hierarchy; original card2 functional-loss example.',
}
unknowns={
'debian-cf102b2bab':'locale-gen is the reader and generated locales affect other programs; exact enabled lines/removal effect require inspection.',
'ubuntu-cf102b2bab':'locale-gen is the reader and generates shared locales; evidence says exits if missing but active selections are not captured here.',
'alpine-8809189527':'EXTLINUX reads boot selection values; distinguish device boot order explicitly named by S2.2-16 from kernel/menu parameters before counting.',
'alpine-1dc18c9809':'apk reads repositories/world/architecture; mixed package-manager state and configuration need member separation.',
'ubuntu-f3f8b50a94':'initramfs module list appears to affect generated image; exact active directives are not established.',
'ubuntu-6245454f68':'mdadm configuration can affect arrays; exact non-default array definitions and readers unestablished.',
'freebsd-50a05876e0':'loader configuration may include executable loader commands or plain values; exact contents and distinction from explicit boot order not established.',
'freebsd-83d81e4cca':'Device hints passed into kernel; multiple possible readers and exact active hardware effects not established.',
'freebsd-19082d7c49':'devfs.conf affects node modes and links; exact parser and active directives not captured.',
'freebsd-1996d2e6ea':'dhclient.conf can alter system network; content may be comments/defaults and exact non-default effect unestablished.',
'freebsd-f9029ebf38':'freebsd-update.conf can control filesystem changes; distinguish shell sourcing from value parsing before counting.',
'freebsd-4c9798c002':'nsmb.conf may be used by multiple SMB tools; one-reader premise unestablished.',
'freebsd-a2259a4339':'ntpd configuration includes time sources and possibly explicit open-port/access rules; exact member effects unestablished.',
'freebsd-691aa913ee':'sysctl.conf may have only commented defaults; actual active values unestablished.',
'freebsd-3f48fc0892':'syslog.conf routes logs but may contain executable action syntax; exact contents unestablished.',
'freebsd-4b9bab7bca':'auto_master values govern mounts; multiple automount tools and exact use unestablished.',
'freebsd-57b67ff179':'disktab may serve several disk tools; one-reader premise unestablished.',
'freebsd-3c9edc761b':'printcap used by lpd and printing clients; one-reader premise unestablished.',
'freebsd-0cfe0a7601':'Wireless regulatory data; device applicability and exact reader unestablished.',
'freebsd-4be88090f4':'gettytab terminal settings can affect kernel terminal state; exact non-default values unestablished.',
'freebsd-5f6bb69053':'fbtab device permissions affect other applications; relation to explicit login rules and active console configuration unestablished.',
'guix-a5a1d4c84c':'PulseAudio flat-volumes=no affects mixing shared by clients; whether interface-confined setting or system-device state is the relevant effect requires exact reader/effect evidence.',
'coreos-98660c121d':'vconsole configuration also read by localed; one-reader premise not established.',
'arch-1ef4d5e9cf':'vconsole configuration also read by localed; one-reader premise not established.',
'ubuntu-1ef4d5e9cf':'vconsole/keyboard link has possible multiple readers and defaults; exact behaviour unestablished.',
'guix-d4230c6ee7':'udev rules can mix value assignments and executable RUN/PROGRAM actions; exact member separation is not available.',
'guix-cf4cde143a':'udev tree mixes rules and configuration; exact constituent one-program values not established.',
'guix-561d6a5935':'udev tree mixes rules and configuration; exact constituent one-program values not established.',
'nixos-561d6a5935':'udev tree mixes multiple-reader hwdb and executable rules with values; exact candidate constituent not established.',
'guix-af3d16f493':'D-Bus activation files hold Exec values rather than being Scheme/shell source; exact inline payload/port/login clauses need inspection.',
'coreos-1ba388a08e':'LVM system.devices may be maintained program state; no exact configuration/state separation established.',
}
for r in rows:
 if r['id'] in adds:add(r,'CONFIRMED-STANDALONE',adds[r['id']],'A1/compare/joined.tsv descriptions and '+r['evidence'])
 if r['id'] in unknowns:add(r,'FACTUAL-UNKNOWN',unknowns[r['id']],'A1/compare/joined.tsv; '+r['evidence'])
 # Preserve all already unresolved config facts for this family, without converting them into holes.
 a=adj.get(r['id'],{})
 if a.get('verdict')=='UNKNOWN' and r['kind'] in ['stored','package-owned-paths'] and re.search(r'conf|modprobe|netplan|udev|/etc/dma|/etc/samba|/etc/python|/etc/keys|/etc/pkg|evolution',r['name']):
  add(r,'FACTUAL-UNKNOWN',a['note'],'A1/adjudication/rows.tsv; '+r['evidence'])
 # Stored native unit configuration is parsed as values, unlike separate unit-script outputs.
 if r['kind']=='system-closure-store-object' and '-unit-' in r['name'] and '-unit-script-' not in r['name']:
  unit=r['name'].split('-unit-',1)[1]
  if unit.endswith('.socket'):
   add(r,'EXCLUDED-EXPLICIT','Socket configuration supplies connection endpoints, covered by explicit S2.2-15; not counted in this hole.',r['evidence'])
  elif 'firewall' in unit or 'sshd' in unit or 'suid-sgid' in unit:
   add(r,'EXCLUDED-EXPLICIT','The named configuration directly implements firewall, remote login or superuser-right mechanisms explicitly covered by S2.2-15.',r['evidence'])
  else:
   add(r,'CONFIRMED-STANDALONE','Stored '+unit+' is a value-parsed native unit configuration; systemd uses it to control other processes, activation, mounts or resource allocation. ExecStart values identify a separate executed program; they do not make this unit file executed source code.','A1/in/raw/nixos/unit-realpaths.tsv; '+r['evidence']+'; systemd.service/target/timer/mount documentation')
 if r['id'] in ['nixos-ee908f90c5','nixos-b9f001fe55']:
  add(r,'CONFIRMED-CONSTITUENT','Tree includes the separately inventoried native unit value files; count row coverage once, not every contained unit again.','A1/in/raw/nixos/unit-realpaths.tsv; '+r['evidence'])
 # Potential PAM analogues cannot be inferred to fail without their exact fallback policy.
 if r['kind']=='system-closure-store-object' and r['name'].endswith('.pam'):
  name=r['name'].split('/')[-1][33:-4]
  if name in ['usermod','groupadd','groupmems','chfn','chsh','chpasswd','groupdel','userdel','useradd','groupmod','vlock','passwd']:
   add(r,'FACTUAL-UNKNOWN','Single-tool PAM value file analogous to Guix card anchors; exact policy and fallback difference on this system not established.',r['evidence'])
# Unit inventory rows are file definitions when their own evidence explicitly supplies a fragment.
for r in rows:
 if r['kind'] not in ['system-unit','user-unit']:continue
 a=adj.get(r['id'],{})
 if a.get('hole')=='5':
  add(r,'EXCLUDED-STATE','No-fragment runtime reflection; card5 is outside definition under S2.5-1.',r['evidence']);continue
 if a.get('verdict')=='RESOLVED:NOT':
  add(r,'EXCLUDED-FACT',a['note'],'A1/adjudication/rows.tsv; '+r['evidence']);continue
 if a.get('verdict')=='UNKNOWN':
  add(r,'FACTUAL-UNKNOWN',a['note'],'A1/adjudication/rows.tsv; '+r['evidence']);continue
 ev=r['evidence']
 hasfile=bool(re.search(r'fragment=/[^; ]+',ev) or re.search(r'FragmentPath[^/]{0,20}/',ev))
 if not hasfile:
  add(r,'FACTUAL-UNKNOWN','Unit file definition is not established by a nonempty fragment path in this row evidence; runtime reflection alone does not establish a settings-file example.',ev);continue
 if r['name'].endswith('.socket') or any(t in r['name'] for t in ['firewall','sshd','ssh-access','sudo','suid-sgid']):
  add(r,'EXCLUDED-EXPLICIT','Connection endpoint, firewall, login or superuser-right mechanism has an explicit S2.2-15 recording clause.',ev);continue
 add(r,'CONFIRMED-STANDALONE','File-backed '+r['name']+' definition identified by its fragment path; systemd parses settings that control another process, mount, activation dependency or resource allocation. Native unit file is not the child executable. Active-now status is not a condition of the removal-capability test.',ev+'; systemd unit-type documentation')
for r in rows:
 if r['kind'] in ['system-units','user-units'] and r['name'].endswith(('*.mount','*.automount')):
  add(r,'FACTUAL-UNKNOWN','Grouped generated/synthesized mount units may mix file-backed configuration and runtime reflections. The row does not map each member to its fragment; do not infer either blanket membership or blanket state exemption.',r['evidence'])
# Final boundary review: client settings and manager enablement selectors.
for r in rows:
 if r['id']=='nixos-6cad6264ed':
  add(r,'CONFIRMED-STANDALONE','ssh reads connection-policy values; they select external connections. The same inside-reader versus external-effect boundary applies, without an explicit clause recording these client options.','A1/adjudication/rows.tsv; '+r['evidence'])
 if r['id'] in ['coreos-c366c1919d','debian-c366c1919d','nixos-0075a76d48']:
  add(r,'CONFIRMED-CONSTITUENT','ssh_config client-settings constituent has the same one-reader/external-connection boundary; sshd_config and authorized login keys remain explicit MUST separately.','A1/adjudication/rows.tsv; '+r['evidence'])
 if r['name']=='/etc/systemd' and r['kind'] in ['stored','package-owned-paths']:
  a=adj.get(r['id'],{}); note=a.get('note',r['c2_what'])
  if any(x in note.lower() for x in ['enablement','enable','unit dirs']):
   prior=out.get(r['id'],{}).get('qualification','')
   add(r,'CONFIRMED-CONSTITUENT',prior+' Manager enablement-link values select which other units start; known generated scripts and explicit login/port rules are separate members.','A1/adjudication/rows.tsv and A1/compare/joined.tsv; '+r['evidence'])
 if r['name']=='/var/lib/systemd' and r['kind'] in ['stored','package-owned-paths']:
  note=adj.get(r['id'],{}).get('note','')
  if 'linger' in note and not r['id'].startswith('ubuntu-'):
   add(r,'CONFIRMED-CONSTITUENT','Known linger selector is read by the service manager and enables another user-manager process at boot; remaining timer stamps/seeds are separately excluded as state.','A1/adjudication/rows.tsv; '+r['evidence'])
  elif r['id'].startswith('ubuntu-'):
   add(r,'FACTUAL-UNKNOWN','Most members not inventoried; a linger selector is possible but not established.',r['evidence'])
 if r['id'] in ['freebsd-0075a76d48','alpine-0075a76d48','arch-0075a76d48']:
  add(r,'FACTUAL-UNKNOWN','Known host keys are state; exact presence and active values of a separate ssh client configuration constituent are not established.','A1/adjudication/rows.tsv; '+r['evidence'])
# Audit of the single-reader premise and names that do not establish explicit-clause content.
for r in rows:
 old=out.get(r['id'],{})
 if old.get('extent_status')=='EXCLUDED-EXPLICIT' and (r['kind'] in ['system-unit','user-unit'] or '-unit-' in r['name']):
  if r['name'].endswith('.socket'):
   add(r,'FACTUAL-UNKNOWN','Socket unit is value configuration; exact network port versus Unix/FIFO/device endpoint and applicable explicit S2.2-15 clause are not established from its name. Do not exclude or confirm solely by suffix.',r['evidence'])
  else:
   add(r,'CONFIRMED-STANDALONE','File-backed manager unit is a settings object controlling another process; service name mentioning login/firewall does not turn its manager values into the separate explicit login/firewall rule object.',r['evidence']+'; systemd.service documentation')
 if r['id'] in ['nixos-4d1b734b98','nixos-2009ac3ba5','nixos-8d44cbf2f9','nixos-7ab5b73f41','coreos-29d771e7fa']:
  add(r,'EXCLUDED-MULTIPLE-READERS','Both systemd-sysctl and the installed procps sysctl --system can read these sysctl.d values. One-program exemption premise is false; kernel-parameter effects satisfy S2.2-2.','A1/in/raw/nixos/system-closure.txt or A1/in/raw/coreos/packages.tsv; https://man7.org/linux/man-pages/man8/sysctl.8.html; '+r['evidence'])
 if r['id'] in ['nixos-3f6895f897','nixos-5bcb04cfbe']:
  add(r,'FACTUAL-UNKNOWN','Preset values are applied through systemctl preset and possibly first-boot manager code; exact distinct reader paths not established, so the original single-reader anchor is not presumed.',r['evidence'])
 if r['id'] in ['coreos-4c24122c97','guix-9a671be062','guix-5d1d3b6b13']:
  add(r,'FACTUAL-UNKNOWN','Skeleton may contain directly executable or sourceable shell-startup files; copying is its ordinary role but does not establish absence of code under S2.2-10/13. Exact member treatment not established.',r['evidence'])
 if r['id']=='debian-a349a8354f':
  add(r,'FACTUAL-UNKNOWN','Kernel-image configuration is described as read by kernel install scripts in plural; exact one-reader premise not established.','A1/adjudication/rows.tsv; '+r['evidence'])
for r in rows:
 if r['id']=='coreos-160df5d64d':
  add(r,'FACTUAL-UNKNOWN','nftables-services package evidence identifies service/configuration and .nft filenames, but does not establish actual rule contents or exact single-reader composition. Explicit firewall rules and manager settings cannot be separated from names alone.',r['evidence']+'; A1/compare/joined.tsv')
# Final independent accuracy corrections, without broadening the candidate set.
for r in rows:
 if r['id'] in ['arch-c5c3eb977b','silverblue-dc8fe5998a','ubuntu-96787848d5','debian-desktop-96787848d5','debian-desktop-0758efc3b0','debian-desktop-53d095e912','debian-desktop-fdb6cb41a8','debian-desktop-ba3d3e02a2','debian-desktop-7218a536a4']:
  add(r,'EXCLUDED-STATE','Fragment is runtime generator output or transient manager state under /run; a nonempty fragment alone does not establish a persistent settings definition. Treatment of this generated state is outside under S2.5-1.',r['evidence']+'; A1/review/final-boundaries.md')
 if r['id']=='ubuntu-7ab5b73f41':
  add(r,'FACTUAL-UNKNOWN','systemd-sysctl applies these IPv6 values, but absence of an additional procps sysctl --system reader is unproved; exact single-reader premise remains unestablished.',r['evidence']+'; A1/review/final-boundaries.md')
fields=['id','kind','name','extent_status','qualification','evidence','same']
with open('A1/review/hole-1-extent.tsv','w') as f:
 w=csv.DictWriter(f,fields,delimiter='\t');w.writeheader();w.writerows(out[r['id']] for r in rows if r['id'] in out)
print(collections.Counter(x['extent_status'] for x in out.values()))
print('confirmed same',collections.Counter(x['same'] for x in out.values() if x['extent_status'].startswith('CONFIRMED')))
# Every table row receives a scope disposition; this is a reproducible exhaustive traversal, not a claim that names prove unrecorded facts.
with open('A1/review/hole-1-scan.tsv','w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['id','kind','name','scope_disposition'])
 for r in rows:
  if r['id'] in out:why=out[r['id']]['extent_status']+'; see hole-1-extent.tsv'
  elif r['kind'] in ['system-unit','user-unit','system-units','user-units','system-service','rc-service','openrc-service']:
   why='MANAGED-OBJECT: service/unit inventory names a managed operation or runtime reflection, not a separately inventoried stored value file; do not silently retype as config file.'
  elif r['kind'] in ['account','account-group','kernel-module','process','user-profile-package']:
   why='NON-SETTING: account, executing program or kernel code; explicit recording provisions or separate object type.'
  elif r['id'] in adj:why='OTHER-CASE: '+adj[r['id']]['note']
  else:why='OTHER-CASE: '+r['c1_what']+'; '+r['c2_what']
  w.writerow([r['id'],r['kind'],r['name'],why])
