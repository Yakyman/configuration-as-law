WEIGHTS: 3 gaps in the idea, 1 gaps in the wording, 0 decided on the second reading
Under PROTOCOL.md: no — the cases with a known decision did not all receive their decisions (W0/RESULT.md); the weights below are outside the published order and are reported as such

Written 2026-11-23 13:50 UTC by the third party of the weighting, which took no part in `W2/m1/` or `W2/m2/`. Gate: (not published: orchestration or scratch) exists (its content: `CALIBRATION: FAILED 2 of 8`); (not published: orchestration) does not.

Sources: `PROTOCOL.md`; `TEXT.md` Sections 8 and 9.2 with `SENTENCES.md`; `W2/GAPS.md` (4 gaps); `W2/OBJECTS.tsv` (16 objects); `W2/UNMATCHED.md`; `W2/m1/objects.tsv` (party 1, 16 rows); `W2/m2/objects.tsv` (party 2, 16 rows); `A3/RESULT.md` (the source of all four gaps: the three lived-in machines “developer”, “gaming”, “server”) with its scope ledger `A3/fix-a3-h-2/gap-scope.tsv`.

No outcome and no verdict of the source is changed here. All four gaps stand in `A3/RESULT.md` as confirmed gaps, whatever weight they receive below. `A3/RESULT.md` is an investigation beyond the plan and assigns no outcome of a check.

## 1. Summary

| Gap | Title in the source | Objects | Party 1 | Party 2 | Second reading | Same answer about the meaning | Both: can be met | Weight |
|---|---|---|---|---|---|---|---|---|
| G1 | Fetched repository history fits both branches of question four | 7 (developer) | no sentence decides (7 of 7) | decides both ways (7 of 7) | no party decided by a sentence; confirmed for weighting | yes: “no” and “no” | yes | **wording** |
| G2 | Program-generated values versus the person-chosen condition | 2 (developer) | no sentence decides (2 of 2) | decided by a sentence (2 of 2) | checked in Section 5: the sentence does not decide unambiguously; confirmed for weighting | no: both “yes”, by different lines | yes | **idea** (first sign) |
| G3 | Value files whose entries include executed commands | 3 (2 developer, 1 server) | no sentence decides (3 of 3) | decides both ways (3 of 3) | no party decided by a sentence; confirmed for weighting | no: “yes” against “no” for 2 of 3 objects | yes | **idea** (first sign) |
| G4 | Container-image deployment and the installer definition | 4 (1 developer, 3 server) | no sentence decides (4 of 4) | decides both ways (4 of 4) | no party decided by a sentence; confirmed for weighting | no: both “yes”, by different lines | yes | **idea** (first sign) |

The second sign failed nowhere: for all 16 objects both parties said that the requirement of their answer can be met without forbidding an ordinary action of Section 9.2. No ordinary action would have to be forbidden under any answer given.

The gaming machine has no object in any of the four gaps.

## 2. What the weights rest on

**How “the same answer” was compared.** Each party was asked the question of the first sign in the form of its task: must this be in the declaration — yes, by a line of its own; yes, covered by another line (and which); or no. The answers were compared whole: two answers are the same only if they agree on yes or no and, for yes, on the line. For G2 and G4 both parties answered “yes” and named different lines, so a declaration that meets the answer of one party does not meet the answer of the other, and the second sign has no single requirement to be tested against. These two gaps are therefore weighed as gaps in the idea. Under the other reading, in which only yes or no is compared, G2 and G4 would be gaps in the wording and the first line would read 1 gap in the idea and 3 in the wording. `PROTOCOL.md` Section 2 does not say which comparison is meant; the question is written in `W2/QUESTIONS.md`. G1 and G3 have the same weight under both readings.

**Limits of this weighting.**

- The calibration failed (line 2). Nothing below is a weight under the published order.
- `W2/OBJECTS.tsv` carries the titles of the gaps in its `source` column, and both parties read that file. Party 1 states in `W2/m1/QUESTIONS.md` that independence from the titles cannot be claimed. `PROTOCOL.md` Section 3 requires that the second party decide without seeing the arguments of the first; the titles state the claims in short form.
- Party 1 marked all 16 objects `none-decides` and wrote in every row that this denotes a missing fact, not an accepted gap of the text: for G1 who created or brought the members, for G2 who created the two files, for G3 the contents of the files, for G4 the documentation of the container engine. The source addresses each of these: the action log of the clone (G1), the documentation of the container engine together with its own statement that the origin is inferred and not established by the inventory (G2), the contents recovered from the committed action inputs with matching checksums (G3), the documentation lookup (G4). Party 1 named no sentence that decides any object, so by the task its rows do not open a second reading. Party 1 answered the question about the meaning for all 16 objects, with the remark that its answers address the roles of the objects and do not assert the missing facts.
- The counts are rows of the inventories, including directory groups, not single files. For G2 the source calls its count a lower bound.

