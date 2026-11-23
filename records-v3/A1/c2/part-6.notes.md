# Classification c2, part 6 of A1 — notes

Input: `../in/part-6.tsv` (528 rows; machines debian-desktop and freebsd). Output: `part-6.tsv`.
Script: `scripts/part6_decide.py` (rules below, then a row-by-row table keyed by machine, kind and name).
Hand-check listing: `work/p6-handcheck.txt` (made by `work/p6_sample.py`).

The inventory files named in `evidence` (`raw-X1/freebsd/…`, `raw-X2/debian-desktop/…`) are not present under
`A1/in/raw/`. Every decision therefore rests on the evidence text and on public documentation. No probe was run.

## General reading applied to every row

- A row is one object: the `members` column is 1 everywhere, so no row is a group in the task's sense. MIXED is not
  used. For a directory object, the removal test of S2.2-2 is applied to the whole directory as it stands.
- The count `n=` in the evidence counts every entry of the stored object, directories included. I checked this on the
  same inventory tool's file for another machine (`../in/raw/debian/unowned-groups.json`): `n` equals the number of
  entries, directories included, for all 110 debian stored rows of parts 1–5 (`work/p6_ncheck.py`). Small
  objects such as `n=2` with one sample file are therefore fully visible: one directory plus that file.
- If the visible samples already decide the case, unseen members cannot change it. If they do not decide it and unseen
  members could, the decision is UNKNOWN (S3-2). This applies to `/home/census/.config/libreoffice`,
  `/var/lib/containers`, `/var/lib/flatpak` and `/usr/local/share`.
- A script file is a program that can be started (S2.1-3 “can be started”, S2.2-9 “a program in the home directory”).
  After removal, running it is impossible (S2.2-2), so it is MUST. This applies to the operator's workload scripts, the
  boot loaders in `/boot`, the loader's Forth and Lua code, and nuageinit's saved user-data script.
- A setting whose value is not visible is decided by what the setting does (its kind), not by a guess at its value.
- Readings carried over unchanged from part 5 of this classification:
  - databases whose removal disables a tool are HOLE (S2.2-4 against S2.2-2);
  - marker (stamp) files are HOLE (S2.2-6 against S2.2-1);
  - appearance settings shared by several programs are HOLE (S2.2-7 against S2.2-1);
  - S2.2-7 is not applied when a setting's effect reaches beyond the one program.

## Rules applied by script (each follows from the cited sentences)

