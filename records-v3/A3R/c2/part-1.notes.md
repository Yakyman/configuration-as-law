# Classification c2 of `A3R` part 1 — notes

Input: (not published: outside selected checks and direct evidence) (5212 rows, machine `lived`). Output: `part-1.tsv` (one row per input id).
Per-member breakdown of every directory and subtree row: `part-1.members.tsv` (row id, decision, leaf rule,
number of member files, up to three example paths). Scripts: `(not published: external working record)` (`build_index.py bin raw/index.pkl` builds the file index from the inventory, `decide.py` decides all rows,
`sanitize.py` replaces quoted path segments naming software products by `<name>` (publication rule), `verify.py` checks the output:
`python3 -I bin/decide.py bin part-1.tsv <breakdown>`). Documentation lookups: `raw/doc-generated-files.md`,
`raw/doc-groups.md`, `raw/doc-flatpak-runtimes.md`. Nothing was removed anywhere; every removal test below is applied by
reasoning from what the object does (S3-1). Only Section 2.2 and S3-1/S3-2 decide; other sentences are cited only where
they define a word used by 2.2 (S2.1-3 “in force”).

## Readings applied everywhere (from the text, not added to it)

1. **Removal test, literally (S2.2-1, S2.2-2).** An object must be recorded when, after its removal, the computer stops
   doing something or something becomes impossible. “Something” is taken as something beyond the object itself; otherwise
   every file would pass the test and S2.2-4 would be empty. An object whose removal changes nothing (a comment-only file,
   a backup copy, an empty directory, a stale lock, a file used only by an absent program) is therefore not required: the
   text requires only what 2.2 names, so such an object is decided NOT with S2.2-1, S2.2-2.
2. **Exemptions apply only when their own explanation fits.** S2.2-4 (content), S2.2-5 (cache), S2.2-6 (records), S2.2-7
   (setting in force only inside one program) are used only when the clause after the colon is true for the object.
   A file named “cache” whose removal breaks a function (e.g. `loaders.cache`, `mimeinfo.cache`, `gschemas.compiled`,
   the man index, the APT lists) is not a cache in the sense of S2.2-5 and gets MUST by S2.2-2 (evidence:
   `raw/doc-generated-files.md`). A key or keyring is not content: after removal the computer cannot decrypt, sign or
   authenticate (S2.2-2).
