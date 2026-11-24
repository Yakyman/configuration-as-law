# Classification c2, part gentoo: notes

2026-11-23 UTC. Input `D1b/in/part-gentoo.tsv` (32 775 rows). Output `D1b/c2/part-gentoo.tsv`. Facts were read from the
handoff copy `D1b/handoff/gentoo/` (for `raw:` read `D1b/handoff/gentoo/raw/`, for `raw:members/` read
`D1b/handoff/gentoo/members/`). Scripts and intermediate tables are in (not published: record outside selected evidence): `classify.py` (writes the table),
(not published: orchestration or scratch) and (not published: orchestration or scratch) (rules for stored paths), `verify.py` (final check), `meaning.py` (meaning file).

## 1. Facts established from the inventory

- **Canonical paths (merged /usr).** The scan (`raw/0004-filesystem.out`) records `/bin -> usr/bin`, `/sbin -> usr/bin`,
  `/lib -> usr/lib`, `/lib64 -> usr/lib64`, `/usr/sbin -> bin` and 29 other directory links. Portage CONTENTS (decoded
  from the `*-metadata-read-*.out` (some matches not published: direct evidence at least 2 MB) (some matches not published: pre-observation input or preparation record) outputs, 321 packages, 124 680 entries) record files under `/bin`, `/sbin`, `/lib`.
  A stored path counts as "listed in CONTENTS" only when its canonical path (directory links resolved in the parent
  components) equals the canonical path of a CONTENTS entry. Integrity is the `package-files.tsv` row of that entry;
  for symlinks the observed target (scan) is compared with the CONTENTS target; directories have no integrity row.
  Result: 5 230 group members and 243 single code rows recorded "ownership unresolved" are files of packages, recorded
  unchanged (e.g. `/usr/bin/bash` = CONTENTS `/bin/bash` of app-shells/bash, unchanged).
- **Digests of small files.** For files of at most 4 096 bytes the recorded `sha256-prefix4096` is the full SHA-256.
  Established this way: `/etc/env.d/02locale` = `LANG="en_US.UTF-8"`; `/etc/subuid` and `/etc/subgid` =
  `user:100000:65536`; `/home/user/.bashrc`, `.bash_profile`, `.bash_logout` are byte-identical to `/etc/skel/*` of
  app-shells/bash (recorded unchanged); `/boot/grub/grubenv` is not the empty GRUB environment block (computed digest
  `2e4234c8...` differs from recorded `f6412285...`); pip (not published: record outside selected evidence) scripts equal their RECORD SHA-256 and size.
- **baselayout defaults.** The baselayout `share/passwd` and `share/group` texts (from the baselayout source mirror)
  give exactly the MD5 values recorded in CONTENTS of sys-apps/baselayout-2.18-r1 (`86924eb7...`, `c5639248...`;
  (not published: orchestration or scratch), (not published: orchestration or scratch)). Accounts and groups were compared line by line.
- **sudo.** `/etc/sudoers` is recorded `changed`; its active lines (`raw/0153-metadata-read-0.out`) end with two
  `@includedir /etc/sudoers.d`; `/etc/sudoers.d/lab-access` = `user ALL=(ALL) NOPASSWD: ALL`, so `sudo -l` for user lists
  it twice (`raw/0150-sudo-user.out`).
- **Package reasons.** Portage: 10 explicit (selected set), 359 unknown; Python: 2 explicit (REQUESTED), 69 unknown, of
  which 53 have native Portage ownership and all their package files under the location are recorded unchanged
  ((not published: orchestration or scratch)).
- **Profile chain** of `/etc/portage/make.profile` (`default/linux/amd64/23.0`): arch/base, features/multilib,
  arch/amd64, releases, releases/23.0, default/linux/amd64/23.0 (parent files of the Gentoo repository; the snapshot's
  member lists show `parent` files exactly in arch/amd64, releases/23.0, default/linux/amd64/23.0).
- **Installed interpreters:** bash, perl, python 3.14, openrc-run, gawk; no emacs, php, ruby, lua, node, vim, csh.

