LIVED-IN: 1 confirmed gaps

A3-H review, 2026-11-23 UTC. This is the beyond-plan investigation identified in [in/READY.md](../in/READY.md), not D1 or any other published check. No machine outcome or combined hypothesis outcome is assigned. Appendix A.4.1 combines cases of a check; it does not turn this folder into one.

## Inventory and comparison

Counts refer to rows, including directory groups, not unique files. Level-two groups list immediate members; a gap affecting one member does not make every member a gap.

| Machine | Objects before reduction | Objects compared | Level-two rows compared | Second level obtained | Rows adjudicated |
|---|---:|---:|---:|---|---:|
| developer | 11,852 | 6,409 | 5,554 | Yes; filesystem traversal complete, package ownership incomplete | 5,381 |
| gaming | 24,243 | 16,515 | 15,926 | Yes; filesystem traversal complete, package ownership incomplete | 15,714 |
| server | 3,287 | 1,325 | 451 | Yes; filesystem traversal and package ownership complete | 156 |
| Total | 39,382 | 24,249 | 21,931 | Three inventories obtained | 21,251 |

Evidence: [in/READY.md](../in/READY.md), each `in/raw/MACHINE/metadata.json`, `level-2.tsv` and `objects.tsv`, and [compare/joined.tsv](../compare/joined.tsv). All three metadata files still say `ready_for_observation=false`; obtaining the second level is not a claim that all classification facts are known. The gaming anonymous-download action failed; it was not repeated or replaced.

As reported in [compare/STATS.md](../compare/STATS.md): **3,007 / 24,249 matching decisions (12.40%); Cohen’s kappa 0.11479**. Both classifications supplied valid decisions for all objects. There are 2,998 agreed rows outside adjudication: nine matching MIXED rows were nevertheless adjudicated.

The following are the input adjudication counts, not newly certified classifications of every row. The review challenges all seven gap cards and the specified samples; it does not silently rewrite `rows.tsv`.

| Input verdict | Rows |
|---|---:|
| GAP | 16,598 |
| UNKNOWN | 2,153 |
| RESOLVED:RECORD | 806 |
| RESOLVED:INSTALLED-PACKAGE | 548 |
| RESOLVED:PROGRAM-OWN | 412 |
| RESOLVED:MATERIAL | 272 |
| RESOLVED:MIXED | 197 |
| RESOLVED:INSTALLED-DERIVED | 96 |
| RESOLVED:SETTING-DEFAULT | 53 |
| RESOLVED:RUNTIME | 42 |
| RESOLVED:ACTION | 36 |
| RESOLVED:SETTING-OWN | 21 |
| RESOLVED:PROGRAM-DERIVED | 10 |
| RESOLVED:INSTALLED-OWN | 7 |
| Total | 21,251 |

### Unknown facts

[review/unknown-inventory.tsv](../review/unknown-inventory.tsv) identifies every original UNKNOWN row and preserves its missing-fact explanation and evidence. It includes 2,153 adjudicated UNKNOWN rows and 61 agreed UNKNOWN rows: 2,214 distinct input UNKNOWN rows. An unknown fact is not counted as a textual gap.

| Kind | Adjudicated UNKNOWN | Agreed UNKNOWN | Missing facts |
|---|---:|---:|---|
| 2:stored-ownership-unresolved | 1,964 | 6 | Received-state integrity; SteamCMD/Lutris whole-installation membership; member creator, contents, link targets or interpreter; alternative auto/manual mode; installation default versus later choice |
| 2:code-ownership-unresolved | 172 | 9 | Installer/package membership and whether code remains as received; provenance or executable interpretation where unresolved |
| 2:stored-outside-packages | 14 | 1 | Member origin, installation default versus builder choice, alternative mode, configuration contents or integrity |
| 2:executable-code-outside-packages | 0 | 41 | Maintainer-script received-state integrity absent from the supported package-file comparison |
| 2:image-container-store | 1 | 4 | Unexpanded store members, deployment membership and received-state integrity |
| 1:sudo-access | 2 | 0 | Which actual rights the report heading denotes: defaults or a person’s rule |

