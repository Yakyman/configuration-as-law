# Rules used in this run

26 scripted rules: D1 5, A1 8, A3R 13. The following sections contain each rule and ten manually inspected example IDs. Individual entries are separately justified in the table and source adjudication files.

# D1 classification rules

Five scripted rules are used; all other decisions are explicit row adjudications in (not published: trial helper scripts). The script appends only IDs not already present. The actual input contains 1840 rows. Inventory labels such as “outside packages” do not decide classification.

## Reading conventions

R6 controls: an unchanged object received inside a package is classified by Q1 before Q2, even when it contains executable code. Thus `INSTALLED` includes unchanged image-shipped executable files in this table: the requested output description's parenthetical “not itself executed code” cannot reverse PAGE's expressly required question order. Packages themselves are INSTALLED irrespective of their contents.

`YES` means a mandatory line of its own, not merely “belongs somewhere in the declaration.” Package installation reasons are missing from the permitted package listings; an independent package and an automatically obtained dependency differ under L1. This is factual uncertainty, not two incompatible textual rules, nor an audit of an absent existing declaration.

RUNTIME uses `NO` for the runtime object itself because R5 excludes it as a separate object; creator and creator's record are named in the reason. `COVERED` is reserved for L1–L3. Multiple concatenated PIDs in the raw process files prevent attaching a single program confidently to the first PID. Kernel/last-named-program candidates remain runtime objects, so this uncertainty does not change their own NO.

A directory listed as a member is classified as that stored directory; its contents are not silently substituted for it. Subgroups containing actual files have their own rows. There are no `:subtree` rows in this table. This matters for `/home`, `/var/lib`, and `timers.target.wants`: account values, daemon code, and activation links are not identical to their storage directory.

The clean-install premise is used positively alongside exact vendor/default paths or values. Arbitrary hypothetical tampering is not invented. User provisioning is visible in the added `user` account/group, supplementary membership, and `authorized_keys.d/ignition`; these are not treated as stock defaults.

## D1-PACKAGE — whole installed packages (1037 rows)

I1,I2,Q1,R1,L1: an installed RPM, dpkg, or Flatpak package is INSTALLED. The permitted raw files give identity/version/architecture or reference, but not root/dependency installation reason. Therefore record=NA, status=FACT_UNKNOWN: own line YES if independently selected; COVERED if obtained as a dependency of another recorded package. No claim is made that package names alone identify dependency status.

Ten manually inspected rows, including comparison of the full member string with the named raw package listing:

| ID | Check |
|---|---|
| fedora-f102747e5201750f7482940a | redhat-systemd-presets, version/architecture only |
| fedora-a72bbb3ac6e34b6db736c8d9 | cups-filesystem, installed RPM identity |
| fedora-386bda0b82486dad8fb56a3b | abattis-cantarell-fonts, no installation reason |
| fedora-8a2aa8cd8699fe1a6000221a | user-context noto Tamil font package, same missing reason |
| fedora-56947d87a17faf33ccc2b388 | noto emoji fonts; context label does not decide dependency |
| mint-1d2ad4a6b5f28aaa86d733fa | xed-dbg has dpkg installed `ii` status |
| tumbleweed-2b526c5fb8b26b3bc16614bc | phonon4qt5-lang, no install reason |
| tumbleweed-f930414351a4a1b2409054de | libksieve, package despite library name |
| tumbleweed-d8620423f05d02d99e676201 | Baloo translations, still a package |
| tumbleweed-6aa862424bccb9f5ca9b17cc | Flatpak GTK theme reference; dependency versus explicit install absent |

## D1-RUNTIME — objects existing only during operation (336 rows)

R5: process instances, sysfs driver associations, in-memory not-found unit records, generated/transient user units, `/run` objects, and the individually named private service temporary directories are RUNTIME/NO/DECIDED. Program ownership is stated; packaged creator programs are COVERED by their package or Flatcar image under Q1,L1. Rule does not classify persistent logs or arbitrary `/tmp` files by their name alone.

