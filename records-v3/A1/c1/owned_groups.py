from owned_build import *
# Individually inspected group partitions. Dirs initially UNKNOWN; necessary ancestors of MUST members MUST.
# Each entry: group, file default, member selector overrides, function.
data='''
/boot/grub2|MUST|NOT:*/unicode.pf2|Provides boot menu code, boot variables, and display font
/etc/NetworkManager|MUST||Configures network management and executes network-event hooks
/etc/X11|MUST||Runs session-startup shell integration
/etc/audit|MUST|HOLE:*/auditd.conf|Sets kernel audit rules and audit-daemon preferences
/etc/authselect|MUST|UNKNOWN:*/authselect.conf;UNKNOWN:*/dconf-db;UNKNOWN:*/dconf-locks|Supplies authentication stacks and name-service selection
/etc/bash_completion.d|MUST||Executes shell completion functions
/etc/cifs-utils|UNKNOWN||Selects an identity-mapping plugin through a symbolic link
/etc/containerd|HOLE||Configures container-runtime behavior
/etc/containers|UNKNOWN||Stores container trust, registry, and toolbox configuration
/etc/crypto-policies|MUST||Distributes cryptographic policy to multiple program backends
/etc/dbus-1|MUST||Configures message-bus connectivity and interprocess access policy
/etc/default|MUST||Supplies defaults used when creating accounts
/etc/dnf|HOLE|NOT:*/README|Stores package-manager configuration and explanatory documentation
/etc/fwupd|HOLE|NOT:*/README.md|Stores firmware-update daemon settings and explanatory documentation
/etc/grub.d|MUST|NOT:*/README|Executes boot-configuration generator scripts and includes explanatory documentation
/etc/gss|UNKNOWN||Configures an authentication mechanism plugin
/etc/gssproxy|UNKNOWN||Stores authentication-proxy configuration
/etc/iproute2|NOT||Provides explanatory documentation for networking configuration
/etc/iscsi|UNKNOWN||Stores storage-session daemon configuration
/etc/keys|MUST||Supplies integrity-verification certificates
/etc/kmscon|NOT||Provides an example terminal configuration
/etc/krb5.conf.d|MUST||Includes shared authentication and cryptography configuration
/etc/ld.so.conf.d|MUST||Adds shared-library discovery directories
/etc/libblockdev|UNKNOWN||Selects block-device library configuration
/etc/libibverbs.d|UNKNOWN||Stores driver-selection values for userspace RDMA
/etc/libnl|UNKNOWN||Supplies network library identifier tables
/etc/libreport|UNKNOWN||Stores event-handler configuration
/etc/logrotate.d|UNKNOWN||Configures log processing, potentially including executed hook code
/etc/lvm|HOLE||Stores volume-manager defaults and optional profiles
/etc/nftables|UNKNOWN||Stores firewall rule files and operating-system fingerprint data
/etc/nmstate|NOT||Provides explanatory network-state documentation
/etc/nvme|UNKNOWN||Stores storage-discovery configuration
/etc/openldap|MUST||Supplies defaults shared by LDAP clients
/etc/pam.d|MUST||Defines authentication and account-access stacks
/etc/pki|UNKNOWN|NOT:*/README;MUST:*/ca-trust/extracted/*.pem;MUST:*/ca-trust/extracted/*.crt;MUST:*/ca-trust/extracted/java/cacerts;MUST:*/tls/certs/*.crt;MUST:*/tls/certs/*.pem;MUST:*/tls/certs/*.0;MUST:*/tls/misc/*.sh|Stores trust anchors, cryptographic configuration, scripts, and explanatory documents
/etc/profile.d|MUST||Executes shell initialization scripts
/etc/rc.d|NOT||Provides explanatory initialization documentation
/etc/request-key.d|MUST||Selects helpers for kernel key requests
/etc/rwtab.d|UNKNOWN||Stores writable-filesystem setup descriptions
/etc/samba|UNKNOWN|NOT:*/smb.conf.example|Stores file-sharing configuration and a sample configuration
/etc/security|MUST|HOLE:*/opasswd|Controls authentication, account resources, namespaces, and password history
/etc/selinux|MUST|UNKNOWN:*/.policy.sha512;NOT:*/file_contexts*.bin|Stores access-control policy, labels, and compiled label caches
/etc/skel|MUST||Supplies shell startup code copied into new accounts
/etc/ssh|MUST|HOLE:*/ssh_config;HOLE:*/ssh_config.d/*;UNKNOWN:*/moduli|Controls login access and SSH client behavior
/etc/ssl|MUST|NOT:*/README;UNKNOWN:*/ct_log_list.cnf;UNKNOWN:*/openssl.cnf|Exposes shared trust bundles and cryptographic configuration
/etc/swid|NOT||Exposes software-identification metadata
/etc/sysconfig|UNKNOWN|MUST:*/arptables;MUST:*/ip6tables;MUST:*/iptables;MUST:*/selinux|Stores firewall policy and service-startup options
/etc/sysctl.d|MUST||Exposes persistent kernel parameter configuration
/etc/tpm2-tss|UNKNOWN||Stores TPM library configuration and cryptographic profiles
/etc/udev|MUST||Supplies compiled hardware properties for device setup
/etc/udisks2|UNKNOWN|NOT:*/mount_options.conf.example|Stores disk-management settings and a sample configuration
/etc/xdg|UNKNOWN||Exposes desktop autostart and user-service search locations
/etc/yum.repos.d|HOLE||Sets software package repository sources
/var/cache/ldconfig|NOT||Stores an auxiliary cache for rebuilding the library index
/var/lib/chrony|HOLE||Persists measured clock drift used for future time correction
/var/lib/dnf|UNKNOWN||Provides a package-manager locking object
/var/lib/gssproxy|UNKNOWN||Exposes an authentication-proxy socket and storage directories
/var/lib/systemd|UNKNOWN|NOT:*/catalog/database;MUST:*/random-seed|Stores message catalog data, boot entropy seed, and service-state directories
'''
import fnmatch
members_file=base/'part-1.owned.members.tsv'
with members_file.open('w') as mf, (base/'part-1.owned.notes.md').open('a') as notes:
 mw=csv.writer(mf,delimiter='\t',lineterminator='\n');mw.writerow(['id','member_ordinal','type','decision'])
 notes.write('\n## Individually inspected grouped objects\n\nThe member table `part-1.owned.members.tsv` gives every member’s decision. Ordinals use the order of normalized intersection entries in raw `files.tsv`, excluding nested groups. Paths are intentionally not duplicated. Directory members are UNKNOWN unless they are ancestors necessary to reach a classified MUST member; such ancestors are MUST because removing them removes access to that required object. Unused sibling directories remain UNKNOWN. The table below records the individually selected file classes and exceptions; these selections are not a classifier inferred from package ownership.\n\nAncestor checks by hand: coreos-9945c88deb (dispatcher script), coreos-0a38e83850 (session shell script), coreos-47cc2958ff (completion scripts), coreos-96885714dc (backend policy links), coreos-ec5f04bd95 (bus configuration), coreos-4f3962b16e (account defaults), coreos-b91b989f2d (generator scripts), coreos-8265490c79 (library path configuration), coreos-cbdd239882 (authentication stacks), coreos-2f70798fb0 (shell startup scripts). In each, direct pathname prefixes identify exactly the needed containing directories; sibling directories do not inherit the child’s decision.\n\n')
 for line in data.strip().splitlines():
  name,default,overrides,what=line.split('|');row=next(r for r in rows if r['name']==name);m=groups[row['id']];cl=[]
  for x in m:
   d='UNKNOWN' if x[0]=='d' else default
   if x[0]!='d':
    for override in overrides.split(';'):
     if override:
      dec,patt=override.split(':',1)
      if fnmatch.fnmatch(x[1],patt):d=dec
   cl.append(d)
  required=[x[1] for x,d in zip(m,cl) if d=='MUST']
  for i,x in enumerate(m):
   if x[0]=='d' and any(p.startswith(x[1]+'/') for p in required):cl[i]='MUST'
  kinds=set(cl);decision=next(iter(kinds)) if len(kinds)==1 else 'MIXED'
  if decision=='MIXED':reason='Member decisions differ: '+', '.join(sorted(kinds))+'. Exact ordinal partition is in part-1.owned.members.tsv; reasons and documented functions are in notes.'
  elif decision=='MUST':reason='Required code, access rules, or shared system behavior depends on these members; containing directories provide necessary access to those required objects.'
  elif decision=='NOT':reason='Only explanatory content is lost, or only a regenerable auxiliary index is lost; no new operational capability is removed.'
  elif decision=='UNKNOWN':reason='Inventory establishes paths but not their actual functional contents or consumers; available format documentation does not determine these particular members’ roles.'
  else:reason='Values configure one program but alter external behavior; the text does not define the boundary of settings in force inside one program.'
  sent='S2.2-1,S2.2-2,S2.2-4,S2.2-7,S2.2-10,S3-2'
  if name=='/etc/security':sent+=',S2.2-6,S2.2-15'
  if name=='/var/lib/chrony':sent='S2.2-1,S2.2-5,S2.2-6'
  append(row,decision,sent,what,'raw:coreos/files.tsv',reason)
  for i,(x,d) in enumerate(zip(m,cl),1):mw.writerow([row['id'],i,x[0],d])
  counts=collections.Counter(cl);notes.write('- '+row['id']+': '+what+'. '+', '.join(f'{d}={n}' for d,n in sorted(counts.items()))+'.\n')
print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))
