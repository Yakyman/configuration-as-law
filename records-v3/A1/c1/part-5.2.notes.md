# Part 5, stored objects on the two assigned distributions

Only COMMON.md, TEXT.md Sections 2 and 3, SENTENCES.md, and the assigned input rows were read locally. The expected raw directories for these distributions do not exist. No objects were removed. Directory groups have `members=1` in the input, but inventory evidence often supplies a larger `n`; that underlying count was respected rather than treating four sample paths as the entire group.

The classifications are row-specific except the two explicitly identified rules below. The build script records each individual assessment. This is a classification, not independent acceptance.

## Exact governing sentences

- S2.2-1: Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- S2.2-2: The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- S2.2-5: cache: after it is removed, the computer does the same, only more slowly;
- S2.2-6: records of the past—logs, history;
- S2.2-7: settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- S2.2-9: a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- S2.2-10: code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- S2.2-13: A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- S2.2-15: accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- S3-2: If what the object does remains unknown, the case yields ?.

## Rule L: standalone historical log files

S2.2-6 directly exempts logs. This rule applies only to individually identified, standalone log files. It does not classify incompletely enumerated log directories. Hand checks of ten input rows:

- alpine-4156dc1632: acpid event log, one file.
- alpine-336e9af6dd: apk operation log, one file.
- alpine-93b020b2d3: cloud initialization output log, one file.
- alpine-2954505d9d: cloud initialization execution log, one file.
- alpine-293699acd1: saved kernel message log, one file.
- alpine-91a21a61f1: system message log, one file.
- alpine-d6ce9987c3: completed login-session history, one file.
- arch-9c96b64591: failed-login history, one file.
- arch-698c23461f: last-login history, one file.
- arch-abc9f2b51d: package transaction history, one file.

The additional row arch-d6ce9987c3 is also a single login-history file. All eleven fit the historical-log exemption.

## Rule U: incomplete stored-directory enumeration

The input supplies only a subset of members and the full raw listing is absent. Documentation can describe a known filename, but cannot recover unnamed members of these particular directories. S3-2 therefore requires UNKNOWN for the complete group; neither homogeneity nor a complete member-by-member MIXED allocation is inferred from samples. Ten hand checks, each comparing the inventory count with the actual displayed sample paths:

- alpine-312e18febb: 24 objects, four service-link samples.
- alpine-0075a76d48: seven objects, four server-key samples.
- alpine-561d6a5935: three objects, one device-rule sample.
- alpine-c3a3dd6c9b: two objects, one login-key sample.
- alpine-351644c1fd: two objects, one login-key sample.
- alpine-995a8560ba: 53 objects, four initialization-state samples.
- arch-76634f69cd: 699 objects, four bootloader samples.
- arch-472ce9551e: 361 objects, four certificate-store samples.
- arch-d938b25615: 19 objects, four package-signing samples.
- arch-0075a76d48: eight objects, four server-key samples.

The remaining Rule U rows were likewise read individually: arch-0306bdd9a9, arch-b86fee9a16, arch-c3a3dd6c9b, arch-2b7dd179b7, arch-b618c77d89, arch-23338df933, arch-cafdef0617, arch-57da4d32dc, arch-e6b33c3854. Each gives fewer sample paths than its inventory count. The two unnamed directory skeletons were separately assessed as UNKNOWN because even their paths are unavailable.

## Documentation and exact supporting excerpts

Short quotations below identify the relevant documentation; deductions are in the TSV reasons. No source substitutes for a missing machine-specific inventory.

