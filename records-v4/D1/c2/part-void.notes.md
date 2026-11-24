# c2, part void — notes

Input: `D1/in/part-void.tsv` (3,282 rows). Output: `D1/c2/part-void.tsv`. Decisions are produced by
(not published: orchestration or scratch) (run from `D1/c2/`), whose rules are listed below. Rules apply the four questions of
Section 8.2 in order (S8.2-6) and the sentences under "Which line records an object" (S8.2-16 to S8.2-19).
Times are UTC.

## Inventory facts used

- Package reason (`explicit` / `dependency` / `unknown`): `members` JSON of package rows (FACTS.md, void).
- Packaged-file integrity: `D1/in/raw/void/package-files.tsv` (`unchanged`, `changed`, `missing`, `unknown`).
- Group members and persistence: (not published: record outside selected evidence).
- XBPS manifests, directories included: decoded from the raw `*metadata-read*.out` (some matches not published: direct evidence at least 2 MB) (some matches not published: pre-observation input or preparation record) reads by
  (not published: orchestration or scratch) into (not published: downloaded distribution package metadata or sources). The six unread plists are meta-packages with no file
  list ((not published: downloaded distribution package metadata or sources)). This confirms that every group member is absent from all installed
  manifests, directories included.
- What the ordinary actions did: `D1/in/control/void/actions-logs/` and the action scripts carried in
  `D1/in/control/void/launch.sh`, unpacked for reading only into `raw/void-actions-payload/` (`void.sh`,
  `ordinary.sh`, `firefox-addon.py`).
- Running kernel: the machine booted about 11:16 and `lifecycle.tsv` records no reboot. The kernel update ran at
  11:18–11:19 (`package_program.log`), so the running kernel is 6.12.11_1, and its modules are in the old-kernel tree.
  The inventory does not show the running kernel directly; this follows from the times.

## Public documentation cited

- Void kernel handbook, https://docs.voidlinux.org/config/kernel.html: "When updating the kernel, old versions are
  left behind in case it is necessary to roll back to an older version."
- linux6.12 template, https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/linux6.12/template:
  `preserve=yes`. Manual.md, https://raw.githubusercontent.com/void-linux/void-packages/master/Manual.md: "`preserve`:
  If set, files owned by the package in the system are not removed when the package is updated, reinstalled or
  removed." Manual.md, `make_dirs`: "directories and permissions to be created at install time".
- runit-void INSTALL, https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/runit-void/INSTALL:
  "# Enable default services:"; `ln -sf /etc/sv/agetty-tty$f etc/runit/runsvdir/default`;
  `ln -sf /etc/sv/sulogin etc/runit/runsvdir/single`; `ln -sf default etc/runit/runsvdir/current`.
- mklive.sh, https://raw.githubusercontent.com/void-linux/void-mklive/master/mklive.sh:
  `DEFAULT_SERVICE_LIST:=agetty-tty1 … agetty-tty6 udevd`; `-S "<service> ..." Enable services in the ISO image`;
  `copy_void_keys` (`cp keys/*.plist "$1"/var/db/xbps/keys`); `echo "dm-raid" > "$ROOTFS"/etc/modules-load.d/dm-raid.conf`.
- installer.sh, https://raw.githubusercontent.com/void-linux/void-mklive/master/installer.sh:
  `ln -sf "/usr/share/zoneinfo/${TIMEZONE}" "${TARGETDIR}/etc/localtime"`; `chroot $TARGETDIR grub-install …`;
  `chroot $TARGETDIR useradd -m -G …`. Two lines are known only from a summary of the truncated page, not verbatim:
  the `/etc/sudoers.d/wheel` line and the copy of `/etc/skel` files to `/root`.
- base-files `passwd` and `group`,
  https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/base-files/files/passwd and `.../group`:
  `root:x:0:0:root:/root:/bin/bash`, `nobody:x:99:99:…`, and 29 groups with no members. On the host,
  `/etc/passwd.new-0.146_1` is 86 bytes, the exact length of the two shipped lines.
- System accounts: chrony template `system_accounts="chrony"`, dhcpcd template `system_accounts="_dhcpcd"`,
  util-linux template `system_accounts="_uuidd"`. The action logs record "Created _tss / polkitd / _flatpak / dbus /
  docker system group/user".
- eudev INSTALL: `usr/bin/udevadm hwdb --update`. ca-certificates INSTALL: `update-ca-certificates --fresh`.
  openssh sshd run: `ssh-keygen -A … # Will generate host keys if they don't already exist`.
