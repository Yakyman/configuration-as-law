# A3R scripted classification rules

Script rule count: **13**. Individual adjudications: **300**.

Classification code: (not published: trial helper scripts); explicit individual decisions: (not published: trial helper scripts); review corrections to already appended rows: (not published: trial helper scripts). `a3r-assignments.jsonl` maps each output ID to its rule or individual decision. Revisions concern this run only.

A group listing directory objects is not automatically a recursive group; `:subtree` groups are recursive but their selected membership is not recoverable merely by enumerating every raw path under the prefix. Older inventory class labels do not establish PAGE classifications. The unreferenced part-1.tsv mentioned by some evidence is outside the permitted raw roots and was not read.

Q1 has priority over Q2 even for executable received package parts. NONE/NO/DECIDED is used when material-versus-record creator uncertainty cannot change record=NO, as the task explicitly requires. MIXED is retained only when differing member decisions are established.

## A3-01. Effective group and SSH access values
Rows: 124. Sentences: R6,Q1,Q3,Q3a,R1,L2.

Effective values do not establish installation-default versus independent-choice origin. These alternatives yield COVERED versus YES, hence FACT_UNKNOWN. Group entities are SETTING; SSH effective values retain NONE where received/default and locally selected objects can differ under Q1/Q3a. The group entries give name/GID/membership; SSH entries give effective parameters without per-value origin.

Ten manually inspected rows:

- `424cb5f40e407805606b43e3` — `root`
- `c9026e221a81a2c85175525f` — `uucp`
- `9a8089d2eeea3b59a0b02b99` — `www-data`
- `2e62e78d8fca69e2a348f1e5` — `nogroup`
- `7b30d550f377d95effa87f34` — `user`
- `5f8fcf77e7c5041de9f3e517` — `ssh-access:usepam`
- `d858b7eb5b5db644a78163d0` — `ssh-access:pubkeyauthentication`
- `acdf33b140bddd83baac8d1a` — `ssh-access:xauthlocation`
- `60d688cfe3148facddc7533d` — `ssh-access:subsystem`
- `b3bc32c5ee21a357406dd84d` — `ssh-access:persourcepenalties`

## A3-02. Live process representations
Rows: 22. Sentences: R5,Q2,L1.

Each process instance is RUNTIME/NO. Its executable is named and creator record=NA when package provenance is absent. Concatenated PID evidence can obscure the exact executable association but every candidate remains a process with NO for its own line.

Ten manually inspected rows:

- `1c460643fdd8cfbbd196d5c8` — `10`
- `8b1dbd0e6a04dda53f042fdf` — `11`
- `42c8a140e560dc29380e1d8c` — `12`
- `7f68c5deb8bee8904640065d` — `17`
- `f33262b97d15e4256f2f249d` — `207`
- `0182a17a4f357d35fb9e7954` — `33`
- `2130dee9e966a8190632a24f` — `395`
- `5bf49f96a1afbe0b43e14736` — `78`
- `47c30908758abecdcb2d11b7` — `87`
- `e117d280137522e247ca6e90` — `9`

## A3-03. Metadata files without established receipt or unchangedness
Rows: 901. Sentences: R6,Q1,Q3b,Q4,U4,L1,R2.

The filesystem metadata proves paths and types, not unchanged installer receipt or original source provenance. Original package metadata can be COVERED; independently generated descriptive records can be NO; launch-controlling values can require YES. Therefore FACT_UNKNOWN. The ten checks include Python METADATA, VS Code package.json, packages.config and nested npm package.json. The referenced npm JSON archive provides contents for npm cases but no integrity/provenance comparison.

Ten manually inspected rows:

