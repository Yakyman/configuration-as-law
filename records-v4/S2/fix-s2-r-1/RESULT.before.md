STEP 2: 6 of 15 families with outcome 0; 9 with ?; sample outcome ?, 0 of 600 agreements do not follow

Supplement 1, step 2; result prepared 2026-11-23 14:42:19 UTC. Review: RV-S2-R (separate party; pending).

The first-line sample count is **0 confirmed failures to follow**, with **16 agreements still factually undetermined**; it does not say that all 600 follow. The sample has 584 established agreements. The fifteen family outcomes are taken from `S2/adjudication/FAMILIES.md` and recomputed from all 105 rows of `S2/adjudication/rows.tsv`: 18 object rows with outcome 0, 83 with ?, and 4 with 1. Those give six families with 0, nine with ?, and none with 1. These are inventory rows, including overlapping directory/member rows, not a count of independent physical failures.

The combination rule is `TEXT.md` Appendix A.4.1: any 0 gives 0; otherwise any ? gives ?; otherwise 1. A shared gap remains a gap under (not published: orchestration or scratch), including when both readings demand the same declaration. Unknown facts are not converted into gaps. Section 8.5 leaves implementation mechanisms outside the definition. No weighting list is made: `SUP1/step-2.md`, Rules of Supplement 1, reserves that question for the author.

**The fifteen fixed families.** Every example ID is included below; its scope and factual limitations are in `S2/FACTS.md`, with detailed evidence in (not published: direct evidence at least 2 MB). The decisions and declaration differences are the existing family adjudication, not a second adjudication of those objects. In the objects column, 0, ? and 1 are object outcomes, not verdict names. Sentence IDs refer to `SENTENCES.md`; exact sentences used in the report are reproduced at the end.

