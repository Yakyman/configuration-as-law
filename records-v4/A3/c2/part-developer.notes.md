# Classification c2, part developer of A3: rules and checks

Input: (not published: direct evidence at least 2 MB) (6409 rows). Output: `A3/c2/part-developer.tsv`. Scripts: `A3/c2/scripts/`
(`build.py` writes the output, `members_rules.py` and `system_groups.py` hold the rules, `verify.py` checks it,
`sample_check.py` printed the hand-check sample, saved as `raw/hand-check-samples.txt`).
`raw:` paths in the `basis` column are relative to the inventory root `A3/in/raw/developer/`.
Text read: TEXT.md Sections 8.1–8.3 and 8.5, SENTENCES.md. No other classification was read.

## How group rows are decided

Each `2:stored-ownership-unresolved` row is a directory whose complete list of immediate children is in
`members/<id>.tsv` (all 4933 lists are complete). Every child (file, link, directory, socket, fifo) is decided by
the four questions of S8.2-6 in order. A row whose members all get one decision gets that decision; otherwise
`MIXED`, and the reason gives the count per decision with the most frequent label. The 619
`2:code-ownership-unresolved` rows are single files that are also members of group rows; they get exactly the
decision of that member, so code rows and their groups cannot disagree.

Facts used for members: type, mode/exec bit, mtime from the member table; ctime from `configuration-origin.tsv`
(present for every regular file under the home trees); package file lists and integrity from
(not published: over 20 MB) and `package-files.tsv`; the `shebang` flag of code rows (COLLECT.md: files with
executable bits, `#!`, or shell startup paths are listed). File contents are not in the inventory.

## Rules applied by script, with sentences

General rules (all members):

