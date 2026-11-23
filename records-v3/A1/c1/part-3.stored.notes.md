# Part 3 stored-object decisions

All 97 rows were decided individually. The writing script contains one explicit decision per ID; it does not classify rows by a homogeneous rule. Therefore the ten-sample requirement for scripted homogeneous classification does not apply. No files were removed or experiments run.

The inventory sometimes reports members=1 for a whole directory. Its full saved inventory was consulted; a directory with missing target contents is not presumed homogeneous. UNKNOWN denotes missing operational evidence, not a claimed defect in the text. Questions about state-management design were not independently treated as holes.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;

- **S2.2-6** records of the past—logs, history;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Raw evidence

`../in/raw/nixos/unowned-groups.json` establishes each stored file type, target, size, and enumerated directory membership. `../in/raw/nixos/directory-only-groups.json` lists directory remainder members. `../in/raw/nixos/day.log` demonstrates hello execution through its user profile and writes the editor command `set number` and an ordinary work note. `../in/raw/nixos/user-profile.txt` and `user-closure-outside-system.txt` identify the installed hello environment. `../in/raw/nixos/root-profile.txt` supplies no installed packages. `A1/in/raw/nixos/nixos-configuration/configuration.nix` specifies boot, accounts, login keys, services, and privilege policy. `../in/raw/nixos/store-outside-system-closure.txt` supplies names, not the contents or consumer of every store object.

## Public documentation

The following short quotations establish functions independently of inventory classification language. URL citations supplement raw identity evidence; they do not prove absent local settings.