Technical facts were checked against [systemd file hierarchy](https://www.freedesktop.org/software/systemd/man/247/file-hierarchy.html), [systemctl unit states](https://github.com/systemd/systemd/blob/main/man/systemctl.xml), [Linux sysfs documentation](https://www.kernel.org/doc/Documentation/filesystems/sysfs.txt), and [systemd execution environment](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec). These establish volatile storage, absent unit files, kernel-backed links, and private service directory lifetimes, respectively.

Ten manually inspected rows:

| ID | Check |
|---|---|
| fedora-75876cae6b37d970268e6022 | PIDs 10 and 1008 concatenated before atd; runtime either way |
| flatcar-14525dd9e4b7bbef650b9011 | Many PIDs before journald, same invariant runtime decision |
| flatcar-f680f2ced5cbbbb98c0f7e6e | sysfs rtc_cmos driver link, not the stored driver binary |
| flatcar-b605afe2f102578e85a9a076 | sysfs virtio_net association |
| flatcar-f79b464b166dee8a6edf7235 | plymouth-quit-wait explicitly not-found/inactive |
| tumbleweed-70d71746ae30f45711522288 | user PipeWire session unit explicitly not-found |
| tumbleweed-106b78a49881386e5c2089f8 | Discover autostart unit explicitly generated |
| flatcar-27ab5a6b2bcd37afb4af1e52 | journal runtime sockets, sequence state, and streams |
| flatcar-bf1a27b86060d3ef4c7eb4fc | four udev links, all runtime associations |
| flatcar-db094f84370913cb34fb0235 | named polkit private temporary directory |

## D1-IMAGE — unchanged components received in the Flatcar image (368 rows)

I2,R6,Q1,R1,L1: unchanged image components are INSTALLED/COVERED/DECIDED. The rule's scope is exactly the stock boot files/directories, four stock shell templates, the enumerated default Flatcar groups, the 61 observed stock SSH daemon parameters, and `/etc` groups whose every listed member has a factory counterpart under `/usr/share/flatcar/etc`. The latter comparison checks type, mode, owner, group, and link target from the raw filesystem file. The implemented equality check covers all 184 members in 37 included groups; none differs. Content hashes are absent; matching factory metadata and the clean-install premise support these stock templates, not provisioned identity values. Groups with newly generated members are explicitly excluded and adjudicated separately. Code permissions and foreign boot targets do not defeat Q1.

The [Flatcar GRUB image-construction script](https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh) identifies the observed GRUB list/module/load files, BIOS images, Xen loader, configuration archive, and EFI loader paths as disk-image contents. The [configuration-update documentation](https://www.flatcar.org/docs/latest/updates-releases/releases/update-strategies/) explains the factory `/etc` overlay. [Flatcar's versioned default group file](https://raw.githubusercontent.com/flatcar/baselayout/509343f640e48feced4c861f14100c60457e55b9/share/baselayout/group) supplies group defaults; additional clean-image service groups are package defaults included at image build. [Flatcar's OpenSSH build configuration](https://raw.githubusercontent.com/flatcar/scripts/main/sdk_container/src/third_party/coreos-overlay/coreos/config/env/net-misc/openssh), together with [OpenSSH daemon parameter documentation](https://github.com/openssh/openssh-portable/blob/master/sshd_config.5), establishes the stock daemon values, including the Flatcar internal-sftp override and ssh-rsa compatibility addition. [Flatcar's audit packaging source](https://raw.githubusercontent.com/flatcar/scripts/main/sdk_container/src/third_party/coreos-overlay/coreos/config/env/sys-process/audit) identifies the three factory audit-rule files.

Ten manually inspected rows across the rule's domains:

| ID | Check |
|---|---|
| flatcar-e5869975107dd1606ec51809 | command.lst is an image-shipped lookup list, despite executable mode |
| flatcar-01863b09aee65b84699191fd | x86_64-xen adler32.mod is still received in image; Q1 precedes U1 |
| flatcar-b59146c6ef774b9d1e7896fc | grubx64.efi exact image-builder destination |
| flatcar-3415242185dd23520c96ddd0 | gawk.csh has matching factory template |
| flatcar-fc45dc0952375e7ffa324357 | all three EFI members shipped by image builder |
| flatcar-3e7acd7861265a9c89184e3b | root:x:0:root exactly matches stock group |
| flatcar-cf16ef23ac448b364d518f26 | core:x:500: exactly matches stock group |
| flatcar-f56e165ce3982c8e4e92a18f | PAMServiceName sshd matches OpenSSH default |
| flatcar-63f55f60c51fb4d3434fa466 | internal-sftp explicitly supplied by Flatcar build configuration |
| flatcar-3e3328fa5aa3c0625e5e872a | placeholder plus 00-clear,80-selinux,99-default all factory entries |

## D1-STATIC-GROUP — Mint base-passwd defaults (32 rows)

Q3a,R1,L2: fixed system-group values matching base-passwd's master are SETTING/COVERED/DECIDED. The script compares name, GID, and complete membership against the fetched public master in `d1-group-master.txt`; it separately requires the observed `x` and master `*` password placeholders. The clean-install premise and exact master values support default origin. A generated shadow placeholder is not assumed verbatim identical to a shipped entry; L2 covers the initialized default.

The [Debian base-passwd master](https://salsa.debian.org/debian/base-passwd/-/raw/master/group.master) supplies the exact fixed values; [grpconv's manual](https://manpages.debian.org/bookworm/passwd/grpconv.8.en.html) documents conversion of the group password field to `x`. The provisioned `users` membership is excluded and decided individually.

Ten manually inspected rows; all have an empty membership field, matching the master, and the documented shadow placeholder:

| ID | Check |
|---|---|
| mint-3136b62060275c8fadd91328 | root, GID 0 |
| mint-dc260ea0e8626ccdfac1c339 | daemon, GID 1 |
| mint-42152dfde33260586ffb999f | bin, GID 2 |
| mint-ec18df0499b4fa2f501d7452 | sys, GID 3 |
| mint-ccd8ea46f68c1e9c3085723d | tty, GID 5 |
| mint-f289dab6f9dec1d9e0cbd966 | disk, GID 6 |
| mint-038eeafccfe1ead5cb1ac351 | lp, GID 7 |
| mint-6b5b5602d47c692f7ea50898 | mail, GID 8 |
| mint-243b97c711d3fa7fdd3f0dc2 | news, GID 9 |
| mint-1f50123b990054509fcd5a24 | nogroup, GID 65534 |

## D1-GROUP-ORIGIN — Mint groups without established default origin (36 rows)

Q3a,R1,L2: these group values govern account access and are SETTING. Neither the raw group listing nor the fixed base-passwd master establishes their specific creation origin. Package installation defaults would be COVERED; locally chosen group values would require YES. The differing record outcomes require NA/FACT_UNKNOWN. A daemon-like name and clean installation alone do not establish the creating package or its exact default. No package maintainer scripts establishing these particular values were available in the cited evidence; generic documentation that packages can create groups is insufficient.

Ten manually inspected rows; each is absent from the fixed master and its inventory member gives only name, shadow placeholder, GID, and empty membership:

| ID | Check |
|---|---|
| mint-932933741fcf9c9df00e2e75 | systemd-journal, GID 999 |
| mint-d734a244186d872fca46df76 | systemd-network, GID 998 |
| mint-bd5e113be298c6fb730f7f4f | crontab, GID 997 |
| mint-0c7ab5288023382761510d68 | systemd-timesync, GID 996 |
| mint-fed793d380c59af7dbc9cfc8 | messagebus, GID 101 |
| mint-b1db9e8301d8a165189b163b | _ssh, GID 108 |
| mint-d5e64d111c4d4ce7c08f5f97 | lightdm, GID 117 |
| mint-23169a70e48971ae8b22d2d2 | nm-openvpn, GID 116 |
| mint-e4274ffd45ee975f2a648b53 | _flatpak, GID 115 |
| mint-424eaad680639755098a3b98 | gamemode, GID 987 |

## Individually decided rows (31 rows)

Three provisioned account/group rows are individually identified in the script (`flatcar-c23346b48a0e548523a60586`, `mint-e63044cd4464e2c0ce26546b`, `mint-9b54f9c71f99640a51d4e9dc`). Their actual values are not image defaults. The 27 remaining stored-directory cases are explicit dictionary entries; the single NetworkManager loopback row is an explicit ID decision, not a fallback rule.

For `/etc/audit`, [auditctl's own manual](https://github.com/linux-audit/audit-userspace/blob/master/docs/auditctl.8) says that -R executes commands from a file; [augenrules](https://github.com/linux-audit/audit-userspace/blob/master/docs/augenrules.8) combines factory inputs. Thus generated audit.rules is PROGRAM/COVERED under Q2,U4,L1, while factory inputs remain INSTALLED/COVERED under Q1. This is a mixed group with a common record value.

For `/etc/ssh`, [Flatcar's host-key generation script](https://raw.githubusercontent.com/flatcar/init/flatcar-master/scripts/sshd_keygen) creates host identity keys during startup. These authenticate the server; they do not grant a client entry. They are PROGRAM_RECORD/NO under Q4, unlike supplied defaults and the separately observed user's authorized_keys.

The loopback connection listing gives only name/UUID/type/device. It does not distinguish an in-memory generated connection from persistent locally chosen or installation-default configuration. That fact changes NO/YES/COVERED, so this is FACT_UNKNOWN. No absence of persistence is guessed from the name `lo`.

No D1 row was assigned NOT_DECIDED or TWO_WAYS. This is a classification result, not a claim about all possible objects or all other input sets.


---

# A1 classification rules

Script rule count: **8**.

The script is (not published: trial helper scripts). It appends missing IDs. Explicit `MANUAL` entries are row-by-row decisions selected after examining each row; the helper only serializes those decisions and shares wording for the same observed role. These explicit assignments are not pattern-based classification rules. Small groups have individually entered decisions, not invented ten-row samples.

Read scope: PAGE.md, this task folder, and evidence-named inventory files in the permitted A1 raw root. The raw-X1, raw-X2 and raw-E6 files named by later A1 rows were not found in the permitted raw roots; supplied evidence excerpts were used without looking in other project directories.

Directory decisions concern the directory object rather than every descendant. Runtime NO follows R5; containing-program record is stated in the reason. L1/L2 coverage means an eligible source/package line, not proof that an actual declaration already has it.

## A1-1. Packages in the CoreOS image

Sentences: I2,Q1,R1,L1. Each named installed RPM is part of the clean CoreOS operating-system image. Classify INSTALLED/COVERED by the image line. The ten checks cover metadata packages, coreutils data, dbus, EFI scaffolding, release identification, FUSE support, locales, kernel metapackage, libreport data, and Moby directory scaffolding.

Technical documentation: https://github.com/coreos/fedora-coreos-docs/blob/main/modules/ROOT/pages/storage.adoc

Ten manually inspected rows:
- `coreos-d49702b0f3` — containers-common-extra
- `coreos-3ed34b954a` — coreutils-common
- `coreos-5ddf73f1ac` — dbus
- `coreos-bc2b712980` — efi-filesystem
- `coreos-d9db8ebd61` — fedora-release-coreos
- `coreos-4c44b1402c` — fuse-common
- `coreos-80c805d99c` — glibc-minimal-langpack
- `coreos-326325fdeb` — kernel
- `coreos-bd48096336` — libreport-filesystem
- `coreos-cc816199e8` — moby-filesystem

## A1-2. Debian packages with unknown selection provenance

Sentences: Q1,R1,L1. The ii status establishes installation, but these records do not establish direct selection versus automatically installed dependency. Classify INSTALLED/NA/FACT_UNKNOWN. Each checked row has a package name/version and installed status, but no manual/automatic flag.

Ten manually inspected rows:
- `debian-e62af4f5a5` — cloud-utils
- `debian-95bb80c619` — init
- `debian-f1ae2388d8` — libmagic-mgc
- `debian-d805aa0253` — libpython3-stdlib:amd64
- `debian-44132e21a0` — libsemanage-common
- `debian-8e648115c5` — libtirpc-common
- `debian-ad283af0ea` — media-types
- `debian-9c32a751d6` — ncurses-base
- `debian-614d6e2913` — netbase
- `debian-9e34733f17` — python-apt-common

## A1-3. Package-owned directory objects

Sentences: Q1,R6,R1,L1. Intersect the named files.tsv entries with package-files.txt and require every selected member to have type d. Classify INSTALLED/COVERED. The object is the package-owned directory itself, not its recursive contents or a separate permission value. All ten checked entries exist, are package-owned directories, and have one listed member.

Ten manually inspected rows:
- `coreos-3cd182c07b` — /boot
- `coreos-827c5914e9` — /boot/efi
- `coreos-037231a728` — /etc
- `coreos-d3d071d2ba` — /etc/alternatives
- `coreos-c0faa16997` — /etc/binfmt.d
- `coreos-43399114f3` — /etc/credstore
- `coreos-edd98ae366` — /etc/credstore.encrypted
- `coreos-fc1b65b090` — /etc/depmod.d
- `coreos-31a0673933` — /etc/dnsmasq.d
- `coreos-1ae98d3e98` — /etc/dracut.conf.d

## A1-4. Nix store outputs with unknown covering source

Sentences: I1,I2,Q1,R1,L1. The exact store paths exist in packages.tsv, but that file inventories the whole store. Neither path existence nor immutability establishes current-system membership, dependency edges or a covering construction line. Classify INSTALLED/NA/FACT_UNKNOWN. Ten checks: nix.conf, dhcpcd.conf, hosts, gai.conf, mailcap, fuse.conf, nixos-init, restart-trigger data, hostname and tmpfiles.d. Their existence is established; source coverage is not.

Technical documentation: https://nix.dev/manual/nix/2.24/store/store-object

Ten manually inspected rows:
- `nixos-a332c16c0a` — /nix/store/00gmmr7b9slac4srbg4rqlwrw1k9rxnf-nix.conf
- `nixos-bd414d6b6a` — /nix/store/07n7039ak38i26hgf2s3501y9l5f6fs2-dhcpcd.conf
- `nixos-e78f81d36e` — /nix/store/0f5y6wcik5ldry8d1kl4a2f7hi5mq9pn-hosts
- `nixos-903eca0ec8` — /nix/store/0fhmy5gh22w9ysg62aj04bah31xyb0a5-etc-gai.conf
- `nixos-e3ea449be8` — /nix/store/0kk05fksy78xybp0jvvbnyiindqxz7ag-mailcap-2.1.54
- `nixos-70bca474fd` — /nix/store/0qqf2bnfp16a6y3448n7bz1rl9yyfvjq-etc-fuse.conf
- `nixos-90649e5e3f` — /nix/store/0xppmwrpx3d3wrvzq57kqkg9mlrim6r6-nixos-init-0.1.0
- `nixos-a738960c81` — /nix/store/15qy3pqkq3503xgypbmp3dbinngslxy6-X-Restart-Triggers-reload-systemd-vconsole-setup
- `nixos-d3ac6fc3e9` — /nix/store/1za4k4r5lkd3j0hnxhrazwwvyy9x61s6-etc-hostname
- `nixos-532c5e327b` — /nix/store/24ky217wazac3asqmzw1jy76nx7b368v-tmpfiles.d

## A1-8. Guix store output units

Sentences: I1,I2,Q1,R6,R1,L1. Guix installer-managed immutable output units include compiled/imported modules, generated system configuration, profile integration and received package data. These units are covered by their system construction line. Ten individually checked roles: module import, D-Bus configuration, icon package, desktop database, elogind configuration, another module import, groupmod wrapper, Guile launcher source, fonts directory and system test source.

Technical documentation: https://guix.gnu.org/manual/en/guix.pdf

Ten manually inspected rows:
- `guix-2a85615a21` — /gnu/store/0ibs0670s2b86pgrv53zph81h31ad1cx-module-import
- `guix-331ca6e362` — /gnu/store/0icq9vkz96352mgq8f31wm1d5rnxjy9w-dbus-configuration
- `guix-d8c1d6933d` — /gnu/store/18ngrsi4i7y2d05bz3xxpg1znqiq2bw1-hicolor-icon-theme-0.17
- `guix-f0f6c755c7` — /gnu/store/1mh7p4gzgndd576qlnc1p0ypjp2p965b-xdg-desktop-database
- `guix-ad573531ab` — /gnu/store/1rf9x4sy3mgjhvkppsj0mxbbrqmd2zcx-etc-elogind
- `guix-a1c1e67353` — /gnu/store/1vq19qhhqhx68lr3cp0a6kxpfrq7cd0q-module-import
- `guix-2838d57c33` — /gnu/store/207kx6f9a0j2nixr8225bka6147x4j4a-groupmod
- `guix-9e59c1810b` — /gnu/store/2dvxx7hdc8fsy4mfhddx16kyh4kf3cbm-guile-launcher.c
- `guix-987332f8d2` — /gnu/store/2ll8zirz0ih1yvzfzmpckhic7gbm160b-fonts-dir
- `guix-cf8bd029de` — /gnu/store/2mc7g2khyf8n49101f5nx6g8skx9lq7a-guix-system-tests-source

## A1-5. Owned content without unchangedness evidence

Sentences: Q1,Q2,Q3,Q4,L1,L2. The path inventory establishes ownership, but at least one member is content-bearing. No captured checksum/content comparison establishes that it remains as received. Unchanged content is Q1/COVERED; changed code or selected values can require an own line, and changed passive values can become optional. Classify NONE/NA/FACT_UNKNOWN. Each of the ten checks contains a non-directory member and lacks comparison evidence.

Ten manually inspected rows:
- `coreos-1d70ce548d` — /boot/grub2
- `coreos-cc15017ada` — /etc/GREP_COLORS
- `coreos-9945c88deb` — /etc/NetworkManager
- `coreos-0a38e83850` — /etc/X11
- `coreos-d20d960ea0` — /etc/adjtime
- `coreos-341d2df2d9` — /etc/aliases
- `coreos-a4c2c16ae9` — /etc/audit
- `coreos-e2885ad43a` — /etc/authselect
- `coreos-f536dafd04` — /etc/azure-ephemeral-disk-setup.conf
- `coreos-d68859230e` — /etc/bindresvport.blacklist

## A1-6. Runtime representations

Sentences: R5,Q1,Q3a,L1,L2. Classify live device, mount, scope, slice, unresolved manager reference, swap and process representations RUNTIME/NO/DECIDED. Name their creating program or setting and its record separately. Creator coverage uncertainty cannot change the runtime object's own NO. The ten checks identify devices twice, two /run-generated service representations, further devices, mounts, init/session scopes, slices, user devices and user mounts. Stored files are not included merely because their paths contain run.

Technical documentation: https://www.freedesktop.org/software/systemd/man/254/systemd.device.html

Ten manually inspected rows:
- `coreos-a3f2270221` — unpackaged *.device
- `coreos-88335c6c87` — unpackaged *.device
- `debian-96787848d5` — netplan-ovs-cleanup.service
- `debian-0758efc3b0` — systemd-growfs@-.service
- `debian-a3f2270221` — unpackaged *.device
- `debian-18fb2985ed` — unpackaged *.mount
- `debian-0ff15b2741` — unpackaged *.scope
- `debian-253d752b01` — unpackaged *.slice
- `debian-88335c6c87` — unpackaged *.device
- `debian-565df89b5f` — unpackaged *.mount

## A1-7. Installation-provided service defaults

Sentences: Q3a,R1,L2. The row denotes a service/target, not its on-disk fragment file. A standard systemd fragment under /lib/systemd/system with no drop-ins supplies the installation default: SETTING/COVERED. The ten manually checked initrd service/target entries each name their fragment and an empty drop-in list.

Ten manually inspected rows:
- `debian-6b5b5b2232` — initrd-cleanup.service
- `debian-8786c9eece` — initrd-fs.target
- `debian-646aa477ec` — initrd-parse-etc.service
- `debian-00a56889bd` — initrd-root-device.target
- `debian-6e3a25797c` — initrd-root-fs.target
- `debian-c1428e493e` — initrd-switch-root.service
- `debian-bc71f8a67c` — initrd-switch-root.target
- `debian-cc14a4c724` — initrd-udevadm-cleanup-db.service
- `debian-59f9abe755` — initrd-usr-fs.target
- `debian-101133305f` — initrd.target

## Additional documentation for individual decisions

- Guile compiled Scheme cache: https://www.gnu.org/software/guile/manual/guile.pdf
- APK supplied configuration copies: https://docs.alpinelinux.org/user-handbook/0.1a/Working/apk.html
- Ghostscript PostScript files: https://ghostscript.readthedocs.io/en/latest/Develop.html
- Kyua Lua configuration: https://man.freebsd.org/cgi/man.cgi?manpath=FreeBSD+14.3-RELEASE&query=kyua.conf&sektion=5
- Guix store and system construction: https://guix.gnu.org/manual/en/guix.pdf

## Independent-review points

- Independent review changed all 122 individual Nix store-output rows to FACT_UNKNOWN because the evidence establishes existence but not a covering dependency or construction source. No unreferenced closure file was used.
- Mutable package-owned paths have only type/path/size evidence, so their unchangedness is left factual rather than presumed from ownership.
- Explicit service rows describe service defaults; package-owned fragment-file rows describe stored objects. These are different objects under Q1/Q3a.

## Individually reviewed link and state exceptions

The following are explicit row-by-row corrections, not an additional script rule:
- Channel/profile selectors: nixos-3e7f003ce6, nixos-a5c695f848, nixos-63d8a049ea, guix-76e4372b50 — SETTING; default-versus-choice provenance unknown.
- CoreOS boot scaffolding: coreos-3620611c7e — INSTALLED/COVERED by its image.
- Vendor/palette selectors: ubuntu-7740cdd4af, ubuntu-de7f67781f — SETTING; default-versus-choice provenance unknown.
- Persistent mtab symlinks: debian-6b4026dd02, nixos-6b4026dd02, guix-6b4026dd02 — package receipt versus separately generated provenance unknown; runtime-target status does not classify the persistent link.
- Release-identification link: arch-6a38277ef0 — package receipt versus separate generation unknown.
- Mail-alias selector: freebsd-0b0c34385f — SETTING; default-versus-choice provenance unknown.
- NixOS marker: nixos-c093c82f20 — package receipt versus separate generation unknown.
- Account reconciliation state: nixos-ec96d00e30 — active account-control values versus passive history unknown.

## Final independent-review corrections

(not published: trial helper scripts) revises twenty explicit individual rows after reviewing their actual evidence. `coreos-2d7adb8ef6`, `nixos-bfd49e603a`, `guix-da5f01a3ef`, and `freebsd-c2cf70a5ff` become FACT_UNKNOWN because the alleged mixed member decisions were not established. `guix-a2b4d23600` and `guix-d084f3423e` are RUNTIME/NO; their PID files are not independently persistent settings. `guix-c2cf70a5ff` is NONE/NO/DECIDED: runtime and directory-container alternatives all need no own line. These are individual corrections, not an additional scripted classification rule.

Further individual corrections distinguish actual per-machine GRUB evidence, correct GTK accelerator-map data under U4, separate received dpkg control metadata from generated status/lists, and leave Guix checkout code coverage conditional. These corrections are recorded explicitly in (not published: trial helper scripts), not inferred from a new pathname rule. Technical references: https://www.gnu.org/software/grub/manual/grub/html_node/Environment-block.html ; https://docs.gtk.org/gtk3/class.AccelMap.html .


---

# A3R scripted classification rules

Script rule count: **13**. Individual adjudications: **300**.

Classification code: (not published: trial helper scripts); explicit individual decisions: (not published: trial helper scripts); review corrections to already appended rows: (not published: trial helper scripts). `a3r-assignments.jsonl` maps each output ID to its rule or individual decision. Revisions concern this run only.

A group listing directory objects is not automatically a recursive group; `:subtree` groups are recursive but their selected membership is not recoverable merely by enumerating every raw path under the prefix. Older inventory class labels do not establish PAGE classifications. The unreferenced part-1.tsv mentioned by some evidence is outside the permitted raw roots and was not read.

Q1 has priority over Q2 even for executable received package parts. NONE/NO/DECIDED is used when material-versus-record creator uncertainty cannot change record=NO, as the task explicitly requires. MIXED is retained only when differing member decisions are established.

## A3-01. Effective group and SSH access values
Rows: 124. Sentences: R6,Q1,Q3,Q3a,R1,L2.

Effective values do not establish installation-default versus independent-choice origin. These alternatives yield COVERED versus YES, hence FACT_UNKNOWN. Group entities are SETTING; SSH effective values retain NONE where received/default and locally selected objects can differ under Q1/Q3a. The group entries give name/GID/membership; SSH entries give effective parameters without per-value origin.

Ten manually inspected rows:

- `424cb5f40e407805606b43e3` — `root`
- `c9026e221a81a2c85175525f` — `uucp`
- `9a8089d2eeea3b59a0b02b99` — `www-data`
- `2e62e78d8fca69e2a348f1e5` — `nogroup`
- `7b30d550f377d95effa87f34` — `user`
- `5f8fcf77e7c5041de9f3e517` — `ssh-access:usepam`
- `d858b7eb5b5db644a78163d0` — `ssh-access:pubkeyauthentication`
- `acdf33b140bddd83baac8d1a` — `ssh-access:xauthlocation`
- `60d688cfe3148facddc7533d` — `ssh-access:subsystem`
- `b3bc32c5ee21a357406dd84d` — `ssh-access:persourcepenalties`

## A3-02. Live process representations
Rows: 22. Sentences: R5,Q2,L1.

Each process instance is RUNTIME/NO. Its executable is named and creator record=NA when package provenance is absent. Concatenated PID evidence can obscure the exact executable association but every candidate remains a process with NO for its own line.

Ten manually inspected rows:

- `1c460643fdd8cfbbd196d5c8` — `10`
- `8b1dbd0e6a04dda53f042fdf` — `11`
- `42c8a140e560dc29380e1d8c` — `12`
- `7f68c5deb8bee8904640065d` — `17`
- `f33262b97d15e4256f2f249d` — `207`
- `0182a17a4f357d35fb9e7954` — `33`
- `2130dee9e966a8190632a24f` — `395`
- `5bf49f96a1afbe0b43e14736` — `78`
- `47c30908758abecdcb2d11b7` — `87`
- `e117d280137522e247ca6e90` — `9`

## A3-03. Metadata files without established receipt or unchangedness
Rows: 901. Sentences: R6,Q1,Q3b,Q4,U4,L1,R2.

The filesystem metadata proves paths and types, not unchanged installer receipt or original source provenance. Original package metadata can be COVERED; independently generated descriptive records can be NO; launch-controlling values can require YES. Therefore FACT_UNKNOWN. The ten checks include Python METADATA, VS Code package.json, packages.config and nested npm package.json. The referenced npm JSON archive provides contents for npm cases but no integrity/provenance comparison.

Ten manually inspected rows:

- `3ce5b4911a70e4f372f050fc` — `/home/user/.vscode/extensions/ms-vscode.cpptools-1.35.6-linux-x64/package.json`
- `440bccd20764e280ea521c1a` — `/home/user/.vscode/extensions/ms-python.debugpy-2026.6.0-linux-x64/packages.config`
- `4845c523758595ad09dc608b` — `/home/user/.vscode/extensions/ms-python.python-2026.10.0-linux-x64/python_files/lib/python/microvenv-2025.0.dist-info/METADATA`
- `0ef0bcc49c7c28c1c746129b` — `/home/user/.local/share/pipx/venvs/pre-commit/lib/python3.13/site-packages/packaging-26.3.dist-info/METADATA`
- `ab8e0d6b13c2e3ff0e856223` — `/home/user/Projects/express/node_modules/@nodelib/fs.scandir/package.json`
- `01b39a7e7ca4afbd186ad23b` — `/home/user/Projects/express/node_modules/@isaacs/cliui/node_modules/ansi-regex/package.json`
- `225a3cf1cab7ef096e921b39` — `/home/user/Projects/express/node_modules/cliui/node_modules/wrap-ansi/package.json`
- `d398a97eca3186fa2ad9a5d4` — `/home/user/Projects/express/node_modules/body-parser/package.json`
- `449f54455c7cdc741fe0faf1` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/http-proxy-agent/package.json`
- `dc127f353179f767622f14f2` — `/usr/lib/python3/dist-packages/python_debian-1.0.1.dist-info/METADATA`

## A3-04. Immediate shell and Emacs extension file groups
Rows: 401. Sentences: R6,Q1,Q2,Q4,L1.

Immediate named plugin groups have source/compiled-file names and support data, without actual current code contents, unchanged-package provenance or a generating declaration source. Thus FACT_UNKNOWN rather than inferring blanket package coverage or a certain mixed result from suffixes. Each sample was checked against its member list; numeric collapsed subtrees are excluded.

Ten manually inspected rows:

- `ab4e48545791db0d53dc71b0` — `/home/user/.oh-my-zsh/plugins/1password`
- `92da532490c5e0e8cdfd4554` — `/home/user/.oh-my-zsh/plugins/argocd`
- `4291b3badbd506a67c858704` — `/home/user/.oh-my-zsh/plugins/bedtools`
- `5bd34cd01937767ea4867a5e` — `/home/user/.oh-my-zsh/plugins/cake`
- `e98614533c5d71a7094f16a2` — `/home/user/.oh-my-zsh/plugins/compleat`
- `aad804a919899545a7be1f36` — `/home/user/.oh-my-zsh/plugins/git-escape-magic`
- `064a9ca3d9ec62f471f8d61f` — `/home/user/.oh-my-zsh/plugins/nats`
- `147187a5315d2a32f8444caf` — `/home/user/.oh-my-zsh/plugins/symfony`
- `93a93428a9d00a2b2aac9e6f` — `/home/user/.emacs.d/elpa/ace-window-20220911.358`
- `38cc2f41f8f8aac99bb9fbcd` — `/home/user/.emacs.d/elpa/consult-20261004.957`

## A3-05. Volatile /run objects
Rows: 42. Sentences: R5,Q2,L1.

Every selected object is in volatile /run storage: sockets, synchronization state, manager records or runtime-generated objects. RUNTIME/NO, naming the creating daemon and creator record=NA when provenance is absent. Creator provenance cannot change the absence of an own runtime line.

Ten manually inspected rows:

- `3c4a5ca44a8a5ebbd1c4566e` — `/run`
- `1e2ffbcef22fc31ed10f5e2a` — `/run/NetworkManager/devices`
- `02ccedeb2249f1994496d9d4` — `/run/cloud-init`
- `0a33a6bb86c050fb7cd4a6d8` — `/run/containers/networks`
- `073776a01f9ed67f0b1842b3` — `/run/crun/bfd24acb04736a47cf127d1325687a516315ccbe1fa0e1ec6cb4e839e9ebcc13`
- `fa10de89915f71337d422abb` — `/run/cups`
- `96faee23cfad80f11c62c89d` — `/run/netdata`
- `939e3d48274711135dfc0610` — `/run/systemd`
- `2ffe13225126b0eafd7bc1cf` — `/run/systemd/netif`
- `lived-t912dff2b99` — `/run/user/1000/systemd`

## A3-06. Man-db cache groups
Rows: 26. Sentences: R6,Q4,R2.

Observed cache directories and index.db files are generated search/formatting records, not manual package payloads or executable code: PROGRAM_RECORD/NO. Ten language-specific groups were checked for their index and directory members.

Ten manually inspected rows:

- `4510afc64020ce965c69c93a` — `/var/cache/man`
- `8d3198283b0bc001a8363861` — `/var/cache/man/cs`
- `d5d756c7be695e8e3c3240e3` — `/var/cache/man/da`
- `775c7e0626a8d2764f6561aa` — `/var/cache/man/de`
- `0c14914a1646a594dd64c510` — `/var/cache/man/es`
- `359b5c84d186097c4737d4f3` — `/var/cache/man/fi`
- `d93b8cfda4b3fa40f11328c7` — `/var/cache/man/fr`
- `ecaea5af3e3b04c0aadb97f4` — `/var/cache/man/hr`
- `67cab6a3b21ee18171e913bf` — `/var/cache/man/hu`
- `cfbbb1277d81eda3111f05d7` — `/var/cache/man/id`

## A3-07. Package service-enablement history
Rows: 25. Sentences: R6,Q4,R2.

These deb-systemd-helper and deb-systemd-user-helper markers remember installation operations. They are distinct from actual service activation links: PROGRAM_RECORD/NO. The ten checks include system and user helper directories and individual dsh-also/target history markers.

Ten manually inspected rows:

- `4e072a15763b4a1a1133071b` — `/var/lib/systemd/deb-systemd-helper-enabled`
- `9140d0e0763d33c3a86e94f5` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-config.target.wants`
- `b76a79bba43e1c1f9abcbaf0` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-init.target.wants`
- `13177aa156a7ffca6aadb143` — `/var/lib/systemd/deb-systemd-helper-enabled/default.target.wants`
- `067ca62be79e9cfb037e1fb2` — `/var/lib/systemd/deb-systemd-helper-enabled/firewalld.service.wants`
- `038156e92c4b157696ea5476` — `/var/lib/systemd/deb-systemd-helper-enabled/graphical.target.wants`
- `f0a9fc130f6243697682fcca` — `/var/lib/systemd/deb-systemd-helper-enabled/hibernate.target.wants`
- `e6c7b500df6175d8c883f1e4` — `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`
- `60af4555f895a621f8fdd8b5` — `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants`
- `3dbad18363c3236ada19e5bb` — `/var/lib/systemd/deb-systemd-user-helper-enabled/sockets.target.wants`

## A3-08. Exact installed Flatpak runtime components
Rows: 42. Sentences: I1,I2,R6,Q1,R1,L1.

The paths identify the exact org.gnome.Platform installed checkout by commit and files/ subtree. These received metadata components are INSTALLED/COVERED by that runtime package. The ten checks verify distinct dist-info metadata entries within the same deployed commit, including vendored setuptools dependencies.

Ten manually inspected rows:

- `51cba7cfc1bf2684737e1902` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools-80.10.2.dist-info/METADATA`
- `35b08e5e2c7d0df863990fcb` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/jinja2-3.1.6.dist-info/METADATA`
- `55f8a1b78a6e7fe96e1c0645` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/attrs-26.1.0.dist-info/METADATA`
- `b5a812108fee30bde128868b` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/packaging-26.3.dist-info/METADATA`
- `6971545a28a58d7a6172ec28` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/mako-1.4.1.dev0.dist-info/METADATA`
- `608b6340b64cfca363330534` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/markdown-3.10.3.dist-info/METADATA`
- `5e4917158f087301a8fc8b13` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/tomli-2.4.0.dist-info/METADATA`
- `e78e15d8f9683164d61faf24` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/more_itertools-10.8.0.dist-info/METADATA`
- `e85b221073f95ef465518069` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/jaraco_context-6.1.0.dist-info/METADATA`
- `7356c19233248767ccd1f7a1` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/jaraco_functools-4.4.0.dist-info/METADATA`

## A3-09. Git sample-hook groups
Rows: 11. Sentences: Q1,Q2,U1,L1.

The names match Git template sample hooks, but current contents and unchanged-template/source relation are absent. Generated original copies may be COVERED, independently changed executable files YES, or nonexecutable fixtures NO: FACT_UNKNOWN. Ten lists were checked for sample hook names and the absence of content/provenance evidence.

Ten manually inspected rows:

- `lived-t98b49255b3` — `/home/user/.config/nvim/.git`
- `lived-tf3cef8f65e` — `/home/user/Projects/zlib/.git`
- `lived-teaff14fb6e` — `/home/user/Projects/express/.git`
- `lived-t5524f36a07` — `/home/user/Projects/dotfiles/.git`
- `lived-t377338389c` — `/home/user/Projects/awesome-compose/.git`
- `lived-tb8a7a2c063` — `/home/user/.emacs.d/.git/hooks`
- `lived-ta4806d9131` — `/home/user/.oh-my-zsh/.git/hooks`
- `lived-tc5d3d1ad66` — `/home/user/.nvm/.git/hooks`
- `62c9ae1c4efb4911e0b9bb51` — `/home/user/.emacs.d/.git/hooks`
- `e8b46637cbde5543ea5779f8` — `/home/user/.nvm/.git/hooks`

## A3-10. Collapsed Python library/cache subgroups
Rows: 35. Sentences: Q1,Q2,Q4,U4,L1.

The raw filesystem prefix contains more objects than the collapsed selected-member count. The allowed evidence does not recover which members are selected, or their source integrity. Received files, compiled copies and independent additions have different kinds/coverage: FACT_UNKNOWN. Ten raw prefixes were checked and compared with selected counts; no whole-prefix membership was silently substituted.

Ten manually inspected rows:

- `lived-t913be4d2c3` — `/usr/lib/python3.13/__phello__`
- `lived-tc5242e687e` — `/usr/lib/python3.13/_pyrepl`
- `lived-td2cb3c5e97` — `/usr/lib/python3.13/asyncio`
- `lived-ta4abd40fce` — `/usr/lib/python3.13/collections`
- `lived-ta2011e6fc2` — `/usr/lib/python3.13/concurrent`
- `lived-t4ca37c4992` — `/usr/lib/python3.13/ctypes`
- `lived-t020ed9822e` — `/usr/lib/python3.13/curses`
- `lived-td982437c2e` — `/usr/lib/python3.13/dbm`
- `lived-t3ded61c21e` — `/usr/lib/python3.13/email`
- `lived-td75eac9783` — `/usr/lib/python3.13/encodings`

## A3-11. Generated MIME database groups
Rows: 14. Sentences: R6,Q4,R2.

The observed type-description outputs and lookup indexes are generated by update-mime-database, outside its source packages/ directory: PROGRAM_RECORD/NO. L1 is a coverage rule for already-classified installed objects; its generated-list example does not turn all generated descriptive data into installed objects. Ten MIME-type/index groups were checked.

Ten manually inspected rows:

- `a4de6292d1e78167decc7081` — `/usr/share/mime`
- `4aba607ff59c3ee376310758` — `/usr/share/mime/application`
- `4ff815d792c6f07c0e70cdd2` — `/usr/share/mime/audio`
- `a1bc9af2c8b24e04764d16e0` — `/usr/share/mime/chemical`
- `2c84f6f7d6b126564d10c278` — `/usr/share/mime/font`
- `946c59a84dd618138088be86` — `/usr/share/mime/image`
- `a3a29542d4b538e850acb99b` — `/usr/share/mime/inode`
- `7d4c3c7f666b1008ee71489d` — `/usr/share/mime/message`
- `a57811114eec1362d29f52a8` — `/usr/share/mime/model`
- `f4785d34ecdd63e5d9727007` — `/usr/share/mime/multipart`

## A3-12. Collapsed extension groups
Rows: 28. Sentences: I1,I2,Q1,Q2,Q4,L1.

Collapsed Emacs, shell and VS Code extension groups do not expose the selected member list or current content/receipt integrity. The raw full-prefix count differs from the selected count. Received assets, executable additions and inert records can differ, so FACT_UNKNOWN. Ten full raw prefixes were inspected for these limits without treating them as exact group membership.

Ten manually inspected rows:

- `lived-t0981664644` — `/home/user/.emacs.d/elpa/company-20261120.417`
- `lived-tc9fb19d567` — `/home/user/.emacs.d/elpa/magit-20261117.1103`
- `lived-t9b2b9a2814` — `/home/user/.oh-my-zsh/plugins/alias-finder`
- `lived-t515b2ce401` — `/home/user/.oh-my-zsh/plugins/chucknorris`
- `lived-tfa879dd69f` — `/home/user/.oh-my-zsh/plugins/copyfile`
- `lived-t7404fddb53` — `/home/user/.oh-my-zsh/plugins/docker`
- `lived-tc7dcfd5d34` — `/home/user/.oh-my-zsh/plugins/dotenv`
- `lived-t52437ba96a` — `/home/user/.oh-my-zsh/plugins/extract`
- `lived-t44ea0088c1` — `/home/user/.vscode/extensions/dbaeumer.vscode-eslint-3.0.34`
- `lived-t4af9917634` — `/home/user/.vscode/extensions/esbenp.prettier-vscode-12.4.0`

## A3-13. Container project examples with unobserved content/use
Rows: 39. Sentences: Q2,Q3a,Q3b,Q4,U1,U4,L1,L2.

Every group is a container example containing a Compose description, sometimes sources/build files, and supporting project material. Contents and actual local launch/access use are unavailable; executable code, active launch settings and unused project material differ. FACT_UNKNOWN. Ten cases were checked across simple YAML/document groups and Python, Go, Rust, TypeScript and monitoring subtrees.

Ten manually inspected rows:

- `lived-t1f59d917a6` — `/home/user/Projects/awesome-compose/angular`
- `lived-t29bfb9ffd0` — `/home/user/Projects/awesome-compose/django`
- `lived-t6ac1b2aa39` — `/home/user/Projects/awesome-compose/elasticsearch-logstash-kibana`
- `628f01597373050cc3080375` — `/home/user/Projects/awesome-compose/flask-redis`
- `cae287e95aa05bd036f2cc17` — `/home/user/Projects/awesome-compose/gitea-postgres`
- `lived-t7dfefe9c09` — `/home/user/Projects/awesome-compose/nginx-golang`
- `38b5dec25d1535b3b1972c0a` — `/home/user/Projects/awesome-compose/pihole-cloudflared-DoH`
- `lived-td7912413ab` — `/home/user/Projects/awesome-compose/prometheus-grafana`
- `lived-t70c3c558e1` — `/home/user/Projects/awesome-compose/react-rust-postgres`
- `98d6d2b79e68b842de14fde3` — `/home/user/Projects/awesome-compose/wordpress-mysql`

## Technical documentation

- Volatile storage: https://uapi-group.org/specifications/specs/linux_file_system_hierarchy/
- Man-db cache generation: https://manpages.debian.org/trixie/man-db/mandb.8.en.html
- Service-helper history: https://manpages.debian.org/testing/init-system-helpers/deb-systemd-helper.1p.en.html
- Flatpak deployment paths: https://docs.flatpak.org/en/latest/flatpak-command-reference.html
- Git templates: https://git-scm.com/docs/git-init
- MIME generation: https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html
- Python bytecode copies: https://docs.python.org/3/tutorial/modules.html#compiled-python-files
- Neovim Lua cache: https://neovim.io/doc/user/lua#vim.loader
- Other individual rows cite their documentation in basis; raw facts use the evidence-referenced files only.
