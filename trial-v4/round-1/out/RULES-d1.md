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
