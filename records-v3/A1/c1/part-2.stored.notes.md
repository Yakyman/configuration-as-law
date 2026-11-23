# c1 part 2: stored-object classification

Scope: 253 rows of kinds `package-owned-paths`, `stored`, and `stored-directory-skeleton`. No other classification was consulted. No object was removed and no probe was run. File types, sizes, symlink targets, and group membership come from `../in/raw/debian/files.tsv`, `package-files.txt`, `unowned-groups.json`, and `directory-only-groups.json`. Package groups were reconstructed by assigning each owned pathname to its longest matching input group; every reconstructed count equals the input's `members` count. For stored rows, the raw group membership is used even when the input's `members` column is 1: the evidence itself identifies a group containing more objects. No implication is drawn from inventory classification terminology.

The output was appended as cases were settled. Refinement corrected an initially overbroad directory HOLE reading to factual UNKNOWN, and removed database-content HOLE readings where functional dependence is established. These are c1's own intermediate corrections, not consultation of an earlier classification. The final TSV is authoritative; the construction and refinement scripts preserve the process.

## Governing sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-6: “records of the past—logs, history;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

An operational database is not exempt merely because it is a database: S2.2-4 requires unchanged capability. Shared library tables and systemwide policy are not confined to one program. Merely storing a file under a cache directory does not establish the conditional cache exemption. In particular the dynamic linker cache is UNKNOWN because library locations and cache entries were not collected; the auxiliary ldconfig cache has a documented optional role.

## Homogeneous rules and ten manual checks

Rule D: directory-only objects receive UNKNOWN (S3-1, S3-2). The observed fact is namespace storage. The inventory does not establish the directory's independent functional dependency or reconstruction after absence. A pathname becoming unavailable is not by itself sufficient: S2.2-4 already distinguishes content unavailability from lost capability. No automatic inference from package ownership, conventional directory name, or nonzero directory size is made. The same uncertainty is explicitly retained for directory members in heterogeneous groups. This is a conservative evidence limitation, not a textual hole.

Ten individually checked cases against `files.tsv` intersected with `package-files.txt`:

| ID | Manual inspection |
| --- | --- |
| debian-c0faa16997 | binfmt.d is only a directory entry, without a collected rule in this group. |
| debian-7642c049c2 | ca-certificates and update.d are both directories; no hook body occurs in the group. |
| debian-ec5f04bd95 | dbus-1, session.d, system.d are directory entries; no policy payload occurs in this group. |
| debian-35fa9d83db | gss and mech.d are directory entries without mechanism definitions. |
| debian-b69b9d321c | modprobe.d has one directory entry; actual unowned policy is a separate row. |
| debian-5c3528c19a | netplan has one directory entry; network YAML is in a separate row. |
| debian-ad79f60794 | polkit-1 and rules.d are directories, with no rule body in this group. |
| debian-1d27c32fa0 | rc0.d here contains only the directory object; service links form a separate stored row. |
| debian-0b197a23e7 | rc1.d here contains only the directory object; service links form a separate stored row. |
| debian-cadf3ec932 | rc2.d here contains only the directory object; service links form a separate stored row. |

Rule L: identified log/history payloads receive NOT under S2.2-6. This rule applies only to payloads whose event-recording role is established, not every path under a log directory. The README is separately content, and the journal group is MIXED because it also contains directories.

Ten manually checked input IDs and raw payload roles:

| ID | Manual inspection |
| --- | --- |
| debian-83df02e6eb | eipp.log.xz, history.log, term.log record package operations. |
| debian-9c96b64591 | btmp records failed login attempts. |
| debian-93b020b2d3 | cloud-init-output.log records provisioning command output. |
| debian-2954505d9d | cloud-init.log records provisioning events. |
| debian-6f5cf081f0 | dpkg.log records package management events. |
| debian-8dc29397cf | faillog records login failures. |
| debian-698c23461f | lastlog records previous account logins. |
| debian-dea214b7e3 | unattended-upgrades-shutdown.log records upgrade shutdown events. |
| debian-d6ce9987c3 | wtmp records login/session history. |
| debian-917d8d1269 | resolver .bak file preserves previous configuration, rather than the active resolver symlink. |

All other cases have individual records in the construction/refinement scripts and final TSV; no ownership-wide rule assigns a decision to heterogeneous groups. Short MIXED reasons enumerate member categories. “Directory dependency: UNKNOWN” means each directory member, not a missing classification of the group.

## Documentation and quoted functional evidence

The inventory establishes which object exists; these primary manuals establish its role. Quotes are deliberately short. URLs are linked here for compact rows whose basis points to inventory membership.