- docker image pull, https://docs.docker.com/reference/cli/docker/image/pull/: "Download an image from a registry".

## Rules (scripted; each follows from the cited sentences)

- R1 Packages (`L1:package`): an installed package answers question 1 "yes" (S8.2-7, S8.2-8). The line follows
  S8.2-16. Reason `explicit` → INSTALLED-OWN. Reason `dependency` → INSTALLED-DERIVED ("a package installed as a
  dependency of a recorded package"). Reason `unknown` with a native owner (npm modules bundled in `/usr/lib/node_modules`,
  and pip under `/usr/lib/python3.14`) → INSTALLED-PACKAGE when all its files are recorded `unchanged` ("obtained as
  part of such a package and … remain as received"). Reason `unknown` without an owner (16 pip packages under
  (not published: record outside this collection)) → UNKNOWN; the missing fact is explicit or dependency.
- R2 Any object recorded `unchanged` in `package-files.tsv` → INSTALLED-PACKAGE (S8.2-7, S8.2-8, S8.2-16). This covers
  PAM, polkit and sudoers default files, wpa_supplicant.conf and the GRUB images under `/usr/lib/grub`. Default
  setting values obtained with a package fall here and not under S8.2-17, because question 1 comes first (S8.2-6).
  The same holds for polkit actions defined in such files, for `sudo -l` lines that come from the unchanged
  `/etc/sudoers`, and for base-files account and group records that are identical to the shipped ones.
- R3 Objects on a filesystem whose recorded persistence is `runtime` (`/run`, `/tmp`), processes, open ports,
  `/sys/module` names, `/sys/bus/*/drivers`, the live netfilter dump, NetworkManager profiles held only in `/run` and
  `sudo -l` headings → RUNTIME (S8.2-5). The reason names the creating program and that program's decision.
- R4 The old kernel tree `/usr/lib/modules/6.12.11_1`, plus `/boot/vmlinuz-6.12.11_1` and `config-6.12.11_1` →
  GAP-TWO. These are files of linux6.12 version 6.12.11_1, kept by `preserve=yes` after the update to 6.12.118_1.
  Question 1 asks whether the object was obtained as part of "a package installed on the computer". The text does not
  say whether a file kept from an earlier version of an installed package qualifies. If it qualifies, the decision is
  INSTALLED-PACKAGE (integrity is unrecorded). If not, code is PROGRAM-DERIVED (S8.2-9, S8.2-16) and data is RECORD
  (S8.2-15).
- R5 Bytecode `.pyc` under `/usr/lib/python3.14`, and pip `__pycache__` directories → PROGRAM-DERIVED. These are not in
  a manifest; Python executes them (S8.2-9); they are a "compiled copy" the system built (S8.2-16).
- R6a Lists and caches generated by installation triggers from package files → GAP-TWO. They are not in a package
  (question 1), are read as values (S8.2-23, so question 2 is "no") and are not chosen by a person (S8.2-11). By the
  order of the questions (S8.2-6) they are RECORD (S8.2-15 "cache"); S8.2-16 names "a generated list" as something
  installed and covered by a derived line, which gives INSTALLED-DERIVED. No sentence ranks the two. This covers
  ld.so.cache, aux-cache, the icon, GIO, GTK and GdkPixbuf caches, gschemas.compiled, mimeinfo.cache, mandoc.db,
  locale-archive, hwdb.bin, the `/usr/share/mime` database and the CA trust links in `/etc/ssl/certs`.
- R6b Caches written by programs as they run → RECORD (S8.2-15): the XBPS package cache and database, and the pip,
  npm, fontconfig and Firefox caches.
- R7 Program working state and logs → RECORD (S8.2-15): `/var/log`, `/var/db/dhcpcd`, `/var/db/sudo`,
  `/var/lib/{NetworkManager,chrony,dbus,seedrng}`, runsv `supervise/` state, shadow backups and locks, `resolv.conf`
  (written from DHCP), SSH host keys (generated by `ssh-keygen -A`), Firefox profile state, the empty `user.js`,
  `.gitconfig` (`color.ui false`: obeyed only by git, launches nothing, grants nothing, S8.2-14), `.inputrc`, and npm
  `package.json` / `package-lock.json` (S8.2-14).