The 18 sampled resolutions with missing facts are additional to that input total; their ids and precise missing facts are in [review/sample-resolved.tsv](../review/sample-resolved.tsv). They are not counted as confirmed gaps. Rejected gap cards also contain factual limits; rejecting the alleged textual gap does not establish missing integrity or provenance for their thousands of rows.

## Confirmed gap: Fetched repository history fits both branches of question four

Git objects and references fetched for a requested checkout are both repository history recorded by Git while it runs and project material brought at a person’s request. Question four assigns these descriptions to different classes without choosing between them.

S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»

S8.2-6 «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»

S8.2-2 «The rest need not be recorded.»

**Two decisions:** RECORD or MATERIAL. Neither requires a declaration line, so the declarations can be identical; the unresolved result is the object’s class. Section 9.2 asks both what an object is and whether it must be recorded. The ambiguity is therefore retained without inventing a difference in required declaration contents.

**Attempted refutations:** Q1 does not establish these Git metadata groups as installed packages; executable hook files are instead removed from this gap by Q2. Q3 supplies no computer-wide chosen setting for the repository objects/references. The four-question order reaches Q4 but does not order the two conditions inside Q4. Calling this only a storage-design question would avoid the classification being asked: Section 8.5 leaves handling outside, not the meaning of the two classes. quote: «How to store, transfer and remove program records and material.»

**Examples and evidence:**

| Id | Name |
|---|---|
| developer-216b547047e9bd323ef8a31b | `/home/linuxbrew/.linuxbrew/Homebrew/.git/objects/3d` |
| developer-6bf67733481480cdeaa37d0c | `/home/linuxbrew/.linuxbrew/Homebrew/.git/refs/tags` |
| developer-05617e28292b94b182cc73aa | `/home/linuxbrew/.linuxbrew/Homebrew/.git/objects/45` |
| developer-53425eb85c9fbc80fd72ef81 | `/home/user/Projects/scc/.git/objects` |

For each id, `in/raw/developer/members/ID-WITHOUT-MACHINE.tsv` supplies the complete member list; (not published: direct evidence at least 2 MB) supplies the group identity. Checkout provenance is corroborated by `in/operator/developer/actions-logs/actions-logs/developer_second_package_manager.log` and `developer_public_project.log`. No content of a compressed repository object is assumed executable merely because it may encode source code.

**Exact row extent:** developer **67**, gaming **0**, server **0**. [review/gap-scope.tsv](../review/gap-scope.tsv), rows `card=C2, review_status=CONFIRMED`, lists every id and name. The reproducible search in [review/build_scope.py](../review/build_scope.py) traverses the entire joined table by kind and name, including agreements and resolved rows, rather than selecting the old hole column. The included stored groups are the two `.git` roots and their `objects`/`refs` subtrees, excluding commit-graph metadata; generated operational logs/cache/info outside those subtrees are also excluded. Of the original card’s 84 rows, 14 executable Homebrew sample hooks and their immediate hook group are excluded: Q2 decides the executable members before Q4. Two more rows, `developer-4fbf65b1725f19d2f17c9c20` (`.git/objects/info`, an original example) and `developer-419b511cc8523c257792bd83` (`.git/objects/info/commit-graphs`), contain commit-graph metadata whose fetched-versus-locally-generated provenance is not established; they are FACT_UNKNOWN for this claimed overlap, not confirmed instances. Their complete raw member tables support this correction. The full search found no additional confirmed rows beyond those 67.

**Missing sentence or collision:** a precedence sentence is missing between the two simultaneously applicable conditions of S8.2-15. This is a collision of two branches within one sentence, not two separately numbered sentences. No choice between the readings is made here.

## Cards that did not survive

