# Reviewed individual package cases; facts come from descriptions and file listings.
file_cases={
'anaconda-webui':('MUST','S2.2-9,S2.2-12','Provides installer web UI and standalone proxy and authentication helpers.','Standalone service helpers run as host processes; the web-page exemption does not exempt those programs.'),
'blivet-data':('MUST','S2.2-9,S2.2-12','Provides a storage-management daemon and its service activation files.','The file listing includes blivetd and service activation files, so this package supplies a program.'),
'coreutils-common':('MUST','S2.2-10','Provides shell initialization scripts alongside manuals and translations.','Shell initialization scripts execute with shell rights and must be recorded even when configuring command colors.'),
'dracut-config-rescue':('MUST','S2.2-10','Provides a kernel-install script and rescue-image configuration.','The kernel-install script executes code with interpreter rights; its configuration-oriented purpose does not exempt it.'),
'fedora-release-identity-workstation':('MUST','S2.2-1,S2.2-2','Provides edition identity, service presets, and desktop defaults.','Its service presets change default system service enablement, which determines computer behavior.'),
'fedora-chromium-config':('HOLE','S2.2-1,S2.2-2','Provides customization package identity and licensing material.','The listed payload is licensing text, but dependency or scriptlet behavior is unspecified; the text gives no package-identity classification.'),
'fedora-release-workstation':('HOLE','S2.2-1,S2.2-2','Provides a dependency target for edition-specific configuration packages.','An empty-payload dependency target may influence installation, but removal need not remove installed capabilities; the text gives no package-identity rule.'),
'fedora-release-common':('HOLE','S2.2-1,S2.2-2,S2.2-4','Provides release identity, login banners, and distribution macros.','Release labels are descriptive content but programs can branch on them; the text lacks a boundary between description and behavioral input.'),
'gnome-classic-session':('MUST','S2.2-1,S2.2-2','Adds a selectable desktop session and session service configuration.','Removal prevents launching the configured classic session through the login interface.'),
'gnome-shell-common':('HOLE','S2.2-1,S2.2-7','Defines the desktop shell settings schema.','Settings are read by one shell but govern the desktop; the text does not define whether this is only inside one program.'),
'gnome-shell-extension-common':('HOLE','S2.2-2,S2.2-4','Provides extension translations, documentation, and licensing text.','Translated UI output can be a lost capability or unavailable content; the text does not distinguish those readings.'),
'google-noto-fonts-common':('NOT','S2.2-4','Provides font documentation and licensing text.','The file listing contains documentation and licensing material; removal makes only those documents unavailable.'),
'kasumi-common':('NOT','S2.2-4','Provides a manual page and application icon.','These documented payloads are documents and decorative image content; only that content becomes unavailable.'),
'langtable':('MUST','S2.2-10','Supplies documentation including executable Python test cases.','The documented payload includes Python test code, which can execute with interpreter rights despite its documentation-directory location.'),
'libreoffice-data':('MUST','S2.2-10','Supplies Java component bindings alongside icons and MIME definitions.','The payload includes a Java archive of component code; code executed with interpreter rights must be recorded.'),
'nano-default-editor':('MUST','S2.2-10','Sets the default editor through shell startup scripts.','Shell initialization scripts are explicitly code even when their purpose is setting an editor preference.'),
'mutter-common':('MUST','S2.2-1,S2.2-2','Supplies device rules and shared desktop window-management settings.','Device rules and cross-application window-management settings affect system behavior beyond one program.'),
'qt6-qtbase-common':('HOLE','S2.2-10,S2.2-13','Provides package-building macros.','The file list establishes macros but not whether their expansions execute commands or merely substitute values; code and setting readings remain.'),
'rdma-core-common':('HOLE','S2.2-1,S2.2-2','Owns shared device-subsystem configuration directories.','Directory ownership metadata may leave all device behavior unchanged; the text does not specify package versus directory removal semantics.'),
'rootfiles':('MUST','S2.2-10','Supplies privileged-account shell initialization files.','Shell startup files are explicitly required code under the interpreter-rights rule.'),
'samba-common':('MUST','S2.2-1,S2.2-2,S2.2-15','Supplies shared file-service configuration and account-creation rules.','System account rules and configuration shared by servers and clients affect system-wide capabilities.'),
'vim-data':('MUST','S2.2-10,S2.2-13','Supplies editor initialization code and packaging templates.','The defaults.vim file is editor-language initialization code, explicitly included even when it holds settings.'),
'yelp-xsl':('HOLE','S2.2-10,S2.2-11,S2.2-13','Supplies help-rendering transformation stylesheets and browser-side scripts.','The text distinguishes unrestricted and interface-confined code but does not specify how transformation stylesheets fit when their execution rights are unspecified.')
}
for n,args in file_cases.items():
 case(n,*args);a=list(result[n]);a[3]='doc:'+D['file_source'];result[n]=tuple(a)