## 3. The gaps in the idea

### G2. An access rule that a program wrote by itself, without a person choosing it

**What kind of object.** A firewall keeps its rules as files in its configuration folder. When the container engine is started on such a machine, it adds a zone and a forwarding policy of its own to that folder, so that the traffic of its containers is let through. Nobody typed these rules and nobody chose their values, yet the whole computer obeys them from then on.

**Two real examples.**

- Machine “developer”, `/etc/firewalld/zones`, member `docker.xml` (object `developer-24c8232c52212725d6ea3882`).
- Machine “developer”, `/etc/firewalld/policies`, member `docker-forwarding.xml` (object `developer-70be1c323890746c1a78c6f5`).

**What the text says.** The question that makes an object a setting asks for a value chosen by a person; the list that follows it names access rules among the settings without that condition; and what a program writes as it runs is a program record.

- S8.2-11 «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»
- S8.2-13 «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»
- S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»
- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»
- S8.2-17 «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»

The source finds two decisions: a setting, which needs a line of its own, or a program record, which needs no line.

**What the two parties answered about the meaning.**

| | Must this be in the declaration? | Can it be met without forbidding an ordinary action? |
|---|---|---|
| Party 1 | “yes, by a line of its own specifying the effective firewall policy represented here; an inactive backup needs no separate line.” | “yes; a system can record the effective firewall policy when configuring networking or containers while still allowing every Section 9.2 action.” |
| Party 2 | “yes, covered by another line: the line of the docker package with its enabled service, which creates this zone/policy whenever it starts with firewalld” | “yes: the system regenerates them from the recorded docker line; installing, enabling and running containers stay allowed” |

**Which sign failed: the first.** Both parties say the rule belongs in the declaration, and they differ on what the declaration must contain. For party 1 the firewall policy itself must be written as a line. For party 2 no such line is needed: the line of the container engine is enough, because the engine writes the rule again at every start. A declaration with only the line of the container engine meets the answer of party 2 and does not meet the answer of party 1. The second sign did not fail: neither party names an ordinary action that would have to be forbidden.

**How many objects.** 2 objects of the machine “developer”; 0 of “gaming”; 0 of “server”. The source states this as a lower bound: 23 further candidate rows of its scope ledger (3 developer, 1 gaming, 19 server) have unknown facts and are not counted.

### G3. A file of values in which some entries are commands that get executed

**What kind of object.** A file that a program reads as a list of values, where one of the values is a command line that the program later hands over for execution. A system timetable of jobs is such a file: the fields for minute and hour are values, the last field is a command. A file that tells a tool what to run before a commit, or how to build and start a container, is of the same kind. The file is not run as a program from its first line to its last, and it is not only read either.

**Real examples.**

- Machine “server”, `/etc/cron.d`, member `cal-maintenance`: a schedule line whose last field is a shell command (object `server-c354536d6d9a738329571706`).
- Machine “developer”, `/home/user/Projects/scc`, member `lefthook.yml` with the entry `run: git diff --cached --check` (object `developer-e56b4f802a20335d455ecb3a`).
- Machine “developer”, `/home/user/Projects/development-web`, member `Dockerfile` with a `CMD` entry (object `developer-d916e8927ebf41371ab8dd1d`).

**What the text says.** The text separates a file that is executed as code from a file that is only read as values, and has no word for a file of which a part is executed.

- S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

The source finds two decisions, a program or a setting, and notes that both must be recorded. Party 2 finds a third decision for the two files in the project folders: material that a person created or brought, which need not be recorded, by the second half of this sentence:

- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»

**What the two parties answered about the meaning.**

| Object | Party 1 | Party 2 |
|---|---|---|
| The schedule file `cal-maintenance` | “yes, by a line of its own specifying the maintenance schedule and command.” | “yes, by a line of its own: a system-wide scheduled job chosen by a person” |
| The project folder with `lefthook.yml` | “yes, by lines of their own for executable programs and launch instructions in the group; documents and non-executable project material need no lines.” | “no as a whole: a fetched project with its own build, hook and CI files and its build output is the person's material; the hook installed into .git/hooks is a separate object” |
| The project folder with the `Dockerfile` | “yes, by a line of its own for the Dockerfile build/launch instructions; the static page needs no line of its own.” | “no: the project files are the person's material; what they produced (the image and the running container) is what the declaration must describe” |

