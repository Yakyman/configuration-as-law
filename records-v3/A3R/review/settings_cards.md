# Review of cards 2, 3 and 4

Review used TEXT.md Sections 2–5, SENTENCES.md, A3R/adjudication/HOLES.md, A3R/adjudication/rows.tsv, the whole (not published: direct evidence over 2 MB) table, and the available inventory. The following judgments challenge the stated gaps; they do not claim that every unseen member of a subtree has been inspected. Unknown factual contents remain unknown under S3-2.

## Exact sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-6: “records of the past—logs, history;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”
- S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Card 2 — Compiler and build input — REFUTED

S2.2-13 never says that its two clauses exhaust every kind of file. A compiler input need not be an executed program to fall under S2.2-2: on the facts asserted by this card, removing it prevents the specified build or type-checking operation, so the content exemption's condition that the computer can do the same is not met. No explicit exemption for all source documents is present. A source-language declaration parsed to establish an API is not simply a program preference read as values; describing it as such would add a classification the text does not supply.

Each example, on the stated facts:

| ID | Name | Decision and literal reason |
|---|---|---|
| 7ab53c3d01fc5b25f6f43afb | /home/user/Projects/express/node_modules/hasha/node_modules/type-fest | MUST, S2.2-2: supplies static declarations used for type checking; without the declarations that checking is unavailable. The saved package manifest additionally contains the command `xo && tsd` (S2.2-10). |
| lived-t9bcd444add | /home/user/.vscode/extensions/ms-python.vscode-pylance-2026.4.1 | MUST for the named .pyi inputs, S2.2-2: util.pyi and build_spatial_filters.pyi supply API declarations needed for those checks. The row is the two inventoried stubs, not automatically all extension code. |
| lived-t4a8c2cf574 | /home/user/Projects/awesome-compose/sparkjava-mysql | MUST for App.java, S2.2-2: the stated application build requires it; Dockerfile is a separate build instruction input. |
| lived-t3a5e8c36ee | /home/user/Projects/awesome-compose/nginx-golang-postgres | MUST for backend/main.go, S2.2-2: compiling that service requires the source. This does not decide the separate nginx values as compiler input. |
| lived-tf9e8ae870c | /home/user/Projects/awesome-compose/aspnet-mssql | MUST for C#/Razor build inputs, S2.2-2: the specified application cannot be built from absent inputs. Browser assets and appsettings values remain separate members. |
| lived-tb1657f171f | /home/user/Projects/awesome-compose/spring-postgres | MUST for the Java build inputs, S2.2-2. A template used only as replaceable output content can instead meet S2.2-4; naming a template is insufficient to establish a contrary build requirement. |
| lived-t88b40d452e | /home/user/.local/share/nvim | MUST for the native matcher source required for its on-demand build, S2.2-2. Lisp/Lua code, history and caches elsewhere in the subtree are not settled by this card. |

Evidence: each ID's name, evidence and c1_what fields in joined.tsv; the original card's explicit compilation/type-checking descriptions; saved type-fest manifest in A3R/in/raw/lived/raw/168-npm-package-records.out. No claim is made that removal of these inputs necessarily prevents an already-built executable from running: losing the stated build operation is the relevant consequence.

## Card 3 — In force only inside one program — REFUTED

The card's first proposed reading substitutes 'applied by one program' for the actual 'in force only inside one program'. A single reader is not enough to establish the exemption. On the card's own factual descriptions, the settings below govern external accounts, network operations, device output, independent processes or firmware; S2.2-1 and S2.2-2 therefore apply. An internal implementation location does not make those external rules internal program preferences.

| ID | Name | Decision and literal reason |
|---|---|---|
| 5f8fcf77e7c5041de9f3e517 | ssh-access:usepam | MUST, S2.2-1: governs PAM account and session checks for external login sessions. |
| 83bfbe2fd66f60bcc74b2389 | ssh-access:allowtcpforwarding | MUST, S2.2-1: governs availability of network tunnels beyond the daemon. |
| 73b70232c07e15bee2c93628 | ssh-access:maxauthtries | MUST, S2.2-1: the applied limit decides permitted attempts to authenticate for account access; its being implemented inside sshd does not establish confinement of its force. |
| ab310cbf841cfc3d22cb157b | /etc/ssh | MUST for host identity keys and external login rules, S2.2-2: host authentication to network peers depends on the keys. S2.2-15's account-login keys do not need to be stretched to include host keys. |
| lived-t5593bedbb3 | /home/user/Projects/awesome-compose/apache-php | MUST for the deployment recipe, S2.2-1: it governs launching separate containers. The PHP program is independently covered by S2.2-10; README content is exempt. |
| 041bcd50f0176118f1200688 | /home/user/.config/pulse | MUST for the specified routing/default-device and volume rules, S2.2-1: their force governs sound from other programs. Cookie identity and individual database records require their own facts, not classification from a suffix. |
| a236c198c6522e6154ee71e9 | /etc/cups | MUST for active printer queues and service-access rules, S2.2-1: they control other programs' printing; historical .O backups can meet S2.2-6. |
| f291cc06cd1e8855bc44b998 | /boot/efi/EFI/debian | MUST for BOOTX64.CSV used to create firmware boot entries, S2.2-1 and S2.2-16: the described force is on device boot order. This does not mistake a CSV for executable code. |
| lived-t51cc65dbda | /home/user/.config/xfce4/xfconf | MUST for shared display/input/launch rules, S2.2-1: they govern other programs' windows, input and processes. Appearance values genuinely confined to one program can meet S2.2-7. |