- Boot image: https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html — “Set a background image for use with the ‘gfxterm’ graphical terminal.”
- Boot fonts: https://www.gnu.org/software/grub/manual/grub/grub.html — “Fonts are loaded with the “loadfont” command in GRUB”.
- Shell initialization: https://man7.org/linux/man-pages/man1/bash.1.html — “executes commands from the file /etc/profile, if that file exists.”
- DHCP hooks: https://manpages.debian.org/testing/dhcpcd-base/dhcpcd-run-hooks.8.en.html — “run any system and user defined hook scripts.”
- Binary registration: https://www.freedesktop.org/software/systemd/man/latest/binfmt.d.html — “register in the kernel additional binary formats for executables.”
- Service environment: https://www.freedesktop.org/software/systemd/man/latest/environment.d.html — “environment variable assignments passed to services started by the systemd user instance.”
- Filesystems: https://man7.org/linux/man-pages/man5/fstab.5.html — “The file fstab contains descriptive information about the filesystems the system can mount.”
- Account creation: https://man7.org/linux/man-pages/man8/useradd.8.html — “useradd - create a new user or update default new user information”.
- Address ordering: https://man7.org/linux/man-pages/man5/gai.conf.5.html — “these answers must be sorted so that the answer with the highest success rate is first in the list.”
- Groups: https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.”
- Resolver: https://man7.org/linux/man-pages/man5/host.conf.5.html — “The file /etc/host.conf contains configuration information specific to the resolver library.”
- Host name: https://www.freedesktop.org/software/systemd/man/latest/hostname.html — “The `/etc/hostname` file configures the name of the local system.”
- Host mapping: https://man7.org/linux/man-pages/man5/hosts.5.html — “This file is a simple text file that associates IP addresses with hostnames”.
- Shared input: https://man7.org/linux/man-pages/man3/readline.3.html — “Other lines denote key bindings and variable settings.”
- Login banner: https://man7.org/linux/man-pages/man5/issue.5.html — “a message or system identification to be printed before the login prompt.”
- Locale: https://www.freedesktop.org/software/systemd/man/latest/locale.conf.html — “The locale settings configured in `/etc/locale.conf` are system-wide and are inherited by every service or user”.
- Login defaults: https://man7.org/linux/man-pages/man5/login.defs.5.html — “The /etc/login.defs file defines the site-specific configuration for the shadow password suite.”
- Machine identity: https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “The `/etc/machine-id` file contains the unique machine ID of the local system that is set during installation or boot.”
- Manual settings: https://man7.org/linux/man-pages/man5/manpath.5.html — “The manpath configuration file is used by the manual page utilities to assess users' manpaths at run time”.
- Kernel module settings: https://man7.org/linux/man-pages/man5/modprobe.d.5.html — “modprobe.d - Configuration directory for modprobe”.
- Boot modules: https://www.freedesktop.org/software/systemd/man/latest/modules-load.d.html — “contain kernel modules to load during boot in a static list.”
- Editor settings: https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano”.
- Shared name-service policy: https://www.man7.org/linux/man-pages/man5/nsswitch.conf.5.html — “sources from which to obtain name-service information”; netgroup: “Network-wide list of hosts and users, used for access rules.”
- Name-service cache configuration: https://man7.org/linux/man-pages/man5/nscd.conf.5.html — “The file /etc/nscd.conf is read from nscd(8) at startup.”
- Session environment: https://man7.org/linux/man-pages/man5/pam_env.conf.5.html — “When someone logs in, these files are read and the environment variables are set according.”
- Authentication: https://man7.org/linux/man-pages/man5/pam.d.5.html — “When a PAM aware privilege granting application is started, it activates its attachment to the PAM-API.”
- Accounts: https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.”
- Certificate trust: https://docs.openssl.org/3.0/man3/SSL_CTX_load_verify_locations/ — “The certificates available via CAfile, CApath and CAstore are trusted.”
- Protocol lookup: https://man7.org/linux/man-pages/man5/protocols.5.html — “This file is a plain ASCII file, describing the various DARPA internet protocols that are available from the TCP/IP subsystem.”
- DNS lookup: https://man7.org/linux/man-pages/man5/resolv.conf.5.html — “The resolver is a set of routines in the C library that provide access to the Internet Domain Name System (DNS).”
- Resolver generator configuration: https://man.netbsd.org/NetBSD-6.0.3/resolvconf.conf.5 — “resolvconf.conf file is a shell script that is sourced by resolvconf(8)”.
- RPC lookup: https://man7.org/linux/man-pages/man5/rpc.5.html — “The rpc file contains user readable names that can be used in place of RPC program numbers.”
- Service lookup: https://man7.org/linux/man-pages/man5/services.5.html — “providing a mapping between human-friendly textual names for internet services, and their underlying assigned port numbers and protocol types.”
- Environment script: https://wiki.nixos.org/wiki/NixOS_system_configuration — “source /etc/set-environment”.
- Password policy: https://man7.org/linux/man-pages/man5/shadow.5.html — “If the password field begins with an exclamation mark !, the password is locked.”
- Login shells: https://man7.org/linux/man-pages/man5/shells.5.html — “This file is consulted by chsh(1) and available to be queried by other programs.”
- Subordinate groups: https://man7.org/linux/man-pages/man5/subgid.5.html — “Subgid authorizes a group id to map ranges of group ids from its namespace into child namespaces.”
- Subordinate users: https://man7.org/linux/man-pages/man5/subuid.5.html — “Subuid authorizes a user id to map ranges of user ids from its namespace into child namespaces.”
- Kernel parameters: https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html — “Configure kernel parameters at boot”.
- Terminal descriptions: https://man7.org/linux/man-pages/man5/termcap.5.html — “new programs should use the terminfo(5) database and associated libraries.”
- Runtime file rules: https://www.freedesktop.org/software/systemd/man/latest/tmpfiles.d.html — “Configuration for creation, deletion, and cleaning of files and directories”.
- Device rules: https://www.freedesktop.org/software/systemd/man/latest/udev.html — “udev supplies the system software with device events, manages permissions of device nodes”.
- Console: https://www.freedesktop.org/software/systemd/man/latest/vconsole.conf.html — “The `/etc/vconsole.conf` file configures the virtual console, i.e. keyboard mapping and console font.”
- Timezone: https://man7.org/linux/man-pages/man5/tzfile.5.html — “The timezone information files used by tzset(3) are typically found under a directory with a name like /usr/share/zoneinfo.”
- Profile selection: https://nix.dev/manual/nix/2.28/package-management/profiles — “The solution Nix uses is to create directory trees of symlinks to activated packages.”
- Channels: https://nix.dev/manual/nix/2.28/command-ref/nix-channel — “Channels are a mechanism for referencing remote Nix expressions and conveniently retrieving their latest version.”
- Daemon access: https://nix.dev/manual/nix/2.28/command-ref/nix-daemon — “It runs build tasks and other operations on the Nix store on behalf of unprivileged users.”
- Store database: https://nix.dev/manual/nix/2.28/store/types/local-store — “Nix's store metadata is in `/tmp/root/nix/var/nix/db`.”
- Collection roots: https://nix.dev/manual/nix/2.28/package-management/garbage-collector-roots — “the garbage collector will not remove `/nix/store/d718ef...-foo` or any of its dependencies.”
- Cache lookup: https://nix.dev/manual/nix/2.34/command-ref/conf-file.html?highlight=allowed-user — “Set to `0` to force updating the lookup cache.”
- Update markers: https://www.freedesktop.org/software/systemd/man/latest/systemd-update-done.service.html — “use the `ConditionNeedsUpdate=`”; “according to the modification times of the files described above.”
- Lingering: https://www.freedesktop.org/software/systemd/man/latest/loginctl.html — “a user manager is spawned for the user at boot and kept around after logouts.”
- Timer state: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “If true, the time when the service unit was last triggered is stored on disk.”
- Random seed: https://www.freedesktop.org/software/systemd/man/latest/systemd-random-seed.service.html — “loads an on-disk random seed into the kernel entropy pool during boot and saves it at shutdown.”
- Clock state: https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html — “uses this to possibly advance the system realtime clock on subsequent reboots”.
- Last login: https://man7.org/linux/man-pages/man8/lastlog2.8.html — “lastlog2 - displays date of last login for all users or a specific one”.
- Journal: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — “journalctl is used to print the log entries stored in the journal”.
- Login history: https://man7.org/linux/man-pages/man5/utmp.5.html — “utmp, wtmp - login records”.
- Runtime compatibility: https://man7.org/linux/man-pages/man7/hier.7.html — “Once this purpose was served by /var/run and programs may continue to use it.”

