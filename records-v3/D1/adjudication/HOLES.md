# D1 adjudication: holes

Each card describes one kind of case where Sections 2–3 of `../../TEXT.md` do not decide whether an object must be recorded,
or where two sentences decide it in opposite ways. The rows for each card are in `rows.tsv` (column `hole`). The
example rows give the id, the object name and what the object does, as established in the row's note (file lists
come from the distribution repositories where the inventory query had none; see the notes).

Totals: 8 cards, 924 HOLE rows.

## Hole 1: presentation data read by several programs (fonts, shared translations, themes, artwork, sounds)

The objects are files that several programs read as values to draw or phrase their output: typefaces, message
catalogues of shared libraries or desktop-wide components, icon, cursor and widget themes, branding pictures and
sounds. S2.2-4 defines content only by examples and a rationale, while S2.2-13 makes such a file a setting and S2.2-7
exempts only settings confined to one program; the text does not say whether losing a typeface, a language or a look
counts as "only the content itself is unavailable" or as something that becomes impossible under S2.2-2.

Sentences involved:
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| fedora-825992c02de7410b9de93d54 | root:abattis-cantarell-vf-fonts | font files and fontconfig rules read by all text-drawing programs |
| tumbleweed-25d4e59fef6a08262890c4c4 | root:google-roboto-fonts | font files only, read by many programs |
| fedora-f6384d9de305cf7440d4a349 | user:gnulib-l10n | message catalogues shared by coreutils, tar, gawk and others |
| tumbleweed-d8620423f05d02d99e676201 | user:libKF6Baloo6-lang | message catalogues of several Baloo programs |
| mint-f029447dfa5b81e83920cfc2 | root:cinnamon-l10n | translations of several Cinnamon programs |
| fedora-e94d6040fe6b71468614c285 | user:adwaita-icon-theme-legacy | icon theme read by several programs |
| tumbleweed-819b570cdea5ea55df85afe1 | user:gtk4-metatheme-breeze6 | GTK4 CSS theme read by several programs |

Rows in this hole: 413.

## Hole 2: reference and lookup data read as values (databases whose loss makes a lookup impossible)

The objects are tables and databases that programs read as values to look something up: terminfo, GPU name tables,
character entity sets, CMaps, provider and transport databases, colour profiles, dictionaries, trusted keys in the
package database. S2.2-4 names "the contents of databases" as content that need not be recorded, but for these
objects removal makes the corresponding lookup or processing impossible, so S2.2-2 is positive; no sentence says which
prevails.

Sentences involved:
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| fedora-1616320aeaca00e35b428e9b | user:ncurses-base | terminfo database read by all terminal programs |
| tumbleweed-eaa3bb18d4c9f9d9e224e05d | user:terminfo | terminfo database only |
| mint-cef67297df4b26083898d0be | root:libdrm-common | GPU name table read by libdrm users |
| tumbleweed-856378d1c349da9571edbf48 | root:poppler-data | CMaps and encoding data for PDF rendering |
| tumbleweed-cb6bae922bf2ef3c7006b5b6 | root:mobile-broadband-provider-info | mobile provider APN database |
| mint-ef80a80feb7709633f6d40e4 | root:libtirpc-common | /etc/netconfig transport database read by libtirpc users |
| tumbleweed-d8740b0efbb387551a5f8266 | user:gpg-pubkey | public key in the rpm database used to verify package signatures |

Rows in this hole: 161.

## Hole 3: packages that only carry dependency metadata (patterns, metapackages, transitional packages)

The objects are packages whose own files do nothing or only describe (a README, a pattern description, no files at
all), while their dependencies make later package-manager runs install, keep or upgrade other packages. Removing such a
package changes nothing the computer does at that moment, but a later package-manager run would autoremove or stop
selecting packages; S2.2-2 gives no time scope for the removal test, and the text does not say whether package metadata
that steers the package manager counts as something the computer's behaviour depends on.

