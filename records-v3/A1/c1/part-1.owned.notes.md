# Package-owned path classification

Membership is the normalized intersection of `files.tsv` and `package-files.txt`, applying `path-aliases.tsv`. Nested input groups are excluded from ancestor groups. All 237 member counts agree after normalization. Package ownership is never a recording criterion. Filesystem contents were not collected: the raw file table supplies type, path, link target, and size only.

## Directory-only rule

For rows consisting solely of directory entries, the inventory establishes a namespace container but not operational consumers or reconstruction behavior. General directory-purpose documentation does not establish these instances’ actual functional dependence. These are UNKNOWN under S3-2, not a presumption that empty directories are content. No physical removal is performed.

Manual checks: coreos-3cd182c07b, coreos-827c5914e9, coreos-037231a728, coreos-d3d071d2ba, coreos-c0faa16997, coreos-43399114f3, coreos-edd98ae366, coreos-fc1b65b090, coreos-31a0673933, coreos-1ae98d3e98. Each has one member with raw type d and no supplied contents or consumer trace.

General source: https://man7.org/linux/man-pages/man7/hier.7.html — “A typical Linux system has, among others, the following directories:” This describes typical layout, not operational use on this instance.

## Individually consulted sources

- https://man7.org/linux/man-pages/man5/dir_colors.5.html — “The program ls(1) uses the environment variable LS_COLORS”; “configuration file for dircolors(1)”
- https://man7.org/linux/man-pages/man5/adjtime.5.html — “hardware mode clock setting and clock drift factor”
- https://man7.org/linux/man-pages/man5/aliases.5.html — “an alias can refer to other aliases”
- https://man7.org/linux/man-pages/man1/bash.1.html — “executes commands read from the standard input, from a string, or from a file”
- https://man7.org/linux/man-pages/man5/host.conf.5.html — “configuration information specific to the resolver library”
- https://man7.org/linux/man-pages/man5/hosts.5.html — “associates IP addresses with hostnames”
- https://man7.org/linux/man-pages/man5/exports.5.html — “Each file system in this table has a list of options and an access control list.”
- https://man7.org/linux/man-pages/man5/group.5.html — “defines the groups on the system”
- https://man7.org/linux/man-pages/man5/passwd.5.html — “describes user login accounts for the system”
- https://man7.org/linux/man-pages/man5/gshadow.5.html — “contains the shadowed information for group accounts”
- https://man7.org/linux/man-pages/man5/shadow.5.html — “contains the password information for the system's accounts and optional aging information”
- https://man7.org/linux/man-pages/man5/ld.so.conf.5.html — “a list of directories, one per line, in which to search for libraries”
- https://man7.org/linux/man-pages/man5/libaudit.conf.5.html — “configuration information for user space applications that link to libaudit”
- https://man7.org/linux/man-pages/man5/locale.conf.5.html — “configures system-wide locale settings”
- https://man7.org/linux/man-pages/man5/login.defs.5.html — “defines the site-specific configuration for the shadow password suite”
- https://man7.org/linux/man-pages/man8/logrotate.8.html — “allows automatic rotation, compression, removal, and mailing of log files”
- https://man7.org/linux/man-pages/man5/machine-id.5.html — “contains the unique machine ID of the local system”
- https://man7.org/linux/man-pages/man5/mke2fs.conf.5.html — “controls the default parameters used by mke2fs(8)”
- https://man7.org/linux/man-pages/man5/networks.5.html — “describes known DARPA networks and symbolic names for these networks”
- https://man7.org/linux/man-pages/man5/nfs.conf.5.html — “site-specific configuration for various NFS daemons and other processes”
- https://man7.org/linux/man-pages/man5/nfsmount.conf.5.html — “section headers followed by variable assignments associated with that section”
- https://man7.org/linux/man-pages/man5/protocols.5.html — “describing the various DARPA internet protocols”
- https://man7.org/linux/man-pages/man5/request-key.conf.5.html — “determine which program it should run to instantiate a key”
- https://man7.org/linux/man-pages/man5/rpc.5.html — “names that can be used in place of RPC program numbers”
- https://man7.org/linux/man-pages/man5/rsyncd.conf.5.html — “controls authentication, access, logging and available modules”
- https://man7.org/linux/man-pages/man5/sestatus.conf.5.html — “determine what file and process security contexts should be displayed”
- https://man7.org/linux/man-pages/man5/shells.5.html — “full pathnames of valid login shells”
- https://man7.org/linux/man-pages/man5/subgid.5.html — “authorizes a group id to map ranges of group ids”
- https://man7.org/linux/man-pages/man5/subuid.5.html — “authorizes a user id to map ranges of user ids”
- https://man7.org/linux/man-pages/man5/sudo.conf.5.html — “used to configure the sudo front-end”
- https://man7.org/linux/man-pages/man5/sudoers.5.html — “determines a user's sudo privileges”
- https://man7.org/linux/man-pages/man5/sysctl.conf.5.html — “contain Linux kernel configuration parameters”
- https://man7.org/linux/man-pages/man5/vconsole.conf.5.html — “configures the virtual console, i.e. keyboard mapping and console font”
- https://man7.org/linux/man-pages/man5/issue.5.html — “contains a message or system identification to be printed before the login prompt”
- https://man7.org/linux/man-pages/man5/motd.5.html — “displayed by login(1) after a successful login”
- https://man7.org/linux/man-pages/man5/os-release.5.html — “contain operating system identification data”

