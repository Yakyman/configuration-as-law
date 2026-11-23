# A3R scripted classification rules

15 homogeneous rules. Full final membership is in (not published: trial intermediate downloads and scratch); other rows were inspected by explicit member/path lists and serialized individually.

Q1, Q2 and Q3 are tested in R5 order. U1 and U2 are coverage statements. Nonexecutable-file U3 conflicts with functional Q2/Q3/U7 classifications where coverage does not determine the result. Missing factual contents are marked FACT_UNKNOWN, not treated as omissions in PAGE.

All subtree assessments use the inline description and allowed raw filesystem/candidate inventories. The original `(not published: direct evidence over 2 MB)` named by some subtree descriptions was not opened. When a raw descendant listing could not reconstruct the selected members sufficiently, the result remains FACT_UNKNOWN.

## A3-GROUP

Applied rows: 39. Sentences: Q2a,R1. Result: SETTING / YES / DECIDED.

The local Unix group identity and membership determine permission rights. Q2a names rights explicitly. This classifies the group object, not a stored /etc/group file.

Manual check: Checked ten distinct GID and membership entries, including empty groups, against the supplied raw group lines.

Ten manually checked rows:

- `424cb5f40e407805606b43e3` — `root`.
- `2f8d930a409d1f2bdd2c5fa3` — `news`.
- `66f84c6596ff4a6dc3ea673c` — `fax`.
- `9a8089d2eeea3b59a0b02b99` — `www-data`.
- `b72dd4393cd9f7458b722482` — `irc`.
- `da017f5c4a67da07e8a06462` — `staff`.
- `1d85d40be9bd534d0216f83d` — `systemd-timesync`.
- `67c5fe367565649d58a7dac6` — `systemd-resolve`.
- `21cd7479491cdca0c99ad183` — `rtkit`.
- `31bd900cf43ed37298d6d895` — `colord`.

## A3-PROCESS

Applied rows: 22. Sentences: Q1,R5,U6,R1. Result: PROGRAM / YES / DECIDED.

A reported running executable with its own process satisfies Q1 and U6. A row aggregating PIDs of that executable has the same decision.

Manual check: Checked the ten executable names and PID evidence: dbus-daemon, conmon, gvfsd, two Netdata helpers, timesyncd, networkd, NetworkManager, cupsd and cups-browsed.

Ten manually checked rows:

- `1c460643fdd8cfbbd196d5c8` — `10`.
- `42c8a140e560dc29380e1d8c` — `12`.
- `1de8c224f0b98ee3c699a8f1` — `15`.
- `5170ad8d1f6cab983ec4aac9` — `2`.
- `405fd3b1305197a3b82e9395` — `204`.
- `0182a17a4f357d35fb9e7954` — `33`.
- `2130dee9e966a8190632a24f` — `395`.
- `5bf49f96a1afbe0b43e14736` — `78`.
- `0720c840cf4025df688545f2` — `82`.
- `e117d280137522e247ca6e90` — `9`.

## A3-PACKAGED-METADATA

Applied rows: 914. Sentences: U1. Result: PACKAGE_PART / COVERED / DECIDED.

Installed package metadata accompanies executable code in that same distribution: Python dist-info, npm program manifests, or bundled editor extension metadata. A dependency in another package does not satisfy this rule. Data-only packages and repository manifests without established package receipt were excluded.

Manual check: Checked the ten named distributions and their companion code: setuptools, rich, accepts, foreground-child, @noble/hashes, which, lru-cache, minipass, VS Code profile-table, and python-debian. Raw filesystem evidence confirms code; npm archive fields confirm package identities where present.

Ten manually checked rows:

