# c2, part 4: notes

Input: `../in/part-4.tsv`, 1143 rows, all from the Guix machine. Output: `part-4.tsv`.
Script: `raw/rules_part4.py` (rules, then the row-by-row table `ROWS`). Trace of which rule decided each
row: `raw/rule-trace.tsv`. Check script: `raw/verify_part4.py`. Group members were read with
`raw/peek_groups.py` from `../in/raw/guix/unowned-groups.json` and `directory-only-groups.json`.

## Sources used for what objects do

- Guix manual, Derivations: "References are the set of run-time dependencies of the build results."
  https://guix.gnu.org/manual/en/html_node/Derivations.html. Every system-closure object is therefore a
  run-time dependency of the current system (closure = transitive references, Invoking guix gc page).
- Guix source `gnu/system/pam.scm`: pam.d is `(computed-file "pam.d" …)` holding one file per service,
  `(symlink file (string-append #$output "/" name))`. The service names include "other", "passwd",
  "chfn", "sudo", "su", "useradd" … https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/system/pam.scm
- Guix source `gnu/services/base.scm`: `%default-console-font` is
  `#+font-gnu-unifont:psf "/share/consolefonts/Unifont-APL8x16.psf.gz"`.
- Guix source `gnu/services/xorg.scm`: `%default-xorg-fonts` lists font-alias, font-misc-misc
  ("default fonts for xterm") and font-adobe75dpi directories.
- Guix source `gnu/services/sound.scm`: `client-conf` default `'()`, `daemon-conf` default
  `'((flat-volumes . no))`, and /etc/pulse holds default.pa (from `script-file`), system.pa, daemon.conf
  and client.conf.
- The machine's configuration: `in/raw/guix/configuration/etc/config.scm` and `…/home/guest/home.scm`.

Not reached: the Guile manual (connection reset). So it is not established whether guix reads its
`.scm` sources at run time. Rule R-GUIXSRC gives UNKNOWN for this reason.

## Rules (homogeneous kinds). Each follows from the cited sentences

| Rule | Applies to | Decision | Sentences | Why |
|---|---|---|---|---|
| R-PKG | versioned package outputs in the system closure that no rule below takes (542) | MUST | S2.2-1, S2.2-2, S2.2-9, S2.2-10 | run-time dependency. Removing it stops the programs that use it, or its own programs can no longer start |
| R-SHEP | `shepherd-*.scm/.go`, `shepherd.conf` (109) | MUST | S2.2-10, S2.2-13 | code that shepherd (PID 1) runs with its own rights |
| R-CODE | `activate*.scm`, `boot`, `module-import*`, `raw-initrd` (37) | MUST | S2.2-10, S2.2-13 | Guile code that activation and boot run as root |
| R-SYSDIR | `system`, `etc`, `profile`, `parameters` (7) | MUST | S2.2-1, S2.2-2, S2.2-9 | the system reaches its programs and configuration through them |
| R-SCRIPT | wrappers and scripts (xinitrc, startx, *-wrapper, bashrc, aliases.sh, modprobe …) (20) | MUST | S2.2-10, S2.2-13 | executable code |
| R-GUIXMOD | guix command and daemon module trees and union (17) | MUST | S2.2-2, S2.2-9, S2.2-10 | guix loads them as code. Without them guix commands are impossible |
| R-GUIXSRC | `guix-*-source` (6) | UNKNOWN | S3-1, S3-2 | run-time use not established |
| R-PAM | PAM service files and pam.d (19) | MUST | S2.2-15, S2.2-2 | they decide password login and becoming superuser |
| R-DATA | data read as values by many programs: tzdata, certificates, locales, keyboard data, MIME and GSettings data, loaders/IM lists, module DB, hwdb, net-base (24) | MUST | S2.2-1, S2.2-2, S2.2-13 | a setting that is not confined to one program. Removal makes functions impossible |
| R-SYSCONF | system-wide configuration (nsswitch, hosts, environment, login.defs, sysctl, asound, shells, fstab, nscd.conf, udev rules, skel) (15) | MUST | S2.2-1, S2.2-2, S2.2-13 | read by many programs, so S2.2-7 does not apply |
| R-ONECONF | configuration read by one daemon only (dhcpcd, ntpd, pulseaudio daemon.conf, dbus, elogind, upower, geoclue, Xorg, slim, guix acl) (14) | HOLE | S2.2-7 vs S2.2-2 | see question Q1 |
| R-THEME | icon/GTK themes, sound theme, desktop and console fonts, iso-codes, guix-icons (11) | HOLE | S2.2-4, S2.2-7, S2.2-2 | see question Q2 |
| R-HEADERS | vulkan-headers, xorgproto, util-macros, wayland-protocols (4) | MUST | S2.2-2 | gcc and pkg-config are in the system. Removal makes compiling against them impossible |
| R-KMOD | loaded kernel modules (70) | MUST | S2.2-10, S2.2-2 | the kernel runs them with its own rights |
| R-SERVICE | shepherd services from herd status (56) | MUST | S2.1-3, S2.2-1, S2.2-2 | an enabled service is in force. Removal stops what it does |
| R-PROC | running processes (33) | MUST | S2.2-9 | running program |
| R-ACCT | accounts (11) | MUST | S2.2-15 | accounts |

