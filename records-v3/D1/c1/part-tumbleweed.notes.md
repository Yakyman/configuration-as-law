# Tumbleweed c1 classification notes

Date: 2026-11-22 UTC. Scope: only `../in/part-tumbleweed.tsv`, its corresponding inventory, the fixed text, and public primary documentation. No other classification or earlier-night material was consulted. No object was removed. The removal test is counterfactual reasoning from established function.

The input contains 6,779 rows, all level-1 objects. The `members` field contains JSON, not a numeric count. Repeated package inventories in different contexts remain separate input IDs. A package containing ancillary documentation is classified as its package object; it is not a directory-group row requiring a separate decision for each packaged file.

The classification uses Section 2.2 and S3-1/S3-2 only. Section 2.5 design choices are not treated as holes. Inventory evaluative labels have no authority. The main TSV is appended and flushed row by row; completed package shards are merged without replacing existing IDs.

## Local homogeneous rules

The exact implementation and per-row exceptions are in `part-tumbleweed.local.py`. Each rule below has ten manually inspected input rows listed in the sample register below. The three masks and eighteen small-category objects were individually inspected. Rule applicability was checked against the actual members, not merely the kind label.

- **accounts**: MUST under S2.2-15. The account records include numeric identity, group and login shell. Noninteractive service accounts remain accounts.
- **groups**: MUST under S2.2-1/S2.2-2. These are named system group identities and membership mappings used by credentials and access operations across programs. Removing a group removes the named identity even if its supplementary member list is empty; an empty member list alone does not establish absence of primary-group users.
- **services**: MUST under S2.2-1/S2.2-2/S2.2-9. A loaded service defines program activation. Inactive services retain that activation capability. Log-producing or cache-building services are programs, rather than the log/cache objects they produce.
- **missing_services**: UNKNOWN under S3-1/S3-2. `not-found` establishes a missing unit file, not the commands or dependencies of the particular unit. Some entries are inactive; others report active/exited. No unit contents establish their retained effects. Neither the historical-looking name nor an upstream service with the same name establishes this missing object's behavior.
- **units**: MUST under S2.2-1/S2.2-2/S2.2-13. Available service, socket and timer definitions or aliases govern activation of other programs. Static/disabled does not mean nonexistent or incapable of activation. They are values, but their effects are not confined inside the service manager. Generated/transient state is not excluded merely because generated.
- **timers**: MUST under S2.2-1/S2.2-2. The listed timers activate named service units. Removing the timer removes that activation path. Past/next timestamp fields do not make the timer itself a historical record. The timer without a displayed next event remains a timer object; its individual trigger details are unnecessary to identify its activation role.
- **processes**: MUST under S2.2-9/S2.2-12. Exactly one PID and one executable pathname are established by the collector. The observed process executes that program.
- **bad_processes**: UNKNOWN under S3-1/S3-2. The collector prints a PID before calling readlink, without printing a newline when readlink produces no pathname. Several PIDs therefore precede one pathname. Input `name` takes the first PID, while the pathname belongs to the last. We cannot substitute another process for the named object. The reason for the missing executable is not assumed.
- **modules**: MUST under S2.2-1/S2.2-10. All entries are loaded kernel modules. They execute code in kernel space, not confined application content. A zero reference count does not change their status as loaded executable code.
- **drivers**: MUST under S2.2-1/S2.2-2. At level 1 these entries inventory device-driver associations through sysfs links. The object is the binding, not an independently editable decorative link. Removing the binding removes that device-control path. This includes platform and software-created devices.
- **firewall_rules**: MUST under S2.2-15. All entries have actual nftables expressions, including matches, verdicts and jumps. Current matching traffic is not required by the explicit sentence.
- **firewall_chains**: MUST under S2.2-1/S2.2-2/S2.2-15. Each chain has a hook, contains rules, or is referenced by a jump/goto rule. This predicate was checked over the complete ruleset. Empty referenced chains are required targets of existing rules; they were not assumed to contain filtering statements. No empty unreferenced chain was found.
- **polkit**: MUST under S2.2-1/S2.2-2. Installed action definitions register authorization operations offered by privileged mechanisms to requesting programs. Removing their definition removes this registered authorization capability. No inference is made that every action grants a full superuser session. Effects cross program boundaries, so S2.2-7 does not apply.

## Individually examined local cases

The three `masked-runtime` NetworkManager initrd units prevent service activation: MUST under S2.2-1. Removal changes a behavioral prohibition, even though S2.2-2 describes loss of capabilities rather than their addition.

All six sockets enable communication: two multicast-DNS UDP endpoints, two loopback chrony control endpoints and two loopback printing TCP endpoints. MUST under S2.2-1/S2.2-2/S2.2-15. UDP is covered by its communication function even without connection-oriented transport.

All four sudo rules explicitly allow commands as superuser: MUST under S2.2-15. The populated `firewalld` inet table contains rules, hence MUST. Three Ethernet profiles and one loopback profile configure networking beyond NetworkManager: MUST under S2.2-1/S2.2-2. The saved wireless profile is expressly MUST under S2.2-14, without treating its password as required.

The exited container retains a restartable echo program, and the Alpine image supplies installed container programs: MUST under S2.2-2/S2.2-9/S2.2-12. An image being downloadable again does not by itself establish the cache exception; reinstalling programs from an external source is not evidence of an already installed cache-regeneration mechanism.

## Primary documentation and quoted supporting passages

Documentation establishes object function only; the fixed sentences establish decisions. The public documentation below was read during classification.

