# Classification rules and checked examples

Only PAGE.md supplies classification rules. Inventory labels supply no authority. Q1, Q2 and Q3 are tested in R5 order; same-package U1 and recorded-source U2 coverage are kept distinct from unrestricted dependency coverage.

Each rule below records ten manually examined row IDs. Explicit individual decisions are not counted as homogeneous script rules. Final classifications include the documented correction overlays; original appended classification rows remain available.

# D1 classification rules

16 homogeneous rules. The table evidence, referenced raw inventory, and cited public primary documentation alone were used. Inventory labels were not treated as conclusions.

Q1/Q2/Q3 are applied in R5 order. U1 and U2 encode coverage; a package dependency is not same-package delivery. Q2/Q3 versus non-executable-file U3 conflicts are retained where neither U1 nor U2 supplies coverage.

Package lists were obtained from Fedora Packages, Ubuntu Packages, and openSUSE official repository primary/filelists metadata. Source install manifests were checked for Mint-specific packages. Each row carries its relevant URL. Local audit JSON lists the full rule membership.

## D1-PROCESS

Sentences: Q1,R5,U6,R1. Applied rows: 55.

A reported running executable process is PROGRAM/YES/DECIDED. Q1 is first; U6 expressly includes its own process. PID aggregation does not change this result when the reported executable is the same.

Manual check: Checked PID evidence and executable names, including atd, uresourced, systemd, packagekitd, accounts-daemon, catatonit, hostnamed, resolved and udevadm.

- `fedora-75876cae6b37d970268e6022` — 10
- `fedora-c1b06a71daa3183f8bb707bb` — 11
- `fedora-0630a103ed7d87f90879cea5` — 1188
- `fedora-3bb57218f1c926de8bb86718` — 12
- `fedora-67a84a7fec95df7a4be19897` — 1542
- `fedora-8a86a417e50b10384b88e9c9` — 1632
- `fedora-4186187c9918c8d29eceefdf` — 19
- `fedora-b1fc537fbe4d04253cf4af87` — 2
- `fedora-fb364c6193d616102d3710c4` — 46
- `fedora-d33a20f315ba0bc4af9cc5ce` — 49

## D1-GROUP

Sentences: Q2a,R1. Applied rows: 130.

An inventoried local permission-group identity and membership is SETTING/YES/DECIDED: Q2a expressly includes rights. This classifies the group object, not the /etc/group file.

Manual check: Checked group entries, numeric GIDs and membership lists; empty membership still has a group identity used for rights.

- `flatcar-3e7acd7861265a9c89184e3b` — root
- `flatcar-cf16ef23ac448b364d518f26` — core
- `flatcar-cfc75235c662052fb431b2e4` — shadow
- `flatcar-c23346b48a0e548523a60586` — user
- `flatcar-3e7acd7861265a9c89184e3b-occurrence-2` — root
- `flatcar-b02db9969b55ac0233754dec` — bin
- `flatcar-02ebf59a3162d26c558a50df` — daemon
- `flatcar-a7245c0c58caf4e0f270123e` — sys
- `flatcar-f7c3c15c9088a1e93c85517b` — adm
- `flatcar-f6ac9006a6adba520d55ec59` — tty

## D1-SERVICE

Sentences: Q2a,A3,R1,R3. Applied rows: 44.

A service-manager object present in the inventory is SETTING/YES/DECIDED. Q2a names services; A3 states when active, but R1 does not exempt disabled or inactive settings. Missing unit files are not treated as executable files.

Manual check: Checked named service objects and manager states, including inactive/not-found entries; these are manager state rows rather than unit-file payloads.

- `flatcar-f79b464b166dee8a6edf7235` — plymouth-quit-wait.service
- `flatcar-db3479ac6a4a75602d47f30f` — plymouth-start.service
- `flatcar-4ebcb6edd91450f4eb5aa735` — syslog.service
- `flatcar-88464f8a7422c36c077c2907` — systemd-quotacheck.service
- `flatcar-ee9d2efa3352fec63a32b097` — systemd-tpm2-setup-early.service
- `tumbleweed-70d71746ae30f45711522288` — user:pipewire-media-session.service
- `tumbleweed-27d56d5bac60be15f531556c` — user:plasma-foreground-booster.service
- `tumbleweed-ca27a508150e23fbe83ae99e` — user:plasma-kcminit.service
- `tumbleweed-acedc1c8803379656020dbdf` — user:plasma-kglobalaccel.service
- `tumbleweed-ec277111af46e76b0a09397b` — user:pulseaudio.service

## D1-ACCESS

Sentences: Q2a,R1. Applied rows: 50.

An SSH option specifying admission, authentication, session rights, permitted forwarding or resulting access is SETTING/YES/DECIDED by Q2a. Generic runtime path/cleanup defaults are excluded.

Manual check: Checked each selected option meaning against sshd_config: PAM selection, session limit, RSA minimum, socket mask, host-based authentication, credential delegation and X11 forwarding.

- `flatcar-f56e165ce3982c8e4e92a18f` — ssh-access:PAMServiceName
- `flatcar-4e34a3c8592ce4ab88dea652` — ssh-access:MaxSessions
- `flatcar-5b1b239bd3ddc18fe021389c` — ssh-access:RequiredRSASize
- `flatcar-27deb26d2fe4af2f7297e996` — ssh-access:StreamLocalBindMask
- `flatcar-c2ecb15cf6b0b94511e9a53b` — ssh-access:IgnoreRhosts
- `flatcar-611195fc9200fcb530a884d1` — ssh-access:IgnoreUserKnownHosts
- `flatcar-c3888d88a98301bd3b9b3d45` — ssh-access:HostbasedAuthentication
- `flatcar-a2f43615467461d74cd71b86` — ssh-access:GSSAPIAuthentication
- `flatcar-fb371a938b48ad8f2110ae85` — ssh-access:GSSAPIDelegateCredentials
- `flatcar-3879c5635f8487590fbc98a3` — ssh-access:X11Forwarding

## D1-DRIVER-LINK

Sentences: Q3,U3,R2. Applied rows: 29.

An inventoried sysfs driver symlink is non-executable runtime output: Q3 PROGRAM_RECORD/NO versus U3 MATERIAL/NO, hence NONE/NO/TWO_WAYS. It is the binding link, not driver code or the device.

Manual check: Checked symlink paths and target driver directories. Kernel sysfs documentation establishes runtime-generated links; recorded source derivation required by U2 is not established.

- `flatcar-f680f2ced5cbbbb98c0f7e6e` — /sys/devices/pnp0/00:05/driver
- `flatcar-4ff7c0363c7bcaed36cee8c4` — /sys/devices/pnp0/00:05/rtc/rtc0/alarmtimer.0.auto/driver
- `flatcar-3ec540466dde50c24e4e6a58` — /sys/devices/pnp0/00:01/driver
- `flatcar-f0515208c7470ebde5ef43b0` — /sys/devices/pnp0/00:04/00:04:0/driver
- `flatcar-bafb06ed0c03f82136071d0b` — /sys/devices/pnp0/00:04/00:04:0/00:04:0.0/driver
- `flatcar-dc571710b764793b61bfe463` — /sys/devices/pnp0/00:04/driver
- `flatcar-1f9163a7e2f94b85174294f1` — /sys/devices/pnp0/00:00/driver
- `flatcar-44bd92356b91b0b47cf8277a` — /sys/devices/platform/reg-dummy/driver
- `flatcar-6861c749394b4335ae375e11` — /sys/devices/platform/serial8250/serial8250:0/serial8250:0.3/driver
- `flatcar-3d0421dd3fe9ece92d5747d4` — /sys/devices/platform/serial8250/serial8250:0/serial8250:0.1/driver

## D1-SSH-PROVENANCE

Sentences: Q2,U1,R1. Applied rows: 11.

The specifically enumerated generic SSH helper-path, host-key-path and cleanup defaults have unknown human-decision versus same-package-default provenance: NONE/NA/FACT_UNKNOWN. Their function is known; their source is not.