## Mixed group and limits

`nixos-57da4d32dc` retains MIXED with the following complete partition. Paths below are relative to the group's directory. Each of the twelve inventoried members appears once; the account-specific lingering filename is described without publishing an account name.

| Member | Decision | Evidence and reason |
| --- | --- | --- |
| Group directory itself | MUST | Removing the containing directory makes the known required descendants unavailable. |
| `catalog` directory | NOT | Container of the catalog content described below. |
| `coredump` directory | UNKNOWN | Empty in the inventory; no saved permissions, local retention settings, or actual use establish this directory's removal effects. |
| `ephemeral-trees` directory | UNKNOWN | Empty in the inventory; no saved permissions or local consumers establish this directory's removal effects. |
| `linger` directory | MUST | Makes the known user-lingering marker available to the login manager. |
| `timers` directory | HOLE | Contains the operational history stamp described below. |
| `timesync` directory | MUST | Makes the stored clock file available. |
| `catalog/database` | NOT | A message catalog of descriptive strings; removing it loses explanatory content rather than journaling capability. |
| Account-specific file in `linger` | MUST | Enables continued user services according to loginctl documentation. |
| `random-seed` | MUST | Feeds the kernel entropy pool according to random-seed service documentation. |
| `timers/stamp-fstrim.timer` | HOLE | Records a previous invocation but controls future scheduling: S2.2-1 versus S2.2-6. |
| `timesync/clock` | MUST | Advances boot time according to timesyncd service documentation. |