- `3ce5b4911a70e4f372f050fc` — `/home/user/.vscode/extensions/ms-vscode.cpptools-1.35.6-linux-x64/package.json`
- `440bccd20764e280ea521c1a` — `/home/user/.vscode/extensions/ms-python.debugpy-2026.6.0-linux-x64/packages.config`
- `4845c523758595ad09dc608b` — `/home/user/.vscode/extensions/ms-python.python-2026.10.0-linux-x64/python_files/lib/python/microvenv-2025.0.dist-info/METADATA`
- `0ef0bcc49c7c28c1c746129b` — `/home/user/.local/share/pipx/venvs/pre-commit/lib/python3.13/site-packages/packaging-26.3.dist-info/METADATA`
- `ab8e0d6b13c2e3ff0e856223` — `/home/user/Projects/express/node_modules/@nodelib/fs.scandir/package.json`
- `01b39a7e7ca4afbd186ad23b` — `/home/user/Projects/express/node_modules/@isaacs/cliui/node_modules/ansi-regex/package.json`
- `225a3cf1cab7ef096e921b39` — `/home/user/Projects/express/node_modules/cliui/node_modules/wrap-ansi/package.json`
- `d398a97eca3186fa2ad9a5d4` — `/home/user/Projects/express/node_modules/body-parser/package.json`
- `449f54455c7cdc741fe0faf1` — `/home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/http-proxy-agent/package.json`
- `dc127f353179f767622f14f2` — `/usr/lib/python3/dist-packages/python_debian-1.0.1.dist-info/METADATA`

## A3-04. Immediate shell and Emacs extension file groups
Rows: 401. Sentences: R6,Q1,Q2,Q4,L1.

Immediate named plugin groups have source/compiled-file names and support data, without actual current code contents, unchanged-package provenance or a generating declaration source. Thus FACT_UNKNOWN rather than inferring blanket package coverage or a certain mixed result from suffixes. Each sample was checked against its member list; numeric collapsed subtrees are excluded.

Ten manually inspected rows:

- `ab4e48545791db0d53dc71b0` — `/home/user/.oh-my-zsh/plugins/1password`
- `92da532490c5e0e8cdfd4554` — `/home/user/.oh-my-zsh/plugins/argocd`
- `4291b3badbd506a67c858704` — `/home/user/.oh-my-zsh/plugins/bedtools`
- `5bd34cd01937767ea4867a5e` — `/home/user/.oh-my-zsh/plugins/cake`
- `e98614533c5d71a7094f16a2` — `/home/user/.oh-my-zsh/plugins/compleat`
- `aad804a919899545a7be1f36` — `/home/user/.oh-my-zsh/plugins/git-escape-magic`
- `064a9ca3d9ec62f471f8d61f` — `/home/user/.oh-my-zsh/plugins/nats`
- `147187a5315d2a32f8444caf` — `/home/user/.oh-my-zsh/plugins/symfony`
- `93a93428a9d00a2b2aac9e6f` — `/home/user/.emacs.d/elpa/ace-window-20220911.358`
- `38cc2f41f8f8aac99bb9fbcd` — `/home/user/.emacs.d/elpa/consult-20261004.957`

## A3-05. Volatile /run objects
Rows: 42. Sentences: R5,Q2,L1.

Every selected object is in volatile /run storage: sockets, synchronization state, manager records or runtime-generated objects. RUNTIME/NO, naming the creating daemon and creator record=NA when provenance is absent. Creator provenance cannot change the absence of an own runtime line.

Ten manually inspected rows:

- `3c4a5ca44a8a5ebbd1c4566e` — `/run`
- `1e2ffbcef22fc31ed10f5e2a` — `/run/NetworkManager/devices`
- `02ccedeb2249f1994496d9d4` — `/run/cloud-init`
- `0a33a6bb86c050fb7cd4a6d8` — `/run/containers/networks`
- `073776a01f9ed67f0b1842b3` — `/run/crun/bfd24acb04736a47cf127d1325687a516315ccbe1fa0e1ec6cb4e839e9ebcc13`
- `fa10de89915f71337d422abb` — `/run/cups`
- `96faee23cfad80f11c62c89d` — `/run/netdata`
- `939e3d48274711135dfc0610` — `/run/systemd`
- `2ffe13225126b0eafd7bc1cf` — `/run/systemd/netif`
- `lived-t912dff2b99` — `/run/user/1000/systemd`