Manual check: Checked complete effective option values and OpenSSH descriptions. Excluded admission rules from this set; HostKey paths concern server identity rather than permission to enter.

- `flatcar-5d80395a659e8419162b17af` — ssh-access:KerberosTicketCleanup
- `flatcar-9a331615508f9e7abf819565` — ssh-access:GSSAPICleanupCredentials
- `flatcar-75c6a8db40c3f9b508e5f565` — ssh-access:ExposeAuthInfo
- `flatcar-27668ef22c0c53aded70245e` — ssh-access:PidFile
- `flatcar-34324cc03d257717c37ae293` — ssh-access:XAuthLocation
- `flatcar-f8b927b906391312b6e57dad` — ssh-access:SshdSessionPath
- `flatcar-1f7fcb5f10b8cfb81a096d03` — ssh-access:SshdAuthPath
- `flatcar-4ffd82fa38286ea6436e1a9e` — ssh-access:HostKey
- `flatcar-57f829c278e3a32ae67a5421` — ssh-access:HostKey
- `flatcar-c488b0dd3a035637e0c2c96d` — ssh-access:HostKey

## D1-UDEV-LINKS

Sentences: Q3,U3,R2. Applied rows: 160.

Groups whose actual direct members are only runtime udev index symlinks have homogeneous Q3 PROGRAM_RECORD/NO versus U3 MATERIAL/NO: NONE/NO/TWO_WAYS. Live device-event derivation does not establish U2 source coverage.

Manual check: Checked full group members against raw filesystem types and targets, not merely directory names.

- `flatcar-4c7805e498936e7ae1a37d41` — /run/udev/links/cdrom
- `flatcar-bd0133edb221e27985df2227` — /run/udev/links/disk\x2fby-designator\x2fesp
- `flatcar-1cb524bac06b114d8c41a8a6` — /run/udev/links/disk\x2fby-diskseq\x2f1
- `flatcar-1c411ec87f6acfcc4f55f92d` — /run/udev/links/disk\x2fby-diskseq\x2f1-part1
- `flatcar-bba8be43840f2f36a2b136ca` — /run/udev/links/disk\x2fby-diskseq\x2f1-part2
- `flatcar-1b737ae065846fd789823210` — /run/udev/links/disk\x2fby-diskseq\x2f1-part3
- `flatcar-cefadffd03a43b047ead19e4` — /run/udev/links/disk\x2fby-diskseq\x2f1-part4
- `flatcar-4e9e827b657b4c3060d82376` — /run/udev/links/disk\x2fby-diskseq\x2f1-part6
- `flatcar-9ff8e7d6973a4e9755171632` — /run/udev/links/disk\x2fby-diskseq\x2f1-part7
- `flatcar-e0348fda624c24f4577eb8fa` — /run/udev/links/disk\x2fby-diskseq\x2f1-part9

## D1-DIRECTORY-PACKAGE

Sentences: Q2,Q3,U1,U2. Applied rows: 22.

Reviewed directory-only package scaffolding has no same-package program or regular-file payload: NONE/NA/FACT_UNKNOWN. Q3 can classify directories by provenance, but creation and derivation from a recorded source are unknown. Installation metadata does not establish that provenance.

Manual check: Checked complete official file lists: every supplied pathname is a directory; dependency programs are not in this package.

- `fedora-370f9670318663db7d7af56f` — root:fonts-filesystem
- `fedora-639b8e0571307211e00cbfb0` — root:libreport-filesystem
- `fedora-e4b9d40339d4d7cefa55878c` — root:hunspell-filesystem
- `fedora-a9c8a55feb440518882c62f9` — root:mozilla-filesystem
- `fedora-9053b3a7e45ae753a4a9e8d3` — root:llvm-filesystem
- `fedora-5e338f6bb866db8e2a41edeb` — root:cmake-filesystem
- `fedora-291391442518d127bc2231d4` — user:efi-filesystem
- `fedora-c6e3487f1dd311c024cdaf4f` — user:cups-filesystem
- `fedora-2b5e35f23d38ef68d14e9eb4` — user:gnome-control-center-filesystem
- `fedora-9e1f16af76b3544acc56be62` — user:emacs-filesystem

## D1-DATA-PACKAGE

Sentences: U3,R2,U1. Applied rows: 457.

Explicitly reviewed packages containing only non-executable resources, reference data, translations, documentation or fonts are MATERIAL/NO/DECIDED by U3. A program in a different dependency package does not satisfy U1.

Manual check: Checked file lists and selected payload types. tzdata tables are not the setting selecting a zone; theme resources are not the setting selecting a theme; metapackages with documentation differ from fileless ones.

- `fedora-ba3bec32ce48f0d42c233721` — root:tzdata
- `fedora-be3b374981a3829a279d80ae` — root:words
- `fedora-56947d87a17faf33ccc2b388` — user:google-noto-emoji-fonts
- `mint-46b5afb6397df38a0f147efa` — root:libgtksourceview-3.0-common
- `mint-224e806a9e786a6e195a3fb8` — root:va-driver-all:amd64
- `tumbleweed-8e84d13ea1b940f02e6994e2` — root:gtk3-metatheme-breeze6
- `tumbleweed-ef3aa7aca9b0dae41430097d` — root:hack-fonts
- `tumbleweed-4cddc16d9e0fac1b3a153037` — root:patterns-kde-kde_utilities
- `tumbleweed-416cf73a88cad1ab9ce270fd` — user:kidentitymanagement-lang
- `tumbleweed-8e744ca7c5bce1c753ac7525` — user:google-opensans-fonts

## D1-SEPARATE-DEFAULTS

Sentences: Q2,Q2a,U3,R1,R2,U1. Applied rows: 140.

Reviewed packages without same-package executable code contain configuration values. Configuration has Q2/Q2a SETTING/YES versus U3 MATERIAL/NO; when distinct ancillary material exists, output MIXED and identifies both subsets. Single-policy cases are TWO_WAYS.

Manual check: Checked actual configuration filenames and ancillary documentation/resources. Wholly-configuration multi-file corrections are recorded individually, not counted as homogeneous mixtures.

- `mint-541845641e039a9006fb173c` — root:brasero-common
- `mint-488c9c6152f9a5f984d35271` — root:libreoffice-uiconfig-common
- `tumbleweed-cfee098921beb2a44ecc53d7` — root:gtk3-data
- `tumbleweed-9634ad371fce8297a5cd9f39` — root:ca-certificates-mozilla
- `tumbleweed-a27b3688034c9ebdda011757` — root:ImageMagick-config-7-SUSE
- `tumbleweed-3aaa4a271e91672f44eb2d31` — root:plasma6-session
- `tumbleweed-fb68f8c55638ce0185db1206` — user:displaymanager-sysconfig
- `tumbleweed-4d0a78044e911ca278f2ee68` — user:system-group-audit
- `fedora-4a22d436d49ac52def61f28f` — root:hwdata
- `fedora-d2d21c3359edaae41805b76b` — root:xml-common

## D1-MACRO-CONTENTS

Sentences: Q1,Q2,U3,U1. Applied rows: 12.

Reviewed RPM-macro packages whose file lists omit expansion contents are NONE/NA/FACT_UNKNOWN: plain substitution values and executable shell/Lua expansions have different Q1/Q2 results. Filename alone cannot determine U1.

Manual check: Checked actual macro paths in package lists; RPM manual confirms both plain and executable macro forms. No execution is inferred from a macros.d pathname.

- `fedora-fb0599f30fe760a9d966e609` — root:fedora-release-common
- `fedora-d22742c2d858ca4320eeec76` — root:firewalld-filesystem
- `fedora-54ecb7154dd261f862688cde` — root:javapackages-filesystem
- `fedora-8438efe3ac4e53814216c4cc` — root:color-filesystem
- `fedora-087d11c0fcdb74782da40ad0` — user:fedora-release-common
- `fedora-23f5223f65f30b0f662b1ed3` — user:firewalld-filesystem
- `fedora-29f0d46386a444ac59fb4906` — user:javapackages-filesystem
- `fedora-72d00200df0ea12fe939ab8c` — user:color-filesystem
- `tumbleweed-dc123bdc513c409035c84aa5` — root:hicolor-icon-theme
- `tumbleweed-805fce69915400aba79d77c2` — root:javapackages-filesystem