Additional catalog evidence: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html describes `--list-catalog` contents as “message IDs, plus their short description strings.” The same page's `--root` option explicitly maps `--update-catalog` to `var/lib/systemd/catalog/database`; `--update-catalog` rebuilds the binary index from installed catalog files. This establishes the content function of the inventoried database. Unknown empty-directory members are now explicit rather than silently inherited from absent content.

Review correction for `nixos-2527479582`: the documentation identifies multiple manual-page utilities; no local contents or consumer evidence establish the literal one-program condition. The decision is UNKNOWN under S3-1/S3-2. This corrects an unsupported exemption inference, not the fixed text.


For single files containing both mandatory and exempt fields, MUST means the object cannot be omitted wholesale, not that every password byte must be recorded. Thus the shadow-file decision retains S2.2-15's explicit password exemption. A group uses MIXED when its members receive different decisions, including explicitly identified UNKNOWN members. Missing knowledge is retained at member level when other members have established decisions.

The update-marker holes and timer hole concern dual applicability of a stated history exemption and a documented behavioral dependency, not an objection that the text leaves state-transfer design unspecified.

## Reviewed heterogeneous-group partitions

These partitions replace the original whole-group UNKNOWN results. The classification does not require every member's function to be known before MIXED is usable. UNKNOWN is one of the allowed member decisions. A disjoint named subset followed by its explicit complement exhausts the saved group.

- `nixos-bfd49e603a` (4347 members): NOT applies to `/nix/store/wsm1x62rvhk30y7mqy1mp4yj8hhgglz1-nixos-rebuild.8.scd` and `/nix/store/yyrh92g94j8ljs6jaylqb8s7lkh6kggi-nixos-version.8`, which are the named manual-page documents. UNKNOWN applies to all 4345 other paths in `../in/raw/nixos/store-outside-system-closure.txt`; their names alone do not establish all contents, execution boundaries, and consumers. No hello path from `user-closure-outside-system.txt` appears in this particular saved listing; the two inventories must not be silently conflated.
- `nixos-76634f69cd` (338 members, paths relative to `/boot/grub`): MUST applies to the 274 `i386-pc/*.mod` loadable GRUB modules and the containing `i386-pc` and group directories (276 members). NOT applies to `fonts/unicode.pf2`, the 43 `locale/*.mo` translation catalogs, and their `fonts` and `locale` directories (46 members). UNKNOWN applies to all remaining 16 inventoried members; saved contents and consumers do not establish their individual local roles. The module functions, command implementations, filesystem drivers, and loader support run within the bootloader's authority; they are not documents.
- `nixos-0075a76d48` (11 members, paths relative to `/etc/ssh`): MUST applies to the account-specific authorized-key file, its `authorized_keys.d` directory, and the group directory (3 members), because removing them removes login-key availability. UNKNOWN applies to the two private host-key files, two public host-key files, and the `moduli`, `ssh_config`, `ssh_known_hosts`, and `sshd_config` links (8 members). This retains uncertainty about their particular local consumers, policy contents, and effects rather than assuming they are exempt.
- `nixos-b86fee9a16` (21 members, paths relative to `/etc/systemd`): MUST applies to `system-environment-generators/env-generator`, its `system-environment-generators` directory, and the group directory (3 members). UNKNOWN applies to all other 18 members: the two preset directories, two preset links, eight `.conf` links, `generator-environment.json`, and the five service/generator/shutdown-tree links. The actual preset and daemon settings and the target tree members were not saved. The known generator is executed by the manager and exports environment to services.

Additional primary documentation:

- https://www.gnu.org/software/grub/manual/grub/grub.html — “Modules can be loaded via the `insmod` (see insmod) command.”
- https://www.gnu.org/software/gettext/manual/gettext.html — “messages are converted to UTF-8 encoding before being stored in a MO file”.
- https://man.openbsd.org/sshd — “`AuthorizedKeysFile` specifies the files containing public keys for public key authentication”.
- https://www.freedesktop.org/software/systemd/man/254/systemd.environment-generator.html — “Generators are small executables”; “before starting any units.”