## A3-06. Man-db cache groups
Rows: 26. Sentences: R6,Q4,R2.

Observed cache directories and index.db files are generated search/formatting records, not manual package payloads or executable code: PROGRAM_RECORD/NO. Ten language-specific groups were checked for their index and directory members.

Ten manually inspected rows:

- `4510afc64020ce965c69c93a` — `/var/cache/man`
- `8d3198283b0bc001a8363861` — `/var/cache/man/cs`
- `d5d756c7be695e8e3c3240e3` — `/var/cache/man/da`
- `775c7e0626a8d2764f6561aa` — `/var/cache/man/de`
- `0c14914a1646a594dd64c510` — `/var/cache/man/es`
- `359b5c84d186097c4737d4f3` — `/var/cache/man/fi`
- `d93b8cfda4b3fa40f11328c7` — `/var/cache/man/fr`
- `ecaea5af3e3b04c0aadb97f4` — `/var/cache/man/hr`
- `67cab6a3b21ee18171e913bf` — `/var/cache/man/hu`
- `cfbbb1277d81eda3111f05d7` — `/var/cache/man/id`

## A3-07. Package service-enablement history
Rows: 25. Sentences: R6,Q4,R2.

These deb-systemd-helper and deb-systemd-user-helper markers remember installation operations. They are distinct from actual service activation links: PROGRAM_RECORD/NO. The ten checks include system and user helper directories and individual dsh-also/target history markers.

Ten manually inspected rows:

- `4e072a15763b4a1a1133071b` — `/var/lib/systemd/deb-systemd-helper-enabled`
- `9140d0e0763d33c3a86e94f5` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-config.target.wants`
- `b76a79bba43e1c1f9abcbaf0` — `/var/lib/systemd/deb-systemd-helper-enabled/cloud-init.target.wants`
- `13177aa156a7ffca6aadb143` — `/var/lib/systemd/deb-systemd-helper-enabled/default.target.wants`
- `067ca62be79e9cfb037e1fb2` — `/var/lib/systemd/deb-systemd-helper-enabled/firewalld.service.wants`
- `038156e92c4b157696ea5476` — `/var/lib/systemd/deb-systemd-helper-enabled/graphical.target.wants`
- `f0a9fc130f6243697682fcca` — `/var/lib/systemd/deb-systemd-helper-enabled/hibernate.target.wants`
- `e6c7b500df6175d8c883f1e4` — `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`
- `60af4555f895a621f8fdd8b5` — `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants`
- `3dbad18363c3236ada19e5bb` — `/var/lib/systemd/deb-systemd-user-helper-enabled/sockets.target.wants`

## A3-08. Exact installed Flatpak runtime components
Rows: 42. Sentences: I1,I2,R6,Q1,R1,L1.

The paths identify the exact org.gnome.Platform installed checkout by commit and files/ subtree. These received metadata components are INSTALLED/COVERED by that runtime package. The ten checks verify distinct dist-info metadata entries within the same deployed commit, including vendored setuptools dependencies.

Ten manually inspected rows:

- `51cba7cfc1bf2684737e1902` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools-80.10.2.dist-info/METADATA`
- `35b08e5e2c7d0df863990fcb` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/jinja2-3.1.6.dist-info/METADATA`
- `55f8a1b78a6e7fe96e1c0645` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/attrs-26.1.0.dist-info/METADATA`
- `b5a812108fee30bde128868b` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/packaging-26.3.dist-info/METADATA`
- `6971545a28a58d7a6172ec28` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/mako-1.4.1.dev0.dist-info/METADATA`
- `608b6340b64cfca363330534` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/markdown-3.10.3.dist-info/METADATA`
- `5e4917158f087301a8fc8b13` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/tomli-2.4.0.dist-info/METADATA`
- `e78e15d8f9683164d61faf24` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/more_itertools-10.8.0.dist-info/METADATA`
- `e85b221073f95ef465518069` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/jaraco_context-6.1.0.dist-info/METADATA`
- `7356c19233248767ccd1f7a1` — `/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/49/2bb946ea4ebb050f6a32f90e979feb975b08280d1ff1aac881dec3d1361ad84d/files/lib/python3.13/site-packages/setuptools/_vendor/jaraco_functools-4.4.0.dist-info/METADATA`

