# Part 4 stored objects: c1 notes

Scope: 108 rows, stored objects, store groups, directory skeleton, and user-profile rows. The classification used only supplied input, the numbered sentences, raw inventory, and public program documentation. Inventory class labels were not used. A structural probe of the input file `../in/raw/guix/group-members.json` unexpectedly exposed legacy classification fields; those fields were ignored and the file was not used again. Membership was obtained from `unowned-groups.json` instead.

No removals or experiments were performed. UNKNOWN means missing object behavior, not a defect in the definition. No generation, rollback, or state-design question was treated as a hole.

## Scripted rule

Only log rows were classified by a homogeneous rule: an inventoried service, build, display, or login log records past events and is NOT under S2.2-6, "records of the past—logs, history;". This rule applies to the 12 rows under the system log directory and the rotated resize log. Hand checks of ten input rows and corresponding group membership:

- guix-a4963ec3b5: display server log.
- guix-2cd84ac792: service-discovery daemon log.
- guix-b6a2c8e4dd: message-bus daemon log.
- guix-5ba0b35443: debug log.
- guix-985ad63959: build derivation logs, including compressed build records.
- guix-43c963f378: package-store daemon log.
- guix-698c23461f: last-login history.
- guix-91a21a61f1: system message log.
- guix-e684d315eb: clock synchronization log.
- guix-4ac29aa55a: authentication log.

All other rows were decided individually. The assignment script serializes explicit row decisions, rather than applying inferred classes to unseen rows. Small repeated decisions (two debugger files, two interpreter files, two editor option files, two compiled caches) were checked individually against each inventory row.

## Documentary evidence

The raw inventory establishes each object identity; documentation establishes format and function. The following quotations are exact excerpts, with conclusions limited to the recorded object types:

- https://sourceware.org/gdb/current/onlinedocs/gdb.html/gdbinit-man.html: "These files contain GDB commands to automatically execute during GDB startup." Both debugger initialization rows execute commands, rather than merely supply values.
- https://www.gnu.org/software/guile/manual/html_node/Init-File.html: "This file should contain Scheme expressions for evaluation." Both interactive initialization rows are executable Scheme.
- https://www.gnu.org/software/guile/manual/guile.pdf: "Scheme source files will be compiled automatically, by default." The two captured `.go` files correspond to captured Scheme sources. They are both recompilable cache and executed interpreter code; S2.2-5 and S2.2-10 give opposing specific requirements without an explicit priority.
- https://www.nano-editor.org/dist/latest/nano.html: "Read only this file for setting nano’s options". The nanorc objects supply editor-local options; unlike the observed executable editor command file, their documented grammar specifies options.
- https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html: "determine the sources from which to obtain name-service information in a range of categories, and in what order."
- https://man7.org/linux/man-pages/man5/hosts.5.html: "associates IP addresses with hostnames".
- https://man7.org/linux/man-pages/man5/resolv.conf.5.html: "access to the Internet Domain Name System (DNS)."
- https://man7.org/linux/man-pages/man5/protocols.5.html: "describing the various DARPA internet protocols that are available from the TCP/IP subsystem."
- https://man7.org/linux/man-pages/man5/services.5.html: "providing a mapping between human-friendly textual names for internet services, and their underlying assigned port numbers and protocol types."
- https://man7.org/linux/man-pages/man5/shells.5.html: "valid login shells" and "This file is consulted by chsh(1)".
- https://man7.org/linux/man-pages/man5/shadow.5.html: "contains the password information for the system's accounts and optional aging information." This single file combines exempt password material and mandatory login policy. Its account-policy role makes the file MUST; representation of exempt password portions is a declaration-design question.
- https://man7.org/linux/man-pages/man5/fstab.5.html: "contains descriptive information about the filesystems the system can mount."
- https://man7.org/linux/man-pages/man5/issue.5.html: "contains a message or system identification to be printed before the login prompt."
- https://man7.org/linux/man-pages/man5/localtime.5.html: "configures the system-wide timezone".
- https://man7.org/linux/man-pages/man5/rpc.5.html: "contains user readable names that can be used in place of RPC program numbers."
- https://man7.org/linux/man-pages/man8/nscd.8.html: "provides a cache for the most common name service requests."
- https://man7.org/linux/man-pages/man5/environment.5.html: "the environment variables config files".
- https://www.x.org/guide/communication/: "X Protocol Security model". The documented cookie protocol uses Xauthority authorization material for display access.
- https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html: "Fontconfig is a library designed to provide system-wide font configuration, customization and application access."
- https://docs.mesa3d.org/envvars.html documents the shader disk cache and its disabling switch. The captured cache avoids repeated graphics compilation.
- https://guix.gnu.org/manual/en/guix.pdf: "Guix uses an sqlite database to keep track of the items". The operational store database is mandatory under removal: S2.2-4 expressly requires unchanged capability for exempt content, so it does not exempt an operational database whose loss breaks store management.
- https://docs.xfce.org/xfce/thunar/custom-actions: "Thunar allows users to add custom actions to the file and folder context menus". Actual command contents were not captured; this establishes the file's purpose but not the code/value distinction of the observed file.

