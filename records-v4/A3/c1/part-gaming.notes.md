# Gaming classification c1

This file consolidates the independently partitioned work within c1. The parts are disjoint input rows, not comparisons with another classification. The input contained 16,515 rows; every row was retained exactly once. Rules below are conditional on the supplied inventory facts, with manual checks for scripted rules. Detailed member decisions for grouped rows are in (not published: direct evidence at least 2 MB).

`part-gaming.merge.py` verifies exact header, identical input/output ID sets and counts, unique IDs, the fifteen permitted decisions, sentence IDs, field lengths, and absence of embedded delimiters. The final counts are in `part-gaming.done`. No hypothesis outcome is inferred by this classification.


---

# File-row decisions

Scope: the 14,053 individual file rows assigned to this part. Input class-like labels were used only to partition the work, never to decide whether a file is code. All these rows are regular files on persistent filesystems. No earlier classification was consulted. `raw:` paths in the output resolve from `A3/in/raw/`; `raw:../operator/` therefore points into the supplied inventory's operator evidence.

The reproducible append script is `part-gaming.code.py`. `part-gaming.code.audit.json` lists all rows assigned to each rule. A missing installation comparison is not a textual gap. A prefix signature, even when it covers a small complete current file, has no installation baseline by itself. Actual program installation logs establish events but do not establish that every later observed payload byte remains as received.

## Decisive text

- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-8: “Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-10: “Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.”
- S8.2-14: “A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

## Rules

C1 — Ten observed native-package aliases or hardlinks: INSTALLED-PACKAGE. Join through observed `/lib` and `/sbin` symlink targets, or through equal device and inode in (not published: over 20 MB), to an unchanged entry of (not published: over 20 MB). Four AppArmor files are aliases; six CUPS backend paths refer to the same filesystem objects as unchanged package members. S8.2-7 answers yes before code is considered; S8.2-16 supplies the package line. Native package installation reason affects its own line, not whether an unchanged member is covered by that package.

C2 — 130 package-control scripts without an installation comparison: UNKNOWN. Debian documents their package origin and execution purpose. They are not ordinary application records just because they are stored in the package database. The recorded shebangs confirm scripts, but cannot distinguish an unchanged packaged script (question one) from changed code (question two). Missing baseline is the deciding factual limitation, S8.2-6/7/9/16. Raw decoded maintainer scripts were inspected in metadata-read outputs; none supplies its original installation digest.

C3 — 210 Wine-prefix executables: UNKNOWN. The supplied `gaming_windows_program.stderr` records prefix creation and update; Wine's installation source lists builtin executable creation. The inventory lacks the comparison needed to establish which observed executables remain packaged originals, generated copies, or replacements. Thus the facts do not choose between the installed-package branch and the program/derived branch. Windows executable format alone is not grounds to call them unexecutable: Wine is installed and its action log records execution.

C4 — Ten Steam diagnostic text logs: RECORD. These are runtime-written diagnostic output, retained on a persistent filesystem. The Steam startup/update logs identify the logging operation. No code shebang is present. An execute permission bit does not make diagnostic output code. S8.2-15 applies; S8.2-5 does not because the files persist.

C5 — 31 compressed update archives in Steam's updater cache: RECORD. The supplied updater logs record downloading, extraction, installation and cleanup. These named compressed archive files are retained downloads, distinct from their installed extracted contents. The archives are neither executing code nor installed payload files. They are the updater's cache under S8.2-15. This does not infer that the extracted files are unchanged.

C6 — 13,650 remaining Steam client/runtime resources lacking installation comparisons: UNKNOWN. This is a homogeneous rule about the unresolved first question, not a claim that all resources have the same format. It includes images, locale data, shared libraries, JavaScript, shell scripts and binaries. Startup/update logs and the runtime documentation establish the role of these trees, but neither supplies the missing current-to-installation comparison. If unchanged package content, question one applies regardless of format; if changed, subsequent questions are required. S8.2-6 prevents guessing no to question one. The installed runtime's name does not make persistent files RUNTIME. The script asserts persistent regular-file metadata and checks native aliases/inodes before applying this rule. App caches, logs, update archives, metrics and user configuration were separated for individual or other-rule treatment.