| Original card | Review verdict | Reason |
|---|---|---|
| 1. Self-managing clients | REFUTED | S8.1-4/6 contain no exclusion for self-installation; self-uninstall/reset establishes the relevant installation/removal functionality; Q1 precedes cache/code classification, with unresolved membership/integrity kept factual. |
| 3. Container images and containers | REFUTED | An execution engine is not made an installer by calling its data an image; the documented operations in the card do not establish Q1, executable image contents reach Q2, and running processes follow S8.2-5/22; unexpanded stores remain factually unknown. |
| 4. Package contents in installer caches | FACT-WRONG | The premise that cached packages are installed there and removable only with the whole cache fails: uv supports per-package cache removal, while Bun/Go document downloaded cache data separately from installation; executable content reaches Q2 before Q4. |
| 5. Copied or generated code | REFUTED | Q2 decides PROGRAM and S8.2-16 expressly permits an own line; it does not demand a unique line form or make every possible derived line mandatory. |
| 6. Program-generated values | REFUTED | Apply Q3’s person-chosen condition before Q4; S8.2-13 is the list within Q3, not a waiver of that condition; S8.2-14 separately decides the personal program’s access cookie. Unproved origin remains FACT_UNKNOWN. |
| 7. Value files containing executed commands | REFUTED | Q2 and S8.2-23 cover code executed through another program even when the file contains settings; neither says that every entry must be code. |

Totals: **1 CONFIRMED, 5 REFUTED, 1 FACT-WRONG, 0 OUTSIDE**. Detailed application to every example follows. Refuting a proposed dichotomy does not certify every member of a mixed directory.

### Deciding sentences and application to the rejected examples

S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»

S8.1-5 «A general-purpose program with a built-in installer counts as an installer in that part of its functionality.»

S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»

S8.1-7 «Built-in tool—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.»

S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»

S8.2-8 «Then it is an installed object, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.»

S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»

S8.2-10 «Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.»

S8.2-16 «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»

S8.2-5 «What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.»

S8.2-22 «A program that runs as its own process on the computer, including in a container, is a program.»

S8.2-11 «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»

S8.2-12 «Then it is a setting, however it was entered and whatever file stores it.»

S8.2-13 «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»

S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

S8.2-17 «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»

S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»

**Card 1.** The saved Julia installation log expressly describes installation of Juliaup and documents `juliaup self uninstall`: [developer_julia.log](../in/operator/developer/actions-logs/actions-logs/developer_julia.log). The Steam source (not published: downloaded distribution package metadata or sources), `reset_steam` lines 533–610, removes client payload and reinstalls its bootstrap while saving game/user/download data. S8.1-6 does not require a removal command to leave the application absent indefinitely, and S8.1-5 does not exclude functionality operating on the installer itself. That defeats the card’s claimed missing self-installation rule.

| Example id | Application |
|---|---|
| gaming-cfd36e0732b4def2d5ecaf69 | Client SVG payload: Q1 INSTALLED-PACKAGE when received state is established; missing integrity is FACT_UNKNOWN, not a rule excluding self-installed resources. |
| gaming-820d8fed19aa17b72181a2d7 | Runtime locale payload: same Q1 test; non-executability does not override Q1. |
| gaming-495169019fec2fb328ec9636 | `bin/hardwareupdater` group: client payload reaches Q1 when unchanged; executable non-package members reach Q2, and membership/integrity must be checked per member. |
| gaming-1fd35bf6b4019193bad37621 | `steam-runtime.old`: retention by an updater is not itself proof of current package membership or received state; those are facts to establish, not an undefined self-installer category. |
| gaming-4cf3d1cb3da5181824cbdf16 | Steam root is mixed: payload and preserved `userdata`, `package`, `steamapps` do not acquire one class just because reset visits the same tree; use Q1/Q2/Q4 per member. |
| gaming-5e400a5875aa136f688db7de | UI sounds are payload data, so Q1 applies when their received state is known, independently of whether they are executable. |
| developer-cbe2f19f976b603f5bb42193 | Juliaup binary belongs to the documented self-install/uninstall unit; received-state uncertainty remains factual; code outside Q1 reaches Q2. |

