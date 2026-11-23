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