| No. and fixed title | Outcome | Objects examined | Sentences | Decisions and what differs in the declaration |
|---|---|---|---|---|
| 1. a default value created during installation that no person of the computer chose | ? | 10 rows. Default service states, accounts and alternative/command links.<br>? (10): `alma-37c4765f1bc3df9c50c7463a`, `alma-53fa364e2cf166bce33a9d60`, `alma-71966c5e14f6b1d3115de310`, `alma-9a2b3f5598419c41bbb752af`, `alma-ade8ccca9c3e357d72437c37`, `microos-13cd5b718c5e71a530a2bed1`, `void-081c93f14c8fa7e6bfd59961`, `void-4768b27116e866909ce713da`, `void-65591628311f83a7842469aa`, `void-f1bd8c260127e9a626b5f82f` | S8.2-7, S8.2-11, S8.2-13, S8.2-15, S8.2-17 | No established pair. Unknown personal choice, producing transaction and/or as-received status prevent a decision. A chosen setting could require its own line; an installation default could use the package line; a program record would require none. These are conditional alternatives, not a confirmed gap. |
| 2. a list the system generated from installed packages | ? | 9 rows. Module indexes, dconf/SELinux/MIME databases, certificate stores and ldconfig cache.<br>? (9): `alma-889f8cd2dae65a248533322a`, `alma-caff428f8364f0a663721a85`, `microos-2ce40b9afb2194333071f853`, `microos-a1f877f4c02acd2a5f9a0d97`, `microos-c111706edb49a56b42b0ff18`, `microos-dcce813055fa256ed012c87a`, `void-4ab73c90e99c24b1fb10c341`, `void-982c71cf468c85befb1aa508`, `void-f2e5d5edfa5902c8aee7bace` | S8.2-6, S8.2-7, S8.2-11, S8.2-15, S8.2-16 | No established pair. c2 proposed a generated-list line versus no line for a record; some groups also contain candidate settings. Unknown receipt status, producer, inputs and member contents leave earlier questions open. |
| 3. files left from an earlier version of a package that is still installed | ? | 4 rows. Retained 6.12.11_1 kernel/module files and their directory groups.<br>? (4): `void-0ffeda9e5b96728703a1b7ed`, `void-2715a0cd9890aae192131492`, `void-7c442df1fb52f7545f18f9cb`, `void-b42866904294dd5e14707b80` | S8.2-7, S8.2-9, S8.2-16, S8.2-20 | No established pair. The current package-name line versus the retained version line is conditional on unknown unchangedness and module loadability. The package-name/exact-version reading question remains conditional. |
| 4. a stored archive whose contents are executed | 0 | 6 rows. Initramfs files and boot-directory groups; the three 0 rows concern two Void archives and their containing group.<br>0 (3): `void-0d4bff48fce03ced27aa83a4`, `void-386e90812bdecbec21d0785c`, `void-a6e5bb36a961f99d2e09e83e`<br>? (3): `alma-2c25c1a886c5db421b08087b`, `alma-c4a7c6d6eb439eb9d680a65e`, `microos-62ccb03ff56e2af8ff91ff68` | S8.2-6, S8.2-7, S8.2-9, S8.2-10, S8.2-15, S8.2-16, S8.2-23 | PROGRAM versus PROGRAM RECORD: executing unpacked contents is read as executing the archive through another program, or the archive itself is only read/unpacked. The first requires archive coverage by a kernel/package-derived line or its own line; the second requires nothing for the archive. Other members of the boot group remain undetermined. The saved adjudication establishes the archive producer and treats the remaining unknown sources as affecting the covering line, not the gap. |
| 5. a package of a program's built-in installer whose code runs only inside that program | ? | 2 rows. Two browser-extension groups.<br>? (2): `alma-2ea4b9f74eb9ce06f9d317ff`, `void-61a9a88ad2b852b6cf106db6` | S8.2-1, S8.2-6, S8.2-7, S8.2-21 | No established pair. An own package line versus no required line under the inside-program exception depends on unknown effective extension rights. Whether the exception applies after question 1 remains a conditional reading question. |
| 6. files that a self-managing client installs and deletes for itself | ? | 7 rows. The juliaup executable and six Steam client/runtime/resource objects.<br>? (7): `developer-cbe2f19f976b603f5bb42193`, `gaming-1fd35bf6b4019193bad37621`, `gaming-495169019fec2fb328ec9636`, `gaming-4cf3d1cb3da5181824cbdf16`, `gaming-5e400a5875aa136f688db7de`, `gaming-820d8fed19aa17b72181a2d7`, `gaming-cfd36e0732b4def2d5ecaf69` | S8.1-4, S8.1-5, S8.1-6, S8.2-6, S8.2-7, S8.2-9, S8.2-15, S8.2-16 | No established pair or determinate declaration difference: receipt integrity, group contents and execution/launch capabilities remain unknown. Being managed by the client does not by itself establish a decision. |
| 7. repository history fetched at a person's command | 0 | 10 rows. Six cloned-project repository-storage groups and four Homebrew repository groups.<br>0 (6): `developer-2cd27841286438a33a7be083`, `developer-3f398d23eb0fcf553dff5b42`, `developer-53425eb85c9fbc80fd72ef81`, `developer-6939a0c70bd7e159e638d411`, `developer-b33a49ff4891eb30d52c7e46`, `developer-e6a1511f1247825437884782`<br>? (4): `developer-05617e28292b94b182cc73aa`, `developer-216b547047e9bd323ef8a31b`, `developer-4fbf65b1725f19d2f17c9c20`, `developer-6bf67733481480cdeaa37d0c` | S8.2-7, S8.2-15, S8.2-2 | PROGRAM RECORD versus MATERIAL for the six project groups: Git wrote them and a person brought them by requesting the fetch. Nothing differs in the declaration; neither decision requires a line. The four Homebrew groups retain an unknown earlier package question. |
| 8. container images and containers | 0 | 7 rows. One stored container, four images and two engine-directory groups.<br>0 (1): `developer-59a4ddfe60a8a1b18f6627c9`<br>1 (4): `developer-78e8326714450972e0134fb6`, `server-46f5ba6815bb94894157236c`, `server-bce2d2fe9dfb24c822a93809`, `server-fc8e0ac75ce9ed64a08ff655`<br>? (2): `developer-fd23729ab637faddccc1bc3e`, `developer-ffcb51cbd136cf2f6e7408cf` | S8.1-4, S8.1-6, S8.2-6, S8.2-7, S8.2-9, S8.2-11, S8.2-13, S8.2-16, S8.2-17, S8.2-22, S8.2-23 | For the container, c1 gives INSTALLED-OWN or SETTING-OWN and c2 PROGRAM-OWN or SETTING-OWN. Nothing differs in the declaration: all require its own line. This shared gap is carried forward under TASK-S2-J.md. The four images were resolved as PROGRAM-OWN; the engine groups remain unknown. |
| 9. package contents held in an installer's cache | 0 | 11 rows. Go module source caches, uv/bun caches and a retained gem archive.<br>0 (3): `developer-28b0928f32a3bd540164f5c2`, `developer-4bc7e8a9213ac909292c2e0a`, `developer-9e6d06f152c07e5c13f841e0`<br>? (8): `developer-226fd83ddc29964f9bdb3d55`, `developer-880c223d69d1d6670ff0f5f3`, `developer-95ffe3a0117370c7c58c4a2c`, `developer-967f944eb81a27eff658797b`, `developer-a69abe8bb84f8c032e1fc8ed`, `developer-b62fee8be986a1229ba680e5`, `developer-b8d0d1ff228a2993234f695a`, `developer-d1fbc4bd76f69c08a8b6ecf7` | S8.1-6, S8.2-6, S8.2-7, S8.2-9, S8.2-15, S8.2-16, S8.2-23 | For the three Go cache rows, PROGRAM versus PROGRAM RECORD: source executable through a toolchain, or values only read by the compiler. The first requires an own line for the cached source; the second requires nothing. The other eight rows retain unknown receipt/member facts; the retained-gem reading is conditional. |
| 10. code that an installed program copies or generates as it runs | 0 | 7 rows. A Git template-hook copy, K3s CNI links, shell completions, a wrapper and Wine code groups.<br>0 (2): `developer-3bcbeded8b7cf5aedc1382fb`, `server-be5afc83ca654a448cd1fb60`<br>? (5): `developer-35549cad55c96268fcaf4f24`, `developer-bc1494f6f41c4c0f3175eb8c`, `gaming-542ab2b7a1cac1d1e2d23e7f`, `gaming-85b507e7ce1d3c2a16693bb3`, `gaming-fe91919b6bab6568dfdea112` | S8.2-6, S8.2-7, S8.2-9, S8.2-10, S8.2-15, S8.2-16, S8.2-20, S8.2-21, S8.2-23 | Hook: unchanged package content (git-core line) versus a copied PROGRAM (own or template-copy line). Links: PROGRAM (K3s line or own lines) versus PROGRAM RECORD (nothing). Five other rows retain unknown receipt, interpreter or member-execution facts. |
| 11. values the computer obeys that a program generated rather than a person chose | ? | 8 rows. Resource controls, forwarding policy, audio cookie, K3s datastore/manifests/credentials and node-password storage.<br>? (8): `developer-342e1a9fd229e3473b8c35b3`, `developer-70be1c323890746c1a78c6f5`, `gaming-1ba8cee6c38131f0b6c75952`, `server-034bd74a045c24aa6dd19160`, `server-0a575e792deb53a2ae502487`, `server-7bf44e4e4a03c100b6ad395a`, `server-c6809ad0393bc02f2943127a`, `server-ddd20eb86c2fac35aad9742a` | S8.2-6, S8.2-7, S8.2-9, S8.2-11, S8.2-13, S8.2-14, S8.2-15, S8.2-17 | No established pair. A setting with its own line, coverage by an installation/registration line, or no line for a record depends on unknown writer, personal choice, contents or derivation inputs. |
| 12. value files whose entries include commands that are run | 0 | 3 rows. Groups containing a Dockerfile, lefthook.yml and a cron file.<br>0 (3): `developer-d916e8927ebf41371ab8dd1d`, `developer-e56b4f802a20335d455ecb3a`, `server-c354536d6d9a738329571706` | S8.2-6, S8.2-7, S8.2-9, S8.2-11, S8.2-13, S8.2-14, S8.2-15, S8.2-16, S8.2-17, S8.2-23 | PROGRAM versus SETTING: code executed by a consumer, or values whose commands launch something. Nothing differs for the disputed files; both require their own line. The Dockerfile group also contains index.html material, requiring no line. |
| 13. a browser's home page and “launches something” | ? | 2 rows. Two channel-described browser preferences: theme and home-page URL.<br>? (2): `s2-1`, `s2-2` | S8.2-3, S8.2-9, S8.2-11, S8.2-14 | No established pair. No instance was observed on a computer. A home-page launch/ordinary navigation distinction also lacks the selected URL and its behavior. No actual declaration difference is established. |
| 14. a compiler or a build tool as a built-in tool or as general-purpose work | ? | 17 rows. Seventeen channel artifacts: compiler outputs/source, build recipes/cache/log, installed outputs, PATH/link, replacement libraries and plugins.<br>? (17): `s2-10`, `s2-11`, `s2-12`, `s2-13`, `s2-14`, `s2-15`, `s2-16`, `s2-17`, `s2-18`, `s2-19`, `s2-3`, `s2-4`, `s2-5`, `s2-6`, `s2-7`, `s2-8`, `s2-9` | S8.2-3, S8.2-7, S8.2-9, S8.2-16, S8.2-20, S8.2-23 | No established pair. All lack observed presence. c2 proposed own lines, a containing-package line for s2-18, no lines for s2-8/s2-9, and own-line versus no-line readings for s2-5; none settles an observed instance. The additional missing fact for each disputed row is named in adjudication/rows.tsv. |
| 15. saved history as values read or as executable statements | ? | 2 rows. Two channel-described saved histories: Python and shell.<br>? (2): `s2-20`, `s2-21` | S8.2-3, S8.2-9, S8.2-15, S8.2-16, S8.2-23 | No established pair. PROGRAM with an own line versus PROGRAM RECORD requiring nothing remains conditional on observed presence and whole-file executability, both unknown. |