**Which sign failed: the first.** The parties agree on the system schedule file and give opposite answers for the two files in a person's project folders: party 1 holds that an instruction which launches something must be in the declaration wherever it lies; party 2 holds that it is part of the person's project and that only what it produces belongs in the declaration. The second sign did not fail: for all three objects both parties say their requirement can be met without forbidding an ordinary action.

**How many objects.** 3 objects: 2 of the machine “developer”, 1 of “server”, 0 of “gaming”. Ten further developer rows with file names of this kind have unknown contents or facts in the source and are not counted.

### G4. A container image stored by the container engine

**What kind of object.** An image is an archive with a ready-made program and everything it needs. The container engine downloads it, or builds it from a recipe, stores it, starts containers from it and can remove it again as a whole. On the machines the images lie in the store of the engine; each had one container made from it.

**Real examples.**

- Machine “server”, image `caddy:2-alpine` (object `server-fc8e0ac75ce9ed64a08ff655`), downloaded.
- Machine “developer”, image `cal-development-web:local` (object `developer-78e8326714450972e0134fb6`), built on the machine from a person's recipe.
- Also on the machine “server”: `postgres:17-alpine` and `traefik/whoami:v1.11.0`.

**What the text says.** A package is what an installer installs and removes as a whole, and an installer is known by its documented purpose of installing and removing programs. The text does not say whether downloading, storing and removing images is that. If it is, the image is a package and an installed object by the first question, with everything in it. If it is not, only the executable part of the image is a program by the second question, and the rest of its contents are decided one by one.

- S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-5 «A general-purpose program with a built-in installer counts as an installer in that part of its functionality.»
- S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-22 «A program that runs as its own process on the computer, including in a container, is a program.»
- S8.2-16 «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»

**What the two parties answered about the meaning.**

| | Must this be in the declaration? | Can it be met without forbidding an ordinary action? |
|---|---|---|
| Party 1 (all four images) | “yes, by a line of its own identifying the caddy:2-alpine image and required version/content.” (the same wording for each image, with its name) | “yes; a system can record the image reference when obtaining or building it and still permit container execution and all other Section 9.2 actions.” |
| Party 2 (the three downloaded images) | “yes, covered by another line: the line declaring the container (on the server, the compose stack) that names this image” | “yes: running a container stays allowed if the container tool adds the container and its image to the declaration, as P4 already requires of installation tools” |
| Party 2 (the image built on the machine) | “yes, covered by another line: the line declaring the container cal-development-web, which names the image and its build recipe” | the same |

**Which sign failed: the first.** Both parties say the image belongs in the declaration, and both would have it named there. They differ on what is recorded: for party 1 the image is a recorded thing in its own right, with a line of its own that fixes its version or content; for party 2 the recorded thing is the container, and the image has no line of its own but is obtained by the line of the container, for the built image together with its recipe. The two answers require different declarations: an image line without a container line meets the first and not the second, and they part again when the line of the container is removed. This is the closest of the three differences; under the comparison by yes or no alone (Section 2) this gap would be a gap in the wording. The second sign did not fail.

**How many objects.** 4 objects: 1 of the machine “developer”, 3 of “server”, 0 of “gaming”. Seven further rows of the source (stores of the engine whose members were not expanded: 2 developer, 5 server) have unknown facts and are not counted.

## 4. The gaps in the wording

| Gap | Kind of object | The common answer about the meaning | The sentences that come closest | Objects |
|---|---|---|---|---|
| G1 | The history that the version-control program stores next to a project a person fetched: the `.git` folder of the project `scc` with its packed objects and its references (for example `/home/user/Projects/scc/.git/objects/pack` and `/home/user/Projects/scc/.git/refs` on the machine “developer”). The program wrote these files as it ran, and the person brought them by fetching the project, so both halves of the fourth question fit and the text does not say which class the object has. | No, it need not be in the declaration: it is neither installed nor a setting. Both parties add that this answer does not cover an executable hook inside the folder, which is a separate object. Both say the requirement can be met: nothing has to be recorded, so nothing has to be forbidden. | S8.2-15 and S8.2-2, quoted below | 7 (developer 7, gaming 0, server 0) |

- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»
- S8.2-2 «The rest need not be recorded.»

The answers of the parties, for six of the seven objects word for word: party 1, “no; repository history, references and bookkeeping as such need no declaration line.”; party 2, “no: fetched history and git's own bookkeeping of a person's project are neither installed nor a setting of the computer”. For the seventh, the `.git` folder itself: party 1, “no; the repository-metadata group needs no line as such; independently executable hooks or launch/access settings require their respective program or setting lines.”; party 2, “no for the history and bookkeeping; the executable hook under hooks/ (written by lefthook install) is a separate code object and is not answered here”. The source excludes the executable hooks from this gap as well.

