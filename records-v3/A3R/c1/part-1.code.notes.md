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