There are also small exact-name rules, each listed in the script with its sentences:
- MUST: sudoers, sshd_config, authorized keys (S2.2-15); polkit rules (S2.2-10, S2.2-13, S2.2-15); avahi-daemon.conf (open port, S2.2-15); /etc/pulse (default.pa script, S2.2-13).
- NOT: documents (S2.2-4); caches (S2.2-5); provenance and configuration copies (S2.2-6); motd, issue and backgrounds (S2.2-4); themes used inside one program (S2.2-7); guix message catalogs (S2.2-7); emacs-subdirs (no Emacs installed); client.conf (empty by default).
- UNKNOWN: hostname, timezone and os-release files (no program shown to read them); X core fonts (whether "fixed" is fatal is not confirmed); firmware dir (contents not inventoried); guile-launcher.c.

### Rows checked by hand (10 per rule; all rows where a rule has fewer than 10)

I read the name of every row covered by every rule (full list in `raw/rule-trace.tsv`). For each rule, the
first 10 rows are listed in `raw/rule-samples.md`. For the five largest rules:

- R-PKG: guix-0d48c6bf44, guix-18b042cc42, guix-173608568b, guix-e02c6d27c9, guix-fbf59e700f, guix-6f86d03666, guix-944d419b5c, guix-9a814c7a91, guix-c8d1d95195, guix-d862ac9682
- R-KMOD: guix-7fdc5c58fa, guix-ecd1d0957d, guix-cd486effed, guix-96c2a6c092, guix-ddb5a87d9a, guix-baeebd18d2, guix-13fab1e09e, guix-519f0efa4c, guix-145a20b523, guix-3cd1d09ac0
- R-SERVICE: guix-c7e5f38d94, guix-a5fb612d86, guix-99b95ecba6, guix-d968cf24a8, guix-9eb7d7527b, guix-8199876f9a, guix-d5354a6cef, guix-a6ab41631c, guix-028034d635, guix-881cf8472f
- R-PROC: guix-c260909efc, guix-d4c0f6937e, guix-8dd6185781, guix-3d247384aa, guix-06cf17ff41, guix-83de6c2f7f, guix-270c5e4acc, guix-92bd9a5073, guix-63186abb2b, guix-a53c13b3d7
- R-ACCT: guix-ebda0cbba2, guix-c23681be3a, guix-27d89cb149, guix-e9ecf34b23, guix-6a022e8f54, guix-9911292f99, guix-af2a58bec6, guix-829a5eaf21, guix-1f9ebd3eec, guix-cbaf0b4232

The hand check found three problems, and each was fixed in the rules before the final run:
- `polkit-1` looked like a versioned package but is a PAM service file. It moved to R-PAM.
- Header packages would have been given the "programs or libraries" wording. They got their own rule, R-HEADERS.
- `guix-icons` is an icon set. It moved to R-THEME.

## Row-by-row decisions

Every `stored` row, the store groups, the user-profile rows, the build-user group, the directory
skeleton, `kernel threads` and `ps` were decided one by one (table `ROWS` in the script). Program state
that the system writes at run time (sockets, locks, leases, cookies, store DB, GC roots, random seed,
resolv.conf, machine-id) gets NOT under S2.5-1/S2.5-2. COMMON says Section 2.5 matters are not holes.

## Questions only the author can decide (readings, not decided here)

- Q1 (S2.2-7 vs S2.2-2): is the configuration of a daemon that only that daemon reads "in force only inside
  one program" (then NOT), or does it count because its effect reaches the whole computer (network address,
  clock, sessions, bus policy) (then MUST)?
- Q2 (S2.2-4, S2.2-7, S2.2-2): fonts, icon and GTK themes, and sounds used by many programs are neither content
  nor a setting of one program. Does a change of appearance after removal count as "the computer stops
  doing something"?
- Q3 (S2.1-1, S2.2-2): must the files of the declaration itself (config.scm, home.scm) be recorded in the declaration?
- Q4 (S2.2-14, S2.2-15, S2.2-2): SSH host keys and the guix signing key behave like passwords (changing them
  leaves behaviour the same), but removing them stops something. Host keys also take part in SSH login, yet
  they are not keys "to log in to an account".
- Q5 (S2.2-7, S2.2-13): is a command line that a program runs on request (Thunar custom actions, panel
  launchers, keyboard-shortcut commands) a file executed as code?

## MIXED rows: which members get which decision

- guix-da5f01a3ef: NOT for `.drv`, `-builder`, source tarballs, patches and `.links`, because removal changes nothing and they can be rebuilt (S2.2-1, S2.2-2, S2.2-5). NOT for the closure of system generation 1 (S2.5-1). User-profile and Home items are decided in their own rows.
- guix-25ad6943ae: MUST for home, activate, on-first-login, setup-environment, update-symlinks, shell-profile, module-import*, profile, fonts.conf and guix. NOT for w1-declared-note (S2.2-4), configuration.scm and provenance (S2.2-6).
- guix-76634f69cd: MUST for grub.cfg, grubenv and the i386-pc modules (S2.2-16, S2.2-10). NOT for fonts and locale (S2.2-7).
- guix-c7553146ab: HOLE for the signing key pair (Q4) and for acl (Q1).
- guix-0075a76d48: MUST for authorized_keys.d (S2.2-15). HOLE for the host keys (Q4).
- guix-7bc12ec287: NOT for desktop accels and icons, thunar.xml, xfwm4.xml, xfce4-notifyd.xml, xfce4-panel.xml, xsettings.xml and displays.xml (S2.2-7). HOLE for the panel launcher .desktop files and xfce4-keyboard-shortcuts.xml (Q5).
- guix-64f62c6553: NOT for cache, state and run directories (S2.2-5, S2.5-1). NOT for empty user directories (S2.2-4). UNKNOWN for /var/empty, /var/log and the parent directories, because what stops without them is not established.