## A3-09. Git sample-hook groups
Rows: 11. Sentences: Q1,Q2,U1,L1.

The names match Git template sample hooks, but current contents and unchanged-template/source relation are absent. Generated original copies may be COVERED, independently changed executable files YES, or nonexecutable fixtures NO: FACT_UNKNOWN. Ten lists were checked for sample hook names and the absence of content/provenance evidence.

Ten manually inspected rows:

- `lived-t98b49255b3` — `/home/user/.config/nvim/.git`
- `lived-tf3cef8f65e` — `/home/user/Projects/zlib/.git`
- `lived-teaff14fb6e` — `/home/user/Projects/express/.git`
- `lived-t5524f36a07` — `/home/user/Projects/dotfiles/.git`
- `lived-t377338389c` — `/home/user/Projects/awesome-compose/.git`
- `lived-tb8a7a2c063` — `/home/user/.emacs.d/.git/hooks`
- `lived-ta4806d9131` — `/home/user/.oh-my-zsh/.git/hooks`
- `lived-tc5d3d1ad66` — `/home/user/.nvm/.git/hooks`
- `62c9ae1c4efb4911e0b9bb51` — `/home/user/.emacs.d/.git/hooks`
- `e8b46637cbde5543ea5779f8` — `/home/user/.nvm/.git/hooks`

## A3-10. Collapsed Python library/cache subgroups
Rows: 35. Sentences: Q1,Q2,Q4,U4,L1.

The raw filesystem prefix contains more objects than the collapsed selected-member count. The allowed evidence does not recover which members are selected, or their source integrity. Received files, compiled copies and independent additions have different kinds/coverage: FACT_UNKNOWN. Ten raw prefixes were checked and compared with selected counts; no whole-prefix membership was silently substituted.

Ten manually inspected rows:

- `lived-t913be4d2c3` — `/usr/lib/python3.13/__phello__`
- `lived-tc5242e687e` — `/usr/lib/python3.13/_pyrepl`
- `lived-td2cb3c5e97` — `/usr/lib/python3.13/asyncio`
- `lived-ta4abd40fce` — `/usr/lib/python3.13/collections`
- `lived-ta2011e6fc2` — `/usr/lib/python3.13/concurrent`
- `lived-t4ca37c4992` — `/usr/lib/python3.13/ctypes`
- `lived-t020ed9822e` — `/usr/lib/python3.13/curses`
- `lived-td982437c2e` — `/usr/lib/python3.13/dbm`
- `lived-t3ded61c21e` — `/usr/lib/python3.13/email`
- `lived-td75eac9783` — `/usr/lib/python3.13/encodings`

## A3-11. Generated MIME database groups
Rows: 14. Sentences: R6,Q4,R2.

The observed type-description outputs and lookup indexes are generated by update-mime-database, outside its source packages/ directory: PROGRAM_RECORD/NO. L1 is a coverage rule for already-classified installed objects; its generated-list example does not turn all generated descriptive data into installed objects. Ten MIME-type/index groups were checked.

Ten manually inspected rows:

- `a4de6292d1e78167decc7081` — `/usr/share/mime`
- `4aba607ff59c3ee376310758` — `/usr/share/mime/application`
- `4ff815d792c6f07c0e70cdd2` — `/usr/share/mime/audio`
- `a1bc9af2c8b24e04764d16e0` — `/usr/share/mime/chemical`
- `2c84f6f7d6b126564d10c278` — `/usr/share/mime/font`
- `946c59a84dd618138088be86` — `/usr/share/mime/image`
- `a3a29542d4b538e850acb99b` — `/usr/share/mime/inode`
- `7d4c3c7f666b1008ee71489d` — `/usr/share/mime/message`
- `a57811114eec1362d29f52a8` — `/usr/share/mime/model`
- `f4785d34ecdd63e5d9727007` — `/usr/share/mime/multipart`