- `51cba7cfc1bf2684737e1902` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools-80.10.2.dist-info/METADATA`.
- `dc5f771fd89e773fe701d2b2` — `/home/user/.local/share/pipx/venvs/httpie/lib/python3.13/site-packages/rich-15.0.0.dist-info/METADATA`.
- `3c13c1b446f62a2091e66f53` — `/home/user/Projects/express/node_modules/accepts/package.json`.
- `fe9da317da5b967b33c925dc` — `/home/user/Projects/express/node_modules/spawn-wrap/node_modules/foreground-child/package.json`.
- `9ccb3e1db3c71ae0579ef07e` — `/home/user/Projects/express/node_modules/@noble/hashes/package.json`.
- `2e9eb7a5d906ca90c5e08108` — `/home/user/Projects/express/node_modules/which/package.json`.
- `12db1f81bda753113f8c78e7` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/lru-cache/package.json`.
- `b1f92c6af383244e223ed275` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/minipass-pipeline/node_modules/minipass/package.json`.
- `89263f1523eab494b081abea` — `/usr/share/code/resources/app/extensions/ms-vscode.vscode-js-profile-table/package.json`.
- `dc127f353179f767622f14f2` — `/usr/lib/python3/dist-packages/python_debian-1.0.1.dist-info/METADATA`.

## A3-PROJECT-MANIFEST

Applied rows: 20. Sentences: Q1,Q2,Q3,U1,U3. Result: NONE / NA / FACT_UNKNOWN.

The actual manifest content/use or same-package receipt is not established for the reviewed project/test repository manifests. Names alone cannot decide active launch values, inert test fixtures, or covered program companions.

Manual check: Checked the ten supplied manifest paths and found no corresponding content in the allowed npm manifest archive; the raw filesystem gives only file metadata. The executable bit on the React-nginx JSON file does not make JSON executable code.

Ten manually checked rows:

- `111ac6ae8f61f144f23a651b` — `/home/user/Projects/express/package.json`.
- `1755b8b12329fa9ef4e7d695` — `/home/user/Projects/awesome-compose/react-express-mongodb/backend/package.json`.
- `95e10fb176d8247651f64687` — `/home/user/Projects/awesome-compose/angular/angular/package.json`.
- `dfea1ccd803a93bd82d031c8` — `/home/user/Projects/awesome-compose/vuejs/vuejs/package.json`.
- `4fe53d82e2d45abc64274c5d` — `/home/user/Projects/awesome-compose/react-express-mysql/frontend/package.json`.
- `16ad8b552b196edd6936655b` — `/home/user/Projects/awesome-compose/react-java-mysql/frontend/package.json`.
- `bf9cdf50537bde62221191cf` — `/home/user/Projects/awesome-compose/react-nginx/package.json`.
- `d4a673ba0f9e480ad29d2ae8` — `/home/user/.nvm/test/fast/Unit tests/mocks/project_dirs/no-nesting-both/package.json`.
- `471978163bc81d841e96f954` — `/home/user/.nvm/test/fast/Unit tests/mocks/project_dirs/nested-both/package.json`.
- `de96b9753d56039499868261` — `/home/user/.nvm/test/slow/nvm reinstall-packages/test-npmlink/package.json`.

## A3-ELPA

Applied rows: 48. Sentences: Q1,U4,U1,U2,R1. Result: PROGRAM / YES / DECIDED.

Each reviewed installed ELPA group contains executable Emacs Lisp constituting its program. Same-package accompanying data and bytecode compiled from its sources are included through U1/U2. An unrestricted Lisp program is not shown to satisfy the restricted-code condition in U5.

Manual check: Checked full member arrays: each sample contains .el code and corresponding .elc copies, with only its package metadata, manuals or other companions. Verified individual file types, rather than treating the directory name as proof.

Ten manually checked rows:

- `93a93428a9d00a2b2aac9e6f` — `/home/user/.emacs.d/elpa/ace-window-20220911.358`.
- `2849da8d3ffd4d63a249cb05` — `/home/user/.emacs.d/elpa/compat-31.1.0.0`.
- `b57acba86305d76781092c20` — `/home/user/.emacs.d/elpa/diff-hl-20261001.135`.
- `2de188ef32a4888a6c5dfacd` — `/home/user/.emacs.d/elpa/embark-20260610.302`.
- `4a3a2165780fe4bdeefc00e5` — `/home/user/.emacs.d/elpa/flycheck-eglot-20260810.1731`.
- `25869031ce72c51019016578` — `/home/user/.emacs.d/elpa/llama-20261001.1538`.
- `73f9ca51f63a8a99456a158c` — `/home/user/.emacs.d/elpa/operate-on-number-20231114.1921`.
- `a5e614ff093c756b5eb313dc` — `/home/user/.emacs.d/elpa/rainbow-delimiters-20210515.1254`.
- `28c2162d8f319e0dbebb54ab` — `/home/user/.emacs.d/elpa/transient-20261113.1458`.
- `f268c0c891b35623595c114b` — `/home/user/.emacs.d/elpa/zop-to-char-20260105.452`.

## A3-SHELL-AND-DOCS

Applied rows: 327. Sentences: Q1,U3,U4,R1,R2. Result: NONE / NA / MIXED.

For the reviewed direct-member groups containing only sourceable .zsh/completion code and nonexecuted documentation, code is PROGRAM/YES and documentation MATERIAL/NO. These source-tree groups have no established same-package coverage. Extensionless unfamiliar fixtures are excluded.

Manual check: Checked all members of ten sample groups: each has README.md and its named .plugin.zsh. Shell source can execute through the installed shell even without an executable mode bit.

Ten manually checked rows:

- `02509ece652faa30d530a089` — `/home/user/.oh-my-zsh/plugins/ansible`.
- `2e55b962c4165c285c96a9e1` — `/home/user/.oh-my-zsh/plugins/cloudfoundry`.
- `07618ec243b56b1f72ea40c8` — `/home/user/.oh-my-zsh/plugins/fancy-ctrl-z`.
- `00ef3ec2875b821c3a651330` — `/home/user/.oh-my-zsh/plugins/hanami`.
- `cd63ca51db3751138b8437a7` — `/home/user/.oh-my-zsh/plugins/kops`.
- `4744c5712ac928b5dcfaec2e` — `/home/user/.oh-my-zsh/plugins/nmap`.
- `31c628b483398e953ad3d390` — `/home/user/.oh-my-zsh/plugins/pulumi`.
- `223cb070f41f6dc7a7ff0dbc` — `/home/user/.oh-my-zsh/plugins/skaffold`.
- `493bd0f8dc99ec1aae6a61c6` — `/home/user/.oh-my-zsh/plugins/tig`.
- `4f25115549cd290ab72efd82` — `/home/user/.oh-my-zsh/plugins/zoxide`.

## A3-MIME-INDEX

Applied rows: 13. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The standard generated per-type MIME database XML files are constructed from installed MIME definitions. U2 covers the generated list through its recorded source definitions; this is not a rule that every file under /usr/share is covered.

Manual check: Checked every direct member and its regular-file type in ten content-type groups. They contain only the generated XML descriptions, with counts 516,62,1,101,7,7,9,150,33,1 respectively.

Ten manually checked rows:

- `4aba607ff59c3ee376310758` — `/usr/share/mime/application`.
- `4ff815d792c6f07c0e70cdd2` — `/usr/share/mime/audio`.
- `a1bc9af2c8b24e04764d16e0` — `/usr/share/mime/chemical`.
- `946c59a84dd618138088be86` — `/usr/share/mime/image`.
- `a3a29542d4b538e850acb99b` — `/usr/share/mime/inode`.
- `7d4c3c7f666b1008ee71489d` — `/usr/share/mime/message`.
- `f4785d34ecdd63e5d9727007` — `/usr/share/mime/multipart`.
- `f9b368f6ebd3f6e3a358d20e` — `/usr/share/mime/text`.
- `b4719b4d765ff90d4af34b9b` — `/usr/share/mime/video`.
- `e5ab7eeee3f7f8114537bfea` — `/usr/share/mime/x-epoc`.

## A3-MAN-INDEX

Applied rows: 26. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The reviewed man-db cache groups contain derived lookup indexes, formatted-page cache layout and its constant cache tags. Their installed manual/source definitions and manager construction cover the generated representation under U2.

Manual check: Checked ten full member arrays containing index.db, cat directories and CACHEDIR.TAG; no user-authored setting or unrelated history file appeared in these groups.

Ten manually checked rows:

- `4510afc64020ce965c69c93a` — `/var/cache/man`.
- `d5d756c7be695e8e3c3240e3` — `/var/cache/man/da`.
- `359b5c84d186097c4737d4f3` — `/var/cache/man/fi`.
- `67cab6a3b21ee18171e913bf` — `/var/cache/man/hu`.
- `bf30125ac236b891339b4642` — `/var/cache/man/ja`.
- `2045c9f7bc5deb3e07489e08` — `/var/cache/man/nl`.
- `08d5b1a0eccbb1fe0ea550ec` — `/var/cache/man/pt_BR`.
- `ee5ad85821d870c36b151353` — `/var/cache/man/sl`.
- `e4ee0cd5019fba5e14c8c679` — `/var/cache/man/tr`.
- `6e304c9a1e2d8b725f108cc5` — `/var/cache/man/zh_TW`.

## A3-SERVICE-MARKERS

Applied rows: 23. Sentences: Q3,U3,R2. Result: NONE / NO / TWO_WAYS.

The selected deb-systemd-helper marker files remember earlier package enablement operations. Q3 calls them PROGRAM_RECORD and U3 calls their nonexecuted file form MATERIAL. Both allow omission. They are not the service-manager enablement links themselves.

Manual check: Checked ten complete marker groups and helper documentation. Named target directories contain helper state files for the listed services; parent directory groups with mixed contents were excluded.

Ten manually checked rows:

- `9140d0e0763d33c3a86e94f5` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-config.target.wants`.
- `13177aa156a7ffca6aadb143` — `/var/lib/systemd/deb-systemd-helper-enabled/default.target.wants`.
- `038156e92c4b157696ea5476` — `/var/lib/systemd/deb-systemd-helper-enabled/graphical.target.wants`.
- `e6c7b500df6175d8c883f1e4` — `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`.
- `54924688efdcbb112c962280` — `/var/lib/systemd/deb-systemd-helper-enabled/printer.target.wants`.
- `5e5ac15281a5827c5b46e88e` — `/var/lib/systemd/deb-systemd-helper-enabled/ssh.socket.wants`.
- `1810ae1e70bf481d6cba3512` — `/var/lib/systemd/deb-systemd-helper-enabled/sshd@.service.wants`.
- `2afaf280a4caf6a672848578` — `/var/lib/systemd/deb-systemd-helper-enabled/sysinit.target.wants`.
- `60af4555f895a621f8fdd8b5` — `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants`.
- `3dbad18363c3236ada19e5bb` — `/var/lib/systemd/deb-systemd-user-helper-enabled/sockets.target.wants`.