- R8 Defaults created during package installation, of a kind S8.2-13 names as a setting → SETTING-DEFAULT (S8.2-13,
  S8.2-17). This covers system accounts and groups created by `system_accounts`, the runit service links and the
  `current` link created by runit-void INSTALL (re-created at 11:19 by the update), and `/etc/shells`.
- R9 Defaults created during installation, of a kind S8.2-13 does not name and not chosen by a person → GAP-TWO,
  SETTING-DEFAULT (S8.2-17) versus RECORD (S8.2-11 asks for "a value chosen by a person"). This covers xbps
  alternatives links in `/usr/bin`, `/usr/share/man/man1|man8`, `/etc/kernel.d/post-*/20-initramfs` and `/etc/sv/ntpd`,
  and npm `.bin` links.
- R10 Values written by the image build script (mklive), not by a package → GAP-TWO, SETTING-OWN versus RECORD:
  `/var/db/xbps/keys/*.plist` and `/etc/modules-load.d/dm-raid.conf`. S8.2-17 covers only package defaults.
- R11 Person-made settings → SETTING-OWN (S8.2-11, S8.2-13): services enabled by the actions (NetworkManager, dbus,
  docker, runsvdir-user), services enabled at image build with `-S` (acpid, chronyd, sshd), agetty-ttyS0 (05:49,
  laboratory), sudoers.d `wheel` and `zz-lab`, `/etc/localtime`, `/etc/shadow`, `/etc/gshadow`, the nmcli profiles,
  `authorized_keys`, account `user` and its group, `root` (its shell differs from the shipped record), group
  memberships that list `user`, and Firefox `extension-preferences.json` (grants access, S8.2-14).
- R12 Person-made code → PROGRAM-OWN (S8.2-9, S8.2-10, S8.2-16): `cal-user-script`, `service/cal-user/run`,
  `/etc/sv/runsvdir-user/run`, and the docker busybox image (pulled by a person command; docker documents pulling
  images, not installing programs, so it is no package; S8.2-22).
- R13 Code the system built or copied → PROGRAM-DERIVED (S8.2-9, S8.2-16, S8.2-23): initramfs images (dracut),
  `grub.cfg` (GRUB executes it as a script), GRUB modules and images written by grub-install, pip console scripts in
  `cal-marionette/bin`, and bash startup files copied from `/etc/skel`. Non-code files written by grub-install
  (fonts, locale, `.lst`, grubenv) → RECORD.
- R14 npm package files in (not published: record outside this collection) → UNKNOWN. The missing fact is whether they remain as received
  (metadata gap: "npm lock records packages but not installed per-file provenance"). If yes INSTALLED-PACKAGE; if no
  PROGRAM-OWN for code, RECORD for the rest.
- R15 Opaque stores (`/var/lib/docker`, `/var/lib/containerd`, (not published: record outside this collection)) → UNKNOWN; their contents are
  not enumerated.
- R16 Files downloaded by the action ((not published: record outside this collection)) → MATERIAL (S8.2-15 "downloaded files").

Single cases decided row by row (no script rule beyond a fixed path):

- The Firefox extension `.xpi`: GAP-TWO. It is code that Firefox's add-on manager installs, so INSTALLED-OWN by
  S8.2-1, S8.2-7 and S8.2-16 (S8.1-5 makes Firefox an installer in that part). S8.2-21 says code running inside a
  recorded program need not be recorded. S8.2-6 keeps the order of the questions but does not say which of the two
  prevails.
- The exited docker container: GAP-TWO, PROGRAM-OWN (S8.2-22) versus RECORD (stored state after exit).
- `prefs.js`: UNKNOWN; its content was not collected.
- `/etc/default/live.conf`: UNKNOWN; content and creator not recorded.
- `/mnt/lab`: UNKNOWN; who created it is not recorded.
- `.new-<version>` configuration copies: GAP-TWO, INSTALLED-PACKAGE versus RECORD.

## Convention for directories (not a text rule; stated so it can be reviewed)

The text does not say what a directory is apart from its entries. The script uses this convention:

- A member directory that has its own group row takes that row's decision. The member list of `/` includes `/`
  itself; that self-entry is skipped.
- A member directory without its own row takes the decision of the package files inside it.
- An empty directory on a persistent filesystem → RECORD, as made by an installer, image build or program as it ran.
  The exception is `/mnt/lab` (UNKNOWN).

A row whose entries get one decision takes that decision; otherwise it is MIXED, and the reason lists the decisions
with counts. The convention is recorded in `QUESTIONS.md`.

