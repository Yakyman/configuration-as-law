# A1 adjudication — holes

Holes found by the adjudication of the 1084 disputed objects of A1 (`../compare/to-adjudicate.tsv`). Each card is a
kind of case, not a row; the rows are in `rows.tsv` (column `hole` = card number). Sentence texts are quoted from
`../../TEXT.md` (IDs from `../../SENTENCES.md`). Total HOLE rows: 174.

## Hole 1 — A setting read by one program whose effect reaches beyond that program

**Gap.** A configuration file read as values by exactly one program (a daemon or a tool) often decides something
outside that program: the system clock, kernel parameters and modules, mounts, network configuration, files and logs
the program writes or deletes, which other processes may use a bus, which accounts get which defaults. The text
exempts settings “in force only inside one program” but does not say whether that means “read and applied by one
program” (then such a file need not be recorded) or “whose effect stays inside that program” (then the removal test
makes it must-record); the browser example fits both readings.

**Sentences.**
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-13: “a file that a program only reads as values counts as a setting”

**Examples.**
- nixos-009e4f8fbe `/etc/modules-load.d`: module list read only by systemd-modules-load, which loads kernel modules.
- nixos-4d1b734b98 `…-50-coredump.conf` (sysctl.d): applied by systemd-sysctl, sets kernel parameters for the whole system.
- nixos-99f150a190 `…-logrotate.conf`: read only by logrotate, which rotates and deletes other programs' log files.
- nixos-195e0d56cd `…-etc-systemd-logind.conf`: read only by logind, sets KillUserProcesses=false, which decides the fate of user processes.
- guix-331ca6e362 `…-dbus-configuration`: system bus policy read only by dbus-daemon, which decides other processes' access.
- guix-f8cae21bbc `…-ntpd.conf`: read only by ntpd, names the servers used to set the system clock.
- coreos-d159c2f1cf `/etc/request-key.d`: read only by request-key, which starts upcall helpers for kernel key requests.
- coreos-a4c2c16ae9 `/etc/audit`: audit.rules loaded into the kernel by auditctl; auditd.conf decides log files and disk actions.
- debian-desktop-bbe4c8f871 `/etc/netplan`: read only by the netplan generator; without it the interface stays unconfigured.
- freebsd-83dfca210b `/var/crash` (minfree): read only by savecore, decides whether crash dumps are written.

**Rows: 97.**

## Hole 2 — A shipped lookup database that programs need

**Gap.** Data tables shipped with the system and looked up by programs at run time (service and protocol names, time
zones, terminal definitions, the file-type and MIME databases, locale aliases and archives, the hardware database) are
literally “the contents of databases”, which the text says need not be recorded; but they are also files read as
values, which the text calls settings, and their removal makes lookups or whole programs fail. One sentence names them
as need-not, the removal test makes them must-record, and no sentence says which prevails.

**Sentences.**
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-13: “a file that a program only reads as values counts as a setting”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- debian-614d6e2913 `netbase`: /etc/services, protocols, rpc, ethertypes, read through libc; lookups by name fail without them.
- debian-9c32a751d6 `ncurses-base`: basic terminfo entries; full-screen programs fail on those terminals without them.
- debian-f1ae2388d8 `libmagic-mgc`: compiled magic database; `file` and other libmagic users cannot identify types.
- debian-b26e3ddcb0 `tzdata`: time zone rules; zone lookups (TZ=…, /etc/localtime target) fail without it.
- debian-425798e82a `/etc/locale.alias`: locale alias table read by glibc; alias names stop resolving.
- nixos-7d271b79b7 `…-iana-etc-20251215`: /etc/services and /etc/protocols tables for all programs.
- nixos-d42821389f `…-glibc-locales-2.42-103`: compiled locale archive read by glibc in every program.
- coreos-ec7d8d80c0 `/etc/udev` (hwdb.bin): compiled hardware database; device property lookups fail without it.
- ubuntu-86abcca5d5 `/var/lib/command-not-found`: command-to-package database; suggestions fail without it.
- freebsd-1166c4aa4a `/etc/mtree`: specifications of the base hierarchy read by mtree; creating the hierarchy from them fails.

**Rows: 26.**

## Hole 3 — A cache whose removal does more than slow the computer down

**Gap.** Some regenerable files are caches by origin (built from other files, rebuilt on demand), yet until they are
rebuilt programs fail or operations are impossible, not merely slower. The text names cache as need-not and gives as
its reason that the computer then does the same only more slowly, while the removal test makes such an object
must-record; the text does not say whether the exemption holds for a cache whose removal breaks something.