## D1-EMPTY-PACKAGE

Sentences: Q1,Q2,Q3,U1,R1,R2. Applied rows: 20.

A reviewed fileless dependency package is NONE/NA/NOT_DECIDED. The text does not classify the fileless package/dependency aggregate; U1 only covers contents in the same package as a program.

Manual check: Checked official payload lists are empty rather than unavailable, and descriptions identify dependency packages. Blank failed requests were excluded and investigated separately.

- `fedora-6c4e6a443cca6462b71a16e4` — root:dbus
- `fedora-1a77dc2217703003a26ef1b1` — root:qemu-system-x86
- `fedora-422a3d919b9e167f68b19178` — root:libvirt-daemon-kvm
- `fedora-403319a64492c37639799f51` — root:passwdqc
- `fedora-6a287db8da44086cfca8ec9e` — user:google-noto-color-emoji-fonts
- `fedora-7571a286b32edb46d3b08dc8` — user:libvirt-daemon-driver-storage
- `fedora-eadc13919871cf4ec2e78d3a` — user:hyperv-daemons
- `tumbleweed-ea0c53ef0c50fd2e8fcaf935` — root:myspell-dictionaries
- `tumbleweed-e181871cb7da8fceff1721cb` — root:openssh
- `tumbleweed-255999ada4afb173b049b428` — user:permissions

## D1-FIRMWARE-CAPABILITY

Sentences: A1,Q1,U3,U5,U1. Applied rows: 68.

Reviewed hardware firmware or platform boot-code packages without runnable host helpers are NONE/NA/FACT_UNKNOWN when compatible hardware/boot execution is unproved. Code format alone does not establish A1/Q1 on this computer.

Manual check: Checked firmware/EFI/ROM payloads and excluded packages containing gen_grub_cfgstub. Inventory package presence does not establish supported hardware, active firmware or compatible launch environment.

- `fedora-011a3c8a5d3fa8afc639db45` — root:iwlbluetooth-firmware
- `fedora-af7ad761d8f132f73b217eef` — root:edk2-ovmf
- `fedora-da83ec25380057f49914af2e` — root:nvidia-gpu-firmware
- `fedora-4aeb8ef58f03412cf56ccd3a` — root:iwlegacy-firmware
- `fedora-6ea87f9a8daa8f1f8dc79f3c` — root:edk2-shell-x64
- `fedora-831543ea9963b468a6ce516c` — user:shim-x64
- `fedora-4b6cc5cb464ec8856b9e0706` — user:linux-firmware
- `fedora-1aff221d5eb7ebdeb89f61d0` — user:iwlwifi-dvm-firmware
- `fedora-9b799e73b210f14b6db6bd81` — user:brcmfmac-firmware
- `fedora-36738aab58a509e65b3265e9` — root:shim-x64

## D1-FONT-CONFIG

Sentences: Q2,U3,R1,R2,U1. Applied rows: 205.

Reviewed font packages containing both fonts and active font-selection preferences are MIXED: font material NO; preferences SETTING/YES by Q2 versus MATERIAL/NO by U3. No same-package executable establishes U1.

Manual check: Checked actual font files and conf.d/conf.avail preference payloads, rather than relying on a font package name. Fontconfig documentation establishes preference semantics.

- `fedora-8c3e89a5ae934125438bc720` — root:adwaita-mono-fonts
- `fedora-80283cd067e1f44857e96a29` — root:urw-base35-z003-fonts
- `fedora-747acdcead624545038d341d` — root:google-noto-serif-telugu-vf-fonts
- `fedora-8af0ea08a9644e1f7b74ae16` — root:google-noto-sans-ol-chiki-vf-fonts
- `fedora-4c92148469182dcc4f516d8c` — root:stix-fonts
- `fedora-e65bcf0a9d3a4db9cde1580a` — user:urw-base35-d050000l-fonts
- `fedora-64d1f368097d17953df425f1` — user:google-noto-serif-hebrew-vf-fonts
- `fedora-d8c664ea19fec4622ac0b73b` — user:google-noto-sans-khmer-vf-fonts
- `fedora-bd1c9e7d5a8e6e04030a9cf2` — user:abattis-cantarell-fonts
- `mint-515816f17b3f22b0d4757ac2` — root:fonts-ubuntu

## D1-XEN-CAPABILITY

Sentences: A1,Q1,U3. Applied rows: 182.

The explicitly inventoried x86_64-xen GRUB modules and pvboot image are NONE/NA/FACT_UNKNOWN: executable compatibility with a launchable Xen environment is not established. Executable permission bits alone cannot settle Q1/U3.

Manual check: Checked architecture-qualified paths and raw regular-file types/modes for ten distinct modules; no current or alternate compatible Xen launch path is assumed.

- `flatcar-01863b09aee65b84699191fd` — /boot/flatcar/grub/x86_64-xen/adler32.mod
- `flatcar-6aa9c7cc664d46b907fd209e` — /boot/flatcar/grub/x86_64-xen/affs.mod
- `flatcar-09261b13f0242be389097b3d` — /boot/flatcar/grub/x86_64-xen/afs.mod
- `flatcar-da06825ad4492564f1dfb14d` — /boot/flatcar/grub/x86_64-xen/afsplitter.mod
- `flatcar-400f1d60de3d783e79bfcc2c` — /boot/flatcar/grub/x86_64-xen/all_video.mod
- `flatcar-a3d82262b27bd1f7b771dad1` — /boot/flatcar/grub/x86_64-xen/appendedsig.mod
- `flatcar-30b481633c0e03cf9a5e828b` — /boot/flatcar/grub/x86_64-xen/archelp.mod
- `flatcar-a5038bee601026e1410729a3` — /boot/flatcar/grub/x86_64-xen/asn1.mod
- `flatcar-c14413689e4e173b4bd79592` — /boot/flatcar/grub/x86_64-xen/backtrace.mod
- `flatcar-8184293b91be010779dc1e39` — /boot/flatcar/grub/x86_64-xen/bfs.mod

## D1-DEBUG-SYMBOLS

Sentences: U3,R2,U1. Applied rows: 12.

The reviewed Mint separated debugging-symbol packages are MATERIAL/NO/DECIDED. Symbols describe executable code delivered in other packages; U1 cannot cross that boundary.

Manual check: Checked each source debian/control description; for descriptions saying unstripped binaries, inspected debian/rules dh_strip --dbg-package separation, including cjs, nemo and cinnamon-desktop.

- `mint-ff58418b0703f7cafb0e40ac` — root:cinnamon-control-center-dbg
- `mint-6bce92151e226b7ac96fe618` — root:cinnamon-dbg
- `mint-df392dd32c573575dc9af6cb` — root:libcinnamon-desktop-dbg:amd64
- `mint-3112f73fda8dde2c470e105d` — root:libcinnamon-menu-3-0-dbg
- `mint-786315c46bebc2d5e4cedb2e` — root:libcjs-dbg
- `mint-2308d2a796c876e3b9e27bd3` — root:libcvc-dbg:amd64
- `mint-0485f4f637e07234412cee1b` — root:muffin-dbg
- `mint-7edd253b844e18b8ddcdadd2` — root:nemo-dbg
- `mint-64c62b8bf5b610e37b30e296` — root:pix-dbg
- `mint-1d2ad4a6b5f28aaa86d733fa` — root:xed-dbg

## Individually examined rows

Remaining rows were assigned explicit path/package decisions in d1_files.py, d1_rest.py, d1_rest2.py and d1_finish.py. Their mapping tables are writing aids, not suffix-based semantic classifiers. Stored groups were checked against actual direct-member arrays and raw filesystem types; cut member arrays were reconstructed from the named raw inventory. Group reasons identify program, policy, material, runtime-record and unresolved subsets as applicable.