## Hand checks (10 rows per scripted rule; sample `raw/void-handcheck-sample.txt`, seed 1123)

For every sampled row I compared the raw facts with the rule's condition: member types, extensions and persistence
from the member TSV; the package reason; the executable path. All 170 rows fit their rule.

- R1 explicit: void-b634b9e73a6cc90dcb9368b5 void-d1a6342719808d440e416fb5 void-d7c8c9be4bb24a247fc7e249 void-1cccca1d50dee9738694e965 void-bd17767441e3004ea755186c void-2e391e3678099208f53f49ee void-beb7c20e2acc5d09338cf27c void-16835a573ba9028e2922fdf7 void-e67864859539dfc3e052263c void-bbf048357171b7089e69dcbc
- R1 dependency: void-08dedd1353261595b97276d0 void-4b7142cd2a3c4b60999166f7 void-ee4eca916b20123224c52bd4 void-e67a9303774f0d09f88561a8 void-84005c90e5b60ccf0aa198c9 void-932240552387d7c655a8826a void-21dc3eb098db65f56a8c5195 void-d79c02d2625cfe12032d1e48 void-50461e5ec7b7c400b3e5b159 void-f18d57aef7cf9147c883ba5b
- R1 bundled: void-de4c7b28bc7de4e9c443fc90 void-52743bf71ba6e8960449ad93 void-bbdbda1450c81f8e8223e63c void-181f1a5e5b0fabcefe2e84f4 void-a0dcd995bc9320444b9fbd95 void-9e77bdc6c50fd583781f6cee void-203e90fefc64ca561dd83447 void-7fe7349a1f1a032f40fe3524 void-7074e6d888d2d4a33c22ff9f void-114ea75193fabb92d74d0055
- R2 package files: void-ec564683f8b0aba561b18e11 void-de1fe6cc77ef458001963e74 void-a365d3e3b518437e36e7036a void-2dbeff424bb0e79738dfae3e void-f82b56aabbbb95b80fba17c0 void-b959641f896bb9f89663beb9 void-06aa0f65f4d80f0408bc9eeb void-edbb787c772774604e8c7dbe void-e4dfb1ec5f15f54e32d76c31 void-7d95ff8e200590ad44e0422c
- R2 polkit actions: void-98b721a07ebe82a9863629f9 void-bedf108901d92823142212f3 void-dd1272697ad0b083ce01772b void-72ebf325007bd69f02789ecd void-8c187e8e26bdfe661bd10d07 void-e0ac902d4d91e210fd29f3c0 void-b5ca4a6bb332c5519a30651b void-38349dbf9e98c643c7084d94 void-a82240a97aa436a258b0dd7b void-7a2072c1026c26f1f80a0a39
- R2/R8/R11 accounts and groups: void-1193d18a7a1cff135a824590 void-ce6a10ab4b63038472e06d9d void-cbb52b01a8aa9c4020b5c796 void-f42c2e5d5f04be742abc9e3f void-f5a28a9b09190744fc575c7b void-4a9a1bb10f9fd98cc5dd1dbc void-f206810b0ca7fdc4efe49d2d void-a5617f07bbf5290ccc5885d5 void-80ec9b4a3bee8a96bce61e7a void-d1dd8d7aab0a97cb0d7b3045
- R3 runtime files: void-f9b2444977462e693de0c745 void-c8e0d681ca168522d7f71b09 void-be609642219b97b855a53883 void-8821afed067840cd5f7ceb4f void-d2cd54f77bbfd89f28f78a17 void-8a9f9bb60d4cdc38982e8cf6 void-bd00157a38308b6f5f889902 void-1ff2f6524884bf13dd006817 void-449d0634ab8c8428d779e079 void-29dd9d2bb5edb661247d6482
- R3 modules: void-3fe2d45e1b2c81ce90e2c91c void-f6cc1fda5544539f9659d9e3 void-536864bc11804739ce3a9bf3 void-8cbd7f0be32c1d3a50d8994e void-22d45abf81d0e50073be481b void-f95b90782d4b554bdc80a902 void-85eb08e6755feaa9b64ecf24 void-2f34d0d9c3cf8a7294c5b0a4 void-1e4e9d0c9ed536348f63365c void-8ab0857be11abc986ced9463
- R3 drivers: void-c65cf2b3090c9480cdcf980b void-9dc8ba6864d378e5bc3dcf23 void-2c70723a69b302a3b37fb015 void-5dd2bbd7276b6d1884832642 void-b72de812234e4e1635e49adc void-15d1a1bb6adb31531052777a void-79c5d72ff8f762feb3e9d8b9 void-a36b4b0301561e548c0c4fca void-891cc37a1bd6a5c4601f10b9 void-0ae6b3e05a215b63746c9705
- R3 processes: void-10168ffb69e3955345202ab6 void-a7420a8bf6c5210f17e9760e void-65e1889013109fb4ab861083 void-e3a6f6a1ed12856e6fa00ef9 void-63a8614367263166b6962d8e void-4f2c4c69cdf7297383693777 void-c83bcafd2a811b819893f144 void-5a24dd1cf1ebfe89fe75eeb8 void-57b19bc9b5c702eb44bdd849 void-1a8045f4e662d2b5e436a077
- R3 firewall: void-4f1635dc90f7377384f40e39 void-7edeea0a468964b961f8a9e0 void-3859f7bb365ba428f30cb205 void-241000ed4e0e2bcfbbb7e55f void-88869804139f56487afb9423 void-e8af52cc1cd4a4be612b834f void-1ed8f362554935dbdcd5b27a void-6a8ac694052679cbe6a2db79 void-729d15f2340d597dbae39e3a void-b7f285fa9e678fbd8484c837
- R4 old kernel: void-04e3eea4c2fb87a603d0895d void-eeb8607fd77342bc5ebd266e void-e13f42e6d8947070fc87dd47 void-4b403739dbebb11240c40615 void-9d6a328268bae14d0117254f void-0bd1968056703de095cea93b void-0643e22223e732a826fa3630 void-f451c25da25b73d773c84f64 void-cbaef55d9f08a6196e1df543 void-1fd5d5eb9427f8f6ca27be05
- R5 bytecode: void-e1521dceb9362ca2032fd12d void-45149bf5108720c13ba09d2a void-9f1ac564dbe621a26111acd6 void-688ea0f6ae5233746d997bee void-7416a342d2f9e970b5848fd0 void-30e25d96c1f32aa2e72c3d8d void-4fd78c751d213cc90ddaf4f2 void-2ee949ce4c184e1cfaacdb35 void-eea18c2af51440f2e65e7a73 void-fee79e854512c9cac0224d29
- R6a MIME database: void-dacbbaea5fd0e1584cb3ce83 void-aa5952247dee0726fa4a93ed void-9f71a3d05aa0b8883e429a2d void-1b76f2b44c6677eaadefc56f void-9539a40ad287b2cb3c008cc9 void-1c6e59e1da4d2b39942e2c6c void-3c53d5a2bea4b5ffdd8b3725 void-e237d9083ceefc9ed7a744a0 void-f185ac6a8236aa68ceb0513b void-4fc1997e76eb1314366ddaa6
- R6b pip cache: void-056fb0c3034a3e56f1b0980e void-b2765f1d6b3f25837de0c8bb void-72bc6a73389130b57e18dd9e void-36414cd1ec1395e8344b654e void-2aee0498436343820fcddf0a void-432926a2ce495ff0a09b7502 void-6b2f22a499294219669a93f3 void-2e2986792ce0ba49f9b785cb void-f118d57f7af06d009fb2de25 void-9fd039663ae7be1646dd6a5e
- R6b npm cache: void-6844e399c700d4ffcd29743d void-8d6a4658fd621dc2903e8043 void-4180d0a9945a5284f430e138 void-72694af8a1180f4a10ac2a1e void-56dd610aeefa3cfff141a00a void-96d208feabadb659e4d3214d void-967413d6f17714587988f17f void-7858907a6d463e708be91d6f void-34771e4fdf0fe1d7e9bc829f void-22a1c019fdc33cdf542b18ab
- R14 npm tree: void-c4994e7829420ff37a008fb2 void-532c50ce762b2ea2ece1b84b void-e00bb4b95e6e7f2013d09973 void-a3a5c1ff5857a1086de06855 void-8f7fd43980d10a2426a5ea64 void-9992f667b4fb451afdbbabf1 void-a99e2797d84ce334a9a54ae0 void-6f3a1d6daf04e71f44bdc9f8 void-3be4be09469fe2e48ba1b513 void-51fc9356ab9def26b3483747

The rules with fewer than 10 rows (R7–R13, R15, R16) and every MIXED row were reviewed one by one from the full
listing in `raw/void-groups-annotated.txt`.
