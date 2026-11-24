LIVED-IN: 3 confirmed gaps

A3-H review, corrected by FX-A3-H-1 on 2026-11-23 UTC. Findings and dispositions: [FIX-A3-H-1.md](../FIX-A3-H-1.md). This is the beyond-plan investigation identified in [in/READY.md](../in/READY.md), not D1 or any other published check. No machine outcome or combined hypothesis outcome is assigned. Appendix A.4.1 combines cases of a check; it does not turn this folder into one.

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

**Evidence correction:** 467 of these input RESOLVED rows rely on the rejected `ctime` rule: 459 INSTALLED-PACKAGE (of 548), six PROGRAM-DERIVED and two MIXED. They are **FACT_UNKNOWN pending a received-content comparison** for the relevant members; the historical verdict table is not a certification. [fix-a3-h-1/ctime-unknown.tsv](../fix-a3-h-1/ctime-unknown.tsv) preserves every id, original note and missing fact. Nine are already among the 18 sampled FACT_UNKNOWN rows, so these sets must not be added without deduplication.

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

The 18 sampled resolutions with missing facts are additional to that input total; the systematic correction above extends the same evidence limit beyond the sample; their ids and precise missing facts are in [review/sample-resolved.tsv](../review/sample-resolved.tsv). They are not counted as confirmed gaps. Rejected gap cards also contain factual limits; rejecting the alleged textual gap does not establish missing integrity or provenance for their thousands of rows.

## Confirmed gap: Fetched repository history fits both branches of question four

Git objects and references fetched for a requested checkout are both repository history recorded by Git while it runs and project material brought at a person’s request. Question four assigns these descriptions to different classes without choosing between them.

S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»

S8.2-6 «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»

S8.2-2 «The rest need not be recorded.»

**Two decisions:** RECORD or MATERIAL. Neither requires a declaration line, so the declarations can be identical; the unresolved result is the object’s class. Section 9.2 asks both what an object is and whether it must be recorded. The ambiguity is therefore retained without inventing a difference in required declaration contents.

**Attempted refutations:** The person’s `scc` checkout is supported by the saved public-project action log; it is not an installation by a documented installer. Homebrew metadata is held out pending Q1 facts, as explained below; executable hook files are instead removed from this gap by Q2. Q3 supplies no computer-wide chosen setting for the repository objects/references. The four-question order reaches Q4 but does not order the two conditions inside Q4. Calling this only a storage-design question would avoid the classification being asked: Section 8.5 leaves handling outside, not the meaning of the two classes. quote: «How to store, transfer and remove program records and material.»

**Examples and evidence:**

| Id | Name |
|---|---|
| developer-53425eb85c9fbc80fd72ef81 | `/home/user/Projects/scc/.git/objects` |
| developer-6939a0c70bd7e159e638d411 | `/home/user/Projects/scc/.git/objects/pack` |
| developer-b33a49ff4891eb30d52c7e46 | `/home/user/Projects/scc/.git/refs` |

For each id, `in/raw/developer/members/ID-WITHOUT-MACHINE.tsv` supplies the member list. Checkout provenance is recorded in [developer_public_project.log](../in/operator/developer/actions-logs/actions-logs/developer_public_project.log). Compressed repository objects are not assumed executable merely because they may encode source code.

**Exact confirmed row extent:** developer **7**, gaming **0**, server **0**. [fix-a3-h-1/gap-scope.tsv](../fix-a3-h-1/gap-scope.tsv), `card=C2`, is the revised full-table search: 7 CONFIRMED, 62 FACT_UNKNOWN, 177 EXCLUDED (including `.github` substring matches). The seven are the `scc` `.git` group and its `objects`/`refs` subtrees. This counts inventory groups, not unique files. Executable hooks reach Q2; operational logs/cache/info are excluded from this fetched-history claim.