for n in ['cockpit-networkmanager','cockpit-storaged','cockpit-system']:
 case(n,'NOT','S2.2-11','Supplies browser-executed administrative HTML and JavaScript pages.','The payload is web-page code confined to the browser interface; the explicit web-page exemption applies.')
for n in ['gnome-shell-extension-apps-menu','gnome-shell-extension-background-logo','gnome-shell-extension-launch-new-instance','gnome-shell-extension-places-menu','gnome-shell-extension-window-list']:
 case(n,'MUST','S2.2-10,S2.2-13','Executes desktop-shell extension code in the shell process.','Extension code executes in the shell process with its rights; executable code remains code even when customizing presentation.')
 a=list(result[n]);a[3]='doc:https://gjs.guide/extensions/overview/anatomy.html';result[n]=tuple(a)
case('fedora-chromium-config-gnome','NOT','S2.2-7','Configures installation of a browser integration extension.','This package supplies browser-extension configuration; the explicit browser-extension exemption applies.')
# Runtime tables are homogeneous by function: non-executable tables read to provide particular operations.
tables={
'adobe-mappings-cmap':'Maps encoded characters to glyph identifiers for text rendering.',
'adobe-mappings-cmap-deprecated':'Supplies legacy character-to-glyph mappings needed by some applications.',
'adobe-mappings-pdf':'Maps character identifiers and encodings for PDF processing.',
'appstream-data':'Supplies searchable application metadata and software-center icons.',
'cldr-emoji-annotation':'Supplies localized emoji names and annotations.',
'cldr-emoji-annotation-dtd':'Defines document types for locale data interchange.',
'gweather-locations':'Supplies a weather-location database.',
'gweather-locations-common':'Supplies source-format weather-location data.',
'hunspell-en':'Supplies English spelling dictionaries.',
'hunspell-en-AU':'Supplies Australian English spelling dictionaries.',
'hunspell-en-CA':'Supplies Canadian English spelling dictionaries.',
'hunspell-en-GB':'Supplies British English spelling dictionaries.',
'hunspell-en-US':'Supplies American English spelling dictionaries.',
'hwdata':'Supplies hardware identification and configuration databases.',
'hyphen-en':'Supplies English hyphenation rules.',
'liblangtag-data':'Supplies language-tag and locale reference tables.',
'liblouis-tables':'Maps characters to Braille dot patterns and attributes.',
'libpinyin-data':'Supplies pronunciation and phrase databases for text input.',
'm17n-db':'Supplies input maps and language-specific text rendering tables.',
'mobile-broadband-provider-info':'Supplies mobile-provider network and subscription information.',
'mythes-en':'Supplies an English thesaurus.',
'ncurses-base':'Describes terminal capabilities for terminal-aware programs.',
'osinfo-db':'Describes operating systems and hypervisors for automated virtual-machine provisioning.',
'poppler-data':'Maps text encodings for PDF character rendering.',
'publicsuffix-list-dafsa':'Identifies domain suffix boundaries for cookie security decisions.',
'unicode-ucd':'Supplies Unicode character properties and algorithm conformance data.',
'words':'Supplies a word database used by spelling and password checkers.',
'xml-common':'Supplies XML schemas and catalogs used by XML processors.'}
for n,what in tables.items():
 put(n,'tables','HOLE','S2.2-1,S2.2-2,S2.2-4',what,'Removing operational tables loses specific lookup or processing abilities, yet they are database content; the text does not delimit these readings.')