## A3-GIT-TEMPLATES

Applied rows: 11. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

Git initialization copies its supplied hook templates into each repository. The reviewed groups contain only those .sample template copies, whose recorded Git package source covers the copies under U2. Active non-template hooks are excluded.

Manual check: Checked all fourteen .sample files in each of ten sample rows against the raw listing and Git template documentation. The Flask repository with an extra pre-commit hook was separately classified.

Ten manually checked rows:

- `lived-t98b49255b3` — `/home/user/.config/nvim/.git`.
- `lived-tf3cef8f65e` — `/home/user/Projects/zlib/.git`.
- `lived-teaff14fb6e` — `/home/user/Projects/express/.git`.
- `lived-t5524f36a07` — `/home/user/Projects/dotfiles/.git`.
- `lived-t377338389c` — `/home/user/Projects/awesome-compose/.git`.
- `lived-tb8a7a2c063` — `/home/user/.emacs.d/.git/hooks`.
- `lived-ta4806d9131` — `/home/user/.oh-my-zsh/.git/hooks`.
- `lived-tc5d3d1ad66` — `/home/user/.nvm/.git/hooks`.
- `62c9ae1c4efb4911e0b9bb51` — `/home/user/.emacs.d/.git/hooks`.
- `35edf48c3f0ceba543518341` — `/home/user/.oh-my-zsh/.git/hooks`.

