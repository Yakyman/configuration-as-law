WEIGHTS: 2 gaps in the idea, 3 gaps in the wording, 1 decided on the second reading
Under PROTOCOL.md: no — the cases with a known decision did not all receive their decisions (W0/RESULT.md); the weights below are outside the published order and are reported as such

# W1 — weighting of the gaps: the third party and the result

Written 2026-11-23 13:43 UTC by the third party of the weighting. The third party took no part in the work of party 1
(`W1/m1/`) or of party 2 (`W1/m2/`).

Read for this result: `PROTOCOL.md` (whole); `TEXT.md` Section 8 and Section 9.2 with `SENTENCES.md`; `W1/GAPS.md`,
`W1/OBJECTS.tsv`, `W1/UNMATCHED.md`; `W1/m1/objects.tsv` and `W1/m2/objects.tsv` (28 rows each); the sources of the
gaps: `D1/RESULT.md`, `A2/VERIFY.md` with `A2/CARDS.md`, `B1/fix-b1-1/GAPS.md` with `B1/RESULT.md` and
`B1/REVIEW-B1-2.md`; `W0/RESULT.md` for the second line above; and, to check the facts stated below about members of
directories, the member lists that `W1/OBJECTS.tsv` names ((not published: record outside selected evidence), (not published: record outside selected evidence)).
Nothing was run on any machine and no inventory was taken or repeated.

**No outcome and no verdict of a source is changed by this file.** `PROTOCOL.md`, Section 1: "any object for which
the text of Sections 8.1 and 8.2 does not allow deciding, or allows deciding both ways, gives check 1 the outcome 0,
whatever weight it is assigned below." Every gap below stands in its source with the outcome it has there.

**Under what this weighting runs.** (not published: orchestration or scratch) exists (its content: "CALIBRATION: FAILED 2 of 8");
(not published: orchestration) does not exist. `PROTOCOL.md`, Section 4: "If even one of them receives a different decision,
weighting does not begin, and the discrepancy is published." The weights below were nevertheless computed, by the two
signs of Section 2 exactly as written, and they are outside the published order.

## 1. Overview

28 rows of `W1/OBJECTS.tsv`, 26 distinct objects (the two objects of G3 are also the two objects of G4). The answers of
the two parties are placed side by side, without any judgement, in `W1/j/compare.tsv` (made by `W1/j/compare.py`); the
columns "same answer" and "result" below are the reading of the third party.

| Gap | Source and its title | Objects | Party 1 decided by a sentence | Party 2 decided by a sentence | Second reading | Same answer about the meaning | Both said: can be met | Result |
|---|---|---:|---:|---:|---|---|---|---|
| G1 | `D1/RESULT.md`, card 2 — A list the system generated from installed packages | 10 | 0 of 10 | 5 of 10 | no party decided every object: confirmed for weighting | no: same on 8, different on 2 | yes, 10 of 10 | **gap in the idea** — the first sign failed |
| G2 | `D1/RESULT.md`, card 4 — A stored archive whose contents are executed | 9 | 0 of 9 | 0 of 9 | confirmed for weighting | no: same on 7, different on 2 | yes, 9 of 9 | **gap in the idea** — the first sign failed |
| G3 | `D1/RESULT.md`, card 5 — An installed package whose code runs only inside its program | 2 | 2 of 2 | 0 of 2 | party 1's sentence checked: it does not decide without an added word; confirmed for weighting | yes, 2 of 2 | yes, 2 of 2 | **gap in the wording** |
| G4 | `A2/VERIFY.md`, candidate N1 — Must restricted code installed inside a recorded program be recorded? | 2 (the same two as G3) | 2 of 2 | 0 of 2 | as G3 | yes, 2 of 2 | yes, 2 of 2 | **gap in the wording** |
| G5 | `B1/fix-b1-1/GAPS.md` — Compiler and build-tool purpose versus general-purpose work | 3 | 3 of 3 | 3 of 3 | **decided on the second reading** | (yes, 3 of 3) | (yes, 3 of 3) | not weighted |
| G6 | `B1/fix-b1-1/GAPS.md` — Saved history: values read versus executable statements | 2 | 0 of 2 | 0 of 2 | confirmed for weighting | yes, 2 of 2, for the history file | yes, 2 of 2 | **gap in the wording** |

The two signs (`PROTOCOL.md`, Section 2). First: "two parties, asked separately 'must this be in the declaration, if
the declaration describes everything installed and every setting', give the same answer." Second: "a system can meet
this requirement without forbidding any ordinary action from the list in Section 9.2." A gap in the wording needs both;
everything else is a gap in the idea. Each party answered the first question in one of three forms: yes, by a line of
its own; yes, covered by another line (named); no. Two answers are counted as the same when the form is the same and the
named lines agree in substance.