Documentation used (quoted by the reasons): Portage `ebuild.5` ("All ebuild scripts are written in bash"), `portage.5`
(profile.bashrc: "same as for any other bash script"), `env-update.1` (generates profile.env and ld.so.conf);
PMS 11.2 (variables preserved "for later functions, including functions executed as part of a later uninstall");
toolchain.eclass (`do_gcc_config`), binutils-2.47.ebuild (`binutils-config`), rust-bin ebuild (`eselect rust update`),
iptables-1.8.13.ebuild (`eselect iptables set`), pinentry-1.3.3.ebuild (`eselect pinentry update ifunset`),
kernel-install.eclass (`dist-kernel_update_src_symlink`, `installkernel`), baselayout-2.18.ebuild (copies
passwd/group/shadow/fstab in pkg_postinst if missing), acct-user.eclass (useradd in preinst, usermod of comment, home,
shell, groups in postinst), acct-group.eclass (groupadd in preinst), shadow ebuild (grpconv when gshadow is missing),
OpenRC `runlevels/meson.build` (default runlevel links), udev-init-scripts-35, kmod-34.2, systemd-utils-262 ebuilds
(sysinit/boot links in pkg_postinst), installkernel wiki page (dracut plugin), grub-install(8) (`--themes` default
starfield; copies images and modules into boot/grub), Docker firewall-iptables page (DOCKER chains, FORWARD policy DROP),
dhcpcd(8), dhcpcd-run-hooks(8), OpenRC user guide (user runlevels in ~/.config/rc/runlevels), AppImage docs (run
without installation), Firefox libpref docs (prefs.js managed by Firefox, user.js by the user), ClearURLs manifest
(no nativeMessaging), MDN native messaging, ScriptPreloader.h (cached script stencils).

## 2. Rules applied by script (each follows from the cited sentences)

Order inside a stored path: R1, R2, then the area rules. Group rows (`L2:stored-ownership-unresolved`): every member of
the complete member table is decided by these rules; if all members get one decision the row gets it, otherwise
MIXED with the members per decision named in `reason` (R11).

- **R1 runtime** (member `persistence` = runtime, tmpfs): RUNTIME, belongs to the program owning that subtree
  (S8.2-5).
- **R2 listed in CONTENTS and unchanged** (canonical path, see 1): INSTALLED-PACKAGE (S8.2-7, S8.2-8, S8.2-16).
- **R3 repository bash code**: `*.ebuild`, `*.eclass`, `profile.bashrc` under `/var/db/repos/gentoo`:
  PROGRAM-DERIVED — code Portage executes with its rights (S8.2-9, S8.2-10, S8.2-23), obtained by Portage sync from the
  repository line (S8.2-16).
- **R4 repository scripts in an installed language** (shell-named init/rc/sh/bash files, `.py`, `.pl`): PROGRAM-DERIVED.
  conf.d templates are read as values when installed and executed by nothing here: handled as R8.
- **R5 repository shebang files whose name gives no language**, and `metadata/install-qa-check.d/*` (execution not
  documented in the sources consulted): UNKNOWN — interpreter or execution not recorded; installed interpreter gives
  PROGRAM-DERIVED, otherwise R8.
- **R6 code for an interpreter not installed** (`.el`, `.php`, `.rb`, `.lua`, `.vim`, `.js`, `.tcl`): not a program
  (S8.2-20), then R8.
- **R7 profile values Portage applies**: value files of the six chain directories, and repository-wide
  `profiles/{package.mask, thirdpartymirrors, license_groups, categories, repo_name, eapi, arch.list,
  package.deprecated}`: SETTING-OWN (S8.2-11, S8.2-12, S8.2-13; not obtained with a package, S8.2-17).
- **R8 other repository files and directories**: GAP-TWO, RECORD or MATERIAL (S8.2-15): the snapshot was written by
  Portage sync as it ran (program record) and fetched at a person's command (downloaded file, material); no sentence
  says which prevails.
- **R9 vdb code**: `/var/db/pkg/*/*/*.ebuild` and `environment.bz2`: PROGRAM-DERIVED (PMS 11.2; S8.2-9, S8.2-23,
  S8.2-16). **R10 other vdb files and directories**: RECORD (S8.2-15).
- **R11 aggregation** of group rows, as stated above.
- **R12 packages**: Portage selected → INSTALLED-OWN (S8.2-1, S8.2-16); Portage reason unknown → UNKNOWN (explicit gives
  own line, dependency gives derived line); Python with native Portage owner → INSTALLED-PACKAGE; Python REQUESTED →
  INSTALLED-OWN; Python without REQUESTED → UNKNOWN.
- **R13 processes, kernel modules, drivers, ports, firewall rows**: RUNTIME (S8.2-5); `reason` names the owning
  executable/package (process), the `.ko` file or the kernel image (module), dockerd or the kernel (firewall).

### Hand checks (10 rows per rule; all agreed with the rule)