## A3-SSH-ACCESS

Applied rows: 72. Sentences: Q2a,R1. Result: SETTING / YES / DECIDED.

Each reviewed effective SSH value directly defines admission, permitted session rights, or network transport. Q2a expressly names access rules, rights and network settings. Generic helper paths, server-identity sourcing and cleanup values are excluded.

Manual check: Checked the ten complete option values and their OpenSSH semantics: PAM, minimum RSA size, Kerberos authentication, TTY permission, forwarding prohibition, trusted user CA, ciphers, accepted environment names, source network grouping and connection penalties.

Ten manually checked rows:

- `5f8fcf77e7c5041de9f3e517` — `ssh-access:usepam`.
- `64c3eeeb56074c666b06d5da` — `ssh-access:requiredrsasize`.
- `c820f0571c36594777b32e84` — `ssh-access:kerberosauthentication`.
- `d6235a098bb82243371dc8d0` — `ssh-access:permittty`.
- `63d8ebafc9125aab5fdb691d` — `ssh-access:disableforwarding`.
- `6fa7d4f75e0e35c7fade8b0d` — `ssh-access:trustedusercakeys`.
- `602b5e23a1883323cc8e5024` — `ssh-access:ciphers`.
- `d962db55ec61443e174b4687` — `ssh-access:acceptenv`.
- `363323f681d7fb46cf88fb80` — `ssh-access:persourcenetblocksize`.
- `b3bc32c5ee21a357406dd84d` — `ssh-access:persourcepenalties`.