**Card 3.** The three server image ids `server-fc8e0ac75ce9ed64a08ff655` (caddy), `server-46f5ba6815bb94894157236c` (postgres) and `server-bce2d2fe9dfb24c822a93809` (whoami), and `developer-78e8326714450972e0134fb6` (development image), identify executable image contents available through Docker. With no documented installer function establishing Q1 in the card’s facts, Q2 makes executable contents programs, and S8.2-16 permits own lines. Ancillary files inside an unexpanded image are not all thereby code. `developer-59a4ddfe60a8a1b18f6627c9` is a running container: its process is not a separate stored object under S8.2-5; the program running in it is expressly covered by S8.2-22. `developer-ffcb51cbd136cf2f6e7408cf` (`/var/lib/containerd`) and `developer-fd23729ab637faddccc1bc3e` (`/var/lib/docker`) are unexpanded stores, so their member classes are FACT_UNKNOWN. Evidence: their full joined rows and raw Docker queries named there. An engine’s undocumented installation status would require factual documentation, not a new sentence defining every product.

**Card 4.** The [Go reference](https://go.dev/ref/mod#go-mod-download) describes downloading modules to pre-fill the cache; [Bun’s cache documentation](https://bun.sh/docs/pm/global-cache) distinguishes downloading to the cache from installing into `node_modules`. The [uv documentation](https://docs.astral.sh/uv/concepts/cache/) explicitly documents `uv cache clean ruff`, refuting the whole-cache-only premise. These are factual distinctions in the tools, not a change to the hypothesis.

For `developer-28b0928f32a3bd540164f5c2` (`circl/.../ot/simot`), `developer-4bc7e8a9213ac909292c2e0a` (`go-billy/v5@v5.9.0`), and `developer-9e6d06f152c07e5c13f841e0` (`go-git/go-git`), downloading/extracting source into the module cache does not establish an installed package. Executable members are decided by Q2, otherwise generated cache data by Q4; ability to execute cannot be inferred from the directory name alone. `developer-880c223d69d1d6670ff0f5f3` (`hookified`) actually lists two cache-index symlinks in its raw member table, not two package payload files. `developer-b8d0d1ff228a2993234f695a` (`yocto-queue@0.1.0@@@1`) contains a downloaded package tree: executing its JavaScript is Q2; non-code cached files are Q4. uv’s extracted cache and the RubyGems archive likewise require facts about installed versus cached membership, not the false condition that packages must be removed individually by a dedicated uninstall operation. Where those facts or executable contents are missing, the result is FACT_UNKNOWN.

**Card 5.** The own-line alternative in S8.2-16 is sufficient for the Wine `rundll.exe` (`gaming-85b507e7ce1d3c2a16693bb3`), executable members of `system32/wbem` (`gaming-542ab2b7a1cac1d1e2d23e7f`) and `syswow64` (`gaming-fe91919b6bab6568dfdea112`), Git’s executable hook (`developer-3bcbeded8b7cf5aedc1382fb`), Ruby wrapper (`developer-bc1494f6f41c4c0f3175eb8c`), shell-completion code (`developer-35549cad55c96268fcaf4f24`), and extracted k3s tools (`server-be5afc83ca654a448cd1fb60`). Q2 decides the executable members as PROGRAM; S8.2-1 requires recording. Records in mixed groups remain records. Whether a particular real generating line also covers them is tested against that line, not answered by requiring a unique classification label. The note that RubyGems is not a built-in tool is additionally contradicted by S8.1-4/7: a language installer is explicitly included.

**Card 6.** The two developer firewall groups contain `docker-forwarding.xml` and `docker.xml`, respectively. Docker documents generating these exact policy/zone names; the persisted files and their active chains are observed in (not published: over 20 MB) (lines 31800 and 31805) and `raw/0288-firewall-nft.out`. The saved [developer_container.stderr](../in/operator/developer/actions-logs/actions-logs/developer_container.stderr), lines 34–35, records the package transaction completing before service enablement and the subsequent startup. Thus their automatic origin is supported by the documented operation and observed results, not solely a timestamp. Under Q3 as actually asked, these concrete policy values were not person-chosen; Q4 therefore decides RECORD. S8.2-13’s list within Q3 does not supply a competing affirmative answer after Q3’s explicit condition fails. [Docker’s firewalld integration documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/#integration-with-firewalld).

The resource drop-ins in `developer-342e1a9fd229e3473b8c35b3` have unknown provenance in (not published: direct evidence at least 2 MB); their names do not prove that no person chose their values. For the k3s examples `server-c6809ad0393bc02f2943127a` (credentials), `server-ddd20eb86c2fac35aad9742a` (node password), `server-0a575e792deb53a2ae502487` (metrics manifests), and `server-7bf44e4e4a03c100b6ad395a` (agent), apply the same order: a person-chosen system value is SETTING, a package/installation default uses Q1 or S8.2-17 as applicable, and a purely program-generated value that fails Q3 reaches Q4. Actual per-member origin, access destination and installation timing must be known before choosing; unresolved members remain FACT_UNKNOWN. The datastore `server-034bd74a045c24aa6dd19160` lists database/WAL/shared-memory files without their effective field contents, so it cannot certify a whole group of chosen settings. `gaming-1ba8cee6c38131f0b6c75952` contains the personal sound-server authentication cookie; S8.2-14 expressly makes a value granting access a SETTING. None of these establishes two conflicting required decisions with the facts fixed.

The full-table C6 search in [review/gap-scope.tsv](../review/gap-scope.tsv) includes all firewall kinds and related persistent paths, not just the 27 old rows. It records runtime exclusions, the two refuted firewall examples, member/provenance unknowns, and the cookie exception. The `static/charts` group contains three `.tgz` archives, not the active generated value files claimed in the card.

**Card 7.** `server-c354536d6d9a738329571706` contains `/etc/cron.d/cal-maintenance`: its command field is code executed through a shell, so Q2/S8.2-23 decide the code-bearing file before Q3. `developer-e56b4f802a20335d455ecb3a` contains `lefthook.yml`: the `run:` command is likewise executed through another program; ordinary project members keep their own classes. `developer-d916e8927ebf41371ab8dd1d` contains a Dockerfile and `index.html`: the build instructions/commands are executed code under Q2, while the separate HTML document remains material on the stated facts. Their complete member lists are `in/raw/MACHINE/members/ID-WITHOUT-MACHINE.tsv`. The fact that a launcher parses a file before executing its commands does not add an entire-file-execution requirement to S8.2-23.

## Seeded sample audits

| Sample | Seed | Eligible population | Drawn | Supported affirmative decisions | Existing UNKNOWN upheld | Newly FACT_UNKNOWN | New confirmed gaps |
|---|---:|---:|---:|---:|---:|---:|---:|
| RESOLVED rows | 2026112302 | 2,500 | 40 | 22 | 0 | 18 | 0 |
| Agreed, not adjudicated | 2026112303 | 2,998 | 60 | 58 | 2 | 0 | 0 |

For each sample, sort eligible full ids lexicographically, then use `random.Random(seed).sample(eligible, count)`. The draw order, every id, exact quoted sentences, evidence and individual result are recorded in [review/sample-resolved.tsv](../review/sample-resolved.tsv) and [review/sample-agreed.tsv](../review/sample-agreed.tsv); summaries are [review/sample-resolved.md](../review/sample-resolved.md) and [review/sample-agreed.md](../review/sample-agreed.md). These are 100 distinct sampled rows.

Every failed resolution was tested as a gap candidate. Nine need a received-content comparison; six Go build-cache groups need payload/executability facts; one shader-cache group needs contents/capability facts; one persistent PrivateTmp entry needs its runtime-only lifetime established; one plugin directory needs creation provenance. These 18 fail as fully resolved rows because facts are missing, not because the text supplies incompatible decisions. No candidate from either sample adds a confirmed gap. The samples do not certify the unsampled rows.

The final independent review is recorded in [review/verification.md](../review/verification.md); its two-row scope correction has been applied. The text is unchanged. No weighting or proposal to amend it is made.