**Sample adjudication and accounting.**

Inputs `S2/a1/sample.tsv` and `S2/a2/sample.tsv` each contain the same 600 unique `(source, id)` keys and the same original decisions: 300 from D1 and 300 from A3. Their union of `DOES-NOT-FOLLOW` rows is exactly the eight rows of `S2/sample/flagged.tsv`, all from A3. Each has exactly one row in `S2/sample-adjudication.tsv` and one answer from each of `S2/b1/answers.tsv` and `S2/b2/answers.tsv`. The `a1` and `a2` columns of the new adjudication copy their findings; the original decision is identified in its reason and below.

| Source | Sampled | Both parties FOLLOWS | Challenged and resolved to original decision | Confirmed does not follow | Factually undetermined after this task | Sample outcome |
|---|---:|---:|---:|---:|---:|---|
| D1 | 300 | 291 | 0 | 0 | 9 | ? |
| A3 | 300 | 291 | 2 | 0 | 7 | ? |
| Total | 600 | 582 | 2 | 0 | 16 | ? |

**Agreements that do not follow, grouped by cause:** none is established after adjudication. The eight challenges form the following three groups; their rejection or factual uncertainty must not be reported as a confirmed gap.

| Cause of challenge | Example IDs (all challenged rows) | Original agreement and adjudication | Reason and evidence |
|---|---|---|---|
| Additional hard-link names for unchanged packaged files | `gaming-0b9c75abae9461b0be7b041d`, `gaming-7b8b804e906bab4f5a36ccf2` | INSTALLED-PACKAGE; both RESOLVED:INSTALLED-PACKAGE; outcome 1 | The six backend members and the separately sampled snmp file are the same files as unchanged package members: saved device/inode pairs and full-digest integrity records in `S2/a2/raw/evidence.txt:1–18`; complete group in `S2/a2/raw/facts.jsonl`. S8.2-7 asks about the object, not manifest coverage of every pathname. Question 1 therefore wins under S8.2-6; S8.2-8 and S8.2-16 give the original category and package line. a2 adds a pathname condition that the sentence does not contain. Installation link commands are saved in `S2/b2/raw/cups-daemon-postinst-backends.txt`. |
| Retained Steam update archives with unknown package relationship and content behavior | `gaming-4538cc406b1a701b2b46aa9a`, `gaming-92303a3b6a6e1ad452236f8b`, `gaming-b9490dffe916c5dcc4575874` | RECORD; all FACT-UNKNOWN; outcome ? | Download and extraction are established (`S2/b1/evidence.md#steam`); exact archive members, installed-unit membership, applicable receipt integrity and execution semantics are not (`S2/a1/sample.tsv`, `S2/a1/raw/a3-first-notes.md`, `S2/a1/raw/a3-second-notes.md`, and `S2/a2/raw/facts.jsonl`, these IDs). S8.2-7 and S8.2-9 remain open before S8.2-15. a2 assumes the retained archive is the installed package in one branch and that compression excludes question 2 in the other. No gap on complete facts is established. |
| Self-extracted K3s executables with unknown receipt integrity | `server-0343cc0e3743fdc6279f4a3e`, `server-9c59629a43e8b28a746de9d5`, `server-a1bf573f2de859142047fce6` | PROGRAM-DERIVED; all FACT-UNKNOWN; outcome ? | Installation/extraction and executable status are established (`S2/b1/evidence.md#k3s`). Individual received-content integrity is not (`S2/a1/raw/a3-second-notes.md`, three-executable paragraph; `S2/a2/raw/facts.jsonl`). Absence from the native manifest does not exclude a package under S8.1-6. S8.2-7 may decide before S8.2-9, so a2 cannot assume PROGRAM and treat the later S8.2-16 reading as a confirmed gap. Recording is required under the executable alternatives, but the exact category and derived-line agreement remain unestablished. |

