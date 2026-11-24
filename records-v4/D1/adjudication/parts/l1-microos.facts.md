# Facts used for the L1 rows (all machines) and the d1-microos L2 rows

Paths are relative to (not published: record outside selected evidence) unless they start with `D1/` or `check-inputs-v4`. Scripts: (not published: record outside selected evidence).
Raw outputs: `D1/adjudication/raw/`.

## microos: retained snapshot 1 (4,316 rows resolved INSTALLED-PACKAGE)

- The active root is snapshot 2: `/` has device 41, `/.snapshots/2/snapshot` has device 41 (`raw/0004-filesystem.out`);
  snapshot 1 (`/.snapshots/1/snapshot`, device 76) is the earlier root generation.
- Per member ((not published: orchestration or scratch) → `raw/microos-members.tsv`): 9,469 snapshot-1 files have the same inode,
  ctime (nanoseconds), size, mode, mtime and prefix signature as the active copy, and the active copy is `unchanged`
  against the rpm digest (`package-files.tsv`). Writing to a file changes its ctime (inode(7)), so an equal ctime with
  the verified active copy shows the snapshot copy unchanged. 5,999 files are not longer than 4,096 bytes, so their
  signature is the full sha256; it equals the rpm FILEDIGEST (`raw/0010-package-files-rpm.out`). 837 symlinks have the
  target recorded by rpm (FILELINKTOS). 4,386 directories are in the rpm file list with the recorded mode.
- The active `/etc` is a separate subvolume (`/etc`, device 42, `atomic: snapshot`) and was not traversed: no record
  under `/etc/` in `raw/0004-filesystem.out`. Hence unit definitions, overrides and enablement links of the active
  system are not in the inventory (all 254 microos unit-file rows UNKNOWN) and the `/etc` snapshot row is UNKNOWN.
- Copies outside packages ((not published: orchestration or scratch)): `/home/user/.bashrc` and `.profile` have the full digest of
  `/usr/etc/skel/.bashrc` and `.profile` of package bash; `/boot/grub2/i386-pc/boot.img`, `modinfo.sh` and
  `activate-theme` have the full digest of the packaged originals; the EFI binaries have the size and prefix of the
  packaged shim/grub2 files.
- No ordinary actions were performed on microos (Section 9.2; `D1/in/control/microos/status.jsonl` has only new,
  collector, destroy).

## alma

- Package reasons: `raw/0016-package-reasons-dnf.out` gives `group` for 261 packages; `raw/0018-package-selected-groups-dnf.out`
  lists them as members of `environment:graphical-server-environment` groups.
- npm: `check-inputs-v4/actions/ordinary.sh` runs `npm install --global --prefix "$HOME/.local" cowsay`;
  `D1/in/control/alma/actions-logs/language_program.log` line 52 `added 41 packages`; 40 packages lie in
  `cowsay/node_modules`.
- Unit files ((not published: orchestration or scratch) → `raw/l1-alma-units.tsv`, (not published: orchestration or scratch)): every disputed unit file is
  in a package and `unchanged`; no `/etc` or `/run` unit file or drop-in of the same name except alias links (one
  packaged drop-in directory, `/usr/lib/systemd/system/cups.service.d`).
  Package files were unpacked 05:52–05:54 (ctime), the person's account was written 05:56:18 (`/etc/passwd` ctime),
  the kickstart files 05:56:57. Every `/etc/systemd` enablement or alias link of a disputed row has ctime 05:52:39–
  05:54:22, equal (0–37 s) to its unit file's unpack time: made during package installation.
- sudo: `/etc/sudoers` `unchanged` (`package-files.tsv`); `/etc/sudoers.d/lab-access` in no package, ctime
  05:56:57.
- Accounts/groups ((not published: orchestration or scratch) → `raw/l1-accounts.tsv`): the setup-2.14.5 sources (CentOS Stream lookaside,
  sha512 as in the `sources` file; patch `add-clock-group.patch`) with the password field set to `x` give sha256
  `9e8cdba8…44f5` (group) and `20f397fd…9228` (passwd), equal to the rpm FILEDIGEST of setup-2.14.5-7.el10
  ((not published: over 20 MB)). Copies in (not published: record outside selected evidence).

## void

- npm/pip inside native packages ((not published: orchestration or scratch) → `raw/l1-void-npm.tsv`): all 146 locations' files belong to the
  native package and are `unchanged`.
- pip dependencies: `D1/in/control/void/actions-logs/actions-logs/browser_extension.log`, `Collecting X (from
  marionette_driver)` for all 16.
- base-files 0.146_1: `group` and `passwd` from void-packages (template version 0.146, revision 1) have sha256
  `805a1498…7f6d` and `745770f9…1094`, equal to the xbps file records ((not published: orchestration or scratch) on
  `raw/0012-metadata-read-0.out`).
- runit links (`raw/0004-filesystem.out` under `/etc/runit/runsvdir/default/`): dbus, NetworkManager 11:21:00–01,
  docker 11:21:10, runsvdir-user 11:20:51 (made by `check-inputs-v4/actions/void.sh` lines 84, 101–103, 114); agetty-tty1..6 and
  udevd mtime 11:19:02 (package update); acpid, chronyd, sshd mtime 2025-02-02 (image build); agetty-ttyS0 mtime
  05:49:56 (laboratory preparation).
- sudoers.d `wheel` and `zz-lab`: content in `objects.tsv` access-rule rows; in no package (`package-files.tsv`).
- NetworkManager profiles of the disputed rows exist only under `/run/NetworkManager/system-connections` with
  persistence `runtime`.

## documentation

- systemd.exec(5), PrivateTmp=: "all temporary files created by a service in these directories will be removed after
  the service is stopped" (https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html; copy in
  (not published: downloaded distribution package metadata or sources)). It promises removal of files, not that the directory exists only while
  the computer runs; the directories are on persistent storage, hence RECORD.