## A3-SSHD-INTERNAL

Applied rows: 13. Sentences: Q2,Q2a,U1. Result: NONE / NA / FACT_UNKNOWN.

The enumerated operational SSH helper paths, server-identity sources and cleanup values are known, but human selection versus supplied defaults is not. They do not themselves establish incoming authorization under Q2a.

Manual check: Checked the ten complete effective values: Kerberos cleanup, GSSAPI cleanup/rekey storage, authentication information exposure, PID path, xauth path, two helper paths and two server host-key paths.

Ten manually checked rows:

- `c462b75395e079a1aca2a05a` — `ssh-access:kerberosticketcleanup`.
- `bbad5c6166456c8edcbaefd6` — `ssh-access:gssapicleanupcredentials`.
- `19dab249d75fc4989eb0155c` — `ssh-access:gssapistorecredentialsonrekey`.
- `9a64547fcefb3cbdbd52c4f3` — `ssh-access:exposeauthinfo`.
- `21f275a8d1b48381331c9b31` — `ssh-access:pidfile`.
- `acdf33b140bddd83baac8d1a` — `ssh-access:xauthlocation`.
- `17e46fc45310b9c16b42f4fa` — `ssh-access:sshdsessionpath`.
- `8ec96424e643f241a4f7de9b` — `ssh-access:sshdauthpath`.
- `837ebb63632431b7c3f91ae6` — `ssh-access:hostkey`.
- `8fe45bad30e49b61dfc9f9ca` — `ssh-access:hostkey`.

## A3-BARE-DIRS

Applied rows: 32. Sentences: Q2,Q3,U1,U2. Result: NONE / NA / FACT_UNKNOWN.

The actual listed members are only directory objects. Their ownership and names do not establish human-selected values, creator, same-package receipt or recorded construction source. Descendant contents are not silently added to a direct-member row.

Manual check: Checked all members of ten sampled arrays against the raw filesystem type d. The evidence establishes directories, but not the provenance or purpose needed to choose Q2, Q3, U1 or U2.

Ten manually checked rows:

- `124769f893ee21f77303b4c8` — `/etc/.java`.
- `0f67b7bae2a57cc2763a2fa2` — `/home`.
- `56e2e00352bb36231b2da3cd` — `/home/user/.config/xfce4`.
- `f0f627cc3b46b105b0b8df40` — `/home/user/.mozilla`.
- `993eeee5d668d53456ff626c` — `/home/user/.rustup/toolchains`.
- `c89bfd140525874cbc0324a5` — `/home/user/go/pkg`.
- `e49ce9aff8bf785dea731470` — `/root/.cache`.
- `70a8e6d79cabbeacbabea47c` — `/usr/lib/systemd`.
- `71d0194ea4194cf7d9b01977` — `/var/cache`.
- `ccbaeccf53ee2710e325cf92` — `/var/lib/flatpak/runtime`.

