# c2, part void of D1b: notes

Written 2026-11-23 (UTC). Input: `D1b/in/part-void.tsv` (1,143 rows). Facts: handoff copy `D1b/handoff/void/`.
Output: `part-void.tsv`; script (not published: orchestration or scratch); per-row rule evidence `rule-check.tsv`; check (not published: orchestration or scratch).

## Facts established and their sources

- XBPS file manifests were read for every installed package except six with no files (`base-system`, `docker`,
  `linux`, `removed-packages`, `void-docs-browse`, `wifi-firmware`: "no such file or directory" in
  raw/0012, 0015, 0016, 0017). So "ownership unresolved" means that no installed package's manifest lists the path.
- Kernel 6.12.11_1: no manifest or archive of that package version is on the machine. Every member path of the
  old-kernel groups, and `/boot/config-6.12.11_1` and `/boot/vmlinuz-6.12.11_1`, have status `no-reference-found` in
  `old-package-member-integrity.tsv`, checked for every row by (not published: orchestration or scratch) (column `old_statuses` of
  `rule-check.tsv`). No public archive of old Void package versions was found. Void documentation: "When updating
  the kernel, old versions are left behind in case it is necessary to roll back to an older version"
  (https://docs.voidlinux.org/config/kernel.html). The template has `preserve=yes`
  (https://github.com/void-linux/void-packages/blob/master/srcpkgs/linux6.12/template); Manual.md: "`preserve` If set,
  files owned by the package in the system are not removed when the package is updated, reinstalled or removed"
  (https://github.com/void-linux/void-packages/blob/master/Manual.md).
- Initramfs: "The `{pre,post}-install` hooks are executed by xbps-reconfigure when configuring a Linux kernel, such
  as building its initramfs. This happens when a kernel series is installed for the first time or updated"
  (kernel.html). The files for 6.12.118_1 and 6.18.64_1 have mtimes inside the update window (16:17:54, 16:18:01).
  For `initramfs-6.12.11_1.img` (05:52:27) two documented producers exist (the installer's
  `dracut --no-hostonly` call, https://github.com/void-linux/void-mklive/blob/master/installer.sh, and the kernel
  hook); the creator is not recorded, so that member is UNKNOWN.
- `/etc/default/libc-locales.new-2.41_1`: full SHA256 `d05a0727…d275` (full-digests.tsv) equals the
  `glibc-locales-2.41_1` manifest entry for `/etc/default/libc-locales` (raw/0013). XBPS extracts a conf file whose
  installed copy was modified to `<file>.new-<version>` (`archive_entry_copy_pathname`,
  https://github.com/void-linux/xbps/blob/master/lib/package_config_files.c).
- `/etc/default/live.conf` (`USERNAME=anon`): written by the live image's boot hook
  (https://github.com/void-linux/void-mklive/blob/master/dracut/vmklive/adduser.sh: default `USERNAME=anon`,
  `echo "USERNAME=$USERNAME" >> ${NEWROOT}/etc/default/live.conf`). Its only reader, the installer, is not on the
  machine (raw/0004 lists no `void-installer` and no `vmklive` module).
- `/etc/modules-load.d/dm-raid.conf`: mklive writes exactly `dm-raid` there (mklive.sh, post_install_packages).
- `/var/db/xbps/keys/3d:b9:…plist`: git blob of the current bytes `41bc2cb7…` equals
  https://github.com/void-linux/void-mklive/tree/master/keys ; mklive copies keys into the image (copy_void_keys).
  The `xbps` package ships only the 60:ae key (github.com/void-linux/xbps, data/).
- `/etc/sudoers.d/wheel` content equals the installer line `echo "%wheel ALL=(ALL:ALL) ALL"` (installer.sh), written
  when the person's group choice includes wheel. Groups: base-files ships `wheel:x:4:` etc. without members
  (srcpkgs/base-files/files/group); the installer's default membership list is exactly the nine groups found.
- Root: base-files up to 0.145 shipped `root:x:0:0:root:/root:/bin/sh`; 0.146 (commit 1183ba14, 2025-12-22) ships
  `/bin/bash`; installed is 0.146_1 and `/etc/passwd.new-0.146_1` exists.
- `/var/lib/containerd`: containerd 2.3.2_2 template has `make_dirs="/var/lib/containerd 0755 root root"`; Manual.md:
  "`make_dirs` A list of entries defining directories and permissions to be created at install time". The store
  holds only its root (store-coverage.tsv).
- npm: every file member has status `equal` against a cryptographically verified archive, every directory member
  status `directory` (npm-member-integrity.tsv). npm docs: "any of foo's dependencies are similarly unpacked into
  ./node_modules/foo/node_modules/..." (https://docs.npmjs.com/cli/v11/configuring-npm/folders); `node_modules` is
  always ignored and "cannot be included" in a package (…/package-json, "files"); a package is "A folder containing a
  program described by a package.json file" (https://docs.npmjs.com/about-packages-and-modules). Package reasons:
  cowsay explicit, all others dependency (objects.tsv).
- Docker: "Docker is an open platform for developing, shipping, and running applications"
  (https://docs.docker.com/get-started/docker-overview/): its documented purpose does not include installing and
  removing programs (S8.1-4), so its image is not a package (S8.1-6).
- Flatpak: "the per-user data is in $HOME/.local/share/flatpak/ … a local repository in the repo/ subdirectory …
  installed runtimes and applications are in the corresponding runtime/ and app/ subdirectories"
  (https://docs.flatpak.org/en/latest/flatpak-command-reference.html). Deployment integrity was not collected
  (metadata.json gaps).

## Store rows

The three `L2:image-container-store` rows have no member count in `members`, but the extended collector traversed
them completely (store-coverage.tsv: 71,630, 1 and 531 members). The flatpak and docker stores hold objects of
different kinds and are given MIXED; the containerd store holds only its own empty root and is decided as one object.

## Rule A (script): kernel 6.12.11_1 leftovers — 1,068 group rows

Rule: a stored group whose name is `/usr/lib/modules` or lies at or under `/usr/lib/modules/6.12.11_1`, all of whose
members have no reference (`no-reference-found`), is UNKNOWN. Derivation: S8.2-7 asks whether the object was obtained
as part of an installed package and remains as received. Whether these members remain as received cannot be
established (no manifest; none public). If they were changed, question 1 is no, and modules are programs (S8.2-9,
S8.2-10) not built by the system from a line (S8.2-16: PROGRAM-OWN), lookup tables and directories program records
(S8.2-15). If unchanged, the decision also depends on whether `linux6.12` at 6.12.118_1 is still "such a package" for
objects of 6.12.11_1 (S8.1-6 does not say), giving INSTALLED-PACKAGE or PROGRAM-OWN. The values of the missing fact
give different decisions, so the row is UNKNOWN. Check by hand (members and statuses read one by one):
d1b-void-1b50d3fa9bca32ff4efd7fbf, d1b-void-7c768bff6f267ee883027ee1, d1b-void-3e59a1133b67b50bdb986e49,
d1b-void-d9f6a8b94a426b0f53327556, d1b-void-aa3e463fa8e059fdb882c5e3, d1b-void-3f07d6efb40d39c7ab30928d,
d1b-void-70fa7f21f6bab76b669e8d0b, d1b-void-590ea919d2bc24a14421c208, d1b-void-8b93f57f0ebc28f112cbe57b,
d1b-void-64b4a13ff51ad3d23bc6be30 — all fit.

## Rule B (script): npm groups under the home directory — 53 group rows

Rule, per member: a file whose status is `equal` → INSTALLED-PACKAGE (S8.2-7, S8.2-8, S8.2-16; npm is an installer,
S8.1-4); a directory named `node_modules` → RECORD (npm created it while placing dependencies and never packs it:
not part of a package, not code, not a value; S8.2-15); a directory whose parent is `node_modules` → INSTALLED-DERIVED
(an npm package folder installed as a dependency, S8.2-7, S8.2-16); any other directory inside a package folder →
INSTALLED-PACKAGE (part of the package folder). A row whose members all get one decision gets it; otherwise MIXED.
Any member outside these cases would have stopped the script (none did). Check by hand:
d1b-void-1ba9285006328ef21a46ac12, d1b-void-7bc8b3ab15f09eb51540dc7a, d1b-void-2671e0c8194a80cfbd661158,
d1b-void-f87e0a7d80b2ec524d9a3988, d1b-void-e3d7e7593a77dd0242dde8df, d1b-void-fe00841dd65a674ad24d1986,
d1b-void-060a42ae4f6373f859fcdd9b, d1b-void-e5906cf200ec45cbcbd81325, d1b-void-d8153f733f2baca55aa98c65,
d1b-void-b723532a738b861b7e6d35f3 — all fit.

## Rows decided one by one

Accounts, groups, access rule, two npm code rows, three store rows, and the groups `/boot`, `/etc/default`,
`/etc/modules-load.d`, `/etc/sudoers.d`, `/mnt`, `/var/db/xbps/keys`, `/home/user/.local/share` (hand-written table
in (not published: orchestration or scratch); reasons in the output).

## Question for the author (not decided here)

Whether a package updated to a new version is still "such a package" in S8.2-7 for objects obtained from its
earlier version that remain on the computer. Reading 1: the package is the same (by name), so they are installed
objects covered by its line. Reading 2: each version is a different package, so the earlier version is no longer
installed and question 1 is no. It decides the root account (GAP-TWO) and, together with an unknown fact, the
kernel 6.12.11_1 leftovers.