Each single-file entry above was decided individually; the script only serializes the written decisions.

## Individually inspected grouped objects

The member table `part-1.owned.members.tsv` gives every member’s decision. Ordinals use the order of normalized intersection entries in raw `files.tsv`, excluding nested groups. Paths are intentionally not duplicated. Directory members are UNKNOWN unless they are ancestors necessary to reach a classified MUST member; such ancestors are MUST because removing them removes access to that required object. Unused sibling directories remain UNKNOWN. The table below records the individually selected file classes and exceptions; these selections are not a classifier inferred from package ownership.

Ancestor checks by hand: coreos-9945c88deb (dispatcher script), coreos-0a38e83850 (session shell script), coreos-47cc2958ff (completion scripts), coreos-96885714dc (backend policy links), coreos-ec5f04bd95 (bus configuration), coreos-4f3962b16e (account defaults), coreos-b91b989f2d (generator scripts), coreos-8265490c79 (library path configuration), coreos-cbdd239882 (authentication stacks), coreos-2f70798fb0 (shell startup scripts). In each, direct pathname prefixes identify exactly the needed containing directories; sibling directories do not inherit the child’s decision.

- coreos-1d70ce548d: Provides boot menu code, boot variables, and display font. MUST=3, NOT=1, UNKNOWN=1.
- coreos-9945c88deb: Configures network management and executes network-event hooks. MUST=4, UNKNOWN=7.
- coreos-0a38e83850: Runs session-startup shell integration. MUST=4, UNKNOWN=3.
- coreos-a4c2c16ae9: Sets kernel audit rules and audit-daemon preferences. HOLE=1, MUST=5, UNKNOWN=1.
- coreos-e2885ad43a: Supplies authentication stacks and name-service selection. MUST=7, UNKNOWN=4.
- coreos-47cc2958ff: Executes shell completion functions. MUST=3.
- coreos-8ff1651d76: Selects an identity-mapping plugin through a symbolic link. UNKNOWN=2.
- coreos-3a7a7fb965: Configures container-runtime behavior. HOLE=1, UNKNOWN=1.
- coreos-c2d2685965: Stores container trust, registry, and toolbox configuration. UNKNOWN=15.
- coreos-96885714dc: Distributes cryptographic policy to multiple program backends. MUST=18, UNKNOWN=3.
- coreos-ec5f04bd95: Configures message-bus connectivity and interprocess access policy. MUST=5, UNKNOWN=1.
- coreos-4f3962b16e: Supplies defaults used when creating accounts. MUST=2.
- coreos-05942fe9ff: Stores package-manager configuration and explanatory documentation. HOLE=9, NOT=1, UNKNOWN=10.
- coreos-e9bcb7e1df: Stores firmware-update daemon settings and explanatory documentation. HOLE=5, NOT=1, UNKNOWN=3.
- coreos-b91b989f2d: Executes boot-configuration generator scripts and includes explanatory documentation. MUST=13, NOT=1.
- coreos-35fa9d83db: Configures an authentication mechanism plugin. UNKNOWN=3.
- coreos-89042bc9be: Stores authentication-proxy configuration. UNKNOWN=3.
- coreos-95865da962: Provides explanatory documentation for networking configuration. NOT=1, UNKNOWN=1.
- coreos-d33aabe318: Stores storage-session daemon configuration. UNKNOWN=2.
- coreos-85898eb196: Supplies integrity-verification certificates. MUST=10.
- coreos-5fd4dee5c3: Provides an example terminal configuration. NOT=1.
- coreos-3368ad3458: Includes shared authentication and cryptography configuration. MUST=3.
- coreos-8265490c79: Adds shared-library discovery directories. MUST=2.
- coreos-a17631eb59: Selects block-device library configuration. UNKNOWN=3.
- coreos-66ca6c2372: Stores driver-selection values for userspace RDMA. UNKNOWN=19.
- coreos-ee7f18d46b: Supplies network library identifier tables. UNKNOWN=3.
- coreos-f5454e1609: Stores event-handler configuration. UNKNOWN=6.
- coreos-1af8073cda: Configures log processing, potentially including executed hook code. UNKNOWN=9.
- coreos-a45be4a17a: Stores volume-manager defaults and optional profiles. HOLE=10, UNKNOWN=6.
- coreos-20d5a4dc7b: Stores firewall rule files and operating-system fingerprint data. UNKNOWN=6.
- coreos-34af1b92eb: Provides explanatory network-state documentation. NOT=1, UNKNOWN=1.
- coreos-ae5247403a: Stores storage-discovery configuration. UNKNOWN=2.
- coreos-1ef6a866b0: Supplies defaults shared by LDAP clients. MUST=2, UNKNOWN=1.
- coreos-cbdd239882: Defines authentication and account-access stacks. MUST=22.
- coreos-17a7caf72b: Stores trust anchors, cryptographic configuration, scripts, and explanatory documents. MUST=368, NOT=7, UNKNOWN=563.
- coreos-2f70798fb0: Executes shell initialization scripts. MUST=29.
- coreos-5d89e4193b: Provides explanatory initialization documentation. NOT=1, UNKNOWN=2.
- coreos-d159c2f1cf: Selects helpers for kernel key requests. MUST=4.
- coreos-29ef947721: Stores writable-filesystem setup descriptions. UNKNOWN=4.
- coreos-38d62d7f56: Stores file-sharing configuration and a sample configuration. NOT=1, UNKNOWN=3.
- coreos-aaa1adf124: Controls authentication, account resources, namespaces, and password history. HOLE=1, MUST=13, UNKNOWN=3.
- coreos-c9f542a45c: Stores access-control policy, labels, and compiled label caches. MUST=43, NOT=2, UNKNOWN=2.
- coreos-4c24122c97: Supplies shell startup code copied into new accounts. MUST=4.
- coreos-c366c1919d: Controls login access and SSH client behavior. HOLE=3, MUST=7, UNKNOWN=2.
- coreos-5f604fda76: Exposes shared trust bundles and cryptographic configuration. MUST=6, NOT=1, UNKNOWN=2.
- coreos-cc6acfb8b2: Exposes software-identification metadata. NOT=1, UNKNOWN=2.
- coreos-0fea41ffe5: Stores firewall policy and service-startup options. MUST=5, UNKNOWN=11.
- coreos-2b4fe000fc: Exposes persistent kernel parameter configuration. MUST=2.
- coreos-0c7a1a4d1e: Stores TPM library configuration and cryptographic profiles. UNKNOWN=7.
- coreos-ec7d8d80c0: Supplies compiled hardware properties for device setup. MUST=2, UNKNOWN=2.
- coreos-3da21e28f6: Stores disk-management settings and a sample configuration. NOT=1, UNKNOWN=3.
- coreos-3eb238bafa: Exposes desktop autostart and user-service search locations. UNKNOWN=4.
- coreos-b656843499: Sets software package repository sources. HOLE=5, UNKNOWN=1.
- coreos-e2cc7e7fb6: Stores an auxiliary cache for rebuilding the library index. NOT=1, UNKNOWN=1.
- coreos-e48d7a5dbe: Persists measured clock drift used for future time correction. HOLE=1, UNKNOWN=1.
- coreos-a51d3ac08b: Provides a package-manager locking object. UNKNOWN=2.
- coreos-94db10583a: Exposes an authentication-proxy socket and storage directories. UNKNOWN=4.
- coreos-89229e49e6: Stores message catalog data, boot entropy seed, and service-state directories. MUST=2, NOT=1, UNKNOWN=3.