For CUPS, the resolution concerns unchanged file identity and does not decide the meaning of a copied file with a new identity (family 10). For Steam and K3s, the parties’ answers by meaning below do not fill gaps in the observations. The full literal quotations, deciding facts and party-specific reasons are in `S2/sample-adjudication.tsv`.

Ten other sampled rows have no `DOES-NOT-FOLLOW` finding and are outside the requested eight-row adjudication. Nine D1 cache rows have `FACT-UNKNOWN` from both parties; the netplan bytecode group has `FACT-UNKNOWN` from a1 and `FOLLOWS` from a2. These unknowns are retained in the sample outcome, not silently counted as successful agreements.

| Unchallenged but unresolved group | All IDs | Missing fact and source |
|---|---|---|
| Cached HTTP/package payloads, 9 rows | `alma-0c65c3ff2333b5855dfa1218`, `alma-287954d7986f9463a1d03ac8`, `alma-69ab72dbf21ea1a6fe95344f`, `alma-93b0c210150c3de57fd663ee`, `alma-f5ab3aad000b60bbc3ac8948`, `void-12f32d2564ec32286c1c2b07`, `void-699cd2b65d15f73d24572000`, `void-9d09e92bf4395146455c4fb1`, `void-e2089ad0c038bd9d897b2a5e` | Content and execution/package status; hashes and metadata do not distinguish response values from package/code payloads. `S2/a1/sample.tsv` and `S2/a2/sample.tsv`, these IDs. Earlier questions S8.2-7/S8.2-9 cannot be skipped for S8.2-15. |
| netplan.io bytecode, 1 row | `server-ab60c4296b0c35885f31cca0` | a1 reports missing generation provenance: the retained compilation script belongs to python3-netplan, a different package. a2 calls the compiled-copy route established. Neither marks DOES-NOT-FOLLOW, so this task does not extend its adjudication to that difference. The unresolved S8.2-16 route remains ?. `S2/a1/sample.tsv`, `S2/a2/sample.tsv`, `S2/a1/raw/a3-second-notes.md`. |

