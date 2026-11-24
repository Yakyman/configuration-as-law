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