| Rule | Applies to | Decision | Sentences | Rows | Hand-checked ids |
|---|---|---|---|---|---|
| A | kind `account` | MUST | S2.2-15 (“accounts … must be recorded”) | 59 | debian-desktop-54a0a0356a, debian-desktop-8d1e409524, debian-desktop-707e10c2e4, debian-desktop-9911292f99, debian-desktop-cbaf0b4232, debian-desktop-54ef0687f4, debian-desktop-8c8f9ffd14, freebsd-8d1e409524, freebsd-9aaab646ac, freebsd-af2a58bec6 |
| P | kind `process` (programs, kernel threads, ps) | MUST | S2.2-9 (“a program that runs on the computer must be recorded regardless of how it was installed”) | 16 | debian-desktop-015af60fe8, debian-desktop-377e7f2465, debian-desktop-89ce5c5668, debian-desktop-d8ee8908a9, freebsd-966dfcae87, freebsd-3f55296154, freebsd-288a960bcc, freebsd-fdd8b25853, freebsd-ca230cdfbe, freebsd-ef537795af |
| V | kind `rc-service` (enabled FreeBSD rc.d services) | MUST | S2.2-10 (code rc runs with root rights), S2.2-2 | 30 | freebsd-03fa3830f7, freebsd-7c164f0a1e, freebsd-c16e56505a, freebsd-cc5f87b39c, freebsd-b3d8fa2ced, freebsd-a2d0ca41e1, freebsd-abfe7e89b1, freebsd-1b3d19b22f, freebsd-8dd0bf7d19, freebsd-348337138d |
| L | stored object under `/var/log/` except `README`, `x2-install-attempt1.sh` and the `.done` markers (decided by row) | NOT | S2.2-6 (records of the past: logs, history) | 35 | debian-desktop-5ce874f910, debian-desktop-93b020b2d3, debian-desktop-6f5cf081f0, debian-desktop-e6b33c3854, debian-desktop-d6ce9987c3, debian-desktop-e24194c06e, freebsd-3f3dc85096, freebsd-3577a2c8c2, freebsd-063e60271f, freebsd-c1a31fd033 |
| C | stored object under `/var/cache/` (except `debconf`, `cups`, `nuageinit`) or under `~/.cache/` | NOT | S2.2-5 (cache) | 18 | debian-desktop-2411908510, debian-desktop-f9d73be5c8, debian-desktop-07086313b7, debian-desktop-320eaf03f3, debian-desktop-1f891ecdc5, debian-desktop-32e4e6f22d, debian-desktop-56f3219102, debian-desktop-df65631681, debian-desktop-c8b4d957fe, debian-desktop-7c5794d4eb |
| B | `/etc/{group,passwd,shadow,gshadow,subuid,subgid}-` backup copies | NOT | S2.2-2, S2.2-6 | 6 | all 6: debian-desktop-d3bb1c2fce, debian-desktop-42b0af3cd4, debian-desktop-c169edc1ca, debian-desktop-9ed4eb3a99, debian-desktop-c1ef82d842, debian-desktop-a2bc9043e2 |
| S | shell startup and logout files (`/etc/profile`, `/etc/csh.*`, `.bashrc`, `.bash_logout`, `.profile`, `.shrc`, `.cshrc`, `.login`) | MUST | S2.2-10 (names shell startup files; code the shell executes) | 18 | debian-desktop-3543b3a205, debian-desktop-3787beb4db, debian-desktop-2d36998dd6, debian-desktop-c15063bcfe, debian-desktop-90017bfd94, debian-desktop-0fbf442b3c, freebsd-ebed2756ae, freebsd-6dfa5e3768, freebsd-edb359c9e6, freebsd-3543b3a205 |
| K | `.ssh` directory whose evidence shows `authorized_keys` | MUST | S2.2-15 (keys used to log in) | 4 | all 4: debian-desktop-c3a3dd6c9b, debian-desktop-351644c1fd, freebsd-c3a3dd6c9b, freebsd-351644c1fd |
| F | FreeBSD `/boot/*.4th`, `/boot/loader.rc`, `/boot/menu.rc`, `/boot/lua` | MUST | S2.2-10, S2.2-13 (code the loader executes, even where it holds settings) | 24 | freebsd-af28845615, freebsd-78668f24af, freebsd-b2efea8f22, freebsd-f44593fb1f, freebsd-340ff3043f, freebsd-e49e910453, freebsd-ea785acc31, freebsd-ba1d1aa9f9, freebsd-0f588fe222, freebsd-505c963e77 |
| G | FreeBSD boot programs in `/boot` (boot0/1/2, gptboot, pmbr, mbr, cdboot, isoboot, pxeboot, zfsboot, loaders, userboot) | MUST | S2.2-9, S2.2-2 (programs started by firmware, the boot prompt, an EFI entry or bhyveload, or written by gpart bootcode) | 28 | freebsd-3620611c7e, freebsd-3df86f4ce3, freebsd-f951e11455, freebsd-afb66c345b, freebsd-28ebab0eba, freebsd-27566e85c2, freebsd-657e4957da, freebsd-f1c6c0762c, freebsd-9d8168bcf2, freebsd-18ae73641c |

Result of the hand check: every checked row fits its rule.
- The accounts are entries of the account database.
- The processes include a Flatpak application (`/app/bin/gnome-calculator`), busybox, init, daemons, getty, the
  kernel threads and `ps`.
- Every rc service checked is listed as enabled in `rc-services.tsv`, and rc runs it as root.
- Every `/var/log` member checked is a log, a journal or a login record.
- Every cache checked is data its program rebuilds: font, shader, GStreamer and babl caches, the browser and mail
  caches, pip, gnome-software, the tracker index, libcanberra sounds, the APT and pkg archives, AppArmor and man
  indexes.