The ordinary actions of Section 9.2, quote: «installing a program with the package manager and as an application package; installing a program in the home directory with a programming language package manager; installing a browser extension; changing a setting of a program that a person runs for himself or herself; enabling a user service; connecting to a network; a user script in the home directory; running a container».
For all 28 rows both parties answered that the requirement of their own answer can be met without forbidding any of
them. The second sign therefore failed nowhere; no ordinary action would have to be forbidden in any gap.

## 2. The gaps in the idea

### G1 — A list the system generated from installed packages

**Source and its outcome.** `D1/RESULT.md`, card 2: CONFIRMED there; it stands unchanged.

**What kind of object this is.** A file that no package delivers and no person wrote. The system itself computes it
from the packages that are installed: an index of what is installed, a table compiled from many small files, a look-up
cache. When packages change, the system computes it again.

**Two real examples.**

- AlmaLinux machine, `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64`: the directory of one kernel, 29 members. Ten of
  them are the `modules.*` index files (`modules.dep`, `modules.alias` and others) that the system builds from the
  installed kernel modules and then follows when it loads a driver; the source counts the other 19 members as
  unchanged parts of the kernel packages, and they are not in the gap.
- openSUSE MicroOS machine, `/usr/share/mime`: 25 members, the database of file types that the system compiles from the
  definitions delivered by installed packages.

**The sentences involved.** The source reads the text in two ways and finds no sentence that chooses.

- S8.2-15: «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.» Read this way, the generated file is a program record.
- S8.2-2: «The rest need not be recorded.» A program record need not be recorded.
- S8.2-16: «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.» This sentence names a generated list among what is installed.
- S8.2-1: «Everything that is installed and every setting must be recorded.» What is installed must be recorded.
- S8.2-6: «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.» The source: this orders the four questions and does not rank the paragraph about lines against the fourth question.

**The second reading.** Party 1 decided none of the ten objects by a sentence: for each it wrote that no sentence
decides and named the facts the inventory does not hold. Party 2 decided five by a sentence and found the other five
decided both ways. No party decided every object, so the gap is confirmed for weighting. For the record, the five
decisions of party 2: the manual-page index, the auxiliary cache of the library loader and the empty application index
are program records by the fourth question (S8.2-15) and need not be recorded; the boot-loader modules are programs by
the second question, covered by the line of the package they were copied from; the directory of the earlier snapshot is
decided member by member. In the three program-record decisions party 2 followed one of the two readings of the source
and named no sentence that sets aside the words "a generated list" of S8.2-16.

