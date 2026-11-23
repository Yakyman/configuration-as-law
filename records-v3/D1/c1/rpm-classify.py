import json,csv,re,collections
D=json.load(open('D1/c1/raw/rpm-documentation.json')); P=D['packages']; result={}; rule={}
def put(n,r,dec,sent,what,reason):
 result[n]=(dec,sent,what,'doc:'+D['source'],reason);rule[n]=r
for n,d in P.items():
 s=d['summary']; t=d['description']; v=s+' '+t
 if re.search(r'meta-?package|metapackage',v,re.I) and not any(re.match(r'^/(?:usr/)?s?bin/',x) for x in d['files']):
  put(n,'meta','HOLE','S2.2-1,S2.2-2','Selects dependencies through a package-management metapackage.','The text does not say whether dependency-selection metadata itself changes capabilities when its installed dependencies remain.')
 elif re.search(r'documentation|license file',s,re.I) and n not in ['containers-common','perl-Pod-Simple'] and not any(re.match(r'^/(?:usr/)?s?bin/',x) for x in d['files']):
  put(n,'documents','NOT','S2.2-4','Supplies documentation or licensing text.','Removing these documents makes only their content unavailable; executable capabilities remain.')
 elif re.search(r'font',s,re.I) and re.search(r'fonts?(?: |$)|typeface',s,re.I) and ('fonts' in n) and not n.endswith(('common','filesystem')):
  put(n,'fonts','HOLE','S2.2-1,S2.2-2,S2.2-4','Supplies typefaces and glyph shapes for rendering text.','Unavailable glyph rendering is a lost capability under removal, or merely unavailable font content; the text supplies no boundary.')
 elif re.search(r'translations|locali[sz]ation|langpacks|language packs|language pack|gettext catalogs',s,re.I) and n!='gnome-software-fedora-langpacks':
  put(n,'translations','HOLE','S2.2-1,S2.2-2,S2.2-4','Supplies localized language resources.','Removing translations loses language-specific output, or only removes translated content; the text does not distinguish these readings.')
 elif re.search(r'firmware|microcode updates',s,re.I) and not n.startswith(('edk2-ovmf','seabios','seavgabios')):
  put(n,'firmware','MUST','S2.2-1,S2.2-2,S2.2-16','Supplies device firmware or firmware-loading support.','Removing firmware support prevents supplying the device functionality that depends on those firmware images.')
 elif re.search(r'SELinux.*polic|polic.*SELinux|selinux policy|Polkit rule',s,re.I) and n not in ['checkpolicy','libsemanage','libsepol','policycoreutils','policycoreutils-python-utils','python3-policycoreutils','python3-setools']:
  put(n,'access','MUST','S2.2-1,S2.2-2,S2.2-15','Supplies access-control policy governing permitted system operations.','Removing access policy changes which system operations are permitted; access rules determine what can be done.')
 elif any(re.match(r'^/(?:usr/)?s?bin/[^/]+$',x) for x in d['files']):
  put(n,'program','MUST','S2.2-9,S2.2-12','Provides installed executable commands.','Executable programs run as processes on the computer and must be recorded regardless of installation method.')
 elif re.search(r'\blibrar(?:y|ies)\b',s,re.I):
  put(n,'library','MUST','S2.2-1,S2.2-10','Supplies executable library routines used by other programs.','Library routines execute with their calling programs privileges; removing them also removes their supported operations.')
 elif n.startswith(('python3-','perl-')) and not re.search('data|filesystem|wheel',s,re.I):
  put(n,'module','MUST','S2.2-10','Supplies interpreter modules or executable language support.','Interpreter modules execute code with the interpreting program rights, so they must be recorded.')
 elif re.search(r'directory layout|directories used|filesystem layout|filesystem for|filesystem package|directories$',s,re.I) or n.endswith('-filesystem'):
  put(n,'directories','HOLE','S2.2-1,S2.2-2','Supplies directory ownership and layout for other packages.','The text does not specify whether removing directory ownership while retaining other packages contents counts as removing their capabilities.')
 elif re.search(r'background|wallpaper|icons and pictures|cursor theme|icon theme|sound theme',s,re.I) and not 'extension' in n:
  put(n,'art','NOT','S2.2-4','Supplies decorative images, icons, or sounds.','Removal makes only the decorative content unavailable; programs retain their operations.')
 elif re.search(r'plugin|plug-in|\bmodule\b|backend|driver|bindings|wrapper|codec|parser|implementation|engine|runtime|routines|API|framework|functions',s,re.I) and not re.search(r'config|data|schema|policy|meta',s,re.I):
  put(n,'native','MUST','S2.2-1,S2.2-10','Supplies executable modules implementing program operations.','These modules implement operations using their executing programs rights; removing their code removes those operations.')
 else:pass
def copy_rule(n,r):
 exemplar=next(k for k in rule if rule[k]==r)
 result[n]=result[exemplar];rule[n]=r
