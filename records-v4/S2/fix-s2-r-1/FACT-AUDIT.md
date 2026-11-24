# Deciding-fact audit for finding 2

The 11 shared-gap rows named in finding 2 have 23 facts explicitly marked UNKNOWN in (not published: direct evidence at least 2 MB). Every one is copied, with its original line reference, the applicable sentences and the reason it does not decide the stated alternatives, into `S2/fix-s2-r-1/unknown-facts-audit.tsv`. No UNKNOWN value has been filled in. The audit also checks qualifications embedded in otherwise known facts, as explained below. The original decisions remain in `S2/c1/decisions.tsv` and `S2/c2/decisions.tsv`; the revised adjudication is `S2/fix-s2-r-1/rows.tsv`.

## What unknown designation does and does not affect

All 11 objects have unknown `primary_description_designation`. S8.1-3 “The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.” This determines which files constitute an actual declaration. The question here is what must be recorded, not whether a particular declaration already records it: S8.2-1 “Everything that is installed and every setting must be recorded.” S8.2-2 “The rest need not be recorded.” S8.2-19 “What need not be recorded may also be recorded in the declaration.” A designation cannot turn optional inclusion into required inclusion or settle any of the disputed categories. No claim about an existing declaration, a successful application, or the properties of Section 8.3 is made.

Exact historical author identity and drafting time are not supplied beyond the operator role and action interval. S8.2-11 requires a person's choice, not that person's identity or a drafting timestamp. Where that question matters, the choice itself is recorded. The absence of those finer details is not used to infer a choice.

## Family 7: six project repository-storage rows

| Object | Unknown facts (lines in (not published: direct evidence at least 2 MB)) | Known delivery / reading / producer (lines in the same file) |
|---|---|---|
| `developer-2cd27841286438a33a7be083` | designation 19225; unchangedness 19231 | 19205 / 19208 / 19228 |
| `developer-3f398d23eb0fcf553dff5b42` | designation 19254; unchangedness 19260 | 19234 / 19237 / 19257 |
| `developer-53425eb85c9fbc80fd72ef81` | designation 19319; unchangedness 19325 | 19292 / 19295 / 19322 |
| `developer-6939a0c70bd7e159e638d411` | designation 19362; unchangedness 19368 | 19328 / 19331 / 19365 |
| `developer-b33a49ff4891eb30d52c7e46` | designation 19455; unchangedness 19461 | 19421 / 19424 / 19458 |
| `developer-e6a1511f1247825437884782` | designation 19484; unchangedness 19490 | 19464 / 19467 / 19487 |

The known delivery is the requested project clone. These are repository objects and references written by Git, not objects received with the installed Git package, and the project clone is not an installer transaction under S8.1-4/-6. Thus unknown receipt integrity does not open S8.2-7. This conclusion uses the known delivery, not the lack of a native-package manifest entry. The stored references and packs are read as repository data, with no registered hook, startup command or access directive at these paths; S8.2-9/-23 and S8.2-11/-14 do not decide before question 4. The remaining alternatives are Git recording the data and a person bringing the data through the requested clone. Both clauses of S8.2-15 fit. Neither requires a line.

The four Homebrew repository groups remain FACT-UNKNOWN: their installation-fetch provenance differs. No inference about their package status is made from this six-row audit.

## Family 8: the stored container

`developer-59a4ddfe60a8a1b18f6627c9` has four UNKNOWN facts: `execution_rights` (19496), `host_change_capability` (19498), `primary_description_designation` (19522), `unchanged_since_receipt` (19526). Each receives its own entry in the TSV audit.

The old description of this as an unexamined shared gap is withdrawn. c1's INSTALLED-OWN alternative is set aside, consistently with the frozen four-image resolutions (`S2/adjudication/rows.tsv:51` and the other image rows). The same dossier gives creation, starting and removal of containers (19502), rather than an installed-package receipt for this object. Unknown receipt integrity therefore does not decide either remaining alternative.

The remaining alternatives are established on the saved facts:

