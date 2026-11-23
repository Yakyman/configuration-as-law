import csv,json,pathlib,collections
folder=pathlib.Path('A1/c1'); docs=json.load(open(folder/'part-2.packages.docs.json'))
rows=[r for r in csv.DictReader(open('A1/in/part-2.tsv'),delimiter='\t') if r['kind']=='package']
# Row-specific decisions are excluded before the two homogeneous code rules.
special={}
def s(names,decision,sentences,what,reason):
 for name in names.split('|'):special[name]=(decision,sentences,what,reason)
s('base-files','MUST','S2.2-10,S2.2-13','Provides filesystem hierarchy and system shell startup code.','Includes /etc/profile, explicitly covered shell startup code; ancillary documentation does not make the package merely content.')
s('base-passwd','MUST','S2.2-9,S2.2-15','Maintains standard system account and group definitions.','Account definitions and the program maintaining them must be recorded.')
s('bash-completion','MUST','S2.2-10,S2.2-13','Executes shell routines implementing programmable command completion.','Shell-executed routines have shell rights; treating executable settings as code resolves the settings exemption.')
s('cloud-utils|init|linux-image-cloud-amd64|libpython3-stdlib','MUST','S2.2-1,S2.2-2','Uses package dependencies to keep a suite or system component installed.','Installed dependency requirements direct package maintenance and upgrades; removing them loses that maintained dependency constraint, changing system behaviour.')
s('usr-is-merged','MUST','S2.2-10,S2.2-13','Executes package scripts checking merged layout and cleaning obsolete architecture directories.','The package contains shell maintainer scripts executed with installer rights; executable code must be recorded even when ordinary payload files are documentation.')
s('gcc-12-base','NOT','S2.2-4,S2.2-6','Supplies compiler documentation, licensing text, and changelog.','Published file list contains documentation and past records, exempt under the content and history clauses.')
s('manpages','NOT','S2.2-4','Supplies reference manual documents.','Removing manuals removes their content; the programs and document-reading capability remain.')
s('distro-info-data','NOT','S2.2-4','Supplies distribution release dates and version tables.','These are reference database contents; removing them removes the release facts, not the lookup programs.')
s('libc-l10n','NOT','S2.2-4','Supplies translated library messages.','Message catalogs are textual content; removing them removes translated content while retaining the programs.')
s('pci.ids','NOT','S2.2-4','Maps PCI identifiers to readable device and vendor names.','The identification database contains reference content; numerical device inspection remains possible without these names.')
s('ca-certificates','MUST','S2.2-1,S2.2-2,S2.2-9','Provides certificate trust anchors and tools maintaining system trust.','Trust verification depends on these anchors, and the package supplies executable certificate maintenance tools.')
s('debian-archive-keyring','MUST','S2.2-1,S2.2-2','Supplies trusted archive signature verification keys.','Removing trusted keys prevents authenticated archive verification; these are operational trust inputs, not account passwords or ordinary content.')
s('dbus-session-bus-common','MUST','S2.2-1,S2.2-2','Configures session message bus permissions and activation.','Bus permissions govern communication among multiple programs; removing them changes available messaging operations, beyond settings in force only inside one program.')
s('dbus-system-bus-common','MUST','S2.2-1,S2.2-2','Configures system message bus permissions and activation.','Bus permissions govern communication among multiple programs; removing them changes available messaging operations, beyond settings in force only inside one program.')
s('grub-cloud-amd64','MUST','S2.2-10,S2.2-13','Supplies shell-sourced bootloader defaults.','The /etc/default/grub file is sourced as shell code; the text counts executable settings as code.')
s('libaudit-common','MUST','S2.2-1,S2.2-2','Sets audit failure behaviour for applications using the audit library.','Configuration governs multiple applications, including whether they terminate after audit failure; it is not confined to one program.')
s('libsemanage-common','MUST','S2.2-1,S2.2-2','Configures shared security policy management.','Shared policy management controls system access behaviour, beyond settings confined to one program.')
s('libtirpc-common','MUST','S2.2-1,S2.2-2','Defines available RPC transports for library-using applications.','Transport configuration controls communication across applications; removing it changes available RPC operations.')
s('libpam-runtime','MUST','S2.2-1,S2.2-2,S2.2-15','Provides authentication configuration required by system login programs.','System authentication and account access depend on these rules, rather than settings confined to one application.')
s('libmagic-mgc','MUST','S2.2-1,S2.2-2','Supplies compiled rules identifying file formats.','Shared libmagic consumers depend on these recognition rules; removal changes file identification capabilities across programs, so content and single-program settings exemptions do not apply.')
s('media-types','MUST','S2.2-1,S2.2-2','Maps filename extensions to standard media types.','Removing type mappings changes automatic classification capabilities; the content exemption requires unchanged behaviour and therefore does not apply.')
s('ncurses-base','MUST','S2.2-1,S2.2-2','Defines terminal capabilities used by terminal applications.','Removing terminal definitions prevents correct terminal operations across programs, rather than merely hiding document content.')
s('netbase','MUST','S2.2-1,S2.2-2','Maps network service and protocol names to numbers.','Shared mappings enable named network operations across applications; removal prevents those operations rather than merely hiding displayed content.')
s('python-apt-common','MUST','S2.2-1,S2.2-2','Supplies templates enabling distribution-aware repository management and translated messages.','Repository templates enable distribution-aware source management; without matching templates the library raises an exception, so removal loses an operational capability.')
s('readline-common','MUST','S2.2-1,S2.2-2','Provides shared editing key bindings for readline-based programs.','Shared bindings govern interactive behaviour across multiple programs, not settings confined to one program.')
s('systemd-sysv','MUST','S2.2-1,S2.2-2','Connects standard init and shutdown commands to the service manager.','Removing compatibility links removes standard boot and shutdown entry points; behaviour depends on these links.')
s('tzdata','MUST','S2.2-1,S2.2-2','Provides timezone transition rules for systemwide time conversion.','Systemwide clock conversions depend on these operational rules; removal prevents timezone-specific computations.')
s('vim-common','MUST','S2.2-9,S2.2-10,S2.2-13','Provides editor startup code and help tag generation utility.','File list includes /usr/bin/helpztags and executable editor configuration; both satisfy explicit code requirements.')
s('vim-runtime','MUST','S2.2-10,S2.2-13','Provides editor runtime scripts for syntax, indentation, and plugins.','Editor-language scripts run with editor rights; the explicit rule counts executable settings as code.')
s('linux-image-6.1.0-56-cloud-amd64','MUST','S2.2-1,S2.2-2,S2.2-9','Provides the running kernel and loadable device support.','Kernel execution supplies system operations; removing its executable image prevents that kernel from starting.')
fields=['id','decision','sentences','what_it_does','basis','reason'];p=folder/'part-2.packages.tsv';seen=set()
if p.exists():seen={r['id'] for r in csv.DictReader(open(p),delimiter='\t')}
with open(p,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not p.stat().st_size:w.writerow(fields)
 for r in rows:
  if r['id'] in seen:continue
  n=r['name'].split(':')[0];url='https://packages.debian.org/bookworm/'+n
  if n in special:decision,sentences,what,reason=special[n]
  else:
   d=docs[n]['DescriptionExcerpt']
   if n=='libwrap0':d='TCP wrappers shared library'
   if n=='libnewt0.52':d='Text mode windowing library'
   what=' '.join(d.split()[:15])
   library=(n.startswith('lib') and n not in ['libc-bin','libcap2-bin','libpam-modules-bin']) or (n.startswith('python3-') and n!='python3-minimal') or n in ['bind9-libs','zlib1g']
   decision='MUST';sentences='S2.2-1,S2.2-10' if library else 'S2.2-1,S2.2-9'
   reason='The documented runtime library or module supplies executable code run with the consuming program’s rights; it must be recorded.' if library else 'The documented utility or executable system component provides a runnable capability; the explicit program requirement applies regardless of package installation.'
  if n=='usr-is-merged':url='https://deb.debian.org/debian/pool/main/u/usrmerge/usrmerge_37~deb12u1.tar.xz'
  if n=='python-apt-common':url='https://deb.debian.org/debian/pool/main/p/python-apt/python-apt_2.6.0.tar.xz'
  w.writerow([r['id'],decision,sentences,what,'doc:'+url,reason]);f.flush()
print(collections.Counter(r['decision'] for r in csv.DictReader(open(p),delimiter='\t')))