Sentences involved:
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| tumbleweed-8ffe304c89c8c7e36f097d58 | root:patterns-fonts-fonts | pattern package with one description text; its dependencies select fonts |
| tumbleweed-aac6aa8494b1f3e8c0028242 | user:grub2 | metapackage with documentation only; its dependencies pull the boot-loader packages |
| tumbleweed-f461fea1b1631f3f7d3a0c18 | root:kernel-firmware-all | compatibility metapackage with one README pulling firmware subpackages |
| mint-10d2b7fe70e9862d28583c28 | root:xserver-xorg-video-all | metapackage with documentation only, pulling X video drivers |
| mint-7588ce4f54fd792c9bd42dd5 | root:libtag1v5:amd64 | dependency package with documentation only |
| fedora-acb86505aa1316e17254882c | user:passwdqc | owns no files; only requires pam_passwdqc and passwdqc-utils |

Rows in this hole: 127.

## Hole 4: a setting read by one program whose effect reaches beyond that program

The objects are settings read by exactly one program that decide what other programs, users or the whole computer can
do: sshd options not named in S2.2-15 (forwarding, accepted environment, principals, host keys, algorithms), a
NetworkManager connectivity drop-in, display-manager configuration, a package-manager plugin macro. S2.2-7 exempts
"settings that are in force only inside one program", which can mean settings read by one program or settings whose
effect stays inside one program; the text does not say which.

Sentences involved:
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| flatcar-939d7a7b0d01b67c8e427d2d | ssh-access:PermitUserRC | decides whether a user's ~/.ssh/rc code runs at login |
| flatcar-fcc568ae504c7531844f5402 | ssh-access:AcceptEnv | passes client locale variables into login sessions |
| flatcar-f7c7fedce0e2f18bdceec831 | ssh-access:RefuseConnection | when set, sshd refuses all connections |
| flatcar-04d20d905cf48789916d65e4 | ssh-access:AuthorizedPrincipalsFile | certificate principals allowed per account |
| fedora-8daf8a09379a987250afb6d4 | user:NetworkManager-config-connectivity-fedora | NetworkManager connectivity check whose result other programs use |
| tumbleweed-398f3c80654469a71f15a2fe | user:sddm-branding-openSUSE | display-manager theme and compositor command |
| tumbleweed-cdd698ee2b182cf9d748a45a | user:rpm-plugin-selinux | rpm macro enabling the plugin that labels installed files |

Rows in this hole: 123.

## Hole 5: support for hardware that is absent but could be attached

The objects are firmware files, udev rules, hardware databases and device configurations for devices that this machine
does not have (wireless, USB modems, tablets, sound cards, media players) but that could be attached to it. Removal
changes nothing the computer does now; S2.2-2 does not say whether devices that could be attached count, and S2.2-16
does not say whether firmware files for an absent device are "device firmware".

Sentences involved:
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

Examples:
| id | name | what it does |
|---|---|---|
| fedora-94e7f0db6259f31f490e456b | root:qcom-wwan-firmware | firmware for Qualcomm WWAN modems, none present |
| fedora-9f61c67c043a3651bdaf564b | user:b43-openfwwf | firmware for Broadcom 43xx wireless chips, none present |
| tumbleweed-616fcce7fd547116d0d09fc7 | root:wireless-regdb | wireless regulatory database; no wireless device present |
| fedora-1b58d19cc948a0cd43fcb240 | root:usb_modeswitch-data | udev rules and switch data for USB modems; no USB controller present |
| fedora-6e50f07c99ff596cc9d0fc4c | root:alsa-ucm | use-case configurations for specific sound cards; no sound device present |
| tumbleweed-9767c3f823fd0b3c16059410 | user:libwacom-data | udev rules and descriptions of graphics tablets; none present |
| tumbleweed-c77416992eb1732fe822e2b9 | root:media-player-info | udev rules for portable media players; no USB device present |

Rows in this hole: 58.

## Hole 6: objects regenerated automatically from another object