- The container's workload is running (`inventory_State`, 19517) and runs as its own host-kernel process (19524). S8.2-9 and S8.2-22 give PROGRAM-OWN if the stored container denotes this executable workload. S8.2-22 “A program that runs as its own process on the computer, including in a container, is a program.” Exact UID, capability and mount details cannot undo this known process boundary. The inside-program exception of S8.2-21 is not the basis of this reading.
- The operator selected the command, ports and restart behavior (19499, 19503, 19514, 19519). S8.2-11/-13 give SETTING-OWN if the stored container denotes these persistent service values. Exact workload capabilities are not a condition for the service values to be settings. Unknown primary-description designation does not affect required inclusion, for the reason above.

This is not a choice between question 2 and question 3 for an already specified file. S8.2-6 orders those questions; it does not identify whether the stored-container object denotes the executable workload or its saved service values. Both are evidenced; neither is an inferred missing fact. The question remains for the author (`S2/RESULT.md`, question 6). The revised verdict is GAP, outcome 0, with PROGRAM-OWN / SETTING-OWN and no declaration difference. Family 8 remains 0: one gap, four resolved images, two unknown engine groups. The original INSTALLED-OWN reading is not needed to sustain that outcome.

## Family 10: the copied sample hook

`developer-3bcbeded8b7cf5aedc1382fb` has one explicit UNKNOWN: designation (20307), addressed above. The complete 482-byte comparison and unchanged source-package digest are known (20279, 20313); Git's template initialization is known (20310); explicit script execution is possible despite the `.sample` suffix (20298, 20304). A historical per-member execution trace is not retained (20309), but S8.2-9 asks whether the computer executes **or can execute** the code, so a past execution event is not needed. The known interpreter/caller behavior supplies that capability. Both parties' unchanged-package-copy / later-created-program readings remain; no sentence chooses whether receipt follows the copy. Outcome 0 remains.

## Family 12: the command-bearing files

| Group object | Explicit UNKNOWN facts (lines in (not published: direct evidence at least 2 MB)) | Known content / producer / consumer (lines in the same file) |
|---|---|---|
| `developer-d916e8927ebf41371ab8dd1d` | designation 26728; unchangedness 26734 | 26701 / 26731 / 26704 |
| `developer-e56b4f802a20335d455ecb3a` | designation 27044; unchangedness 27050 | 26737 / 27047 / 26740 |
| `server-c354536d6d9a738329571706` | designation 27073; unchangedness 27080 | 27053 / 27076 / 27056 |

The disputed files are locally authored Dockerfile, lefthook.yml and cal-maintenance, not files obtained with an installed package. Their known producer settles that premise of S8.2-7 without an unknown package-receipt comparison. Their content, chosen values and consumer behavior are held in the dossier. The remaining question is execution of the file as code versus reading values whose command is executed: S8.2-9/-23 versus S8.2-11/-13/-14. Neither unknown designation nor unknown receipt integrity chooses between these readings.

The Dockerfile facts qualify `execution_rights` with an unobserved UID inside the resulting image (26705), and `host_change_capability` with unretained container capabilities (26707). These concern the resulting workload. The known root-authorized build/run operations create an image/container and port mapping, and CMD launches a host-kernel container process (26704, 26707, 26711, 26730). S8.2-21 therefore does not exclude the disputed build-input program reading as code that cannot launch or change installation/settings. The exact child UID cannot decide code versus values. The lefthook consumer launches sh under user rights (26741, 26743, 27046); cron launches a root shell (27056-27059, 27075). Their launch capability is established, not guessed.

Scope remains the recorded immediate-child groups, not a recursive expansion. The two-member Dockerfile group contains the disputed Dockerfile and the known operator-created index.html material (26706, 26710). The one-member cron group contains cal-maintenance (27058). The 42-member project group has the identified lefthook.yml witness; its other recorded members include fetched project files and the built scc program, as both decisions explain. Receipt integrity is not a deciding premise for those project-clone/local-build objects; no installed-package delivery is claimed for them. A gap for lefthook.yml does not assert that the whole directory has one category. These rows count the existing inventory groups containing those witnesses, not new standalone observations or additional counts for their members.

This differs from the boot group of finding 3, whose retained old-version files have an unresolved installed-package/unchangedness premise. That group's revised outcome is ?; the two separately inventoried archive witnesses still give family 4 outcome 0. See `S2/fix-s2-r-1/rows.tsv`, `void-386e90812bdecbec21d0785c`.