The former 60 confirmed Homebrew rows are now FACT_UNKNOWN for Q1. [Homebrew’s FAQ](https://docs.brew.sh/FAQ#how-do-i-uninstall-homebrew) states: “To uninstall Homebrew, run the uninstall script from the Homebrew/install repository.” Its manual documents fetching Homebrew itself with Git, and the linked uninstall source targets its repository. Exact excerpts and source locations are in [raw/documentation.md](../fix-a3-h-1/raw/documentation.md). Self-installation is therefore not excluded, consistently with card 1. These documents do not prove which inventoried metadata members remain as received from that installation/update; the frozen inventory supplies no received-content comparison. The earlier two commit-graph groups (`developer-4fbf65b1725f19d2f17c9c20`, `developer-419b511cc8523c257792bd83`) remain FACT_UNKNOWN for fetched-versus-generated provenance. All 62 are withheld from the confirmed extent, not silently classified as RECORD or MATERIAL.

**Missing sentence or collision:** the two branches of S8.2-15 collide within one sentence; neither branch orders itself before the other. No choice between the readings is made here.

## Confirmed gap: Program-generated values versus the person-chosen condition

A program-generated access rule is not a value chosen by a person under S8.2-11, but access rules are called settings by S8.2-13. Treating that list, or the access-granting clause S8.2-14, as dependent on the person-chosen condition is a choice between readings that the fixed text does not settle.

S8.2-11 «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»

S8.2-13 «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»

S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

**Two decisions:** SETTING, requiring a line under S8.2-17, or RECORD under S8.2-15, requiring none. The declarations differ in whether the generated access rule must be recorded. The question order does not resolve the scope of conditions within Q3. Section 8.5 concerns handling and implementation, not this classification. **Collision:** S8.2-11’s condition versus the categorical descriptions in S8.2-13/14; no reading is selected.

**Established examples:** `developer-70be1c323890746c1a78c6f5` (`/etc/firewalld/policies`, member `docker-forwarding.xml`) and `developer-24c8232c52212725d6ea3882` (`/etc/firewalld/zones`, member `docker.xml`). [Docker’s documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/#integration-with-firewalld) says “Docker creates a firewalld zone called docker, with target ACCEPT.” and “Docker also creates a forwarding policy called docker-forwarding”. The complete member tables, (not published: over 20 MB) lines 31800/31805, and `in/operator/developer/actions-logs/actions-logs/developer_container.stderr` lines 34–35 support their presence after package completion and service startup. This is the documented generation inference used in the original review, not an integrity claim derived from `ctime`. The zone group also contains other files; only its Docker-generated member establishes this gap.

**Exact confirmed row extent:** developer **2**, gaming **0**, server **0**, in the new `card=C6` scope ledger. The full joined-table search covers firewall kinds and the associated persistent paths, including agreements and resolutions. Runtime firewall objects are excluded under S8.2-5; extracted executable tools reach Q2.

The original card’s 27 rows are **2 CONFIRMED, 23 FACT_UNKNOWN, 2 EXCLUDED**, not 27 established instances. The three developer resource-drop-in groups have unknown origin in (not published: direct evidence at least 2 MB). The gaming cookie (`gaming-1ba8cee6c38131f0b6c75952`, `/home/user/.config/pulse`) likewise has unknown origin in (not published: direct evidence at least 2 MB); its member list proves a cookie file exists, not that it was generated rather than chosen or installed. Nineteen server groups lack the necessary per-member chosen/generated/default provenance or effective contents. This includes the original credentials, node-password, metrics-manifest and agent examples; the database example lists DB/WAL/shared-memory files without their fields. These facts remain open despite the textual gap being confirmed elsewhere. The two excluded original rows are the parent `/etc/systemd/system.control` group (immediate members are directories) and `server-bc0a3760b015fab92372e8e3` (`static/charts`, three `.tgz` archives). Their member tables do not establish the claimed active value files.

## Confirmed gap: Value files whose entries include executed commands

A scheduler or launcher reads a file of values and passes some command entries for execution. S8.2-23 distinguishes a file executed as code from one only read as values, without deciding the whole file when only some entries are executed.

S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»

S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»

**Two decisions:** PROGRAM-OWN under Q2, or SETTING-OWN for values launching a program under Q3/S8.2-14. Both require recording; a class difference does not necessarily require different declaration bytes. The kind of object represented by the line differs. This uses the same classification standard as card 2. **Missing scope rule:** the sentences do not decide whether execution of an entry is execution of the file as code. Treating an entry as the entire file would add a rule. Neither Q2’s priority nor Section 8.5 supplies that rule.

| Example id | Group and relevant member |
|---|---|
| server-c354536d6d9a738329571706 | `/etc/cron.d`, `cal-maintenance` with a shell command field |
| developer-e56b4f802a20335d455ecb3a | `/home/user/Projects/scc`, `lefthook.yml` with a `run:` command |
| developer-d916e8927ebf41371ab8dd1d | `/home/user/Projects/development-web`, the created Dockerfile |

Evidence: `in/raw/MACHINE/members/ID-WITHOUT-MACHINE.tsv`, the original card 7 in [adjudication/HOLES.md](../adjudication/HOLES.md), and the relevant full joined rows. The cron member’s mode is 0644 and its inventory executable flag is false; that flag alone does not rule out interpretation. The unresolved issue is the relationship between parsing the file and executing its command field. Ordinary siblings, such as `index.html`, do not acquire the gap’s classification.

**Exact confirmed row extent:** developer **2**, gaming **0**, server **1**. The full-table kind/name and immediate-member search is saved in [fix-a3-h-1/gap-scope.tsv](../fix-a3-h-1/gap-scope.tsv), `card=C7`, and [command-file-members.tsv](../fix-a3-h-1/command-file-members.tsv). It finds 14 candidate groups: these three, ten additional developer groups with command-file names but unestablished contents/capability or prior Q1 facts (FACT_UNKNOWN), and one server group containing the executable `crontab` tool (EXCLUDED). A Dockerfile name alone is not promoted into a confirmed instance.

## Other cards and factual limits

| Original card | Review verdict | Reason |
|---|---|---|
| 1. Self-managing clients | REFUTED | S8.1-4/6 contain no exclusion for self-installation; self-uninstall/reset establishes the relevant installation/removal functionality; Q1 precedes cache/code classification, with unresolved membership/integrity kept factual. |
| 3. Container images and containers | FACT_UNKNOWN | Quoted pull/removal documentation does not settle Q1 installer/package status; absence of evidence no longer counts as a refutation. Process treatment under S8.2-5/22 is retained. |
| 4. Package contents in installer caches | Split disposition | uv: 5 FACT-WRONG for whole-cache-only removal; Go: 986 and Bun: 344 REFUTED on the documented download/installation distinction; RubyGems: 1 FACT_UNKNOWN. See separate grounds below. |
| 5. Copied or generated code | REFUTED | Q2 decides PROGRAM and S8.2-16 expressly permits an own line; it does not demand a unique line form or make every possible derived line mandatory. |

Card totals: **3 CONFIRMED, 2 REFUTED, 1 FACT_UNKNOWN, 1 split disposition, 0 OUTSIDE**. Detailed application to every example follows. Refuting a proposed dichotomy does not certify every member of a mixed directory.

### Deciding sentences and application to the other examples

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

**Card 1.** The [upstream Juliaup documentation](https://github.com/JuliaLang/juliaup#using-juliaup) states: “juliaup self uninstall uninstalls Juliaup.”

The saved Julia installation log expressly describes installation of Juliaup and documents `juliaup self uninstall`: [developer_julia.log](../in/operator/developer/actions-logs/actions-logs/developer_julia.log). The Steam source (not published: downloaded distribution package metadata or sources), `reset_steam` lines 533–610, removes client payload and reinstalls its bootstrap while saving game/user/download data. S8.1-6 does not require a removal command to leave the application absent indefinitely, and S8.1-5 does not exclude functionality operating on the installer itself. That defeats the card’s claimed missing self-installation rule.

| Example id | Application |
|---|---|
| gaming-cfd36e0732b4def2d5ecaf69 | Client SVG payload: Q1 INSTALLED-PACKAGE when received state is established; missing integrity is FACT_UNKNOWN, not a rule excluding self-installed resources. |
| gaming-820d8fed19aa17b72181a2d7 | Runtime locale payload: same Q1 test; non-executability does not override Q1. |
| gaming-495169019fec2fb328ec9636 | `bin/hardwareupdater` group: client payload reaches Q1 when unchanged; executable non-package members reach Q2, and membership/integrity must be checked per member. |
| gaming-1fd35bf6b4019193bad37621 | `steam-runtime.old`: retention by an updater is not itself proof of current package membership or received state; those are facts to establish, not an undefined self-installer category. |
| gaming-4cf3d1cb3da5181824cbdf16 | Steam root is mixed: payload and preserved `userdata`, `package`, `steamapps` do not acquire one class just because reset visits the same tree; use Q1/Q2/Q4 per member. |
| gaming-5e400a5875aa136f688db7de | UI sounds are payload data, so Q1 applies when their received state is known, independently of whether they are executable. |
| developer-cbe2f19f976b603f5bb42193 | Juliaup binary belongs to the documented self-install/uninstall unit; received-state uncertainty remains factual; code outside Q1 reaches Q2. |

**Card 3.** [Docker pull](https://docs.docker.com/reference/cli/docker/image/pull/) is documented as “Download an image from a registry”; [Docker image rm](https://docs.docker.com/reference/cli/docker/image/rm/) says “Removes (and un-tags) one or more images from the host node.”

This establishes image operations, but does not settle the documented installer purpose under S8.1-4. Q1 is **FACT_UNKNOWN**, not false. The three server image examples (`server-fc8e0ac75ce9ed64a08ff655`, `server-46f5ba6815bb94894157236c`, `server-bce2d2fe9dfb24c822a93809`) and the developer image (`developer-78e8326714450972e0134fb6`) are not certified as whole programs by skipping Q1. Executable members would reach Q2 only once the earlier question is settled negatively. The running container `developer-59a4ddfe60a8a1b18f6627c9` still follows S8.2-5/22 for its process; that does not settle the stored image. The unexpanded stores `developer-ffcb51cbd136cf2f6e7408cf` (`/var/lib/containerd`) and `developer-fd23729ab637faddccc1bc3e` (`/var/lib/docker`) retain unknown member classes. Evidence: the seven full joined rows and raw Docker queries named there. This is a factual documentation limit, not an additional confirmed textual gap.

**Card 4.** The grounds are separate; [fix-a3-h-1/cache-card.tsv](../fix-a3-h-1/cache-card.tsv) lists all 1,336 original rows by family.

| Family | Rows | Ground and exact documentation |
|---|---:|---|
| Go | 986 | REFUTED installation premise: [Go reference](https://go.dev/ref/mod#go-mod-download): “The go mod download command downloads the named modules into the module cache.” The observed download does not establish an installed package at that location. |
| Bun | 344 | REFUTED installation premise: [Bun cache documentation](https://bun.sh/docs/pm/global-cache): “Once a package is downloaded into the cache, Bun still needs to copy those files into node_modules.” Download and installation are distinguished. |
| uv | 5 | FACT-WRONG whole-cache-only premise: [uv documentation](https://docs.astral.sh/uv/concepts/cache/): “To clear the cache for a specific package, run uv cache clean <package-name>.” |
| RubyGems | 1 | FACT_UNKNOWN: `developer-95ffe3a0117370c7c58c4a2c`, `/home/user/.local/share/gem/ruby/cache`; a retained archive does not establish installed membership or removal semantics. The uv argument does not decide this row. |

These dispositions address the card’s premises, not a uniform classification of all members. Q1 still requires actual membership/received-state facts, Q2 actual executable capability, and only then does Q4 apply.

For `developer-28b0928f32a3bd540164f5c2` (`circl/.../ot/simot`), `developer-4bc7e8a9213ac909292c2e0a` (`go-billy/v5@v5.9.0`), and `developer-9e6d06f152c07e5c13f841e0` (`go-git/go-git`), downloading/extracting source into the module cache does not establish an installed package. Executable members are decided by Q2, otherwise generated cache data by Q4; ability to execute cannot be inferred from the directory name alone. `developer-880c223d69d1d6670ff0f5f3` (`hookified`) actually lists two cache-index symlinks in its raw member table, not two package payload files. `developer-b8d0d1ff228a2993234f695a` (`yocto-queue@0.1.0@@@1`) contains a downloaded package tree: executing its JavaScript is Q2; non-code cached files are Q4. uv’s extracted cache and the RubyGems archive likewise require facts about installed versus cached membership; the tool-specific grounds above are not interchangeable. Where those facts or executable contents are missing, the result is FACT_UNKNOWN.

**Card 5.** The own-line alternative in S8.2-16 is sufficient for the Wine `rundll.exe` (`gaming-85b507e7ce1d3c2a16693bb3`), executable members of `system32/wbem` (`gaming-542ab2b7a1cac1d1e2d23e7f`) and `syswow64` (`gaming-fe91919b6bab6568dfdea112`), Git’s executable hook (`developer-3bcbeded8b7cf5aedc1382fb`), Ruby wrapper (`developer-bc1494f6f41c4c0f3175eb8c`), shell-completion code (`developer-35549cad55c96268fcaf4f24`), and extracted k3s tools (`server-be5afc83ca654a448cd1fb60`). Q2 decides the executable members as PROGRAM; S8.2-1 requires recording. Records in mixed groups remain records. Whether a particular real generating line also covers them is tested against that line, not answered by requiring a unique classification label. The note that RubyGems is not a built-in tool is additionally contradicted by S8.1-4/7: a language installer is explicitly included.

## Seeded sample audits

| Sample | Seed | Eligible population | Drawn | Supported affirmative decisions | Existing UNKNOWN upheld | Newly FACT_UNKNOWN | New confirmed gaps |
|---|---:|---:|---:|---:|---:|---:|---:|
| RESOLVED rows | 2026112302 | 2,500 | 40 | 22 | 0 | 18 | 0 |
| Agreed, not adjudicated | 2026112303 | 2,998 | 60 | 58 | 2 | 0 | 0 |

For each sample, sort eligible full ids lexicographically, then use `random.Random(seed).sample(eligible, count)`. The draw order, every id, exact quoted sentences, evidence and individual result are recorded in [review/sample-resolved.tsv](../review/sample-resolved.tsv) and [review/sample-agreed.tsv](../review/sample-agreed.tsv); summaries are [review/sample-resolved.md](../review/sample-resolved.md) and [review/sample-agreed.md](../review/sample-agreed.md). These are 100 distinct sampled rows.

Every failed resolution was tested as a gap candidate. Nine need a received-content comparison; six Go build-cache groups need payload/executability facts; one shader-cache group needs contents/capability facts; one persistent PrivateTmp entry needs its runtime-only lifetime established; one plugin directory needs creation provenance. These 18 fail as fully resolved rows because facts are missing, not because the text supplies incompatible decisions. No candidate from either sample adds a confirmed gap. The samples do not certify the unsampled rows.

The earlier acceptance in [review/verification.md](../review/verification.md) is historical and superseded on the disputed points by [REVIEW.md](../REVIEW.md) and this fix. No independent acceptance of this fix is claimed. Changed scopes and evidence impacts were recomputed in `fix-a3-h-1/`; the unchanged samples were not redrawn or rerun. The published text and failure conditions are unchanged. No weighting, machine outcome, combined outcome or proposal to amend the text is made.
