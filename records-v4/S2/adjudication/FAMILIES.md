FAMILIES: 0 with outcome 1; 6 with outcome 0; 9 with ?

Adjudication of supplement 1, step 2 (third party). Rows: `S2/adjudication/rows.tsv` (105 objects: 52 AGREED, 4 RESOLVED, 9 GAP, 40 FACT-UNKNOWN). Reading questions: `S2/QUESTIONS.md`. Outcome rule of `SUP1/step-2.md`: 1 if every example object receives one decision; 0 if an example object with all deciding facts known receives two decisions or none; ? otherwise. An object on which both parties found the same gap counts as decided (Section 9.2). Gap weights are not assigned (Supplement 1 leaves the lists to the author); the two signs of `PROTOCOL.md` Section 2 are recorded per row.

## Family 1: a default value created during installation that no person of the computer chose — outcome ?

- Objects: all 10 (`alma-37c4765f…`, `alma-53fa364e…`, `alma-71966c5e…`, `alma-9a2b3f55…`, `alma-ade8ccca…`, `microos-13cd5b71…`, `void-081c93f1…`, `void-4768b271…`, `void-65591628…`, `void-f1bd8c26…`) AGREED UNKNOWN by both parties: whether a person chose the value and which transaction created it are unknown in the dossier.
- Sentences: S8.2-11 “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”; S8.2-17.

## Family 2: a list the system generated from installed packages — outcome ?

