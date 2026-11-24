# D1 adjudication — gap cards

Five gap kinds, 1,364 rows of `rows.tsv` (column `hole`). Facts behind the examples are in
`parts/l1-microos.facts.md` and `parts/l2-other.facts.md`. Paths in examples are inventory names.

## 1. A default value created during installation that no person of this computer chose (214 rows)

**The gap.** Accounts, groups, service enablement links, alias links and alternatives links are created during the
installation of a package (by its scripts, presets or sysusers), or are already present in a distribution's
installation image, and no person using this computer chose them. Question 3 makes an object a setting only if it is
“a value chosen by a person”, so read as a person of this computer such a value is not a setting and falls to
question 4 as a program record; but the text lists services and accounts as settings and says that a default value
“created during its installation” is covered by the package line, which only means something if such defaults are
settings.

**Sentences.**
- S8.2-11 “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”
- S8.2-13 “Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.”
- S8.2-17 “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.2-15 “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state”
- S8.2-6 “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

**Decisions.** SETTING-DEFAULT (for a package default; SETTING-OWN for an image default): it must be recorded, the
package line (or a line of its own) must keep it in force, and removing that line must remove it — versus RECORD: it
need not be recorded, and the declaration says nothing about whether it exists.

**Examples.**
- alma-ade8ccca9c3e357d72437c37 `systemd-oom` — system account made by package scripts during installation.
- alma-71966c5e14f6b1d3115de310 `tss` — system account in no shipped file, made by the tpm2-tss sysusers file.
- microos-13cd5b718c5e71a530a2bed1 `root` — account made by the system-user-root sysusers file.
- alma-53fa364e2cf166bce33a9d60 `avahi-daemon.service` — enablement link made at 05:52:39 by the package's preset, before the person's account existed.
- alma-37c4765f1bc3df9c50c7463a `display-manager.service` — alias link made by gdm's preset during installation.
- void-f1bd8c260127e9a626b5f82f `/var/service/agetty-tty1` — runit service link re-created by runit-void's scripts during a package update.
- void-65591628311f83a7842469aa `/var/service/acpid` — runit service link present in the installation image (mtime 2025-02-02), made by no package.
- alma-9a2b3f5598419c41bbb752af `/etc/alternatives` — 45 alternatives links set by package scripts.
- void-081c93f14c8fa7e6bfd59961 `/usr/bin` — 25 alternatives links set at package installation.
- void-4768b27116e866909ce713da `/home/user/.local/node_modules/.bin` — command links npm made while installing a package.

**Rows:** 214 (alma 167, microos 19, void 28).

## 2. A list the system generated from installed packages (71 rows)

**The gap.** Data files that the system generates from the contents of installed packages (the shared MIME database,
certificate bundles and hash links, ld.so.cache, module dependency lists, compiled schemas, icon and loader caches,
SELinux policy store) are in no package and are not code. By the order of the questions they are program records
(question 4 names a cache), yet the sentence on recording lines names “a generated list” among what is installed and
recorded by the line it was built from; the order of the questions ranks only the four questions, not this sentence.

**Sentences.**
- S8.2-15 “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state”
- S8.2-16 “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-6 “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

**Decisions.** INSTALLED-DERIVED: it must be in force whenever its source packages are, and removing their lines must
remove it — versus RECORD: it need not be recorded, and nothing is required of it.

**Examples.**
- microos-a1f877f4c02acd2a5f9a0d97 `/usr/share/mime` — MIME database files written by update-mime-database.
- void-4ab73c90e99c24b1fb10c341 `/usr/share/mime/application` — 505 generated MIME type files.
- void-f2e5d5edfa5902c8aee7bace `/etc/ssl/certs` — 226 hash links and bundles from update-ca-certificates.
- microos-dcce813055fa256ed012c87a `/var/lib/ca-certificates/openssl` — certificate set generated from the packaged bundle.
- microos-c111706edb49a56b42b0ff18 `/.snapshots/1/snapshot/etc` — contains ld.so.cache generated by ldconfig.
- alma-889f8cd2dae65a248533322a `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64` — modules.* lists generated by depmod (rpm ghost entries).
- void-982c71cf468c85befb1aa508 `/var/cache/ldconfig` — ldconfig auxiliary cache.
- alma-caff428f8364f0a663721a85 `/etc/dconf/db` — dconf databases compiled from packaged keyfiles.
- microos-2ce40b9afb2194333071f853 `/.snapshots/1/snapshot/etc/selinux/targeted/active` — policy store compiled by semodule.