- The account-file backups are shadow-tool copies.
- The startup files are those sh, bash or csh executes.
- Each `.ssh` contains `authorized_keys`.
- The `.4th` and `.rc` files and `lua/` are the loader's own scripts (loader_4th(8), loader_lua(8)).
- The boot files are the boot programs described in boot(8), gptboot(8) and loader(8).

## Facts checked in public sources for row-by-row decisions

- `/etc/X11/default-display-manager` (NOT): on Debian 12, `gdm.service` has no check of this file. Its Debian patch
  removes the display-manager alias, and the link `display-manager.service` selects the manager.
  Source: https://sources.debian.org/data/main/g/gdm3/43.0-3/debian/patches/92_systemd_unit.patch
- `/var/lib/gdm3` (NOT): the unit's `ExecStartPre=/usr/share/gdm/generate-config` recompiles
  `greeter-dconf-defaults` before every start. Source: https://sources.debian.org/data/main/g/gdm3/43.0-3/debian/generate-config
- `/var/cache/cups` (MUST): Debian 12 `cups.path` has `PathExists=@CUPS_CACHEDIR@/org.cups.cupsd`, so the
  `org.cups.cupsd` member makes systemd start cupsd. It is not cache.
  Source: https://sources.debian.org/data/main/c/cups/2.4.2-3+deb12u9/scheduler/cups.path.in
- `/var/cache/nuageinit` (MUST): a user-data script is copied to `/var/cache/nuageinit/user_data`, and a firstboot rc
  script executes it. Sources: https://man.freebsd.org/nuageinit/7 and the stable/14 commit announced on
  lists.freebsd.org, dev-commits-src-branches, June 2025.
- `/var/db/mergemaster.mtree` (UNKNOWN): mergemaster was removed from the tree for FreeBSD 15. The evidence does not
  fix the release, so it is not established whether anything reads the file.
  Source: https://lists.freebsd.org/archives/dev-commits-src-all/2024-July/043328.html
- `/etc/termcap` (MUST): the terminal library tries `/etc/termcap.db`, then falls back to the text file
  `/etc/termcap`. Source: https://lists.freebsd.org/archives/freebsd-current/2024-May/005908.html
- `/var/lib/python` (NOT): the python3.11 maintainer scripts only delete `python3.11_installed`.
  Source: https://sources.debian.org/src/python3.11/3.11.2-6%2Bdeb12u6/debian/PVER-minimal.postrm.in
- `xdg-terminals.list` (UNKNOWN): only xdg-terminal-exec reads it, and whether that program is installed here is not
  established. Source: https://man.archlinux.org/man/xdg-terminal-exec.1.en
- `/etc/dictionaries-common` (UNKNOWN): written by update-default-ispell. Which installed program reads it is not
  documented in the sources found. Source: https://manpages.debian.org/bookworm/dictionaries-common/update-default-ispell.8.en.html
- `/boot/entropy` (NOT): the loader passes the saved entropy to the kernel early in boot; random(4) says it is saved
  so that the random device is usable early. Without it the kernel gathers entropy itself.

## Rows that are HOLE (17) and what the text lacks

- Databases whose removal disables a tool: `/var/lib/apt`, `/var/lib/dpkg`, `/var/lib/pam`, `/var/lib/shells.state`,
  `/var/lib/ucf`, `/var/cache/debconf` (debian-desktop), and `/var/db/pkg`, `/var/db/etcupdate` (freebsd). S2.2-4
  exempts “the contents of databases”, but its own justification is false here. S2.2-2 then gives must, and no
  sentence says which prevails.
- Marker files: `.gsd-keyboard.settings-ported`, `gnome-settings-daemon/input-sources-converted`,
  `.sudo_as_admin_successful`, `.local/share/gnome-shell`, `.local/share/nautilus`, and `/var/spool/lock`
  (freebsd). S2.2-6 counts them as records of the past; S2.2-1 counts what behaviour depends on.
- Appearance shared by several programs: `/etc/fonts` (fontconfig rules) and `/boot/fonts` (loader and vt console
  fonts). S2.2-7 exempts only settings of one program, and the text does not say whether appearance is behaviour.
- `/etc/libreoffice`: one program's own configuration data (S2.2-7, need not), without which parts of that program
  stop working (S2.2-2, must).