## A3-12. Collapsed extension groups
Rows: 28. Sentences: I1,I2,Q1,Q2,Q4,L1.

Collapsed Emacs, shell and VS Code extension groups do not expose the selected member list or current content/receipt integrity. The raw full-prefix count differs from the selected count. Received assets, executable additions and inert records can differ, so FACT_UNKNOWN. Ten full raw prefixes were inspected for these limits without treating them as exact group membership.

Ten manually inspected rows:

- `lived-t0981664644` — `/home/user/.emacs.d/elpa/company-20261120.417`
- `lived-tc9fb19d567` — `/home/user/.emacs.d/elpa/magit-20261117.1103`
- `lived-t9b2b9a2814` — `/home/user/.oh-my-zsh/plugins/alias-finder`
- `lived-t515b2ce401` — `/home/user/.oh-my-zsh/plugins/chucknorris`
- `lived-tfa879dd69f` — `/home/user/.oh-my-zsh/plugins/copyfile`
- `lived-t7404fddb53` — `/home/user/.oh-my-zsh/plugins/docker`
- `lived-tc7dcfd5d34` — `/home/user/.oh-my-zsh/plugins/dotenv`
- `lived-t52437ba96a` — `/home/user/.oh-my-zsh/plugins/extract`
- `lived-t44ea0088c1` — `/home/user/.vscode/extensions/dbaeumer.vscode-eslint-3.0.34`
- `lived-t4af9917634` — `/home/user/.vscode/extensions/esbenp.prettier-vscode-12.4.0`

## A3-13. Container project examples with unobserved content/use
Rows: 39. Sentences: Q2,Q3a,Q3b,Q4,U1,U4,L1,L2.

Every group is a container example containing a Compose description, sometimes sources/build files, and supporting project material. Contents and actual local launch/access use are unavailable; executable code, active launch settings and unused project material differ. FACT_UNKNOWN. Ten cases were checked across simple YAML/document groups and Python, Go, Rust, TypeScript and monitoring subtrees.

Ten manually inspected rows:

- `lived-t1f59d917a6` — `/home/user/Projects/awesome-compose/angular`
- `lived-t29bfb9ffd0` — `/home/user/Projects/awesome-compose/django`
- `lived-t6ac1b2aa39` — `/home/user/Projects/awesome-compose/elasticsearch-logstash-kibana`
- `628f01597373050cc3080375` — `/home/user/Projects/awesome-compose/flask-redis`
- `cae287e95aa05bd036f2cc17` — `/home/user/Projects/awesome-compose/gitea-postgres`
- `lived-t7dfefe9c09` — `/home/user/Projects/awesome-compose/nginx-golang`
- `38b5dec25d1535b3b1972c0a` — `/home/user/Projects/awesome-compose/pihole-cloudflared-DoH`
- `lived-td7912413ab` — `/home/user/Projects/awesome-compose/prometheus-grafana`
- `lived-t70c3c558e1` — `/home/user/Projects/awesome-compose/react-rust-postgres`
- `98d6d2b79e68b842de14fde3` — `/home/user/Projects/awesome-compose/wordpress-mysql`

## Technical documentation

- Volatile storage: https://uapi-group.org/specifications/specs/linux_file_system_hierarchy/
- Man-db cache generation: https://manpages.debian.org/trixie/man-db/mandb.8.en.html
- Service-helper history: https://manpages.debian.org/testing/init-system-helpers/deb-systemd-helper.1p.en.html
- Flatpak deployment paths: https://docs.flatpak.org/en/latest/flatpak-command-reference.html
- Git templates: https://git-scm.com/docs/git-init
- MIME generation: https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html
- Python bytecode copies: https://docs.python.org/3/tutorial/modules.html#compiled-python-files
- Neovim Lua cache: https://neovim.io/doc/user/lua#vim.loader
- Other individual rows cite their documentation in basis; raw facts use the evidence-referenced files only.