**Rows:** 71 (alma 8, microos 37, void 26).

## 3. Files left from an earlier version of a package that is still installed (1,068 rows)

**The gap.** On Void, the modules of kernel 6.12.11_1 stayed on disk after the package linux6.12 was updated to
6.12.118_1 (the package keeps old kernels). Question 1 asks whether the object was obtained as part of “such a package”,
a package installed on the computer; the text does not say whether an earlier version of an installed package is that
package, so these files are either installed objects of linux6.12 or objects decided by the later questions.

**Sentences.**
- S8.2-7 “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.1-6 “Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.”
- S8.2-16 “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

**Decisions.** INSTALLED-PACKAGE: the line of linux6.12 covers the old modules, and the declaration requires them —
versus a program (kernel modules are code) or a record (data files) not obtained with any installed package: the code
needs a line of its own (PROGRAM-OWN), the data need not be recorded (RECORD).

**Examples.**
- void-7c442df1fb52f7545f18f9cb `/usr/lib/modules` — contains the 6.12.11_1 directory.
- void-0ffeda9e5b96728703a1b7ed `/usr/lib/modules/6.12.11_1/kernel/drivers/gpu/drm/bridge/analogix` — two old modules.
- void-2715a0cd9890aae192131492 `/usr/lib/modules/6.12.11_1` — the old kernel's module tree.
- void-b42866904294dd5e14707b80 `/usr/lib/modules/6.12.11_1/kernel` — its kernel subdirectory.

**Rows:** 1,068 (void).

## 4. A stored archive whose contents are executed (9 rows)

**The gap.** An initramfs image is built by the system (dracut) from installed packages; the boot loader loads it and
the kernel unpacks it and runs the programs inside it. The text calls code what the computer executes and excludes a
file a program only reads as values, but does not say whether an archive that is unpacked, and whose members are then
executed, is code itself.

**Sentences.**
- S8.2-9 “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-23 “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”
- S8.2-15 “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state”

**Decisions.** PROGRAM-DERIVED: a program built by the system, covered by the kernel package's line and required in
force with it — versus RECORD: generated by dracut as it ran, need not be recorded.

**Examples.**
- alma-c4a7c6d6eb439eb9d680a65e `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64.img` — initramfs built by dracut.
- alma-2c25c1a886c5db421b08087b `/boot/initramfs-0-rescue-…img` — rescue initramfs.
- void-0d4bff48fce03ced27aa83a4 `/boot/initramfs-6.12.118_1.img` — initramfs built by the dracut kernel hook.
- void-a6e5bb36a961f99d2e09e83e `/boot/initramfs-6.18.64_1.img` — initramfs of the second kernel series.
- microos-62ccb03ff56e2af8ff91ff68 `/.snapshots/1/snapshot/boot` — contains the initrd built by dracut.
- void-386e90812bdecbec21d0785c `/boot` — three initramfs images, plus two files of the old 6.12.11_1 kernel (card 3).

**Rows:** 9 (alma 4, microos 1, void 4).

## 5. A package of a program's built-in installer whose code runs only inside that program (2 rows)

**The gap.** A browser extension that Firefox's own installer installed permanently is a package, so by question 1 it
is an installed object, and everything installed must be recorded. Its code runs inside the browser and, by its
declared permissions, cannot launch programs or change what is installed or the settings, and the clarification says
such code need not be recorded; no sentence says which of the two prevails (the order of the questions does not rank
a clarification about recording).

**Sentences.**
- S8.1-5 “A general-purpose program with a built-in installer counts as an installer in that part of its functionality.”
- S8.1-6 “Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.”
- S8.2-7 “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-1 “Everything that is installed and every setting must be recorded.”
- S8.2-21 “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.”

**Decisions.** INSTALLED-OWN: it must be recorded by a line of its own and kept in force — versus need not be recorded:
the declaration may omit it.

**Examples.**
- alma-2ea4b9f74eb9ce06f9d317ff `/home/user/.mozilla/firefox/cal-check/extensions` — one extension package (ClearURLs .xpi), permissions without `downloads.open` or native messaging.
- void-61a9a88ad2b852b6cf106db6 `/home/user/.mozilla/firefox/cal-check/extensions` — the same extension on Void.

**Rows:** 2 (alma 1, void 1).