Evidence: A3R/in/raw/lived/raw/085-ssh-access.out records usepam yes (line 5), maxauthtries 6 (line 9), and allowtcpforwarding yes (line 45); filesystem members and functional descriptions are in the corresponding joined.tsv rows. The card does not establish conflicting requirements by treating every external effect as an internal setting merely because one program reads its representation.

## Card 4 — Command strings in value files — REFUTED

S2.2-10 says 'code that another program executes', not 'a whole file directly executed without passing a string'. A shell command is code even when retrieved from a JSON/XML setting; after dispatch it runs with the shell's rights. S2.2-13's classification of the enclosing values file does not make externally executed command strings settings in force only inside the reader.

| ID | Name | Decision and literal reason |
|---|---|---|
| 5f0c9a232213a85ce17b1a62 | npm-bundled/package.json | MUST for shell scripts, S2.2-10; saved scripts include `tap`, `npm run eslint`, and `template-oss-check`. |
| f2384a93340393c000d0f294 | debug/package.json | MUST for shell scripts, S2.2-10; saved scripts include `xo`, `mocha test.js test.node.js`, and `karma start --single-run`. |
| ab373871de57456ba9bdc8d5 | /usr/share/code/resources/app/extensions/git/package.json | The stated scripts are MUST by S2.2-10; a main entry selecting runtime code also affects execution under S2.2-2. The local manifest contents are not in the inspected tar, so this refutes the alleged textual gap on the card's stated facts, not independently verifies those facts. |
| 87ad719c2a0813ce175c2a89 | /usr/share/code/resources/app/extensions/prompt-basics/package.json | The stated scripts are MUST by S2.2-10. Same factual limit: local manifest not in inspected tar; a manifest without executable fields must not be inferred to have them merely from its name. |
| c04501ebe561207b22284ddb | spdx-exceptions | MUST for saved manifest scripts `node build.js` and `node latest.js`, S2.2-10; reference-table contents can remain exempt under S2.2-4. |
| 54c86841fb0c34fd62a14f37 | /home/user/.config/Thunar | The stated custom action command strings are MUST under S2.2-10. Inventory proves uca.xml exists but does not show actual command values; an empty/customization-only file would be a different factual case, not this contradiction. |
| 56e2e00352bb36231b2da3cd | /home/user/.config/xfce4 | The stated launcher Exec command strings are MUST, S2.2-10; appearance/layout settings remain separate. |
| e39ae1be47374abe25b3a90a | /home/user/.ssh | The stated ProxyCommand command string is MUST, S2.2-10; independent external process launch also defeats S2.2-7's confinement condition. Account login keys are independently MUST under S2.2-15. |

Evidence for saved npm fields: A3R/in/raw/lived/raw/168-npm-package-records.out is a tar archive, inspected in memory without extracting into the filesystem. Member names match the full joined.tsv object paths with their leading slash removed (append /package.json for package rows). Other evidence: corresponding joined.tsv rows and HOLES.md examples. Unknown contents are not promoted to confirmed holes.

## Eight sampled resolved manifests

The following indices refer to A3R/review/resolved_sample.json. All eight saved manifests have executable script fields. Removing each manifest removes the named npm dispatch operations, satisfying S2.2-2; S2.2-10 separately applies to the command strings. No claim that every removal breaks runtime importing is warranted: main=index.js is often the default.

| Sample | ID | Saved main | Saved script examples |
|---|---|---|---|
| 1 | fb103b616b7ea81a780d2695 | forEachAsync.js | test: echo "Error: no test specified" && exit 1 |
| 3 | 172cc141e4e590d5e9ea3093 | source | test: xo && nyc ava && tsd; bench: matcha benchmark.js |
| 18 | 8ea8d529c229fa18decf6c89 | index.js | build: node node_modules/buildman/index.js --all; test: node tests/index.js |
| 20 | 24fc970588cb5dab7cb83110 | index.js | test: mocha; test:watch: npm run test -- --watch |
| 28 | 8b4415310959c3acab63dc3b | absent | lint: eslint . && node ./scripts/lint-readme-list.js; test: mocha --reporter spec |
| 30 | 4978680914d1ad0f72efac47 | absent | test: xo && nyc ava && tsd |
| 32 | e2ea7572a1773314cc50e662 | index.js | test: make test |
| 34 | 5a2f7dc954a27ba7a4466c9d | index.js | pretest: xo; test: tap; release: standard-version |

Source: matching package.json members of A3R/in/raw/lived/raw/168-npm-package-records.out. None of these eight becomes a confirmed hole.

## Extent and limits

Confirmed memberships for cards 2–4: zero. settings_extent.tsv therefore contains only its header. The review searched the entire joined table by kind/name for source declarations, compiled source suffixes, source/include paths, editor stubs, compose subtrees, package manifests, SSH, sound, printing, desktop settings, and build inputs; agreement was not an exclusion criterion. Since each alleged generic gap is refuted, no affected-row count from the original cards is retained as a confirmed extent.

Not OUTSIDE: these cards ask whether an object is covered by the definition, not how to preserve program state, protect secrets, or design the declaration. S2.5 does not replace the coverage decision. The factual limitations above should remain visible rather than be treated as proof of either MUST or NOT for unseen contents.

The reproducible whole-table name/kind search index is settings_search.tsv: compiler/source search 98 rows; external-setting search 291 rows; command-value/container search 1,000 rows. These are search candidates, not confirmed memberships; the searches overlap and include false positives such as executable programs whose names contain ssh. The table preserves agreed decisions as well as disputed ones.