## Additional primary-source evidence and limits

The following short passages establish functions used in the grouped partitions and remaining individual rows. Inventory paths determine membership; documents determine the programs’ handling of these object formats. A format that permits several materially different uses does not establish the actual contents of an uncollected file. UNKNOWN is used where that distinction matters.

- https://man7.org/linux/man-pages/man7/audit.rules.7.html — “a file containing audit rules that will be loaded by the audit daemon's init script”. Audit rules govern kernel recording, not the historical log output.
- https://man7.org/linux/man-pages/man5/auditd.conf.5.html — “configuration information specific to the audit daemon”. The daemon preferences have the inside/outside ambiguity, unlike kernel audit rules.
- https://www.networkmanager.dev/docs/api/latest/NetworkManager-dispatcher.html — “NetworkManager will wait for script execution to complete”. Dispatcher hooks are executed code. Empty sibling directories have no established operational contents.
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html — “Multiple programs connect to the message bus daemon and can exchange messages with one another.” Bus access policy governs communication between processes.
- https://man7.org/linux/man-pages/man8/useradd.8.html — “creates a new user account using the values specified on the command line plus the default values from the system.” Account defaults control system accounts.
- https://man7.org/linux/man-pages/man5/dnf.conf.5.html — “all *.repo files found under /etc/yum.repos.d”. Repository selection is operational input to package management; its treatment as one program’s values versus external system control is not specified.
- https://man7.org/linux/man-pages/man5/dracut.conf.5.html — “Each line specifies an attribute and a value.” Values affect construction of a later boot environment; one-program scope remains ambiguous.
- https://man7.org/linux/man-pages/man8/pam_env.8.html — “allows the (un)setting of environment variables”. Session values propagate to child applications; this is not a single editor’s presentation preference.
- https://man7.org/linux/man-pages/man5/pam.d.5.html — “These files list the PAMs that will do the authentication tasks required by this service”. The stacks implement login and account checks.
- https://man7.org/linux/man-pages/man5/ldap.conf.5.html — “used to set system-wide defaults to be applied when running ldap clients”. These values are shared across clients.
- https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html — “defaults for the current realm and for Kerberos applications”. The same source documents included files; the authentication configuration spans applications.
- https://man7.org/linux/man-pages/man8/selinux.8.html — “an implementation of a flexible mandatory access control architecture in the Linux operating system.” Access-control policy and labeling inputs govern system-wide permissions.
- https://man7.org/linux/man-pages/man8/pam_pwhistory.8.html — “saves the last passwords for each user in order to force password change history”. The saved password history is both a past record and input restricting future passwords: S2.2-6 versus S2.2-1/S2.2-15 has no stated treatment for the dual role.
- https://man7.org/linux/man-pages/man5/sshd_config.5.html — “sshd(8) reads configuration data from /etc/ssh/sshd_config”. Login restrictions are explicitly required. Client configuration remains a scope ambiguity; the uncollected moduli’s operational dependence is left UNKNOWN.
- https://man7.org/linux/man-pages/man7/hwdb.7.html — “used primarily by udev to add the relevant properties to matching devices”. The compiled database supplies device properties affecting other programs; being compiled alone is not the cache exemption.
- https://man7.org/linux/man-pages/man8/systemd-random-seed.service.8.html — “loads an on-disk random seed into the kernel entropy pool during boot and saves it at shutdown”. The seed contributes to future system randomness, not merely display content.
- https://chrony-project.org/doc/latest/chrony.conf.html — “The driftfile directive allows a file to be specified into which chronyd can store the rate information.” Clock configuration controls system time. Stored drift is a past measurement reused for future correction; removing it causes relearning, and the text does not distinguish this from exempt cache or history.
- https://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html — “a lightweight DNS, TFTP, PXE, router advertisement and DHCP server.” Server configuration changes network facilities available to other programs and machines.
- https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano”. Its documented settings and interface commands fall within the single-program setting exemption.
- https://man7.org/linux/man-pages/man5/services.5.html — “a mapping between human-friendly textual names for internet services, and their underlying assigned port numbers and protocol types.” Lookup data is operational across network clients; entries are not themselves open ports.
- https://man7.org/linux/man-pages/man8/lastlog.8.html — “prints the contents of the last login log”. The corresponding file is historical information.
- https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html — “This file lists all the filesystems currently mounted in the process's mount namespace”. The mount-table link exposes live state rather than a historical record.
- https://man7.org/linux/man-pages/man8/ld.so.8.html — “find and load the shared objects (shared libraries) needed by a program”. The main loader cache can identify libraries outside fallback directories: without its entries, the speed-only condition is unproved.
- https://man7.org/linux/man-pages/man8/ldconfig.8.html — “creates the necessary links and cache to the most recent shared libraries”. The auxiliary index caches rebuilding work; it differs from the runtime loader’s primary path index.
- https://github.com/Azure/azure-vm-utils/blob/main/ephemeral-disk-setup/azure-ephemeral-disk-setup — “# Ensure key is valid.” The inspected implementation parses allowed configuration assignments and uses them to select disk aggregation, formatting, and mounts. It does not execute unrestricted configuration text.

