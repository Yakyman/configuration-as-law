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