- R2 (single code rows): 8f6945623c206e0ded79c948 120b2a9358fefbd2c3cd47a9 e5f6b730cbc2fe00acc04acf 266b0fb4c5eeab755b2eee56 fba66f0d14b29bd79288a1c0 2dd528d744754e75ffec3b13 a607e502c298e194d7978dfc 9e3ea9ac9b5fdfc7281c6e94 f771ad1a15de095e38253431 35bceff2764ca2688e5f4987 (checked against package-files.tsv `/sbin/*`, `/lib64/*` rows).
- R2 (module groups): 88f7bfa7485de82a0a10839a 1510c98f3981817cfdd80fe1 94216e1bcc6a8eaa7f3174d1 139aa42224b6a3405145645c 489de492f23ff25214b146aa f3c2c92a693e88ffa61e85c3 cf9a233e41cbfc6666b30d97 d1df354237383876a1256535 bf6cc998fce5747a1f84da1b fd0c8c11cd74309c074e9594.
- R3/R8 (repository package directories, MIXED): 2df7db487d5c487ba3393957 34d9c6263afd04d869ddb329 c58a4bef85bea1183324daaf 6d30b4293223b2618211e095 3c0315aa2c7ad30c803270f2 3fa0921403c60cc43b6d287d 9fef590b5678c3892fcf859c 3b40d70f32e3cd1c3522bfc7 23d64555e8e0ff1f6f64bd6b b8c97c7c507c256d80839c75.
- R4 (single code rows): d1a1869b5087cbcc4f6df688 c61ecd45c427ac8d8bb2344d 88ce35cc42f0e46ba649e518 ab1240d01684ae4a7bcf39e3 e70fb8e55b8be25200da2939 68f08699147401151595dbac e4ef04c8793e1e3f04a6d092 95c4f80cd62fde817fed57ef 582899f846940df36ddfbef0 591091e7797fac52b33acba4.
- R4 (groups): 22188cad44f3c97b031562bd bf56db098d947c8b884334e3 c2c9b1272d5a2d345b5b1126 d1638f9775fe575bf2e60fa5 54e8e3b0a4ce24f30310a0ff b4cf64985f82f53f9ad02a92 472a9076f8e7ab06536e45b3 5849c89ecea9e6118b9fad22 ec602220ea001dd90ab69aed d5bf50d7bb227b8b9d2471aa.
- R5: 572b5d419ab87a02caa7d257 07c08f05b3f66665b293d3d9 e2f092c203a8a139f56b8770 109bfeb59925a0400c2fb9f5 d8385c9b1318f95d25665450 ff3309e46dcc94879d824034 907d81ea40dec77c0de10b6c 1ba65d74f717d349215cdac9 7ffe3e686e67d479ea6a9a72 9821cc27117527d39af22776.
- R6/R8 (GAP-TWO groups): 40f9b81ab90846da84b77156 45565515f5a96316b734de8c e585a78143341b60ebcef330 6ccdf34cc7948b4148c57f11 daef86ece0da369ce82775b3 360d665e26b9b6d8c311db13 acf1bcc5585c7f1a0323a88c ce399d23041dec189cc53e0b f5e45c2465ee563e2e68f3c7 f90a8e74ac6a89e06d8aa5a2; conf.d single rows 81249102e620289601c15e04 0c33a61c3a812bdbbc0ddb0d.
- R7 (only rows of the rule that are not MIXED): d4bcdd8be82152fedbb1c210 ce3e687674d6e09c0b0c80b6; MIXED chain rows checked: 79e131f6f492e20e69973658 (releases/23.0).
- R1: ea1d6248e2d33b8c99785f09 036477011f2e46ab1e24aa6f da7c879fbf578f2981f58339 1831aa9c72991859192d6850 524e5df3f037935ab62b5b70 968a2013c076659b8e2522ce 726b6ec611b8bd44d8f9c349 9fb2ffc31c82cfee77b40afc 39b582d0cd543dad511ba39c fef59845ce7f2d2c57387fe0.
- R9/R10 (MIXED): c4c15b61714c76a8566a2e71 42ffee329c176242abc0e8d6 db6e52b374bef50184894cd2 bbf6b59ecf9939841386de15 0e0647123e0ea4c6fa029fc0 14f487d1ee88a220f6f7a1e7 5ae3401d42568a33edb396a9 3bd719c918e09e558e88fbfe ac20a01e57862f71fea5131a d7ecd3624b252c82b26f048e.
- R10 (RECORD): 913b74c7aea623d095c40f55 84f6c49600ae61fa3e94b740 d0efdabd0c46376057638f4f ebd83fba66212dd8a802004b 4e298f966eae1de46424c614 1099942ef416d3920cd37622 894faeeb82ad8ac5a58f9ed3 0f6b952be7482539b8401068 fa7a3d872ca25c324f45a17b abfdea4281bf01fe489d3285.
- R12: 03ab718ffeb8bd7f475b9750 22e6e62867c2fcb815e74dce 3115c484fad41a4aae69007f a62af40e3db10b9417e7d8c7 2e7f25f868158505ef5ffaa1 4fdc4b1911980b52450bbf10 4fffe2e4098ee826600b2288 6e1edc972d3e6edf02da56e9 126dceea2c0c955656a52d75 191894ff22e051a1571ba20d.
- R13: 60b3154fd682601fdb7eacb0 81a776a523e0d9b81a3c89e1 232fb98f21f3f25243aa3f17 7f655affe70e9a7d4012ef8c 5542a87b6ead732352b9bc92 ca984d4270baac7d2fb5ae93 cb3bb939379c40ab4b704082 9c3becc9f3c0ba3d1105e703 9759df30fc573cc5b93730f8 054a8ec1c6b5ab85b8dede5c.