**Both parties’ answers for every confirmed gap.** The following 18 rows cover all outcome-0 objects in the fixed families, including shared gaps and group rows containing a gap. The four answer cells are copied verbatim from the named columns of `S2/c1/decisions.tsv` and `S2/c2/decisions.tsv`. The first question asks whether inclusion is required by meaning; the second asks whether the requirement can be met without forbidding an ordinary action listed in Section 9.2. No answer is supplied by this result.

For the signs of `PROTOCOL.md` Section 2, equality means the same yes/no answer to required inclusion. The full line qualifications remain visible: yes with an own line and yes with package coverage agree on inclusion, not necessarily on which line. Both second answers must be yes. This reports the two signs only; it assigns no gap to either weighting list. Fifteen gap rows have both signs and three do not.

| Family / gap object | c1 by_meaning | c2 by_meaning | c1 without_forbidding | c2 without_forbidding | Section 2 signs established by these answers |
|---|---|---|---|---|---|
| 4 / `void-0d4bff48fce03ced27aa83a4` | yes: own line | yes: covered by the line of package linux6.12 | yes | yes | both signs: same yes; both yes |
| 4 / `void-386e90812bdecbec21d0785c` | yes: own line | yes: covered by the kernel package lines and the bootloader line | yes | yes | both signs: same yes; both yes |
| 4 / `void-a6e5bb36a961f99d2e09e83e` | yes: own line | yes: covered by the line of package linux6.18 | yes | yes | both signs: same yes; both yes |
| 7 / `developer-2cd27841286438a33a7be083` | no | no | yes | yes | both signs: same no; both yes |
| 7 / `developer-3f398d23eb0fcf553dff5b42` | no | no | yes | yes | both signs: same no; both yes |
| 7 / `developer-53425eb85c9fbc80fd72ef81` | no | no | yes | yes | both signs: same no; both yes |
| 7 / `developer-6939a0c70bd7e159e638d411` | no | no | yes | yes | both signs: same no; both yes |
| 7 / `developer-b33a49ff4891eb30d52c7e46` | no | no | yes | yes | both signs: same no; both yes |
| 7 / `developer-e6a1511f1247825437884782` | no | no | yes | yes | both signs: same no; both yes |
| 8 / `developer-59a4ddfe60a8a1b18f6627c9` | yes: own line | yes: own line | yes | yes | both signs: same yes; both yes |
| 9 / `developer-28b0928f32a3bd540164f5c2` | no | no | yes | yes | both signs: same no; both yes |
| 9 / `developer-4bc7e8a9213ac909292c2e0a` | no | no | yes | yes | both signs: same no; both yes |
| 9 / `developer-9e6d06f152c07e5c13f841e0` | no | no | yes | yes | both signs: same no; both yes |
| 10 / `developer-3bcbeded8b7cf5aedc1382fb` | yes: covered by git-core template-copy line for applypatch-msg.sample | no | yes | yes | not both: first answers differ; both second answers yes |
| 10 / `server-be5afc83ca654a448cd1fb60` | yes: covered by k3s installation and CNI setup line | yes: covered by the line of k3s | yes | yes | both signs: same yes; both yes |
| 12 / `developer-d916e8927ebf41371ab8dd1d` | yes: own line | no | yes | yes | not both: first answers differ; both second answers yes |
| 12 / `developer-e56b4f802a20335d455ecb3a` | yes: own line | no | yes | yes | not both: first answers differ; both second answers yes |
| 12 / `server-c354536d6d9a738329571706` | yes: own line | yes: own line | yes | yes | both signs: same yes; both yes |