Attempted primary manual URLs for missing or ambiguous formats included the corresponding man7 pages for csh, tcsh, idmapd.conf, kdump.conf, netconfig, printcap, xattr.conf, crypto-policies, containers-policy.json, gssproxy.conf, and iscsid.conf. Those pages were unavailable. General filesystem documentation establishes only typical purposes, not the missing contents of this inventory. UNKNOWN groups retain unresolved entries even when some other members have known functions.

Some raw paths directly identify interpreter startup files or scripts; these are judged by the explicitly named S2.2-10 examples. No execution rights are inferred from package ownership. README and sample members are explanatory content identified individually in their group partitions. The group directory members do not silently become exempt because their files are content.

## Specific mixed-group reasoning

- coreos-1d70ce548d: boot configuration and boot variables MUST; the display font NOT; font-only directory UNKNOWN. The latter’s operational requirement is unestablished independently of the content.
- coreos-a4c2c16ae9: audit rule files MUST; daemon preference file HOLE between one-program settings and external operation; unused plugin directory UNKNOWN.
- coreos-05942fe9ff, coreos-e9bcb7e1df: documentation NOT; manager configuration HOLE between internal values and external system changes; directory entries UNKNOWN unless needed by a MUST member.
- coreos-b91b989f2d: generator scripts MUST; explanatory README NOT; parent directory MUST because it exposes the scripts.
- coreos-17a7caf72b: identified shared trust bundles MUST because they control authentication across consumers; explanatory README members NOT; unresolved per-tool configuration, key purposes, and empty directories UNKNOWN. Exact partition is the ordinal member table.
- coreos-aaa1adf124: authentication/resource restrictions and namespace initialization MUST; password history HOLE because past records/passwords are exempt but they enforce future restrictions.
- coreos-c9f542a45c: access-control policy and textual labels MUST; corresponding compiled label lookup caches NOT; the checksum’s actual consumer UNKNOWN.
- coreos-c366c1919d: server login policy MUST; client configuration HOLE between single-client preferences and externally visible connectivity; moduli dependence UNKNOWN.
- coreos-5f604fda76: shared trust-bundle aliases MUST; explanatory README NOT; two cryptographic configuration aliases UNKNOWN without established contents/consumers.
- coreos-e48d7a5dbe: drift measurement HOLE between behavior-affecting future clock correction and exempt history/cache; directory requirement UNKNOWN.
- coreos-89229e49e6: entropy seed MUST; message catalog database NOT as explanatory message content; other directory members UNKNOWN.