The correction overlay rows-d1.corrections.tsv supersedes specified provisional rows from the same attempt. It records XDG generated-unit source coverage, package host helpers, runnable catalogue recipes and entirely-policy multi-file packages. The original completed rows remain available for review.

Public factual references supplementing per-row package URLs: https://man.openbsd.org/sshd_config ; https://www.kernel.org/doc/Documentation/filesystems/sysfs.txt ; https://www.freedesktop.org/software/systemd/man/latest/udev.html ; https://www.freedesktop.org/software/systemd/man/latest/systemd-xdg-autostart-generator.html ; https://rpm.org/docs/6.0.x/man/rpm-macros.7 ; https://www.freedesktop.org/software/fontconfig/fontconfig-user.html .

# A1 scripted classification rules

Ten rules were used. Rule membership after corrections is in (not published: trial intermediate downloads and scratch); all other rows were individually reviewed and encoded by ID or explicit reviewed lists. The merged table is `rows-a1.final.tsv`. The append-only work log and correction overlay are retained.

Q1, Q2, Q3 are applied in the order R5 states. U1/U2 are coverage exceptions; they do not create a conflict merely because an underlying supplied file is also non-executable. Functional Q2/Q3 versus U3 conflicts are retained. No decision relies on an older inventory classification.

## A1-STORE-PATH

Applied rows: 73. Sentences: R5,Q1,Q2,Q3,U1,U2,U3. Result: NONE / NA / FACT_UNKNOWN.

Residual path-only store rows after individually identified outputs and programs are removed. A package-like store name does not establish all members, ability to execute, acquisition with a program, or its particular recorded build source. This is a factual deficit, not a gap in PAGE.

Manual check: Checked each supplied store path against its raw package listing: it adds no payload or derivation information. Known generated outputs were removed from this rule.

Ten manually checked rows:

- `nixos-e3ea449be8` — `/nix/store/0kk05fksy78xybp0jvvbnyiindqxz7ag-mailcap-2.1.54`.
- `nixos-de918b3443` — `/nix/store/2z20x3qpaf2in6gsfpgflaqb3ckf5ijr-dns-root-data-2025-04-14`.
- `nixos-e9323e3380` — `/nix/store/3kqf0x3r47nirq88vlgbqzfnv41x3cna-kmod-blacklist-31+20240202-2ubuntu8`.
- `nixos-055cb95e1b` — `/nix/store/3qcyxn4r28d41w26kvgrwbji4p5hrs0b-hostname-hostname-debian-3.25`.
- `nixos-531f170216` — `/nix/store/50a3iajs470n55xg6qlixpgm2fsswyk2-shared-mime-info-2.4`.
- `nixos-127a576660` — `/nix/store/a5zrx2wp7nwwgcwyg303linq3wzdgm2f-make-initrd-ng-0.1.0`.
- `nixos-b157b75a6a` — `/nix/store/d6yq8c4lkbvhx7cnsmy53w378gdh304m-kmod-debian-aliases.conf-30+20230601-2`.
- `nixos-7584680ee6` — `/nix/store/f32dps8xknyf4s24nsznfqdmnqcap9p0-system-sendmail-1.0`.
- `nixos-191bc7ac6b` — `/nix/store/gj6hz9mj23v01yvq1nn5f655jrcky1qq-nixos-option.nix`.
- `nixos-610d1475a9` — `/nix/store/gri05573gnm4l1nr9jxcyckx9gkgl24f-nixos-manual.desktop`.

## A1-DEVICE

Applied rows: 12. Sentences: R1,R5,Q2a. Result: SETTING / YES / DECIDED.

Runtime *.device unit groups representing devices, rather than stored unit files. Q2a expressly includes devices. The units listings establish a device-only group; no directory contents are inferred.

Manual check: Each sample lists only device units; the source references identify runtime inventories.

Ten manually checked rows:

- `coreos-a3f2270221` — `unpackaged *.device`.
- `coreos-88335c6c87` — `unpackaged *.device`.
- `debian-a3f2270221` — `unpackaged *.device`.
- `debian-88335c6c87` — `unpackaged *.device`.
- `nixos-a3f2270221` — `unpackaged *.device`.
- `nixos-88335c6c87` — `unpackaged *.device`.
- `arch-a3f2270221` — `unpackaged *.device`.
- `arch-88335c6c87` — `unpackaged *.device`.
- `silverblue-a3f2270221` — `unpackaged *.device`.
- `silverblue-88335c6c87` — `unpackaged *.device`.

## A1-OWNERSHIP

Applied rows: 253. Sentences: R5,Q1,Q2,Q3,U1,U2,U3. Result: NONE / NA / FACT_UNKNOWN.

Residual package-owned path groups without established per-package payload membership or generated-file provenance. The raw package-files list is a union: ownership alone cannot establish U1 receiving this object in the same package as a program. Root directory rows remain single directory objects where members=1.

Manual check: Checked raw file types and targets, counts, and the flat ownership list; these do not identify the owning program package or distinguish generated/ghost content from supplied content.

Ten manually checked rows:

- `coreos-3cd182c07b` — `/boot`.
- `coreos-827c5914e9` — `/boot/efi`.
- `coreos-1d70ce548d` — `/boot/grub2`.
- `coreos-037231a728` — `/etc`.
- `coreos-9945c88deb` — `/etc/NetworkManager`.
- `coreos-d20d960ea0` — `/etc/adjtime`.
- `coreos-341d2df2d9` — `/etc/aliases`.
- `coreos-d3d071d2ba` — `/etc/alternatives`.
- `coreos-a4c2c16ae9` — `/etc/audit`.
- `coreos-e2885ad43a` — `/etc/authselect`.

## A1-WORKFILE

Applied rows: 87. Sentences: R2,Q3,U3. Result: NONE / NO / TWO_WAYS.

Non-executable work-state files whose runtime role is established: locks, completion stamps, operational histories, or equivalent state. Q3 says PROGRAM_RECORD, U3 says MATERIAL. Neither reading requires recording. Computed representations with identified recorded sources are excluded under U2.

Manual check: Checked that samples are non-executable operational locks/stamps/state, rather than executable hooks or selected configuration. The man-db option cache and authselect checksum were removed after source verification.

Ten manually checked rows:

- `coreos-fefd90f542` — `/etc/.pwd.lock`.
- `coreos-5932b79e41` — `/etc/.updated`.
- `coreos-5a0b991b97` — `/var/.ostree-selabeled`.
- `coreos-1711d3c8c4` — `/var/.updated`.
- `coreos-99d362e5d4` — `/var/lib/coreos-populate-lvmdevices.stamp`.
- `debian-fefd90f542` — `/etc/.pwd.lock`.
- `debian-769028f968` — `/var/lib/python`.
- `debian-1108460cc8` — `/var/lib/shells.state`.
- `nixos-5932b79e41` — `/etc/.updated`.
- `nixos-cf8679a110` — `/nix/var/nix`.

## A1-SETTING-FILE

Applied rows: 59. Sentences: R1,R2,R5,Q2,Q2a,U3. Result: NONE / NA / TWO_WAYS.

Non-executable operative system-setting files, without established U1/U2 coverage. Q2/Q2a makes their selected values SETTING/YES; U3 makes their files MATERIAL/NO. R5 orders Q1–Q3 but supplies no precedence between these questions and U3.

Manual check: Checked actual role of blacklist, credentials, access-control, timezone, module-load, and subordinate-ID files; no executable shell code or supplied-package exception was identified.

Ten manually checked rows:

- `coreos-1af8deec0e` — `/etc/modprobe.d`.
- `debian-2adfd50853` — `/etc/gshadow`.
- `debian-d47133480a` — `/etc/hosts.allow`.
- `debian-b8a8c42f35` — `/etc/hosts.deny`.
- `debian-966442e2a8` — `/etc/localtime`.
- `debian-9e65e302c3` — `/etc/modules`.
- `debian-cfe66bc678` — `/etc/shadow`.
- `debian-f18cbc897b` — `/etc/subgid`.
- `debian-f17149d114` — `/etc/subuid`.
- `debian-8c833da179` — `/etc/timezone`.