**Sample answers, published for all eight adjudicated rows.** There is no confirmed outcome-0 sample gap. Nevertheless, both parties’ supplied answers are reproduced verbatim below. The last column states whether their answers would establish both signs if a gap were established; it does not turn a resolved row or an unknown fact into a gap.

| Sample ID / adjudication | b1 by_meaning | b2 by_meaning | b1 without_forbidding | b2 without_forbidding | Section 2 signs from the answers alone |
|---|---|---|---|---|---|
| `gaming-0b9c75abae9461b0be7b041d` / RESOLVED:INSTALLED-PACKAGE | yes: covered by the cups package line | yes: covered by the line of package cups | yes | yes | both signs: same yes; both yes; no confirmed gap |
| `gaming-4538cc406b1a701b2b46aa9a` / FACT-UNKNOWN | no | no | yes | yes | both signs: same no; both yes; no confirmed gap |
| `gaming-7b8b804e906bab4f5a36ccf2` / RESOLVED:INSTALLED-PACKAGE | yes: covered by the cups package line | yes: covered by the line of package cups | yes | yes | both signs: same yes; both yes; no confirmed gap |
| `gaming-92303a3b6a6e1ad452236f8b` / FACT-UNKNOWN | no | no | yes | yes | both signs: same no; both yes; no confirmed gap |
| `gaming-b9490dffe916c5dcc4575874` / FACT-UNKNOWN | no | no | yes | yes | both signs: same no; both yes; no confirmed gap |
| `server-0343cc0e3743fdc6279f4a3e` / FACT-UNKNOWN | yes: covered by the K3s installation line | yes: covered by the line of k3s (/usr/local/bin/k3s) | yes | yes | both signs: same yes; both yes; no confirmed gap |
| `server-9c59629a43e8b28a746de9d5` / FACT-UNKNOWN | yes: covered by the K3s installation line | yes: covered by the line of k3s (/usr/local/bin/k3s) | yes | yes | both signs: same yes; both yes; no confirmed gap |
| `server-a1bf573f2de859142047fce6` / FACT-UNKNOWN | yes: covered by the K3s installation line | yes: covered by the line of k3s (/usr/local/bin/k3s) | yes | yes | both signs: same yes; both yes; no confirmed gap |