- https://wiki.archlinux.org/title/Syslinux — “Stage 3 - Load `/boot/syslinux/ldlinux.c32`”. The indexed documentation describes the bootloader stages, native module libraries, configuration loading, and text menu.
- https://kernel.googlesource.com/pub/scm/boot/syslinux/syslinux/+/master/doc/menu.txt — “com32/menu/vesamenu.c32 (graphical) or com32/menu/menu.c32 (text”. This upstream source establishes both menu module functions.
- https://github.com/alpinelinux/mkinitfs — “Tool to create initramfs images”.
- https://github.com/alpinelinux/mkinitfs/blob/master/mkinitfs.in — `for file in $(feature_files "${kerneldir}/" modules); do`. The surrounding routine gathers module dependencies and copies selected drivers into the image.
- https://github.com/alpinelinux/apk-tools/blob/master/doc/apk.8.scd — “Collection of all package scripts from currently installed packages.” Its FILES section separately documents architecture, repository lists, required packages, installed metadata, trigger rules, transaction lock, and index cache.
- https://github.com/OpenRC/openrc/blob/master/sh/openrc-run.sh.in — `sourcex -e "$_f/conf.d/$_c"` and `sourcex "$RC_SERVICE"`. Both service settings and service scripts are sourced by the runner.
- https://man.archlinux.org/man/doas.conf.5.en — “The target user the running user is allowed to run the command as. The default is all users.”
- https://man.archlinux.org/man/sudoers.5.en — “The sudoers policy plugin determines a user's sudo privileges.”
- https://man7.org/linux/man-pages/man5/passwd.5%40%40shadow-utils.html — “Backup file for /etc/passwd.”
- https://man7.org/linux/man-pages/man5/shadow.5.html — “Backup file for /etc/shadow.”
- https://man.archlinux.org/man/subuid.5.en — “Backup file for /etc/subuid.”
- https://man.archlinux.org/man/dhcpcd.8.en — “Text file that holds the DUID used to identify the host.” The same manual describes lease reuse, a stored secret, and resolver configuration. The secret's mere existence does not establish this installation's operational dependence.
- https://www.man7.org/linux/man-pages/man3/getspnam.3.html — “lock file”. This identifies the password lock, but does not show whether this stored inode currently carries a lock.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files — “This section describes how Bash executes its startup files.” The manual explicitly describes login, interactive, and logout command execution.
- https://ftp.gnu.org/old-gnu/Manuals/bash-2.05a/html_mono/bashref.html — “Any user can customize programs that use Readline by putting commands in an inputrc file”. Shared use creates the reported scope ambiguity, not uncertainty over Readline's basic function.
- https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano, a small and friendly text editor.”
- https://man.archlinux.org/man/mkinitcpio.8.en — “Creates an initial ramdisk environment for booting the Linux kernel.” This also documents preset-based generation of images.
- https://man7.org/linux/man-pages/man8/ld.so.8.html — “a compiled list of candidate shared objects previously found in the augmented library path.” Cache contents are unavailable, so the fallback search cannot establish equivalent behavior here.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-update-done.service.html — “Mark `/etc/` and `/var/` as fully updated”. The modification times are compared by conditional update services: both historical recording and future behavioral control are documented.
- https://www.freedesktop.org/software/systemd/man/latest/hostname.html — “The `/etc/hostname` file configures the name of the local system.”
- https://www.freedesktop.org/software/systemd/man/latest/locale.conf.html — “The `/etc/locale.conf` file configures system-wide locale settings.”
- https://www.freedesktop.org/software/systemd/man/latest/localtime.html — “If `/etc/localtime` is missing, the default `UTC` timezone is used.” The input explicitly shows a UTC target, so removal retains the documented timezone default.
- https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “`/etc/machine-id` is used to decide whether a boot is the first one.” The documentation also identifies the D-Bus compatibility link.
- https://www.freedesktop.org/software/systemd/man/latest/vconsole.conf.html — “The `/etc/vconsole.conf` file configures the virtual console, i.e. keyboard mapping and console font.”
- https://www.freedesktop.org/software/systemd/man/latest/os-release.html — “Applications should check for the former, and exclusively use its data if it exists, and only fall back to `/usr/lib/os-release` if that is missing.” Compatibility-only readers are also documented; their presence is not inventoried.

The apk replacement file and the boot-directory alias remain UNKNOWN because their actual readers are not established. The upstream mboot README and mboot documentation URLs were tried but inaccessible, and the inventory supplies no module contents. This is factual insufficiency, not a textual hole.

## Validation

The script verified exactly 87 assigned IDs, identical sets and counts, each once; all decisions allowed; every description and reason meets its word limit. Counts: MUST=31, NOT=23, HOLE=4, UNKNOWN=28, MIXED=1.