## A1-BUILT

Applied rows: 81. Sentences: U2. Result: BUILT / COVERED / DECIDED.

Identified generated representations of required program or setting sources: compiled caches, generated activation links, or assembled installed-source indexes. The source must be identified, not merely the fact that a program wrote the output. Coverage refers to the source line in the proposed declaration.

Manual check: The ld.so cache derives from the selected installed libraries; each sampled Nix link explicitly targets /etc/static and thus the generated system configuration.

Ten manually checked rows:

- `debian-f2368b74f2` — `/etc/ld.so.cache`.
- `nixos-4e2b0e7d53` — `/etc/binfmt.d`.
- `nixos-df290cde86` — `/etc/dbus-1`.
- `nixos-228a030233` — `/etc/default`.
- `nixos-7ec0efa4d1` — `/etc/environment.d`.
- `nixos-41632fad0a` — `/etc/fonts`.
- `nixos-dd17eb66aa` — `/etc/fuse.conf`.
- `nixos-197b8faf2d` — `/etc/kbd`.
- `nixos-8f95c550d5` — `/etc/lsb-release`.
- `nixos-1ba388a08e` — `/etc/lvm`.

## A1-INTERPRETED

Applied rows: 14. Sentences: R1,R5,Q1,U4. Result: PROGRAM / YES / DECIDED.

Identified executable interpreted source files, including Scheme system/home expressions, shell startup files, and command-capable editor/debugger initialization code. Q1 precedes Q2/Q3; their purpose as configuration does not erase execution. No U1/U2 coverage was established for these particular copies.

Manual check: Inspected the named file and inventory members for each sample: Scheme expressions, Vim scripts, shell startup code, and gdbinit are interpreted instruction inputs with command capability.

Ten manually checked rows:

- `debian-211f893687` — `/etc/grub.d`.
- `guix-1ed80370a6` — `/etc/config.scm`.
- `guix-8bcc29aa90` — `/home/guest/guix-home-config.scm`.
- `guix-9690fd0a05` — `/home/guest/home.scm`.
- `guix-88a33ee425` — `/root/guix-home-config.scm`.
- `nixos-dfc5f24c51` — `/home/census/.vimrc`.
- `guix-a5b845fd5c` — `/home/guest/.vimrc`.
- `guix-dea3c6354f` — `/home/guest/.zprofile`.
- `guix-14d33b9392` — `/root/.zprofile`.
- `guix-a9e486a84b` — `/home/guest/.config/gdb`.

## A1-UNEXPANDED

Applied rows: 48. Sentences: R5,Q1,Q2,Q3,U1,U2,U3. Result: NONE / NA / FACT_UNKNOWN.

Residual multi-member stored groups whose inline samples do not identify every relevant member or its role, and whose full raw files are outside the permitted roots. No contents are imported from a similar machine; public documentation cannot establish the actual omitted local members.

Manual check: Compared members count with samples and checked the indicated raw root. Samples are incomplete or their installation/generated origins remain unresolved; forbidden raw-X1/X2/E6 paths were not opened.

Ten manually checked rows:

- `alpine-0075a76d48` — `/etc/ssh`.
- `alpine-995a8560ba` — `/var/lib/cloud`.
- `arch-0075a76d48` — `/etc/ssh`.
- `arch-b618c77d89` — `/var/cache/pacman`.
- `arch-cafdef0617` — `/var/lib/pacman`.
- `silverblue-b86fee9a16` — `/etc/systemd`.
- `silverblue-418d5e5b2b` — `/var/cache/rpm-ostree`.
- `ubuntu-5bf2e2415a` — `/boot/efi`.
- `ubuntu-228a030233` — `/etc/default`.
- `ubuntu-0075a76d48` — `/etc/ssh`.

## A1-SAME-PACKAGE

Applied rows: 61. Sentences: U1. Result: PACKAGE_PART / COVERED / DECIDED.

Inventoried supplied support/default groups matched against official file lists of the very binary packages that also contain executable programs. Every non-directory member must match; reconstruction must match the inventory count. Directory structure belonging to those supplied components is included. Dependencies alone do not qualify.

Manual check: Compared each listed member with official Debian/Fedora payloads and confirmed an executable in that same binary package. The listed ten examples use cloud-init, adduser, dpkg, apparmor, libc-bin, e2fsprogs, apt, and man-db packages.

Ten manually checked rows:

- `debian-9945c88deb` — `/etc/NetworkManager`.
- `debian-45c059e4f3` — `/etc/adduser.conf`.
- `debian-d3d071d2ba` — `/etc/alternatives`.
- `debian-69b4dd2a4c` — `/etc/apparmor`.
- `debian-d68859230e` — `/etc/bindresvport.blacklist`.
- `debian-3eca422b52` — `/etc/cloud`.
- `debian-bb79b160fd` — `/etc/cron.d`.
- `debian-2aaffbbdf6` — `/etc/cron.daily`.
- `debian-effe16345a` — `/etc/cron.weekly`.
- `debian-bfd096eece` — `/etc/deluser.conf`.

## A1-GENERATED-STORE

Applied rows: 153. Sentences: D1,D3,U2. Result: BUILT / COVERED / DECIDED.

Explicitly identified Nix/Guix configuration outputs, assembled indexes, generated activation support, or module-import copies produced from the system description and selected programs. Exact name allowlists are recorded in a1_refine_store.py; generic package outputs and arbitrary source trees are excluded.

Manual check: Checked ten distinct named generated outputs against their inventory paths and the documented construction of system configuration from its source description; these are generated configuration artifacts, not arbitrary package dependencies.

Ten manually checked rows:

- `nixos-a332c16c0a` — `/nix/store/00gmmr7b9slac4srbg4rqlwrw1k9rxnf-nix.conf`.
- `nixos-bd414d6b6a` — `/nix/store/07n7039ak38i26hgf2s3501y9l5f6fs2-dhcpcd.conf`.
- `nixos-e78f81d36e` — `/nix/store/0f5y6wcik5ldry8d1kl4a2f7hi5mq9pn-hosts`.
- `nixos-903eca0ec8` — `/nix/store/0fhmy5gh22w9ysg62aj04bah31xyb0a5-etc-gai.conf`.
- `nixos-70bca474fd` — `/nix/store/0qqf2bnfp16a6y3448n7bz1rl9yyfvjq-etc-fuse.conf`.
- `nixos-a738960c81` — `/nix/store/15qy3pqkq3503xgypbmp3dbinngslxy6-X-Restart-Triggers-reload-systemd-vconsole-setup`.
- `nixos-d3ac6fc3e9` — `/nix/store/1za4k4r5lkd3j0hnxhrazwwvyy9x61s6-etc-hostname`.
- `nixos-532c5e327b` — `/nix/store/24ky217wazac3asqmzw1jy76nx7b368v-tmpfiles.d`.
- `nixos-4d1b734b98` — `/nix/store/26lxap4w380sadn4lv6fg6lp6zb7jbw5-50-coredump.conf`.
- `nixos-12077741ee` — `/nix/store/2l116v46iakhi2jsrqzvigxb968302nr-X-Restart-Triggers-resolvconf`.

## Factual documentation and audit materials