**Comparison with the expectation recorded before this step.** The fixed clauses of `SUP1/step-2.md` are checked separately below. The six-family clause is also expanded into its six named families. An unknown outcome is reported as not met (not established), not as a refutation of the expected complete-facts result. No family, denominator or numerical expectation is changed.

| Expected clause | Met or not met | Observed result |
|---|---|---|
| With complete facts, families 2, 3, 4, 5, 11 and 12 will still receive two decisions or none | Not met as a whole | Families 4 and 12 are 0; 2, 3, 5 and 11 are ?. Complete deciding facts were not obtained for those four families. |
| Family 2 will receive two decisions or none | Not met (not established) | ?; nine rows with deciding facts unknown. |
| Family 3 will receive two decisions or none | Not met (not established) | ?; four rows with deciding facts unknown. |
| Family 4 will receive two decisions or none | Met | 0; three archive-related rows with two decisions. |
| Family 5 will receive two decisions or none | Not met (not established) | ?; both extension groups lack deciding capability facts. |
| Family 11 will receive two decisions or none | Not met (not established) | ?; eight rows with deciding facts unknown. |
| Family 12 will receive two decisions or none | Met | 0; the Dockerfile, hook configuration and cron cases receive two decisions. |
| Family 1 will receive one decision | Not met (not established) | ?; all ten rows are undetermined, rather than one-decision objects. |
| Family 7 will receive two decisions under which the declaration is the same | Met | Six project-repository rows are PROGRAM RECORD or MATERIAL, both requiring nothing; four Homebrew rows remain ?. The family outcome is 0. |
| At most 20 of the 600 sampled agreements will not follow from a sentence | Met | 0 confirmed, 16 still undetermined, 584 established. Even if all 16 unresolved agreements eventually failed, the count would be 16, within the unchanged expectation of at most 20. This arithmetic does not make the sample outcome 1. |

Families 8, 9 and 10 also have outcome 0. The expectation gives no explicit outcome prediction for them, or for families 6, 13, 14 and 15; no additional prediction is inferred. The at-most-20 expectation remains a prediction, never a pass threshold.

**Questions for the author.** Questions 1–3 and 8–10 preserve the reading choices in `S2/QUESTIONS.md`; questions 4–7 state the other confirmed family gaps in plain words. Questions with unknown factual premises remain conditional. The questions ask what the fixed text means and do not propose changes.