- [Linux pathname resolution](https://manpages.debian.org/bookworm/manpages/path_resolution.7.en.html): “If the component is not found, an ENOENT error is returned”. This establishes namespace mechanics, not whether an application requires an observed directory.
- [Filesystem hierarchy](https://manpages.debian.org/bookworm/manpages/hier.7.en.html): “Contains static files for the boot loader.” The conventional role of a directory alone does not establish every observed inode's independent effect.
- [Bash](https://manpages.debian.org/bookworm/bash/bash.1.en.html): “executes commands read from the standard input or from a file.” Supports shell startup and executable hook cases.
- [Nano configuration](https://manpages.debian.org/bookworm/nano/nanorc.5.en.html): “The nanorc files contain the default settings for nano”. Supports both editor preference rows.
- [Account creation configuration](https://manpages.debian.org/bookworm/adduser/adduser.conf.5.en.html): “contains defaults for the programs”. The named programs include account creation and deletion utilities; the file is not confined to one program.
- [APT configuration](https://manpages.debian.org/bookworm/apt/apt.conf.5.en.html): “shared by all the tools in the APT suite of tools”. Shared repository/installation policy is distinguished from listchanges display preferences.
- [dpkg](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html): “dpkg keeps its record of available packages in /var/lib/dpkg/available.” Active records govern package handling; the content exemption is not assumed.
- [Alternatives](https://manpages.debian.org/bookworm/dpkg/update-alternatives.1.en.html): “maintain symbolic links determining default commands”. Raw links to executable paths and links to manual pages are distinguished.
- [Initramfs scripts](https://manpages.debian.org/bookworm/initramfs-tools-core/initramfs-tools.7.en.html): “has one main script and two different sets of subscripts”. Supports early boot code and hook roles.
- [Dynamic loader](https://manpages.debian.org/bookworm/manpages/ld.so.8.en.html): “contains a compiled list of candidate shared objects previously found in the augmented library path.” The cache is not blindly treated as speed-only.
- [ldconfig](https://manpages.debian.org/bookworm/manpages/ldconfig.8.en.html): “Ignore auxiliary cache file.” Supports the auxiliary metadata cache exemption.
- [Manual index](https://manpages.debian.org/bookworm/man-db/mandb.8.en.html): “create or update the manual page index caches”. Cache roles are distinguished from the auto-update enabling marker.
- [Manual package installation script](https://sources.debian.org/src/man-db/2.11.2-2/debian/postinst/): `if [ ! -e /var/lib/man-db/auto-update ]; then`. The branch reports “Not building database”; marker removal skips a real operation.
- [Debconf](https://manpages.debian.org/bookworm/debconf-doc/debconf.7.en.html): “Debconf is a configuration system for Debian packages.” Current answers are operational configuration, templates are question text, old copies are historical.
- [PAM generation](https://manpages.debian.org/bookworm/libpam-runtime/pam-auth-update.8.en.html): “configuring the central authentication policy for the system”. Supports systemwide effects of PAM inputs and generation state.
- [Password history](https://manpages.debian.org/bookworm/libpam-modules/pam_pwhistory.8.en.html): “The last N passwords for each user are saved in /etc/security/opasswd.” Unlike the conditional content exception, the past-record exception is unqualified, motivating the specific operative-history HOLE.
- [Shadow](https://manpages.debian.org/bookworm/passwd/shadow.5.en.html): “contains the password information for the system's accounts and optional aging information.” A single file combines explicitly exempt secrets with access policy; removing the whole file loses that policy, so it is MUST.
- [Group shadow](https://manpages.debian.org/bookworm/passwd/gshadow.5.en.html): “Administrators can change the password or the members of the group.” Membership authority and password fields occupy one object; whole-object removal loses the authority policy, so it is MUST.
- [SSH server configuration](https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html): “OpenSSH daemon configuration file”. Account access and listening-port rules have explicit treatment in S2.2-15.
- [Configuration preservation](https://manpages.debian.org/bookworm/ucf/ucf.1.en.html): “preserve user changes in configuration files”. Active merge baselines change conflict handling; numbered backups are past copies.
- [Python policy](https://www.debian.org/doc/packaging-manuals/python-policy/): “allows configuration how modules should be byte-compiled.” The inventory's Python configuration participates in package module processing, rather than executable application source.
- [Login shell registration](https://manpages.debian.org/bookworm/debianutils/update-shells.8.en.html): “To track changes made by the administrator, it consults a state file”. This establishes the operative past-state boundary rather than assuming a passive database.
- [Cloud first boot](https://docs.cloud-init.io/en/latest/explanation/first_boot.html): “stores a cache of its internal state for use across stages and boots.” The documented role determines whether per-instance configuration runs; this is not a speed-only cache.
- [User lingering](https://manpages.debian.org/bookworm/systemd/loginctl.1.en.html): “a user manager is spawned for the user at boot and kept around after logouts.” Supports the MUST member of the systemd state group.
- [AppArmor parser](https://manpages.debian.org/bookworm/apparmor/apparmor_parser.8.en.html): “specify the default options for the parser”. Compiled policy cache is regenerable; kernel access profiles are operative policy.
- [Groff](https://manpages.debian.org/bookworm/groff-base/groff.1.en.html): “Unsafe mode. Reverts to the (old) unsafe behaviour”. Missing macro contents and execution mode prevent deciding code confinement.
- [Screen](https://manpages.debian.org/bookworm/screen/screen.1.en.html): “creates a single window with a shell in it”. The program has settings and command execution; the collected file contents are insufficient to separate them.

Additional primary manuals for shared mappings and policy:

| Function | Source and quoted identification |
| --- | --- |
| Resolver policy | [host.conf](https://manpages.debian.org/bookworm/manpages/host.conf.5.en.html): “resolver configuration file” |
| Address selection | [gai.conf](https://manpages.debian.org/bookworm/manpages/gai.conf.5.en.html): “getaddrinfo(3) configuration file” |
| Network service names | [services](https://manpages.debian.org/bookworm/manpages/services.5.en.html): “Internet network services list” |
| Protocol names | [protocols](https://manpages.debian.org/bookworm/manpages/protocols.5.en.html): “protocols definition file” |
| RPC transport definitions | [netconfig](https://manpages.debian.org/bookworm/libtirpc-common/netconfig.5.en.html): “network configuration data base” |
| Audit library settings | [libaudit.conf](https://manpages.debian.org/bookworm/libaudit-common/libaudit.conf.5.en.html): “libaudit configuration file” |
| User namespace delegation | [subuid](https://manpages.debian.org/bookworm/passwd/subuid.5.en.html): “configuration for subordinate user ids” |

## Group details and limitations

The bootloader group contains EFI executables and configuration references; the GRUB group includes module binaries, loader images, `.lst` lookup files, configuration, one font, translations, and directories. The font and translation payloads are presentation content; loader/module lookup files support actual boot execution. The alternatives group contains 102 symlinks: executable-target aliases are distinguished from documentation-target aliases.

The package-state group contains maintainer scripts, active status/available information, alternatives/diversions/statoverride/trigger data, old copies, locks, and one directory. Current operational metadata is MUST; `.old`/`-old` copies are NOT; lock lifecycle and cmethopt contents remain UNKNOWN. Mere `.list` or checksum text being database-like is not used to exempt metadata required by removal/verification operations.

The provisioning-state group contains known result/history files, per-instance execution semaphores, identity metadata, saved data of unknown contents, and directories. No assumption is made that every saved user-data file is executable or that a serialized object is benign content. The system-manager state group includes an explicit lingering entry, timestamps and enablement records, a message catalog, a random seed, and directories. The random seed's precise contribution is not inferred from the pathname alone.

For configuration files supporting both internal values and executable actions (screen, logrotate) the absence of contents yields UNKNOWN, not a manufactured textual conflict. The remaining HOLE cases state specific textual boundaries in the TSV; none is based on Section 2.5 design questions.

## Final review corrections

The formatter defaults file is NOT under S2.2-7/13: the defaults are applied inside the formatter; its output filesystem does not continue reading those settings. [mke2fs.conf](https://manpages.debian.org/bookworm/e2fsprogs/mke2fs.conf.5.en.html) states: “Contains relations which influence how mke2fs behaves.”

The shadow and group-shadow objects are MUST because whole-file removal loses required lock/expiry or administration/membership policy, regardless of exempt password fields. The APT mirrors directory uses the same UNKNOWN dependency treatment as other directory members.

The successful-sudo marker is NOT, correcting an unsupported assumption about an advisory consumer. [sudoers](https://manpages.debian.org/bookworm/sudo/sudoers.5.en.html) describes admin_flag as a file “created the first time a user” runs sudo. [Distribution bug 1012276](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1012276) explains that the advice consumer was absent from the distribution shell setup. This historical bug does not prove the inventoried shell contents; it does disprove assuming the advice behavior from the filename alone. The established function is the past-use record. No observed consumer supplies a conflicting active function.

Local magic override correction: debian-3058cb94e3 and debian-4ddca1eeaa are UNKNOWN, replacing the unsupported one-program exemption. [The recognition library manual](https://manpages.debian.org/bookworm/libmagic-dev/libmagic.3.en.html) identifies a “Magic number recognition library”. [The distribution patch archive](https://deb.debian.org/debian/pool/main/f/file/file_5.44-3.debian.tar.xz), patch local.support-local-definitions-in-etc-magic.patch, sets the library default path to include `/etc/magic`. [The upstream source archive](https://deb.debian.org/debian/pool/main/f/file/file_5.44.orig.tar.gz), src/apprentice.c, documents “Compatibility with old code that looked in .mime” and constructs the MIME variant for MAGIC_MIME loading. This establishes shared-library scope. Both observed files are 111 bytes, however, and the inventory captures no contents. The conffile checksums are package database metadata, not independently measured current file hashes. Consequently effective local rules cannot be distinguished from comment-only placeholders. Neither NOT for one-program scope nor MUST for assumed rules is warranted.