(ids above omit the `d1b-gentoo-` prefix; (not published: orchestration or scratch) lists the full sample per rule.)

## 3. Decided row by row

Everything outside R1–R13 is decided individually: the explicit path table `EXACT` and the area functions in
(not published: orchestration or scratch) (/, /boot, /etc, /home/user, /tmp, /usr links and indexes, /var/cache, /var/lib, /var/log,
Firefox profile, pip target trees), and in (not published: orchestration or scratch) accounts, groups, OpenRC service and runlevel rows,
sudo rows, access-rule files, the container, the image and the two stores. Main points:

- System accounts/groups equal to baselayout lines, or created/updated by installed acct-user/acct-group packages:
  SETTING-DEFAULT (S8.2-17). Account `user`, group `user`, and `wheel` (member `user` added): SETTING-OWN.
- OpenRC: enablement links listed in openrc CONTENTS → INSTALLED-PACKAGE (Q1: default setting values obtained with the
  package); links created in pkg_postinst (udev, udev-trigger, kmod-static-nodes, systemd-tmpfiles-setup[-dev]) →
  SETTING-DEFAULT; dhcpcd, docker, sshd in default → SETTING-OWN; services enabled nowhere → their init script
  (INSTALLED-PACKAGE); dynamic runlevels, containerd started as a dependency, user.user → RUNTIME.
- Toolchain selection links and env.d files written by gcc-config, binutils-config, eselect rust/iptables/pinentry in
  pkg_postinst, and `/usr/src/linux` (kernel-install.eclass) → SETTING-DEFAULT. Perl dual-life links: UNKNOWN (creator of
  the links not established).
- `/boot/vmlinuz-*`, initramfs, GRUB modules/images, grub.cfg → PROGRAM-DERIVED; System.map, config, GRUB locale/fonts/
  themes/lists → RECORD; grubenv → UNKNOWN (content).
- Home: skel copies → PROGRAM-DERIVED; user service script, user script, Firefox wrapper and AppImage → PROGRAM-OWN;
  user runlevel link, authorized_keys → SETTING-OWN; pip packages' bin scripts and tree directories → INSTALLED-PACKAGE;
  Downloads → MATERIAL; caches and Firefox state → RECORD; prefs.js, user.js, logins/key4/permissions, .gitconfig,
  cal-secondary-dhcpcd.conf, script preloader caches → UNKNOWN (content or use not recorded); directories whose creator
  is not recorded → UNKNOWN.
- `/var/lib/portage/world` → SETTING-OWN (packages a person chose; S8.2-12 "however it was entered").
- Docker: container → PROGRAM-OWN (S8.2-22); image → GAP-TWO (INSTALLED-OWN if Docker counts as an installer under
  S8.1-4, PROGRAM-OWN otherwise); Firefox extension xpi → GAP-TWO (installed object by Q1 and S8.1-5, but S8.2-21 says
  such code need not be recorded).
- Header and framing lines of `sudo -l` and `iptables-save` output → RUNTIME (output of a running process).

## 4. Gaps and unknown facts (summary)

- GAP-TWO, 7 437 rows: 7 435 repository rows (R8, with R6 and conf.d templates), the docker image, the Firefox extension
  directory. Answers to PROTOCOL Section 2: `D1b/c2/meaning-gentoo.tsv`.
- UNKNOWN, 787 rows: 359 Portage + 16 pip package reasons; 397 repository rows (R5; shebang language or QA-check
  execution); sudo default lines in the changed sudoers (5); directories whose creator is not recorded; content of
  grubenv, prefs.js, user.js, .gitconfig, logins/permissions stores; subuid/subgid (chosen or allocated); perl links.