**Sentences.**
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- coreos-d9f9f1c4e7 `/etc/ld.so.cache`: built by ldconfig; a library under /usr/lib64/llvm18/lib is found only through it, so the program needing it fails.
- debian-53f7b0994c `/var/lib/apt`: downloaded package indexes, rebuilt by apt update; without them apt install fails until refreshed.
- nixos-bfd49e603a `/nix/store outside current system closure`: re-downloadable root channel, without which channel-based nixos-rebuild cannot evaluate.
- guix-317d6b1fbf `…-glib-schemas`: gschemas.compiled built from schema files; GSettings programs abort without it.
- guix-546939a102 `…-manual-database`: mandb index; apropos and whatis fail until it is rebuilt.
- guix-f62a370c22 `…-gtk-im-modules`: GTK input-method module cache; GTK cannot load its input-method modules without it.

**Rows: 6.**

## Hole 4 — Compiled code kept as a cache

**Gap.** Byte-compiled code that a program executes with its own rights, but that is regenerated from the source if it
is removed (Guile `.go` files with the source still on the load path), is both executed code, which must be recorded,
and a cache, which need not be. Both sentences apply literally and no sentence says which prevails.

**Sentences.**
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

**Examples.**
- guix-084d6fb332 `/home/guest/.cache/guile`: auto-compiled `.go` of the user's Guile files, executed by guix; rebuilt from source if removed.
- guix-033f2e4eef `/root/.cache/guile`: the same for the superuser's Guile files.
- guix-4693999f1c `…-module-import-compiled`: compiled Guile modules executed as root by activation and shepherd; source modules stay as fallback.
- guix-a36c632a1b `…-module-import-compiled`: the same, another module set.
- guix-25ad6943ae (store items outside the system and user-package closures): Guix Home compiled modules with source fallback.

**Rows: 12.**

## Hole 5 — Runtime reflections that cannot be removed on their own

**Gap.** Some objects exist only as the service manager's or the kernel's reflection of something else: device units
of present hardware, mount and swap units synthesized from the mount and swap tables, scope and slice units of running
processes, entries the kernel makes in a pseudo-filesystem. There is nothing to delete (or deletion is undone at
once), and the acts that make them disappear—removing hardware, unmounting, swapoff, killing processes—remove other
objects; the text makes removal “the test” but does not say what removal means for such an object, while behaviour
plainly depends on it.

**Sentences.**
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S3-1: “in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”

**Examples.**
- coreos-88335c6c87 `unpackaged *.device` (user manager): device units created from present kernel devices.
- debian-18fb2985ed `unpackaged *.mount`: mount units generated from fstab or synthesized from the mount table.
- debian-0ff15b2741 `unpackaged *.scope`: init.scope of PID 1 and the login session scope.
- debian-253d752b01 `unpackaged *.slice`: control-group slices the service manager creates at runtime.
- arch-2540fd3280 `swap-swapfile.swap`: swap unit with no unit file, reflecting an active swap area.
- silverblue-8d6e6c94ec `dev-zram0.swap`: the same for the zram swap device.
- coreos-0eecaaf2d8 `/var/lib/nfs`: rpc_pipefs entries the kernel creates in a mounted pseudo-filesystem.

**Rows: 30.**

## Hole 6 — Removal stops nothing now but changes what the computer does later

**Gap.** For an object that is not program state, removal can stop nothing and make nothing impossible now, yet change
what the computer does at a later event (here: whether the next account creation allocates subordinate ID ranges).
The general rule makes whatever the computer's behaviour depends on must-record, but the removal test detects only
stopping or impossibility, and the text does not say which decides.

**Sentences.**
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- debian-f17149d114 `/etc/subuid`: subordinate UID range of the test account; no tool reads it now; without the file later useradd allocates no ranges.
- debian-f18cbc897b `/etc/subgid`: the same for subordinate GIDs.

**Rows: 2.**

## Hole 7 — A log directory whose existence switches log keeping on

**Gap.** With journald's default storage mode, logs are kept across reboots only if the directory `/var/log/journal`
exists; the directory is not itself a record and not a file read as values. Logs are exempt as records of the past,
but removing the directory makes the computer stop keeping logs across reboots, which the removal test makes
must-record, and the text does not say whether the exemption of logs covers the place whose existence makes them kept.

**Sentences.**
- S2.2-6: “records of the past—logs, history;”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- debian-47c62f375a `/var/log`: holds the logs and `/var/log/journal`; journald.conf fully commented (Storage=auto), so without the directory journald stops keeping logs across reboots.

**Rows: 1.**