## Individual cases

The twelve rows listed under `individual` in the audit are decided separately. Two Lutris-installed archive utility executables have a logged successful installation but no unchanged-since-installation comparison, hence UNKNOWN. Two updater metric files are RECORD; the Steam update log explicitly records saving metrics. Two app/package metadata caches are RECORD, supported by the documented binary metadata format and the cache paths. Six configuration, library-location or registry files are UNKNOWN: their actual stored values are not included, so launch/access-controlling choices cannot be separated from other application records. This includes the Steam apps library-location file; its classification does not assume it was delivered unchanged with a package.

## Documentation and quoted passages

- [Steam runtime](https://github.com/ValveSoftware/steam-runtime): “The Steam Runtime is also used by the Proton Steam Play compatibility tools”. This establishes the runtime's purpose, not local integrity.
- [Debian package metadata](https://www.debian.org/doc/manuals/debian-handbook/sect.package-meta-information.en.html): “All of the configuration scripts for installed packages are stored in the `/var/lib/dpkg/info/` directory”. This establishes the control-script role.
- [Wine installation source](https://github.com/wine-mirror/wine/blob/master/loader/wine.inf.in): “WineFakeDlls=FakeDlls” and “10,,notepad.exe”. The source lists prefix builtin creation; it cannot authenticate this inventory's executable bytes.
- [Lutris installer specification](https://github.com/lutris/lutris/blob/master/docs/installers.rst): its installer specification documents downloaded files and installation tasks. Local successful installation is separately recorded in `A3/in/operator/gaming/actions-logs/actions-logs/gaming_launcher_tool.log`.
- [Steam metadata parser](https://github.com/xPaw/SteamAppInfo): “Parser for appinfo.vdf and packageinfo.vdf files used by the Steam client”. The documented records include application identifiers, update timestamps and binary key-value data.

No probes, execution of inventory files, downloads of executable payloads, or machine changes were needed.

## Manual checks

Each of the following ten rows per rule was read by hand, including its path, regular-file type, persistence, shebang indicator and signature coverage. C1 additionally checked the actual package-integrity joins. C2 and C3 checked the role and missing comparison; C4 and C5 checked diagnostic/cache identities; C6 deliberately checks different resource formats. Paths below abbreviate the inventory user directory as `~`.

### C1

- `gaming-2602c9f36bee7bdd07b93859`: `/usr/lib/apparmor/apparmor.systemd`; persistent regular file; shebang present; observed signature covers 2231 of 2231 bytes.
- `gaming-d789c89d6c4b15fc84237fdc`: `/usr/lib/apparmor/profile-load`; persistent regular file; shebang present; observed signature covers 1984 of 1984 bytes.
- `gaming-c6b83335abba75a457582b3b`: `/usr/lib/apparmor/rc.apparmor.functions`; persistent regular file; shebang present; observed signature covers 4096 of 9857 bytes.
- `gaming-ccca18b4c41965a08e4d2521`: `/usr/lib/cups/backend/dnssd`; persistent regular file; no shebang; observed signature covers 4096 of 26928 bytes.
- `gaming-e2ec8746c636a3c7c823cb5e`: `/usr/lib/cups/backend/lpd`; persistent regular file; no shebang; observed signature covers 4096 of 51592 bytes.
- `gaming-b441fa9c5df0fd36c00d0f66`: `/usr/lib/cups/backend/mdns`; persistent regular file; no shebang; observed signature covers 4096 of 26928 bytes.
- `gaming-7b8b804e906bab4f5a36ccf2`: `/usr/lib/cups/backend/snmp`; persistent regular file; no shebang; observed signature covers 4096 of 31024 bytes.
- `gaming-efa0671f7d85b8a716cb7265`: `/usr/lib/cups/backend/socket`; persistent regular file; no shebang; observed signature covers 4096 of 43400 bytes.
- `gaming-ed8440f84df0ecb4a2a5c27d`: `/usr/lib/cups/backend/usb`; persistent regular file; no shebang; observed signature covers 4096 of 35120 bytes.
- `gaming-3f36c86f4df1895ed850811d`: `/usr/sbin/apparmor_parser`; persistent regular file; no shebang; observed signature covers 4096 of 1629848 bytes.

### C2

- `gaming-c2ce00f6204e4581fca637ab`: `/var/lib/dpkg/info/apparmor.config`; persistent regular file; shebang present; observed signature covers 124 of 124 bytes.
- `gaming-343b27967a5abbf29ced7e1d`: `/var/lib/dpkg/info/ca-certificates.postinst`; persistent regular file; shebang present; observed signature covers 4096 of 5767 bytes.
- `gaming-db4e8c5d26719a189305a777`: `/var/lib/dpkg/info/cups.prerm`; persistent regular file; shebang present; observed signature covers 295 of 295 bytes.
- `gaming-23b44ed89158f8cb64197c3b`: `/var/lib/dpkg/info/libgdk-pixbuf-2.0-0:amd64.postinst`; persistent regular file; shebang present; observed signature covers 1079 of 1079 bytes.
- `gaming-f64248754b57f0d2d16f130f`: `/var/lib/dpkg/info/libglib2.0-0t64:amd64.preinst`; persistent regular file; shebang present; observed signature covers 2102 of 2102 bytes.
- `gaming-08526a1c61d34c1b04bfd690`: `/var/lib/dpkg/info/libgstreamer1.0-0:i386.postinst`; persistent regular file; shebang present; observed signature covers 831 of 831 bytes.
- `gaming-a27a5a6dc6490e7d6bc78ef5`: `/var/lib/dpkg/info/libsasl2-modules:i386.preinst`; persistent regular file; shebang present; observed signature covers 213 of 213 bytes.
- `gaming-4f680b1bf28d0dcedbb5c5da`: `/var/lib/dpkg/info/network-manager.postrm`; persistent regular file; shebang present; observed signature covers 2373 of 2373 bytes.
- `gaming-e79e15cb5f9ec3093221667a`: `/var/lib/dpkg/info/util-linux.postinst`; persistent regular file; shebang present; observed signature covers 1941 of 1941 bytes.
- `gaming-2e8396bfc9c325e4f7cf1a30`: `/var/lib/dpkg/info/xz-utils.prerm`; persistent regular file; shebang present; observed signature covers 204 of 204 bytes.

### C3

- `gaming-eb2b3a947a931608cb526b55`: `~/Games/wine-tools/drive_c/Program Files (x86)/Internet Explorer/iexplore.exe`; persistent regular file; no shebang; observed signature covers 4096 of 208028 bytes.
- `gaming-4c6cad7e64b2d996af42f374`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 572701 bytes.
- `gaming-81a9e166228372d61241ff85`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 188160 bytes.
- `gaming-544643cd4f07874d8ae5b306`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 135100 bytes.
- `gaming-62bc191048d10cd3de179cc6`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 3379646 bytes.
- `gaming-3459f1ff5dcfd34b8d1961f6`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 1626655 bytes.
- `gaming-51137638118caf8f6f66c569`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 80539 bytes.
- `gaming-de812d624dd5cb9115de419f`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 105269 bytes.
- `gaming-f28abde4d9064f887410fe2e`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 105695 bytes.
- `gaming-ff8757631351e0aeb4d58b9c`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 758722 bytes.

### C4

- `gaming-bf81e2a6616da98711f164c9`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 500 of 500 bytes.
- `gaming-3ceead0e81be46c408ba010b`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 2176 of 2176 bytes.
- `gaming-9200d2598240b9d8a1bcc958`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 49231 bytes.
- `gaming-617da08ab6bceb6164551c44`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 194 of 194 bytes.
- `gaming-d0328c10b47623705b317a6c`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 1265 of 1265 bytes.
- `gaming-68d7e3cf854102cd101b63c1`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 6440 bytes.
- `gaming-e5361c26baf9186c7f51e839`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 342 of 342 bytes.
- `gaming-2748c6f95b256c536b1fcd7f`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 128 of 128 bytes.
- `gaming-f7a489f62af16e72bdde4580`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 778 of 778 bytes.
- `gaming-2fbaf0faa85e1e0e3a37e49a`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 148 of 148 bytes.

### C5

- `gaming-8cc0b1b4f61e41237a509f4b`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 26373096 bytes.
- `gaming-b9490dffe916c5dcc4575874`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 9644164 bytes.
- `gaming-02c5ce2325ffed13e4fc2314`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 788129 bytes.
- `gaming-a18619f0888e2c62038b921b`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 61644426 bytes.
- `gaming-2a2e565a442586f428d15c24`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 25274088 bytes.
- `gaming-9d0f90474effb49313e6e36c`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 63587638 bytes.
- `gaming-92303a3b6a6e1ad452236f8b`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 11298450 bytes.
- `gaming-1bf31fa35842b2def02e6397`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 28679233 bytes.
- `gaming-6eea7e611fbb7d0344f7e79a`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 114150 bytes.
- `gaming-55198cd04a05c574f6a5140a`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 89726448 bytes.

### C6

- `gaming-5f357eb62b3ebf551059d3ac`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 1047092 bytes.
- `gaming-250da866085f64616d41123d`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 1856 of 1856 bytes.
- `gaming-42c62619a8cd8090cb44e771`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 829 of 829 bytes.
- `gaming-800513bd1abfba236aedb6ed`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 7100 bytes.
- `gaming-116b3404525ce2f413c3b40d`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 17832 bytes.
- `gaming-90f0e7c96b461d8a6219e1c1`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 14040 bytes.
- `gaming-46f7a71e2b0247ec7b6b8061`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 6084 bytes.
- `gaming-0570f28e3f788633b078ba93`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 2956 of 2956 bytes.
- `gaming-7f1173ee16006bf0b25baef7`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 70685 bytes.
- `gaming-847958fd4d92409680ef0bf0`: (not published: record outside this collection); persistent regular file; no shebang; observed signature covers 4096 of 203520 bytes.


---

# Special rows: independent classification c1

Scope: 590 rows other than stored-ownership-unresolved and code-ownership-unresolved. Only the fixed text, sentence index, FACTS, gaming inventory and relevant gaming action logs were consulted. No previous classifications were consulted.

The executable rule implementation is `part-gaming.special.py`. It appends and flushes rows, preserving completed IDs on rerun. The package/file integrity join uses original collector IDs and exact paths. No prefix digest was treated as full-file integrity. These rows are packages or runtime observations, except two unit files, a connection profile and an unexpanded persistent directory.

## Literal rules

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

Rule P: installed dpkg packages with explicit reason get INSTALLED-OWN; packages with dependency reason get INSTALLED-DERIVED. The package itself answers question one, so no claim about the contents' executable status is needed. Native manual/automatic reason records were used. Three Python distributions have unknown reason; metadata ownership does not transfer native installation reason, as FACTS explicitly states.

The six Flatpak rows were considered individually. Chess is the installed application marked explicit. The other five rows are runtime/extensions marked dependency solely by application/runtime distinction; the inventory explicitly disclaims historical user intent. The official documentation permits manual runtime installation, so UNKNOWN identifies the missing installation reason. The action log shows a series of installations and Chess's runtime identity but does not record the initiating command or distinguish which runtimes were explicitly requested.

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Rule R: observed processes and sockets are RUNTIME. Known executable paths are joined to package-files.tsv; every matched executable here is unchanged, giving creator INSTALLED-PACKAGE. Missing executable/owner identity leaves creator decision UNKNOWN, but every possible identity still gives the row RUNTIME. The collector probe is executing code, but its acquisition/derivation provenance is not established by the allowed inventory.

Rule T: list-units and list-timers observations describe current in-memory state, not an independent persistent declaration of enablement. These are RUNTIME; unchanged packaged unit files give creator INSTALLED-PACKAGE. Each unit filename was extracted from the actual record, not the inventory name (which is a weekday for timers). All 18 service/timer observations join unchanged packaged unit files.

Two unit-file rows were considered separately. FluidSynth names an unchanged packaged user unit file: INSTALLED-PACKAGE by the first question. The generated Lutris service unit is runtime output of the XDG generator; the persistent autostart entry is an individual launch choice, SETTING-OWN. The filesystem lists the autostart entry as persistent, outside package manifests.

The loopback connection row is UNKNOWN: nmcli connection show does not establish that a profile is persistent or chosen, and NetworkManager can generate an in-memory profile for an existing interface. The unexpanded Flatpak directory is UNKNOWN: its persistence is established, but a directory observation does not supply complete members or their provenance. No executable classification is inferred from a directory's executable permission bit.

## Documentation and factual checks

- https://docs.flatpak.org/en/latest/dependencies.html — “manually install your chosen runtime”; runtimes can be explicitly installed, so runtime type alone does not prove historical dependency acquisition.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.” The list-timers description likewise specifies current memory and next/last firing times.
- https://www.freedesktop.org/software/systemd/man/254/systemd-xdg-autostart-generator.html — the documented generator creates service units for XDG autostart files.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html — “By default, those paths are runtime directories”; user generator output belongs under the runtime directory.
- https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html — “generating a in-memory connection based on the interface current configuration.”
- Raw basis: (not published: over 20 MB); raw/0079-package-reasons-apt-manual.out; raw/0080-package-reasons-apt-auto.out; raw/0433-process-executables.out; raw/0417-service.out; raw/0418-timer.out; raw/0442-user-user-service.out; raw/0443-user-user-timer.out; raw/0444-user-user-unit-file.out; raw/0427-saved-network.sh; raw/0004-filesystem.out.
- Action evidence: A3/in/operator/gaming/actions-logs/actions-logs/gaming_flatpak_game.log, gaming_autostart.log, gaming_user_settings.log. The autostart log is empty; no command was invented from it.

## Manual rule checks

The following rows were individually inspected in input and the cited raw records before applying the corresponding rule. For package checks, each reason was confirmed in apt manual/auto output. For process checks, each executable was inspected against its unchanged manifest row. For timers, each complete record and unchanged unit-file join was checked. Smaller classes were checked in full.

P explicit (first ten native rows): gaming-c7f293bcc7bcf4817808578f, gaming-930e136beb07b315522fcf91, gaming-3cf14c7ed1354d58ec624b62, gaming-420feed371f78300f90fc7e4, gaming-68a8510ef612ec646111c30c, gaming-5fd7a551afe2bf1d7f0c0727, gaming-208a407e9b8ad788f9ed65e5, gaming-5b8937a1441f3afbb07fde65, gaming-6ff4bb862fc7c9a79185e240, gaming-92756e5c1784395c54d48044.

P dependency (first ten native rows): gaming-7406448a9fd1148b0b19ef51, gaming-f1783669f0787c3564a8ecfe, gaming-9142e5339fc6ea84e461b278, gaming-42b7e42a0a1a999533c97971, gaming-22a8e0654be5e800ef2f6bc7, gaming-e1799827c801c18831d4bcb8, gaming-2f1d6d4ca9d1b8351b2d4a03, gaming-a473e408dbb41d6075eafd82, gaming-70a4b47581b29d4eb275deb2, gaming-afd13d1696a86c8581a52644.

R packaged processes (ten): gaming-a6b6b058fce1692666587ec9, gaming-77f39ce29145b21233ae617e, gaming-f331c20b851fe6575db44a02, gaming-e5663600fbffa42ed23c8cbe, gaming-c10c8b660c72066cb7f3c962, gaming-e4d4ebec90d074553f5725c5, gaming-d9efe4b8abfb75ea3f9c020c, gaming-0cb7818fab83e10338da62ab, gaming-642b769dc51f531677cacf2a, gaming-664654ffa9e3f71c098eec17.

R unknown executable identity (ten): gaming-ad80cfa51beac9c25cd7440b, gaming-e9179fe81245ffd3992a4cb1, gaming-fd41e05178017214ddd69c2a, gaming-01d40bf1231fb8db16256a7e, gaming-42390cbbf0b651683170de80, gaming-2a2e7c46defeb7dd95c48a5f, gaming-84634229f7f9364537f20bd6, gaming-0fc0effde8d7359f4fb826cc, gaming-354ea917032345dc2ba7493f, gaming-329a0e29c581ef1941c6d87d.

R ports (all three): gaming-73547c53129fe57e55cbd39c, gaming-334d7e6ea2c8abcbbfae69e0, gaming-3d48195e703e3661e833221e.

T timers (ten): gaming-800b4718bbcdaef798050f69, gaming-ac06b4cde0da2f84829fcade, gaming-99ae628343ffb742cd897b01, gaming-e8dc6daa0166d2d315182b22, gaming-d00aa23e09d01e6b65045db5, gaming-181d0ead3d9b9aa3b67c987f, gaming-30db09b3b7343da38e3873dc, gaming-3c04817973c2c4ff96599d25, gaming-05fa1da6777a4976051c47cd, gaming-eb7b5e337ea143949bd9a31a.

T services (all five): gaming-e4d6e5e83a4ace5785f13e26, gaming-d0fea8ad2579a8323d482fd9, gaming-cd58d8cd105823bb7f4d80e7, gaming-4ab7eabe1911a3b0d19ba92c, gaming-b2da6817c8af70e071138781.

Python packages (all three): gaming-15a5df1726b5e762eb665dc0, gaming-9fcda2e5da0da17c5c7b04bc, gaming-81623cd696d6fa4dcfb9b26e.

Flatpak packages (all six): gaming-0bf2c7ef261b932eddadd387, gaming-94af2c167b7a79b710953f0f, gaming-3744c51d50c0773cd9a880a4, gaming-a079c47a274e46f0230f0608, gaming-7f6321f4b0c51538073f240a, gaming-a77288b7225b9c0ae94074a4.

Validation: exact 590 input IDs, each once; all decisions allowed; all descriptions within 15 words and reasons within 30 words. Counts: {'INSTALLED-OWN': 424, 'INSTALLED-DERIVED': 58, 'UNKNOWN': 10, 'RUNTIME': 97, 'INSTALLED-PACKAGE': 1}.


---

# Gaming stored-member groups, c1

Scope: all 1,872 input rows whose inventory kind is `2:stored-ownership-unresolved`. The inventory label is not a classification. (not published: orchestration or scratch), `TEXT.md` Sections 8.1–8.3 and 8.5, `SENTENCES.md`, and `A3/in/FACTS.md` were read first. No other classification was consulted.

The full tables named by these rows contain 35,128 immediate members. Each table was read completely, its count checked against the row metadata, and its traversal-completeness flag checked. Members include directories as well as files, symlinks, sockets, FIFOs and devices. A directory is not silently replaced with its recursive contents. Classification of a separate row for its contents does not settle the directory entry's origin.

(not published: direct evidence at least 2 MB) identifies every member by input group id, one-based member-table row number, and basename. These three fields refer unambiguously to the complete original table. It gives each member's decision and missing fact or deciding reason. Every MIXED row references this exact map. It also records the reasoning for homogeneous rows rather than concealing exceptions in a sampled group.

## Facts used

- (not published: over 20 MB): installed package membership and whole-file integrity. A missing entry was not treated as proof of non-package origin. The inventory explicitly reports incomplete package ownership coverage in `metadata.json`.
- (not published: direct evidence at least 2 MB): installed native package identity and explicit/dependency reasons. The runtime creators used here all have known native package reasons; their decisions are named in the member map and output reasons.
- (not published: direct evidence at least 2 MB): installation provenance is frequently explicitly unknown. Timestamps and script mentions do not prove that a configuration value was created during installation.
- (not published: over 20 MB): persistence, actual types, symlink targets, and device/inode identity. It establishes the aliases `/bin` → `usr/bin`, `/sbin` → `usr/sbin`, `/lib` → `usr/lib`, and `/lib64` → `usr/lib64`. Package joins normalize these observed aliases. Identical device/inode pairs also recover the CUPS backend hardlinks; a matching prefix hash alone never establishes identity or unchanged status.
- All 35,128 members have known persistence: 34,096 persistent and 1,032 runtime. Persistent sockets/FIFOs were not automatically called transient merely because their active endpoints are transient.
- Input action logs for launcher installation, Windows-program execution, and user settings were also examined. They establish executions and installation events, but do not provide full current-versus-installed comparisons for every Steam, Wine, or downloaded payload member.

## Deciding sentences

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

## Rules and hand checks

The script `part-gaming.groups.py` applies the following member rules in order and aggregates only after all members are decided. UNKNOWN is a missing-fact result, not a proposed repair to the text. Section 8.5's storage and enforcement design questions are not gaps.

### Package and provenance evidence

An unchanged manifest member, including a verified path alias or identical inode, is INSTALLED-PACKAGE by S8.2-6–8 and S8.2-16. Otherwise a missing first-question fact remains UNKNOWN if its possible answers change the decision. In particular, a Steam asset can be unchanged package content or altered content; its pathname and first 4,096-byte signature cannot establish the former. An executable bit does not establish that an arbitrary log or asset contains executable code. A directory's lack of a manifest entry does not establish who created it.

Hand-checked ten group rows for these fact conditions:

- `gaming-f0a9df95219dd5d754a0f6e9`: GRUB entries; no full package/integrity join for these generated/copied paths.
- `gaming-61483700375520f8155e3df6`: configuration and state; recorded origin uncertainty prevents assuming defaults.
- `gaming-d5aba99d46bf02ccbb790689`: alternatives links; target names do not establish original/default versus later selected link state.
- `gaming-b9fd058e4c13a03c9e02ea66`: one AppArmor tuning file; creation provenance unknown.
- `gaming-d451adfd92919bb0ea885c82`: CUPS configuration and subscriptions; no complete provenance/integrity evidence.
- `gaming-c002466b0636040c062a265e`: five PAM generated configuration candidates; installation origin unknown.
- `gaming-37978ac0c56987eb4914c41e`: certificate links and bundle; selected trust sources and current original equivalence unestablished.
- `gaming-8ac297c67303303673ce1fdc`: service link and directories; creation/default origin unestablished.
- `gaming-365cbfb8a4e3624fbec64364`: four service activation links; default versus person-selected state not established.
- `gaming-c6a6144cf5efeea6c1f882d5`: single persistent directory; no observed origin sufficient to choose installed/record/material.

All six native groups with recovered unchanged members were additionally checked individually: `gaming-fc557f3125938f34d3727148`, `gaming-f14f42f597efb3f8a03d34e3`, `gaming-0b9c75abae9461b0be7b041d`, `gaming-7045b2cfb39b6919d6cbb076`, `gaming-b5b399a1952d145cba092894`, `gaming-4b2f118928192eae89e5ccb0`. The first, fourth, fifth and sixth are MIXED because their remaining links or generated objects lack deciding integrity/provenance facts. The AppArmor group and six CUPS backend members are entirely INSTALLED-PACKAGE. The separate `gaming-5024a5607275cd351095bdf1` directory group has package associations but unknown integrity, hence UNKNOWN.

### Python bytecode

Persistent `cpython-312.pyc` members under the system Python `__pycache__` directories, with corresponding unchanged package-owned `.py` sources, are PROGRAM-DERIVED by S8.2-9–10 and S8.2-16. Each source is joined separately; a directory containing a cache directory is not itself executable bytecode.

[Python FAQ](https://docs.python.org/3/faq/programming.html) states: “creation of a .pyc file is automatic if you’re importing a module”. [Debian Python Policy](https://www.debian.org/doc/packaging-manuals/python-policy/) states: “the byte-compiled modules must not be shipped with the binary package”. This distinguishes generated executable cache files from unchanged files received in the package.

Hand-checked ten complete bytecode group rows, confirming version-tagged filenames, persistent files, and their unchanged source-package joins:

`gaming-4907aa06823bfde8dce6f982`, `gaming-d6be9189d16dc2825d0ebaf3`, `gaming-d7207a900f35c49f1cde2f7e`, `gaming-fbb29da26124e26b433935a0`, `gaming-23382bc4609b7d0a44eba5a4`, `gaming-2be08990cdfb1267e67f6400`, `gaming-92fe7321497a6eb0dba3ac6d`, `gaming-d7cc084b7bc880125dedcef7`, `gaming-d6a1624ce14a9344ec8d659f`, `gaming-83d99db0fb36ece0bc035be7`.

### Program records

Observed diagnostic/history files in the enumerated logging locations and package manager `.list` inventories are RECORD by S8.2-15 and S8.2-2. This is not a generic rule for everything in a cache or data directory: possible code caches, launch values, credentials, package metadata received in archives, and directories retain separate decisions.

[Steamworks uploading documentation](https://partner.steamgames.com/doc/sdk/uploading) describes `content_log.txt`: “Lists all logged SteamPipe operations and errors.” [systemd file hierarchy](https://www.freedesktop.org/software/systemd/man/256/file-hierarchy.html) describes `/var/log` as persistent log storage and `/run` as runtime storage. The input's action-log files are the captured command outputs themselves. The dpkg `.list` files contain installed path inventories; their raw contents are available in the metadata-read outputs.

Hand-checked all ten groups to which this record rule applies:

`gaming-2dac226320b6f354608c3b7b`, `gaming-0528c26cdd0cdd77fcb380b1`, `gaming-2ffd964e585c353313bc520e`, `gaming-63e2acee9dd1c09ce676ad5f`, `gaming-ef0828c6f747894897b5efe1`, `gaming-7dc478f00b1ef77f21328793`, `gaming-2720a9e9ed4064eab6eeaece`, `gaming-fa9b5f9fc3de1f5bc7bdb2de`, `gaming-9c924a29b4d7e177f169f369`, `gaming-3c49d8ede866731e9d36a16a`.

The Lutris cache, top log directory and dpkg information directory are MIXED. Their maps distinguish log/files-list records from directories, metadata or scripts whose required provenance/integrity fact is missing. In particular, maintainer scripts were not mislabeled records merely because dpkg stores them.

### Runtime objects

Members positively marked runtime, whose creating subsystem is identified, are RUNTIME by S8.2-5. Their creator's installed native package and its explicit/dependency reason determine the named inherited decision. The runtime map distinguishes NetworkManager, CUPS, D-Bus, systemd, udev, and session daemons. [udev documentation](https://www.freedesktop.org/software/systemd/man/latest/udev.html) states that matching rules provide information “to be stored in the udev database”. [systemd execution documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) documents runtime directories and private temporary directories.

Hand-checked ten complete groups for persistence and creator association:

`gaming-70a5f4e6de517cdfe4d6d563`, `gaming-0a11dcbb1aa2221152ddbe04`, `gaming-579e9ff33bed334e9ea093a5`, `gaming-7b7b6ebff6237a7347c1322f`, `gaming-64b489715c2bde942a579bd0`, `gaming-17c9f1235ee1cb98f258b3a5`, `gaming-1733df06abe7085517577d40`, `gaming-3fe08d01e4f4b7617de68a23`, `gaming-3b45f88a79f6db15c8923720`, `gaming-de883a85e06bfe7120ecc147`.

Four heterogeneous groups additionally contain runtime members with unestablished creator association, individually inspected: `gaming-d6e7cd8207d135165f0e39be`, `gaming-8b7138a7e9691ba6cff8e1e3`, `gaming-48246940849ffde2a4c99c53`, `gaming-cca7f34869a6ff1d0fe2858a`. Their member map names the missing runtime creator fact; `/run` is MIXED because several creators are known. A pathname alone was not used to choose a creator for shared lock/session roots.

## Validation

The script appends and flushes each finished group row, preserves pre-existing ids, and verifies exact id multiset equality with this input subset. All 1,872 ids occur exactly once. It checks the 15-word description and 30-word reason limits. All member counts and complete flags pass. The final parent merge must validate the full gaming part's allowed decisions and id coverage.

Counts: UNKNOWN 1,700; RUNTIME 120; PROGRAM-DERIVED 35; MIXED 8; RECORD 7; INSTALLED-PACKAGE 2.
