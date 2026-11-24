# Classification c1: alma

Scope: the supplied alma inventory only. No other classification was consulted. Results are appended by id; independent partitions are merged after completion.

## Package rules

The object in an L1 package row is the installed distribution unit, not its metadata file. An installed package satisfies the first half of S8.2-7 even if a constituent file changes. A native metadata owner establishes the distribution provenance given in the collector; its installation reason is not transferred to the language package. Individual stored files are decided separately and require installation-integrity facts.

**package-reason:** For packages without native enclosing-package provenance, apply S8.2-7 and S8.2-8 first. Under S8.2-16, explicit installation needs its own line; retained dependency provenance uses the source line. Unknown installation reason gives UNKNOWN because own and derived lines differ. No historical intent is inferred from a package name, group selection, directory nesting, or absence of REQUESTED. Flatpak reason values are used as supplied, including their stated app/runtime interpretation.

**package-native-provenance:** An installed language distribution with retained native_package_ids is obtained with the identified native package, and S8.2-16 permits its package line. This does not transfer the native package installation reason. For the 195 npm distributions, additionally checked every observed non-directory descendant against the native manifest: all are unchanged files owned by nodejs-npm. For Python, the package entity is identified by the native-owned installed-distribution metadata; no rule of directory containment is applied to separate file objects.

**python-transaction:** The sixteen local Python distributions with unknown stored reason are explicitly named as dependencies in the retained pip transaction in D1/in/control/alma/actions-logs/browser_extension.log. Its Collecting lines identify their parent dependencies and Successfully installed confirms installation. S8.2-16 therefore selects INSTALLED-DERIVED. The distro row has a misleading collected display name; its directory, version and transaction identify distro 1.9.0.

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

## Public documentation

https://packaging.python.org/en/latest/specifications/recording-installed-packages/ — “This document specifies a common format of recording information about Python projects installed in an environment.” Installed-distribution metadata also supports integration by system package managers.

https://peps.python.org/pep-0376/ — “the presence of this file indicates that the project installation was explicitly requested (i.e., not installed as a dependency).” This describes REQUESTED; the retained inventory reason remains authoritative where unknown.

https://docs.npmjs.com/cli/v10/configuring-npm/folders/ — “Packages are dropped into the `node_modules` folder under the `prefix`.” Directory structure establishes package layout, not historical installation reason.

## Manual package-rule checks

Each listed row was inspected with its retained manager, reason, provenance and/or transaction entry before applying the rule.

### package-reason

- alma-e7c6fc3e717bdc39acbe0e65: rpm:grub2-tools; retained reason explicit; decision INSTALLED-OWN. Reason/transaction evidence inspected.
- alma-d15afe8d066344657cce9f0e: rpm:libgcc; retained reason dependency; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-6494449f525eb29a533ddefb: rpm:redhat-text-vf-fonts; retained reason unknown; decision UNKNOWN. Reason/transaction evidence inspected.
- alma-77ccb9a9685c546ff4b596ea: flatpak:org.gnome.Calculator/x86_64/stable; retained reason explicit; decision INSTALLED-OWN. Reason/transaction evidence inspected.
- alma-4426938d9cfaf66a2d7f76ac: flatpak:org.freedesktop.Platform.GL.default/x86_64/26.08; retained reason dependency; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-fae4303fc7ec8aa0b6457dcc: rpm:libldac; retained reason dependency; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-84f4a95a340da8476f366e48: rpm:wget; retained reason unknown; decision UNKNOWN. Reason/transaction evidence inspected.
- alma-fd960653df1f48027cf22150: rpm:cockpit-storaged; retained reason unknown; decision UNKNOWN. Reason/transaction evidence inspected.
- alma-aa07c56096e3c04d8b47f08b: npm:locate-path; retained reason unknown; decision UNKNOWN. Reason/transaction evidence inspected.
- alma-1de7785d06643decb0c982c5: npm:camelcase; retained reason unknown; decision UNKNOWN. Reason/transaction evidence inspected.

### package-native-provenance

- alma-5781f1c5e748b32ec6bd2bfd: npm:negotiator; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-8785c4d0afae73edf6ff40d6: npm:read-package-json-fast; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-7c534288e3b1770ca609b28a: npm:parse-conflict-json; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-2545403355ad142b45a00324: npm:; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-c208634804bba39ca48e3228: npm:fastest-levenshtein; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-912cb46ce54333de07fa3bd7: python:setools; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-9c23ebcd29c06347fc2c9da3: python:cupshelpers; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-1f13e5d5fde8f28562017c50: python:pexpect; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-f49733d837fa2b7abe12b867: python:charset-normalizer; retained reason unknown; decision INSTALLED-PACKAGE. Native metadata provenance inspected.
- alma-f620e45c5f534d79f98b0a79: python:setroubleshoot; retained reason explicit; decision INSTALLED-PACKAGE. Native metadata provenance inspected.

### python-transaction

- alma-317678ed0ffc7c1ad32d2df1: python:mozdevice; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-b321ebb1d8d25e3ff86b1922: python:wcwidth; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-5e792ad7daa2de59dfabb7dd: python:psutil; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-82505a705d69df249b2672db: python:Antergos Linux; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-0faeaaa180720d4201db3105: python:mozinfo; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-2478b390d4b644352dc24f74: python:mozprofile; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-325919992f6861836a62dbc6: python:mozversion; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-afbb55e45941dbf71aea7846: python:six; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-69424af0c27db54b28852bb0: python:mozterm; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.
- alma-c9bb0ec522288aabf4ffe0fd: python:mozfile; retained reason unknown; decision INSTALLED-DERIVED. Reason/transaction evidence inspected.

## Individual stored files and images

All 41 non-group L2 rows were inspected individually. Thirteen native packaged files resolve exactly after the four filesystem symlinks /lib, /lib64, /bin and /sbin are followed, using their recorded target fields; the manifest says unchanged. S8.2-7 wins before code classification. Manual checks for this homogeneous unchanged-file rule (more than ten) are listed below.

- alma-25176a28b7d7ed7371093514: mozprofile-3.0.0.dist-info; full RECORD digest and length match; target relocation.
- alma-10bc649121ba7ef86033b403: distro-1.9.0.dist-info; full RECORD digest and length match; target relocation.
- alma-d880c5c4411e5bdcad05db6a: mozinfo-1.2.3.dist-info; full RECORD digest and length match; target relocation.
- alma-7f97fb902f645924421f7c7b: mozprofile-3.0.0.dist-info; full RECORD digest and length match; target relocation.
- alma-13d3dfc50a72ff2813a06b95: mozrunner-8.4.0.dist-info; full RECORD digest and length match; target relocation.
- alma-99622631f1e5793089634f11: mozversion-2.4.0.dist-info; full RECORD digest and length match; target relocation.
- alma-b164e398bd90722262f2331f: mozlog-8.1.0.dist-info; full RECORD digest and length match; target relocation.
- alma-d8583070854b6aad793bd087: mozprofile-3.0.0.dist-info; full RECORD digest and length match; target relocation.
- alma-bc8c1d0bc92e8fedfad3e4de: /usr/lib/grub/i386-pc/boot.img; native manifest unchanged.
- alma-3c5ceed80b44ac39dc52a59a: /usr/lib/grub/i386-pc/boot_hybrid.img; native manifest unchanged.
- alma-03657ab5873778ad0d8335d3: /usr/lib/grub/i386-pc/cdboot.img; native manifest unchanged.
- alma-6a7357367121265496a7598b: /usr/lib/grub/i386-pc/diskboot.img; native manifest unchanged.
- alma-454e94b5083bb77d5d98e678: /usr/lib/grub/i386-pc/kernel.img; native manifest unchanged.
- alma-0a3f791a72dacd2ace6916af: /usr/lib/grub/i386-pc/lnxboot.img; native manifest unchanged.
- alma-ab516f0d2c8063551d1116ef: /usr/lib/grub/i386-pc/lzma_decompress.img; native manifest unchanged.
- alma-479e48e3ec956f3029b757ff: /usr/lib/grub/i386-pc/pxeboot.img; native manifest unchanged.
- alma-bd4b4bd3b7f6287a8e0a964c: /usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/vdso/vdso32.so; native manifest unchanged.
- alma-94aa634cbe3ceca5bb037624: /usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/vdso/vdso64.so; native manifest unchanged.
- alma-5e51775b786d8f19b9eda332: /usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/vmlinuz; native manifest unchanged.
- alma-ab0f7c1aee74801b2910a6b6: /usr/lib64/libgcc_s-14-20260724.so.1; native manifest unchanged.
- alma-7a05249c5c5f0de1ee0dd7ac: /usr/lib64/libtirpc.so.3.0.0; native manifest unchanged.

Eight Python entry scripts require a separate individual integrity calculation: each retained signature covers the whole file (size equals signature_bytes, under 4096), and its digest equals the installed RECORD SHA-256. These are not assumptions from prefix signatures: both the recorded installation digest and the complete-file length were checked. The apparent ../../bin path discrepancy is explained by pip target relocation, documented by the retained pip version source: https://github.com/pypa/pip/blob/23.3.2/src/pip/_internal/commands/install.py — `shutil.move(os.path.join(lib_dir, item), target_item_dir)`. Its _handle_target_dir moves library and data-directory items, including bin, into the target. All eight checks are listed above because the class contains fewer than ten objects. The original package-files.tsv is unchanged.

https://docs.telemetry.mozilla.org/concepts/profile/profile_creation — “a `times.json` containing a timestamp of the current time is stored inside that profile directory”. This resolves the individual Firefox file as RECORD despite its execute bits.

https://github.com/containers/crun/blob/main/src/libcrun/seccomp.c — `#define SECCOMP_CACHE_DIR ".cache/seccomp"`. https://github.com/containers/crun/blob/main/crun.1.md — “Path to the file that will contain the container process PID.” These identify the two volatile files; filesystem persistence is runtime and the native crun executable has unchanged integrity.

https://www.gnu.org/software/grub/manual/grub/grub.html — “The sole function of `boot.img` is to read the first sector of the core image from a local disk and jump to it.” Documentation identifies boot code, but does not establish the actual history of each local copy.

- alma-ccee8b9ad93a05d741a4a687: UNKNOWN. GRUB bootstrap image copied into the boot filesystem. Its code is identifiable, but the retained facts do not establish whether the system obtained this copy from a recorded source.
- alma-c83a82a3d1f5bc0ad561ed46: UNKNOWN. GRUB core image combining boot code and modules. The image is executable boot code; its actual build provenance and source line are not retained.
- alma-6ab52ad29dde92c736eff4ca: UNKNOWN. Shell metadata script for the GRUB module installation. Shell code is present, but its package origin, installation integrity, and derivation from a recorded source are unretained.
- alma-2c25c1a886c5db421b08087b: UNKNOWN. Rescue initial filesystem image for early boot. The opaque image has no retained member inventory or build provenance establishing its contents and covering source line.
- alma-c4a7c6d6eb439eb9d680a65e: UNKNOWN. Initial filesystem image used during kernel startup. The package manifest marks this image changed; actual contents and generation provenance are not retained to determine its class and source line.
- alma-9ba0bbb217552126cc411cf7: UNKNOWN. Crash-dump initial filesystem image. The opaque image has no retained member inventory or build provenance establishing its contents and covering source line.
- alma-abd91d1c4f4b41c4ed6eb130: UNKNOWN. Rescue Linux kernel image. Executable kernel code is identifiable, but its actual copy provenance and covering source line are not retained.
- alma-c5e3c35f51457c614d2f0db6: UNKNOWN. Shell script contributing tuned parameters to generated GRUB configuration. The script is executable code; whether it was separately supplied or generated from a recorded source is unretained.
- alma-d8bd0ebf0971269fa664e177: UNKNOWN. Shell commands executed when a login shell exits. Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.
- alma-d9c06dc1dfaaba01abd91aa8: UNKNOWN. Shell commands executed when a login shell starts. Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.
- alma-fbc363e66275dcb22563f6ee: UNKNOWN. Commands configuring an interactive Bash shell. Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.
- alma-cdd79753059a5ce23c29ee2e: UNKNOWN. Executable local shell script. The shebang establishes executable code, but the retained empty action log does not establish its contents, installation origin or generation source.
- alma-930b9792c746a9bafad93f57: UNKNOWN. Node.js command-line entry script for cowsay. Package placement is known, but npm per-file provenance and installation integrity are unretained; unchanged installed content and separately modified code classify differently.
- alma-79608afad4f605639b600ea2: UNKNOWN. JavaScript library implementing terminal-aware text wrapping. Package placement is known, but npm per-file provenance and installation integrity are unretained; unchanged installed content and separately modified code classify differently.
- alma-0c99474b7568b9110f088ac0: UNKNOWN. User Flatpak application and runtime storage directory. Storage is persistent but unexpanded; its complete members and their deployment provenance are unavailable, so a homogeneous or mixed classification cannot be established.
- alma-469368e2c39591fdcb2f7fa7: RECORD. Firefox profile creation timestamps stored as JSON values. Firefox stores profile creation timestamps as values; executable permission does not make JSON code, and these timestamps neither launch programs nor grant access.
- alma-d63af6bccee7492525c0ef96: RUNTIME. Temporary file recording the container process identifier. Exists on a runtime filesystem; crun writes the container PID file. Its unchanged packaged executable is INSTALLED-PACKAGE.
- alma-fb4fb83f1eb057c2339397fa: RUNTIME. Temporary compiled seccomp filter cache created by crun. Exists on a runtime filesystem; crun creates this cache. Its unchanged packaged executable is INSTALLED-PACKAGE.
- alma-9fb5386f2fe6a4a2a188166a: UNKNOWN. Persistent container image and writable-layer storage. Storage is unexpanded; its complete members and their package, code, setting or record status are unavailable.
- alma-3c6010fa39aa94b271b93734: UNKNOWN. System Flatpak storage directory. The directory is persistent and unexpanded; creation provenance and complete stored membership are not retained.


# Completed partition 1: rules and manual checks

# Stored-member classification notes

Scope: 1,647 input groups, 7,286 complete immediate member records. Only the assigned input, retained raw inventory, fixed text, and public program documentation were consulted. No other classification was consulted.

## Interpretation and evidence

The input groups represent their listed immediate children. A listed child directory is evaluated as that directory, not recursively substituted by descendants. The filesystem traversal explicitly records persistence per member; persistent temporary directories were not called runtime merely because their names contain `tmp`. The runtime exception precedes the four object questions. All other members follow the questions in order. `executable=true` on a directory means search permission and does not establish code.

Raw sources: (not published: over 20 MB), (not published: over 20 MB), (not published: over 20 MB), `D1/in/raw/alma/metadata.json`, the input rows, and every member file identified below. The raw filesystem symlink targets establish `/lib`, `/lib64`, `/bin`, `/sbin` as aliases of their corresponding `/usr` directories. Package matching normalizes only these observed aliases. No full-content equality is inferred from prefix hashes.

Package directories appear in the raw RPM manifest but were omitted from the integrity table. A manifest location alone does not establish that a directory remains as received. Unresolved directories therefore remain UNKNOWN unless their documented generated-cache function establishes a program record. Package reasons do not alter coverage of an unchanged member by its package line. Missing lock records and per-file provenance explicitly remain unresolved for npm installation contents.

`UNKNOWN` in a mixed member list means that member cannot be assigned a determinate class from retained facts. It is not a hypothetical text gap. Public documentation supplies program function and format, not unobserved installation history. Where a runtime creator has UNKNOWN integrity/provenance, the member is still RUNTIME because its own volatility is established independently. The parent runtime filesystem setting is UNKNOWN as to own/default line where no more specific creating program is established.

## Exact deciding sentences

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?
- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.
- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.
- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.
- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.
- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.
- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.
- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

## Public documentation

- [pip](https://pip.pypa.io/en/stable/topics/caching/): “A new cache format is now used, stored in a directory called `http-v2`”
- [npm](https://docs.npmjs.com/cli/v8/commands/npm-cache/): “npm stores cache data in an opaque directory within the configured `cache`, named `_cacache`.”
- [DNF](https://dnf.readthedocs.io/en/latest/conf_ref.html): “Path to a directory used by various DNF subsystems for storing cache data.”
- [fontconfig](https://xorg.freedesktop.org/archive/X11R7.0/doc/html/fc-cache.1.html): “These files are generated by fc-cache and contain maps from file names to font properties.”
- [man-db](https://manpages.debian.org/bookworm/man-db/mandb.8.en.html): “mandb is used to initialise or manually update index database caches.”
- [Python](https://docs.python.org/3/faq/programming.html): “to create a `__pycache__` subdirectory and write the compiled module to that subdirectory.”
- [Firefox telemetry](https://firefox-source-docs.mozilla.org/toolkit/components/telemetry/concepts/archiving.html): “pings submitted to `TelemetryController` are also stored locally in the user profile directory”
- [systemd hierarchy](https://www.freedesktop.org/software/systemd/man/253/file-hierarchy.html): “A "`tmpfs`" file system for system packages to place runtime data, socket files, and similar.”

The hierarchy documentation also identifies `/var/log` as persistent system logs. Cache and log rules concern their stored data representations and directory structures. They do not treat executable bytecode as ordinary records. Python rules apply only to the directory named `__pycache__`, never to its compiled files. Unknown browser startup-code caches were not subsumed under the data-cache rule.

## Rules and manual checks

### package

Every immediate member is persistent and joins an unchanged installed-package record, after observed alias resolution. S8.2-7 and S8.2-8 answer question 1 affirmatively; S8.2-16 gives INSTALLED-PACKAGE.

Manual checks (10 rows):

- `alma-a940bd4318e5aeee1f189864`: 20 members; INSTALLED-PACKAGE=20. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-cf04fc8c9ccdc124230a0efe`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-a18c30849227077fee42ec56`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-15b04ae7edf0c299cf48a363`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-322a37838601db0cf1a1426c`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-a193c1be188f62e92e315818`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-23454853abc8ac867343036a`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-fe409521c9a88c85151c2797`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-406d51cae5fdf01be0fcfd83`: 1 members; INSTALLED-PACKAGE=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-25e612bc18b023f39e398976`: 2 members; INSTALLED-PACKAGE=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
### runtime

Every immediate member has runtime backing. S8.2-5 gives RUNTIME independently of its name or code capability. The output names the known creating program and its decision, or the runtime-filesystem setting with UNKNOWN provenance.

Manual checks (10 rows):

- `alma-8e368cdb5235d8765675f4b5`: 41 members; RUNTIME=41. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-8dda45494a90540e8691e981`: 1 members; RUNTIME=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-4dab36083aa6a4961db95c26`: 1 members; RUNTIME=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-8af80e73b4b6c8b961b5b957`: 12 members; RUNTIME=12. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-a59e8fb1350c7f27463b5297`: 71 members; RUNTIME=71. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-6ce45e85020967205052bcd9`: 1 members; RUNTIME=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-1f6ec29aa8d7a5561aae4e55`: 1 members; RUNTIME=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-c1c061d5272019b8ad097fe4`: 1 members; RUNTIME=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-dbb29aaca7d39650e939e504`: 2 members; RUNTIME=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-73a4f540ff34f70c28ed1366`: 3 members; RUNTIME=3. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
### cache

Every member is documented program-generated cache, log, archive data, or its generated directory structure; it is not installed payload, executable code, or a selected setting. S8.2-15 gives RECORD. Documentation identifies pip HTTP data, npm cache data, DNF metadata, font information maps, manual-page indexes, telemetry archives, logs, and Python cache directories.

Manual checks (10 rows):

- `alma-9bd3f1f0e6faf8a2762fa31d`: 2 members; RECORD=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-0e0536bc612d51064a990bdb`: 1 members; RECORD=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-b5d087d1cb18e62f197b474e`: 4 members; RECORD=4. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-d15f2f63f27850d00f28f708`: 2 members; RECORD=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-525676ee6ca94ab9c1eedc0a`: 40 members; RECORD=40. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-1f2390d4e9abaeaa962b58ba`: 1 members; RECORD=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-957415b00f32bef9aa843279`: 5 members; RECORD=5. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-90a69199f6f833ef299fff53`: 11 members; RECORD=11. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-943f02e9d6500fbe5834e870`: 1 members; RECORD=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-e51c7851f5b874ecd9886309`: 1 members; RECORD=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
### unknown

Retained facts do not establish the first applicable question or its required recording line. Missing package integrity, installation defaults, source provenance, or executable content can change the answer. S8.2-6 requires preserving question order; no later guessed class overrides the missing fact.

Manual checks (10 rows):

- `alma-632511e739337dc6b0644fd0`: 6 members; UNKNOWN=6. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-4dd02dba8687552c588796a8`: 24 members; UNKNOWN=24. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-1270e6e8c836b299ab4094f3`: 4 members; UNKNOWN=4. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-88fd59e42e3ab26eeba64167`: 1 members; UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-4640a2de00fbf9fe09cbd5ab`: 1 members; UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-6d9369d3c07f59df59ed3808`: 6 members; UNKNOWN=6. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-6442cc391b3b5f25bf2d09a6`: 2 members; UNKNOWN=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-82fd6b9f155e2f724cfcdfc7`: 1 members; UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-3b373dfde415a87a7e49f99e`: 2 members; UNKNOWN=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-dbdbdb717c357aa3a860df23`: 1 members; UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
### mixed

Evaluate each complete immediate member separately. Emit MIXED when member decisions differ; the exact member partition is recorded below. This is row-by-row composition of the preceding rules, not a classification from the directory name.

Manual checks (10 rows):

- `alma-ba475455b3f546844965345c`: 3 members; RECORD=2, UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-fdaf111e967686c6e21698b2`: 39 members; INSTALLED-PACKAGE=36, UNKNOWN=3. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-f26caad3ce1e91bfa2d45f0b`: 2 members; INSTALLED-PACKAGE=1, UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-2023b790147069a52d36fd1e`: 46 members; INSTALLED-PACKAGE=43, UNKNOWN=3. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-3be9cf7ae131291404a7f544`: 5 members; INSTALLED-PACKAGE=1, UNKNOWN=4. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-cd4a06e2e63eb02b772d7c9f`: 37 members; INSTALLED-PACKAGE=34, UNKNOWN=3. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-ec9c241e8438bc1d56a6d8a9`: 3 members; INSTALLED-PACKAGE=1, UNKNOWN=2. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-84fb246937b4a54db733ab41`: 4 members; INSTALLED-PACKAGE=1, UNKNOWN=3. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-ad8845dcbd762503b9c736bf`: 15 members; INSTALLED-PACKAGE=11, UNKNOWN=4. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.
- `alma-1580186e030a0e0eb14fb8e8`: 2 members; RECORD=1, UNKNOWN=1. Confirmed member types, persistence, and the applicable provenance/format condition against the raw list.

The single sudo rule was evaluated individually: `alma-9b55d85b3e8beb263c1f1957`. The retained content in `raw/0226-metadata-read-0.out` grants passwordless administrative access in a local sudoers fragment, producing SETTING-OWN under S8.2-11–13 and S8.2-17.

## Evidence corrections during this attempt

Initial exact-path joins were replaced by verified filesystem-alias joins before the first output rows. A later documentation pass resolved manual indexes, telemetry archives, logs, and generated Python cache directories previously marked UNKNOWN. Their enclosing mixed groups were recalculated. These are evidence corrections within this attempt, not changes to the definition. Final counts and validation refer to the corrected output.

## Complete member decisions

Member names below are relative to each named group. `$USER_HOME` and `$ROOT_HOME` replace private home-directory prefixes. Each source is the unmodified complete member TSV; no inferred members are added.

### alma-632511e739337dc6b0644fd0

Group: `/boot`. Source: `D1/in/raw/alma/members/632511e739337dc6b0644fd0.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.vmlinuz-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20.hmac`, `initramfs-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20.img`, `initramfs-6.12.0-264.16.1.el10_3.x86_64kdump.img`, `vmlinuz-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `efi`, `loader`. Directory installation integrity and creation provenance are not established.
### alma-660d4708ed5b1e9ce2a99eef

Group: `/boot/efi`. Source: `D1/in/raw/alma/members/660d4708ed5b1e9ce2a99eef.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `EFI`. Directory installation integrity and creation provenance are not established.
### alma-ad9fb12eeb027086dae92d57

Group: `/boot/grub2`. Source: `D1/in/raw/alma/members/ad9fb12eeb027086dae92d57.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `device.map`, `grubenv`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `fonts`, `i386-pc`, `locale`. Directory installation integrity and creation provenance are not established.
### alma-bc541f2fd6f826d2013040f7

Group: `/boot/grub2/fonts`. Source: `D1/in/raw/alma/members/bc541f2fd6f826d2013040f7.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `unicode.pf2`. Package origin, unchangedness, and source of this object are not established.
### alma-11d1bad65ac77ce3ba75e65d

Group: `/boot/grub2/i386-pc`. Source: `D1/in/raw/alma/members/11d1bad65ac77ce3ba75e65d.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `acpi.mod`, `adler32.mod`, `affs.mod`, `afs.mod`, `afsplitter.mod`, `ahci.mod`, `all_video.mod`, `aout.mod`, `archelp.mod`, `asn1.mod`, `at_keyboard.mod`, `ata.mod`, `backtrace.mod`, `bfs.mod`, `biosdisk.mod`, `bitmap.mod`, `bitmap_scale.mod`, `blocklist.mod`, `blscfg.mod`, `boot.img`, `boot.mod`, `bsd.mod`, `bswap_test.mod`, `btrfs.mod`, `bufio.mod`, `cat.mod`, `cbfs.mod`, `cbls.mod`, `cbmemc.mod`, `cbtable.mod`, `cbtime.mod`, `chain.mod`, `cmdline_cat_test.mod`, `cmosdump.mod`, `cmostest.mod`, `cmp.mod`, `cmp_test.mod`, `command.lst`, `configfile.mod`, `core.img`, `cpio.mod`, `cpio_be.mod`, `cpuid.mod`, `crc64.mod`, `crypto.lst`, `crypto.mod`, `cryptodisk.mod`, `cs5536.mod`, `ctz_test.mod`, `date.mod`, `datehook.mod`, `datetime.mod`, `disk.mod`, `diskfilter.mod`, `div.mod`, `div_test.mod`, `dm_nv.mod`, `drivemap.mod`, `dsa_sexp_test.mod`, `echo.mod`, `efiemu.mod`, `ehci.mod`, `elf.mod`, `eval.mod`, `exfat.mod`, `exfctest.mod`, `ext2.mod`, `extcmd.mod`, `f2fs.mod`, `fat.mod`, `file.mod`, `font.mod`, `freedos.mod`, `fs.lst`, `fshelp.mod`, `functional_test.mod`, `gcry_arcfour.mod`, `gcry_aria.mod`, `gcry_blake2.mod`, `gcry_blowfish.mod`, `gcry_camellia.mod`, `gcry_cast5.mod`, `gcry_crc.mod`, `gcry_des.mod`, `gcry_dsa.mod`, `gcry_gost28147.mod`, `gcry_gostr3411_94.mod`, `gcry_idea.mod`, `gcry_keccak.mod`, `gcry_md4.mod`, `gcry_md5.mod`, `gcry_rfc2268.mod`, `gcry_rijndael.mod`, `gcry_rmd160.mod`, `gcry_rsa.mod`, `gcry_salsa20.mod`, `gcry_seed.mod`, `gcry_serpent.mod`, `gcry_sha1.mod`, `gcry_sha256.mod`, `gcry_sha512.mod`, `gcry_sm3.mod`, `gcry_sm4.mod`, `gcry_stribog.mod`, `gcry_tiger.mod`, `gcry_twofish.mod`, `gcry_whirlpool.mod`, `gdb.mod`, `geli.mod`, `gettext.mod`, `gfxmenu.mod`, `gfxterm.mod`, `gfxterm_background.mod`, `gfxterm_menu.mod`, `gptsync.mod`, `gzio.mod`, `halt.mod`, `hashsum.mod`, `hdparm.mod`, `hello.mod`, `help.mod`, `hexdump.mod`, `hfs.mod`, `hfsplus.mod`, `hfspluscomp.mod`, `http.mod`, `increment.mod`, `iorw.mod`, `iso9660.mod`, `jfs.mod`, `jpeg.mod`, `json.mod`, `keylayouts.mod`, `keystatus.mod`, `ldm.mod`, `legacy_password_test.mod`, `legacycfg.mod`, `linux.mod`, `loadenv.mod`, `loopback.mod`, `ls.mod`, `lsacpi.mod`, `lsapm.mod`, `lsmmap.mod`, `lspci.mod`, `luks.mod`, `luks2.mod`, `lvm.mod`, `lzopio.mod`, `macbless.mod`, `macho.mod`, `mda_text.mod`, `mdraid09.mod`, `mdraid09_be.mod`, `mdraid1x.mod`, `memdisk.mod`, `memrw.mod`, `minicmd.mod`, `minix.mod`, `minix2.mod`, `minix2_be.mod`, `minix3.mod`, `minix3_be.mod`, `minix_be.mod`, `mmap.mod`, `moddep.lst`, `modinfo.sh`, `morse.mod`, `mpi.mod`, `msdospart.mod`, `mul_test.mod`, `multiboot.mod`, `multiboot2.mod`, `nativedisk.mod`, `net.mod`, `newc.mod`, `nilfs2.mod`, `normal.mod`, `ntfs.mod`, `ntfscomp.mod`, `ntldr.mod`, `odc.mod`, `offsetio.mod`, `ohci.mod`, `part_acorn.mod`, `part_amiga.mod`, `part_apple.mod`, `part_bsd.mod`, `part_dfly.mod`, `part_dvh.mod`, `part_gpt.mod`, `part_msdos.mod`, `part_plan.mod`, `part_sun.mod`, `part_sunpc.mod`, `partmap.lst`, `parttool.lst`, `parttool.mod`, `password.mod`, `password_pbkdf2.mod`, `pata.mod`, `pbkdf2.mod`, `pbkdf2_test.mod`, `pci.mod`, `pcidump.mod`, `pgp.mod`, `plainmount.mod`, `plan9.mod`, `play.mod`, `png.mod`, `priority_queue.mod`, `probe.mod`, `procfs.mod`, `progress.mod`, `pubkey.mod`, `pxe.mod`, `pxechain.mod`, `raid5rec.mod`, `raid6rec.mod`, `random.mod`, `rdmsr.mod`, `read.mod`, `reboot.mod`, `regexp.mod`, `reiserfs.mod`, `relocator.mod`, `romfs.mod`, `rsa_sexp_test.mod`, `scsi.mod`, `search.mod`, `search_fs_file.mod`, `search_fs_uuid.mod`, `search_label.mod`, `sendkey.mod`, `serial.mod`, `setjmp.mod`, `setjmp_test.mod`, `setpci.mod`, `sfs.mod`, `shift_test.mod`, `signature_test.mod`, `sleep.mod`, `sleep_test.mod`, `smbios.mod`, `spkmodem.mod`, `squash4.mod`, `strtoull_test.mod`, `syslinuxcfg.mod`, `tar.mod`, `terminal.lst`, `terminal.mod`, `terminfo.mod`, `test.mod`, `test_asn1.mod`, `test_blockarg.mod`, `testload.mod`, `testspeed.mod`, `tftp.mod`, `tga.mod`, `time.mod`, `tr.mod`, `trig.mod`, `true.mod`, `truecrypt.mod`, `udf.mod`, `ufs1.mod`, `ufs1_be.mod`, `ufs2.mod`, `uhci.mod`, `usb.mod`, `usb_keyboard.mod`, `usbms.mod`, `usbserial_common.mod`, `usbserial_ftdi.mod`, `usbserial_pl2303.mod`, `usbserial_usbdebug.mod`, `usbtest.mod`, `vbe.mod`, `version.mod`, `vga.mod`, `vga_text.mod`, `video.lst`, `video.mod`, `video_bochs.mod`, `video_cirrus.mod`, `video_colors.mod`, `video_fb.mod`, `videoinfo.mod`, `videotest.mod`, `videotest_checksum.mod`, `wrmsr.mod`, `xfs.mod`, `xnu.mod`, `xnu_uuid.mod`, `xnu_uuid_test.mod`, `xzio.mod`, `zfs.mod`, `zfscrypt.mod`, `zfsinfo.mod`, `zstd.mod`. Package origin, unchangedness, and source of this object are not established.
### alma-8950265a4290e71ab392f077

Group: `/boot/grub2/locale`. Source: `D1/in/raw/alma/members/8950265a4290e71ab392f077.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `ast.mo`, `ca.mo`, `da.mo`, `de.mo`, `<REDACTED>`, `de_CH.mo`, `<REDACTED>`, `<REDACTED>`, `<REDACTED>`, `<REDACTED>`, `<REDACTED>`, `<REDACTED>`, `eo.mo`, `es.mo`, `fi.mo`, `fr.mo`, `gl.mo`, `he.mo`, `hr.mo`, `hu.mo`, `id.mo`, `it.mo`, `ja.mo`, `ka.mo`, `ko.mo`, `lg.mo`, `lt.mo`, `nb.mo`, `nl.mo`, `pa.mo`, `pl.mo`, `pt.mo`, `pt_BR.mo`, `ro.mo`, `ru.mo`, `sl.mo`, `sr.mo`, `sv.mo`, `tr.mo`, `uk.mo`, `vi.mo`, `zh_CN.mo`, `zh_TW.mo`. Package origin, unchangedness, and source of this object are not established.
### alma-89527f1e1cad2288da20c659

Group: `/boot/loader`. Source: `D1/in/raw/alma/members/89527f1e1cad2288da20c659.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `entries`. Directory installation integrity and creation provenance are not established.
### alma-5bafee22bc69b6fb7e9b4c37

Group: `/boot/loader/entries`. Source: `D1/in/raw/alma/members/5bafee22bc69b6fb7e9b4c37.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `8ef0d28cd1cb4a80b9baa123cb63ef20-0-rescue.conf`, `8ef0d28cd1cb4a80b9baa123cb63ef20-6.12.0-264.16.1.el10_3.x86_64.conf`. Package origin, unchangedness, and source of this object are not established.
### alma-81280a382ce7c18f1fe7dadb

Group: `/etc`. Source: `D1/in/raw/alma/members/81280a382ce7c18f1fe7dadb.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.pwd.lock`, `.updated`, `group-`, `gshadow-`, `passwd-`, `resolv.conf`, `shadow-`, `subgid-`, `subuid-`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `debuginfod`, `dhcp`, `gnome-remote-desktop`, `ras`, `sos`, `yum`. Directory installation integrity and creation provenance are not established.
### alma-692bae3e82cf4ace35cbce54

Group: `/etc/NetworkManager/system-connections`. Source: `D1/in/raw/alma/members/692bae3e82cf4ace35cbce54.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cal-secondary.nmconnection`, `cal-test.nmconnection`, `ens3.nmconnection`. Package origin, unchangedness, and source of this object are not established.
### alma-3faecf03fe13bf74cff2bea1

Group: `/etc/X11`. Source: `D1/in/raw/alma/members/3faecf03fe13bf74cff2bea1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `Xsession.d`, `xorg.conf.d`. Directory installation integrity and creation provenance are not established.
### alma-c3d63fb0d3d8e06ed8a8e0b5

Group: `/etc/alsa`. Source: `D1/in/raw/alma/members/c3d63fb0d3d8e06ed8a8e0b5.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `conf.d`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `state-daemon.conf`. Package origin, unchangedness, and source of this object are not established.
### alma-9a2b3f5598419c41bbb752af

Group: `/etc/alternatives`. Source: `D1/in/raw/alma/members/9a2b3f5598419c41bbb752af.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `apropos`, `apropos.1.gz`, `arptables`, `arptables-helper`, `arptables-man`, `arptables-restore`, `arptables-restore-man`, `arptables-save`, `arptables-save-man`, `cifs-idmap-plugin`, `ebtables`, `ebtables-man`, `ebtables-restore`, `ebtables-save`, `ip6tables`, `ip6tables-restore`, `ip6tables-save`, `iptables`, `iptables-restore`, `iptables-save`, `ld`, `libnssckbi.so.x86_64`, `man`, `man.1.gz`, `man.7.gz`, `nc`, `nc-man`, `print`, `print-cancel`, `print-cancelman`, `print-lp`, `print-lpc`, `print-lpcman`, `print-lpman`, `print-lpq`, `print-lpqman`, `print-lprm`, `print-lprman`, `print-lprmman`, `print-lpstat`, `print-lpstatman`, `soelim`, `soelim.1.gz`, `whatis`, `whatis.1.gz`. Package origin, unchangedness, and source of this object are not established.
### alma-3e5f5dbee6de8563eff59b1c

Group: `/etc/authselect`. Source: `D1/in/raw/alma/members/3e5f5dbee6de8563eff59b1c.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `switchable-auth`. Package origin, unchangedness, and source of this object are not established.
### alma-bb6ecb6aa8b2ecb79575617f

Group: `/etc/cups`. Source: `D1/in/raw/alma/members/bb6ecb6aa8b2ecb79575617f.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cups-browsed.conf.rpmsave`. Package origin, unchangedness, and source of this object are not established.
### alma-caff428f8364f0a663721a85

Group: `/etc/dconf/db`. Source: `D1/in/raw/alma/members/caff428f8364f0a663721a85.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `distro`, `gdm`, `ibus`, `local`, `site`. Package origin, unchangedness, and source of this object are not established.
### alma-a2a4dad76ebf3ae13a87aecb

Group: `/etc/dconf/db/distro.d`. Source: `D1/in/raw/alma/members/a2a4dad76ebf3ae13a87aecb.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `20-authselect`. Package origin, unchangedness, and source of this object are not established.
### alma-dd368a47812a0e1fb4525ca8

Group: `/etc/dconf/db/distro.d/locks`. Source: `D1/in/raw/alma/members/dd368a47812a0e1fb4525ca8.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `20-authselect`. Package origin, unchangedness, and source of this object are not established.
### alma-102682307f251c9815e9cdac

Group: `/etc/dhcp`. Source: `D1/in/raw/alma/members/102682307f251c9815e9cdac.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `dhclient.d`. Directory installation integrity and creation provenance are not established.
### alma-dab39645202d97d80dcf72f3

Group: `/etc/firewalld/zones`. Source: `D1/in/raw/alma/members/dab39645202d97d80dcf72f3.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `public.xml`, `public.xml.old`. Package origin, unchangedness, and source of this object are not established.
### alma-383dc4644881a5acdc97817a

Group: `/etc/grub.d`. Source: `D1/in/raw/alma/members/383dc4644881a5acdc97817a.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `00_tuned`. Package origin, unchangedness, and source of this object are not established.
### alma-894535cc1ce55c243421555b

Group: `/etc/kernel`. Source: `D1/in/raw/alma/members/894535cc1ce55c243421555b.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cmdline`. Package origin, unchangedness, and source of this object are not established.
### alma-99e9f883f52f6901cdd9040e

Group: `/etc/libblockdev`. Source: `D1/in/raw/alma/members/99e9f883f52f6901cdd9040e.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `3`. Directory installation integrity and creation provenance are not established.
### alma-2a50078297142eb5d683cdc6

Group: `/etc/lvm/archive`. Source: `D1/in/raw/alma/members/2a50078297142eb5d683cdc6.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `almalinux_00000-594443534.vg`. Package origin, unchangedness, and source of this object are not established.
### alma-225e2fad4968c7f2c24682ed

Group: `/etc/lvm/backup`. Source: `D1/in/raw/alma/members/225e2fad4968c7f2c24682ed.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `almalinux`. Package origin, unchangedness, and source of this object are not established.
### alma-fa482ac6a10c184944b225d2

Group: `/etc/lvm/devices`. Source: `D1/in/raw/alma/members/fa482ac6a10c184944b225d2.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `backup`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `system.devices`. Package origin, unchangedness, and source of this object are not established.
### alma-2ca64402cce58966f6f02ba7

Group: `/etc/lvm/devices/backup`. Source: `D1/in/raw/alma/members/2ca64402cce58966f6f02ba7.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `system.devices-20261123.111630.0005`, `system.devices-20261123.111633.0006`. Package origin, unchangedness, and source of this object are not established.
### alma-7418f2844ccd58f8ba49aa78

Group: `/etc/nvme`. Source: `D1/in/raw/alma/members/7418f2844ccd58f8ba49aa78.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `hostid`, `hostnqn`. Package origin, unchangedness, and source of this object are not established.
### alma-8810b72f9d5f224b1ec48e9d

Group: `/etc/pam.d`. Source: `D1/in/raw/alma/members/8810b72f9d5f224b1ec48e9d.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `switchable-auth`. Package origin, unchangedness, and source of this object are not established.
### alma-894c85b754848823e3688b91

Group: `/etc/pki`. Source: `D1/in/raw/alma/members/894c85b754848823e3688b91.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `sigstore`. Directory installation integrity and creation provenance are not established.
### alma-a6c48f5b5b8714cffd1e996f

Group: `/etc/pki/ca-trust/extracted`. Source: `D1/in/raw/alma/members/a6c48f5b5b8714cffd1e996f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `edk2`. Directory installation integrity and creation provenance are not established.
### alma-662a712e065589640e0503d3

Group: `/etc/ssh`. Source: `D1/in/raw/alma/members/662a712e065589640e0503d3.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `ssh_host_ecdsa_key`, `ssh_host_ecdsa_key.pub`, `ssh_host_ed25519_key`, `ssh_host_ed25519_key.pub`, `ssh_host_rsa_key`, `ssh_host_rsa_key.pub`. Package origin, unchangedness, and source of this object are not established.
### alma-9b55d85b3e8beb263c1f1957

Group: `/etc/sudoers.d`. Source: `D1/in/raw/alma/members/9b55d85b3e8beb263c1f1957.tsv`. Decision: **SETTING-OWN**.

Captured local rule grants access to this computer and requires its own line.

- **SETTING-OWN**: `lab-access`. Captured sudo access rule is locally selected and not a packaged default.
### alma-babf6a10543af22e535e0c4e

Group: `/etc/sysconfig`. Source: `D1/in/raw/alma/members/babf6a10543af22e535e0c4e.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `anaconda`, `kernel`, `network`. Package origin, unchangedness, and source of this object are not established.
### alma-a2270b7bf27cfa5baec1d6a2

Group: `/etc/systemd/system`. Source: `D1/in/raw/alma/members/a2270b7bf27cfa5baec1d6a2.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `ctrl-alt-del.target`, `dbus-org.bluez.service`, `dbus-org.fedoraproject.FirewallD1.service`, `dbus-org.freedesktop.Avahi.service`, `dbus-org.freedesktop.ModemManager1.service`, `dbus-org.freedesktop.nm-dispatcher.service`, `dbus.service`, `default.target`, `display-manager.service`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `dev-virtio\x2dports-org.qemu.guest_agent.0.device.wants`, `vmtoolsd.service.requires`. Directory installation integrity and creation provenance are not established.
### alma-e4dd63f73ebe8ee244c10cd4

Group: `/etc/systemd/system/bluetooth.target.wants`. Source: `D1/in/raw/alma/members/e4dd63f73ebe8ee244c10cd4.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `bluetooth.service`. Package origin, unchangedness, and source of this object are not established.
### alma-3d942f05d6c68541a4a01fd0

Group: `/etc/systemd/system/default.target.wants`. Source: `D1/in/raw/alma/members/3d942f05d6c68541a4a01fd0.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `nvmefc-boot-connections.service`. Package origin, unchangedness, and source of this object are not established.
### alma-cda3bd4c76727ccc7f8b2075

Group: `/etc/systemd/system/dev-virtio\x2dports-org.qemu.guest_agent.0.device.wants`. Source: `D1/in/raw/alma/members/cda3bd4c76727ccc7f8b2075.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `qemu-guest-agent.service`. Package origin, unchangedness, and source of this object are not established.
### alma-9768e905983c68d58ca911fa

Group: `/etc/systemd/system/getty.target.wants`. Source: `D1/in/raw/alma/members/9768e905983c68d58ca911fa.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `getty@tty1.service`. Package origin, unchangedness, and source of this object are not established.
### alma-2b25403fe7f9aed63ba0c09f

Group: `/etc/systemd/system/graphical.target.wants`. Source: `D1/in/raw/alma/members/2b25403fe7f9aed63ba0c09f.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `accounts-daemon.service`, `rtkit-daemon.service`, `switcheroo-control.service`, `tuned-ppd.service`, `udisks2.service`, `upower.service`. Package origin, unchangedness, and source of this object are not established.
### alma-4dd02dba8687552c588796a8

Group: `/etc/systemd/system/multi-user.target.wants`. Source: `D1/in/raw/alma/members/4dd02dba8687552c588796a8.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `ModemManager.service`, `NetworkManager.service`, `atd.service`, `audit-rules.service`, `auditd.service`, `avahi-daemon.service`, `chronyd.service`, `crond.service`, `cups.path`, `cups.service`, `firewalld.service`, `irqbalance.service`, `kdump.service`, `libstoragemgmt.service`, `mcelog.service`, `mdmonitor.service`, `remote-cryptsetup.target`, `remote-fs.target`, `rsyslog.service`, `smartd.service`, `sshd.service`, `sssd.service`, `tuned.service`, `vmtoolsd.service`. Package origin, unchangedness, and source of this object are not established.
### alma-a96808a86f1e0fb361771993

Group: `/etc/systemd/system/network-online.target.wants`. Source: `D1/in/raw/alma/members/a96808a86f1e0fb361771993.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `NetworkManager-wait-online.service`. Package origin, unchangedness, and source of this object are not established.
### alma-3db47f2d028b13951a2873b0

Group: `/etc/systemd/system/printer.target.wants`. Source: `D1/in/raw/alma/members/3db47f2d028b13951a2873b0.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `cups.service`. Package origin, unchangedness, and source of this object are not established.
### alma-7753d30a8947c87d83d747be

Group: `/etc/systemd/system/sockets.target.wants`. Source: `D1/in/raw/alma/members/7753d30a8947c87d83d747be.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `avahi-daemon.socket`, `cockpit.socket`, `cups.socket`, `dbus.socket`, `dm-event.socket`, `iscsid.socket`, `iscsiuio.socket`, `sssd-kcm.socket`, `systemd-userdbd.socket`. Package origin, unchangedness, and source of this object are not established.
### alma-1d1874a6f4d7da7582cc38a9

Group: `/etc/systemd/system/sysinit.target.wants`. Source: `D1/in/raw/alma/members/1d1874a6f4d7da7582cc38a9.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `fips-crypto-policy-overlay.service`, `iscsi-onboot.service`, `iscsi-starter.service`, `lvm2-lvmpolld.socket`, `lvm2-monitor.service`, `multipathd.service`, `selinux-autorelabel-mark.service`, `systemd-confext.service`, `systemd-network-generator.service`, `systemd-pstore.service`, `systemd-sysext.service`. Package origin, unchangedness, and source of this object are not established.
### alma-2598e57f0f6bff95725398e9

Group: `/etc/systemd/system/timers.target.wants`. Source: `D1/in/raw/alma/members/2598e57f0f6bff95725398e9.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `dnf-makecache.timer`, `fstrim.timer`, `fwupd-refresh.timer`, `logrotate.timer`, `plocate-updatedb.timer`, `raid-check.timer`. Package origin, unchangedness, and source of this object are not established.
### alma-1e33fe58f57b8be4bcbaadc4

Group: `/etc/systemd/system/vmtoolsd.service.requires`. Source: `D1/in/raw/alma/members/1e33fe58f57b8be4bcbaadc4.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `vgauthd.service`. Package origin, unchangedness, and source of this object are not established.
### alma-b9f1455d007149f01ba5d60c

Group: `/etc/systemd/user`. Source: `D1/in/raw/alma/members/b9f1455d007149f01ba5d60c.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `basic.target.wants`, `graphical-session-pre.target.wants`, `pipewire.service.wants`, `sockets.target.wants`, `timers.target.wants`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `dbus-org.bluez.obex.service`, `dbus.service`, `pipewire-session-manager.service`. Package origin, unchangedness, and source of this object are not established.
### alma-a744ef402acb5488caa508bf

Group: `/etc/systemd/user/basic.target.wants`. Source: `D1/in/raw/alma/members/a744ef402acb5488caa508bf.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `systemd-tmpfiles-setup.service`. Package origin, unchangedness, and source of this object are not established.
### alma-f18b12c328db39d35ad18d45

Group: `/etc/systemd/user/graphical-session-pre.target.wants`. Source: `D1/in/raw/alma/members/f18b12c328db39d35ad18d45.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `xdg-user-dirs.service`. Package origin, unchangedness, and source of this object are not established.
### alma-49c961709e8dcebf4ceccf17

Group: `/etc/systemd/user/pipewire.service.wants`. Source: `D1/in/raw/alma/members/49c961709e8dcebf4ceccf17.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `wireplumber.service`. Package origin, unchangedness, and source of this object are not established.
### alma-130bd3c32242f60379fad449

Group: `/etc/systemd/user/sockets.target.wants`. Source: `D1/in/raw/alma/members/130bd3c32242f60379fad449.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `dbus.socket`, `pipewire-pulse.socket`, `pipewire.socket`. Package origin, unchangedness, and source of this object are not established.
### alma-3af62683b9237d855355a021

Group: `/etc/systemd/user/timers.target.wants`. Source: `D1/in/raw/alma/members/3af62683b9237d855355a021.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `grub-boot-success.timer`, `systemd-tmpfiles-clean.timer`. Package origin, unchangedness, and source of this object are not established.
### alma-30028a0ec3da85d9ce761204

Group: `/etc/xdg`. Source: `D1/in/raw/alma/members/30028a0ec3da85d9ce761204.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `menus`. Directory installation integrity and creation provenance are not established.
### alma-99b8115befb7a596a3a89033

Group: `/home`. Source: `D1/in/raw/alma/members/99b8115befb7a596a3a89033.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `$USER_HOME`. Directory installation integrity and creation provenance are not established.
### alma-825ccda13415099cb2fa6040

Group: `$USER_HOME`. Source: `D1/in/raw/alma/members/825ccda13415099cb2fa6040.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.bash_logout`, `.bash_profile`, `.bashrc`, `.gitconfig`, `cal-user-script.log`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `.cache`, `.config`, `.local`, `.mozilla`, `.npm`, `.ssh`, `Downloads`. Directory installation integrity and creation provenance are not established.
### alma-ba475455b3f546844965345c

Group: `$USER_HOME/.cache`. Source: `D1/in/raw/alma/members/ba475455b3f546844965345c.tsv`. Decision: **MIXED**.

RECORD: fontconfig,pip; UNKNOWN: mozilla

- **RECORD**: `fontconfig`. Generated font lookup cache or its directory.
- **UNKNOWN**: `mozilla`. Directory installation integrity and creation provenance are not established.
- **RECORD**: `pip`. Pip HTTP cache or cache directory, stored as working data.
### alma-d15f2f63f27850d00f28f708

Group: `$USER_HOME/.cache/fontconfig`. Source: `D1/in/raw/alma/members/d15f2f63f27850d00f28f708.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `477ff6b974c3c1b81af411ebecb34280-le64.cache-9`, `CACHEDIR.TAG`. Generated font lookup cache or its directory.
### alma-7d5511cf9b8535fc8442a7f5

Group: `$USER_HOME/.cache/mozilla`. Source: `D1/in/raw/alma/members/7d5511cf9b8535fc8442a7f5.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `firefox`. Directory installation integrity and creation provenance are not established.
### alma-d22358159be5e809adf3f1d9

Group: `$USER_HOME/.cache/mozilla/firefox`. Source: `D1/in/raw/alma/members/d22358159be5e809adf3f1d9.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cal-check`. Directory installation integrity and creation provenance are not established.
### alma-3068a3c43224e9c76e972eb1

Group: `$USER_HOME/.cache/mozilla/firefox/cal-check`. Source: `D1/in/raw/alma/members/3068a3c43224e9c76e972eb1.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `activity-stream.shortcut_cache.json`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `cache2`, `safebrowsing`, `startupCache`, `thumbnails`. Directory installation integrity and creation provenance are not established.
### alma-ddc1f12633f0b3c7fcabeded

Group: `$USER_HOME/.cache/mozilla/firefox/cal-check/cache2`. Source: `D1/in/raw/alma/members/ddc1f12633f0b3c7fcabeded.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `ce_T151c2VyQ29udGV4dElkPTUs`, `ce_T151c2VyQ29udGV4dElkPTUsYSw=`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `doomed`, `entries`. Directory installation integrity and creation provenance are not established.
### alma-740880f4cd0b3686e3f4650a

Group: `$USER_HOME/.cache/mozilla/firefox/cal-check/cache2/entries`. Source: `D1/in/raw/alma/members/740880f4cd0b3686e3f4650a.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `3E840EE2DA4DBE23E48492A94C30958D16834758`, `40D6B93D1B8D8F55EAB18B4C54872B17F2647D64`. Package origin, unchangedness, and source of this object are not established.
### alma-02565ed2145d532039503ede

Group: `$USER_HOME/.cache/mozilla/firefox/cal-check/startupCache`. Source: `D1/in/raw/alma/members/02565ed2145d532039503ede.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `scriptCache-child.bin`, `scriptCache.bin`, `startupCache.8.little`, `urlCache.bin`, `webext.sc.lz4`. Package origin, unchangedness, and source of this object are not established.
### alma-517a823b6b324a754d5a5086

Group: `$USER_HOME/.cache/pip`. Source: `D1/in/raw/alma/members/517a823b6b324a754d5a5086.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `http-v2`, `selfcheck`, `wheels`. Pip HTTP cache or cache directory, stored as working data.
### alma-1924e7e7c98621387285db92

Group: `$USER_HOME/.cache/pip/http-v2`. Source: `D1/in/raw/alma/members/1924e7e7c98621387285db92.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `a`, `b`, `c`, `d`, `e`, `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-b9b4b8c91977006577657ff1

Group: `$USER_HOME/.cache/pip/http-v2/0`. Source: `D1/in/raw/alma/members/b9b4b8c91977006577657ff1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`, `c`, `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-670e2bf2f8895faaa8f70c45

Group: `$USER_HOME/.cache/pip/http-v2/0/4`. Source: `D1/in/raw/alma/members/670e2bf2f8895faaa8f70c45.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-d709af35da485ba1346c3ffc

Group: `$USER_HOME/.cache/pip/http-v2/0/4/1`. Source: `D1/in/raw/alma/members/d709af35da485ba1346c3ffc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-1b41d0db54489978b3d9cb73

Group: `$USER_HOME/.cache/pip/http-v2/0/4/1/8`. Source: `D1/in/raw/alma/members/1b41d0db54489978b3d9cb73.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-9bd3f1f0e6faf8a2762fa31d

Group: `$USER_HOME/.cache/pip/http-v2/0/4/1/8/c`. Source: `D1/in/raw/alma/members/9bd3f1f0e6faf8a2762fa31d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0418c83b80f7f7bfaec2738bfbbee53d2c1562196c0781702f6eddc8`, `0418c83b80f7f7bfaec2738bfbbee53d2c1562196c0781702f6eddc8.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-d59d38be34c6edfd24322440

Group: `$USER_HOME/.cache/pip/http-v2/0/c`. Source: `D1/in/raw/alma/members/d59d38be34c6edfd24322440.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-7a0bb545aae1e5acef09f882

Group: `$USER_HOME/.cache/pip/http-v2/0/c/5`. Source: `D1/in/raw/alma/members/7a0bb545aae1e5acef09f882.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-8d3f4b902285c3bc5b911005

Group: `$USER_HOME/.cache/pip/http-v2/0/c/5/a`. Source: `D1/in/raw/alma/members/8d3f4b902285c3bc5b911005.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-39fe94e514b97de160e14323

Group: `$USER_HOME/.cache/pip/http-v2/0/c/5/a/b`. Source: `D1/in/raw/alma/members/39fe94e514b97de160e14323.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0c5abfdef47a2a10a9b2220f281d462aab95a80f6a99faa466f44cbf`, `0c5abfdef47a2a10a9b2220f281d462aab95a80f6a99faa466f44cbf.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-539e7541ff985559b7ea073a

Group: `$USER_HOME/.cache/pip/http-v2/0/e`. Source: `D1/in/raw/alma/members/539e7541ff985559b7ea073a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-ac3a61b218888cb2b1659cf2

Group: `$USER_HOME/.cache/pip/http-v2/0/e/6`. Source: `D1/in/raw/alma/members/ac3a61b218888cb2b1659cf2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-a60c2dc8830e7d2550a8c2da

Group: `$USER_HOME/.cache/pip/http-v2/0/e/6/9`. Source: `D1/in/raw/alma/members/a60c2dc8830e7d2550a8c2da.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-5c8d29d5e5b293b555282b90

Group: `$USER_HOME/.cache/pip/http-v2/0/e/6/9/9`. Source: `D1/in/raw/alma/members/5c8d29d5e5b293b555282b90.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0e6995b77e300dcc4018aee3726e876dd8034c43dad301a6895623ba`, `0e6995b77e300dcc4018aee3726e876dd8034c43dad301a6895623ba.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-5facd97ecb981140b085c0b3

Group: `$USER_HOME/.cache/pip/http-v2/1`. Source: `D1/in/raw/alma/members/5facd97ecb981140b085c0b3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`, `4`, `8`, `9`, `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-84ddd101f4308d91b7225aa5

Group: `$USER_HOME/.cache/pip/http-v2/1/3`. Source: `D1/in/raw/alma/members/84ddd101f4308d91b7225aa5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-3a674ecabf76de52e6cf48af

Group: `$USER_HOME/.cache/pip/http-v2/1/3/8`. Source: `D1/in/raw/alma/members/3a674ecabf76de52e6cf48af.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-c4131b56d91c7928886db4cb

Group: `$USER_HOME/.cache/pip/http-v2/1/3/8/4`. Source: `D1/in/raw/alma/members/c4131b56d91c7928886db4cb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-98b9ba18b48c38dce7fee280

Group: `$USER_HOME/.cache/pip/http-v2/1/3/8/4/e`. Source: `D1/in/raw/alma/members/98b9ba18b48c38dce7fee280.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1384e7b9879ef03c2fa3be03a098c44d8a8544a63c11c82a86ab7fc3`, `1384e7b9879ef03c2fa3be03a098c44d8a8544a63c11c82a86ab7fc3.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-d7e736571f001362d0234dd4

Group: `$USER_HOME/.cache/pip/http-v2/1/4`. Source: `D1/in/raw/alma/members/d7e736571f001362d0234dd4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-f306468c15432d086e258ea6

Group: `$USER_HOME/.cache/pip/http-v2/1/4/e`. Source: `D1/in/raw/alma/members/f306468c15432d086e258ea6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-ed6e9723c875d42cdbd1aab6

Group: `$USER_HOME/.cache/pip/http-v2/1/4/e/a`. Source: `D1/in/raw/alma/members/ed6e9723c875d42cdbd1aab6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-8de7347a02a87632c4ef72f4

Group: `$USER_HOME/.cache/pip/http-v2/1/4/e/a/2`. Source: `D1/in/raw/alma/members/8de7347a02a87632c4ef72f4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `14ea2de2df224b55ec7a93d8eb7d2d0ec512fc522397347c471bede7`, `14ea2de2df224b55ec7a93d8eb7d2d0ec512fc522397347c471bede7.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-add3f7dde4ebc6e17d3abff2

Group: `$USER_HOME/.cache/pip/http-v2/1/8`. Source: `D1/in/raw/alma/members/add3f7dde4ebc6e17d3abff2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-741abd03a4e9f3c9bc67f19b

Group: `$USER_HOME/.cache/pip/http-v2/1/8/3`. Source: `D1/in/raw/alma/members/741abd03a4e9f3c9bc67f19b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-c6cac082147f8541376900f3

Group: `$USER_HOME/.cache/pip/http-v2/1/8/3/9`. Source: `D1/in/raw/alma/members/c6cac082147f8541376900f3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-287954d7986f9463a1d03ac8

Group: `$USER_HOME/.cache/pip/http-v2/1/8/3/9/9`. Source: `D1/in/raw/alma/members/287954d7986f9463a1d03ac8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1839911afa3a298741e207e7e99aea7177030d328debd377548f19e2`, `1839911afa3a298741e207e7e99aea7177030d328debd377548f19e2.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-ae4c564cc353de72678c59eb

Group: `$USER_HOME/.cache/pip/http-v2/1/9`. Source: `D1/in/raw/alma/members/ae4c564cc353de72678c59eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-6e3d2c61b244234704a18358

Group: `$USER_HOME/.cache/pip/http-v2/1/9/f`. Source: `D1/in/raw/alma/members/6e3d2c61b244234704a18358.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-f6cc220a8713fb4ac0d74e81

Group: `$USER_HOME/.cache/pip/http-v2/1/9/f/8`. Source: `D1/in/raw/alma/members/f6cc220a8713fb4ac0d74e81.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-0ccb7d47453f51c021b66883

Group: `$USER_HOME/.cache/pip/http-v2/1/9/f/8/1`. Source: `D1/in/raw/alma/members/0ccb7d47453f51c021b66883.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `19f8155a88a162a61d22fdb90d0a20701e8d83fbf1706cb1ca590cba`, `19f8155a88a162a61d22fdb90d0a20701e8d83fbf1706cb1ca590cba.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-9530f8103264867a5aca9672

Group: `$USER_HOME/.cache/pip/http-v2/1/b`. Source: `D1/in/raw/alma/members/9530f8103264867a5aca9672.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-4e018487c0e353c3690dd2f3

Group: `$USER_HOME/.cache/pip/http-v2/1/b/2`. Source: `D1/in/raw/alma/members/4e018487c0e353c3690dd2f3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-c1faf2713ce80c3fcce77f9d

Group: `$USER_HOME/.cache/pip/http-v2/1/b/2/b`. Source: `D1/in/raw/alma/members/c1faf2713ce80c3fcce77f9d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-231b41b673027c1e5ed947dd

Group: `$USER_HOME/.cache/pip/http-v2/1/b/2/b/c`. Source: `D1/in/raw/alma/members/231b41b673027c1e5ed947dd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1b2bc31cab0d2dfd0efbcf66a3ec3068e9b379a272895890c7c0e704`, `1b2bc31cab0d2dfd0efbcf66a3ec3068e9b379a272895890c7c0e704.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-aeb131c0c1305b77ad353738

Group: `$USER_HOME/.cache/pip/http-v2/2`. Source: `D1/in/raw/alma/members/aeb131c0c1305b77ad353738.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`, `8`, `b`, `c`, `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-e172e9e1350961e2dd3ae965

Group: `$USER_HOME/.cache/pip/http-v2/2/1`. Source: `D1/in/raw/alma/members/e172e9e1350961e2dd3ae965.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-97af1e6319873d68a3d1e493

Group: `$USER_HOME/.cache/pip/http-v2/2/1/f`. Source: `D1/in/raw/alma/members/97af1e6319873d68a3d1e493.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-e7deff3d4f470f68845b9576

Group: `$USER_HOME/.cache/pip/http-v2/2/1/f/4`. Source: `D1/in/raw/alma/members/e7deff3d4f470f68845b9576.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-7e1a780f30599d0a93ec8d15

Group: `$USER_HOME/.cache/pip/http-v2/2/1/f/4/e`. Source: `D1/in/raw/alma/members/7e1a780f30599d0a93ec8d15.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `21f4e9712e111d761a92e0d31a824b7bd46764eb93957670628c9f84`, `21f4e9712e111d761a92e0d31a824b7bd46764eb93957670628c9f84.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-dcf033b7880be5ebaf8f0cfe

Group: `$USER_HOME/.cache/pip/http-v2/2/8`. Source: `D1/in/raw/alma/members/dcf033b7880be5ebaf8f0cfe.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-f1dd1356d91e32cc05fd077c

Group: `$USER_HOME/.cache/pip/http-v2/2/8/9`. Source: `D1/in/raw/alma/members/f1dd1356d91e32cc05fd077c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-95452ab13c3e069a90af65ac

Group: `$USER_HOME/.cache/pip/http-v2/2/8/9/9`. Source: `D1/in/raw/alma/members/95452ab13c3e069a90af65ac.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-a9ddf948178ad341c729c345

Group: `$USER_HOME/.cache/pip/http-v2/2/8/9/9/0`. Source: `D1/in/raw/alma/members/a9ddf948178ad341c729c345.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2899045923bb0d4f280237e0cd659bbb1f118078474438fc8f50a5c9`, `2899045923bb0d4f280237e0cd659bbb1f118078474438fc8f50a5c9.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-ab885afc9a88a0394904fdf7

Group: `$USER_HOME/.cache/pip/http-v2/2/b`. Source: `D1/in/raw/alma/members/ab885afc9a88a0394904fdf7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-0ad93e401fa7864ba302f44e

Group: `$USER_HOME/.cache/pip/http-v2/2/b/7`. Source: `D1/in/raw/alma/members/0ad93e401fa7864ba302f44e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-9c12c6f0acc0b7fe2482e948

Group: `$USER_HOME/.cache/pip/http-v2/2/b/7/d`. Source: `D1/in/raw/alma/members/9c12c6f0acc0b7fe2482e948.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-ab49825d1a57fb4ecf0ba5bb

Group: `$USER_HOME/.cache/pip/http-v2/2/b/7/d/2`. Source: `D1/in/raw/alma/members/ab49825d1a57fb4ecf0ba5bb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2b7d2ea23f374f5a061cfe65040e5bcedebb00a8114faf60e4033096`, `2b7d2ea23f374f5a061cfe65040e5bcedebb00a8114faf60e4033096.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-05360a29e79cd10fd9e1cbb4

Group: `$USER_HOME/.cache/pip/http-v2/2/c`. Source: `D1/in/raw/alma/members/05360a29e79cd10fd9e1cbb4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-635697d30c4e1ecc503fb847

Group: `$USER_HOME/.cache/pip/http-v2/2/c/b`. Source: `D1/in/raw/alma/members/635697d30c4e1ecc503fb847.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-4d99c5566e233274c8631c2a

Group: `$USER_HOME/.cache/pip/http-v2/2/c/b/3`. Source: `D1/in/raw/alma/members/4d99c5566e233274c8631c2a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-dc8374b064563defa3501e26

Group: `$USER_HOME/.cache/pip/http-v2/2/c/b/3/5`. Source: `D1/in/raw/alma/members/dc8374b064563defa3501e26.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2cb350e763685ae808790082a2895451048254d495f9f802e3a850a7`, `2cb350e763685ae808790082a2895451048254d495f9f802e3a850a7.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-da94b6718e1f3d6aed505740

Group: `$USER_HOME/.cache/pip/http-v2/2/e`. Source: `D1/in/raw/alma/members/da94b6718e1f3d6aed505740.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-1a0743f9b33865b2b11817b6

Group: `$USER_HOME/.cache/pip/http-v2/2/e/6`. Source: `D1/in/raw/alma/members/1a0743f9b33865b2b11817b6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-4f8e0266a8ca961c0daad7f3

Group: `$USER_HOME/.cache/pip/http-v2/2/e/6/9`. Source: `D1/in/raw/alma/members/4f8e0266a8ca961c0daad7f3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-403a04ea7b68fcfcdfa4314d

Group: `$USER_HOME/.cache/pip/http-v2/2/e/6/9/5`. Source: `D1/in/raw/alma/members/403a04ea7b68fcfcdfa4314d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2e695db3f30b3e1f3f37df61efc2c407f2a6101c03e6b973a566d8e3`, `2e695db3f30b3e1f3f37df61efc2c407f2a6101c03e6b973a566d8e3.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-2efca9515b8884a048795d4e

Group: `$USER_HOME/.cache/pip/http-v2/3`. Source: `D1/in/raw/alma/members/2efca9515b8884a048795d4e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `1`, `4`, `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-d84120275c09cb63c79f39bb

Group: `$USER_HOME/.cache/pip/http-v2/3/0`. Source: `D1/in/raw/alma/members/d84120275c09cb63c79f39bb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-21c7a5ab5db650ebae47a459

Group: `$USER_HOME/.cache/pip/http-v2/3/0/9`. Source: `D1/in/raw/alma/members/21c7a5ab5db650ebae47a459.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-04e4bfbc96cd1ae6dc9976fe

Group: `$USER_HOME/.cache/pip/http-v2/3/0/9/6`. Source: `D1/in/raw/alma/members/04e4bfbc96cd1ae6dc9976fe.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-9a981a100e066daf681e2f1c

Group: `$USER_HOME/.cache/pip/http-v2/3/0/9/6/6`. Source: `D1/in/raw/alma/members/9a981a100e066daf681e2f1c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3096620e700ab3c794191e9340f3b1d079af5462000376c484596199`, `3096620e700ab3c794191e9340f3b1d079af5462000376c484596199.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-cec55353e71dcd0e0bd3d0d8

Group: `$USER_HOME/.cache/pip/http-v2/3/1`. Source: `D1/in/raw/alma/members/cec55353e71dcd0e0bd3d0d8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-18683cf937f53edddb354c41

Group: `$USER_HOME/.cache/pip/http-v2/3/1/e`. Source: `D1/in/raw/alma/members/18683cf937f53edddb354c41.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-2d1b2d7af140dfb3133473a6

Group: `$USER_HOME/.cache/pip/http-v2/3/1/e/0`. Source: `D1/in/raw/alma/members/2d1b2d7af140dfb3133473a6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-69ab72dbf21ea1a6fe95344f

Group: `$USER_HOME/.cache/pip/http-v2/3/1/e/0/0`. Source: `D1/in/raw/alma/members/69ab72dbf21ea1a6fe95344f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `31e0063c274aa3545f95e68aeecec7e139aff757a5a545bccd447139`, `31e0063c274aa3545f95e68aeecec7e139aff757a5a545bccd447139.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-66e64caca0b7974decf094c1

Group: `$USER_HOME/.cache/pip/http-v2/3/4`. Source: `D1/in/raw/alma/members/66e64caca0b7974decf094c1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-599989005d5d0846b1ad9d1f

Group: `$USER_HOME/.cache/pip/http-v2/3/4/0`. Source: `D1/in/raw/alma/members/599989005d5d0846b1ad9d1f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-6d33c4c98c30fd4974f58648

Group: `$USER_HOME/.cache/pip/http-v2/3/4/0/0`. Source: `D1/in/raw/alma/members/6d33c4c98c30fd4974f58648.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-71d0b4e0c5eff74f9a77ccc0

Group: `$USER_HOME/.cache/pip/http-v2/3/4/0/0/6`. Source: `D1/in/raw/alma/members/71d0b4e0c5eff74f9a77ccc0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `340061226969c04b85b987862c88e4484e0001d630d72018d02a9a98`, `340061226969c04b85b987862c88e4484e0001d630d72018d02a9a98.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-fa596cbd606f47c609b1f4e7

Group: `$USER_HOME/.cache/pip/http-v2/3/a`. Source: `D1/in/raw/alma/members/fa596cbd606f47c609b1f4e7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-8a67813365390cdfc12208ad

Group: `$USER_HOME/.cache/pip/http-v2/3/a/c`. Source: `D1/in/raw/alma/members/8a67813365390cdfc12208ad.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-add82366a8ec0e32efe60bc5

Group: `$USER_HOME/.cache/pip/http-v2/3/a/c/9`. Source: `D1/in/raw/alma/members/add82366a8ec0e32efe60bc5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-22d694912803faf1e6b34457

Group: `$USER_HOME/.cache/pip/http-v2/3/a/c/9/7`. Source: `D1/in/raw/alma/members/22d694912803faf1e6b34457.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3ac9704515dbf9cb549c1d083b648fc504e1f41cc783e493a6d0baf9`, `3ac9704515dbf9cb549c1d083b648fc504e1f41cc783e493a6d0baf9.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-ede9cb01a6363edefe4b8994

Group: `$USER_HOME/.cache/pip/http-v2/4`. Source: `D1/in/raw/alma/members/ede9cb01a6363edefe4b8994.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `2`, `3`, `4`, `d`, `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-eaf28f02ce13cb1f4998ce96

Group: `$USER_HOME/.cache/pip/http-v2/4/0`. Source: `D1/in/raw/alma/members/eaf28f02ce13cb1f4998ce96.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-f05c28054c270ac8a4df2ca2

Group: `$USER_HOME/.cache/pip/http-v2/4/0/0`. Source: `D1/in/raw/alma/members/f05c28054c270ac8a4df2ca2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-dcde67315f3effc34eb9ab4e

Group: `$USER_HOME/.cache/pip/http-v2/4/0/0/d`. Source: `D1/in/raw/alma/members/dcde67315f3effc34eb9ab4e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-04662e15bd0eae09f8da427a

Group: `$USER_HOME/.cache/pip/http-v2/4/0/0/d/b`. Source: `D1/in/raw/alma/members/04662e15bd0eae09f8da427a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `400db3c9a550719d76958c9c597bfbff6eb98533f684c02cc870de92`, `400db3c9a550719d76958c9c597bfbff6eb98533f684c02cc870de92.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-c6f11f14e76673823bdaae4b

Group: `$USER_HOME/.cache/pip/http-v2/4/2`. Source: `D1/in/raw/alma/members/c6f11f14e76673823bdaae4b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-4969c79409cedc90ec64144e

Group: `$USER_HOME/.cache/pip/http-v2/4/2/4`. Source: `D1/in/raw/alma/members/4969c79409cedc90ec64144e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-943983d35efa160fc2348ad3

Group: `$USER_HOME/.cache/pip/http-v2/4/2/4/a`. Source: `D1/in/raw/alma/members/943983d35efa160fc2348ad3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-644714ef6d27284ab173b39d

Group: `$USER_HOME/.cache/pip/http-v2/4/2/4/a/1`. Source: `D1/in/raw/alma/members/644714ef6d27284ab173b39d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `424a192b7287fe6da616486df0ecf2a78f7da8b275ac11ba81e90d32`, `424a192b7287fe6da616486df0ecf2a78f7da8b275ac11ba81e90d32.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-4af6167f5e58d5b43842eeac

Group: `$USER_HOME/.cache/pip/http-v2/4/3`. Source: `D1/in/raw/alma/members/4af6167f5e58d5b43842eeac.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-1527c67c6574ccd5d40f0a9e

Group: `$USER_HOME/.cache/pip/http-v2/4/3/3`. Source: `D1/in/raw/alma/members/1527c67c6574ccd5d40f0a9e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-bded4702d7dc2895a1cb4061

Group: `$USER_HOME/.cache/pip/http-v2/4/3/3/f`. Source: `D1/in/raw/alma/members/bded4702d7dc2895a1cb4061.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-dc4b7a907a48daccd8bc2a50

Group: `$USER_HOME/.cache/pip/http-v2/4/3/3/f/c`. Source: `D1/in/raw/alma/members/dc4b7a907a48daccd8bc2a50.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `433fc562620ff37ae2c144d3bd09c0cce0e4ef09c0797ae18a217762`, `433fc562620ff37ae2c144d3bd09c0cce0e4ef09c0797ae18a217762.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-f4bf205c344ded983d9d5c78

Group: `$USER_HOME/.cache/pip/http-v2/4/4`. Source: `D1/in/raw/alma/members/f4bf205c344ded983d9d5c78.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-49747718d66c944cccc43246

Group: `$USER_HOME/.cache/pip/http-v2/4/4/e`. Source: `D1/in/raw/alma/members/49747718d66c944cccc43246.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-dc346b253c41fc8829560cab

Group: `$USER_HOME/.cache/pip/http-v2/4/4/e/5`. Source: `D1/in/raw/alma/members/dc346b253c41fc8829560cab.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-85358ddbc2f196314c4aa4ba

Group: `$USER_HOME/.cache/pip/http-v2/4/4/e/5/b`. Source: `D1/in/raw/alma/members/85358ddbc2f196314c4aa4ba.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `44e5b11a6caa92636d8ccfe658d420ba4ed8f67f7f4e835b214255aa`, `44e5b11a6caa92636d8ccfe658d420ba4ed8f67f7f4e835b214255aa.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-23fbf1af7a612604a8059a83

Group: `$USER_HOME/.cache/pip/http-v2/4/d`. Source: `D1/in/raw/alma/members/23fbf1af7a612604a8059a83.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-e3262463a95087cef8f48756

Group: `$USER_HOME/.cache/pip/http-v2/4/d/2`. Source: `D1/in/raw/alma/members/e3262463a95087cef8f48756.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-389e1ee3c3bcf807e5f28d8d

Group: `$USER_HOME/.cache/pip/http-v2/4/d/2/7`. Source: `D1/in/raw/alma/members/389e1ee3c3bcf807e5f28d8d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-c570a9b524c4786afeecbf1e

Group: `$USER_HOME/.cache/pip/http-v2/4/d/2/7/2`. Source: `D1/in/raw/alma/members/c570a9b524c4786afeecbf1e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4d272e6453941ce8b0a37a02cdb1685fc612c33441fa74691fb40656`, `4d272e6453941ce8b0a37a02cdb1685fc612c33441fa74691fb40656.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-419d2e63f070188632de6166

Group: `$USER_HOME/.cache/pip/http-v2/4/e`. Source: `D1/in/raw/alma/members/419d2e63f070188632de6166.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-c51c82b4da049c53cc795c43

Group: `$USER_HOME/.cache/pip/http-v2/4/e/5`. Source: `D1/in/raw/alma/members/c51c82b4da049c53cc795c43.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-a66f4e33da20d3e67ba4fbde

Group: `$USER_HOME/.cache/pip/http-v2/4/e/5/9`. Source: `D1/in/raw/alma/members/a66f4e33da20d3e67ba4fbde.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-4dc13a673712cbfcb925bd06

Group: `$USER_HOME/.cache/pip/http-v2/4/e/5/9/c`. Source: `D1/in/raw/alma/members/4dc13a673712cbfcb925bd06.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4e59c67d9e71ce824c6a9f89338b0f886ab79a08e39218380516a054`, `4e59c67d9e71ce824c6a9f89338b0f886ab79a08e39218380516a054.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-a1e7acf7c5f3c58cd807cb7f

Group: `$USER_HOME/.cache/pip/http-v2/5`. Source: `D1/in/raw/alma/members/a1e7acf7c5f3c58cd807cb7f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`, `7`, `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-a43bb099a3fdb27c1ec5b1ef

Group: `$USER_HOME/.cache/pip/http-v2/5/5`. Source: `D1/in/raw/alma/members/a43bb099a3fdb27c1ec5b1ef.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-f5ff018ddd81855fb20c73eb

Group: `$USER_HOME/.cache/pip/http-v2/5/5/9`. Source: `D1/in/raw/alma/members/f5ff018ddd81855fb20c73eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-2686e3217da5bc53792ba08c

Group: `$USER_HOME/.cache/pip/http-v2/5/5/9/5`. Source: `D1/in/raw/alma/members/2686e3217da5bc53792ba08c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-c1195883d3abecc32902d12e

Group: `$USER_HOME/.cache/pip/http-v2/5/5/9/5/8`. Source: `D1/in/raw/alma/members/c1195883d3abecc32902d12e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `559585ce87a922c6a3939c14156afea29f370337e39dc8c33f2ea781`, `559585ce87a922c6a3939c14156afea29f370337e39dc8c33f2ea781.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-101389cda3334da6ae1e6ca5

Group: `$USER_HOME/.cache/pip/http-v2/5/7`. Source: `D1/in/raw/alma/members/101389cda3334da6ae1e6ca5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-8254b05f1135dfa7e2f520ad

Group: `$USER_HOME/.cache/pip/http-v2/5/7/3`. Source: `D1/in/raw/alma/members/8254b05f1135dfa7e2f520ad.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-4118c756d90202bcdb30d053

Group: `$USER_HOME/.cache/pip/http-v2/5/7/3/9`. Source: `D1/in/raw/alma/members/4118c756d90202bcdb30d053.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-ef67c0cb3dd412d6172b9a10

Group: `$USER_HOME/.cache/pip/http-v2/5/7/3/9/8`. Source: `D1/in/raw/alma/members/ef67c0cb3dd412d6172b9a10.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `57398b561082ff00b477d7ac6b262ac5d0624c540c91ab07578a32d1`, `57398b561082ff00b477d7ac6b262ac5d0624c540c91ab07578a32d1.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-80dc76888c7fe4285b160268

Group: `$USER_HOME/.cache/pip/http-v2/5/c`. Source: `D1/in/raw/alma/members/80dc76888c7fe4285b160268.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-df7bda122b7b4fe37bb5667f

Group: `$USER_HOME/.cache/pip/http-v2/5/c/5`. Source: `D1/in/raw/alma/members/df7bda122b7b4fe37bb5667f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-ad83b23c9d08c1dee9499f71

Group: `$USER_HOME/.cache/pip/http-v2/5/c/5/4`. Source: `D1/in/raw/alma/members/ad83b23c9d08c1dee9499f71.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-d6b8b2888a75804ad5854303

Group: `$USER_HOME/.cache/pip/http-v2/5/c/5/4/9`. Source: `D1/in/raw/alma/members/d6b8b2888a75804ad5854303.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5c549c4221710890f3ade329782d3c04c27aa75d9f68539b08177fa7`, `5c549c4221710890f3ade329782d3c04c27aa75d9f68539b08177fa7.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-115377a8694fb8b7cfe6cde1

Group: `$USER_HOME/.cache/pip/http-v2/6`. Source: `D1/in/raw/alma/members/115377a8694fb8b7cfe6cde1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-377667d27d24eb0384f97f12

Group: `$USER_HOME/.cache/pip/http-v2/6/f`. Source: `D1/in/raw/alma/members/377667d27d24eb0384f97f12.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`, `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-107ef68598a5ef1f9d578953

Group: `$USER_HOME/.cache/pip/http-v2/6/f/4`. Source: `D1/in/raw/alma/members/107ef68598a5ef1f9d578953.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-4290fa191ca00d0f43b90d76

Group: `$USER_HOME/.cache/pip/http-v2/6/f/4/e`. Source: `D1/in/raw/alma/members/4290fa191ca00d0f43b90d76.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-a34182b956f185217bc77364

Group: `$USER_HOME/.cache/pip/http-v2/6/f/4/e/c`. Source: `D1/in/raw/alma/members/a34182b956f185217bc77364.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6f4ecd3fbc79bc497ff7ecd8baf235d059edf19f15587e6d5eedfdb8`, `6f4ecd3fbc79bc497ff7ecd8baf235d059edf19f15587e6d5eedfdb8.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-41801e6cef6462af10fd155e

Group: `$USER_HOME/.cache/pip/http-v2/6/f/5`. Source: `D1/in/raw/alma/members/41801e6cef6462af10fd155e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-1a0b76af2d3dff745ab104c8

Group: `$USER_HOME/.cache/pip/http-v2/6/f/5/8`. Source: `D1/in/raw/alma/members/1a0b76af2d3dff745ab104c8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-5fd5628efbbc58e53bbf0b3e

Group: `$USER_HOME/.cache/pip/http-v2/6/f/5/8/3`. Source: `D1/in/raw/alma/members/5fd5628efbbc58e53bbf0b3e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6f58315105f89fee1362c31502969537488db877c79a9478a63bd668`, `6f58315105f89fee1362c31502969537488db877c79a9478a63bd668.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-1b0bd8fa70c85f19d99bc94b

Group: `$USER_HOME/.cache/pip/http-v2/7`. Source: `D1/in/raw/alma/members/1b0bd8fa70c85f19d99bc94b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`, `a`, `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-ab278649cbd910a06089c81d

Group: `$USER_HOME/.cache/pip/http-v2/7/4`. Source: `D1/in/raw/alma/members/ab278649cbd910a06089c81d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-12c46f68b5355030a10eb4be

Group: `$USER_HOME/.cache/pip/http-v2/7/4/b`. Source: `D1/in/raw/alma/members/12c46f68b5355030a10eb4be.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-1786251e60014adab86806c3

Group: `$USER_HOME/.cache/pip/http-v2/7/4/b/d`. Source: `D1/in/raw/alma/members/1786251e60014adab86806c3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-097d7760d110ab4b109a3009

Group: `$USER_HOME/.cache/pip/http-v2/7/4/b/d/f`. Source: `D1/in/raw/alma/members/097d7760d110ab4b109a3009.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `74bdf372f3d845193f395b9ba4ed91510cd09dc32621fc25fe02568d`, `74bdf372f3d845193f395b9ba4ed91510cd09dc32621fc25fe02568d.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-e82c60785288ef9f863445ac

Group: `$USER_HOME/.cache/pip/http-v2/7/a`. Source: `D1/in/raw/alma/members/e82c60785288ef9f863445ac.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-083ec27a7ce94aac68b52a9c

Group: `$USER_HOME/.cache/pip/http-v2/7/a/a`. Source: `D1/in/raw/alma/members/083ec27a7ce94aac68b52a9c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-362c9c3c8df1452447a352e1

Group: `$USER_HOME/.cache/pip/http-v2/7/a/a/5`. Source: `D1/in/raw/alma/members/362c9c3c8df1452447a352e1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`, `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-66d5f6d72bcc2dc4afc47f83

Group: `$USER_HOME/.cache/pip/http-v2/7/a/a/5/1`. Source: `D1/in/raw/alma/members/66d5f6d72bcc2dc4afc47f83.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7aa51a08089aff26f021bff22bb0f6a33880ab66e5e2cc1b9584b065`, `7aa51a08089aff26f021bff22bb0f6a33880ab66e5e2cc1b9584b065.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-93b0c210150c3de57fd663ee

Group: `$USER_HOME/.cache/pip/http-v2/7/a/a/5/8`. Source: `D1/in/raw/alma/members/93b0c210150c3de57fd663ee.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7aa58973910fd6c56eaa6723fd5b5e7054e5f1b3c6ee8a145c1af3ec`, `7aa58973910fd6c56eaa6723fd5b5e7054e5f1b3c6ee8a145c1af3ec.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-493f78ef1303a4e1b77a1dad

Group: `$USER_HOME/.cache/pip/http-v2/7/c`. Source: `D1/in/raw/alma/members/493f78ef1303a4e1b77a1dad.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-943f02e9d6500fbe5834e870

Group: `$USER_HOME/.cache/pip/http-v2/7/c/2`. Source: `D1/in/raw/alma/members/943f02e9d6500fbe5834e870.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-72f9401116b4bb2ab8e28d85

Group: `$USER_HOME/.cache/pip/http-v2/7/c/2/1`. Source: `D1/in/raw/alma/members/72f9401116b4bb2ab8e28d85.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-f60007050df28fa043e9dfb7

Group: `$USER_HOME/.cache/pip/http-v2/7/c/2/1/c`. Source: `D1/in/raw/alma/members/f60007050df28fa043e9dfb7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7c21c843b2bfe7c38ea8bf3c1e54bdb4859bfa36f5b7a46caaeb4fe2`, `7c21c843b2bfe7c38ea8bf3c1e54bdb4859bfa36f5b7a46caaeb4fe2.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-a39913ee153ebdcef2fdea3a

Group: `$USER_HOME/.cache/pip/http-v2/8`. Source: `D1/in/raw/alma/members/a39913ee153ebdcef2fdea3a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`, `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-7552d3ef87374f13cada5ec9

Group: `$USER_HOME/.cache/pip/http-v2/8/5`. Source: `D1/in/raw/alma/members/7552d3ef87374f13cada5ec9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-2ac1ff8309b45fa7be990679

Group: `$USER_HOME/.cache/pip/http-v2/8/5/2`. Source: `D1/in/raw/alma/members/2ac1ff8309b45fa7be990679.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-41e24b90c120fd74d898791d

Group: `$USER_HOME/.cache/pip/http-v2/8/5/2/6`. Source: `D1/in/raw/alma/members/41e24b90c120fd74d898791d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-5c3f1bb8697beae5872a1265

Group: `$USER_HOME/.cache/pip/http-v2/8/5/2/6/7`. Source: `D1/in/raw/alma/members/5c3f1bb8697beae5872a1265.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `85267f4a19c6ab1eb80e089133e17483bc373920a4cb6bdd53ce7e08`, `85267f4a19c6ab1eb80e089133e17483bc373920a4cb6bdd53ce7e08.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-6ff51ece01319c5465c1c988

Group: `$USER_HOME/.cache/pip/http-v2/8/f`. Source: `D1/in/raw/alma/members/6ff51ece01319c5465c1c988.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-bba22b0302116d8e9fd38113

Group: `$USER_HOME/.cache/pip/http-v2/8/f/7`. Source: `D1/in/raw/alma/members/bba22b0302116d8e9fd38113.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-e763ea2323303768051c33e4

Group: `$USER_HOME/.cache/pip/http-v2/8/f/7/8`. Source: `D1/in/raw/alma/members/e763ea2323303768051c33e4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-0c65c3ff2333b5855dfa1218

Group: `$USER_HOME/.cache/pip/http-v2/8/f/7/8/a`. Source: `D1/in/raw/alma/members/0c65c3ff2333b5855dfa1218.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8f78a59c750512c5eff98117526033c3ddca4a99c7d75426a1ad4942`, `8f78a59c750512c5eff98117526033c3ddca4a99c7d75426a1ad4942.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-27784c1b1595cbc5dcf6fffb

Group: `$USER_HOME/.cache/pip/http-v2/9`. Source: `D1/in/raw/alma/members/27784c1b1595cbc5dcf6fffb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`, `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-4103d65c8137b85d1ffb0eea

Group: `$USER_HOME/.cache/pip/http-v2/9/8`. Source: `D1/in/raw/alma/members/4103d65c8137b85d1ffb0eea.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-f45959dfd0e857846cc54882

Group: `$USER_HOME/.cache/pip/http-v2/9/8/f`. Source: `D1/in/raw/alma/members/f45959dfd0e857846cc54882.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-9464764c4587d6cb3ebc0687

Group: `$USER_HOME/.cache/pip/http-v2/9/8/f/8`. Source: `D1/in/raw/alma/members/9464764c4587d6cb3ebc0687.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-c2a837f0c1429e8ac54cf6d6

Group: `$USER_HOME/.cache/pip/http-v2/9/8/f/8/d`. Source: `D1/in/raw/alma/members/c2a837f0c1429e8ac54cf6d6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `98f8d5870dd89b04ada97fe6d93142610a57367cb36dac3708758aae`, `98f8d5870dd89b04ada97fe6d93142610a57367cb36dac3708758aae.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-3024b0bcc6b970629f803919

Group: `$USER_HOME/.cache/pip/http-v2/9/f`. Source: `D1/in/raw/alma/members/3024b0bcc6b970629f803919.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-229eb1a2d1acb5f5abd3e8e6

Group: `$USER_HOME/.cache/pip/http-v2/9/f/9`. Source: `D1/in/raw/alma/members/229eb1a2d1acb5f5abd3e8e6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-e0fa9fcc61c3b1f249f7605a

Group: `$USER_HOME/.cache/pip/http-v2/9/f/9/3`. Source: `D1/in/raw/alma/members/e0fa9fcc61c3b1f249f7605a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-d641425d2bd8435544b58a0b

Group: `$USER_HOME/.cache/pip/http-v2/9/f/9/3/3`. Source: `D1/in/raw/alma/members/d641425d2bd8435544b58a0b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9f93306d7b672475999e1ccb003ed535876b07060341d71f2c054af0`, `9f93306d7b672475999e1ccb003ed535876b07060341d71f2c054af0.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-53760dc2e97d1aeb639f21bd

Group: `$USER_HOME/.cache/pip/http-v2/a`. Source: `D1/in/raw/alma/members/53760dc2e97d1aeb639f21bd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`, `9`, `c`, `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-fe6a240a85e16047767355ba

Group: `$USER_HOME/.cache/pip/http-v2/a/1`. Source: `D1/in/raw/alma/members/fe6a240a85e16047767355ba.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`, `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-a72691f60c404b2526f8efa4

Group: `$USER_HOME/.cache/pip/http-v2/a/1/9`. Source: `D1/in/raw/alma/members/a72691f60c404b2526f8efa4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-12603c4d7a5594df3424ccd6

Group: `$USER_HOME/.cache/pip/http-v2/a/1/9/5`. Source: `D1/in/raw/alma/members/12603c4d7a5594df3424ccd6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-5922fae921870d6cc63d7a81

Group: `$USER_HOME/.cache/pip/http-v2/a/1/9/5/3`. Source: `D1/in/raw/alma/members/5922fae921870d6cc63d7a81.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a19537d3cf37c122db841d6fe4cd322bc10d1a558bb00d146b85cb9a`, `a19537d3cf37c122db841d6fe4cd322bc10d1a558bb00d146b85cb9a.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-27b00c9429c2f7896896442d

Group: `$USER_HOME/.cache/pip/http-v2/a/1/d`. Source: `D1/in/raw/alma/members/27b00c9429c2f7896896442d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-10e2da836d794d19c4dbe25e

Group: `$USER_HOME/.cache/pip/http-v2/a/1/d/8`. Source: `D1/in/raw/alma/members/10e2da836d794d19c4dbe25e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-7c6bcdfb1d3d19b696d906ea

Group: `$USER_HOME/.cache/pip/http-v2/a/1/d/8/d`. Source: `D1/in/raw/alma/members/7c6bcdfb1d3d19b696d906ea.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a1d8d6b76fba8754c44ce6685b82beb3909173f9c1d49de0aca30afe`, `a1d8d6b76fba8754c44ce6685b82beb3909173f9c1d49de0aca30afe.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-a78afe0aea095b55c05036fd

Group: `$USER_HOME/.cache/pip/http-v2/a/9`. Source: `D1/in/raw/alma/members/a78afe0aea095b55c05036fd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-7705273aae1b011150f66093

Group: `$USER_HOME/.cache/pip/http-v2/a/9/0`. Source: `D1/in/raw/alma/members/7705273aae1b011150f66093.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-4b9f5bfbe1740d5ca9b66122

Group: `$USER_HOME/.cache/pip/http-v2/a/9/0/5`. Source: `D1/in/raw/alma/members/4b9f5bfbe1740d5ca9b66122.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-96935c51faa3253a75654979

Group: `$USER_HOME/.cache/pip/http-v2/a/9/0/5/8`. Source: `D1/in/raw/alma/members/96935c51faa3253a75654979.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a905843eb01b88aea284f46d56195b2724e8acc9156ba33f8a2d6dbb`, `a905843eb01b88aea284f46d56195b2724e8acc9156ba33f8a2d6dbb.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-13f3fc49e00d758f4a5b3ae2

Group: `$USER_HOME/.cache/pip/http-v2/a/9/b`. Source: `D1/in/raw/alma/members/13f3fc49e00d758f4a5b3ae2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-7949c65c1ddbcd726d28e0d5

Group: `$USER_HOME/.cache/pip/http-v2/a/9/b/b`. Source: `D1/in/raw/alma/members/7949c65c1ddbcd726d28e0d5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-bfbf6e480b1b091ecda81772

Group: `$USER_HOME/.cache/pip/http-v2/a/9/b/b/0`. Source: `D1/in/raw/alma/members/bfbf6e480b1b091ecda81772.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a9bb03c14862c205bb1e9afada2f7f82ad28a3777c5a8617903b6dcc`, `a9bb03c14862c205bb1e9afada2f7f82ad28a3777c5a8617903b6dcc.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-d7487151c3985edafc623f78

Group: `$USER_HOME/.cache/pip/http-v2/a/c`. Source: `D1/in/raw/alma/members/d7487151c3985edafc623f78.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-4982dffae099e69f0ee3a165

Group: `$USER_HOME/.cache/pip/http-v2/a/c/1`. Source: `D1/in/raw/alma/members/4982dffae099e69f0ee3a165.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-8ca58908c64182967920b669

Group: `$USER_HOME/.cache/pip/http-v2/a/c/1/1`. Source: `D1/in/raw/alma/members/8ca58908c64182967920b669.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-f5ab3aad000b60bbc3ac8948

Group: `$USER_HOME/.cache/pip/http-v2/a/c/1/1/c`. Source: `D1/in/raw/alma/members/f5ab3aad000b60bbc3ac8948.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ac11cc5759c33ab9345f591d822764ae2d17407f9d6946f53fd7bd9f`, `ac11cc5759c33ab9345f591d822764ae2d17407f9d6946f53fd7bd9f.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-d315317a7985fd7125076703

Group: `$USER_HOME/.cache/pip/http-v2/a/e`. Source: `D1/in/raw/alma/members/d315317a7985fd7125076703.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-163e691dcfe75d720a92781c

Group: `$USER_HOME/.cache/pip/http-v2/a/e/5`. Source: `D1/in/raw/alma/members/163e691dcfe75d720a92781c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-33d0cdfbca85913791035695

Group: `$USER_HOME/.cache/pip/http-v2/a/e/5/7`. Source: `D1/in/raw/alma/members/33d0cdfbca85913791035695.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-8a341b9d5491356a39abe0dd

Group: `$USER_HOME/.cache/pip/http-v2/a/e/5/7/6`. Source: `D1/in/raw/alma/members/8a341b9d5491356a39abe0dd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ae57694b79d905c0784e33405926b2df18d6981a2b571cf072490071`, `ae57694b79d905c0784e33405926b2df18d6981a2b571cf072490071.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-1af1bf1bea18a2f9ede38d38

Group: `$USER_HOME/.cache/pip/http-v2/b`. Source: `D1/in/raw/alma/members/1af1bf1bea18a2f9ede38d38.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `1`, `5`, `7`, `8`, `9`, `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-3b94c13a10c8149bc3e8ec05

Group: `$USER_HOME/.cache/pip/http-v2/b/0`. Source: `D1/in/raw/alma/members/3b94c13a10c8149bc3e8ec05.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-f65f4f012b131e8e33850ae1

Group: `$USER_HOME/.cache/pip/http-v2/b/0/6`. Source: `D1/in/raw/alma/members/f65f4f012b131e8e33850ae1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-78bbaca9989755acbf8787e4

Group: `$USER_HOME/.cache/pip/http-v2/b/0/6/d`. Source: `D1/in/raw/alma/members/78bbaca9989755acbf8787e4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-0bca70907bb39da29c0d1257

Group: `$USER_HOME/.cache/pip/http-v2/b/0/6/d/a`. Source: `D1/in/raw/alma/members/0bca70907bb39da29c0d1257.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b06da2406a946603ad8758c07596341b63be1198f27faac2957d8476`, `b06da2406a946603ad8758c07596341b63be1198f27faac2957d8476.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-e4fac084629dc82913627747

Group: `$USER_HOME/.cache/pip/http-v2/b/1`. Source: `D1/in/raw/alma/members/e4fac084629dc82913627747.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-129febe489273402f4f2580c

Group: `$USER_HOME/.cache/pip/http-v2/b/1/1`. Source: `D1/in/raw/alma/members/129febe489273402f4f2580c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-0f156edc538beaea8c740182

Group: `$USER_HOME/.cache/pip/http-v2/b/1/1/9`. Source: `D1/in/raw/alma/members/0f156edc538beaea8c740182.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-2fc3ee95d7e7fb64ab019001

Group: `$USER_HOME/.cache/pip/http-v2/b/1/1/9/0`. Source: `D1/in/raw/alma/members/2fc3ee95d7e7fb64ab019001.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b11909f451f61fb29636217082b1c638b177c59eac335e0200a136e6`, `b11909f451f61fb29636217082b1c638b177c59eac335e0200a136e6.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-3a446f21fcffcd5a89302ca3

Group: `$USER_HOME/.cache/pip/http-v2/b/5`. Source: `D1/in/raw/alma/members/3a446f21fcffcd5a89302ca3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-1b1aac44affeaa383cbc2f2a

Group: `$USER_HOME/.cache/pip/http-v2/b/5/0`. Source: `D1/in/raw/alma/members/1b1aac44affeaa383cbc2f2a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-b2de6b590d588876abd62edc

Group: `$USER_HOME/.cache/pip/http-v2/b/5/0/1`. Source: `D1/in/raw/alma/members/b2de6b590d588876abd62edc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-8595c7a65cb1b2e851cba5ab

Group: `$USER_HOME/.cache/pip/http-v2/b/5/0/1/6`. Source: `D1/in/raw/alma/members/8595c7a65cb1b2e851cba5ab.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b50161ce80a3ddd3f50977d5414a93660648823b703e10f65f16eeeb`, `b50161ce80a3ddd3f50977d5414a93660648823b703e10f65f16eeeb.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-45b4f10903cf1b6082147652

Group: `$USER_HOME/.cache/pip/http-v2/b/7`. Source: `D1/in/raw/alma/members/45b4f10903cf1b6082147652.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-9231a4ba91b7172634f042da

Group: `$USER_HOME/.cache/pip/http-v2/b/7/7`. Source: `D1/in/raw/alma/members/9231a4ba91b7172634f042da.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-aea74ecec76f329de40b2dba

Group: `$USER_HOME/.cache/pip/http-v2/b/7/7/0`. Source: `D1/in/raw/alma/members/aea74ecec76f329de40b2dba.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-d5c75674f3c85aee89b81b41

Group: `$USER_HOME/.cache/pip/http-v2/b/7/7/0/d`. Source: `D1/in/raw/alma/members/d5c75674f3c85aee89b81b41.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b770dbc927194b44de3253fb2a74a226552978ba02220f61c8cdf5b6`, `b770dbc927194b44de3253fb2a74a226552978ba02220f61c8cdf5b6.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-335a34f2e02f172233de6780

Group: `$USER_HOME/.cache/pip/http-v2/b/8`. Source: `D1/in/raw/alma/members/335a34f2e02f172233de6780.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-4180d02146f39e7d3e54700a

Group: `$USER_HOME/.cache/pip/http-v2/b/8/2`. Source: `D1/in/raw/alma/members/4180d02146f39e7d3e54700a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-c66bba214b1e78fa88e2965c

Group: `$USER_HOME/.cache/pip/http-v2/b/8/2/9`. Source: `D1/in/raw/alma/members/c66bba214b1e78fa88e2965c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-02136196521069f0e2bd2227

Group: `$USER_HOME/.cache/pip/http-v2/b/8/2/9/2`. Source: `D1/in/raw/alma/members/02136196521069f0e2bd2227.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b82925d93488b43ba8ddfeb7ee4d9fef079d43c15f712c7da055b589`, `b82925d93488b43ba8ddfeb7ee4d9fef079d43c15f712c7da055b589.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-402bc909c9e89a5bd5625645

Group: `$USER_HOME/.cache/pip/http-v2/b/9`. Source: `D1/in/raw/alma/members/402bc909c9e89a5bd5625645.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-7dd46db0e5059938d160b70e

Group: `$USER_HOME/.cache/pip/http-v2/b/9/3`. Source: `D1/in/raw/alma/members/7dd46db0e5059938d160b70e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-290746c7c2915f232eb18995

Group: `$USER_HOME/.cache/pip/http-v2/b/9/3/0`. Source: `D1/in/raw/alma/members/290746c7c2915f232eb18995.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-27c4fcce981c7cc51a68c984

Group: `$USER_HOME/.cache/pip/http-v2/b/9/3/0/2`. Source: `D1/in/raw/alma/members/27c4fcce981c7cc51a68c984.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b930289540950ad36568515698a952601bc141581af83f9ca11e5122`, `b930289540950ad36568515698a952601bc141581af83f9ca11e5122.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-e02d54e428a093a5601853b8

Group: `$USER_HOME/.cache/pip/http-v2/b/b`. Source: `D1/in/raw/alma/members/e02d54e428a093a5601853b8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-9636089d71120b27a7c7de51

Group: `$USER_HOME/.cache/pip/http-v2/b/b/7`. Source: `D1/in/raw/alma/members/9636089d71120b27a7c7de51.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-8058b122b53f10981a411936

Group: `$USER_HOME/.cache/pip/http-v2/b/b/7/1`. Source: `D1/in/raw/alma/members/8058b122b53f10981a411936.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-9c36a2f39d61454e7b52175c

Group: `$USER_HOME/.cache/pip/http-v2/b/b/7/1/9`. Source: `D1/in/raw/alma/members/9c36a2f39d61454e7b52175c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `bb7192a13c2e6fee9242c9c2cb1ff8a79b127b7079d339e5e13b20a5`, `bb7192a13c2e6fee9242c9c2cb1ff8a79b127b7079d339e5e13b20a5.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-817415d39d72146386412706

Group: `$USER_HOME/.cache/pip/http-v2/c`. Source: `D1/in/raw/alma/members/817415d39d72146386412706.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`, `1`, `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-e2366e5f4e29ac5a20dd1b1f

Group: `$USER_HOME/.cache/pip/http-v2/c/0`. Source: `D1/in/raw/alma/members/e2366e5f4e29ac5a20dd1b1f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-07c1722a0f8b6eef44a3d66a

Group: `$USER_HOME/.cache/pip/http-v2/c/0/4`. Source: `D1/in/raw/alma/members/07c1722a0f8b6eef44a3d66a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-9c667f94a28c6a1b593c6f2a

Group: `$USER_HOME/.cache/pip/http-v2/c/0/4/0`. Source: `D1/in/raw/alma/members/9c667f94a28c6a1b593c6f2a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-3660a26d8f743dafa9c0b25c

Group: `$USER_HOME/.cache/pip/http-v2/c/0/4/0/0`. Source: `D1/in/raw/alma/members/3660a26d8f743dafa9c0b25c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c0400f4849a16bb7ec1db13ba6d964327b0869995ab53c54f6668654`, `c0400f4849a16bb7ec1db13ba6d964327b0869995ab53c54f6668654.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-d9aac0b9df5918baae7de7d9

Group: `$USER_HOME/.cache/pip/http-v2/c/1`. Source: `D1/in/raw/alma/members/d9aac0b9df5918baae7de7d9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-29eaf0e055da756f84a3e2b8

Group: `$USER_HOME/.cache/pip/http-v2/c/1/b`. Source: `D1/in/raw/alma/members/29eaf0e055da756f84a3e2b8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-fef53fee128114e9408e3e89

Group: `$USER_HOME/.cache/pip/http-v2/c/1/b/4`. Source: `D1/in/raw/alma/members/fef53fee128114e9408e3e89.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-f75ae482e37b65c3689f421b

Group: `$USER_HOME/.cache/pip/http-v2/c/1/b/4/7`. Source: `D1/in/raw/alma/members/f75ae482e37b65c3689f421b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c1b479405629295f30559904eb4fcfb5777e91530064453c564b8a03`, `c1b479405629295f30559904eb4fcfb5777e91530064453c564b8a03.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-b942a65047e1ae0f66860a52

Group: `$USER_HOME/.cache/pip/http-v2/c/a`. Source: `D1/in/raw/alma/members/b942a65047e1ae0f66860a52.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-b37fbccd1c4719e6d2967642

Group: `$USER_HOME/.cache/pip/http-v2/c/a/6`. Source: `D1/in/raw/alma/members/b37fbccd1c4719e6d2967642.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-a71581aecd0e6bdd4c7ac0fa

Group: `$USER_HOME/.cache/pip/http-v2/c/a/6/3`. Source: `D1/in/raw/alma/members/a71581aecd0e6bdd4c7ac0fa.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-ca223805a800fc4fb4afa727

Group: `$USER_HOME/.cache/pip/http-v2/c/a/6/3/e`. Source: `D1/in/raw/alma/members/ca223805a800fc4fb4afa727.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ca63e6fd3ce4f2c3288b06d034aac68164ba715b551198cc8de89a6a`, `ca63e6fd3ce4f2c3288b06d034aac68164ba715b551198cc8de89a6a.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-ec53ac2f1492971be4620e70

Group: `$USER_HOME/.cache/pip/http-v2/d`. Source: `D1/in/raw/alma/members/ec53ac2f1492971be4620e70.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`, `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-7a70c5a785d6e2980f183e27

Group: `$USER_HOME/.cache/pip/http-v2/d/3`. Source: `D1/in/raw/alma/members/7a70c5a785d6e2980f183e27.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-54b2ad452b93a8f422f74ed2

Group: `$USER_HOME/.cache/pip/http-v2/d/3/b`. Source: `D1/in/raw/alma/members/54b2ad452b93a8f422f74ed2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a`. Pip HTTP cache or cache directory, stored as working data.
### alma-db40cf668b18489f7e3a1231

Group: `$USER_HOME/.cache/pip/http-v2/d/3/b/a`. Source: `D1/in/raw/alma/members/db40cf668b18489f7e3a1231.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-6a64fa8fe71426661fb711d6

Group: `$USER_HOME/.cache/pip/http-v2/d/3/b/a/7`. Source: `D1/in/raw/alma/members/6a64fa8fe71426661fb711d6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d3ba739aa20ed17781f881c1bb05a0ac6f314d7a741c97bfcdd8fece`, `d3ba739aa20ed17781f881c1bb05a0ac6f314d7a741c97bfcdd8fece.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-1b02772166b0902f2fed4576

Group: `$USER_HOME/.cache/pip/http-v2/d/8`. Source: `D1/in/raw/alma/members/1b02772166b0902f2fed4576.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-002b3384c73b6ab9fbd7e3c6

Group: `$USER_HOME/.cache/pip/http-v2/d/8/c`. Source: `D1/in/raw/alma/members/002b3384c73b6ab9fbd7e3c6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-ce29ada5f49cca8508c804fd

Group: `$USER_HOME/.cache/pip/http-v2/d/8/c/d`. Source: `D1/in/raw/alma/members/ce29ada5f49cca8508c804fd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-69f13433c79b44ed9983081a

Group: `$USER_HOME/.cache/pip/http-v2/d/8/c/d/8`. Source: `D1/in/raw/alma/members/69f13433c79b44ed9983081a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d8cd8c62e690ab29b773948431329e5f9e2455966700cac81c8b0ff3`, `d8cd8c62e690ab29b773948431329e5f9e2455966700cac81c8b0ff3.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-05d8dbbbeb872f31fb349ab3

Group: `$USER_HOME/.cache/pip/http-v2/e`. Source: `D1/in/raw/alma/members/05d8dbbbeb872f31fb349ab3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`, `3`, `9`, `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-dcba6a53faf76b103b6d20f1

Group: `$USER_HOME/.cache/pip/http-v2/e/1`. Source: `D1/in/raw/alma/members/dcba6a53faf76b103b6d20f1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e`. Pip HTTP cache or cache directory, stored as working data.
### alma-8a0c2cc4c07de3eb4e0c99dc

Group: `$USER_HOME/.cache/pip/http-v2/e/1/e`. Source: `D1/in/raw/alma/members/8a0c2cc4c07de3eb4e0c99dc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-470a4452af9b00ed0d0aabbb

Group: `$USER_HOME/.cache/pip/http-v2/e/1/e/3`. Source: `D1/in/raw/alma/members/470a4452af9b00ed0d0aabbb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-fb8a42b1ebf9494df755ebcc

Group: `$USER_HOME/.cache/pip/http-v2/e/1/e/3/5`. Source: `D1/in/raw/alma/members/fb8a42b1ebf9494df755ebcc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e1e353c2468471571780f9a97348e73888d6231894c139b9466648d0`, `e1e353c2468471571780f9a97348e73888d6231894c139b9466648d0.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-6803b18b6c934a895f898c8f

Group: `$USER_HOME/.cache/pip/http-v2/e/3`. Source: `D1/in/raw/alma/members/6803b18b6c934a895f898c8f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-4f18a5051ba1514d6697b51c

Group: `$USER_HOME/.cache/pip/http-v2/e/3/4`. Source: `D1/in/raw/alma/members/4f18a5051ba1514d6697b51c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-9c13f88483e47b386dd4314d

Group: `$USER_HOME/.cache/pip/http-v2/e/3/4/7`. Source: `D1/in/raw/alma/members/9c13f88483e47b386dd4314d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2`. Pip HTTP cache or cache directory, stored as working data.
### alma-e5f631907b990f780f9158ac

Group: `$USER_HOME/.cache/pip/http-v2/e/3/4/7/2`. Source: `D1/in/raw/alma/members/e5f631907b990f780f9158ac.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e3472991c55ba2fbaddced5931d34182eca51c3c130aba12041f2914`, `e3472991c55ba2fbaddced5931d34182eca51c3c130aba12041f2914.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-2b877a63ce495c1c8e84acda

Group: `$USER_HOME/.cache/pip/http-v2/e/9`. Source: `D1/in/raw/alma/members/2b877a63ce495c1c8e84acda.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0`. Pip HTTP cache or cache directory, stored as working data.
### alma-ef1ba3b978791e5bb3feacf2

Group: `$USER_HOME/.cache/pip/http-v2/e/9/0`. Source: `D1/in/raw/alma/members/ef1ba3b978791e5bb3feacf2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3`. Pip HTTP cache or cache directory, stored as working data.
### alma-6d529b75933ed717e0f4c0c7

Group: `$USER_HOME/.cache/pip/http-v2/e/9/0/3`. Source: `D1/in/raw/alma/members/6d529b75933ed717e0f4c0c7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-a50091664b57196f21cb3738

Group: `$USER_HOME/.cache/pip/http-v2/e/9/0/3/6`. Source: `D1/in/raw/alma/members/a50091664b57196f21cb3738.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e90365fc27ba769e4130064af8e005b498b4fb85327c6ecc107eea74`, `e90365fc27ba769e4130064af8e005b498b4fb85327c6ecc107eea74.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-e676dd80ba9b33f05c801db4

Group: `$USER_HOME/.cache/pip/http-v2/e/f`. Source: `D1/in/raw/alma/members/e676dd80ba9b33f05c801db4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`, `f`. Pip HTTP cache or cache directory, stored as working data.
### alma-2240a536d31c4bec2501d527

Group: `$USER_HOME/.cache/pip/http-v2/e/f/b`. Source: `D1/in/raw/alma/members/2240a536d31c4bec2501d527.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1`. Pip HTTP cache or cache directory, stored as working data.
### alma-cf3050f64f9b0b25302e22dc

Group: `$USER_HOME/.cache/pip/http-v2/e/f/b/1`. Source: `D1/in/raw/alma/members/cf3050f64f9b0b25302e22dc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7`. Pip HTTP cache or cache directory, stored as working data.
### alma-95c9360531cfb373ccc7f1e3

Group: `$USER_HOME/.cache/pip/http-v2/e/f/b/1/7`. Source: `D1/in/raw/alma/members/95c9360531cfb373ccc7f1e3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `efb1797fecf69338b5b4cb262017f195ef526ceb0b5224cf04afe0d6`, `efb1797fecf69338b5b4cb262017f195ef526ceb0b5224cf04afe0d6.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-ce4665651375162b0b534b70

Group: `$USER_HOME/.cache/pip/http-v2/e/f/f`. Source: `D1/in/raw/alma/members/ce4665651375162b0b534b70.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-ffd02660c172ad5c4dffa57e

Group: `$USER_HOME/.cache/pip/http-v2/e/f/f/c`. Source: `D1/in/raw/alma/members/ffd02660c172ad5c4dffa57e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`. Pip HTTP cache or cache directory, stored as working data.
### alma-d3c38c836744f93483b34a4b

Group: `$USER_HOME/.cache/pip/http-v2/e/f/f/c/5`. Source: `D1/in/raw/alma/members/d3c38c836744f93483b34a4b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `effc58f781e46675ba231bf893f5bb686f7ff29da4a21e441ae6f410`, `effc58f781e46675ba231bf893f5bb686f7ff29da4a21e441ae6f410.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-56d03d1e5aa765d5839e40d7

Group: `$USER_HOME/.cache/pip/http-v2/f`. Source: `D1/in/raw/alma/members/56d03d1e5aa765d5839e40d7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5`, `d`. Pip HTTP cache or cache directory, stored as working data.
### alma-3258ae3d5f26d765ddd4f18f

Group: `$USER_HOME/.cache/pip/http-v2/f/5`. Source: `D1/in/raw/alma/members/3258ae3d5f26d765ddd4f18f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9`. Pip HTTP cache or cache directory, stored as working data.
### alma-e4a6e0b2bc7ede4c49844ab1

Group: `$USER_HOME/.cache/pip/http-v2/f/5/9`. Source: `D1/in/raw/alma/members/e4a6e0b2bc7ede4c49844ab1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6`. Pip HTTP cache or cache directory, stored as working data.
### alma-308ca24719b96829d50942ba

Group: `$USER_HOME/.cache/pip/http-v2/f/5/9/6`. Source: `D1/in/raw/alma/members/308ca24719b96829d50942ba.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b`. Pip HTTP cache or cache directory, stored as working data.
### alma-2b858baa1b7ba6fb45764027

Group: `$USER_HOME/.cache/pip/http-v2/f/5/9/6/b`. Source: `D1/in/raw/alma/members/2b858baa1b7ba6fb45764027.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f596b2bf9ffff811921c4b61c488d0377c26074ddb5ef6446013cd08`, `f596b2bf9ffff811921c4b61c488d0377c26074ddb5ef6446013cd08.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-f00b8ce27bf4e3827f20721b

Group: `$USER_HOME/.cache/pip/http-v2/f/d`. Source: `D1/in/raw/alma/members/f00b8ce27bf4e3827f20721b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8`. Pip HTTP cache or cache directory, stored as working data.
### alma-f363b75a1a1147ab764ff3b6

Group: `$USER_HOME/.cache/pip/http-v2/f/d/8`. Source: `D1/in/raw/alma/members/f363b75a1a1147ab764ff3b6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4`. Pip HTTP cache or cache directory, stored as working data.
### alma-71d2d343a2acabbe4b6b357b

Group: `$USER_HOME/.cache/pip/http-v2/f/d/8/4`. Source: `D1/in/raw/alma/members/71d2d343a2acabbe4b6b357b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c`. Pip HTTP cache or cache directory, stored as working data.
### alma-473f8093c1c10ba6cb6cc3cd

Group: `$USER_HOME/.cache/pip/http-v2/f/d/8/4/c`. Source: `D1/in/raw/alma/members/473f8093c1c10ba6cb6cc3cd.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `fd84c46b9ca35d1b3dffcde8cf808cf28a8ce0d20a74e8bc1c4b59f8`, `fd84c46b9ca35d1b3dffcde8cf808cf28a8ce0d20a74e8bc1c4b59f8.body`. Pip HTTP cache or cache directory, stored as working data.
### alma-f9817f71fe6edace5bb7efc9

Group: `$USER_HOME/.cache/pip/selfcheck`. Source: `D1/in/raw/alma/members/f9817f71fe6edace5bb7efc9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `241e69162522ccf5846a2f42ebc24b17464915a155679666b89a9f31`. Pip HTTP cache or cache directory, stored as working data.
### alma-f50911a1ede74909d7be3f52

Group: `$USER_HOME/.cache/pip/wheels`. Source: `D1/in/raw/alma/members/f50911a1ede74909d7be3f52.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2a`. Pip HTTP cache or cache directory, stored as working data.
### alma-ed5e323650f882ffc247adb4

Group: `$USER_HOME/.cache/pip/wheels/2a`. Source: `D1/in/raw/alma/members/ed5e323650f882ffc247adb4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `98`. Pip HTTP cache or cache directory, stored as working data.
### alma-a5de34a83d9ad98368f65bf2

Group: `$USER_HOME/.cache/pip/wheels/2a/98`. Source: `D1/in/raw/alma/members/a5de34a83d9ad98368f65bf2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c2`. Pip HTTP cache or cache directory, stored as working data.
### alma-48660fb145a374f01142db4d

Group: `$USER_HOME/.cache/pip/wheels/2a/98/c2`. Source: `D1/in/raw/alma/members/48660fb145a374f01142db4d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `385a3733e190ae2b170804566e081ce9690ad9154edfcc3e64`. Pip HTTP cache or cache directory, stored as working data.
### alma-a423b35c10bacdd63e89b6fa

Group: `$USER_HOME/.cache/pip/wheels/2a/98/c2/385a3733e190ae2b170804566e081ce9690ad9154edfcc3e64`. Source: `D1/in/raw/alma/members/a423b35c10bacdd63e89b6fa.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `mozprofile-3.0.0-py2.py3-none-any.whl`, `origin.json`. Pip HTTP cache or cache directory, stored as working data.
### alma-c605f21df76c759160940695

Group: `$USER_HOME/.config`. Source: `D1/in/raw/alma/members/c605f21df76c759160940695.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `systemd`. Directory installation integrity and creation provenance are not established.
### alma-baf76d61c6ad95e30e863125

Group: `$USER_HOME/.config/systemd`. Source: `D1/in/raw/alma/members/baf76d61c6ad95e30e863125.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `user`. Directory installation integrity and creation provenance are not established.
### alma-1fdc6107b61543ccef8bb780

Group: `$USER_HOME/.config/systemd/user`. Source: `D1/in/raw/alma/members/1fdc6107b61543ccef8bb780.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `cal-user.service`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `default.target.wants`. Directory installation integrity and creation provenance are not established.
### alma-0684819f2449b7aed3e871b5

Group: `$USER_HOME/.config/systemd/user/default.target.wants`. Source: `D1/in/raw/alma/members/0684819f2449b7aed3e871b5.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `cal-user.service`. Package origin, unchangedness, and source of this object are not established.
### alma-6538e72fa4d2c05506b1d1ae

Group: `$USER_HOME/.local`. Source: `D1/in/raw/alma/members/6538e72fa4d2c05506b1d1ae.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `bin`, `lib`, `share`, `state`. Directory installation integrity and creation provenance are not established.
### alma-b13434b9e45de2b37ca95924

Group: `$USER_HOME/.local/bin`. Source: `D1/in/raw/alma/members/b13434b9e45de2b37ca95924.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cal-user-script`, `cowsay`, `cowthink`. Package origin, unchangedness, and source of this object are not established.
### alma-5dfd4312f60708fb1ed2c6b1

Group: `$USER_HOME/.local/lib`. Source: `D1/in/raw/alma/members/5dfd4312f60708fb1ed2c6b1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cal-marionette`, `node_modules`. Directory installation integrity and creation provenance are not established.
### alma-48a87d0890cd6edfa5da6567

Group: `$USER_HOME/.local/lib/cal-marionette`. Source: `D1/in/raw/alma/members/48a87d0890cd6edfa5da6567.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: bin,blessed,blessed-1.53.0.dist-info,distro,distro-1.9.0.dist-info,jinxed,jinxed-2.1.1.dist-info,marionette_driver,marionette_driver-3.7.1.dist-info,mozdevice,mozdevice-4.3.0.dist-info,mozfile,mozfile-3.0.0.dist-info,mozinfo,mozinfo-1.2.3.dist-info,mozlog,mozlog-8.1.0.dist-info,mozprocess,mozprocess-1.4.0.dist-info,mozprofile,mozprofile-3.0.0.dist-info,mozrunner,mozrunner-8.4.0.dist-info,mozsystemmonitor,mozsystemmonitor-1.0.1.dist-info,mozterm,mozterm-1.0.0.dist-info,mozversion,mozversion-2.4.0.dist-info,psutil,psutil-7.2.2.dist-info,six-1.17.0.dist-info,wcwidth,wcwidth-0.9.5.dist-info

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `bin`, `blessed`, `blessed-1.53.0.dist-info`, `distro`, `distro-1.9.0.dist-info`, `jinxed`, `jinxed-2.1.1.dist-info`, `marionette_driver`, `marionette_driver-3.7.1.dist-info`, `mozdevice`, `mozdevice-4.3.0.dist-info`, `mozfile`, `mozfile-3.0.0.dist-info`, `mozinfo`, `mozinfo-1.2.3.dist-info`, `mozlog`, `mozlog-8.1.0.dist-info`, `mozprocess`, `mozprocess-1.4.0.dist-info`, `mozprofile`, `mozprofile-3.0.0.dist-info`, `mozrunner`, `mozrunner-8.4.0.dist-info`, `mozsystemmonitor`, `mozsystemmonitor-1.0.1.dist-info`, `mozterm`, `mozterm-1.0.0.dist-info`, `mozversion`, `mozversion-2.4.0.dist-info`, `psutil`, `psutil-7.2.2.dist-info`, `six-1.17.0.dist-info`, `wcwidth`, `wcwidth-0.9.5.dist-info`. Directory installation integrity and creation provenance are not established.
### alma-70de7fc7f553163fc60718af

Group: `$USER_HOME/.local/lib/cal-marionette/bin`. Source: `D1/in/raw/alma/members/70de7fc7f553163fc60718af.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `diff-profiles`, `distro`, `mozinfo`, `mozprofile`, `mozrunner`, `mozversion`, `structlog`, `view-profile`. Package origin, unchangedness, and source of this object are not established.
### alma-1f2390d4e9abaeaa962b58ba

Group: `$USER_HOME/.local/lib/cal-marionette/blessed`. Source: `D1/in/raw/alma/members/1f2390d4e9abaeaa962b58ba.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-f6721e024e84b81e6c59481d

Group: `$USER_HOME/.local/lib/cal-marionette/blessed-1.53.0.dist-info`. Source: `D1/in/raw/alma/members/f6721e024e84b81e6c59481d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `licenses`. Directory installation integrity and creation provenance are not established.
### alma-8ba1c3e4358f3bb31128a7f1

Group: `$USER_HOME/.local/lib/cal-marionette/distro`. Source: `D1/in/raw/alma/members/8ba1c3e4358f3bb31128a7f1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-015c20688e56fd7edc632218

Group: `$USER_HOME/.local/lib/cal-marionette/jinxed`. Source: `D1/in/raw/alma/members/015c20688e56fd7edc632218.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: terminfo

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `terminfo`. Directory installation integrity and creation provenance are not established.
### alma-29a57b4457b05b7e4ef2787a

Group: `$USER_HOME/.local/lib/cal-marionette/jinxed-2.1.1.dist-info`. Source: `D1/in/raw/alma/members/29a57b4457b05b7e4ef2787a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `licenses`. Directory installation integrity and creation provenance are not established.
### alma-329108881fcf417d47e10f82

Group: `$USER_HOME/.local/lib/cal-marionette/jinxed/terminfo`. Source: `D1/in/raw/alma/members/329108881fcf417d47e10f82.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-365f8b579c64fcfb2f4e0ac0

Group: `$USER_HOME/.local/lib/cal-marionette/marionette_driver`. Source: `D1/in/raw/alma/members/365f8b579c64fcfb2f4e0ac0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-61b7f12b6d9f36278e375733

Group: `$USER_HOME/.local/lib/cal-marionette/mozdevice`. Source: `D1/in/raw/alma/members/61b7f12b6d9f36278e375733.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-e96e2ab35a81fbdb7c3e1b82

Group: `$USER_HOME/.local/lib/cal-marionette/mozfile`. Source: `D1/in/raw/alma/members/e96e2ab35a81fbdb7c3e1b82.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-5578dfe7a34ad4881953577e

Group: `$USER_HOME/.local/lib/cal-marionette/mozinfo`. Source: `D1/in/raw/alma/members/5578dfe7a34ad4881953577e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-6db56d1518f935d603e064f8

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog`. Source: `D1/in/raw/alma/members/6db56d1518f935d603e064f8.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: formatters,handlers,pytest_mozlog,scripts,unstructured

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `formatters`, `handlers`, `pytest_mozlog`, `scripts`, `unstructured`. Directory installation integrity and creation provenance are not established.
### alma-05272c3f5c89bf56601d0bca

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/formatters`. Source: `D1/in/raw/alma/members/05272c3f5c89bf56601d0bca.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: html

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `html`. Directory installation integrity and creation provenance are not established.
### alma-65332c70093d34d3eea47ac0

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/formatters/html`. Source: `D1/in/raw/alma/members/65332c70093d34d3eea47ac0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-90345759e55cecb686010a22

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/handlers`. Source: `D1/in/raw/alma/members/90345759e55cecb686010a22.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-38ca8ddcc9867bacbd7c5760

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/pytest_mozlog`. Source: `D1/in/raw/alma/members/38ca8ddcc9867bacbd7c5760.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-63aed9f5be6ee974a560931e

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/scripts`. Source: `D1/in/raw/alma/members/63aed9f5be6ee974a560931e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-590292ba9ddb192fac6d6cae

Group: `$USER_HOME/.local/lib/cal-marionette/mozlog/unstructured`. Source: `D1/in/raw/alma/members/590292ba9ddb192fac6d6cae.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-9f0c07a5594acc0a65a68da2

Group: `$USER_HOME/.local/lib/cal-marionette/mozprocess`. Source: `D1/in/raw/alma/members/9f0c07a5594acc0a65a68da2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-d0f5cd91368cb342107e6496

Group: `$USER_HOME/.local/lib/cal-marionette/mozprofile`. Source: `D1/in/raw/alma/members/d0f5cd91368cb342107e6496.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-e417f69ac1fb35d3b5eda638

Group: `$USER_HOME/.local/lib/cal-marionette/mozrunner`. Source: `D1/in/raw/alma/members/e417f69ac1fb35d3b5eda638.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: base,devices

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `base`, `devices`. Directory installation integrity and creation provenance are not established.
### alma-ede9e88a0fcf1e7fdd7cb811

Group: `$USER_HOME/.local/lib/cal-marionette/mozrunner/base`. Source: `D1/in/raw/alma/members/ede9e88a0fcf1e7fdd7cb811.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-eb6c9d434fcf1678fea67019

Group: `$USER_HOME/.local/lib/cal-marionette/mozrunner/devices`. Source: `D1/in/raw/alma/members/eb6c9d434fcf1678fea67019.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-a3ab841f2f4298c5a2b7a219

Group: `$USER_HOME/.local/lib/cal-marionette/mozsystemmonitor`. Source: `D1/in/raw/alma/members/a3ab841f2f4298c5a2b7a219.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-5963a64351037f5b6cb1c15c

Group: `$USER_HOME/.local/lib/cal-marionette/mozterm`. Source: `D1/in/raw/alma/members/5963a64351037f5b6cb1c15c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-614cdcb34d9ae2ce07d9f240

Group: `$USER_HOME/.local/lib/cal-marionette/mozversion`. Source: `D1/in/raw/alma/members/614cdcb34d9ae2ce07d9f240.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-f12eed00667356d7769882af

Group: `$USER_HOME/.local/lib/cal-marionette/psutil`. Source: `D1/in/raw/alma/members/f12eed00667356d7769882af.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-84f6e9e9179c85430536786f

Group: `$USER_HOME/.local/lib/cal-marionette/wcwidth`. Source: `D1/in/raw/alma/members/84f6e9e9179c85430536786f.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: table_grapheme_overrides

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `table_grapheme_overrides`. Directory installation integrity and creation provenance are not established.
### alma-318239de77794939e9831ed1

Group: `$USER_HOME/.local/lib/cal-marionette/wcwidth-0.9.5.dist-info`. Source: `D1/in/raw/alma/members/318239de77794939e9831ed1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `licenses`. Directory installation integrity and creation provenance are not established.
### alma-42631442e81e8c0f515e1dd3

Group: `$USER_HOME/.local/lib/cal-marionette/wcwidth/table_grapheme_overrides`. Source: `D1/in/raw/alma/members/42631442e81e8c0f515e1dd3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-8a7505386adbe0e2413ed766

Group: `$USER_HOME/.local/lib/node_modules`. Source: `D1/in/raw/alma/members/8a7505386adbe0e2413ed766.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cowsay`. Directory installation integrity and creation provenance are not established.
### alma-af27daed7a703d9138e44c5a

Group: `$USER_HOME/.local/lib/node_modules/cowsay`. Source: `D1/in/raw/alma/members/af27daed7a703d9138e44c5a.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `LICENSE`, `README.md`, `cli.js`, `index.d.ts`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `build`, `cows`, `lib`, `node_modules`. Directory installation integrity and creation provenance are not established.
### alma-5451c1a600f09bd58868c590

Group: `$USER_HOME/.local/lib/node_modules/cowsay/build`. Source: `D1/in/raw/alma/members/5451c1a600f09bd58868c590.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `cowsay.es.js`, `cowsay.umd.js`. Package origin, unchangedness, and source of this object are not established.
### alma-c299a482078fc5b7cb4b8229

Group: `$USER_HOME/.local/lib/node_modules/cowsay/cows`. Source: `D1/in/raw/alma/members/c299a482078fc5b7cb4b8229.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `C3PO.cow`, `R2-D2.cow`, `USA.cow`, `ackbar.cow`, `aperture-blank.cow`, `aperture.cow`, `armadillo.cow`, `atat.cow`, `atom.cow`, `awesome-face.cow`, `banana.cow`, `bearface.cow`, `beavis.zen.cow`, `bees.cow`, `bill-the-cat.cow`, `biohazard.cow`, `bishop.cow`, `black-mesa.cow`, `bong.cow`, `box.cow`, `broken-heart.cow`, `bud-frogs.cow`, `bunny.cow`, `cake-with-candles.cow`, `cake.cow`, `cat.cow`, `cat2.cow`, `catfence.cow`, `charizardvice.cow`, `charlie.cow`, `cheese.cow`, `chessmen.cow`, `chito.cow`, `claw-arm.cow`, `clippy.cow`, `companion-cube.cow`, `cower.cow`, `cowfee.cow`, `cthulhu-mini.cow`, `cube.cow`, `daemon.cow`, `dalek-shooting.cow`, `dalek.cow`, `default.cow`, `docker-whale.cow`, `doge.cow`, `dolphin.cow`, `dragon-and-cow.cow`, `dragon.cow`, `ebi_furai.cow`, `elephant-in-snake.cow`, `elephant.cow`, `elephant2.cow`, `explosion.cow`, `eyes.cow`, `fat-banana.cow`, `fat-cow.cow`, `fence.cow`, `fire.cow`, `flaming-sheep.cow`, `fox.cow`, `ghost.cow`, `ghostbusters.cow`, `glados.cow`, `goat.cow`, `goat2.cow`, `golden-eagle.cow`, `hand.cow`, `happy-whale.cow`, `hedgehog.cow`, `hellokitty.cow`, `hippie.cow`, `hiya.cow`, `hiyoko.cow`, `homer.cow`, `hypno.cow`, `ibm.cow`, `iwashi.cow`, `jellyfish.cow`, `karl_marx.cow`, `kilroy.cow`, `king.cow`, `kiss.cow`, `kitten.cow`, `kitty.cow`, `knight.cow`, `koala.cow`, `kosh.cow`, `lamb.cow`, `lamb2.cow`, `lightbulb.cow`, `lobster.cow`, `lollerskates.cow`, `luke-koala.cow`, `mailchimp.cow`, `maze-runner.cow`, `mech-and-cow.cow`, `meow.cow`, `milk.cow`, `minotaur.cow`, `mona-lisa.cow`, `moofasa.cow`, `mooghidjirah.cow`, `moojira.cow`, `moose.cow`, `mule.cow`, `mutilated.cow`, `nyan.cow`, `octopus.cow`, `okazu.cow`, `owl.cow`, `pawn.cow`, `periodic-table.cow`, `personality-sphere.cow`, `pinball-machine.cow`, `psychiatrichelp.cow`, `psychiatrichelp2.cow`, `pterodactyl.cow`, `queen.cow`, `radio.cow`, `ren.cow`, `renge.cow`, `robot.cow`, `robotfindskitten.cow`, `roflcopter.cow`, `rook.cow`, `sachiko.cow`, `satanic.cow`, `seahorse-big.cow`, `seahorse.cow`, `sheep.cow`, `shikato.cow`, `shrug.cow`, `skeleton.cow`, `small.cow`, `smiling-octopus.cow`, `snoopy.cow`, `snoopyhouse.cow`, `snoopysleep.cow`, `spidercow.cow`, `squid.cow`, `squirrel.cow`, `stegosaurus.cow`, `stimpy.cow`, `sudowoodo.cow`, `supermilker.cow`, `surgery.cow`, `tableflip.cow`, `taxi.cow`, `telebears.cow`, `template.cow`, `threader.cow`, `threecubes.cow`, `toaster.cow`, `tortoise.cow`, `turkey.cow`, `turtle.cow`, `tux-big.cow`, `tux.cow`, `tweety-bird.cow`, `vader-koala.cow`, `vader.cow`, `weeping-angel.cow`, `whale.cow`, `wizard.cow`, `wood.cow`, `world.cow`, `www.cow`, `yasuna_01.cow`, `yasuna_02.cow`, `yasuna_03.cow`, `yasuna_03a.cow`, `yasuna_04.cow`, `yasuna_05.cow`, `yasuna_06.cow`, `yasuna_07.cow`, `yasuna_08.cow`, `yasuna_09.cow`, `yasuna_10.cow`, `yasuna_11.cow`, `yasuna_12.cow`, `yasuna_13.cow`, `yasuna_14.cow`, `yasuna_16.cow`, `yasuna_17.cow`, `yasuna_18.cow`, `yasuna_19.cow`, `yasuna_20.cow`, `ymd_udon.cow`, `zen-noh-milk.cow`. Package origin, unchangedness, and source of this object are not established.
### alma-fdecadc52ade076bcda7a8eb

Group: `$USER_HOME/.local/lib/node_modules/cowsay/lib`. Source: `D1/in/raw/alma/members/fdecadc52ade076bcda7a8eb.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `balloon.js`, `cows.js`, `faces.js`, `replacer.js`. Package origin, unchangedness, and source of this object are not established.
### alma-b96b41a4fbe1c092756b9612

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules`. Source: `D1/in/raw/alma/members/b96b41a4fbe1c092756b9612.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ansi-regex`, `ansi-styles`, `camelcase`, `cliui`, `color-convert`, `color-name`, `decamelize`, `emoji-regex`, `find-up`, `get-caller-file`, `get-stdin`, `is-fullwidth-code-point`, `locate-path`, `p-limit`, `p-locate`, `p-try`, `path-exists`, `require-directory`, `require-main-filename`, `set-blocking`, `string-width`, `strip-ansi`, `strip-final-newline`, `which-module`, `wrap-ansi`, `y18n`, `yargs`, `yargs-parser`. Directory installation integrity and creation provenance are not established.
### alma-1270e6e8c836b299ab4094f3

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/ansi-regex`. Source: `D1/in/raw/alma/members/1270e6e8c836b299ab4094f3.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-7c249b4e85c8b62b8d4190ea

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/ansi-styles`. Source: `D1/in/raw/alma/members/7c249b4e85c8b62b8d4190ea.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-a1172fe717274bcb3a77b0f1

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/camelcase`. Source: `D1/in/raw/alma/members/a1172fe717274bcb3a77b0f1.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-a21b5980f2d69a44b6509823

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui`. Source: `D1/in/raw/alma/members/a21b5980f2d69a44b6509823.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE.txt`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `node_modules`. Directory installation integrity and creation provenance are not established.
### alma-e0b9a5a60bbeb8375a158b68

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules`. Source: `D1/in/raw/alma/members/e0b9a5a60bbeb8375a158b68.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ansi-regex`, `is-fullwidth-code-point`, `string-width`, `strip-ansi`. Directory installation integrity and creation provenance are not established.
### alma-e3ac89b4136be2f8fd8390d5

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/ansi-regex`. Source: `D1/in/raw/alma/members/e3ac89b4136be2f8fd8390d5.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-642d8bf8a1aa6fa3d5888a6c

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/is-fullwidth-code-point`. Source: `D1/in/raw/alma/members/642d8bf8a1aa6fa3d5888a6c.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-47ca636a891ff9c67eec35fd

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/string-width`. Source: `D1/in/raw/alma/members/47ca636a891ff9c67eec35fd.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-7ca071d35467ab8f64e2a5d7

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/strip-ansi`. Source: `D1/in/raw/alma/members/7ca071d35467ab8f64e2a5d7.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-0dfae747e06c5824e8c27deb

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/color-convert`. Source: `D1/in/raw/alma/members/0dfae747e06c5824e8c27deb.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE`, `README.md`, `conversions.js`, `index.js`, `package.json`, `route.js`. Package origin, unchangedness, and source of this object are not established.
### alma-949842d9eda0bd8dd6461c9d

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/color-name`. Source: `D1/in/raw/alma/members/949842d9eda0bd8dd6461c9d.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `LICENSE`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-e1590b8c27669a2d935f3869

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/decamelize`. Source: `D1/in/raw/alma/members/e1590b8c27669a2d935f3869.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-0775bdced8f5e336e1899de5

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/emoji-regex`. Source: `D1/in/raw/alma/members/0775bdced8f5e336e1899de5.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `LICENSE-MIT.txt`, `README.md`, `index.d.ts`, `index.js`, `package.json`, `text.js`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `es2015`. Directory installation integrity and creation provenance are not established.
### alma-37fe49b20f1540f9b29bd9cd

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/emoji-regex/es2015`. Source: `D1/in/raw/alma/members/37fe49b20f1540f9b29bd9cd.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `text.js`. Package origin, unchangedness, and source of this object are not established.
### alma-158635226420b9a1ec41f618

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/find-up`. Source: `D1/in/raw/alma/members/158635226420b9a1ec41f618.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-7b4695c1bfab97c08acbf770

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/get-caller-file`. Source: `D1/in/raw/alma/members/7b4695c1bfab97c08acbf770.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `LICENSE.md`, `README.md`, `index.d.ts`, `index.js`, `index.js.map`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-89a3c5f249697f9f1ac2abcc

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/get-stdin`. Source: `D1/in/raw/alma/members/89a3c5f249697f9f1ac2abcc.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-6691ba0f4bbca15e1f342cbb

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/is-fullwidth-code-point`. Source: `D1/in/raw/alma/members/6691ba0f4bbca15e1f342cbb.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-2378d6f274fb58e64d1821e4

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/locate-path`. Source: `D1/in/raw/alma/members/2378d6f274fb58e64d1821e4.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-9dfea5a57bc86f405e3ae0c3

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/p-limit`. Source: `D1/in/raw/alma/members/9dfea5a57bc86f405e3ae0c3.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-0992221176232280ccdcc0b9

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/p-locate`. Source: `D1/in/raw/alma/members/0992221176232280ccdcc0b9.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-3e7e56118eb7c2717607f633

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/p-try`. Source: `D1/in/raw/alma/members/3e7e56118eb7c2717607f633.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-a1fce78f8bf1996a3571087b

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/path-exists`. Source: `D1/in/raw/alma/members/a1fce78f8bf1996a3571087b.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-bde72c953d9e249b906620c5

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/require-directory`. Source: `D1/in/raw/alma/members/bde72c953d9e249b906620c5.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `.jshintrc`, `.npmignore`, `.travis.yml`, `LICENSE`, `README.markdown`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-f7ee01c83482561a2cf042b9

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/require-main-filename`. Source: `D1/in/raw/alma/members/f7ee01c83482561a2cf042b9.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE.txt`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-9e19a4736dd6e6f38c7196ed

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/set-blocking`. Source: `D1/in/raw/alma/members/9e19a4736dd6e6f38c7196ed.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE.txt`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-f0fd38e1a214fd214a189218

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/string-width`. Source: `D1/in/raw/alma/members/f0fd38e1a214fd214a189218.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-d30cd481688f21f09a67fed5

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/strip-ansi`. Source: `D1/in/raw/alma/members/d30cd481688f21f09a67fed5.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-377dda98f5174997e505b29e

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/strip-final-newline`. Source: `D1/in/raw/alma/members/377dda98f5174997e505b29e.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-333afdbdbc9a48e0c6d1708e

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/which-module`. Source: `D1/in/raw/alma/members/333afdbdbc9a48e0c6d1708e.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `LICENSE`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-e7f55306c21a5def7ee20b22

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi`. Source: `D1/in/raw/alma/members/e7f55306c21a5def7ee20b22.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `node_modules`. Directory installation integrity and creation provenance are not established.
### alma-c883ef1d0b21945b42fb9b96

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules`. Source: `D1/in/raw/alma/members/c883ef1d0b21945b42fb9b96.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ansi-regex`, `is-fullwidth-code-point`, `string-width`, `strip-ansi`. Directory installation integrity and creation provenance are not established.
### alma-f926f4778984e259b5281388

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/ansi-regex`. Source: `D1/in/raw/alma/members/f926f4778984e259b5281388.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-b548a7ed608da24a4e5d58d1

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/is-fullwidth-code-point`. Source: `D1/in/raw/alma/members/b548a7ed608da24a4e5d58d1.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-54ed698dbfa0fda9b8ea59df

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/string-width`. Source: `D1/in/raw/alma/members/54ed698dbfa0fda9b8ea59df.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-45c2eda7aec0104a163bbc43

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/strip-ansi`. Source: `D1/in/raw/alma/members/45c2eda7aec0104a163bbc43.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-a1c5c6d8831220ffd972ccaa

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/y18n`. Source: `D1/in/raw/alma/members/a1c5c6d8831220ffd972ccaa.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
### alma-1c92207b67b0c7ebbce8f988

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs`. Source: `D1/in/raw/alma/members/1c92207b67b0c7ebbce8f988.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE`, `README.md`, `index.js`, `package.json`, `yargs.js`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `build`, `locales`, `node_modules`. Directory installation integrity and creation provenance are not established.
### alma-c83f99622553a56e7b5bad36

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs-parser`. Source: `D1/in/raw/alma/members/c83f99622553a56e7b5bad36.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: (not published: orchestration or scratch), `LICENSE.txt`, `README.md`, `index.js`, `package.json`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `lib`. Directory installation integrity and creation provenance are not established.
### alma-88fd59e42e3ab26eeba64167

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs-parser/lib`. Source: `D1/in/raw/alma/members/88fd59e42e3ab26eeba64167.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `tokenize-arg-string.js`. Package origin, unchangedness, and source of this object are not established.
### alma-4fbe01b8a10bfdf3042ff90d

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/build`. Source: `D1/in/raw/alma/members/4fbe01b8a10bfdf3042ff90d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `lib`. Directory installation integrity and creation provenance are not established.
### alma-e91f48a4f4dac062b5c8f92e

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/build/lib`. Source: `D1/in/raw/alma/members/e91f48a4f4dac062b5c8f92e.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `apply-extends.d.ts`, `apply-extends.js`, `argsert.d.ts`, `argsert.js`, `command.d.ts`, `command.js`, `common-types.d.ts`, `common-types.js`, `completion-templates.d.ts`, `completion-templates.js`, `completion.d.ts`, `completion.js`, `is-promise.d.ts`, `is-promise.js`, `levenshtein.d.ts`, `levenshtein.js`, `middleware.d.ts`, `middleware.js`, `obj-filter.d.ts`, `obj-filter.js`, `parse-command.d.ts`, `parse-command.js`, `process-argv.d.ts`, `process-argv.js`, `usage.d.ts`, `usage.js`, `validation.d.ts`, `validation.js`, `yargs.d.ts`, `yargs.js`, `yerror.d.ts`, `yerror.js`. Package origin, unchangedness, and source of this object are not established.
### alma-75895161584b9b74153015d4

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/locales`. Source: `D1/in/raw/alma/members/75895161584b9b74153015d4.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `be.json`, `de.json`, `en.json`, `es.json`, `fi.json`, `fr.json`, `hi.json`, `hu.json`, `id.json`, `it.json`, `ja.json`, `ko.json`, `nb.json`, `nl.json`, `nn.json`, `pirate.json`, `pl.json`, `pt.json`, `pt_BR.json`, `ru.json`, `th.json`, `tr.json`, `zh_CN.json`, `zh_TW.json`. Package origin, unchangedness, and source of this object are not established.
### alma-f29bce251ffeb222f8772825

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules`. Source: `D1/in/raw/alma/members/f29bce251ffeb222f8772825.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ansi-regex`, `is-fullwidth-code-point`, `string-width`, `strip-ansi`. Directory installation integrity and creation provenance are not established.
### alma-2692e186951aa3010b5e5bf6

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/ansi-regex`. Source: `D1/in/raw/alma/members/2692e186951aa3010b5e5bf6.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-bb5cfd1cad56acbe5768e45f

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/is-fullwidth-code-point`. Source: `D1/in/raw/alma/members/bb5cfd1cad56acbe5768e45f.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-da78eefbf5cf48a9769ecc39

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/string-width`. Source: `D1/in/raw/alma/members/da78eefbf5cf48a9769ecc39.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-37e64d66a42b19ce6becc67d

Group: `$USER_HOME/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/strip-ansi`. Source: `D1/in/raw/alma/members/37e64d66a42b19ce6becc67d.tsv`. Decision: **UNKNOWN**.

Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.

- **UNKNOWN**: `index.d.ts`, `index.js`, `license`, `package.json`, `readme.md`. Package origin, unchangedness, and source of this object are not established.
### alma-30b8a4877604fc3ce69702cf

Group: `$USER_HOME/.local/share`. Source: `D1/in/raw/alma/members/30b8a4877604fc3ce69702cf.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `flatpak`. Directory installation integrity and creation provenance are not established.
### alma-b24be7f4f7977de4f3816ed9

Group: `$USER_HOME/.local/state`. Source: `D1/in/raw/alma/members/b24be7f4f7977de4f3816ed9.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `wireplumber`. Directory installation integrity and creation provenance are not established.
### alma-fe77e80e3fd7cf8e98e1112a

Group: `$USER_HOME/.mozilla`. Source: `D1/in/raw/alma/members/fe77e80e3fd7cf8e98e1112a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `extensions`, `firefox`, `plugins`. Directory installation integrity and creation provenance are not established.
### alma-c32745a6dc6001e9c5aa4507

Group: `$USER_HOME/.mozilla/extensions`. Source: `D1/in/raw/alma/members/c32745a6dc6001e9c5aa4507.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `{<REDACTED>}`. Directory installation integrity and creation provenance are not established.
### alma-348bb79b986dbca1f56dc09d

Group: `$USER_HOME/.mozilla/firefox`. Source: `D1/in/raw/alma/members/348bb79b986dbca1f56dc09d.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `Profile Groups`, `cal-check`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `profiles.ini`. Package origin, unchangedness, and source of this object are not established.
### alma-7451256905844be0a90a5db3

Group: `$USER_HOME/.mozilla/firefox/Profile Groups`. Source: `D1/in/raw/alma/members/7451256905844be0a90a5db3.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `662af698.sqlite`, `662af698.sqlite-shm`, `662af698.sqlite-wal`. Package origin, unchangedness, and source of this object are not established.
### alma-a647fcfdbb97b91e83721827

Group: `$USER_HOME/.mozilla/firefox/cal-check`. Source: `D1/in/raw/alma/members/a647fcfdbb97b91e83721827.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.parentlock`, `AlternateServices.bin`, `addonStartup.json.lz4`, `bounce-tracking-protection.sqlite`, `cert9.db`, `compatibility.ini`, `containers.json`, `content-prefs.sqlite`, `cookies.sqlite`, `domain_to_categories.sqlite`, `domain_to_categories.sqlite-journal`, `extension-preferences.json`, `extensions.json`, `favicons.sqlite`, `favicons.sqlite-wal`, `handlers.json`, `key4.db`, `lock`, `logins.db`, `permissions.sqlite`, `pkcs11.txt`, `places.sqlite`, `places.sqlite-wal`, `prefs.js`, `search.json.mozlz4`, `sessionCheckpoints.json`, `sessionstore.jsonlz4`, `shield-preference-experiments.json`, `storage.sqlite`, `times.json`, `user.js`, `xulstore.json`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `bookmarkbackups`, `datareporting`, `extension-store`, `extension-store-menus`, `extensions`, `minidumps`, `saved-telemetry-pings`, `security_state`, `sessionstore-backups`, `storage`. Directory installation integrity and creation provenance are not established.
### alma-d339cf6a31d98b03365f7a68

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting`. Source: `D1/in/raw/alma/members/d339cf6a31d98b03365f7a68.tsv`. Decision: **MIXED**.

RECORD: archived; UNKNOWN: glean,session-(not published: orchestration),(not published: orchestration)

- **RECORD**: `archived`. Firefox telemetry archive data or archive directories.
- **UNKNOWN**: `glean`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `session-(not published: orchestration)`, (not published: orchestration or scratch). Package origin, unchangedness, and source of this object are not established.
### alma-79efb6217a0f36e156face9f

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting/archived`. Source: `D1/in/raw/alma/members/79efb6217a0f36e156face9f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2026-11`. Firefox telemetry archive data or archive directories.
### alma-957415b00f32bef9aa843279

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting/archived/2026-11`. Source: `D1/in/raw/alma/members/957415b00f32bef9aa843279.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1795432656284.<REDACTED>.deletion-request.jsonlz4`, `1795432657992.<REDACTED>.new-profile.jsonlz4`, `1795432657994.<REDACTED>.event.jsonlz4`, `1795432657996.<REDACTED>.main.jsonlz4`, `1795432657997.<REDACTED>.first-shutdown.jsonlz4`. Firefox telemetry archive data or archive directories.
### alma-b75dc674c04eed6655f1b094

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting/glean`. Source: `D1/in/raw/alma/members/b75dc674c04eed6655f1b094.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `client_id.txt`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `db`, `events`, `pending_pings`, `tmp`. Directory installation integrity and creation provenance are not established.
### alma-0336b412c46c7bbcb7b0243b

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting/glean/db`. Source: `D1/in/raw/alma/members/0336b412c46c7bbcb7b0243b.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `data.safe.bin`. Package origin, unchangedness, and source of this object are not established.
### alma-dcea14bb07274a1f8b10b905

Group: `$USER_HOME/.mozilla/firefox/cal-check/datareporting/glean/events`. Source: `D1/in/raw/alma/members/dcea14bb07274a1f8b10b905.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `events`. Package origin, unchangedness, and source of this object are not established.
### alma-7244a18cf0230e6528ca4146

Group: `$USER_HOME/.mozilla/firefox/cal-check/extension-store`. Source: `D1/in/raw/alma/members/7244a18cf0230e6528ca4146.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `data.safe.bin`. Package origin, unchangedness, and source of this object are not established.
### alma-2ea4b9f74eb9ce06f9d317ff

Group: `$USER_HOME/.mozilla/firefox/cal-check/extensions`. Source: `D1/in/raw/alma/members/2ea4b9f74eb9ce06f9d317ff.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `{<REDACTED>}.xpi`. Package origin, unchangedness, and source of this object are not established.
### alma-96501029e1b2761aea916f88

Group: `$USER_HOME/.mozilla/firefox/cal-check/saved-telemetry-pings`. Source: `D1/in/raw/alma/members/96501029e1b2761aea916f88.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `<REDACTED>`. Package origin, unchangedness, and source of this object are not established.
### alma-88e56ad90f1a81b69caa3d64

Group: `$USER_HOME/.mozilla/firefox/cal-check/security_state`. Source: `D1/in/raw/alma/members/88e56ad90f1a81b69caa3d64.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `data.safe.bin`. Package origin, unchangedness, and source of this object are not established.
### alma-b9e9d69af26557379347fbfc

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage`. Source: `D1/in/raw/alma/members/b9e9d69af26557379347fbfc.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `default`, `permanent`, `temporary`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `ls-archive.sqlite`. Package origin, unchangedness, and source of this object are not established.
### alma-830f5df537f0a586a68f3e6b

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/default`. Source: `D1/in/raw/alma/members/830f5df537f0a586a68f3e6b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `moz-extension+++<REDACTED>^userContextId=4294967295`. Directory installation integrity and creation provenance are not established.
### alma-6f975c3c92cedef1dfb594bd

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/default/moz-extension+++<REDACTED>^userContextId=4294967295`. Source: `D1/in/raw/alma/members/6f975c3c92cedef1dfb594bd.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.metadata-v2`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `idb`. Directory installation integrity and creation provenance are not established.
### alma-13958403d1042f2cc768a6ee

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/default/moz-extension+++<REDACTED>^userContextId=4294967295/idb`. Source: `D1/in/raw/alma/members/13958403d1042f2cc768a6ee.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `3647222921wleabcEoxlt-eengsairo.files`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `3647222921wleabcEoxlt-eengsairo.sqlite`, `3647222921wleabcEoxlt-eengsairo.sqlite-wal`. Package origin, unchangedness, and source of this object are not established.
### alma-8f7f2ff3beae15642f011da1

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/permanent`. Source: `D1/in/raw/alma/members/8f7f2ff3beae15642f011da1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `chrome`. Directory installation integrity and creation provenance are not established.
### alma-2f04803e69d18d59751cf174

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/permanent/chrome`. Source: `D1/in/raw/alma/members/2f04803e69d18d59751cf174.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.metadata-v2`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `idb`. Directory installation integrity and creation provenance are not established.
### alma-00c32c6e7ef078929ed36d12

Group: `$USER_HOME/.mozilla/firefox/cal-check/storage/permanent/chrome/idb`. Source: `D1/in/raw/alma/members/00c32c6e7ef078929ed36d12.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `1451318868ntouromlalnodry--epcr.files`, `1657114595AmcateirvtiSty.files`, `2823318777ntouromlalnodry--naod.files`, `2918063365piupsah.files`, `3561288849sdhlie.files`, `3870112724rsegmnoittet-es.files`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `1451318868ntouromlalnodry--epcr.sqlite`, `1451318868ntouromlalnodry--epcr.sqlite-wal`, `1657114595AmcateirvtiSty.sqlite`, `1657114595AmcateirvtiSty.sqlite-wal`, `2823318777ntouromlalnodry--naod.sqlite`, `2823318777ntouromlalnodry--naod.sqlite-wal`, `2918063365piupsah.sqlite`, `2918063365piupsah.sqlite-wal`, `3561288849sdhlie.sqlite`, `3561288849sdhlie.sqlite-wal`, `3870112724rsegmnoittet-es.sqlite`, `3870112724rsegmnoittet-es.sqlite-wal`. Package origin, unchangedness, and source of this object are not established.
### alma-8cb98287a3975b39eca4ceb4

Group: `$USER_HOME/.npm`. Source: `D1/in/raw/alma/members/8cb98287a3975b39eca4ceb4.tsv`. Decision: **MIXED**.

RECORD: _cacache; UNKNOWN: _logs

- **RECORD**: `_cacache`. Npm content cache or its directory, not an installed package.
- **UNKNOWN**: `_logs`. Directory installation integrity and creation provenance are not established.
### alma-717dc96f4762ba06728d28eb

Group: `$USER_HOME/.npm/_cacache`. Source: `D1/in/raw/alma/members/717dc96f4762ba06728d28eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `content-v2`, `index-v5`, `tmp`. Npm content cache or its directory, not an installed package.
### alma-b4545c0a3a3779b419d3b70c

Group: `$USER_HOME/.npm/_cacache/content-v2`. Source: `D1/in/raw/alma/members/b4545c0a3a3779b419d3b70c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `sha512`. Npm content cache or its directory, not an installed package.
### alma-b898a6e6ef1aa6250c59a472

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512`. Source: `D1/in/raw/alma/members/b898a6e6ef1aa6250c59a472.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `00`, `06`, `0b`, `0c`, `0d`, `0e`, `0f`, `12`, `20`, `24`, `2a`, `2f`, `31`, `34`, `3c`, `3e`, `45`, `47`, `50`, `54`, `5d`, `63`, `67`, `69`, `6a`, `72`, `74`, `7c`, `7d`, `80`, `88`, `9c`, `9d`, `a3`, `a4`, `aa`, `ac`, `af`, `b1`, `b5`, `b7`, `bb`, `bd`, `c0`, `cd`, `ce`, `cf`, `d4`, `e1`, `f0`, `f5`, `f8`, `ff`. Npm content cache or its directory, not an installed package.
### alma-3e3aeee6e7b69ec2a4b05ee6

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/00`. Source: `D1/in/raw/alma/members/3e3aeee6e7b69ec2a4b05ee6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `44`. Npm content cache or its directory, not an installed package.
### alma-0e0536bc612d51064a990bdb

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/00/44`. Source: `D1/in/raw/alma/members/0e0536bc612d51064a990bdb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3a22b0469fe953c57a0589bb57c7240719aace83ba33bad98f88b4cc69c0434f84b6938e92c420df991f61b5df019ab4c68b7ca1ba2ef294cdc0a50665a7`. Npm content cache or its directory, not an installed package.
### alma-f39fae3a762c167a0849fb15

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/06`. Source: `D1/in/raw/alma/members/f39fae3a762c167a0849fb15.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ba`. Npm content cache or its directory, not an installed package.
### alma-527966d4a61b715e36c33e63

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/06/ba`. Source: `D1/in/raw/alma/members/527966d4a61b715e36c33e63.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6f7cd004ddd72fabb965df156e9b38ca8d9439b48d6c11420aaf752892cd17525e394addc595ab55a9e7fda6b9388d10f3856e96660fb76e4f77cbaa4b8c`. Npm content cache or its directory, not an installed package.
### alma-35fbe0ff7927d858af595d9a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0b`. Source: `D1/in/raw/alma/members/35fbe0ff7927d858af595d9a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `51`. Npm content cache or its directory, not an installed package.
### alma-050df0d440cce8d3d7c77085

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0b/51`. Source: `D1/in/raw/alma/members/050df0d440cce8d3d7c77085.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `cd1222332a29441feae02e2bb3ba6c9d3991f268f6e8e6a81efb6c95b9ef89413976f159ea820450bd4e97946aa0a108e8c37edf3a13694ed470b646681f`. Npm content cache or its directory, not an installed package.
### alma-ea2f5d92f23d6a5f948f68c1

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0c`. Source: `D1/in/raw/alma/members/ea2f5d92f23d6a5f948f68c1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `68`. Npm content cache or its directory, not an installed package.
### alma-9165cf39357fb748a850ee8f

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0c/68`. Source: `D1/in/raw/alma/members/9165cf39357fb748a850ee8f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d6f724fed4545f226a19eda593468803654cbce0d6cbe326fb527940920b93f4d5f6360b05aefc5495faa369f92ea1fabab003573af4db69d5e1b699837c`. Npm content cache or its directory, not an installed package.
### alma-10fd729f96f880f422513687

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0d`. Source: `D1/in/raw/alma/members/10fd729f96f880f422513687.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4c`. Npm content cache or its directory, not an installed package.
### alma-22ea2eeda0ecaab9fc67e36a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0d/4c`. Source: `D1/in/raw/alma/members/22ea2eeda0ecaab9fc67e36a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `573d246ddcb6390ec4e5a7d91c72b23a17bbd309f485cbd12937e84b614396cbb8ad2fd410d58f14c859a858fe97a8bad2866fe6373f98fdfe9547043b93`. Npm content cache or its directory, not an installed package.
### alma-47e5ea683d515627b9ba8a0d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0e`. Source: `D1/in/raw/alma/members/47e5ea683d515627b9ba8a0d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `99`. Npm content cache or its directory, not an installed package.
### alma-fc6ef0cbefd4b6c538a9a7a5

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0e/99`. Source: `D1/in/raw/alma/members/fc6ef0cbefd4b6c538a9a7a5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b3880c199320ed10b596915afad4965c211ccc2c742c41c2053c59e98e436b86fb029469d6e3b779a379ba7c36d5792fd5a342df79cb836d3fbb441471a9`. Npm content cache or its directory, not an installed package.
### alma-54fbea61a43493ac95e15bb5

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0f`. Source: `D1/in/raw/alma/members/54fbea61a43493ac95e15bb5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `21`. Npm content cache or its directory, not an installed package.
### alma-d907ae0c16e2126adfcb8fff

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/0f/21`. Source: `D1/in/raw/alma/members/d907ae0c16e2126adfcb8fff.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4fdc133fdd81d340e0942ffc343991d1d25a4a786af1a2d70759ca8d11d9e5b6a1705d57e110143de1e228df801f429a34ac6922e1cc8889fb58d3a87616`. Npm content cache or its directory, not an installed package.
### alma-af11fc7a7b2f5c8bb68cba39

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/12`. Source: `D1/in/raw/alma/members/af11fc7a7b2f5c8bb68cba39.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2f`. Npm content cache or its directory, not an installed package.
### alma-e1af3f16ee2cf369ac09ec6d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/12/2f`. Source: `D1/in/raw/alma/members/e1af3f16ee2cf369ac09ec6d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0c8aaa040801e58e03051a85d65d332a4694cc616d803f0b9ced5be1ddf9fc21439370cdadfd339ff62f3211b5aef8bece38718f36479138ba8647d87b19`. Npm content cache or its directory, not an installed package.
### alma-6a9e2647e5fb7abd9c3bd735

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/20`. Source: `D1/in/raw/alma/members/6a9e2647e5fb7abd9c3bd735.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `fd`. Npm content cache or its directory, not an installed package.
### alma-9cd9ef4fab08bdb99410bae8

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/20/fd`. Source: `D1/in/raw/alma/members/9cd9ef4fab08bdb99410bae8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7fed085bb5baf1012495bf3588ef294ba6f149592fae71febfb0981fb8d805e5ab4275f890fb3d85bf58bbada36b7e8c788f4ee64513ca1d0a492006c12a`. Npm content cache or its directory, not an installed package.
### alma-42e727038b620c9b301a9cb7

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/24`. Source: `D1/in/raw/alma/members/42e727038b620c9b301a9cb7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `58`, `63`, `a8`. Npm content cache or its directory, not an installed package.
### alma-831bc0eb3be2eb883e7aa293

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/24/58`. Source: `D1/in/raw/alma/members/831bc0eb3be2eb883e7aa293.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c46baf88504d137b15be0388961388e5988bdde66ab1b14e273af36fff77430c918072125e4228bc47005bf5b50bbdbca0c551dfeffab9a7470bbd4159a7`. Npm content cache or its directory, not an installed package.
### alma-fe3febb8de43cf6aa9d08dc8

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/24/63`. Source: `D1/in/raw/alma/members/fe3febb8de43cf6aa9d08dc8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ccf5baa847b900c2575cea2408ae12bd40e4598818e264681062e42479f3457ac6ed517a1f5cfd18abc3c5bdad9f030b9be30ab00e3bb1af4c096c955fb5`. Npm content cache or its directory, not an installed package.
### alma-eafb3abb8a3220f10d317718

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/24/a8`. Source: `D1/in/raw/alma/members/eafb3abb8a3220f10d317718.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6a4cec12aea340d4d639952ced2751ab06252874b326219b8b88368c449fa2b4577e001544f170633af2162fead2a8d0c2ef82c24859a56ff538519e2125`. Npm content cache or its directory, not an installed package.
### alma-6a6a6e21a7e04c14e0254d65

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/2a`. Source: `D1/in/raw/alma/members/6a6a6e21a7e04c14e0254d65.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `22`. Npm content cache or its directory, not an installed package.
### alma-498f88d56afa6ddf56339aa0

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/2a/22`. Source: `D1/in/raw/alma/members/498f88d56afa6ddf56339aa0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `814bc0275861322f3a1f15f9af2b0a5d3f3aa2cb5e8bbd07cadf2bff7d51fb063d77ff097725247527eadf81113dabbc5424ae2abe04bcada48e78b51e87`. Npm content cache or its directory, not an installed package.
### alma-c9b90c55f318f585ec9d7f70

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/2f`. Source: `D1/in/raw/alma/members/c9b90c55f318f585ec9d7f70.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6f`. Npm content cache or its directory, not an installed package.
### alma-233fbf7e10b7de580dad74bb

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/2f/6f`. Source: `D1/in/raw/alma/members/233fbf7e10b7de580dad74bb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `124c1d7bd27c164badd48ed944384ddd95d400a5a257664388d6e3057f37f7ad1b8f7a01da1deb3279ef98c50f96e92bd10d057a52b74e751891d79df026`. Npm content cache or its directory, not an installed package.
### alma-fc4ed6983601fd22e3af84a2

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/31`. Source: `D1/in/raw/alma/members/fc4ed6983601fd22e3af84a2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `28`. Npm content cache or its directory, not an installed package.
### alma-650027f27cf6f2a3e8dc6f90

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/31/28`. Source: `D1/in/raw/alma/members/650027f27cf6f2a3e8dc6f90.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d8cdc58d380d1ec001e9cf4331a5816fc20eb28f2d4d1b7c6d7a8ab3eb8e150a8fd13e09ebd7f186b7e89cde2253cd0f04bb74dd335e126b09d5526184e8`. Npm content cache or its directory, not an installed package.
### alma-6d32d5eb50f3257e4656b2f0

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/34`. Source: `D1/in/raw/alma/members/6d32d5eb50f3257e4656b2f0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a3`. Npm content cache or its directory, not an installed package.
### alma-e06499d01a656c8790e16ca6

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/34/a3`. Source: `D1/in/raw/alma/members/e06499d01a656c8790e16ca6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7990c0f294aba577160b4947eb6e8e53bb387885dfb613c34f3d7d36999b67d55b911104e861efd9765272f89dee0a97da886174e5eec1f16d225db4079a`. Npm content cache or its directory, not an installed package.
### alma-458fa6c7859b29885e99a741

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/3c`. Source: `D1/in/raw/alma/members/458fa6c7859b29885e99a741.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `54`. Npm content cache or its directory, not an installed package.
### alma-65d3254d40b0155b0495eb21

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/3c/54`. Source: `D1/in/raw/alma/members/65d3254d40b0155b0495eb21.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `291cc2d70977c802da47b33549e015b4d14f25cdd383e960bafcfb84de124bd21aa9c763ef9d5d885d8049e625d038b71c8b6cc6d35b0c70840624d2649e`. Npm content cache or its directory, not an installed package.
### alma-ad853e79d6c0f36fe3def2bf

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/3e`. Source: `D1/in/raw/alma/members/ad853e79d6c0f36fe3def2bf.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `93`. Npm content cache or its directory, not an installed package.
### alma-35c4a39258e7a4717d49bef7

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/3e/93`. Source: `D1/in/raw/alma/members/35c4a39258e7a4717d49bef7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b001d43f6255d0daf8fc6b787c222a43b98462df071e550406616c4d20d71cab8d009f0ec196c11708c6edd59b7e38b03a16af6cb88a48583d0eb2721297`. Npm content cache or its directory, not an installed package.
### alma-a0f2c61fece75d15549cb871

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/45`. Source: `D1/in/raw/alma/members/a0f2c61fece75d15549cb871.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `11`. Npm content cache or its directory, not an installed package.
### alma-9f61a87c26e0e6c2641a8f4e

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/45/11`. Source: `D1/in/raw/alma/members/9f61a87c26e0e6c2641a8f4e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `023ec8fb8aeff16f9a0a61cb051d2a6914d9ec8ffe763954d129be333f9a275f0545df3566993a0d70e7c60be0910e97cafd4e7ce1f320dfc64709a12529`. Npm content cache or its directory, not an installed package.
### alma-4d149f4bf9989b0f398d9756

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/47`. Source: `D1/in/raw/alma/members/4d149f4bf9989b0f398d9756.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `89`, `bf`. Npm content cache or its directory, not an installed package.
### alma-a03730f736a6f1b2f7536843

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/47/89`. Source: `D1/in/raw/alma/members/a03730f736a6f1b2f7536843.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `cf0154c053407d0f7e7f1a4dee25fffb5d86d0732a2148a76f03121148d821165e1eef5855a069c1350cfd716697c4ed88d742930bede331dbefa0ac3a75`. Npm content cache or its directory, not an installed package.
### alma-d822e7e523a68bc1be552fd4

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/47/bf`. Source: `D1/in/raw/alma/members/d822e7e523a68bc1be552fd4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5967fd30031286bb7a18325cfc8f2fe46e1b0dad2ed2299ecfc441c1809e7e1769ad156d9f2b670eb4187570762442c6f3155ec8f84a1129ee98b74a0aec`. Npm content cache or its directory, not an installed package.
### alma-d31e179ae38cd401fe5fa80f

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/50`. Source: `D1/in/raw/alma/members/d31e179ae38cd401fe5fa80f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `92`. Npm content cache or its directory, not an installed package.
### alma-8a01240cbe28d7d45e7ef97a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/50/92`. Source: `D1/in/raw/alma/members/8a01240cbe28d7d45e7ef97a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e4247a4f512e9452503f6e2e4316ad2e23d7f70d184e657c5b33c6d9c33ccfee8ac95a552d306442142795ea2eb983cdc464ee94da70d980af27b6077e31`. Npm content cache or its directory, not an installed package.
### alma-ec0291f481633938f0d1c22e

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/54`. Source: `D1/in/raw/alma/members/ec0291f481633938f0d1c22e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7b`. Npm content cache or its directory, not an installed package.
### alma-a2123328bbe544b174c8e3a7

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/54/7b`. Source: `D1/in/raw/alma/members/a2123328bbe544b174c8e3a7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2400a60cf117d2157c1e7b9b7971b3793d97aad56ae1eaa7796e4ca25c87fa51070deb0fc0d1e5ccf6beadf1df8660e87ea3a6618849dbf3c2cdfd8f26db`. Npm content cache or its directory, not an installed package.
### alma-50db5410f9afa933aae0db4b

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/5d`. Source: `D1/in/raw/alma/members/50db5410f9afa933aae0db4b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f5`. Npm content cache or its directory, not an installed package.
### alma-658e9964bf1cd618fb4e3ad2

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/5d/f5`. Source: `D1/in/raw/alma/members/658e9964bf1cd618fb4e3ad2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0b20bc0e463eb11b8b0f835c1e4bf050700583c94d9262c0ad582d8ff7745993deaa951832740a622d307f86e87559b4585f6de25d9170059b7ae5f19bfa`. Npm content cache or its directory, not an installed package.
### alma-8acb8a5ab8bd04d2228e0145

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/63`. Source: `D1/in/raw/alma/members/8acb8a5ab8bd04d2228e0145.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7f`, `92`. Npm content cache or its directory, not an installed package.
### alma-ecd058c72c7ad9eb166f43f9

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/63/7f`. Source: `D1/in/raw/alma/members/ecd058c72c7ad9eb166f43f9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `153d21dcaa416b0a916743dbee4979aabaebf9a1738aa46793e9a1abaf7a3719cf409556ba2417d448e0a76f1186645fbfd28a08ecaacfb944b3b54754e4`. Npm content cache or its directory, not an installed package.
### alma-dced29d25e3ed756c4dbca5d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/63/92`. Source: `D1/in/raw/alma/members/dced29d25e3ed756c4dbca5d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `627341a40db084af786ec601197944068adaa557b6389acfd486ea46cdd8dbbd214519c8062174e3c6c69b38c64f4229564006c2cbd0cfa82b435c2e3cbd`. Npm content cache or its directory, not an installed package.
### alma-07af33e823af3bb26a298fbb

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/67`. Source: `D1/in/raw/alma/members/07af33e823af3bb26a298fbb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3a`. Npm content cache or its directory, not an installed package.
### alma-566967717b0928eb59caf419

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/67/3a`. Source: `D1/in/raw/alma/members/566967717b0928eb59caf419.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ecae41cbd3bbd7fc73898f4c211d1c1f44c878ea7d04ea66fd4222bc54fa195a23a1482ca17bc09866ae323f3c92b8cc0cc568839871d5b37334d760f1b3`. Npm content cache or its directory, not an installed package.
### alma-483a998e2f2f9efc4e278b34

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/69`. Source: `D1/in/raw/alma/members/483a998e2f2f9efc4e278b34.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e3`. Npm content cache or its directory, not an installed package.
### alma-28105ca86106e68aa34f2a8f

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/69/e3`. Source: `D1/in/raw/alma/members/28105ca86106e68aa34f2a8f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `dbc4399c616fbe3daa81b09f8761417009dbf82d5bdd9e1072efc139ecf228afcfce56f84cac00c51440e1f031c3151bff3bd8b794f86c10d8ceed05f4f8`. Npm content cache or its directory, not an installed package.
### alma-ba329ddf7a47c0648fcc2e0a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/6a`. Source: `D1/in/raw/alma/members/ba329ddf7a47c0648fcc2e0a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4f`. Npm content cache or its directory, not an installed package.
### alma-a592096921f99c01c01f6abf

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/6a/4f`. Source: `D1/in/raw/alma/members/a592096921f99c01c01f6abf.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `50cb943b8d86f65b071ecb9169be0d8aa0073f64884b48b392066466ca03ec1b091556dd1f65ad2aaed333fa6ead2530077d943c167981e0c1b82d6cbbff`. Npm content cache or its directory, not an installed package.
### alma-a3da8a75ce91378e2d94b3e4

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/72`. Source: `D1/in/raw/alma/members/a3da8a75ce91378e2d94b3e4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `13`. Npm content cache or its directory, not an installed package.
### alma-d6d186ac3d0d708e7ec30528

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/72/13`. Source: `D1/in/raw/alma/members/d6d186ac3d0d708e7ec30528.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ad5112ce31a1bda765d1adce97bb124ec474f53088b70e39bd01c83cd7518d96acbc710c0de43adc2e84ef8c4e99570e2ed02adf471a791e93db8738ee3f`. Npm content cache or its directory, not an installed package.
### alma-ac0a4211b3439de228372b36

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/74`. Source: `D1/in/raw/alma/members/ac0a4211b3439de228372b36.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ec`. Npm content cache or its directory, not an installed package.
### alma-d0ecd22b80cd4d07d5cc143d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/74/ec`. Source: `D1/in/raw/alma/members/d0ecd22b80cd4d07d5cc143d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `bedc0b96ddadb035b64722e319a537208c6b8b53fb812ffb9b71917d3976c3a3c7dfe0ef32569e417f479f4bcb84a18a39ab8171edd63d3a04065e002c40`. Npm content cache or its directory, not an installed package.
### alma-dda966a4d8aacd7c69a4fee5

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/7c`. Source: `D1/in/raw/alma/members/dda966a4d8aacd7c69a4fee5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0a`, `6c`. Npm content cache or its directory, not an installed package.
### alma-83fde391729865e65ae547c7

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/7c/0a`. Source: `D1/in/raw/alma/members/83fde391729865e65ae547c7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4a5163e85babaf17652051b925a02e4e83cbd2197a295d1fd6a11c1606742371182dfa21f7086562bf8f2fe2b4f55c133beb80ba5e525f07dfbef823d0e2`. Npm content cache or its directory, not an installed package.
### alma-10109fc684bf56e31882ef1b

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/7c/6c`. Source: `D1/in/raw/alma/members/10109fc684bf56e31882ef1b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4423bfb0b06f71aef763b2b9662f6d8e3134e21d1c0032ba2211e320abc833a0b0bf3d0afb46c4434932d483f6d9019b45f9354890773aff84482abba2f9`. Npm content cache or its directory, not an installed package.
### alma-ab96a6c032b4f577536d3c01

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/7d`. Source: `D1/in/raw/alma/members/ab96a6c032b4f577536d3c01.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `27`. Npm content cache or its directory, not an installed package.
### alma-4da22257b157b58ae0c3459a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/7d/27`. Source: `D1/in/raw/alma/members/4da22257b157b58ae0c3459a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9dbddc1a9aba6e32f3cb9271ba29dda878040c4f824bcdb4aad454fade6feb646a0c61d2767645346c4252a5be6a0ac4aeb38eec0439e8d7d1d46bafd727`. Npm content cache or its directory, not an installed package.
### alma-32aa0508ca855e42feaa3bf3

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/80`. Source: `D1/in/raw/alma/members/32aa0508ca855e42feaa3bf3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4c`. Npm content cache or its directory, not an installed package.
### alma-34c201a3900d89c161730b09

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/80/4c`. Source: `D1/in/raw/alma/members/34c201a3900d89c161730b09.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `55d33a5ab8110f2769122bc27d6f35ea94c2a0b9450dc16f94d858a31d7447c329d5465cd2d6614e945663179073dde3e1828c9c29cf32b79ae22838e007`. Npm content cache or its directory, not an installed package.
### alma-948bd9ee0f8ca6bf40a4700d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/88`. Source: `D1/in/raw/alma/members/948bd9ee0f8ca6bf40a4700d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `17`. Npm content cache or its directory, not an installed package.
### alma-bd90f0fe3d48e9fd0aaa85c6

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/88/17`. Source: `D1/in/raw/alma/members/bd90f0fe3d48e9fd0aaa85c6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `59e7b443be7391f4018184c2f6bc565fee1f2f9818e1a1a66a3832411561d5b4a90398ab876a2ddcc793e054cad7e580cda76ec0a1f61b03072d492faf85`. Npm content cache or its directory, not an installed package.
### alma-ed03472e987b1c61a7479c8c

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/9c`. Source: `D1/in/raw/alma/members/ed03472e987b1c61a7479c8c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ea`. Npm content cache or its directory, not an installed package.
### alma-d6887f240df97e04f010d3e5

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/9c/ea`. Source: `D1/in/raw/alma/members/d6887f240df97e04f010d3e5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `87e7d75e0aaf52447971ab5030f39267b78c3a2af2caa9656293aa00f599255cb3483a5aa0e05db2ad3d4c55a4e302abd5c1d7de67bc3b682bc90fbba093`. Npm content cache or its directory, not an installed package.
### alma-9e0fc259c822561a9dce2700

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/9d`. Source: `D1/in/raw/alma/members/9e0fc259c822561a9dce2700.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ad`. Npm content cache or its directory, not an installed package.
### alma-7d6547eef6121e988edcfcce

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/9d/ad`. Source: `D1/in/raw/alma/members/7d6547eef6121e988edcfcce.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8beae5d08de90eb68bd40a858c4d4bc7da8b723299a32cef0bcf55a877917682a93f82e75da697c85a1efa7df658bc61f2e7fb43695bbac165c405dc58d6`. Npm content cache or its directory, not an installed package.
### alma-2a9fc93e8c5433fab1b98e66

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/a3`. Source: `D1/in/raw/alma/members/2a9fc93e8c5433fab1b98e66.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9d`. Npm content cache or its directory, not an installed package.
### alma-e735dc51f193f80eb5e7ace4

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/a3/9d`. Source: `D1/in/raw/alma/members/e735dc51f193f80eb5e7ace4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `23d09793a32ff82ba39971a4265ba9725d72a1abb72c4445dc0f0936a2614f244c1434e56d24abe60ebf442357c025953265c445ee4c460569915ee76b09`. Npm content cache or its directory, not an installed package.
### alma-b23a8edd0a14553c7aba2987

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/a4`. Source: `D1/in/raw/alma/members/b23a8edd0a14553c7aba2987.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `33`. Npm content cache or its directory, not an installed package.
### alma-4d55d25026fe100fbd8f460d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/a4/33`. Source: `D1/in/raw/alma/members/4d55d25026fe100fbd8f460d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `bb70a7af78e3cc3119d65c1b5010a868fbc68820acf4b20220e88b74f095463dd39ed250c8b8396d880abe74004bec095adc5fe8850d2ff73d33de78d32e`. Npm content cache or its directory, not an installed package.
### alma-397cd0021a632641d565b9d2

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/aa`. Source: `D1/in/raw/alma/members/397cd0021a632641d565b9d2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e2`. Npm content cache or its directory, not an installed package.
### alma-096c13f5e28309c7b0a4b3c0

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/aa/e2`. Source: `D1/in/raw/alma/members/096c13f5e28309c7b0a4b3c0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `505e54d25062f62c7f52517a3c570b18e2ca1a9e1828e8b3529bce04d4b05c13cb373b4c29762473c91f73fd9649325316bf7eea38e6fda5d26531410a15`. Npm content cache or its directory, not an installed package.
### alma-c1fa92ebd584fabb6e69a8f1

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ac`. Source: `D1/in/raw/alma/members/c1fa92ebd584fabb6e69a8f1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c7`. Npm content cache or its directory, not an installed package.
### alma-18fa82d69d12cb2e613db225

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ac/c7`. Source: `D1/in/raw/alma/members/18fa82d69d12cb2e613db225.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `55dcc2f9d6d5171aea15f1d81fd4f48211a8895276bcaa241c1b16be893a90b76770583bd9e39e093527459d6931888f1dc74ee089dee24e0dee46ccf38d`. Npm content cache or its directory, not an installed package.
### alma-1d50fcce42a5a774e957bc14

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/af`. Source: `D1/in/raw/alma/members/1d50fcce42a5a774e957bc14.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a9`. Npm content cache or its directory, not an installed package.
### alma-4ce11aeef33e79da68fb5b63

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/af/a9`. Source: `D1/in/raw/alma/members/4ce11aeef33e79da68fb5b63.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4f7011b1657948732984bbb227c43321756d0a0f1a4b82814b720b9ab3109a27f48e219c0835ab4af4a63fb5ff99ae5cb038a5345038f70135d405fc495c`. Npm content cache or its directory, not an installed package.
### alma-65c14b394db65d223ddce946

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b1`. Source: `D1/in/raw/alma/members/65c14b394db65d223ddce946.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8d`. Npm content cache or its directory, not an installed package.
### alma-9d2d0f059857601105980e53

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b1/8d`. Source: `D1/in/raw/alma/members/9d2d0f059857601105980e53.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b6680eb1721033a6b8f2aa648442fe146c003344dd0bd9d401d0d94de5a7134caf43a27ea78687377806d49e966208034031f77ffb8d2455d29f17282886`. Npm content cache or its directory, not an installed package.
### alma-d37ffb8168930492e095451e

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b5`. Source: `D1/in/raw/alma/members/d37ffb8168930492e095451e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `40`. Npm content cache or its directory, not an installed package.
### alma-dc00e954936d12b20b29f037

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b5/40`. Source: `D1/in/raw/alma/members/dc00e954936d12b20b29f037.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9adf08c0590200f17ca3212a1bde0146674697b484b7b1849467e505065d479329b0573ed52b723d709b8ea8db97a67f1c64bc171abe43e2cd74beedd178`. Npm content cache or its directory, not an installed package.
### alma-a2f38840d1f8d467579f0e66

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b7`. Source: `D1/in/raw/alma/members/a2f38840d1f8d467579f0e66.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ac`, `b8`. Npm content cache or its directory, not an installed package.
### alma-a874a282c763442287121074

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b7/ac`. Source: `D1/in/raw/alma/members/a874a282c763442287121074.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1b82da025ef033b2ded0817c4962a3edd2eb047db81075fb443db2cbfdcbefe873c4e5582fa82b80203474360539d9db3aac5c2aae06a434bac712309bad`. Npm content cache or its directory, not an installed package.
### alma-053e6138c835ac18380ae039

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/b7/b8`. Source: `D1/in/raw/alma/members/053e6138c835ac18380ae039.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `70f6923e5afbb03495f0939cd51e9ca122ace0daa4e592524e7f4995c4649b7b7169d9589e65c76e3588da2c3a32ea9f6e1a94041961bced6a4c2a536af2`. Npm content cache or its directory, not an installed package.
### alma-10b08a0a62afa5b92fd4ceee

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/bb`. Source: `D1/in/raw/alma/members/10b08a0a62afa5b92fd4ceee.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `16`, `98`. Npm content cache or its directory, not an installed package.
### alma-22d01f18a968470602874a72

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/bb/16`. Source: `D1/in/raw/alma/members/22d01f18a968470602874a72.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2e878b7905c278579d99f9ed755a5be969edc7073c5f3173af6ab0479f6600c13fb11ac0d37bd3c249e2a4ced7e50f7124b7620ed8bb857780710e7ea0a1`. Npm content cache or its directory, not an installed package.
### alma-26e01bc075943abbd580d99a

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/bb/98`. Source: `D1/in/raw/alma/members/26e01bc075943abbd580d99a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `53a29f87d7612d42395bc9f6e373edc93e002ca14d73e2bee7e6283c4c14c772556f835b20c6de25099569476f2e7dff5af0ff25cd5fb11e2ebb2ff19502`. Npm content cache or its directory, not an installed package.
### alma-32c9640516e32166ce217334

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/bd`. Source: `D1/in/raw/alma/members/32c9640516e32166ce217334.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `78`. Npm content cache or its directory, not an installed package.
### alma-cb2f761a34c0b938d0fbc505

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/bd/78`. Source: `D1/in/raw/alma/members/cb2f761a34c0b938d0fbc505.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c4ea6005e3f4b3d36f9b5625454291b5a7846e1005b9e2ebccc3332b27be7be36fd04b3a8f27311cc5d31926187da4bac6b1cbad31f0f0912967ad6010d4`. Npm content cache or its directory, not an installed package.
### alma-7d200a6e52f2322e3bcb2a5d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/c0`. Source: `D1/in/raw/alma/members/7d200a6e52f2322e3bcb2a5d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ac`. Npm content cache or its directory, not an installed package.
### alma-f20ef1ba23741eca035e638f

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/c0/ac`. Source: `D1/in/raw/alma/members/f20ef1ba23741eca035e638f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `90450a63274b08a7ad84ad265d1ac8cc256b1aa79a1136284786ee86ec954effd8c807a5327af2feb57b8eaab9e0f23fdcc4a4d6c96530bd24eb8a2673fe`. Npm content cache or its directory, not an installed package.
### alma-b766ff7ccadd9c9dcf0d6892

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/cd`. Source: `D1/in/raw/alma/members/b766ff7ccadd9c9dcf0d6892.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b0`. Npm content cache or its directory, not an installed package.
### alma-09cd5ec8710263498035aa5e

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/cd/b0`. Source: `D1/in/raw/alma/members/09cd5ec8710263498035aa5e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7dac22404f5adb8e25436f686a2851cd60bc60b64f0d511c59dc86700f717a36dc5b5d94029e74a2d4b931f880e885d3e5169db6db05402c885e64941212`. Npm content cache or its directory, not an installed package.
### alma-c0b87326704beb1e1e29bd91

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ce`. Source: `D1/in/raw/alma/members/c0b87326704beb1e1e29bd91.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `43`. Npm content cache or its directory, not an installed package.
### alma-1711c959b408a3f1a153c38d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ce/43`. Source: `D1/in/raw/alma/members/1711c959b408a3f1a153c38d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d15d156160a7fea496a10a96cdd4174192c50754627437af60cb8902675b4194937f40f50ab7eeec50b6bb9d577d9246ca52a5980bd3fa4c171a25c94d86`. Npm content cache or its directory, not an installed package.
### alma-ba0349cf81f57570480ba6de

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/cf`. Source: `D1/in/raw/alma/members/ba0349cf81f57570480ba6de.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `29`, `64`. Npm content cache or its directory, not an installed package.
### alma-19f104456a646f8122a70b70

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/cf/29`. Source: `D1/in/raw/alma/members/19f104456a646f8122a70b70.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a6e7ebbeb02b125b20fda8d69e8d5dc316f84229c94a762cd868952e1c0f3744b8dbee74ae1a775d0871afd2193e298ec130096c59e2b851e83a115e9742`. Npm content cache or its directory, not an installed package.
### alma-a73cce0fc814bf81dcabafb4

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/cf/64`. Source: `D1/in/raw/alma/members/a73cce0fc814bf81dcabafb4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `be5bd5fbde10145248be37ef596b694196e9fcf738a03b21abb1ac7e29443ac0a5b86685a91180641a1423c008e30c2916c6163454a12193cc3363b17970`. Npm content cache or its directory, not an installed package.
### alma-2537da5b99adced6907f2553

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/d4`. Source: `D1/in/raw/alma/members/2537da5b99adced6907f2553.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `86`. Npm content cache or its directory, not an installed package.
### alma-48104a625d8a1901b94072c8

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/d4/86`. Source: `D1/in/raw/alma/members/48104a625d8a1901b94072c8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `97c7b1d8f61752367af85078a5ba2aea69b49b040f304df0508691e59fb1e02a5fee6e3582a89269de889e6b07fa73eafc793242d4087128808a34b12be5`. Npm content cache or its directory, not an installed package.
### alma-f61931e6dfb6413c88225879

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/e1`. Source: `D1/in/raw/alma/members/f61931e6dfb6413c88225879.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `76`. Npm content cache or its directory, not an installed package.
### alma-95ad545da1e2be63f4d1c56d

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/e1/76`. Source: `D1/in/raw/alma/members/95ad545da1e2be63f4d1c56d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `89db341d0b344e6438af1152033e47109fc2cc1526bc923f06c5bfcb9f0ceff40f1572d359fa57e2bc2fec5778af5bc1252531115d9a0f051ad92a434aa3`. Npm content cache or its directory, not an installed package.
### alma-ddeefa03a289548c9d7b56d7

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f0`. Source: `D1/in/raw/alma/members/ddeefa03a289548c9d7b56d7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2e`. Npm content cache or its directory, not an installed package.
### alma-53b1d3f85286b1f64ec8d022

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f0/2e`. Source: `D1/in/raw/alma/members/53b1d3f85286b1f64ec8d022.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `07d6376b80dbac4d0af762ee120a6f992ac0250c56e96b4292d19de29bcb9e6a0fbda4639fdc2ae2a2bbaf99e696fc0e68aa0f4bd1aafaa9e7ed021d378f`. Npm content cache or its directory, not an installed package.
### alma-ff5ac15200f6e10aee426d53

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f5`. Source: `D1/in/raw/alma/members/ff5ac15200f6e10aee426d53.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `31`. Npm content cache or its directory, not an installed package.
### alma-04ec440e1bcc84490972688c

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f5/31`. Source: `D1/in/raw/alma/members/04ec440e1bcc84490972688c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6b5217c4b4f5945bea03bb238f6a9b8ef9bd05962d68f1b90d0b8d61919db5ada28442d471512016b78c1b1c1b4477edaee41d463cfeeaa91394aace0704`. Npm content cache or its directory, not an installed package.
### alma-ad09f64d3d4dddd9f0adcbf1

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f8`. Source: `D1/in/raw/alma/members/ad09f64d3d4dddd9f0adcbf1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9c`, `ef`. Npm content cache or its directory, not an installed package.
### alma-94b03161a0b65de2e34a632c

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f8/9c`. Source: `D1/in/raw/alma/members/94b03161a0b65de2e34a632c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4958b2c242d96c345ca9a5c5f44e24253c6dd5d4fe07806c25b02bc77037a17bddd4b774a381cbdee119599ad64a61a7241b9a4fa47332f2fe94636edeb5`. Npm content cache or its directory, not an installed package.
### alma-9f70d8a79ca7a4146060a0eb

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/f8/ef`. Source: `D1/in/raw/alma/members/9f70d8a79ca7a4146060a0eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4972df307fefa55f1c4573885cf0bb23692ab41c5cf32fb715b30f2944320f763283da64f8cad0d994bb92059e1c2ca6455c8acc18eec36d00ad30924c2b`. Npm content cache or its directory, not an installed package.
### alma-e51c7851f5b874ecd9886309

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ff`. Source: `D1/in/raw/alma/members/e51c7851f5b874ecd9886309.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ff`. Npm content cache or its directory, not an installed package.
### alma-4d3bb6e25d699154b1851b6b

Group: `$USER_HOME/.npm/_cacache/content-v2/sha512/ff/ff`. Source: `D1/in/raw/alma/members/4d3bb6e25d699154b1851b6b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3c985592271f25c42cf07400014c92f6332581d76f9e218ecc0cbd92a8b98091e294f6ac51bd6b92c938e6dc5526a4110cb857dc90022a11a546503c5beb`. Npm content cache or its directory, not an installed package.
### alma-5356f3d802833a27db66064c

Group: `$USER_HOME/.npm/_cacache/index-v5`. Source: `D1/in/raw/alma/members/5356f3d802833a27db66064c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `00`, `0b`, `18`, `21`, `22`, `2d`, `31`, `37`, `38`, `39`, `3c`, `3f`, `40`, `44`, `48`, `4d`, `4f`, `59`, `5d`, `5e`, `6a`, `6b`, `73`, `84`, `85`, `86`, `89`, `8a`, `8b`, `8d`, `8e`, `95`, `9d`, `a4`, `aa`, `ac`, `b3`, `b8`, `ba`, `c0`, `c5`, `c8`, `cd`, `cf`, `df`, `e3`, `e8`, `f1`, `f2`, `fa`. Npm content cache or its directory, not an installed package.
### alma-b864c8cba4870b5ada297e90

Group: `$USER_HOME/.npm/_cacache/index-v5/00`. Source: `D1/in/raw/alma/members/b864c8cba4870b5ada297e90.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5f`. Npm content cache or its directory, not an installed package.
### alma-85915c93cc9a97e65a7266eb

Group: `$USER_HOME/.npm/_cacache/index-v5/00/5f`. Source: `D1/in/raw/alma/members/85915c93cc9a97e65a7266eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `18224c2157be67c545ab9f5fde051127158e10b6eae5d7fc9efec64f4275`. Npm content cache or its directory, not an installed package.
### alma-019b22aefbb768fb5c779770

Group: `$USER_HOME/.npm/_cacache/index-v5/0b`. Source: `D1/in/raw/alma/members/019b22aefbb768fb5c779770.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `47`, `90`. Npm content cache or its directory, not an installed package.
### alma-30b566b531d44683d6e8e01c

Group: `$USER_HOME/.npm/_cacache/index-v5/0b/47`. Source: `D1/in/raw/alma/members/30b566b531d44683d6e8e01c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6967dcc4b56fb8d4206276f53c8a122844fb389159f8a1148b4227c2857a`. Npm content cache or its directory, not an installed package.
### alma-da426c047078d79b69116b85

Group: `$USER_HOME/.npm/_cacache/index-v5/0b/90`. Source: `D1/in/raw/alma/members/da426c047078d79b69116b85.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c147816be94e86ed9bbb4b9e20409e4791a8991fcfd41d7a44489dedd29b`. Npm content cache or its directory, not an installed package.
### alma-fcee633498ebc0b5b900654d

Group: `$USER_HOME/.npm/_cacache/index-v5/18`. Source: `D1/in/raw/alma/members/fcee633498ebc0b5b900654d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ec`. Npm content cache or its directory, not an installed package.
### alma-9e30d6db4f71b3f37e747d23

Group: `$USER_HOME/.npm/_cacache/index-v5/18/ec`. Source: `D1/in/raw/alma/members/9e30d6db4f71b3f37e747d23.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `417d14d45d0c2b0eeccef6e81982a2bbb8f34c64d282460fb854bea0e46f`. Npm content cache or its directory, not an installed package.
### alma-e2e007f737ee005d4619f368

Group: `$USER_HOME/.npm/_cacache/index-v5/21`. Source: `D1/in/raw/alma/members/e2e007f737ee005d4619f368.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6a`. Npm content cache or its directory, not an installed package.
### alma-4b997bfd191aec4bdcfe0bcc

Group: `$USER_HOME/.npm/_cacache/index-v5/21/6a`. Source: `D1/in/raw/alma/members/4b997bfd191aec4bdcfe0bcc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2bfd7290b1a45b0c2c2bf1a8e91246dd164cf42af5f53d5356f305b0318a`. Npm content cache or its directory, not an installed package.
### alma-2be432fd3625403ef57ba2e7

Group: `$USER_HOME/.npm/_cacache/index-v5/22`. Source: `D1/in/raw/alma/members/2be432fd3625403ef57ba2e7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f3`. Npm content cache or its directory, not an installed package.
### alma-f9dc03f6335eb78f6424e264

Group: `$USER_HOME/.npm/_cacache/index-v5/22/f3`. Source: `D1/in/raw/alma/members/f9dc03f6335eb78f6424e264.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e108780d0b1201b05a0d04984f993f1afe66be14e06c8f586e201dab7c63`. Npm content cache or its directory, not an installed package.
### alma-9a99b917159a7c800029fee6

Group: `$USER_HOME/.npm/_cacache/index-v5/2d`. Source: `D1/in/raw/alma/members/9a99b917159a7c800029fee6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `59`. Npm content cache or its directory, not an installed package.
### alma-ca75e11cd1e14bfe36b5e97b

Group: `$USER_HOME/.npm/_cacache/index-v5/2d/59`. Source: `D1/in/raw/alma/members/ca75e11cd1e14bfe36b5e97b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `67d6c55f651fb4888d6a298d04ba46692a3bd9662c3cf157126bdb90b95c`. Npm content cache or its directory, not an installed package.
### alma-7720adac80b5f9fea5c36822

Group: `$USER_HOME/.npm/_cacache/index-v5/31`. Source: `D1/in/raw/alma/members/7720adac80b5f9fea5c36822.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ac`. Npm content cache or its directory, not an installed package.
### alma-050195687361ee5ca3d40c7f

Group: `$USER_HOME/.npm/_cacache/index-v5/31/ac`. Source: `D1/in/raw/alma/members/050195687361ee5ca3d40c7f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4d241faeb3fea9ec8318fd93dd55eb70a87cc8a6e3f849ccef9863882b4b`. Npm content cache or its directory, not an installed package.
### alma-fe1751843dae12e8dfb83052

Group: `$USER_HOME/.npm/_cacache/index-v5/37`. Source: `D1/in/raw/alma/members/fe1751843dae12e8dfb83052.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ed`. Npm content cache or its directory, not an installed package.
### alma-3550be5eaea4035a848aede1

Group: `$USER_HOME/.npm/_cacache/index-v5/37/ed`. Source: `D1/in/raw/alma/members/3550be5eaea4035a848aede1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9b273efe143c8378f357988499dd0af10441125cc0c6006d3b310cf194dc`. Npm content cache or its directory, not an installed package.
### alma-324368ee210ebfb8b92a91c1

Group: `$USER_HOME/.npm/_cacache/index-v5/38`. Source: `D1/in/raw/alma/members/324368ee210ebfb8b92a91c1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2e`. Npm content cache or its directory, not an installed package.
### alma-f9cf7a913037afc42d75e99d

Group: `$USER_HOME/.npm/_cacache/index-v5/38/2e`. Source: `D1/in/raw/alma/members/f9cf7a913037afc42d75e99d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `fe53691fa43d2f5ac447c8a2431535ec49118be55bf483c6362d4f72c79b`. Npm content cache or its directory, not an installed package.
### alma-38cbf044b7772e1823479693

Group: `$USER_HOME/.npm/_cacache/index-v5/39`. Source: `D1/in/raw/alma/members/38cbf044b7772e1823479693.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8b`. Npm content cache or its directory, not an installed package.
### alma-1cb4812f32e21a46295b3231

Group: `$USER_HOME/.npm/_cacache/index-v5/39/8b`. Source: `D1/in/raw/alma/members/1cb4812f32e21a46295b3231.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `49d4a3e3178da4617cbbda567e5ff8893e0922252f15362a87a459706440`. Npm content cache or its directory, not an installed package.
### alma-53242fc87d6f5938c40b3e59

Group: `$USER_HOME/.npm/_cacache/index-v5/3c`. Source: `D1/in/raw/alma/members/53242fc87d6f5938c40b3e59.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d5`. Npm content cache or its directory, not an installed package.
### alma-f21a4ace182fdddcb3c7ac79

Group: `$USER_HOME/.npm/_cacache/index-v5/3c/d5`. Source: `D1/in/raw/alma/members/f21a4ace182fdddcb3c7ac79.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `aa89d76ede71d9b1f8420eb87a6464bfddcbe330bb9eeb9c1198289af2b7`. Npm content cache or its directory, not an installed package.
### alma-7c7419f793a8bd79b32f96e6

Group: `$USER_HOME/.npm/_cacache/index-v5/3f`. Source: `D1/in/raw/alma/members/7c7419f793a8bd79b32f96e6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `00`. Npm content cache or its directory, not an installed package.
### alma-842e90f811296c469f9e7e42

Group: `$USER_HOME/.npm/_cacache/index-v5/3f/00`. Source: `D1/in/raw/alma/members/842e90f811296c469f9e7e42.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `5054c4dc0b0faa876ce494b47e2a161c3f912dea243a955ffd488db7fa25`. Npm content cache or its directory, not an installed package.
### alma-63e105f55393813d2b12afe2

Group: `$USER_HOME/.npm/_cacache/index-v5/40`. Source: `D1/in/raw/alma/members/63e105f55393813d2b12afe2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `62`, `ac`. Npm content cache or its directory, not an installed package.
### alma-336dc7926ef495e189ba650f

Group: `$USER_HOME/.npm/_cacache/index-v5/40/62`. Source: `D1/in/raw/alma/members/336dc7926ef495e189ba650f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d04e75208dec117f72a95a5989f81fac7565a530fd22f70ea5e3abc377c3`. Npm content cache or its directory, not an installed package.
### alma-7b5824b1d41df5919cf6b281

Group: `$USER_HOME/.npm/_cacache/index-v5/40/ac`. Source: `D1/in/raw/alma/members/7b5824b1d41df5919cf6b281.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `83d48046309a72e2d050fe8797a5ee3d0bfd0a55b78c905647806423ebe8`. Npm content cache or its directory, not an installed package.
### alma-c6f411a4c2bd699681366498

Group: `$USER_HOME/.npm/_cacache/index-v5/44`. Source: `D1/in/raw/alma/members/c6f411a4c2bd699681366498.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `83`. Npm content cache or its directory, not an installed package.
### alma-49a1a0e2bce9e7e97816148a

Group: `$USER_HOME/.npm/_cacache/index-v5/44/83`. Source: `D1/in/raw/alma/members/49a1a0e2bce9e7e97816148a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `dbe195e07ec9c71e45f2a16e652399324e7f3fa4c89a961847afd3d2e2c5`. Npm content cache or its directory, not an installed package.
### alma-7826349c72519d3bd69196a6

Group: `$USER_HOME/.npm/_cacache/index-v5/48`. Source: `D1/in/raw/alma/members/7826349c72519d3bd69196a6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `10`. Npm content cache or its directory, not an installed package.
### alma-22b5677518ba84e5465354f9

Group: `$USER_HOME/.npm/_cacache/index-v5/48/10`. Source: `D1/in/raw/alma/members/22b5677518ba84e5465354f9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9ab28e6de2edc1bf095464a39efb220841d4f79989c0a67895fe802889f7`. Npm content cache or its directory, not an installed package.
### alma-f4612cdb8684249d930a912b

Group: `$USER_HOME/.npm/_cacache/index-v5/4d`. Source: `D1/in/raw/alma/members/f4612cdb8684249d930a912b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `11`. Npm content cache or its directory, not an installed package.
### alma-7c5c8fd491aba065894ba343

Group: `$USER_HOME/.npm/_cacache/index-v5/4d/11`. Source: `D1/in/raw/alma/members/7c5c8fd491aba065894ba343.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7187e7fc42ccba59e77df7bbf53d622cedcd8d775ef19b4e431b4de8eaed`. Npm content cache or its directory, not an installed package.
### alma-f765634aa9a89a7568f6c46a

Group: `$USER_HOME/.npm/_cacache/index-v5/4f`. Source: `D1/in/raw/alma/members/f765634aa9a89a7568f6c46a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `eb`. Npm content cache or its directory, not an installed package.
### alma-84c80c5e491bea86e79008c1

Group: `$USER_HOME/.npm/_cacache/index-v5/4f/eb`. Source: `D1/in/raw/alma/members/84c80c5e491bea86e79008c1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `8cbab322150a907404391ad4927a8ed9a63841592a7782ee11c42d795426`. Npm content cache or its directory, not an installed package.
### alma-8eba173b2e825310a4aa855a

Group: `$USER_HOME/.npm/_cacache/index-v5/59`. Source: `D1/in/raw/alma/members/8eba173b2e825310a4aa855a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `51`. Npm content cache or its directory, not an installed package.
### alma-9442c91124ddafa660cc44c8

Group: `$USER_HOME/.npm/_cacache/index-v5/59/51`. Source: `D1/in/raw/alma/members/9442c91124ddafa660cc44c8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b4eaa023d06f838c97818e3714054b5b460d1e8679160f6dfe031012cb73`. Npm content cache or its directory, not an installed package.
### alma-478ebf23ffd2e516cfe11715

Group: `$USER_HOME/.npm/_cacache/index-v5/5d`. Source: `D1/in/raw/alma/members/478ebf23ffd2e516cfe11715.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c7`. Npm content cache or its directory, not an installed package.
### alma-a8d511559bd6788122868316

Group: `$USER_HOME/.npm/_cacache/index-v5/5d/c7`. Source: `D1/in/raw/alma/members/a8d511559bd6788122868316.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `264ea6d41e603370a95a68dd46e4358e4d977bf308384d88604ad0b6c5ed`. Npm content cache or its directory, not an installed package.
### alma-4c5218840162e9d4c4d4a69b

Group: `$USER_HOME/.npm/_cacache/index-v5/5e`. Source: `D1/in/raw/alma/members/4c5218840162e9d4c4d4a69b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e7`. Npm content cache or its directory, not an installed package.
### alma-62ccf476fdf144abbc79daaf

Group: `$USER_HOME/.npm/_cacache/index-v5/5e/e7`. Source: `D1/in/raw/alma/members/62ccf476fdf144abbc79daaf.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `453bd89145eccf9d67f5797fb09e5a017b5b13f1ac45cb7b70bda45940ec`. Npm content cache or its directory, not an installed package.
### alma-65f5ed1991491f43b370c455

Group: `$USER_HOME/.npm/_cacache/index-v5/6a`. Source: `D1/in/raw/alma/members/65f5ed1991491f43b370c455.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `a7`. Npm content cache or its directory, not an installed package.
### alma-56caf76dcf038eeac0b9910e

Group: `$USER_HOME/.npm/_cacache/index-v5/6a/a7`. Source: `D1/in/raw/alma/members/56caf76dcf038eeac0b9910e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1cbd001cd62203bc47d9086e371da3823c4fe7cb824efdfcccee13ad1ce3`. Npm content cache or its directory, not an installed package.
### alma-e4bc289498e808a953b0d85f

Group: `$USER_HOME/.npm/_cacache/index-v5/6b`. Source: `D1/in/raw/alma/members/e4bc289498e808a953b0d85f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `aa`, `f4`. Npm content cache or its directory, not an installed package.
### alma-3b6709e59447a4099422322e

Group: `$USER_HOME/.npm/_cacache/index-v5/6b/aa`. Source: `D1/in/raw/alma/members/3b6709e59447a4099422322e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `74c56b4f0c9326e8f333981868167e34c27432025784fc9077102b20416c`. Npm content cache or its directory, not an installed package.
### alma-18be0666a62045ae6bdc95a9

Group: `$USER_HOME/.npm/_cacache/index-v5/6b/f4`. Source: `D1/in/raw/alma/members/18be0666a62045ae6bdc95a9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9e845476c976b8f9b91dc89b232bf40c00b5ff1d1bd141e780de532e76c0`. Npm content cache or its directory, not an installed package.
### alma-c677f332d2cdc931b85c6486

Group: `$USER_HOME/.npm/_cacache/index-v5/73`. Source: `D1/in/raw/alma/members/c677f332d2cdc931b85c6486.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c1`. Npm content cache or its directory, not an installed package.
### alma-4e9e2cccd1fd0ebcbcf62d76

Group: `$USER_HOME/.npm/_cacache/index-v5/73/c1`. Source: `D1/in/raw/alma/members/4e9e2cccd1fd0ebcbcf62d76.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2f699add58dcbb2a2d0f4c9a8a135df99a8179216a1b5bd26649876a2b00`. Npm content cache or its directory, not an installed package.
### alma-b648b2bd7f911a4e183b9c01

Group: `$USER_HOME/.npm/_cacache/index-v5/84`. Source: `D1/in/raw/alma/members/b648b2bd7f911a4e183b9c01.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `82`. Npm content cache or its directory, not an installed package.
### alma-74d78cd341b79f261735f8f1

Group: `$USER_HOME/.npm/_cacache/index-v5/84/82`. Source: `D1/in/raw/alma/members/74d78cd341b79f261735f8f1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3fa8cdf58bf2fe359b6df055ad5f7a24f3495b4fd8f6d64768a5ec8335c3`. Npm content cache or its directory, not an installed package.
### alma-c04364d48f58f2c8f50cd409

Group: `$USER_HOME/.npm/_cacache/index-v5/85`. Source: `D1/in/raw/alma/members/c04364d48f58f2c8f50cd409.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `79`, `e8`. Npm content cache or its directory, not an installed package.
### alma-68ae98d12148101878507f6c

Group: `$USER_HOME/.npm/_cacache/index-v5/85/79`. Source: `D1/in/raw/alma/members/68ae98d12148101878507f6c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `3fb741604093d8d76d46cd7ae5aae318318281c865ac55e74dfb55e3425d`. Npm content cache or its directory, not an installed package.
### alma-2777b3ae5af32d8ad3f595eb

Group: `$USER_HOME/.npm/_cacache/index-v5/85/e8`. Source: `D1/in/raw/alma/members/2777b3ae5af32d8ad3f595eb.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `62bb0eee7c81dc0a064df57ee4bc3ef332c5f3e0cf654b5c582da024f5f3`. Npm content cache or its directory, not an installed package.
### alma-95dbbfb1666b74fd5baf32c7

Group: `$USER_HOME/.npm/_cacache/index-v5/86`. Source: `D1/in/raw/alma/members/95dbbfb1666b74fd5baf32c7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `38`. Npm content cache or its directory, not an installed package.
### alma-c9c7c9dbee218c849dffd36e

Group: `$USER_HOME/.npm/_cacache/index-v5/86/38`. Source: `D1/in/raw/alma/members/c9c7c9dbee218c849dffd36e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `67cd332218e56148ab0eb89ec176defd516fc7b0dc3276cbe6a7b525e744`. Npm content cache or its directory, not an installed package.
### alma-7bda43a73eb18e5393233734

Group: `$USER_HOME/.npm/_cacache/index-v5/89`. Source: `D1/in/raw/alma/members/7bda43a73eb18e5393233734.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d4`. Npm content cache or its directory, not an installed package.
### alma-f48a88c53cc04f370cd23e8f

Group: `$USER_HOME/.npm/_cacache/index-v5/89/d4`. Source: `D1/in/raw/alma/members/f48a88c53cc04f370cd23e8f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ec52c00102545b78746b59671488264963abd741664f5be1ec73fef527a4`. Npm content cache or its directory, not an installed package.
### alma-0457b0eb197603be4f0f82c1

Group: `$USER_HOME/.npm/_cacache/index-v5/8a`. Source: `D1/in/raw/alma/members/0457b0eb197603be4f0f82c1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c9`, `ee`. Npm content cache or its directory, not an installed package.
### alma-9b21665ebf617da592424c94

Group: `$USER_HOME/.npm/_cacache/index-v5/8a/c9`. Source: `D1/in/raw/alma/members/9b21665ebf617da592424c94.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c10bf71d66461aba0899e81d7a146332c45dbbacb1693c38fc2e4e578e39`. Npm content cache or its directory, not an installed package.
### alma-83abd8935ba16e7c25fd4b7f

Group: `$USER_HOME/.npm/_cacache/index-v5/8a/ee`. Source: `D1/in/raw/alma/members/83abd8935ba16e7c25fd4b7f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `e3e86b627c10a9fc4ed610c15792507293ba1c14e7ba839e22aec609f1e0`. Npm content cache or its directory, not an installed package.
### alma-e72ba46c2fe771089bf3bb2d

Group: `$USER_HOME/.npm/_cacache/index-v5/8b`. Source: `D1/in/raw/alma/members/e72ba46c2fe771089bf3bb2d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ee`. Npm content cache or its directory, not an installed package.
### alma-374cf7859a882f93fbe8bfb1

Group: `$USER_HOME/.npm/_cacache/index-v5/8b/ee`. Source: `D1/in/raw/alma/members/374cf7859a882f93fbe8bfb1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c2ea22c4bf9c5ddcd0333850e543442de3364478847c7ebc382b1ff3a70d`. Npm content cache or its directory, not an installed package.
### alma-18f0311b2b39deab2d4ca305

Group: `$USER_HOME/.npm/_cacache/index-v5/8d`. Source: `D1/in/raw/alma/members/18f0311b2b39deab2d4ca305.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2c`. Npm content cache or its directory, not an installed package.
### alma-9bdcb5cb36a9932c5a5f8799

Group: `$USER_HOME/.npm/_cacache/index-v5/8d/2c`. Source: `D1/in/raw/alma/members/9bdcb5cb36a9932c5a5f8799.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `bf742c29757d7367d6a3aeb1fdc6d85b963e45fd23b6557f6f3b2b98eb14`. Npm content cache or its directory, not an installed package.
### alma-134f476d8b423b7f1cb659af

Group: `$USER_HOME/.npm/_cacache/index-v5/8e`. Source: `D1/in/raw/alma/members/134f476d8b423b7f1cb659af.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `28`, `58`. Npm content cache or its directory, not an installed package.
### alma-fd12324e5993af68c5ddc7a1

Group: `$USER_HOME/.npm/_cacache/index-v5/8e/28`. Source: `D1/in/raw/alma/members/fd12324e5993af68c5ddc7a1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ceb72ed3f4563883e7b5e0818c2e525c244782d6a9499c4a88bf1bc6c4a2`. Npm content cache or its directory, not an installed package.
### alma-31416613d876a6b39a1b4c25

Group: `$USER_HOME/.npm/_cacache/index-v5/8e/58`. Source: `D1/in/raw/alma/members/31416613d876a6b39a1b4c25.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1ce1355f39c75fa063f8dc1c958c11d57446438253b206afc18efb9f28c9`. Npm content cache or its directory, not an installed package.
### alma-13453975476fdc9697edf27e

Group: `$USER_HOME/.npm/_cacache/index-v5/95`. Source: `D1/in/raw/alma/members/13453975476fdc9697edf27e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ab`. Npm content cache or its directory, not an installed package.
### alma-03df84032396de1017d72164

Group: `$USER_HOME/.npm/_cacache/index-v5/95/ab`. Source: `D1/in/raw/alma/members/03df84032396de1017d72164.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `f8b689adc5f40d4c9811dacca0ed258f07342ae7c9fd3c50c8c34f6d9f53`. Npm content cache or its directory, not an installed package.
### alma-4f96c509b5e30e18e1b6bd73

Group: `$USER_HOME/.npm/_cacache/index-v5/9d`. Source: `D1/in/raw/alma/members/4f96c509b5e30e18e1b6bd73.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `02`. Npm content cache or its directory, not an installed package.
### alma-e65388ec060a021fd7efc3f6

Group: `$USER_HOME/.npm/_cacache/index-v5/9d/02`. Source: `D1/in/raw/alma/members/e65388ec060a021fd7efc3f6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7875456cd7212123eec140a8f9025caa189a7e0199e1b37ba94cf397353c`. Npm content cache or its directory, not an installed package.
### alma-6aa845b4adc0a9b64bec3c4f

Group: `$USER_HOME/.npm/_cacache/index-v5/a4`. Source: `D1/in/raw/alma/members/6aa845b4adc0a9b64bec3c4f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `44`. Npm content cache or its directory, not an installed package.
### alma-8421d53920782caec7f56d90

Group: `$USER_HOME/.npm/_cacache/index-v5/a4/44`. Source: `D1/in/raw/alma/members/8421d53920782caec7f56d90.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c797a676c91c1866342b9b548736d8f581612b6024cf63b883a4e67da4d6`. Npm content cache or its directory, not an installed package.
### alma-52b181c17ff0b8da2eb52056

Group: `$USER_HOME/.npm/_cacache/index-v5/aa`. Source: `D1/in/raw/alma/members/52b181c17ff0b8da2eb52056.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c4`, `cc`. Npm content cache or its directory, not an installed package.
### alma-610e962af1057301ee67365e

Group: `$USER_HOME/.npm/_cacache/index-v5/aa/c4`. Source: `D1/in/raw/alma/members/610e962af1057301ee67365e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `489c0e6a9e4cbd64a8acd4fbfda113e9dfdd114f464830471fda53fff0cd`. Npm content cache or its directory, not an installed package.
### alma-a845b2005cb4f45888b0d585

Group: `$USER_HOME/.npm/_cacache/index-v5/aa/cc`. Source: `D1/in/raw/alma/members/a845b2005cb4f45888b0d585.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7a257ce74459a2b13efd969ec4bdc6f7162b60f7f6d90aa2ce66dd0ffaca`. Npm content cache or its directory, not an installed package.
### alma-16b3b1cb159b5cb2e0bb2a8c

Group: `$USER_HOME/.npm/_cacache/index-v5/ac`. Source: `D1/in/raw/alma/members/16b3b1cb159b5cb2e0bb2a8c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `59`. Npm content cache or its directory, not an installed package.
### alma-fb0f458f6daa4e4086e3a154

Group: `$USER_HOME/.npm/_cacache/index-v5/ac/59`. Source: `D1/in/raw/alma/members/fb0f458f6daa4e4086e3a154.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0d9aa27abbf50d839a6d5069a547db7424d523bd5bd00a7df466deca232a`. Npm content cache or its directory, not an installed package.
### alma-b4aecfb73b9707d0bcba7def

Group: `$USER_HOME/.npm/_cacache/index-v5/b3`. Source: `D1/in/raw/alma/members/b4aecfb73b9707d0bcba7def.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b3`. Npm content cache or its directory, not an installed package.
### alma-fd60bfd35d18c46a69856e79

Group: `$USER_HOME/.npm/_cacache/index-v5/b3/b3`. Source: `D1/in/raw/alma/members/fd60bfd35d18c46a69856e79.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `05a8af0a671c32b41850c1223429fe74449cfcb4c7cac54a9c7c213dfcae`. Npm content cache or its directory, not an installed package.
### alma-924b1bb4da94a020067dd7e9

Group: `$USER_HOME/.npm/_cacache/index-v5/b8`. Source: `D1/in/raw/alma/members/924b1bb4da94a020067dd7e9.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `4d`. Npm content cache or its directory, not an installed package.
### alma-86ef4ebd8dadcd5f8390b8d7

Group: `$USER_HOME/.npm/_cacache/index-v5/b8/4d`. Source: `D1/in/raw/alma/members/86ef4ebd8dadcd5f8390b8d7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `25488400e3aa575fbd3068239a528958ee8f7823c7eb5dbe0507d0223fea`. Npm content cache or its directory, not an installed package.
### alma-2451b5662846efa638f7c82b

Group: `$USER_HOME/.npm/_cacache/index-v5/ba`. Source: `D1/in/raw/alma/members/2451b5662846efa638f7c82b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2d`. Npm content cache or its directory, not an installed package.
### alma-c0bae47cf9c36b44bab920e4

Group: `$USER_HOME/.npm/_cacache/index-v5/ba/2d`. Source: `D1/in/raw/alma/members/c0bae47cf9c36b44bab920e4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `bf68f0d62bdfbeba06424f5aade18f120e1738f9c25f45cfafd54b56fab3`. Npm content cache or its directory, not an installed package.
### alma-f7e4313279828b2e06b00158

Group: `$USER_HOME/.npm/_cacache/index-v5/c0`. Source: `D1/in/raw/alma/members/f7e4313279828b2e06b00158.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `42`, `4d`, `e0`. Npm content cache or its directory, not an installed package.
### alma-2a2e13207b722f48a9ac8bb8

Group: `$USER_HOME/.npm/_cacache/index-v5/c0/42`. Source: `D1/in/raw/alma/members/2a2e13207b722f48a9ac8bb8.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `ed6a53773a82278174035feafc3eecdaa5d451bbe310c51890218455bf08`. Npm content cache or its directory, not an installed package.
### alma-cf4521b16c1856c94abaad4b

Group: `$USER_HOME/.npm/_cacache/index-v5/c0/4d`. Source: `D1/in/raw/alma/members/cf4521b16c1856c94abaad4b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `91ce60f404280e12042f3e51d70bf1e3db83f9ea609a8ee861af124e4af1`. Npm content cache or its directory, not an installed package.
### alma-412da6c9fbc849ff47f101fe

Group: `$USER_HOME/.npm/_cacache/index-v5/c0/e0`. Source: `D1/in/raw/alma/members/412da6c9fbc849ff47f101fe.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6bc9f5a2253c7ef1c79319e59c99f139f5084b9deae5421347e3f770cea8`. Npm content cache or its directory, not an installed package.
### alma-d67b71476e1c06d2c6ad4ee2

Group: `$USER_HOME/.npm/_cacache/index-v5/c5`. Source: `D1/in/raw/alma/members/d67b71476e1c06d2c6ad4ee2.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `2d`. Npm content cache or its directory, not an installed package.
### alma-16efe806c8635a62493c4fc4

Group: `$USER_HOME/.npm/_cacache/index-v5/c5/2d`. Source: `D1/in/raw/alma/members/16efe806c8635a62493c4fc4.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `90031096314e15f4fcc35c804c2180f88214a7851b531aa27bd64064f740`. Npm content cache or its directory, not an installed package.
### alma-10de80f3cabed4eff3b777c3

Group: `$USER_HOME/.npm/_cacache/index-v5/c8`. Source: `D1/in/raw/alma/members/10de80f3cabed4eff3b777c3.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `28`, `3d`. Npm content cache or its directory, not an installed package.
### alma-5d4f64ae0fa2ebfec227d8a1

Group: `$USER_HOME/.npm/_cacache/index-v5/c8/28`. Source: `D1/in/raw/alma/members/5d4f64ae0fa2ebfec227d8a1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `de5666528cd6e5b97476f31c38f7b3937c75954f61d0208b79f4bb5da5c2`. Npm content cache or its directory, not an installed package.
### alma-faa8e694bee9a726f91582e6

Group: `$USER_HOME/.npm/_cacache/index-v5/c8/3d`. Source: `D1/in/raw/alma/members/faa8e694bee9a726f91582e6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `cc1fe92e1b5db69db451b8de03d2ad187825443c55724c4f5293f8f71e8b`. Npm content cache or its directory, not an installed package.
### alma-660445469f23cd728e45392e

Group: `$USER_HOME/.npm/_cacache/index-v5/cd`. Source: `D1/in/raw/alma/members/660445469f23cd728e45392e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d3`. Npm content cache or its directory, not an installed package.
### alma-6e0278e131a58dc2a7e40523

Group: `$USER_HOME/.npm/_cacache/index-v5/cd/d3`. Source: `D1/in/raw/alma/members/6e0278e131a58dc2a7e40523.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `470c9cbb447615faafb6dfdf54632831f7f96c77771ea06a1eeffba41373`. Npm content cache or its directory, not an installed package.
### alma-7f103bc9959049aefc8f0c2c

Group: `$USER_HOME/.npm/_cacache/index-v5/cf`. Source: `D1/in/raw/alma/members/7f103bc9959049aefc8f0c2c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `56`. Npm content cache or its directory, not an installed package.
### alma-407f835129e014e0bcc2bc2d

Group: `$USER_HOME/.npm/_cacache/index-v5/cf/56`. Source: `D1/in/raw/alma/members/407f835129e014e0bcc2bc2d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `427919eefb09afe942b12902069325293191afa7d59ff0f2b016c402b4ec`. Npm content cache or its directory, not an installed package.
### alma-fa5dc6c4f57052be7d068459

Group: `$USER_HOME/.npm/_cacache/index-v5/df`. Source: `D1/in/raw/alma/members/fa5dc6c4f57052be7d068459.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `9e`. Npm content cache or its directory, not an installed package.
### alma-e4b689306524dc91852cd26c

Group: `$USER_HOME/.npm/_cacache/index-v5/df/9e`. Source: `D1/in/raw/alma/members/e4b689306524dc91852cd26c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `d48d421be29376fcd64900675bb9fba7efa738af9cd711ed8a6fe2e21e76`. Npm content cache or its directory, not an installed package.
### alma-01de2c17810a6d073ff215fc

Group: `$USER_HOME/.npm/_cacache/index-v5/e3`. Source: `D1/in/raw/alma/members/01de2c17810a6d073ff215fc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `6a`. Npm content cache or its directory, not an installed package.
### alma-2d153a381a0d81caa0c4d08c

Group: `$USER_HOME/.npm/_cacache/index-v5/e3/6a`. Source: `D1/in/raw/alma/members/2d153a381a0d81caa0c4d08c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b90e45414a9e52cdf1e4a96698065357795b9400d7af079b0a75ee8fd76d`. Npm content cache or its directory, not an installed package.
### alma-9c869ce6e0f6eeb22c564588

Group: `$USER_HOME/.npm/_cacache/index-v5/e8`. Source: `D1/in/raw/alma/members/9c869ce6e0f6eeb22c564588.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `7b`. Npm content cache or its directory, not an installed package.
### alma-c34aa202b370d332e23efd19

Group: `$USER_HOME/.npm/_cacache/index-v5/e8/7b`. Source: `D1/in/raw/alma/members/c34aa202b370d332e23efd19.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0817eb9f1646f60b27e507cd62e9e466ab147621279b2b9c754664d522ad`. Npm content cache or its directory, not an installed package.
### alma-785606bc870c24d89bcbff9b

Group: `$USER_HOME/.npm/_cacache/index-v5/f1`. Source: `D1/in/raw/alma/members/785606bc870c24d89bcbff9b.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `0d`, `ad`. Npm content cache or its directory, not an installed package.
### alma-fc8fbe53d31f071b7f886fff

Group: `$USER_HOME/.npm/_cacache/index-v5/f1/0d`. Source: `D1/in/raw/alma/members/fc8fbe53d31f071b7f886fff.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c6029d51f93afd01a0113d7d479df0817dcf4fb9386094683c5ab033d76e`. Npm content cache or its directory, not an installed package.
### alma-dae4074a38817e541b4430f5

Group: `$USER_HOME/.npm/_cacache/index-v5/f1/ad`. Source: `D1/in/raw/alma/members/dae4074a38817e541b4430f5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b0025aeabb0d0f44a6447ad4de748b50aab2ab733f90c6e5d2130d8e4c27`. Npm content cache or its directory, not an installed package.
### alma-c2814a4466c1b442bb35d85e

Group: `$USER_HOME/.npm/_cacache/index-v5/f2`. Source: `D1/in/raw/alma/members/c2814a4466c1b442bb35d85e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1f`, `3c`. Npm content cache or its directory, not an installed package.
### alma-6990321f35168eb2d918e4a0

Group: `$USER_HOME/.npm/_cacache/index-v5/f2/1f`. Source: `D1/in/raw/alma/members/6990321f35168eb2d918e4a0.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `c662626ec8eafafa54476678b9f71799a74ee368f2b7845a6ec9f9174a4d`. Npm content cache or its directory, not an installed package.
### alma-06291bc5e42af41447b6f6a5

Group: `$USER_HOME/.npm/_cacache/index-v5/f2/3c`. Source: `D1/in/raw/alma/members/06291bc5e42af41447b6f6a5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1c79abdced79951257dabca02e144d20a105eb60113c0f31c0df105f3a18`. Npm content cache or its directory, not an installed package.
### alma-4554b60dc340eebb553c5156

Group: `$USER_HOME/.npm/_cacache/index-v5/fa`. Source: `D1/in/raw/alma/members/4554b60dc340eebb553c5156.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `aa`. Npm content cache or its directory, not an installed package.
### alma-21fccc4cb5a4340d04cbe0ef

Group: `$USER_HOME/.npm/_cacache/index-v5/fa/aa`. Source: `D1/in/raw/alma/members/21fccc4cb5a4340d04cbe0ef.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `b053fe5b7646ebbce9357e64b532ef6a932755f352ab30cd1ad5fcb5242f`. Npm content cache or its directory, not an installed package.
### alma-b4f87cb25739062fda57c232

Group: `$USER_HOME/.npm/_logs`. Source: `D1/in/raw/alma/members/b4f87cb25739062fda57c232.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `2026-11-23T11_17_21_380Z-debug-0.log`. Package origin, unchangedness, and source of this object are not established.
### alma-436688690a5e6cf085aad702

Group: `$USER_HOME/.ssh`. Source: `D1/in/raw/alma/members/436688690a5e6cf085aad702.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `authorized_keys`. Package origin, unchangedness, and source of this object are not established.
### alma-042cb4cbb0e4f47fccd33163

Group: `$USER_HOME/Downloads`. Source: `D1/in/raw/alma/members/042cb4cbb0e4f47fccd33163.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `clearurls-source.json`, `clearurls.xpi`. Package origin, unchangedness, and source of this object are not established.
### alma-ac73aef78caf7e7da0d53fa2

Group: `$ROOT_HOME`. Source: `D1/in/raw/alma/members/ac73aef78caf7e7da0d53fa2.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.cache`, `.ssh`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `anaconda-ks.cfg`, `original-ks.cfg`. Package origin, unchangedness, and source of this object are not established.
### alma-8e368cdb5235d8765675f4b5

Group: `/run`. Source: `D1/in/raw/alma/members/8e368cdb5235d8765675f4b5.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `.heim_org.h5l.kcm-socket`, `NetworkManager`, `agetty.reload`, `atd.pid`, `blkid`, `chrony`, `chrony-dhcp`, `cockpit`, `console`, `containers`, `credentials`, `cron.reboot`, `crond.pid`, `crun`, `dmeventd-client`, `dmeventd-server`, `firewalld`, `fsck`, `initctl`, `initramfs`, `irqbalance`, `libpod`, `log`, `media`, `modprobe.d`, `mount`, `multipath`, `netns`, `plymouth`, `podman`, `rsyslogd.pid`, `selinux-policy`, `ssh-unix-local`, `sshd.pid`, `sudo`, `sysctl.d`, `systemd`, `tmpfiles.d`, `tpm2-tss`, `udev`, `user`. Runtime object disappears with its backing filesystem.
### alma-d18ab2b1e272cd0bcf711072

Group: `/run/NetworkManager`. Source: `D1/in/raw/alma/members/d18ab2b1e272cd0bcf711072.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by NetworkManager (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `conf.d`, `devices`, `initrd`, `no-stub-resolv.conf`, `resolv.conf`, `system-connections`. Runtime object disappears with its backing filesystem.
### alma-ddcbab7d1b41058b1851e06a

Group: `/run/NetworkManager/conf.d`. Source: `D1/in/raw/alma/members/ddcbab7d1b41058b1851e06a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by NetworkManager (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `15-carrier-timeout.conf`. Runtime object disappears with its backing filesystem.
### alma-5a8a97f67be3c6ed1eb2ae33

Group: `/run/NetworkManager/devices`. Source: `D1/in/raw/alma/members/5a8a97f67be3c6ed1eb2ae33.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by NetworkManager (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `1`, `2`, `3`, `4`. Runtime object disappears with its backing filesystem.
### alma-8bbca6e6017cf018706ee7e0

Group: `/run/NetworkManager/system-connections`. Source: `D1/in/raw/alma/members/8bbca6e6017cf018706ee7e0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by NetworkManager (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `lo.nmconnection`. Runtime object disappears with its backing filesystem.
### alma-0a70758d64395565d052d765

Group: `/run/avahi-daemon`. Source: `D1/in/raw/alma/members/0a70758d64395565d052d765.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `pid`, `socket`. Runtime object disappears with its backing filesystem.
### alma-cbb62c639bb9f63c13a9abbe

Group: `/run/blkid`. Source: `D1/in/raw/alma/members/cbb62c639bb9f63c13a9abbe.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `blkid.tab`, `blkid.tab.old`. Runtime object disappears with its backing filesystem.
### alma-19d1f43cf5e7c3606241eb2e

Group: `/run/chrony`. Source: `D1/in/raw/alma/members/19d1f43cf5e7c3606241eb2e.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by chronyd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `chronyd.pid`, `chronyd.sock`. Runtime object disappears with its backing filesystem.
### alma-b5899345a93785121f4311d5

Group: `/run/cockpit`. Source: `D1/in/raw/alma/members/b5899345a93785121f4311d5.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `inactive.issue`, `issue`. Runtime object disappears with its backing filesystem.
### alma-76a08b7b3af974eabf9fb099

Group: `/run/containers`. Source: `D1/in/raw/alma/members/76a08b7b3af974eabf9fb099.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `networks`, `storage`. Runtime object disappears with its backing filesystem.
### alma-26a23d2104fea49b1b65e6d3

Group: `/run/containers/networks`. Source: `D1/in/raw/alma/members/26a23d2104fea49b1b65e6d3.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `firewall`, `ipam.db`. Runtime object disappears with its backing filesystem.
### alma-48b92e1195bd9ef135096b55

Group: `/run/containers/networks/firewall`. Source: `D1/in/raw/alma/members/48b92e1195bd9ef135096b55.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `firewall-driver`, `firewall-reload.lock`, `networks`, `ports`. Runtime object disappears with its backing filesystem.
### alma-4011563e398785250101b941

Group: `/run/containers/storage`. Source: `D1/in/raw/alma/members/4011563e398785250101b941.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `overlay`, `overlay-containers`, `overlay-layers`, `overlay-locks`. Runtime object disappears with its backing filesystem.
### alma-abb7400a170151686c2b081a

Group: `/run/containers/storage/overlay`. Source: `D1/in/raw/alma/members/abb7400a170151686c2b081a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `idmapped-lower-dir-true`, `metacopy(nodev,metacopy=on)-true`, `native-diff(nodev,metacopy=on)-false`, `overlay-true`. Runtime object disappears with its backing filesystem.
### alma-8dda45494a90540e8691e981

Group: `/run/containers/storage/overlay-containers`. Source: `D1/in/raw/alma/members/8dda45494a90540e8691e981.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `80fc64f7d1e8b3958e7843bf106e5bba9744e9489ad62482eceedfbb8d7437c8`. Runtime object disappears with its backing filesystem.
### alma-cb71dc919aa866a953b0e419

Group: `/run/containers/storage/overlay-containers/80fc64f7d1e8b3958e7843bf106e5bba9744e9489ad62482eceedfbb8d7437c8`. Source: `D1/in/raw/alma/members/cb71dc919aa866a953b0e419.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `healthcheck.log`, `userdata`. Runtime object disappears with its backing filesystem.
### alma-501bc86c9730dafd236c0227

Group: `/run/containers/storage/overlay-containers/80fc64f7d1e8b3958e7843bf106e5bba9744e9489ad62482eceedfbb8d7437c8/userdata`. Source: `D1/in/raw/alma/members/501bc86c9730dafd236c0227.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `.containerenv`, `conmon.pid`, `hostname`, `hosts`, `oci-log`, `pidfile`, `resolv.conf`, `run`. Runtime object disappears with its backing filesystem.
### alma-4b3adac5114a229206208282

Group: `/run/containers/storage/overlay-containers/80fc64f7d1e8b3958e7843bf106e5bba9744e9489ad62482eceedfbb8d7437c8/userdata/run`. Source: `D1/in/raw/alma/members/4b3adac5114a229206208282.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `secrets`. Runtime object disappears with its backing filesystem.
### alma-23af5b487be2d300f6af6edf

Group: `/run/containers/storage/overlay-layers`. Source: `D1/in/raw/alma/members/23af5b487be2d300f6af6edf.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `mountpoints.json`, `mountpoints.lock`. Runtime object disappears with its backing filesystem.
### alma-74da7829bd899c722240f780

Group: `/run/credentials`. Source: `D1/in/raw/alma/members/74da7829bd899c722240f780.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `getty@tty1.service`, `serial-getty@ttyS0.service`, `systemd-journald.service`. Runtime object disappears with its backing filesystem.
### alma-50bb1e8a6b2151c89f181d7d

Group: `/run/crun`. Source: `D1/in/raw/alma/members/50bb1e8a6b2151c89f181d7d.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by crun (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `.cache`, `.empty-directory`. Runtime object disappears with its backing filesystem.
### alma-ce3aec3014353731f9a5bd97

Group: `/run/crun/.cache`. Source: `D1/in/raw/alma/members/ce3aec3014353731f9a5bd97.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by crun (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `seccomp`. Runtime object disappears with its backing filesystem.
### alma-0c343bb2d22287555c118dba

Group: `/run/crun/.cache/seccomp`. Source: `D1/in/raw/alma/members/0c343bb2d22287555c118dba.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by crun (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `11d5106f82417bee3424eea64c41854ebc73a580938fb8a406c2f8e89d358410`. Runtime object disappears with its backing filesystem.
### alma-e77e40d4209a47a9c224d6f9

Group: `/run/cups`. Source: `D1/in/raw/alma/members/e77e40d4209a47a9c224d6f9.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by cupsd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `cups.sock`. Runtime object disappears with its backing filesystem.
### alma-27c99c2920b7cf7538b1765d

Group: `/run/cups/certs`. Source: `D1/in/raw/alma/members/27c99c2920b7cf7538b1765d.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by cupsd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `0`. Runtime object disappears with its backing filesystem.
### alma-1bddeae14bb902061fde4fce

Group: `/run/dbus`. Source: `D1/in/raw/alma/members/1bddeae14bb902061fde4fce.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by dbus-broker (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `containers`, `system_bus_socket`. Runtime object disappears with its backing filesystem.
### alma-9ea58f80bfa0ee9660833b81

Group: `/run/fsck`. Source: `D1/in/raw/alma/members/9ea58f80bfa0ee9660833b81.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `dm-0.lock`. Runtime object disappears with its backing filesystem.
### alma-336038df0d255d79e80d0da0

Group: `/run/initramfs`. Source: `D1/in/raw/alma/members/336038df0d255d79e80d0da0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `.need_shutdown`, `log`. Runtime object disappears with its backing filesystem.
### alma-29456d00810288f2d3b7375a

Group: `/run/initramfs/log`. Source: `D1/in/raw/alma/members/29456d00810288f2d3b7375a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `btmp`, `lastlog`, `private`, `wtmp`. Runtime object disappears with its backing filesystem.
### alma-4dab36083aa6a4961db95c26

Group: `/run/irqbalance`. Source: `D1/in/raw/alma/members/4dab36083aa6a4961db95c26.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by irqbalance (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `irqbalance1097.sock`. Runtime object disappears with its backing filesystem.
### alma-7d043e590f7bae190581950c

Group: `/run/libpod`. Source: `D1/in/raw/alma/members/7d043e590f7bae190581950c.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by podman (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `alive`, `alive.lck`, `exits`, `persist`. Runtime object disappears with its backing filesystem.
### alma-ac1a26bed53b835cb406eb54

Group: `/run/lock`. Source: `D1/in/raw/alma/members/ac1a26bed53b835cb406eb54.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `kdump`, `netavark.lock`, `subsys`. Runtime object disappears with its backing filesystem.
### alma-2520ff48b107dc63f0b571b2

Group: `/run/lock/lvm`. Source: `D1/in/raw/alma/members/2520ff48b107dc63f0b571b2.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by lvm (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `D_system.devices`. Runtime object disappears with its backing filesystem.
### alma-65d43ca23f2435227bc35ffb

Group: `/run/log`. Source: `D1/in/raw/alma/members/65d43ca23f2435227bc35ffb.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-journald (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `journal`. Runtime object disappears with its backing filesystem.
### alma-7d3b25b913ddd47068b2dbfb

Group: `/run/log/journal`. Source: `D1/in/raw/alma/members/7d3b25b913ddd47068b2dbfb.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-journald (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `8ef0d28cd1cb4a80b9baa123cb63ef20`. Runtime object disappears with its backing filesystem.
### alma-595b87c9ffffbd0e80b0f586

Group: `/run/log/journal/8ef0d28cd1cb4a80b9baa123cb63ef20`. Source: `D1/in/raw/alma/members/595b87c9ffffbd0e80b0f586.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-journald (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `system.journal`. Runtime object disappears with its backing filesystem.
### alma-6253ca1def2105a53e86eddb

Group: `/run/lsm/ipc`. Source: `D1/in/raw/alma/members/6253ca1def2105a53e86eddb.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `.lsmd-ipc-lock`, `sim`, `simc`. Runtime object disappears with its backing filesystem.
### alma-3219fa2a25de45908392b8ec

Group: `/run/lvm`. Source: `D1/in/raw/alma/members/3219fa2a25de45908392b8ec.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by lvm (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `hints`, `initrd_no_filter`, `lvmpolld.socket`, `pvs_lookup`, `pvs_online`, `vgs_online`. Runtime object disappears with its backing filesystem.
### alma-7b15f71f3efe203df417893c

Group: `/run/lvm/pvs_online`. Source: `D1/in/raw/alma/members/7b15f71f3efe203df417893c.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by lvm (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `uIHV0WhCwwlaBud1S5GnovZs8pS8MEaV`. Runtime object disappears with its backing filesystem.
### alma-390ef834dd3266b1979625a9

Group: `/run/lvm/vgs_online`. Source: `D1/in/raw/alma/members/390ef834dd3266b1979625a9.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by lvm (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `almalinux`. Runtime object disappears with its backing filesystem.
### alma-217ea2ed7d6e051c56d28616

Group: `/run/selinux-policy`. Source: `D1/in/raw/alma/members/217ea2ed7d6e051c56d28616.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `extra_varrun.cil`, `extra_varrun_entries.txt`, `extra_varrun_entries_dup.txt`, `file_contexts_unified`. Runtime object disappears with its backing filesystem.
### alma-401ebe1b19f3dfbe6c025c3e

Group: `/run/ssh-unix-local`. Source: `D1/in/raw/alma/members/401ebe1b19f3dfbe6c025c3e.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `socket`. Runtime object disappears with its backing filesystem.
### alma-84e8f7c52f7aa85d9dcee0dd

Group: `/run/sudo`. Source: `D1/in/raw/alma/members/84e8f7c52f7aa85d9dcee0dd.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by sudo (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `ts`. Runtime object disappears with its backing filesystem.
### alma-413bae5a334118861dc76bb0

Group: `/run/systemd`. Source: `D1/in/raw/alma/members/413bae5a334118861dc76bb0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `ask-password`, `coredump`, `generator`, `inaccessible`, `incoming`, `inhibit`, `io.systemd.BootControl`, `io.systemd.Credentials`, `io.systemd.Hostname`, `io.systemd.ManagedOOM`, `io.systemd.sysext`, `journal`, `machines`, `mount-rootfs`, `network`, `notify`, `private`, `propagate`, `seats`, `sessions`, `shutdown`, `system`, `systemd-units-load`, `transient`, `units`, `userdb`, `users`. Runtime object disappears with its backing filesystem.
### alma-8af80e73b4b6c8b961b5b957

Group: `/run/systemd/generator`. Source: `D1/in/raw/alma/members/8af80e73b4b6c8b961b5b957.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `-.mount`, `boot.mount`, `dev-disk-by\x2duuid-7645a9bb\x2d294e\x2d4608\x2d9ac8\x2d0870677ce085.swap`, `getty.target.wants`, `local-fs.target.requires`, `local-fs.target.wants`, `sockets.target.wants`, `sshd-unix-local.socket`, `sshd-unix-local@.service`, `sshd-vsock.socket`, `sshd-vsock@.service`, `swap.target.requires`. Runtime object disappears with its backing filesystem.
### alma-75478788402be8c7b6967a4a

Group: `/run/systemd/generator/getty.target.wants`. Source: `D1/in/raw/alma/members/75478788402be8c7b6967a4a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `serial-getty@ttyS0.service`. Runtime object disappears with its backing filesystem.
### alma-3abcda753e4e302074db9a1f

Group: `/run/systemd/generator/local-fs.target.requires`. Source: `D1/in/raw/alma/members/3abcda753e4e302074db9a1f.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `-.mount`, `boot.mount`. Runtime object disappears with its backing filesystem.
### alma-904ac6b1c3dde89ef0c1ae58

Group: `/run/systemd/generator/local-fs.target.wants`. Source: `D1/in/raw/alma/members/904ac6b1c3dde89ef0c1ae58.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `systemd-remount-fs.service`. Runtime object disappears with its backing filesystem.
### alma-5b633e93a260cc6e4bb12437

Group: `/run/systemd/generator/sockets.target.wants`. Source: `D1/in/raw/alma/members/5b633e93a260cc6e4bb12437.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `sshd-unix-local.socket`, `sshd-vsock.socket`. Runtime object disappears with its backing filesystem.
### alma-dfd7f704cfbe04ec3aab90c7

Group: `/run/systemd/generator/swap.target.requires`. Source: `D1/in/raw/alma/members/dfd7f704cfbe04ec3aab90c7.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `dev-disk-by\x2duuid-7645a9bb\x2d294e\x2d4608\x2d9ac8\x2d0870677ce085.swap`. Runtime object disappears with its backing filesystem.
### alma-a57e2965bf7d1526bfb62caa

Group: `/run/systemd/inaccessible`. Source: `D1/in/raw/alma/members/a57e2965bf7d1526bfb62caa.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `blk`, `chr`, `dir`, `fifo`, `reg`, `sock`. Runtime object disappears with its backing filesystem.
### alma-7259977fddd8433ef380c0d0

Group: `/run/systemd/inhibit`. Source: `D1/in/raw/alma/members/7259977fddd8433ef380c0d0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `1`, `1.ref`, `2`, `2.ref`, `6`, `6.ref`. Runtime object disappears with its backing filesystem.
### alma-cca4d538f092aa1abbaceb25

Group: `/run/systemd/journal`. Source: `D1/in/raw/alma/members/cca4d538f092aa1abbaceb25.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `dev-log`, `io.systemd.journal`, `kernel-seqnum`, `seqnum`, `socket`, `stdout`, `streams`. Runtime object disappears with its backing filesystem.
### alma-53ba7ad7650b8ebc64cc5822

Group: `/run/systemd/journal/streams`. Source: `D1/in/raw/alma/members/53ba7ad7650b8ebc64cc5822.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `9:16463`, `9:16615`, `9:18355`, `9:18400`, `9:23500`, `9:26698`, `9:28586`, `9:29722`, `9:7450`, `9:7572`, `9:8034`, `9:8092`, `9:8123`, `9:8158`, `9:8196`, `9:8198`, `9:8259`, `9:8408`, `9:8489`, `9:8635`, `9:8658`, `9:8725`. Runtime object disappears with its backing filesystem.
### alma-15805d894690a78d31a843c3

Group: `/run/systemd/propagate`. Source: `D1/in/raw/alma/members/15805d894690a78d31a843c3.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `.os-release-stage`, `ModemManager.service`, `NetworkManager.service`, `accounts-daemon.service`, `chronyd.service`, `dbus-broker.service`, `firewalld.service`, `irqbalance.service`, `polkit.service`, `rsyslog.service`, `rtkit-daemon.service`, `systemd-hostnamed.service`, `systemd-logind.service`, `systemd-udevd.service`, `systemd-userdbd.service`, `upower.service`. Runtime object disappears with its backing filesystem.
### alma-1d97d157070ff8bacaa4df76

Group: `/run/systemd/propagate/.os-release-stage`. Source: `D1/in/raw/alma/members/1d97d157070ff8bacaa4df76.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `os-release`. Runtime object disappears with its backing filesystem.
### alma-61f1eb28c19ef6c2bb547ac2

Group: `/run/systemd/seats`. Source: `D1/in/raw/alma/members/61f1eb28c19ef6c2bb547ac2.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `seat0`. Runtime object disappears with its backing filesystem.
### alma-9dd63a3fa58a206e735a8f6a

Group: `/run/systemd/sessions`. Source: `D1/in/raw/alma/members/9dd63a3fa58a206e735a8f6a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `10`, `10.ref`, `18`, `18.ref`. Runtime object disappears with its backing filesystem.
### alma-2e3d765019cab6526cd7bd9f

Group: `/run/systemd/transient`. Source: `D1/in/raw/alma/members/2e3d765019cab6526cd7bd9f.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `session-18.scope`. Runtime object disappears with its backing filesystem.
### alma-a59e8fb1350c7f27463b5297

Group: `/run/systemd/units`. Source: `D1/in/raw/alma/members/a59e8fb1350c7f27463b5297.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `invocation:ModemManager.service`, `invocation:NetworkManager-wait-online.service`, `invocation:NetworkManager.service`, `invocation:accounts-daemon.service`, `invocation:atd.service`, `invocation:auditd.service`, `invocation:avahi-daemon.service`, `invocation:boot.mount`, `invocation:chronyd.service`, `invocation:cockpit.socket`, `invocation:crond.service`, `invocation:cups.service`, `invocation:dbus-broker.service`, `invocation:dev-disk-by\x2duuid-7645a9bb\x2d294e\x2d4608\x2d9ac8\x2d0870677ce085.swap`, `invocation:dev-hugepages.mount`, `invocation:dev-mqueue.mount`, `invocation:dracut-shutdown.service`, `invocation:firewalld.service`, `invocation:getty@tty1.service`, `invocation:irqbalance.service`, `invocation:kdump.service`, `invocation:kmod-static-nodes.service`, `invocation:ldconfig.service`, `invocation:libstoragemgmt.service`, `invocation:lvm2-monitor.service`, `invocation:packagekit.service`, `invocation:plymouth-quit-wait.service`, `invocation:plymouth-quit.service`, `invocation:plymouth-read-write.service`, `invocation:plymouth-start.service`, `invocation:polkit.service`, `invocation:rsyslog.service`, `invocation:rtkit-daemon.service`, `invocation:serial-getty@ttyS0.service`, `invocation:session-18.scope`, `invocation:ssh-host-keys-migration.service`, `invocation:sshd.service`, `invocation:sys-fs-fuse-connections.mount`, `invocation:sys-kernel-config.mount`, `invocation:sys-kernel-debug.mount`, `invocation:sys-kernel-tracing.mount`, `invocation:sysroot.mount`, `invocation:systemd-hostnamed.service`, `invocation:systemd-hwdb-update.service`, `invocation:systemd-journal-catalog-update.service`, `invocation:systemd-journal-flush.service`, `invocation:systemd-journald.service`, `invocation:systemd-logind.service`, `invocation:systemd-modules-load.service`, `invocation:systemd-network-generator.service`, `invocation:systemd-random-seed.service`, `invocation:systemd-remount-fs.service`, `invocation:systemd-sysctl.service`, `invocation:systemd-sysusers.service`, `invocation:systemd-tmpfiles-setup-dev-early.service`, `invocation:systemd-tmpfiles-setup-dev.service`, `invocation:systemd-tmpfiles-setup.service`, `invocation:systemd-udev-load-credentials.service`, `invocation:systemd-udev-trigger.service`, `invocation:systemd-udevd.service`, `invocation:systemd-update-done.service`, `invocation:systemd-update-utmp.service`, `invocation:systemd-user-sessions.service`, `invocation:systemd-userdbd.service`, `invocation:systemd-vconsole-setup.service`, `invocation:tuned-ppd.service`, `invocation:tuned.service`, `invocation:upower.service`, `invocation:user-runtime-dir@1000.service`, `invocation:user@1000.service`, `log-level-max:rtkit-daemon.service`. Runtime object disappears with its backing filesystem.
### alma-88ae7a6f45d4c15fb732a93a

Group: `/run/systemd/userdb`. Source: `D1/in/raw/alma/members/88ae7a6f45d4c15fb732a93a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `io.systemd.DropIn`, `io.systemd.DynamicUser`, `io.systemd.Multiplexer`, `io.systemd.NameServiceSwitch`. Runtime object disappears with its backing filesystem.
### alma-c2702c745b430adc63a6a7cb

Group: `/run/systemd/users`. Source: `D1/in/raw/alma/members/c2702c745b430adc63a6a7cb.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `1000`. Runtime object disappears with its backing filesystem.
### alma-abc3e1d04735ab930a624c37

Group: `/run/tmpfiles.d`. Source: `D1/in/raw/alma/members/abc3e1d04735ab930a624c37.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `static-nodes.conf`. Runtime object disappears with its backing filesystem.
### alma-4230d18f750bda20e1227cbc

Group: `/run/tpm2-tss`. Source: `D1/in/raw/alma/members/4230d18f750bda20e1227cbc.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `eventlog`. Runtime object disappears with its backing filesystem.
### alma-6c68574241d392e1ebe0afec

Group: `/run/tuned`. Source: `D1/in/raw/alma/members/6c68574241d392e1ebe0afec.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by tuned (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `tuned.pid`. Runtime object disappears with its backing filesystem.
### alma-55de793a8bf5a0fe8f203246

Group: `/run/udev`. Source: `D1/in/raw/alma/members/55de793a8bf5a0fe8f203246.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `control`, `data`, `links`, `links.lock`, `static_node-tags`, `tags`, `watch`. Runtime object disappears with its backing filesystem.
### alma-22ab90f5a079367165a637d7

Group: `/run/udev/data`. Source: `D1/in/raw/alma/members/22ab90f5a079367165a637d7.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `+acpi:ACPI0010:00`, `+acpi:LNXCPU:00`, `+acpi:LNXCPU:01`, `+acpi:LNXPWRBN:00`, `+acpi:LNXSYBUS:00`, `+acpi:LNXSYBUS:01`, `+acpi:LNXSYSTM:00`, `+acpi:PNP0103:00`, `+acpi:PNP0303:00`, `+acpi:PNP0400:00`, `+acpi:PNP0501:00`, `+acpi:PNP0700:00`, `+acpi:PNP0A03:00`, `+acpi:PNP0A06:00`, `+acpi:PNP0A06:01`, `+acpi:PNP0A06:02`, `+acpi:PNP0B00:00`, `+acpi:PNP0C0F:00`, `+acpi:PNP0C0F:01`, `+acpi:PNP0C0F:02`, `+acpi:PNP0C0F:03`, `+acpi:PNP0C0F:04`, `+acpi:PNP0F13:00`, `+acpi:QEMU0002:00`, `+dmi:id`, `+drm:card0-Virtual-1`, `+input:input0`, `+input:input1`, `+input:input3`, `+input:input4`, `+input:input5`, `+leds:input1::capslock`, `+leds:input1::numlock`, `+leds:input1::scrolllock`, `+module:configfs`, `+module:fuse`, `+pci:0000:00:00.0`, `+pci:0000:00:01.0`, `+pci:0000:00:01.1`, `+pci:0000:00:01.3`, `+pci:0000:00:02.0`, `+pci:0000:00:03.0`, `+pci:0000:00:04.0`, `+pci:0000:00:05.0`, `+platform:LNXPWRBN:00`, `+platform:PNP0103:00`, `+platform:QEMU0002:00`, `+platform:alarmtimer.0.auto`, `+platform:i8042`, `+platform:intel_rapl_msr.0`, `+platform:kgdboc`, `+platform:pcspkr`, `+platform:reg-dummy`, `+platform:serial8250`, `b11:0`, `b252:0`, `b252:1`, `b252:2`, `b252:3`, `b253:0`, `b253:1`, `c10:120`, `c10:121`, `c10:122`, `c10:123`, `c10:124`, `c10:125`, `c10:126`, `c10:127`, `c10:144`, `c10:183`, `c10:227`, `c10:228`, `c10:229`, `c10:231`, `c10:232`, `c10:234`, `c10:235`, `c10:236`, `c10:237`, `c10:242`, `c13:32`, `c13:33`, `c13:63`, `c13:64`, `c13:65`, `c13:66`, `c13:67`, `c13:68`, `c1:1`, `c1:11`, `c1:3`, `c1:4`, `c1:5`, `c1:7`, `c1:8`, `c1:9`, `c202:0`, `c202:1`, `c203:0`, `c203:1`, `c21:0`, `c226:0`, `c244:0`, `c246:0`, `c250:0`, `c251:0`, `c4:0`, `c4:1`, `c4:10`, `c4:11`, `c4:12`, `c4:13`, `c4:14`, `c4:15`, `c4:16`, `c4:17`, `c4:18`, `c4:19`, `c4:2`, `c4:20`, `c4:21`, `c4:22`, `c4:23`, `c4:24`, `c4:25`, `c4:26`, `c4:27`, `c4:28`, `c4:29`, `c4:3`, `c4:30`, `c4:31`, `c4:32`, `c4:33`, `c4:34`, `c4:35`, `c4:36`, `c4:37`, `c4:38`, `c4:39`, `c4:4`, `c4:40`, `c4:41`, `c4:42`, `c4:43`, `c4:44`, `c4:45`, `c4:46`, `c4:47`, `c4:48`, `c4:49`, `c4:5`, `c4:50`, `c4:51`, `c4:52`, `c4:53`, `c4:54`, `c4:55`, `c4:56`, `c4:57`, `c4:58`, `c4:59`, `c4:6`, `c4:60`, `c4:61`, `c4:62`, `c4:63`, `c4:64`, `c4:65`, `c4:66`, `c4:67`, `c4:7`, `c4:8`, `c4:9`, `c5:0`, `c5:1`, `c5:2`, `c7:0`, `c7:1`, `c7:128`, `c7:129`, `c7:130`, `c7:131`, `c7:132`, `c7:133`, `c7:134`, `c7:2`, `c7:3`, `c7:4`, `c7:5`, `c7:6`, `c7:64`, `c7:65`, `c7:66`, `c7:67`, `c7:68`, `c7:69`, `c7:70`, `c89:0`, `c99:0`, `n1`, `n2`, `n3`. Runtime object disappears with its backing filesystem.
### alma-746ea75f9f9f6e8014955998

Group: `/run/udev/links`. Source: `D1/in/raw/alma/members/746ea75f9f9f6e8014955998.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `almalinux\x2froot`, `almalinux\x2fswap`, `cdrom`, `disk\x2fby-diskseq\x2f1`, `disk\x2fby-diskseq\x2f1-part1`, `disk\x2fby-diskseq\x2f1-part2`, `disk\x2fby-diskseq\x2f1-part3`, `disk\x2fby-diskseq\x2f3`, `disk\x2fby-diskseq\x2f4`, `disk\x2fby-diskseq\x2f5`, `disk\x2fby-id\x2fata-QEMU_DVD-ROM_QM00003`, `disk\x2fby-id\x2fdm-name-almalinux-root`, `disk\x2fby-id\x2fdm-name-almalinux-swap`, `disk\x2fby-id\x2fdm-uuid-LVM-YN4YBItWITVpOTwVgVKzOw0rlAjdAq331HlXIW5RW5378StXhT7a4d7QlZpWFQlq`, `disk\x2fby-id\x2fdm-uuid-LVM-YN4YBItWITVpOTwVgVKzOw0rlAjdAq33vc8rttUlVWd1fSWY4Q2eKRHglsqg254W`, `disk\x2fby-id\x2flvm-pv-uuid-uIHV0W-hCww-laBu-d1S5-Gnov-Zs8p-S8MEaV`, `disk\x2fby-partuuid\x2f6ae9c8f1-fe86-4f12-a80d-468894b7d3e8`, `disk\x2fby-partuuid\x2fb159cbeb-817d-4f4f-bc81-5ec22c16a211`, `disk\x2fby-partuuid\x2fe63705f0-f14a-462d-a7df-f27a0cd8a693`, `disk\x2fby-path\x2fpci-0000:00:01.1-ata-2`, `disk\x2fby-path\x2fpci-0000:00:01.1-ata-2.0`, `disk\x2fby-path\x2fpci-0000:00:05.0`, `disk\x2fby-path\x2fpci-0000:00:05.0-part1`, `disk\x2fby-path\x2fpci-0000:00:05.0-part2`, `disk\x2fby-path\x2fpci-0000:00:05.0-part3`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f1`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f2`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f3`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2f6ae9c8f1-fe86-4f12-a80d-468894b7d3e8`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2fb159cbeb-817d-4f4f-bc81-5ec22c16a211`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2fe63705f0-f14a-462d-a7df-f27a0cd8a693`, `disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-uuid\x2f806e879d-60b4-4731-aa5b-d04420a5eddf`, `disk\x2fby-path\x2fvirtio-pci-0000:00:05.0`, `disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part1`, `disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part2`, `disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part3`, `disk\x2fby-uuid\x2f7645a9bb-294e-4608-9ac8-0870677ce085`, `disk\x2fby-uuid\x2f806e879d-60b4-4731-aa5b-d04420a5eddf`, `disk\x2fby-uuid\x2f9775aa51-073e-45c3-9aaf-2527c3e81c77`, `dri\x2fby-path\x2fpci-0000:00:02.0-card`, `input\x2fby-path\x2fplatform-LNXPWRBN:00-event`, `input\x2fby-path\x2fplatform-i8042-serio-0-event-kbd`, `input\x2fby-path\x2fplatform-i8042-serio-1-event-mouse`, `input\x2fby-path\x2fplatform-i8042-serio-1-mouse`, `input\x2fby-path\x2fplatform-pcspkr-event-spkr`, `mapper\x2falmalinux-root`, `mapper\x2falmalinux-swap`, `rtc`. Runtime object disappears with its backing filesystem.
### alma-7d9d8c998a3ab58e6a9a3491

Group: `/run/udev/links/almalinux\x2froot`. Source: `D1/in/raw/alma/members/7d9d8c998a3ab58e6a9a3491.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-ff90e20308dba785356b9554

Group: `/run/udev/links/almalinux\x2fswap`. Source: `D1/in/raw/alma/members/ff90e20308dba785356b9554.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-13a44f7217f3be3ba9c26206

Group: `/run/udev/links/cdrom`. Source: `D1/in/raw/alma/members/13a44f7217f3be3ba9c26206.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`. Runtime object disappears with its backing filesystem.
### alma-78ee6014d4d199371d0acc51

Group: `/run/udev/links/disk\x2fby-diskseq\x2f1`. Source: `D1/in/raw/alma/members/78ee6014d4d199371d0acc51.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:0`. Runtime object disappears with its backing filesystem.
### alma-c9da361c99d79c9cbaaad2cd

Group: `/run/udev/links/disk\x2fby-diskseq\x2f1-part1`. Source: `D1/in/raw/alma/members/c9da361c99d79c9cbaaad2cd.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-a3df757fb369f4ccc8010ec7

Group: `/run/udev/links/disk\x2fby-diskseq\x2f1-part2`. Source: `D1/in/raw/alma/members/a3df757fb369f4ccc8010ec7.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-6ce45e85020967205052bcd9

Group: `/run/udev/links/disk\x2fby-diskseq\x2f1-part3`. Source: `D1/in/raw/alma/members/6ce45e85020967205052bcd9.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-98f6e9f4cfac85f4d1d07148

Group: `/run/udev/links/disk\x2fby-diskseq\x2f3`. Source: `D1/in/raw/alma/members/98f6e9f4cfac85f4d1d07148.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`. Runtime object disappears with its backing filesystem.
### alma-a2501e69a9412e5ffc2eecf8

Group: `/run/udev/links/disk\x2fby-diskseq\x2f4`. Source: `D1/in/raw/alma/members/a2501e69a9412e5ffc2eecf8.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-c0191e61a6483fc2dc91bc2f

Group: `/run/udev/links/disk\x2fby-diskseq\x2f5`. Source: `D1/in/raw/alma/members/c0191e61a6483fc2dc91bc2f.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-3313d2bfb6637601b0f6e2b8

Group: `/run/udev/links/disk\x2fby-id\x2fata-QEMU_DVD-ROM_QM00003`. Source: `D1/in/raw/alma/members/3313d2bfb6637601b0f6e2b8.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`. Runtime object disappears with its backing filesystem.
### alma-f94c0b543128fb19b9fe0a5c

Group: `/run/udev/links/disk\x2fby-id\x2fdm-name-almalinux-root`. Source: `D1/in/raw/alma/members/f94c0b543128fb19b9fe0a5c.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-62e9c54380fbcec874763e7c

Group: `/run/udev/links/disk\x2fby-id\x2fdm-name-almalinux-swap`. Source: `D1/in/raw/alma/members/62e9c54380fbcec874763e7c.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-c6d7d8bab14655f540012b3f

Group: `/run/udev/links/disk\x2fby-id\x2fdm-uuid-LVM-YN4YBItWITVpOTwVgVKzOw0rlAjdAq331HlXIW5RW5378StXhT7a4d7QlZpWFQlq`. Source: `D1/in/raw/alma/members/c6d7d8bab14655f540012b3f.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-df28b8158f95e248078c9e3b

Group: `/run/udev/links/disk\x2fby-id\x2fdm-uuid-LVM-YN4YBItWITVpOTwVgVKzOw0rlAjdAq33vc8rttUlVWd1fSWY4Q2eKRHglsqg254W`. Source: `D1/in/raw/alma/members/df28b8158f95e248078c9e3b.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-1a80796388e304dbc7e59da5

Group: `/run/udev/links/disk\x2fby-id\x2flvm-pv-uuid-uIHV0W-hCww-laBu-d1S5-Gnov-Zs8p-S8MEaV`. Source: `D1/in/raw/alma/members/1a80796388e304dbc7e59da5.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-c2a477df134ada8ebf819afd

Group: `/run/udev/links/disk\x2fby-partuuid\x2f6ae9c8f1-fe86-4f12-a80d-468894b7d3e8`. Source: `D1/in/raw/alma/members/c2a477df134ada8ebf819afd.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-bbf0d1e7cc28bc90d8fbfd9a

Group: `/run/udev/links/disk\x2fby-partuuid\x2fb159cbeb-817d-4f4f-bc81-5ec22c16a211`. Source: `D1/in/raw/alma/members/bbf0d1e7cc28bc90d8fbfd9a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-430fe728336351264d5db271

Group: `/run/udev/links/disk\x2fby-partuuid\x2fe63705f0-f14a-462d-a7df-f27a0cd8a693`. Source: `D1/in/raw/alma/members/430fe728336351264d5db271.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-a60b6626c3424f0c171de029

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:01.1-ata-2`. Source: `D1/in/raw/alma/members/a60b6626c3424f0c171de029.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`. Runtime object disappears with its backing filesystem.
### alma-3a5147bc393f4835cb64f045

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:01.1-ata-2.0`. Source: `D1/in/raw/alma/members/3a5147bc393f4835cb64f045.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`. Runtime object disappears with its backing filesystem.
### alma-1f6ec29aa8d7a5561aae4e55

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0`. Source: `D1/in/raw/alma/members/1f6ec29aa8d7a5561aae4e55.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:0`. Runtime object disappears with its backing filesystem.
### alma-e7dff59b69368afdcb5907ff

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part1`. Source: `D1/in/raw/alma/members/e7dff59b69368afdcb5907ff.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-8eb217a7067e1bed3d1066d2

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part2`. Source: `D1/in/raw/alma/members/8eb217a7067e1bed3d1066d2.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-61ced196638afa9b56c21c5b

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part3`. Source: `D1/in/raw/alma/members/61ced196638afa9b56c21c5b.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-700ea897bdbe8e3296380fdb

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f1`. Source: `D1/in/raw/alma/members/700ea897bdbe8e3296380fdb.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-d97a06a207686faf4e43af74

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f2`. Source: `D1/in/raw/alma/members/d97a06a207686faf4e43af74.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-367520eed3be145f15c63e17

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f3`. Source: `D1/in/raw/alma/members/367520eed3be145f15c63e17.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-84990ebaaba3e0779cbb7741

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2f6ae9c8f1-fe86-4f12-a80d-468894b7d3e8`. Source: `D1/in/raw/alma/members/84990ebaaba3e0779cbb7741.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-72fc140848aca804887d6bed

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2fb159cbeb-817d-4f4f-bc81-5ec22c16a211`. Source: `D1/in/raw/alma/members/72fc140848aca804887d6bed.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-e8b6454c7425d2f4950c53a4

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partuuid\x2fe63705f0-f14a-462d-a7df-f27a0cd8a693`. Source: `D1/in/raw/alma/members/e8b6454c7425d2f4950c53a4.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-6708c55192e643bdf5a35022

Group: `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-uuid\x2f806e879d-60b4-4731-aa5b-d04420a5eddf`. Source: `D1/in/raw/alma/members/6708c55192e643bdf5a35022.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-7043f18b2ae61fcefc4bb8b6

Group: `/run/udev/links/disk\x2fby-path\x2fvirtio-pci-0000:00:05.0`. Source: `D1/in/raw/alma/members/7043f18b2ae61fcefc4bb8b6.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:0`. Runtime object disappears with its backing filesystem.
### alma-5df24d9f4fd80a9b406bc303

Group: `/run/udev/links/disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part1`. Source: `D1/in/raw/alma/members/5df24d9f4fd80a9b406bc303.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:1`. Runtime object disappears with its backing filesystem.
### alma-c6c5acb27fa502ccc0ce02e0

Group: `/run/udev/links/disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part2`. Source: `D1/in/raw/alma/members/c6c5acb27fa502ccc0ce02e0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-9708e6d2f5203c57162bba02

Group: `/run/udev/links/disk\x2fby-path\x2fvirtio-pci-0000:00:05.0-part3`. Source: `D1/in/raw/alma/members/9708e6d2f5203c57162bba02.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:3`. Runtime object disappears with its backing filesystem.
### alma-c1c061d5272019b8ad097fe4

Group: `/run/udev/links/disk\x2fby-uuid\x2f7645a9bb-294e-4608-9ac8-0870677ce085`. Source: `D1/in/raw/alma/members/c1c061d5272019b8ad097fe4.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-1e8ae716d73ddaa2260f3ec0

Group: `/run/udev/links/disk\x2fby-uuid\x2f806e879d-60b4-4731-aa5b-d04420a5eddf`. Source: `D1/in/raw/alma/members/1e8ae716d73ddaa2260f3ec0.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b252:2`. Runtime object disappears with its backing filesystem.
### alma-2b524c3fe7d3ff0909e02508

Group: `/run/udev/links/disk\x2fby-uuid\x2f9775aa51-073e-45c3-9aaf-2527c3e81c77`. Source: `D1/in/raw/alma/members/2b524c3fe7d3ff0909e02508.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-a2b1015175be39e31591b798

Group: `/run/udev/links/dri\x2fby-path\x2fpci-0000:00:02.0-card`. Source: `D1/in/raw/alma/members/a2b1015175be39e31591b798.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c226:0`. Runtime object disappears with its backing filesystem.
### alma-4c2c0293eff90d31cc4849f4

Group: `/run/udev/links/input\x2fby-path\x2fplatform-LNXPWRBN:00-event`. Source: `D1/in/raw/alma/members/4c2c0293eff90d31cc4849f4.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:64`. Runtime object disappears with its backing filesystem.
### alma-067ee47347ed1b4d66791410

Group: `/run/udev/links/input\x2fby-path\x2fplatform-i8042-serio-0-event-kbd`. Source: `D1/in/raw/alma/members/067ee47347ed1b4d66791410.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:65`. Runtime object disappears with its backing filesystem.
### alma-436a54f4e6d8b30a5e5442bc

Group: `/run/udev/links/input\x2fby-path\x2fplatform-i8042-serio-1-event-mouse`. Source: `D1/in/raw/alma/members/436a54f4e6d8b30a5e5442bc.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:66`, `c13:67`. Runtime object disappears with its backing filesystem.
### alma-4d32ab7a1983e098ca0fdcc9

Group: `/run/udev/links/input\x2fby-path\x2fplatform-i8042-serio-1-mouse`. Source: `D1/in/raw/alma/members/4d32ab7a1983e098ca0fdcc9.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:32`, `c13:33`. Runtime object disappears with its backing filesystem.
### alma-b3d1225b32a173d809fa6b25

Group: `/run/udev/links/input\x2fby-path\x2fplatform-pcspkr-event-spkr`. Source: `D1/in/raw/alma/members/b3d1225b32a173d809fa6b25.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:68`. Runtime object disappears with its backing filesystem.
### alma-c491c707a21fd9bda8bc2c2a

Group: `/run/udev/links/mapper\x2falmalinux-root`. Source: `D1/in/raw/alma/members/c491c707a21fd9bda8bc2c2a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:0`. Runtime object disappears with its backing filesystem.
### alma-d9a4a20238051218a2e16f38

Group: `/run/udev/links/mapper\x2falmalinux-swap`. Source: `D1/in/raw/alma/members/d9a4a20238051218a2e16f38.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b253:1`. Runtime object disappears with its backing filesystem.
### alma-ad249d485a6c47f2922f06d9

Group: `/run/udev/links/rtc`. Source: `D1/in/raw/alma/members/ad249d485a6c47f2922f06d9.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c250:0`. Runtime object disappears with its backing filesystem.
### alma-08b20e9683c1477e7cd084ca

Group: `/run/udev/static_node-tags`. Source: `D1/in/raw/alma/members/08b20e9683c1477e7cd084ca.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `uaccess`. Runtime object disappears with its backing filesystem.
### alma-edde743795079f14c2449784

Group: `/run/udev/static_node-tags/uaccess`. Source: `D1/in/raw/alma/members/edde743795079f14c2449784.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `snd\x2fseq`, `snd\x2ftimer`. Runtime object disappears with its backing filesystem.
### alma-3341a20e12db1c5f77acfdf7

Group: `/run/udev/tags`. Source: `D1/in/raw/alma/members/3341a20e12db1c5f77acfdf7.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `master-of-seat`, `power-switch`, `seat`, `systemd`, `uaccess`. Runtime object disappears with its backing filesystem.
### alma-dbb29aaca7d39650e939e504

Group: `/run/udev/tags/master-of-seat`. Source: `D1/in/raw/alma/members/dbb29aaca7d39650e939e504.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `+drm:card0-Virtual-1`, `c226:0`. Runtime object disappears with its backing filesystem.
### alma-4a08926197b62c3d574edb71

Group: `/run/udev/tags/power-switch`. Source: `D1/in/raw/alma/members/4a08926197b62c3d574edb71.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `c13:64`, `c13:65`. Runtime object disappears with its backing filesystem.
### alma-6467831a74f19635edeefb72

Group: `/run/udev/tags/seat`. Source: `D1/in/raw/alma/members/6467831a74f19635edeefb72.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `+drm:card0-Virtual-1`, `+input:input0`, `+input:input1`, `+input:input3`, `+input:input4`, `+input:input5`, `+leds:input1::capslock`, `+leds:input1::numlock`, `+leds:input1::scrolllock`, `b11:0`, `c10:125`, `c10:242`, `c21:0`, `c226:0`. Runtime object disappears with its backing filesystem.
### alma-1c062017d0dbd2323ffc757e

Group: `/run/udev/tags/systemd`. Source: `D1/in/raw/alma/members/1c062017d0dbd2323ffc757e.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `+module:configfs`, `+module:fuse`, `b11:0`, `b252:0`, `b252:1`, `b252:2`, `b252:3`, `b253:0`, `b253:1`, `c10:242`, `c4:64`, `c4:65`, `c4:66`, `c4:67`, `n2`, `n3`. Runtime object disappears with its backing filesystem.
### alma-8c202744a7f93334ba8090ea

Group: `/run/udev/tags/uaccess`. Source: `D1/in/raw/alma/members/8c202744a7f93334ba8090ea.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `b11:0`, `c10:125`, `c10:242`, `c21:0`, `c226:0`. Runtime object disappears with its backing filesystem.
### alma-4698e0e9a0c3c226834b2241

Group: `/run/udev/watch`. Source: `D1/in/raw/alma/members/4698e0e9a0c3c226834b2241.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd-udevd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `10`, `11`, `12`, `7`, `8`, `9`, `b252:0`, `b252:1`, `b252:2`, `b252:3`, `b253:0`, `b253:1`. Runtime object disappears with its backing filesystem.
### alma-59d03bb85a2144d9bc59b4c6

Group: `/run/user`. Source: `D1/in/raw/alma/members/59d03bb85a2144d9bc59b4c6.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `1000`. Runtime object disappears with its backing filesystem.
### alma-ca3222221a77d4bfdac50c9a

Group: `/run/user/1000`. Source: `D1/in/raw/alma/members/ca3222221a77d4bfdac50c9a.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by runtime filesystem setting (UNKNOWN); none is a separate stored object.

- **RUNTIME**: `bus`, `cal-agent.sock`, `pipewire-0`, `pipewire-0-manager`, `pulse`, `systemd`. Runtime object disappears with its backing filesystem.
### alma-3654a1c9596e75f86a8c4989

Group: `/run/user/1000/pulse`. Source: `D1/in/raw/alma/members/3654a1c9596e75f86a8c4989.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by pipewire-pulse (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `native`. Runtime object disappears with its backing filesystem.
### alma-7b89b2ac185727d3dd0b3299

Group: `/run/user/1000/systemd`. Source: `D1/in/raw/alma/members/7b89b2ac185727d3dd0b3299.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `generator.late`, `inaccessible`, `notify`, `private`, `propagate`, `units`. Runtime object disappears with its backing filesystem.
### alma-f6873193d606fd8d4f805efe

Group: `/run/user/1000/systemd/generator.late`. Source: `D1/in/raw/alma/members/f6873193d606fd8d4f805efe.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `app-at\x2dspi\x2ddbus\x2dbus@autostart.service`, `app-geoclue\x2ddemo\x2dagent@autostart.service`, `app-gnome\x2dinitial\x2dsetup\x2dfirst\x2dlogin@autostart.service`, `app-gnome\x2dkeyring\x2dpkcs11@autostart.service`, `app-gnome\x2dkeyring\x2dsecrets@autostart.service`, `app-gnome\x2dkeyring\x2dssh@autostart.service`, `app-orca\x2dautostart@autostart.service`, `app-org.gnome.Evolution\x2dalarm\x2dnotify@autostart.service`, `app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service`, `app-org.gnome.Software@autostart.service`, `app-spice\x2dvdagent@autostart.service`, `app-user\x2ddirs\x2dupdate\x2dgtk@autostart.service`, `app-vmware\x2duser@autostart.service`, `xdg-desktop-autostart.target.wants`. Runtime object disappears with its backing filesystem.
### alma-f88e364f7fcdcc897ea7d949

Group: `/run/user/1000/systemd/generator.late/xdg-desktop-autostart.target.wants`. Source: `D1/in/raw/alma/members/f88e364f7fcdcc897ea7d949.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `app-at\x2dspi\x2ddbus\x2dbus@autostart.service`, `app-geoclue\x2ddemo\x2dagent@autostart.service`, `app-gnome\x2dinitial\x2dsetup\x2dfirst\x2dlogin@autostart.service`, `app-gnome\x2dkeyring\x2dpkcs11@autostart.service`, `app-gnome\x2dkeyring\x2dsecrets@autostart.service`, `app-gnome\x2dkeyring\x2dssh@autostart.service`, `app-orca\x2dautostart@autostart.service`, `app-org.gnome.Evolution\x2dalarm\x2dnotify@autostart.service`, `app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service`, `app-org.gnome.Software@autostart.service`, `app-spice\x2dvdagent@autostart.service`, `app-user\x2ddirs\x2dupdate\x2dgtk@autostart.service`, `app-vmware\x2duser@autostart.service`. Runtime object disappears with its backing filesystem.
### alma-f6c8c24342e9c2d58b5d4b45

Group: `/run/user/1000/systemd/inaccessible`. Source: `D1/in/raw/alma/members/f6c8c24342e9c2d58b5d4b45.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `chr`, `dir`, `fifo`, `reg`, `sock`. Runtime object disappears with its backing filesystem.
### alma-c8164bf417f7683ad0ffad5c

Group: `/run/user/1000/systemd/propagate`. Source: `D1/in/raw/alma/members/c8164bf417f7683ad0ffad5c.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `.os-release-stage`. Runtime object disappears with its backing filesystem.
### alma-d7d4d6f74925956d5296154e

Group: `/run/user/1000/systemd/propagate/.os-release-stage`. Source: `D1/in/raw/alma/members/d7d4d6f74925956d5296154e.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `os-release`. Runtime object disappears with its backing filesystem.
### alma-73a4f540ff34f70c28ed1366

Group: `/run/user/1000/systemd/units`. Source: `D1/in/raw/alma/members/73a4f540ff34f70c28ed1366.tsv`. Decision: **RUNTIME**.

All members have runtime backing; created by systemd (INSTALLED-PACKAGE); none is a separate stored object.

- **RUNTIME**: `invocation:cal-user.service`, `invocation:dbus.socket`, `invocation:systemd-tmpfiles-setup.service`. Runtime object disappears with its backing filesystem.
### alma-c571e054fdcb5f06b326b34f

Group: `/tmp`. Source: `D1/in/raw/alma/members/c571e054fdcb5f06b326b34f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `.ICE-unix`, `.X11-unix`, `.XIM-unix`, `.font-unix`, `node-compile-cache`, `systemd-private-fc33f2ec36db4febbb440b973d327901-ModemManager.service-MT9ySN`, `systemd-private-fc33f2ec36db4febbb440b973d327901-NetworkManager.service-eNm85Z`, `systemd-private-fc33f2ec36db4febbb440b973d327901-chronyd.service-EVSzSZ`, `systemd-private-fc33f2ec36db4febbb440b973d327901-dbus-broker.service-otpwJi`, `systemd-private-fc33f2ec36db4febbb440b973d327901-irqbalance.service-BN32Zb`, `systemd-private-fc33f2ec36db4febbb440b973d327901-polkit.service-2cQkkN`, `systemd-private-fc33f2ec36db4febbb440b973d327901-rtkit-daemon.service-UZ5bPP`, `systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-hostnamed.service-YninRA`, `systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-logind.service-bs7FQZ`, `systemd-private-fc33f2ec36db4febbb440b973d327901-upower.service-WOUtsm`, `tmp2rnbd63v.mozrunner`. Directory installation integrity and creation provenance are not established.
### alma-fc3a9c1a217920505a6344db

Group: `/tmp/node-compile-cache`. Source: `D1/in/raw/alma/members/fc3a9c1a217920505a6344db.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `v22.23.4-x64-9de703df-1000`. Directory installation integrity and creation provenance are not established.
### alma-b00aa976d81ff928ec33f54c

Group: `/tmp/node-compile-cache/v22.23.4-x64-9de703df-1000`. Source: `D1/in/raw/alma/members/b00aa976d81ff928ec33f54c.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `0035fdca`, `00a3b020`, `00c19c05`, `0103303a`, `0160f3ae`, `019407bf`, `020fccc4`, `032fbb62`, `03aafa65`, `03c10c15`, `0405e474`, `0496bc19`, `0499d7c8`, `0536e6ac`, `053d5c1a`, `059f135a`, `0669367f`, `06bca121`, `06eaa93a`, `0772e738`, `0807c413`, `08583f07`, `09108240`, `09f39bb4`, `0a178b28`, `0a50a256`, `0aa69f38`, `0ace7c3c`, `0b1aadd5`, `0b4bb695`, `0b5cf72e`, `0baf8f12`, `0c03dbde`, `0c0f0d98`, `0c4a5655`, `0c5ae2f6`, `0ceb8ffc`, `0cefb93a`, `0cfc75a4`, `0d726693`, `0d778cb6`, `0dccb794`, `0e2234d8`, `0f086f03`, `0f247247`, `0f686ccb`, `0fc7c350`, `115b7f92`, `1243cd83`, `131dbc67`, `13b36fd3`, `14de52f4`, `152f406c`, `1559c03d`, `159b838d`, `15bb81e1`, `15c1d6d1`, `16371285`, `1642077d`, `16dbb0ab`, `16f73ca2`, `18738909`, `195c0a13`, `1a526084`, `1b068456`, `1b810ebd`, `1ed9aac4`, `1f244e0a`, `1f960353`, `208a5f82`, `209ed445`, `20c1bdad`, `2241cab2`, `224f0406`, `225ad284`, `23f070a1`, `243f93da`, `246ace1d`, `2474562e`, `24edd14e`, `257b809a`, `25b28a05`, `265575c2`, `2658fce3`, `267dfe37`, `26b18fe0`, `26d3bc39`, `274c23c0`, `27bce088`, `27fd403e`, `285f8c5e`, `28767493`, `28b81c55`, `28bafc0a`, `28cd5635`, `293fd4af`, `29603379`, `29c46d20`, `2ab661a4`, `2b5cfb1e`, `2bc99fe0`, `2bf4b3ef`, `2c93bbe5`, `2cd0fca2`, `2da2c104`, `2eae9040`, `2f258e25`, `2f95606c`, `2fc76576`, `3079ceb1`, `30d4661c`, `310c9d45`, `314a004f`, `322684ce`, `323cc4fa`, `32a99e36`, `331cfeef`, `334601da`, `33588215`, `35c53b8d`, `35fbf102`, `36621ffd`, `36a068b5`, `36a1737f`, `36a6399a`, `36c9e234`, `3860a317`, `386cb91e`, `38906414`, `38c0cf77`, `397066d7`, `3992922d`, `3a0efdcd`, `3a17021b`, `3aa3bbe0`, `3afb5d64`, `3b0c8889`, `3b0ed02e`, `3c740539`, `3d44f8ad`, `3dcaf6b0`, `3e3076ff`, `3f65c88d`, `3fc3776d`, `405d2cd5`, `411bc386`, `412c8319`, `413469a3`, `41b980a4`, `4322f2fa`, `4332ea13`, `439d86da`, `43be58c2`, `4406b13c`, `444d5d1a`, `445e6276`, `44ca9fa9`, `45f71794`, `45fc8ff6`, `46b7c450`, `47615d77`, `47e14bcd`, `47f2223d`, `486b0c83`, `4919e81c`, `4a045667`, `4a1a0997`, `4b0e2937`, `4ce16b65`, `4d57acd1`, `4de36ff6`, `4e164e56`, `4ef07ed9`, `4f852f2e`, `4feae201`, `4fee5fe3`, `500dc8ff`, `51086f64`, `510b2bf0`, `5113adba`, `51dffe84`, `52be73ea`, `533efb9a`, `5381c5a6`, `539675fc`, `54775c05`, `55208a24`, `552a9266`, `557a0990`, `55ed895c`, `561de353`, `567a89f0`, `5779a5af`, `5792478c`, `58642d29`, `589ab9a7`, `593f9078`, `5965aea2`, `599e7503`, `59a90b2a`, `5b26dbc1`, `5b2df877`, `5b3361fc`, `5bfdf6bd`, `5c1b5879`, `5d4e5ae2`, `5e3bd39d`, `5e758b8b`, `5ea22fb2`, `5ea2f522`, `5f211940`, `5f5e9b44`, `5fa926a7`, `5fb33bcd`, `605b4916`, `60b00a2b`, `613a5202`, `6246a164`, `62f96799`, `63270266`, `6450d8c2`, `64a9aac0`, `65214822`, `657d04c9`, `65b6e1df`, `66cd71c9`, `67c025e0`, `67ed505d`, `67f76d7d`, `6853473e`, `68a79769`, `69962814`, `69b72a1d`, `6a41e48e`, `6a92dd29`, `6af6e22e`, `6b04a6fb`, `6b1fc179`, `6c3221b3`, `6ced7693`, `6d1f832c`, `6dc1d215`, `6f543c2e`, `6f8aa49b`, `6ff1166f`, `703c5873`, `703f9ae8`, `70b0f832`, `71008d04`, `7111a7ff`, `711697cf`, `7151814a`, `72a7ac40`, `73430f21`, `74bee3cf`, `75d41d45`, `761cd9ff`, `762cf1ca`, `773ac697`, `774f3eac`, `77586e02`, `776961f4`, `77cd7596`, `783c40bc`, `783f5b9e`, `78f12523`, `7917fd18`, `795a2207`, `7a127ae6`, `7a88efc6`, `7b031a55`, `7b37b65b`, `7b973688`, `7b9c8f51`, `7d743605`, `7dfd1f2f`, `7e2debc2`, `7e5b1790`, `7eb70763`, `7f9a7fb6`, `804592b6`, `80fd6fda`, `8103e428`, `815cedfb`, `825644d5`, `83569cce`, `840e212e`, `8412e3c0`, `85af3f9a`, `866f09dd`, `86a0024a`, `88e1eaeb`, `8918d195`, `8941ffae`, `8944f076`, `89bae011`, `8a0dd34b`, `8af34ba4`, `8af6ac60`, `8b0355ba`, `8b0bac7f`, `8b34abdf`, `8bc076b0`, `8c06745d`, `8c13b9cf`, `8edf9b00`, `90f4185f`, `912b487b`, `916bff17`, `919a891b`, `91e31421`, `91f483c5`, `927abb58`, `92b8ee12`, `941e605a`, `947763e1`, `948c7fa5`, `94b15d3c`, `94b41c48`, `9536cf46`, `95421764`, `95427227`, `95b502d4`, `96194414`, `97f18b9e`, `981bb3a8`, `9825e365`, `98c28851`, `99354747`, `9967b89d`, `9a832e19`, `9aae81c4`, `9acc1461`, `9afada42`, `9b21c91c`, `9b3d9c16`, `9b562b0e`, `9b9a3f45`, `9badda03`, `9c028c68`, `9c3952ef`, `9ce5652d`, `9ce7fbb1`, `9d5038af`, `9e1ad488`, `9e30f13c`, `9e61cf58`, `9ea81fee`, `9f791004`, `9f87cb83`, `9fc32991`, `a035e8c2`, `a039abb5`, `a27a74c7`, `a315e5e4`, `a389555a`, `a45b1e09`, `a4e400a8`, `a4ee1175`, `a52006eb`, `a54199b8`, `a65ed53d`, `a66622c4`, `a6cb37b7`, `a78e8bde`, `a7b21c65`, `a7d84a00`, `a8985853`, `a91e6f10`, `a93858d8`, `a93f84d5`, `a994a4d2`, `a9ad46e5`, `a9b30a21`, `a9c44b8f`, `aa7bcc08`, `ab086642`, `ab6fd6b9`, `acee6846`, `ae636b9c`, `ae7fcf7f`, `ae8a5f8b`, `ae8d4be1`, `aeb6b547`, `aed378db`, `aee4a880`, `aefb21ef`, `af2cdbcf`, `b0a7c23c`, `b18fa0d0`, `b1c180b2`, `b1d46c51`, `b21a9c41`, `b26dbabf`, `b2cef868`, `b30169e8`, `b38594f1`, `b3bfca11`, `b3c44dd9`, `b42d7203`, `b466c4b0`, `b4af50a0`, `b5ea9a53`, `b672d3bf`, `b6f376db`, `b70d58cf`, `b8bbfec0`, `b8c4ddb6`, `b997b161`, `ba216ef3`, `baffda37`, `bb863f12`, `bc176a8b`, `bd78b1f9`, `bd7b7430`, `bd9fec0c`, `bdf401e0`, `c06b0e91`, `c16e4c82`, `c27673e8`, `c2d47a2f`, `c31a6a75`, `c44990c3`, `c4b7c9b7`, `c4c1f465`, `c4cc7f96`, `c544b9b6`, `c733aa68`, `c735069c`, `c805f1e6`, `c907d031`, `c98f6c2b`, `caa38f08`, `cb0ee660`, `cbc71f9e`, `cbdc3536`, `cc5cd89c`, `ccc7ff63`, `cce31d21`, `cd028e4e`, `cdc901e0`, `cf0d611c`, `cff0632c`, `d02dd804`, `d0596e4f`, `d08b8661`, `d0fd956e`, `d1396dd4`, `d164440b`, `d1ad410b`, `d295f7ff`, `d2de9960`, `d30020e4`, `d335b322`, `d34bcd0b`, `d37dc23b`, `d3ad8313`, `d4b58431`, `d5b282c1`, `d5cafcd1`, `d5f27103`, `d680b7b2`, `d6e102f4`, `d707b8ae`, `d7080463`, `d70a3c38`, `d872225f`, `d9affe6e`, `da38e175`, `da837369`, `db93463b`, `dc67fb1b`, `dc8d94e1`, `dd0783c4`, `dd1ac194`, `dd494ba7`, `ddb753be`, `ddf169dc`, `de780730`, `de8dc1e2`, `de8fffda`, `dfa07c5e`, `e0c9dc96`, `e27cd459`, `e2bc9eb9`, `e38ee5da`, `e3abe648`, `e414dfe4`, `e4c29f93`, `e4f81cfe`, `e52223c6`, `e533fbd2`, `e67af891`, `e793034a`, `e8760ef7`, `e8a608a6`, `e8c68c2b`, `e99d18eb`, `e9a987c2`, `ea1bf64c`, `eb2284a9`, `eb31072e`, `ec083fc8`, `ec27b8d0`, `ec3dc670`, `ed2cb918`, `ed6b1a31`, `edd1c0ed`, `ee25d27b`, `ee96d5c6`, `eeb0c590`, `eec00604`, `eedfb42b`, `ef3048f2`, `efb9b987`, `f09e9831`, `f11a0840`, `f18305cc`, `f20c1da3`, `f25e3dde`, `f528922c`, `f531b8a1`, `f573532f`, `f586066c`, `f5869e48`, `f5da3ce6`, `f5e149b5`, `f65dd091`, `f698e1bb`, `f78a941b`, `f7aa18f8`, `f7bda4c6`, `f9e3fc0f`, `fa55b7b1`, `faa52471`, `faa61ba9`, `fb2a53c0`, `fb6b2e0e`, `fbaac3d6`, `fbd3a493`, `fbead110`, `fbf89df5`, `fbfbb93e`, `fc460f17`, `fccaabd8`, `fd38a18d`, `fd5e8655`, `fd761e6b`, `fe321e2b`, `fe5803af`, `ff18df37`, `ff1d6c8f`. Package origin, unchangedness, and source of this object are not established.
### alma-f83399fbbeacfcf957b9a068

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-ModemManager.service-MT9ySN`. Source: `D1/in/raw/alma/members/f83399fbbeacfcf957b9a068.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-d76221fd84e871f412bc2c22

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-NetworkManager.service-eNm85Z`. Source: `D1/in/raw/alma/members/d76221fd84e871f412bc2c22.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-4640a2de00fbf9fe09cbd5ab

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-chronyd.service-EVSzSZ`. Source: `D1/in/raw/alma/members/4640a2de00fbf9fe09cbd5ab.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-2ab87cb73cbd2e087708bf95

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-dbus-broker.service-otpwJi`. Source: `D1/in/raw/alma/members/2ab87cb73cbd2e087708bf95.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-83e5a1f1adbce000d88ad712

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-irqbalance.service-BN32Zb`. Source: `D1/in/raw/alma/members/83e5a1f1adbce000d88ad712.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-e88f4f93d94907142c435d59

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-polkit.service-2cQkkN`. Source: `D1/in/raw/alma/members/e88f4f93d94907142c435d59.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-08c42992ea726939c20afc0b

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-rtkit-daemon.service-UZ5bPP`. Source: `D1/in/raw/alma/members/08c42992ea726939c20afc0b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-9674ecd7c1d78e48e967c3cb

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-hostnamed.service-YninRA`. Source: `D1/in/raw/alma/members/9674ecd7c1d78e48e967c3cb.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-dbcc79dfaa18943b2b995358

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-logind.service-bs7FQZ`. Source: `D1/in/raw/alma/members/dbcc79dfaa18943b2b995358.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-87e3bb861224781042e0f84b

Group: `/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-upower.service-WOUtsm`. Source: `D1/in/raw/alma/members/87e3bb861224781042e0f84b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-3d21e04a8d06b030e2bb4f02

Group: `/tmp/tmp2rnbd63v.mozrunner`. Source: `D1/in/raw/alma/members/3d21e04a8d06b030e2bb4f02.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `prefs.js`, `user.js`. Package origin, unchangedness, and source of this object are not established.
### alma-7a44f2401045f014c7068af6

Group: `/usr/bin`. Source: `D1/in/raw/alma/members/7a44f2401045f014c7068af6.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cancel`, `lp`, `lpq`, `lpr`, `lprm`, `lpstat`. Package origin, unchangedness, and source of this object are not established.
### alma-3366d0a0c1683ebef137e695

Group: `/usr/lib`. Source: `D1/in/raw/alma/members/3366d0a0c1683ebef137e695.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `fontconfig`. Directory installation integrity and creation provenance are not established.
### alma-512b36ff92a2052e00532af6

Group: `/usr/lib/firewalld`. Source: `D1/in/raw/alma/members/512b36ff92a2052e00532af6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `xmlschema`. Directory installation integrity and creation provenance are not established.
### alma-1e4f414e9f1c5f285104a2f6

Group: `/usr/lib/firmware`. Source: `D1/in/raw/alma/members/1e4f414e9f1c5f285104a2f6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `6.12.0-264.16.1.el10_3.x86_64`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `intel-ucode`. Whether this package member remains as received is unrecorded.
### alma-89a360eef7f9675bad849907

Group: `/usr/lib/firmware/6.12.0-264.16.1.el10_3.x86_64`. Source: `D1/in/raw/alma/members/89a360eef7f9675bad849907.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `intel-ucode`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `readme-intel`, `readme-intel-06-8f-08`. Package origin, unchangedness, and source of this object are not established.
### alma-826dd084c5d972e2cf9f2604

Group: `/usr/lib/firmware/6.12.0-264.16.1.el10_3.x86_64/intel-ucode`. Source: `D1/in/raw/alma/members/826dd084c5d972e2cf9f2604.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `06-03-02`, `06-05-00`, `06-05-01`, `06-05-02`, `06-05-03`, `06-06-00`, `06-06-05`, `06-06-0a`, `06-06-0d`, `06-07-01`, `06-07-02`, `06-07-03`, `06-08-01`, `06-08-03`, `06-08-06`, `06-08-0a`, `06-09-05`, `06-0a-00`, `06-0a-01`, `06-0b-01`, `06-0b-04`, `06-0d-06`, `06-0e-08`, `06-0e-0c`, `06-0f-02`, `06-0f-06`, `06-0f-07`, `06-0f-0a`, `06-0f-0b`, `06-0f-0d`, `06-16-01`, `06-17-06`, `06-17-07`, `06-17-0a`, `06-1a-04`, `06-1a-05`, `06-1c-02`, `06-1c-0a`, `06-1d-01`, `06-1e-05`, `06-25-02`, `06-25-05`, `06-26-01`, `06-2a-07`, `06-2c-02`, `06-2d-06`, `06-2d-07`, `06-2e-06`, `06-2f-02`, `06-37-08`, `06-37-09`, `06-3a-09`, `06-3c-03`, `06-3d-04`, `06-3e-04`, `06-3e-06`, `06-3e-07`, `06-3f-02`, `06-3f-04`, `06-45-01`, `06-46-01`, `06-47-01`, `06-4c-03`, `06-4c-04`, `06-4d-08`, `06-4e-03`, `06-55-03`, `06-55-04`, `06-55-05`, `06-55-06`, `06-55-07`, `06-55-0b`, `06-56-02`, `06-56-03`, `06-56-04`, `06-56-05`, `06-5c-02`, `06-5c-09`, `06-5c-0a`, `06-5e-03`, `06-5f-01`, `06-66-03`, `06-6a-05`, `06-6a-06`, `06-6c-01`, `06-7a-01`, `06-7a-08`, `06-7e-05`, `06-8a-01`, `06-8c-01`, `06-8c-02`, `06-8d-01`, `06-8e-09`, `06-8e-0a`, `06-8e-0b`, `06-8e-0c`, `06-8f-07`, `06-8f-08`, `06-96-01`, `06-97-02`, `06-97-05`, `06-9a-03`, `06-9a-04`, `06-9c-00`, `06-9e-09`, `06-9e-0a`, `06-9e-0b`, `06-9e-0c`, `06-9e-0d`, `06-a5-02`, `06-a5-03`, `06-a5-05`, `06-a6-00`, `06-a6-01`, `06-a7-01`, `06-aa-04`, `06-ad-01`, `06-ae-01`, `06-af-03`, `06-b5-00`, `06-b7-01`, `06-b7-04`, `06-ba-02`, `06-ba-03`, `06-bd-01`, `06-be-00`, `06-bf-02`, `06-bf-05`, `06-c5-02`, `06-c6-02`, `06-cc-02`, `06-cc-03`, `06-cf-01`, `06-cf-02`, `06-d5-01`, `06-d7-00`, `0f-00-07`, `0f-00-0a`, `0f-01-02`, `0f-02-04`, `0f-02-05`, `0f-02-06`, `0f-02-07`, `0f-02-09`, `0f-03-02`, `0f-03-03`, `0f-03-04`, `0f-04-01`, `0f-04-03`, `0f-04-04`, `0f-04-07`, `0f-04-08`, `0f-04-09`, `0f-04-0a`, `0f-06-02`, `0f-06-04`, `0f-06-05`, `0f-06-08`. Package origin, unchangedness, and source of this object are not established.
### alma-22d9524df6813c1275345f42

Group: `/usr/lib/fontconfig/cache`. Source: `D1/in/raw/alma/members/22d9524df6813c1275345f42.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `01d40cee498be4726842ba21cbce24ab-le64.cache-9`, `035f0ebf2f86af269427f030f354ef4b-le64.cache-9`, `123d59b33ddb0e7c76bb24004bd5cfac-le64.cache-9`, `131ab5cc1583381c4f7ce0194912c56d-le64.cache-9`, `221930ae9526a9cb8049af2916f03412-le64.cache-9`, `22f06f3be2d16d058da85b73ae1dc5b1-le64.cache-9`, `2a90ec7ec7fc01d3a9f58fddf8db0237-le64.cache-9`, `3830d5c3ddfd5cd38a049b759396e72e-le64.cache-9`, `39377a11d38956c26ecfe23db50b3cd3-le64.cache-9`, `42536ef14367b24656ac994a93d66238-le64.cache-9`, `427eb62078a821f08aa6ed364f2467bf-le64.cache-9`, `6ee3103884cce7b2fe6f32eba9089175-le64.cache-9`, `7bbebb41f246c24642924bd8585d5345-le64.cache-9`, `7ee6df7a8311986241317a58487e0145-le64.cache-9`, `9d9e7a658cb1f50f02561d1ed3ca8bca-le64.cache-9`, `CACHEDIR.TAG`, `aa02322cc1375fea2382deabf4339973-le64.cache-9`, `b2307de753f1224d9542f27e8b3975ae-le64.cache-9`, `bf4088b6c6290c8d6936483b844e6a40-le64.cache-9`, `c4be257954870c0bf6972134c1de66d5-le64.cache-9`, `cc8b894d3abbdf0310c48629c0737d80-le64.cache-9`, `cf759820c416606818fc74e5e9991313-le64.cache-9`, `d63f98f14a274bd69a5425fc33aaac6b-le64.cache-9`, `efcfae1a52990961975415036867654f-le64.cache-9`. Generated font lookup cache or its directory.
### alma-c4523c0a2eb2e7f8a85e7b8f

Group: `/usr/lib/modules`. Source: `D1/in/raw/alma/members/c4523c0a2eb2e7f8a85e7b8f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `6.12.0-264.16.1.el10_3.x86_64`. Directory installation integrity and creation provenance are not established.
### alma-889f8cd2dae65a248533322a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64`. Source: `D1/in/raw/alma/members/889f8cd2dae65a248533322a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: .vmlinuz.hmac,System.map,config,modules.block,modules.builtin,modules.builtin.modinfo,modules.drm,modules.modesetting,modules.networking,modules.order,symvers.xz,vmlinuz; UNKNOWN: build,kernel,modules.alias,modules.alias.bin,modules.builtin.alias.bin,modules.builtin.bin,modules.dep,modules.dep.bin,modules.devname,modules.softdep,modules.symbols,modules.symbols.bin,source,systemtap,updates,vdso,weak-updates

- **INSTALLED-PACKAGE**: `.vmlinuz.hmac`, `System.map`, `config`, `modules.block`, `modules.builtin`, `modules.builtin.modinfo`, `modules.drm`, `modules.modesetting`, `modules.networking`, `modules.order`, `symvers.xz`, `vmlinuz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `build`, `modules.alias`, `modules.alias.bin`, `modules.builtin.alias.bin`, `modules.builtin.bin`, `modules.dep`, `modules.dep.bin`, `modules.devname`, `modules.softdep`, `modules.symbols`, `modules.symbols.bin`, `source`. Whether this package member remains as received is unrecorded.
- **UNKNOWN**: `kernel`, `systemtap`, `updates`, `vdso`, `weak-updates`. Directory installation integrity and creation provenance are not established.
### alma-d2abea544fcf311a7a430e93

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel`. Source: `D1/in/raw/alma/members/d2abea544fcf311a7a430e93.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `arch`, `crypto`, `drivers`, `fs`, `kernel`, `lib`, `mm`, `net`, `samples`, `sound`, `virt`. Directory installation integrity and creation provenance are not established.
### alma-496b026d0bc38b94528fc075

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch`. Source: `D1/in/raw/alma/members/496b026d0bc38b94528fc075.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `x86`. Directory installation integrity and creation provenance are not established.
### alma-5221ec070989b128f4769447

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86`. Source: `D1/in/raw/alma/members/5221ec070989b128f4769447.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `crypto`, `events`, `kernel`, `kvm`. Directory installation integrity and creation provenance are not established.
### alma-a940bd4318e5aeee1f189864

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/crypto`. Source: `D1/in/raw/alma/members/a940bd4318e5aeee1f189864.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `blowfish-x86_64.ko.xz`, `camellia-aesni-avx-x86_64.ko.xz`, `camellia-aesni-avx2.ko.xz`, `camellia-x86_64.ko.xz`, `cast5-avx-x86_64.ko.xz`, `cast6-avx-x86_64.ko.xz`, `crc32-pclmul.ko.xz`, `crc32c-intel.ko.xz`, `crct10dif-pclmul.ko.xz`, `curve25519-x86_64.ko.xz`, `des3_ede-x86_64.ko.xz`, `ghash-clmulni-intel.ko.xz`, `nhpoly1305-avx2.ko.xz`, `nhpoly1305-sse2.ko.xz`, `serpent-avx-x86_64.ko.xz`, `serpent-avx2.ko.xz`, `serpent-sse2-x86_64.ko.xz`, `twofish-avx-x86_64.ko.xz`, `twofish-x86_64-3way.ko.xz`, `twofish-x86_64.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a1fcd9594d1beeee02bca4c9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/events`. Source: `D1/in/raw/alma/members/a1fcd9594d1beeee02bca4c9.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: rapl.ko.xz; UNKNOWN: amd,intel

- **UNKNOWN**: `amd`, `intel`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `rapl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8555fad1bb88b97dc35816e3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/events/amd`. Source: `D1/in/raw/alma/members/8555fad1bb88b97dc35816e3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `power.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fb0d6ef1186188d9522aa790

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/events/intel`. Source: `D1/in/raw/alma/members/fb0d6ef1186188d9522aa790.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-cstate.ko.xz`, `intel-uncore.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-84b2505f2161463d1055b3b0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/kernel`. Source: `D1/in/raw/alma/members/84b2505f2161463d1055b3b0.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cpu`. Directory installation integrity and creation provenance are not established.
### alma-b5d41568bbc85b4b69fe509d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/kernel/cpu`. Source: `D1/in/raw/alma/members/b5d41568bbc85b4b69fe509d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mce`. Directory installation integrity and creation provenance are not established.
### alma-8eaaa8ce6928c2d10f0532ab

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/kernel/cpu/mce`. Source: `D1/in/raw/alma/members/8eaaa8ce6928c2d10f0532ab.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mce-inject.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-54f642f1df6ce68c4e603d3d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/arch/x86/kvm`. Source: `D1/in/raw/alma/members/54f642f1df6ce68c4e603d3d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `kvm-amd.ko.xz`, `kvm-intel.ko.xz`, `kvm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fdaf111e967686c6e21698b2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/crypto`. Source: `D1/in/raw/alma/members/fdaf111e967686c6e21698b2.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: adiantum.ko.xz,ansi_cprng.ko.xz,blake2b_generic.ko.xz,blowfish_common.ko.xz,blowfish_generic.ko.xz,camellia_generic.ko.xz,cast5_generic.ko.xz,cast6_generic.ko.xz,cast_common.ko.xz,chacha20poly1305.ko.xz,chacha_generic.ko.xz,crc32_generic.ko.xz,curve25519-generic.ko.xz,des_generic.ko.xz,echainiv.ko.xz,essiv.ko.xz,fcrypt.ko.xz,krb5enc.ko.xz,lrw.ko.xz,md4.ko.xz,michael_mic.ko.xz,nhpoly1305.ko.xz,pcbc.ko.xz,pcrypt.ko.xz,poly1305_generic.ko.xz,rmd160.ko.xz,serpent_generic.ko.xz,tcrypt.ko.xz,twofish_common.ko.xz,twofish_generic.ko.xz,vmac.ko.xz,wp512.ko.xz,xcbc.ko.xz,xor.ko.xz,xxhash_generic.ko.xz,zstd.ko.xz; UNKNOWN: asymmetric_keys,async_tx,krb5

- **INSTALLED-PACKAGE**: `adiantum.ko.xz`, `ansi_cprng.ko.xz`, `blake2b_generic.ko.xz`, `blowfish_common.ko.xz`, `blowfish_generic.ko.xz`, `camellia_generic.ko.xz`, `cast5_generic.ko.xz`, `cast6_generic.ko.xz`, `cast_common.ko.xz`, `chacha20poly1305.ko.xz`, `chacha_generic.ko.xz`, `crc32_generic.ko.xz`, `curve25519-generic.ko.xz`, `des_generic.ko.xz`, `echainiv.ko.xz`, `essiv.ko.xz`, `fcrypt.ko.xz`, `krb5enc.ko.xz`, `lrw.ko.xz`, `md4.ko.xz`, `michael_mic.ko.xz`, `nhpoly1305.ko.xz`, `pcbc.ko.xz`, `pcrypt.ko.xz`, `poly1305_generic.ko.xz`, `rmd160.ko.xz`, `serpent_generic.ko.xz`, `tcrypt.ko.xz`, `twofish_common.ko.xz`, `twofish_generic.ko.xz`, `vmac.ko.xz`, `wp512.ko.xz`, `xcbc.ko.xz`, `xor.ko.xz`, `xxhash_generic.ko.xz`, `zstd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `asymmetric_keys`, `async_tx`, `krb5`. Directory installation integrity and creation provenance are not established.
### alma-8e64bb5685f76d6a6db64178

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/crypto/asymmetric_keys`. Source: `D1/in/raw/alma/members/8e64bb5685f76d6a6db64178.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pkcs8_key_parser.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-72ab081debf711282692646b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/crypto/async_tx`. Source: `D1/in/raw/alma/members/72ab081debf711282692646b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `async_memcpy.ko.xz`, `async_pq.ko.xz`, `async_raid6_recov.ko.xz`, `async_tx.ko.xz`, `async_xor.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-235dec110dc082f6e62b51f8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/crypto/krb5`. Source: `D1/in/raw/alma/members/235dec110dc082f6e62b51f8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `krb5.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-37047470fe0b04a0d96e090b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers`. Source: `D1/in/raw/alma/members/37047470fe0b04a0d96e090b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `accel`, `accessibility`, `acpi`, `ata`, `base`, `bcma`, `block`, `bluetooth`, `bus`, `cdrom`, `char`, `clk`, `counter`, `cpufreq`, `crypto`, `cxl`, `dax`, `dca`, `dma`, `dpll`, `edac`, `firmware`, `fwctl`, `gnss`, `gpio`, `gpu`, `hid`, `hv`, `hwmon`, `hwtracing`, `i2c`, `iio`, `infiniband`, `input`, `iommu`, `leds`, `md`, `media`, `memstick`, `message`, `mfd`, `misc`, `mmc`, `mtd`, `net`, `ntb`, `nvdimm`, `nvme`, `parport`, `pci`, `perf`, `pinctrl`, `platform`, `power`, `powercap`, `pps`, `ptp`, `pwm`, `ras`, `regulator`, `rtc`, `scsi`, `soc`, `soundwire`, `spi`, `target`, `tee`, `thermal`, `tty`, `uio`, `usb`, `vdpa`, `vfio`, `vhost`, `video`, `virt`, `virtio`, `watchdog`, `xen`. Directory installation integrity and creation provenance are not established.
### alma-af81cdebc9b48a4f57b37dda

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accel`. Source: `D1/in/raw/alma/members/af81cdebc9b48a4f57b37dda.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `amdxdna`, `ivpu`, `qaic`. Directory installation integrity and creation provenance are not established.
### alma-2f47a0c361ce71cacaa343a0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accel/amdxdna`. Source: `D1/in/raw/alma/members/2f47a0c361ce71cacaa343a0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amdxdna.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5419dfb81acc4af6b84691e4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accel/ivpu`. Source: `D1/in/raw/alma/members/5419dfb81acc4af6b84691e4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_vpu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f34a4b8048d962406af08879

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accel/qaic`. Source: `D1/in/raw/alma/members/f34a4b8048d962406af08879.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qaic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d56ee9aa2e0eb2fb5ecbe612

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accessibility`. Source: `D1/in/raw/alma/members/d56ee9aa2e0eb2fb5ecbe612.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `speakup`. Directory installation integrity and creation provenance are not established.
### alma-72c94d7f7b83a269fc1a4946

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/accessibility/speakup`. Source: `D1/in/raw/alma/members/72c94d7f7b83a269fc1a4946.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `speakup.ko.xz`, `speakup_acntsa.ko.xz`, `speakup_apollo.ko.xz`, `speakup_audptr.ko.xz`, `speakup_bns.ko.xz`, `speakup_dectlk.ko.xz`, `speakup_ltlk.ko.xz`, `speakup_soft.ko.xz`, `speakup_spkout.ko.xz`, `speakup_txprt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-138fb4575b2ded71a51f0ba4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/acpi`. Source: `D1/in/raw/alma/members/138fb4575b2ded71a51f0ba4.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: acpi_extlog.ko.xz,acpi_ipmi.ko.xz,acpi_pad.ko.xz,acpi_tad.ko.xz,pfr_telemetry.ko.xz,pfr_update.ko.xz,platform_profile.ko.xz,sbs.ko.xz,sbshc.ko.xz,video.ko.xz; UNKNOWN: apei,dptf,nfit

- **INSTALLED-PACKAGE**: `acpi_extlog.ko.xz`, `acpi_ipmi.ko.xz`, `acpi_pad.ko.xz`, `acpi_tad.ko.xz`, `pfr_telemetry.ko.xz`, `pfr_update.ko.xz`, `platform_profile.ko.xz`, `sbs.ko.xz`, `sbshc.ko.xz`, `video.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `apei`, `dptf`, `nfit`. Directory installation integrity and creation provenance are not established.
### alma-2aa5926851fdd1f0dd722592

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/acpi/apei`. Source: `D1/in/raw/alma/members/2aa5926851fdd1f0dd722592.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `einj.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-70c6b60f904e872090864eec

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/acpi/dptf`. Source: `D1/in/raw/alma/members/70c6b60f904e872090864eec.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dptf_pch_fivr.ko.xz`, `dptf_power.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aafdbdeb05f4a368becc231a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/acpi/nfit`. Source: `D1/in/raw/alma/members/aafdbdeb05f4a368becc231a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nfit.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ea00e7aeb0b9fc801a69c6e0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ata`. Source: `D1/in/raw/alma/members/ea00e7aeb0b9fc801a69c6e0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ahci.ko.xz`, `ahci_platform.ko.xz`, `ata_generic.ko.xz`, `ata_piix.ko.xz`, `libahci.ko.xz`, `libahci_platform.ko.xz`, `libata.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5499d8aabdf81b08502af30d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/base`. Source: `D1/in/raw/alma/members/5499d8aabdf81b08502af30d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `power`, `regmap`, `test`. Directory installation integrity and creation provenance are not established.
### alma-f2c0904eae069fb2a036844a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/base/regmap`. Source: `D1/in/raw/alma/members/f2c0904eae069fb2a036844a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `regmap-i2c.ko.xz`, `regmap-ram.ko.xz`, `regmap-raw-ram.ko.xz`, `regmap-sdw-mbq.ko.xz`, `regmap-sdw.ko.xz`, `regmap-spi-avmm.ko.xz`, `regmap-spi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-96fd2037e91c81c384818d4d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/bcma`. Source: `D1/in/raw/alma/members/96fd2037e91c81c384818d4d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bcma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ffa55a9bed2bf4c083c860f7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/block`. Source: `D1/in/raw/alma/members/ffa55a9bed2bf4c083c860f7.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: brd.ko.xz,loop.ko.xz,nbd.ko.xz,pktcdvd.ko.xz,rbd.ko.xz,ublk_drv.ko.xz,virtio_blk.ko.xz,xen-blkfront.ko.xz; UNKNOWN: null_blk,zram

- **INSTALLED-PACKAGE**: `brd.ko.xz`, `loop.ko.xz`, `nbd.ko.xz`, `pktcdvd.ko.xz`, `rbd.ko.xz`, `ublk_drv.ko.xz`, `virtio_blk.ko.xz`, `xen-blkfront.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `null_blk`, `zram`. Directory installation integrity and creation provenance are not established.
### alma-0eff2b2437bedf31a7555eac

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/block/null_blk`. Source: `D1/in/raw/alma/members/0eff2b2437bedf31a7555eac.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `null_blk.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e2a9b9f49fdad43e4b700c02

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/block/zram`. Source: `D1/in/raw/alma/members/e2a9b9f49fdad43e4b700c02.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `zram.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-190e62a42e37b6822a704f2d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/bluetooth`. Source: `D1/in/raw/alma/members/190e62a42e37b6822a704f2d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ath3k.ko.xz`, `bcm203x.ko.xz`, `bfusb.ko.xz`, `bpa10x.ko.xz`, `btbcm.ko.xz`, `btintel.ko.xz`, `btintel_pcie.ko.xz`, `btmrvl.ko.xz`, `btmrvl_sdio.ko.xz`, `btmtk.ko.xz`, `btrtl.ko.xz`, `btsdio.ko.xz`, `btusb.ko.xz`, `hci_uart.ko.xz`, `hci_vhci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c28c89523bee566ea0bd0a47

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/bus`. Source: `D1/in/raw/alma/members/c28c89523bee566ea0bd0a47.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mhi`. Directory installation integrity and creation provenance are not established.
### alma-4d8201c220ff6244d7fcd227

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/bus/mhi`. Source: `D1/in/raw/alma/members/4d8201c220ff6244d7fcd227.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `host`. Directory installation integrity and creation provenance are not established.
### alma-6faf0d3914400c9d896d87c0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/bus/mhi/host`. Source: `D1/in/raw/alma/members/6faf0d3914400c9d896d87c0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mhi.ko.xz`, `mhi_pci_generic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1eced33b085cc87e66564e42

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/cdrom`. Source: `D1/in/raw/alma/members/1eced33b085cc87e66564e42.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cdrom.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-15584b6745983d383b7c0de9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/char`. Source: `D1/in/raw/alma/members/15584b6745983d383b7c0de9.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: hangcheck-timer.ko.xz,lp.ko.xz,ppdev.ko.xz,tlclk.ko.xz,uv_mmtimer.ko.xz,virtio_console.ko.xz; UNKNOWN: agp,hw_random,ipmi,tpm

- **UNKNOWN**: `agp`, `hw_random`, `ipmi`, `tpm`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `hangcheck-timer.ko.xz`, `lp.ko.xz`, `ppdev.ko.xz`, `tlclk.ko.xz`, `uv_mmtimer.ko.xz`, `virtio_console.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4cf747ee00ce987dafc9305b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/char/agp`. Source: `D1/in/raw/alma/members/4cf747ee00ce987dafc9305b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-gtt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-df3e8d4c0b7e7be36a348d0e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/char/hw_random`. Source: `D1/in/raw/alma/members/df3e8d4c0b7e7be36a348d0e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd-rng.ko.xz`, `intel-rng.ko.xz`, `timeriomem-rng.ko.xz`, `via-rng.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0af348231e90bdb52cec91ad

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/char/ipmi`. Source: `D1/in/raw/alma/members/0af348231e90bdb52cec91ad.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ipmi_devintf.ko.xz`, `ipmi_msghandler.ko.xz`, `ipmi_poweroff.ko.xz`, `ipmi_si.ko.xz`, `ipmi_ssif.ko.xz`, `ipmi_watchdog.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f2f0d4d4dfdf2829ae7c68d5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/char/tpm`. Source: `D1/in/raw/alma/members/f2f0d4d4dfdf2829ae7c68d5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tpm_i2c_nuvoton.ko.xz`, `tpm_svsm.ko.xz`, `tpm_tis_i2c_cr50.ko.xz`, `tpm_vtpm_proxy.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-92a480cfdacc5bc6c8307f4a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/clk`. Source: `D1/in/raw/alma/members/92a480cfdacc5bc6c8307f4a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `clk-tps68470.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b43a338da2a5120520ee4a61

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/counter`. Source: `D1/in/raw/alma/members/b43a338da2a5120520ee4a61.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `counter.ko.xz`, `intel-qep.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-241b8b6cbc0df97bdab98a08

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/cpufreq`. Source: `D1/in/raw/alma/members/241b8b6cbc0df97bdab98a08.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `acpi-cpufreq.ko.xz`, `amd_freq_sensitivity.ko.xz`, `p4-clockmod.ko.xz`, `powernow-k8.ko.xz`, `speedstep-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-41f900b8e5d1c22eef944dae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto`. Source: `D1/in/raw/alma/members/41f900b8e5d1c22eef944dae.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: padlock-aes.ko.xz,padlock-sha.ko.xz; UNKNOWN: cavium,ccp,chelsio,intel

- **UNKNOWN**: `cavium`, `ccp`, `chelsio`, `intel`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `padlock-aes.ko.xz`, `padlock-sha.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7f7671f049e21db58864c575

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/cavium`. Source: `D1/in/raw/alma/members/7f7671f049e21db58864c575.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `nitrox`. Directory installation integrity and creation provenance are not established.
### alma-e9db9bff159bd5bc3990f90d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/cavium/nitrox`. Source: `D1/in/raw/alma/members/e9db9bff159bd5bc3990f90d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `n5pf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-29060b944e6359e9e6795c6d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/ccp`. Source: `D1/in/raw/alma/members/29060b944e6359e9e6795c6d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ccp-crypto.ko.xz`, `ccp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e08cc5371d1af0e500dc12ac

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/chelsio`. Source: `D1/in/raw/alma/members/e08cc5371d1af0e500dc12ac.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `chcr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0c70b5a7902dedc8e4997b9f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel`. Source: `D1/in/raw/alma/members/0c70b5a7902dedc8e4997b9f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `iaa`, `qat`. Directory installation integrity and creation provenance are not established.
### alma-8058becf7776697a1a52e599

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/iaa`. Source: `D1/in/raw/alma/members/8058becf7776697a1a52e599.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iaa_crypto.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d218d10a9cbf53573e1b5806

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat`. Source: `D1/in/raw/alma/members/d218d10a9cbf53573e1b5806.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `qat_420xx`, `qat_4xxx`, `qat_6xxx`, `qat_c3xxx`, `qat_c3xxxvf`, `qat_c62x`, `qat_c62xvf`, `qat_common`, `qat_dh895xcc`, `qat_dh895xccvf`. Directory installation integrity and creation provenance are not established.
### alma-f33662d6c263c2704feef8dc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_420xx`. Source: `D1/in/raw/alma/members/f33662d6c263c2704feef8dc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_420xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d2c556f8a95ce9826b9911af

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_4xxx`. Source: `D1/in/raw/alma/members/d2c556f8a95ce9826b9911af.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_4xxx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-62ff6b2efc1e67b42c948934

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_6xxx`. Source: `D1/in/raw/alma/members/62ff6b2efc1e67b42c948934.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_6xxx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-275f1a5d8d3321b94cd02f4c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_c3xxx`. Source: `D1/in/raw/alma/members/275f1a5d8d3321b94cd02f4c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_c3xxx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-18ea0d6f8316f3ff90c92bb2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_c3xxxvf`. Source: `D1/in/raw/alma/members/18ea0d6f8316f3ff90c92bb2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_c3xxxvf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-61c46651fb777ba24d2481b8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_c62x`. Source: `D1/in/raw/alma/members/61c46651fb777ba24d2481b8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_c62x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aaf64e0dbd1750321c95abc2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_c62xvf`. Source: `D1/in/raw/alma/members/aaf64e0dbd1750321c95abc2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_c62xvf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-18353a34dd02947e5673c648

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_common`. Source: `D1/in/raw/alma/members/18353a34dd02947e5673c648.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_qat.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-851b6c626bc75d940e4e1706

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_dh895xcc`. Source: `D1/in/raw/alma/members/851b6c626bc75d940e4e1706.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_dh895xcc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-da84d27363b044da677d50c5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/crypto/intel/qat/qat_dh895xccvf`. Source: `D1/in/raw/alma/members/da84d27363b044da677d50c5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qat_dh895xccvf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-badc0d345e6ea1dc122d25e1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/cxl`. Source: `D1/in/raw/alma/members/badc0d345e6ea1dc122d25e1.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cxl_acpi.ko.xz,cxl_mem.ko.xz,cxl_pci.ko.xz,cxl_pmem.ko.xz,cxl_port.ko.xz; UNKNOWN: core

- **UNKNOWN**: `core`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `cxl_acpi.ko.xz`, `cxl_mem.ko.xz`, `cxl_pci.ko.xz`, `cxl_pmem.ko.xz`, `cxl_port.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b1488d63c0345d2836f313be

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/cxl/core`. Source: `D1/in/raw/alma/members/b1488d63c0345d2836f313be.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxl_core.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-deadbd4ba75e44c545d843e4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dax`. Source: `D1/in/raw/alma/members/deadbd4ba75e44c545d843e4.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: dax_cxl.ko.xz,dax_pmem.ko.xz,device_dax.ko.xz,kmem.ko.xz; UNKNOWN: hmem

- **INSTALLED-PACKAGE**: `dax_cxl.ko.xz`, `dax_pmem.ko.xz`, `device_dax.ko.xz`, `kmem.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `hmem`. Directory installation integrity and creation provenance are not established.
### alma-b3f4f021589d40bdbe0ff6a5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dax/hmem`. Source: `D1/in/raw/alma/members/b3f4f021589d40bdbe0ff6a5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dax_hmem.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7fdb4cc3d44402d84bc1d8cd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dca`. Source: `D1/in/raw/alma/members/7fdb4cc3d44402d84bc1d8cd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dca.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1be48c457bc7147a465bd91f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma`. Source: `D1/in/raw/alma/members/1be48c457bc7147a465bd91f.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: idma64.ko.xz; UNKNOWN: amd,dw,idxd,ioat

- **UNKNOWN**: `amd`, `dw`, `idxd`, `ioat`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `idma64.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-22686c6a598f8fa469a05a43

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/amd`. Source: `D1/in/raw/alma/members/22686c6a598f8fa469a05a43.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ae4dma`, `ptdma`. Directory installation integrity and creation provenance are not established.
### alma-fb55a7a298434ad39091823a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/amd/ae4dma`. Source: `D1/in/raw/alma/members/fb55a7a298434ad39091823a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ae4dma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d173d2a771144434559752e7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/amd/ptdma`. Source: `D1/in/raw/alma/members/d173d2a771144434559752e7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ptdma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1e56ceba140ad42032f71413

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/dw`. Source: `D1/in/raw/alma/members/1e56ceba140ad42032f71413.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dw_dmac.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-de2875409dcea6d66611c4b3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/idxd`. Source: `D1/in/raw/alma/members/de2875409dcea6d66611c4b3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `idxd.ko.xz`, `idxd_bus.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ace9f5efd57d1a0e2be69206

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dma/ioat`. Source: `D1/in/raw/alma/members/ace9f5efd57d1a0e2be69206.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ioatdma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7e20f018882020bade15adb6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dpll`. Source: `D1/in/raw/alma/members/7e20f018882020bade15adb6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `zl3073x`. Directory installation integrity and creation provenance are not established.
### alma-41d6f3a85bebb239be0f7b0c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/dpll/zl3073x`. Source: `D1/in/raw/alma/members/41d6f3a85bebb239be0f7b0c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `zl3073x.ko.xz`, `zl3073x_i2c.ko.xz`, `zl3073x_spi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b5e8236dce2348fb5bc4a122

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/edac`. Source: `D1/in/raw/alma/members/b5e8236dce2348fb5bc4a122.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd64_edac.ko.xz`, `e752x_edac.ko.xz`, `edac_mce_amd.ko.xz`, `i10nm_edac.ko.xz`, `i3000_edac.ko.xz`, `i3200_edac.ko.xz`, `i5100_edac.ko.xz`, `i5400_edac.ko.xz`, `i7300_edac.ko.xz`, `i7core_edac.ko.xz`, `i82975x_edac.ko.xz`, `ie31200_edac.ko.xz`, `igen6_edac.ko.xz`, `pnd2_edac.ko.xz`, `sb_edac.ko.xz`, `skx_edac.ko.xz`, `skx_edac_common.ko.xz`, `x38_edac.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6108f902077bf0e302bfb338

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/firmware`. Source: `D1/in/raw/alma/members/6108f902077bf0e302bfb338.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: edd.ko.xz,iscsi_ibft.ko.xz; UNKNOWN: cirrus

- **UNKNOWN**: `cirrus`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `edd.ko.xz`, `iscsi_ibft.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c8bc0a057830ca19b7a07bea

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/firmware/cirrus`. Source: `D1/in/raw/alma/members/c8bc0a057830ca19b7a07bea.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cs_dsp.ko.xz; UNKNOWN: test

- **INSTALLED-PACKAGE**: `cs_dsp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `test`. Directory installation integrity and creation provenance are not established.
### alma-7888e5054324886613fd41bc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/fwctl`. Source: `D1/in/raw/alma/members/7888e5054324886613fd41bc.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: fwctl.ko.xz; UNKNOWN: mlx5

- **INSTALLED-PACKAGE**: `fwctl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `mlx5`. Directory installation integrity and creation provenance are not established.
### alma-cf04fc8c9ccdc124230a0efe

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/fwctl/mlx5`. Source: `D1/in/raw/alma/members/cf04fc8c9ccdc124230a0efe.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx5_fwctl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-39e4f4e93571f1c892c1b37a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gnss`. Source: `D1/in/raw/alma/members/39e4f4e93571f1c892c1b37a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gnss.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c5a4da8d890705a160e0c1e6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpio`. Source: `D1/in/raw/alma/members/c5a4da8d890705a160e0c1e6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gpio-amdpt.ko.xz`, `gpio-generic.ko.xz`, `gpio-ich.ko.xz`, `gpio-ljca.ko.xz`, `gpio-novalake-events.ko.xz`, `gpio-sim.ko.xz`, `gpio-tps68470.ko.xz`, `gpio-usbio.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8aee62d28064f03dab6f82dd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu`. Source: `D1/in/raw/alma/members/8aee62d28064f03dab6f82dd.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `drm`. Directory installation integrity and creation provenance are not established.
### alma-97f6b1a6aa8dd807fd717908

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm`. Source: `D1/in/raw/alma/members/97f6b1a6aa8dd807fd717908.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: drm_buddy.ko.xz,drm_exec.ko.xz,drm_gpusvm_helper.ko.xz,drm_gpuvm.ko.xz,drm_panel_backlight_quirks.ko.xz,drm_suballoc_helper.ko.xz,drm_ttm_helper.ko.xz; UNKNOWN: amd,ast,display,gma500,gud,hyperv,i915,mgag200,nouveau,qxl,radeon,scheduler,tests,tiny,ttm,udl,virtio,vkms,vmwgfx,xe

- **UNKNOWN**: `amd`, `ast`, `display`, `gma500`, `gud`, `hyperv`, `i915`, `mgag200`, `nouveau`, `qxl`, `radeon`, `scheduler`, `tests`, `tiny`, `ttm`, `udl`, `virtio`, `vkms`, `vmwgfx`, `xe`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `drm_buddy.ko.xz`, `drm_exec.ko.xz`, `drm_gpusvm_helper.ko.xz`, `drm_gpuvm.ko.xz`, `drm_panel_backlight_quirks.ko.xz`, `drm_suballoc_helper.ko.xz`, `drm_ttm_helper.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d0cf21cbc4780c392a7f68c9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/amd`. Source: `D1/in/raw/alma/members/d0cf21cbc4780c392a7f68c9.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `amdgpu`, `amdxcp`. Directory installation integrity and creation provenance are not established.
### alma-018965f1993859f3140b337a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/amd/amdgpu`. Source: `D1/in/raw/alma/members/018965f1993859f3140b337a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amdgpu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2bbc712ea920b6caff1d6968

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/amd/amdxcp`. Source: `D1/in/raw/alma/members/2bbc712ea920b6caff1d6968.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amdxcp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cdd2e324739a05950eb10db4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/ast`. Source: `D1/in/raw/alma/members/cdd2e324739a05950eb10db4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ast.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4639830854594b1401e6cad3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/display`. Source: `D1/in/raw/alma/members/4639830854594b1401e6cad3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `drm_display_helper.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a30136b13fbc2b58e28381c1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/gma500`. Source: `D1/in/raw/alma/members/a30136b13fbc2b58e28381c1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gma500_gfx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9d4e73757cdada5af1c12c95

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/gud`. Source: `D1/in/raw/alma/members/9d4e73757cdada5af1c12c95.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gud.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9359b40b52b536442744f02f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/hyperv`. Source: `D1/in/raw/alma/members/9359b40b52b536442744f02f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hyperv_drm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e52df590e81b8c5bba46cba1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/i915`. Source: `D1/in/raw/alma/members/e52df590e81b8c5bba46cba1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i915.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c5fcb42297b7464aad9d2f19

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/mgag200`. Source: `D1/in/raw/alma/members/c5fcb42297b7464aad9d2f19.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mgag200.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b4d26c462df6e7364c54f249

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/nouveau`. Source: `D1/in/raw/alma/members/b4d26c462df6e7364c54f249.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ch7006.ko.xz`, `nouveau.ko.xz`, `sil164.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bd4332dadc6a882bcd87d5c2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/qxl`. Source: `D1/in/raw/alma/members/bd4332dadc6a882bcd87d5c2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qxl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c000b4784ae9c5e5c917a6ec

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/radeon`. Source: `D1/in/raw/alma/members/c000b4784ae9c5e5c917a6ec.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `radeon.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f26caad3ce1e91bfa2d45f0b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/scheduler`. Source: `D1/in/raw/alma/members/f26caad3ce1e91bfa2d45f0b.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: gpu-sched.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `gpu-sched.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-33b59f883d047932be978fc4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/tiny`. Source: `D1/in/raw/alma/members/33b59f883d047932be978fc4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bochs.ko.xz`, `cirrus-qemu.ko.xz`, `gm12u320.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fbbce926ea659555387c87ee

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/ttm`. Source: `D1/in/raw/alma/members/fbbce926ea659555387c87ee.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ttm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3e10e8f682067bf5e065985a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/udl`. Source: `D1/in/raw/alma/members/3e10e8f682067bf5e065985a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `udl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-63e5c987ac2adbe7a97a7b03

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/virtio`. Source: `D1/in/raw/alma/members/63e5c987ac2adbe7a97a7b03.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `virtio-gpu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d82d7b4a70563d1a562c7f5a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/vkms`. Source: `D1/in/raw/alma/members/d82d7b4a70563d1a562c7f5a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: vkms.ko.xz; UNKNOWN: tests

- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `vkms.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1400446bdafcf1c31c9be2c1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/vmwgfx`. Source: `D1/in/raw/alma/members/1400446bdafcf1c31c9be2c1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vmwgfx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a4886bd5eebd29ddf01828b7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/gpu/drm/xe`. Source: `D1/in/raw/alma/members/a4886bd5eebd29ddf01828b7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xe.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9c8c31ca6d00a541e51c8665

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hid`. Source: `D1/in/raw/alma/members/9c8c31ca6d00a541e51c8665.tsv`. Decision: **MIXED**.

Member decisions differ: INSTALLED-PACKAGE, UNKNOWN. Exact member split: part-alma.1.notes.md, alma-9c8c31ca6d00a541e51c8665.

- **UNKNOWN**: `amd-sfh-hid`, `i2c-hid`, `intel-ish-hid`, `intel-thc-hid`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `hid-a4tech.ko.xz`, `hid-alps.ko.xz`, `hid-apple.ko.xz`, `hid-appleir.ko.xz`, `hid-asus.ko.xz`, `hid-aureal.ko.xz`, `hid-axff.ko.xz`, `hid-belkin.ko.xz`, `hid-betopff.ko.xz`, `hid-cherry.ko.xz`, `hid-chicony.ko.xz`, `hid-cmedia.ko.xz`, `hid-corsair-void.ko.xz`, `hid-corsair.ko.xz`, `hid-cougar.ko.xz`, `hid-cypress.ko.xz`, `hid-dr.ko.xz`, `hid-elan.ko.xz`, `hid-elecom.ko.xz`, `hid-elo.ko.xz`, `hid-evision.ko.xz`, `hid-ezkey.ko.xz`, `hid-gaff.ko.xz`, `hid-gembird.ko.xz`, `hid-gfrm.ko.xz`, `hid-gt683r.ko.xz`, `hid-gyration.ko.xz`, `hid-holtek-kbd.ko.xz`, `hid-holtek-mouse.ko.xz`, `hid-holtekff.ko.xz`, `hid-hyperv.ko.xz`, `hid-icade.ko.xz`, `hid-ite.ko.xz`, `hid-jabra.ko.xz`, `hid-kensington.ko.xz`, `hid-keytouch.ko.xz`, `hid-kye.ko.xz`, `hid-lcpower.ko.xz`, `hid-led.ko.xz`, `hid-lenovo.ko.xz`, `hid-letsketch.ko.xz`, `hid-lg-g15.ko.xz`, `hid-logitech-dj.ko.xz`, `hid-logitech-hidpp.ko.xz`, `hid-logitech.ko.xz`, `hid-microsoft.ko.xz`, `hid-monterey.ko.xz`, `hid-multitouch.ko.xz`, `hid-nti.ko.xz`, `hid-ortek.ko.xz`, `hid-penmount.ko.xz`, `hid-petalynx.ko.xz`, `hid-picolcd.ko.xz`, `hid-pl.ko.xz`, `hid-plantronics.ko.xz`, `hid-primax.ko.xz`, `hid-prodikeys.ko.xz`, `hid-rmi.ko.xz`, `hid-roccat-arvo.ko.xz`, `hid-roccat-common.ko.xz`, `hid-roccat-isku.ko.xz`, `hid-roccat-kone.ko.xz`, `hid-roccat-koneplus.ko.xz`, `hid-roccat-konepure.ko.xz`, `hid-roccat-kovaplus.ko.xz`, `hid-roccat-lua.ko.xz`, `hid-roccat-pyra.ko.xz`, `hid-roccat-ryos.ko.xz`, `hid-roccat-savu.ko.xz`, `hid-roccat.ko.xz`, `hid-saitek.ko.xz`, `hid-samsung.ko.xz`, `hid-semitek.ko.xz`, `hid-sensor-custom.ko.xz`, `hid-sigmamicro.ko.xz`, `hid-sjoy.ko.xz`, `hid-sony.ko.xz`, `hid-speedlink.ko.xz`, `hid-steelseries.ko.xz`, `hid-sunplus.ko.xz`, `hid-thrustmaster.ko.xz`, `hid-tivo.ko.xz`, `hid-tmff.ko.xz`, `hid-topseed.ko.xz`, `hid-twinhan.ko.xz`, `hid-uclogic.ko.xz`, `hid-waltop.ko.xz`, `hid-wiimote.ko.xz`, `hid-xiaomi.ko.xz`, `hid-xinmo.ko.xz`, `hid-zpff.ko.xz`, `hid-zydacron.ko.xz`, `uhid.ko.xz`, `wacom.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e6af8c8cec7a9e0f3eb12b6c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hid/amd-sfh-hid`. Source: `D1/in/raw/alma/members/e6af8c8cec7a9e0f3eb12b6c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd_sfh.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9606dbc75ae1696b664e6d65

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hid/i2c-hid`. Source: `D1/in/raw/alma/members/9606dbc75ae1696b664e6d65.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i2c-hid-acpi.ko.xz`, `i2c-hid.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5afd9b871201aaadad129578

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hid/intel-ish-hid`. Source: `D1/in/raw/alma/members/5afd9b871201aaadad129578.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-ish-ipc.ko.xz`, `intel-ishtp-hid.ko.xz`, `intel-ishtp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-30e86b7eb005fb7e1a881819

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hid/intel-thc-hid`. Source: `D1/in/raw/alma/members/30e86b7eb005fb7e1a881819.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-quicki2c.ko.xz`, `intel-quickspi.ko.xz`, `intel-thc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-27b56abb46b26f6078c6aad7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hv`. Source: `D1/in/raw/alma/members/27b56abb46b26f6078c6aad7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hv_balloon.ko.xz`, `hv_utils.ko.xz`, `hv_vmbus.ko.xz`, `mshv_root.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ca13f5a2ee35501f33f30ae3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hwmon`. Source: `D1/in/raw/alma/members/ca13f5a2ee35501f33f30ae3.tsv`. Decision: **MIXED**.

Member decisions differ: INSTALLED-PACKAGE, UNKNOWN. Exact member split: part-alma.1.notes.md, alma-ca13f5a2ee35501f33f30ae3.

- **INSTALLED-PACKAGE**: `abituguru.ko.xz`, `abituguru3.ko.xz`, `acpi_power_meter.ko.xz`, `ad7414.ko.xz`, `ad7418.ko.xz`, `adm1025.ko.xz`, `adm1026.ko.xz`, `adm1029.ko.xz`, `adm1031.ko.xz`, `adm9240.ko.xz`, `ads7828.ko.xz`, `adt7410.ko.xz`, `adt7411.ko.xz`, `adt7462.ko.xz`, `adt7470.ko.xz`, `adt7475.ko.xz`, `adt7x10.ko.xz`, `amc6821.ko.xz`, `applesmc.ko.xz`, `asb100.ko.xz`, `asc7621.ko.xz`, `asus_atk0110.ko.xz`, `atxp1.ko.xz`, `coretemp.ko.xz`, `dell-smm-hwmon.ko.xz`, `dme1737.ko.xz`, `ds1621.ko.xz`, `ds620.ko.xz`, `emc1403.ko.xz`, `emc6w201.ko.xz`, `f71805f.ko.xz`, `f71882fg.ko.xz`, `f75375s.ko.xz`, `fam15h_power.ko.xz`, `fschmd.ko.xz`, `g760a.ko.xz`, `gl518sm.ko.xz`, `gl520sm.ko.xz`, `hwmon-vid.ko.xz`, `i5500_temp.ko.xz`, `i5k_amb.ko.xz`, `ibmaem.ko.xz`, `ibmpex.ko.xz`, `ina209.ko.xz`, `ina2xx.ko.xz`, `intel-m10-bmc-hwmon.ko.xz`, `it87.ko.xz`, `jc42.ko.xz`, `k10temp.ko.xz`, `k8temp.ko.xz`, `lineage-pem.ko.xz`, `lm63.ko.xz`, `lm73.ko.xz`, `lm75.ko.xz`, `lm77.ko.xz`, `lm78.ko.xz`, `lm80.ko.xz`, `lm83.ko.xz`, `lm85.ko.xz`, `lm87.ko.xz`, `lm90.ko.xz`, `lm92.ko.xz`, `lm93.ko.xz`, `lm95234.ko.xz`, `lm95241.ko.xz`, `lm95245.ko.xz`, `ltc4151.ko.xz`, `ltc4215.ko.xz`, `ltc4245.ko.xz`, `ltc4261.ko.xz`, `max16065.ko.xz`, `max1619.ko.xz`, `max1668.ko.xz`, `max197.ko.xz`, `max6639.ko.xz`, `max6650.ko.xz`, `max6697.ko.xz`, `mcp3021.ko.xz`, `nct6775-core.ko.xz`, `nct6775.ko.xz`, `ntc_thermistor.ko.xz`, `pc87360.ko.xz`, `pc87427.ko.xz`, `pcf8591.ko.xz`, `sch5627.ko.xz`, `sch5636.ko.xz`, `sch56xx-common.ko.xz`, `sht15.ko.xz`, `sht21.ko.xz`, `sis5595.ko.xz`, `smsc47b397.ko.xz`, `smsc47m1.ko.xz`, `smsc47m192.ko.xz`, `thmc50.ko.xz`, `tmp102.ko.xz`, `tmp401.ko.xz`, `tmp421.ko.xz`, `via-cputemp.ko.xz`, `via686a.ko.xz`, `vt1211.ko.xz`, `vt8231.ko.xz`, `w83627ehf.ko.xz`, `w83627hf.ko.xz`, `w83781d.ko.xz`, `w83791d.ko.xz`, `w83792d.ko.xz`, `w83793.ko.xz`, `w83795.ko.xz`, `w83l785ts.ko.xz`, `w83l786ng.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `pmbus`. Directory installation integrity and creation provenance are not established.
### alma-4e02ca639a2b8e1bddff1c79

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hwmon/pmbus`. Source: `D1/in/raw/alma/members/4e02ca639a2b8e1bddff1c79.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `adm1275.ko.xz`, `lm25066.ko.xz`, `ltc2978.ko.xz`, `max16064.ko.xz`, `max34440.ko.xz`, `max8688.ko.xz`, `pmbus.ko.xz`, `pmbus_core.ko.xz`, `ucd9000.ko.xz`, `ucd9200.ko.xz`, `zl6100.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2581118e9d9f25f901224ea4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hwtracing`. Source: `D1/in/raw/alma/members/2581118e9d9f25f901224ea4.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `intel_th`, `stm`. Directory installation integrity and creation provenance are not established.
### alma-2d24707ac36a20e1a145603e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hwtracing/intel_th`. Source: `D1/in/raw/alma/members/2d24707ac36a20e1a145603e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_th.ko.xz`, `intel_th_acpi.ko.xz`, `intel_th_gth.ko.xz`, `intel_th_msu.ko.xz`, `intel_th_msu_sink.ko.xz`, `intel_th_pci.ko.xz`, `intel_th_pti.ko.xz`, `intel_th_sth.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-07be943778320f077ae5ab68

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/hwtracing/stm`. Source: `D1/in/raw/alma/members/07be943778320f077ae5ab68.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dummy_stm.ko.xz`, `stm_console.ko.xz`, `stm_core.ko.xz`, `stm_ftrace.ko.xz`, `stm_heartbeat.ko.xz`, `stm_p_basic.ko.xz`, `stm_p_sys-t.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cbf8396b7aaa8b1779df8dd8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/i2c`. Source: `D1/in/raw/alma/members/cbf8396b7aaa8b1779df8dd8.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: i2c-dev.ko.xz,i2c-mux.ko.xz,i2c-smbus.ko.xz,i2c-stub.ko.xz; UNKNOWN: algos,busses,muxes

- **UNKNOWN**: `algos`, `busses`, `muxes`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `i2c-dev.ko.xz`, `i2c-mux.ko.xz`, `i2c-smbus.ko.xz`, `i2c-stub.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0c82bab032c87f7e35ebfda8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/i2c/algos`. Source: `D1/in/raw/alma/members/0c82bab032c87f7e35ebfda8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i2c-algo-bit.ko.xz`, `i2c-algo-pca.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0e1e3434316d44f9fae19d3e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/i2c/busses`. Source: `D1/in/raw/alma/members/0e1e3434316d44f9fae19d3e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i2c-amd756-s4882.ko.xz`, `i2c-amd756.ko.xz`, `i2c-amd8111.ko.xz`, `i2c-designware-amdisp.ko.xz`, `i2c-designware-core.ko.xz`, `i2c-designware-platform.ko.xz`, `i2c-diolan-u2c.ko.xz`, `i2c-i801.ko.xz`, `i2c-isch.ko.xz`, `i2c-ismt.ko.xz`, `i2c-ljca.ko.xz`, `i2c-mlxcpld.ko.xz`, `i2c-nforce2-s4985.ko.xz`, `i2c-nforce2.ko.xz`, `i2c-parport.ko.xz`, `i2c-pca-platform.ko.xz`, `i2c-piix4.ko.xz`, `i2c-scmi.ko.xz`, `i2c-simtec.ko.xz`, `i2c-sis96x.ko.xz`, `i2c-tiny-usb.ko.xz`, `i2c-usbio.ko.xz`, `i2c-via.ko.xz`, `i2c-viapro.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f01eb446ae0869758793832b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/i2c/muxes`. Source: `D1/in/raw/alma/members/f01eb446ae0869758793832b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i2c-mux-mlxcpld.ko.xz`, `i2c-mux-pca954x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bfd50aea45a881c857ac9da8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio`. Source: `D1/in/raw/alma/members/bfd50aea45a881c857ac9da8.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: industrialio-gts-helper.ko.xz,industrialio.ko.xz; UNKNOWN: accel,buffer,common,gyro,humidity,light,magnetometer,orientation,pressure,temperature,test

- **UNKNOWN**: `accel`, `buffer`, `common`, `gyro`, `humidity`, `light`, `magnetometer`, `orientation`, `pressure`, `temperature`, `test`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `industrialio-gts-helper.ko.xz`, `industrialio.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b9885ec4f80af1e98579f24e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/accel`. Source: `D1/in/raw/alma/members/b9885ec4f80af1e98579f24e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-accel-3d.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-940f1f4be5891632ec1a41f1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/buffer`. Source: `D1/in/raw/alma/members/940f1f4be5891632ec1a41f1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `industrialio-triggered-buffer.ko.xz`, `kfifo_buf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fe9ae7a27ee7777d61afe283

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/common`. Source: `D1/in/raw/alma/members/fe9ae7a27ee7777d61afe283.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `hid-sensors`. Directory installation integrity and creation provenance are not established.
### alma-71e75dfea3c1b462286d9f7f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/common/hid-sensors`. Source: `D1/in/raw/alma/members/71e75dfea3c1b462286d9f7f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-iio-common.ko.xz`, `hid-sensor-trigger.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8be1078dae17a6aac0980f33

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/gyro`. Source: `D1/in/raw/alma/members/8be1078dae17a6aac0980f33.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-gyro-3d.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-016f13c2241e73d55e81fcb6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/humidity`. Source: `D1/in/raw/alma/members/016f13c2241e73d55e81fcb6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-humidity.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0700e40ec8dd7d7d267dd0de

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/light`. Source: `D1/in/raw/alma/members/0700e40ec8dd7d7d267dd0de.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-als.ko.xz`, `hid-sensor-prox.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-067e98711137608271650483

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/magnetometer`. Source: `D1/in/raw/alma/members/067e98711137608271650483.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-magn-3d.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-14e8523f696dece93c71875e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/orientation`. Source: `D1/in/raw/alma/members/14e8523f696dece93c71875e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-incl-3d.ko.xz`, `hid-sensor-rotation.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1a6da98d1752ed049e0533db

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/pressure`. Source: `D1/in/raw/alma/members/1a6da98d1752ed049e0533db.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-press.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-06ae721e33c49429fef097b4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iio/temperature`. Source: `D1/in/raw/alma/members/06ae721e33c49429fef097b4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hid-sensor-temperature.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-212a4acf5efc6a09765de9c4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband`. Source: `D1/in/raw/alma/members/212a4acf5efc6a09765de9c4.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `core`, `hw`, `sw`, `ulp`. Directory installation integrity and creation provenance are not established.
### alma-229038602dd112f600c44e66

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/core`. Source: `D1/in/raw/alma/members/229038602dd112f600c44e66.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_cm.ko.xz`, `ib_core.ko.xz`, `ib_umad.ko.xz`, `ib_uverbs.ko.xz`, `iw_cm.ko.xz`, `rdma_cm.ko.xz`, `rdma_ucm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-74ed6343c03d7ad1860bf9a0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw`. Source: `D1/in/raw/alma/members/74ed6343c03d7ad1860bf9a0.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `bnxt_re`, `cxgb4`, `efa`, `hfi1`, `irdma`, `mana`, `mlx4`, `mlx5`, `qedr`, `vmw_pvrdma`. Directory installation integrity and creation provenance are not established.
### alma-c12b1ad2fb857650c79d15ec

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/bnxt_re`. Source: `D1/in/raw/alma/members/c12b1ad2fb857650c79d15ec.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnxt_re.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8d18b47f1144023cdb9aa0d2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/cxgb4`. Source: `D1/in/raw/alma/members/8d18b47f1144023cdb9aa0d2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iw_cxgb4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2460bb20b5b68447d0e285c8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/efa`. Source: `D1/in/raw/alma/members/2460bb20b5b68447d0e285c8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `efa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e002f46ecf7f356a27be2d1a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/hfi1`. Source: `D1/in/raw/alma/members/e002f46ecf7f356a27be2d1a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hfi1.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-42aa6a304721231a5acf2dae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/irdma`. Source: `D1/in/raw/alma/members/42aa6a304721231a5acf2dae.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `irdma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b0e5cdecc5f503d9905ccc5c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/mana`. Source: `D1/in/raw/alma/members/b0e5cdecc5f503d9905ccc5c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mana_ib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-966ec7fe03986698fd431291

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/mlx4`. Source: `D1/in/raw/alma/members/966ec7fe03986698fd431291.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx4_ib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fe823d8763a4ba37ca88811e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/mlx5`. Source: `D1/in/raw/alma/members/fe823d8763a4ba37ca88811e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx5_ib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f74ad4025ed685e6828ec49a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/qedr`. Source: `D1/in/raw/alma/members/f74ad4025ed685e6828ec49a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qedr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-190a24611c086008ac7046cc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/hw/vmw_pvrdma`. Source: `D1/in/raw/alma/members/190a24611c086008ac7046cc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vmw_pvrdma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fef573da6e70bd435913465f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/sw`. Source: `D1/in/raw/alma/members/fef573da6e70bd435913465f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `rdmavt`. Directory installation integrity and creation provenance are not established.
### alma-9e7f62f6282a7918823dfb92

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/sw/rdmavt`. Source: `D1/in/raw/alma/members/9e7f62f6282a7918823dfb92.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rdmavt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6d9369d3c07f59df59ed3808

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp`. Source: `D1/in/raw/alma/members/6d9369d3c07f59df59ed3808.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ipoib`, `iser`, `isert`, `opa_vnic`, `srp`, `srpt`. Directory installation integrity and creation provenance are not established.
### alma-a18c30849227077fee42ec56

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/ipoib`. Source: `D1/in/raw/alma/members/a18c30849227077fee42ec56.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_ipoib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-eef0b24779bba0e41e15c1de

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/iser`. Source: `D1/in/raw/alma/members/eef0b24779bba0e41e15c1de.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_iser.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5d70b416b971eb1b5597f8a4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/isert`. Source: `D1/in/raw/alma/members/5d70b416b971eb1b5597f8a4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_isert.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0e2259d860842724e9535480

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/opa_vnic`. Source: `D1/in/raw/alma/members/0e2259d860842724e9535480.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `opa_vnic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b700e870f35c8b582f532984

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/srp`. Source: `D1/in/raw/alma/members/b700e870f35c8b582f532984.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_srp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0522e95de5cfd07669bcde1d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/infiniband/ulp/srpt`. Source: `D1/in/raw/alma/members/0522e95de5cfd07669bcde1d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ib_srpt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-faff5109fe405e0fdc362237

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input`. Source: `D1/in/raw/alma/members/faff5109fe405e0fdc362237.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ff-memless.ko.xz,joydev.ko.xz,sparse-keymap.ko.xz; UNKNOWN: keyboard,misc,mouse,rmi4,serio,tablet,tests,touchscreen

- **INSTALLED-PACKAGE**: `ff-memless.ko.xz`, `joydev.ko.xz`, `sparse-keymap.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `keyboard`, `misc`, `mouse`, `rmi4`, `serio`, `tablet`, `tests`, `touchscreen`. Directory installation integrity and creation provenance are not established.
### alma-fcf37072e896abc8180fba44

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/keyboard`. Source: `D1/in/raw/alma/members/fcf37072e896abc8180fba44.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gpio_keys.ko.xz`, `gpio_keys_polled.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-471b5be015173cd1cb9865dc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/misc`. Source: `D1/in/raw/alma/members/471b5be015173cd1cb9865dc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `apanel.ko.xz`, `ati_remote2.ko.xz`, `atlas_btns.ko.xz`, `cm109.ko.xz`, `keyspan_remote.ko.xz`, `pcspkr.ko.xz`, `powermate.ko.xz`, `rotary_encoder.ko.xz`, `soc_button_array.ko.xz`, `uinput.ko.xz`, `xen-kbdfront.ko.xz`, `yealink.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3a4f986753188fe5920b3cb9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/mouse`. Source: `D1/in/raw/alma/members/3a4f986753188fe5920b3cb9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `appletouch.ko.xz`, `bcm5974.ko.xz`, `cyapatp.ko.xz`, `elan_i2c.ko.xz`, `sermouse.ko.xz`, `synaptics_i2c.ko.xz`, `synaptics_usb.ko.xz`, `vsxxxaa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dd246c2b7ac50053a3fcdb9e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/rmi4`. Source: `D1/in/raw/alma/members/dd246c2b7ac50053a3fcdb9e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rmi_core.ko.xz`, `rmi_i2c.ko.xz`, `rmi_smbus.ko.xz`, `rmi_spi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-89cf16d89d2a4409687e6934

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/serio`. Source: `D1/in/raw/alma/members/89cf16d89d2a4409687e6934.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `altera_ps2.ko.xz`, `arc_ps2.ko.xz`, `hyperv-keyboard.ko.xz`, `serio_raw.ko.xz`, `serport.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0b3ad609abd407927d8d190a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/tablet`. Source: `D1/in/raw/alma/members/0b3ad609abd407927d8d190a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `acecad.ko.xz`, `aiptek.ko.xz`, `kbtab.ko.xz`, `wacom_serial4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dd4ba04bd66720099069d654

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/input/touchscreen`. Source: `D1/in/raw/alma/members/dd4ba04bd66720099069d654.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `elo.ko.xz`, `wacom_i2c.ko.xz`, `wacom_w8001.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-29e2b762c1f687d93552ca98

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iommu`. Source: `D1/in/raw/alma/members/29e2b762c1f687d93552ca98.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `iommufd`. Directory installation integrity and creation provenance are not established.
### alma-2d5ae6c53ca775f8974f07d0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/iommu/iommufd`. Source: `D1/in/raw/alma/members/2d5ae6c53ca775f8974f07d0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iommufd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f84ecff98bf0f4cc2f04a3f9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/leds`. Source: `D1/in/raw/alma/members/f84ecff98bf0f4cc2f04a3f9.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: led-class-multicolor.ko.xz,leds-blinkm.ko.xz,leds-lm3530.ko.xz,leds-lp3944.ko.xz,leds-lt3593.ko.xz,leds-mlxcpld.ko.xz,leds-ss4200.ko.xz; UNKNOWN: trigger

- **INSTALLED-PACKAGE**: `led-class-multicolor.ko.xz`, `leds-blinkm.ko.xz`, `leds-lm3530.ko.xz`, `leds-lp3944.ko.xz`, `leds-lt3593.ko.xz`, `leds-mlxcpld.ko.xz`, `leds-ss4200.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `trigger`. Directory installation integrity and creation provenance are not established.
### alma-4c1fd9c82acc1b7190ef5f7a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/leds/trigger`. Source: `D1/in/raw/alma/members/4c1fd9c82acc1b7190ef5f7a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ledtrig-backlight.ko.xz`, `ledtrig-camera.ko.xz`, `ledtrig-default-on.ko.xz`, `ledtrig-gpio.ko.xz`, `ledtrig-heartbeat.ko.xz`, `ledtrig-netdev.ko.xz`, `ledtrig-oneshot.ko.xz`, `ledtrig-timer.ko.xz`, `ledtrig-transient.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-24eb3fc0428babbc9b5fa2b7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/md`. Source: `D1/in/raw/alma/members/24eb3fc0428babbc9b5fa2b7.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: dm-bio-prison.ko.xz,dm-bufio.ko.xz,dm-cache-smq.ko.xz,dm-cache.ko.xz,dm-crypt.ko.xz,dm-delay.ko.xz,dm-era.ko.xz,dm-flakey.ko.xz,dm-historical-service-time.ko.xz,dm-integrity.ko.xz,dm-io-affinity.ko.xz,dm-log-userspace.ko.xz,dm-log-writes.ko.xz,dm-log.ko.xz,dm-mirror.ko.xz,dm-mod.ko.xz,dm-multipath.ko.xz,dm-queue-length.ko.xz,dm-raid.ko.xz,dm-region-hash.ko.xz,dm-round-robin.ko.xz,dm-service-time.ko.xz,dm-snapshot.ko.xz,dm-switch.ko.xz,dm-thin-pool.ko.xz,dm-verity.ko.xz,dm-writecache.ko.xz,dm-zero.ko.xz,linear.ko.xz,raid0.ko.xz,raid1.ko.xz,raid10.ko.xz,raid456.ko.xz; UNKNOWN: dm-vdo,persistent-data

- **INSTALLED-PACKAGE**: `dm-bio-prison.ko.xz`, `dm-bufio.ko.xz`, `dm-cache-smq.ko.xz`, `dm-cache.ko.xz`, `dm-crypt.ko.xz`, `dm-delay.ko.xz`, `dm-era.ko.xz`, `dm-flakey.ko.xz`, `dm-historical-service-time.ko.xz`, `dm-integrity.ko.xz`, `dm-io-affinity.ko.xz`, `dm-log-userspace.ko.xz`, `dm-log-writes.ko.xz`, `dm-log.ko.xz`, `dm-mirror.ko.xz`, `dm-mod.ko.xz`, `dm-multipath.ko.xz`, `dm-queue-length.ko.xz`, `dm-raid.ko.xz`, `dm-region-hash.ko.xz`, `dm-round-robin.ko.xz`, `dm-service-time.ko.xz`, `dm-snapshot.ko.xz`, `dm-switch.ko.xz`, `dm-thin-pool.ko.xz`, `dm-verity.ko.xz`, `dm-writecache.ko.xz`, `dm-zero.ko.xz`, `linear.ko.xz`, `raid0.ko.xz`, `raid1.ko.xz`, `raid10.ko.xz`, `raid456.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `dm-vdo`, `persistent-data`. Directory installation integrity and creation provenance are not established.
### alma-4d0e2ee4fcc17fd49cbcff16

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/md/dm-vdo`. Source: `D1/in/raw/alma/members/4d0e2ee4fcc17fd49cbcff16.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dm-vdo.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aea7aad4f08a04308068c3c2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/md/persistent-data`. Source: `D1/in/raw/alma/members/aea7aad4f08a04308068c3c2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dm-persistent-data.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-737c80a08a17c5317539444a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media`. Source: `D1/in/raw/alma/members/737c80a08a17c5317539444a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cec`, `common`, `i2c`, `mc`, `pci`, `platform`, `usb`, `v4l2-core`. Directory installation integrity and creation provenance are not established.
### alma-e2da01ddb96d2cdd42307674

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/cec`. Source: `D1/in/raw/alma/members/e2da01ddb96d2cdd42307674.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `core`, `usb`. Directory installation integrity and creation provenance are not established.
### alma-9d48c1a9abc5c081258d9fa7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/cec/core`. Source: `D1/in/raw/alma/members/9d48c1a9abc5c081258d9fa7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ec41342b3957ec9519a2e138

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/cec/usb`. Source: `D1/in/raw/alma/members/ec41342b3957ec9519a2e138.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `pulse8`, `rainshadow`. Directory installation integrity and creation provenance are not established.
### alma-a843880f69badb334c7dfc4a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/cec/usb/pulse8`. Source: `D1/in/raw/alma/members/a843880f69badb334c7dfc4a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pulse8-cec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c867e01926ac1875f06348bc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/cec/usb/rainshadow`. Source: `D1/in/raw/alma/members/c867e01926ac1875f06348bc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rainshadow-cec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0796c699acf3050406265769

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/common`. Source: `D1/in/raw/alma/members/0796c699acf3050406265769.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cx2341x.ko.xz,tveeprom.ko.xz,uvc.ko.xz; UNKNOWN: videobuf2

- **INSTALLED-PACKAGE**: `cx2341x.ko.xz`, `tveeprom.ko.xz`, `uvc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `videobuf2`. Directory installation integrity and creation provenance are not established.
### alma-c484c17f8422b13d50fbde5a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/common/videobuf2`. Source: `D1/in/raw/alma/members/c484c17f8422b13d50fbde5a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `videobuf2-common.ko.xz`, `videobuf2-dma-contig.ko.xz`, `videobuf2-dma-sg.ko.xz`, `videobuf2-memops.ko.xz`, `videobuf2-v4l2.ko.xz`, `videobuf2-vmalloc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-22e6e5f67f2ee9391cfb0a57

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/i2c`. Source: `D1/in/raw/alma/members/22e6e5f67f2ee9391cfb0a57.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cs3308.ko.xz,hi556.ko.xz,ov01a10.ko.xz,ov08x40.ko.xz,ov13858.ko.xz,ov13b10.ko.xz,ov2740.ko.xz,ov5675.ko.xz,ov8856.ko.xz,saa6588.ko.xz,saa6752hs.ko.xz; UNKNOWN: cx25840

- **INSTALLED-PACKAGE**: `cs3308.ko.xz`, `hi556.ko.xz`, `ov01a10.ko.xz`, `ov08x40.ko.xz`, `ov13858.ko.xz`, `ov13b10.ko.xz`, `ov2740.ko.xz`, `ov5675.ko.xz`, `ov8856.ko.xz`, `saa6588.ko.xz`, `saa6752hs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `cx25840`. Directory installation integrity and creation provenance are not established.
### alma-28f016eef22137f4dd3c6739

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/i2c/cx25840`. Source: `D1/in/raw/alma/members/28f016eef22137f4dd3c6739.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cx25840.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f42d5b8f57fcb11ef028ba16

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/mc`. Source: `D1/in/raw/alma/members/f42d5b8f57fcb11ef028ba16.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c68e225618653949d2b7faf5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/pci`. Source: `D1/in/raw/alma/members/c68e225618653949d2b7faf5.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `intel`. Directory installation integrity and creation provenance are not established.
### alma-de0fac83ba2079eb1a9ad760

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/pci/intel`. Source: `D1/in/raw/alma/members/de0fac83ba2079eb1a9ad760.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ipu-bridge.ko.xz; UNKNOWN: ipu6,ivsc

- **INSTALLED-PACKAGE**: `ipu-bridge.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `ipu6`, `ivsc`. Directory installation integrity and creation provenance are not established.
### alma-c9fed32eef0b7fec281170b3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/pci/intel/ipu6`. Source: `D1/in/raw/alma/members/c9fed32eef0b7fec281170b3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-ipu6-isys.ko.xz`, `intel-ipu6.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e0d953bf481f66815ac4baf0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/pci/intel/ivsc`. Source: `D1/in/raw/alma/members/e0d953bf481f66815ac4baf0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ivsc-ace.ko.xz`, `ivsc-csi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-991161390085c152d691d51f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/platform`. Source: `D1/in/raw/alma/members/991161390085c152d691d51f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `amd`. Directory installation integrity and creation provenance are not established.
### alma-145337a56363a215e168664a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/platform/amd`. Source: `D1/in/raw/alma/members/145337a56363a215e168664a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `isp4`. Directory installation integrity and creation provenance are not established.
### alma-ba2009e4dd3bee4cfe3cf5f7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/platform/amd/isp4`. Source: `D1/in/raw/alma/members/ba2009e4dd3bee4cfe3cf5f7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd_isp4_capture.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-acbcd10668f28e3ca8f54b8f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb`. Source: `D1/in/raw/alma/members/acbcd10668f28e3ca8f54b8f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cx231xx`, `gspca`, `pwc`, `s2255`, `uvc`. Directory installation integrity and creation provenance are not established.
### alma-8b4f8a9cbd75d090c1d6c768

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/cx231xx`. Source: `D1/in/raw/alma/members/8b4f8a9cbd75d090c1d6c768.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cx231xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2023b790147069a52d36fd1e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/gspca`. Source: `D1/in/raw/alma/members/2023b790147069a52d36fd1e.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: gspca_benq.ko.xz,gspca_conex.ko.xz,gspca_cpia1.ko.xz,gspca_etoms.ko.xz,gspca_finepix.ko.xz,gspca_jeilinj.ko.xz,gspca_jl2005bcd.ko.xz,gspca_konica.ko.xz,gspca_main.ko.xz,gspca_mars.ko.xz,gspca_mr97310a.ko.xz,gspca_nw80x.ko.xz,gspca_ov519.ko.xz,gspca_ov534.ko.xz,gspca_ov534_9.ko.xz,gspca_pac207.ko.xz,gspca_pac7302.ko.xz,gspca_pac7311.ko.xz,gspca_se401.ko.xz,gspca_sn9c2028.ko.xz,gspca_sn9c20x.ko.xz,gspca_sonixb.ko.xz,gspca_sonixj.ko.xz,gspca_spca1528.ko.xz,gspca_spca500.ko.xz,gspca_spca501.ko.xz,gspca_spca505.ko.xz,gspca_spca506.ko.xz,gspca_spca508.ko.xz,gspca_spca561.ko.xz,gspca_sq905.ko.xz,gspca_sq905c.ko.xz,gspca_sq930x.ko.xz,gspca_stk014.ko.xz,gspca_stv0680.ko.xz,gspca_sunplus.ko.xz,gspca_t613.ko.xz,gspca_topro.ko.xz,gspca_tv8532.ko.xz,gspca_vc032x.ko.xz,gspca_vicam.ko.xz,gspca_xirlink_cit.ko.xz,gspca_zc3xx.ko.xz; UNKNOWN: gl860,m5602,stv06xx

- **UNKNOWN**: `gl860`, `m5602`, `stv06xx`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `gspca_benq.ko.xz`, `gspca_conex.ko.xz`, `gspca_cpia1.ko.xz`, `gspca_etoms.ko.xz`, `gspca_finepix.ko.xz`, `gspca_jeilinj.ko.xz`, `gspca_jl2005bcd.ko.xz`, `gspca_konica.ko.xz`, `gspca_main.ko.xz`, `gspca_mars.ko.xz`, `gspca_mr97310a.ko.xz`, `gspca_nw80x.ko.xz`, `gspca_ov519.ko.xz`, `gspca_ov534.ko.xz`, `gspca_ov534_9.ko.xz`, `gspca_pac207.ko.xz`, `gspca_pac7302.ko.xz`, `gspca_pac7311.ko.xz`, `gspca_se401.ko.xz`, `gspca_sn9c2028.ko.xz`, `gspca_sn9c20x.ko.xz`, `gspca_sonixb.ko.xz`, `gspca_sonixj.ko.xz`, `gspca_spca1528.ko.xz`, `gspca_spca500.ko.xz`, `gspca_spca501.ko.xz`, `gspca_spca505.ko.xz`, `gspca_spca506.ko.xz`, `gspca_spca508.ko.xz`, `gspca_spca561.ko.xz`, `gspca_sq905.ko.xz`, `gspca_sq905c.ko.xz`, `gspca_sq930x.ko.xz`, `gspca_stk014.ko.xz`, `gspca_stv0680.ko.xz`, `gspca_sunplus.ko.xz`, `gspca_t613.ko.xz`, `gspca_topro.ko.xz`, `gspca_tv8532.ko.xz`, `gspca_vc032x.ko.xz`, `gspca_vicam.ko.xz`, `gspca_xirlink_cit.ko.xz`, `gspca_zc3xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4ea901a367a230f4e4594ded

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/gspca/gl860`. Source: `D1/in/raw/alma/members/4ea901a367a230f4e4594ded.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gspca_gl860.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a9bc322e7e1a1dab78a87be6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/gspca/m5602`. Source: `D1/in/raw/alma/members/a9bc322e7e1a1dab78a87be6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gspca_m5602.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-10c3f7859b4463c56fd63642

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/gspca/stv06xx`. Source: `D1/in/raw/alma/members/10c3f7859b4463c56fd63642.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gspca_stv06xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1b1260ce885954c4bb1f7fcb

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/pwc`. Source: `D1/in/raw/alma/members/1b1260ce885954c4bb1f7fcb.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pwc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f3dd66a6df28d1c10816c605

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/s2255`. Source: `D1/in/raw/alma/members/f3dd66a6df28d1c10816c605.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `s2255drv.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e836ec408bdc82c8d6456d49

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/usb/uvc`. Source: `D1/in/raw/alma/members/e836ec408bdc82c8d6456d49.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `uvcvideo.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-530362b5e159b30fe5803b63

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/media/v4l2-core`. Source: `D1/in/raw/alma/members/530362b5e159b30fe5803b63.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tuner.ko.xz`, `v4l2-async.ko.xz`, `v4l2-cci.ko.xz`, `v4l2-dv-timings.ko.xz`, `v4l2-fwnode.ko.xz`, `videodev.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-62cc7bea48cbaeb0e281d810

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/memstick`. Source: `D1/in/raw/alma/members/62cc7bea48cbaeb0e281d810.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `core`, `host`. Directory installation integrity and creation provenance are not established.
### alma-8c475c69350305b35b076066

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/memstick/core`. Source: `D1/in/raw/alma/members/8c475c69350305b35b076066.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `memstick.ko.xz`, `mspro_block.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8ad15907878ccd92773e775c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/memstick/host`. Source: `D1/in/raw/alma/members/8ad15907878ccd92773e775c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `jmb38x_ms.ko.xz`, `r592.ko.xz`, `rtsx_usb_ms.ko.xz`, `tifm_ms.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-eb7f629cfdc547e6da282bda

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/message`. Source: `D1/in/raw/alma/members/eb7f629cfdc547e6da282bda.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `fusion`. Directory installation integrity and creation provenance are not established.
### alma-3dbab6fc2e66974deab9b312

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/message/fusion`. Source: `D1/in/raw/alma/members/3dbab6fc2e66974deab9b312.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mptbase.ko.xz`, `mptsas.ko.xz`, `mptscsih.ko.xz`, `mptspi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f8933d1e489297385c915ab9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mfd`. Source: `D1/in/raw/alma/members/f8933d1e489297385c915ab9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cs42l43-sdw.ko.xz`, `cs42l43.ko.xz`, `intel-m10-bmc-core.ko.xz`, `intel-m10-bmc-spi.ko.xz`, `lpc_ich.ko.xz`, `lpc_sch.ko.xz`, `sm501.ko.xz`, `vx855.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3633746d03e4f06267330c20

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc`. Source: `D1/in/raw/alma/members/3633746d03e4f06267330c20.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: apds9802als.ko.xz,apds990x.ko.xz,bh1770glc.ko.xz,enclosure.ko.xz,hpilo.ko.xz,isl29003.ko.xz,isl29020.ko.xz,rpmb-core.ko.xz,tifm_7xx1.ko.xz,tifm_core.ko.xz,tsl2550.ko.xz,vmw_balloon.ko.xz; UNKNOWN: altera-stapl,cardreader,cb710,eeprom,lis3lv02d,mei,pvpanic,sgi-gru,sgi-xp,vmw_vmci

- **UNKNOWN**: `altera-stapl`, `cardreader`, `cb710`, `eeprom`, `lis3lv02d`, `mei`, `pvpanic`, `sgi-gru`, `sgi-xp`, `vmw_vmci`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `apds9802als.ko.xz`, `apds990x.ko.xz`, `bh1770glc.ko.xz`, `enclosure.ko.xz`, `hpilo.ko.xz`, `isl29003.ko.xz`, `isl29020.ko.xz`, `rpmb-core.ko.xz`, `tifm_7xx1.ko.xz`, `tifm_core.ko.xz`, `tsl2550.ko.xz`, `vmw_balloon.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b141cad87e60197004b383b6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/altera-stapl`. Source: `D1/in/raw/alma/members/b141cad87e60197004b383b6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `altera-stapl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e5b4f01fb24daa2722fd9d9e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/cardreader`. Source: `D1/in/raw/alma/members/e5b4f01fb24daa2722fd9d9e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtsx_pci.ko.xz`, `rtsx_usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-17ade1a0636a95dacfafb255

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/cb710`. Source: `D1/in/raw/alma/members/17ade1a0636a95dacfafb255.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cb710.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a99d1e77ec54df481ada90db

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/eeprom`. Source: `D1/in/raw/alma/members/a99d1e77ec54df481ada90db.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `eeprom_93cx6.ko.xz`, `max6875.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-802e7c41842d802b229ee60d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/lis3lv02d`. Source: `D1/in/raw/alma/members/802e7c41842d802b229ee60d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `lis3lv02d.ko.xz`, `lis3lv02d_i2c.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2bca2f6c0f567142fe8c5fab

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/mei`. Source: `D1/in/raw/alma/members/2bca2f6c0f567142fe8c5fab.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mei-gsc.ko.xz,mei-me.ko.xz,mei-vsc-hw.ko.xz,mei-vsc.ko.xz,mei.ko.xz; UNKNOWN: gsc_proxy,pxp

- **UNKNOWN**: `gsc_proxy`, `pxp`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `mei-gsc.ko.xz`, `mei-me.ko.xz`, `mei-vsc-hw.ko.xz`, `mei-vsc.ko.xz`, `mei.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-db9d3a732d0e0dc963b831b9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/mei/gsc_proxy`. Source: `D1/in/raw/alma/members/db9d3a732d0e0dc963b831b9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mei_gsc_proxy.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-06174afae412d2e046de57b5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/mei/pxp`. Source: `D1/in/raw/alma/members/06174afae412d2e046de57b5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mei_pxp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-147b10066374f4bb11868e6f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/pvpanic`. Source: `D1/in/raw/alma/members/147b10066374f4bb11868e6f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pvpanic-mmio.ko.xz`, `pvpanic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dfe52718fbbe64212b12a4ea

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/sgi-gru`. Source: `D1/in/raw/alma/members/dfe52718fbbe64212b12a4ea.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gru.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e1222153ee1b8a943720121d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/sgi-xp`. Source: `D1/in/raw/alma/members/e1222153ee1b8a943720121d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xp.ko.xz`, `xpc.ko.xz`, `xpnet.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-34ea36b893e3ffa8a8b95120

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/misc/vmw_vmci`. Source: `D1/in/raw/alma/members/34ea36b893e3ffa8a8b95120.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vmw_vmci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5c32cb7c31692e574cc3ea36

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mmc`. Source: `D1/in/raw/alma/members/5c32cb7c31692e574cc3ea36.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `core`, `host`. Directory installation integrity and creation provenance are not established.
### alma-ddb0f9fddf2c6ff232792fa9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mmc/core`. Source: `D1/in/raw/alma/members/ddb0f9fddf2c6ff232792fa9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mmc_block.ko.xz`, `mmc_core.ko.xz`, `sdio_uart.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-62d0426b49740406e305954b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mmc/host`. Source: `D1/in/raw/alma/members/62d0426b49740406e305954b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cb710-mmc.ko.xz`, `cqhci.ko.xz`, `rtsx_pci_sdmmc.ko.xz`, `rtsx_usb_sdmmc.ko.xz`, `sdhci-acpi.ko.xz`, `sdhci-pci.ko.xz`, `sdhci-pltfm.ko.xz`, `sdhci.ko.xz`, `tifm_sd.ko.xz`, `ushc.ko.xz`, `via-sdmmc.ko.xz`, `vub300.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0414488135d507688f8c41d3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mtd`. Source: `D1/in/raw/alma/members/0414488135d507688f8c41d3.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mtd.ko.xz,mtd_blkdevs.ko.xz,mtdblock.ko.xz; UNKNOWN: chips,devices,ubi

- **UNKNOWN**: `chips`, `devices`, `ubi`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `mtd.ko.xz`, `mtd_blkdevs.ko.xz`, `mtdblock.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-96e3221a3231d225fea7a132

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mtd/chips`. Source: `D1/in/raw/alma/members/96e3221a3231d225fea7a132.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `chipreg.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d30241772b5f4ac5c25c8556

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mtd/devices`. Source: `D1/in/raw/alma/members/d30241772b5f4ac5c25c8556.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mtd_intel_dg.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-33080793d72834b48a940627

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/mtd/ubi`. Source: `D1/in/raw/alma/members/33080793d72834b48a940627.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ubi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-94305049b4a392182107f57a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net`. Source: `D1/in/raw/alma/members/94305049b4a392182107f57a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: bareudp.ko.xz,dummy.ko.xz,geneve.ko.xz,ifb.ko.xz,macsec.ko.xz,macvlan.ko.xz,macvtap.ko.xz,mdio.ko.xz,mhi_net.ko.xz,mii.ko.xz,net_failover.ko.xz,netconsole.ko.xz,nlmon.ko.xz,ntb_netdev.ko.xz,tap.ko.xz,tun.ko.xz,veth.ko.xz,virtio_net.ko.xz,vrf.ko.xz,vsockmon.ko.xz,xen-netfront.ko.xz; UNKNOWN: bonding,can,ethernet,fjes,hyperv,ieee802154,ipvlan,mdio,netdevsim,pcs,phy,ppp,slip,thunderbolt,usb,vmxnet3,vxlan,wan,wireguard,wireless,wwan

- **INSTALLED-PACKAGE**: `bareudp.ko.xz`, `dummy.ko.xz`, `geneve.ko.xz`, `ifb.ko.xz`, `macsec.ko.xz`, `macvlan.ko.xz`, `macvtap.ko.xz`, `mdio.ko.xz`, `mhi_net.ko.xz`, `mii.ko.xz`, `net_failover.ko.xz`, `netconsole.ko.xz`, `nlmon.ko.xz`, `ntb_netdev.ko.xz`, `tap.ko.xz`, `tun.ko.xz`, `veth.ko.xz`, `virtio_net.ko.xz`, `vrf.ko.xz`, `vsockmon.ko.xz`, `xen-netfront.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `bonding`, `can`, `ethernet`, `fjes`, `hyperv`, `ieee802154`, `ipvlan`, `mdio`, `netdevsim`, `pcs`, `phy`, `ppp`, `slip`, `thunderbolt`, `usb`, `vmxnet3`, `vxlan`, `wan`, `wireguard`, `wireless`, `wwan`. Directory installation integrity and creation provenance are not established.
### alma-15b04ae7edf0c299cf48a363

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/bonding`. Source: `D1/in/raw/alma/members/15b04ae7edf0c299cf48a363.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bonding.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-63eb67e0bca196994654682d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can`. Source: `D1/in/raw/alma/members/63eb67e0bca196994654682d.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: vcan.ko.xz,vxcan.ko.xz; UNKNOWN: dev,m_can,peak_canfd,slcan,spi,usb

- **UNKNOWN**: `dev`, `m_can`, `peak_canfd`, `slcan`, `spi`, `usb`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `vcan.ko.xz`, `vxcan.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1f651159eae089f0edf15aa4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/dev`. Source: `D1/in/raw/alma/members/1f651159eae089f0edf15aa4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `can-dev.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-17fbf7ee5eba740e9accc1a6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/m_can`. Source: `D1/in/raw/alma/members/17fbf7ee5eba740e9accc1a6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `m_can.ko.xz`, `m_can_pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9ff348daebbc598c301e5816

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/peak_canfd`. Source: `D1/in/raw/alma/members/9ff348daebbc598c301e5816.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `peak_pciefd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a19ea26ffb82d597157782e3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/slcan`. Source: `D1/in/raw/alma/members/a19ea26ffb82d597157782e3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `slcan.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7fa5370953387651d56b6bc0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/spi`. Source: `D1/in/raw/alma/members/7fa5370953387651d56b6bc0.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mcp251x.ko.xz; UNKNOWN: mcp251xfd

- **INSTALLED-PACKAGE**: `mcp251x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `mcp251xfd`. Directory installation integrity and creation provenance are not established.
### alma-c6f5e6073176d49555554cf0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/spi/mcp251xfd`. Source: `D1/in/raw/alma/members/c6f5e6073176d49555554cf0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mcp251xfd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3ea55060335146b5240cf38b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/usb`. Source: `D1/in/raw/alma/members/3ea55060335146b5240cf38b.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ems_usb.ko.xz,gs_usb.ko.xz,usb_8dev.ko.xz; UNKNOWN: kvaser_usb,peak_usb

- **INSTALLED-PACKAGE**: `ems_usb.ko.xz`, `gs_usb.ko.xz`, `usb_8dev.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `kvaser_usb`, `peak_usb`. Directory installation integrity and creation provenance are not established.
### alma-d6c54b4bb0e123903b8470ba

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/usb/kvaser_usb`. Source: `D1/in/raw/alma/members/d6c54b4bb0e123903b8470ba.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `kvaser_usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f4ba7e164dd2d9f85a3f8e01

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/can/usb/peak_usb`. Source: `D1/in/raw/alma/members/f4ba7e164dd2d9f85a3f8e01.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `peak_usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-de21be329da50e372845edc3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet`. Source: `D1/in/raw/alma/members/de21be329da50e372845edc3.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: dnet.ko.xz,ethoc.ko.xz; UNKNOWN: amazon,amd,aquantia,atheros,broadcom,chelsio,cisco,dlink,emulex,google,huawei,intel,marvell,mellanox,microchip,microsoft,myricom,pensando,qlogic,realtek,rocker,sfc,stmicro

- **UNKNOWN**: `amazon`, `amd`, `aquantia`, `atheros`, `broadcom`, `chelsio`, `cisco`, `dlink`, `emulex`, `google`, `huawei`, `intel`, `marvell`, `mellanox`, `microchip`, `microsoft`, `myricom`, `pensando`, `qlogic`, `realtek`, `rocker`, `sfc`, `stmicro`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `dnet.ko.xz`, `ethoc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0861e049525516a6910566c6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/amazon`. Source: `D1/in/raw/alma/members/0861e049525516a6910566c6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ena`. Directory installation integrity and creation provenance are not established.
### alma-764f8ad7784d15d8b0d06462

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/amazon/ena`. Source: `D1/in/raw/alma/members/764f8ad7784d15d8b0d06462.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ena.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4f13401a93e99c6653b7fd7e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/amd`. Source: `D1/in/raw/alma/members/4f13401a93e99c6653b7fd7e.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `xgbe`. Directory installation integrity and creation provenance are not established.
### alma-ede2ed7ed027d53661649c06

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/amd/xgbe`. Source: `D1/in/raw/alma/members/ede2ed7ed027d53661649c06.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd-xgbe.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c75af676d312ab8f46184612

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/aquantia`. Source: `D1/in/raw/alma/members/c75af676d312ab8f46184612.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `atlantic`. Directory installation integrity and creation provenance are not established.
### alma-f9372f09e8878fb3f5bb3a54

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/aquantia/atlantic`. Source: `D1/in/raw/alma/members/f9372f09e8878fb3f5bb3a54.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `atlantic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d6df27a396092135f36c317e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/atheros`. Source: `D1/in/raw/alma/members/d6df27a396092135f36c317e.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `alx`, `atl1c`, `atl1e`, `atlx`. Directory installation integrity and creation provenance are not established.
### alma-b1edbce9dcd7526f8e869e7b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/atheros/alx`. Source: `D1/in/raw/alma/members/b1edbce9dcd7526f8e869e7b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `alx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f6ff9333166f33d320e4583b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/atheros/atl1c`. Source: `D1/in/raw/alma/members/f6ff9333166f33d320e4583b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `atl1c.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2c69f9f6fafd998cba3030a0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/atheros/atl1e`. Source: `D1/in/raw/alma/members/2c69f9f6fafd998cba3030a0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `atl1e.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-19c7b2fd2aeee1066e3dce70

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/atheros/atlx`. Source: `D1/in/raw/alma/members/19c7b2fd2aeee1066e3dce70.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `atl1.ko.xz`, `atl2.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-90345e0f58ec79cef7ea7943

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/broadcom`. Source: `D1/in/raw/alma/members/90345e0f58ec79cef7ea7943.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: bnx2.ko.xz,cnic.ko.xz,tg3.ko.xz; UNKNOWN: bnx2x,bnxt,genet

- **INSTALLED-PACKAGE**: `bnx2.ko.xz`, `cnic.ko.xz`, `tg3.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `bnx2x`, `bnxt`, `genet`. Directory installation integrity and creation provenance are not established.
### alma-06f3083cad7edff778eb1b0c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/broadcom/bnx2x`. Source: `D1/in/raw/alma/members/06f3083cad7edff778eb1b0c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnx2x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-413c669f296603f734e5222f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/broadcom/bnxt`. Source: `D1/in/raw/alma/members/413c669f296603f734e5222f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnxt_en.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bfb5bb1a12406e2523acdd38

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/broadcom/genet`. Source: `D1/in/raw/alma/members/bfb5bb1a12406e2523acdd38.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `genet.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7a936ec21633c95a616f157d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio`. Source: `D1/in/raw/alma/members/7a936ec21633c95a616f157d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cxgb4`, `cxgb4vf`, `inline_crypto`, `libcxgb`. Directory installation integrity and creation provenance are not established.
### alma-1d5460b4babc9adc51e07bc5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/cxgb4`. Source: `D1/in/raw/alma/members/1d5460b4babc9adc51e07bc5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxgb4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fec0ebbc3c4cea8f72ceea1d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/cxgb4vf`. Source: `D1/in/raw/alma/members/fec0ebbc3c4cea8f72ceea1d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxgb4vf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9b0ccc043a006924258253aa

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/inline_crypto`. Source: `D1/in/raw/alma/members/9b0ccc043a006924258253aa.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ch_ipsec`, `ch_ktls`. Directory installation integrity and creation provenance are not established.
### alma-40426afbf14284a64bee7e6d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/inline_crypto/ch_ipsec`. Source: `D1/in/raw/alma/members/40426afbf14284a64bee7e6d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ch_ipsec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7499bea678ff57f1db9970f1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/inline_crypto/ch_ktls`. Source: `D1/in/raw/alma/members/7499bea678ff57f1db9970f1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ch_ktls.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1803926e498a7d24c1f82919

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/chelsio/libcxgb`. Source: `D1/in/raw/alma/members/1803926e498a7d24c1f82919.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libcxgb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e89eb8698d65976af6361599

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/cisco`. Source: `D1/in/raw/alma/members/e89eb8698d65976af6361599.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `enic`. Directory installation integrity and creation provenance are not established.
### alma-b77dbb02673d23859f1d9043

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/cisco/enic`. Source: `D1/in/raw/alma/members/b77dbb02673d23859f1d9043.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `enic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-78ba4e7545422d65c6543a96

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/dlink`. Source: `D1/in/raw/alma/members/78ba4e7545422d65c6543a96.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dl2k.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ce4953bd5b01ff18d5fe4442

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/emulex`. Source: `D1/in/raw/alma/members/ce4953bd5b01ff18d5fe4442.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `benet`. Directory installation integrity and creation provenance are not established.
### alma-2935eead6c10ef370f7c0713

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/emulex/benet`. Source: `D1/in/raw/alma/members/2935eead6c10ef370f7c0713.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `be2net.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-223b757fff6fc125d10cd437

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/google`. Source: `D1/in/raw/alma/members/223b757fff6fc125d10cd437.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `gve`. Directory installation integrity and creation provenance are not established.
### alma-3fe66a6b2c4725c984482751

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/google/gve`. Source: `D1/in/raw/alma/members/3fe66a6b2c4725c984482751.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `gve.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c0a9a99e5c6f8e8c25b7e16d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/huawei`. Source: `D1/in/raw/alma/members/c0a9a99e5c6f8e8c25b7e16d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `hinic`. Directory installation integrity and creation provenance are not established.
### alma-e9d86a48bc3907e180dc2a4d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/huawei/hinic`. Source: `D1/in/raw/alma/members/e9d86a48bc3907e180dc2a4d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hinic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-75dbe7586c8dc1033cc6af53

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel`. Source: `D1/in/raw/alma/members/75dbe7586c8dc1033cc6af53.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `e1000`, `e1000e`, `fm10k`, `i40e`, `iavf`, `ice`, `idpf`, `igb`, `igbvf`, `igc`, `ixgbe`, `ixgbevf`, `libeth`, `libie`. Directory installation integrity and creation provenance are not established.
### alma-0e59bea94935a73ce9538077

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/e1000`. Source: `D1/in/raw/alma/members/0e59bea94935a73ce9538077.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `e1000.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4a98968ed2c09ab9a5a50436

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/e1000e`. Source: `D1/in/raw/alma/members/4a98968ed2c09ab9a5a50436.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `e1000e.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7dca69c4fd006258a99a8f4f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/fm10k`. Source: `D1/in/raw/alma/members/7dca69c4fd006258a99a8f4f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fm10k.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c5720bfc802b4868718b12c7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/i40e`. Source: `D1/in/raw/alma/members/c5720bfc802b4868718b12c7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `i40e.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-de151a7f7035961014ce4f14

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/iavf`. Source: `D1/in/raw/alma/members/de151a7f7035961014ce4f14.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iavf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f265b5046390d225bdb2e556

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/ice`. Source: `D1/in/raw/alma/members/f265b5046390d225bdb2e556.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ice.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-445c7b04f0e6ecbf939b081d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/idpf`. Source: `D1/in/raw/alma/members/445c7b04f0e6ecbf939b081d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `idpf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-144b7de4068193494adc3119

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/igb`. Source: `D1/in/raw/alma/members/144b7de4068193494adc3119.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `igb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-60b30e316494129a4444cf35

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/igbvf`. Source: `D1/in/raw/alma/members/60b30e316494129a4444cf35.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `igbvf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-eea641bc8b66c948f9293302

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/igc`. Source: `D1/in/raw/alma/members/eea641bc8b66c948f9293302.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `igc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c5ecdd3cfa9e69e91eb1dfa1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/ixgbe`. Source: `D1/in/raw/alma/members/c5ecdd3cfa9e69e91eb1dfa1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ixgbe.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1188373a2870f6a73f396f6b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/ixgbevf`. Source: `D1/in/raw/alma/members/1188373a2870f6a73f396f6b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ixgbevf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fa65c3cd2c6007548567df27

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/libeth`. Source: `D1/in/raw/alma/members/fa65c3cd2c6007548567df27.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libeth.ko.xz`, `libeth_xdp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1d63ec546c11d71c211db06d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/intel/libie`. Source: `D1/in/raw/alma/members/1d63ec546c11d71c211db06d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libie.ko.xz`, `libie_adminq.ko.xz`, `libie_fwlog.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c8a20d71a2822b43adf2a394

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/marvell`. Source: `D1/in/raw/alma/members/c8a20d71a2822b43adf2a394.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `octeon_ep`, `octeon_ep_vf`. Directory installation integrity and creation provenance are not established.
### alma-23185281c74ec1fbd10b13f6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/marvell/octeon_ep`. Source: `D1/in/raw/alma/members/23185281c74ec1fbd10b13f6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `octeon_ep.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a402e3fa544b0ba1da50bc70

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/marvell/octeon_ep_vf`. Source: `D1/in/raw/alma/members/a402e3fa544b0ba1da50bc70.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `octeon_ep_vf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-606857bb6143346cbff1cf7e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox`. Source: `D1/in/raw/alma/members/606857bb6143346cbff1cf7e.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mlx4`, `mlx5`, `mlxfw`, `mlxsw`. Directory installation integrity and creation provenance are not established.
### alma-1ef878b2fae1af560d7e0fb5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox/mlx4`. Source: `D1/in/raw/alma/members/1ef878b2fae1af560d7e0fb5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx4_core.ko.xz`, `mlx4_en.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4e259c98db5f14c0db032da1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox/mlx5`. Source: `D1/in/raw/alma/members/4e259c98db5f14c0db032da1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `core`. Directory installation integrity and creation provenance are not established.
### alma-058c211b786265a568815cba

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox/mlx5/core`. Source: `D1/in/raw/alma/members/058c211b786265a568815cba.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx5_core.ko.xz`, `mlx5_dpll.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d94479b9531144a417a87298

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox/mlxfw`. Source: `D1/in/raw/alma/members/d94479b9531144a417a87298.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlxfw.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8f00a1b0984e0987c66f8beb

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/mellanox/mlxsw`. Source: `D1/in/raw/alma/members/8f00a1b0984e0987c66f8beb.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlxsw_core.ko.xz`, `mlxsw_i2c.ko.xz`, `mlxsw_minimal.ko.xz`, `mlxsw_pci.ko.xz`, `mlxsw_spectrum.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7b0a6ea53fa889623ed5d426

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/microchip`. Source: `D1/in/raw/alma/members/7b0a6ea53fa889623ed5d426.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `lan743x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2f1d7c4803073679906d0c07

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/microsoft`. Source: `D1/in/raw/alma/members/2f1d7c4803073679906d0c07.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mana`. Directory installation integrity and creation provenance are not established.
### alma-8a816451410661d021c124bd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/microsoft/mana`. Source: `D1/in/raw/alma/members/8a816451410661d021c124bd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mana.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-098b207d53951e422083d7c3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/myricom`. Source: `D1/in/raw/alma/members/098b207d53951e422083d7c3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `myri10ge`. Directory installation integrity and creation provenance are not established.
### alma-0835ce53ca2e6ee6ba480912

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/myricom/myri10ge`. Source: `D1/in/raw/alma/members/0835ce53ca2e6ee6ba480912.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `myri10ge.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6c7a2f44f8cabbfbed885de1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/pensando`. Source: `D1/in/raw/alma/members/6c7a2f44f8cabbfbed885de1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ionic`. Directory installation integrity and creation provenance are not established.
### alma-4b47d294fd7178e899027fca

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/pensando/ionic`. Source: `D1/in/raw/alma/members/4b47d294fd7178e899027fca.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ionic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-75bdc3ca9c527e6724bfd809

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/qlogic`. Source: `D1/in/raw/alma/members/75bdc3ca9c527e6724bfd809.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `netxen`, `qed`, `qede`. Directory installation integrity and creation provenance are not established.
### alma-9edd19890ca6fe42234cf331

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/qlogic/netxen`. Source: `D1/in/raw/alma/members/9edd19890ca6fe42234cf331.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `netxen_nic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-73c66ec99ed598ce6d265fd3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/qlogic/qed`. Source: `D1/in/raw/alma/members/73c66ec99ed598ce6d265fd3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qed.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-322a37838601db0cf1a1426c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/qlogic/qede`. Source: `D1/in/raw/alma/members/322a37838601db0cf1a1426c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qede.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a21b01977366cd5c16e886bc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/realtek`. Source: `D1/in/raw/alma/members/a21b01977366cd5c16e886bc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `8139cp.ko.xz`, `8139too.ko.xz`, `r8169.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0e4aecde73617ef2abd47220

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/sfc`. Source: `D1/in/raw/alma/members/0e4aecde73617ef2abd47220.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: sfc.ko.xz; UNKNOWN: siena

- **INSTALLED-PACKAGE**: `sfc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `siena`. Directory installation integrity and creation provenance are not established.
### alma-972ccfbeccaa5ca996f3f1dc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/sfc/siena`. Source: `D1/in/raw/alma/members/972ccfbeccaa5ca996f3f1dc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `sfc-siena.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-82de037daeb88b4f255fa44a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/stmicro`. Source: `D1/in/raw/alma/members/82de037daeb88b4f255fa44a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `stmmac`. Directory installation integrity and creation provenance are not established.
### alma-689a5b450d8b5c433bd7d9b6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ethernet/stmicro/stmmac`. Source: `D1/in/raw/alma/members/689a5b450d8b5c433bd7d9b6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dwmac-intel.ko.xz`, `stmmac.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-af7a5426fbc5409d7c393891

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/fjes`. Source: `D1/in/raw/alma/members/af7a5426fbc5409d7c393891.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fjes.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f0b5db2754c26948e62f9ebf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/hyperv`. Source: `D1/in/raw/alma/members/f0b5db2754c26948e62f9ebf.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hv_netvsc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fbeac81efb8e3d6f694ee5a6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ieee802154`. Source: `D1/in/raw/alma/members/fbeac81efb8e3d6f694ee5a6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fakelb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7ab09301c00064700698d306

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ipvlan`. Source: `D1/in/raw/alma/members/7ab09301c00064700698d306.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ipvlan.ko.xz`, `ipvtap.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6108f47a7a338bb276c5a031

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/mdio`. Source: `D1/in/raw/alma/members/6108f47a7a338bb276c5a031.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mdio-bcm-unimac.ko.xz`, `mdio-bitbang.ko.xz`, `mdio-cavium.ko.xz`, `mdio-thunder.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fd4fbbfb5efc72fd6dd2888c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/pcs`. Source: `D1/in/raw/alma/members/fd4fbbfb5efc72fd6dd2888c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pcs_xpcs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-be9647e0109cf4ad997bddff

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/phy`. Source: `D1/in/raw/alma/members/be9647e0109cf4ad997bddff.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: air_en8811h.ko.xz,amd.ko.xz,as21xxx.ko.xz,ax88796b.ko.xz,bcm-phy-lib.ko.xz,bcm-phy-ptp.ko.xz,bcm7xxx.ko.xz,bcm87xx.ko.xz,broadcom.ko.xz,cicada.ko.xz,cortina.ko.xz,davicom.ko.xz,dp83640.ko.xz,dp83822.ko.xz,dp83848.ko.xz,dp83867.ko.xz,dp83tc811.ko.xz,dp83tg720.ko.xz,et1011c.ko.xz,icplus.ko.xz,intel-xway.ko.xz,lxt.ko.xz,marvell-88q2xxx.ko.xz,marvell.ko.xz,marvell10g.ko.xz,micrel.ko.xz,microchip.ko.xz,microchip_rds_ptp.ko.xz,microchip_t1.ko.xz,mxl-86110.ko.xz,mxl-gpy.ko.xz,national.ko.xz,phy_package.ko.xz,phylink.ko.xz,qsemi.ko.xz,rockchip.ko.xz,smsc.ko.xz,spi_ks8995.ko.xz,ste10Xp.ko.xz,teranetics.ko.xz,uPD60620.ko.xz,vitesse.ko.xz,xilinx_gmii2rgmii.ko.xz; UNKNOWN: aquantia,mscc,qcom,realtek

- **INSTALLED-PACKAGE**: `air_en8811h.ko.xz`, `amd.ko.xz`, `as21xxx.ko.xz`, `ax88796b.ko.xz`, `bcm-phy-lib.ko.xz`, `bcm-phy-ptp.ko.xz`, `bcm7xxx.ko.xz`, `bcm87xx.ko.xz`, `broadcom.ko.xz`, `cicada.ko.xz`, `cortina.ko.xz`, `davicom.ko.xz`, `dp83640.ko.xz`, `dp83822.ko.xz`, `dp83848.ko.xz`, `dp83867.ko.xz`, `dp83tc811.ko.xz`, `dp83tg720.ko.xz`, `et1011c.ko.xz`, `icplus.ko.xz`, `intel-xway.ko.xz`, `lxt.ko.xz`, `marvell-88q2xxx.ko.xz`, `marvell.ko.xz`, `marvell10g.ko.xz`, `micrel.ko.xz`, `microchip.ko.xz`, `microchip_rds_ptp.ko.xz`, `microchip_t1.ko.xz`, `mxl-86110.ko.xz`, `mxl-gpy.ko.xz`, `national.ko.xz`, `phy_package.ko.xz`, `phylink.ko.xz`, `qsemi.ko.xz`, `rockchip.ko.xz`, `smsc.ko.xz`, `spi_ks8995.ko.xz`, `ste10Xp.ko.xz`, `teranetics.ko.xz`, `uPD60620.ko.xz`, `vitesse.ko.xz`, `xilinx_gmii2rgmii.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `aquantia`, `mscc`, `qcom`, `realtek`. Directory installation integrity and creation provenance are not established.
### alma-80efaed15e278811260ab2b8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/phy/aquantia`. Source: `D1/in/raw/alma/members/80efaed15e278811260ab2b8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `aquantia.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-204344a961d76455faeb04c1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/phy/mscc`. Source: `D1/in/raw/alma/members/204344a961d76455faeb04c1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mscc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cd6106b4bac6865c61b17e7a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/phy/qcom`. Source: `D1/in/raw/alma/members/cd6106b4bac6865c61b17e7a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `at803x.ko.xz`, `qca808x.ko.xz`, `qca83xx.ko.xz`, `qcom-phy-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-94b4b29e0fc8977c8a4493d2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/phy/realtek`. Source: `D1/in/raw/alma/members/94b4b29e0fc8977c8a4493d2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `realtek.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0f37ab21abe415d3c6be8c2f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/ppp`. Source: `D1/in/raw/alma/members/0f37ab21abe415d3c6be8c2f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bsd_comp.ko.xz`, `ppp_async.ko.xz`, `ppp_deflate.ko.xz`, `ppp_generic.ko.xz`, `ppp_mppe.ko.xz`, `ppp_synctty.ko.xz`, `pppoe.ko.xz`, `pppox.ko.xz`, `pptp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5557d580d3d45bfd0586b9a5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/slip`. Source: `D1/in/raw/alma/members/5557d580d3d45bfd0586b9a5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `slhc.ko.xz`, `slip.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a933554e8a21e12ced13ea97

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/thunderbolt`. Source: `D1/in/raw/alma/members/a933554e8a21e12ced13ea97.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `thunderbolt_net.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-33f2e2681995f2d97cb54985

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/usb`. Source: `D1/in/raw/alma/members/33f2e2681995f2d97cb54985.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `asix.ko.xz`, `ax88179_178a.ko.xz`, `catc.ko.xz`, `cdc_eem.ko.xz`, `cdc_ether.ko.xz`, `cdc_mbim.ko.xz`, `cdc_ncm.ko.xz`, `cdc_subset.ko.xz`, `ch9200.ko.xz`, `cx82310_eth.ko.xz`, `dm9601.ko.xz`, `gl620a.ko.xz`, `hso.ko.xz`, `huawei_cdc_ncm.ko.xz`, `int51x1.ko.xz`, `ipheth.ko.xz`, `kalmia.ko.xz`, `kaweth.ko.xz`, `lan78xx.ko.xz`, `lg-vl600.ko.xz`, `mcs7830.ko.xz`, `net1080.ko.xz`, `pegasus.ko.xz`, `plusb.ko.xz`, `qmi_wwan.ko.xz`, `r8152.ko.xz`, `r8153_ecm.ko.xz`, `rndis_host.ko.xz`, `rtl8150.ko.xz`, `sierra_net.ko.xz`, `smsc75xx.ko.xz`, `smsc95xx.ko.xz`, `usbnet.ko.xz`, `zaurus.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a0634198ddb24f5bc6b5e311

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/vmxnet3`. Source: `D1/in/raw/alma/members/a0634198ddb24f5bc6b5e311.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vmxnet3.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1c64e5c4ae07dd8b115063d1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/vxlan`. Source: `D1/in/raw/alma/members/1c64e5c4ae07dd8b115063d1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vxlan.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e453f1800c9fdbe89efa8a51

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wan`. Source: `D1/in/raw/alma/members/e453f1800c9fdbe89efa8a51.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hdlc.ko.xz`, `hdlc_cisco.ko.xz`, `hdlc_fr.ko.xz`, `hdlc_ppp.ko.xz`, `hdlc_raw.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d9f6f6f1498858a54c5779da

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireguard`. Source: `D1/in/raw/alma/members/d9f6f6f1498858a54c5779da.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `wireguard.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-30b0eea01e457626636588f6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless`. Source: `D1/in/raw/alma/members/30b0eea01e457626636588f6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ath`, `broadcom`, `intel`, `marvell`, `mediatek`, `ralink`, `realtek`, `virtual`. Directory installation integrity and creation provenance are not established.
### alma-3be9cf7ae131291404a7f544

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath`. Source: `D1/in/raw/alma/members/3be9cf7ae131291404a7f544.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ath.ko.xz; UNKNOWN: ath10k,ath11k,ath12k,ath9k

- **INSTALLED-PACKAGE**: `ath.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `ath10k`, `ath11k`, `ath12k`, `ath9k`. Directory installation integrity and creation provenance are not established.
### alma-5eaadd1c05e883157d9306ec

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath/ath10k`. Source: `D1/in/raw/alma/members/5eaadd1c05e883157d9306ec.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ath10k_core.ko.xz`, `ath10k_pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bdfb1d3e294ac0db2f8eee2d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath/ath11k`. Source: `D1/in/raw/alma/members/bdfb1d3e294ac0db2f8eee2d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ath11k.ko.xz`, `ath11k_pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4fd7e57d3848c7a4c89e5bda

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath/ath12k`. Source: `D1/in/raw/alma/members/4fd7e57d3848c7a4c89e5bda.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ath12k.ko.xz; UNKNOWN: wifi7

- **INSTALLED-PACKAGE**: `ath12k.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `wifi7`. Directory installation integrity and creation provenance are not established.
### alma-9822494867999fbd700e0b71

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath/ath12k/wifi7`. Source: `D1/in/raw/alma/members/9822494867999fbd700e0b71.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ath12k_wifi7.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-85fe7faf623165f90294daad

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ath/ath9k`. Source: `D1/in/raw/alma/members/85fe7faf623165f90294daad.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ath9k.ko.xz`, `ath9k_common.ko.xz`, `ath9k_htc.ko.xz`, `ath9k_hw.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d12538a9ef572ec2d3fbe3e8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom`. Source: `D1/in/raw/alma/members/d12538a9ef572ec2d3fbe3e8.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `brcm80211`. Directory installation integrity and creation provenance are not established.
### alma-ccd62c6bd8e4c073d92f75b4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211`. Source: `D1/in/raw/alma/members/ccd62c6bd8e4c073d92f75b4.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `brcmfmac`, `brcmsmac`, `brcmutil`. Directory installation integrity and creation provenance are not established.
### alma-ad025c523d9188cc6fb5546b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac`. Source: `D1/in/raw/alma/members/ad025c523d9188cc6fb5546b.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: brcmfmac.ko.xz; UNKNOWN: bca,cyw,wcc

- **UNKNOWN**: `bca`, `cyw`, `wcc`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `brcmfmac.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-15a90835e379efe66b3cab59

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/bca`. Source: `D1/in/raw/alma/members/15a90835e379efe66b3cab59.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `brcmfmac-bca.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c37e712be039f1187a9d9a86

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/cyw`. Source: `D1/in/raw/alma/members/c37e712be039f1187a9d9a86.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `brcmfmac-cyw.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5bd0d1230301c9d25fe2d592

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/wcc`. Source: `D1/in/raw/alma/members/5bd0d1230301c9d25fe2d592.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `brcmfmac-wcc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e6d575cda1e7e4dc5452bd38

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmsmac`. Source: `D1/in/raw/alma/members/e6d575cda1e7e4dc5452bd38.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `brcmsmac.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f89238917fe48b9ab9da92eb

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/broadcom/brcm80211/brcmutil`. Source: `D1/in/raw/alma/members/f89238917fe48b9ab9da92eb.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `brcmutil.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3e882a8ac04abdccdc577efe

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/intel`. Source: `D1/in/raw/alma/members/3e882a8ac04abdccdc577efe.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `iwlwifi`. Directory installation integrity and creation provenance are not established.
### alma-b285730bc4ac4054ffe7231d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/intel/iwlwifi`. Source: `D1/in/raw/alma/members/b285730bc4ac4054ffe7231d.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: iwlwifi.ko.xz; UNKNOWN: dvm,mld,mvm,tests

- **UNKNOWN**: `dvm`, `mld`, `mvm`, `tests`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `iwlwifi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8ae6adebc14219b9040d5fbc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/intel/iwlwifi/dvm`. Source: `D1/in/raw/alma/members/8ae6adebc14219b9040d5fbc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iwldvm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c57e526e3e7d85411b47a02b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/intel/iwlwifi/mld`. Source: `D1/in/raw/alma/members/c57e526e3e7d85411b47a02b.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: iwlmld.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `iwlmld.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-32ee74924b9c4d61d24127de

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/intel/iwlwifi/mvm`. Source: `D1/in/raw/alma/members/32ee74924b9c4d61d24127de.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: iwlmvm.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `iwlmvm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-cfe837115faef1eddf661b87

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/marvell`. Source: `D1/in/raw/alma/members/cfe837115faef1eddf661b87.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mwifiex`. Directory installation integrity and creation provenance are not established.
### alma-2adf442ca781e6b57e5d8ae7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/marvell/mwifiex`. Source: `D1/in/raw/alma/members/2adf442ca781e6b57e5d8ae7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mwifiex.ko.xz`, `mwifiex_pcie.ko.xz`, `mwifiex_sdio.ko.xz`, `mwifiex_usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3c199034c9de75c55122ae65

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek`. Source: `D1/in/raw/alma/members/3c199034c9de75c55122ae65.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mt76`, `mt7601u`. Directory installation integrity and creation provenance are not established.
### alma-5b4213959c5f7b5ce6b86e01

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt76`. Source: `D1/in/raw/alma/members/5b4213959c5f7b5ce6b86e01.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mt76-connac-lib.ko.xz,mt76-usb.ko.xz,mt76.ko.xz,mt76x02-lib.ko.xz,mt76x02-usb.ko.xz,mt792x-lib.ko.xz; UNKNOWN: mt76x0,mt76x2,mt7921,mt7925

- **INSTALLED-PACKAGE**: `mt76-connac-lib.ko.xz`, `mt76-usb.ko.xz`, `mt76.ko.xz`, `mt76x02-lib.ko.xz`, `mt76x02-usb.ko.xz`, `mt792x-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `mt76x0`, `mt76x2`, `mt7921`, `mt7925`. Directory installation integrity and creation provenance are not established.
### alma-429e56f9cdcd546a37d4cb61

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt76/mt76x0`. Source: `D1/in/raw/alma/members/429e56f9cdcd546a37d4cb61.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mt76x0-common.ko.xz`, `mt76x0e.ko.xz`, `mt76x0u.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7eca70c1843af8d99ad22de6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt76/mt76x2`. Source: `D1/in/raw/alma/members/7eca70c1843af8d99ad22de6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mt76x2-common.ko.xz`, `mt76x2e.ko.xz`, `mt76x2u.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c50d96005466f8e7cf5c4a2f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt76/mt7921`. Source: `D1/in/raw/alma/members/c50d96005466f8e7cf5c4a2f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mt7921-common.ko.xz`, `mt7921e.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-48a72413b1d24b9311047c12

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt76/mt7925`. Source: `D1/in/raw/alma/members/48a72413b1d24b9311047c12.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mt7925-common.ko.xz`, `mt7925e.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-beb80298b0c94500bf97d6c4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/mediatek/mt7601u`. Source: `D1/in/raw/alma/members/beb80298b0c94500bf97d6c4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mt7601u.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b7ad4abea2dc82533366517b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ralink`. Source: `D1/in/raw/alma/members/b7ad4abea2dc82533366517b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `rt2x00`. Directory installation integrity and creation provenance are not established.
### alma-12d1dbe0026fa6f27121d1ee

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/ralink/rt2x00`. Source: `D1/in/raw/alma/members/12d1dbe0026fa6f27121d1ee.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rt2800lib.ko.xz`, `rt2800mmio.ko.xz`, `rt2800pci.ko.xz`, `rt2800usb.ko.xz`, `rt2x00lib.ko.xz`, `rt2x00mmio.ko.xz`, `rt2x00pci.ko.xz`, `rt2x00usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c83a8fdb9deb53992282ffb5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek`. Source: `D1/in/raw/alma/members/c83a8fdb9deb53992282ffb5.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `rtl8xxxu`, `rtlwifi`, `rtw88`, `rtw89`. Directory installation integrity and creation provenance are not established.
### alma-c3c381c517ccc12626744a19

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtl8xxxu`. Source: `D1/in/raw/alma/members/c3c381c517ccc12626744a19.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8xxxu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-79554bcbf3567fea26480807

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi`. Source: `D1/in/raw/alma/members/79554bcbf3567fea26480807.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: rtl_pci.ko.xz,rtl_usb.ko.xz,rtlwifi.ko.xz; UNKNOWN: btcoexist,rtl8188ee,rtl8192c,rtl8192ce,rtl8192cu,rtl8192d,rtl8192de,rtl8192ee,rtl8192se,rtl8723ae,rtl8723be,rtl8723com,rtl8821ae

- **UNKNOWN**: `btcoexist`, `rtl8188ee`, `rtl8192c`, `rtl8192ce`, `rtl8192cu`, `rtl8192d`, `rtl8192de`, `rtl8192ee`, `rtl8192se`, `rtl8723ae`, `rtl8723be`, `rtl8723com`, `rtl8821ae`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `rtl_pci.ko.xz`, `rtl_usb.ko.xz`, `rtlwifi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-306b27614fb9cff45dc717cd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/btcoexist`. Source: `D1/in/raw/alma/members/306b27614fb9cff45dc717cd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `btcoexist.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f84d931b3a3151a6d85fffb0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8188ee`. Source: `D1/in/raw/alma/members/f84d931b3a3151a6d85fffb0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8188ee.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7243c3b523683cb741e6367f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192c`. Source: `D1/in/raw/alma/members/7243c3b523683cb741e6367f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192c-common.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7f864086d9890460df56676c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192ce`. Source: `D1/in/raw/alma/members/7f864086d9890460df56676c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192ce.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-afc483f1e1cd75a2bf4a51fa

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192cu`. Source: `D1/in/raw/alma/members/afc483f1e1cd75a2bf4a51fa.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192cu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c4b259096aa0b459e47fe11d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192d`. Source: `D1/in/raw/alma/members/c4b259096aa0b459e47fe11d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192d-common.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-de6e4df83dec55660c50d5a2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192de`. Source: `D1/in/raw/alma/members/de6e4df83dec55660c50d5a2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192de.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9637a2be01e91b3f9cf67793

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192ee`. Source: `D1/in/raw/alma/members/9637a2be01e91b3f9cf67793.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192ee.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-47f7dd6c89602fbe559e26d8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192se`. Source: `D1/in/raw/alma/members/47f7dd6c89602fbe559e26d8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8192se.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-09618f7cc13553a7f7fc2b3d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8723ae`. Source: `D1/in/raw/alma/members/09618f7cc13553a7f7fc2b3d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8723ae.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c9a5c9a39e08f3bccb36b35e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8723be`. Source: `D1/in/raw/alma/members/c9a5c9a39e08f3bccb36b35e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8723be.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5d707467c5073084fed7679e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8723com`. Source: `D1/in/raw/alma/members/5d707467c5073084fed7679e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8723-common.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5a459b4c72c6ee63021e5878

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8821ae`. Source: `D1/in/raw/alma/members/5a459b4c72c6ee63021e5878.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtl8821ae.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-61f36c1c8648030e14d39285

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtw88`. Source: `D1/in/raw/alma/members/61f36c1c8648030e14d39285.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtw88_8723d.ko.xz`, `rtw88_8723de.ko.xz`, `rtw88_8723x.ko.xz`, `rtw88_8821c.ko.xz`, `rtw88_8821ce.ko.xz`, `rtw88_8822b.ko.xz`, `rtw88_8822be.ko.xz`, `rtw88_8822bu.ko.xz`, `rtw88_8822c.ko.xz`, `rtw88_8822ce.ko.xz`, `rtw88_core.ko.xz`, `rtw88_pci.ko.xz`, `rtw88_usb.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d2b66c1ee549e3f98db840ea

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wireless/realtek/rtw89`. Source: `D1/in/raw/alma/members/d2b66c1ee549e3f98db840ea.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtw89_8852a.ko.xz`, `rtw89_8852ae.ko.xz`, `rtw89_8852b.ko.xz`, `rtw89_8852b_common.ko.xz`, `rtw89_8852be.ko.xz`, `rtw89_8852c.ko.xz`, `rtw89_8852ce.ko.xz`, `rtw89_8922a.ko.xz`, `rtw89_8922ae.ko.xz`, `rtw89_core.ko.xz`, `rtw89_pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1681fe3efce2b7151985503a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wwan`. Source: `D1/in/raw/alma/members/1681fe3efce2b7151985503a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mhi_wwan_ctrl.ko.xz,mhi_wwan_mbim.ko.xz; UNKNOWN: iosm,t7xx

- **UNKNOWN**: `iosm`, `t7xx`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `mhi_wwan_ctrl.ko.xz`, `mhi_wwan_mbim.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a193c1be188f62e92e315818

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wwan/iosm`. Source: `D1/in/raw/alma/members/a193c1be188f62e92e315818.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `iosm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6284719529c9321afebfec8c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/net/wwan/t7xx`. Source: `D1/in/raw/alma/members/6284719529c9321afebfec8c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mtk_t7xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5e08070a4e03ba3d54f0797e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ntb`. Source: `D1/in/raw/alma/members/5e08070a4e03ba3d54f0797e.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ntb.ko.xz,ntb_transport.ko.xz; UNKNOWN: hw,test

- **UNKNOWN**: `hw`, `test`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `ntb.ko.xz`, `ntb_transport.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6442cc391b3b5f25bf2d09a6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ntb/hw`. Source: `D1/in/raw/alma/members/6442cc391b3b5f25bf2d09a6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `amd`, `intel`. Directory installation integrity and creation provenance are not established.
### alma-25a3397ebe014ea3f5ebf1f1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ntb/hw/amd`. Source: `D1/in/raw/alma/members/25a3397ebe014ea3f5ebf1f1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ntb_hw_amd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0b6c8dbd211c7eef5e206436

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ntb/hw/intel`. Source: `D1/in/raw/alma/members/0b6c8dbd211c7eef5e206436.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ntb_hw_intel.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-66137c7f7fb1e25b2fab0bd5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ntb/test`. Source: `D1/in/raw/alma/members/66137c7f7fb1e25b2fab0bd5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ntb_perf.ko.xz`, `ntb_pingpong.ko.xz`, `ntb_tool.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5185907144a29058aa6526c1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/nvdimm`. Source: `D1/in/raw/alma/members/5185907144a29058aa6526c1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libnvdimm.ko.xz`, `nd_e820.ko.xz`, `nd_pmem.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f00f63936651339ea3a43d8c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/nvme`. Source: `D1/in/raw/alma/members/f00f63936651339ea3a43d8c.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `common`, `host`, `target`. Directory installation integrity and creation provenance are not established.
### alma-378592a375ad3cddbf46404b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/nvme/common`. Source: `D1/in/raw/alma/members/378592a375ad3cddbf46404b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nvme-auth.ko.xz`, `nvme-keyring.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f00a3c7e6993869d883c4a63

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/nvme/host`. Source: `D1/in/raw/alma/members/f00a3c7e6993869d883c4a63.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nvme-core.ko.xz`, `nvme-fabrics.ko.xz`, `nvme-fc.ko.xz`, `nvme-rdma.ko.xz`, `nvme-tcp.ko.xz`, `nvme.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-29101e369c1733061556700e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/nvme/target`. Source: `D1/in/raw/alma/members/29101e369c1733061556700e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nvme-fcloop.ko.xz`, `nvme-loop.ko.xz`, `nvmet-fc.ko.xz`, `nvmet-rdma.ko.xz`, `nvmet-tcp.ko.xz`, `nvmet.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9a2fd568327535bb5e0a9f92

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/parport`. Source: `D1/in/raw/alma/members/9a2fd568327535bb5e0a9f92.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `parport.ko.xz`, `parport_pc.ko.xz`, `parport_serial.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c87aa5a21b7a3ed018392288

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pci`. Source: `D1/in/raw/alma/members/c87aa5a21b7a3ed018392288.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: pci-pf-stub.ko.xz; UNKNOWN: controller,hotplug,pcie

- **UNKNOWN**: `controller`, `hotplug`, `pcie`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `pci-pf-stub.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d0a749b9df5aadbd298a0f01

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pci/controller`. Source: `D1/in/raw/alma/members/d0a749b9df5aadbd298a0f01.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pci-hyperv-intf.ko.xz`, `pci-hyperv.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c66a275b65e582159dcd3115

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pci/hotplug`. Source: `D1/in/raw/alma/members/c66a275b65e582159dcd3115.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `acpiphp_ibm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7d0f0c15d542557acfd27af2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pci/pcie`. Source: `D1/in/raw/alma/members/7d0f0c15d542557acfd27af2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `aer_inject.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0002fcb57cae52983ce0ac39

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/perf`. Source: `D1/in/raw/alma/members/0002fcb57cae52983ce0ac39.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxl_pmu.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5f3abe1e603942de7b2f7bbc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pinctrl`. Source: `D1/in/raw/alma/members/5f3abe1e603942de7b2f7bbc.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: pinctrl-amdisp.ko.xz; UNKNOWN: cirrus,intel

- **UNKNOWN**: `cirrus`, `intel`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `pinctrl-amdisp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f3d65bb937017f0225f8d180

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pinctrl/cirrus`. Source: `D1/in/raw/alma/members/f3d65bb937017f0225f8d180.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pinctrl-cs42l43.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4e00d4b94bc915382957381a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pinctrl/intel`. Source: `D1/in/raw/alma/members/4e00d4b94bc915382957381a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pinctrl-alderlake.ko.xz`, `pinctrl-broxton.ko.xz`, `pinctrl-cannonlake.ko.xz`, `pinctrl-cedarfork.ko.xz`, `pinctrl-denverton.ko.xz`, `pinctrl-elkhartlake.ko.xz`, `pinctrl-emmitsburg.ko.xz`, `pinctrl-geminilake.ko.xz`, `pinctrl-icelake.ko.xz`, `pinctrl-intel-platform.ko.xz`, `pinctrl-jasperlake.ko.xz`, `pinctrl-lakefield.ko.xz`, `pinctrl-lewisburg.ko.xz`, `pinctrl-meteorlake.ko.xz`, `pinctrl-meteorpoint.ko.xz`, `pinctrl-sunrisepoint.ko.xz`, `pinctrl-tigerlake.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-789732b21ce2a7f1f6a05653

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform`. Source: `D1/in/raw/alma/members/789732b21ce2a7f1f6a05653.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `mellanox`, `x86`. Directory installation integrity and creation provenance are not established.
### alma-ed5fa1cc46586a1022907f43

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/mellanox`. Source: `D1/in/raw/alma/members/ed5fa1cc46586a1022907f43.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlxreg-hotplug.ko.xz`, `mlxreg-io.ko.xz`, `nvsw-sn2201.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cd4a06e2e63eb02b772d7c9f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86`. Source: `D1/in/raw/alma/members/cd4a06e2e63eb02b772d7c9f.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: acer-wireless.ko.xz,acer-wmi.ko.xz,amilo-rfkill.ko.xz,apple-gmux.ko.xz,asus-laptop.ko.xz,asus-nb-wmi.ko.xz,asus-wmi.ko.xz,compal-laptop.ko.xz,eeepc-laptop.ko.xz,eeepc-wmi.ko.xz,firmware_attributes_class.ko.xz,fujitsu-laptop.ko.xz,fujitsu-tablet.ko.xz,hdaps.ko.xz,ideapad-laptop.ko.xz,intel_ips.ko.xz,mlx-platform.ko.xz,msi-laptop.ko.xz,msi-wmi.ko.xz,mxm-wmi.ko.xz,nvidia-wmi-ec-backlight.ko.xz,panasonic-laptop.ko.xz,samsung-laptop.ko.xz,samsung-q10.ko.xz,serial-multi-instantiate.ko.xz,sony-laptop.ko.xz,think-lmi.ko.xz,thinkpad_acpi.ko.xz,topstar-laptop.ko.xz,toshiba_bluetooth.ko.xz,uv_sysfs.ko.xz,wireless-hotkey.ko.xz,wmi-bmof.ko.xz,wmi.ko.xz; UNKNOWN: amd,dell,intel

- **INSTALLED-PACKAGE**: `acer-wireless.ko.xz`, `acer-wmi.ko.xz`, `amilo-rfkill.ko.xz`, `apple-gmux.ko.xz`, `asus-laptop.ko.xz`, `asus-nb-wmi.ko.xz`, `asus-wmi.ko.xz`, `compal-laptop.ko.xz`, `eeepc-laptop.ko.xz`, `eeepc-wmi.ko.xz`, `firmware_attributes_class.ko.xz`, `fujitsu-laptop.ko.xz`, `fujitsu-tablet.ko.xz`, `hdaps.ko.xz`, `ideapad-laptop.ko.xz`, `intel_ips.ko.xz`, `mlx-platform.ko.xz`, `msi-laptop.ko.xz`, `msi-wmi.ko.xz`, `mxm-wmi.ko.xz`, `nvidia-wmi-ec-backlight.ko.xz`, `panasonic-laptop.ko.xz`, `samsung-laptop.ko.xz`, `samsung-q10.ko.xz`, `serial-multi-instantiate.ko.xz`, `sony-laptop.ko.xz`, `think-lmi.ko.xz`, `thinkpad_acpi.ko.xz`, `topstar-laptop.ko.xz`, `toshiba_bluetooth.ko.xz`, `uv_sysfs.ko.xz`, `wireless-hotkey.ko.xz`, `wmi-bmof.ko.xz`, `wmi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `amd`, `dell`, `intel`. Directory installation integrity and creation provenance are not established.
### alma-f5450c61b69b0223ea41fa6c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/amd`. Source: `D1/in/raw/alma/members/f5450c61b69b0223ea41fa6c.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: amd_3d_vcache.ko.xz,amd_isp4.ko.xz; UNKNOWN: hsmp,pmc,pmf

- **INSTALLED-PACKAGE**: `amd_3d_vcache.ko.xz`, `amd_isp4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `hsmp`, `pmc`, `pmf`. Directory installation integrity and creation provenance are not established.
### alma-e7e3de9c3f29b50037d310a7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/amd/hsmp`. Source: `D1/in/raw/alma/members/e7e3de9c3f29b50037d310a7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd_hsmp.ko.xz`, `hsmp_acpi.ko.xz`, `hsmp_common.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9229e58bf6e64fae1d092638

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/amd/pmc`. Source: `D1/in/raw/alma/members/9229e58bf6e64fae1d092638.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd-pmc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5402be78fdd6a8d46f44b49a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/amd/pmf`. Source: `D1/in/raw/alma/members/5402be78fdd6a8d46f44b49a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd-pmf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d91d92fca7d1211cbcaa2542

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/dell`. Source: `D1/in/raw/alma/members/d91d92fca7d1211cbcaa2542.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: dcdbas.ko.xz,dell-laptop.ko.xz,dell-lis3lv02d.ko.xz,dell-pc.ko.xz,dell-rbtn.ko.xz,dell-smbios.ko.xz,dell-smo8800.ko.xz,dell-wmi-aio.ko.xz,dell-wmi-ddv.ko.xz,dell-wmi-descriptor.ko.xz,dell-wmi-led.ko.xz,dell-wmi.ko.xz; UNKNOWN: dell-wmi-sysman

- **INSTALLED-PACKAGE**: `dcdbas.ko.xz`, `dell-laptop.ko.xz`, `dell-lis3lv02d.ko.xz`, `dell-pc.ko.xz`, `dell-rbtn.ko.xz`, `dell-smbios.ko.xz`, `dell-smo8800.ko.xz`, `dell-wmi-aio.ko.xz`, `dell-wmi-ddv.ko.xz`, `dell-wmi-descriptor.ko.xz`, `dell-wmi-led.ko.xz`, `dell-wmi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `dell-wmi-sysman`. Directory installation integrity and creation provenance are not established.
### alma-4613a5495334c5c10b6514a1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/dell/dell-wmi-sysman`. Source: `D1/in/raw/alma/members/4613a5495334c5c10b6514a1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dell-wmi-sysman.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cb8a9fdb5ceecaeca6f9c59c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel`. Source: `D1/in/raw/alma/members/cb8a9fdb5ceecaeca6f9c59c.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: intel-hid.ko.xz,intel-ishtp_eclite.ko.xz,intel-oaktrail.ko.xz,intel-rst.ko.xz,intel-sdsi.ko.xz,intel-tpmi_power_domains.ko.xz,intel-vbtn.ko.xz,intel-vsec.ko.xz,intel-vsec_tpmi.ko.xz; UNKNOWN: ifs,int3472,pmc,pmt,speed_select_if,uncore-frequency,wmi

- **UNKNOWN**: `ifs`, `int3472`, `pmc`, `pmt`, `speed_select_if`, `uncore-frequency`, `wmi`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `intel-hid.ko.xz`, `intel-ishtp_eclite.ko.xz`, `intel-oaktrail.ko.xz`, `intel-rst.ko.xz`, `intel-sdsi.ko.xz`, `intel-tpmi_power_domains.ko.xz`, `intel-vbtn.ko.xz`, `intel-vsec.ko.xz`, `intel-vsec_tpmi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f8eeeab19a0a6dee8eaad74c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/ifs`. Source: `D1/in/raw/alma/members/f8eeeab19a0a6dee8eaad74c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_ifs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-adcd6702b6cbc7d4117364c9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/int3472`. Source: `D1/in/raw/alma/members/adcd6702b6cbc7d4117364c9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_skl_int3472_common.ko.xz`, `intel_skl_int3472_discrete.ko.xz`, `intel_skl_int3472_tps68470.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6445e96dd324fa98aa08a7db

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/pmc`. Source: `D1/in/raw/alma/members/6445e96dd324fa98aa08a7db.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_pmc_core.ko.xz`, `intel_pmc_core_pltdrv.ko.xz`, `intel_pmc_ssram_telemetry.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-baed447fce7dd1b8d32e23ed

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/pmt`. Source: `D1/in/raw/alma/members/baed447fce7dd1b8d32e23ed.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pmt_class.ko.xz`, `pmt_crashlog.ko.xz`, `pmt_discovery.ko.xz`, `pmt_telemetry.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-06413416e5ff43eb221b522e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/speed_select_if`. Source: `D1/in/raw/alma/members/06413416e5ff43eb221b522e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `isst_if_common.ko.xz`, `isst_if_mbox_msr.ko.xz`, `isst_if_mbox_pci.ko.xz`, `isst_if_mmio.ko.xz`, `isst_tpmi.ko.xz`, `isst_tpmi_core.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2e2af1cd96e7d17ede5c3ee0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/uncore-frequency`. Source: `D1/in/raw/alma/members/2e2af1cd96e7d17ede5c3ee0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-uncore-frequency-common.ko.xz`, `intel-uncore-frequency-tpmi.ko.xz`, `intel-uncore-frequency.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-649455fdadf5455bed125f20

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/platform/x86/intel/wmi`. Source: `D1/in/raw/alma/members/649455fdadf5455bed125f20.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-wmi-thunderbolt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-798219b1f724eddfe4b76258

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/power`. Source: `D1/in/raw/alma/members/798219b1f724eddfe4b76258.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `supply`. Directory installation integrity and creation provenance are not established.
### alma-ec3399f079bcf41c1fd745ef

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/power/supply`. Source: `D1/in/raw/alma/members/ec3399f079bcf41c1fd745ef.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `smb347-charger.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-137ccbe1dfe7a5806de5e8a5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/powercap`. Source: `D1/in/raw/alma/members/137ccbe1dfe7a5806de5e8a5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel_rapl_common.ko.xz`, `intel_rapl_msr.ko.xz`, `intel_rapl_tpmi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4115958402fba54607834cf2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pps`. Source: `D1/in/raw/alma/members/4115958402fba54607834cf2.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `clients`. Directory installation integrity and creation provenance are not established.
### alma-6df89414df6227399f6ede4a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pps/clients`. Source: `D1/in/raw/alma/members/6df89414df6227399f6ede4a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pps-gpio.ko.xz`, `pps-ldisc.ko.xz`, `pps_parport.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0a39e00287e5533556fd11ed

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ptp`. Source: `D1/in/raw/alma/members/0a39e00287e5533556fd11ed.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ptp_kvm.ko.xz`, `ptp_vmw.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cfb407226d4985ae36efdbc9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/pwm`. Source: `D1/in/raw/alma/members/cfb407226d4985ae36efdbc9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `pwm-lpss-pci.ko.xz`, `pwm-lpss-platform.ko.xz`, `pwm-lpss.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-daf21b8ef38857f3ad3bd1b2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ras`. Source: `D1/in/raw/alma/members/daf21b8ef38857f3ad3bd1b2.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `amd`. Directory installation integrity and creation provenance are not established.
### alma-166c32b101dd230f6c80294d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ras/amd`. Source: `D1/in/raw/alma/members/166c32b101dd230f6c80294d.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: fmpm.ko.xz; UNKNOWN: atl

- **UNKNOWN**: `atl`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `fmpm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-78c9ec8f6b5f28f4896e1836

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/ras/amd/atl`. Source: `D1/in/raw/alma/members/78c9ec8f6b5f28f4896e1836.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amd_atl.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0863cf35e9acf9b8e9c192fc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/regulator`. Source: `D1/in/raw/alma/members/0863cf35e9acf9b8e9c192fc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fixed.ko.xz`, `tps68470-regulator.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2821642a5edb59bff25e15af

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/rtc`. Source: `D1/in/raw/alma/members/2821642a5edb59bff25e15af.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rtc-bq32k.ko.xz`, `rtc-ds1286.ko.xz`, `rtc-ds1307.ko.xz`, `rtc-ds1374.ko.xz`, `rtc-ds1511.ko.xz`, `rtc-ds1553.ko.xz`, `rtc-ds1672.ko.xz`, `rtc-ds1742.ko.xz`, `rtc-ds2404.ko.xz`, `rtc-ds3232.ko.xz`, `rtc-em3027.ko.xz`, `rtc-fm3130.ko.xz`, `rtc-isl12022.ko.xz`, `rtc-isl1208.ko.xz`, `rtc-m41t80.ko.xz`, `rtc-m48t35.ko.xz`, `rtc-m48t59.ko.xz`, `rtc-max6900.ko.xz`, `rtc-msm6242.ko.xz`, `rtc-pcf8523.ko.xz`, `rtc-pcf8563.ko.xz`, `rtc-pcf8583.ko.xz`, `rtc-rp5c01.ko.xz`, `rtc-rs5c372.ko.xz`, `rtc-rv3029c2.ko.xz`, `rtc-rv8803.ko.xz`, `rtc-rx4581.ko.xz`, `rtc-rx8025.ko.xz`, `rtc-rx8581.ko.xz`, `rtc-stk17ta8.ko.xz`, `rtc-x1205.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-96843c23641bde36c657f169

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi`. Source: `D1/in/raw/alma/members/96843c23641bde36c657f169.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ch.ko.xz,hpsa.ko.xz,hv_storvsc.ko.xz,iscsi_boot_sysfs.ko.xz,iscsi_tcp.ko.xz,libiscsi.ko.xz,libiscsi_tcp.ko.xz,raid_class.ko.xz,scsi_debug.ko.xz,scsi_transport_fc.ko.xz,scsi_transport_iscsi.ko.xz,scsi_transport_sas.ko.xz,scsi_transport_spi.ko.xz,scsi_transport_srp.ko.xz,sd_mod.ko.xz,ses.ko.xz,sg.ko.xz,sr_mod.ko.xz,st.ko.xz,virtio_scsi.ko.xz,vmw_pvscsi.ko.xz; UNKNOWN: aacraid,be2iscsi,bnx2fc,bnx2i,csiostor,cxgbi,fcoe,fnic,libfc,libsas,lpfc,megaraid,mpi3mr,mpt3sas,qedf,qedi,qla2xxx,smartpqi

- **UNKNOWN**: `aacraid`, `be2iscsi`, `bnx2fc`, `bnx2i`, `csiostor`, `cxgbi`, `fcoe`, `fnic`, `libfc`, `libsas`, `lpfc`, `megaraid`, `mpi3mr`, `mpt3sas`, `qedf`, `qedi`, `qla2xxx`, `smartpqi`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `ch.ko.xz`, `hpsa.ko.xz`, `hv_storvsc.ko.xz`, `iscsi_boot_sysfs.ko.xz`, `iscsi_tcp.ko.xz`, `libiscsi.ko.xz`, `libiscsi_tcp.ko.xz`, `raid_class.ko.xz`, `scsi_debug.ko.xz`, `scsi_transport_fc.ko.xz`, `scsi_transport_iscsi.ko.xz`, `scsi_transport_sas.ko.xz`, `scsi_transport_spi.ko.xz`, `scsi_transport_srp.ko.xz`, `sd_mod.ko.xz`, `ses.ko.xz`, `sg.ko.xz`, `sr_mod.ko.xz`, `st.ko.xz`, `virtio_scsi.ko.xz`, `vmw_pvscsi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1f0507dc17a86fff33aaefb8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/aacraid`. Source: `D1/in/raw/alma/members/1f0507dc17a86fff33aaefb8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `aacraid.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7beacd2232a65ca81c723e16

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/be2iscsi`. Source: `D1/in/raw/alma/members/7beacd2232a65ca81c723e16.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `be2iscsi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-95b11b4011912b790fa7fa5e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/bnx2fc`. Source: `D1/in/raw/alma/members/95b11b4011912b790fa7fa5e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnx2fc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-db3d1f267cce30e53eed4ca1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/bnx2i`. Source: `D1/in/raw/alma/members/db3d1f267cce30e53eed4ca1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnx2i.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5be068306ffd78eb4cb14dbd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/csiostor`. Source: `D1/in/raw/alma/members/5be068306ffd78eb4cb14dbd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `csiostor.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-11f0fd3ccc50ab26f319d63d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/cxgbi`. Source: `D1/in/raw/alma/members/11f0fd3ccc50ab26f319d63d.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: libcxgbi.ko.xz; UNKNOWN: cxgb4i

- **UNKNOWN**: `cxgb4i`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `libcxgbi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aad2e84439e7d49d6fe07058

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/cxgbi/cxgb4i`. Source: `D1/in/raw/alma/members/aad2e84439e7d49d6fe07058.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxgb4i.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7c6b540c6535902041c24362

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/fcoe`. Source: `D1/in/raw/alma/members/7c6b540c6535902041c24362.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libfcoe.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b5b883b6b17909dce9e982b8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/fnic`. Source: `D1/in/raw/alma/members/b5b883b6b17909dce9e982b8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fnic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d91982e8d1ad81165c856b89

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/libfc`. Source: `D1/in/raw/alma/members/d91982e8d1ad81165c856b89.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libfc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c3cc3774797a0538c5104e3b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/libsas`. Source: `D1/in/raw/alma/members/c3cc3774797a0538c5104e3b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libsas.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-042abff286d1b88c19d267d5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/lpfc`. Source: `D1/in/raw/alma/members/042abff286d1b88c19d267d5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `lpfc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-001b79758c86137b99b995d8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/megaraid`. Source: `D1/in/raw/alma/members/001b79758c86137b99b995d8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `megaraid_sas.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9d505e0f8d6f2e69d5097427

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/mpi3mr`. Source: `D1/in/raw/alma/members/9d505e0f8d6f2e69d5097427.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mpi3mr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-04cb22f01964553fe20c2372

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/mpt3sas`. Source: `D1/in/raw/alma/members/04cb22f01964553fe20c2372.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mpt3sas.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e3ff91902c14b46600daee45

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/qedf`. Source: `D1/in/raw/alma/members/e3ff91902c14b46600daee45.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qedf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2a28c8dcdf2de35f6abaf272

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/qedi`. Source: `D1/in/raw/alma/members/2a28c8dcdf2de35f6abaf272.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qedi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c34b321c1da3d163eef281b8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/qla2xxx`. Source: `D1/in/raw/alma/members/c34b321c1da3d163eef281b8.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qla2xxx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c330f7d84f54ac93fe551a43

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/scsi/smartpqi`. Source: `D1/in/raw/alma/members/c330f7d84f54ac93fe551a43.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `smartpqi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6bc9a57cf2bcd85cf8632729

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/soc`. Source: `D1/in/raw/alma/members/6bc9a57cf2bcd85cf8632729.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `qcom`. Directory installation integrity and creation provenance are not established.
### alma-23454853abc8ac867343036a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/soc/qcom`. Source: `D1/in/raw/alma/members/23454853abc8ac867343036a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qmi_helpers.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-24e23bbcab572329ee2a60b7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/soundwire`. Source: `D1/in/raw/alma/members/24e23bbcab572329ee2a60b7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `soundwire-amd.ko.xz`, `soundwire-bus.ko.xz`, `soundwire-cadence.ko.xz`, `soundwire-generic-allocation.ko.xz`, `soundwire-intel.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bae1668a81774613d1f5c6c2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/spi`. Source: `D1/in/raw/alma/members/bae1668a81774613d1f5c6c2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `spi-cs42l43.ko.xz`, `spi-ljca.ko.xz`, `spi-pxa2xx-core.ko.xz`, `spi-pxa2xx-pci.ko.xz`, `spi-pxa2xx-platform.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-02f60611ae027e99df6d9c0b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/target`. Source: `D1/in/raw/alma/members/02f60611ae027e99df6d9c0b.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: target_core_file.ko.xz,target_core_iblock.ko.xz,target_core_mod.ko.xz,target_core_pscsi.ko.xz,target_core_user.ko.xz; UNKNOWN: iscsi,loopback,tcm_fc

- **UNKNOWN**: `iscsi`, `loopback`, `tcm_fc`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `target_core_file.ko.xz`, `target_core_iblock.ko.xz`, `target_core_mod.ko.xz`, `target_core_pscsi.ko.xz`, `target_core_user.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8a6659c9c183312c78bc52f3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/target/iscsi`. Source: `D1/in/raw/alma/members/8a6659c9c183312c78bc52f3.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: iscsi_target_mod.ko.xz; UNKNOWN: cxgbit

- **UNKNOWN**: `cxgbit`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `iscsi_target_mod.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c03593a2e318ed432a0a1ed0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/target/iscsi/cxgbit`. Source: `D1/in/raw/alma/members/c03593a2e318ed432a0a1ed0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cxgbit.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-665383210eac771e0d3bdda7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/target/loopback`. Source: `D1/in/raw/alma/members/665383210eac771e0d3bdda7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tcm_loop.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dccc19d8ff2b3a9eca13cfa5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/target/tcm_fc`. Source: `D1/in/raw/alma/members/dccc19d8ff2b3a9eca13cfa5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tcm_fc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0d846b6ac8e529a4bd285f6e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tee`. Source: `D1/in/raw/alma/members/0d846b6ac8e529a4bd285f6e.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: tee.ko.xz; UNKNOWN: amdtee

- **UNKNOWN**: `amdtee`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `tee.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-910f09752ae98120ee543eb4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tee/amdtee`. Source: `D1/in/raw/alma/members/910f09752ae98120ee543eb4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `amdtee.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7058faccbaff3704af81621a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/thermal`. Source: `D1/in/raw/alma/members/7058faccbaff3704af81621a.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `intel`. Directory installation integrity and creation provenance are not established.
### alma-4f006edea571d779f2e109a6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/thermal/intel`. Source: `D1/in/raw/alma/members/4f006edea571d779f2e109a6.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: intel_pch_thermal.ko.xz,intel_powerclamp.ko.xz,intel_soc_dts_iosf.ko.xz,intel_tcc_cooling.ko.xz,x86_pkg_temp_thermal.ko.xz; UNKNOWN: int340x_thermal

- **UNKNOWN**: `int340x_thermal`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `intel_pch_thermal.ko.xz`, `intel_powerclamp.ko.xz`, `intel_soc_dts_iosf.ko.xz`, `intel_tcc_cooling.ko.xz`, `x86_pkg_temp_thermal.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2acf81f7d9d2f01c0b2b4036

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/thermal/intel/int340x_thermal`. Source: `D1/in/raw/alma/members/2acf81f7d9d2f01c0b2b4036.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `acpi_thermal_rel.ko.xz`, `int3400_thermal.ko.xz`, `int3401_thermal.ko.xz`, `int3402_thermal.ko.xz`, `int3403_thermal.ko.xz`, `int340x_thermal_zone.ko.xz`, `platform_temperature_control.ko.xz`, `processor_thermal_device.ko.xz`, `processor_thermal_device_pci.ko.xz`, `processor_thermal_device_pci_legacy.ko.xz`, `processor_thermal_mbox.ko.xz`, `processor_thermal_power_floor.ko.xz`, `processor_thermal_rapl.ko.xz`, `processor_thermal_rfim.ko.xz`, `processor_thermal_soc_slider.ko.xz`, `processor_thermal_wt_hint.ko.xz`, `processor_thermal_wt_req.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7b9188c3d7e47d75fb9b1997

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tty`. Source: `D1/in/raw/alma/members/7b9188c3d7e47d75fb9b1997.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: n_hdlc.ko.xz,nozomi.ko.xz; UNKNOWN: serial

- **INSTALLED-PACKAGE**: `n_hdlc.ko.xz`, `nozomi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `serial`. Directory installation integrity and creation provenance are not established.
### alma-ec9c241e8438bc1d56a6d8a9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tty/serial`. Source: `D1/in/raw/alma/members/ec9c241e8438bc1d56a6d8a9.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: arc_uart.ko.xz; UNKNOWN: 8250,jsm

- **UNKNOWN**: `8250`, `jsm`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `arc_uart.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e0757ccfed675c811e88000d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tty/serial/8250`. Source: `D1/in/raw/alma/members/e0757ccfed675c811e88000d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `8250_lpss.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-14383d78255ac873aacb75ae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/tty/serial/jsm`. Source: `D1/in/raw/alma/members/14383d78255ac873aacb75ae.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `jsm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-17fd4dfc3ca96750e8510b89

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/uio`. Source: `D1/in/raw/alma/members/17fd4dfc3ca96750e8510b89.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `uio.ko.xz`, `uio_hv_generic.ko.xz`, `uio_pci_generic.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-eb528e5a4e71ed4eef15d720

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb`. Source: `D1/in/raw/alma/members/eb528e5a4e71ed4eef15d720.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `class`, `core`, `image`, `misc`, `roles`, `serial`, `storage`, `typec`, `usbip`. Directory installation integrity and creation provenance are not established.
### alma-0f3898b7cf8eea0341479396

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/class`. Source: `D1/in/raw/alma/members/0f3898b7cf8eea0341479396.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cdc-acm.ko.xz`, `cdc-wdm.ko.xz`, `usblp.ko.xz`, `usbtmc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-04964e62a6b9e0e68cf51ba4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/core`. Source: `D1/in/raw/alma/members/04964e62a6b9e0e68cf51ba4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ledtrig-usbport.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ef468b5b5cd920ab58000752

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/image`. Source: `D1/in/raw/alma/members/ef468b5b5cd920ab58000752.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mdc800.ko.xz`, `microtek.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5dfbadad9c3bd77f076fa86e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/misc`. Source: `D1/in/raw/alma/members/5dfbadad9c3bd77f076fa86e.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: adutux.ko.xz,appledisplay.ko.xz,emi26.ko.xz,emi62.ko.xz,ezusb.ko.xz,idmouse.ko.xz,iowarrior.ko.xz,isight_firmware.ko.xz,ldusb.ko.xz,legousbtower.ko.xz,usb-ljca.ko.xz,usb3503.ko.xz,usbio.ko.xz,usblcd.ko.xz,usbsevseg.ko.xz,uss720.ko.xz; UNKNOWN: sisusbvga

- **INSTALLED-PACKAGE**: `adutux.ko.xz`, `appledisplay.ko.xz`, `emi26.ko.xz`, `emi62.ko.xz`, `ezusb.ko.xz`, `idmouse.ko.xz`, `iowarrior.ko.xz`, `isight_firmware.ko.xz`, `ldusb.ko.xz`, `legousbtower.ko.xz`, `usb-ljca.ko.xz`, `usb3503.ko.xz`, `usbio.ko.xz`, `usblcd.ko.xz`, `usbsevseg.ko.xz`, `uss720.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `sisusbvga`. Directory installation integrity and creation provenance are not established.
### alma-c3a0138a39cb49eb3e5bed92

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/misc/sisusbvga`. Source: `D1/in/raw/alma/members/c3a0138a39cb49eb3e5bed92.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `sisusbvga.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0291fe4899a1c0832d3226a0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/roles`. Source: `D1/in/raw/alma/members/0291fe4899a1c0832d3226a0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `intel-xhci-usb-role-switch.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2529497dc8bd854bf4e240f2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/serial`. Source: `D1/in/raw/alma/members/2529497dc8bd854bf4e240f2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `aircable.ko.xz`, `ark3116.ko.xz`, `belkin_sa.ko.xz`, `ch341.ko.xz`, `cp210x.ko.xz`, `cyberjack.ko.xz`, `cypress_m8.ko.xz`, `digi_acceleport.ko.xz`, `empeg.ko.xz`, `f81534.ko.xz`, `ftdi_sio.ko.xz`, `garmin_gps.ko.xz`, `io_edgeport.ko.xz`, `io_ti.ko.xz`, `ipaq.ko.xz`, `ipw.ko.xz`, `ir-usb.ko.xz`, `iuu_phoenix.ko.xz`, `keyspan.ko.xz`, `keyspan_pda.ko.xz`, `kl5kusb105.ko.xz`, `kobil_sct.ko.xz`, `mct_u232.ko.xz`, `mos7720.ko.xz`, `mos7840.ko.xz`, `mxuport.ko.xz`, `navman.ko.xz`, `omninet.ko.xz`, `opticon.ko.xz`, `option.ko.xz`, `oti6858.ko.xz`, `pl2303.ko.xz`, `qcaux.ko.xz`, `qcserial.ko.xz`, `quatech2.ko.xz`, `safe_serial.ko.xz`, `sierra.ko.xz`, `spcp8x5.ko.xz`, `ssu100.ko.xz`, `symbolserial.ko.xz`, `ti_usb_3410_5052.ko.xz`, `upd78f0730.ko.xz`, `usb_debug.ko.xz`, `usb_wwan.ko.xz`, `visor.ko.xz`, `whiteheat.ko.xz`, `xr_serial.ko.xz`, `xsens_mt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-748259a3099010dc2f11a120

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/storage`. Source: `D1/in/raw/alma/members/748259a3099010dc2f11a120.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `uas.ko.xz`, `ums-alauda.ko.xz`, `ums-cypress.ko.xz`, `ums-datafab.ko.xz`, `ums-eneub6250.ko.xz`, `ums-freecom.ko.xz`, `ums-isd200.ko.xz`, `ums-jumpshot.ko.xz`, `ums-karma.ko.xz`, `ums-onetouch.ko.xz`, `ums-realtek.ko.xz`, `ums-sddr09.ko.xz`, `ums-sddr55.ko.xz`, `ums-usbat.ko.xz`, `usb-storage.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d7dfa93cdcba2cf34d6113b8

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/typec`. Source: `D1/in/raw/alma/members/d7dfa93cdcba2cf34d6113b8.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `altmodes`, `mux`, `tcpm`, `tipd`. Directory installation integrity and creation provenance are not established.
### alma-f566d60e986ceaadf15e778b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/typec/altmodes`. Source: `D1/in/raw/alma/members/f566d60e986ceaadf15e778b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `typec_displayport.ko.xz`, `typec_thunderbolt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4834f327863f488c9aeba5ae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/typec/mux`. Source: `D1/in/raw/alma/members/4834f327863f488c9aeba5ae.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fsa4480.ko.xz`, `pi3usb30532.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9a8fecadfeb44c1b865bde63

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/typec/tcpm`. Source: `D1/in/raw/alma/members/9a8fecadfeb44c1b865bde63.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fusb302.ko.xz`, `tcpci.ko.xz`, `tcpm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0eac7cbe348ee21ceb3866cf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/usb/typec/tipd`. Source: `D1/in/raw/alma/members/0eac7cbe348ee21ceb3866cf.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tps6598x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2746ee477fa3dab4ccffd839

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa`. Source: `D1/in/raw/alma/members/2746ee477fa3dab4ccffd839.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: vdpa.ko.xz; UNKNOWN: ifcvf,mlx5,vdpa_sim,vdpa_user,virtio_pci

- **UNKNOWN**: `ifcvf`, `mlx5`, `vdpa_sim`, `vdpa_user`, `virtio_pci`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `vdpa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e4b662cea8a18554847c5b6f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa/ifcvf`. Source: `D1/in/raw/alma/members/e4b662cea8a18554847c5b6f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ifcvf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-19f879a32936e4772e9c00f7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa/mlx5`. Source: `D1/in/raw/alma/members/19f879a32936e4772e9c00f7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx5_vdpa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9ff4e0770d5260daa49f5f92

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa/vdpa_sim`. Source: `D1/in/raw/alma/members/9ff4e0770d5260daa49f5f92.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vdpa_sim.ko.xz`, `vdpa_sim_blk.ko.xz`, `vdpa_sim_net.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f79710549be47e370742846a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa/vdpa_user`. Source: `D1/in/raw/alma/members/f79710549be47e370742846a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vduse.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3597f774a87d5fadb3697b5b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vdpa/virtio_pci`. Source: `D1/in/raw/alma/members/3597f774a87d5fadb3697b5b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vp_vdpa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dbea6d3a9bef22576a11a43f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vfio`. Source: `D1/in/raw/alma/members/dbea6d3a9bef22576a11a43f.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: vfio.ko.xz,vfio_iommu_type1.ko.xz; UNKNOWN: mdev,pci

- **UNKNOWN**: `mdev`, `pci`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `vfio.ko.xz`, `vfio_iommu_type1.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b8d9a9dce9880f95bf24fce9

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vfio/mdev`. Source: `D1/in/raw/alma/members/b8d9a9dce9880f95bf24fce9.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mdev.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6b86a53da6970e431f7c2c41

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vfio/pci`. Source: `D1/in/raw/alma/members/6b86a53da6970e431f7c2c41.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: vfio-pci-core.ko.xz,vfio-pci.ko.xz; UNKNOWN: mlx5

- **UNKNOWN**: `mlx5`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `vfio-pci-core.ko.xz`, `vfio-pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-75df2f873d2fe92cc76e1a5e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vfio/pci/mlx5`. Source: `D1/in/raw/alma/members/75df2f873d2fe92cc76e1a5e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mlx5-vfio-pci.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ba1c2ea7ce66bb9d6a9f452e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/vhost`. Source: `D1/in/raw/alma/members/ba1c2ea7ce66bb9d6a9f452e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vhost.ko.xz`, `vhost_iotlb.ko.xz`, `vhost_net.ko.xz`, `vhost_vdpa.ko.xz`, `vhost_vsock.ko.xz`, `vringh.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-40f334e92c48707117cebb38

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/video`. Source: `D1/in/raw/alma/members/40f334e92c48707117cebb38.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `backlight`. Directory installation integrity and creation provenance are not established.
### alma-95f8a33e04fc129451ebe33d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/video/backlight`. Source: `D1/in/raw/alma/members/95f8a33e04fc129451ebe33d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `apple_bl.ko.xz`, `lcd.ko.xz`, `lp855x_bl.ko.xz`, `platform_lcd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-eb3201ff00aab9fe82ebaf1b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt`. Source: `D1/in/raw/alma/members/eb3201ff00aab9fe82ebaf1b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `coco`, `nitro_enclaves`. Directory installation integrity and creation provenance are not established.
### alma-6194bfbe15a6704867fcbb96

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt/coco`. Source: `D1/in/raw/alma/members/6194bfbe15a6704867fcbb96.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: tsm.ko.xz; UNKNOWN: efi_secret,sev-guest,tdx-guest

- **UNKNOWN**: `efi_secret`, `sev-guest`, `tdx-guest`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `tsm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-48f0cd364b67fdeba4825b67

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt/coco/efi_secret`. Source: `D1/in/raw/alma/members/48f0cd364b67fdeba4825b67.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `efi_secret.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f890639b91af7e6f949b8b99

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt/coco/sev-guest`. Source: `D1/in/raw/alma/members/f890639b91af7e6f949b8b99.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `sev-guest.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3a17a8da5a68df24e2ad5365

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt/coco/tdx-guest`. Source: `D1/in/raw/alma/members/3a17a8da5a68df24e2ad5365.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tdx-guest.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-606099da5942982a28eab665

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virt/nitro_enclaves`. Source: `D1/in/raw/alma/members/606099da5942982a28eab665.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nitro_enclaves.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7e4ca2b39ca73e76eff250a0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/virtio`. Source: `D1/in/raw/alma/members/7e4ca2b39ca73e76eff250a0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `virtio_balloon.ko.xz`, `virtio_dma_buf.ko.xz`, `virtio_input.ko.xz`, `virtio_mem.ko.xz`, `virtio_vdpa.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aafc2627ba1c924dcd766f2a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/watchdog`. Source: `D1/in/raw/alma/members/aafc2627ba1c924dcd766f2a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hpwdt.ko.xz`, `i6300esb.ko.xz`, `iTCO_vendor_support.ko.xz`, `iTCO_wdt.ko.xz`, `ib700wdt.ko.xz`, `ibmasr.ko.xz`, `mei_wdt.ko.xz`, `softdog.ko.xz`, `sp5100_tco.ko.xz`, `wdat_wdt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3ad6ff40d2a03056f66e919a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/drivers/xen`. Source: `D1/in/raw/alma/members/3ad6ff40d2a03056f66e919a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xen-evtchn.ko.xz`, `xen-front-pgdir-shbuf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a01b69a57523431ebf7b38fc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs`. Source: `D1/in/raw/alma/members/a01b69a57523431ebf7b38fc.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: binfmt_misc.ko.xz,mbcache.ko.xz; UNKNOWN: afs,btrfs,cachefiles,ceph,erofs,exfat,ext4,fat,fuse,isofs,jbd2,lockd,netfs,nfs,nfs_common,nfsd,nls,overlayfs,pstore,smb,squashfs,udf,xfs

- **UNKNOWN**: `afs`, `btrfs`, `cachefiles`, `ceph`, `erofs`, `exfat`, `ext4`, `fat`, `fuse`, `isofs`, `jbd2`, `lockd`, `netfs`, `nfs`, `nfs_common`, `nfsd`, `nls`, `overlayfs`, `pstore`, `smb`, `squashfs`, `udf`, `xfs`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `binfmt_misc.ko.xz`, `mbcache.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a189efe9f7e9c3d329396eeb

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/btrfs`. Source: `D1/in/raw/alma/members/a189efe9f7e9c3d329396eeb.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `btrfs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-83ccbba048fdb2a9810254ba

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/cachefiles`. Source: `D1/in/raw/alma/members/83ccbba048fdb2a9810254ba.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cachefiles.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-63351ca88c7d55422667450e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/ceph`. Source: `D1/in/raw/alma/members/63351ca88c7d55422667450e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ceph.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-aef5c5b0a96d6594b5f78430

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/erofs`. Source: `D1/in/raw/alma/members/aef5c5b0a96d6594b5f78430.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `erofs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-18674cabee944cb36db06964

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/exfat`. Source: `D1/in/raw/alma/members/18674cabee944cb36db06964.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `exfat.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6ea30c73f56b21f96a906645

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/ext4`. Source: `D1/in/raw/alma/members/6ea30c73f56b21f96a906645.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ext4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5a2bcce6b4f18c44996a5ff0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/fat`. Source: `D1/in/raw/alma/members/5a2bcce6b4f18c44996a5ff0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `fat.ko.xz`, `msdos.ko.xz`, `vfat.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a438aa59afdd1c54a5021e37

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/fuse`. Source: `D1/in/raw/alma/members/a438aa59afdd1c54a5021e37.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cuse.ko.xz`, `fuse.ko.xz`, `virtiofs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2f4ebf8959dd4d8838748f29

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/isofs`. Source: `D1/in/raw/alma/members/2f4ebf8959dd4d8838748f29.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `isofs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6987662da9511baac569b985

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/jbd2`. Source: `D1/in/raw/alma/members/6987662da9511baac569b985.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `jbd2.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-680c57b70e5937b0bf8ac7c6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/lockd`. Source: `D1/in/raw/alma/members/680c57b70e5937b0bf8ac7c6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `lockd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8c63e2d5d5ef92e2dd2964b7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/netfs`. Source: `D1/in/raw/alma/members/8c63e2d5d5ef92e2dd2964b7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `netfs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c82ebde669ae2ca43c4339a7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfs`. Source: `D1/in/raw/alma/members/c82ebde669ae2ca43c4339a7.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: nfs.ko.xz,nfsv3.ko.xz,nfsv4.ko.xz; UNKNOWN: blocklayout,filelayout,flexfilelayout

- **UNKNOWN**: `blocklayout`, `filelayout`, `flexfilelayout`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `nfs.ko.xz`, `nfsv3.ko.xz`, `nfsv4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e0debb5162a074e009950f8a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfs/blocklayout`. Source: `D1/in/raw/alma/members/e0debb5162a074e009950f8a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `blocklayoutdriver.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a503dbfb25bf1642d0baa92b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfs/filelayout`. Source: `D1/in/raw/alma/members/a503dbfb25bf1642d0baa92b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nfs_layout_nfsv41_files.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ce30f52a40706dac80654704

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfs/flexfilelayout`. Source: `D1/in/raw/alma/members/ce30f52a40706dac80654704.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nfs_layout_flexfiles.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-398620d0389967d4838586a5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfs_common`. Source: `D1/in/raw/alma/members/398620d0389967d4838586a5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `grace.ko.xz`, `nfs_acl.ko.xz`, `nfs_localio.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fe409521c9a88c85151c2797

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nfsd`. Source: `D1/in/raw/alma/members/fe409521c9a88c85151c2797.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `nfsd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-620c6b1a4ecc294879ad9241

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/nls`. Source: `D1/in/raw/alma/members/620c6b1a4ecc294879ad9241.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mac-celtic.ko.xz`, `mac-centeuro.ko.xz`, `mac-croatian.ko.xz`, `mac-cyrillic.ko.xz`, `mac-gaelic.ko.xz`, `mac-greek.ko.xz`, `mac-iceland.ko.xz`, `mac-inuit.ko.xz`, `mac-roman.ko.xz`, `mac-romanian.ko.xz`, `mac-turkish.ko.xz`, `nls_cp1250.ko.xz`, `nls_cp1251.ko.xz`, `nls_cp1255.ko.xz`, `nls_cp737.ko.xz`, `nls_cp775.ko.xz`, `nls_cp850.ko.xz`, `nls_cp852.ko.xz`, `nls_cp855.ko.xz`, `nls_cp857.ko.xz`, `nls_cp860.ko.xz`, `nls_cp861.ko.xz`, `nls_cp862.ko.xz`, `nls_cp863.ko.xz`, `nls_cp864.ko.xz`, `nls_cp865.ko.xz`, `nls_cp866.ko.xz`, `nls_cp869.ko.xz`, `nls_cp874.ko.xz`, `nls_cp932.ko.xz`, `nls_cp936.ko.xz`, `nls_cp949.ko.xz`, `nls_cp950.ko.xz`, `nls_euc-jp.ko.xz`, `nls_iso8859-1.ko.xz`, `nls_iso8859-13.ko.xz`, `nls_iso8859-14.ko.xz`, `nls_iso8859-15.ko.xz`, `nls_iso8859-2.ko.xz`, `nls_iso8859-3.ko.xz`, `nls_iso8859-4.ko.xz`, `nls_iso8859-5.ko.xz`, `nls_iso8859-6.ko.xz`, `nls_iso8859-7.ko.xz`, `nls_iso8859-9.ko.xz`, `nls_koi8-r.ko.xz`, `nls_koi8-ru.ko.xz`, `nls_koi8-u.ko.xz`, `nls_ucs2_utils.ko.xz`, `nls_utf8.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-582425ffd4a953846101e7c0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/overlayfs`. Source: `D1/in/raw/alma/members/582425ffd4a953846101e7c0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `overlay.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bbb029c78f47e511a5bbcb67

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/pstore`. Source: `D1/in/raw/alma/members/bbb029c78f47e511a5bbcb67.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ramoops.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fbe2dddac930fb6dfa7498b6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/smb`. Source: `D1/in/raw/alma/members/fbe2dddac930fb6dfa7498b6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `client`, `common`, `smbdirect`. Directory installation integrity and creation provenance are not established.
### alma-b98293dcb04c021980b98b7e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/smb/client`. Source: `D1/in/raw/alma/members/b98293dcb04c021980b98b7e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cifs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-15edb86d974a75bece0428e5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/smb/common`. Source: `D1/in/raw/alma/members/15edb86d974a75bece0428e5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `cifs_arc4.ko.xz`, `cifs_md4.ko.xz`, `smb_compress.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-88b7777a503b9e67cbfc3e09

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/smb/smbdirect`. Source: `D1/in/raw/alma/members/88b7777a503b9e67cbfc3e09.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `smbdirect.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ed017b606c7367a3efa4ac82

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/squashfs`. Source: `D1/in/raw/alma/members/ed017b606c7367a3efa4ac82.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `squashfs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-78dc0e268bd4d3c9452d6bbc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/udf`. Source: `D1/in/raw/alma/members/78dc0e268bd4d3c9452d6bbc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `udf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-96d1bbe98b6d5ad9f43eb72d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/fs/xfs`. Source: `D1/in/raw/alma/members/96d1bbe98b6d5ad9f43eb72d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xfs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f3ce813febcdd237714cc1af

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/kernel`. Source: `D1/in/raw/alma/members/f3ce813febcdd237714cc1af.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: kheaders.ko.xz; UNKNOWN: locking,rcu,time,trace

- **INSTALLED-PACKAGE**: `kheaders.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `locking`, `rcu`, `time`, `trace`. Directory installation integrity and creation provenance are not established.
### alma-5d2e181a760539f6a6fd0b5f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/kernel/trace`. Source: `D1/in/raw/alma/members/5d2e181a760539f6a6fd0b5f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ring_buffer_benchmark.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b4234354c7d061234a270b89

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib`. Source: `D1/in/raw/alma/members/b4234354c7d061234a270b89.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: crc-itu-t.ko.xz,crc7.ko.xz,crc8.ko.xz,objagg.ko.xz,parman.ko.xz,polynomial.ko.xz,ts_bm.ko.xz,ts_fsm.ko.xz,ts_kmp.ko.xz; UNKNOWN: 842,crypto,kunit,lz4,math,raid6,reed_solomon,zstd

- **UNKNOWN**: `842`, `crypto`, `kunit`, `lz4`, `math`, `raid6`, `reed_solomon`, `zstd`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `crc-itu-t.ko.xz`, `crc7.ko.xz`, `crc8.ko.xz`, `objagg.ko.xz`, `parman.ko.xz`, `polynomial.ko.xz`, `ts_bm.ko.xz`, `ts_fsm.ko.xz`, `ts_kmp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ab7f53ea1ec9745f80a45c5c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/842`. Source: `D1/in/raw/alma/members/ab7f53ea1ec9745f80a45c5c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `842_compress.ko.xz`, `842_decompress.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-64990841f3ca0e17152752c0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/crypto`. Source: `D1/in/raw/alma/members/64990841f3ca0e17152752c0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libarc4.ko.xz`, `libcurve25519-generic.ko.xz`, `libcurve25519.ko.xz`, `libdes.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4a1435899730b153a872c7ae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/lz4`. Source: `D1/in/raw/alma/members/4a1435899730b153a872c7ae.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `lz4_compress.ko.xz`, `lz4hc_compress.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-359d1eb7995f1fb4c3288633

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/math`. Source: `D1/in/raw/alma/members/359d1eb7995f1fb4c3288633.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cordic.ko.xz,prime_numbers.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `cordic.ko.xz`, `prime_numbers.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-ad43c454a44c5dbc524900b2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/raid6`. Source: `D1/in/raw/alma/members/ad43c454a44c5dbc524900b2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `raid6_pq.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-208b27a08d4c04977dc388ac

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/reed_solomon`. Source: `D1/in/raw/alma/members/208b27a08d4c04977dc388ac.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `reed_solomon.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-bf0cec24bf36c83988f5ad96

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/lib/zstd`. Source: `D1/in/raw/alma/members/bf0cec24bf36c83988f5ad96.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `zstd_compress.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a390c7aa5df3f4cb361fb0c1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/mm`. Source: `D1/in/raw/alma/members/a390c7aa5df3f4cb361fb0c1.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: hwpoison-inject.ko.xz; UNKNOWN: kfence

- **INSTALLED-PACKAGE**: `hwpoison-inject.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `kfence`. Directory installation integrity and creation provenance are not established.
### alma-77fa9d7234f1f61c38648b46

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net`. Source: `D1/in/raw/alma/members/77fa9d7234f1f61c38648b46.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `802`, `8021q`, `bluetooth`, `bridge`, `can`, `ceph`, `core`, `dns_resolver`, `handshake`, `hsr`, `ieee802154`, `ipv4`, `ipv6`, `l2tp`, `llc`, `mac80211`, `mac802154`, `mpls`, `mptcp`, `netfilter`, `openvswitch`, `psample`, `qrtr`, `rfkill`, `rxrpc`, `sched`, `sctp`, `sunrpc`, `tipc`, `tls`, `vmw_vsock`, `wireless`, `xdp`, `xfrm`. Directory installation integrity and creation provenance are not established.
### alma-2f3ea343e20df3088d1f51f1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/802`. Source: `D1/in/raw/alma/members/2f3ea343e20df3088d1f51f1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `garp.ko.xz`, `mrp.ko.xz`, `p8022.ko.xz`, `psnap.ko.xz`, `stp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7181c202627c8f2bcdc0feed

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/8021q`. Source: `D1/in/raw/alma/members/7181c202627c8f2bcdc0feed.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `8021q.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-84fb246937b4a54db733ab41

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bluetooth`. Source: `D1/in/raw/alma/members/84fb246937b4a54db733ab41.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: bluetooth.ko.xz; UNKNOWN: bnep,hidp,rfcomm

- **INSTALLED-PACKAGE**: `bluetooth.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `bnep`, `hidp`, `rfcomm`. Directory installation integrity and creation provenance are not established.
### alma-f8eecdd0313c90863770054c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bluetooth/bnep`. Source: `D1/in/raw/alma/members/f8eecdd0313c90863770054c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `bnep.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-19a8236cc88ee5bfe8cc0ab5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bluetooth/hidp`. Source: `D1/in/raw/alma/members/19a8236cc88ee5bfe8cc0ab5.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hidp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e9569dbf7973acd974ce766a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bluetooth/rfcomm`. Source: `D1/in/raw/alma/members/e9569dbf7973acd974ce766a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rfcomm.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-165fc04fcdd590d3dcee0196

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bridge`. Source: `D1/in/raw/alma/members/165fc04fcdd590d3dcee0196.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: br_netfilter.ko.xz,bridge.ko.xz; UNKNOWN: netfilter

- **INSTALLED-PACKAGE**: `br_netfilter.ko.xz`, `bridge.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `netfilter`. Directory installation integrity and creation provenance are not established.
### alma-5c59b15e2176ee7d493a3d96

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/bridge/netfilter`. Source: `D1/in/raw/alma/members/5c59b15e2176ee7d493a3d96.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ebt_802_3.ko.xz`, `ebt_among.ko.xz`, `ebt_arp.ko.xz`, `ebt_arpreply.ko.xz`, `ebt_dnat.ko.xz`, `ebt_ip.ko.xz`, `ebt_ip6.ko.xz`, `ebt_limit.ko.xz`, `ebt_log.ko.xz`, `ebt_mark.ko.xz`, `ebt_mark_m.ko.xz`, `ebt_nflog.ko.xz`, `ebt_pkttype.ko.xz`, `ebt_redirect.ko.xz`, `ebt_snat.ko.xz`, `ebt_stp.ko.xz`, `ebt_vlan.ko.xz`, `ebtable_broute.ko.xz`, `ebtable_filter.ko.xz`, `ebtable_nat.ko.xz`, `ebtables.ko.xz`, `nf_conntrack_bridge.ko.xz`, `nft_meta_bridge.ko.xz`, `nft_reject_bridge.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1d09f3aad757575bb14a3511

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/can`. Source: `D1/in/raw/alma/members/1d09f3aad757575bb14a3511.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: can-bcm.ko.xz,can-gw.ko.xz,can-isotp.ko.xz,can-raw.ko.xz,can.ko.xz; UNKNOWN: j1939

- **INSTALLED-PACKAGE**: `can-bcm.ko.xz`, `can-gw.ko.xz`, `can-isotp.ko.xz`, `can-raw.ko.xz`, `can.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `j1939`. Directory installation integrity and creation provenance are not established.
### alma-1b98c818f2f57e92eacddb93

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/can/j1939`. Source: `D1/in/raw/alma/members/1b98c818f2f57e92eacddb93.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `can-j1939.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c6b0a4b76b62a8a2fba817f2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ceph`. Source: `D1/in/raw/alma/members/c6b0a4b76b62a8a2fba817f2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `libceph.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6383af2435f99b34e7fc94f6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/core`. Source: `D1/in/raw/alma/members/6383af2435f99b34e7fc94f6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `failover.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e43edb75f9d3c9f89af2f9f3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/dns_resolver`. Source: `D1/in/raw/alma/members/e43edb75f9d3c9f89af2f9f3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `dns_resolver.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6867d2afcbe9ddef2af01962

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/hsr`. Source: `D1/in/raw/alma/members/6867d2afcbe9ddef2af01962.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hsr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7b068bc83b90061057d84e2b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ieee802154`. Source: `D1/in/raw/alma/members/7b068bc83b90061057d84e2b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ieee802154.ko.xz`, `ieee802154_socket.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-36aa16585d317db8ad028d70

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ipv4`. Source: `D1/in/raw/alma/members/36aa16585d317db8ad028d70.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ah4.ko.xz,esp4.ko.xz,esp4_offload.ko.xz,fou.ko.xz,gre.ko.xz,ip_gre.ko.xz,ip_tunnel.ko.xz,ip_vti.ko.xz,ipcomp.ko.xz,ipip.ko.xz,tcp_bbr.ko.xz,tcp_bic.ko.xz,tcp_dctcp.ko.xz,tcp_htcp.ko.xz,tcp_illinois.ko.xz,tcp_nv.ko.xz,tcp_westwood.ko.xz,tunnel4.ko.xz,udp_tunnel.ko.xz,xfrm4_tunnel.ko.xz; UNKNOWN: netfilter

- **INSTALLED-PACKAGE**: `ah4.ko.xz`, `esp4.ko.xz`, `esp4_offload.ko.xz`, `fou.ko.xz`, `gre.ko.xz`, `ip_gre.ko.xz`, `ip_tunnel.ko.xz`, `ip_vti.ko.xz`, `ipcomp.ko.xz`, `ipip.ko.xz`, `tcp_bbr.ko.xz`, `tcp_bic.ko.xz`, `tcp_dctcp.ko.xz`, `tcp_htcp.ko.xz`, `tcp_illinois.ko.xz`, `tcp_nv.ko.xz`, `tcp_westwood.ko.xz`, `tunnel4.ko.xz`, `udp_tunnel.ko.xz`, `xfrm4_tunnel.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `netfilter`. Directory installation integrity and creation provenance are not established.
### alma-2d6006f71870b086687012bd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ipv4/netfilter`. Source: `D1/in/raw/alma/members/2d6006f71870b086687012bd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `arp_tables.ko.xz`, `arpt_mangle.ko.xz`, `arptable_filter.ko.xz`, `ip_tables.ko.xz`, `ipt_ECN.ko.xz`, `ipt_REJECT.ko.xz`, `ipt_ah.ko.xz`, `ipt_rpfilter.ko.xz`, `iptable_filter.ko.xz`, `iptable_mangle.ko.xz`, `iptable_nat.ko.xz`, `iptable_raw.ko.xz`, `iptable_security.ko.xz`, `nf_defrag_ipv4.ko.xz`, `nf_dup_ipv4.ko.xz`, `nf_nat_h323.ko.xz`, `nf_nat_pptp.ko.xz`, `nf_nat_snmp_basic.ko.xz`, `nf_reject_ipv4.ko.xz`, `nf_socket_ipv4.ko.xz`, `nf_tproxy_ipv4.ko.xz`, `nft_dup_ipv4.ko.xz`, `nft_fib_ipv4.ko.xz`, `nft_reject_ipv4.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f5334373588bf63e11ba14e7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ipv6`. Source: `D1/in/raw/alma/members/f5334373588bf63e11ba14e7.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ah6.ko.xz,esp6.ko.xz,esp6_offload.ko.xz,fou6.ko.xz,ip6_gre.ko.xz,ip6_tunnel.ko.xz,ip6_udp_tunnel.ko.xz,ip6_vti.ko.xz,ipcomp6.ko.xz,mip6.ko.xz,sit.ko.xz,tunnel6.ko.xz,xfrm6_tunnel.ko.xz; UNKNOWN: netfilter

- **INSTALLED-PACKAGE**: `ah6.ko.xz`, `esp6.ko.xz`, `esp6_offload.ko.xz`, `fou6.ko.xz`, `ip6_gre.ko.xz`, `ip6_tunnel.ko.xz`, `ip6_udp_tunnel.ko.xz`, `ip6_vti.ko.xz`, `ipcomp6.ko.xz`, `mip6.ko.xz`, `sit.ko.xz`, `tunnel6.ko.xz`, `xfrm6_tunnel.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `netfilter`. Directory installation integrity and creation provenance are not established.
### alma-fca501a1302e163b3f20a85f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/ipv6/netfilter`. Source: `D1/in/raw/alma/members/fca501a1302e163b3f20a85f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ip6_tables.ko.xz`, `ip6t_NPT.ko.xz`, `ip6t_REJECT.ko.xz`, `ip6t_ah.ko.xz`, `ip6t_eui64.ko.xz`, `ip6t_frag.ko.xz`, `ip6t_hbh.ko.xz`, `ip6t_ipv6header.ko.xz`, `ip6t_mh.ko.xz`, `ip6t_rpfilter.ko.xz`, `ip6t_rt.ko.xz`, `ip6table_filter.ko.xz`, `ip6table_mangle.ko.xz`, `ip6table_nat.ko.xz`, `ip6table_raw.ko.xz`, `ip6table_security.ko.xz`, `nf_defrag_ipv6.ko.xz`, `nf_dup_ipv6.ko.xz`, `nf_reject_ipv6.ko.xz`, `nf_socket_ipv6.ko.xz`, `nf_tproxy_ipv6.ko.xz`, `nft_dup_ipv6.ko.xz`, `nft_fib_ipv6.ko.xz`, `nft_reject_ipv6.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ba445f27369ed2eb6b397d52

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/l2tp`. Source: `D1/in/raw/alma/members/ba445f27369ed2eb6b397d52.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `l2tp_core.ko.xz`, `l2tp_debugfs.ko.xz`, `l2tp_eth.ko.xz`, `l2tp_ip.ko.xz`, `l2tp_ip6.ko.xz`, `l2tp_netlink.ko.xz`, `l2tp_ppp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-823f16fa617628e92cdfdabf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/llc`. Source: `D1/in/raw/alma/members/823f16fa617628e92cdfdabf.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `llc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a1bd371e71ec218189e12199

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/mac80211`. Source: `D1/in/raw/alma/members/a1bd371e71ec218189e12199.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: mac80211.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `mac80211.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-3b94e76b4f3abef23ae9ffd4

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/mac802154`. Source: `D1/in/raw/alma/members/3b94e76b4f3abef23ae9ffd4.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mac802154.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-51e11150614fb8e15c687ee7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/mpls`. Source: `D1/in/raw/alma/members/51e11150614fb8e15c687ee7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `mpls_iptunnel.ko.xz`, `mpls_router.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2769c790c09a83de9baf7c8f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/netfilter`. Source: `D1/in/raw/alma/members/2769c790c09a83de9baf7c8f.tsv`. Decision: **MIXED**.

Member decisions differ: INSTALLED-PACKAGE, UNKNOWN. Exact member split: part-alma.1.notes.md, alma-2769c790c09a83de9baf7c8f.

- **UNKNOWN**: `ipset`, `ipvs`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `nf_conncount.ko.xz`, `nf_conntrack.ko.xz`, `nf_conntrack_amanda.ko.xz`, `nf_conntrack_broadcast.ko.xz`, `nf_conntrack_ftp.ko.xz`, `nf_conntrack_h323.ko.xz`, `nf_conntrack_irc.ko.xz`, `nf_conntrack_netbios_ns.ko.xz`, `nf_conntrack_netlink.ko.xz`, `nf_conntrack_pptp.ko.xz`, `nf_conntrack_sane.ko.xz`, `nf_conntrack_sip.ko.xz`, `nf_conntrack_snmp.ko.xz`, `nf_conntrack_tftp.ko.xz`, `nf_dup_netdev.ko.xz`, `nf_flow_table.ko.xz`, `nf_flow_table_inet.ko.xz`, `nf_log_syslog.ko.xz`, `nf_nat.ko.xz`, `nf_nat_amanda.ko.xz`, `nf_nat_ftp.ko.xz`, `nf_nat_irc.ko.xz`, `nf_nat_sip.ko.xz`, `nf_nat_tftp.ko.xz`, `nf_synproxy_core.ko.xz`, `nf_tables.ko.xz`, `nfnetlink.ko.xz`, `nfnetlink_cthelper.ko.xz`, `nfnetlink_cttimeout.ko.xz`, `nfnetlink_hook.ko.xz`, `nfnetlink_log.ko.xz`, `nfnetlink_osf.ko.xz`, `nfnetlink_queue.ko.xz`, `nft_chain_nat.ko.xz`, `nft_compat.ko.xz`, `nft_connlimit.ko.xz`, `nft_ct.ko.xz`, `nft_dup_netdev.ko.xz`, `nft_fib.ko.xz`, `nft_fib_inet.ko.xz`, `nft_fib_netdev.ko.xz`, `nft_flow_offload.ko.xz`, `nft_fwd_netdev.ko.xz`, `nft_hash.ko.xz`, `nft_limit.ko.xz`, `nft_log.ko.xz`, `nft_masq.ko.xz`, `nft_nat.ko.xz`, `nft_numgen.ko.xz`, `nft_osf.ko.xz`, `nft_queue.ko.xz`, `nft_quota.ko.xz`, `nft_redir.ko.xz`, `nft_reject.ko.xz`, `nft_reject_inet.ko.xz`, `nft_reject_netdev.ko.xz`, `nft_socket.ko.xz`, `nft_synproxy.ko.xz`, `nft_tproxy.ko.xz`, `nft_tunnel.ko.xz`, `nft_xfrm.ko.xz`, `xt_AUDIT.ko.xz`, `xt_CHECKSUM.ko.xz`, `xt_CLASSIFY.ko.xz`, `xt_CONNSECMARK.ko.xz`, `xt_CT.ko.xz`, `xt_DSCP.ko.xz`, `xt_HL.ko.xz`, `xt_HMARK.ko.xz`, `xt_IDLETIMER.ko.xz`, `xt_LOG.ko.xz`, `xt_MASQUERADE.ko.xz`, `xt_NETMAP.ko.xz`, `xt_NFLOG.ko.xz`, `xt_NFQUEUE.ko.xz`, `xt_RATEEST.ko.xz`, `xt_REDIRECT.ko.xz`, `xt_SECMARK.ko.xz`, `xt_TCPMSS.ko.xz`, `xt_TCPOPTSTRIP.ko.xz`, `xt_TEE.ko.xz`, `xt_TPROXY.ko.xz`, `xt_TRACE.ko.xz`, `xt_addrtype.ko.xz`, `xt_bpf.ko.xz`, `xt_cgroup.ko.xz`, `xt_cluster.ko.xz`, `xt_comment.ko.xz`, `xt_connbytes.ko.xz`, `xt_connlabel.ko.xz`, `xt_connlimit.ko.xz`, `xt_connmark.ko.xz`, `xt_conntrack.ko.xz`, `xt_cpu.ko.xz`, `xt_dccp.ko.xz`, `xt_devgroup.ko.xz`, `xt_dscp.ko.xz`, `xt_ecn.ko.xz`, `xt_esp.ko.xz`, `xt_hashlimit.ko.xz`, `xt_helper.ko.xz`, `xt_hl.ko.xz`, `xt_iprange.ko.xz`, `xt_ipvs.ko.xz`, `xt_length.ko.xz`, `xt_limit.ko.xz`, `xt_mac.ko.xz`, `xt_mark.ko.xz`, `xt_multiport.ko.xz`, `xt_nat.ko.xz`, `xt_osf.ko.xz`, `xt_owner.ko.xz`, `xt_physdev.ko.xz`, `xt_pkttype.ko.xz`, `xt_policy.ko.xz`, `xt_quota.ko.xz`, `xt_rateest.ko.xz`, `xt_realm.ko.xz`, `xt_recent.ko.xz`, `xt_sctp.ko.xz`, `xt_set.ko.xz`, `xt_socket.ko.xz`, `xt_state.ko.xz`, `xt_statistic.ko.xz`, `xt_string.ko.xz`, `xt_tcpmss.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4935ac121601c19c09b7c74e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/netfilter/ipset`. Source: `D1/in/raw/alma/members/4935ac121601c19c09b7c74e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ip_set.ko.xz`, `ip_set_bitmap_ip.ko.xz`, `ip_set_bitmap_ipmac.ko.xz`, `ip_set_bitmap_port.ko.xz`, `ip_set_hash_ip.ko.xz`, `ip_set_hash_ipmac.ko.xz`, `ip_set_hash_ipmark.ko.xz`, `ip_set_hash_ipport.ko.xz`, `ip_set_hash_ipportip.ko.xz`, `ip_set_hash_ipportnet.ko.xz`, `ip_set_hash_mac.ko.xz`, `ip_set_hash_net.ko.xz`, `ip_set_hash_netiface.ko.xz`, `ip_set_hash_netnet.ko.xz`, `ip_set_hash_netport.ko.xz`, `ip_set_hash_netportnet.ko.xz`, `ip_set_list_set.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ec5bbeea0ada94b655f8010b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/netfilter/ipvs`. Source: `D1/in/raw/alma/members/ec5bbeea0ada94b655f8010b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `ip_vs.ko.xz`, `ip_vs_dh.ko.xz`, `ip_vs_fo.ko.xz`, `ip_vs_ftp.ko.xz`, `ip_vs_lblc.ko.xz`, `ip_vs_lblcr.ko.xz`, `ip_vs_lc.ko.xz`, `ip_vs_mh.ko.xz`, `ip_vs_nq.ko.xz`, `ip_vs_ovf.ko.xz`, `ip_vs_pe_sip.ko.xz`, `ip_vs_rr.ko.xz`, `ip_vs_sed.ko.xz`, `ip_vs_sh.ko.xz`, `ip_vs_wlc.ko.xz`, `ip_vs_wrr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8e39b6b67b1c5a1d41d2365c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/openvswitch`. Source: `D1/in/raw/alma/members/8e39b6b67b1c5a1d41d2365c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `openvswitch.ko.xz`, `vport-geneve.ko.xz`, `vport-gre.ko.xz`, `vport-vxlan.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f5384b59a32b1ef44b93dc61

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/psample`. Source: `D1/in/raw/alma/members/f5384b59a32b1ef44b93dc61.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `psample.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5df272316030e742bc73ce2b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/qrtr`. Source: `D1/in/raw/alma/members/5df272316030e742bc73ce2b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `qrtr-mhi.ko.xz`, `qrtr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c79c577d10d15ad870640881

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/rfkill`. Source: `D1/in/raw/alma/members/c79c577d10d15ad870640881.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rfkill.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e23316f98617ccbe004577c2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/sched`. Source: `D1/in/raw/alma/members/e23316f98617ccbe004577c2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `act_bpf.ko.xz`, `act_csum.ko.xz`, `act_ct.ko.xz`, `act_ctinfo.ko.xz`, `act_gact.ko.xz`, `act_mirred.ko.xz`, `act_mpls.ko.xz`, `act_pedit.ko.xz`, `act_police.ko.xz`, `act_sample.ko.xz`, `act_skbedit.ko.xz`, `act_tunnel_key.ko.xz`, `act_vlan.ko.xz`, `cls_bpf.ko.xz`, `cls_flow.ko.xz`, `cls_flower.ko.xz`, `cls_fw.ko.xz`, `cls_matchall.ko.xz`, `cls_u32.ko.xz`, `sch_cake.ko.xz`, `sch_cbs.ko.xz`, `sch_etf.ko.xz`, `sch_ets.ko.xz`, `sch_fq.ko.xz`, `sch_gred.ko.xz`, `sch_hfsc.ko.xz`, `sch_htb.ko.xz`, `sch_ingress.ko.xz`, `sch_mqprio.ko.xz`, `sch_mqprio_lib.ko.xz`, `sch_multiq.ko.xz`, `sch_netem.ko.xz`, `sch_prio.ko.xz`, `sch_red.ko.xz`, `sch_sfq.ko.xz`, `sch_taprio.ko.xz`, `sch_tbf.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c8f3907b2ad7c911d03e6a41

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/sctp`. Source: `D1/in/raw/alma/members/c8f3907b2ad7c911d03e6a41.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `sctp.ko.xz`, `sctp_diag.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a78d22bd646fa36def682b0a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/sunrpc`. Source: `D1/in/raw/alma/members/a78d22bd646fa36def682b0a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: sunrpc.ko.xz; UNKNOWN: auth_gss,xprtrdma

- **UNKNOWN**: `auth_gss`, `xprtrdma`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `sunrpc.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-26b143ae2e6f3c39aa1efaa6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/sunrpc/auth_gss`. Source: `D1/in/raw/alma/members/26b143ae2e6f3c39aa1efaa6.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `auth_rpcgss.ko.xz`, `rpcsec_gss_krb5.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b326711741fcc91fc83702fa

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/sunrpc/xprtrdma`. Source: `D1/in/raw/alma/members/b326711741fcc91fc83702fa.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `rpcrdma.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-6f13d1f394ead13ca90feff3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/tipc`. Source: `D1/in/raw/alma/members/6f13d1f394ead13ca90feff3.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tipc.ko.xz`, `tipc_diag.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-30c61d621ca6f318fa46f9bf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/tls`. Source: `D1/in/raw/alma/members/30c61d621ca6f318fa46f9bf.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `tls.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-06b0eeb5f3b4e7c7e959f5ef

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/vmw_vsock`. Source: `D1/in/raw/alma/members/06b0eeb5f3b4e7c7e959f5ef.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `hv_sock.ko.xz`, `vmw_vsock_virtio_transport.ko.xz`, `vmw_vsock_virtio_transport_common.ko.xz`, `vmw_vsock_vmci_transport.ko.xz`, `vsock.ko.xz`, `vsock_diag.ko.xz`, `vsock_loopback.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ab0e2734f24dc225063896b3

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/wireless`. Source: `D1/in/raw/alma/members/ab0e2734f24dc225063896b3.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: cfg80211.ko.xz; UNKNOWN: tests

- **INSTALLED-PACKAGE**: `cfg80211.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `tests`. Directory installation integrity and creation provenance are not established.
### alma-1595c24e7adab5b78c9ce00e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/xdp`. Source: `D1/in/raw/alma/members/1595c24e7adab5b78c9ce00e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xsk_diag.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-cbcf11492299ae17e0561319

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/net/xfrm`. Source: `D1/in/raw/alma/members/cbcf11492299ae17e0561319.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `xfrm_interface.ko.xz`, `xfrm_ipcomp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3f1e4a7ddd464dfb6274ef75

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/samples`. Source: `D1/in/raw/alma/members/3f1e4a7ddd464dfb6274ef75.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `vfio-mdev`. Directory installation integrity and creation provenance are not established.
### alma-4f89312dee26eba854b2f145

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound`. Source: `D1/in/raw/alma/members/4f89312dee26eba854b2f145.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: ac97_bus.ko.xz,soundcore.ko.xz; UNKNOWN: core,drivers,hda,i2c,pci,soc,synth,usb,virtio,x86,xen

- **INSTALLED-PACKAGE**: `ac97_bus.ko.xz`, `soundcore.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `core`, `drivers`, `hda`, `i2c`, `pci`, `soc`, `synth`, `usb`, `virtio`, `x86`, `xen`. Directory installation integrity and creation provenance are not established.
### alma-46f79aa26569af8ab8b0174a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/core`. Source: `D1/in/raw/alma/members/46f79aa26569af8ab8b0174a.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-compress.ko.xz,snd-ctl-led.ko.xz,snd-hrtimer.ko.xz,snd-hwdep.ko.xz,snd-pcm.ko.xz,snd-rawmidi.ko.xz,snd-seq-device.ko.xz,snd-timer.ko.xz,snd-ump.ko.xz,snd.ko.xz; UNKNOWN: seq

- **UNKNOWN**: `seq`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-compress.ko.xz`, `snd-ctl-led.ko.xz`, `snd-hrtimer.ko.xz`, `snd-hwdep.ko.xz`, `snd-pcm.ko.xz`, `snd-rawmidi.ko.xz`, `snd-seq-device.ko.xz`, `snd-timer.ko.xz`, `snd-ump.ko.xz`, `snd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0cb1d81da4e34b8533435097

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/core/seq`. Source: `D1/in/raw/alma/members/0cb1d81da4e34b8533435097.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-seq-dummy.ko.xz`, `snd-seq-midi-emul.ko.xz`, `snd-seq-midi-event.ko.xz`, `snd-seq-midi.ko.xz`, `snd-seq-ump-client.ko.xz`, `snd-seq-virmidi.ko.xz`, `snd-seq.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-70c666eb3fb95fb026cda690

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/drivers`. Source: `D1/in/raw/alma/members/70c666eb3fb95fb026cda690.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-aloop.ko.xz,snd-dummy.ko.xz,snd-mtpav.ko.xz,snd-virmidi.ko.xz; UNKNOWN: mpu401,opl3,pcsp,vx

- **UNKNOWN**: `mpu401`, `opl3`, `pcsp`, `vx`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-aloop.ko.xz`, `snd-dummy.ko.xz`, `snd-mtpav.ko.xz`, `snd-virmidi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-949a19626a0068e911c1ddcf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/drivers/mpu401`. Source: `D1/in/raw/alma/members/949a19626a0068e911c1ddcf.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-mpu401-uart.ko.xz`, `snd-mpu401.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-58a6d96ce996483bff2e9ddd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/drivers/opl3`. Source: `D1/in/raw/alma/members/58a6d96ce996483bff2e9ddd.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-opl3-lib.ko.xz`, `snd-opl3-synth.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-94dabf446956a9a491e9d886

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/drivers/pcsp`. Source: `D1/in/raw/alma/members/94dabf446956a9a491e9d886.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-pcsp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-406d51cae5fdf01be0fcfd83

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/drivers/vx`. Source: `D1/in/raw/alma/members/406d51cae5fdf01be0fcfd83.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-vx-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-52a0bb93c98ebe0ffb8e44b6

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda`. Source: `D1/in/raw/alma/members/52a0bb93c98ebe0ffb8e44b6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `codecs`, `common`, `controllers`, `core`. Directory installation integrity and creation provenance are not established.
### alma-ad8845dcbd762503b9c736bf

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/codecs`. Source: `D1/in/raw/alma/members/ad8845dcbd762503b9c736bf.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-hda-codec-analog.ko.xz,snd-hda-codec-ca0110.ko.xz,snd-hda-codec-ca0132.ko.xz,snd-hda-codec-cm9825.ko.xz,snd-hda-codec-cmedia.ko.xz,snd-hda-codec-conexant.ko.xz,snd-hda-codec-generic.ko.xz,snd-hda-codec-idt.ko.xz,snd-hda-codec-senarytech.ko.xz,snd-hda-codec-si3054.ko.xz,snd-hda-codec-via.ko.xz; UNKNOWN: cirrus,hdmi,realtek,side-codecs

- **UNKNOWN**: `cirrus`, `hdmi`, `realtek`, `side-codecs`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-hda-codec-analog.ko.xz`, `snd-hda-codec-ca0110.ko.xz`, `snd-hda-codec-ca0132.ko.xz`, `snd-hda-codec-cm9825.ko.xz`, `snd-hda-codec-cmedia.ko.xz`, `snd-hda-codec-conexant.ko.xz`, `snd-hda-codec-generic.ko.xz`, `snd-hda-codec-idt.ko.xz`, `snd-hda-codec-senarytech.ko.xz`, `snd-hda-codec-si3054.ko.xz`, `snd-hda-codec-via.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-244ab16b3f50be371d123762

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/codecs/cirrus`. Source: `D1/in/raw/alma/members/244ab16b3f50be371d123762.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-codec-cs420x.ko.xz`, `snd-hda-codec-cs421x.ko.xz`, `snd-hda-codec-cs8409.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-637f6f7ed994901421759e05

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/codecs/hdmi`. Source: `D1/in/raw/alma/members/637f6f7ed994901421759e05.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-codec-atihdmi.ko.xz`, `snd-hda-codec-hdmi.ko.xz`, `snd-hda-codec-intelhdmi.ko.xz`, `snd-hda-codec-nvhdmi-mcp.ko.xz`, `snd-hda-codec-nvhdmi.ko.xz`, `snd-hda-codec-simplehdmi.ko.xz`, `snd-hda-codec-tegrahdmi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8c678d588e270243a1c45a70

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/codecs/realtek`. Source: `D1/in/raw/alma/members/8c678d588e270243a1c45a70.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-codec-alc260.ko.xz`, `snd-hda-codec-alc262.ko.xz`, `snd-hda-codec-alc268.ko.xz`, `snd-hda-codec-alc269.ko.xz`, `snd-hda-codec-alc662.ko.xz`, `snd-hda-codec-alc680.ko.xz`, `snd-hda-codec-alc861.ko.xz`, `snd-hda-codec-alc861vd.ko.xz`, `snd-hda-codec-alc880.ko.xz`, `snd-hda-codec-alc882.ko.xz`, `snd-hda-codec-realtek-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f800ef7462e7546f6e3a71f1

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/codecs/side-codecs`. Source: `D1/in/raw/alma/members/f800ef7462e7546f6e3a71f1.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-cirrus-scodec.ko.xz`, `snd-hda-scodec-component.ko.xz`, `snd-hda-scodec-cs35l41-i2c.ko.xz`, `snd-hda-scodec-cs35l41-spi.ko.xz`, `snd-hda-scodec-cs35l41.ko.xz`, `snd-hda-scodec-cs35l56-i2c.ko.xz`, `snd-hda-scodec-cs35l56-spi.ko.xz`, `snd-hda-scodec-cs35l56.ko.xz`, `snd-hda-scodec-tas2781-i2c.ko.xz`, `snd-hda-scodec-tas2781-spi.ko.xz`, `snd-hda-scodec-tas2781.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ac40aa8ed63ce6d9db1083c2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/common`. Source: `D1/in/raw/alma/members/ac40aa8ed63ce6d9db1083c2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-codec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5a8e0b02ac9bcdc6ba015d05

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/controllers`. Source: `D1/in/raw/alma/members/5a8e0b02ac9bcdc6ba015d05.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-acpi.ko.xz`, `snd-hda-intel.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3edec7e408747d749136a8dd

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/core`. Source: `D1/in/raw/alma/members/3edec7e408747d749136a8dd.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-hda-core.ko.xz,snd-intel-dspcfg.ko.xz,snd-intel-sdw-acpi.ko.xz; UNKNOWN: ext

- **UNKNOWN**: `ext`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-hda-core.ko.xz`, `snd-intel-dspcfg.ko.xz`, `snd-intel-sdw-acpi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-05e7ad1eba9e7c13d25b0825

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/hda/core/ext`. Source: `D1/in/raw/alma/members/05e7ad1eba9e7c13d25b0825.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hda-ext-core.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7c95473c78ebeaa50339273e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/i2c`. Source: `D1/in/raw/alma/members/7c95473c78ebeaa50339273e.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-cs8427.ko.xz,snd-i2c.ko.xz; UNKNOWN: other

- **UNKNOWN**: `other`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-cs8427.ko.xz`, `snd-i2c.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-acd5b1530c1e7ee9bb374481

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/i2c/other`. Source: `D1/in/raw/alma/members/acd5b1530c1e7ee9bb374481.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ak4113.ko.xz`, `snd-ak4114.ko.xz`, `snd-ak4xxx-adda.ko.xz`, `snd-pt2258.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-88ffa4d1b4014efe9a98ee23

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci`. Source: `D1/in/raw/alma/members/88ffa4d1b4014efe9a98ee23.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-ad1889.ko.xz,snd-atiixp-modem.ko.xz,snd-atiixp.ko.xz,snd-bt87x.ko.xz,snd-cmipci.ko.xz,snd-ens1370.ko.xz,snd-ens1371.ko.xz,snd-es1968.ko.xz,snd-intel8x0.ko.xz,snd-intel8x0m.ko.xz,snd-maestro3.ko.xz,snd-rme32.ko.xz,snd-rme96.ko.xz,snd-via82xx-modem.ko.xz,snd-via82xx.ko.xz; UNKNOWN: ac97,ali5451,asihpi,au88x0,ca0106,cs46xx,ctxfi,echoaudio,emu10k1,ice1712,korg1212,lola,lx6464es,mixart,oxygen,pcxhr,rme9652,trident,vx222

- **UNKNOWN**: `ac97`, `ali5451`, `asihpi`, `au88x0`, `ca0106`, `cs46xx`, `ctxfi`, `echoaudio`, `emu10k1`, `ice1712`, `korg1212`, `lola`, `lx6464es`, `mixart`, `oxygen`, `pcxhr`, `rme9652`, `trident`, `vx222`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-ad1889.ko.xz`, `snd-atiixp-modem.ko.xz`, `snd-atiixp.ko.xz`, `snd-bt87x.ko.xz`, `snd-cmipci.ko.xz`, `snd-ens1370.ko.xz`, `snd-ens1371.ko.xz`, `snd-es1968.ko.xz`, `snd-intel8x0.ko.xz`, `snd-intel8x0m.ko.xz`, `snd-maestro3.ko.xz`, `snd-rme32.ko.xz`, `snd-rme96.ko.xz`, `snd-via82xx-modem.ko.xz`, `snd-via82xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-fa920406583a86537064316e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/ac97`. Source: `D1/in/raw/alma/members/fa920406583a86537064316e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ac97-codec.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7d6bb081768d90e7f9ee0100

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/ali5451`. Source: `D1/in/raw/alma/members/7d6bb081768d90e7f9ee0100.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ali5451.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2e44fef0572b0641a8c55901

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/asihpi`. Source: `D1/in/raw/alma/members/2e44fef0572b0641a8c55901.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-asihpi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9483a8eb060ad9d56875a94f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/au88x0`. Source: `D1/in/raw/alma/members/9483a8eb060ad9d56875a94f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-au8810.ko.xz`, `snd-au8820.ko.xz`, `snd-au8830.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1ad3e6822fc90e37ab83b27e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/ca0106`. Source: `D1/in/raw/alma/members/1ad3e6822fc90e37ab83b27e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ca0106.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-dbe277c031be2bb77f3e3f14

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/cs46xx`. Source: `D1/in/raw/alma/members/dbe277c031be2bb77f3e3f14.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-cs46xx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1d6726dc4de33c13b3a88d55

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/ctxfi`. Source: `D1/in/raw/alma/members/1d6726dc4de33c13b3a88d55.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ctxfi.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-82b1a37017756a4847c11314

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/echoaudio`. Source: `D1/in/raw/alma/members/82b1a37017756a4847c11314.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-darla20.ko.xz`, `snd-darla24.ko.xz`, `snd-echo3g.ko.xz`, `snd-gina20.ko.xz`, `snd-gina24.ko.xz`, `snd-indigo.ko.xz`, `snd-indigodj.ko.xz`, `snd-indigodjx.ko.xz`, `snd-indigoio.ko.xz`, `snd-indigoiox.ko.xz`, `snd-layla20.ko.xz`, `snd-layla24.ko.xz`, `snd-mia.ko.xz`, `snd-mona.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-492387a0f3bad7a5827feab0

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/emu10k1`. Source: `D1/in/raw/alma/members/492387a0f3bad7a5827feab0.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-emu10k1-synth.ko.xz`, `snd-emu10k1.ko.xz`, `snd-emu10k1x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-26d2e11dd7f2a303d3ea559f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/ice1712`. Source: `D1/in/raw/alma/members/26d2e11dd7f2a303d3ea559f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ice1712.ko.xz`, `snd-ice1724.ko.xz`, `snd-ice17xx-ak4xxx.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-33d22109bf7db892e264dafc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/korg1212`. Source: `D1/in/raw/alma/members/33d22109bf7db892e264dafc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-korg1212.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d5e72fb7cdbf0d5e68dc1895

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/lola`. Source: `D1/in/raw/alma/members/d5e72fb7cdbf0d5e68dc1895.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-lola.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-71477cdec69f3b89e50cbe65

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/lx6464es`. Source: `D1/in/raw/alma/members/71477cdec69f3b89e50cbe65.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-lx6464es.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5271fbd6ff28bbe0e3bcbacc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/mixart`. Source: `D1/in/raw/alma/members/5271fbd6ff28bbe0e3bcbacc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-mixart.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f808fb7119727561cc23442f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/oxygen`. Source: `D1/in/raw/alma/members/f808fb7119727561cc23442f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-oxygen-lib.ko.xz`, `snd-oxygen.ko.xz`, `snd-virtuoso.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-ea7df900ac456de3dcef6c8f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/pcxhr`. Source: `D1/in/raw/alma/members/ea7df900ac456de3dcef6c8f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-pcxhr.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-c8a2432a55f6c402bc42fa57

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/rme9652`. Source: `D1/in/raw/alma/members/c8a2432a55f6c402bc42fa57.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hdsp.ko.xz`, `snd-hdspm.ko.xz`, `snd-rme9652.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-2eb2be50623c66184bf32578

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/trident`. Source: `D1/in/raw/alma/members/2eb2be50623c66184bf32578.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-trident.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-0db54234701c7eeb774e5d94

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/pci/vx222`. Source: `D1/in/raw/alma/members/0db54234701c7eeb774e5d94.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-vx222.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1a3c018e6d105db9b2436940

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc`. Source: `D1/in/raw/alma/members/1a3c018e6d105db9b2436940.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-soc-acpi.ko.xz,snd-soc-core.ko.xz; UNKNOWN: amd,codecs,intel,sdca,sdw_utils,sof

- **UNKNOWN**: `amd`, `codecs`, `intel`, `sdca`, `sdw_utils`, `sof`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-soc-acpi.ko.xz`, `snd-soc-core.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-93b61c720fc82143747ec404

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/amd`. Source: `D1/in/raw/alma/members/93b61c720fc82143747ec404.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-acp-config.ko.xz; UNKNOWN: acp,ps,renoir,yc

- **UNKNOWN**: `acp`, `ps`, `renoir`, `yc`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-acp-config.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-12963d842040fbc5ec200d1c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/amd/acp`. Source: `D1/in/raw/alma/members/12963d842040fbc5ec200d1c.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-acp-i2s.ko.xz`, `snd-acp-legacy-common.ko.xz`, `snd-acp-legacy-mach.ko.xz`, `snd-acp-mach.ko.xz`, `snd-acp-pci.ko.xz`, `snd-acp-pcm.ko.xz`, `snd-acp-pdm.ko.xz`, `snd-acp-rembrandt.ko.xz`, `snd-acp-renoir.ko.xz`, `snd-acp-sdw-legacy-mach.ko.xz`, `snd-acp-sdw-mach.ko.xz`, `snd-acp-sdw-sof-mach.ko.xz`, `snd-acp-sof-mach.ko.xz`, `snd-acp63.ko.xz`, `snd-acp70.ko.xz`, `snd-amd-acpi-mach.ko.xz`, `snd-amd-sdw-acpi.ko.xz`, `snd-soc-acpi-amd-match.ko.xz`, `snd-soc-acpi-amd-sdca-quirks.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-057607912c473d499c33876a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/amd/ps`. Source: `D1/in/raw/alma/members/057607912c473d499c33876a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-pci-ps.ko.xz`, `snd-ps-pdm-dma.ko.xz`, `snd-ps-sdw-dma.ko.xz`, `snd-soc-ps-mach.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d9b87a9f0f2d51fdbf94f2ba

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/amd/renoir`. Source: `D1/in/raw/alma/members/d9b87a9f0f2d51fdbf94f2ba.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-acp3x-pdm-dma.ko.xz`, `snd-acp3x-rn.ko.xz`, `snd-rn-pci-acp3x.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-40864c3c99315e387f407325

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/amd/yc`. Source: `D1/in/raw/alma/members/40864c3c99315e387f407325.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-acp6x-pdm-dma.ko.xz`, `snd-pci-acp6x.ko.xz`, `snd-soc-acp6x-mach.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9cabf3f90b0fa3a80930de1b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/codecs`. Source: `D1/in/raw/alma/members/9cabf3f90b0fa3a80930de1b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-cs-amp-lib.ko.xz`, `snd-soc-cs35l41-i2c.ko.xz`, `snd-soc-cs35l41-lib.ko.xz`, `snd-soc-cs35l41-spi.ko.xz`, `snd-soc-cs35l41.ko.xz`, `snd-soc-cs35l56-sdw.ko.xz`, `snd-soc-cs35l56-shared.ko.xz`, `snd-soc-cs35l56-spi.ko.xz`, `snd-soc-cs35l56.ko.xz`, `snd-soc-cs42l42-i2c.ko.xz`, `snd-soc-cs42l42-sdw.ko.xz`, `snd-soc-cs42l42.ko.xz`, `snd-soc-cs42l43-sdw.ko.xz`, `snd-soc-cs42l43.ko.xz`, `snd-soc-cx2072x.ko.xz`, `snd-soc-da7213.ko.xz`, `snd-soc-da7219.ko.xz`, `snd-soc-dmic.ko.xz`, `snd-soc-es8316.ko.xz`, `snd-soc-es8326.ko.xz`, `snd-soc-es83xx-dsm-common.ko.xz`, `snd-soc-hda-codec.ko.xz`, `snd-soc-hdac-hda.ko.xz`, `snd-soc-max98090.ko.xz`, `snd-soc-max98357a.ko.xz`, `snd-soc-max98363.ko.xz`, `snd-soc-max98373-i2c.ko.xz`, `snd-soc-max98373-sdw.ko.xz`, `snd-soc-max98373.ko.xz`, `snd-soc-max98388.ko.xz`, `snd-soc-max98390.ko.xz`, `snd-soc-max98927.ko.xz`, `snd-soc-nau8315.ko.xz`, `snd-soc-nau8821.ko.xz`, `snd-soc-nau8824.ko.xz`, `snd-soc-nau8825.ko.xz`, `snd-soc-pcm3168a-i2c.ko.xz`, `snd-soc-pcm3168a.ko.xz`, `snd-soc-pcm512x-i2c.ko.xz`, `snd-soc-pcm512x.ko.xz`, `snd-soc-pm4125-sdw.ko.xz`, `snd-soc-pm4125.ko.xz`, `snd-soc-rl6231.ko.xz`, `snd-soc-rl6347a.ko.xz`, `snd-soc-rt-sdw-common.ko.xz`, `snd-soc-rt1011.ko.xz`, `snd-soc-rt1015.ko.xz`, `snd-soc-rt1015p.ko.xz`, `snd-soc-rt1019.ko.xz`, `snd-soc-rt1308-sdw.ko.xz`, `snd-soc-rt1308.ko.xz`, `snd-soc-rt1316-sdw.ko.xz`, `snd-soc-rt1318-sdw.ko.xz`, `snd-soc-rt1320-sdw.ko.xz`, `snd-soc-rt274.ko.xz`, `snd-soc-rt286.ko.xz`, `snd-soc-rt298.ko.xz`, `snd-soc-rt5514.ko.xz`, `snd-soc-rt5640.ko.xz`, `snd-soc-rt5645.ko.xz`, `snd-soc-rt5651.ko.xz`, `snd-soc-rt5660.ko.xz`, `snd-soc-rt5663.ko.xz`, `snd-soc-rt5670.ko.xz`, `snd-soc-rt5677-spi.ko.xz`, `snd-soc-rt5677.ko.xz`, `snd-soc-rt5682-i2c.ko.xz`, `snd-soc-rt5682-sdw.ko.xz`, `snd-soc-rt5682.ko.xz`, `snd-soc-rt5682s.ko.xz`, `snd-soc-rt700.ko.xz`, `snd-soc-rt711-sdca.ko.xz`, `snd-soc-rt711.ko.xz`, `snd-soc-rt712-sdca-dmic.ko.xz`, `snd-soc-rt712-sdca.ko.xz`, `snd-soc-rt715-sdca.ko.xz`, `snd-soc-rt715.ko.xz`, `snd-soc-rt721-sdca.ko.xz`, `snd-soc-rt722-sdca.ko.xz`, `snd-soc-ssm4567.ko.xz`, `snd-soc-tas2781-comlib-i2c.ko.xz`, `snd-soc-tas2781-comlib.ko.xz`, `snd-soc-tas2781-fmwlib.ko.xz`, `snd-soc-tas2781-i2c.ko.xz`, `snd-soc-tas2783-sdw.ko.xz`, `snd-soc-ts3a227e.ko.xz`, `snd-soc-wcd-common.ko.xz`, `snd-soc-wcd-mbhc.ko.xz`, `snd-soc-wm-adsp.ko.xz`, `snd-soc-wm8804-i2c.ko.xz`, `snd-soc-wm8804.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-f056adbcd932c90d34b9c1ae

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel`. Source: `D1/in/raw/alma/members/f056adbcd932c90d34b9c1ae.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `atom`, `avs`, `boards`, `catpt`, `common`. Directory installation integrity and creation provenance are not established.
### alma-08f0c70f417556f7b89f29ad

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/atom`. Source: `D1/in/raw/alma/members/08f0c70f417556f7b89f29ad.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-soc-sst-atom-hifi2-platform.ko.xz; UNKNOWN: sst

- **INSTALLED-PACKAGE**: `snd-soc-sst-atom-hifi2-platform.ko.xz`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `sst`. Directory installation integrity and creation provenance are not established.
### alma-7a09fa0763bf491d8b71d9fc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/atom/sst`. Source: `D1/in/raw/alma/members/7a09fa0763bf491d8b71d9fc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-intel-sst-acpi.ko.xz`, `snd-intel-sst-core.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-1926f04a40ff04684531cf79

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/avs`. Source: `D1/in/raw/alma/members/1926f04a40ff04684531cf79.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-soc-avs.ko.xz; UNKNOWN: boards

- **UNKNOWN**: `boards`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-soc-avs.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-7b99cdae2cd736ccf60a64f2

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/avs/boards`. Source: `D1/in/raw/alma/members/7b99cdae2cd736ccf60a64f2.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-avs-da7219.ko.xz`, `snd-soc-avs-dmic.ko.xz`, `snd-soc-avs-es8336.ko.xz`, `snd-soc-avs-hdaudio.ko.xz`, `snd-soc-avs-max98357a.ko.xz`, `snd-soc-avs-max98373.ko.xz`, `snd-soc-avs-max98927.ko.xz`, `snd-soc-avs-nau8825.ko.xz`, `snd-soc-avs-pcm3168a.ko.xz`, `snd-soc-avs-probe.ko.xz`, `snd-soc-avs-rt274.ko.xz`, `snd-soc-avs-rt286.ko.xz`, `snd-soc-avs-rt298.ko.xz`, `snd-soc-avs-rt5514.ko.xz`, `snd-soc-avs-rt5640.ko.xz`, `snd-soc-avs-rt5663.ko.xz`, `snd-soc-avs-rt5682.ko.xz`, `snd-soc-avs-ssm4567.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-00927ee6fb99020406961105

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/boards`. Source: `D1/in/raw/alma/members/00927ee6fb99020406961105.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-bdw-rt286.ko.xz`, `snd-soc-ehl-rt5660.ko.xz`, `snd-soc-hsw-rt5640.ko.xz`, `snd-soc-intel-hda-dsp-common.ko.xz`, `snd-soc-intel-sof-board-helpers.ko.xz`, `snd-soc-intel-sof-cirrus-common.ko.xz`, `snd-soc-intel-sof-maxim-common.ko.xz`, `snd-soc-intel-sof-nuvoton-common.ko.xz`, `snd-soc-intel-sof-realtek-common.ko.xz`, `snd-soc-intel-sof-ti-common.ko.xz`, `snd-soc-skl_hda_dsp.ko.xz`, `snd-soc-sof-sdw.ko.xz`, `snd-soc-sof-ssp-amp.ko.xz`, `snd-soc-sof_cs42l42.ko.xz`, `snd-soc-sof_da7219.ko.xz`, `snd-soc-sof_es8336.ko.xz`, `snd-soc-sof_nau8825.ko.xz`, `snd-soc-sof_rt5682.ko.xz`, `snd-soc-sst-bdw-rt5650-mach.ko.xz`, `snd-soc-sst-bdw-rt5677-mach.ko.xz`, `snd-soc-sst-byt-cht-cx2072x.ko.xz`, `snd-soc-sst-byt-cht-da7213.ko.xz`, `snd-soc-sst-byt-cht-es8316.ko.xz`, `snd-soc-sst-byt-cht-nocodec.ko.xz`, `snd-soc-sst-bytcr-rt5640.ko.xz`, `snd-soc-sst-bytcr-rt5651.ko.xz`, `snd-soc-sst-cht-bsw-max98090_ti.ko.xz`, `snd-soc-sst-cht-bsw-nau8824.ko.xz`, `snd-soc-sst-cht-bsw-rt5645.ko.xz`, `snd-soc-sst-cht-bsw-rt5672.ko.xz`, `snd-soc-sst-sof-pcm512x.ko.xz`, `snd-soc-sst-sof-wm8804.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-15d7667dc470c34558d769c7

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/catpt`. Source: `D1/in/raw/alma/members/15d7667dc470c34558d769c7.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-catpt.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-70b12e87a2d29b2890bf312e

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/intel/common`. Source: `D1/in/raw/alma/members/70b12e87a2d29b2890bf312e.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-acpi-intel-match.ko.xz`, `snd-soc-acpi-intel-sdca-quirks.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b470ca3f3594a04a040aa57d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sdca`. Source: `D1/in/raw/alma/members/b470ca3f3594a04a040aa57d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-sdca-class-function.ko.xz`, `snd-soc-sdca-class.ko.xz`, `snd-soc-sdca.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-4d58ca134441fe93dffbbc51

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sdw_utils`. Source: `D1/in/raw/alma/members/4d58ca134441fe93dffbbc51.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-soc-sdw-utils.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9fdd90ae7e5f1a756296c09c

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sof`. Source: `D1/in/raw/alma/members/9fdd90ae7e5f1a756296c09c.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-sof-acpi.ko.xz,snd-sof-pci.ko.xz,snd-sof-probes.ko.xz,snd-sof-utils.ko.xz,snd-sof.ko.xz; UNKNOWN: amd,intel,xtensa

- **UNKNOWN**: `amd`, `intel`, `xtensa`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-sof-acpi.ko.xz`, `snd-sof-pci.ko.xz`, `snd-sof-probes.ko.xz`, `snd-sof-utils.ko.xz`, `snd-sof.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-61f8895973420c20f2c72898

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sof/amd`. Source: `D1/in/raw/alma/members/61f8895973420c20f2c72898.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-sof-amd-acp.ko.xz`, `snd-sof-amd-acp63.ko.xz`, `snd-sof-amd-acp70.ko.xz`, `snd-sof-amd-rembrandt.ko.xz`, `snd-sof-amd-renoir.ko.xz`, `snd-sof-amd-vangogh.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-8c0c6e3a1ec7453614bf3f4f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sof/intel`. Source: `D1/in/raw/alma/members/8c0c6e3a1ec7453614bf3f4f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-sof-acpi-intel-bdw.ko.xz`, `snd-sof-acpi-intel-byt.ko.xz`, `snd-sof-intel-atom.ko.xz`, `snd-sof-intel-hda-common.ko.xz`, `snd-sof-intel-hda-generic.ko.xz`, `snd-sof-intel-hda-mlink.ko.xz`, `snd-sof-intel-hda-sdw-bpt.ko.xz`, `snd-sof-intel-hda.ko.xz`, `snd-sof-pci-intel-apl.ko.xz`, `snd-sof-pci-intel-cnl.ko.xz`, `snd-sof-pci-intel-icl.ko.xz`, `snd-sof-pci-intel-lnl.ko.xz`, `snd-sof-pci-intel-mtl.ko.xz`, `snd-sof-pci-intel-nvl.ko.xz`, `snd-sof-pci-intel-ptl.ko.xz`, `snd-sof-pci-intel-tgl.ko.xz`, `snd-sof-pci-intel-tng.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-41ad879aab53f9f13e70455f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/soc/sof/xtensa`. Source: `D1/in/raw/alma/members/41ad879aab53f9f13e70455f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-sof-xtensa-dsp.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3147df43b30cce4858cc1207

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/synth`. Source: `D1/in/raw/alma/members/3147df43b30cce4858cc1207.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-util-mem.ko.xz; UNKNOWN: emux

- **UNKNOWN**: `emux`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-util-mem.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-d6aeb03b7ba834c4012e8cbc

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/synth/emux`. Source: `D1/in/raw/alma/members/d6aeb03b7ba834c4012e8cbc.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-emux-synth.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-b10d3814f1e83323efb77ca5

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb`. Source: `D1/in/raw/alma/members/b10d3814f1e83323efb77ca5.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: snd-usb-audio.ko.xz,snd-usbmidi-lib.ko.xz; UNKNOWN: 6fire,bcd2000,caiaq,hiface,line6,misc,usx2y

- **UNKNOWN**: `6fire`, `bcd2000`, `caiaq`, `hiface`, `line6`, `misc`, `usx2y`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `snd-usb-audio.ko.xz`, `snd-usbmidi-lib.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-e24c7bfae3bc2a93d99f1125

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/6fire`. Source: `D1/in/raw/alma/members/e24c7bfae3bc2a93d99f1125.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-usb-6fire.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-9a56192878dcdbcfa17fd3ec

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/bcd2000`. Source: `D1/in/raw/alma/members/9a56192878dcdbcfa17fd3ec.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-bcd2000.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3ca6f473f199ed85323de44b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/caiaq`. Source: `D1/in/raw/alma/members/3ca6f473f199ed85323de44b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-usb-caiaq.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-43fcfa992abcd609363c070f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/hiface`. Source: `D1/in/raw/alma/members/43fcfa992abcd609363c070f.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-usb-hiface.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-3012cdf0e8342dd7a073acfa

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/line6`. Source: `D1/in/raw/alma/members/3012cdf0e8342dd7a073acfa.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-usb-line6.ko.xz`, `snd-usb-pod.ko.xz`, `snd-usb-podhd.ko.xz`, `snd-usb-toneport.ko.xz`, `snd-usb-variax.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5328ecc4a7fec7d291f1a298

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/misc`. Source: `D1/in/raw/alma/members/5328ecc4a7fec7d291f1a298.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-ua101.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a80646047bc34a8093f24c2b

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/usb/usx2y`. Source: `D1/in/raw/alma/members/a80646047bc34a8093f24c2b.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-usb-us122l.ko.xz`, `snd-usb-us144mkii.ko.xz`, `snd-usb-usx2y.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-a6cb217300285004d9f12214

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/virtio`. Source: `D1/in/raw/alma/members/a6cb217300285004d9f12214.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `virtio_snd.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-26c513a08fab5882dad5c14d

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/x86`. Source: `D1/in/raw/alma/members/26c513a08fab5882dad5c14d.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd-hdmi-lpe-audio.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-5429003b86671716cf22194a

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/sound/xen`. Source: `D1/in/raw/alma/members/5429003b86671716cf22194a.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `snd_xen_front.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-314874cb83efaf0d6cc7606f

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/virt`. Source: `D1/in/raw/alma/members/314874cb83efaf0d6cc7606f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `lib`. Directory installation integrity and creation provenance are not established.
### alma-d6720b3e433d0940b79ea644

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/kernel/virt/lib`. Source: `D1/in/raw/alma/members/d6720b3e433d0940b79ea644.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `irqbypass.ko.xz`. Unchanged package member after verified filesystem alias resolution.
### alma-25e612bc18b023f39e398976

Group: `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64/vdso`. Source: `D1/in/raw/alma/members/25e612bc18b023f39e398976.tsv`. Decision: **INSTALLED-PACKAGE**.

Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.

- **INSTALLED-PACKAGE**: `vdso32.so`, `vdso64.so`. Unchanged package member after verified filesystem alias resolution.
### alma-b348893f7f3225378d1776eb

Group: `/usr/lib/sysimage/rpm`. Source: `D1/in/raw/alma/members/b348893f7f3225378d1776eb.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.rpmdbdirsymlink_created`. Package origin, unchangedness, and source of this object are not established.
### alma-09f24c7dad696b979d9a163d

Group: `/usr/lib/systemd`. Source: `D1/in/raw/alma/members/09f24c7dad696b979d9a163d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ntp-units.d`, `system-environment-generators`. Directory installation integrity and creation provenance are not established.
### alma-f436dd1c81663a6be2feb765

Group: `/usr/lib64`. Source: `D1/in/raw/alma/members/f436dd1c81663a6be2feb765.tsv`. Decision: **MIXED**.

INSTALLED-PACKAGE: libgcc_s-14-20260724.so.1,libtirpc.so.3.0.0; UNKNOWN: alsa-lib,gbm,gnome-software,hmaccalc,libgcc_s.so.1,libtirpc.so.3,ossl-modules,pipewire-0.3

- **UNKNOWN**: `alsa-lib`, `gbm`, `gnome-software`, `hmaccalc`, `ossl-modules`, `pipewire-0.3`. Directory installation integrity and creation provenance are not established.
- **INSTALLED-PACKAGE**: `libgcc_s-14-20260724.so.1`, `libtirpc.so.3.0.0`. Unchanged package member after verified filesystem alias resolution.
- **UNKNOWN**: `libgcc_s.so.1`, `libtirpc.so.3`. Whether this package member remains as received is unrecorded.
### alma-1e8142534cba60c604af31da

Group: `/usr/lib64/firefox`. Source: `D1/in/raw/alma/members/1e8142534cba60c604af31da.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `browser`, `defaults`, `distribution`, `fonts`. Directory installation integrity and creation provenance are not established.
### alma-16002cbef09cef1eda8daeed

Group: `/usr/lib64/firefox/browser`. Source: `D1/in/raw/alma/members/16002cbef09cef1eda8daeed.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `defaults`. Directory installation integrity and creation provenance are not established.
### alma-9ba7fbbf37bab3c8c2191473

Group: `/usr/lib64/firefox/defaults`. Source: `D1/in/raw/alma/members/9ba7fbbf37bab3c8c2191473.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `pref`. Directory installation integrity and creation provenance are not established.
### alma-8a17134d085769d2559aa702

Group: `/usr/lib64/open-vm-tools`. Source: `D1/in/raw/alma/members/8a17134d085769d2559aa702.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `lib64`, `share`. Directory installation integrity and creation provenance are not established.
### alma-aaada2bca5e019c2042a07d1

Group: `/usr/lib64/pipewire-0.3`. Source: `D1/in/raw/alma/members/aaada2bca5e019c2042a07d1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `jack`. Directory installation integrity and creation provenance are not established.
### alma-1580186e030a0e0eb14fb8e8

Group: `/usr/lib64/python3.12/site-packages/gi`. Source: `D1/in/raw/alma/members/1580186e030a0e0eb14fb8e8.tsv`. Decision: **MIXED**.

RECORD: __pycache__; UNKNOWN: overrides

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
- **UNKNOWN**: `overrides`. Directory installation integrity and creation provenance are not established.
### alma-de151556c072fd6c5550fadc

Group: `/usr/lib64/python3.12/site-packages/gi/overrides`. Source: `D1/in/raw/alma/members/de151556c072fd6c5550fadc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `__pycache__`. Python-generated cache directory; the directory itself is not bytecode.
### alma-3635e115d264fea907eebc25

Group: `/usr/lib64/spa-0.2`. Source: `D1/in/raw/alma/members/3635e115d264fea907eebc25.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `filter-graph`. Directory installation integrity and creation provenance are not established.
### alma-56a7594a6c7993da54691693

Group: `/usr/libexec`. Source: `D1/in/raw/alma/members/56a7594a6c7993da54691693.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `libkcapi`. Directory installation integrity and creation provenance are not established.
### alma-9dacb0f7ce0a31c843d66c4c

Group: `/usr/local/share/applications`. Source: `D1/in/raw/alma/members/9dacb0f7ce0a31c843d66c4c.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `mimeinfo.cache`. Package origin, unchangedness, and source of this object are not established.
### alma-564a08001519d020704d7252

Group: `/usr/sbin`. Source: `D1/in/raw/alma/members/564a08001519d020704d7252.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `lpc`. Package origin, unchangedness, and source of this object are not established.
### alma-1d52d3d9de6f01f799804320

Group: `/usr/share`. Source: `D1/in/raw/alma/members/1d52d3d9de6f01f799804320.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `gir-1.0`, `gnome-background-properties`, `ima`, `installed-tests`, `mdadm`, `paps`, `qemu-kvm`. Directory installation integrity and creation provenance are not established.
### alma-132ed68f45f86c9a823aa793

Group: `/usr/share/PackageKit`. Source: `D1/in/raw/alma/members/132ed68f45f86c9a823aa793.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `helpers`. Directory installation integrity and creation provenance are not established.
### alma-a9897afb9e2a41af6aa72be4

Group: `/usr/share/PackageKit/helpers`. Source: `D1/in/raw/alma/members/a9897afb9e2a41af6aa72be4.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `test_spawn`. Directory installation integrity and creation provenance are not established.
### alma-a6305f89e7865b639c10c8e9

Group: `/usr/share/alsa`. Source: `D1/in/raw/alma/members/a6305f89e7865b639c10c8e9.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `alsa.conf.d`. Directory installation integrity and creation provenance are not established.
### alma-b2f53f97f94f1bd5d21e023d

Group: `/usr/share/applications`. Source: `D1/in/raw/alma/members/b2f53f97f94f1bd5d21e023d.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `mimeinfo.cache`. Package origin, unchangedness, and source of this object are not established.
### alma-9d4d706dd1c8946f5f80506b

Group: `/usr/share/cockpit/static/fonts`. Source: `D1/in/raw/alma/members/9d4d706dd1c8946f5f80506b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `RedHatDisplay`, `RedHatMono`, `RedHatText`. Directory installation integrity and creation provenance are not established.
### alma-aa86adb3f8b5f315437c765b

Group: `/usr/share/containers`. Source: `D1/in/raw/alma/members/aa86adb3f8b5f315437c765b.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `podman-sequoia`. Directory installation integrity and creation provenance are not established.
### alma-865eed53b1bcb537caf2fbab

Group: `/usr/share/dbus-1`. Source: `D1/in/raw/alma/members/865eed53b1bcb537caf2fbab.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `accessibility-services`. Directory installation integrity and creation provenance are not established.
### alma-05cd3ecaf8ef92697ccf2fbc

Group: `/usr/share/doc`. Source: `D1/in/raw/alma/members/05cd3ecaf8ef92697ccf2fbc.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `HTML`, `cockpit`, `kernel-keys`, `nftables`, `rdma-core`. Directory installation integrity and creation provenance are not established.
### alma-38ce2ed4ed0b2618485457a1

Group: `/usr/share/doc/nftables`. Source: `D1/in/raw/alma/members/38ce2ed4ed0b2618485457a1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `examples`. Directory installation integrity and creation provenance are not established.
### alma-82fd6b9f155e2f724cfcdfc7

Group: `/usr/share/doc/rpm`. Source: `D1/in/raw/alma/members/82fd6b9f155e2f724cfcdfc7.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `examples`. Directory installation integrity and creation provenance are not established.
### alma-c8b3dbb3f4d639cbde713085

Group: `/usr/share/glib-2.0/schemas`. Source: `D1/in/raw/alma/members/c8b3dbb3f4d639cbde713085.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `gschemas.compiled`. Package origin, unchangedness, and source of this object are not established.
### alma-869a94a754524c530508e711

Group: `/usr/share/gnome`. Source: `D1/in/raw/alma/members/869a94a754524c530508e711.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `autostart`, `shutdown`. Directory installation integrity and creation provenance are not established.
### alma-bb1b3b9e34a9891e6f5cc670

Group: `/usr/share/gnome-shell`. Source: `D1/in/raw/alma/members/bb1b3b9e34a9891e6f5cc670.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `modes`. Directory installation integrity and creation provenance are not established.
### alma-746b03e01ffad8d75d2c246d

Group: `/usr/share/help`. Source: `D1/in/raw/alma/members/746b03e01ffad8d75d2c246d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `C`, `ar`, `as`, `bg`, `ca`, `cs`, `da`, `de`, `el`, `en_GB`, `es`, `eu`, `fa`, `fi`, `fr`, `gl`, `gu`, `he`, `hi`, `hr`, `hu`, `id`, `it`, `ja`, `ka`, `kn`, `ko`, `lt`, `lv`, `ml`, `mr`, `nds`, `ne`, `nl`, `oc`, `pa`, `pl`, `pt`, `pt_BR`, `ro`, `ru`, `sl`, `sr`, `sr@latin`, `sv`, `ta`, `te`, `tr`, `uk`, `vi`, `zh_CN`, `zh_HK`, `zh_TW`. Directory installation integrity and creation provenance are not established.
### alma-f02ef77a205104fc0de5cd70

Group: `/usr/share/icons/Adwaita`. Source: `D1/in/raw/alma/members/f02ef77a205104fc0de5cd70.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `icon-theme.cache`. Package origin, unchangedness, and source of this object are not established.
### alma-ae099e964210c321b5cf7e69

Group: `/usr/share/installed-tests`. Source: `D1/in/raw/alma/members/ae099e964210c321b5cf7e69.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `upower`. Directory installation integrity and creation provenance are not established.
### alma-4f20b0bfd1e0d8a7253d0992

Group: `/usr/share/locale`. Source: `D1/in/raw/alma/members/4f20b0bfd1e0d8a7253d0992.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `bar`, `es_EU`, `jam`, `kmr`, `mjw`, `pa_PK`, `ro_MD`, `sr_Latn`, `yue`, `zh_Hans`, `zh_Hant`. Directory installation integrity and creation provenance are not established.
### alma-28ebfc705c197dbc94398076

Group: `/usr/share/locale/bar`. Source: `D1/in/raw/alma/members/28ebfc705c197dbc94398076.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-d9f91240c2a2207be7cd266f

Group: `/usr/share/locale/es_EU`. Source: `D1/in/raw/alma/members/d9f91240c2a2207be7cd266f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-bb12bb6565f033e546f8b106

Group: `/usr/share/locale/jam`. Source: `D1/in/raw/alma/members/bb12bb6565f033e546f8b106.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-d631793486e2aae1a49055bc

Group: `/usr/share/locale/kmr`. Source: `D1/in/raw/alma/members/d631793486e2aae1a49055bc.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-5cd77fda5f7a76040f8f21ac

Group: `/usr/share/locale/mjw`. Source: `D1/in/raw/alma/members/5cd77fda5f7a76040f8f21ac.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-fe5589499379dc49e9242566

Group: `/usr/share/locale/pa_PK`. Source: `D1/in/raw/alma/members/fe5589499379dc49e9242566.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-76415d25a86f7c3472b68f6f

Group: `/usr/share/locale/ro_MD`. Source: `D1/in/raw/alma/members/76415d25a86f7c3472b68f6f.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-a909d92b49ab67522d6299e7

Group: `/usr/share/locale/sr_Latn`. Source: `D1/in/raw/alma/members/a909d92b49ab67522d6299e7.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-f4eb45f6caf258f9324ebf61

Group: `/usr/share/locale/yue`. Source: `D1/in/raw/alma/members/f4eb45f6caf258f9324ebf61.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-6b6c30917aa1a380b65cc9d4

Group: `/usr/share/locale/zh_Hans`. Source: `D1/in/raw/alma/members/6b6c30917aa1a380b65cc9d4.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-edf519f865cb06592712cfda

Group: `/usr/share/locale/zh_Hant`. Source: `D1/in/raw/alma/members/edf519f865cb06592712cfda.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `LC_MESSAGES`. Directory installation integrity and creation provenance are not established.
### alma-c9b0924e62c06af82ff7fae3

Group: `/usr/share/man`. Source: `D1/in/raw/alma/members/c9b0924e62c06af82ff7fae3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `man2type`, `man3const`, `man3head`, `man3type`. Directory installation integrity and creation provenance are not established.
### alma-85626f6a7e5137d286217ffa

Group: `/usr/share/man/man1`. Source: `D1/in/raw/alma/members/85626f6a7e5137d286217ffa.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cancel.1.gz`, `lp.1.gz`, `lpq.1.gz`, `lpr.1.gz`, `lprm.1.gz`, `lpstat.1.gz`. Package origin, unchangedness, and source of this object are not established.
### alma-95b1adb21de151f70b3f36a7

Group: `/usr/share/man/man8`. Source: `D1/in/raw/alma/members/95b1adb21de151f70b3f36a7.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `lpc.8.gz`. Package origin, unchangedness, and source of this object are not established.
### alma-c1f1d5aca71a57c2f2a2daa4

Group: `/usr/share/mime/application`. Source: `D1/in/raw/alma/members/c1f1d5aca71a57c2f2a2daa4.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `pkcs10+pem.xml`, `pkcs12+pem.xml`, `pkcs7-mime+pem.xml`, `pkcs8+pem.xml`, `pkix-cert+pem.xml`, `pkix-crl+pem.xml`, `x-pem-file.xml`, `x-pem-key.xml`, `x-pkcs12.xml`, `x-spkac+base64.xml`, `x-spkac.xml`, `x.systemd-catalog.xml`, `x.systemd-confext.xml`, `x.systemd-credential.xml`, `x.systemd-hwdb.xml`, `x.systemd-journal.xml`, `x.systemd-sysext.xml`. Package origin, unchangedness, and source of this object are not established.
### alma-960b2681f7eacb67125249df

Group: `/usr/share/pipewire`. Source: `D1/in/raw/alma/members/960b2681f7eacb67125249df.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `client.conf.avail`, `filter-chain`, `pipewire-pulse.conf.avail`, `pipewire.conf.avail`. Directory installation integrity and creation provenance are not established.
### alma-8e9baef8b7a385a7769d3ff6

Group: `/usr/share/plymouth/themes`. Source: `D1/in/raw/alma/members/8e9baef8b7a385a7769d3ff6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tribar`. Directory installation integrity and creation provenance are not established.
### alma-77b0d205d1fedd595d5d0130

Group: `/usr/share/sounds`. Source: `D1/in/raw/alma/members/77b0d205d1fedd595d5d0130.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `gnome`. Directory installation integrity and creation provenance are not established.
### alma-664baf78a81d75130dcc6220

Group: `/usr/share/sounds/gnome`. Source: `D1/in/raw/alma/members/664baf78a81d75130dcc6220.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `default`. Directory installation integrity and creation provenance are not established.
### alma-9ba7c09503991f795d4aa19d

Group: `/usr/share/sounds/gnome/default`. Source: `D1/in/raw/alma/members/9ba7c09503991f795d4aa19d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `alerts`. Directory installation integrity and creation provenance are not established.
### alma-811e3e2a8671c1d11f1358e3

Group: `/usr/share/spa-0.2`. Source: `D1/in/raw/alma/members/811e3e2a8671c1d11f1358e3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `bluez5`. Directory installation integrity and creation provenance are not established.
### alma-12c63b432813219050c84163

Group: `/usr/share/swcatalog/icons`. Source: `D1/in/raw/alma/members/12c63b432813219050c84163.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `rhel-10`. Directory installation integrity and creation provenance are not established.
### alma-2c4c651b0915730f1aa483ce

Group: `/var`. Source: `D1/in/raw/alma/members/2c4c651b0915730f1aa483ce.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.updated`. Package origin, unchangedness, and source of this object are not established.
### alma-e56f44818454d8ca9d1fb205

Group: `/var/cache/PackageKit`. Source: `D1/in/raw/alma/members/e56f44818454d8ca9d1fb205.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `10.3`. Directory installation integrity and creation provenance are not established.
### alma-8c8cde185792565d876b71a1

Group: `/var/cache/PackageKit/10.3`. Source: `D1/in/raw/alma/members/8c8cde185792565d876b71a1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `hawkey`, `metadata`. Directory installation integrity and creation provenance are not established.
### alma-03c8820b788e90608a746287

Group: `/var/cache/cups`. Source: `D1/in/raw/alma/members/03c8820b788e90608a746287.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `org.cups.cupsd`. Package origin, unchangedness, and source of this object are not established.
### alma-e354d6a9002d3f87d89d606f

Group: `/var/cache/dnf`. Source: `D1/in/raw/alma/members/e354d6a9002d3f87d89d606f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `.gpgkeyschecked.yum`, `appstream-0221375ef9ab2490`, `appstream-updateinfo.solvx`, `appstream.solv`, `baseos-dd34f9106e98b1fa`, `baseos-updateinfo.solvx`, `baseos.solv`, `clean_command.lock`, `crb-47f2899d10f358c8`, `crb-updateinfo.solvx`, `crb.solv`, `expired_repos.json`, `extras-7dc392d1da0a70f9`, `extras.solv`, `tempfiles.json`. DNF cache metadata or cache directory.
### alma-6ae6381800e16e6c192dceec

Group: `/var/cache/dnf/appstream-0221375ef9ab2490`. Source: `D1/in/raw/alma/members/6ae6381800e16e6c192dceec.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `mirrorlist`, `packages`, `repodata`. DNF cache metadata or cache directory.
### alma-b5d087d1cb18e62f197b474e

Group: `/var/cache/dnf/appstream-0221375ef9ab2490/repodata`. Source: `D1/in/raw/alma/members/b5d087d1cb18e62f197b474e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1b4fb640b3021d9061e1b21c5cb51636042973e72128e34eccc9eceb487fb025-comps.xml`, `2ea1dcea647ff08982a63471934e6572db3cf4c83746139eb9c054ef9eab8b3c-primary.xml.gz`, `9b2076d72d683420c4905e649ffa3d6545a3b95c53591a503b33ce0d4c79ac3f-updateinfo.xml.gz`, `repomd.xml`. DNF cache metadata or cache directory.
### alma-90db0c15e6f7adb4ef67639d

Group: `/var/cache/dnf/baseos-dd34f9106e98b1fa`. Source: `D1/in/raw/alma/members/90db0c15e6f7adb4ef67639d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `mirrorlist`, `packages`, `repodata`. DNF cache metadata or cache directory.
### alma-d3573f8f54abbbf08ca1b4a5

Group: `/var/cache/dnf/baseos-dd34f9106e98b1fa/repodata`. Source: `D1/in/raw/alma/members/d3573f8f54abbbf08ca1b4a5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `60889a921fcc4e21869e878ea653eb718a364f4ba0e816095460e1af992ed6bc-primary.xml.gz`, `ca749bb0b66434360c4646c046cda42e544f73c9f8230cef2a3e134e40223ac6-comps.xml`, `fde84ecc83ed4f3ffafe926184b77242e70aeba37ac98d004cbc42d8300902fb-updateinfo.xml.gz`, `repomd.xml`. DNF cache metadata or cache directory.
### alma-c99abfac6bbd25402cb17a88

Group: `/var/cache/dnf/crb-47f2899d10f358c8`. Source: `D1/in/raw/alma/members/c99abfac6bbd25402cb17a88.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `mirrorlist`, `repodata`. DNF cache metadata or cache directory.
### alma-058c3001c24c5386d8b54ca5

Group: `/var/cache/dnf/crb-47f2899d10f358c8/repodata`. Source: `D1/in/raw/alma/members/058c3001c24c5386d8b54ca5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `62def1f9bd20e34d230e8929c9e45e997014877427fde6d8a712a7d7349dbf2b-comps.xml`, `96ca4dea027bda230604cf3ad47f46612ec34c7b03c95e0d57942873aecb6a55-primary.xml.gz`, `a62b8edf181cb7f472865a519f3e44340d02275de00c106406cc7f357ce1057d-updateinfo.xml.gz`, `repomd.xml`. DNF cache metadata or cache directory.
### alma-6dce3c0cb6cc9008d3e2ee38

Group: `/var/cache/dnf/extras-7dc392d1da0a70f9`. Source: `D1/in/raw/alma/members/6dce3c0cb6cc9008d3e2ee38.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `mirrorlist`, `repodata`. DNF cache metadata or cache directory.
### alma-c754aa8be5763ac88e392e6e

Group: `/var/cache/dnf/extras-7dc392d1da0a70f9/repodata`. Source: `D1/in/raw/alma/members/c754aa8be5763ac88e392e6e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `1d3fdffbf43360b2df6c2035206991937d6a5cf78d9a0f1581f2492460d7938b-primary.xml.gz`, `ccd6e546ac35d351453e3dab212c3503ae97ece7d6a2bfa2177e137f22c1c462-comps.xml`, `repomd.xml`. DNF cache metadata or cache directory.
### alma-525676ee6ca94ab9c1eedc0a

Group: `/var/cache/man`. Source: `D1/in/raw/alma/members/525676ee6ca94ab9c1eedc0a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `ca`, `cat1`, `cat2`, `cat3`, `cat4`, `cat5`, `cat6`, `cat7`, `cat8`, `cat9`, `cs`, `da`, `de`, `es`, `fi`, `fr`, `hr`, `hu`, `id`, `index.db`, `it`, `ja`, `ka`, `ko`, `lo`, `local`, `nl`, `nodejs-22`, `pl`, `pt`, `pt_BR`, `ro`, `ru`, `sr`, `sv`, `tr`, `uk`, `zh_CN`, `zh_TW`. Manual-page index cache, cache tag, or cache directory.
### alma-bf58e46ff1423480f4f5845f

Group: `/var/cache/man/ca`. Source: `D1/in/raw/alma/members/bf58e46ff1423480f4f5845f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-b201fc34dbc4f932aab010a5

Group: `/var/cache/man/cs`. Source: `D1/in/raw/alma/members/b201fc34dbc4f932aab010a5.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-4233853ea741b2fbf2c699d1

Group: `/var/cache/man/da`. Source: `D1/in/raw/alma/members/4233853ea741b2fbf2c699d1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-b1647b3f75fa0fe1bf000d84

Group: `/var/cache/man/de`. Source: `D1/in/raw/alma/members/b1647b3f75fa0fe1bf000d84.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-d0ff996b8320ccb4d0f38e0c

Group: `/var/cache/man/es`. Source: `D1/in/raw/alma/members/d0ff996b8320ccb4d0f38e0c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-b4b9c4ee427dd862097a1728

Group: `/var/cache/man/fi`. Source: `D1/in/raw/alma/members/b4b9c4ee427dd862097a1728.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-df08ec73ccb4c54ad40d2a32

Group: `/var/cache/man/fr`. Source: `D1/in/raw/alma/members/df08ec73ccb4c54ad40d2a32.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-fa3d671632399e5ed02f64aa

Group: `/var/cache/man/hr`. Source: `D1/in/raw/alma/members/fa3d671632399e5ed02f64aa.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-515e315e9efce6c08ed69fca

Group: `/var/cache/man/hu`. Source: `D1/in/raw/alma/members/515e315e9efce6c08ed69fca.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-3827efd6d880bbf3bcd0736f

Group: `/var/cache/man/id`. Source: `D1/in/raw/alma/members/3827efd6d880bbf3bcd0736f.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-c995f5b0b7d7fd5cfd4ed038

Group: `/var/cache/man/it`. Source: `D1/in/raw/alma/members/c995f5b0b7d7fd5cfd4ed038.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-e634e410aa2ce2c925ac2b7a

Group: `/var/cache/man/ja`. Source: `D1/in/raw/alma/members/e634e410aa2ce2c925ac2b7a.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-68c9d9cb46f0fae41c0ba34c

Group: `/var/cache/man/ka`. Source: `D1/in/raw/alma/members/68c9d9cb46f0fae41c0ba34c.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-13b881b187356b22fc9eb1ee

Group: `/var/cache/man/ko`. Source: `D1/in/raw/alma/members/13b881b187356b22fc9eb1ee.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-602b551d280a3bd7c74b98f1

Group: `/var/cache/man/lo`. Source: `D1/in/raw/alma/members/602b551d280a3bd7c74b98f1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-5c8470dce9f98ad8363c038d

Group: `/var/cache/man/local`. Source: `D1/in/raw/alma/members/5c8470dce9f98ad8363c038d.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat2`, `cat3`, `cat4`, `cat5`, `cat6`, `cat7`, `cat8`, `cat9`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-780bfe0f7d362c75eb56d406

Group: `/var/cache/man/nl`. Source: `D1/in/raw/alma/members/780bfe0f7d362c75eb56d406.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-5cf644dd117134e12b77c924

Group: `/var/cache/man/nodejs-22`. Source: `D1/in/raw/alma/members/5cf644dd117134e12b77c924.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-69b8c2ba43b71cf2d8f798a7

Group: `/var/cache/man/pl`. Source: `D1/in/raw/alma/members/69b8c2ba43b71cf2d8f798a7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-4376ee5df19252085496d484

Group: `/var/cache/man/pt`. Source: `D1/in/raw/alma/members/4376ee5df19252085496d484.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-d7a28f5267a9b12c628aa852

Group: `/var/cache/man/pt_BR`. Source: `D1/in/raw/alma/members/d7a28f5267a9b12c628aa852.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-56298adfb979a3b80ce30858

Group: `/var/cache/man/ro`. Source: `D1/in/raw/alma/members/56298adfb979a3b80ce30858.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-46fb2ca3c35ce1afd47ddbb1

Group: `/var/cache/man/ru`. Source: `D1/in/raw/alma/members/46fb2ca3c35ce1afd47ddbb1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-274fee2b26618777f9255394

Group: `/var/cache/man/sr`. Source: `D1/in/raw/alma/members/274fee2b26618777f9255394.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-2503dc1730804dfecdb8d724

Group: `/var/cache/man/sv`. Source: `D1/in/raw/alma/members/2503dc1730804dfecdb8d724.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-a4811a693584eae90c3d28d7

Group: `/var/cache/man/tr`. Source: `D1/in/raw/alma/members/a4811a693584eae90c3d28d7.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-834e5f8a746261c2243cebdc

Group: `/var/cache/man/uk`. Source: `D1/in/raw/alma/members/834e5f8a746261c2243cebdc.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat7`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-69609d1221cf1bc6f58303c6

Group: `/var/cache/man/zh_CN`. Source: `D1/in/raw/alma/members/69609d1221cf1bc6f58303c6.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat3`, `cat5`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-1432189929cf74a2d109c23e

Group: `/var/cache/man/zh_TW`. Source: `D1/in/raw/alma/members/1432189929cf74a2d109c23e.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `CACHEDIR.TAG`, `cat1`, `cat8`, `index.db`. Manual-page index cache, cache tag, or cache directory.
### alma-7d86889f65b808dd8613b8e2

Group: `/var/cache/swcatalog`. Source: `D1/in/raw/alma/members/7d86889f65b808dd8613b8e2.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cache`. Directory installation integrity and creation provenance are not established.
### alma-aba1546c2e9c220943384746

Group: `/var/cache/swcatalog/cache`. Source: `D1/in/raw/alma/members/aba1546c2e9c220943384746.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `en-US-local-metainfo.xb`, `en-US-os-catalog.xb`. Package origin, unchangedness, and source of this object are not established.
### alma-2174271ff38f7861452efe29

Group: `/var/lib`. Source: `D1/in/raw/alma/members/2174271ff38f7861452efe29.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `containers`, `gnome-remote-desktop`, `tpm2-tss`, `xfsdump`. Directory installation integrity and creation provenance are not established.
- **UNKNOWN**: `rpm`. Package origin, unchangedness, and source of this object are not established.
### alma-3a1d740e11a9be2a191c50ca

Group: `/var/lib/NetworkManager`. Source: `D1/in/raw/alma/members/3a1d740e11a9be2a191c50ca.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `NetworkManager-intern.conf`, `internal-<REDACTED>-ens3.lease`, `internal-<REDACTED>-ens4.lease`, `seen-bssids`, `timestamps`. Package origin, unchangedness, and source of this object are not established.
### alma-cda2c7e4fb8ebbb50cbaf960

Group: `/var/lib/alternatives`. Source: `D1/in/raw/alma/members/cda2c7e4fb8ebbb50cbaf960.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `arptables`, `cifs-idmap-plugin`, `ebtables`, `iptables`, `ld`, `libnssckbi.so.x86_64`, `man`, `man.7.gz`, `nc`, `print`, `soelim`. Package origin, unchangedness, and source of this object are not established.
### alma-3b373dfde415a87a7e49f99e

Group: `/var/lib/containers`. Source: `D1/in/raw/alma/members/3b373dfde415a87a7e49f99e.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `cache`, `storage`. Directory installation integrity and creation provenance are not established.
### alma-113a9ff0a771c44eb9d9a58c

Group: `/var/lib/containers/cache`. Source: `D1/in/raw/alma/members/113a9ff0a771c44eb9d9a58c.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `blob-info-cache-v1.sqlite`. Package origin, unchangedness, and source of this object are not established.
### alma-faede4c86a51922a042ae435

Group: `/var/lib/dbus`. Source: `D1/in/raw/alma/members/faede4c86a51922a042ae435.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `machine-id`. Package origin, unchangedness, and source of this object are not established.
### alma-58af51b4cabfca8a15294928

Group: `/var/lib/dnf`. Source: `D1/in/raw/alma/members/58af51b4cabfca8a15294928.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `history.sqlite`, `history.sqlite-shm`, `history.sqlite-wal`. Package origin, unchangedness, and source of this object are not established.
- **UNKNOWN**: `repos`. Directory installation integrity and creation provenance are not established.
### alma-3e476e65ef8545d7a3f649b3

Group: `/var/lib/dnf/repos`. Source: `D1/in/raw/alma/members/3e476e65ef8545d7a3f649b3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `appstream-0221375ef9ab2490`, `baseos-dd34f9106e98b1fa`, `crb-47f2899d10f358c8`, `extras-7dc392d1da0a70f9`. Directory installation integrity and creation provenance are not established.
### alma-932fdb1315bb706592853cda

Group: `/var/lib/dnf/repos/appstream-0221375ef9ab2490`. Source: `D1/in/raw/alma/members/932fdb1315bb706592853cda.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `countme`. Package origin, unchangedness, and source of this object are not established.
### alma-5f716212353f78037e531913

Group: `/var/lib/dnf/repos/baseos-dd34f9106e98b1fa`. Source: `D1/in/raw/alma/members/5f716212353f78037e531913.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `countme`. Package origin, unchangedness, and source of this object are not established.
### alma-11c94dae750e151910b50695

Group: `/var/lib/dnf/repos/crb-47f2899d10f358c8`. Source: `D1/in/raw/alma/members/11c94dae750e151910b50695.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `countme`. Package origin, unchangedness, and source of this object are not established.
### alma-09db4eab093aad8ecde95473

Group: `/var/lib/dnf/repos/extras-7dc392d1da0a70f9`. Source: `D1/in/raw/alma/members/09db4eab093aad8ecde95473.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `countme`. Package origin, unchangedness, and source of this object are not established.
### alma-a36cbb2fa50f46810f6c7eec

Group: `/var/lib/rpm-state`. Source: `D1/in/raw/alma/members/a36cbb2fa50f46810f6c7eec.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `kernel`. Directory installation integrity and creation provenance are not established.
### alma-07a31ec852761719538d8220

Group: `/var/lib/rsyslog`. Source: `D1/in/raw/alma/members/07a31ec852761719538d8220.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `imjournal.state`. Package origin, unchangedness, and source of this object are not established.
### alma-59641fe61e56d1bb77f4746d

Group: `/var/lib/selinux`. Source: `D1/in/raw/alma/members/59641fe61e56d1bb77f4746d.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `final`. Directory installation integrity and creation provenance are not established.
### alma-6417296a51f56e3cd1211479

Group: `/var/lib/selinux/targeted/active`. Source: `D1/in/raw/alma/members/6417296a51f56e3cd1211479.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `booleans.local`. Package origin, unchangedness, and source of this object are not established.
### alma-19a6183fd171be026f4265f1

Group: `/var/lib/selinux/targeted/active/modules`. Source: `D1/in/raw/alma/members/19a6183fd171be026f4265f1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `100`, `200`, `400`, `disabled`. Directory installation integrity and creation provenance are not established.
### alma-8c6b67426c96b2a320e74e9c

Group: `/var/lib/selinux/targeted/active/modules/200`. Source: `D1/in/raw/alma/members/8c6b67426c96b2a320e74e9c.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `flatpak`, `passt`, `passt-repair`, `pasta`, `pesto`. Directory installation integrity and creation provenance are not established.
### alma-f4a3cf975b99eb987562c0bf

Group: `/var/lib/selinux/targeted/active/modules/200/adcli`. Source: `D1/in/raw/alma/members/f4a3cf975b99eb987562c0bf.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-37a6b00f2a2f30cc17fdc85c

Group: `/var/lib/selinux/targeted/active/modules/200/cockpit`. Source: `D1/in/raw/alma/members/37a6b00f2a2f30cc17fdc85c.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-4a24f8c9ddf33e66bb90542b

Group: `/var/lib/selinux/targeted/active/modules/200/container`. Source: `D1/in/raw/alma/members/4a24f8c9ddf33e66bb90542b.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-c4ce799d3d6273bd56f0ebcf

Group: `/var/lib/selinux/targeted/active/modules/200/flatpak`. Source: `D1/in/raw/alma/members/c4ce799d3d6273bd56f0ebcf.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-2165e4c349c9bf3c1ed63d63

Group: `/var/lib/selinux/targeted/active/modules/200/passt`. Source: `D1/in/raw/alma/members/2165e4c349c9bf3c1ed63d63.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-e0bc1aea2a636f3546e09751

Group: `/var/lib/selinux/targeted/active/modules/200/passt-repair`. Source: `D1/in/raw/alma/members/e0bc1aea2a636f3546e09751.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-2fc3a91ad86515e195f303dd

Group: `/var/lib/selinux/targeted/active/modules/200/pasta`. Source: `D1/in/raw/alma/members/2fc3a91ad86515e195f303dd.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-dfbbec8c0f7d667d72597960

Group: `/var/lib/selinux/targeted/active/modules/200/pesto`. Source: `D1/in/raw/alma/members/dfbbec8c0f7d667d72597960.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-162f076cc6f370eac2474fcd

Group: `/var/lib/selinux/targeted/active/modules/200/smartmon`. Source: `D1/in/raw/alma/members/162f076cc6f370eac2474fcd.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `cil`, `hll`, `lang_ext`. Package origin, unchangedness, and source of this object are not established.
### alma-3e316174c4e21669b4145ca9

Group: `/var/lib/systemd`. Source: `D1/in/raw/alma/members/3e316174c4e21669b4145ca9.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `ephemeral-trees`, `pstore`, `timers`. Directory installation integrity and creation provenance are not established.
### alma-97991ce4dba34a3aaa3bb5e3

Group: `/var/lib/systemd/timers`. Source: `D1/in/raw/alma/members/97991ce4dba34a3aaa3bb5e3.tsv`. Decision: **UNKNOWN**.

Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.

- **UNKNOWN**: `stamp-fstrim.timer`, `stamp-fwupd-refresh.timer`, `stamp-logrotate.timer`, `stamp-plocate-updatedb.timer`, `stamp-raid-check.timer`. Package origin, unchangedness, and source of this object are not established.
### alma-0e64c650135e46b3d35386fa

Group: `/var/lib/tpm2-tss`. Source: `D1/in/raw/alma/members/0e64c650135e46b3d35386fa.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `system`. Directory installation integrity and creation provenance are not established.
### alma-ff39baa8553d2e0ec7050733

Group: `/var/lib/tpm2-tss/system`. Source: `D1/in/raw/alma/members/ff39baa8553d2e0ec7050733.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `keystore`. Directory installation integrity and creation provenance are not established.
### alma-c6ced98e5cc2963402a27fa1

Group: `/var/log`. Source: `D1/in/raw/alma/members/c6ced98e5cc2963402a27fa1.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `anaconda`, `boot.log`, `cron`, `firewalld`, `maillog`, `messages`, `secure`, `spooler`. Persistent system or installer logs and their directories.
### alma-90a69199f6f833ef299fff53

Group: `/var/log/anaconda`. Source: `D1/in/raw/alma/members/90a69199f6f833ef299fff53.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `anaconda.log`, `dbus.log`, `dnf.librepo.log`, `hawkey.log`, `journal.log`, `lorax-packages.log`, `lvm.log`, `packaging.log`, `program.log`, `storage.log`, `syslog`. Persistent system or installer logs and their directories.
### alma-babd26103390768dd5892c68

Group: `/var/log/audit`. Source: `D1/in/raw/alma/members/babd26103390768dd5892c68.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `audit.log`. Persistent system or installer logs and their directories.
### alma-27e05bc344af2c7816d34b94

Group: `/var/log/tuned`. Source: `D1/in/raw/alma/members/27e05bc344af2c7816d34b94.tsv`. Decision: **RECORD**.

Members are documented working data or generated data directories recorded during program operation, not code or selected settings.

- **RECORD**: `tuned-ppd.log`, `tuned.log`. Persistent system or installer logs and their directories.
### alma-a1d8fbf991d4ce2092ff5ba2

Group: `/var/spool/at`. Source: `D1/in/raw/alma/members/a1d8fbf991d4ce2092ff5ba2.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `.SEQ`. Package origin, unchangedness, and source of this object are not established.
### alma-466a8b28ab228265f8971efb

Group: `/var/spool/mail`. Source: `D1/in/raw/alma/members/466a8b28ab228265f8971efb.tsv`. Decision: **UNKNOWN**.

Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.

- **UNKNOWN**: `user`. Package origin, unchangedness, and source of this object are not established.
### alma-f2c9693d472bd5fda1ddfd45

Group: `/var/tmp`. Source: `D1/in/raw/alma/members/f2c9693d472bd5fda1ddfd45.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `systemd-private-fc33f2ec36db4febbb440b973d327901-ModemManager.service-fy4qqe`, `systemd-private-fc33f2ec36db4febbb440b973d327901-NetworkManager.service-qKDIug`, `systemd-private-fc33f2ec36db4febbb440b973d327901-chronyd.service-bbaGB4`, `systemd-private-fc33f2ec36db4febbb440b973d327901-dbus-broker.service-YPk0sV`, `systemd-private-fc33f2ec36db4febbb440b973d327901-irqbalance.service-vlqutZ`, `systemd-private-fc33f2ec36db4febbb440b973d327901-polkit.service-Dd8IU8`, `systemd-private-fc33f2ec36db4febbb440b973d327901-rtkit-daemon.service-mOyLzm`, `systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-hostnamed.service-HCSToy`, `systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-logind.service-C0Vygm`, `systemd-private-fc33f2ec36db4febbb440b973d327901-upower.service-bL3XPT`. Directory installation integrity and creation provenance are not established.
### alma-5f3370122ce2292de1c2d1b6

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-ModemManager.service-fy4qqe`. Source: `D1/in/raw/alma/members/5f3370122ce2292de1c2d1b6.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-928f72f88b5ea4a687abf222

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-NetworkManager.service-qKDIug`. Source: `D1/in/raw/alma/members/928f72f88b5ea4a687abf222.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-356ac3a1673644c1836ea984

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-chronyd.service-bbaGB4`. Source: `D1/in/raw/alma/members/356ac3a1673644c1836ea984.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-7b2420100a53ea24ff3825e2

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-dbus-broker.service-YPk0sV`. Source: `D1/in/raw/alma/members/7b2420100a53ea24ff3825e2.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-c6b9933d5da3c0142b501fab

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-irqbalance.service-vlqutZ`. Source: `D1/in/raw/alma/members/c6b9933d5da3c0142b501fab.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-a7a98e456112106bcaa35153

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-polkit.service-Dd8IU8`. Source: `D1/in/raw/alma/members/a7a98e456112106bcaa35153.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-e915028e0f0ac62c93d5e2c3

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-rtkit-daemon.service-mOyLzm`. Source: `D1/in/raw/alma/members/e915028e0f0ac62c93d5e2c3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-67d62609129d87298c3f0ed3

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-hostnamed.service-HCSToy`. Source: `D1/in/raw/alma/members/67d62609129d87298c3f0ed3.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-c7a0ddbfe7198d5fabcb10f1

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-systemd-logind.service-C0Vygm`. Source: `D1/in/raw/alma/members/c7a0ddbfe7198d5fabcb10f1.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.
### alma-dbdbdb717c357aa3a860df23

Group: `/var/tmp/systemd-private-fc33f2ec36db4febbb440b973d327901-upower.service-bL3XPT`. Source: `D1/in/raw/alma/members/dbdbdb717c357aa3a860df23.tsv`. Decision: **UNKNOWN**.

Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.

- **UNKNOWN**: `tmp`. Directory installation integrity and creation provenance are not established.

## Final validation

Validated exact assigned input/output ID set and count, uniqueness, all 15 permitted decision values, sentence IDs, field lengths, and complete member counts.

- INSTALLED-PACKAGE: 489
- MIXED: 108
- RECORD: 561
- RUNTIME: 135
- SETTING-OWN: 1
- UNKNOWN: 353


# Completed partition 2: rules and manual checks

# L1 non-package classification notes

Scope: exactly 3,044 L1 rows other than packages, from `D1/in/part-alma.tsv`. The output is `part-alma.2.tsv`. Classification uses object identity from the retained query, not its collector class label. Package integrity comes from (not published: over 20 MB); runtime filesystem metadata comes from (not published: over 20 MB). Packages remain separate rows assigned elsewhere.

## Deciding sentences

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Documentation used to identify objects

- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.” This distinguishes missing-unit references from installed files. Timer listings include live deadlines.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “A unit file is a plain text ini-style file”. Unit files supply values; executable content is not inferred from ExecStart values. The documented search order selects local overrides before vendor files.
- https://polkit.pages.freedesktop.org/polkit/polkit.8.html — “Actions are defined by applications.” Each captured action identifier was matched to an actual action element in the retained policy XML; all 299 identifiers matched.
- https://docs.kernel.org/filesystems/sysfs.html — “sysfs is a RAM-based filesystem initially based on ramfs.” The module and driver query scripts enumerate sysfs registrations, not stored module binaries.
- https://firewalld.org/documentation/configuration/runtime-versus-permanent.html — “The runtime configuration will be lost with a firewalld service stop.” The nft query reports live kernel tables, chains and rules, not the persistent files.
- https://docs.podman.io/en/latest/markdown/podman.1.html — “Simple management tool for pods, containers and images”. This description does not by itself establish an installer under S8.1-4.
- https://docs.podman.io/en/latest/markdown/podman-start.1.html — “Start one or more containers using container IDs or names as input.” Exited containers remain startable; they are not merely historical log records.
- https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html — “NetworkManager is based on the concept of connection profiles that contain network configuration”. Stored connection files provide values, not executable source code.

## Rules applied by the script

`part-alma.2.classify.py` appends missing ids and flushes every row. Corrections discovered during checking were confined to two generated SSH aliases: their explicit runtime filesystem records establish RUNTIME. No sampling substitutes for member or integrity joins.

- **setting-origin:** For account, group or service values, S8.2-13 establishes settings. Neither presence nor a familiar system name establishes whether the current value is a package default or a later choice. S8.2-17 then leaves the recording line factually unknown. The aggregate passwd/group files are changed; this does not prove individual records changed. Existing missing-unit references and the locally enabled authentication service are separate cases.
- **unchanged-package:** If the selected actual file, or XML action's containing file, has an unchanged package-file entry, S8.2-6–8 decide at question one. S8.2-16 covers it through its package. This includes code-like rules and default values; no settings clarification overrides question order. The script checks exact paths, unit search precedence and XML identifiers.
- **unit-origin:** The remaining ten persistent unit aliases lack reliable facts on default creation versus later configuration; S8.2-7 and S8.2-17 require UNKNOWN. A target's unchanged bytes do not prove that a separately created alias was received with a package.
- **runtime-process:** Every process is explicitly covered by S8.2-5, regardless of whether its creator is identified. Where executable integrity is known unchanged, the creator is INSTALLED-PACKAGE. Missing executable identity or integrity leaves the creator UNKNOWN, without changing the process's RUNTIME decision.
- **runtime-kernel:** The captured module names and driver paths are sysfs registrations created by the kernel during execution. S8.2-5 gives RUNTIME. The retained kernel image integrity is unknown; no unchanged-image assumption is made for its creator decision.
- **runtime-firewall:** nft's live tables, chains and rules exist in the running kernel. S8.2-5 gives RUNTIME; the observed owning tables distinguish firewalld from netavark, whose program files are unchanged packaged content. Persistent policy is not identified with these live objects.
- **runtime-manager:** A missing unit loaded only as an in-memory reference, or a unit file positively identified on a runtime filesystem, exists only during execution. S8.2-5 gives RUNTIME. The reasons identify systemd, its autostart generator or the SSH generator and the creator decision; unknown SSH generator provenance remains explicit.

## Manual ten-row checks per rule

For each list below, the retained record and the rule's deciding predicate were examined. Account rows have complete identity records but no individual default provenance. Missing-unit rows explicitly say not-found. Packaged unit rows join unchanged entries. Unit aliases have persistent links without creation provenance. Firewall entries are live table/chain objects. Process records contain a PID and the stated executable or unknown. Kernel entries came from the sysfs enumeration.

### setting-origin

alma-1270901ac803f087770d4a03, alma-18ded40433b6af01a8b11595, alma-09fe3e2ff1af708b3e2f3cc4, alma-3a9032548c4616d565f24feb, alma-b2d0097b60aae99ae9ddedac, alma-2306394bc0f92c33d49a6439, alma-448646fafcede98990f077af, alma-986feb2c79e9e648fbc39e33, alma-013789c485cfe6ad406fb020, alma-adb91fb58b73a818d97424ca

### unchanged-package

alma-b6d46ec30f2a5544c8f034eb, alma-dd2e571f5cdae7a0aea00765, alma-603e2163557a3fa31b3f1153, alma-395e07fd1415587cadf07f46, alma-fc8e6f4b3aebd52ec58570e2, alma-2ba8c538abcd0c153252e88c, alma-c719ee65ca6427a425f4f522, alma-751b49f4326ea93b25b6bb98, alma-3b2e8e00da65dbcf24bc87bd, alma-53fa364e2cf166bce33a9d60

### unit-origin

alma-d33e0438b1ccb4129ae9ab25, alma-e72dbb895ddd9bd0b38bf52a, alma-a4b5dace6048c24e81811995, alma-6a26dbb966bac7d9fb0abda6, alma-4c81a69e31ead4120098f60b, alma-7cca1c6906c99a886e86a692, alma-37c4765f1bc3df9c50c7463a, alma-5404dea0fe8c5190436c31c2, alma-b40629803b933a2b052a5d96, alma-0bd28f6010aed40c90735f95

### runtime-process

alma-9a469fe77b60b9eee6cbc515, alma-75112624ed82d0e836f2ee39, alma-77e5d61dde1f088c197037f2, alma-9df7398e97f9cabd55360708, alma-3e28697c90e169b6c550c7db, alma-777296add37822d2eea78d3e, alma-a1c243a655ffb692916a77b1, alma-bb2694c887ad035a89e32d81, alma-fd6b39a52e45b2be95e932c9, alma-745b2a282c25d73ae65778f6

### runtime-kernel

alma-5af8cb1ac7d4e30d3d553dfd, alma-ca5ea4d08e696ec77a27abca, alma-560aa70d01e89fade6df1603, alma-a9b6c7abd3408634d9f2b559, alma-0b81fc9ad7e1a078a37e337f, alma-9de8441033d886077fa55e16, alma-e2e9fc511c77b1af2b5f829d, alma-c405862ece732c9908e94b15, alma-d3fafbd1cca07dee22d1c425, alma-b0fee5f436b48c4afccef587

### runtime-firewall

alma-29c00ab03689c5595ac65e00, alma-0c695f336bb265c216f7580d, alma-46c44d88c85808a30abe4396, alma-5d2eac647b1caffc0399f7fb, alma-b066134477290f823c90fa58, alma-4490b98ebd1bb292cf7be570, alma-0e03ad75fcfbc172e17db3ed, alma-aebda2823cfbe5da62e9eaec, alma-d0d13c64d97968b31767e4a5, alma-2f69e065457643db27086f00

### runtime-manager

alma-fab6357cc46e0afe3e20300f, alma-1be76eae4b11dbcdae07b4eb, alma-4129e3f409a79b3d38a21046, alma-95ff055b8b66bf4cbca9f279, alma-29a28d1283ab2c445bd3ccaf, alma-c0411eed574d1c9e19fb3d05, alma-7281b2c2ab87affb0fa1d77d, alma-fa682c4e155d67c2da71234d, alma-62edff09e6688088a39f7ac8, alma-dbfa31eb16cc5f0a78cfaf37

Additional cross-kind checks: all access-policy files were joined to the package-file table; only the local sudoers grant lacked an unchanged package match. All 299 policy identifiers matched XML action elements. Generated autostart units had runtime persistence. The two generated SSH aliases also had runtime persistence and were corrected before completion. The entire group record, including membership, was considered; empty named membership is not evidence that a group is inert.

## Individually decided objects

The nine timer entries describe future live deadlines; systemd creates those schedules. The nine socket entries omit owning executables, so creator UNKNOWN is explicit. Four sudo report headings are textual program output and RECORD. Two sudo default-value rows and two broad permission rows match unchanged packaged sudoers; the passwordless local grant is SETTING-OWN, as is its source file. The two stopped-container rows refer to the same retained executable instance from the same image and are PROGRAM-DERIVED. Both image rows identify the same executable image, already used successfully, and are PROGRAM-OWN. This is duplicate inventory representation, not duplicated ids.

NetworkManager's added connection UUIDs in `D1/in/control/alma/actions-logs/network_connection.log` match the two local profile rows and their persistent files: four SETTING-OWN rows. `D1/in/control/alma/actions-logs/user_service.stderr` establishes the locally enabled authentication service: its service and file rows are SETTING-OWN. No local path is reproduced here. Initial ethernet profile origin is unknown; the loopback profile listing does not establish persistent versus automatic creation. The unchanged packaged supplicant file is INSTALLED-PACKAGE.

## Validation

The assigned input ids and output ids have equal sets and counts, each once. Each decision is allowed, every row has six fields, all sentence ids exist, and word limits hold. Counts follow in the completion record. This is mechanical verification, not independent adjudication.

## Final table formatting audit

Mixed-group reasons were shortened without changing any member decision. Where member type exactly determines the partition, the reason names all file/directory members by type. Otherwise it names every member of the smaller partition and assigns all other members to the second decision. This avoids counting long comma-glued member lists as a single word. The complete named member partitions above remain authoritative evidence for every group.

Mechanical verification checks the exact header, identical input/output id sets and counts, unique ids, all fifteen allowed decisions, valid sentence ids, six fields, and the 15/30-word limits. No completion marker is emitted until the review stage is complete.

## Unit-file identity checked during review

The retained command in `D1/in/raw/alma/raw/0197-unit-file.sh` is `systemctl --no-pager --no-legend list-unit-files --type=service,timer`. The official systemctl documentation identifies its objects as installed unit files and presents enablement as accompanying state. Enabling and disabling operate on separate symlinks. Consequently an unchanged vendor file remains INSTALLED-PACKAGE under the first question even when its enablement differs from the preset. This does not classify the separate enablement object as unchanged package content.

The four challenged unit-file ids were checked against this distinction: `alma-5979198b1523e9e8195df68e`, `alma-15147e7885ba0fa16cd90853`, `alma-09a5589fa3207b4f96928577`, and `alma-681a12c25d037c20fee1a21b`. For example, the vgauthd enablement link is separately included in `alma-1e33fe58f57b8be4bcbaadc4` with unresolved provenance. The remount service's runtime links appear separately in `alma-904ac6b1c3dde89ef0c1ae58` and `alma-a59e8fb1350c7f27463b5297` as RUNTIME. The review withdrew the proposed unit-file changes after checking these identities and separate objects. No decision changed.

Source: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html (list-unit-files, enable, disable).