## A3-RUNTIME-DIRS

Applied rows: 12. Sentences: Q3,R2. Result: PROGRAM_RECORD / NO / DECIDED.

The reviewed direct members are transient directories created by identified running service managers. Q3 classifies their operational records; U3 speaks of a file, whereas these rows specifically enumerate directory objects. No executable or human-selected value is in the member array.

Manual check: Checked ten complete arrays and raw directory types for Netdata, container runtime, service credentials, propagation, per-user runtime and service-private temporary directories. This rule is limited to the actual directory objects.

Ten manually checked rows:

- `e53242b3cc2dd5fcf94d88a7` — `/opt/netdata/var/run`.
- `26c5fe90313f5bf3ea6859d3` — `/run/containers`.
- `0ee52b625691a0ca6eee4e12` — `/run/containers/storage`.
- `bb48fe46d346c4c264f69544` — `/run/credentials`.
- `e191ecb79f099f28214c9bb4` — `/run/crun`.
- `75072271e5ce774a1e4c074d` — `/run/systemd/propagate`.
- `2eb7344e200f359ad0143ac1` — `/run/user`.
- `aef603088133409bc780d22b` — `/run/user/0`.
- `3f7a15da0c1d5f890fa3d77e` — `/run/user/1000/dbus-1`.
- `8297b831c6bc820c295b314d` — `/var/tmp`.

## A3-STDLIB-CACHES

Applied rows: 32. Sentences: U1,U2. Result: BUILT / COVERED / DECIDED.

The reviewed outside-package Python standard-library stored groups are compiled __pycache__ copies of adjacent installed sources. The source/cache pairing, not the older inventory class label, establishes U2.

Manual check: Checked source and cache pairs in ten distinct modules: __phello__, collections, curses, ensurepip, importlib, pathlib, sqlite3, unittest, wsgiref and zoneinfo. Raw .cpython-313.pyc basenames match the adjacent .py sources; imported package subdirectories have the same pairing.

Ten manually checked rows:

- `lived-t913be4d2c3` — `/usr/lib/python3.13/__phello__`.
- `lived-ta4abd40fce` — `/usr/lib/python3.13/collections`.
- `lived-t020ed9822e` — `/usr/lib/python3.13/curses`.
- `lived-tfaa53a1101` — `/usr/lib/python3.13/ensurepip`.
- `lived-tc32257a21c` — `/usr/lib/python3.13/importlib`.
- `lived-t2c72d68466` — `/usr/lib/python3.13/pathlib`.
- `lived-t1897ca9a23` — `/usr/lib/python3.13/sqlite3`.
- `lived-t30677237b3` — `/usr/lib/python3.13/unittest`.
- `lived-t4a9f19aaf4` — `/usr/lib/python3.13/wsgiref`.
- `lived-tbe88daa394` — `/usr/lib/python3.13/zoneinfo`.

## Factual documentation

- [Installed Python package metadata](https://packaging.python.org/en/latest/specifications/recording-installed-packages/).
- [npm package.json](https://docs.npmjs.com/files/package.json/) and [npm scripts](https://docs.npmjs.com/using-npm/scripts.html/).
- [Unix groups](https://man7.org/linux/man-pages/man5/group.5.html).
- [Emacs package installation](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html).
- [Zsh source execution](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html).
- [Debian service helper state](https://manpages.debian.org/testing/init-system-helpers/deb-systemd-helper.1p.en.html).
- [MIME database generation](https://specifications.freedesktop.org/shared-mime-info/latest-single/).
- [Git initialization templates](https://git-scm.com/docs/git-init).
- [Python compilation](https://docs.python.org/3/library/py_compile.html).
- [OpenSSH options](https://man.openbsd.org/sshd_config).

Raw factual evidence is cited in individual rows; public documentation supplies the general file-format and mechanism semantics. Original appended rows and the correction overlay are retained for audit.
