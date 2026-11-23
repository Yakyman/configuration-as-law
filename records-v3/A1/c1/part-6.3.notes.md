# Part 6, c1 subset 3

Scope: 54 stored-object rows from the supplied part, excluding boot and system configuration directories. Only the task input, the fixed text and public primary documentation were consulted. Raw inventory files are unavailable. No object was removed. Directory counts in evidence include entries not enumerated by the sample; large incomplete groups remain UNKNOWN. No inference of file contents from an upstream sample is made.

## Scripted rule: logs

S2.2-6: "records of the past—logs, history;"

A row explicitly identifying an event log or login history is NOT. The completion-marker file is excluded because its control-flow role is unknown. Hand-checked cases: freebsd-3f3dc85096 (authentication log), freebsd-1a6382c15a (scheduler log), freebsd-17935511d8 (daemon log), freebsd-3577a2c8c2 (debug log), freebsd-71ac7977fa (device-event log), freebsd-a3218f48ea (printing error log), freebsd-063e60271f (mail log), freebsd-91a21a61f1 (system messages), freebsd-bf93d84cc6 (initialization log), freebsd-c1a31fd033 (connection log). Each is one named log, not an arbitrary directory. Login histories were separately checked against https://man.freebsd.org/cgi/man.cgi?query=utmpx&format=html: "Log of all entries, sorted by date of addition."

Every remaining row was decided individually; the serialization script only writes those explicit decisions.

## Primary documentation and supporting passages

- https://man.freebsd.org/cgi/man.cgi?query=sh&format=html: "A login shell first reads commands from the files /etc/profile"; "Default shell resources." The manual describes the profile, ENV and shell-resource execution mechanism.
- https://man.freebsd.org/cgi/man.cgi?query=tcsh&format=html: "Non-login shells read only /etc/csh.cshrc and ~/.tcshrc or ~/.cshrc on startup." Login startup also executes the login file.
- https://man.freebsd.org/cgi/man.cgi?query=vi&format=html: "Execute an ex command." The manual identifies the ex startup files; the inventory independently reports the executed `set number` command. S2.2-13 makes this code despite its setting purpose.
- https://man.freebsd.org/cgi/man.cgi?query=mail&format=html: "commands in the user's personal command file ~/.mailrc are executed"; "Executes the shell". The command language is not confined to displaying mail.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/skel/dot.mail_aliases: ".mail_aliases - private mail aliases". This establishes intended purpose only; actual contents and sourcing are unavailable.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/skel/dot.mailrc: "source ~/.mail_aliases". This documents the default sourcing mechanism, not the actual installed contents.
- https://man.freebsd.org/cgi/man.cgi?query=login.conf&format=html: "this file is used by login(1) to set user-defined environment settings". These settings propagate into the login session, beyond one program.
- https://man.freebsd.org/cgi/man.cgi?query=sshd&format=html: "AuthorizedKeysFile specifies the files containing public keys for public key authentication". The inventory identifies authorized-key files.
- https://man.freebsd.org/cgi/man.cgi?query=k5login&format=html: "Anyone with valid tickets for a principal in the file is allowed host access with the UID of the user".
- https://man.freebsd.org/cgi/man.cgi?query=pam.conf&format=html: "The PAM library searches for policies in the following files, in decreasing order of preference". The inventory identifies the privilege tool's PAM policy.
- https://man.freebsd.org/cgi/man.cgi?query=pkg.conf&format=html: "pkg.conf is the system-wide configuration file used by the pkg(8) tools." Its actual directives are not provided.
- https://man.freebsd.org/cgi/man.cgi?query=sudo.conf&format=html: "It is used to configure sudo plugins, plugin-agnostic path names, debug flags, and other settings." Actual enabled directives are unknown.
- https://man.freebsd.org/cgi/man.cgi?query=sudo_logsrvd.conf&format=html: "The sudo_logsrvd.conf file is used to configure the sudo_logsrvd log server." Configuration can involve listening addresses, storage and logging; actual values are unavailable.
- https://man.freebsd.org/cgi/man.cgi?query=sudoers&format=html: "The sudoers policy plugin determines a user's sudo privileges." Applies to the main policy and included policy directory.
- https://man.freebsd.org/cgi/man.cgi?query=pkg-clean&format=html: "Delete all cached packages including those which have not been superseded by newer versions yet and are still in use." Downloaded archive copies are distinct from installed executable programs.
- https://man.freebsd.org/cgi/man.cgi?query=savecore&format=html: "the copies are not attempted." This is the documented consequence of the minimum-free-space threshold. The setting governs only savecore's dump-saving operation.
- https://man.freebsd.org/cgi/man.cgi?query=dhclient&format=html: "if they are determined to be valid, they are used until either they expire or the DHCP server becomes available." Saved leases enable network use without a responding server. Actual lease validity is not supplied.
- https://man.freebsd.org/cgi/man.cgi?query=etcupdate&format=html: "To perform a three-way merge, etcupdate keeps copies of the current and previous versions of files that it manages." The inventory gives only four samples of hundreds of members.
- https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&format=html: "temporary files, downloaded updates, and files required for rollback." This broad directory is not established as homogeneous from its four samples.
- https://man.freebsd.org/cgi/man.cgi?query=mergemaster&format=html: "Location to store the list of mtree values for AUTO_UPGRADE purposes". Historical file fingerprints provide a baseline for detecting local changes.
- https://man.freebsd.org/cgi/man.cgi?query=services&format=html: "If \"db\" is specified as source in the nsswitch.conf(5), /var/db/services.db is searched." Neither the lookup configuration nor fallback behavior on this machine is supplied.
- https://man.freebsd.org/cgi/man.cgi?query=msgs&format=html: "an error will be displayed if /var/msgs/bounds does not exist." This bounds file is functional metadata; the given sample contains it.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/usr.sbin/ypserv/Makefile.yp: "These are commands which this Makefile needs to properly rebuild the NIS databases." The supplied directory contains the makefile and its symlink; make executes recipes with caller rights.
- https://man.freebsd.org/cgi/man.cgi?query=nuageinit&format=html: "because the user_data provided is a script." The cached user-data file can instead contain configuration values, so its name does not establish its contents.

## Limits of inference

Shell startup files and policy/key files have documented functional roles identified by their standard filenames. Whether a file contains active directives, rather than comments, matters most where the documented format mixes materially different categories; those cases are UNKNOWN here. The private alias file is not established as sourced on this installation. The large shared-data, update, package-database and runtime groups do not have full member listings. The bootstrap completion and cleanup marker names have no supplied producer/consumer code.

## Exact fixed-text sentences cited

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.