# Individually inspected additions to functionally homogeneous rules.
additions={
'library':'''atk codec2 glycin-gtk4-libs gnome-bluetooth-libs gtksourceview5 highway iptables-libs libX11-xcb liba52 libdovi libfsverity libldb libsolv libtsm libutempter libuv libxcvt lz4-libs mpg123-libs ngtcp2-crypto-gnutls ngtcp2-crypto-ossl opencore-amr pcre2-utf16 pcre2-utf32 rutabaga-gfx-ffi speech-dispatcher-libs spice-glib spice-gtk3 spice-server svt-av1-libs tpm2-tss-fapi xcb-util-keysyms''',
'native':'''PackageKit-gtk3-module anaconda-tui at-spi2-core clucene-contribs-lib cyrus-sasl-plain dracut-live dracut-network evolution-ews-core fips-provider glib-networking glibc-gconv-extra glusterfs-client-xlators gnome-software-fedora-langpacks gssdp gstreamer1-plugin-gtk4 gtk-vnc2 gupnp-av gvfs-afc gvfs-fuse gvfs-goa gvfs-gphoto2 gvfs-mtp gvfs-smb gvnc gvncpulse ibus-typing-booster kdump-anaconda-addon kernel-core kernel-modules kernel-modules-core kernel-modules-extra kmscon-freetype libXau libaribcaption libdhash libdnf5-plugin-appstream libev libfprint libglvnd-egl libglvnd-gles libglvnd-glx libglvnd-opengl libhandy libheif libical libimagequant libpcap librdmacm libreoffice-emailmerge libreoffice-graphicfilter libreoffice-ogltrans libreoffice-pdfimport libreoffice-pyuno libshumate libslirp libstemmer libvirt-gconfig libvirt-glib libxcb libxshmfence lpcnetfreedv mod_lua nbdkit-basic-filters nss pam_afs_session pam_passwdqc pangomm2.48 papers-nautilus pipewire-alsa pipewire-gstreamer pipewire-plugin-libcamera pkcs11-provider qemu-device-display-qxl qemu-device-display-vhost-user-gpu qemu-device-display-virtio-gpu qemu-device-display-virtio-gpu-ccw qemu-device-display-virtio-gpu-gl qemu-device-display-virtio-gpu-pci qemu-device-display-virtio-gpu-pci-gl qemu-device-display-virtio-gpu-pci-rutabaga qemu-device-display-virtio-gpu-rutabaga qemu-device-display-virtio-vga qemu-device-display-virtio-vga-gl qemu-device-display-virtio-vga-rutabaga qemu-device-uefi-vars qemu-device-usb-host qemu-device-usb-redirect qemu-device-usb-smartcard qemu-ui-opengl qt6-qtdeclarative qt6-qtsvg simdutf sssd-proxy stratisd-dracut tpm2-tss vulkan-loader webkit2gtk4.1 zlib-ng''',
'program':'''PackageKit-command-not-found aardvark-dns accountsservice bluez-obexd braille-printer-app catatonit cockpit-ws cups-pk-helper dbus evolution-data-server flatpak-session-helper geoclue2 glusterfs gnome-initial-setup gnome-menus gnome-settings-daemon gnome-user-share gnupg2-keyboxd httpd hyperv-daemons libvirt-ssh-proxy netavark oo7-daemon oo7-portal p11-kit-server passwdqc prefixdevname qemu-common qemu-system-x86 system-config-printer-udev uresourced virtiofsd xdg-desktop-portal zram-generator''',
'module':'''perl-Class-Struct perl-Data-Dumper perl-Storable perl-Pod-Simple python3-langtable ibus-anthy-python''',
'fonts':'''julietaula-montserrat-fonts open-sans-fonts vazirmatn-vf-fonts''',
'documents':'''hyperv-daemons-license libreoffice-help-en urw-base35-fonts-common''',
'meta':'''containers-common-extra kernel''',
'directories':'''grub2-common''',
'access':'''passt-selinux'''
}
for r,names in additions.items():
 for n in names.split():copy_rule(n,r)
# Distinct facts judged row by row; no catch-all rule for unresolved packages.
def case(n,dec,sent,what,reason):put(n,'individual',dec,sent,what,reason)
case('edk2-ovmf','NOT','S2.2-11','Supplies UEFI guest firmware executed inside virtual machines.','This guest firmware runs within the virtual machine interface; code confined to that interface need not be recorded.')
case('ipxe-roms-qemu','NOT','S2.2-11','Supplies network boot ROMs for emulated devices inside virtual machines.','These ROMs execute within emulated guest devices, so the confined-code exemption applies.')
case('seavgabios-bin','HOLE','S2.2-10,S2.2-11,S2.2-16','Supplies VGA BIOS implementation code.','The text gives different answers for device firmware and guest-confined firmware; the package description does not identify its execution location.')
case('seabios-bin','HOLE','S2.2-10,S2.2-11,S2.2-16','Supplies legacy BIOS usable as a firmware payload.','Physical firmware and guest-confined firmware receive different decisions; the text does not classify a stored payload independently of its execution location.')
for n in ['grub2-efi-ia32-cdboot','grub2-efi-x64-cdboot','grub2-pc','shim-ia32','shim-x64','edk2-shell-x64']:
 case(n,'MUST','S2.2-1,S2.2-2,S2.2-9','Supplies executable boot-environment components.','Removing these components prevents their boot or firmware-environment operations; executable programs must be recorded.')