- [NixOS generation and source descriptions](https://nixos.org/guides/how-nix-works/).
- [NixOS etc generation implementation](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/system/etc/etc.nix).
- [GNU Guix Reference Manual, G-expressions and operating-system configuration](https://guix.gnu.org/manual/en/guix.pdf).
- [systemd device units](https://www.freedesktop.org/software/systemd/man/248/systemd.device.html).
- [ldconfig](https://www.man7.org/linux/man-pages/man8/ldconfig.8.html).
- (not published: trial intermediate downloads and scratch) and (not published: trial intermediate downloads and scratch) preserve official URL-to-payload mappings. (not published: trial intermediate downloads and scratch) records raw members and Debian URL matches. The Fedora matcher is (not published: trial helper scripts); it requires executable commands in the same binary package.
- (not published: trial helper scripts) verifies 1084 unique matching IDs, allowed labels, exact output header, and word limits. This is a mechanical check, not independent substantive acceptance.

# A3R scripted classification rules

15 homogeneous rules. Full final membership is in (not published: trial intermediate downloads and scratch); other rows were inspected by explicit member/path lists and serialized individually.

Q1, Q2 and Q3 are tested in R5 order. U1 and U2 are coverage statements. Nonexecutable-file U3 conflicts with functional Q2/Q3/U7 classifications where coverage does not determine the result. Missing factual contents are marked FACT_UNKNOWN, not treated as omissions in PAGE.

All subtree assessments use the inline description and allowed raw filesystem/candidate inventories. The original `(not published: direct evidence over 2 MB)` named by some subtree descriptions was not opened. When a raw descendant listing could not reconstruct the selected members sufficiently, the result remains FACT_UNKNOWN.

## A3-GROUP

Applied rows: 39. Sentences: Q2a,R1. Result: SETTING / YES / DECIDED.

The local Unix group identity and membership determine permission rights. Q2a names rights explicitly. This classifies the group object, not a stored /etc/group file.

Manual check: Checked ten distinct GID and membership entries, including empty groups, against the supplied raw group lines.

Ten manually checked rows:

- `424cb5f40e407805606b43e3` — `root`.
- `2f8d930a409d1f2bdd2c5fa3` — `news`.
- `66f84c6596ff4a6dc3ea673c` — `fax`.
- `9a8089d2eeea3b59a0b02b99` — `www-data`.
- `b72dd4393cd9f7458b722482` — `irc`.
- `da017f5c4a67da07e8a06462` — `staff`.
- `1d85d40be9bd534d0216f83d` — `systemd-timesync`.
- `67c5fe367565649d58a7dac6` — `systemd-resolve`.
- `21cd7479491cdca0c99ad183` — `rtkit`.
- `31bd900cf43ed37298d6d895` — `colord`.

## A3-PROCESS

Applied rows: 22. Sentences: Q1,R5,U6,R1. Result: PROGRAM / YES / DECIDED.

A reported running executable with its own process satisfies Q1 and U6. A row aggregating PIDs of that executable has the same decision.

Manual check: Checked the ten executable names and PID evidence: dbus-daemon, conmon, gvfsd, two Netdata helpers, timesyncd, networkd, NetworkManager, cupsd and cups-browsed.

Ten manually checked rows:

- `1c460643fdd8cfbbd196d5c8` — `10`.
- `42c8a140e560dc29380e1d8c` — `12`.
- `1de8c224f0b98ee3c699a8f1` — `15`.
- `5170ad8d1f6cab983ec4aac9` — `2`.
- `405fd3b1305197a3b82e9395` — `204`.
- `0182a17a4f357d35fb9e7954` — `33`.
- `2130dee9e966a8190632a24f` — `395`.
- `5bf49f96a1afbe0b43e14736` — `78`.
- `0720c840cf4025df688545f2` — `82`.
- `e117d280137522e247ca6e90` — `9`.

## A3-PACKAGED-METADATA

Applied rows: 914. Sentences: U1. Result: PACKAGE_PART / COVERED / DECIDED.

Installed package metadata accompanies executable code in that same distribution: Python dist-info, npm program manifests, or bundled editor extension metadata. A dependency in another package does not satisfy this rule. Data-only packages and repository manifests without established package receipt were excluded.

Manual check: Checked the ten named distributions and their companion code: setuptools, rich, accepts, foreground-child, @noble/hashes, which, lru-cache, minipass, VS Code profile-table, and python-debian. Raw filesystem evidence confirms code; npm archive fields confirm package identities where present.

Ten manually checked rows:

- `51cba7cfc1bf2684737e1902` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools-80.10.2.dist-info/METADATA`.
- `dc5f771fd89e773fe701d2b2` — `/home/user/.local/share/pipx/venvs/httpie/lib/python3.13/site-packages/rich-15.0.0.dist-info/METADATA`.
- `3c13c1b446f62a2091e66f53` — `/home/user/Projects/express/node_modules/accepts/package.json`.
- `fe9da317da5b967b33c925dc` — `/home/user/Projects/express/node_modules/spawn-wrap/node_modules/foreground-child/package.json`.
- `9ccb3e1db3c71ae0579ef07e` — `/home/user/Projects/express/node_modules/@noble/hashes/package.json`.
- `2e9eb7a5d906ca90c5e08108` — `/home/user/Projects/express/node_modules/which/package.json`.
- `12db1f81bda753113f8c78e7` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/lru-cache/package.json`.
- `b1f92c6af383244e223ed275` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/minipass-pipeline/node_modules/minipass/package.json`.
- `89263f1523eab494b081abea` — `/usr/share/code/resources/app/extensions/ms-vscode.vscode-js-profile-table/package.json`.
- `dc127f353179f767622f14f2` — `/usr/lib/python3/dist-packages/python_debian-1.0.1.dist-info/METADATA`.

## A3-PROJECT-MANIFEST

Applied rows: 20. Sentences: Q1,Q2,Q3,U1,U3. Result: NONE / NA / FACT_UNKNOWN.

The actual manifest content/use or same-package receipt is not established for the reviewed project/test repository manifests. Names alone cannot decide active launch values, inert test fixtures, or covered program companions.

Manual check: Checked the ten supplied manifest paths and found no corresponding content in the allowed npm manifest archive; the raw filesystem gives only file metadata. The executable bit on the React-nginx JSON file does not make JSON executable code.

Ten manually checked rows:

- `111ac6ae8f61f144f23a651b` — `/home/user/Projects/express/package.json`.
- `1755b8b12329fa9ef4e7d695` — `/home/user/Projects/awesome-compose/react-express-mongodb/backend/package.json`.
- `95e10fb176d8247651f64687` — `/home/user/Projects/awesome-compose/angular/angular/package.json`.
- `dfea1ccd803a93bd82d031c8` — `/home/user/Projects/awesome-compose/vuejs/vuejs/package.json`.
- `4fe53d82e2d45abc64274c5d` — `/home/user/Projects/awesome-compose/react-express-mysql/frontend/package.json`.
- `16ad8b552b196edd6936655b` — `/home/user/Projects/awesome-compose/react-java-mysql/frontend/package.json`.
- `bf9cdf50537bde62221191cf` — `/home/user/Projects/awesome-compose/react-nginx/package.json`.
- `d4a673ba0f9e480ad29d2ae8` — `/home/user/.nvm/test/fast/Unit tests/mocks/project_dirs/no-nesting-both/package.json`.
- `471978163bc81d841e96f954` — `/home/user/.nvm/test/fast/Unit tests/mocks/project_dirs/nested-both/package.json`.
- `de96b9753d56039499868261` — `/home/user/.nvm/test/slow/nvm reinstall-packages/test-npmlink/package.json`.

## A3-ELPA

Applied rows: 48. Sentences: Q1,U4,U1,U2,R1. Result: PROGRAM / YES / DECIDED.

Each reviewed installed ELPA group contains executable Emacs Lisp constituting its program. Same-package accompanying data and bytecode compiled from its sources are included through U1/U2. An unrestricted Lisp program is not shown to satisfy the restricted-code condition in U5.

Manual check: Checked full member arrays: each sample contains .el code and corresponding .elc copies, with only its package metadata, manuals or other companions. Verified individual file types, rather than treating the directory name as proof.

Ten manually checked rows:

- `93a93428a9d00a2b2aac9e6f` — `/home/user/.emacs.d/elpa/ace-window-20220911.358`.
- `2849da8d3ffd4d63a249cb05` — `/home/user/.emacs.d/elpa/compat-31.1.0.0`.
- `b57acba86305d76781092c20` — `/home/user/.emacs.d/elpa/diff-hl-20261001.135`.
- `2de188ef32a4888a6c5dfacd` — `/home/user/.emacs.d/elpa/embark-20260610.302`.
- `4a3a2165780fe4bdeefc00e5` — `/home/user/.emacs.d/elpa/flycheck-eglot-20260810.1731`.
- `25869031ce72c51019016578` — `/home/user/.emacs.d/elpa/llama-20261001.1538`.
- `73f9ca51f63a8a99456a158c` — `/home/user/.emacs.d/elpa/operate-on-number-20231114.1921`.
- `a5e614ff093c756b5eb313dc` — `/home/user/.emacs.d/elpa/rainbow-delimiters-20210515.1254`.
- `28c2162d8f319e0dbebb54ab` — `/home/user/.emacs.d/elpa/transient-20261113.1458`.
- `f268c0c891b35623595c114b` — `/home/user/.emacs.d/elpa/zop-to-char-20260105.452`.

## A3-SHELL-AND-DOCS

Applied rows: 327. Sentences: Q1,U3,U4,R1,R2. Result: NONE / NA / MIXED.

For the reviewed direct-member groups containing only sourceable .zsh/completion code and nonexecuted documentation, code is PROGRAM/YES and documentation MATERIAL/NO. These source-tree groups have no established same-package coverage. Extensionless unfamiliar fixtures are excluded.

Manual check: Checked all members of ten sample groups: each has README.md and its named .plugin.zsh. Shell source can execute through the installed shell even without an executable mode bit.

Ten manually checked rows:

- `02509ece652faa30d530a089` — `/home/user/.oh-my-zsh/plugins/ansible`.
- `2e55b962c4165c285c96a9e1` — `/home/user/.oh-my-zsh/plugins/cloudfoundry`.
- `07618ec243b56b1f72ea40c8` — `/home/user/.oh-my-zsh/plugins/fancy-ctrl-z`.
- `00ef3ec2875b821c3a651330` — `/home/user/.oh-my-zsh/plugins/hanami`.
- `cd63ca51db3751138b8437a7` — `/home/user/.oh-my-zsh/plugins/kops`.
- `4744c5712ac928b5dcfaec2e` — `/home/user/.oh-my-zsh/plugins/nmap`.
- `31c628b483398e953ad3d390` — `/home/user/.oh-my-zsh/plugins/pulumi`.
- `223cb070f41f6dc7a7ff0dbc` — `/home/user/.oh-my-zsh/plugins/skaffold`.
- `493bd0f8dc99ec1aae6a61c6` — `/home/user/.oh-my-zsh/plugins/tig`.
- `4f25115549cd290ab72efd82` — `/home/user/.oh-my-zsh/plugins/zoxide`.

## A3-MIME-INDEX

Applied rows: 13. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The standard generated per-type MIME database XML files are constructed from installed MIME definitions. U2 covers the generated list through its recorded source definitions; this is not a rule that every file under /usr/share is covered.

Manual check: Checked every direct member and its regular-file type in ten content-type groups. They contain only the generated XML descriptions, with counts 516,62,1,101,7,7,9,150,33,1 respectively.

Ten manually checked rows:

- `4aba607ff59c3ee376310758` — `/usr/share/mime/application`.
- `4ff815d792c6f07c0e70cdd2` — `/usr/share/mime/audio`.
- `a1bc9af2c8b24e04764d16e0` — `/usr/share/mime/chemical`.
- `946c59a84dd618138088be86` — `/usr/share/mime/image`.
- `a3a29542d4b538e850acb99b` — `/usr/share/mime/inode`.
- `7d4c3c7f666b1008ee71489d` — `/usr/share/mime/message`.
- `f4785d34ecdd63e5d9727007` — `/usr/share/mime/multipart`.
- `f9b368f6ebd3f6e3a358d20e` — `/usr/share/mime/text`.
- `b4719b4d765ff90d4af34b9b` — `/usr/share/mime/video`.
- `e5ab7eeee3f7f8114537bfea` — `/usr/share/mime/x-epoc`.

## A3-MAN-INDEX

Applied rows: 26. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The reviewed man-db cache groups contain derived lookup indexes, formatted-page cache layout and its constant cache tags. Their installed manual/source definitions and manager construction cover the generated representation under U2.

Manual check: Checked ten full member arrays containing index.db, cat directories and CACHEDIR.TAG; no user-authored setting or unrelated history file appeared in these groups.

Ten manually checked rows:

- `4510afc64020ce965c69c93a` — `/var/cache/man`.
- `d5d756c7be695e8e3c3240e3` — `/var/cache/man/da`.
- `359b5c84d186097c4737d4f3` — `/var/cache/man/fi`.
- `67cab6a3b21ee18171e913bf` — `/var/cache/man/hu`.
- `bf30125ac236b891339b4642` — `/var/cache/man/ja`.
- `2045c9f7bc5deb3e07489e08` — `/var/cache/man/nl`.
- `08d5b1a0eccbb1fe0ea550ec` — `/var/cache/man/pt_BR`.
- `ee5ad85821d870c36b151353` — `/var/cache/man/sl`.
- `e4ee0cd5019fba5e14c8c679` — `/var/cache/man/tr`.
- `6e304c9a1e2d8b725f108cc5` — `/var/cache/man/zh_TW`.

## A3-SERVICE-MARKERS

Applied rows: 23. Sentences: Q3,U3,R2. Result: NONE / NO / TWO_WAYS.

The selected deb-systemd-helper marker files remember earlier package enablement operations. Q3 calls them PROGRAM_RECORD and U3 calls their nonexecuted file form MATERIAL. Both allow omission. They are not the service-manager enablement links themselves.

Manual check: Checked ten complete marker groups and helper documentation. Named target directories contain helper state files for the listed services; parent directory groups with mixed contents were excluded.

Ten manually checked rows:

- `9140d0e0763d33c3a86e94f5` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-config.target.wants`.
- `13177aa156a7ffca6aadb143` — `/var/lib/systemd/deb-systemd-helper-enabled/default.target.wants`.
- `038156e92c4b157696ea5476` — `/var/lib/systemd/deb-systemd-helper-enabled/graphical.target.wants`.
- `e6c7b500df6175d8c883f1e4` — `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`.
- `54924688efdcbb112c962280` — `/var/lib/systemd/deb-systemd-helper-enabled/printer.target.wants`.
- `5e5ac15281a5827c5b46e88e` — `/var/lib/systemd/deb-systemd-helper-enabled/ssh.socket.wants`.
- `1810ae1e70bf481d6cba3512` — `/var/lib/systemd/deb-systemd-helper-enabled/sshd@.service.wants`.
- `2afaf280a4caf6a672848578` — `/var/lib/systemd/deb-systemd-helper-enabled/sysinit.target.wants`.
- `60af4555f895a621f8fdd8b5` — `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants`.
- `3dbad18363c3236ada19e5bb` — `/var/lib/systemd/deb-systemd-user-helper-enabled/sockets.target.wants`.

## A3-GIT-TEMPLATES

Applied rows: 11. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

Git initialization copies its supplied hook templates into each repository. The reviewed groups contain only those .sample template copies, whose recorded Git package source covers the copies under U2. Active non-template hooks are excluded.

Manual check: Checked all fourteen .sample files in each of ten sample rows against the raw listing and Git template documentation. The Flask repository with an extra pre-commit hook was separately classified.

Ten manually checked rows:

- `lived-t98b49255b3` — `/home/user/.config/nvim/.git`.
- `lived-tf3cef8f65e` — `/home/user/Projects/zlib/.git`.
- `lived-teaff14fb6e` — `/home/user/Projects/express/.git`.
- `lived-t5524f36a07` — `/home/user/Projects/dotfiles/.git`.
- `lived-t377338389c` — `/home/user/Projects/awesome-compose/.git`.
- `lived-tb8a7a2c063` — `/home/user/.emacs.d/.git/hooks`.
- `lived-ta4806d9131` — `/home/user/.oh-my-zsh/.git/hooks`.
- `lived-tc5d3d1ad66` — `/home/user/.nvm/.git/hooks`.
- `62c9ae1c4efb4911e0b9bb51` — `/home/user/.emacs.d/.git/hooks`.
- `35edf48c3f0ceba543518341` — `/home/user/.oh-my-zsh/.git/hooks`.

## A3-SSH-ACCESS

Applied rows: 72. Sentences: Q2a,R1. Result: SETTING / YES / DECIDED.

Each reviewed effective SSH value directly defines admission, permitted session rights, or network transport. Q2a expressly names access rules, rights and network settings. Generic helper paths, server-identity sourcing and cleanup values are excluded.

Manual check: Checked the ten complete option values and their OpenSSH semantics: PAM, minimum RSA size, Kerberos authentication, TTY permission, forwarding prohibition, trusted user CA, ciphers, accepted environment names, source network grouping and connection penalties.

Ten manually checked rows:

- `5f8fcf77e7c5041de9f3e517` — `ssh-access:usepam`.
- `64c3eeeb56074c666b06d5da` — `ssh-access:requiredrsasize`.
- `c820f0571c36594777b32e84` — `ssh-access:kerberosauthentication`.
- `d6235a098bb82243371dc8d0` — `ssh-access:permittty`.
- `63d8ebafc9125aab5fdb691d` — `ssh-access:disableforwarding`.
- `6fa7d4f75e0e35c7fade8b0d` — `ssh-access:trustedusercakeys`.
- `602b5e23a1883323cc8e5024` — `ssh-access:ciphers`.
- `d962db55ec61443e174b4687` — `ssh-access:acceptenv`.
- `363323f681d7fb46cf88fb80` — `ssh-access:persourcenetblocksize`.
- `b3bc32c5ee21a357406dd84d` — `ssh-access:persourcepenalties`.

## A3-SSHD-INTERNAL

Applied rows: 13. Sentences: Q2,Q2a,U1. Result: NONE / NA / FACT_UNKNOWN.

The enumerated operational SSH helper paths, server-identity sources and cleanup values are known, but human selection versus supplied defaults is not. They do not themselves establish incoming authorization under Q2a.

Manual check: Checked the ten complete effective values: Kerberos cleanup, GSSAPI cleanup/rekey storage, authentication information exposure, PID path, xauth path, two helper paths and two server host-key paths.

Ten manually checked rows:

- `c462b75395e079a1aca2a05a` — `ssh-access:kerberosticketcleanup`.
- `bbad5c6166456c8edcbaefd6` — `ssh-access:gssapicleanupcredentials`.
- `19dab249d75fc4989eb0155c` — `ssh-access:gssapistorecredentialsonrekey`.
- `9a64547fcefb3cbdbd52c4f3` — `ssh-access:exposeauthinfo`.
- `21f275a8d1b48381331c9b31` — `ssh-access:pidfile`.
- `acdf33b140bddd83baac8d1a` — `ssh-access:xauthlocation`.
- `17e46fc45310b9c16b42f4fa` — `ssh-access:sshdsessionpath`.
- `8ec96424e643f241a4f7de9b` — `ssh-access:sshdauthpath`.
- `837ebb63632431b7c3f91ae6` — `ssh-access:hostkey`.
- `8fe45bad30e49b61dfc9f9ca` — `ssh-access:hostkey`.

## A3-BARE-DIRS

Applied rows: 32. Sentences: Q2,Q3,U1,U2. Result: NONE / NA / FACT_UNKNOWN.

The actual listed members are only directory objects. Their ownership and names do not establish human-selected values, creator, same-package receipt or recorded construction source. Descendant contents are not silently added to a direct-member row.

Manual check: Checked all members of ten sampled arrays against the raw filesystem type d. The evidence establishes directories, but not the provenance or purpose needed to choose Q2, Q3, U1 or U2.

Ten manually checked rows:

- `124769f893ee21f77303b4c8` — `/etc/.java`.
- `0f67b7bae2a57cc2763a2fa2` — `/home`.
- `56e2e00352bb36231b2da3cd` — `/home/user/.config/xfce4`.
- `f0f627cc3b46b105b0b8df40` — `/home/user/.mozilla`.
- `993eeee5d668d53456ff626c` — `/home/user/.rustup/toolchains`.
- `c89bfd140525874cbc0324a5` — `/home/user/go/pkg`.
- `e49ce9aff8bf785dea731470` — `/root/.cache`.
- `70a8e6d79cabbeacbabea47c` — `/usr/lib/systemd`.
- `71d0194ea4194cf7d9b01977` — `/var/cache`.
- `ccbaeccf53ee2710e325cf92` — `/var/lib/flatpak/runtime`.

## A3-RUNTIME-DIRS

Applied rows: 12. Sentences: Q3,R2. Result: PROGRAM_RECORD / NO / DECIDED.

The reviewed direct members are transient directories created by identified running service managers. Q3 classifies their operational records; U3 speaks of a file, whereas these rows specifically enumerate directory objects. No executable or human-selected value is in the member array.

Manual check: Checked ten complete arrays and raw directory types for Netdata, container runtime, service credentials, propagation, per-user runtime and service-private temporary directories. This rule is limited to the actual directory objects.

Ten manually checked rows:

- `e53242b3cc2dd5fcf94d88a7` — `/opt/netdata/var/run`.
- `26c5fe90313f5bf3ea6859d3` — `/run/containers`.
- `0ee52b625691a0ca6eee4e12` — `/run/containers/storage`.
- `bb48fe46d346c4c264f69544` — `/run/credentials`.
- `e191ecb79f099f28214c9bb4` — `/run/crun`.
- `75072271e5ce774a1e4c074d` — `/run/systemd/propagate`.
- `2eb7344e200f359ad0143ac1` — `/run/user`.
- `aef603088133409bc780d22b` — `/run/user/0`.
- `3f7a15da0c1d5f890fa3d77e` — `/run/user/1000/dbus-1`.
- `8297b831c6bc820c295b314d` — `/var/tmp`.

## A3-STDLIB-CACHES

Applied rows: 32. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The reviewed outside-package Python standard-library stored groups are compiled __pycache__ copies of adjacent installed sources. The source/cache pairing, not the older inventory class label, establishes U2.

Manual check: Checked source and cache pairs in ten distinct modules: __phello__, collections, curses, ensurepip, importlib, pathlib, sqlite3, unittest, wsgiref and zoneinfo. Raw .cpython-313.pyc basenames match the adjacent .py sources; imported package subdirectories have the same pairing.

Ten manually checked rows:

- `lived-t913be4d2c3` — `/usr/lib/python3.13/__phello__`.
- `lived-ta4abd40fce` — `/usr/lib/python3.13/collections`.
- `lived-t020ed9822e` — `/usr/lib/python3.13/curses`.
- `lived-tfaa53a1101` — `/usr/lib/python3.13/ensurepip`.
- `lived-tc32257a21c` — `/usr/lib/python3.13/importlib`.
- `lived-t2c72d68466` — `/usr/lib/python3.13/pathlib`.
- `lived-t1897ca9a23` — `/usr/lib/python3.13/sqlite3`.
- `lived-t30677237b3` — `/usr/lib/python3.13/unittest`.
- `lived-t4a9f19aaf4` — `/usr/lib/python3.13/wsgiref`.
- `lived-tbe88daa394` — `/usr/lib/python3.13/zoneinfo`.

## Factual documentation

- [Installed Python package metadata](https://packaging.python.org/en/latest/specifications/recording-installed-packages/).
- [npm package.json](https://docs.npmjs.com/files/package.json/) and [npm scripts](https://docs.npmjs.com/using-npm/scripts.html/).
- [Unix groups](https://man7.org/linux/man-pages/man5/group.5.html).
- [Emacs package installation](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html).
- [Zsh source execution](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html).
- [Debian service helper state](https://manpages.debian.org/testing/init-system-helpers/deb-systemd-helper.1p.en.html).
- [MIME database generation](https://specifications.freedesktop.org/shared-mime-info/latest-single/).
- [Git initialization templates](https://git-scm.com/docs/git-init).
- [Python compilation](https://docs.python.org/3/library/py_compile.html).
- [OpenSSH options](https://man.openbsd.org/sshd_config).

Raw factual evidence is cited in individual rows; public documentation supplies the general file-format and mechanism semantics. Original appended rows and the correction overlay are retained for audit.