- [group(5)](https://www.man7.org/linux/man-pages/man5/group.5.html): “defines the groups on the system”. Documents the group name, numeric identifier and member fields.
- [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html): “encodes information about a process controlled and supervised by systemd”.
- [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html): “Units can be aliased (have an alternative name), by creating a symlink”. Describes unit configuration and activation dependencies.
- [systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html): “not-found” means “no unit file was found for this unit”; masking makes it “impossible to start them”.
- [systemd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html): “a matching unit file must exist, describing the unit to activate when the timer elapses”.
- [proc_pid_exe(5)](https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html): “containing the actual pathname of the executed command”. Compare the collected command in `../in/raw/tumbleweed/raw/076-process.sh` and concatenated output in `076-process.out`.
- [proc_modules(5)](https://man7.org/linux/man-pages/man5/proc_modules.5.html): “A text list of the modules that have been loaded by the system.”
- [init_module(2)](https://man7.org/linux/man-pages/man2/init_module.2.html): “loads an ELF image into kernel space”. Describes execution of the module initialization function.
- [Kernel driver binding](https://docs.kernel.org/driver-api/driver-model/binding.html): “associating a device with a device driver that can control it”.
- [nftables manual](https://netfilter.org/projects/nftables/manpage.html): “Chains are containers for rules.” A chain being deleted “must not contain any rules or be used as jump target”.
- [polkit manual](https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html): “Actions correspond to operations that clients can request the mechanism to carry out”. The same section specifies installed XML action definitions.
- [NetworkManager connection profiles](https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html): “These connection profiles contain a network configuration.” Activation applies this configuration to a network device.
- [Podman start](https://docs.podman.io/en/latest/markdown/podman-start.1.html): “Start one or more containers”. Describes starting existing containers.
- [Podman run](https://docs.podman.io/en/latest/markdown/podman-run.1.html): “Run a process in a new container.” Describes the image as the source for the process filesystem.
- [Avahi](https://avahi.org/): “service discovery on a local network via the mDNS/DNS-SD protocol suite”.
- [chrony configuration](https://chrony-project.org/doc/4.8/chrony.conf.html): the `cmdport` directive documents the command/monitoring port, default 323.
- [CUPS configuration](https://www.cups.org/doc/man-cupsd.conf.html): `Listen`/`Port` document the printer server's listening addresses and ports.

## Package subsets

The package rule statements, sources, manual sample IDs and individual exceptions are in `part-tumbleweed.rpm-a.notes.md`, `part-tumbleweed.rpm-b.notes.md`, and `part-tumbleweed.language.notes.md`; their completed contents are incorporated below when merging. Their public metadata is factual documentation, not an earlier classification. No automated package classification is accepted merely from a package-name prefix without documented functional support.

## Local manual sample register

**accounts**: tumbleweed-824e812c387bc4cd79ee187e, tumbleweed-cf1c8960eb5905508e385d35, tumbleweed-36da60582c8b4e5b33be0e77, tumbleweed-b5c80c294b9633d705a4223f, tumbleweed-0fb74e1cd4a89fecb0184c37, tumbleweed-7e9737b900b10c5a7768c195, tumbleweed-608a9c26376163f1682f9d51, tumbleweed-c8e4550418f47207ceb6adee, tumbleweed-436a875de3384a1393e08aab, tumbleweed-7847c3bcccb9f676b8aa2221.

**groups**: tumbleweed-7498378c17d4eb94ab472e97, tumbleweed-c351458a13a0bc6732a3f67b, tumbleweed-668fc6925159474da6efffdd, tumbleweed-f624f601a38fee776be43d1a, tumbleweed-2e822b4b9d324130d40c2278, tumbleweed-347b9c85fbb3a6481d3f26c2, tumbleweed-3d272032010aef04efe93146, tumbleweed-276ecce41a5b550e8f4f0975, tumbleweed-328abc94b7144d9901d9afdd, tumbleweed-1779331cf5381b112d4eb97f.

**services**: tumbleweed-49fa3497300d7af314d08014, tumbleweed-de2d172f94be7fdccbd453b9, tumbleweed-d20e6446a823362e71508d0d, tumbleweed-97e069dafaa54be54b30ed6c, tumbleweed-f612d64d811ecbe78eccd196, tumbleweed-3e9d53bbcb48f4760d02403f, tumbleweed-4c4caf58d88f51fa9822fdf9, tumbleweed-d218d71d3fc23bfcba040323, tumbleweed-354c600e6cc3bc6729eb4d42, tumbleweed-05a6a1b94d2ac276fc53ae19.

**missing_services**: tumbleweed-70d71746ae30f45711522288, tumbleweed-ec277111af46e76b0a09397b, tumbleweed-d864f982af79161ce72360ad, tumbleweed-02d707c50341a07be5e308bf, tumbleweed-91a1953d5c93bb9d6a6bc87c, tumbleweed-ec3a3171294da3d9f1d6edf5, tumbleweed-7ed90aaf19bee32844bb8824, tumbleweed-6190555eb7a3114f0d7984dc, tumbleweed-84c8fd07814a2fc4616b6c6a, tumbleweed-e6f416af40e7213cf96aa007.

**timers**: tumbleweed-126f50c11de036a60e79336d, tumbleweed-d00653dee5760f4d589e9a6d, tumbleweed-85e4a6617be8dfa6608f1d9e, tumbleweed-64ea9b829d670eafc117d08e, tumbleweed-ad5107d9ca769418f2fef487, tumbleweed-7a9055b600857acfbe08bf26, tumbleweed-3e3f8109f66399c96d241e6e, tumbleweed-5833537d9bc019b162de88b6, tumbleweed-85cda803b179d556b63a750f, tumbleweed-817ff77d9bf363aa5e643432.

**units**: tumbleweed-c77c285427e939a23f75173a, tumbleweed-bf61842076bceb9d5415acc3, tumbleweed-0daef9836cb476e319e7cc85, tumbleweed-0f996c3936bf7e01048cb9ae, tumbleweed-57a6c0e9957a4ae35da92320, tumbleweed-22a65badcbd67d33ad574507, tumbleweed-c5b9a8a67132f786689d7957, tumbleweed-f59349977b4ab5e3eba6f755, tumbleweed-8c88824446ace65593ccfe17, tumbleweed-66d3fe835d3fc3294cf324aa.

**masked**: tumbleweed-e34465db11efc9ee8bcdca05, tumbleweed-e37ecd74c4b90b6f73128061, tumbleweed-a882a6ec07582da337c54bf4.

**processes**: tumbleweed-d1971847629718b5c9867caa, tumbleweed-5443e7c81d6174ef445ee1f7, tumbleweed-57a39741db12af6370c7152a, tumbleweed-5733ca24f8720f7df16e3b6a, tumbleweed-868f2227b9517b13cb7da29f, tumbleweed-61aa5cc06603bc49c0f5d3eb, tumbleweed-23cb971f6663f451f8b5c07c, tumbleweed-050a7a4baf9987760c7ed08f, tumbleweed-80ceb0ed8584fb905311b189, tumbleweed-0aed088b05a998fdf2171023.

**bad_processes**: tumbleweed-350993705bca851f8115a15c, tumbleweed-e0e07676a2b45150a7303e31, tumbleweed-a865f8fd04adb499d0274c23, tumbleweed-6fc3db127de85b1141c30d64, tumbleweed-0c14710350a137980e048712, tumbleweed-80136c9c7a80061b327cc23b, tumbleweed-ef8b5a358eafe66141ed8d90, tumbleweed-edcc20978579ffcb6ab71651, tumbleweed-c29209f9e6aaa1750fe965fb, tumbleweed-eb5e5f35cfac43455552fb5b.

**modules**: tumbleweed-d232acf53b6dfad3b337a10b, tumbleweed-aef25d9d851b97d954c7fe16, tumbleweed-92a9dee6a35f48521839ee1b, tumbleweed-69184936396a7ffbe88f8eab, tumbleweed-551b6144b448eb92201ca88e, tumbleweed-c8eec94d2aa951984cda2dcd, tumbleweed-52d772dff269b0aa56bf48c8, tumbleweed-15859a7206257ba46199fe53, tumbleweed-a06fe6611f428d50346f3f67, tumbleweed-e1c82fdc6b5505208b4baa10.

**drivers**: tumbleweed-5d29c398c6c62c4b31338d6f, tumbleweed-9d87dd83eb23ec37aca348c2, tumbleweed-03d45ab213e0837d6dbaf248, tumbleweed-5fd022a019e7e04e73c8be0b, tumbleweed-254acfbc38b48dd263d145d7, tumbleweed-7cbc26afdce369b3eec457ab, tumbleweed-69986e117f41bc215c3b9752, tumbleweed-a6e69acc675645ee4a5e46a5, tumbleweed-17da72f215cad6cc7cdd3a37, tumbleweed-567bc1d0540ee2c39ad8da7c.

**individual**: tumbleweed-c02d0e9052ef4a9195188b3f, tumbleweed-92bc101232efef1c8c840eaa, tumbleweed-5254a014d31c9226f0767152, tumbleweed-b3301c8d53cbc9d569a18b78, tumbleweed-44953ab7f7bdc81732c84e2c, tumbleweed-dcdc56a06be335845b07422e, tumbleweed-770efc86c7ccfd4620b7b89b, tumbleweed-4bd6a67d898eeef2db601dd9, tumbleweed-71f2c3be741d27ce42a8acf7, tumbleweed-dfef9ef984c3c49501483e66, tumbleweed-d9a948d4a48c172b82f5b9fc, tumbleweed-cb9d455b417d42059282eba5, tumbleweed-e95a02bb8e22aa56aed4066d, tumbleweed-46ccb95936c821188da69e15, tumbleweed-71fa379da109c0a4b248ec44, tumbleweed-e55fa16314dd42978bb4d9dc, tumbleweed-1297f5f596320f4de34b8853, tumbleweed-83c090ab83e82a39aaad12ea.

**firewall_chains**: tumbleweed-c021359b1b5fff70cdbd1472, tumbleweed-48d9a5c36981412471fc3d6c, tumbleweed-4ca7b4938c9b5e91033db99c, tumbleweed-44632902aa0dad7d90d1fb64, tumbleweed-ab8aba76679142dae7887ce5, tumbleweed-dfe4747349b6f8ee7cf85485, tumbleweed-8472da3edeed93d01066bff8, tumbleweed-01faf317d4e9eb73bf288085, tumbleweed-9086d798929c922bc4a9d0cd, tumbleweed-001177584fec12bee9037736.

**firewall_rules**: tumbleweed-b4ca694bf3fabff7d0854b50, tumbleweed-aa9c4a2db8886ef53654cd44, tumbleweed-5d33f805e6b675f099f38ada, tumbleweed-8200e18b49250e30a629e0c7, tumbleweed-4c6b9ef02b25ae52c6b0922b, tumbleweed-743bd8de4e9b1373934aa8f7, tumbleweed-3293681ed74e336817417b12, tumbleweed-27aeaf5a369c95a000257fa4, tumbleweed-3e33cef7d4aaeab5b8d4e672, tumbleweed-601d92ab40e8e3ebff654728.

**polkit**: tumbleweed-32123ab1e35c58946847c825, tumbleweed-309707a4f12b67b4342098dd, tumbleweed-5b5a0582542a3ddd9677c2a2, tumbleweed-86a49930c23913afa07a2aae, tumbleweed-270d30716ee6035ef56dddeb, tumbleweed-ef93b10ec19a684aa2f2a160, tumbleweed-6fb334dfd2a2ba9531001cee, tumbleweed-144881461ec213b5723b33a1, tumbleweed-97d96d0b893d70234d640a20, tumbleweed-d6e51174e3f196d501bc2442.

## Fixed sentences used in local classification

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.


# Subset working record: rpm-a

# c1: first RPM inventory half

Scope: first 2,390 L1:package:rpm rows, in input order. COMMON.md, TEXT.md Sections 2 and 3, and SENTENCES.md were read. No other classification was consulted. No objects were removed.

The inventory lists installed package names, versions, and architecture, but `../in/raw/tumbleweed/raw/113-ownership-rpm.out` is empty. Public official repository descriptions and full file lists were therefore used. The package object is classified by its own payload, not by a similarly named application. A package containing both required code and documents is one package object, not an inventory group of independently classified stored files.

## Evidence

Official primary metadata: URL in (not published: downloaded distribution package metadata). Official file lists: URL in (not published: downloaded distribution package metadata). Compressed original metadata is retained. Installed versions were compared against file-list versions: all match except openSUSE-build-key (installed 1.0-69.1, available 1.0-68.1); its documented purpose is used without claiming byte identity. Five imported gpg-pubkey entries have no repository counterpart.

Additional documentation:

- https://rpm.org/docs/6.0.x/man/rpmkeys.8 : “Digital signatures cannot be verified without the corresponding public key (aka certificate).”
- https://gi.readthedocs.io/en/latest/ : “language bindings can read this metadata and automatically provide bindings to call into the C library.”
- https://docs.kde.org/trunk_kf6/en/kdebugsettings/kdebugsettings/categories-file.html describes category names, descriptions, defaults, and rename mappings consumed by the category editor.
- https://docs.kde.org/trunk_kf6/en/kdebugsettings/kdebugsettings/custom-rules-tab.html explains that categories can be configured without an installed category description. The executable libraries remain independently packaged.
- https://download.opensuse.org/tumbleweed/repo/oss/noarch/hicolor-icon-theme-0.18-1.5.noarch.rpm : inspected `usr/lib/rpm/macros.d/macros.hicolor`. Its `%icon_theme_cache_create_ghost` expands to shell `mkdir` and `touch` operations. This package is MUST despite its theme name.

## Literal grounds

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S3-2: “If what the object does remains unknown, the case yields ?.”

## Homogeneous rules and manual checks

Rules are implemented in `part-tumbleweed.rpm-a.classify.py`. Executable payload detection precedes names such as theme, presets, data, and branding. Explicit nonhomogeneous cases use named decisions. The following checks inspected actual paths and package descriptions, not just labels. Each rule below lists ten manually checked object IDs.

### code (2001 rows)

MUST: executable programs, native shared libraries, interpreter scripts, and runtime modules. These supply executable operations under S2.2-9/10/13. Only non-documentation paths count; executable content overrides a theme or data package name.

- `tumbleweed-2194ecddf8f96383cae8f9a9` — gxditview; inspected `/usr/bin/gxditview`.
- `tumbleweed-384b789273ac07e5b755d800` — python313-pycairo; inspected `/usr/lib64/python3.13/site-packages/cairo/__init__.py`.
- `tumbleweed-c7867d9621c22e0b97006af6` — python313-puremagic; inspected `/usr/bin/puremagic`.
- `tumbleweed-e880790a58444d3bafa14fa5` — python313-nftables; inspected `/usr/lib/python3.13/site-packages/nftables/__init__.py`.
- `tumbleweed-9746777c7b5f013afd157f4d` — python313-hyperframe; inspected `/usr/lib/python3.13/site-packages/hyperframe/__init__.py`.
- `tumbleweed-d33455986c66ff248d59eef2` — Mesa-libva; inspected `/usr/lib64/dri/nouveau_drv_video.so`.
- `tumbleweed-cc32ce44527335a224b417dd` — busybox-static; inspected `/usr/bin/busybox-static`.
- `tumbleweed-b891edce09972457274125e3` — compat-usrmerge-tools; inspected `/usr/bin/usrmergecheck`.
- `tumbleweed-4d8757f93c50b0bfcead2627` — debuginfod-profile; inspected `/etc/profile.d/debuginfod.sh`.
- `tumbleweed-668b190c43f169fc63e4be91` — freecell-solver-presets; inspected `/usr/share/freecell-solver/presets/abra-kadabra.sh`.

### category (62 rows)

NOT: packages whose non-documentation payload consists exclusively of diagnostic category and rename descriptions. These supply descriptive choices in the category editor; custom rules remain possible and executable libraries remain. S2.2-4 applies to descriptions, not to recorded log events.

- `tumbleweed-301c13d4a59931a7b5c91c83` — akonadi-calendar; inspected `/usr/share/qlogging-categories6/akonadi-calendar.categories`.
- `tumbleweed-c61693ca0d9c338b6719b0d3` — akonadi-mime; inspected `/usr/share/qlogging-categories6/akonadi-mime.categories`.
- `tumbleweed-7695b0145913f25106970cd7` — calendarsupport; inspected `/usr/share/qlogging-categories6/calendarsupport.categories`.
- `tumbleweed-413f0500532691a1403b99e4` — eventviews; inspected `/usr/share/qlogging-categories6/eventviews.categories`.
- `tumbleweed-2273f5235f66c502aa5c172b` — incidenceeditor; inspected `/usr/share/qlogging-categories6/incidenceeditor.categories`.
- `tumbleweed-cfbb9493d3cc953559180595` — kf6-attica; inspected `/usr/share/qlogging-categories6/attica.categories`.
- `tumbleweed-e51e5f35a865a939595bab30` — kf6-bluez-qt; inspected `/usr/share/qlogging-categories6/bluezqt.categories`.
- `tumbleweed-dd4240e6ee3b671d67697c5d` — kf6-karchive; inspected `/usr/share/qlogging-categories6/karchive.categories`.
- `tumbleweed-88fe72d3de4e08b187d1511a` — kf6-kbookmarks; inspected `/usr/share/qlogging-categories6/kbookmarks.categories`.
- `tumbleweed-764aa158abfb0c6a7192d979` — kf6-kcodecs; inspected `/usr/share/qlogging-categories6/kcodecs.categories`.

### document (12 rows)

NOT: documentation and license-only packages under S2.2-4. The text expressly introduces content as an exception, so inability to read the removed document is not counted again as loss of program behavior.

- `tumbleweed-ce54db5c43dcf480996ace27` — boost-license1_92_0; inspected `/usr/share/licenses/boost-license1_92_0/LICENSE_1_0.txt`.
- `tumbleweed-21c473dcf355645958b2923e` — cryptsetup-doc; inspected `/usr/share/doc/packages/cryptsetup-doc/AUTHORS`.
- `tumbleweed-34f1d68aa8f99541fd83b097` — kaddressbook-doc; inspected `/usr/share/doc/HTML/en/kaddressbook/KDE_logo.png`.
- `tumbleweed-48601afb75375826257791bf` — pam-manpages; inspected `/usr/share/man/man3/misc_conv.3.gz`.
- `tumbleweed-ce47e21fa36959c229791ea2` — unzip-doc; inspected `/usr/share/doc/packages/unzip-doc/BUGS`.
- `tumbleweed-4c680d99add6f6e22e4e15c9` — bash-doc; inspected `/usr/share/doc/packages/bash/BUGS`.
- `tumbleweed-0b374b0c6cdc5193e1c634a0` — coreutils-doc; inspected `/usr/share/info/coreutils.info.gz`.
- `tumbleweed-158dbe5ce67a1f463f677898` — coreutils-systemd-doc; inspected `/usr/share/man/man1/pinky.1.gz`.
- `tumbleweed-88c545e32bc24c4e9325ebcf` — info-std; inspected `/usr/share/info/info-stnd.info.gz`.
- `tumbleweed-1a2ff00a85c08b7185dc99db` — man-pages; inspected `/usr/share/doc/packages/man-pages/CONTRIBUTING`.

### translation (30 rows)

NOT: interface translations and translated names are content. Under S2.2-4 the same operation remains available while its translated wording is unavailable. This rule does not cover language-processing engines or dictionaries that enable distinct processing.

- `tumbleweed-69d8cbcefe0629f32ed6c8e8` — desktop-translations; inspected `/usr/share/locale/af/LC_MESSAGES/desktop_translations.mo`.
- `tumbleweed-e3ffdbeeab220be3a54cafba` — iso-codes; inspected `/usr/share/iso-codes/json/iso_15924.json`.
- `tumbleweed-cef9aa36975108f20d6841ff` — kImageAnnotator-lang; inspected `/usr/share/kImageAnnotator/translations/kImageAnnotator_ar.qm`.
- `tumbleweed-527aeb630ad9f2636cdd559f` — libksane-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/libksane.mo`.
- `tumbleweed-6a567e1b020369e9b4a15b5e` — libqt5-qttranslations; inspected `/usr/share/qt5/translations/assistant_ar.qm`.
- `tumbleweed-debbb43da15a0050abbd7e0a` — libstorage-ng-lang; inspected `/usr/share/locale/af/LC_MESSAGES/libstorage-ng.mo`.
- `tumbleweed-af2b623383a61a33374a59f1` — qt6-translations; inspected `/usr/share/qt6/translations/assistant_ar.qm`.
- `tumbleweed-14b4feff4d3b3c916032ed56` — snapper-lang; inspected `/usr/share/locale/af/LC_MESSAGES/snapper.mo`.
- `tumbleweed-f73eeb400766d5a937dddc88` — kf6-kuserfeedback-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/userfeedbackconsole6_qt.qm`.
- `tumbleweed-e4b043dbfeb54717e5f66dcc` — kidentitymanagement-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/libkpimidentities6.mo`.

### asset (11 rows)

NOT: pictures, icons, audio samples, and card artwork under S2.2-4. The visual or audio work itself becomes unavailable; execution of the operation displaying or playing content remains. Packages with macros or code are excluded.

- `tumbleweed-f30a186bd1cff9957e0f7b5c` — kdegames-carddecks-default; inspected `/usr/share/carddecks/svg-oxygen-air/11.png`.
- `tumbleweed-39af3faa265fdda45dd7c62f` — kf6-breeze-icons; inspected `/usr/share/icons/breeze-dark/actions/12/external-link-symbolic.svg`.
- `tumbleweed-8deb6bea53de73438bc0b1e6` — kmail-application-icons; inspected `/usr/share/icons/breeze-dark/16x16/emblems/gpg-key-trust-level-0.svg`.
- `tumbleweed-d2388c321ef8b22307dcf7bd` — ocean-sound-theme6; inspected `/usr/share/licenses/ocean-sound-theme6/BSD-2-Clause.txt`.
- `tumbleweed-bf9029a4ec645e21be37f294` — wallpaper-branding-openSUSE; inspected `/usr/share/gnome-background-properties/wallpaper-branding-openSUSE.xml`.
- `tumbleweed-9fe77d5b5a8d7bb3aa41ea6a` — xbitmaps; inspected `/usr/include/X11/bitmaps/1x1`.
- `tumbleweed-6cc4dd2ccf77fb4f5b6b01f6` — distribution-logos-openSUSE-icons; inspected `/usr/share/icons/hicolor/scalable/apps/distributor-logo-Aeon.svg`.
- `tumbleweed-9d4553a31373cb92d9b4fd44` — sound-theme-freedesktop; inspected `/usr/share/doc/packages/sound-theme-freedesktop/README`.
- `tumbleweed-aa92a36c91f7c095a4cf0ae4` — hicolor-icon-theme-branding-openSUSE; inspected `/usr/share/icons/hicolor/16x16/apps/distributor.png`.
- `tumbleweed-0c9194115520ab49a173b08c` — libreoffice-icon-themes; inspected `/usr/share/libreoffice/share/config/images_breeze.zip`.

### presentation (15 rows)

NOT: nonexecuted presentation themes containing visual assets and color/style values, S2.2-4/7/13. Unlike code themes, these merely supply presentation content. Verified file lists exclude runtime scripts and shared-object implementations.

- `tumbleweed-694485646109ee5946fed689` — libplasma6-desktoptheme; inspected `/usr/share/plasma/desktoptheme/breeze-dark/colors`.
- `tumbleweed-ff8414e8fa9b41b847ba8f03` — metatheme-breeze6-common; inspected `/usr/share/doc/packages/metatheme-breeze6-common/README.md`.
- `tumbleweed-8e84d13ea1b940f02e6994e2` — gtk3-metatheme-breeze6; inspected `/usr/share/themes/Breeze-Dark/gtk-3.0/gtk.css`.
- `tumbleweed-c99ceaa989531e038628e42e` — gtk4-metatheme-breeze6; inspected `/usr/share/themes/Breeze-Dark/gtk-4.0/gtk.css`.
- `tumbleweed-8950e190d14060a369183dc1` — metatheme-adwaita-common; inspected `/usr/share/doc/packages/metatheme-adwaita-common/NEWS`.
- `tumbleweed-99e98e78a19742451d9457a5` — gtk3-metatheme-adwaita; inspected `/usr/share/themes/Adwaita-dark/gtk-3.0/gtk.css`.
- `tumbleweed-d095a3b61de32b1463d7c78b` — yast2-qt-branding-openSUSE; inspected `/usr/share/YaST2/theme/current/wizard/arr_down.png`.
- `tumbleweed-6ec882183d132324cb0208a4` — plymouth-theme-spinner; inspected `/usr/share/plymouth/themes/spinner/animation-0001.png`.
- `tumbleweed-4deaf55db08341f000a852f5` — yast2-theme; inspected `/etc/icewm/preferences.yast2`.
- `tumbleweed-65bfdabf3b6608dedffb67e5` — plymouth-theme-bgrt; inspected `/usr/share/plymouth/themes/bgrt/bgrt.plymouth`.

### selector (28 rows)

HOLE: dependency-only package selectors. Removal can leave installed implementations unchanged but alter future selection by package tools. S2.2-1/2 do not specify whether that future consequence belongs to the removal test; S2.2-7 offers a competing single-manager-values reading.

- `tumbleweed-37db51661957d09b5c15eacf` — patterns-games-games; inspected `/usr/share/doc/packages/patterns/games.txt`.
- `tumbleweed-8ebb5b342bc9dc105f0138a9` — patterns-glibc-hwcaps-x86_64_v3; inspected `/usr/share/doc/packages/patterns/x86_64_v3.txt`.
- `tumbleweed-296f03671ca8befb4893d5e2` — openSUSE-release-ftp; inspected `/usr/share/doc/packages/openSUSE-release-ftp/README`.
- `tumbleweed-4aa703e25ccc5895e1cee141` — patterns-base-minimal_base; inspected `/usr/share/doc/packages/patterns/minimal_base.txt`.
- `tumbleweed-604a999da494f2de35403dee` — patterns-base-sw_management; inspected `/usr/share/doc/packages/patterns/sw_management.txt`.
- `tumbleweed-2f7c08878cbbd469fe4f4547` — patterns-base-selinux; inspected `/usr/share/doc/packages/patterns/selinux.txt`.
- `tumbleweed-887caba836a7c23b3fedba9d` — patterns-fonts-fonts_opt; inspected `/usr/share/doc/packages/patterns/fonts_opt.txt`.
- `tumbleweed-7ff02912d648f6301fd0d572` — patterns-yast-x11_yast; inspected `/usr/share/doc/packages/patterns/x11_yast.txt`.
- `tumbleweed-8e6d6eb9be69c877faa7bd08` — patterns-kde-kde_yast; inspected `/usr/share/doc/packages/patterns/kde_yast.txt`.
- `tumbleweed-8ffe304c89c8c7e36f097d58` — patterns-fonts-fonts; inspected `/usr/share/doc/packages/patterns/fonts.txt`.

### introspection (18 rows)

MUST: runtime typelib interface metadata required to generate native language bindings. S2.2-1/2 apply because removing these descriptions prevents calls, rather than merely making explanatory content unavailable. They are not incorrectly called executable libraries.

- `tumbleweed-7a6ad33f358961bfad1a3cba` — typelib-1_0-GLib-2_0; inspected `/usr/lib64/girepository-1.0/GLib-2.0.typelib`.
- `tumbleweed-900dbc71741501e821d1c709` — typelib-1_0-GObject-2_0; inspected `/usr/lib64/girepository-1.0/GObject-2.0.typelib`.
- `tumbleweed-b7d547e3a754a9f5372ffdcf` — typelib-1_0-GModule-2_0; inspected `/usr/lib64/girepository-1.0/GModule-2.0.typelib`.
- `tumbleweed-50bd7f4cb772b73088964c52` — typelib-1_0-GLibUnix-2_0; inspected `/usr/lib64/girepository-1.0/GLibUnix-2.0.typelib`.
- `tumbleweed-272491cb93106d5053d88d39` — typelib-1_0-Atk-1_0; inspected `/usr/lib64/girepository-1.0/Atk-1.0.typelib`.
- `tumbleweed-c94a1b3acbd79a0bc4cb5cf6` — typelib-1_0-HarfBuzz-0_0; inspected `/usr/lib64/girepository-1.0/HarfBuzz-0.0.typelib`.
- `tumbleweed-80a3e282e5b79c37931671ce` — typelib-1_0-Gio-2_0; inspected `/usr/lib64/girepository-1.0/Gio-2.0.typelib`.
- `tumbleweed-e61016bde855c68fde4fd1ec` — typelib-1_0-Secret-1; inspected `/usr/lib64/girepository-1.0/Secret-1.typelib`.
- `tumbleweed-70589ea9923cebb923c91aef` — typelib-1_0-Pango-1_0; inspected `/usr/lib64/girepository-1.0/Pango-1.0.typelib`.
- `tumbleweed-e7b05fc9fc3e1f0f168dfc36` — typelib-1_0-GdkPixbuf-2_0; inspected `/usr/lib64/girepository-1.0/GdkPixbuf-2.0.typelib`.

### font (35 rows)

HOLE: font glyphs and associated font substitution mappings. S2.2-2 can count losing character rendering as lost capability; S2.2-4 can treat the typeface as unavailable content. The text does not define this boundary.

- `tumbleweed-33499c40cabacd70ef4d21d9` — urw-base35-fonts-Z003; inspected `/usr/share/fonts/truetype/Z003-MediumItalic.otf`.
- `tumbleweed-862ddc569edf79ec6aece441` — urw-base35-fonts-URWGothic; inspected `/usr/share/fonts/truetype/URWGothic-Book.otf`.
- `tumbleweed-0e9ba7156c0c20c550992121` — urw-base35-fonts-URWBookman; inspected `/usr/share/fonts/truetype/URWBookman-Demi.otf`.
- `tumbleweed-1a229bd3c5b65cda8f942bd8` — urw-base35-fonts-StandardSymbolsPS; inspected `/usr/share/fonts/truetype/StandardSymbolsPS.otf`.
- `tumbleweed-296a32b8080e5f74e2f35430` — urw-base35-fonts-P052; inspected `/usr/share/fonts/truetype/P052-Bold.otf`.
- `tumbleweed-59566a89cf17ed81b1692100` — urw-base35-fonts-NimbusSans; inspected `/usr/share/fonts/truetype/NimbusSans-Bold.otf`.
- `tumbleweed-74d9d28ed3c6446f8ad2696e` — urw-base35-fonts-NimbusRoman; inspected `/usr/share/fonts/truetype/NimbusRoman-Bold.otf`.
- `tumbleweed-ed87f367256d9993c15e4c83` — urw-base35-fonts-NimbusMonoPS; inspected `/usr/share/fonts/truetype/NimbusMonoPS-Bold.otf`.
- `tumbleweed-96e3075e617c5983470c405d` — urw-base35-fonts-D050000L; inspected `/usr/share/fonts/truetype/D050000L.otf`.
- `tumbleweed-40516f5352772e4cca300618` — urw-base35-fonts-C059; inspected `/usr/share/fonts/truetype/C059-BdIta.otf`.

### firmware (34 rows)

MUST: firmware images supplied to drivers for loading into supported devices, S2.2-1/2/16. Their documented role enables device behavior. Catch-all dependency metapackages are excluded.

- `tumbleweed-412a36df79780b825ecaee73` — kernel-firmware-usb-network; inspected `/usr/lib/firmware/aic/aic8800d80/fmacfw_8800d80_u02.bin.xz`.
- `tumbleweed-c0ef9ecf5b546861a2691bb0` — kernel-firmware-ueagle; inspected `/usr/lib/firmware/ueagle-atm/CMV4p.bin.v2.xz`.
- `tumbleweed-798825e63087dcf733dd5a63` — kernel-firmware-ti; inspected `/usr/lib/firmware/ti-connectivity/TIInit_6.2.31.bts.xz`.
- `tumbleweed-b3a3ec819bae794ee9f21037` — kernel-firmware-sound; inspected `/usr/lib/firmware/1534-2-0x8.bin.xz`.
- `tumbleweed-c7e4a57192087cdf95acd8e8` — kernel-firmware-serial; inspected `/usr/lib/firmware/edgeport/boot.fw.xz`.
- `tumbleweed-5da966f776fc272cbd679806` — kernel-firmware-realtek; inspected `/usr/lib/firmware/realtek/rt1320/rt1320-patch-code-vab.bin.xz`.
- `tumbleweed-8c2e91ec924f052ebbc3b8a8` — kernel-firmware-radeon; inspected `/usr/lib/firmware/radeon/ARUBA_me.bin.xz`.
- `tumbleweed-f057cdb52209ca0d28de1bf1` — kernel-firmware-qlogic; inspected `/usr/lib/firmware/cbfw-3.2.5.1.bin.xz`.
- `tumbleweed-c588fd227e5e14b1a8d6fcf2` — kernel-firmware-qcom; inspected `/usr/lib/firmware/a300_pfp.fw.xz`.
- `tumbleweed-8bfe28daef97939f9944f764` — kernel-firmware-platform; inspected `/usr/lib/firmware/Lontium/lt7911exc_fw.bin.xz`.

## Individual cases

All cases outside the homogeneous rules were considered individually using their specific payload and description. Their per-row grounds and uncertainty are recorded in the TSV. Notable distinctions: installed public-key copies explicitly unused by RPM are content; imported RPM verification keys are operational trust values with a setting/capability boundary; account definitions and multi-application policies are MUST. Systemd defaults have an unresolved single-reader versus multiple-affected-programs scope. No decision is based merely on the inventory word “package”.

Three UNKNOWN rows remain: the GNOME resource bundle whose internal payload is unspecified, and two XSLT transformation packages whose execution-rights/confinement evidence is insufficient. This is uncertainty about object behavior under S3-2, not a declaration-design question.

Validation: 2,390 unique output IDs equal the assigned input IDs, each once; all decisions are allowed; descriptions and reasons satisfy word limits. Final counts: MUST 2,119; NOT 158; HOLE 110; UNKNOWN 3; MIXED 0.


# Subset working record: rpm-b

# RPM second-half classification notes

Scope: last 2390 RPM rows, original input order. No other classification was consulted.

The ownership dump `../in/raw/tumbleweed/raw/113-ownership-rpm.out` is empty. Package names and versions are established by input evidence. Public repository descriptions establish the package roles. The public repository is a rolling source: it establishes purpose, not identity of every historical byte. No claim of exact installed file identity is made.

Source: https://download.opensuse.org/tumbleweed/repo/oss/repodata/27d143aba154b3643c2f0190d4849cfbe4f4e9da1d112131a8aa743f4b8e8e4c298349e2fe066d304f50c27cab559110b91228bd7ae9d8f5976fb08bccd3d06b-primary.xml.zst

Metadata summaries/descriptions and selected primary file paths are preserved in (not published: downloaded distribution package metadata). The scripts contain the explicit role selection and corrections. Every output is one package object, not a group of its files.

## Rule code

S2.2-9,S2.2-10: Executable programs and native/interpreter library code must be recorded. Descriptions or documented binary paths establish code; package names alone do not. Translation, content, config and metapackage exceptions are reviewed first.

Ten hand-checked examples (description checked against role):

- tumbleweed-60c4817b88fb7bd852b85007 — `gxditview`: Ditroff Output Displayer for Groff. Check: MUST; Ditroff Output Displayer for Groff.
- tumbleweed-197b296a65b71dde96352fc5 — `python313-pycairo`: Python Bindings for Cairo. Check: MUST; Python Bindings for Cairo.
- tumbleweed-431845990e7a6c4e40daa124 — `python313-puremagic`: Pure python implementation of magic file detection. Check: MUST; Pure python implementation of magic file detection.
- tumbleweed-9d78f81908b4597563af8e98 — `python313-nftables`: Python bindings for nftables. Check: MUST; Python bindings for nftables.
- tumbleweed-694c4e45b94cb4ea75d264d0 — `python313-hyperframe`: HTTP/2 framing layer for Python. Check: MUST; HTTP/2 framing layer for Python.
- tumbleweed-57b744fba8565804434dea06 — `Mesa-libva`: Mesa VA-API implementation. Check: MUST; Mesa VA-API implementation.
- tumbleweed-ad71216d622d1dca6742e261 — `akonadi-calendar`: Akonadi calendar integration. Check: MUST; Akonadi calendar integration.
- tumbleweed-effe590234671115bf028903 — `akonadi-contacts`: KDE PIM Libraries for Akonadi Contacts. Check: MUST; KDE PIM Libraries for Akonadi Contacts.
- tumbleweed-dcb819e6db4b67a32f27764f — `akonadi-mime`: MIME email parser for KDE PIM. Check: MUST; MIME email parser for KDE PIM.
- tumbleweed-6b071013d72da654f2636b71 — `busybox-static`: Static linked version of Busybox, a compact UNIX utility collection. Check: MUST; Static linked version of Busybox, a compact UNIX utility collection.

## Rule data

S2.2-2,S2.2-4: Operational text, icons, fonts and reference datasets lose their particular content when removed, but also stop corresponding rendering/language/recognition results. The text supplies no boundary between these two readings: HOLE.

Ten hand-checked examples (description checked against role):

- tumbleweed-d4ff03222fe3efc98f95872f — `desktop-translations`: Desktop Files Translations. Check: HOLE; Desktop Files Translations.
- tumbleweed-88c6d153fb922b34384bb62c — `distribution-logos-openSUSE-Tumbleweed`: Logos for openSUSE Tumbleweed. Check: HOLE; Logos for openSUSE Tumbleweed.
- tumbleweed-3b3aed8cb0eceacdbdbe6dec — `file-magic`: Database for libmagic to help identify files. Check: HOLE; Database for libmagic to help identify files.
- tumbleweed-c3769a3b91a480a1eb8680b6 — `gnome-tour-data`: GNOME Tour data. Check: HOLE; GNOME Tour data.
- tumbleweed-753ec04c3399c7c24f6764f9 — `gtk3-data`: Data files for the GTK+ toolkit library v3. Check: HOLE; Data files for the GTK+ toolkit library v3.
- tumbleweed-628aba51170df68037b752da — `hicolor-icon-theme`: Fallback Icon Theme. Check: HOLE; Fallback Icon Theme.
- tumbleweed-fb37a4a8d9cbdde019568fee — `iso-codes`: ISO Code Lists and Translations. Check: HOLE; ISO Code Lists and Translations.
- tumbleweed-803cd9885d5ac3af08d2e0a6 — `kImageAnnotator-lang`: Translations for package kImageAnnotator. Check: HOLE; Translations for package kImageAnnotator.
- tumbleweed-10a7e6c22aeeee7b7f43e322 — `kdegames-carddecks-default`: Default Card Decks for KDE Games. Check: HOLE; Default Card Decks for KDE Games.
- tumbleweed-9b979d05f7cbf004bcb901d2 — `kf6-breeze-icons`: Breeze icon theme. Check: HOLE; Breeze icon theme.

## Rule metadata

S2.2-1,S2.2-2,S2.2-4,S2.2-13: Structural/package/introspection metadata has downstream operational uses without itself being the program. The text does not distinguish that behavior dependence from descriptive data or settings: HOLE.

Ten hand-checked examples (description checked against role):

- tumbleweed-afd24c8aacb62bb4d83a4713 — `branding-openSUSE`: openSUSE Tumbleweed Brand File. Check: HOLE; openSUSE Tumbleweed Brand File.
- tumbleweed-7a02732097fb92ad188d98e9 — `javapackages-filesystem`: Java packages filesystem layout. Check: HOLE; Java packages filesystem layout.
- tumbleweed-2f4b0dcaee7ccc4ae3445c43 — `patterns-games-games`: Games. Check: HOLE; Games.
- tumbleweed-cae0778ca79df14155e00d1c — `filesystem`: Basic Directory Layout. Check: HOLE; Basic Directory Layout.
- tumbleweed-46d7dfbc72a2231daf3f2e00 — `patterns-glibc-hwcaps-x86_64_v3`: Install x86-64-v3 optimized libraries. Check: HOLE; Install x86-64-v3 optimized libraries.
- tumbleweed-b6506c20dbd511bc9d1cea43 — `typelib-1_0-GLib-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-54f349aab25a45dcdffb851f — `typelib-1_0-GObject-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-6f6fb0bebafbad99f7e14193 — `typelib-1_0-GModule-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-1071b28ebfc759ac33f9c4d0 — `typelib-1_0-GLibUnix-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-4427d7290d8883e9a3b55338 — `typelib-1_0-Atk-1_0`: Introspection bindings for the ATK accessibility toolkit. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.

## Rule settings

S2.2-7,S2.2-13: passive settings or visual resources whose documented effects remain in the named application are NOT. Passive values alone are insufficient: shared/system effects are individually reviewed.

Ten final hand-checked IDs:

- tumbleweed-a8553410b9fddc2ff2491faa — MozillaFirefox-branding-openSUSE: openSUSE branding of MozillaFirefox; NOT.
- tumbleweed-d86c1763518f3862d3fda0c3 — libreoffice-branding-openSUSE: openSUSE Tumbleweed branding for LibreOffice; NOT.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — ImageMagick-config-7-SUSE: SUSE Provided Configuration; NOT.
- tumbleweed-0159ede568ef0c869d94d259 — yast2-trans-stats: YaST2 - Translation Statistics; NOT.
- tumbleweed-c8f4c2c6d01069dd3d2fc4b0 — breeze6-wallpapers: Plasma Desktop artwork, styles and assets; NOT.
- tumbleweed-f510b3dff6fb9aea54ecde4b — yast2-qt-branding-openSUSE: openSUSE Tumbleweed branding for YaST2 Qt; NOT.
- tumbleweed-1aab5a897328c80e9013865f — plymouth-theme-spinner: Plymouth "Spinner" theme; NOT.
- tumbleweed-6d886abe9a6cda2c58a8257c — yast2-theme: YaST2 - Theme; NOT.
- tumbleweed-9204233e0aa0cf9aab69c1ef — plymouth-theme-bgrt: Plymouth "bgrt" theme; NOT.
- tumbleweed-9fc24fec2b1fcf347973ce46 — plymouth-branding-openSUSE: openSUSE Tumbleweed branding for Plymouth bootsplash; NOT.

## Rule firmware

S2.2-2,S2.2-16: Firmware files supplied to drivers implement device capabilities and are system-changeable; MUST. The firmware metapackage is reviewed separately.

Ten hand-checked examples (description checked against role):

- tumbleweed-724711caee15a8fa7ea2080c — `kernel-firmware-usb-network`: Kernel firmware files for various USB WiFi / Ethernet drivers. Check: MUST; Kernel firmware files for various USB WiFi / Ethernet drivers.
- tumbleweed-dd8ee3785f6f285fb48e576f — `kernel-firmware-ueagle`: Kernel firmware files for Eagle IV USB ADSL modem driver. Check: MUST; Kernel firmware files for Eagle IV USB ADSL modem driver.
- tumbleweed-bd29f6f54c4489b6a855d409 — `kernel-firmware-ti`: Kernel firmware files for Texas Instruments wireless drivers. Check: MUST; Kernel firmware files for Texas Instruments wireless drivers.
- tumbleweed-e03a008188b0349326fcc821 — `kernel-firmware-sound`: Kernel firmware files for various sound drivers. Check: MUST; Kernel firmware files for various sound drivers.
- tumbleweed-cdc3b0868985c57eb8fec9e2 — `kernel-firmware-serial`: Kernel firmware files for various serial drivers. Check: MUST; Kernel firmware files for various serial drivers.
- tumbleweed-c7befae8bed637e53273cfea — `kernel-firmware-realtek`: Kernel firmware files for Realtek wireless drivers. Check: MUST; Kernel firmware files for Realtek wireless drivers.
- tumbleweed-425c386939a5e074eab65e53 — `kernel-firmware-radeon`: Kernel firmware files for Radeon graphics driver. Check: MUST; Kernel firmware files for Radeon graphics driver.
- tumbleweed-70d07efd9d1f5cffc3cb0921 — `kernel-firmware-qlogic`: Kernel firmware files for QLogic network drivers. Check: MUST; Kernel firmware files for QLogic network drivers.
- tumbleweed-37e13f1077d9f71f79cb9837 — `kernel-firmware-qcom`: Kernel firmware files for Qualcomm device drivers. Check: MUST; Kernel firmware files for Qualcomm device drivers.
- tumbleweed-2c5c2e67d511379fe0eedc3f — `kernel-firmware-platform`: Kernel firmware files for various platform drivers. Check: MUST; Kernel firmware files for various platform drivers.

## Rule systemrules

S2.2-1,S2.2-2,S2.2-15: Documented rules affecting system-wide accounts, access, multiple programs, hardware handling or service activation change system behavior; MUST.

Ten hand-checked examples (description checked against role):

- tumbleweed-9c9a31c174eb5087255797d8 — `btrfsprogs-udev-rules`: Udev rules for configuring btrfs file systems. Check: MUST; Udev rules for configuring btrfs file systems.
- tumbleweed-81ef65c1ae2937fc90855b48 — `systemd-presets-common-SUSE`: Systemd default presets for SUSE distributions. Check: MUST; Systemd default presets for SUSE distributions.
- tumbleweed-5b055dad34fdb2510e5fbec4 — `permissions-config`: SUSE Linux Default Permissions config files. Check: MUST; SUSE Linux Default Permissions config files.
- tumbleweed-d662b0ca91e5066d46c114e5 — `login_defs`: The login.defs configuration file. Check: MUST; The login.defs configuration file.
- tumbleweed-7d45a3b81903e644cb0a1a7b — `systemd-presets-branding-openSUSE`: Systemd default presets for openSUSE. Check: MUST; Systemd default presets for openSUSE.
- tumbleweed-255999ada4afb173b049b428 — `permissions`: SUSE Linux Default Permissions. Check: MUST; SUSE Linux Default Permissions.
- tumbleweed-bda85357fedd335a5cb58962 — `crypto-policies`: System-wide crypto policies. Check: MUST; System-wide crypto policies.
- tumbleweed-56798c3832841b5fa72f428c — `polkit-default-privs`: SUSE PolicyKit default permissions. Check: MUST; SUSE PolicyKit default permissions.
- tumbleweed-1a1a7279a135dfcb57862153 — `selinux-policy`: SELinux policy configuration. Check: MUST; SELinux policy configuration.
- tumbleweed-af1e8e3ac0ae67a3d1085d6b — `selinux-policy-targeted`: SELinux targeted base policy. Check: MUST; SELinux targeted base policy.

## Rule docs

S2.2-4: Documentation, man pages and license texts are content. Removing them removes only the supplied documents: NOT.

Ten hand-checked examples (description checked against role):

- tumbleweed-0f41df0655e967611e3bf2d4 — `boost-license1_92_0`: Boost License. Check: NOT; Boost License.
- tumbleweed-82f198b84f0a837b3d019a68 — `cryptsetup-doc`: Cryptsetup Documentation. Check: NOT; Cryptsetup Documentation.
- tumbleweed-3fe4a22b49973ebea268d0e2 — `kaddressbook-doc`: Documentation for kaddressbook. Check: NOT; Documentation for kaddressbook.
- tumbleweed-c028a41281b0380c204f3025 — `pam-manpages`: Manualpages for Pluggable Authentication Modules. Check: NOT; Manualpages for Pluggable Authentication Modules.
- tumbleweed-64435b11463ed9cdda92a153 — `unzip-doc`: Documentation files for unzip. Check: NOT; Documentation files for unzip.
- tumbleweed-17fdad9c009ebecc797d552f — `bash-doc`: Documentation on how to use the GNU Bourne-Again Shell. Check: NOT; Documentation on how to use the GNU Bourne-Again Shell.
- tumbleweed-503a2a8840f0eee326685f81 — `coreutils-doc`: Documentation for the GNU Core Utilities. Check: NOT; Documentation for the GNU Core Utilities.
- tumbleweed-1262fb67b31e2d0ce2899fd8 — `coreutils-systemd-doc`: Documentation for the GNU Core Utilities. Check: NOT; Documentation for the GNU Core Utilities.
- tumbleweed-584ac100b9634a333ea60306 — `info-std`: The info pages of the Info Browser. Check: NOT; The info pages of the Info Browser.
- tumbleweed-932ec7bb00e03939ae99dec9 — `man-pages`: Linux Manual Pages. Check: NOT; Linux Manual Pages.

## Rule accounts

S2.2-1,S2.2-15: Packages expressly providing system accounts or groups establish accounts/access rights: MUST.

Ten hand-checked examples (description checked against role):

- tumbleweed-581dc7f25f20a1e28db1ed8a — `system-user-root`: System user and group root. Check: MUST; System user and group root.
- tumbleweed-21147f7a49a36d49f7e90a1b — `system-user-tftp`: System user and group tftp. Check: MUST; System user and group tftp.
- tumbleweed-199aefaf0b2e48faf3b4ecbf — `system-user-nobody`: System user and group nobody. Check: MUST; System user and group nobody.
- tumbleweed-c1b44d232b18646f973866a6 — `system-user-man`: System user and group 'man'. Check: MUST; System user and group 'man'.
- tumbleweed-7a50559cd5b0631eef1c29a5 — `system-user-lp`: System user lp. Check: MUST; System user lp.
- tumbleweed-aadadfa0b4d6b609a064b9a4 — `system-user-flatpak`: System user for the flatpak system helper. Check: MUST; System user for the flatpak system helper.
- tumbleweed-3007827ae54d64f608b15663 — `system-user-daemon`: System user and group 'daemon'. Check: MUST; System user and group 'daemon'.
- tumbleweed-c05e5872551d2cca1bb3ac4c — `system-user-bin`: System user and group 'bin'. Check: MUST; System user and group 'bin'.
- tumbleweed-d0d7287450da9982552a7ec9 — `system-group-wheel`: System group 'wheel'. Check: MUST; System group 'wheel'.
- tumbleweed-5e72b8b86230d393ccaa6a34 — `system-group-kvm`: System group kvm. Check: MUST; System group kvm.

## Individual exceptions

- tumbleweed-c7ac4a140066a37feed0450b — `dbus-broker-block-restart`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-57e50cddde9ed86fbce3d1d5 — `libnl-config`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-ad652a1173c64b17a408185a — `libsemanage-conf`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-ef50d89379c7e871dae8bd93 — `libtirpc-netconfig`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-d498682ee466c92a9bda41af — `openal-soft-data`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-0e525d3910526d6eee658d42 — `xorg-x11-libX11-ccache`: NOT. Precomputed compose-file cache accelerates processing; removing it leaves the underlying functionality available.
- tumbleweed-d8740b0efbb387551a5f8266 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-555aaab3c0b41a2d668cec0d — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-f0da0e6ac4776e60abf294fc — `alsa-ucm-conf`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-e3d3873501cf7db4507694a3 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-a6fae8b63e5f860e9a3120a9 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-e6a0cad2e99c05eaa9b60f3d — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-27de7a07eb2d915e8d077283 — `libplasma6-desktoptheme`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-dc765c68f43062a7012cce85 — `mozilla-nss-certs`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-58bfaed75b767465bff8e84a — `augeas-lenses`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-76b744f6e5224226b42c953c — `ca-certificates-mozilla`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-56e10a9583dfdf4bb1f034fc — `docbook-xsl-stylesheets`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-f1666f13a7a062c4114b60de — `breeze6-decoration`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-2a26e0ab4eebc2800ede336b — `breeze6-style-qt5`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-8d42513019a08c5e53a35728 — `breeze6`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-13ac61f8cda40017b6ecc6dc — `pam_kwallet6-common`: UNKNOWN. Documentation names support files or providers without establishing whether they are executable code or passive values; ownership inventory is empty.
- tumbleweed-88ccab0957f9ba5efef032af — `kaccounts-providers`: UNKNOWN. Documentation names support files or providers without establishing whether they are executable code or passive values; ownership inventory is empty.
- tumbleweed-b8d3bce61d0c4d8c4fd618cc — `plasma6-theme-openSUSE`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.

Introspection source: https://gi.readthedocs.io/en/latest/architecture.html describes typelibs as “Binary version of the invocation info” and shows libgirepository presenting them to language bindings.

RPM key source: https://rpm.org/docs/6.0.x/man/rpmkeys.8 states: “Digital signatures cannot be verified without the corresponding public key (aka certificate).”

No removal experiment was performed. UNKNOWN support/provider packages have descriptions insufficient to establish executable versus passive payload, and their ownership dump is empty.

## Payload verification and superseding corrections

Public filelists were checked because source-level summaries can describe code held in a separate library package. Source: https://download.opensuse.org/tumbleweed/repo/oss/repodata/7b1bc6a47608886f73287d87e0d5118aa88c8359e40cf145e5da198474c57a078c8a4ed47018525d2378f13081428c790d370005a0ab7e1de42563d55275c9a1-filelists.xml.zst. This verification supersedes any earlier example wording based solely on source summaries.

Rule logginglabels: S2.2-4,S2.2-7,S2.2-13. Packages containing only category labels/aliases plus documentation supply descriptive labels, not code; NOT. Ten manually checked examples:

- tumbleweed-ad71216d622d1dca6742e261 — akonadi-calendar: /usr/share/qlogging-categories6/akonadi-calendar.categories, /usr/share/qlogging-categories6/akonadi-calendar.renamecategories.
- tumbleweed-dcb819e6db4b67a32f27764f — akonadi-mime: /usr/share/qlogging-categories6/akonadi-mime.categories.
- tumbleweed-4177d74ef2db56b8164d8bd8 — calendarsupport: /usr/share/qlogging-categories6/calendarsupport.categories, /usr/share/qlogging-categories6/calendarsupport.renamecategories.
- tumbleweed-b92dc84facf07c5fdd78716c — eventviews: /usr/share/qlogging-categories6/eventviews.categories, /usr/share/qlogging-categories6/eventviews.renamecategories.
- tumbleweed-a4301a99f972fd14517f3acd — incidenceeditor: /usr/share/qlogging-categories6/incidenceeditor.categories, /usr/share/qlogging-categories6/incidenceeditor.renamecategories.
- tumbleweed-4932a4e38ea53c0c0477596b — kf6-attica: /usr/share/qlogging-categories6/attica.categories, /usr/share/qlogging-categories6/attica.renamecategories.
- tumbleweed-5405e6ac25114b7cd58058dd — kf6-bluez-qt: /usr/share/qlogging-categories6/bluezqt.categories, /usr/share/qlogging-categories6/bluezqt.renamecategories.
- tumbleweed-58983866de0f514269a145cf — kf6-karchive: /usr/share/qlogging-categories6/karchive.categories, /usr/share/qlogging-categories6/karchive.renamecategories.
- tumbleweed-1c63df883d1b5778cf7c76e9 — kf6-kbookmarks: /usr/share/qlogging-categories6/kbookmarks.renamecategories, /usr/share/qlogging-categories6/kbookmarkswidgets.categories.
- tumbleweed-ddfc3f6ce3f0979f9e904359 — kf6-kcodecs: /usr/share/qlogging-categories6/kcodecs.categories, /usr/share/qlogging-categories6/kcodecs.renamecategories.

Individual corrected payload inspections:

- tumbleweed-ad71216d622d1dca6742e261 — akonadi-calendar: NOT. Payload: /usr/share/qlogging-categories6/akonadi-calendar.categories, /usr/share/qlogging-categories6/akonadi-calendar.renamecategories.
- tumbleweed-effe590234671115bf028903 — akonadi-contacts: HOLE. Payload: /usr/share/kf6/akonadi/contact/data/zone.tab, /usr/share/kf6/akonadi/contact/pics/world.jpg, /usr/share/qlogging-categories6/akonadi-contacts.categories.
- tumbleweed-dcb819e6db4b67a32f27764f — akonadi-mime: NOT. Payload: /usr/share/qlogging-categories6/akonadi-mime.categories.
- tumbleweed-4177d74ef2db56b8164d8bd8 — calendarsupport: NOT. Payload: /usr/share/qlogging-categories6/calendarsupport.categories, /usr/share/qlogging-categories6/calendarsupport.renamecategories.
- tumbleweed-238e48ea1ab5728fcde3b110 — cracklib-dict-full: HOLE. Payload: /usr/share/cracklib/pw_dict.hwm, /usr/share/cracklib/pw_dict.pwd, /usr/share/cracklib/pw_dict.pwi.
- tumbleweed-b92dc84facf07c5fdd78716c — eventviews: NOT. Payload: /usr/share/qlogging-categories6/eventviews.categories, /usr/share/qlogging-categories6/eventviews.renamecategories.
- tumbleweed-66ed6c20efbe0f068d1a3273 — freecell-solver-presets: MUST. Payload: /usr/share/freecell-solver/presetrc, /usr/share/freecell-solver/presets/abra-kadabra.sh, /usr/share/freecell-solver/presets/amateur-star.sh.
- tumbleweed-94733f055f9f9e259def1555 — gtk3-schema: HOLE. Payload: /usr/share/glib-2.0/schemas/org.gtk.Demo.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml.
- tumbleweed-1c13d4d6011ae45ca83363fb — gtk4-schema: HOLE. Payload: /usr/share/glib-2.0/schemas/org.gtk.gtk4.Inspector.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml.
- tumbleweed-a4301a99f972fd14517f3acd — incidenceeditor: NOT. Payload: /usr/share/qlogging-categories6/incidenceeditor.categories, /usr/share/qlogging-categories6/incidenceeditor.renamecategories.
- tumbleweed-4932a4e38ea53c0c0477596b — kf6-attica: NOT. Payload: /usr/share/qlogging-categories6/attica.categories, /usr/share/qlogging-categories6/attica.renamecategories.
- tumbleweed-5405e6ac25114b7cd58058dd — kf6-bluez-qt: NOT. Payload: /usr/share/qlogging-categories6/bluezqt.categories, /usr/share/qlogging-categories6/bluezqt.renamecategories.
- tumbleweed-58983866de0f514269a145cf — kf6-karchive: NOT. Payload: /usr/share/qlogging-categories6/karchive.categories, /usr/share/qlogging-categories6/karchive.renamecategories.
- tumbleweed-1c63df883d1b5778cf7c76e9 — kf6-kbookmarks: NOT. Payload: /usr/share/qlogging-categories6/kbookmarks.categories, /usr/share/qlogging-categories6/kbookmarks.renamecategories, /usr/share/qlogging-categories6/kbookmarkswidgets.categories.
- tumbleweed-ddfc3f6ce3f0979f9e904359 — kf6-kcodecs: NOT. Payload: /usr/share/qlogging-categories6/kcodecs.categories, /usr/share/qlogging-categories6/kcodecs.renamecategories.
- tumbleweed-3ca96ec2e4dad04e30927bb1 — kf6-kcolorscheme: NOT. Payload: /usr/share/qlogging-categories6/kcolorscheme.categories.
- tumbleweed-9321e330cfc32c06a725a989 — kf6-kcompletion: NOT. Payload: /usr/share/qlogging-categories6/kcompletion.categories.
- tumbleweed-6a50fe2fbf58a513826d1501 — kf6-kconfigwidgets: HOLE. Payload: /usr/share/locale/af/kf6_entry.desktop, /usr/share/locale/ar/kf6_entry.desktop, /usr/share/locale/as/kf6_entry.desktop.
- tumbleweed-3aecb042f881b2a94ac5abce — kf6-kcontacts: NOT. Payload: /usr/share/qlogging-categories6/kcontacts.categories, /usr/share/qlogging-categories6/kcontacts.renamecategories.
- tumbleweed-40dd874ebc42494ff32aef06 — kf6-kcrash: NOT. Payload: /usr/share/qlogging-categories6/kcrash.categories, /usr/share/qlogging-categories6/kcrash.renamecategories.
- tumbleweed-546164c6e23808c3873d5591 — kf6-kdav: NOT. Payload: /usr/share/qlogging-categories6/kdav.categories, /usr/share/qlogging-categories6/kdav.renamecategories.
- tumbleweed-ce2e994a9b7e086f585b0ae7 — kf6-kdbusaddons: NOT. Payload: /usr/share/qlogging-categories6/kdbusaddons.categories, /usr/share/qlogging-categories6/kdbusaddons.renamecategories.
- tumbleweed-a46f3cb29437313807396ce6 — kf6-kglobalaccel: NOT. Payload: /usr/share/qlogging-categories6/kglobalaccel.categories, /usr/share/qlogging-categories6/kglobalaccel.renamecategories.
- tumbleweed-49cf0696219df6d1fef9d0c8 — kf6-kholidays: NOT. Payload: /usr/share/qlogging-categories6/kholidays.categories.
- tumbleweed-4f9b8ac208e593f05af10108 — kf6-kidletime: NOT. Payload: /usr/share/qlogging-categories6/kidletime.categories, /usr/share/qlogging-categories6/kidletime.renamecategories.
- tumbleweed-3dbbb8eeb29fac511481e787 — kf6-kitemviews: NOT. Payload: /usr/share/qlogging-categories6/kitemviews.categories.
- tumbleweed-cf13112a814714d9e4d7c14a — kf6-kjobwidgets: NOT. Payload: /usr/share/qlogging-categories6/kjobwidgets.categories, /usr/share/qlogging-categories6/kjobwidgets.renamecategories.
- tumbleweed-3410446f1ed72703ac24b55d — kf6-kmime: NOT. Payload: /usr/share/qlogging-categories6/kmime.categories, /usr/share/qlogging-categories6/kmime.renamecategories.
- tumbleweed-b2cf17e87aa6993326191dda — kf6-knotifications: NOT. Payload: /usr/share/qlogging-categories6/knotifications.categories, /usr/share/qlogging-categories6/knotifications.renamecategories.
- tumbleweed-cb16344a8ce1ddc867d25f01 — kf6-knotifyconfig: NOT. Payload: /usr/share/qlogging-categories6/knotifyconfig.categories.
- tumbleweed-c265baa129e0a3048ca3783c — kf6-kparts: NOT. Payload: /usr/share/qlogging-categories6/kparts.categories.
- tumbleweed-7b6aa4e6c7766d530389c967 — kf6-kpty: NOT. Payload: /usr/share/qlogging-categories6/kpty.categories.
- tumbleweed-d3ede3314d71b10c5ccf6bc1 — kf6-krunner: NOT. Payload: /usr/share/qlogging-categories6/krunner.categories, /usr/share/qlogging-categories6/krunner.renamecategories.
- tumbleweed-3905173803e5628b56b34e44 — kf6-kstatusnotifieritem: NOT. Payload: /usr/share/qlogging-categories6/kstatusnotifieritem.categories.
- tumbleweed-b662958ef523497c1a6b6f7e — kf6-kunitconversion: NOT. Payload: /usr/share/qlogging-categories6/kunitconversion.categories.
- tumbleweed-a9a509d26eddcee3768333c7 — kf6-kuserfeedback: NOT. Payload: /usr/share/qlogging-categories6/org_kde_UserFeedback.categories.
- tumbleweed-8bb555ff0660f03cd18f62f1 — kf6-kwallet: NOT. Payload: /usr/share/qlogging-categories6/kwallet.categories, /usr/share/qlogging-categories6/kwallet.renamecategories.
- tumbleweed-95730b8532cda7be903ef338 — kf6-kwidgetsaddons: NOT. Payload: /usr/share/qlogging-categories6/kwidgetsaddons.categories.
- tumbleweed-1b0524dd130f0ac4bd3d3a7c — kf6-kxmlgui: NOT. Payload: /usr/share/qlogging-categories6/kxmlgui.categories, /usr/share/qlogging-categories6/kxmlgui.renamecategories.
- tumbleweed-a209572637b5cb0c0001cb10 — kf6-modemmanager-qt: NOT. Payload: /usr/share/qlogging-categories6/modemmanagerqt.categories, /usr/share/qlogging-categories6/modemmanagerqt.renamecategories.
- tumbleweed-811408d0a9f055f84c15e74d — kf6-networkmanager-qt: NOT. Payload: /usr/share/qlogging-categories6/networkmanagerqt.categories, /usr/share/qlogging-categories6/networkmanagerqt.renamecategories.
- tumbleweed-20f37ce3fde24cfe6a9cc3fe — kf6-prison: NOT. Payload: /usr/share/qlogging-categories6/prison.categories, /usr/share/qlogging-categories6/prison.renamecategories.
- tumbleweed-064a19e73856f6118be94f4c — kf6-solid: NOT. Payload: /usr/share/qlogging-categories6/solid.categories, /usr/share/qlogging-categories6/solid.renamecategories.
- tumbleweed-059593370a95934f4cb8f7fd — kf6-syndication: NOT. Payload: /usr/share/qlogging-categories6/syndication.categories, /usr/share/qlogging-categories6/syndication.renamecategories.
- tumbleweed-324e8048b157aca3c0d3e352 — kglobalacceld6: NOT. Payload: /usr/share/qlogging-categories6/kglobalacceld.categories.
- tumbleweed-718448a6a632567a048d5041 — kidentitymanagement: NOT. Payload: /usr/share/qlogging-categories6/kidentitymanagement.categories, /usr/share/qlogging-categories6/kidentitymanagement.renamecategories.
- tumbleweed-1cb70a69bdb75319620778db — kimap: NOT. Payload: /usr/share/qlogging-categories6/kimap.categories, /usr/share/qlogging-categories6/kimap.renamecategories.
- tumbleweed-6c6b04c67e41eebd25d6632a — kmbox: NOT. Payload: /usr/share/qlogging-categories6/kmbox.categories, /usr/share/qlogging-categories6/kmbox.renamecategories.
- tumbleweed-cf356d684d50cb522b4a7456 — kontactinterface: NOT. Payload: /usr/share/qlogging-categories6/kontactinterface.categories, /usr/share/qlogging-categories6/kontactinterface.renamecategories.
- tumbleweed-e3ec7c645d0303a75a81af0c — kpimtextedit: NOT. Payload: /usr/share/qlogging-categories6/kpimtextedit.categories.
- tumbleweed-5e271c939fb929db0c8692be — kpkpass: NOT. Payload: /usr/share/qlogging-categories6/org_kde_kpkpass.categories.
- tumbleweed-142611cc5e946fee6c2cbd1e — kscreenlocker6-imports: HOLE. Payload: /usr/lib64/qt6/qml/org/kde/kscreenlocker/kscreenlocker_greet.qmltypes, /usr/lib64/qt6/qml/org/kde/kscreenlocker/qmldir.
- tumbleweed-30ef83f71326677301415692 — ksmtp: NOT. Payload: /usr/share/qlogging-categories6/ksmtp.categories.
- tumbleweed-54ffce2db8ebee996775a4a3 — kwayland6: NOT. Payload: /usr/share/qlogging-categories6/kwayland.categories, /usr/share/qlogging-categories6/kwayland.renamecategories.
- tumbleweed-ff341235b6a6b85b4a229442 — libX11-data: HOLE. Payload: /usr/share/X11/XErrorDB, /usr/share/X11/Xcms.txt, /usr/share/X11/locale/C/Compose.
- tumbleweed-8da91186d1f050933803f022 — libgravatar: NOT. Payload: /usr/share/qlogging-categories6/libgravatar.categories, /usr/share/qlogging-categories6/libgravatar.renamecategories.
- tumbleweed-ff5a40235b19dda44ab14272 — libkdcraw-qt6: NOT. Payload: /usr/share/qlogging-categories6/libkdcraw.categories.
- tumbleweed-d098194c82a02b391c39a274 — libkexiv2-qt6: NOT. Payload: /usr/share/qlogging-categories6/libkexiv2.categories.
- tumbleweed-f930414351a4a1b2409054de — libksieve: HOLE. Payload: /usr/share/knsrcfiles/ksieve_script.knsrc, /usr/share/qlogging-categories6/libksieve.categories, /usr/share/qlogging-categories6/libksieve.renamecategories.
- tumbleweed-16fb885c3a893800e8e1b4b5 — libqaccessibilityclient-qt6: NOT. Payload: /usr/share/qlogging-categories6/libqaccessibilityclient.categories.
- tumbleweed-389082f789dff57ea9a3006e — mailcommon: NOT. Payload: /usr/share/qlogging-categories6/mailcommon.categories, /usr/share/qlogging-categories6/mailcommon.renamecategories.
- tumbleweed-c95b5e50b33872fb68a16eb6 — mailimporter: NOT. Payload: /usr/share/qlogging-categories6/mailimporter.categories, /usr/share/qlogging-categories6/mailimporter.renamecategories.
- tumbleweed-7227fee0dfbb99b63174d021 — mimetreeparser: NOT. Payload: /usr/share/qlogging-categories6/mimetreeparser.categories.
- tumbleweed-78b05b6d088bac9e598205f7 — pimcommon: NOT. Payload: /usr/share/qlogging-categories6/pimcommon.categories, /usr/share/qlogging-categories6/pimcommon.renamecategories.
- tumbleweed-816d6c5d6a1ef36b976abcfb — plasma6-activities: NOT. Payload: /usr/share/qlogging-categories6/plasma-activities.categories, /usr/share/qlogging-categories6/plasma-activities.renamecategories.
- tumbleweed-4ea8d2ead3a27fdab0050c13 — plasma6-activities-stats: NOT. Payload: /usr/share/qlogging-categories6/plasma-activities-stats.categories, /usr/share/qlogging-categories6/plasma-activities-stats.renamecategories.
- tumbleweed-3d4c57fc4aefee47626583de — rgb: MUST. Payload: /usr/bin/showrgb, /usr/share/X11/rgb.txt.
- tumbleweed-bd1b1ad9cc51890ba30622ec — terminfo-base: MUST. Payload: /etc/termcap, /usr/bin/termerase, /usr/share/misc/termcap.
- tumbleweed-b8844433a232609731e25abb — girepository-1_0: HOLE. Payload: /usr/lib64/girepository-1.0/DBus-1.0.typelib, /usr/lib64/girepository-1.0/DBusGLib-1.0.typelib, /usr/lib64/girepository-1.0/GIRepository-2.0.typelib.
- tumbleweed-67486972373cb0f28ea8c779 — Mesa: HOLE. Payload: .
- tumbleweed-e605cf8492e45b603637b5d5 — rpm-config-SUSE: MUST. Payload: /usr/lib/rpm/brp-suse, /usr/lib/rpm/fileattrs/firmware.attr, /usr/lib/rpm/fileattrs/kernel.attr.
- tumbleweed-4545c25860335fbbb54f7242 — shared-mime-info: MUST. Payload: /usr/bin/update-mime-database, /usr/lib/rpm/macros.d/macros.shared-mime-info, /usr/share/gettext/its/shared-mime-info.its.
- tumbleweed-95709d632bb78c758db4db62 — libssh-config: HOLE. Payload: /usr/etc/libssh/libssh_client.config, /usr/etc/libssh/libssh_server.config.
- tumbleweed-c9074ea775e56a8c729f3272 — kf6-kcoreaddons: HOLE. Payload: /usr/share/mime/packages/kde6.xml, /usr/share/qlogging-categories6/kcoreaddons.categories, /usr/share/qlogging-categories6/kcoreaddons.renamecategories.
- tumbleweed-7781b81cdd531b4c92391295 — kcoreaddons: HOLE. Payload: /usr/share/kf5/licenses/ARTISTIC, /usr/share/kf5/licenses/BSD, /usr/share/kf5/licenses/GPL_V2.
- tumbleweed-a2af4e5d036288899230dad9 — kdoctools: MUST. Payload: /usr/bin/checkXML5, /usr/bin/meinproc5, /usr/share/kf5/kdoctools/customization/README.
- tumbleweed-4b07c4c7f4e07e54f7d27a8e — libKF5DocTools5: MUST. Payload: /usr/lib64/libKF5DocTools.so.5, /usr/lib64/libKF5DocTools.so.5.116.0.
- tumbleweed-5cb38da8ace4818e55967f7b — ruby: HOLE. Payload: .
- tumbleweed-cb7a1b9080ffbdae219abc2c — kf6-kdoctools: MUST. Payload: /usr/bin/checkXML6, /usr/bin/meinproc6, /usr/share/kf6/kdoctools/customization/af/catalog.xml.
- tumbleweed-c77ebc23069bbe8596dff10d — yast2-country-data: MUST. Payload: /usr/share/YaST2/data/languages/language_af_ZA.ycp, /usr/share/YaST2/data/languages/language_ar_EG.ycp, /usr/share/YaST2/data/languages/language_ast_ES.ycp.
- tumbleweed-5fa45966f561960d04de8d01 — openssl: HOLE. Payload: .
- tumbleweed-62806377d9c1aad47a8a1587 — libKF6DocTools6: MUST. Payload: /usr/lib64/libKF6DocTools.so.6, /usr/lib64/libKF6DocTools.so.6.32.0.
- tumbleweed-d5d61f27fcecb455461283e1 — qalculate-data: HOLE. Payload: /usr/share/qalculate/currencies.xml, /usr/share/qalculate/datasets.xml, /usr/share/qalculate/elements.xml.
- tumbleweed-0b930082aeaa5454d0b21f09 — tesseract-ocr-common: HOLE. Payload: /usr/share/tessdata/configs/alto, /usr/share/tessdata/configs/ambigs.train, /usr/share/tessdata/configs/api_config.
- tumbleweed-f0209fbc9694ef2b0a11140d — kf6-ksvg: NOT. Payload: /usr/share/qlogging-categories6/ksvg.categories.
- tumbleweed-1c7bbc9651e3117e1332ebc5 — dbus-1: HOLE. Payload: .
- tumbleweed-2704d243d710bba19ef6616f — openssh: HOLE. Payload: .
- tumbleweed-974c6a6e6058683d4f9f985d — yast2-control-center: HOLE. Payload: /usr/share/applications/org.opensuse.YaST.desktop, /usr/share/icons/hicolor/scalable/apps/yast-control-center.svg, /usr/share/icons/hicolor/symbolic/apps/yast-control-center-symbolic.svg.
- tumbleweed-5917e63796071bd56bc521c5 — xterm: HOLE. Payload: /usr/share/applications/xterm.desktop, /usr/share/pixmaps/filled-xterm_16x16.xpm, /usr/share/pixmaps/filled-xterm_32x32.xpm.
- tumbleweed-49b7e58c9ade1153330e3892 — yast2-theme-breeze: HOLE. Payload: /usr/share/icons/breeze-dark/apps/32/pattern-basis-addon.svg, /usr/share/icons/breeze-dark/apps/32/pattern-basis-devel.svg, /usr/share/icons/breeze-dark/apps/32/pattern-basis.svg.
- tumbleweed-53b281acb9a167690cdee264 — khelpcenter: MUST. Payload: /usr/bin/khelpcenter, /usr/libexec/khc_mansearch.py, /usr/libexec/khc_xapianindexer.
- tumbleweed-a7932bee81af8eff1a35652f — kf6-purpose-services: HOLE. Payload: /usr/share/accounts/services/kde/google-youtube.service, /usr/share/accounts/services/kde/nextcloud-upload.service.
- tumbleweed-ccbf06b5d53eb0e656661f73 — ktnef-debug-categories: NOT. Payload: /usr/share/qlogging-categories6/ktnef.categories, /usr/share/qlogging-categories6/ktnef.renamecategories.
- tumbleweed-98ea5f9f5792a1578edd7016 — libkdegames: NOT. Payload: /usr/share/qlogging-categories6/libkdegames.categories.
- tumbleweed-3b3a80c65b40f0cd6d838b21 — libkdepim: NOT. Payload: /usr/share/qlogging-categories6/libkdepim.categories, /usr/share/qlogging-categories6/libkdepim.renamecategories.
- tumbleweed-0e7d57f7eff2ff2d962b042f — libkgapi6: NOT. Payload: /usr/share/qlogging-categories6/libkgapi.categories.
- tumbleweed-6133fb619cc177cebd450517 — libkleo: HOLE. Payload: /etc/xdg/libkleopatrarc, /usr/share/libkleopatra/pics/smartcard.xpm, /usr/share/qlogging-categories6/libkleo.categories.
- tumbleweed-139df17d42bdf459183ce14d — libkmahjongg: HOLE. Payload: /usr/share/kmahjongglib/backgrounds/chinese_landscape.desktop, /usr/share/kmahjongglib/backgrounds/chinese_landscape.svgz, /usr/share/kmahjongglib/backgrounds/color_plain.desktop.
- tumbleweed-a9f781f6fa923e586a78340a — libpaper: HOLE. Payload: /etc/paperspecs.
- tumbleweed-f3e1feec55bb77366429903b — myspell-lightproof-en: MUST. Payload: /usr/lib64/libreoffice/share/extensions/lightproof-en/Lightproof.components, /usr/lib64/libreoffice/share/extensions/lightproof-en/Lightproof.py, /usr/lib64/libreoffice/share/extensions/lightproof-en/Linguistic.xcu.
- tumbleweed-dc765c68f43062a7012cce85 — mozilla-nss-certs: MUST. Payload: /usr/lib64/libnssckbi.so.
- tumbleweed-1045ff1e7efbe5cb410ee837 — libfido2-udev: MUST. Payload: /usr/lib/udev/rules.d/70-fido2.rules.
- tumbleweed-d04fc937c2b7df2241677eaf — desktop-data-openSUSE: MUST. Payload: /etc/profile.d/desktop-data.csh, /etc/profile.d/desktop-data.sh, /etc/xdg/menus/applications.menu.
- tumbleweed-56e10a9583dfdf4bb1f034fc — docbook-xsl-stylesheets: MUST. Payload: /etc/xml/catalog.d/docbook-xsl-stylesheets.xml, /usr/share/xml/docbook/stylesheet/nwalsh/1.79.2/VERSION, /usr/share/xml/docbook/stylesheet/nwalsh/1.79.2/VERSION.xsl.
- tumbleweed-f1666f13a7a062c4114b60de — breeze6-decoration: MUST. Payload: /usr/lib64/qt6/plugins/org.kde.kdecoration3.kcm/kcm_breezedecoration.so, /usr/lib64/qt6/plugins/org.kde.kdecoration3/org.kde.breeze.so, /usr/share/applications/kcm_breezedecoration6.desktop.
- tumbleweed-2a26e0ab4eebc2800ede336b — breeze6-style-qt5: MUST. Payload: /usr/lib64/qt5/plugins/styles/breeze5.so.
- tumbleweed-39868119fbc3c121f2e07895 — purge-kernels-service: MUST. Payload: /usr/lib/systemd/system/purge-kernels.service.
- tumbleweed-aac6aa8494b1f3e8c0028242 — grub2: HOLE. Payload: .
- tumbleweed-13ac61f8cda40017b6ecc6dc — pam_kwallet6-common: MUST. Payload: /etc/xdg/autostart/pam_kwallet_init.desktop, /usr/lib/systemd/user/plasma-kwallet-pam.service, /usr/libexec/pam_kwallet_init.
- tumbleweed-344dbaf5493cb095a81695b2 — vlc: HOLE. Payload: /usr/share/applications/vlc-openbd.desktop, /usr/share/applications/vlc-opencda.desktop, /usr/share/applications/vlc-opendvd.desktop.
- tumbleweed-88ccab0957f9ba5efef032af — kaccounts-providers: MUST. Payload: /usr/lib64/qt6/plugins/kaccounts/ui/nextcloud_plugin_kaccounts.so, /usr/lib64/qt6/plugins/kaccounts/ui/owncloud_plugin_kaccounts.so, /usr/share/accounts/providers/kde/google.provider.
- tumbleweed-c225ad126cda23f96aa4609e — plasma6-sddm-theme-openSUSE: HOLE. Payload: /usr/lib/sddm/sddm.conf.d/20-breeze-openSUSE.conf, /usr/share/sddm/themes/breeze-openSUSE/Background.qml, /usr/share/sddm/themes/breeze-openSUSE/KeyboardButton.qml.
- tumbleweed-b8d3bce61d0c4d8c4fd618cc — plasma6-theme-openSUSE: MUST. Payload: /usr/share/color-schemes/openSUSE.colors, /usr/share/color-schemes/openSUSEdark.colors, /usr/share/icons/breeze-dark/places/16/start-here-branding.svg.
- tumbleweed-7920eda55c2de20a6c5a0725 — plasma6-session: HOLE. Payload: /usr/share/wayland-sessions/plasmawayland.desktop.

Source summaries were not used to claim shared libraries in packages whose filelists only contain descriptions. Browser help JavaScript is confined to rendering help; its presence does not turn help data into unrestricted code.

## Final rule samples after payload corrections

These final ten-row checks supersede initial samples for code, settings, data and metadata. Each listed payload was inspected; irrelevant documentation paths are excluded from the examples.

### code

- tumbleweed-60c4817b88fb7bd852b85007 — gxditview; MUST; payload example: /usr/bin/gxditview, /usr/share/X11/app-defaults/GXditview.
- tumbleweed-197b296a65b71dde96352fc5 — python313-pycairo; MUST; payload example: /usr/lib64/python3.13/site-packages/cairo/__init__.py, /usr/lib64/python3.13/site-packages/cairo/__init__.pyi.
- tumbleweed-431845990e7a6c4e40daa124 — python313-puremagic; MUST; payload example: /usr/bin/puremagic, /usr/bin/puremagic-3.13.
- tumbleweed-9d78f81908b4597563af8e98 — python313-nftables; MUST; payload example: /usr/lib/python3.13/site-packages/nftables-0.1.dist-info/INSTALLER, /usr/lib/python3.13/site-packages/nftables-0.1.dist-info/METADATA.
- tumbleweed-694c4e45b94cb4ea75d264d0 — python313-hyperframe; MUST; payload example: /usr/lib/python3.13/site-packages/hyperframe-6.1.0.dist-info/INSTALLER, /usr/lib/python3.13/site-packages/hyperframe-6.1.0.dist-info/METADATA.
- tumbleweed-57b744fba8565804434dea06 — Mesa-libva; MUST; payload example: /usr/lib64/dri/nouveau_drv_video.so, /usr/lib64/dri/r600_drv_video.so.
- tumbleweed-6b071013d72da654f2636b71 — busybox-static; MUST; payload example: /usr/bin/busybox-static.
- tumbleweed-f627c6779989d2a4bdc9eb96 — compat-usrmerge-tools; MUST; payload example: /usr/bin/usrmergecheck, /usr/libexec/convertfs.
- tumbleweed-50852ceddd763a29a0118542 — debuginfod-profile; MUST; payload example: /etc/debuginfod/elfutils.urls, /etc/profile.d/debuginfod.csh.
- tumbleweed-66ed6c20efbe0f068d1a3273 — freecell-solver-presets; MUST; payload example: /usr/share/freecell-solver/presetrc, /usr/share/freecell-solver/presets/abra-kadabra.sh.
### settings

- tumbleweed-a8553410b9fddc2ff2491faa — MozillaFirefox-branding-openSUSE; NOT; payload example: /usr/lib64/firefox/browser/defaults/preferences/firefox-openSUSE.js, /usr/lib64/firefox/defaults/pref/all-openSUSE.js.
- tumbleweed-d86c1763518f3862d3fda0c3 — libreoffice-branding-openSUSE; NOT; payload example: /usr/share/libreoffice/program/flat_logo.svg, /usr/share/libreoffice/program/intro.png.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — ImageMagick-config-7-SUSE; NOT; payload example: /etc/IM-7/policy.xml.
- tumbleweed-0440ecd1e9571cf8cde1be87 — chrony-pool-openSUSE; NOT; payload example: /usr/etc/chrony.d/pool.conf.
- tumbleweed-e788c0407bc909d3a1ff0c64 — NetworkManager-branding-openSUSE; NOT; payload example: /usr/lib/NetworkManager/conf.d/conncheck-openSUSE.conf.
- tumbleweed-88de43bb31abf3d91ab8c376 — PackageKit-branding-openSUSE; NOT; payload example: /etc/PackageKit/PackageKit.conf, /etc/PackageKit/Vendor.conf.
- tumbleweed-a08bac3bb4eead7e0306e601 — flatpak-remote-flathub; NOT; payload example: /etc/flatpak/remotes.d/flathub.flatpakrepo.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — gtk4-branding-openSUSE; NOT; payload example: /usr/share/gtk-4.0/settings.ini.
- tumbleweed-7b897cdfd9256cc00b039c05 — gtk3-branding-openSUSE; NOT; payload example: /etc/gtk-3.0/settings.ini.
- tumbleweed-20e31b9f2ffa6df7884e3b3d — registries-conf-default; NOT; payload example: /usr/share/containers/registries.conf.d/00-suse-registries.conf.
### data

- tumbleweed-effe590234671115bf028903 — akonadi-contacts; HOLE; payload example: /usr/share/kf6/akonadi/contact/data/zone.tab, /usr/share/kf6/akonadi/contact/pics/world.jpg.
- tumbleweed-238e48ea1ab5728fcde3b110 — cracklib-dict-full; HOLE; payload example: /usr/share/cracklib/pw_dict.hwm, /usr/share/cracklib/pw_dict.pwd.
- tumbleweed-d4ff03222fe3efc98f95872f — desktop-translations; HOLE; payload example: /usr/share/locale/af/LC_MESSAGES/desktop_translations.mo, /usr/share/locale/af/LC_MESSAGES/polkit-action-distro-translations.mo.
- tumbleweed-88c6d153fb922b34384bb62c — distribution-logos-openSUSE-Tumbleweed; HOLE; payload example: /usr/share/pixmaps/distribution-logos/apple-touch-icon.png, /usr/share/pixmaps/distribution-logos/apple-touch-icon.svg.
- tumbleweed-3b3aed8cb0eceacdbdbe6dec — file-magic; HOLE; payload example: /etc/magic, /usr/share/file/magic.
- tumbleweed-c3769a3b91a480a1eb8680b6 — gnome-tour-data; HOLE; payload example: /usr/share/gnome-tour/resources.gresource, /usr/share/icons/hicolor/scalable/apps/org.gnome.Tour.svg.
- tumbleweed-753ec04c3399c7c24f6764f9 — gtk3-data; HOLE; payload example: /usr/share/locale/en/LC_MESSAGES/gtk30-properties.mo, /usr/share/locale/en/LC_MESSAGES/gtk30.mo.
- tumbleweed-628aba51170df68037b752da — hicolor-icon-theme; HOLE; payload example: /usr/lib/rpm/macros.d/macros.hicolor, /usr/share/icons/hicolor/icon-theme.cache.
- tumbleweed-fb37a4a8d9cbdde019568fee — iso-codes; HOLE; payload example: /usr/share/iso-codes/json/iso_15924.json, /usr/share/iso-codes/json/iso_3166-1.json.
- tumbleweed-803cd9885d5ac3af08d2e0a6 — kImageAnnotator-lang; HOLE; payload example: /usr/share/kImageAnnotator/translations/kImageAnnotator_ar.qm, /usr/share/kImageAnnotator/translations/kImageAnnotator_bg.qm.
### metadata

- tumbleweed-afd24c8aacb62bb4d83a4713 — branding-openSUSE; HOLE; payload example: /usr/etc/SUSE-brand.
- tumbleweed-7a02732097fb92ad188d98e9 — javapackages-filesystem; HOLE; payload example: /usr/lib/rpm/macros.d/macros.javapackages-filesystem.
- tumbleweed-142611cc5e946fee6c2cbd1e — kscreenlocker6-imports; HOLE; payload example: /usr/lib64/qt6/qml/org/kde/kscreenlocker/kscreenlocker_greet.qmltypes, /usr/lib64/qt6/qml/org/kde/kscreenlocker/qmldir.
- tumbleweed-2f4b0dcaee7ccc4ae3445c43 — patterns-games-games; HOLE; payload example: no operational payload listed.
- tumbleweed-cae0778ca79df14155e00d1c — filesystem; HOLE; payload example: /bin, /lib.
- tumbleweed-46d7dfbc72a2231daf3f2e00 — patterns-glibc-hwcaps-x86_64_v3; HOLE; payload example: no operational payload listed.
- tumbleweed-b6506c20dbd511bc9d1cea43 — typelib-1_0-GLib-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GLib-2.0.typelib.
- tumbleweed-b8844433a232609731e25abb — girepository-1_0; HOLE; payload example: /usr/lib64/girepository-1.0/DBus-1.0.typelib, /usr/lib64/girepository-1.0/DBusGLib-1.0.typelib.
- tumbleweed-54f349aab25a45dcdffb851f — typelib-1_0-GObject-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GObject-2.0.typelib.
- tumbleweed-6f6fb0bebafbad99f7e14193 — typelib-1_0-GModule-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GModule-2.0.typelib.

Verification: 2390 input IDs and 2390 output IDs; equal sets, each ID once; all decisions allowed; description and reason word limits passed. Counts: MUST 2082, NOT 103, HOLE 205, UNKNOWN 0, MIXED 0.

## Confinement re-review amendment

The initial settings samples below are retained only as an audit record and are superseded by the replacement Rule settings list above.

S2.2-7,S2.2-13: Documented passive settings or themes confined to one program need not be recorded. Values are not treated as executable merely because shipped in a package.

Ten hand-checked examples (description checked against role):

- tumbleweed-a8553410b9fddc2ff2491faa — `MozillaFirefox-branding-openSUSE`: openSUSE branding of MozillaFirefox. Check: NOT; openSUSE branding of MozillaFirefox.
- tumbleweed-66ed6c20efbe0f068d1a3273 — `freecell-solver-presets`: Freecell Solver presets. Check: NOT; Freecell Solver presets.
- tumbleweed-d86c1763518f3862d3fda0c3 — `libreoffice-branding-openSUSE`: openSUSE Tumbleweed branding for LibreOffice. Check: NOT; openSUSE Tumbleweed branding for LibreOffice.
- tumbleweed-e605cf8492e45b603637b5d5 — `rpm-config-SUSE`: SUSE specific RPM configuration files. Check: NOT; SUSE specific RPM configuration files.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — `ImageMagick-config-7-SUSE`: SUSE Provided Configuration. Check: NOT; SUSE Provided Configuration.
- tumbleweed-0440ecd1e9571cf8cde1be87 — `chrony-pool-openSUSE`: Chrony preconfiguration for openSUSE. Check: NOT; Chrony preconfiguration for openSUSE.
- tumbleweed-e788c0407bc909d3a1ff0c64 — `NetworkManager-branding-openSUSE`: Default openSUSE branding for NetworkManager configuration file. Check: NOT; Default openSUSE branding for NetworkManager configuration file.
- tumbleweed-88de43bb31abf3d91ab8c376 — `PackageKit-branding-openSUSE`: Simple software installation management software -- openSUSE default configuration. Check: NOT; Simple software installation management software -- openSUSE default configuration.
- tumbleweed-a08bac3bb4eead7e0306e601 — `flatpak-remote-flathub`: Add Flathub repository to system flatpak. Check: NOT; Add Flathub repository to system flatpak.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — `gtk4-branding-openSUSE`: The GTK+ toolkit library (version 3) -- openSUSE theme configuration. Check: NOT; The GTK+ toolkit library (version 3) -- openSUSE theme configuration.


Reviewed corrections:

- tumbleweed-0440ecd1e9571cf8cde1be87 — chrony-pool-openSUSE: MUST. Configures system clock synchronization or system network connectivity assessment; these effects extend beyond the consuming program to other system users.
- tumbleweed-e788c0407bc909d3a1ff0c64 — NetworkManager-branding-openSUSE: MUST. Configures system clock synchronization or system network connectivity assessment; these effects extend beyond the consuming program to other system users.
- tumbleweed-88de43bb31abf3d91ab8c376 — PackageKit-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-a08bac3bb4eead7e0306e601 — flatpak-remote-flathub: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — gtk4-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-7b897cdfd9256cc00b039c05 — gtk3-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-20e31b9f2ffa6df7884e3b3d — registries-conf-default: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-604e994fbd779b550d9377de — breeze6-cursors: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-b9c111aab7a79f2e0d7c33b6 — metatheme-breeze6-common: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-132eadc911f7cc2633da5ffd — gtk3-metatheme-breeze6: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-819b570cdea5ea55df85afe1 — gtk4-metatheme-breeze6: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-1b6ff4c84ec0c06e7e9cac74 — metatheme-adwaita-common: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-b323fb0780ed0774fe52a8c7 — gtk3-metatheme-adwaita: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-21c689370df3d76a7ab7285f — sddm-qt6-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-398f3c80654469a71f15a2fe — sddm-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-06d3881473145922f997835c — plasma6-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-4c394b49c4edbaf1ac753966 — libcontainers-default-policy: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.

Final counts after confinement review: MUST 2084, NOT 86, HOLE 220, UNKNOWN 0, MIXED 0.


# Subset working record: language

# Language package classification notes

Only the assigned pip, pip3, gem and Flatpak rows were classified. Registry summaries establish function, not the inventory labels. Root/user and pip/pip3 duplicates remain distinct input objects. No removal or executable probes were performed.

## Literal decision rule

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

Rule L: Distributions documented as executable interpreter libraries, native bindings, or commands receive MUST under S2.2-9 and S2.2-10. Package membership alone is insufficient. Each distinct distribution function was checked against the publisher description below; the script applies the same executable-code criterion after that check. This includes modules that generate logs or manipulate documents: these objects are the generating code, not the resulting logs or documents.

The certifi distribution includes callable Python code exposing its trust bundle; it is not classified merely from the certificate data. The rbs distribution includes a parser and executable processing library, not just signatures. The same-name registry entries for crit and setools describe different projects; upstream distribution documentation replaces those entries. The rpm and selinux modules use distribution upstream documentation, not similarly named registry shims.

## Manual rule checks

Each check compared input name and version membership, documentation of function, and whether the documented operation executes as interpreter or native library code. All passed Rule L. Twenty checks cover both ecosystems (ten per ecosystem):

- tumbleweed-91003489d9c6d84b6bd5a5e7 — bcrypt: Hashes passwords using executable cryptographic routines. Executable code, Rule L applies.
- tumbleweed-8efb93d0f65e02d08d825b05 — brotli: Compresses and decompresses data using Python bindings. Executable code, Rule L applies.
- tumbleweed-4f4472d16a42b1f89c38355c — cffi: Calls native C functions from Python. Executable code, Rule L applies.
- tumbleweed-03570c53d3d665aace086b68 — configobj: Reads writes and validates configuration files. Executable code, Rule L applies.
- tumbleweed-9c9a5af6cd79f480cfe794d9 — h2: Implements HTTP/2 networking protocol. Executable code, Rule L applies.
- tumbleweed-5389f1cad541525a16e30701 — psutils: Manipulates PDF and PostScript pages. Executable code, Rule L applies.
- tumbleweed-bc22e130404255602beef624 — pycparser: Parses C source code. Executable code, Rule L applies.
- tumbleweed-c29fe5ad92614b05a5b9696a — requests: Makes HTTP requests. Executable code, Rule L applies.
- tumbleweed-38ba6e0ada70367cb00323c9 — six: Provides Python version compatibility routines. Executable code, Rule L applies.
- tumbleweed-2bb73fd5c1d1cf9e3090ad0a — zstandard: Compresses and decompresses data. Executable code, Rule L applies.
- tumbleweed-cd665989a3023f589b8c955c — abbrev: Calculates unique abbreviations for strings. Executable code, Rule L applies.
- tumbleweed-19f11611aab12cf15951c710 — base64: Encodes and decodes Base64 data. Executable code, Rule L applies.
- tumbleweed-712c0b6b0feccc3784259371 — cfa: Reads and modifies configuration files. Executable code, Rule L applies.
- tumbleweed-213114cb508c754fa48336c8 — cheetah: Executes external commands from Ruby. Executable code, Rule L applies.
- tumbleweed-6ea0372074481e2fb1d67cc5 — fileutils: Copies moves and removes files. Executable code, Rule L applies.
- tumbleweed-47c2a344efbc750e157de2cd — irb: Runs an interactive Ruby interpreter. Executable code, Rule L applies.
- tumbleweed-d5182a2190fd7dc51159ca33 — json: Parses and generates JSON data. Executable code, Rule L applies.
- tumbleweed-8c2da33af6ad8dc27dcd837f — net-http: Performs HTTP requests. Executable code, Rule L applies.
- tumbleweed-880947f6f5d67baa5dd38ca1 — rbs: Parses and processes Ruby type signatures. Executable code, Rule L applies.
- tumbleweed-2c852d4eafbf03d1c83b723f — syslog: Writes messages to system logging. Executable code, Rule L applies.

## Documentation evidence

Publisher metadata was retrieved from the linked package-registry API; quoted excerpts are at most twenty words. Raw inventory membership is in the evidence file named by each input row.

- gem abbrev — https://rubygems.org/api/v1/gems/abbrev.json — “Calculates a set of unique abbreviations for a given set of strings”
- gem abstract_method — https://rubygems.org/api/v1/gems/abstract_method.json — “Abstract Method is a tiny library enabling you to define abstract methods in Ruby classes and modules.”
- gem base64 — https://rubygems.org/api/v1/gems/base64.json — “Support for encoding and decoding binary data using a Base64 representation.”
- gem benchmark — https://rubygems.org/api/v1/gems/benchmark.json — “a performance benchmarking library”
- gem bigdecimal — https://rubygems.org/api/v1/gems/bigdecimal.json — “This library provides arbitrary-precision decimal floating-point number class.”
- gem bundler — https://rubygems.org/api/v1/gems/bundler.json — “Bundler manages an application's dependencies through its entire life, across many machines, systematically and repeatably”
- gem cfa — https://rubygems.org/api/v1/gems/cfa.json — “Library offering separation of parsing and file access from the rest of the logic for managing configuraton files. It has”
- gem cfa_grub2 — https://rubygems.org/api/v1/gems/cfa_grub2.json — “Models allowing easy read and modification of GRUB2 configuration files. It is a plugin for cfa framework.”
- gem cgi — https://rubygems.org/api/v1/gems/cgi.json — “Support for the Common Gateway Interface protocol.”
- gem cheetah — https://rubygems.org/api/v1/gems/cheetah.json — “Your swiss army knife for executing external commands in Ruby safely and conveniently.”
- gem csv — https://rubygems.org/api/v1/gems/csv.json — “The CSV library provides a complete interface to CSV files and data. It offers tools to enable you to read”
- gem date — https://rubygems.org/api/v1/gems/date.json — “The official date library for Ruby.”
- gem debug — https://rubygems.org/api/v1/gems/debug.json — “Debugging functionality for Ruby. This is completely rewritten debug.rb which was contained by the ancient Ruby versions.”
- gem delegate — https://rubygems.org/api/v1/gems/delegate.json — “Provides three abilities to delegate method calls to an object.”
- gem did_you_mean — https://rubygems.org/api/v1/gems/did_you_mean.json — “The gem that has been saving people from typos since 2014.”
- gem digest — https://rubygems.org/api/v1/gems/digest.json — “Provides a framework for message digest libraries.”
- gem drb — https://rubygems.org/api/v1/gems/drb.json — “Distributed object system for Ruby”
- gem english — https://rubygems.org/api/v1/gems/english.json — “Require 'English.rb' to reference global variables with less cryptic names.”
- gem erb — https://rubygems.org/api/v1/gems/erb.json — “An easy to use but powerful templating system for Ruby.”
- gem error_highlight — https://rubygems.org/api/v1/gems/error_highlight.json — “The gem enhances Exception#message by adding a short explanation where the exception is raised”
- gem etc — https://rubygems.org/api/v1/gems/etc.json — “Provides access to information typically stored in UNIX /etc directory.”
- gem fast_gettext — https://rubygems.org/api/v1/gems/fast_gettext.json — “A simple, fast, memory-efficient and threadsafe implementation of GetText”
- gem fcntl — https://rubygems.org/api/v1/gems/fcntl.json — “Loads constants defined in the OS fcntl.h C header file”
- gem fiddle — https://rubygems.org/api/v1/gems/fiddle.json — “A libffi wrapper for Ruby.”
- gem fileutils — https://rubygems.org/api/v1/gems/fileutils.json — “Several file utility methods for copying, moving, removing, etc.”
- gem find — https://rubygems.org/api/v1/gems/find.json — “This module supports top-down traversal of a set of file paths.”
- gem forwardable — https://rubygems.org/api/v1/gems/forwardable.json — “Provides delegation of specified methods to a designated object.”
- gem gem2rpm — https://rubygems.org/api/v1/gems/gem2rpm.json — “Generate source rpms and rpm spec files from a Ruby Gem. The spec file tries to follow the gem as”
- gem getoptlong — https://rubygems.org/api/v1/gems/getoptlong.json — “GetoptLong for Ruby”
- gem io-console — https://rubygems.org/api/v1/gems/io-console.json — “add console capabilities to IO instances.”
- gem io-nonblock — https://rubygems.org/api/v1/gems/io-nonblock.json — “Enables non-blocking mode with IO class”
- gem io-wait — https://rubygems.org/api/v1/gems/io-wait.json — “Deprecated: All functionality ships with Ruby 3.2 and higher.”
- gem ipaddr — https://rubygems.org/api/v1/gems/ipaddr.json — “IPAddr provides a set of methods to manipulate an IP address. Both IPv4 and IPv6 are supported.”
- gem irb — https://rubygems.org/api/v1/gems/irb.json — “Interactive Ruby command-line tool for REPL (Read Eval Print Loop).”
- gem json — https://rubygems.org/api/v1/gems/json.json — “This is a JSON implementation as a Ruby extension in C.”
- gem logger — https://rubygems.org/api/v1/gems/logger.json — “Provides a simple logging utility for outputting messages.”
- gem matrix — https://rubygems.org/api/v1/gems/matrix.json — “An implementation of Matrix and Vector classes.”
- gem minitest — https://rubygems.org/api/v1/gems/minitest.json — “minitest provides a complete suite of testing facilities supporting TDD, BDD, and benchmarking.”
- gem mutex_m — https://rubygems.org/api/v1/gems/mutex_m.json — “Mixin to extend objects to be handled like a Mutex.”
- gem net-ftp — https://rubygems.org/api/v1/gems/net-ftp.json — “Support for the File Transfer Protocol.”
- gem net-http — https://rubygems.org/api/v1/gems/net-http.json — “HTTP client api for Ruby.”
- gem net-imap — https://rubygems.org/api/v1/gems/net-imap.json — “Ruby client api for Internet Message Access Protocol”
- gem net-pop — https://rubygems.org/api/v1/gems/net-pop.json — “Ruby client library for POP3.”
- gem net-protocol — https://rubygems.org/api/v1/gems/net-protocol.json — “The abstract interface for net-* client.”
- gem net-smtp — https://rubygems.org/api/v1/gems/net-smtp.json — “Simple Mail Transfer Protocol client library for Ruby.”
- gem nkf — https://rubygems.org/api/v1/gems/nkf.json — “Ruby extension for Network Kanji Filter”
- gem nokogiri — https://rubygems.org/api/v1/gems/nokogiri.json — “Nokogiri (鋸) makes it easy and painless to work with XML and HTML from Ruby. It provides a sensible, easy-to-understand”
- gem observer — https://rubygems.org/api/v1/gems/observer.json — “Implementation of the Observer object-oriented design pattern.”
- gem open-uri — https://rubygems.org/api/v1/gems/open-uri.json — “An easy-to-use wrapper for Net::HTTP, Net::HTTPS and Net::FTP.”
- gem open3 — https://rubygems.org/api/v1/gems/open3.json — “Popen, but with stderr, too”
- gem openssl — https://rubygems.org/api/v1/gems/openssl.json — “OpenSSL for Ruby provides access to SSL/TLS and general-purpose cryptography based on the OpenSSL library.”
- gem optparse — https://rubygems.org/api/v1/gems/optparse.json — “OptionParser is a class for command-line option analysis. It is much more advanced, yet also easier to use, than GetoptLong,”
- gem ostruct — https://rubygems.org/api/v1/gems/ostruct.json — “Class to build custom data structures, similar to a Hash.”
- gem power_assert — https://rubygems.org/api/v1/gems/power_assert.json — “Power Assert shows each value of variables and method calls in the expression. It is useful for testing, providing which”
- gem pp — https://rubygems.org/api/v1/gems/pp.json — “Provides a PrettyPrinter for Ruby objects”
- gem prettyprint — https://rubygems.org/api/v1/gems/prettyprint.json — “Implements a pretty printing algorithm for readable structure.”
- gem prime — https://rubygems.org/api/v1/gems/prime.json — “Prime numbers and factorization library.”
- gem prism — https://rubygems.org/api/v1/gems/prism.json — “Prism Ruby parser”
- gem pstore — https://rubygems.org/api/v1/gems/pstore.json — “Transactional File Storage for Ruby Objects”
- gem psych — https://rubygems.org/api/v1/gems/psych.json — “Psych is a YAML parser and emitter. Psych leverages libyaml[https://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting capabilities. In addition to”
- gem racc — https://rubygems.org/api/v1/gems/racc.json — “Racc is an LALR(1) parser generator. It is written in Ruby itself, and generates Ruby program. NOTE: Ruby 1.8.x comes”
- gem rake — https://rubygems.org/api/v1/gems/rake.json — “Rake is a Make-like program implemented in Ruby. Tasks and dependencies are specified in standard Ruby syntax. Rake has the”
- gem rbs — https://github.com/ruby/rbs/blob/master/docs/architecture.md — “The parser is implemented in C extension.”
- gem rdoc — https://rubygems.org/api/v1/gems/rdoc.json — “RDoc produces HTML and command-line documentation for Ruby projects. RDoc includes the +rdoc+ and +ri+ tools for generating and displaying”
- gem readline — https://rubygems.org/api/v1/gems/readline.json — “This is just a loader for "readline". If Ruby has the "readline-ext" gem that is a native extension, this gem”
- gem reline — https://rubygems.org/api/v1/gems/reline.json — “Alternative GNU Readline or Editline implementation by pure Ruby.”
- gem repl_type_completor — https://rubygems.org/api/v1/gems/repl_type_completor.json — “Type based completion for REPL.”
- gem resolv — https://rubygems.org/api/v1/gems/resolv.json — “Thread-aware DNS resolver library in Ruby.”
- gem resolv-replace — https://rubygems.org/api/v1/gems/resolv-replace.json — “Replace Socket DNS with Resolv.”
- gem rexml — https://rubygems.org/api/v1/gems/rexml.json — “An XML toolkit for Ruby”
- gem rinda — https://rubygems.org/api/v1/gems/rinda.json — “The Linda distributed computing paradigm in Ruby.”
- gem rss — https://rubygems.org/api/v1/gems/rss.json — “Family of libraries that support various formats of XML "feeds".”
- gem ruby-augeas — https://rubygems.org/api/v1/gems/ruby-augeas.json — “Provides bindings for augeas.”
- gem ruby-dbus — https://rubygems.org/api/v1/gems/ruby-dbus.json — “Pure Ruby module for interaction with D-Bus IPC system”
- gem ruby2_keywords — https://rubygems.org/api/v1/gems/ruby2_keywords.json — “Shim library for Module#ruby2_keywords”
- gem securerandom — https://rubygems.org/api/v1/gems/securerandom.json — “Interface for secure random number generator.”
- gem shellwords — https://rubygems.org/api/v1/gems/shellwords.json — “Manipulates strings with word parsing rules of UNIX Bourne shell.”
- gem simpleidn — https://rubygems.org/api/v1/gems/simpleidn.json — “This gem allows easy conversion from punycode ACE strings to unicode UTF-8 strings and vice-versa.”
- gem singleton — https://rubygems.org/api/v1/gems/singleton.json — “The Singleton module implements the Singleton pattern.”
- gem stringio — https://rubygems.org/api/v1/gems/stringio.json — “Pseudo `IO` class from/to `String`.”
- gem strscan — https://rubygems.org/api/v1/gems/strscan.json — “Provides lexical scanning operations on a String.”
- gem syntax_suggest — https://rubygems.org/api/v1/gems/syntax_suggest.json — “When you get an "unexpected end" in your syntax this gem helps you find it”
- gem syslog — https://rubygems.org/api/v1/gems/syslog.json — “Ruby interface for the POSIX system logging facility.”
- gem tempfile — https://rubygems.org/api/v1/gems/tempfile.json — “A utility class for managing temporary files.”
- gem test-unit — https://rubygems.org/api/v1/gems/test-unit.json — “test-unit (Test::Unit) is unit testing framework for Ruby, based on xUnit principles.”
- gem time — https://rubygems.org/api/v1/gems/time.json — “Extends the Time class with methods for parsing and conversion.”
- gem timeout — https://rubygems.org/api/v1/gems/timeout.json — “Auto-terminate potentially long-running operations in Ruby.”
- gem tmpdir — https://rubygems.org/api/v1/gems/tmpdir.json — “Extends the Dir class to manage the OS temporary file path.”
- gem tsort — https://rubygems.org/api/v1/gems/tsort.json — “Topological sorting”
- gem typeprof — https://rubygems.org/api/v1/gems/typeprof.json — “TypeProf performs a type analysis of non-annotated Ruby code. It abstractly executes input Ruby code in a level of types”
- gem un — https://rubygems.org/api/v1/gems/un.json — “Utilities to replace common UNIX commands”
- gem uri — https://rubygems.org/api/v1/gems/uri.json — “URI is a module providing classes to handle Uniform Resource Identifiers”
- gem weakref — https://rubygems.org/api/v1/gems/weakref.json — “Allows a referenced object to be garbage-collected.”
- gem yaml — https://rubygems.org/api/v1/gems/yaml.json — “YAML Ain't Markup Language”
- gem zlib — https://rubygems.org/api/v1/gems/zlib.json — “Ruby interface for the zlib compression/decompression library”
- pip PyGObject — https://pypi.org/pypi/PyGObject/json — “Python bindings for GObject Introspection”
- pip PySocks — https://pypi.org/pypi/PySocks/json — “A Python SOCKS client module.”
- pip bcrypt — https://pypi.org/pypi/bcrypt/json — “Modern password hashing for your software and your servers”
- pip brotli — https://pypi.org/pypi/brotli/json — “Python bindings for the Brotli compression library”
- pip certifi — https://pypi.org/project/certifi/ — “you can use the built-in function:”
- pip cffi — https://pypi.org/pypi/cffi/json — “Foreign Function Interface for Python calling C code.”
- pip charset-normalizer — https://pypi.org/pypi/charset-normalizer/json — “The Real First Universal Charset Detector. Open, modern and actively maintained alternative to Chardet.”
- pip cmdln — https://pypi.org/pypi/cmdln/json — “An improved cmd.py for writing multi-command scripts and shells.”
- pip configobj — https://pypi.org/pypi/configobj/json — “Config file reading, writing and validation.”
- pip createrepo_c — https://pypi.org/pypi/createrepo_c/json — “C implementation of createrepo”
- pip crit — https://criu.org/GSoC_completed_projects — “Currently CRIT is implemented in Python”
- pip cryptography — https://pypi.org/pypi/cryptography/json — “cryptography is a package which provides cryptographic recipes and primitives to Python developers.”
- pip cupshelpers — https://github.com/OpenPrinting/system-config-printer/blob/master/Makefile.am — “cupshelpers/cupshelpers.py”
- pip decorator — https://pypi.org/pypi/decorator/json — “Decorators for Humans”
- pip h2 — https://pypi.org/pypi/h2/json — “Pure-Python HTTP/2 protocol implementation”
- pip hpack — https://pypi.org/pypi/hpack/json — “Pure-Python HPACK header encoding”
- pip hyperframe — https://pypi.org/pypi/hyperframe/json — “Pure-Python HTTP/2 framing”
- pip idna — https://pypi.org/pypi/idna/json — “Internationalized Domain Names in Applications (IDNA)”
- pip nftables — https://wiki.iptables.org/wiki-nftables/index.php/Scripting — “The same functionality provided by the nft command-line utility is available from within Python programs”
- pip pip — https://pypi.org/pypi/pip/json — “The PyPA recommended tool for installing Python packages.”
- pip protobuf — https://protobuf.dev/reference/python/python-generated/ — “The Python Protobuf implementation is a little different from C++ and Java.”
- pip psutil — https://pypi.org/pypi/psutil/json — “Cross-platform lib for process and system monitoring.”
- pip psutils — https://pypi.org/pypi/psutils/json — “Manipulate PDF and PostScript documents”
- pip puremagic — https://pypi.org/pypi/puremagic/json — “Pure python implementation of magic file detection”
- pip pyOpenSSL — https://pypi.org/pypi/pyOpenSSL/json — “Python wrapper module around the OpenSSL library”
- pip pycairo — https://pypi.org/pypi/pycairo/json — “Python interface for cairo”
- pip pycparser — https://pypi.org/pypi/pycparser/json — “C parser in Python”
- pip pycriu — https://packages.debian.org/sid/python3-pycriu — “This package provides the criu Python bindings”
- pip pycups — https://pypi.org/pypi/pycups/json — “Python bindings for libcups”
- pip pycurl — https://pypi.org/pypi/pycurl/json — “PycURL -- A Python Interface To The cURL library”
- pip pygdbmi — https://pypi.org/pypi/pygdbmi/json — “Parse gdb machine interface output with Python”
- pip pyinotify — https://pypi.org/pypi/pyinotify/json — “Linux filesystem events monitoring”
- pip pypdf — https://pypi.org/pypi/pypdf/json — “A pure-python PDF library capable of splitting, merging, cropping, and transforming PDF files”
- pip pysmbc — https://pypi.org/pypi/pysmbc/json — “Python bindings for libsmbclient”
- pip python-linux-procfs — https://packagehub.suse.com/packages/python-linux-procfs/ — “Abstractions to extract information from the Linux kernel /proc files.”
- pip pyudev — https://pypi.org/pypi/pyudev/json — “A libudev binding”
- pip requests — https://pypi.org/pypi/requests/json — “Python HTTP for Humans.”
- pip rpm — https://rpm.org/docs/4.20.x/api/ — “This documents the librpm API as available to rpm itself”
- pip selinux — https://github.com/SELinuxProject/selinux/wiki/Userspace-Packages — “libselinux is the runtime SELinux library”
- pip sepolicy — https://github.com/SELinuxProject/selinux/wiki/Tools — “front-end for inspecting or generating policy”
- pip setools — https://github.com/SELinuxProject/setools — “libraries designed to facilitate SELinux policy analysis.”
- pip setuptools — https://pypi.org/pypi/setuptools/json — “Most extensible Python build backend with support for C/C++ extension modules”
- pip six — https://pypi.org/pypi/six/json — “Python 2 and 3 compatibility utilities”
- pip urllib3 — https://pypi.org/pypi/urllib3/json — “HTTP library with thread-safe connection pooling, file post, and more.”
- pip zstandard — https://pypi.org/pypi/zstandard/json — “Zstandard bindings for Python”

## Eight Flatpak rows, individually assessed

https://docs.flatpak.org/en/latest/extension.html: “stable mesa fallback build”; “support for patented codecs”; “Extension point for Gtk3 themes.” These document the two GL rows, the codecs-extra successor, and the shared theme respectively. Graphics and codec libraries are executed with application rights. The theme is provided by the runtime to multiple applications, so S2.2-7 does not exempt it.

https://docs.flatpak.org/en/latest/basic-concepts.html: “Runtimes provide the basic dependencies used by applications.” The platform is executable runtime support, required by S2.2-2 and S2.2-10.

https://apps.gnome.org/Calculator/: “Calculator is an application that solves mathematical equations.” Calculator receives MUST under S2.2-9 and S2.2-12.

https://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html: “Separate out locale files and translations to an extension runtime.” Both Locale rows receive HOLE: translated strings can be read as content whose removal leaves operations intact, or as the ability to produce a localized interface. S2.2-2 and S2.2-4 do not specify the boundary; S2.2-7 additionally comes close for calculator-only localization. This is a classification boundary, not a choice of state migration design.

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

## Verification

The append-resumable script language-write.py verifies the assigned input/output ID sets and counts, uniqueness, allowed decisions, and word limits. Result after review: 378 rows; MUST 375, HOLE 3, NOT 0, UNKNOWN 0, MIXED 0.

## Review amendment

The shared GTK theme row tumbleweed-6aa862424bccb9f5ca9b17cc was initially MUST because the theme affects multiple applications, excluding S2.2-7. That inference did not resolve S2.2-4: documentation establishes shared styling but does not establish executable theme code. The same distinction between lost presentation capability and unavailable presentation content that affects translations also applies here. Decision amended to HOLE, citing S2.2-2, S2.2-4, and S2.2-7. This amendment supersedes the initial theme assessment above.

Version limitation: package-registry summaries and some upstream documentation describe the currently published project, not necessarily the exact installed version. They establish the stable functional role of the identified distribution, rather than exact installed contents or version-specific behavior. Recorded versions and related package identities were checked for obvious project-name collisions; replacements are documented above. No exact-version source audit is claimed.


# Final c1 integration decisions

This section and the final TSV supersede inconsistent preliminary subset decisions above. The subset files remain intact as the append-progress record. `part-tumbleweed.reconcile.py` creates `part-tumbleweed.rpm-final.tsv`; `part-tumbleweed.reconciliation.json` records every specifically reviewed package and both paired IDs. Root and user RPM rows have identical package membership strings, verified for all 2,390 pairs. Consequently the same function and final sentence interpretation apply to each pair; they are separate rows, not different installations inferred from the context prefix.

The first RPM subset's filelist-grounded rules are applied to both copies, with the explicit per-package resolutions in the reconciliation script. This is one c1 classification split for work, not consultation of c2, adjudication, prior nights or earlier classifications.

## Final boundaries and corrections

- Executable library/code payload remains MUST under S2.2-9/S2.2-10; S2.2-13 resolves settings-versus-code classification. A package description alone did not establish an executable subpackage. `yast2-theme-breeze` contains an actual Bash helper creating symlinks. `plasma6-sddm-theme-openSUSE` includes a shell script independently of questions about QML confinement. The hicolor package contains a shell-producing RPM macro. These are MUST, not ambiguous merely because their packages also contain theme assets.
- Pure artwork, backgrounds, cursors, bitmaps and sound recordings are NOT under S2.2-4. Losing a particular image or recording is loss of that content. The description of an image as a theme does not establish executable behavior. `libkmahjongg` contains SVG artwork, descriptive theme files and category labels, so its preliminary UNKNOWN was unsupported and is corrected to NOT.
- Translated interface catalogs remain HOLE under S2.2-2/S2.2-4: their removal can be described as loss of translated content or loss of localized-output capability. The text does not distinguish these readings. This final rule applies to 29 RPM packages in both inventories and is consistent with the Flatpak Locale rows. It does not apply indiscriminately to all documentation or all data. `iso-codes` additionally contains structured reference lists and is individually retained as HOLE under the operational-data boundary.
- Runtime GObject typelibs are MUST under S2.2-1/S2.2-2: they provide invocation information necessary to call library interfaces through language bindings. They are not classified as executable machine code. Their removal loses callable interfaces, not merely an unavailable descriptive document. The earlier generic metadata HOLE was too broad for this established use.
- Device configuration, shared toolkit schemas/keybindings and real filesystem layout are MUST where the documented effects govern devices, multiple applications or pathname capabilities. A file read by one manager is not thereby a setting in force only inside that manager. The systemd defaults/presets and D-Bus restart restrictions therefore follow the same MUST reasoning as the inventoried service definitions. No S2.2-15 account/firewall requirement is incorrectly attributed to arbitrary systemd settings.
- The NetworkManager connectivity configuration is MUST: primary documentation explicitly connects probes with changed default-route metrics and other applications. The chrony pool configuration is MUST because it governs the system clock used by other processes. The RPM SELinux plugin-selection package is MUST because its setting selects SELinux labeling of installed files and scriptlets. The latter package contains a macro and a manual, not the plugin implementation; its final reason makes that distinction.
- No-payload dependency packages remain HOLE where package-manager metadata may be read as descriptive records or as controlling future program selection. `permissions` is such a dependency package, not the separately packaged policy implementation. This is a recording-boundary question about metadata, not a claim that Section 2.5 design choices themselves are holes.
- Shared style configuration, integration descriptors, signature trust values and certain reference tables retain individually stated HOLE decisions where the text does not resolve content/capability or single-program scope. The presence of values alone does not establish the S2.2-7 exemption. The exact selected cases are enumerated in the script and audit file, not inferred for every configuration file.
- `gnome-tour-data` remains UNKNOWN: the inventory and public package metadata identify a resource bundle but do not establish its packaged contents or behavior sufficiently. `libreoffice-filters-optional` remains UNKNOWN: XSLT transformations are established, but evidence does not establish whether this execution confines the code or grants its processor's full rights. By contrast, `docbook-xsl-stylesheets` contains independently identifiable executable Java support, so it is MUST. Both UNKNOWN package decisions apply to their two inventory copies.

Public filelists match the inventoried package versions except `openSUSE-build-key` (repository 1.0-68.1 versus inventory 1.0-69.1); that package is classified by its documented stable signing-key role, not claimed exact byte identity. Imported `gpg-pubkey` records are documented by RPM's own key-management manual. Language ecosystem documentation likewise establishes stable program roles, not exact current-versus-installed byte identity.

## Additional primary evidence used in integration

- https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html, connectivity section: “default-route of devices without global connectivity get a penalty of +20000 to the route-metric”. The adjacent documentation establishes the D-Bus consumers.
- https://rpm.org/docs/6.0.x/man/rpm-plugin-selinux.8: “The plugin sets SELinux contexts for installed files and executed scriptlets.” The filelist establishes that this package configures that plugin.
- https://gi.readthedocs.io/en/latest/architecture.html: “Binary version of the invocation info and required .typelib files”. The architecture connects typelibs through libgirepository and libffi to language bindings.
- https://raw.githubusercontent.com/yast/yast-theme/master/icons/breeze/make-symlinks.sh: “#! /bin/bash”; it loops over supplied mapping files and invokes `ln -sf`.
- https://download.opensuse.org/tumbleweed/repo/oss/noarch/hicolor-icon-theme-0.18-1.5.noarch.rpm: the inspected `%icon_theme_cache_create_ghost()` macro invokes `mkdir` and `touch` in the build root. This is executable shell expansion, not just passive image data.

## Final translated-interface rule: ten manual checks

The following exact IDs were checked against actual `.mo`/`.qm` translation payloads and the final content-versus-localized-output reasoning. License/documentation files do not alter the function of these packages.

- tumbleweed-69d8cbcefe0629f32ed6c8e8 — desktop-translations: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-cef9aa36975108f20d6841ff — kImageAnnotator-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-527aeb630ad9f2636cdd559f — libksane-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-6a567e1b020369e9b4a15b5e — libqt5-qttranslations: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-debbb43da15a0050abbd7e0a — libstorage-ng-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-af2b623383a61a33374a59f1 — qt6-translations: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-14b4feff4d3b3c916032ed56 — snapper-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-f73eeb400766d5a937dddc88 — kf6-kuserfeedback-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-e4b043dbfeb54717e5f66dcc — kidentitymanagement-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.
- tumbleweed-dedd102fa4c17b964a081ec2 — libkgapi6-lang: translated interface catalog; HOLE under S2.2-2/S2.2-4.

## Individual integration register

Each entry below was specifically considered using the two current subset records and the corresponding package payload. This register records final reasons, not a vote between subsets.

- branding-openSUSE (tumbleweed-9c27fd6cc1f6e95eaeda2b15, tumbleweed-afd24c8aacb62bb4d83a4713): MUST. The brand file triggers package selection; removal changes subsequent system installation behavior.
- breeze6-cursors (tumbleweed-51d8e1057ebd0be44f76c82d, tumbleweed-604e994fbd779b550d9377de): NOT. Payload contains presentation assets; removal makes only that artwork unavailable.
- dbus-broker-block-restart (tumbleweed-e8596c1f2e7cf3225d78566f, tumbleweed-c7ac4a140066a37feed0450b): MUST. The service drop-ins constrain restarting separate message-bus processes; their effects are not confined inside one program.
- desktop-translations (tumbleweed-69d8cbcefe0629f32ed6c8e8, tumbleweed-d4ff03222fe3efc98f95872f): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- distribution-logos-openSUSE-Tumbleweed (tumbleweed-207892425f45c7f1ff152fb5, tumbleweed-88c6d153fb922b34384bb62c): NOT. Payload contains presentation assets; removal makes only that artwork unavailable.
- gnome-tour-data (tumbleweed-4a4dfe61ec107005d2e1e593, tumbleweed-c3769a3b91a480a1eb8680b6): UNKNOWN. Package description does not establish the subpackage contents or removal consequences; raw ownership inventory is empty.
- gtk3-data (tumbleweed-cfee098921beb2a44ecc53d7, tumbleweed-753ec04c3399c7c24f6764f9): MUST. Toolkit schemas and keybindings affect multiple applications; removal changes shared interface behavior.
- gtk3-schema (tumbleweed-9168ed9921348431a160dfbd, tumbleweed-94733f055f9f9e259def1555): MUST. Toolkit schemas and keybindings affect multiple applications; removal changes shared interface behavior.
- gtk4-schema (tumbleweed-94aabfb89fb2b64b1f06bc7c, tumbleweed-1c13d4d6011ae45ca83363fb): MUST. Toolkit schemas and keybindings affect multiple applications; removal changes shared interface behavior.
- iso-codes (tumbleweed-e3ffdbeeab220be3a54cafba, tumbleweed-fb37a4a8d9cbdde019568fee): HOLE. Removal loses supplied text, artwork, or reference data; the text does not distinguish unavailable content from lost rendering, language, or recognition capability.
- javapackages-filesystem (tumbleweed-805fce69915400aba79d77c2, tumbleweed-7a02732097fb92ad188d98e9): MUST. Removing required directories prevents their software and stored objects from being accessed.
- kImageAnnotator-lang (tumbleweed-cef9aa36975108f20d6841ff, tumbleweed-803cd9885d5ac3af08d2e0a6): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- kdegames-carddecks-default (tumbleweed-f30a186bd1cff9957e0f7b5c, tumbleweed-10a7e6c22aeeee7b7f43e322): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- kf6-breeze-icons (tumbleweed-39af3faa265fdda45dd7c62f, tumbleweed-9b979d05f7cbf004bcb901d2): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- kf6-kconfigwidgets (tumbleweed-555907102e5e611d02ba43fa, tumbleweed-6a50fe2fbf58a513826d1501): HOLE. Removal loses language-selection descriptions or the ability to present those choices; the text does not distinguish this content from interface capability.
- kf6-purpose-services (tumbleweed-85b5251c5f01299b8ed5f228, tumbleweed-a7932bee81af8eff1a35652f): HOLE. Values configure libraries or application integration; the text does not determine whether effects remain inside one program.
- kmail-application-icons (tumbleweed-8deb6bea53de73438bc0b1e6, tumbleweed-57a1dd2591b7ee64af0fc2f9): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- kscreenlocker6-imports (tumbleweed-7d8d618d7aee68e4f0b88913, tumbleweed-142611cc5e946fee6c2cbd1e): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- ksysguardsystemstats6-data (tumbleweed-eee438d72ab81b664173bca6, tumbleweed-eff364d4e6ac3e0fa97b66b0): NOT. The package supplies an interface-description XML document, not the service implementation or its activation policy.
- libkleo (tumbleweed-f6c9b74cc941ca216b2b4f00, tumbleweed-6133fb619cc177cebd450517): HOLE. Values configure libraries or application integration; the text does not determine whether effects remain inside one program.
- libkmahjongg (tumbleweed-3ce8f43f3335b61c4fbd7b99, tumbleweed-139df17d42bdf459183ce14d): NOT. Only the supplied artwork and descriptions become unavailable; filelists establish no game implementation in this package.
- libksane-icons (tumbleweed-27ce24f45c743a72178fdae6, tumbleweed-20628fa1fe408105dd49c66b): NOT. Payload contains presentation assets; removal makes only that artwork unavailable.
- libksane-lang (tumbleweed-527aeb630ad9f2636cdd559f, tumbleweed-f8aef4a27312ebc7f111d4cc): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libksieve (tumbleweed-96511044c97fd0e083b030ca, tumbleweed-f930414351a4a1b2409054de): HOLE. Payload has data and descriptions rather than advertised code; text does not resolve descriptive content versus effects on application functionality.
- libnl-config (tumbleweed-44ac2878cd1bcaaea18757cd, tumbleweed-57e50cddde9ed86fbce3d1d5): HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- libpaper (tumbleweed-8fa99d7de9ae7eeed6b04c4f, tumbleweed-a9f781f6fa923e586a78340a): HOLE. Values configure libraries or application integration; the text does not determine whether effects remain inside one program.
- libplasma6-desktoptheme (tumbleweed-694485646109ee5946fed689, tumbleweed-27de7a07eb2d915e8d077283): HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- libqt5-qttranslations (tumbleweed-6a567e1b020369e9b4a15b5e, tumbleweed-948045f52341e1e72f76b635): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libsemanage-conf (tumbleweed-fcc948a559fb78283d68a052, tumbleweed-ad652a1173c64b17a408185a): HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- libstorage-ng-lang (tumbleweed-debbb43da15a0050abbd7e0a, tumbleweed-0ab2bb3fafb9fac820306c2c): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libtirpc-netconfig (tumbleweed-acf8b249ca546c3d3db5ca4d, tumbleweed-ef50d89379c7e871dae8bd93): MUST. Documentation identifies shared defaults across applications; removal changes behavior beyond one program.
- ocean-sound-theme6 (tumbleweed-d2388c321ef8b22307dcf7bd, tumbleweed-9142d0bdb665215fcceafc81): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- qt6-translations (tumbleweed-af2b623383a61a33374a59f1, tumbleweed-abf58d89cb28c95c39c19058): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- snapper-lang (tumbleweed-14b4feff4d3b3c916032ed56, tumbleweed-21ca4798e791f08c9baab6c4): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- wallpaper-branding-openSUSE (tumbleweed-bf9029a4ec645e21be37f294, tumbleweed-e611f296dca7b2cfc334a802): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- xbitmaps (tumbleweed-9fe77d5b5a8d7bb3aa41ea6a, tumbleweed-62d402c2551a56cb162b49d4): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- metatheme-breeze6-common (tumbleweed-ff8414e8fa9b41b847ba8f03, tumbleweed-b9c111aab7a79f2e0d7c33b6): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- gtk3-metatheme-breeze6 (tumbleweed-8e84d13ea1b940f02e6994e2, tumbleweed-132eadc911f7cc2633da5ffd): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- distribution-logos-openSUSE-icons (tumbleweed-6cc4dd2ccf77fb4f5b6b01f6, tumbleweed-09328326db8cc83a6b20de6f): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- kf6-kuserfeedback-lang (tumbleweed-f73eeb400766d5a937dddc88, tumbleweed-1b4b23a3596c6c72480401e8): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- kidentitymanagement-lang (tumbleweed-e4b043dbfeb54717e5f66dcc, tumbleweed-416cf73a88cad1ab9ce270fd): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libkgapi6-lang (tumbleweed-dedd102fa4c17b964a081ec2, tumbleweed-7a897347e8001d0658ee6828): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- filesystem (tumbleweed-d3f932cd4413f85b7a0dd24a, tumbleweed-cae0778ca79df14155e00d1c): MUST. Removing required directories prevents their software and stored objects from being accessed.
- gtk4-metatheme-breeze6 (tumbleweed-c99ceaa989531e038628e42e, tumbleweed-819b570cdea5ea55df85afe1): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- augeas-lenses (tumbleweed-eeeceb9dea1a900d85a2b621, tumbleweed-58bfaed75b767465bff8e84a): MUST. Documented executable functions run as programs or with the invoking program rights.
- alsa-ucm-conf (tumbleweed-10abe303067f45019dadd870, tumbleweed-f0da0e6ac4776e60abf294fc): MUST. Settings govern multiple consumers or devices; removal changes shared behavior beyond one program.
- typelib-1_0-GLib-2_0 (tumbleweed-7a6ad33f358961bfad1a3cba, tumbleweed-b6506c20dbd511bc9d1cea43): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- girepository-1_0 (tumbleweed-6240417d927371402a3afcc8, tumbleweed-b8844433a232609731e25abb): MUST. Language bindings require these interface descriptions to invoke corresponding native operations.
- typelib-1_0-GObject-2_0 (tumbleweed-900dbc71741501e821d1c709, tumbleweed-54f349aab25a45dcdffb851f): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-GModule-2_0 (tumbleweed-b7d547e3a754a9f5372ffdcf, tumbleweed-6f6fb0bebafbad99f7e14193): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-GLibUnix-2_0 (tumbleweed-50bd7f4cb772b73088964c52, tumbleweed-1071b28ebfc759ac33f9c4d0): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-Atk-1_0 (tumbleweed-272491cb93106d5053d88d39, tumbleweed-4427d7290d8883e9a3b55338): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-HarfBuzz-0_0 (tumbleweed-c94a1b3acbd79a0bc4cb5cf6, tumbleweed-76fd873cf562e0c5fb4f8e63): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- Mesa (tumbleweed-855ad8c48fdbd681d9a7fbe1, tumbleweed-67486972373cb0f28ea8c779): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- rpm-plugin-selinux (tumbleweed-696aec51c689c2a848ec2d21, tumbleweed-cdd698ee2b182cf9d748a45a): MUST. The configuration selects labeling of installed files and scriptlets; effects extend beyond RPM. The package itself does not contain plugin code.
- systemd-presets-common-SUSE (tumbleweed-9d2a17c65c7d0f613f430846, tumbleweed-81ef65c1ae2937fc90855b48): MUST. These values govern other services and processes; being read by one manager does not confine their effects inside that manager.
- systemd-default-settings-branding-openSUSE (tumbleweed-1817ca562b1a0c7ae7647a05, tumbleweed-44476dfef6681a4c07b026b9): MUST. These values govern other services and processes; being read by one manager does not confine their effects inside that manager.
- systemd-default-settings (tumbleweed-fa43d1bdb79b1bf3c672dda1, tumbleweed-af6349a44190ec884e69ba95): MUST. These values govern other services and processes; being read by one manager does not confine their effects inside that manager.
- sound-theme-freedesktop (tumbleweed-9d4553a31373cb92d9b4fd44, tumbleweed-4efba37278070710fee7ab15): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- libssh-config (tumbleweed-6131ae58ce030a383e82f2ec, tumbleweed-95709d632bb78c758db4db62): MUST. Documentation identifies shared defaults across applications; removal changes behavior beyond one program.
- hicolor-icon-theme-branding-openSUSE (tumbleweed-aa92a36c91f7c095a4cf0ae4, tumbleweed-df9d675a32e5d6a4a33bf4e7): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- systemd-presets-branding-openSUSE (tumbleweed-e912f4efac89b08dc3a3427d, tumbleweed-7d45a3b81903e644cb0a1a7b): MUST. These values govern other services and processes; being read by one manager does not confine their effects inside that manager.
- kf6-kcoreaddons (tumbleweed-5af8f561b7ccb1aa8b1e29dd, tumbleweed-c9074ea775e56a8c729f3272): MUST. Shared MIME type definitions enable recognition and dispatch across applications; effect is not confined to one program.
- kcoreaddons (tumbleweed-8c4834567709f4438623ddcf, tumbleweed-7781b81cdd531b4c92391295): MUST. Shared MIME type definitions enable recognition and dispatch across applications; effect is not confined to one program.
- permissions (tumbleweed-550067369a58c28023491aa6, tumbleweed-255999ada4afb173b049b428): HOLE. Removing the selector leaves existing code intact but changes package selection; removal test gives no temporal scope.
- kf6-kcoreaddons-lang (tumbleweed-9ea2c6724e303abdda7e5731, tumbleweed-31dd829cd3d204a81012a82c): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- kcoreaddons-lang (tumbleweed-f26f0039c10ac5d7b9eb7fdf, tumbleweed-820d867dc9ae3382f0fd838e): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- typelib-1_0-Gio-2_0 (tumbleweed-80a3e282e5b79c37931671ce, tumbleweed-6455caea510a0c238f9e567c): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-Secret-1 (tumbleweed-e61016bde855c68fde4fd1ec, tumbleweed-7769497f7bd1158eda7070c5): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-Pango-1_0 (tumbleweed-70589ea9923cebb923c91aef, tumbleweed-a0a946f12961a3da9e476606): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-GdkPixbuf-2_0 (tumbleweed-e7b05fc9fc3e1f0f168dfc36, tumbleweed-a3c5a4f65d4d7e6f87d40f6c): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- info-lang (tumbleweed-5e98285ef0a1baddc79ba349, tumbleweed-679a99f1e70a45be2caaed6b): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- ruby (tumbleweed-daa4705f2a56ae9fbb16b74f, tumbleweed-5cb38da8ace4818e55967f7b): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- typelib-1_0-Atspi-2_0 (tumbleweed-8b89c29d76b3f11d585898d3, tumbleweed-4925f073c57698d6d637fe23): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- qtkeychain-qt6-lang (tumbleweed-de929cdb4a5022b567dda621, tumbleweed-19db1f7e7b5a88f9b88a6c6d): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- openssl (tumbleweed-cb451634ee2eefd18c46af93, tumbleweed-5fa45966f561960d04de8d01): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- libreoffice-icon-themes (tumbleweed-0c9194115520ab49a173b08c, tumbleweed-5b027a0fdc9ceabbb8c1ca25): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- typelib-1_0-NM-1_0 (tumbleweed-b68a2f51de24a967e062733a, tumbleweed-08f3a7852a66c471c7b6ffb4): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- tesseract-ocr-common (tumbleweed-21eff087b77fb58f160ba922, tumbleweed-0b930082aeaa5454d0b21f09): HOLE. Values configure libraries or application integration; the text does not determine whether effects remain inside one program.
- libKF5WidgetsAddons5-lang (tumbleweed-dee16399c907d247e629e279, tumbleweed-0b24665e209b2504c6019d1d): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libKF5JobWidgets5-lang (tumbleweed-e697bbb27d5ae72b19fdcbbb, tumbleweed-7af81b7bf15e2592c06e5fc3): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libKF6WidgetsAddons6-lang (tumbleweed-54fc6800943a1d0259693075, tumbleweed-cf30f1d92afa436f01aa7c98): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libKF6CalendarCore6-lang (tumbleweed-a615de32f8e90f1a4bedf010, tumbleweed-241ce940c8a944fef8b2501c): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libKF6JobWidgets6-lang (tumbleweed-821ff52735a7ca22cf3e5e1c, tumbleweed-ad54581a3d7f6326e1ab37cc): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- openSUSE-release (tumbleweed-db62e6171947e4d1346ccfc9, tumbleweed-2dba08873e49df3a281f2b7e): MUST. System identity and shared product defaults affect multiple installation and management tools.
- dbus-1 (tumbleweed-d8ec3330d38527ef431d50a9, tumbleweed-1c7bbc9651e3117e1332ebc5): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- typelib-1_0-Polkit-1_0 (tumbleweed-9bbc952e5e5869e5ca370b93, tumbleweed-3a0058d5f4427f79864bda9a): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- kf6-kauth-lang (tumbleweed-aaa4214a525be4a27976c652, tumbleweed-bebc5a5d46ac17921f5dc409): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libKF5Auth5-lang (tumbleweed-00f6faa7919bc639b275a5d8, tumbleweed-584b5b5fddfa41e96cea9139): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- usb_modeswitch-data (tumbleweed-a9c7da8fffa9c58809d73688, tumbleweed-03157754505268e3d9b2f8d2): MUST. Device matching rules invoke switching that makes hardware functions available beyond a single program.
- chrony-pool-openSUSE (tumbleweed-3fddd84530d7d0c31df015d9, tumbleweed-0440ecd1e9571cf8cde1be87): MUST. The configured sources govern the system clock used by other programs; this is not a setting confined inside chrony.
- openconnect-lang (tumbleweed-77a4e6c9383222b6ef2e9db7, tumbleweed-2cc7c28f6d2b0bd98f167419): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- NetworkManager-branding-openSUSE (tumbleweed-44c3b58f80b5d66089a33032, tumbleweed-e788c0407bc909d3a1ff0c64): MUST. Connectivity results change default-route metrics and are exposed to other applications; effects are not confined inside NetworkManager.
- firewalld-lang (tumbleweed-8da311a12c8890ea10a09a96, tumbleweed-bc4ed4a0d90fa39a64e28f57): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- PackageKit-branding-openSUSE (tumbleweed-3ac4eeb862bd4a20289cab82, tumbleweed-88de43bb31abf3d91ab8c376): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- metatheme-adwaita-common (tumbleweed-8950e190d14060a369183dc1, tumbleweed-1b6ff4c84ec0c06e7e9cac74): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- gtk3-metatheme-adwaita (tumbleweed-99e98e78a19742451d9457a5, tumbleweed-b323fb0780ed0774fe52a8c7): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- gsettings-desktop-schemas (tumbleweed-b8d83f1a0d2f476273247468, tumbleweed-092a5a5077a4aa62cdda0634): MUST. Documentation identifies shared defaults across applications; removal changes behavior beyond one program.
- typelib-1_0-PackageKitGlib-1_0 (tumbleweed-af4b49d0a7d52b0827ecb5b1, tumbleweed-1820210d0ef66cf6a5569071): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- xorg-x11-driver-video (tumbleweed-adca233073ff23d3f930a6c3, tumbleweed-7aecb91b81cec91f654dab24): MUST. System display configuration determines device availability across applications.
- yast2-theme-breeze (tumbleweed-baa068a8d5487cfed3bd790d, tumbleweed-49b7e58c9ade1153330e3892): MUST. The packaged Bash script invokes filesystem commands with interpreter rights; executable code remains code even when packaged with theme assets.
- flatpak-remote-flathub (tumbleweed-8bd4bea3220cc915155c4add, tumbleweed-a08bac3bb4eead7e0306e601): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- plymouth-lang (tumbleweed-e8b349efa81999eb3254bcfa, tumbleweed-afd0456e9faa11ada6e68c41): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- grub2 (tumbleweed-3a5424813d4b9d2c4bc646f1, tumbleweed-aac6aa8494b1f3e8c0028242): HOLE. Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.
- libKF6Baloo6-lang (tumbleweed-bc3fcb50c4e791af6510e215, tumbleweed-d8620423f05d02d99e676201): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- adwaita-icon-theme (tumbleweed-69ae64c8389433b269d88bb4, tumbleweed-eb9dcce62701fd2c47fea2d3): NOT. Removing artwork or sounds makes only that presentation content unavailable.
- gtk4-branding-openSUSE (tumbleweed-cd056181d467173557b158d3, tumbleweed-8fba25fb55f307fa4b8ffcd0): MUST. Documentation identifies shared defaults across applications; removal changes behavior beyond one program.
- konsole-part-lang (tumbleweed-3671752d547530c2e50b0f5f, tumbleweed-7a4775e0cf54ae314b82147d): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- gtk3-branding-openSUSE (tumbleweed-137a527bf6c4dbe43722554d, tumbleweed-7b897cdfd9256cc00b039c05): MUST. Documentation identifies shared defaults across applications; removal changes behavior beyond one program.
- typelib-1_0-Gtk-3_0 (tumbleweed-421dbfce1d277c686a4990e3, tumbleweed-140ebdef1b7fa0d54c32ee08): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- libreoffice-l10n-en (tumbleweed-4d04745d1b6f2c0164398cc0, tumbleweed-298d1d68f55f699e351f3be1): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- typelib-1_0-Handy-1_0 (tumbleweed-890e2ba0b9deddb0047aed77, tumbleweed-7e1b3535382849f2c8e6be07): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- typelib-1_0-Notify-0_7 (tumbleweed-ceecb247c3de6184bb017c56, tumbleweed-ddfdc5887173f2d794089459): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- phonon4qt5-lang (tumbleweed-2b526c5fb8b26b3bc16614bc, tumbleweed-a4edb4233a2dabfba9404808): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- phonon-vlc-lang (tumbleweed-152240b336a732ee8c788b72, tumbleweed-dd5147cdcfebccd535774556): HOLE. Removal loses translated-output capability or only translated content; the text does not distinguish those readings.
- libreoffice-filters-optional (tumbleweed-b66b6e6586d2543db7fadb72, tumbleweed-458bd2d25764f4b4b0aa2150): UNKNOWN. Transformation code is established, but evidence does not establish whether this processor confines it or grants the program’s full rights.
- plasma6-sddm-theme-openSUSE (tumbleweed-5e0021f998f99319a0ff105f, tumbleweed-c225ad126cda23f96aa4609e): MUST. Documented package payload includes executable code; removing it removes the corresponding callable operations.
- sddm-qt6-branding-openSUSE (tumbleweed-cb185dbc194f5f6a1895b5d3, tumbleweed-21c689370df3d76a7ab7285f): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- sddm-branding-openSUSE (tumbleweed-65d31620d369de83109c9fb8, tumbleweed-398f3c80654469a71f15a2fe): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- plasma6-branding-openSUSE (tumbleweed-e908396bce4f54f9bec66bfa, tumbleweed-06d3881473145922f997835c): HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- typelib-1_0-Fwupd-2_0 (tumbleweed-61f34ac9328e7bb4f5198926, tumbleweed-9e908df731cd0bf59ddd4226): MUST. Removing runtime introspection descriptions prevents language bindings from calling these library interfaces.
- libcontainers-default-policy (tumbleweed-8a0f96226b9f5119262f9093, tumbleweed-4c394b49c4edbaf1ac753966): MUST. Shared container policy affects which images multiple tools accept or locate; removal changes system capabilities.
- registries-conf-default (tumbleweed-a7cfefd659c7a59cf7dcc32f, tumbleweed-20e31b9f2ffa6df7884e3b3d): MUST. Shared container policy affects which images multiple tools accept or locate; removal changes system capabilities.
- hicolor-icon-theme (tumbleweed-dc123bdc513c409035c84aa5, tumbleweed-628aba51170df68037b752da): MUST. The package macro expands to shell mkdir and touch commands; executable installation code requires recording despite accompanying artwork.

## Final mechanical verification

2026-11-22 UTC: exact input/output ID multisets match; 6,779 rows, each ID once. Header, five allowed decision words, sentence scope, field word limits and absence of embedded tabs/newlines passed. All 2,390 paired RPM memberships have identical final decision fields. The required decision counts are written in `part-tumbleweed.done`. No experimental removal occurred.