3. **Code (S2.2-10, S2.2-13).** A file an interpreter executes with its own rights is code that must be recorded; the
   condition of S2.2-10 is about rights, not about whether the code is running at the moment of inventory (S2.1-3: in force
   = runs or can be started). Hence every script, plugin, theme, editor package and installed language package is MUST,
   including oh-my-zsh plugins not listed in `.zshrc`, test scripts, and scripts written for another platform. Source a
   compiler only reads (C, Java, Go, Rust, C#) is not executed (S2.2-13) and is the user's work: NOT by S2.2-4.
   Documentation inside program trees (README, licences, changelogs, man pages, `doc/`) is NOT by S2.2-4.
4. **Settings (S2.2-7, S2.2-13).** A file read as values is a setting; it is NOT when in force only inside one program
   (browser profile — the example of S2.2-7 —, VS Code, Zotero, Obsidian, KeePassXC, LibreOffice, Thunar, xfwm4, panel,
   desktop, PulseAudio state, `.curlrc`, `.wgetrc`, global git ignore files). A setting read by the system or several
   programs (`/etc` configuration, `dconf`, `user-dirs`, `.inputrc`, `.editorconfig`, keyboard/display/xsettings
   channels) is MUST by S2.2-1/S2.2-2.
5. **Runtime state.** Sockets, pid files, udev and systemd runtime databases, X authority files: a running program uses
   them and their removal breaks it now. 2.2 offers no exemption for them (they are not cache, record or content), so
   they are MUST by S2.2-2. Logs under `/run` stay NOT (S2.2-6).
6. **Directory rows.** A `stored-outside-packages` row stands for its listed members; a member that is a directory stands
   for every inventoried file under it (removing it removes them). Leaves are classified with the leaf rules below; the row
   gets the common decision of its leaves, or MIXED, with the split in `part-1.members.tsv`. A `…:subtree` row is decided
   the same way from all inventoried files under its prefix ((not published: outside selected checks and direct evidence), level 2, plus the
   file-type listing (not published: external working record)).

## Kind rules (applied by (not published: orchestration and working notes))

| Kind | Decision | Sentences | Rule |
|---|---|---|---|
| account | MUST | S2.2-15 | accounts must be recorded |
| group | per group | S2.2-1, S2.2-2, S2.2-15 | table (not published: orchestration and working notes) from `raw/doc-groups.md`: MUST when removal stops a program, a udev/tmpfiles rule or a member's access (sudo: S2.2-15); NOT for floppy, clock (nothing references them); HOLE when the only documented effect is a failed `pwck` check for an account whose primary group it is; UNKNOWN when documentation names no consumer (fax, voice, dip, operator, src, sasl, staff, users, pulse-access) or the group works only by numeric GID (shadow, _ssh) |
| process | MUST | S2.2-9 (+S2.2-12 for container processes) | a running program |
| port | MUST | S2.2-15 | listening socket |
| driver | MUST | S2.2-1, S2.2-2 | kernel code bound to a device; unbinding makes the device unusable |
| firewall-table/chain/rule | MUST | S2.2-15 | firewall rules (tables and chains hold them) |
| polkit-actions | MUST | S2.2-1, S2.2-2, S2.2-15 | action definition with default authorizations; polkit refuses unknown actions |
| service, user-service | MUST if loaded; NOT if `not-found` | S2.1-3, S2.2-9 / S2.2-1, S2.2-2 | a `not-found` unit has no file, cannot run or be enabled |
| unit-file, user-unit-file | MUST | S2.1-3, S2.2-1, S2.2-2 | defines, generates or masks a startable unit |
| timer (logrotate.timer) | NOT | S2.2-1, S2.2-2 | no unit file, logrotate absent (`records-v3/A3R/in/raw/lived/raw/073-service.out:41`) |
| user-timer, cron | MUST | S2.2-1, S2.2-2, S2.2-10 | scheduled job |
| container, container-image | MUST | S2.2-9, S2.2-12 | programs in containers |
| package:flatpak | apps and runtimes MUST; `.Locale` NOT | S2.2-9, S2.2-2 / S2.2-4 | runtimes 49 and 50 are each required by one app (`raw/doc-flatpak-runtimes.md`); locale extensions are translations |
| package:pipx, package:cargo, package:go (hey and its linked modules) | MUST | S2.2-9 | programs in the home directory |
| package:go (go.mod in module cache) | NOT | S2.2-5 | module cache |
| package:cargo-record | MUST | S2.2-1, S2.2-2 | cargo's present install record; uninstall depends on it |
| package:npm, python-distribution | MUST | S2.2-10, S2.2-2 (S2.2-9 for VS Code bundles) | installed language packages executed by the interpreter |
| login-key | MUST | S2.2-15 | |
| saved-network | MUST | S2.2-14 (Wi-Fi); S2.2-1, S2.2-2 (WireGuard) | |
| network (NetworkManager profiles) | MUST | S2.2-14 / S2.2-1, S2.2-2 | |
| network-link | podman0, veth0 MUST; lo, ens3, ens4 HOLE | S2.2-1, S2.2-16 | see holes |
| access-rule: sudo, sudoers, PAM, polkit rules | MUST | S2.2-15, S2.2-1, S2.2-2 | rights and login rules |
| access-rule: comment-only files (`sudoers.d/README`, `security/access.conf`) | NOT | S2.2-1, S2.2-2 | nothing in force from them |
| access-rule: sshd values | port, listenaddress, addressfamily, passwordauthentication, kbdinteractiveauthentication, permitemptypasswords, permitrootlogin, authorizedkeysfile MUST (S2.2-15); logging/banner/transport values NOT (S2.2-7); all other values HOLE | | see holes |

## Leaf rules for files (applied by (not published: orchestration and working notes), (not published: orchestration and working notes); first matching rule wins)

| Leaf rule | Decision | Sentences | Matches | Files |
|---|---|---|---|---:|
| H_CODECACHE | HOLE | S2.2-5,S2.2-10,S2.2-13 | __pycache__/*.pyc, *.elc, eln-cache, nvim luac cache, *.zwc | 2733 |
| H_EMBEDDEDCMD | HOLE | S2.2-7,S2.2-10,S2.2-13 | ~/.gitconfig, ~/.ssh/config, Thunar uca.xml, xfce4 keyboard shortcuts | 4 |
| H_STAMP | HOLE | S2.2-2,S2.2-6 | systemd timer stamps, /etc/.updated, /var/.updated | 10 |
| R_CLOCK | HOLE | S2.2-2,S2.2-6 | timestamp of last NTP sync, used as clock floor at boot (https://manpages.debian.org/trixie/systemd-timesyncd/systemd-timesyncd.service.8.en.html) | 1 |
| R_NMTIMESTAMPS | HOLE | S2.2-2,S2.2-6 | last successful activation time of each connection (https://manpages.debian.org/trixie/network-manager/nm-settings-nmcli.5.en.html) | 1 |
| ACCESS | MUST | S2.2-15 | passwd/group/shadow/subuid/subgid, sudoers, PAM, polkit rules, Xwrapper, authorized_keys | 17 |
| AUTOSTART | MUST | S2.2-1,S2.2-2 | autostart, menu and panel launchers, native-messaging manifest, Flatpak exports | 15 |
| BOOT | MUST | S2.2-16,S2.2-2 | /boot (except locale/fonts), /etc/default/grub.d, /etc/grub.d, initramfs-tools | 591 |
| CLOUDSTATE | MUST | S2.2-1,S2.2-2 | cloud-init instance state and semaphores (https://cloudinit.readthedocs.io/en/latest/reference/modules.html) | 30 |
| CODE | MUST | S2.2-10,S2.2-13 | scripts (*.sh, *.py, *.js, *.lua, *.zsh, …), executable files in projects, oh-my-zsh, nvm scripts and tests, .screenrc, .tmux.conf, .gdbinit, dotfile copies | 1931 |
| CONTAINER | MUST | S2.2-9,S2.2-12 | container storage and container configuration | 320 |
| CRON | MUST | S2.2-1,S2.2-2,S2.2-10 | user crontab: commands cron runs on schedule | 1 |
| DPKGSCRIPT | MUST | S2.2-10,S2.2-13 | package maintainer script dpkg executes as root (https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html) | 808 |
| EDITORCODE | MUST | S2.2-10 | ~/.emacs.d (Prelude, ELPA), ~/.config/nvim, Neovim plugins, vim files | 3839 |
| FIREWALL | MUST | S2.2-15 | /etc/nftables.d | 1 |
| KEY | MUST | S2.2-1,S2.2-2 | SSH host and user keys, GnuPG keys and keyrings, TLS keys/certificates, WireGuard key, NSS db, apt keyrings, NetworkManager secret_key | 34 |
| MOUNTPOINT | MUST | S2.2-1,S2.2-2 | mount point of a tmpfs file system from fstab | 1 |
| MULTISET | MUST | S2.2-1,S2.2-2 | settings read by several programs (dconf, user-dirs, inputrc, editorconfig, keyboard/display/xsettings) | 10 |
| NETCONF | MUST | S2.2-14,S2.2-1,S2.2-2 | NetworkManager/netplan/ppp profiles, hosts, hostname, resolv.conf, nsswitch | 17 |
| PKGCODE | MUST | S2.2-10,S2.2-2 | node_modules, site-packages/dist-packages, venvs, pipx, rustup toolchain, ~/.cargo/bin, ~/go/bin, jupyter kernel | 891 |
| PROGRAM | MUST | S2.2-9,S2.2-2 | files inside /opt programs, AppImage, Zotero, VS Code extensions, Neovim plugin data, node toolchain, Flatpak deployments, /usr/lib/cups/backend | 19325 |
| RUNSTATE | MUST | S2.2-1,S2.2-2 | /run, /tmp, /var/tmp runtime objects, X authority files | 676 |
| R_APTLISTS | MUST | S2.2-1,S2.2-2 | APT package index lists (https://manpages.debian.org/trixie/apt/apt-get.8.en.html) | 18 |
| R_CATALOG | MUST | S2.2-1,S2.2-2 | SGML/XML catalog registry (https://manpages.debian.org/trixie/xml-core/update-xmlcatalog.8.en.html) | 4 |
| R_CATALOGDB | MUST | S2.2-1,S2.2-2 | journal message catalog index (https://manpages.debian.org/trixie/systemd/journalctl.1.en.html) | 1 |
| R_DICTCOMMON | MUST | S2.2-1,S2.2-2 | generated dictionary lists for editors and spell checkers (https://sources.debian.org/src/dictionaries-common/1.30.10/policy/dsdt-policy.xml.in/) | 9 |
| R_DPKGDB | MUST | S2.2-1,S2.2-2 | dpkg database of installed packages (https://manpages.debian.org/trixie/dpkg/dpkg.1.en.html) | 5257 |
| R_DSH | MUST | S2.2-1,S2.2-2 | deb-systemd-helper enablement state (https://manpages.debian.org/trixie/init-system-helpers/deb-systemd-helper.1p.en.html) | 142 |
| R_GSCHEMA | MUST | S2.2-1,S2.2-2 | compiled GSettings schemas (https://docs.gtk.org/gio/class.Settings.html) | 1 |
| R_HWDB | MUST | S2.2-1,S2.2-2 | compiled udev hardware database (https://manpages.debian.org/trixie/udev/hwdb.7.en.html) | 1 |
| R_IMMOD | MUST | S2.2-1,S2.2-2 | GTK 3 input-method module index (https://manpages.debian.org/trixie/libgtk-3-bin/gtk-query-immodules-3.0.1.en.html) | 1 |
| R_INFODIR | MUST | S2.2-1,S2.2-2 | Info directory node (https://www.gnu.org/software/texinfo/manual/info-stnd/html_node/Invoking-Info.html) | 1 |
| R_LDSOCACHE | MUST | S2.2-1,S2.2-2 | dynamic linker cache (https://manpages.debian.org/trixie/manpages/ld.so.8.en.html) | 1 |
| R_LINGER | MUST | S2.2-1,S2.2-2 | linger flag: start user manager at boot (https://manpages.debian.org/trixie/systemd/loginctl.1.en.html) | 1 |
| R_LOCALE | MUST | S2.2-1,S2.2-2 | compiled locale archive (https://manpages.debian.org/trixie/locales/locale-gen.8.en.html) | 1 |
| R_MACHINEID | MUST | S2.2-1,S2.2-2 | D-Bus machine ID (fallback for machine-id) (https://manpages.debian.org/trixie/systemd/machine-id.5.en.html) | 1 |
| R_MANDB | MUST | S2.2-1,S2.2-2 | man-db auto-update flag (https://sources.debian.org/src/man-db/2.13.1-1/debian/postinst/) | 1 |
| R_MANINDEX | MUST | S2.2-1,S2.2-2 | man-db index for apropos/whatis (https://manpages.debian.org/trixie/man-db/apropos.1.en.html) | 26 |
| R_MIME | MUST | S2.2-1,S2.2-2 | shared MIME-info database (https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html) | 930 |
| R_MIMEINFO | MUST | S2.2-1,S2.2-2 | desktop MIME-handler index (https://manpages.debian.org/trixie/desktop-file-utils/update-desktop-database.1.en.html) | 1 |
| R_MODULESDEP | MUST | S2.2-1,S2.2-2 | kernel module dependency and alias index (https://manpages.debian.org/trixie/kmod/modprobe.8.en.html) | 22 |
| R_OSTREE | MUST | S2.2-9,S2.2-2 | Flatpak OSTree objects: the files of installed apps and runtimes (https://docs.flatpak.org/en/latest/under-the-hood.html) | 23369 |
| R_PIXBUF | MUST | S2.2-1,S2.2-2 | gdk-pixbuf loader index (https://manpages.debian.org/trixie/libgdk-pixbuf2.0-bin/gdk-pixbuf-query-loaders.1.en.html) | 1 |
| R_SHELLS | MUST | S2.2-1,S2.2-2 | update-shells state (https://manpages.debian.org/trixie/debianutils/update-shells.8.en.html) | 1 |
| R_UCF | MUST | S2.2-1,S2.2-2 | ucf conffile checksums and registry (https://manpages.debian.org/trixie/ucf/ucf.1.en.html) | 7 |
| SHELLRC | MUST | S2.2-10 | ~/.bashrc, .profile, .zshrc, .zshenv, .aliases, .functions, .exports, .bash_prompt, /etc/profile, ~/.cargo/env | 14 |
| STATE | MUST | S2.2-1,S2.2-2 | state a system program acts on (apt extended_states, flatpak refs/config, emacsen-common, colord, netdata identity) | 57 |
| SWAP | MUST | S2.2-1,S2.2-2 | swap file activated from fstab | 1 |
| SYSCONF | MUST | S2.2-1,S2.2-2 | /etc files read by the system or several programs, netdata configuration, exim generated config, ghostscript font map, X font indexes | 73 |
| TOOLCODE | MUST | S2.2-10,S2.2-13 | Makefile, CMake, Dockerfile, compose, package.json in projects | 141 |
| UNIT | MUST | S2.1-3,S2.2-1,S2.2-2 | systemd units, wants links, tmpfiles.d, generated units, transient units | 64 |
| APPSET | NOT | S2.2-7,S2.2-13 | per-program settings/state: VS Code, Obsidian, Zotero profile, LibreOffice, KeePassXC, Thunar, pulse, go telemetry config, ~/.var/app data, nvim state, single-program dotfiles | 276 |
| BROWSER | NOT | S2.2-7,S2.2-11 | Firefox profile, Firefox policies | 190 |
| CACHE | NOT | S2.2-5 | ~/.cache, /var/cache (except below), browser-engine cache dirs, npm _cacache, cargo registry, Go module cache, buildah cache, oh-my-zsh cache, apt archives/pkgcache, fontconfig, apparmor, cups, debconf (docs call it a cache) | 8817 |
| COMPILEDSRC | NOT | S2.2-4,S2.2-13 | C/C++/Java/C#/Go/Rust sources in projects | 131 |
| CONFINEDCODE | NOT | S2.2-11 | Zotero translators (run inside Zotero), downloaded VM disk image | 753 |
| CONTENT | NOT | S2.2-4 | Documents, Downloads, PDF, mail and print spools, Zotero library database, container volumes, non-code project files | 234 |
| DOC | NOT | S2.2-4 | README/LICENSE/CHANGELOG-type names, *.md/*.txt/images/fonts outside program trees, man/doc directories | 1972 |
| DPKGLOCK | NOT | S2.2-1,S2.2-2 | dpkg lock file, held only while dpkg runs (https://man7.org/linux/man-pages/man1/dpkg.1.html) | 4 |
| DPKGLOCK_FP | NOT | S2.2-1,S2.2-2 | lock file of the Flatpak repository | 1 |
| EMPTYDIR | NOT | S2.2-1,S2.2-2 | empty directory no program needs | 72 |
| FOREIGN | NOT | S2.2-1,S2.2-2 | .github, .devcontainer, CI files, macOS/Sublime files (scripts among them go to CODE) | 434 |
| GIT | NOT | S2.2-4,S2.2-6 | .git directories (objects, refs, index, logs, config) | 936 |
| GITSAMPLE | NOT | S2.2-1,S2.2-2 | .git/hooks/*.sample | 574 |
| INERT | NOT | S2.2-1,S2.2-2 | *.old, *-old, *~, backups (passwd- etc.), .gitkeep, stale locks, comment-only stubs, convenience symlinks | 90 |
| LOG | NOT | S2.2-6 | /var/log, /run/log, *.log, _logs/, logs/, shell/python histories, recentf, savehist, wtmp, crash reports, go telemetry counts | 186 |
| NETDATA_METRICS | NOT | S2.2-4,S2.2-6 | netdata metrics database: collected history of measurements (https://learn.netdata.cloud/docs/netdata-agent/database) | 20 |
| NETSECRET | NOT | S2.2-14 | PPP secrets files | 2 |
| NOLOGROTATE | NOT | S2.2-1,S2.2-2 | logrotate rule file; logrotate is not installed (raw:records-v3/A3R/in/raw/lived/raw/073-service.out) | 2 |
| R_GIOMOD | NOT | S2.2-5 | GIO module index (https://manpages.debian.org/trixie/libglib2.0-bin/gio-querymodules.1.en.html) | 2 |
| R_ICONCACHE | NOT | S2.2-5 | icon theme cache (https://manpages.debian.org/trixie/gtk-update-icon-cache/gtk-update-icon-cache.1.en.html) | 5 |
| R_NMBSSIDS | NOT | S2.2-6 | access points seen before (https://manpages.debian.org/trixie/network-manager/nm-settings-nmcli.5.en.html) | 1 |
| R_NMLEASE | NOT | S2.2-6 | previous DHCP lease of an interface (https://manpages.debian.org/trixie/network-manager/nm-settings-nmcli.5.en.html) | 1 |
| R_PYINST | NOT | S2.2-6 | marker of a first Python runtime install (https://sources.debian.org/src/python3.13/3.13.5-2+deb13u5/debian/PVER-minimal.preinst.in/) | 1 |
| R_SEED | NOT | S2.2-1,S2.2-2 | saved random seed (https://manpages.debian.org/trixie/systemd/systemd-random-seed.service.8.en.html) | 1 |
| R_SUMDB | NOT | S2.2-6 | Go checksum database tree head seen last (https://go.googlesource.com/proposal/+/master/design/25530-sumdb.md) | 1 |
| SECRETDATA | NOT | S2.2-4,S2.2-14,S2.2-15 | pass store entries | 1 |
| TRANSLATION | NOT | S2.2-4 | translation catalog or locale extension of a program | 12 |
| R_ACCOUNTSSVC | UNKNOWN | S3-1,S3-2 | AccountsService per-user record (https://gitlab.freedesktop.org/accountsservice/accountsservice/-/blob/main/data/org.freedesktop.Accounts.User.xml) | 1 |
| R_NMSTATE | UNKNOWN | S3-1,S3-2 | NetworkManager persistent state file (https://manpages.debian.org/trixie/network-manager/NetworkManager.8.en.html) | 1 |
| R_PAMSTATE | UNKNOWN | S3-1,S3-2 | pam-auth-update state files (https://manpages.debian.org/trixie/libpam-runtime/pam-auth-update.8.en.html) | 6 |
| R_UNDOC | UNKNOWN | S3-1,S3-2 | generated file without documented consumer | 15 |
| UNKNOWN | UNKNOWN | S3-1,S3-2 | not established | 4 |
| UNKNOWN_APPARMOR | UNKNOWN | S3-1,S3-2 | local AppArmor include; content not in inventory | 14 |

## Holes found (what the text lacks)

- **H1 — compiled/byte-code caches of executed code** (`__pycache__/*.pyc`, Emacs `*.elc` and `eln-cache`, Neovim
  `luac` cache, zsh `*.zwc`; 43 rows HOLE, many MIXED rows contain them): S2.2-5 says cache need not be recorded and
  documentation confirms these are regenerated (`raw/doc-generated-files.md` items 21–23); S2.2-10/S2.2-13 say a file a
  program executes as code with its rights must be. No sentence says which prevails.
- **H2 — single-program setting files that hold commands the program runs** (`~/.gitconfig` with `!` aliases,
  `~/.ssh/config` with ProxyCommand, Thunar custom actions, xfce4 keyboard shortcuts): read as values by one program
  (S2.2-7, S2.2-13: need not) yet containing shell commands executed with the program's rights (S2.2-10: must).
- **H3 — sshd configuration values other than those S2.2-15 names** (80 rows): a setting applied only by sshd (S2.2-7:
  need not) that changes what can be done on the computer remotely — forwarding, authentication methods, host keys,
  ciphers, limits (S2.2-1: must). S2.2-15 names only accounts, superuser right, login keys, password-login rule, ports.
- **H4 — timestamps of past runs that steer future behaviour** (systemd timer stamps, `/etc/.updated`, `/var/.updated`,
  timesyncd `clock`, NetworkManager `timestamps`): records of the past (S2.2-6) that systemd/timesyncd/NetworkManager use
  to decide whether or when to act (S2.2-2).
- **H5 — network interfaces of (virtual) hardware and loopback** (`networkd:1–3`: lo, ens3, ens4): behaviour depends on
  them (S2.2-1), but they exist by device and kernel; of device-bound objects 2.2 names only firmware and boot order
  (S2.2-16) and says nothing about devices or their interfaces.
- **H6 — primary groups of system accounts with no other documented user** (26 groups): S2.2-15 requires accounts and is
  silent on groups; the only documented removal effect is a `pwck` consistency error (`raw/doc-groups.md`, [N3]). Whether
  a failing check counts as “the computer stops doing something” (S2.2-2) is not decided by the text.

## UNKNOWN rows (S3-2)

- 9 groups with no documented consumer and 2 groups used only by numeric GID (`raw/doc-groups.md`).
- `/etc/apparmor.d/local`, `tunables/home.d`, `tunables/xdg-user-dirs.d`: local AppArmor includes whose content is not in
  the inventory; with rules they change confinement, comment-only they do nothing.
- VS Code `CachedData`, `CachedExtensionVSIXs`, `CachedProfilesData` and `/var/cache/ldconfig/aux-cache`: no public
  documentation of their consumer (items 10b, 39d).
- `/var/lib/AccountsService/users`, `/var/lib/pam`: documentation does not establish the effect of removal (items 35, 36).
- Inside MIXED rows: NetworkManager.state, `/var/lib/flatpak/.changed`, `/var/lib/exim4/berkeleydbvers.txt`.

## Hand check (10 rows per rule; all rows where a kind has fewer than 10)

Each listed row was read with its evidence, members (for directory and subtree rows: the per-member split in
`part-1.members.tsv`) and decision, and the rule was confirmed to fit. Errors found during the checks were corrected in the
rules before the final run (shell dotfile copies in the dotfiles project read as content; `index.php` read as a document
by the name pattern; man-section suffixes matching udev data files; `package.json` in projects; Flatpak locale
deployments; dev-container scripts; generated user units under `/run/user`; the APT list lock). Leaf rules were checked on
10 member paths each, listed in `raw/handcheck-leaves.tsv` (rule, files matched, path).

- `access-rule`: 1c3f3e73a9b7512cd3491b21, 84c1f410613424a2c2846127, bc748d9e22c3fa931e8e0921, e1182fe531b91f83ddde87ef, 4b8a98d8f999fea37b32bde2, 3c8fbdb169ca038e2f7a8f7a, 73b70232c07e15bee2c93628, ba7e43ae48e7b7e88b3ea292, a1a8b86c2f09f76c21f4cfd6, f4d118580a3e7aa82d912ac9
- `account`: dcf85c599976efe3f0fadf4c, 40e833964547387f3ca4e553, c045f40ab9fc1ec3959a9dbc, 5e3cf8572609dda2008fd88a
- `container`: 9a6877ef4dd6c4c7bffb594f, 5d27dbfeaaba365841790985, 81efdb137b7129e363e54bc8, 0e7b4eb5eb41a5b6d4329b4e, 976a51452aa5aaabce9936bc, 0ec69b7d8b30779dc1e36f2f, 275587ed29b693da11e27dee, d5004a94c316645f5bf68e8a
- `container-image`: c97d9f250787c54baa1e0b72, ad5ed316ad45d6f4424c5073, cbaf6f16dab7fb21b548717b, 51e0bcb301dea3bd5c64a3ac
- `cron`: 64a3574bd2259c1ed1eca376
- `driver`: 37249d47f7d6cb3975a13205, 1c7fdfade81743123c431b7a, 49a0af6d1259d7e524659def, 7285a2d79b6340611118e1b8
- `executable-code-outside-packages`: 2b71ef5edd8b703d007bd83a, 404d776d19f9a68932085d32, 36efeba9c9c28b6f5d845719, b9cc019523b0d66d0e47c3fe, c7bc1fe807df7769d0fbb42e, 720007ac16bb21db294b63c3, 6c8873f27b8cad0caee5e39a
- `executable-code-outside-packages:subtree`: lived-t619f4374c5, lived-t71881e496d, lived-tf883bef0f0, lived-tb8a7a2c063, lived-tb47428d5b8, lived-td9eebc32f3, lived-tc8b30d941d, lived-tb1657f171f, lived-t91f66d4e8c, lived-t98b49255b3
- `firewall-chain`: 402a14bcdc254a1331a2d91c, ea5d40a2dff60d224d49f01a, 717eb2770380a84a60c5c313, 68e163de5be454c2c0f3b7ff
- `firewall-rule`: 32d581eebb12d54853ebf91c, 58a06c7bb97e18b1404ae5fb, f91536e8cd43a6fb200dfec6, 47921eae029fa610270e94f1
- `firewall-table`: 42fee34c37890e2ec7bad698, 6545c01a63ed249cce38d052, 48c1fa93a17da9d38e506def
- `group`: 1e65753705892b42cc55b56e, 2fbc9ac38a1fca0e96fb41a8, a5243be5b85fd639a6f8ad5a, 8cd4186084c6fbce8d500cbf, 7b30d550f377d95effa87f34, 52f5f6be8f0b41aa5cdf2046, c9026e221a81a2c85175525f, d606bff3752eefc1ee888580, da017f5c4a67da07e8a06462, bd20cb7545024910f539c53c
- `login-key`: b28703b0cdea90b900c8cad7
- `network`: 44bcf67fcda29b9fa6d3de74, 37e697762632a2f0de4384fd, 45494a3628cd9f2a6a155e72, 65df70aaa862229cd4fd3618, ad5b73353f54e5a01ea55bb9, 29b72142ba82d7d23e0e9bbd
- `network-link`: fbc43cf4d2bace79f0e65a70, de63db4254e7f1cbf407dffd, 91ecf17e0567fccc77b8e076, 204facdaa40276808ea45ed2, 62d714301de740e46b1a3024
- `package:cargo`: 6991627eaf75395605043196
- `package:cargo-record`: 2b716aa0aed143e719689d4c
- `package-environment-evidence`: 534168955efd43cf8b1b3301, c65095cb6961bb571203a2f0, c235fd74db83d877c7cdc7de, 18a2a6e1a146fef4908fd731, 7dbefedebf6375158b6ca300, 6a4bf5ce0c1500b15a598b0c, 8b70c9714a7c27e0ef90e5ed, a6f4d414babd94a2238be68c
- `package:flatpak`: 18b9bb5aa3012aab4095fe54, eb382b4326ecc0b326cbdfc3, acd7640f0b986ad10dbb1129, 47b71fb1018cbc43f4cde174, 5ce7d66a86cdca280e42bc93, 693f3fa4d7636583688f6af5, cdf8dd3fd9a93b29569c3cf2, 77a9aec3657312bb967201e2
- `package:go`: e67b8c76c997bed7186e9949, 5be8a648fc80cb7646411618, 385fe3240425d92fb767c342, 93f00a01084efb1d83134d11, 6100c7453b06a35b9799e9cc, 9968c746c7aaa62cb6fa5d17
- `package:npm`: 6be05e15fdf7269e01542673, fc4e5a075dd57fdd98cf4d25, 121bad3ed70be6a805b6975b, d75981ad39f83b1f4576a61e
- `package:pipx`: c589139bdd7c4b3bf707780e, 7604f7d20e7dbf7c1f68c6a3
- `polkit-actions`: 3ec59e60e2c2b7c76b039708, b7d79d96d478183f1ccc075d, be75483819863b17a0e527a4, 9349beeda15717fda8ad48c9
- `port`: 8e611a3eaca3b173290afa5f, d531eb2deba1edeb8c322875, f4bbb25a9e6780d70e006fe9, f63fd0600c18846258c07f68
- `process`: 726afb221f57533b4008ecb7, 1de8c224f0b98ee3c699a8f1, d30d33c0d7efdc75b5551c7f, 2959fdb88f8e9d41d9db1578
- `python-distribution`: a6dacb809dc75691895def0e, 915cd9116f4fbc48500d4a00, feff37bc6ca255b67c91f699, 0b3d4fcbe5b87ffc9422f6fc
- `saved-network`: d9012fa4771e4e4686e9c967, 5cc49500f354bc1cf21844ee, 3ab18b850bed1101d762fa08
- `service`: 3f1c73b48d9806792c04fcb4, eda9e97b12c68e63a5c07b3b, 4b5d8b7f915ede11ee02dc23, 4af542743d75972de3477dc2, 90f390ddf29b7369718d4977, 58c43b15061fe1a4a1e41fe4
- `stored-outside-packages`: efe73cda98499e12b9c732b9, fa63b149dbac14887436a94b, 4f25115549cd290ab72efd82, c302f79ec70b11e9f3c9c8a7, a7dd2848d4f67deab8876f89, c8d354f09cf6deeda67bed15, 2484b9a7200f48906e5a0a25, 499c36d697b0f35774976d68, 6ace9e160dd7d845ceff0368, a772ec12f7549af88ea9080b
- `stored-outside-packages:subtree`: lived-tc966a381ae, lived-te8c8833c8d, lived-ta0d1cc4da2, lived-td77750f304, lived-t91c412ad0e, lived-tcbbfd4fbc4, lived-t976f564825, lived-td100132f45, lived-t0f4233b4e2, lived-t5d1f10ffd4
- `timer`: ce9cf885ee9d5f0106f81e49
- `unit-file`: a409b189537d3b51d55f24b6, dc5f63136c1d66d1ae5d6ec6, 7e08804c81806445e3fff317, 8ce5df0ab07f695598cd53b1, afb343afc024d97074c96919
- `user-service`: d6bc83a7f2ca4f16f6e78efe, 1413205ac7d1d69a837dabb3, 47c7815588e844c881916f82, d3e48201fd0cea28236a5902, 3c4f4e65c757b551ff3b1f81
- `user-timer`: b8093dd460d9b0712167e99d
- `user-unit-file`: 9a48a4d3192e87cc31ef13b9, 758c5db3a309011cad803bf7, df6003b998e902e368f48f0c, 270e80a8bef7e0a8a0d2b4f0

## Counts

- HOLE: 156
- MIXED: 650
- MUST: 3714
- NOT: 672
- UNKNOWN: 20