The parties differ on why the text gives no class: party 2 says both halves of the sentence fit and nothing orders them, as the source does; party 1 says the inventory does not show who created or brought the files. The source rests the provenance on the saved log of the action that fetched the project. Whether the object must be recorded is the same under both classes, as the source notes; what stays open is the class, which Section 9.2 asks for as well.

## 5. The gaps decided on the second reading

None.

One gap, G2, was decided by a party: party 2 decided both of its objects by a sentence. The check follows.

**The sentences named by party 2.** S8.2-11, with S8.2-6 and S8.2-15: the rule was chosen by the container engine and not by a person, so the third question is answered “no”; the fourth question then makes it a program record, which need not be recorded. Of the list of settings that names access rules, party 2 says that it is the consequence of an affirmative answer to the third question and that the order of the questions decides.

- S8.2-6 «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»
- S8.2-11 «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»
- S8.2-13 «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»

**The argument of the source.** The rule is not a value chosen by a person, but S8.2-13 calls access rules settings; to make S8.2-13 depend on the condition of S8.2-11 is a choice between two readings that the text does not make.

**The check.** The decision of party 2 holds only if S8.2-13 applies solely to objects for which S8.2-11 has already been answered “yes”. That restriction is not in the text.

1. S8.2-13 has no condition in its words. It says what settings are and names access rules. A firewall zone that lets traffic through is an access rule and fits the sentence as it stands. To take the zone out of it, the words “chosen by a person” have to be added to it.
2. S8.2-6 fixes the order of the four questions and says that the clarifications do not change it. It does not say that, within the third numbered question, only the interrogative sentence decides and the sentences after it merely describe its affirmative answer.
3. The text itself shows that the sentences after the interrogative one do more than that. A value obeyed only by a program that a person runs for himself or herself gets the answer “no” to S8.2-11, by the words of that question; the sentence below nevertheless makes such a value a setting when it launches something or grants access. So “setting” is not confined to an affirmative answer to S8.2-11, and the same may hold for S8.2-13.

- S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

Both readings are therefore open: the rule is a program record that need not be recorded, or a setting that must be recorded by a line of its own. The named sentence does not decide the two objects unambiguously without an added word. **G2 is confirmed for weighting**; this agrees with the source, and there is no disagreement with the source to report. No choice between the two readings is made here.

Two further observations on the same rows. Party 2, having decided by the text that the rule need not be recorded, answered the question about the meaning with “yes”: by the meaning it belongs in the declaration, covered by the line of the container engine. And in the row of `/etc/firewalld/zones` party 2 left the two other members of the folder (`FedoraWorkstation.xml` and its `.old` copy) as an unknown fact; the gap of the source rests only on the member `docker.xml`.

## 6. The three decisions for each gap

`PROTOCOL.md` Section 3: all three decisions are published. The party that puts the gaps forward is the source, `A3/RESULT.md`.

| Gap | The source (puts the gap forward) | Party 1 (`W2/m1/objects.tsv`) | Party 2 (`W2/m2/objects.tsv`) | Third party |
|---|---|---|---|---|
| G1 | Gap: both halves of the fourth question fit; program record or material; neither needs a line | No sentence decides; held to be a missing fact (who created or brought the members) | Decides both ways, by the two halves of S8.2-15; not recorded under either | Confirmed for weighting; gap in the wording |
| G2 | Gap: setting with a line of its own, or program record without a line | No sentence decides; held to be a missing fact (who created the files) | Decided: program record, need not be recorded (S8.2-11, S8.2-6, S8.2-15) | The named sentence does not decide unambiguously (Section 5); confirmed for weighting; gap in the idea |
| G3 | Gap: program or setting; both recorded | No sentence decides; held to be a missing fact (contents of the files) | Decides both ways: program or setting for the schedule file; program, setting or material for the two project files | Confirmed for weighting; gap in the idea |
| G4 | Gap: the image is a package, or it is not and its contents are decided one by one | No sentence decides; held to be a missing fact (documentation of the engine; whether the host is installed as this image) | Decides both ways: installed object or program; a line of its own under both | Confirmed for weighting; gap in the idea |

## 7. Cards not weighted

`W2/UNMATCHED.md` reads: “Unmatched cards: 0.” No card of the source was left without an object of a real inventory, so no card is listed as not weighted.

## 8. The ordinary actions against which the second sign was read

Section 9.2, quote: «installing a program with the package manager and as an application package; installing a program in the home directory with a programming language package manager; installing a browser extension; changing a setting of a program that a person runs for himself or herself; enabling a user service; connecting to a network; a user script in the home directory; running a container»

The third party did not test the second sign itself; as the task states the rule, it records what both parties said. All 32 answers are “yes”.