## Scope and limitations

These are classification outputs, not a removal experiment. No system object was changed or removed. Public documentation supplies format and intended-consumer evidence; unavailable instance contents are not silently replaced with distribution defaults. Directory-only uncertainty is not a claimed defect of the definition. The text’s exclusion of state-management design questions is respected: only whether the object’s established function meets Section 2.2 is considered.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.

## Final source checks and clarification

- https://p11-glue.github.io/p11-glue/p11-kit/manual/trust.html — “Extract trust policy from the shared trust policy store.” Extracted trust bundles are operational authentication inputs across libraries, not automatically speed-only caches.
- https://www.mankier.com/8/update-ca-trust — “new applications that read the consolidated configuration files found in the /etc/pki/ca-trust/extracted directory”. This is the program’s manual, reproduced on a manual-page host, and confirms the collected directory’s role.
- https://www.mankier.com/7/crypto-policies — “allow consistently deprecating and disabling algorithms system-wide”. This is the program manual; it supports required shared cryptographic backend policy rather than single-program preferences.
- https://www.mankier.com/8/authselect — “configure system identity and authentication sources and providers by selecting a specific profile”. The generated authentication and name-service files implement account access across processes.
- https://www.mankier.com/5/containers-policy.json — “Signature verification policy files are used to specify policy”. This program manual establishes shared image-verification policy. Final correction for coreos-c2d2685965: policy.json and its containing directory MUST; all other collected members UNKNOWN, producing MIXED. This supersedes the earlier UNKNOWN-only count line.
- https://www.gnu.org/software/grub/manual/grub/html_node/Embedded-configuration.html — “read the real configuration file from $prefix/grub.cfg”. The configuration links target the bootloader’s command configuration.
- https://www.gnu.org/software/grub/manual/grub-dev/html_node/File-Structure.html — “The standard file extension for PFF2 font files is .pf2.” The collected font is display material, classified separately from boot commands.
- https://man7.org/linux/man-pages/man5/file_contexts.5.html — “This optimization is no longer required due to the use of file_contexts.bin files and is deprecated.” The binary files optimize lookup of the corresponding textual mapping members; the text sources remain present in this inventory.
- https://man7.org/linux/man-pages/man8/ldconfig.8.html — “Ignore auxiliary cache file.” The explicit option establishes that the auxiliary cache is dispensable for rebuilding the main index.

The standalone operating-system release identifiers are HOLE because their documented descriptive role does not exclude use as behavioral input. The software-tag group is treated as explanatory metadata; its directory members remain UNKNOWN. Directory UNKNOWN does not assert that every directory has the same runtime role.

## Exception-priority review

The explicit introduction S2.2-3 (“The following need not be recorded:”) makes S2.2-6 a stated exception to the broad dependency rule. Merely consulting history later does not cancel that exception. Final corrections therefore supersede the earlier discussions and count lines: password-history member in coreos-aaa1adf124 is NOT; recorded drift member in coreos-e48d7a5dbe is NOT; migration stamp coreos-845955a7d2 is NOT. Their earlier HOLE/UNKNOWN reasoning overextended the general dependency sentence. Directory decisions are unchanged. The final TSV and ordinal member table contain the corrected decisions.

The remaining single-program-setting HOLE cases concern the undefined scope of “only inside one program”: whether settings whose values a single program reads but whose operation creates external artifacts satisfy that qualifier. They do not assume that the broad rule overrides a known exemption. Password-plus-lock files remain HOLE because distinct required and exempt information occupies the same ungrouped file and no aggregate file rule is provided.

- **S2.2-3** The following need not be recorded:
