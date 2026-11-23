# Classification c1, part 1
The final table contains one decision for every input row. Classification used only Section 2.2 and the “Whether an object must be recorded” indicator in Section 3. The factual sources were the supplied evidence, A3R/in/raw/lived, the permitted build description and public program documentation. Inventory words such as “recorded”, “closure”, “proxy” and “works” were not taken as decisions. No removal experiment was performed. No other classification, comparison or adjudication was read.

Subtree rows were expanded against (not published: direct evidence over 2 MB) using their original kind and path prefix, as REDUCTION.md specifies. MIXED identifies different member decisions; UNKNOWN identifies missing factual evidence, whereas HOLE identifies a boundary or conflict in the fixed text. Questions about declaration format, state transfer, timing of edits or rollback were not used as holes.

Completed rows were appended and flushed. The disjoint executable, package, system, runtime, source-tree and persistent-state parts were merged by missing ID. In-session factual corrections preserve the original and corrected rows in part-1.corrections.jsonl. That audit and the scripts retain intermediate wording; part-1.tsv and the explanations here are authoritative.

The main stored-object assignment comprised 1,275 rows. The rules below cover the explicitly homogeneous subsets; the remaining main-assignment objects were inspected row by row. The component notes reproduced below contain the other assignments’ rules, manual checks and individual explanations. A bounded independent review checked ten examples of each main rule and additional individual rows; its findings and follow-up are in part-1.review.md.

## Exact deciding text
- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-8** Consequences of this rule that we fix explicitly:
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Main stored-object rules and manual checks

### Go build output cache (257 rows; `cache-go`)

NOT under S2.2-5. These are the standard go-build hash directories and their cached build outputs. Removing a reusable build result requires rebuilding it; it does not remove the build inputs or the Go tool. This rule is restricted to go-build, not the module source tree or installed binaries.

Manual check: The ten expanded rows contain the cache root or its hash buckets, with cached output/action entries rather than installed command paths.

- `5838877df3655d1d057b4054` — `guest-home/.cache/go-build`; final decision NOT.
- `ba46d887effa1e9130eb29e1` — `guest-home/.cache/go-build/00`; final decision NOT.
- `59c8e5f4edd07fe31b73fdb8` — `guest-home/.cache/go-build/01`; final decision NOT.
- `46cdbf570275e355f91ae07c` — `guest-home/.cache/go-build/02`; final decision NOT.
- `e7b813188cbec4870d2ffd78` — `guest-home/.cache/go-build/03`; final decision NOT.
- `3b81e1fc6a7467637ddf08d7` — `guest-home/.cache/go-build/04`; final decision NOT.
- `efd406897705f309fbae9f3b` — `guest-home/.cache/go-build/05`; final decision NOT.
- `bd78ecfa14e9bf612475acc3` — `guest-home/.cache/go-build/06`; final decision NOT.
- `4501dd6e42605ba11e3d7fa9` — `guest-home/.cache/go-build/07`; final decision NOT.
- `928e45d2506ab0d3f63f0dfb` — `guest-home/.cache/go-build/08`; final decision NOT.

### Mesa shader compilation cache (102 rows; `cache-mesa`)

NOT under S2.2-5. The mesa_shader_cache_db entries hold regenerable graphics compilation results and lookup indexes. The documentation permits disabling this disk cache while retaining rendering. These shader results are not treated as unrestricted scripts running with a host interpreter’s own rights.

Manual check: The ten rows contain the database cache root or numbered cache parts; mesa_cache.db and mesa_cache.idx are the observed file families.

- `83d82b45f8607deef00a23f6` — `guest-home/.cache/mesa_shader_cache_db`; final decision NOT.
- `d1be8f86d0a36f6e9805c0a1` — `guest-home/.cache/mesa_shader_cache_db/part0`; final decision NOT.
- `6c66230269177479f8129253` — `guest-home/.cache/mesa_shader_cache_db/part1`; final decision NOT.
- `344cf6842cd8463e4046df4c` — `guest-home/.cache/mesa_shader_cache_db/part10`; final decision NOT.
- `22ffbcfbf12aeb4516d8f828` — `guest-home/.cache/mesa_shader_cache_db/part11`; final decision NOT.
- `c16ccbf357c5320b47f98fd3` — `guest-home/.cache/mesa_shader_cache_db/part12`; final decision NOT.
- `33725f15c624d5a33587ae7e` — `guest-home/.cache/mesa_shader_cache_db/part13`; final decision NOT.
- `de7d4279bc86ca62865026f1` — `guest-home/.cache/mesa_shader_cache_db/part14`; final decision NOT.
- `e2924486efbc1c054fb61555` — `guest-home/.cache/mesa_shader_cache_db/part15`; final decision NOT.
- `5f97e8f20c717217b638a695` — `guest-home/.cache/mesa_shader_cache_db/part16`; final decision NOT.

### Manual-page caches (26 rows; `cache-man`)

NOT under S2.2-5. The /var/cache/man rows hold generated manual indexes, cache tags and formatted-page cache directories. Manual source content remains outside these rows; the cache only avoids repeated indexing or formatting.

Manual check: The ten rows were expanded and checked for index.db, CACHEDIR.TAG and manual-cache directories, not manual source installation files.

- `4510afc64020ce965c69c93a` — `/var/cache/man`; final decision NOT.
- `8d3198283b0bc001a8363861` — `/var/cache/man/cs`; final decision NOT.
- `d5d756c7be695e8e3c3240e3` — `/var/cache/man/da`; final decision NOT.
- `775c7e0626a8d2764f6561aa` — `/var/cache/man/de`; final decision NOT.
- `0c14914a1646a594dd64c510` — `/var/cache/man/es`; final decision NOT.
- `359b5c84d186097c4737d4f3` — `/var/cache/man/fi`; final decision NOT.
- `d93b8cfda4b3fa40f11328c7` — `/var/cache/man/fr`; final decision NOT.
- `ecaea5af3e3b04c0aadb97f4` — `/var/cache/man/hr`; final decision NOT.
- `67cab6a3b21ee18171e913bf` — `/var/cache/man/hu`; final decision NOT.
- `cfbbb1277d81eda3111f05d7` — `/var/cache/man/id`; final decision NOT.

### Shell plugin groups containing code and documents (372 rows; `shell-with-docs`)

MIXED under S2.2-4, S2.2-10 and S2.2-13. Actual .zsh programs and completion functions execute with shell rights and are MUST; README/manual/image content is NOT. The selector verifies both families in the expanded group, rather than using the inventory’s label. This is a rule for this inspected plugin set, not a rule that all plugins in any program are unrestricted code.

Manual check: The ten groups are 1password, alias-finder, aliases, ansible, ant, apache2-macports, appsignal-cli, arcanist, archlinux and arduino-cli. Each contains executable shell definitions and explanatory documents.

- `ab4e48545791db0d53dc71b0` — `guest-home/.oh-my-zsh/plugins/1password`; final decision MIXED.
- `lived-t9b2b9a2814` — `guest-home/.oh-my-zsh/plugins/alias-finder`; final decision MIXED.
- `63b7ee6e4fbfe5162d1d10d4` — `guest-home/.oh-my-zsh/plugins/aliases`; final decision MIXED.
- `02509ece652faa30d530a089` — `guest-home/.oh-my-zsh/plugins/ansible`; final decision MIXED.
- `362aab6721c560fe6916a612` — `guest-home/.oh-my-zsh/plugins/ant`; final decision MIXED.
- `56e55538f39bb25c82bccbb7` — `guest-home/.oh-my-zsh/plugins/apache2-macports`; final decision MIXED.
- `1e034c102785466f86ebbed4` — `guest-home/.oh-my-zsh/plugins/appsignal-cli`; final decision MIXED.
- `c74937c1adc7b0e5b9d636c7` — `guest-home/.oh-my-zsh/plugins/arcanist`; final decision MIXED.
- `29e5ea27d8d538454e25a803` — `guest-home/.oh-my-zsh/plugins/archlinux`; final decision MIXED.
- `b6ce7dc989ed90fe3de8094d` — `guest-home/.oh-my-zsh/plugins/arduino-cli`; final decision MIXED.

### Editor Lisp sources paired with compiled copies (41 rows; `lisp-source-bytecode`)

MIXED under S2.2-5 and S2.2-10. The .el source is same-rights editor code, hence MUST. The corresponding regenerable .elc is both same-rights code and a faster compiled copy, hence HOLE: cache exemption and code requirement give opposite answers without precedence. Only groups containing both forms enter this rule. The source-only group at stored index 519 was removed from the rule and decided MUST individually.

Manual check: Each of the ten inspected member lists contains both .el source and corresponding .elc bytecode; groups containing manuals or other non-Lisp members were handled individually.

- `93a93428a9d00a2b2aac9e6f` — `guest-home/.emacs.d/elpa/ace-window-20220911.358`; final decision MIXED.
- `5959a2218f288946d9133588` — `guest-home/.emacs.d/elpa/ag-20201031.2202`; final decision MIXED.
- `eebd64d14c879499f989c089` — `guest-home/.emacs.d/elpa/avy-20241101.1357`; final decision MIXED.
- `8bd5707cf2447e2b1dada846` — `guest-home/.emacs.d/elpa/browse-kill-ring-20260503.1620`; final decision MIXED.
- `7f3effb4817586bb43bf25b7` — `guest-home/.emacs.d/elpa/cmake-mode-20261119.1320`; final decision MIXED.
- `ac57a7e849c4d7b15f209c04` — `guest-home/.emacs.d/elpa/cond-let-20261001.1537`; final decision MIXED.
- `38cc2f41f8f8aac99bb9fbcd` — `guest-home/.emacs.d/elpa/consult-20261004.957`; final decision MIXED.
- `e21b280e5634bcf817e00a27` — `guest-home/.emacs.d/elpa/crux-20261002.1340`; final decision MIXED.
- `b57acba86305d76781092c20` — `guest-home/.emacs.d/elpa/diff-hl-20261001.135`; final decision MIXED.
- `d6bd932b0be5d3172a03dc9b` — `guest-home/.emacs.d/elpa/diminish-20260904.1820`; final decision MIXED.

### Regenerable Python bytecode (39 rows; `python-bytecode`)

HOLE under S2.2-5 and S2.2-10. These __pycache__ groups contain compiled copies used to accelerate module loading, while the interpreter executes their instructions with its rights. The text states both the cache exemption and unrestricted-code requirement without precedence for their overlap.

Manual check: The ten lists were checked within the Python 3.13, __phello__, __pycache__, _pyrepl, asyncio, collections, concurrent, ctypes, curses and dbm paths. Every stored member is in __pycache__.

- `bd26f6d902ca7e032cf494a9` — `/usr/lib/python3.13`; final decision HOLE.
- `lived-t913be4d2c3` — `/usr/lib/python3.13/__phello__`; final decision HOLE.
- `66398dc44267754147f1a614` — `/usr/lib/python3.13/__pycache__`; final decision HOLE.
- `lived-tc5242e687e` — `/usr/lib/python3.13/_pyrepl`; final decision HOLE.
- `lived-td2cb3c5e97` — `/usr/lib/python3.13/asyncio`; final decision HOLE.
- `lived-ta4abd40fce` — `/usr/lib/python3.13/collections`; final decision HOLE.
- `lived-ta2011e6fc2` — `/usr/lib/python3.13/concurrent`; final decision HOLE.
- `lived-t4ca37c4992` — `/usr/lib/python3.13/ctypes`; final decision HOLE.
- `lived-t020ed9822e` — `/usr/lib/python3.13/curses`; final decision HOLE.
- `lived-td982437c2e` — `/usr/lib/python3.13/dbm`; final decision HOLE.

### Explicitly inspected retrieval and lookup caches (37 rows; `cache-retrieval-index`)

NOT under S2.2-5. The enumerated download-response and discovery-index rows retain results that can be fetched or scanned again. This rule covers only the named inspected Flatpak, font, GStreamer, HTTP, package-download and similar cache rows. Cached executable scripts and bytecode were excluded and decided separately; a path merely named cache was insufficient.

Manual check: The ten checks cover Flatpak system-cache, fontconfig, GStreamer registry, browser HTTP, reference-manager download and pip cache entries, including cache-directory tags. Their recorded role is reuse of retrieved or scanned material.

- `1993f096f5ded6b00e6061ca` — `guest-home/.cache/flatpak`; final decision NOT.
- `f722e3ffcc608fb2cd788463` — `guest-home/.cache/fontconfig`; final decision NOT.
- `40dd358fd75f344925b26f0b` — `guest-home/.cache/gstreamer-1.0`; final decision NOT.
- `fd686e2bc4308668549dd947` — `guest-home/.cache/mozilla`; final decision NOT.
- `lived-t7d9b1ee6b7` — `guest-home/.cache/mozilla/firefox`; final decision NOT.
- `52e2f6dbb440bef6ca9cd9db` — `guest-home/.cache/pip`; final decision NOT.
- `lived-t9ed8a8e8da` — `guest-home/.cache/pip/http-v2`; final decision NOT.
- `b5ccef452dbb826d064592cb` — `guest-home/.cache/pipx`; final decision NOT.
- `5d95c2800dd29e62451372ab` — `guest-home/.cache/zotero`; final decision NOT.
- `lived-t9f0d8603f4` — `guest-home/.cache/zotero/zotero`; final decision NOT.

### Passive past-event records (23 rows; `history`)

NOT under S2.2-6. The enumerated logs, telemetry counts, crash descriptions and saved event records describe past events. This rule excludes active control files, authentication history whose enforcement is unknown, and persistent trust checkpoints. The crash-report group containing crashping.pid and the empty .gitkeep-only log directory were removed and decided individually.

Manual check: The ten checks cover Go telemetry counts and logs, editor crash records, npm/pipx logs, and monitoring logs. Their expanded member names and inventory roles identify past records, with no control-file member folded into these samples.

- `lived-ta2ca521d61` — `guest-home/.config/Code/logs`; final decision NOT.
- `7e2570886b92e6dace049d7b` — `guest-home/.config/go`; final decision NOT.
- `lived-ta8fe4cecbe` — `guest-home/.config/go/telemetry`; final decision NOT.
- `55c83d3fcf40dd8be37b58cc` — `guest-home/.config/mozilla`; final decision NOT.
- `lived-tf0bfdb6bd0` — `guest-home/.config/mozilla/firefox-esr`; final decision NOT.
- `lived-t5f97cf4182` — `guest-home/.local/state/pipx`; final decision NOT.
- `4b696a72838384d18fd29e12` — `guest-home/.npm/_logs`; final decision NOT.
- `lived-t8d443b9174` — `/opt/netdata/var/log`; final decision NOT.
- `98a2002129b01e4bd21550ae` — `guest-root/.config`; final decision NOT.
- `d263fa44f0d6f58ef22018cd` — `guest-root/.config/go`; final decision NOT.

### Generated shared MIME lookup descriptions (14 rows; `mime-generated`)

HOLE under S2.2-2 and S2.2-4. These XML and lookup entries are generated MIME database descriptions. One reading treats type descriptions as exempt database content; another treats their removal as loss of recognition operations. The text does not specify the boundary between unavailable descriptive content and unavailable operation here. The final rationale does not depend on when regeneration happens and does not assume that all generated files are slower-only caches.

Manual check: The ten rows cover the generated MIME lookup root and media/type XML groups. The specification explicitly lists MEDIA/SUBTYPE.xml among update-mime-database outputs, distinct from packages input files.

- `a4de6292d1e78167decc7081` — `/usr/share/mime`; final decision HOLE.
- `4aba607ff59c3ee376310758` — `/usr/share/mime/application`; final decision HOLE.
- `4ff815d792c6f07c0e70cdd2` — `/usr/share/mime/audio`; final decision HOLE.
- `a1bc9af2c8b24e04764d16e0` — `/usr/share/mime/chemical`; final decision HOLE.
- `2c84f6f7d6b126564d10c278` — `/usr/share/mime/font`; final decision HOLE.
- `946c59a84dd618138088be86` — `/usr/share/mime/image`; final decision HOLE.
- `a3a29542d4b538e850acb99b` — `/usr/share/mime/inode`; final decision HOLE.
- `7d4c3c7f666b1008ee71489d` — `/usr/share/mime/message`; final decision HOLE.
- `a57811114eec1362d29f52a8` — `/usr/share/mime/model`; final decision HOLE.
- `f4785d34ecdd63e5d9727007` — `/usr/share/mime/multipart`; final decision HOLE.

## Factual documentation for the main assignment

These short passages support the functional distinctions; decisions still follow the cited hypothesis sentences. Where the table cites raw membership, these sources explain the corresponding file family.

- [Go command](https://pkg.go.dev/cmd/go): “The go command caches build outputs for reuse in future builds.” This is the go-build cache rule, distinct from module source/cache mixtures.
- [Mesa environment variables](https://docs.mesa3d.org/envvars.html): “if set to `true`, disables the on-disk shader cache.” The page identifies the compiled shader cache and its database variants.
- [mandb](https://manpages.debian.org/trixie/man-db/mandb.8.en.html): “mandb - create or update the manual page index caches”. This establishes the /var/cache/man index role.
- [Oh My Zsh customization](https://github.com/ohmyzsh/ohmyzsh/wiki/Customization): “your redefinitions only take effect after the plugin has been loaded by `source`-ing its definition file.” Thus these shell plugin definitions are executed code, not only read values.
- [Python compiled modules](https://docs.python.org/3/tutorial/modules.html#compiled-python-files): “To speed up loading modules, Python caches the compiled version of each module”. The documented __pycache__ role supports both sides of the cache/code overlap.
- [Emacs byte compilation](https://www.gnu.org/software/emacs/manual/html_node/eintr/Byte-Compiling.html): “Byte compiled code runs faster than humanly readable code.” The source and byte-compiled forms remain editor-executed code.
- [pip caching](https://pip.pypa.io/en/stable/topics/caching/): “Pip provides an on-by-default caching, designed to reduce the amount of time spent on duplicate downloads and builds.” This supports the enumerated retrieval cache rows, not arbitrary executable members.
- [Shared MIME-info specification](https://specifications.freedesktop.org/shared-mime-info/latest-single/): “The files created by `update-mime-database` are:” followed by output formats including MEDIA/SUBTYPE.xml. These generated type descriptions are separate from the packages input directory. The generated status alone does not settle S2.2-2 versus S2.2-4.
- [Desktop Entry Exec key](https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html): “The `Exec` key must contain a command line.” Launch descriptors can start an external program; they were not classified as merely pictures or labels.
- [GRUB scripting](https://www.gnu.org/software/grub/manual/grub/html_node/Shell_002dlike-scripting.html): “grub.cfg is written in GRUB’s built-in scripting language”. This distinguishes boot scripts from passive boot documentation.
- [Git repository layout](https://git-scm.com/docs/gitrepository-layout): “Hooks are customization scripts used by various Git commands.” Script members and repository history were separated in mixed trees.
- [Translator documentation](https://www.zotero.org/support/dev/translators): “Zotero translators are stored as individual JavaScript files.” This establishes code, but not the actual rights confinement of the inventoried version; uncertain confinement remains UNKNOWN.
- [Monitoring database engine](https://learn.netdata.cloud/docs/developer-and-contributor-corner/database-engine): “DBENGINE is the time-series database of Netdata.” Saved metric measurements describe past observations; active configuration and identity material were handled separately.
- [Pinned editor directory values](https://raw.githubusercontent.com/bbatsov/prelude/11a42655b9cba88933660768fa83e2340524e407/personal/.dir-locals.el): `((emacs-lisp-mode . ((flycheck-disabled-checkers . (emacs-lisp-checkdoc)))))`. This particular file contains only checker-disable values; it was not assumed to execute eval code.
- [AppArmor parser](https://manpages.debian.org/trixie/apparmor/apparmor_parser.8.en.html): “Perform no caching at all: disables -W, implies -T.” Source policy compilation is available without using the binary policy cache; these particular cache-only rows are NOT under S2.2-5.
- [Password history module](https://man7.org/linux/man-pages/man8/pam_pwhistory.8.html): “PAM module to remember last passwords”. The module can use opasswd in password reuse enforcement. The inventory did not establish whether this stored history is active in the saved stacks, so the row is UNKNOWN.
- [SGML catalog maintenance](https://manpages.debian.org/trixie/sgml-base/update-catalog.8.en.html): “create or update entry in SGML catalog file”. Global catalog structure does not establish the missing saved entries and their consumers; the uninspected active catalog remains UNKNOWN.

## Individual decisions and review resolutions

The stored-object inspection scripts and JSON audits enumerate each individual decision and its expanded member assignment. Identical wording in small explicit lists does not imply an uninspected kind-wide rule. The following factual distinctions caused refinements before completion:

- EFI boot directories contain programs and boot scripts (MUST); the fallback CSV supplies boot-variable creation input rather than mere labels. Its overlap between internal values and external boot behavior remains HOLE. The executable component notes cite the fallback implementation.
- A WireGuard private key enables the recorded network operation. It is MUST under the removal test; the explicit Wi-Fi and account-password exemptions were not extended to every secret.
- The Cargo source cache contains compiled-language source/documents (NOT), but an executable ELF test fixture has a cache/code overlap (HOLE). No interpreted build scripts were invented for this tree.
- One editor theme group contains only .el files and is MUST. The sample editor configuration files are code, while the pinned directory-local checker values are NOT. The unused preload placeholder is empty content.
- Crash reports are NOT, but crashping.pid has an unestablished control role (UNKNOWN), making its group MIXED. A log directory containing only .gitkeep is content, not a fictional event history.
- Application omni.ja resources include executing application code (MUST), while hyphenation dictionaries and application-internal values are NOT. Membership was not reduced to the archive suffix alone.
- Operational lookup databases and MIME descriptions use the explicit S2.2-2/S2.2-4 boundary rationale. No final decision depends on an invented cache-regeneration deadline.
- AppArmor binary cache entries are NOT because the documented parser can compile source without the cache. This does not exempt the active source policy.
- The print spool control file’s actual job state was not captured, so the row is UNKNOWN rather than a conceptual hole.
- Review found that opasswd had been treated too broadly as passive history; active use is unestablished, so UNKNOWN. The global SGML catalog is likewise UNKNOWN. The XML catalog group is MIXED: old backup content NOT; active catalogs UNKNOWN because the entries and consumers were not saved.
- The reviewer’s initial concern that generated MIME XML was unsupported was superseded by the primary specification’s explicit output list. The final HOLE concerns the descriptive-content/recognition-operation boundary, not generation timing. The reviewer verified the three catalog/password corrections in the merged table.

## Component notes

The following six records are included in full so every delegated homogeneous rule and its ten manual checks are present in this requested notes file. Their component counts describe disjoint assignments, not an additional final result.

---

### Component: code

# Part 1 executable-object notes

Scope: 1009 rows of the two executable-code kinds. The collector selects executable permission, a leading shebang, or a recognized shell-startup pathname. That selection is evidence of candidacy only: PNGs, JSON, Rust crate attributes, and Python type stubs require separate decisions. No object was removed or executed.

Sources inspected: COMMON.md, TEXT.md sections 2–3, SENTENCES.md, (not published: direct evidence over 2 MB), A3R/in/REDUCTION.md, (not published: direct evidence over 2 MB), the supplied raw collector outputs and script, and A3/BUILD.md. Subtree membership was matched by exact prefix plus slash and original executable-code kind; all 54 group counts matched. No other classification was consulted.

## Homogeneous rule D: Debian maintainer programs

All 808 files directly under var/lib/dpkg/info with preinst/postinst/prerm/postrm/config suffixes are package lifecycle programs. S2.2-10 requires their recording because the package manager invokes executable interpreter programs without confining their authority to its interface. The metadata directory does not make these programs mere historical records. Debian Policy explicitly identifies all five forms.

Hand checks, ten individual inventory rows: 77f910004f12f21e157760be (python3-certifi.prerm), 5809e003eda87d110ac376c1 (libnss-mdns.postrm), fb2cd1476cb2839b82e5447e (fonts-font-awesome.postrm), f9003f84eb1a9026a4e6d0e3 (python3.postinst), 1281f90bc323ba9fa50c16f4 (dbus.preinst), f515b5fd2f421e080024e24c (traceroute.prerm), 02a6d2489748917d5d3568e0 (libpam-systemd.postinst), 3e9bd34f8dd5df8bb36b3c3b (libsane-common.postrm), f577be0adc7590800070c855 (tcpdump.postrm), 5a5a372d8b7c0c8c94b2b2e1 (xfonts-base.postinst). Each inventory entry is a regular executable file in the documented lifecycle location. The complete suffix histogram was postinst 286, prerm 188, postrm 187, preinst 125, config 22; no other suffix was swept into the rule.

[Debian Policy](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html): “These scripts are the package metadata files `preinst`, `postinst`, `prerm` and `postrm`.” The same section identifies config as the debconf interaction script.

## Homogeneous rule S: unrestricted interpreter programs

The explicitly enumerated startup/setup/test scripts in code_classify.py and the inspected Oh My Zsh and nvm script families are MUST under S2.2-10 and S2.2-13. Shell assignment syntax remains code when sourced, including themes and startup preferences. Shell and interpreter programs can access files and start subprocesses with their interpreter's rights. Test programs and install helpers remain programs even when not automatically invoked. This rule excludes native Node, cache scripts, Dockerfiles, compiled-language source, and data with executable permission.

Hand checks, ten rows: f24061803084a9814de763f7 (profile startup), 6567792613cfbccdbaa79a9f (bashrc startup), ea853f08eba26ac551aeac51 (editor pager shell wrapper), 5a3f8a70e7ddfa13a6855116 (system shell startup), 6c6590976f30d55a2ee1085a (Cargo environment shell code), 242cffd65ed52594ee64b68b (dotfiles bootstrap script), dc74f56c3d34bd22933fd7b8 (shell function definitions), lived-t2b2e1d800b (four shell/Python proxy programs), lived-tf883bef0f0 (nineteen shell installation tests), lived-ta6a42c1337 (ten sourcing tests and setup/teardown). The group members were expanded in objects.tsv and checked for non-script data; none occurs in those test groups.

[nvm](https://github.com/nvm-sh/nvm): “POSIX-compliant bash script to manage multiple active node.js versions.” [Its contribution guide](https://raw.githubusercontent.com/nvm-sh/nvm/master/CONTRIBUTING.md): “Fast tests do run in these shells”. [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh) documents its plugin/theme shell configuration; the listed plugin test files are executable tests, not test logs. [Public dotfiles](https://github.com/mathiasbynens/dotfiles) supplies the copied shell functions and startup scripts identified in BUILD.md.

## Homogeneous rule P: installed native and helper code

The inspected Netdata and Zotero executable/library members are MUST under S2.2-9 or S2.2-10. Native programs are processes; native libraries execute with their loading program's rights; installation helpers are shell programs. The rule does not include Zotero desktop descriptors or its profile data. All members of the two Netdata executable subtrees were expanded: 38 collector/installer/helper programs and five service-launch scripts.

Hand checks, ten rows: cdd812b6784b8f976425c981 (Netdata shell functions), f4e6310714d36f565893be1c (pairing shell helper), 4e0cb1774db353ff07687b8b (installation/update script), 3ece6080b7b69cb609e60339 (configuration-edit helper), bf730d044910400ca4fb57f3 (Bash executable), 50f92c0193d56c59822b1217 (curl executable), 4e2cfa9245f592b876f72e46 (Netdata agent), lived-t09751b7efe (expanded collector/helper subtree), 6ba83a507974e58f472a9f07 (Zotero launcher), 622cb32f87c05a7ad35ba345 (Zotero binary). Native library names were checked separately against the installed application layout; no .desktop value file enters the rule.

[Netdata project](https://github.com/netdata/netdata): “Netdata Agents collect, store and analyze data where it is generated”. [Zotero installation](https://www.zotero.org/support/installation): “Download the tarball, extract the contents, and run `zotero` from that directory to start Zotero.” Its launcher-icon helper is explicitly documented on that page.

## Individually inspected Git hook groups

There are only nine Git-metadata groups, and all nine were expanded and inspected individually, rather than sampling a larger automatic kind. IDs: lived-t98b49255b3, lived-t667ba4fb10, lived-tf3cef8f65e, lived-teaff14fb6e, lived-t5524f36a07, lived-t377338389c, lived-tb8a7a2c063, lived-ta4806d9131, lived-tc5d3d1ad66. Eight contain fourteen sample programs apiece; Flask adds the installed pre-commit program. The sample suffix prevents automatic Git hook invocation, but these are still executable interpreter programs that can be invoked directly. Removing a sample removes that runnable program, not merely an execution history entry. All are MUST under S2.2-2/S2.2-10; no claim is made that every sample is an active Git hook.

[Git hooks](https://git-scm.com/docs/githooks): “Hooks are programs you can place in a hooks directory to trigger actions at certain points in git’s execution.”

## Individual and heterogeneous decisions

All remaining rows are enumerated individually in code_classify.py. Shared wording for two architecture copies or equivalent sample trees is not a filename-wide inference. Notable distinctions:

- Flatpak's object hashes cannot be mapped to actual applications, scripts, assets, or stale copies from this inventory. All 4678 raw candidate names were checked for descriptive mapping; none provides it. UNKNOWN concerns their actual functions, not uncertainty about the requirement. [Flatpak internals](https://docs.flatpak.org/en/latest/under-the-hood.html): “Flatpak uses repositories to store data”. Generic repository knowledge cannot recover the member roles.
- The Cargo subtree contains 90 Rust source files and one ELF-named binary fixture. Source is unpacked dependency cache; the binary fixture adds the unresolved cache/program overlap. [Cargo home](https://doc.rust-lang.org/cargo/guide/cargo-home.html): “The ‘Cargo home’ functions as a download and source cache.” Registry/src is unpacked from crate archives. The fixture is tests/examples/hello_world_elf64 under hexyl; only that member receives HOLE.
- Emacs native trampolines execute code and are regenerable caches; this is the direct S2.2-5/S2.2-10 conflict, not a state-transfer or rollback question. [Emacs source](https://raw.githubusercontent.com/emacs-mirror/emacs/master/lisp/emacs-lisp/comp.el): “Synthesize compile and return a trampoline for SUBR-NAME.” The five member names identify the wrapped primitives. The Go module-cache script has the same cache/code overlap. [Go reference](https://go.dev/ref/mod#module-cache): “The module cache is the directory where the `go` command stores downloaded module files.”
- Python .pyi members are type descriptions, not implementation bodies. [Typing specification](https://typing.python.org/en/latest/spec/distributing.html): “Stub files, also called type stubs, provide type information for untyped Python packages and modules.” Their parser use differs from unrestricted program execution.
- All 22 company images are PNG screenshots under images/small, NOT content. The Compose JPEG is the image referenced by the project's README. [Compose README](https://raw.githubusercontent.com/docker/awesome-compose/master/README.md): “A curated list of Docker Compose samples.”
- Compose subtrees were expanded individually. Browser JavaScript is confined browser code; server/test JavaScript and Python run as interpreter programs; static documents/images are content; application value files fall under S2.2-7/S2.2-13. Compiled-language source and Dockerfiles leave the content-versus-build-instructions boundary unresolved. [Dockerfile reference](https://docs.docker.com/reference/dockerfile/): “Docker can build images automatically by reading the instructions from a Dockerfile.” Reading that recipe and executing its child commands are not clearly identified as the same object by S2.2-10/13.
- Within aspnet-mssql, the npm.js file under browser-library sources needs separate treatment from the rest of wwwroot: HOLE because its development-tool purpose and the surrounding browser assets do not make the source/build boundary disappear. All other wwwroot images, fonts, browser scripts, maps and licenses are NOT; appsettings values NOT; C#/Razor/solution/Dockerfile HOLE.
- Neovim's 515 members include 448 sample hooks and 67 other entries: Mason tools, unrestricted scripts, and syntax-highlight fixtures. The treesitter test.kos and test.zsh fixtures are HOLE because their use as sample content and their language-code form are distinct plausible readings; the remaining tooling and scripts are MUST. This distinction does not classify the surrounding stored-directory row.
- EFI programs are MUST; BOOTX64.CSV is HOLE because it controls recovery boot-variable creation while being values consumed by one program. [Shim fallback documentation](https://raw.githubusercontent.com/rhboot/shim/main/README.fallback): “It'll parse that, and create new boot variables from what it finds.” grub.cfg is command code. [GRUB module-info template](https://sources.debian.org/src/grub2/2.12-9%2Bdeb13u2/grub-core/modinfo.sh.in): `grub_modinfo_target_cpu=@target_cpu@` is a shell assignment and remains code under S2.2-13.
- The desktop autostart entry acts beyond one application's internal appearance: it starts another program at login. [Autostart specification](https://specifications.freedesktop.org/autostart/latest/): “the application will be automatically launched during startup of the user's desktop environment”. A standalone launcher descriptor retains the inside-one-program ambiguity.
- Profile times.json holds historical timestamps. [ProfileAge source](https://raw.githubusercontent.com/mozilla-firefox/firefox/main/toolkit/modules/ProfileAge.sys.mjs): `const FILE_TIMES = "times.json";`. The source tracks profile creation, reset and first-use times; executable permission does not convert JSON into program code.
- [Python environment helper](https://github.com/microsoft/python-environment-tools): “locating all global Python installs and virtual environments.” [debugpy](https://github.com/microsoft/debugpy): “An implementation of the Debug Adapter Protocol for Python”. Helpers and wrappers are processes/interpreter programs, despite editor-extension packaging.
- [zlib manual](https://zlib.net/manual.html): “The zlib compression library provides in-memory compression and decompression functions”. Built examples and compression utilities are actual programs, unlike their compiled-language source inputs. [CUPS backend manual](https://www.cups.org/doc/man-backend.html): “Backends are a special type of filter(7)”. Its six members discover printers or transmit print data as child processes.

## Verification

The writer appends and flushes each completed row, skips existing IDs on resumption, and verifies exact subset ID equality, count and uniqueness. It validates the decision vocabulary and the 15-word/30-word field limits. Result: 1009 rows; MUST 984, NOT 4, HOLE 6, UNKNOWN 1, MIXED 14. This is structural validation, not independent acceptance of the classification.

## Exact applicable sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-3** The following need not be recorded:

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;

- **S2.2-6** records of the past—logs, history;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-8** Consequences of this rule that we fix explicitly:

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.

---

### Component: packages

# Part 1: package and package-environment decisions

Independent c1 classification. Only the specified text, numbered sentences, reduction explanation, input inventory, its raw files, the permitted build account and public documentation were read. No removal was performed.

## Interpretation and evidence

A package row denotes the installed package; a package-environment-evidence row denotes the named file. A package can contain code even when its manifest itself is only values. JavaScript package directories were checked against the filesystem inventory for actual .js/.cjs/.mjs/.node files. Data-only and type-only exceptions were decided individually. The Python summaries and names were read from the METADATA archive, not inferred from the collector kind.

The 167 and 168 raw outputs are tar archives; entries were read in memory, without extraction or execution. The filesystem output is NUL-delimited in six-field records. Public manifests were retrieved for the exact Express, Compose and version-manager commits in the permitted build account and the editor release tag. package-public-fields.json retains URLs, retrieval failure types and selected field-presence facts, without whole downloaded files.

The manual check corrected an overbroad editor-path match: nested bootstrap, API and server manifests are not automatically editor extension settings. Root extension manifests whose script fields could not be inspected are also UNKNOWN. The public editor source resolved many initially uncertain files, including scripts in language-extension manifests. Existing rows were retained and corrected after these inspections; no IDs were dropped.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Documentation consulted

- https://nodejs.org/api/packages.html — “The \"type\" field defines the module format”. The loader reads package values; directory code is a separate object.
- https://docs.npmjs.com/cli/v11/using-npm/scripts/ — “Scripts are run by passing the line as a script argument to `/bin/sh` on POSIX systems” Script values are passed to a shell; that indirection is the disputed boundary below.
- https://docs.npmjs.com/cli/v11/configuring-npm/package-json/ — documents main, bin, scripts and dependency fields. Installation entry-point mappings affect installed command availability.
- https://docs.python.org/3/library/importlib.metadata.html — “a library that provides access to the metadata of an installed” distribution. Metadata can be read by runtime code as well as installation tools.
- https://packaging.python.org/en/latest/specifications/recording-installed-packages/ — “A common metadata format allows tools to query, manage or uninstall projects, regardless of how they were installed.” This establishes operational use beyond a historical record.
- https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html — “Cargo.lock contains exact information about your dependencies.” Lockfiles supply Cargo values, rather than executing code.
- https://doc.rust-lang.org/cargo/commands/cargo-install.html — “This command manages Cargo’s local set of installed binary crates.” The executable and its tracking record are distinct objects.
- https://go.dev/ref/mod#module-cache — describes downloaded module metadata and source in the module cache. The three go.mod rows name cache copies, while binary module rows identify linked code.
- https://docs.flatpak.org/en/latest/extension.html — “These are automatically created and loaded if installed.” Locale extensions contain language resources; platform, graphics and codec extensions supply executable runtime components.
- https://code.visualstudio.com/api/references/extension-manifest — “Every Visual Studio Code extension needs a manifest file package.json at the root of the extension directory structure.” This does not prove absence of embedded script strings, so missing exact contents remain UNKNOWN.
- https://learn.microsoft.com/en-us/nuget/reference/packages-config — “maintain the list of packages referenced by the project.” Both packages.config rows are NuGet values.

## Rules and manual checks

Each rule below was applied only to the stated homogeneous property, not blindly to an inventory kind. Ten listed IDs were inspected against their names and raw manifest fields or the documented file format. Code checks included actual filesystem paths. Everything outside these rules was decided individually; individual rows retain their own reasons.

### python-code (172 rows)

MUST, S2.2-10. Installed importable modules execute with interpreter rights. The ten checks cover installer, network proxy, certificate-bundle accessor, charset detector, XML protection, HTTP client, domain conversion, Markdown parser, URL utilities and multidict. A distribution summary describing data does not erase its Python accessor/initialization module.

Manually checked IDs: 7a00e818805ccd6a9a42561a, 452429ca69d9d258b2fda78c, c93c0c3ce2d5afcc95c44d79, a751dd59cb2fd328da76bf5a, 75451dd1e4ecfdac51a0f1f3, a6dacb809dc75691895def0e, 24e2d94703c0a5a0fc883439, 112029b022aaff73bbdb4925, 48da39ea4d7024771209574c, 19628990b28a248b157459d8.

### python-metadata (172 rows)

HOLE, S2.2-2 and S2.2-4. The file is descriptive installed-package database content, but tools depend on its version/requirements for management decisions. The text does not say where losing access to this description becomes lost management capability. This concerns what must be recorded, not how a system transfers state under Section 2.5. Checked setuptools, template libraries, attrs, packaging, markdown, TOML and iterable/context utilities.

Manually checked IDs: 51cba7cfc1bf2684737e1902, 35b08e5e2c7d0df863990fcb, 55f8a1b78a6e7fe96e1c0645, b5a812108fee30bde128868b, 6971545a28a58d7a6172ec28, 608b6340b64cfca363330534, 5e4917158f087301a8fc8b13, e78e15d8f9683164d61faf24, e85b221073f95ef465518069, 7356c19233248767ccd1f7a1.

### cargo-lock (13 rows)

NOT, S2.2-7 and S2.2-13. Cargo.lock pins dependency versions as Cargo values. Ten separate crates were checked by pathname and format documentation; the final plugin lockfile has the same format. No lockfile is treated as a shell script.

Manually checked IDs: 7dbefedebf6375158b6ca300, a1f99c6fb53c51b2ced48951, be9f7e7d81bcd831c02f3a98, 2cf212485ca2cad9df932e77, 92dd5e00f5b518655a8deccb, 8b70c9714a7c27e0ef90e5ed, efefcfd0224770fa0b5fad9a, 72a0350f58b2c8c715193d77, 38e8ff297a2d7ce7545a0c05, f3170b1bf4d4e330e7c53bc8.

### unavailable-manifest (22 rows)

UNKNOWN, S3-1 and S3-2. The exact manifest is absent from the raw archive and public format documentation alone does not establish its operational fields. The ten checked rows include extension roots and nested bootstrap/API/client manifests. Some public release paths returned HTTP errors; product documentation establishes what a manifest can do, not which executable strings this copy holds.

Manually checked IDs: 3ce5b4911a70e4f372f050fc, 86daa8c724c19067e0c1d0e2, fdbd88e1eaf71d01e74382e1, d724cf2c390f3bbbd332773f, e704d6a1172573d48e975c32, d96b5d6c959ccc7eeddb43a4, af54cbc2e86d92939542da1e, 1b205701e393abfa128445ca, c30adf2e73e0a4b39a32ec4e, b85ea331a76d4fefe41c7860.

### script-manifest (624 rows)

HOLE, S2.2-10 and S2.2-13. The JSON file is parsed as values, yet its script strings become executable shell code with ordinary process rights. No sentence says whether the file-as-values or embedded-code reading prevails across this indirection. The ten checks explicitly show preinstall, test, build, preparation and publication command strings; none were run.

Manually checked IDs: 01a4e078e7c0b7b294270cbc, cac88f8477725b806868cc1e, 0b680470f40e8c00955e73c0, 6acf32184c8c26c09daae8cd, 9236b09c25fea5c3f482f2e9, 725d789bc9c809520530bfd5, 39339c3abdbbc2b376b09669, a0ae816570ee8d640ca0fdae, df088e7ca5f47186d879707e, 46a102166f7170cc5da0d60d.

### module-values (116 rows)

NOT, S2.2-7 and S2.2-13. These inspected manifests have no script strings or installed bin mappings; they supply program-local module settings or descriptive values. The ten checks are alternating commonjs/module type fields, including yargs helpers, so the distinction from neighboring executable directory rows is explicit.

Manually checked IDs: d38ed16b0807269a4ad0549a, 5afd0885806e9032181d018d, a5a88605f6c070500a969c0e, 6fc7d50def438a9a1117aa51, c5ced7bcaa80188822b2dccb, 02d570a8c56dff73330b404a, c04c769cdd3a9c0bdbe7a310, 0eb15c02ce71fa4848c63144, 4bc82fc8dba564172fee6257, 050d21730580fe959a99184c.

### javascript-code (633 rows)

MUST, S2.2-10. Actual module or command code is present under the package directory and is executed by the ordinary runtime with its rights. The first ten cover yarn, formatter, path predicate, color exports, debugging, header parsing, cache and both compiled module-format directories. Data exported by JavaScript still has executable module initialization.

Manually checked IDs: 7492f124f892f0b5ecaaea16, fb5bce794be68ddc4741e475, d3f8a027b27582f85f6adc28, cd73f71c46ee65add2da566a, 115cb055814abb78c8f6273f, 9dc189870f0a350eff1d6694, 3d873c039338fa89bd3ac1ad, b7ebcc69e43570e7af2091c7, 989e876230b5b225ee60518c, 2ef16fbc8af639d52b16b1ea.

## Individual exceptions

Two type-fest directories supply static declarations and receive HOLE: the text does not identify when loss of source declarations is merely content loss versus loss of compilation capability. Four reference-table packages have no runtime-code files and receive NOT. The native compiler platform package is MUST. Flatpak applications and executable runtimes are MUST, locale content NOT. Cargo and pipx executables are MUST; Cargo tracking values NOT. The AppArmor profile is MUST because it controls access externally; its compiled cache is NOT. The three cached Go manifests are NOT, while linked binary module rows are MUST. These small sets were reviewed row by row, not projected from a blanket package rule.

Validation: output has exactly all 1,806 assigned IDs, once each; decisions and word limits were checked. No MIXED rows occur because these package-level objects are not reduced stored-object subtree groups.

---

### Component: system

# Classification c1: system subset

Only the authorized input, raw inventory, fixed text, build description and cited public documentation were consulted. No objects were removed.

## Exact text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-8** Consequences of this rule that we fix explicitly:
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and manual checks

Each rule below was checked against the displayed raw entries for its first ten listed IDs. Functions, not inventory class labels, determine the decisions.

### accounts

Scope: account. 40 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 66251b78bb6f912aa915abb1, 0500fe8692cdec2d97e72891, 1a8c96d4c282ed70c6167e58, cd80c580185f4091df737c0c, 40e833964547387f3ca4e553, c2b55ec7fb85f936e32f588e, a634e1780bab80e03cbf0e39, 855811c08518bf800c8dd897, 3d2875b6496538d42abc46ba, 3de43376d6f23e3efccd5496.

### groups

Scope: group. 68 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 424cb5f40e407805606b43e3, 9a4c7a2ea9898d9ae38b5554, ca43ae86e803e0ce5b114acb, 275846cd06c295d42d5542fa, cd5cf2d139b549e5462d19b9, 233837b04ee105ad3015470e, d05c192167c5d3fe22d5bcb2, 5af62d641728cadffc3d9ac4, e55ba3e907101bc803a424b4, 2f8d930a409d1f2bdd2c5fa3.

### services

Scope: service, user-service. 19 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 47c7815588e844c881916f82, 3c4f4e65c757b551ff3b1f81, dcac5914e520f17b298b681f, a315658eb8bf9e7eb6a1b6ea, 2a46a74df2451e259b6ed3b0, 4dc126c54aec97463c351c86, 5bcd72a57568d62e4b8eeaa5, 6c6b38144ff0ac1886377992, d59d14dc3535bec649909ff1, 1413205ac7d1d69a837dabb3.

### absent-services

Scope: service, user-service. 19 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: d6bc83a7f2ca4f16f6e78efe, 06fa1242840b189689061719, 90f390ddf29b7369718d4977, fa69fb560b4500fad1f08784, 2f5b18f25d55cf29bd04e4f1, f2aee53f185b859565fdfdc8, 3f1c73b48d9806792c04fcb4, 2dddfe42afbabcf835c845c8, 1fe8a1baafff2cd597376eb3, 978e06a6ed01dcd129258630.

### units

Scope: unit-file, user-unit-file. 55 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 531cdbe55af3004b2739cb22, df6003b998e902e368f48f0c, 6c8613682668a234b62b9293, 502b5f821f78dc4db11523ce, e5550072d851d99906872129, e1e0b163b302a8cbbcc9d7e0, 5ec94a501ed23615be676ed4, c448e0f072952ad51da0e28e, de9bc02887c53b50e0a1898f, cae5392ebf5125dba2b23e25.

### processes

Scope: process. 66 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: a54331f4416f0d3975046f6e, 4d26d5704cf52e5ae4acbf8c, ac12bb908cb86db7ea204809, 47402393f7377f308ce3da35, 2d208f9f569bf7cab0a7cb42, 69554e1c931ffa3c34beb96b, a2c934737dae951e4e69f2ef, a38a087a068b5823d770620c, d22f66dc0415311f8a7c34b5, 4eb464269c6a97375189523e.

### unresolved-processes

Scope: process. 22 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 1c460643fdd8cfbbd196d5c8, 8b1dbd0e6a04dda53f042fdf, 42c8a140e560dc29380e1d8c, 9dfd7d2fb9793e2b0f9e0450, 1de8c224f0b98ee3c699a8f1, 870b4f98bda38de1efeebee1, 7f68c5deb8bee8904640065d, 5170ad8d1f6cab983ec4aac9, a56cebd347b0e2d321707d00, 405fd3b1305197a3b82e9395.

### drivers

Scope: driver. 35 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 362aac25bc3ff6a3adf0a0e5, d12eacb0fc0b883b38c28c81, 31489a1bb2b9bcbc9d50becb, ec02f88264ac6f14cb3c7b48, 516af3b20d07477d0880f173, 7285a2d79b6340611118e1b8, 4a16f044d2a204288036ee84, 21d0a8ca78fa8dab4685b518, 325f463f0ee4c170dfda2160, 4d95912dea3aba87d392ee89.

### ports

Scope: port. 30 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 50569e2b739a95c2d9211520, a10944ac5db4979488d11d44, 818e748f0a25d4ce6b7e112b, 90015923ad530f453981f9d7, c130018c3b73f5cd5e761ce1, f63fd0600c18846258c07f68, f4bbb25a9e6780d70e006fe9, 2b4d1a3fdb18bd8257283ff6, 4e2a49e1518a7ae42fd035da, b12b144e402737d5b7dbfd69.

### firewall-rules

Scope: firewall-rule. 21 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 82cf95c36b73b53f28b0a694, 00e4bb96eba524c41611dcf9, 32d581eebb12d54853ebf91c, e649b8e7c3e336831c4836f6, 38a2815ee993ffdf0b64293f, b64534a87c0760c3621f0857, bbdc0f43e0cc8d2c12d255c1, 47921eae029fa610270e94f1, 85ec649d68b7beab063b6b99, 46a718f82a4f2bc6ba44ef0b.

### polkit

Scope: polkit-actions. 219 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 3e209d6e565fbc2a96423ca5, 93664169da2a08543bebc9fd, 92b43c33b616c9da07700acf, cbc914d3e7e1602d9b6053f5, b3b783db0a8964cfae6d3e79, f086f19d5724019e2120e18e, d88942a7193718431a649c09, f467c8cc721d8153af82e90f, 2ba592b30a400e0fe5514afa, 9689bca4147eb2173056832e.

## Sources

- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html : “Actions correspond to operations that clients can request the mechanism to carry out”. Policies span client, authority and service processes.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html : “A unit file is a plain text ini-style file”. Service units arrange external program activation, rather than settings confined to systemd’s interface.
- https://docs.kernel.org/driver-api/driver-model/binding.html : “Driver binding is the process of associating a device with a device driver that can control it.” Rows identify the binding, not ordinary stored symlink files.
- https://www.man7.org/linux/man-pages/man5/group.5.html : “The /etc/group file is a text file that defines the groups on the system.” Group records define usable named credentials, including empty groups.
- https://netfilter.org/projects/nftables/manpage.html : “nft - Administration tool of the nftables framework for packet filtering and classification”.
- https://man.openbsd.org/sshd_config : “The file contains keyword-argument pairs, one per line.” These are values, not executable code.
- https://docs.podman.io/en/latest/markdown/podman-run.1.html : “Run a process in a new container.” The same documentation specifies automatic image pulling when absent.

## Process evidence defect

`../in/raw/lived/raw/076-process.sh` prints the PID and a tab before `readlink`; a failed readlink emits no newline. Several raw lines therefore concatenate unresolved PIDs before another PID and its executable. The row name is the first PID. Those rows are UNKNOWN, not assigned the last PID’s executable. Public program documentation cannot recover which program an unidentified PID ran.

## Individually considered remaining rows

SSH values were considered individually using https://manpages.debian.org/trixie/openssh-server/sshd_config.5.en.html and the corresponding keywords in https://man.openbsd.org/sshd_config. The sources define each directive. Quote: “Specifies what environment variables sent by the client will be copied into the session”. No actual account password is included.

- b8093dd460d9b0712167e99d: MUST; Schedules the development cleanup service. Removing the active timer stops the scheduled cleanup action.
- ce9cf885ee9d5f0106f81e49: UNKNOWN; Lists a timer without an activation time or target service. The listing supplies no activation or target, and the related service is absent; existence and function of this timer remain unestablished.
- 6545c01a63ed249cce38d052: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- 717eb2770380a84a60c5c313: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- dda59fbc8826d393f7d01a10: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 35cb6ad5449614d23bebe242: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 48c1fa93a17da9d38e506def: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- a09dad130a88e21ac58d25ca: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 42fee34c37890e2ec7bad698: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- a1543f91747b9c5a83532869: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- ea5d40a2dff60d224d49f01a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- dd09d750d72e29a6802c0993: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 68e163de5be454c2c0f3b7ff: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 402a14bcdc254a1331a2d91c: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 45fa13af9c9c2849fefd5d4a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 2714f30ffdeaf1632792f969: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- c170614338f39c0ff9dbc556: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 339a64d45b4a268c2b7939fe: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- c8c7f72048df6524167e19e5: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- baf66f3a90895b339239008f: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- e68b62bdcfb24cc617e6993a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 29b72142ba82d7d23e0e9bbd: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 45494a3628cd9f2a6a155e72: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 44bcf67fcda29b9fa6d3de74: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- ad5b73353f54e5a01ea55bb9: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 37e697762632a2f0de4384fd: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- 65df70aaa862229cd4fd3618: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- fbc43cf4d2bace79f0e65a70: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 62d714301de740e46b1a3024: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 91ecf17e0567fccc77b8e076: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 204facdaa40276808ea45ed2: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- de63db4254e7f1cbf407dffd: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- d1e8812964d588e2a21c6235: MUST; Selects SSH listening port. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 737f1902f893bea8c97a1782: MUST; Selects SSH IPv4 or IPv6 listening. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7e4c1ea41e01e76ab786bf0a: MUST; Selects SSH listening address. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 9570234ba746fde9faa9eeb9: MUST; Selects SSH listening address. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 5f8fcf77e7c5041de9f3e517: MUST; Enables PAM account and session checks. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4725e095d352bc5ed4c1212b: MUST; Selects PAM service configuration. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 70af2f25c61976b23e86474e: HOLE; Limits time available for login. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- a92608a203e2973dcfaed75e: MUST; Selects initial X11 proxy display number. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 73b70232c07e15bee2c93628: HOLE; Limits authentication attempts. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- e8ddd511263a12c14f4e5efe: HOLE; Limits concurrent login sessions. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d29f710b6352ad934c568a48: HOLE; Schedules SSH client liveness probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 8ffdf2c6cb34aa995b80a0b8: HOLE; Limits unanswered client liveness probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 64c3eeeb56074c666b06d5da: HOLE; Sets minimum accepted RSA key size. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- fc175f3fe8e9bfeb82bd30b7: MUST; Sets permissions on forwarded Unix sockets. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 846b368c9c7eb3b2cc9bafda: HOLE; Limits time retaining connections without channels. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 5dfdf1d7b9c621a510a827ea: MUST; Controls remote login to the superuser account. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- ca5a9ae631db41881a734b4e: MUST; Controls rhosts authentication source. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d12c24ce799f60fedc128ce0: MUST; Controls user hostbased authentication sources. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 2b243d7d1c8afe48dcd5638d: MUST; Controls hostbased account authentication. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 63f63d2dbbcced0b61b17eb8: HOLE; Selects hostbased authentication hostname source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d858b7eb5b5db644a78163d0: MUST; Controls public-key account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c820f0571c36594777b32e84: MUST; Controls Kerberos account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 753c27cfe7d736e997bdfae4: MUST; Controls password fallback for Kerberos authentication. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c462b75395e079a1aca2a05a: MUST; Removes session Kerberos tickets at logout. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c8d97c4e5a2cc2c9113c1511: MUST; Controls GSSAPI account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- bbad5c6166456c8edcbaefd6: MUST; Cleans session GSSAPI credentials at logout. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 999504031457ae948155b61a: HOLE; Controls GSSAPI key exchange. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 4df184f1d0b6c034f26d0ce0: HOLE; Controls server principal checks for GSSAPI. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 19dab249d75fc4989eb0155c: MUST; Updates stored GSSAPI credentials on rekey. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 64c1378303db60df30dc481f: HOLE; Selects GSSAPI key-exchange algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- ef20600433d5240311ab31ed: MUST; Controls password account login. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 17944940865f95039d032349: MUST; Controls keyboard-interactive account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 0fa4588a2dad34f680665277: NOT; Controls login message display. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 92e6c624ab79089f59bfa9ac: NOT; Controls display of previous login. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 82afb2db4ffd5e38b0ec4ecd: MUST; Controls X11 access forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 975a5aa0f2ba4519ff6f9882: MUST; Controls X11 forwarding socket binding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d6235a098bb82243371dc8d0: MUST; Controls pseudo-terminal allocation. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c30c19e8bcd5ed9c4c5321d4: MUST; Controls execution of user session startup code. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4b2c2f0ad8ab9f74f3a65c6e: MUST; Checks login-file ownership and permissions. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7f4432571561605278bf1b19: HOLE; Controls transport keepalive probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- c8a680baaf352c8e605fb03e: MUST; Controls login with empty passwords. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 0d65c285875796e9bbf21830: NOT; Controls SSH transport compression. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 74999b1091594f23c49d1e14: MUST; Controls externally reachable forwarding sockets. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ba7e43ae48e7b7e88b3ea292: HOLE; Controls client hostname resolution. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 83bfbe2fd66f60bcc74b2389: MUST; Controls TCP forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6e5a986502606af48e9fae01: MUST; Controls forwarding access to authentication agents. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 63d8ebafc9125aab5fdb691d: MUST; Controls all SSH forwarding capabilities. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 30fc0b2ef1da93db06446a63: MUST; Controls Unix-socket forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- b264b65fcfc3d225ca4cd1e5: MUST; Controls removal of existing forwarding socket paths. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8933d62da3bbf94c46748f84: NOT; Selects displayed key fingerprint hash. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 9a64547fcefb3cbdbd52c4f3: MUST; Exports authentication information to login sessions. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7d7819fbc923d0351a4b6ae9: MUST; Controls refusal of SSH connections. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 5910743adb18dff8d270113c: NOT; Controls distribution identification in server banner. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 21f275a8d1b48381331c9b31: MUST; Selects daemon process identification file. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- cfd777570548528d1120f2ef: HOLE; Selects Diffie-Hellman parameter source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- acdf33b140bddd83baac8d1a: MUST; Selects external X11 authorization helper. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 602b5e23a1883323cc8e5024: HOLE; Selects transport encryption algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 3eb0197357b7f632c0d5a684: HOLE; Selects transport integrity algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1a2131e708503d3c6e9975f5: NOT; Selects authentication banner text. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- eaf28940b541c88787e98e69: MUST; Controls forced session command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 02d364605368ce2e87933c14: MUST; Controls session filesystem confinement. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6fa7d4f75e0e35c7fade8b0d: MUST; Selects trusted login certificate authorities. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d5a6e136b887d644ed5b86d1: MUST; Selects revoked login key list. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- adbbb49cf85548a7b0d4bd2f: HOLE; Selects security-key middleware. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 8f4b98737822decc4aa358e4: MUST; Selects accepted login certificate principals. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6e3034df678eb731d614f899: NOT; Selects server version text suffix. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 761bef463139fca352f38ab7: MUST; Selects external login-key lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 51f5f81517f1036aaf862727: MUST; Selects account for login-key lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- b1656b52f6546343f81d2b33: MUST; Selects external login-principal lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d6c8aa3105290ac72af083e5: MUST; Selects account for login-principal lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- bd2987e4902c8af01f2225cf: HOLE; Selects agent for server host-key signing. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d807dfa19b8414477670f600: HOLE; Selects SSH key-exchange algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 69e2f73b55483fea06b9b8c0: HOLE; Selects accepted certificate signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 151593c72142893b3c097bdf: HOLE; Selects hostbased authentication signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- a1a8b86c2f09f76c21f4cfd6: HOLE; Selects server host-key signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 30303d540f77779033bc6b7a: HOLE; Selects accepted account public-key algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 17e46fc45310b9c16b42f4fa: MUST; Selects external session executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8ec96424e643f241a4f7de9b: MUST; Selects external authentication executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- f448ba068075fa4146ab2811: HOLE; Exempts sources from connection penalties. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- f4d118580a3e7aa82d912ac9: NOT; Selects diagnostic verbosity. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 11e920923f03575bac9def2f: NOT; Selects diagnostic logging facility. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 5d8da4c7ed8f79839659f3c3: MUST; Selects authorized account login-key files. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 837ebb63632431b7c3f91ae6: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 84c1f410613424a2c2846127: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8fe45bad30e49b61dfc9f9ca: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ea3c0282d2d33f7f8f77e5eb: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d962db55ec61443e174b4687: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- dea39dc9c5f82815409c5d3d: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 23220e1a88cbb25f827b3335: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- e1182fe531b91f83ddde87ef: MUST; Selects allowed account authentication combinations. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d913ea330d8c4a39a5ea3001: HOLE; Sets idle SSH channel expiry. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 60d688cfe3148facddc7533d: MUST; Selects external file-transfer subsystem executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4229ee629e74a8e9a246fbc8: HOLE; Limits unauthenticated connections. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 9526c25b3b6c490a157fe0b6: HOLE; Limits unauthenticated connections per source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 363323f681d7fb46cf88fb80: HOLE; Groups connection sources for limits. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 3bf694aa7045763042ac1ed1: MUST; Controls tunnel-device forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d2badf806ff0685bfd641d10: MUST; Sets network packet traffic class. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 3306995d71cfd7876d4d337b: HOLE; Sets encrypted transport rekey thresholds. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1f489f4744d29ff82a43c9ab: MUST; Restricts destinations for TCP forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- fcbb738fa454383ee9ee8f48: MUST; Restricts listeners for TCP forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 072198f6e5546f574cdee23d: MUST; Controls environment passed from account files. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ff18237bd8a718c081eded14: HOLE; Controls additional public-key authentication requirements. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- b3bc32c5ee21a357406dd84d: HOLE; Sets per-source connection penalties. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1c014e18a421906ec23c7c86: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 659db790fbad407e7b491b05: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 3c8fbdb169ca038e2f7a8f7a: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 0e7b4eb5eb41a5b6d4329b4e: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 976a51452aa5aaabce9936bc: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 275587ed29b693da11e27dee: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 81efdb137b7129e363e54bc8: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- c97d9f250787c54baa1e0b72: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 70217070f9a3640192bf6d15: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- be195af2e23105d0bdf5c1e2: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- cd7cb3b2f25e9f09baa807d1: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 6b15c08f7bc1a541a005da17: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- b1e3831b876984497b7e8d93: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- b8b01cfc68bab1c959788e4e: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- d5004a94c316645f5bf68e8a: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 0ec69b7d8b30779dc1e36f2f: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 9a6877ef4dd6c4c7bffb594f: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 5d27dbfeaaba365841790985: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- d15f6d19976fd46865b5f935: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 51e0bcb301dea3bd5c64a3ac: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- cbaf6f16dab7fb21b548717b: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 390e9a29d1bd114fae135522: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- e05bb8e86e06116fe843be06: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- ad5ed316ad45d6f4424c5073: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 2775edcfb0f82fc878c68705: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- b84b415e1bf50514c55e592f: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 3e893bb18da6831140bf5cbf: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 64a3574bd2259c1ed1eca376: MUST; Runs a scheduled shell command measuring document storage usage. Removal stops the scheduled command; its shell executes with account rights.
- 5a58baf83824f5a7aa6fd323: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 1c0d2cf76eb8c9c39f062ad7: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- bc748d9e22c3fa931e8e0921: NOT; Contains explanatory comments without active access rules. The complete raw file contains comments only; removal loses documentation, not an active access policy.
- 1d6abde9e70de201cd9f22cb: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 725c897e37fdd876f805fa42: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 8def8d3af86de559a85b09c5: NOT; Contains explanatory comments without active access rules. The complete raw file contains comments only; removal loses documentation, not an active access policy.
- ce36426d9bc200cddc900200: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 274f9cc66dc198a1cc2ba58d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- e581cb6387cbf187f0923388: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 67912141d193bf207cf5489b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 68492d8fadb2a3e81c76739f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 12166c7ff3c49a8165a055c8: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 10a6f930fb268691b4f8dc71: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 5854afeab0e7e2fb6f6530cb: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 35c07ada63f572ae967d102b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- dc9cd820c00dfebfa30c73e7: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- c4591b600526302f419d3f8f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- ebbae05e7033f89e3b498f7d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- fbe7c34a8b7d57b6d64cccc7: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 0f12515b4d2daa1f7c3adace: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- ecee78bff19a51e9d1e52526: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- a11b005c0e40b20d598aa237: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 1c3f3e73a9b7512cd3491b21: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- aefa03a23283acd5ff4e35ff: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 1407f5dd4ec885764ba87d8d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 021870f6557c1dbd60610edf: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 837b226662b3921cf5c07a59: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- cc9f0e00b416491cdc788c92: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- e612a7941991dfb21f7d0d4b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- d2cc6a2e5c6ac97274cf0c4f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 9824b0d6f5397a64a7646653: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 9a3b6e231bc7eba3365b24bd: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 4b8a98d8f999fea37b32bde2: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- fa6d95b263e511ca146e966d: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 5b0117625a58399aae82e9bb: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- b28703b0cdea90b900c8cad7: MUST; Authorizes public keys to log in to the account. Keys used to log in to an account are explicitly required.
- 5cc49500f354bc1cf21844ee: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- 3ab18b850bed1101d762fa08: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- d9012fa4771e4e4686e9c967: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.

## Additional homogeneous rule checks

PAM stacks: S2.2-1 and S2.2-2 require active authentication/account/session module stacks because they control access and credentials outside their reader. Manual inspection covered the first ten listed entries and raw content: ce36426d9bc200cddc900200, 274f9cc66dc198a1cc2ba58d, e581cb6387cbf187f0923388, 67912141d193bf207cf5489b, 68492d8fadb2a3e81c76739f, 12166c7ff3c49a8165a055c8, 10a6f930fb268691b4f8dc71, 5854afeab0e7e2fb6f6530cb, 35c07ada63f572ae967d102b, dc9cd820c00dfebfa30c73e7.

Firewall chains: S2.2-15 requires firewall policy; chain hooks, default verdicts and referenced chain targets implement that policy. Manual inspection covered the first ten listed entries and raw content: 717eb2770380a84a60c5c313, dda59fbc8826d393f7d01a10, 35cb6ad5449614d23bebe242, a09dad130a88e21ac58d25ca, a1543f91747b9c5a83532869, ea5d40a2dff60d224d49f01a, dd09d750d72e29a6802c0993, 68e163de5be454c2c0f3b7ff, 402a14bcdc254a1331a2d91c, 45fa13af9c9c2849fefd5d4a.

Container images: S2.2-9 and S2.2-12 require programs packaged in container images. Inventory confirms executable server/interpreter images, without establishing cache-only removal behavior. Manual inspection covered the first ten listed entries and raw content: c97d9f250787c54baa1e0b72, 70217070f9a3640192bf6d15, be195af2e23105d0bdf5c1e2, cd7cb3b2f25e9f09baa807d1, 6b15c08f7bc1a541a005da17, b1e3831b876984497b7e8d93, d15f6d19976fd46865b5f935, 51e0bcb301dea3bd5c64a3ac, cbaf6f16dab7fb21b548717b, 390e9a29d1bd114fae135522.

All remaining small categories (fewer than ten cases), individual SSH directives, and non-PAM access files were considered row by row. TSV decisions were appended and flushed; no previous rows were replaced. Verification: 797 unique subset IDs, exact set equality, valid labels, function/reason word bounds.

---

### Component: runtime

# Runtime subset of classification c1

Raw membership was read from (not published: outside selected checks and direct evidence); subtrees were expanded against that inventory. File types and symlink targets were inspected by splitting (not published: external working record) into six NUL-separated fields per object. This inventory supplies metadata, not arbitrary file contents. No removal was performed. Exact applicable sentence quotations are in `part-1.system.notes.md`.

- 3c4a5ca44a8a5ebbd1c4566e: MIXED. Holds runtime communication, configuration, caches, logs, and opaque state. MUST: IPC and service/network/device controls; NOT: logs, blkid cache, motd content; UNKNOWN: credential payloads and unresolved state.
- 6134920786bceac0143188f0: MUST. Supplies network state, resolver configuration, and connection profiles. These records configure connectivity and DNS resolution for other programs; removal prevents their use.
- 1e2ffbcef22fc31ed10f5e2a: UNKNOWN. Holds per-device runtime records with unrecorded contents. Device numbers identify records but do not establish their contents or consumers sufficiently to apply removal.
- 77f73dc46fb102f7d4143c2b: MUST. Stores active Ethernet, loopback, and container-bridge connection profiles. Removing these profiles removes saved network configuration affecting other programs.
- 12903f09c672cfdb37bae7bf: MUST. Supplies daemon control identity and client communication socket. Removal prevents socket-based service requests and PID-file-based daemon control.
- 4ee5f4dd6cfbff8d56159e41: NOT. Caches block-device filesystem identification results. The cached attributes can be probed from devices again; removal costs lookup work.
- 02ccedeb2249f1994496d9d4: MIXED. Combines initialization control, result logs, and unresolved instance records. MUST: stage communication sockets and enable/skip controls; NOT: generator and identification logs; UNKNOWN: configuration and instance-data payloads.
- c3dbba8fd62220c2a05c30b4: MUST. Provides sockets coordinating initialization stages. Removing the socket endpoints prevents those inter-process stage communications.
- 26c5fe90313f5bf3ea6859d3: MIXED. Holds container networking and runtime storage. MUST: networking/control objects; NOT: feature caches and container logs; UNKNOWN: opaque allocation and mount records.
- 0a33a6bb86c050fb7cd4a6d8: UNKNOWN. Holds network allocation database and firewall reconstruction records. Actual allocation and reload payloads are absent; their role after removal cannot be established sufficiently from names.
- lived-t0d208dee0d: UNKNOWN. Holds firewall-driver selection, network mappings, port mappings, and reload lock. All expanded subtree rows were inspected; inventory omits mapping contents and does not establish which records are required versus reconstructible.
- 0ee52b625691a0ca6eee4e12: MIXED. Combines overlay caches, container runtime files, and layer bookkeeping. NOT: overlay feature caches and container logs; MUST: container hostname/resolver/control files; UNKNOWN: mount and lock state.
- 762ffafaa3d3ecf2a97a8b36: NOT. Caches storage-driver capability probe results. Boolean feature-probe markers avoid repeating storage capability detection; removal requires reprobes.
- lived-tfd6364abd7: MIXED. Holds container runtime configuration, process IDs, and execution logs. MUST: hostname, hosts, resolv.conf, process-control IDs; NOT: healthcheck.log and oci-log; UNKNOWN: empty userdata and container marker semantics.
- f10cee980e80d908973eae4e: UNKNOWN. Holds mountpoint metadata and a lock file. Inventory lacks mountpoint contents and lock ownership, preventing a grounded removal decision.
- bb48fe46d346c4c264f69544: UNKNOWN. Holds service credential mount directories without visible credential files. Names identify receiving services, but no credential payload is inventoried; its functional role cannot be established.
- e191ecb79f099f28214c9bb4: MIXED. Combines a seccomp compilation cache with container runtime state. NOT: .cache/seccomp; MUST: container execution configuration; UNKNOWN: status payload and active compiled-filter reconstruction behavior.
- f1a3d1eb92fabda991ee079a: NOT. Caches compiled seccomp filters. The runtime regenerates absent cached filters from the seccomp configuration; only compilation work is repeated.
- 6683d236f92a2116e84aaeb9: NOT. Caches a compiled seccomp filter. The runtime regenerates the missing cached filter from configuration; removal costs recompilation.
- 073776a01f9ed67f0b1842b3: UNKNOWN. Holds OCI configuration, compiled syscall filter, and container status. Configuration affects external processes, but missing status and filter contents prevent classifying all members.
- fa10de89915f71337d422abb: UNKNOWN. Combines printing socket, local authentication certificates, and printcap data. The socket is required, but certificate and printcap payloads are absent; no complete member classification is established.
- 375c0fd4c2dcbd82310abbce: UNKNOWN. Supplies a local CUPS authentication certificate. The object authenticates printing requests; evidence does not establish whether it logs into an account or is an exempt credential value.
- 499c36d697b0f35774976d68: MUST. Provides the system message-bus socket. Removing its pathname prevents new clients from connecting to the system message bus.
- d9b9d57a2cb94aa4b46d135e: MUST. Stores the mail daemon process identifier for control. Removing the PID file prevents other tools from identifying the daemon through that control mechanism.
- d0b1e8126c49fba295e1e2f7: MUST. Provides a device filesystem-check locking object. The lock coordinates filesystem checks across processes; removal disrupts that coordination.
- 8673821e64add7e90b7a2565: NOT. Stores filesystem-check results and log. Both members record earlier filesystem checks; records of the past are explicitly exempt.
- 8acc72cf841e10bf820023ad: UNKNOWN. Holds runtime liveness, synchronization, exit, and persistence records. Metadata alone does not establish active consumers or reconstructibility of each record.
- d12d464dd212e1be081dca1f: UNKNOWN. Holds a container-specific persistence marker. The marker’s content and functional role are not present in the inventory.
- aada1b918d7e6f1ef9633155: MUST. Provides display-server authorization state to the login manager. Removing display authorization prevents clients from obtaining access through that authorization mechanism.
- bfadc2727dd42c7b2498938d: MUST. Provides the display authorization file for the login screen. This authorizes access to the display server, beyond a single program’s internal settings.
- 83df4fcc8614072515c3d1b2: UNKNOWN. Holds a container-network lock and subsystem directory. Active lock ownership and subsystem purpose are not recorded; group removal effects remain unestablished.
- 3514075463fa0b2fb629c62d: NOT. Holds runtime journal logs. These are records of the past, explicitly exempt.
- e207399216a4f2407c5b6d6b: UNKNOWN. Stores userspace mount metadata, event marker, and lock. Without contents the inventory cannot establish whether removal loses required mount-management information or only reconstructed records.
- 96faee23cfad80f11c62c89d: UNKNOWN. Combines monitoring IPC endpoints, shared-memory snapshots, locks, and process records. Sockets provide cross-process communication, but absent shared-memory and plugin contents prevent a complete member decision.
- 2ec09ed4d43badfaf5c422c5: MUST. Provides a named handle to a container network namespace. Removing the handle prevents programs from entering that namespace through its name.
- 7e4bae6cbe52ba4217baf5c6: UNKNOWN. Holds a network proxy socket and lease record. Socket communication is established, but the lease’s content and removal behavior are not.
- 8436e7ac3c935ff9a64f4d4d: MUST. Provides a Unix-socket endpoint for local SSH connections. Removing the socket pathname prevents local clients from connecting through that endpoint.
- 939e3d48274711135dfc0610: UNKNOWN. Combines manager IPC, generated units, runtime identities, and opaque state. Many controls are required, but empty directories and unidentified state prevent a complete member decision; program state is not itself a textual exemption.
- e7d0625995ea6882e9b5f68c: MUST. Supplies inaccessible objects used to mask filesystem paths in services. Removing masking objects prevents constructing the corresponding restricted execution environments.
- 096dac8f293ce472a933e4eb: MUST. Stores active shutdown and sleep inhibition records and references. These references determine whether system-wide sleep or shutdown actions may proceed.
- f45710f1240dec545391e822: UNKNOWN. Combines log transport sockets, sequence state, and stream metadata. Sockets are required communication mechanisms, but sequence and stream payloads are absent; their removal effects cannot all be established.
- c63b26b1e571616560830ffc: UNKNOWN. Combines namespaced journal transport and sequence or stream state. Transport is required; the other members lack content establishing reconstruction and behavior after removal.
- 6c90e97a432b70a67e99e506: UNKNOWN. Stores metadata for a namespaced journal stream. The record’s contents and recovery role are absent; its removal effect cannot be established.
- 852fec2bc63d3ac71655249a: UNKNOWN. Stores journal stream connection metadata. The inventory lists stream identifiers but omits metadata and its persistence requirements.
- 2ffe13225126b0eafd7bc1cf: UNKNOWN. Combines network-manager IPC, leases, and per-link state. The IPC endpoint is required, but missing lease and state contents prevent complete member decisions.
- 2484b9a7200f48906e5a0a25: UNKNOWN. Stores a DHCP lease record. The saved lease contents and whether network configuration depends on this copy are not established.
- 46a1a7e507192230dc2d6500: UNKNOWN. Stores per-link network state records. No contents establish whether each record supplies required network state or regenerable reporting information.
- 05c5cbf3d3e79478dc9e2e5f: MUST. Provides generated network-interface naming and configuration rules. These files govern network interfaces used by other programs; removal loses their configuration.
- 75072271e5ce774a1e4c074d: UNKNOWN. Provides service mount-propagation directories and operating-system identification staging. Metadata alone does not establish the contents and functional significance of every mounted or staged object.
- 4223394cc494d974882ce847: UNKNOWN. Stages an operating-system identification file. Inventory omits the file contents and how consumers use this staged copy.
- 661fb21fd0652ede51512afe: MUST. Supplies resolver IPC and DNS configuration for applications. Removal prevents clients using the sockets or generated resolver files from obtaining name resolution through them.
- 3e4ce0c446a23d164150ee5b: UNKNOWN. Stores interface-specific resolver state. No contents show whether this state changes resolution policy or merely repeats recoverable information.
- 965172b0f877c99e880c2cca: MUST. Tracks the active seat for login and device-access management. Seat records govern session and device access by other programs.
- a13a3ef404a0340bd7b12934: MUST. Tracks active login sessions and lifetime references. Removing these records loses session tracking used for access management and session control.
- 5ce64cd23a18956f7f73d8d5: MUST. Signals successful clock synchronization to dependent services. The synchronization marker controls other services waiting for synchronized time.
- 77294d8118f7be991326b483: MUST. Defines transient process scopes and login sessions. These scope definitions manage external processes; removal loses the associated manager configuration.
- 34aca54d1b3a72227f867869: UNKNOWN. Maps unit names to invocation identifiers. The identifiers are visible but their necessity versus reconstructible observation state is not established.
- fcdd64a0bfe1cae4a8d80c8f: MUST. Provides IPC access to dynamically allocated account information. Removing the socket prevents clients from querying account identities through this interface.
- c4d92427d4f1105932f5cf9a: MUST. Tracks active users for login-session management. The record coordinates account sessions and their lifecycle beyond a single program’s interface.
- c6a7da36ab76e41ca7bb7b64: MUST. Defines creation of static device nodes. Removing the rules prevents the configured device-node creation.
- 655bccb9a0f1c78372d0ac25: MUST. Provides device management IPC, rules, properties, tags, and link arbitration. These objects govern device discovery, naming, permissions, and notifications used across the system.
- 1f73acc6963d3319741a7ec9: MUST. Stores device properties consumed by device-management clients. Removing the database prevents clients from obtaining those device properties for system-wide device management.
- 41e4012b00a54e3c5a47c14f: MUST. Provides generated network-device naming and management rules. Removing these active rules changes network-device handling across the system.
- c4a1dee11485a67935492b1d: MUST. Assigns static device nodes to access-control tags. The tags govern device access outside their reader; removal loses that access-management information.
- c602843c3baeebb0dda0f094: MUST. Marks static sound nodes for session-user access management. Removing these tag links prevents the nodes from being selected through that access-control mechanism.
- 272ca0eea90acf8c418162f2: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- e4c86bf04799f84dc65c5526: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- eb80bcb9340a712e711b9022: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- cc379c16f7a4d6e88614eb17: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- 5713acf00a411e840f191e7b: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- 2dd97b90163476cbf6803daf: MUST. Indexes device tags used by session, device, and service managers. Removal prevents consumers from finding devices by these tags, affecting device access or service activation.
- e10a3b19c715c71585622d29: MUST. Associates device nodes with change-watch identifiers. The association drives device-change monitoring; removal loses the mapping used by the manager.
- 2eb7344e200f359ad0143ac1: UNKNOWN. Contains per-user communication, service control, and unresolved runtime state. Required sockets and controls are present, but not every runtime payload is established.
- aef603088133409bc780d22b: UNKNOWN. Contains an empty runtime directory for the container runtime. No contents or active use establish the effect of removing this directory.
- 9bb994cd6dfde000cc1af9f4: UNKNOWN. Contains desktop IPC, credentials, service control, and unresolved runtime state. Required IPC is established, but credential and opaque state payloads prevent complete member classification.
- d0a97182d1e528680c96661b: MUST. Provides accessibility message-bus IPC. Removing the socket prevents new accessibility clients connecting to the bus.
- lived-t08c37e046d: MIXED. Holds rootless container network state and storage capability caches. NOT: overlay capability markers; MUST: rootless network-namespace handle; UNKNOWN: layer-lock and empty storage-directory behavior.
- 3f7a15da0c1d5f890fa3d77e: UNKNOWN. Contains an empty user D-Bus service-definition directory. No service definitions or consumers of this empty directory are established.
- 2fbf5e7303680e0afe682637: UNKNOWN. Holds a runtime dconf user record. File content and synchronization purpose are absent; names alone cannot distinguish settings, notification state, or cached data.
- 7335bca38ae1aa2cef160d53: MUST. Provides sockets for cryptographic agents and key-management services. Removal prevents new client connections to these cross-program services.
- lived-t742482d423: UNKNOWN. Holds rootless container liveness, process, exit, and persistence state. Expanded members include opaque markers and empty directories; documentation does not establish their current removal effects.
- f4de5507b57b14ea7ee1c9bd: MUST. Provides the sound-server socket and process-control identifier. Removing the socket prevents audio-client connections; the process identifier supports daemon control.
- lived-t912dff2b99: UNKNOWN. Combines generated services, IPC, sandbox objects, and invocation bookkeeping. Generated units and sockets are required; expanded invocation and staging records lack established removal semantics.
- 3f8a1e9dcb986e5bd4ef6c23: MUST. Provides the UUID-generation daemon request socket. Removing the pathname prevents clients requesting UUID generation through this service.
- 6b95eb24a229ca7cc3006cb3: UNKNOWN. Contains display and agent IPC, temporary authorization, and sandbox directories. IPC and sandbox storage functions are established, but the session authority file’s exact function is not recorded.
- c2fea4003589a88b66495f11: MUST. Provides an inter-client desktop session communication socket. Removal prevents new desktop-session clients connecting through the socket.
- 1e82ce9f5d75ca027dd87335: MUST. Provides the X display-server connection socket. Removing the pathname prevents new local graphical clients connecting through it.
- f0e92fe42cf6b79586c49e07: MUST. Provides the authentication-agent connection socket. Removing the socket prevents new clients requesting authentication-agent operations.

## Homogeneous rules, manual checks, and sources

runtime-units: applied the function and cited removal argument printed in the TSV to this homogeneous kind. Ten manual checks: 12c2d64d2ebf681e8767d64e, a7f70abae0cecde027ccb4ec, 6e23c593c8e7e13fa4c560c9, 2522fd31e1b824dae9c0f0c3, 3a5fb2e0dadad685e031e4af, 3d177a90cd7e6a7b4adddecb, 6286c89e9613e865c85c053d, 806602da85009c2283db6ffd, 43bf42b2717f52d3909da367, e9dc2c8f582ded9f8e74211e.

udev-links: applied the function and cited removal argument printed in the TSV to this homogeneous kind. Ten manual checks: d8afe2d2e2457296a32641c5, 84f95d37244bfcc5efb66bd1, dede2f5a66a07bb55c179feb, 7b90d3812458c8bf8f94d1c7, 17dafa76cc2d97c014f43ad2, 0a1c823692d5fb102a24c09e, 8496db9dad161ca529dc38b2, cb9dbab551a2a0cf95633d60, 5da77faaa2abf6319153b6d3, 3cac65e39364d91ef85aa293.

private-tmp: applied the function and cited removal argument printed in the TSV to this homogeneous kind. Ten manual checks: 455662d60114643137f91aaf, 4bc086bca76b1f941115bf27, f66b4d2da0b851d46fcb2b64, 20704b76e189e63df9be6ef1, 28f793abbe5fa4591d560892, 6755ead316becf45477e74ae, 2735cea70cbce64c2ea80bd0, 91c21cebf24b4a1e0a29c4f9, de8f12b69c21fd3a0ad5c4c3, 7ef07f16c38cadd836fc7ba2.

The udev link checks included optical disks, disk sequence numbers, device identifiers and label links; raw targets encode priority and device paths. All ten private temporary directory rows contain only their service-specific backing tmp directory. Runtime unit checks include generated mounts, swap, socket links and network-service drop-ins. All other rows were considered individually.

- https://raw.githubusercontent.com/systemd/systemd/main/src/udev/udev-node.c : “This reads priority and device node from the symlink under /run/udev/links/ directory.”
- https://www.freedesktop.org/software/systemd/man/latest/udev.html : “All device information udev processes is stored in the udev database”. The documentation describes subscribers and device permissions and naming.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html : “the backing storage of the private temporary directories will remain on the host”. The private directories are used as service storage.
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html : “Multiple programs connect to the message bus daemon and can exchange messages with one another.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html : “systemd-journald is a system service that collects and stores logging data.” Stored logs and sockets serving future logging are different objects.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html : “provides network name resolution to local applications”. This includes documented Varlink sockets and generated resolv.conf.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-logind.service.html : “Keeping track of users and sessions, their processes and their idle state.” The documented responsibilities include device access and sleep inhibition.
- https://networkmanager.dev/docs/api/latest/NetworkManager.html : “Information about networking is exported via a D-Bus interface to any interested application”.
- https://raw.githubusercontent.com/containers/crun/main/src/libcrun/seccomp.c : `#define SECCOMP_CACHE_DIR ".cache/seccomp"`; the implementation retrieves cached filters and regenerates them when retrieval fails.
- https://man7.org/linux/man-pages/man8/blkid.8.html : “blkid - locate/print block device attributes”. The documented cache stores probe results.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-tmpfiles.html : “systemd-tmpfiles creates, deletes, and cleans up files and directories”.

UNKNOWN reflects absent payload or use evidence after checking the relevant program documentation; it is not a claim that program state is a definition hole. Mixed rows identify the differing member families explicitly.

Additional primary-source verification:

- https://raw.githubusercontent.com/containers/storage/main/drivers/overlay/overlay.go : `cachedFeatureCheck(runhome, feature)` precedes capability probes; missing cache results fall through to `doesVolatile`, `supportsIdmappedLowerLayers`, `supportsOverlay`, and analogous metacopy/native-diff probes.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-time-wait-sync.service.html : “The presence of this file indicates to this service that the system clock has been synchronized.” This establishes the behavior of the synchronized marker.
- https://www.cups.org/doc/policies.html describes operation authentication and user/group restrictions. The collected certificate file has no payload or issuer/account metadata; its exact role remains UNKNOWN rather than importing an unstated general exemption for secrets.

Validation: 150 unique runtime IDs; exact equality with the assigned runtime subset; all labels valid; all function and reason fields satisfy their word limits.

---

### Component: sources

# Reserved source-tree, Go, and preference rows

The 86 reserved stored-object rows were inspected individually. Their output is part-1.sources.tsv; sources_classify.py records one explicit decision per ID. The three CMake refinements and the checksum-checkpoint source citation are recorded in sources_refine.py. These are named decisions, not a suffix-wide automated classification rule. The writer appended and flushed each row; final in-session refinements changed only the documented rows.

The same permitted inputs and exact sentences listed in part-1.code.notes.md apply. No other classification or unassigned task folder was read. No guest object was deleted or executed. The filesystem dump is a NUL-delimited six-field inventory; it is not newline-delimited. The stored-object members in the original objects.tsv are proper JSON arrays. For every subtree the source rows were selected by exact name or prefix plus slash and the stored-outside-packages kind, and their member arrays were expanded before deciding. Ordinary rows retain their own member arrays.

## Individual review record

The complete 86-row set was read and decisions assigned by named ID, including all of the following distinctions:

- Compose examples were read one subtree at a time, with full member paths. Flask, Django, FastAPI, PHP, Node server and test code are MUST. Browser JavaScript and static pages/assets are NOT under S2.2-11/4. Readme/license/screenshot material is NOT. Values read by an application are NOT under S2.2-7/13. Dockerfile/Compose descriptions remain HOLE because the text does not delimit indirect process specification versus settings. Compiler-input source is HOLE at the content/build-capability boundary; this does not assert that compiled binaries are content.
- Browser frontend directories were not assumed homogeneous: Angular karma.conf.js, Vue babel.config.js, React setupProxy/setupTests and test JavaScript are interpreter programs, while browser-executed frontend code is exempt. The Java and Rust examples additionally hold compiler inputs; SQL files contain database instructions rather than merely captured table contents, leaving the program-interface/authority boundary unresolved.
- Five stored Git subtrees include runnable sample hook programs (MUST), history/logs/source-object records (NOT), and Git-internal values (NOT). These groups differ from the executable-only hook groups because they include stored histories and metadata.
- Each .github subtree contains only hosted workflow/ownership/dependency-update metadata or issue templates. The specified workflows run on designated runners rather than being executable files on this inventoried machine. [Workflow documentation](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows): “each of which will execute on a runner machine”. These repository descriptions receive NOT as content here; this is not a claim about a self-hosted runner installed on a different machine.
- Express lib contains six runtime JavaScript modules, all MUST. Examples and tests contain MUST server/test modules and EJS templates alongside NOT static files. [EJS](https://ejs.co/): “EJS is effectively a JavaScript runtime.” Other template forms retain the unresolved interface/content distinction; they were not assigned unrestricted authority merely by extension.
- The two Python environments contain interpreter activation scripts and program libraries (MUST), distribution metadata/licenses (NOT), and native Python bytecode caches (HOLE: S2.2-5 versus S2.2-10). [Python virtual environments](https://docs.python.org/3/library/venv.html) describes “their own independent set of Python packages”. Environment isolation is package isolation, not a VM exemption. [Python modules](https://docs.python.org/3/tutorial/modules.html): “A module is a file containing Python definitions and statements.” Cached bytecode improves loading but remains executed code; no precedence is supplied by the hypothesis.
- Flask docs includes actual conf.py and make.bat programs as well as RST and images. [Sphinx configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html): “The configuration file is executed as Python code at build time”. The 91 expanded members were checked so the documentation directory was not wrongly treated as entirely content.
- Flask source includes py.typed/README content and __pycache__ alongside Python runtime modules. Flask tests/examples include Python programs and static data; template/SQL roles remain separately marked. [Jinja sandbox](https://jinja.palletsprojects.com/en/stable/sandbox/): “Access to attributes, method calls, operators, mutating data structures, and string formatting can be intercepted and prohibited.” The existence of this optional confinement does not establish the authority of every template in the inventory.
- zlib doc is six content documents, whereas its top-level tree includes built executables and a native shared library (MUST), documents/logs (NOT), and source/build intermediates (HOLE). Contributed and platform-specific trees were inspected separately. [CMake language](https://cmake.org/cmake/help/latest/manual/cmake-language.7.html): “Script mode simply runs the commands in the given CMake Language source file”. Consequently CMakeLists.txt and actual .cmake programs are MUST, even where their filename sounds like configuration; .cmake.in generator templates were not silently equated with executed files. This evidence caused the test row to become MIXED rather than uniformly HOLE.
- Both bin/subl rows contain a symlink whose target is the same absent macOS Applications launcher. The target appears only in the symlink-target fields and never in the pathname fields of the complete six-field filesystem inventory. Removal reasoning therefore loses no runnable program. Both rows are NOT. This finding uses (not published: raw inventory over 20 MB), not a guess from the filename.
- Both init rows have exactly four value files: editor preferences, two terminal color descriptions, and window-manager preferences. These are NOT, separately from the shell and Vimscript configuration programs in dotfiles.
- Go bin contains the installed hey program (MUST). The module tree contains source/archive/checksum-download caches (NOT), as well as cached executable shell/generation/build scripts (HOLE: cache/code overlap). The retained checksum latest file is not treated as an ordinary replaceable tile. [Go checksum client](https://raw.githubusercontent.com/golang/go/master/src/cmd/vendor/golang.org/x/mod/sumdb/client.go) describes it as the “latest known” signed tree and checks that new and older observations share a consistent history. Thus the latest checkpoint is both a record of past observation and an input to detecting inconsistent histories, yielding HOLE under S2.2-1/6.

The apparent homogeneity of Compose folders was not used as a blanket rule: the record explicitly separates the purely documentary official-documentation-samples subtree, Python/PHP/server code, browser code, testing/build code, compiled source, credentials, value files and recipe descriptions. Rows with identical reasons were still expanded individually.

## Validation

86 reserved input IDs equal 86 unique output IDs, with no extra/missing ID. All decisions are in the required five-word vocabulary, all function descriptions are at most 15 words and reasons at most 30 words. Final counts: MUST 2, NOT 10, HOLE 5, UNKNOWN 0, MIXED 69. This is structural validation, not independent acceptance.

---

### Component: varlib

# Part 1: stored objects under /var/lib

The 89 assigned rows were inspected through (not published: direct evidence over 2 MB) and the six-field NUL records in (not published: raw inventory over 20 MB). For each reduced subtree, all original stored-object rows at or below its prefix were gathered. No directory was removed, no service changed and no executable launched.

A directory-group decision refers to the listed members. For example, the overlay row lists layer links, lower-chain metadata and empty mount/work directories, not the excluded layer payloads. The volume subtree contains WiredTiger collections, indexes, journals and diagnostics. Flatpak exports include activation-service links, icons, metadata and generated caches. The repository objects have opaque digest names; mode bits do not establish each file's function, so this subtree remains UNKNOWN instead of assuming every object is executable.

The inventory verifies that cloud script directories, the CNI networks directory and the display-manager data directory contain no files. Their empty contents are NOT; this does not classify hypothetical future scripts or rules. The Cloud-init instance subtree has actual saved configuration/user-data files whose contents were not collected. Completion stamps are known history; uninspected provisioning inputs remain UNKNOWN, yielding MIXED.

All non-helper rows were decided individually. Small loops in classify-varlib.py only emit separately inspected rows with identical explanations; they do not generalize from a sample to unknown paths. MIXED reasons identify the relevant member names or suffix families. An UNKNOWN constituent is expressly named rather than silently treated as content.

## One homogeneous rule: package-maintenance enablement records

The 25 deb-systemd-helper and deb-systemd-user-helper directory rows are NOT under S2.2-6. Their markers preserve previous package-managed service state; they are not the active service-manager enablement symlinks. This matters because the suffix .wants alone could suggest the opposite classification.

S2.2-6: “records of the past—logs, history;”

The specific exemption for records of past events is applied even where later scheduling or maintenance consults the record. It likewise decides the individual timer timestamps, saved synchronization clock and configuration-history copies. This is not a claim that those records have no behavioral consequences, or a new design requirement for accumulated state.

Ten hand-checked IDs and observed roles:

- 4e072a15763b4a1a1133071b: helper root, .dsh-also files and recorded target associations.
- 9140d0e0763d33c3a86e94f5: recorded cloud configuration target association.
- b76a79bba43e1c1f9abcbaf0: recorded provisioning target services.
- 13177aa156a7ffca6aadb143: recorded default-target network helper.
- 067ca62be79e9cfb037e1fb2: recorded firewall reload association.
- 038156e92c4b157696ea5476: recorded graphical-target services.
- f0a9fc130f6243697682fcca: recorded hibernation association.
- a223979f276780ba185c85fb: recorded hybrid-sleep association.
- e6c7b500df6175d8c883f1e4: recorded multi-user-target services.
- eeec51f5cefa10d0ad4cf0e2: recorded network-online association.

## Other sentences used exactly

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-12: “This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

Operational metadata HOLE decisions ask whether removal loses only the described content or also the capability that interprets its associations. They do not ask how a system should retain, transfer or clean application state; Section 2.5 design choices are not counted as holes.

## Public documentation

- https://manpages.debian.org/trixie/init-system-helpers/deb-systemd-helper.1p.en.html — “The "was-enabled" action is not present in systemctl”. The description explains that this detects service state before installing an updated service file.
- https://docs.cloud-init.io/en/latest/explanation/first_boot.html — “When it runs, cloud-init stores a cache of its internal state for use across stages and boots.” The page explains first-boot identity checking; this cache is not automatically the slower-only exemption.
- https://docs.cloud-init.io/en/latest/reference/cli.html — documents cleaning state and rerunning initialization; it does not reveal the actual saved user-data contents here.
- https://www.networkmanager.dev/docs/api/latest/NetworkManager.conf.html — “it is read last and can shadow user configuration”. The internal configuration therefore affects network configuration.
- https://manpages.debian.org/trixie/apt/apt-mark.8.en.html — “manual is used to mark a package as being manually installed”. Manual marking prevents automatic removal; extended_states carries those decisions.
- https://manpages.debian.org/trixie/dpkg/dpkg.1.en.html — “dpkg is a medium-level tool to install, build, remove and manage Debian packages.” It describes status information and executable maintenance operations.
- https://docs.flatpak.org/en/latest/under-the-hood.html — “every application that is installed is stored in a local version control repository”. Deployment links and repository payloads are distinct inventory objects.
- https://docs.flatpak.org/en/latest/extension.html — documents Locale, graphics, codec and runtime extensions; language content differs from executable runtime libraries.
- https://github.com/containers/storage/blob/main/docs/containers-storage.conf.5.md — documents persistent image/container storage, overlay driver and volume storage locations. Inventory member names provide the specific structures classified here.
- https://www.freedesktop.org/software/systemd/man/latest/loginctl.html — documents enable-linger and keeping a user manager running after logout.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — documents persistent timer trigger timestamps.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html — “It also saves the local time to disk every time the clock has been synchronized”. The saved clock is history even though startup consults it.
- https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “This machine ID adheres to the same format and logic as the D-Bus machine ID.” The inventoried D-Bus entry is a symlink to the system identifier.
- https://manpages.debian.org/trixie/ucf/ucf.1.en.html — “ucf optionally creates copies of versions of the configuration file”. The cached copies are previous configuration versions, distinct from active destinations.
- https://manpages.debian.org/trixie/libpam-runtime/pam-auth-update.8.en.html — describes central authentication-policy generation; the precise state-file contents remain unavailable.
- https://ghostscript.readthedocs.io/en/latest/Use.html — describes font mapping and PostScript interpretation. Exact Fontmap/cidfmap contents are needed to distinguish mapping values from interpreted operations here.

Validation: exactly 89 assigned IDs, each once; all decisions valid; function and reason word limits checked.

## Final validation

The final validation script checks the exact header; equality of input and output ID sets and counts; uniqueness; decision vocabulary; sentence IDs; field limits; and absence of embedded tabs/newlines. It writes the completion marker only after all assertions pass. No inventory files were changed.