The objects are units, drop-ins and files that a generator or a service writes again on every boot or manager reload,
from another object that holds their source (XDG autostart units, generator output under /run, a regenerated
resolv.conf, static device-node lists). The computer's behaviour depends on them, but removing them is undone by
regeneration, so the removal test is negative or only temporarily positive; the text does not say how such derived
objects are tested.

Sentences involved:
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| tumbleweed-106b78a49881386e5c2089f8 | user:app-org.kde.discover.notifier@autostart.service | user unit generated from an XDG autostart entry on each manager start or reload |
| flatcar-769ce88f8a54e2150b5cbec9 | /run/systemd/generator/serial-getty@.service.d | autologin drop-in written by a generator on each reload |
| flatcar-e8c3dd1b118f12e4905f5300 | /run/systemd/generator/sockets.target.wants | enablement link of a socket written by a generator |
| flatcar-6abd3cc93dfc5b3e66f60427 | /run/systemd/generator.late | boot mount and automount units written by a late generator |
| flatcar-778d999ce314fbfc50ce240f | /run/tmpfiles.d | static-nodes.conf written at each boot from kernel module data |
| flatcar-b9083577b011da27bfb86f15 | /run/systemd/resolve | resolv.conf files regenerated by the resolver and read by all programs |

Rows in this hole: 20 (some are directories whose other members are decided; the hole comes from the member named).

## Hole 7: code run by one program inside its own interface that acts with that program's rights

The objects are code files that one program executes through its own interface or scripting framework, while that
framework lets the code act with the program's rights: Cockpit web pages that drive the privileged bridge, desktop-shell
layout scripts, display-manager greeter themes in QML, document-filter XSLT, Augeas lenses that decide which files are
written. S2.2-11 exempts code that the program confines to its own interface (a web page in a browser is its example),
while S2.2-10 requires code the program runs with its own rights "so that the code can do whatever the program can
do"; no sentence says which prevails.

Sentences involved:
- S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do”

Examples:
| id | name | what it does |
|---|---|---|
| fedora-d23b5ec58a99a2d5dd98c6d0 | root:cockpit-storaged | storage web pages run in a browser, driving the cockpit bridge |
| fedora-d1549cca8e2e2802d54afae6 | user:cockpit-system | system web pages run in a browser, driving the cockpit bridge |
| tumbleweed-b8d3bce61d0c4d8c4fd618cc | user:plasma6-theme-openSUSE | layout JavaScript and splash QML executed by the desktop shell |
| tumbleweed-c225ad126cda23f96aa4609e | user:plasma6-sddm-theme-openSUSE | active greeter theme in QML run by the display manager, which logs users in |
| tumbleweed-458bd2d25764f4b4b0aa2150 | user:libreoffice-filters-optional | XSLT import/export filters executed by the office suite |
| tumbleweed-58bfaed75b767465bff8e84a | user:augeas-lenses | lenses run by libaugeas that decide which files the tool writes |

Rows in this hole: 14.

## Hole 8: code that runs only inside virtual machines but that the emulator needs to start them

The objects are guest firmware images and option ROMs (UEFI and BIOS images, network and VGA ROMs) that run only inside
a virtual machine, yet without which the emulator cannot start such machines. S2.2-11 exempts code confined in a
virtual machine, while S2.2-2 is positive because starting those machines becomes impossible after removal; no sentence
says which prevails.

Sentences involved:
- S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

Examples:
| id | name | what it does |
|---|---|---|
| fedora-8a717666be03995676d7c21d | user:edk2-ovmf | UEFI firmware images run inside guests; the emulator needs them to start UEFI machines |
| fedora-729138f682023c574071c098 | root:seabios-bin | BIOS images and firmware descriptors needed to start BIOS machines |
| fedora-21a722be1d318ec0f86e5189 | user:ipxe-roms-qemu | network card option ROMs the emulator loads for those cards |
| fedora-d42127df5b3b98e4059e07bb | user:seavgabios-bin | VGA option ROMs for emulated VGA devices |

Rows in this hole: 8.