for n in ['distribution-gpg-keys','fedora-gpg-keys','systemd-import-keys','gpg-pubkey']:
 case(n,'MUST','S2.2-1,S2.2-2','Provides public keys for verifying software or image signatures.','Without the verification key, signatures cannot be verified; removal prevents a concrete operation rather than merely hiding content.')
a=list(result['gpg-pubkey']);a[3]='doc:https://rpm.org/docs/4.20.x/man/rpmkeys.8';result['gpg-pubkey']=tuple(a)
case('dns-root-data','MUST','S2.2-1,S2.2-2','Supplies DNS root hints and DNSSEC trust anchors.','Removing root hints and trust anchors prevents configured root discovery and authenticated DNS resolution.')
for n,what in {
'alsa-ucm':'Configures audio-device routes used by multiple audio applications.',
'containers-common':'Configures storage, registries, and execution shared by container tools.',
'libssh-config':'Provides connection defaults shared by applications using the SSH library.',
'mariadb-connector-c-config':'Provides configuration entry points shared by database clients.',
'kbd-legacy':'Supplies console keymaps selecting keyboard input interpretation.',
'kbd-misc':'Supplies console keymaps and console glyph resources.',
'libX11-common':'Supplies character composition and locale mappings shared by graphical applications.',
'redhat-menus':'Defines desktop application menus shared by desktop environments.',
'usb_modeswitch-data':'Supplies device rules and settings that activate mobile broadband devices.',
'xkeyboard-config':'Supplies keyboard layouts used across graphical applications.',
'zram-generator-defaults':'Enables compressed-memory swap through the system service generator.',
'tzdata':'Defines timezone rules used by system and application time calculations.',
}.items():case(n,'MUST','S2.2-1,S2.2-2',what,'These shared system inputs determine operations across applications; the one-program setting exemption does not apply.')
for n,what in {
'NetworkManager-config-connectivity-fedora':'Enables a network manager connectivity test.',
'dnf-data':'Supplies package-manager directories, state paths, and configuration.',
'fedora-flathub-remote':'Configures a filtered software repository.',
'fedora-repos':'Configures software-package repository sources.',
'fedora-workstation-repositories':'Configures additional software repositories and search availability.',
'fuse-common':'Controls filesystem-in-userspace mounting through configuration.',
'libreport-anaconda':'Configures installer error-reporting destinations and workflows.',
'pipewire-config-raop':'Enables an audio-networking module through media-server configuration.',
}.items():case(n,'HOLE','S2.2-1,S2.2-2,S2.2-7',what,'One program reads these settings, but they affect system capabilities; the text does not define whether that is only inside one program.')
case('autocorr-en','NOT','S2.2-7','Supplies English automatic-correction rules for the office application.','Automatic-correction rules control editing inside one program and are read as settings.')
case('tesseract-common','NOT','S2.2-7,S2.2-13','Supplies configuration profiles read by the OCR program.','These profiles are settings used only within one OCR program, rather than executable program code.')
case('tesseract-langpack-eng','HOLE','S2.2-1,S2.2-2,S2.2-4,S2.2-7','Supplies trained recognition data for English OCR.','The trained data enables recognition, but is also data read inside one program; the text does not distinguish capability-bearing data from exemptions.')
case('tzdata-java','HOLE','S2.2-1,S2.2-2,S2.2-7','Supplies timezone rules read by Java runtimes.','Rules are read inside the runtime but govern many applications; the text does not define whether runtime-wide settings are one-program settings.')