- Objects: `alma-caff428f…` AGREED UNKNOWN; 8 FACT-UNKNOWN (`alma-889f8cd2…`, `microos-2ce40b9a…`, `microos-a1f877f4…`, `microos-c111706e…`, `microos-dcce8130…`, `void-4ab73c90…`, `void-982c71cf…`, `void-f2e5d5ed…`): producer, as-received status (and for trust stores and policy, a person's choice among the inputs) are unknown, so question 1 is open.
- Sentences: S8.2-7 “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”; the conflict c2 found, S8.2-15 against S8.2-16, would arise only if question 1 were answered no.

## Family 3: files left from an earlier version of a package that is still installed — outcome ?

- Objects: `void-0ffeda9e…`, `void-b4286690…` AGREED UNKNOWN; `void-2715a0cd…`, `void-7c442df1…` FACT-UNKNOWN (as-received status of the old files; loadability of the old modules).
- Sentences: S8.2-7; S8.2-20. A reading question on S8.2-7 (package name or exact version) is recorded as item 5 of `S2/QUESTIONS.md`; it arises only once the facts are known.

## Family 4: a stored archive whose contents are executed — outcome 0

- Objects: `alma-2c25c1a8…`, `alma-c4a7c6d6…` AGREED UNKNOWN; `microos-62ccb03f…` FACT-UNKNOWN (producer of the snapshot initrd unknown); `void-0d4bff48fce03ced27aa83a4`, `void-a6e5bb36a961f99d2e09e83e` GAP; `void-386e90812bdecbec21d0785c` GAP through its two archive members.
- Deciding facts known: the producer is “dracut run by kernel update” ((not published: direct evidence at least 2 MB)), so question 1 is no; the kernel unpacks the archive and executes the contained /init ((not published: direct evidence at least 2 MB)). The unknown archive sources change only the covering line.
- Sentences: S8.2-9 “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?” against S8.2-23 “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”
- Two decisions: PROGRAM (reading A) or PROGRAM RECORD (reading B, S8.2-15). Under A the declaration must contain the archive (by the kernel package line or a line of its own); under B it need contain nothing. Question for the author: `S2/QUESTIONS.md` item 1.
- Signs: both signs on all three gap rows (both parties answer yes to the first question, with different lines; both yes to the second).

## Family 5: a package of a program's built-in installer whose code runs only inside that program — outcome ?

- Objects: `alma-2ea4b9f7…`, `void-61a9a88a…` FACT-UNKNOWN: whether the extension can launch programs or change the host (`effective_extension_rights`) is unknown.
- Sentences: S8.2-1 “Everything that is installed and every setting must be recorded.”; S8.2-21 “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings”. If the add-on lacks those rights, the two sentences decide differently unless S8.2-6 excludes S8.2-21 for installed objects (`S2/QUESTIONS.md` item 4).

## Family 6: files that a self-managing client installs and deletes for itself — outcome ?

- Objects: all 7 (`developer-cbe2f19f…`, `gaming-1fd35bf6…`, `gaming-49516901…`, `gaming-4cf3d1cb…`, `gaming-5e400a58…`, `gaming-820d8fed…`, `gaming-cfd36e07…`) AGREED UNKNOWN by both parties (unchangedness since receipt, member contents and capabilities unknown).
- Sentences: S8.2-7; S8.2-9.

## Family 7: repository history fetched at a person's command — outcome 0

- Objects: 6 AGREED GAP (`developer-2cd27841286438a33a7be083`, `developer-3f398d23eb0fcf553dff5b42`, `developer-53425eb85c9fbc80fd72ef81`, `developer-6939a0c70bd7e159e638d411`, `developer-b33a49ff4891eb30d52c7e46`, `developer-e6a1511f1247825437884782`, the cloned project's repository storage); 4 FACT-UNKNOWN (the Homebrew repository groups: unchangedness since the installation fetch unknown, so question 1 is open).
- Sentences: S8.2-15 “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.” Both clauses fit; the text gives neither priority.
- Two decisions: PROGRAM RECORD or MATERIAL. What differs in the declaration: nothing; neither requires a line.
- Signs: both signs on the six agreed gap rows (both answer no to the first question, yes to the second).

## Family 8: container images and containers — outcome 0

- Objects: `developer-59a4ddfe60a8a1b18f6627c9` (the stored container) AGREED GAP; `developer-fd23729a…`, `developer-ffcb51cb…` (engine directories) AGREED UNKNOWN; the four images (`developer-78e83267…`, `server-46f5ba68…`, `server-bce2d2fe…`, `server-fc8e0ac7…`) RESOLVED:PROGRAM-OWN, own line.
- Images: S8.1-4 “Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs” fits Docker only if “download” is read as “install”, so question 1 is no; question 2 is yes (container programs execute as host-kernel processes); S8.2-22 “A program that runs as its own process on the computer, including in a container, is a program.” c1 misread S8.1-4 and, in its second reading, skipped question 2.
- Container, two decisions found by both parties: c1 INSTALLED-OWN or SETTING-OWN, c2 PROGRAM-OWN or SETTING-OWN (S8.2-9, S8.2-22 against S8.2-11, S8.2-13). What differs in the declaration: nothing; every reading requires a line of its own.
- Signs: both signs (both answer yes to the first question, yes to the second).

## Family 9: package contents held in an installer's cache — outcome 0

- Objects: 6 AGREED UNKNOWN; `developer-880c223d…` (bun cache links) and `developer-95ffe3a0…` (retained gem archive) FACT-UNKNOWN (unchangedness since receipt; for the gem also a reading question, `S2/QUESTIONS.md` item 6); `developer-28b0928f32a3bd540164f5c2`, `developer-4bc7e8a9213ac909292c2e0a`, `developer-9e6d06f152c07e5c13f841e0` (Go module cache) GAP.
- Deciding facts known: the modules were placed by `go mod download` and `go build` into a cache removed only as a whole, so S8.1-6 “Package—what an installer installs and removes as a whole” does not fit a module and question 1 is no; Go source is input to compilation.
- Sentences: S8.2-9 against S8.2-23 (quoted under family 4).
- Two decisions: PROGRAM (own line) or PROGRAM RECORD (no line). What differs: under the first the declaration must contain a line for the cached source; under the second, nothing. Question: `S2/QUESTIONS.md` item 2.
- Signs: both signs (both answer no to the first question, yes to the second).

## Family 10: code that an installed program copies or generates as it runs — outcome 0

- Objects: 5 AGREED UNKNOWN; `developer-3bcbeded8b7cf5aedc1382fb` (the sample hook copied from the Git template) AGREED GAP; `server-be5afc83ca654a448cd1fb60` (the k3s network-tool links) GAP.
- Hook, two decisions found by both parties: S8.2-7 “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?” read as following the unchanged bytes into the copy (INSTALLED-PACKAGE, covered by the git-core line) or not (PROGRAM, S8.2-16, own line or template-copy line). What differs: under the second the declaration must cover the copy by a line of its own or a copy line. Signs: not both (c1 answers yes to the first question, c2 no).
- Links: the producer is “k3s startup” ((not published: direct evidence at least 2 MB)), so question 1 is no; the links are the names through which the network setup starts the tool. S8.2-9 against S8.2-23 (quoted under family 4). Two decisions: PROGRAM (k3s line or own lines) or PROGRAM RECORD (nothing). Question: `S2/QUESTIONS.md` item 3. Signs: both signs (both answer yes to the first question, with different lines; yes to the second).

## Family 11: values the computer obeys that a program generated rather than a person chose — outcome ?

- Objects: 6 AGREED UNKNOWN; `developer-70be1c32…` (firewall forwarding policy: writer unknown) and `server-ddd20eb8…` (node password file: stored contents unknown) FACT-UNKNOWN.
- Sentences: S8.2-11 “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”; S8.2-15; S8.2-17.

## Family 12: value files whose entries include commands that are run — outcome 0

- Objects: `server-c354536d6d9a738329571706` (cron file) AGREED GAP; `developer-d916e8927ebf41371ab8dd1d` (Dockerfile) and `developer-e56b4f802a20335d455ecb3a` (lefthook.yml) GAP, the same gap found by both parties.
- Sentences: S8.2-23 “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.” Both halves fit; S8.2-14 or S8.2-13 then makes the value reading a setting.
- Two decisions: PROGRAM or SETTING. What differs in the declaration: nothing; both require a line of its own.
- Signs: cron file both signs (both yes, yes); Dockerfile and lefthook.yml not both (c1 answers yes to the first question, c2 no).

## Family 13: a browser's home page and “launches something” — outcome ?

- Objects: `s2-2` AGREED UNKNOWN; `s2-1` FACT-UNKNOWN: no instance observed on a computer.
- Sentence: S8.2-3 “The rule applies to objects that are on the computer.” With presence unknown, whether the rule applies is undetermined.

## Family 14: a compiler or a build tool as a built-in tool or as general-purpose work — outcome ?

- Objects: `s2-4` AGREED UNKNOWN; the other 16 (`s2-3`, `s2-5` … `s2-19`) FACT-UNKNOWN: observed presence unknown (S8.2-3), plus a second named fact per object.

## Family 15: saved history as values read or as executable statements — outcome ?

- Objects: `s2-20`, `s2-21` FACT-UNKNOWN: observed presence and whole-file executability unknown (S8.2-3).