- **G1 Q1 for files of a package tree.** A file or directory lying inside the unpacked tree of a package that an
  installer installed (Julia versions by juliaup, npm packages by bun, the hello keg by brew, the lefthook gem by
  RubyGems, the ruff wheel by uv, micro plugins by micro's built-in plugin manager) is "obtained as part of such a
  package" (S8.2-7). It "remains as received" when its ctime is not later than the end of the installing action
  (action log mtimes: Julia 11:13:59, bun/gem/uv 11:14:05, micro 11:14:06, brew 11:15:23 UTC; inode(7): ctime
  changes on every write or metadata change, doc:https://man7.org/linux/man-pages/man7/inode.7.html). All such
  files satisfy this. Decision `INSTALLED-PACKAGE` (S8.2-8, S8.2-16). The package's own top directory is the
  package: `INSTALLED-OWN` when installed at a person's command, `INSTALLED-DERIVED` when installed as a
  dependency. Installers: juliaup ("a cross-platform installer for the Julia programming language", README),
  bun, Homebrew's brew, RubyGems, uv (S8.1-4); micro ("a built in plugin manager", plugins.md) and lefthook
  (`lefthook install`/`uninstall` of Git hook scripts) count in that part of their functionality (S8.1-5).
- **G2 What is code (Q2).** A file is code the computer can execute when (a) its extension or name belongs to a
  language whose interpreter/runner is installed here (rpm list `raw/0013`: bash, python3, perl, tcl, ruby,
  java source launcher, go (`go run`), gawk, make, docker; plus julia and bun from the actions): .sh .bash .py .pl
  .pm .tcl .rb .rake .gemspec .java .go .jl .js .mjs .cjs .ts .mts .cts .jsx .tsx .awk .mk, Makefile, Dockerfile,
  Rakefile, Gemfile, bash startup names, uv `activate`; or (b) it is a shared library (.so); or (c) it has an
  executable bit and is not text/data (LICENSE, README, .md, .json, .yml …). Not code: type declarations and
  source maps (.d.ts, .map: read as values, S8.2-23); binaries and libraries for another OS or architecture, and
  Go files excluded on linux/amd64 by their file-name build constraint or lying in golang.org/x/sys/windows or
  /plan9 (S8.2-20; doc:https://pkg.go.dev/go/build#hdr-Build_Constraints); code in languages with no interpreter
  here (zsh, fish, csh, lua, R …; S8.2-20). Limit: build tags written inside Go files are not in the inventory.
- **G3 Links.** A symbolic link holds a path that the kernel and programs read as a value; it is not itself code
  (S8.2-23). Links inside a package tree follow G1; links that are enablement of a service follow Q3; other links
  written by a program are program records (S8.2-15).
- **G4 Directories.** A directory is decided like any object: part of a package tree (G1), otherwise not code and
  not a value chosen by a person, so Q4: written by a program for its own storage → `RECORD`; part of something a
  person brought (a cloned project or downloaded checkout) → `MATERIAL` (S8.2-15).
- **G5 #! without known interpreter.** A file flagged as starting with `#!` that G2 does not already make code and
  that would otherwise be RECORD/MATERIAL is `UNKNOWN`: the interpreter named in the line is not recorded (a
  program if installed here, else not). Exception: bun's `*.npm` manifest cache files start with the format header
  "#!/usr/bin/env bun\nbun-npm-manifest-cache-v0.0.8\n" followed by serialized data
  (doc:https://github.com/oven-sh/bun/blob/main/src/install/npm.rs) → `RECORD`.

Tree rules (each a homogeneous kind; hand-checked ids below):

- **R1 rpm packages** (45 rows). Q1 yes. dnf reason user → `INSTALLED-OWN`; dependency / weak dependency →
  `INSTALLED-DERIVED` ("a package installed as a dependency of a recorded package", S8.2-16); native reason group
  (glibc, glibc-all-langpacks) → `INSTALLED-DERIVED` (obtained by the system from a group list, not chosen
  individually); gpg-pubkey pseudo-packages → `INSTALLED-DERIVED` (dnf imported each key itself from the repository
  `gpgkey`, logs "Importing OpenPGP key 0x621E9F35 / 0xF577861E").
- **R2 npm packages under bun global** (78 rows). Only eslint was requested (log "installed eslint@10.15.0 with
  binaries", "78 packages installed"): eslint `INSTALLED-OWN`, the other 77 `INSTALLED-DERIVED`.
- **R3 rpm-shipped gems** (76 rows). Every gemspec is in an rpm file list (`raw/0017`), integrity unchanged:
  obtained as part of an installed rpm → `INSTALLED-PACKAGE`. lefthook gem (row by row): `INSTALLED-OWN`.
- **R4 processes** (74 rows). `RUNTIME` (S8.2-5), owner = executable; `unknown` = readlink of /proc/PID/exe
  failed, a kernel thread (doc:https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html).
- **R5 netfilter rows** (531 rows). Live kernel ruleset: `RUNTIME`; table inet firewalld → firewalld, ip/ip6
  tables and iptables-save lines → dockerd. iptables-save comment lines ("# Generated by …", "# Completed on …")
  describe the inventory command, not an object → `ACTION` (S8.2-4).
- **R6 Julia version trees** (G1) → `INSTALLED-PACKAGE`; version directories `INSTALLED-OWN`.
- **R7 bun global node_modules** (G1, R2); `.bin` links and manifests → `RECORD`.
- **R8 bun package cache.** Code files (G2) → `PROGRAM-DERIVED` (Q2 precedes Q4; bun obtained them itself for the
  eslint line); everything else → `RECORD`.
- **R9 Homebrew checkout** (`/home/linuxbrew/.linuxbrew/Homebrew`). Not a package: placed by the install script;
  the installer documentation has a separate uninstall script, no installer both installs and removes it (S8.1-4,
  S8.1-6). Code (G2) → `PROGRAM-OWN`; other files and directories → `MATERIAL` (downloaded files); `.git` objects
  `MATERIAL`, git working state `RECORD`, sample hooks `PROGRAM-OWN`.
- **R10 Homebrew prefix and Cellar.** Keg files G1; `Cellar/hello` and its version directory `INSTALLED-OWN`;
  prefix directories, links written by brew, `var/homebrew` state → `RECORD`.
- **R11 scc project** (cloned at a person's command). Code (G2) → `PROGRAM-OWN`; the `scc` binary built by a
  person's `go build` → `PROGRAM-OWN`; `lefthook.yml` → `SETTING-OWN` (S8.2-14: it launches the hook commands);
  `.git/hooks/pre-commit` → `INSTALLED-OWN` (package of lefthook); other files/directories → `MATERIAL`.
- **R12 Go module cache** (`.cal-modcache`). Go source (G2) → `PROGRAM-OWN` (downloaded by `go` for a person's
  build; modules are downloaded, not installed); other entries → `RECORD`.
- **R13 Go build cache.** No member is executable; compiled outputs → `RECORD`.
- **R14 runtime trees** (`/run`, `/tmp`, `/var/tmp/systemd-private-*`, rpc_pipefs). Exist only while running
  (tmpfs; PrivateTmp directories are removed when the service stops, systemd.exec(5)) → `RUNTIME`, creator named.
- **R15 /var/cache** (dnf, PackageKit, man-db caches) → `RECORD`.
- **R16 SELinux module store.** Policy modules (access rules, S8.2-13) written by package scriptlets during
  installation → `SETTING-DEFAULT` (S8.2-17).

Hand-checked rows (10 per rule; printed with members in `raw/hand-check-samples.txt`; all fit the rule — the check
found one wrong sub-rule, executable LICENSE files counted as code, fixed before the final build):

- R1: developer-adace3ff93d390f5f20468bb, developer-03ae8d81719aee482d47b7fe, developer-60e33259995ec8ec0f3027b3, developer-af9c0a608cc0f364c46b411d, developer-f7aa5e692becc0c5c61e0e8b, developer-41e633b9828b9d4c6b54075c, developer-49cfece694819e34b0b2bdc2, developer-3d78f74ecf21220545a26372, developer-a9c234e9e53100aaefb19797, developer-27b851a1b6fae6ac0ac93d84
- R2: developer-33258a0a7d8a25f745dc5d62, developer-a68d7b9e3275c4e05b099159, developer-e9d6250588941d53ae0aafdf, developer-b0e682fa031f5ba17f817367, developer-74660fbb0b0234f75654baf7, developer-56fa9b372bbe5ab119b83cea, developer-6c15a536e991b17af73a8e09, developer-00214b07b4d92d07e427d616, developer-ba60fedd55c56d0023fa36a7, developer-ad8ffcefb997f57554f14aa0
- R3: developer-61e112614ae10c7f28291e6f, developer-fcef9d7bc832dffac259befa, developer-4a46a493c0e5f865a24ef2fd, developer-9a364d90a5ece1bfadd78be6, developer-cfb5a8d1fc19e1ab2f875ead, developer-2d3dda893cd66ebd463fa9fe, developer-2c425af7b032e32349298def, developer-bd09f6b5aef9f19750f63155, developer-7bc1eb4a8f3c15bc6a06b7c4, developer-8d7d5abd632778912e79e87c
- R4: developer-443867e2e1377d066a5c11d1, developer-b62957c281f1ae18457eb314, developer-937321895032a5d5a7c9f42e, developer-e0c7c1f53cdb3be53703d00b, developer-d9c2ff76e2ac3a590a6f37f7, developer-84937f4020d30556c36d468c, developer-bf1af4d29a45db7b71509aa3, developer-283f01e91790e326c3a1cc17, developer-3a5b794cef745cb302d4192d, developer-b7ba42aa58253622baa46f6e
- R5: developer-c7631bc86f8dcb5c92defa04, developer-622117fae8f4e752e272fac8, developer-3c90d9045a752f71df644503, developer-aae8bec781f0d76c2466beb4, developer-4480ed86f01ca53827ebec0a, developer-bca3ed55d2e4136925ccea4f, developer-3048732cb47990a547780147, developer-a3ba5d636a3c6c0967aca85c, developer-b99beb97d3a0428ce9f9b11a, developer-c228cab35ad9f242cbc69702
- R6: developer-679b0f10bc92d69c148c5d86, developer-ca03c9631a64ab60c1d85978, developer-e89e91463ce10afd82756696, developer-8f544d1498c9e1af77ff037d, developer-76637395404a642ec66647e7, developer-46d74e0686c02619fe909c6d, developer-f6aa12e01683bd2ca9ea8938, developer-b932ebf498047204398f8f49, developer-3d14ba0bde8e43dffa5bcf2c, developer-aa1b5400666a47c4202d72d6
- R7: developer-c8b2febdc47c29c1b76f6a63, developer-3c2b5efb77db4dbb4aa23223, developer-111f950089af0c336b509949, developer-54d475f0b73f6b3e4e8f9671, developer-e2fa766da6240ad09560bf0a, developer-6d5ef5f9a7718af07ec36c8a, developer-372014b2910fad6fad91da8e, developer-c24c1663de86f53ee19a40d7, developer-9525b3125a695f0dd69aa605, developer-cbf3a4e54d0bc5321c12f50a
- R8: developer-36acb5e83e0d43825d627db3, developer-572eea2e5c07380f9559e3e4, developer-f291c43a0a58060a36ae69e1, developer-7458c2b96c9674a66b366add, developer-37e91a536ba8fff45f744389, developer-573dc84d4423691f441cbfd1, developer-1eddb8449a1d79aa23506ab1, developer-59b37763101dda48156bd929, developer-b1ace3f2f0f8760a1b351ef7, developer-d6212afaacd014b4d64bbaaa
- R9: developer-faecdc9d2bb66be06532500c, developer-ae7ca9bf4814c8f141d78439, developer-5b0ca0d6f405c8c810905fd5, developer-1ad7b43bf1bf2f60fc4a4028, developer-56c881eebc9d580b045c66bc, developer-e7e2bd8fc3a477d540dd47c4, developer-2f1aac18cceca7a98655895b, developer-85429eee4a0f9d66b96c79f0, developer-eaeb6da805d1c1884b12555a, developer-f0c70c4f9ec590183f1f3de0
- R10: developer-303e7af087530a624b2f4b25, developer-af16a47b2b77eb44089610c4, developer-6333cf15cca29790b883fe3c, developer-0361093c5518f3bc959587af, developer-da0f83e3035426a83d257705, developer-504886de449af61f102ae272, developer-fb29a9ff45f491b6e6fe5846, developer-acf622850b88138f29989fe6, developer-10ff7951098339992fe442bf, developer-ef767df669c457238d263797
- R11: developer-866d127011f5b3349ff3ddad, developer-2c1cf2c92d8832719ee686ab, developer-49686859d7e09c304655b23a, developer-0997991ce6c36bf1d464b5fc, developer-02c252037019691412121cbf, developer-408554e7f54732c22e808e75, developer-7d922a432b3a47c159d8b478, developer-4df01afc948e0d33feb04a2b, developer-0c2556703ef638841a0bcc1c, developer-60965e34ebf0e29465df2295
- R12: developer-a5d4d92ee596597a53a0b569, developer-df1d72de57942bb0d50bbddc, developer-8e68a35c43fe2c85c78cb1f0, developer-36b68d5c50fb866dd813265c, developer-8520f1bbe308cb1ec790ec70, developer-98497de27fe00342d838c94b, developer-4683c0b58af94c75de7c3782, developer-15956ea73c4a843e2ff54723, developer-a0e1441a66e97a6f30005670, developer-1edc82d6c0039cd78c86fd11
- R13: developer-ac78bae1601bb68233bcbcc4, developer-d4cd7bfbba17a026517cc68e, developer-62c23583599848d7b48cec63, developer-72080ff59343e3e1053d6ba8, developer-021bde761fef9193085f6409, developer-9cfe3cd62af5cad35e6acd1c, developer-ad7a656b46121d0a3bb8271c, developer-23f52a9471d9718724fb944b, developer-2ba43df2358630fb671c294e, developer-1789cdc9fa7bc0bc1e756d05
- R14: developer-29e0e54310bc54f4bd737781, developer-d8c82be937425f3a2714f20f, developer-7cc98b97da311e96c6dfe85e, developer-0ef8e3143aa4fbe5cf1d2228, developer-1823a6c15272550982af6ae4, developer-e9742bdc22cf2e4beb72b875, developer-d8deb3f7e7d9b7ed77178048, developer-ad049be7fc84b4e2033c8217, developer-bcf9c367d105e86dec70b0cb, developer-790bfb88293b645aa68bf3ec
- R15: developer-c4a22e672a8fcf730bd68d47, developer-1cd23c18894c0cc477c8ba8f, developer-f3ca214b2449237048a8a48a, developer-cf2c0dc4ac3cde9ee5bcbe9f, developer-9eb01aa1bd924cc2d9814d92, developer-9512f5fb14019fbad63a0265, developer-b18942244cf40aafde94a3ba, developer-124d1926819770671dd1cd42, developer-a7bd0248c98e0d5f216c72f6, developer-6f9a52bcac80bffc6cfb44b7
- R16: developer-827de59a22caf840fe290dd6, developer-7629071caf08bf76d4faebb6, developer-1fbc6f4255b06cd8b6eae86c, developer-415845ec28d649347ee0a93d, developer-32429ba275af6dd0c28aa7dd, developer-b6a60ac96d1daf216eb32707, developer-5ed3ca80705d356b0f6b5deb, developer-cc5c652eaf47718e492adad6, developer-c3578867a926b34eaf097e2b, developer-e8c8e2ba0a562dc2de20f182

## Decided row by row (explicit tables in the scripts)

Level-1 rows other than packages, processes and netfilter: the docker group (`SETTING-DEFAULT`: group file
rewritten 11:14:48 inside the docker-ce dnf transaction), services/timers/user timers (`RUNTIME`, owner named),
unit files (docker.service enabled against preset → `SETTING-OWN`; containerd.service at preset →
`SETTING-DEFAULT`), user units (`SETTING-OWN`), ports and kernel modules (`RUNTIME`), the two NetworkManager
connections (in /run → `RUNTIME`), the container (S8.2-22) and the locally built image (`PROGRAM-OWN`), the two
unexpanded engine stores (`MIXED`), the uv-cache ruff dist-info (`RECORD`). Home files outside the trees
(`.bashrc`, `.bash_profile` → `PROGRAM-OWN`, S8.2-23; `.bash_logout` from /etc/skel → `PROGRAM-DERIVED`;
`authorized_keys` → `SETTING-OWN`; private key → `MATERIAL`; `juliaup.json` → `SETTING-OWN`; uv, bun binaries →
`PROGRAM-OWN`: their documented removal is deleting files, so no installer removes them). System groups under
/etc, /root, /usr, /var/lib, /var/log in `system_groups.py`.

## Gaps and unknowns in this part

- GAP-TWO, juliaup binaries (3 code rows; (not published: record outside this collection) group): juliaup is installed by its own init program
  and removed by `juliaup self uninstall` (README). Whether that makes juliaup "what an installer installs and
  removes as a whole" (S8.1-6) — INSTALLED-PACKAGE — or not — PROGRAM-OWN — the text does not say.
- GAP-TWO, (not published: record outside this collection): self-update options set at juliaup's installation; SETTING-DEFAULT if
  juliaup is a package, SETTING-OWN otherwise (follows the gap above).
- GAP-TWO, values written by a program as it ran with no person choosing them and not at package installation:
  firewalld `docker` zone and `docker-forwarding` policy written by dockerd at its first start; resource drop-ins
  in `/etc/systemd/system.control` written by a daemon. Q3 requires "a value chosen by a person" (→ RECORD by Q4),
  while S8.2-17 covers defaults only "obtained with a package or created during its installation".
- UNKNOWN: (not published: record outside this collection) (content not recorded: setting if it launches something or grants access, S8.2-14,
  else record); `/etc/resolv.conf` link and `FedoraWorkstation.xml` zone (who chose them not recorded);
  SELinux `booleans.local`; 9 files starting with `#!` whose interpreter is not recorded (G5).
