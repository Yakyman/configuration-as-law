from owned_build import *
data='''
/etc/GREP_COLORS|UNKNOWN|Stores color-related material whose parsing method is unestablished|S2.2-7,S2.2-10,S2.2-13,S3-2|The inventory omits contents and the consuming script; values-only interpretation versus sourced shell code cannot be established.
/etc/azure-ephemeral-disk-setup.conf|MUST|Configures ephemeral disk aggregation, formatting, and mounting|S2.2-1,S2.2-2,S2.2-13|Documented values select filesystem creation and mounts affecting the system and other programs.
/etc/bindresvport.blacklist|UNKNOWN|Lists reserved-port exclusions for library implementations|S2.2-1,S2.2-15,S3-2|Documentation shows implementation-dependent support; inventory does not establish which listed restrictions are consumed.
/etc/chrony.conf|MUST|Configures system clock synchronization and time service|S2.2-1,S2.2-2|System time and network time service affect other programs, beyond an internal program preference.
/etc/dhcp|MUST|Executes a DHCP event shell hook for clock synchronization|S2.2-10,S2.2-13|The sole member is a shell hook executed with interpreter rights.
/etc/dnsmasq.conf|MUST|Configures DNS, address allocation, and network services|S2.2-1,S2.2-2,S2.2-15|Network availability and service exposure change, exceeding a setting confined to one program.
/etc/dracut.conf|HOLE|Sets initialization-image construction parameters|S2.2-1,S2.2-7,S2.2-13|Values are consumed by one builder but determine boot-image behavior; the text does not define the boundary of inside one program.
/etc/environment|MUST|Sets environment values inherited by login sessions|S2.2-1,S2.2-13|Session environment influences multiple child programs; it is not a setting confined to one application.
/etc/ethertypes|UNKNOWN|Stores Ethernet protocol identifiers with unestablished consumers|S2.2-1,S2.2-4,S3-2|Neither content nor consumer trace establishes whether this instance supplies operational lookup or merely reference data.
/etc/fedora-release|HOLE|Provides operating-system release identification|S2.2-1,S2.2-4|Release text can be displayed content or input to behavioral selection; the text supplies no boundary for dual-purpose identification data.
/etc/filesystems|MUST|Lists filesystem types to try during mounting|S2.2-1,S2.2-2|Removing mount-type candidates changes filesystem discovery and possible mounting behavior across the system.
/etc/fuse.conf|MUST|Controls userspace filesystem mounting permissions and limits|S2.2-1,S2.2-2|Permission and mount limits determine operations available to users and applications, beyond an internal display preference.
/etc/grub2-efi.cfg|MUST|Links to bootloader configuration code|S2.2-1,S2.2-2,S2.2-10|The link exposes boot commands; losing the configuration path changes bootloader access to required code.
/etc/grub2.cfg|MUST|Links to bootloader configuration code|S2.2-1,S2.2-2,S2.2-10|The link exposes boot commands; losing the configuration path changes bootloader access to required code.
/etc/idmapd.conf|UNKNOWN|Stores identity-mapping daemon configuration|S2.2-1,S2.2-7,S3-2|Available inventory does not establish actual mapping directives, domain selection, or whether configured consumers use them.
/etc/inittab|UNKNOWN|Stores legacy initialization material of unestablished operational use|S2.2-1,S2.2-4,S3-2|A pathname alone cannot distinguish active initialization instructions from a compatibility explanatory file on this system.
/etc/inputrc|NOT|Sets Readline editing keys and interface preferences|S2.2-7,S2.2-13|Values control the interactive editing interface rather than executing unrestricted shell code.
/etc/kdump.conf|UNKNOWN|Stores kernel-crash dump configuration with unestablished active directives|S2.2-1,S2.2-7,S2.2-10,S3-2|Absent contents prevent distinguishing inactive examples, settings, and configured executable hooks.
/etc/krb5.conf|MUST|Sets shared Kerberos realms, server locations, and authentication defaults|S2.2-1,S2.2-2|The shared authentication configuration affects multiple applications and available authentication paths.
/etc/ld.so.cache|UNKNOWN|Indexes library paths for the dynamic loader|S2.2-1,S2.2-2,S2.2-5,S3-2|Missing cache contents prevent determining whether fallback paths suffice or some libraries become undiscoverable; cache naming alone does not prove the exemption.
/etc/magic|UNKNOWN|Stores file-identification patterns of unestablished actual contents|S2.2-1,S2.2-4,S2.2-7,S3-2|Inventory does not reveal whether patterns are present, actively loaded, or merely explanatory material.
/etc/makedumpfile.conf.sample|NOT|Provides sample dump-filter configuration|S2.2-4|A sample configuration is explanatory content; the evidence establishes no use as active configuration.
/etc/mtab|MUST|Exposes live mount information through a procfs link|S2.2-1,S2.2-2|The symlink supplies current mount discovery to utilities; it is not a record of past events.
/etc/nanorc|NOT|Sets editor preferences, highlighting, and key bindings|S2.2-7,S2.2-13|The documented format supplies editor-interface values and commands, not unrestricted editor-language code.
/etc/netconfig|UNKNOWN|Stores transport descriptions for unestablished RPC consumers|S2.2-1,S2.2-4,S3-2|The collected pathname does not establish actual transport entries or their functional use; available sources do not resolve this instance.
/etc/nsswitch.conf|MUST|Selects name-service sources shared by library consumers|S2.2-1,S2.2-2|Lookup sources affect multiple programs and account resolution, outside the one-program settings exemption.
/etc/printcap|UNKNOWN|Stores printer definitions or compatibility material|S2.2-1,S2.2-4,S2.2-7,S3-2|Contents and printing consumers were not supplied; active printer selection cannot be distinguished from unused compatibility content.
/etc/profile|MUST|Executes system login-shell startup commands|S2.2-10,S2.2-13|Shell startup files are an explicit required-code example.
/etc/redhat-release|HOLE|Links to system release-identification data|S2.2-1,S2.2-4|Identification can be displayed content or control program decisions; the text does not delimit those two roles for the same data.
/etc/rpm-ostreed.conf|UNKNOWN|Stores deployment-daemon configuration|S2.2-1,S2.2-7,S3-2|Actual directives are absent, preventing separation of active deployment controls, internal preferences, and commented defaults.
/etc/services|MUST|Maps network service names to ports and protocols|S2.2-1,S2.2-2|Shared service-name lookup enables network operations; this file does not itself mean every listed port is open.
/etc/system-release|HOLE|Links to system release-identification data|S2.2-1,S2.2-4|Identification can be displayed content or control program decisions; the text does not delimit those two roles for the same data.
/etc/system-release-cpe|HOLE|Provides machine-readable platform identification|S2.2-1,S2.2-4|The same identification can be descriptive content or drive software selection; no sentence distinguishes these readings.
/etc/trusted-key.key|UNKNOWN|Stores a cryptographic key of unestablished actual use|S2.2-1,S2.2-14,S2.2-15,S3-2|The inventory supplies neither key contents nor its consumer; a key pathname alone does not establish login authorization or another role.
/etc/virc|MUST|Executes editor initialization commands|S2.2-10,S2.2-13|Editor configuration in the editor command language is explicitly required code despite configuring preferences.
/etc/xattr.conf|UNKNOWN|Stores extended-attribute handling material with unestablished active consumers|S2.2-1,S2.2-7,S3-2|Collected metadata does not establish actual directives or whether they govern operational copying, internal preferences, or unused examples.
/var/lib/.ssh-host-keys-migration|UNKNOWN|Marks host-key migration with unestablished current consumers|S2.2-1,S2.2-6,S3-2|A migration marker may be historical or gate future migration; collected evidence and available documentation do not establish which here.
/var/lib/selinux|MUST|Aliases the active access-control policy directory|S2.2-1,S2.2-2|The symlink exposes system access-control policy; its operational role is not merely stored content.
/var/lock|UNKNOWN|Aliases runtime lock storage|S2.2-1,S2.2-2,S3-2|The link target is known, but actual consumers and whether loss changes locking behavior are not established.
/var/log/btmp|NOT|Records unsuccessful logins|S2.2-6|Failed-login records are records of the past, explicitly exempt.
/var/log/lastlog|NOT|Records each account’s most recent login|S2.2-6|Last-login records are explicitly exempt records of the past.
/var/log/wtmp|NOT|Records login and logout history|S2.2-6|Login history is explicitly exempt.
/var/mail|UNKNOWN|Aliases the mail spool|S2.2-1,S2.2-4,S3-2|The alias target is known, but no delivery consumer or stored messages establish whether removing it affects delivery or only access to content.
/var/run|UNKNOWN|Aliases live runtime storage|S2.2-1,S2.2-2,S3-2|Operational consumers of this compatibility alias are not established; the target’s existence does not prove reliance on this alias.
'''
for line in data.strip().splitlines():
 name,dec,what,sent,reason=line.split('|');r=next(r for r in rows if r['name']==name);append(r,dec,sent,what,'raw:coreos/files.tsv',reason)
print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))