1. **An archive whose contents run (family 4).** Does running code after unpacking an archive make the archive itself a program, or is the archive a program record because it is only read and unpacked? The first reading requires recording the archive; the second does not. S8.2-9 and S8.2-23; `S2/QUESTIONS.md` item 1.
2. **Source read by a compiler (family 9).** Is source code that the toolchain can turn into an executed program itself executable through another program, or is it only input read as values? For the cached source, the alternatives are a required program line and no required line for a record. S8.2-9 and S8.2-23; `S2/QUESTIONS.md` item 2.
3. **A symbolic link used to start a program (family 10).** Is the link a program because starting it runs its target, or is it only a stored path read by the system? The alternatives require recording it or require nothing. S8.2-9 and S8.2-23; `S2/QUESTIONS.md` item 3.
4. **A copied package file (family 10).** Does an unchanged copy made by Git remain an object obtained as part of the original package, or does the new copy need its own line or a line describing the copy operation? S8.2-7 and S8.2-16; `developer-3bcbeded8b7cf5aedc1382fb` in `S2/adjudication/rows.tsv`.
5. **Repository data fetched at a person’s request (family 7).** When Git writes the data and a person has requested that it be brought to the computer, is it a program record or material? Both clauses of S8.2-15 fit the six confirmed rows. Neither requires a declaration line.
6. **A stored container (family 8).** Does the inventoried container stand for the installed or executable contents, or for the person-chosen values that specify what will run? Both parties found two decisions, while all their alternatives require the same own line. `developer-59a4ddfe60a8a1b18f6627c9` in `S2/adjudication/rows.tsv`; S8.2-7, S8.2-9, S8.2-11 and S8.2-13.
7. **Files containing commands among values (family 12).** When a consumer reads fields and runs the commands in them, does it execute the file as code, or only read values that launch something? The program and setting readings both require the file’s own line. S8.2-23 with S8.2-13/S8.2-14; the three family-12 rows.
8. **An installed extension with restricted abilities (family 5; conditional).** If the missing capability facts establish that an extension cannot launch programs or change the computer, does the inside-program exception still remove the recording requirement after question 1 has made it an installed object? Or does question 1 retain the recording requirement? S8.2-1, S8.2-6 and S8.2-21; `S2/QUESTIONS.md` item 4.
9. **Files retained from an old package version (family 3; conditional).** Once unchangedness and loadability are known, does the installed-package condition mean the package name that is still installed, or the exact old version from which the files came? S8.2-7; `S2/QUESTIONS.md` item 5.
10. **A retained package archive (family 9; conditional).** Is the archive the installed package itself, or a member file whose unchangedness must also be known? This is the saved question for the retained gem. The Steam sample raises a related archive-versus-installed-unit issue, but its deciding facts remain unknown; it supplies no additional confirmed gap. S8.2-7; `S2/QUESTIONS.md` item 6 and the three Steam rows of `S2/sample-adjudication.tsv`.
11. **A program extracting its own bundled executables (sample; conditional).** If question 1 is eventually answered no for the K3s files, does the installation line count as a line from which the system itself obtained them, or is a separate line required for each? This records a2’s proposed later reading of S8.2-16 without deciding it or counting it as a gap before the receipt facts are known. The three K3s rows of `S2/a2/sample.tsv` and `S2/sample-adjudication.tsv`.
12. **Publishing the two weighting lists.** Since the calibration did not pass and weighting did not begin, should the two lists nevertheless be made using the signs of Section 2 of `PROTOCOL.md`? `SUP1/step-2.md`, Rules of Supplement 1, explicitly leaves this to the author. Until an answer, the side-by-side answers above establish only whether the two signs agree; no gap is assigned to either list.

**Exact sentences cited.** Copied from `SENTENCES.md`; Markdown emphasis alone is removed.

S8.1-4 “Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.”

S8.1-5 “A general-purpose program with a built-in installer counts as an installer in that part of its functionality.”

S8.1-6 “Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.”

S8.2-1 “Everything that is installed and every setting must be recorded.”

S8.2-2 “The rest need not be recorded.”

S8.2-3 “The rule applies to objects that are on the computer.”

S8.2-6 “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7 “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-8 “Then it is an installed object, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”

S8.2-9 “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-10 “Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.”

S8.2-11 “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”

S8.2-13 “Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.”

S8.2-14 “A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.”

S8.2-15 “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-16 “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

S8.2-17 “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

S8.2-20 “A file containing code that cannot be executed on this computer is not a program.”

S8.2-21 “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.”

S8.2-22 “A program that runs as its own process on the computer, including in a container, is a program.”

S8.2-23 “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

**Mechanical verification.** The required quote check and structural/count checks are recorded in `S2/raw/result-validation.txt`. Independent substantive acceptance remains with review RV-S2-R.
