import csv,json,re,collections
from pathlib import Path
base=Path('D1/c1');meta=json.load(open(base/'part-tumbleweed.rpm-a.metadata.json')); m=meta['packages']; rows=[r for r in csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t') if r['kind']=='L1:package:rpm'][:2390]
manual={}
def add(names,dec,sent,what,reason):
 for n in names.split(): manual[n]=(dec,sent,what,reason,'individual')
add('gpg-pubkey','UNKNOWN','S3-2','Imported package signature verification key','Inventory identifies imported keys but supplies no key policy or contents establishing their operational role.')
add('openSUSE-build-key','NOT','S2.2-4','Stores unused copies of package signing public keys','Documentation explicitly says these installed keys are not used; only their content disappears.')
add('xorg-x11-libX11-ccache','NOT','S2.2-5','Caches X11 Compose character tables','Removing regenerated cache changes lookup speed rather than available operations.')
add('system-user-root system-user-tftp system-user-nobody system-user-man system-user-lp system-user-flatpak system-user-bin system-user-daemon','MUST','S2.2-15','Defines a system user account','Account existence is explicitly required to be recorded.')
add('system-group-wheel system-group-kvm system-group-hardware system-group-audit','MUST','S2.2-1,S2.2-2','Defines groups controlling system access','Removing access groups changes which operations group members may perform.')
add('btrfsprogs-udev-rules libfido2-udev ddcutil-i2c-udev-rules libmtp-udev sane-backends-autoconfig','MUST','S2.2-1,S2.2-2','Configures device availability or access through udev','Removing device rules changes system device setup or access, beyond settings confined to one program.')
add('selinux-policy selinux-policy-targeted container-selinux flatpak-selinux tigervnc-selinux passt-selinux permissions-config','MUST','S2.2-1,S2.2-2','Defines system access control policy','Removing access policy changes which operations the system permits; effects extend beyond one program.')
add('displaymanager-sysconfig','MUST','S2.2-1,S2.2-2','Configures shared display manager login behavior','Settings govern multiple display managers and login access, so the single-program exception does not apply.')
add('libldap-data libnl-config libssh-config libtirpc-netconfig gsettings-desktop-schemas desktop-data-openSUSE gio-branding-openSUSE gtk3-branding-openSUSE gtk4-branding-openSUSE','MUST','S2.2-1,S2.2-2,S2.2-7','Provides shared configuration used by multiple applications','Documentation identifies shared defaults across applications; removal changes behavior beyond one program.')
add('MozillaFirefox-branding-openSUSE libreoffice-branding-openSUSE freecell-solver-presets dbus-broker-block-restart chrony-pool-openSUSE NetworkManager-branding-openSUSE PackageKit-branding-openSUSE ImageMagick-config-7-SUSE cups-config libsemanage-conf rpm-config-SUSE','NOT','S2.2-7,S2.2-13','Provides settings read by one program','Documented values customize the named program; the explicit single-program setting exception applies.')
add('filesystem javapackages-filesystem','MUST','S2.2-1,S2.2-2','Provides directory structure for installed software','Removing required directories prevents their software and stored objects from being accessed.')
add('branding-openSUSE','MUST','S2.2-1,S2.2-2','Selects distribution branding packages during installation','The brand file triggers package selection; removal changes subsequent system installation behavior.')
add('systemd-presets-common-SUSE systemd-presets-branding-openSUSE systemd-default-settings systemd-default-settings-branding-openSUSE','HOLE','S2.2-1,S2.2-2,S2.2-7','Sets service manager defaults affecting system services','Defaults are values read by one manager but control other programs; text does not define where a setting is in force.')
add('libcontainers-default-policy registries-conf-default','MUST','S2.2-1,S2.2-2','Sets container image policy shared by container tools','Shared container policy affects which images multiple tools accept or locate; removal changes system capabilities.')
add('publicsuffix wireless-regdb mozilla-nss-certs ca-certificates-mozilla libicu78-ledata libnumbertext-data libthai-data libX11-data libwacom-data poppler-data terminfo terminfo-base terminfo-iterm terminfo-screen tesseract-ocr-traineddata-eng cracklib-dict-full myspell-dictionaries myspell-en myspell-en_US hwdata media-player-info mobile-broadband-provider-info file-magic openal-soft-data snmp-mibs qalculate-data','HOLE','S2.2-1,S2.2-2,S2.2-4,S2.2-13','Supplies operational lookup data for software','Text does not distinguish losing specific lookup results as unavailable content from losing the software capability those tables enable.')
add('gtk3-data gtk3-schema gtk4-schema gnome-tour-data usb_modeswitch-data','UNKNOWN','S3-2','Supplies package data with insufficiently specified behavior','Package description does not establish the subpackage contents or removal consequences; raw ownership inventory is empty.')
add('ksysguardsystemstats6-data ktnef-debug-categories','NOT','S2.2-4','Supplies interface descriptions or diagnostic category descriptions','Removing descriptive metadata leaves the programs available; only those descriptions disappear.')
add('libkdegames libkmahjongg libkdepim','UNKNOWN','S3-2','Provides unspecified base files for related libraries','Package description identifies general data or base packaging without establishing contents or operational effects.')
add('vim-data vim-data-common shared-python-startup','MUST','S2.2-10,S2.2-13','Provides interpreter startup or editor runtime scripts','Runtime scripts execute with interpreter or editor rights; settings expressed as code remain code.')

def decide(n,d):
 if n in manual:return manual[n]
 s=d.get('summary',''); desc=d.get('description','');both=s+' '+desc
 if n.endswith('-lang') or 'translations' in s.lower() or n in ['desktop-translations','libqt5-qttranslations','qt6-translations','libreoffice-l10n-en']:
  return ('NOT','S2.2-4','Supplies translated interface text','Only translated text becomes unavailable; the programs and operations remain.','translation')
 if re.search(r'(^|[-])(doc|docs|manpages)$',n) or n in ['boost-license1_92_0','man-pages','man-pages-posix','info-std']:
  return ('NOT','S2.2-4','Supplies documentation or license text','Removal makes documents unavailable while executable program operations remain.','document')
 if n.startswith('kernel-firmware-') and n!='kernel-firmware-all' or n=='ucode-amd':
  return ('MUST','S2.2-1,S2.2-2,S2.2-16','Supplies firmware loaded into supported devices','Firmware enables supported hardware operations and is supplied through system software.','firmware')
 if n.startswith('patterns-') or n in ['kernel-firmware-all','openSUSE-release-ftp']:
  return ('HOLE','S2.2-1,S2.2-2,S2.2-7','Selects packages through dependency metadata','Removing the selector can leave software intact but change future package selection; text gives no temporal scope for the removal test.','selector')
 if re.search(r'font|typeface',s,re.I) and ('font' in n) and n not in ['fontconfig','fonts-config']:
  return ('HOLE','S2.2-1,S2.2-2,S2.2-4','Supplies typeface glyph shapes for rendering text','Text does not distinguish losing a typeface as content from losing the ability to render its characters.','font')
 if re.search(r'icon|wallpaper|sound.theme|card.decks|bitmap',s,re.I) and not re.search(r'library|handling|widget|tool|compiler',s,re.I):
  return ('NOT','S2.2-4','Supplies visual or audio presentation assets','Removing artwork or sounds makes only that presentation content unavailable.','asset')
 if re.search(r'branding|theme|metatheme',n) and n not in ['grantleetheme','qt6-platformtheme-gtk3','libqt5-qtbase-platformtheme-gtk3']:
  return ('UNKNOWN','S3-2','Supplies presentation theme with unspecified execution model','Description does not establish whether this theme contains executable code, values, or only artwork.','theme')
 if n.endswith('bash-completion') or n=='bash-completion':
  return ('MUST','S2.2-10,S2.2-13','Executes shell completion functions','Shell completion scripts execute with shell rights; the code rule applies.','code')
 if re.search(r'library|libraries|bindings|module|plugin|plug-in|implementation|daemon|utility|utilities|tool|application|program|interpreter|client|server|framework|editor|compiler|driver|backend|front.?end|parser|codec|engine|runtime|QML|classes|functions|routines|widget|API|wrapper',both,re.I) or d.get('files'):
  return ('MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10','Provides '+ ' '.join(s.split()[:12]),'Documented program or runtime code supplies operations; removal prevents executing that code or its provided functions.','code')
 return None
if __name__=='__main__':
 for i,r in enumerate(rows):
  n=r['name'].split(':',1)[1];d=m.get(n,{})
  if decide(n,d) is None:print(i,n,':',d.get('summary',''),d.get('description','').replace('\n',' ')[:350])
fmeta=json.load(open(base/'part-tumbleweed.rpm-a.filelists.json'));files=fmeta['packages'];olddecide=decide

def codepaths(n):
 return [p for p in files.get(n,[]) if not re.search(r'/(doc|licenses|man)/',p) and (re.search(r'/(s?bin|libexec)/',p) or re.search(r'\.so(?:\.|$)|\.(py|pyc|pm|rb|sh|qml|el|jar|ko(?:\.zst)?|efi)$',p) or re.search(r'/bash-completion/completions/|/lib/systemd/system-generators/|/lib/udev/[^/]+$|/vim\d+/(autoload|plugin|syntax)/',p))]

def decide(n,d):
 ps=files.get(n,[]); code=codepaths(n)
 if code:
  return ('MUST','S2.2-9,S2.2-10,S2.2-13','Provides executable program, library, or interpreter code','Documented package payload includes executable code; removing it removes the corresponding callable operations.','code')
 nongeneric=[p for p in ps if not re.search(r'/(doc|licenses|man)/',p)]
 if nongeneric and all('/qlogging-categories' in p for p in nongeneric):
  return ('NOT','S2.2-4','Supplies descriptions of diagnostic logging categories','Only descriptive category labels disappear; the separately packaged executable libraries remain.','category')
 if n.startswith('typelib-'):
  return ('MUST','S2.2-1,S2.2-2','Describes library interfaces for runtime language bindings','Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.','introspection')
 if n in ['gtk3-data','gtk3-schema','gtk4-schema']:
  return ('MUST','S2.2-1,S2.2-2,S2.2-7','Supplies shared toolkit keybindings or configuration schemas','Toolkit schemas and keybindings affect multiple applications; removal changes shared interface behavior.','individual')
 z=olddecide(n,d)
 if z and z[-1]=='code':return None
 return z
add('breeze6-cursors distribution-logos-openSUSE-Tumbleweed libksane-icons breeze6-wallpapers','NOT','S2.2-4','Supplies cursor, logo, icon, or wallpaper artwork','Payload contains presentation assets; removal makes only that artwork unavailable.')
add('kf6-kconfigwidgets','NOT','S2.2-4','Supplies translated locale names for selection dialogs','Payload contains locale description files rather than the separately packaged widget code.')
add('akonadi-contacts','HOLE','S2.2-1,S2.2-2,S2.2-4','Supplies world imagery and geographic timezone lookup data','Imagery is content; text does not distinguish timezone lookup content from the functionality enabled by those tables.')
add('kf6-purpose-services','NOT','S2.2-7,S2.2-13','Defines online service values used by a sharing framework','Only service descriptors are supplied; settings are read as values by the sharing framework.')
add('kscreenlocker6-imports','NOT','S2.2-7,S2.2-13','Provides module and type descriptors for screen locker QML','Payload has qmldir and qmltypes descriptors, without implementation code; values describe one program interface.')
add('libexttextcat glibc-locale-base glibc-locale xmlcharent iso_ent docbook_4','HOLE','S2.2-1,S2.2-2,S2.2-4','Supplies language or document interpretation tables','Text does not distinguish lookup content from the processing or interpretation capabilities enabled by those tables.')
add('libkleo libksieve tesseract-ocr-common','NOT','S2.2-4,S2.2-7,S2.2-13','Supplies program-specific values and descriptive resources','Payload supplies values or templates for one program plus content; its separately packaged executable code remains.')
add('libpaper netcfg login_defs alsa-ucm-conf libcontainers-common','MUST','S2.2-1,S2.2-2,S2.2-7','Supplies shared system configuration for multiple programs','Settings govern multiple consumers or devices; removal changes shared behavior beyond one program.')
add('pkgconf-m4 bash-loadables augeas-lenses cnf-bash samba-dcerpc snapper-zypp-plugin libzypp-plugin-appdata suse-module-tools-scriptlets bluez-cups grub2-systemd-sleep-plugin grub2-snapper-plugin','MUST','S2.2-9,S2.2-10,S2.2-13','Supplies executable functions, helpers, or interpreter scripts','Documented executable functions run as programs or with the invoking program rights.')
add('systemd-rpm-macros','MUST','S2.2-10,S2.2-13','Expands service packaging macros into installation shell code','Macros supply executable installation code with package installer rights.')
add('rpm-plugin-selinux','NOT','S2.2-7,S2.2-13','Configures RPM transaction SELinux plugin selection','Payload consists of RPM macro settings and a manual, not the plugin implementation.')
add('yast2-trans-stats','NOT','S2.2-4','Reports translation completion statistics','Stored translation statistics describe existing translation coverage; removing them only removes that information.')
add('girepository-1_0','MUST','S2.2-1,S2.2-2','Supplies runtime library interface descriptions','Language bindings require these interface descriptions to invoke corresponding native operations.')
add('Mesa ruby openssl dbus-1 grub2','NOT','S2.2-4','Supplies documentation for separately packaged executable software','Actual package file list contains documentation only; executable components are supplied by other packages.')
add('permissions openssh qtdeclarative-imports-provides-qt6 breeze6','HOLE','S2.2-1,S2.2-2,S2.2-7','Selects related packages through dependency metadata','Removing the selector leaves existing code intact but changes package selection; removal test gives no temporal scope.')
add('kf6-kcoreaddons kcoreaddons','MUST','S2.2-1,S2.2-2','Registers document types across desktop applications','Shared MIME type definitions enable recognition and dispatch across applications; effect is not confined to one program.')
add('xkeyboard-config','MUST','S2.2-1,S2.2-2','Defines shared keyboard mappings and layouts','Removing layout definitions prevents corresponding keyboard input mappings across applications.')
add('dbus-1-common','MUST','S2.2-1,S2.2-2,S2.2-15','Defines message bus sockets, configuration, and system account','Payload includes account definition and system service sockets; removal changes communication and account availability.')
add('openSUSE-release','MUST','S2.2-1,S2.2-2','Defines distribution identity, product and installer configuration','System identity and shared product defaults affect multiple installation and management tools.')
add('purge-kernels-service','MUST','S2.2-1,S2.2-2','Starts obsolete kernel cleanup during boot','Removing its service definition prevents automatic execution of the cleanup operation.')
add('xorg-x11-driver-video','MUST','S2.2-1,S2.2-2','Configures graphics devices and display screens','System display configuration determines device availability across applications.')
add('flatpak-remote-flathub','NOT','S2.2-7,S2.2-13','Configures a package source for Flatpak','Repository URL and options are values used by one package manager; explicit single-program setting exception applies.')
add('yast2-control-center xterm vlc plasma6-session','HOLE','S2.2-1,S2.2-2,S2.2-7,S2.2-13','Registers application or session launch entries','Desktop launch values enable launching separately packaged programs; text does not define whether these settings are in force only inside one launcher.')
add('libreoffice-filters-optional docbook-xsl-stylesheets','UNKNOWN','S3-2','Transforms structured documents with XSLT stylesheets','Execution rights or confinement of these stylesheet transformations are not established by package documentation.')
add('usb_modeswitch-data','MUST','S2.2-1,S2.2-2','Configures udev switching of USB devices into usable modes','Device matching rules invoke switching that makes hardware functions available beyond a single program.')
# Resolve solely presentation themes from precise file lists when no executable payload is present.
lastdecide=decide
def decide(n,d):
 z=lastdecide(n,d)
 if z and z[-1]=='theme':
  ps=files.get(n,[])
  if all(not p.endswith(('.qml','.js','.so','.py','.sh')) for p in ps):
   return ('NOT','S2.2-4,S2.2-7,S2.2-13','Supplies visual presentation assets and theme values','No executable payload is present; theme values and associated artwork fall under explicit setting or content exemptions.','presentation')
 return z
add('gpg-pubkey','HOLE','S2.2-1,S2.2-2,S2.2-7,S2.2-13','Enables verification of RPM package signatures','Keys enable signature verification but are values consumed by RPM; text does not distinguish operational trust data from single-program settings.')
add('hicolor-icon-theme','MUST','S2.2-10,S2.2-13','Provides icon assets and executable installation macros','The package macro expands to shell mkdir and touch commands; executable installation code requires recording despite accompanying artwork.')
