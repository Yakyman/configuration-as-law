# Facts established for part l2-other (L2 rows of alma, void, talos; 1853 rows)

Paths below are relative to the night folder. Inventory paths `members/…`, `raw/…` are relative to (not published: record outside selected evidence).
Scripts are in (not published: record outside selected evidence) (all named `l2o_*`), and their outputs are in `D1/adjudication/raw/`. The class of
every member is in `D1/adjudication/raw/l2o_member_classes.tsv` (id, path, class, tag). Verdicts are made by
(not published: orchestration or scratch), and (not published: orchestration or scratch) checks them (ids equal the input set: 1853 = 1853).

## Sources built from the inventory

- XBPS manifests: (not published: orchestration or scratch) decodes the per-package files plists in void `raw/0012…0017-metadata-read-*.out` into (not published: downloaded distribution package metadata or sources), with 47,044 entries (files 34,474, conf_files 130, links 2,241, dirs 10,200). Six meta packages have no plist ((not published: downloaded distribution package metadata or sources)).
- XBPS pkgdb: (not published: orchestration or scratch) decodes void `raw/0011-metadata-read-0.out` into `raw/l2o_void_pkgdb.tsv`, and (not published: orchestration or scratch) extracts the alternatives into `raw/l2o_void_alts.tsv` (49 links).
- rpm manifest: alma (not published: over 20 MB) is copied to (not published: over 20 MB). On alma `/lib`, `/lib64`, `/bin` and `/sbin` are symlinks to `usr/…` (alma `raw/0004-filesystem.out`), and rpm records `/lib/modules/…` and `/lib64/…`. The collector compared only `/usr/…` paths, so (not published: orchestration or scratch) also looks each path up under its alias.
- Member facts: `raw/l2o_void_members.tsv` (8,921 members, none in the XBPS manifest), `raw/l2o_alma_members.tsv` (3,941 members; with the alias 1,597 are package files), and `raw/l2o_talos_members.tsv`.
- Directory contents: (not published: orchestration or scratch) found no directory member whose contents are represented nowhere else (`raw/l2o_void_uncovered.tsv`, `raw/l2o_alma_uncovered.tsv`). So a directory member is the directory entry only. This includes `__pycache__`, whose `.pyc` files are rows of their own.
- Ordinary actions: the action scripts are unpacked from `D1/in/control/void/launch.sh` into `raw/l2o_void_actions/` (`ordinary.sh`, `void.sh`, `alma.sh`).

## Groups