for n in ['grub2-efi-ia32-modules','grub2-efi-x64-modules','grub2-pc-modules']:
 case(n,'MUST','S2.2-1,S2.2-2','Supplies modules for building customized bootloader images.','Removing these modules prevents building bootloader images with their supplied capabilities.')
for n in ['bash-completion','bash-color-prompt','livesys-scripts','vpnc-script','pkgconf-m4','python-pip-wheel']:
 case(n,'MUST','S2.2-10','Supplies executable scripts, functions, or interpreter input.','These functions and scripts execute with interpreter rights; the explicit code rule requires recording them.')
for n in ['redhat-systemd-presets','redhat-systemd-presets-common','redhat-systemd-presets-desktop']:
 case(n,'MUST','S2.2-1,S2.2-2','Determines which system services are enabled by default.','Service enablement changes what the computer does and can run; the preset governs system-wide behavior.')
case('setup','MUST','S2.2-10,S2.2-15','Supplies account databases and shell initialization files.','Accounts and shell startup code are explicitly required objects, regardless of their packaging.')
case('gsettings-desktop-schemas','MUST','S2.2-1,S2.2-2','Defines settings shared among multiple desktop components.','Shared desktop settings affect multiple programs, so the one-program-only setting exemption does not apply.')
case('crypto-policies','MUST','S2.2-1,S2.2-2','Sets cryptographic policy across cryptographic backends.','System-wide cryptographic restrictions determine permitted operations across programs; removing them changes those capabilities.')
case('dbus-common','MUST','S2.2-1,S2.2-2','Configures system and user message buses.','Message-bus configuration governs communication between programs; its effect is not confined to one program.')
case('mailcap','MUST','S2.2-1,S2.2-2','Maps media types to helper programs and file extensions.','Shared mappings determine which other programs handle files; removing them removes configured cross-program handling.')
case('gnome-session-wayland-session','MUST','S2.2-1,S2.2-2','Adds a desktop-session launch entry to the display manager.','Removing the entry prevents selecting this session through the configured login interface.')
case('systemd-oomd-defaults','MUST','S2.2-1,S2.2-2','Enables resource-pressure termination behavior through service drop-ins.','These drop-ins enable actions on other processes, so their effect extends beyond one program.')
case('nftables-services','MUST','S2.2-1,S2.2-15','Loads firewall rules through a system service.','Firewall enforcement and rules control connection access and must be recorded.')
case('libvirt-daemon-config-network','MUST','S2.2-1,S2.2-2,S2.2-15','Configures default NAT networking for virtual machines.','Network and NAT configuration changes connectivity and connection access beyond the management program.')
case('fedora-bookmarks','NOT','S2.2-7','Supplies default web-browser bookmarks.','Browser bookmarks are settings in force only inside the browser.')
case('gnome-app-list','NOT','S2.2-7','Selects applications featured within the software-center interface.','Featured-list display settings govern only the software-center presentation.')
case('plymouth-theme-spinner','NOT','S2.2-7','Supplies a boot-splash spinner theme.','A display theme operates only inside the splash program; the theme exemption applies.')
case('fwupd-plugin-uefi-capsule-data','NOT','S2.2-4','Supplies localized bitmap artwork displayed during firmware updates.','The documented payload is bitmap content; removal makes only that artwork unavailable.')
for n in ['seabios-bin','seavgabios-bin']:
 case(n,'UNKNOWN','S3-2','Supplies BIOS implementation code with unestablished deployment context.','Documentation establishes BIOS functionality but not whether this stored firmware runs on hardware or inside an exempt guest.')
for n in ['kernel-core','kernel-modules','kernel-modules-core','kernel-modules-extra']:
 case(n,'MUST','S2.2-1,S2.2-2','Supplies kernel code implementing operating-system and device operations.','Removing this kernel code prevents the operating-system or device operations it implements.')
exec(open('D1/c1/rpm-special.py').read())
exec(open('D1/c1/rpm-revisions.py').read())
# Persist each settled row immediately; re-runs preserve already written IDs.
if __name__=='__main__':
 import os
 rows=[r for r in csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t') if r['kind']=='L1:package:rpm']
 out='D1/c1/part-fedora.rpm.tsv';exists=os.path.exists(out)
 seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if exists else set()
 with open(out,'a') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n')
  if not exists:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
  for r in rows:
   n=r['name'].split(':',1)[1]
   if r['id'] not in seen and n in result:
    w.writerow([r['id'],*result[n]]);f.flush()
 print('Settled',len(result),'packages; rows',sum(r['name'].split(':',1)[1] in result for r in rows))