Some HTML pages on the package-manager documentation server returned HTTP 403; its indexed PDF supplied the quoted evidence. Exact configuration values are unnecessary when documentation establishes a mandatory operational role. UNKNOWN is retained where the relevant function or a heterogeneous group's complete partition remains unavailable; no default values are assumed.

## Mixed Home group

For guix-25ad6943ae, the 17 store members in `../in/raw/guix/home-closure-outside-system-and-user.txt` are mapped by their basename suffix (hashes retained in that raw file):

- NOT: `w1-declared-note` (observed plain text in `../in/raw/guix/user-settings.txt`); `provenance` (record of the environment's construction).
- MUST: both `module-import` members and both `module-import-compiled` members (Scheme support code); `setup-environment`, `shell-profile`, `on-first-login`, `activate`, `update-symlinks` (environment setup and activation code); `guix-1.5.0` (program); `configuration.scm` (Scheme configuration); `fonts.conf` (shared font configuration); `profile`, `home`, `files` (operational environment links).

`../in/raw/guix/user-settings.txt` directly shows login code loading the environment and running first-login actions. `../in/raw/guix/day/user-day.log` shows Home reconfiguration, generated activation, file-link updates, and execution of the separately installed user program. Uncaptured internal files of other large groups were not inferred from their directory names.

## Interpretation limits

The store-outside-system group includes thousands of builder and derivation names. It is UNKNOWN because its complete executable/content/cache partition cannot be established from names. The bootloader group likewise includes executable modules alongside font, locale, configuration, and environment data; the inventory supplies membership but insufficient member roles for a complete partition. Empty directory skeleton entries are not automatically cache, content, or programs; consumers and removal consequences are not shown.

Configuration symlinks were evaluated using documented operational roles; descriptive target names alone were insufficient when member functions could differ. A shared library configuration may affect multiple applications, while a setting enforced only inside one editor falls under S2.2-7. For executable startup files, S2.2-13 explicitly resolves the code-versus-setting question even when the command only changes an option.

## Additional documentary evidence

The distinction is between unknown exact settings and unknown function. Exact settings are unnecessary where the documented role establishes that the object controls system behavior. The shadow file is MUST because of its account-policy role; representing its exempt password portions concerns declaration form, not a hole.

- https://raw.githubusercontent.com/lfam/guix/master/gnu/system.scm: "Some programs (e.g., GLib) look at /etc/timezone to find the" followed by "name of the current timezone." The same source constructs the persistent hostname file from the system hostname.
- https://raw.githubusercontent.com/lfam/guix/master/gnu/services/base.scm: "On boot, write random seed into /dev/urandom." The captured `urandom-seed` service and reviewed source establish the consumer; it also credits entropy, refreshes the seed, and saves it at shutdown. Source excerpt: `part-4.service-source.txt`.
- https://raw.githubusercontent.com/lfam/guix/master/guix/profiles.scm: `(normal-top-level-add-to-load-path` in the `emacs-subdirs` builder establishes executable editor Lisp. The `info-dir-file` builder writes the documentation menu with `install-info`. Thus the two-member support group is MIXED: `emacs-subdirs` MUST, `info-dir` NOT.
- https://dbus.freedesktop.org/doc/dbus-specification.html defines the machine identifier used by `org.freedesktop.DBus.Peer.GetMachineId`. Stable machine identity supports interprocess communication, so the identifier is operational rather than a mere document.
- https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html: "This file lists all the filesystems currently mounted in the process's mount namespace". The mount-table alias exposes this operational query interface.
- https://man7.org/linux/man-pages/man5/os-release.5.html: "operating system identification data." Its documented identifier fields support programmatic operating-system detection, beyond a single program's interface.
- https://man7.org/linux/man-pages/man5/pam.d.5.html: "These files list the PAMs that will do the authentication tasks required by this service".
- https://man7.org/linux/man-pages/man5/login.defs.5.html: "shadow password suite configuration".
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html: "Rules files are written in the JavaScript". Their authorization purpose is sufficient even without exact rules: they control callers' privileges.
- https://man7.org/linux/man-pages/man7/udev.7.html: "manages permissions of device nodes and may create additional symlinks".
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html documents bus policy and service activation. These determine communication and available service processes, beyond daemon-internal preferences.

Final decisions: MUST 56, NOT 22, HOLE 2, UNKNOWN 26, MIXED 2. The two HOLE rows concern executed compiled caches under opposing explicit sentences, not declaration format. UNKNOWN groups lack a complete functional partition, or their evidence does not establish the relevant operational role. The two profile-support members are fully partitioned as stated above.

ALSA alias: guix-84d10d5518 is MUST. The target is the system-global audio configuration. https://www.alsa-project.org/wiki/Asoundrc states: "When an alsa application starts both configuration files are read." Shared routing and conversion affect independently running ALSA applications; S2.2-7 does not exempt this as a setting inside one program. The role was checked against the same public evidence used for the target store object.

The Home17 group lists two imported source-module outputs and two imported compiled-module outputs. The supplied Home startup evidence does not expose their exact source-to-compiled correspondence, loader search paths, or fallback behavior. Accordingly, no cache exemption is inferred merely from `module-import-compiled` names; the executable support-code classification remains MUST. This differs from the two user compilation-cache rows, whose specific source files and standard automatic recompilation path are established.