- **void old kernel, 1068 rows → GAP old-version-leftover.** The rows are `/usr/lib/modules/6.12.11_1/**` (1066), the directory itself, and `/usr/lib/modules`. They hold 1066 directories, 5,437 `.ko*` files and 13 `modules.*` lists, with file mtimes of 2025-01, none in the manifest. `D1/in/control/void/actions-logs/actions-logs/package_program.log` line 316 reads `linux6.12 (6.12.11_1 -> 6.12.118_1)` and line 4850 `updating to 6.12.118_1`, and pkgdb has `linux6.12-6.12.118_1`. The current version ships the same `modules.*` files (manifest). `/boot/vmlinuz-6.12.11_1` and `/boot/config-6.12.11_1` are the same kind of leftover.
- **alma kernel modules, 178 rows.** 177 → INSTALLED-PACKAGE: through the alias, members are in `kernel-modules-core` and related packages, with directories of the recorded mode (697), files `unchanged` in `package-files.tsv` (891) and links equal to the record (2). 1 row (`/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64`) → GAP generated-list: there are 10 `modules.*` lists that rpm records with size 0 and no digest, while the files are 433–954,606 bytes and their ctime is 05:56:22.
- **void `__pycache__` and pip directories → RECORD.** 101 rows under `/usr/lib/python3.14` and 29 under (not published: record outside this collection) (including the 3 `*.dist-info` rows) hold only directory entries (`__pycache__`, package directories, `*.dist-info/licenses`). None is in a manifest (pip RECORD lists no directories), and all were created by the XBPS byte-compile trigger (`browser_extension.log`: “Byte-compiling python code in usr/lib/python3.14”, ctime 11:20:31) or by `pip install --target` (`ordinary.sh` browser_extension). Every `.pyc` inside has its `.py` source in the XBPS manifest or in pip RECORD (`raw/l2o_void_pyc.tsv`). Rule 7 applies.
- **pip entry scripts `cal-marionette/bin/*` (void 9 rows, alma 9 rows) → INSTALLED-PACKAGE.** The full sha256 of each script equals the digest that pip RECORD gives for (not published: record outside this collection) (`raw/l2o_void_pipbin.tsv`, `raw/l2o_alma_copies.tsv`; files are under 4096 bytes, so the prefix signature is the full hash). pip installed them as part of the package (S8.1-6).
- **skel copies → PROGRAM-DERIVED.** These are `.bash_logout`, `.bash_profile` and `.bashrc` in void `/home/user` and `/root`, and in alma `/home/user`. Their full digests equal the `/etc/skel/*` package records (void base-files conf_files, alma bash) (`raw/l2o_void_copies.tsv`, `raw/l2o_alma_copies.tsv`). `.inputrc` copies are readline values → RECORD.
- **void `.new` files.** `/etc/issue.new-0.144_1`, `passwd.new-0.146_1` and `rc.conf.new-20250212_4` have full digests equal to the conf_files records (base-files, runit-void) → INSTALLED-PACKAGE. `libc-locales.new-2.41_1` is longer than 4096 bytes → UNKNOWN.
- **GRUB, void and alma.** The `i386-pc` `*.mod`, `*.img` and `*.o` files are code; 155 (void) and 124 (alma) of them have digests equal to `/usr/lib/grub/i386-pc/*`; they are PROGRAM-DERIVED. The 8 `*.lst` files per machine are generated-list. `modinfo.sh` → RECORD, because `grub_install_get_target` reads it with `strstr` as values (S8.2-23; source https://raw.githubusercontent.com/rhboot/grub2/fedora-39/util/grub-install-common.c). Fonts and `.mo` files are copies written by grub-install → RECORD. void `grub.cfg` (ctime 11:19:02, written by the kernel hook during package_program) is GRUB script → PROGRAM-DERIVED. alma `00_tuned` is a byte copy of tuned `/usr/share/tuned/grub2/00_tuned` → PROGRAM-DERIVED.
- **initramfs (void 3 images, alma 3) → GAP archive-of-code** (dracut logs in `package_program.stderr`).
- **Alternatives → GAP default-at-install.** void `/usr/bin` (25), `man1` (13), `man8` (4), `/etc/sv/ntpd` and `/etc/kernel.d/post-*/20-initramfs` all match `raw/l2o_void_alts.tsv`. alma `/etc/alternatives` (45), `/var/lib/alternatives` (11), and `/usr/bin`, `/usr/sbin`, `man1` and `man8` links pointing to `/etc/alternatives/*` are the same. Further default-at-install groups:
  - alma `/etc/systemd/{system,user}` preset links, ctime 05:52–05:56 during package installation;
  - void runit-void links (ctime 11:19:02);
  - alma authselect files and links;
  - alma nvme hostid and hostnqn;
  - alma SELinux module store `modules/200/*/*`;
  - alma microcode links;
  - void `/etc/shadow` and `/etc/gshadow` (they hold accounts that package scripts created, ctime 11:20:59 and 11:21:10);
  - npm bin links (void `node_modules/.bin`, alma (not published: record outside this collection) and `cowthink`);
  - Firefox `extension-preferences.json`.
- **generated-list** (S8.2-15 “cache” against S8.2-16 “a generated list”):
  - MIME database files;
  - `/etc/ssl/certs` (226);
  - `hwdb.bin`, `ld.so.cache`, `aux-cache`, `locale-archive`, `mandoc.db`;
  - `*.cache`, `mimeinfo.cache`, `icon-theme.cache`, `gschemas.compiled`;
  - void `/etc/shells`;
  - alma `/etc/dconf/db/*`, the swcatalog `.xb` caches, and the rescue-kernel `.hmac`.
- **Action-made objects.** Scripts written by actions → PROGRAM-OWN (`cal-user-script` by home_script; `run` files by user_service). Directories made by action commands (`mkdir -p`, `install -D` in `ordinary.sh`, `void.sh`, `alma.sh`) → MATERIAL. `Downloads/*` → MATERIAL. nmcli connections, the alma user unit and its enable link, `authorized_keys` and `zz-lab` → SETTING-OWN.
- **void runit enable links with ctime ≥ 11:20:51 → SETTING-OWN.** These are runsvdir-user, dbus, NetworkManager and docker, linked by `void.sh`.
- **Values written at image build or clean installation whose chooser is not in the inventory → UNKNOWN.** These are void `localtime`, `sudoers.d/wheel`, `dm-raid.conf`, the xbps key, `live.conf`, and the acpid, chronyd, sshd and agetty-ttyS0 links; and alma `ens3.nmconnection`, `sysconfig/kernel`, `sysconfig/network`, `device.map`, `default.target` and `alsa/state-daemon.conf`. Firefox `prefs.js` is UNKNOWN because its content was not collected.
- **alma npm files ((not published: record outside this collection), 50 rows including 2 code rows) → UNKNOWN.** npm keeps no per-file digest, so “remains as received” cannot be shown (rulebook reading 1). Directories in these rows → RECORD.
- **alma opaque stores** (not published: record outside this collection) and `/var/lib/containers/storage` → UNKNOWN, because their contents are not inventoried per file. `/var/lib/flatpak` is a directory of package flatpak with the recorded mode → INSTALLED-PACKAGE.
- **Compiled script caches → PROGRAM-DERIVED:** alma `/tmp/node-compile-cache/v22…` (552 files), and Firefox `startupCache/scriptCache*.bin` and `startupCache.8.little`.
- **alma `/tmp` and `/var/tmp` `systemd-private-*` (21 rows) → RECORD.** The member persistence is `persistent` on XFS (alma `members/*.tsv`), so rule 6 (RUNTIME) does not apply.
- **void `/run` and `/tmp`** have persistence `runtime` → RUNTIME (members of `/`).
- **talos.** The mounts in talos `raw/0004-talos-mounts.out` are: devtmpfs `/dev`; tmpfs `/run`, `/system`, `/tmp`, `/etc/cni`, `/etc/kubernetes`; overlay `/` and `/etc`; and `/dev/vda6` `/var` (`raw/0006-talos-mount-resources.out`: xfs).
  - `/dev`, `/run/**`, `/system`, `/etc/cni` and `/etc/kubernetes/**` → RUNTIME. `/proc` and `/sys` are kernel pseudo filesystems → RUNTIME.
  - `/var`, `/var/lib` and `/var/log` → RECORD.
  - Image entries and `/etc` entries → UNKNOWN: integrity is unknown, there is no image manifest, and the backing of each `/etc` entry is not shown. The architecture doc says only specific `/etc` files are bind-mounted from `/system` (https://docs.siderolabs.com/talos/v1.11/learn-more/architecture).
- **ClearURLs extension (void, alma) → GAP code-inside-program-package** (new; see `l2-other.HOLES-NEW.md`).

## Decision mechanics

The verdict word is the largest member class. A tie is broken by the order of the questions (Q1 before Q2 before Q3 before Q4). The tie-break decided void `/etc/sv/runsvdir-user`, (not published: record outside this collection), (not published: record outside this collection), alma (not published: record outside this collection) and alma `/usr/lib/firmware`. A classification that answered MIXED did not err when its listed classes equal the member classes and it had no UNKNOWN or GAP.