**What the two parties answered about the meaning** ("must this be in the declaration, if the declaration describes
everything installed and every setting").

| Machine | Object | Party 1 | Party 2 | Same |
|---|---|---|---|---|
| AlmaLinux | `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64` (kernel directory with the module index) | yes, covered by another line: the kernel and module package and build lines | yes, covered by another line: the line of the kernel package from which the system generates the index | yes |
| MicroOS | `/usr/share/mime` (file-type database) | yes, covered by another line: the line that generates the database and the definitions it takes as inputs | yes, covered by another line: the line of the package whose definitions are compiled | yes |
| Void | `/usr/share/mime/application` (505 file-type files) | yes, covered by another line: the definition lines and the line generating the database | yes, covered by another line: the line of the package whose definitions are compiled | yes |
| AlmaLinux | `/usr/share/applications` (`mimeinfo.cache`, 6,218 bytes: which application opens which file type) | yes, covered by another line: the index generation line and the application lines it uses | yes, covered by another line: the lines of the packages whose entries it indexes | yes |
| AlmaLinux | `/usr/share/glib-2.0/schemas` (`gschemas.compiled`: compiled default values) | yes, covered by another line: the schema package lines and the line compiling them | yes, covered by another line: the lines of the packages whose schemas it compiles | yes |
| AlmaLinux | `/boot/grub2/i386-pc` (300 boot-loader files) | yes, covered by another line: the boot-loader installation line | yes, covered by another line: the line of the boot-loader package they were copied from | yes |
| AlmaLinux | `/var/cache/man/id` (manual-page index) | no | no | yes |
| Void | `/var/cache/ldconfig` (auxiliary cache of the library loader) | no | no | yes |
| AlmaLinux | `/usr/local/share/applications` (`mimeinfo.cache`, 13 bytes: the same kind of index, empty) | yes, covered by another line: the index generation line and the application lines it uses | no | **no** |
| MicroOS | `/.snapshots/1/snapshot/etc` (the configuration directory of an earlier snapshot, 104 members, among them the generated `ld.so.cache`) | yes, covered by another line: the lines of the recorded generation; "copied cache/log state needs no extra line" | "no: a retained previous generation, not what is installed or set now" | **no** |

In plain words. Both parties hold that an index which the computer then follows — the module index, the file-type
database, the application index, the compiled defaults — must be in the declaration, covered by the lines of the
packages it is built from. Both hold that a pure look-up cache — the manual-page index, the loader's auxiliary cache —
need not be there. So even where they agree, "a generated list" has no single answer: it depends on which list. And
they place the border differently. For the empty application index party 1 answers as for the full one (covered),
party 2 answers no, because the 13 bytes hold only a header and "no value anyone chose". For the copy kept in an
earlier snapshot party 1 answers that the lines of that generation cover it, party 2 that an earlier generation is not
what is installed or set now.

**Which sign failed.** The first: the two parties did not give the same answer for the objects of the gap (same on 8
of 10, different on 2). It fails already on `/usr/local/share/applications`, where the whole object is one generated
list. In the snapshot row the parties answered for the directory as a whole; neither gave a separate answer for its
generated member. The second sign held: both parties said for all ten objects that the requirement can be met without
forbidding an ordinary action; no ordinary action would have to be forbidden.

**How many objects.** Weighed here: 10 example objects (AlmaLinux 6, MicroOS 2, Void 2). In the source the gap covers
100 inventory rows: AlmaLinux 38, Void 28, MicroOS 34, Talos 0; Gentoo gave no inventory.

### G2 — A stored archive whose contents are executed

**Source and its outcome.** `D1/RESULT.md`, card 4: CONFIRMED there; it stands unchanged.

**What kind of object this is.** One stored file that is an archive. At every start the computer unpacks it into
memory and runs the programs that are inside it. The file itself is not marked as executable, and no package delivers
its bytes: a tool of the system builds it when a kernel is installed, from the installed programs and some settings.

**Two real examples.**

- AlmaLinux machine, `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64.img` (59,821,955 bytes, mode 0600, not executable).
- Void Linux machine, `/boot/initramfs-6.18.64_1.img` (28,850,351 bytes, mode 0600, not executable).

**The sentences involved.** The source finds that the text does not say whether the stored archive is itself code.

- S8.2-9: «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?» Read as yes — the computer executes what is in the file — the archive is a program.
- S8.2-10: «Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.» Then it must be recorded, by the line it was built from (S8.2-16, quoted under G1).
- S8.2-23: «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.» Read the other way — the file is unpacked, not executed — it is not code.
- S8.2-15 (quoted under G1): then it is a file a program wrote as it ran, a program record, which need not be recorded.

**The second reading.** Party 1 decided none of the nine objects by a sentence (no sentence decides; the contents of
the archives are not in the inventory). Party 2 found all nine decided both ways, by the same two readings as the
source. No party decided the objects by a sentence, so the gap is confirmed for weighting.

**What the two parties answered about the meaning.**

| Machine | Object | Party 1 | Party 2 | Same |
|---|---|---|---|---|
| AlmaLinux | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64.img` | yes, covered by another line: the line that builds the boot image, with its kernel, programs and boot settings | yes, covered by another line: the kernel and image-generator package lines and the settings it copies | yes |
| AlmaLinux | `/boot/initramfs-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20.img` | the same | the same | yes |
| AlmaLinux | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64kdump.img` | the same | the same | yes |
| AlmaLinux | `/boot` (6 members, two of them archives) | yes, covered by another line: the kernel, boot-loader and image-generation lines | yes, covered by other lines: the kernel, rescue and kdump package lines | yes |
| Void | `/boot/initramfs-6.12.118_1.img` | yes, covered by another line: the line that builds the boot image | yes, covered by another line: the kernel and image-generator package lines | yes |
| Void | `/boot/initramfs-6.18.64_1.img` | the same | the same | yes |
| Void | `/boot` (6 members, three of them archives) | yes, covered by another line: the kernel, boot-loader and image-generation lines | the archives covered by the kernel and generator package lines; the kept earlier kernel by a line of its own, or removed | yes for the archives, as this row states them |
| Void | `/boot/initramfs-6.12.11_1.img` (the archive of a kernel whose package the actions replaced by a newer one) | yes, covered by another line: the line that builds the boot image | "yes, by a line of its own or removed with its kernel: it boots a kernel whose package is no longer installed" | **no** |
| MicroOS | `/.snapshots/1/snapshot/boot` (the boot directory of an earlier snapshot, 13 members, one archive) | yes, covered by another line: the kernel, boot-loader and image-generation lines | "no: a retained previous generation" | **no** |

In plain words. For the archive of an installed kernel both parties answer the same: it must be in the declaration and
is covered by the lines of what it is built from. They part where the source of the archive is no longer there. For the
archive left behind by a replaced kernel, party 1 still answers "covered by the line that builds it"; party 2 answers
that nothing recorded builds it any more, so it needs a line of its own or must go. For the archive inside an earlier
snapshot, party 1 answers "covered", party 2 answers that an earlier generation need not be in the declaration at all.

**Which sign failed.** The first: the two parties did not give the same answer for the objects of the gap (same on 7
of 9, different on 2). Party 2's row for the Void `/boot` directory says "covered" for the three archives in it, while
its own row for one of them, `initramfs-6.12.11_1.img`, says "a line of its own"; the count above takes each row as
written. The second sign held: both parties said for all nine objects that the requirement can be met without
forbidding an ordinary action; no ordinary action would have to be forbidden.

**How many objects.** Weighed here: 9 objects (AlmaLinux 4, Void 4, MicroOS 1). These are all the rows the source
establishes for this gap: AlmaLinux 4, Void 4, MicroOS 1, Talos 0; Gentoo gave no inventory.

## 3. The gaps in the wording

| Gap | Kind of object | The common answer about the meaning | The sentences that come closest | Objects |
|---|---|---|---|---|
| G3 (`D1/RESULT.md`, card 5) | A browser extension that the browser's own add-on installation put into a person's profile: one `.xpi` file of 1,226,057 bytes in `/home/user/.mozilla/firefox/cal-check/extensions`. Its code runs only inside the browser. | Yes, by a line of its own (both parties, both objects). Both: can be met — the browser's installer adds the extension to the declaration as it installs it; installing a browser extension stays allowed. | S8.2-1 «Everything that is installed and every setting must be recorded.» against S8.2-21 «Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.»; S8.2-6 «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»; S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?» | 2: AlmaLinux 1, Void 1 (all the rows the source establishes) |
| G4 (`A2/VERIFY.md`, candidate N1) | The same kind of object. The source describes it from documentation and names no object of an inventory; the preparation matched it to the same two rows as G3. | The same: yes, by a line of its own; can be met. | The same pair: S8.2-1 against S8.2-21, with S8.2-6. | 2: the same two objects as G3 |
| G6 (`B1/fix-b1-1/GAPS.md`) | The saved command history of a shell: the file `.bash_history` in `/home/user`, a list of commands typed earlier, which the shell reads back and can run again. The inventory rows are the home directories that hold it (15 members on the developer machine, 18 on the gaming machine). | No: the history need not be in the declaration (party 1: "ordinary history, caches and material need no extra line"; party 2: "no for .bash_history"). Both add that the shell start-up files in the same directory must be there, by lines of their own. Both: can be met. | S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?» against S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»; S8.2-15, which names «a log, cache, history, working state» as a program record | 2: developer 1, gaming 1. The source names two channel rows (C7.06, C7.17) and no object of an inventory; the preparation matched these two. |

G3 and G4 are one conflict of the text, found by two sources on the same two objects. They are counted as two gaps
because `W1/GAPS.md` lists them as two.

### 3.1. The second reading of G3 and G4: the sentence of party 1 and its check

Party 1 decided both objects by a sentence: the extension is a package that the installer built into the browser
installs (S8.1-5, S8.1-6), so the first question answers yes (S8.2-7, S8.2-8), it must be recorded (S8.2-1) by a line of
its own (S8.2-16); and S8.2-6 "makes Q1 decisive before the restricted-code clarification S8.2-21". Party 2 found both
objects decided both ways: S8.2-1 against S8.2-21, with S8.2-6 fixing only the order of the questions.

The check against the argument of the sources. Neither source disputes what the object is: both accept the first
question's answer, an installed object. Their argument is about the duty. S8.2-1 says an installed object must be
recorded. S8.2-21 says that code running inside a recorded program, unable to launch programs or to change what is
installed and the computer's settings, need not be recorded. The inventory object is such code: `D1/RESULT.md`
establishes the extension and its version and that its manifest asks for none of the permissions that would let it
launch a program. Both sentences therefore apply to the same object, with opposite duties.

S8.2-6 says two things: the first affirmative answer decides «what an object is», and «the clarifications do not change this order».
S8.2-21 answers none of the four questions and names no kind of object; it does not change their order. It states a
duty. For S8.2-6 to settle the conflict it would have to say that a clarification does not lift the duty of S8.2-1 from
an installed object. It says that the order is unchanged, and nothing about the duty. The sentence of party 1 decides
what the object is; it decides whether the object must be recorded only after that word is added. By the rule of
literal reading it does not decide the objects unambiguously. `D1/RESULT.md` adds that the conflict also rests on a
border the text does not draw: whether the stored archive is itself the code that S8.2-21 speaks of (the border of G2).

Result of the second reading: the gap is confirmed for weighting, for G3 and for G4. The disagreement is reported as it
is: party 1 — no gap, decided by the first question; party 2 and both sources — decided both ways.

For orientation only: this kind of object is case 4 of `PROTOCOL.md`, Section 4, whose expected decision was "No gap:
an installed object with a line of its own". `W0/RESULT.md` records that this case did not receive its decision; it is
one of the two cases behind the second line of this file.

## 4. Decided on the second reading

### G5 — Compiler and build-tool purpose versus general-purpose work (`B1/fix-b1-1/GAPS.md`)

**The objects.** Three packages installed with the system package manager on the developer machine:
`rpm:make@4.4.1-13.fc45.x86_64`, `rpm:gcc@16.2.1-3.fc45.x86_64`, `rpm:gcc-c++@16.2.1-3.fc45.x86_64`. The inventory records
each as installed explicitly. The source names no object of an inventory; the preparation matched these three to it.

**The sentence.** Both parties, separately, decided all three objects by the same sentences and the same way:

- S8.2-7: «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?» Yes: each is a package installed on the computer.
- S8.2-8: «Then it is an installed object, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.»
- S8.2-1: «Everything that is installed and every setting must be recorded.»
- S8.2-16: «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.» Installed explicitly, not as a part of another package and not as a dependency: a line of its own.

**The check.** The first question is answered yes by the fact the inventory holds (an installed package), so the
order of S8.2-6 stops there; no word has to be added to any of the four sentences. Against the argument of the source:
the source does not dispute this. It writes that under both of its readings "unchanged packaged objects stop at Q1".
The sentences decide the three objects unambiguously: installed objects, which must be recorded, each by a line of its
own. **Decided on the second reading.**

**The disagreement, reported.** The gap still stands in its source with its outcome: the five channel rows C5.1–C5.5
remain decided both ways there, and nothing here changes that. The source's question is a different one from the
question the second reading answers. The source asks what the tool is when it works: whether compiling and building
make it a built-in tool — S8.1-7: «Built-in tool—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.» —
or leave it a general-purpose program — S8.1-8: «General-purpose programs—an editor, file copying, link creation, the command shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.»
On that depends whether the tool itself has the duty of S8.3-7: «Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.»
The sentences named by the parties say what the three packages are and how they are recorded. They say nothing about
which of the two the tool is. The second reading therefore removes the gap for these inventory objects and leaves the
source's two readings where they were.

For the record, the answers of the parties to the question about the meaning for these objects: both — yes, by a line
of its own; both — can be met. No weight is assigned, because the gap was decided on the second reading; the question
about the meaning was asked about the packages and not about the duty of the tool.

## 5. Cards not weighted

From `W1/UNMATCHED.md`:

- `B1/fix-b1-1/GAPS.md` — Home-page navigation and launching something: no object of a real inventory; not weighted
  (`PROTOCOL.md`, Section 3: "Invented cases are not accepted.").

## 6. Limits of this result

- The calibration did not pass (`W0/RESULT.md`: 2 of 8 cases received a different decision). By `PROTOCOL.md`, Section 4,
  weighting was not to begin. Every weight above is outside the published order.
- A weight is not an outcome. The outcomes of check 1 and the verdicts of the three sources are as their own files
  state them.
- Several objects are directories with many members, and each party answered once per row. Where the source confines
  the gap to some members (the module index inside the kernel directory, the archives inside `/boot`, the history file
  inside the home directory), the answers were compared as far as they speak about those members; the tables give the
  answers of the whole row.
- Party 1 wrote for every object of G1, G2 and G6 that a fact needed for the decision by the text is not in the
  inventory, and answered the question about the meaning all the same, as its task required. Its answers about the
  meaning are therefore answers about the kind of object the row names, not findings about the stored bytes.
- G1 was weighed on 10 example objects out of the 100 rows of its source; G4, G5 and G6 on objects that the
  preparation matched to cards which name no inventory object themselves.
- The counts of "same answer" are a reading of free-text answers by the third party. Both full answers of every row
  are in `W1/j/compare.tsv`, `W1/m1/objects.tsv` and `W1/m2/objects.tsv`.
- Questions that only the author can decide, met while weighing, are in `W1/QUESTIONS.md`.
