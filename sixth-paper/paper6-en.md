# “Configuration as Law”: A Declarative Operating System Built from Its Definition. Results of the Reference Implementation, and Version 5

Arthur Yakymenko

Preprint · 25 November 2026 · Part I reports the check fixed in the fifth paper; Part II is formulated after the
results

## Abstract

The fifth paper [5] fixed one check of version 4 of the “Configuration as Law” hypothesis: a reference
implementation, ConfOS, built from the text as its specification. Part I reports the results strictly under that plan.
ConfOS was built by one party and checked by another, with programs of its own. In the
third complete run, 124 cases gave 458 rows, and no row fails; a search for ways past the declaration made 240
attempts, and none passed; nine actions of ordinary work were performed, and the two that the plan requires on real
radio hardware were performed only on simulated radio. By the letter of the plan, no part receives outcome 0 and
none receives 1: every part yields ?, and no reason for it is a failing row. Part II is formulated after the results.
We conclude that the statement that was our hypothesis—such a system can be built, and ordinary work is
possible in it—is confirmed by construction. From this paper on, we speak of a definition of a declarative
operating system and of a result: the definition is realizable. We set out version 5, a rewording of version 4
around one sentence—the declaration is the law of the computer: what is written in it is what is on the
computer—relate its statements to the cases of the run, and plan a reference implementation with a base of its own.

Keywords: declarative configuration, configuration management, operating systems, reference implementation, check
conditions fixed in advance.

## Introduction

We investigate the question: what is a declarative operating system, and what properties must it have?

The first four papers [1–4] set out four versions of the “Configuration as Law” hypothesis and their checks under
conditions fixed in advance; [5], Table 1, lists them. The fifth paper left version 4 unchanged, withdrew the check
of its wording, and fixed the check that this paper reports.

The earlier papers speak of a hypothesis. That word joined two things: a definition, which is a choice of the
meaning of a word [4, Section 6.4] and is not proven, and a statement that can be checked—a system that meets the
definition can be built and used for ordinary work [3, Section 4.3; 5, Section 7.1]. From this paper on, we call
the first the definition and the second, now checked, the result. Versions 1–4 keep the name under which they were
published.

# Part I. Results under the plan of the fifth paper

## 1. The outcome on one page

**What was claimed.** The plan states what is checked: “Whether a system with the three properties of version 4 can
be built and used for ordinary work, and whether the three consequences hold on it.” [5, Section 9.1]

**What was built.** ConfOS: a small operating system in a virtual machine, assembled from packages of Debian 13,
with Section 8 of [4] as its specification.

**What came out.** In the third complete run, 124 cases gave 458 rows, and no row fails
(Table 1). The search for a way past the declaration, performed on the same release before the run and after it,
made 240 attempts; none passed. Nine actions of ordinary work were performed in the same run; connecting to Wi-Fi
and pairing a Bluetooth device on real hardware were not.

Table 1. The third complete run, release 0.55, 25 November 2026, 05:01–07:14 UTC.

| Part | Rows | As written in the run | By the text, after the review | Under the plan |
|---|---:|---|---|---|
| Ordinary work | 11 | 9 pass, 2 not observed | 9 performed, 2 not performed | condition of outcome 1 not met |
| P1, Completeness | 152 | 128 pass, 24 undecided | 152 met | 152 met |
| P2, Guarantee | 43 | 43 pass | 43 met | 43 met |
| P4, Law | 91 | 24 pass, 67 undecided | 91 met | 81 met, 10 ? |
| Removal | 5 | 5 pass | 5 met | 5 met |
| Reproducibility | 3 | 2 pass, 1 not observed | 2 met, 1 cannot be written in ConfOS | 2 met, 1 ? (not observed) |
| Understanding | 153 | 1 pass, 152 undecided | 153 met | 1 met, 152 ? |
| All | 458 | 212 pass, 243 undecided, 3 not observed, 0 fail | | |

**Under the plan.** No part receives 0: no argument that a requirement cannot be met by any system was needed.
No part receives 1; every part yields ?. There are five reasons, and none is a failing row.

1. Outcome 1 of any part requires the ordinary work of the plan, which includes Wi-Fi and Bluetooth on real
   hardware. Both were performed on simulated radio, beyond the plan.
2. Ten rows of Law are met because a tool of ConfOS recorded the request as a line of the declaration. The plan
   gives ? to a case met through a program written for the implementation.
3. In 152 rows of Understanding, the machine equals a reference installation, built clean from the published
   source and the same declaration, but not the derivation as the plan restricts it.
4. One case of Reproducibility could not be observed: a line that leaves the account identifiers unstated cannot
   be written in ConfOS.
5. The work ended with the third complete run, before the conditions for outcome 1 were met (Table 4).

**How the two parts fit together.** Part I reports by the letter of the plan. The conclusion that the statement is
confirmed by construction is ours; it stands in Part II (Section 6.3) with its reason.

## 2. What was checked and with what

### 2.1. The specification and the conditions

The specification is the text of version 4: Section 8 of [4], unchanged. The check has six parts: three
properties and three consequences (Table 2). The conditions are quoted verbatim from [5], Section 9.

Table 2. What counts against each part ([5], Table 9).

| Part | Counts against |
|---|---|
| P1, Completeness | “An installed object or a setting is in force and no line records it, and this is not breaking” |
| P2, Guarantee | “At least one line is not fulfilled” |
| P4, Law | “A channel installs, launches or changes such a thing although it is not recorded, and this is not breaking; a built-in tool changes it past the declaration” |
| Removal | “Something the line contributed, and the remaining lines do not cover, is in force” |
| Reproducibility | “What is in force under the lines differs between the two machines, and the difference is not explained by hardware. […]” |
| Understanding | “An installed object or a value of a setting on the machine differs from what was derived from the declaration. […]” |

Ordinary work “is a condition of the whole check”; its list includes “connecting to a Wi-Fi network and pairing a
Bluetooth device on real hardware”. Each part receives one outcome, assigned from the last complete run
[5, Section 9.4].

- “**1.** In that run every case of the part is performed, no case of the part yields ?, and nothing counts against
  the part; the ordinary work succeeds in the same run; the run is performed by a party that did not build the
  implementation, from the published materials; and the search of Section 9.5, made on the same version, has found
  nothing.”
- “**0.** A written argument shows that a requirement of the part cannot be met by any system”, and “a separate
  review accepts the argument.”
- “**?.** No decision.” Among the reasons: “a case is met only through a program that does not count as a built-in
  tool under Section 9.3”; “a case cannot be observed”; “the work ended before the conditions for 1 were met”.

A failing case is a defect: it is repaired, and a new complete run is made, at most eight. Two conditions of
Section 9.3 matter below. For Understanding: “The derivation may read, besides the declaration, only the packages
that its lines name”. For a line written by a program: “a program written for the implementation therefore does
not count as such a tool”; this condition “belongs to the plan and is not a reading of [4]”.

### 2.2. The object

ConfOS 0.55 has 113 pinned components: packages of Debian 13 and four of its own. The declaration is plain text,
one line for one recorded thing. The command `confos apply` assembles the system from the declaration, switches to
it and restarts.

The mechanisms are not part of the definition [4, Section 8.5]; ConfOS chose these. The system part is a read-only
image assembled from the declaration. Nothing can be executed from the writable areas. What a logged-in person can
do is confined. Seventeen programs that can execute saved text—Bash, sh, Python, Perl, awk, sed, make, Node, Git,
Neovim, vi, mpv, pdb, gyp, curl, ed and ssh—are each changed to refuse a file that no line records; the macro
language of LibreOffice is switched off. From the second complete run on, a built-in tool asked for a change
records the request as a line or refuses; the change reaches the machine only through the application.

### 2.3. The parties and the inputs

One party built ConfOS. Another wrote the cases and the checking programs and performed the runs; it received
ConfOS only as published source and as a built image. Its programs take the inventory of the whole machine
without the records of the implementation. The review that the plan requires decided the disputed rows (decisions R1–R10); it
was performed by the party that directed the other two (Table 4).

The source of each release, the cases and the checking programs were committed to the repository of records [6]
before each complete run (Table 3). The figures of the result were checked against the records twice, by a second
reading.

## 3. Results

### 3.1. Three complete runs

Table 3. The complete runs. Times in UTC, 24–25 November 2026.

| Run | Release | Inputs committed | Run | Rows | Rows failing because of the implementation | Search on the same release: attempts that passed |
|---|---|---|---|---:|---|---|
| 1 | 0.32 | 24 Nov, 16:27 | 24 Nov, 16:28–19:56 | 388 | none | 14 of 173 routes, 3 of 58 other attempts |
| 2 | 0.49 | 24 Nov, 23:02 | 24 Nov, 23:12 – 25 Nov, 01:34 | 385 | 3 | 0 of 182, 0 of 58 |
| 3 | 0.55 | 25 Nov, 04:59 | 25 Nov, 05:01–07:14 | 458 | none | before and after the run: 0 of 182, 0 of 58 |

The list of the third run has 124 entries: 122 defined cases and two families of rows generated in the run, one
of Guarantee and one of Understanding.

In run 1, the only row written as failing was a defect of the checking programs. The three failing rows of run 2
belong to the ordinary work: the two updates of the system and the update of a game. All were repaired before
run 3, and nineteen cases were added: the seventeen successes of the search on release 0.32, and two for saved
macro libraries, a way the builder found. In three runs no case failed because of the text.

### 3.2. The six parts in the third run

For Completeness, inventories of the whole machine, taken after the ordinary work and
after every attempt of Law, were compared with the declaration in force; nothing installed or configured was in
force without a line. The rows of Guarantee include nine power cuts right after the report of success and an
interrupted installation. The attempts of Law went through every channel of [3], Section 4.3,
and through the built-in tools run as superuser. Of its 67 rows written as undecided, in 36 a tool refused and
nothing changed; in 10 it recorded the request as a line, and nothing was in force until the application; 21
concern saved files that the system refuses to run directly, as do the 24 undecided rows of Completeness
(Section 3.5). For Understanding, 152 rows are undecided: the derivation as the plan restricts it may not read
dependencies that no line names, although [4], Section 8.2, records a dependency by the line of the package that
brought it.

### 3.3. The search

The catalogue of the search has 182 direct routes for executing a saved file that no line records and 58 other
attempts, at least three for each channel besides the fixed cases. On 0.55 the catalogue was performed before the run (04:20–04:48 UTC)
and after it (07:15–08:29 UTC), and none passed. The script counts one attempt as passed because its command ends
with status 0; its recorded output is a refusal (R7).

### 3.4. Ordinary work

Nine actions were performed: installing a program; two updates of the system with a restart after each; working in
a browser; editing documents; ordinary commands and one’s own recorded script; fetching, building, changing and
rebuilding a small program; installing, starting and updating a game through a launcher that downloads it; and an
installation during which the network was lost and restored.

Beyond the plan, connecting to Wi-Fi and pairing Bluetooth passed on simulated radio: a new clean installation
from the same declaration was connected and paired with nothing typed, and removing the lines and applying undid
both. Of their 14 rows, six pass, four of Understanding are undecided as in the run, and four of Guarantee fail
through the checking programs alone.

### 3.5. The decisions of the review

The decisions that read the text form four groups.

- **A saved file (R1, R4, R5, R10).** A file that the system refuses by every direct route is not code that the
  computer can execute; it is the person’s material. A typed command that reads such a file and hands its text to an interpreter is the person’s
  action [4, Section 8.2]. The same is held for a program that a person recorded by a line and that reads and
  executes a file; no case performs this route, and the evidence is a probe of the builder. A file that a program
  only reads as values is not code. Under the opposite reading, no system with a command shell in which a person
  can record a program of his or her own could have Law. After the runs we confirmed R4; it is now our
  decision, not the review’s.
- **A tool that refuses (R3)** and changes nothing has provided no path past the declaration: the row is met.
- **A tool that records the request (R8)** does what [4], Section 8.3, says of an installer: by the text the row is
  met; under the plan it yields ?.
- **A command that downloads and executes code without saving it (R6)** is judged after the restart.

The other decisions concern the procedure (R2, R7, R9).

### 3.6. Beyond the plan

On 0.55, seventeen recording tools were tried in both directions. Each request was recorded as exactly its line,
and nothing of it was in force before the application. Of the 119 rows, X has 14 pass, 2 fail and 1 not observed; Completeness has 34 pass; Guarantee has 31 pass and
3 fail; Understanding has 34 undecided as in the run. The failures and the unobserved row arise through the
checking programs alone. Four recorders are not built; X-REC-LOCALE and X-REC-LINGER are written as failing
because their tools are not built and the cases were not performed. These rows are not
observations of the check.

## 4. Departures from the plan and limits

### 4.1. Departures

Table 4 follows the form of [5], Table 5, recommended for reporting deviations from a fixed plan [7].

Table 4. Departures from the plan.

| What was fixed | What was done | Why | Effect on the results |
|---|---|---|---|
| Ordinary work includes Wi-Fi and Bluetooth on real hardware | Performed only on simulated radio, beyond the plan | The runs were made in virtual machines, and the radio adapter of their host could not be handed to them | The condition of outcome 1 is not met for any part |
| The work ends when a complete run leaves no defect and the search finds nothing, or with the eighth run; a ? through a program written for the implementation is such a defect | The work ended with the third complete run, with ten such rows and the 152 rows of Understanding at ? | The tools would have to refuse instead of recording, and [4], Section 8.3, asks them to record (R8); a ConfOS whose declarations name every package was not built | Every part also yields ? for this reason (Section 1, reason 5) |
| The review reads the records of both parties and takes part in neither | It was performed by the party that directed both and gave them orders, among them repairs and added cases | The rules of the work gave it to that party | The decisions R1–R10, on which the outcomes by the text rest, are those of a party that took part in the work |
| The party that performs the runs searches after a complete run | The catalogue was written on 24 November 2026 by a party of its own, which neither built nor performed the runs; on 0.49 and 0.55 a script performed it again, and no attempt was added | The means chosen for writing new attempts did not accept this work, as in [5], Table 5 | On 0.55 the search shows only that every way found earlier is closed |
| Each success of the search becomes a case before the next complete run | The 14 routes and 3 attempts that passed on 0.32 became cases before run 3, not run 2; on 0.49 they were refused outside the run | Our omission | Run 2 is reported with this departure |
| Components are taken in their latest stable release on the day the inputs are committed | In each run one pinned package was older than the archive: the kernel in run 1, `libzstd1` in runs 2 and 3 | The pinned list was not brought up to that day | In run 3, one of 113 components is older |
| The checking programs are committed before the first complete run | They were corrected before runs 2 and 3; one commit before run 3 was followed by no run (R9) | Defects of the checking programs | Each correction was committed before the run it governs |

### 4.2. Three facts next to the result

**(a) By the letter of the plan, outcome 1 is not set for any part.** Ordinary work with Wi-Fi and Bluetooth was
performed on simulated radio, not on real hardware, and two conditions of the plan itself give ? (Section 1 lists
all five reasons). None of these is a failing row.

**(b) The refusal to execute an unrecorded file is implemented for seventeen named programs.** Other programs of
the Debian archive that have a language of their own are not covered. This is why the reference implementation of
Section 7 gets a closed base of its own.

**(c) The result is confirmed by our own check.** Attempts by others to break it are still ahead.

The check covers one implementation on one base, in virtual machines. One question is recorded and decided by no
case: a running container made from a recorded image appears in the inventory as an object without a line.

# Part II. Formulated after the results

This part changes no outcome of Part I.

## 5. The definition, version 5

### 5.1. Definition

**A declarative operating system is an operating system in which the declaration is the law of the computer: what is
written in it is what is on the computer.**

A declaration (also called a configuration) is a text that a person has designated as the description of his or her
computer: written in it is what is installed on the computer and how the computer is configured.

### 5.2. What follows from this

1. **By default, the system itself does not allow anything to be installed, configured or launched past the
   declaration.** Otherwise there would be something on the computer about which the declaration says not a
   word—no longer what is written. As long as nothing is written about it in the declaration, it is not on the
   computer, and the system itself does not allow it to be done.
2. **The declaration can be trusted.** What it says about the computer is true, and what it is silent about is neither
   installed nor configured on it. There is no need to check it by inspecting the computer.
3. **The same declaration on another computer yields exactly the result described in it,** provided the description
   is unambiguous. There, too, what is written is present. Differences due to hardware do not count.
4. **Remove a line and apply: what it contributed is not on the computer,** unless the remaining lines contribute it.

There are no degrees: a system either is such a system or it is not.

### 5.3. Words

- **In force.** The computer is brought into conformity with the declaration; the declaration is not copied from the
  computer. To bring into conformity means to apply; the system does this. The law is the declaration
  that the system applied last and reported as successful; a line added to a file and not yet applied is not yet law.
  Everywhere in this text, “the declaration” is the one in force. There may be many files; the description is one.
- **What the declaration is about.**
  - About what is installed: the programs put on the computer and everything that came with them, including the
    operating system itself.
  - About settings: what the computer as a whole obeys, whoever set it and however—services and their parameters,
    the network with saved networks, devices and filesystems, time and language, accounts, rights, access rules,
    means of login.
  - Data appear on the computer without the declaration as well: program records (a log, a cache, a history) and a
    person’s material (documents, photographs, projects, downloaded files, his or her keys and passwords for other
    machines).
- **“Written.”** A line names what must be: a program is installed, a service is enabled, a setting has such-and-such
  a value. What the system itself obtains or builds from a line also comes through the declaration: a dependency,
  the program’s own files and values, a compiled copy. The declaration promises what the line names. What a line
  does not name but leaves open (the number of an account, “the newest version”), the declaration does not show and
  does not promise to be the same on two computers. The declaration is silent about what neither comes through any of its lines nor is
  left open by any line; “nothing is written” and “says not a word” mean the same.
- **“By default”** means as long as the declaration has no line that opens this. This is a
  property of the system itself under any declaration: neither the system nor a program with its own values gives a
  path past the declaration. A system in which such a path is open until it is closed by a prohibition does not have
  this property, however many prohibitions are written into it.
- **Breaking.** To install or configure something that the declaration is silent about is
  possible only by force: with superuser privileges and outside the system’s tools—by writing directly to its files,
  by deleting, by disabling its mechanisms. This is a violation on the person’s part, not a property of the system,
  and it does not refute the definition.

### 5.4. Frequently asked questions

Answers to questions that the reader would otherwise decide in his or her own way. This section stands directly under
the definition and goes together with it.

1. **A person has himself or herself written into the declaration “in this folder the rules do not apply”. How does
   this differ from `nix-env`, which installs a program past the declaration?** In who opened the path and where this
   can be seen.
   - Here the path was opened by the person, by a line in the declaration. It is written, so it is so: the
     declaration tells the truth, and everyone who opens it sees the line. It is the same kind of setting as the SSH
     port on a server.
   - The system itself, by default, does not allow anything to be installed past the declaration. That is why the
     declaration is trusted at once. It makes no promise where such a line stands, and exactly as far as that
     line opens.
   - `nix-env` in NixOS is a command that is there by default: the person wrote nothing, and yet a program can be
     installed past the declaration. The declaration does not show this, so it cannot be trusted in anything.
   - A line may open even the whole disk; this does not break the definition. In the same way, the last amendment to
     a constitution could repeal all of its articles: a person wrote this; it is not a hole that the system left.
2. **Is an installer run through `sudo` breaking?** No, and it does not install past the declaration. The system’s
   own tools—the installer, the management of users, of services and of the network—work only through the
   declaration, by default and with superuser privileges too. Breaking is when a person with full root goes around
   these tools: writes to system files by hand, deletes, disables the protection. This is possible, and the fault is
   that person’s own. What is said of the system’s installer applies equally to the installers of programming
   languages and to a program that itself downloads additions and updates for itself.
3. **Python is recorded. May one run one’s own script with it?** By default, no. A script that a person wrote or downloaded is
   that person’s file. By default the system does not run it, and the recording of Python does not change this. Code
   is a file that a program executes; a file from which it only reads values is not code.
4. **And a command that a person typed in the terminal himself or herself?** It is that person’s action, not
   something that is on the computer. The same holds when the person himself or herself feeds text to a program as
   its input: `cat x.sh | bash`. But `bash x.sh` is already the running of a file; question 3 is about it. The same
   holds for a person’s own program, which that person wrote or brought and has himself or herself written into the
   declaration: if it reads a file and executes it, it is the program that does this. But what the declaration is
   silent about cannot be installed or configured in this way.
5. **Is a program in a container a special case?** No, it is an ordinary program: it runs on this computer as its own
   process.
6. **A website in a browser, a system in a virtual machine—must they be written?** No. They are inside a recorded
   program and cannot themselves launch programs or change the computer.
7. **Are a theme and a home page settings?** No, they are a record of the program itself. But a value of a program
   that launches something or opens access to someone is a setting of the computer.
8. **A running process, an open port—must each be written as a separate line?** No. They come from a program or a
   setting that is recorded: the Firefox process from the line of Firefox, the open port from the line of the SSH
   server.
9. **The users are taken from the company’s server—must each be written?** No, it is enough to record the server; it
   must be named in the line.

### 5.5. What the definition does not decide

This is the design of a particular system:

- which lines it lets a person write, and in what language;
- whether a line is written by the person or by a tool of the system at that person’s command;
- how what is installed by a program that itself downloads other programs gets into the declaration;
- by what mechanism the system does not run what nothing is written about;
- how data are stored and transferred;
- user rights, generations and rollback, protection of the declaration and of secrets;
- when an edit takes effect.

## 6. Version 5 and the cases of the reference implementation

### 6.1. The table

Table 5 names, for the statements of version 5, the cases of the third run that exercise them and what they show.
“Met” means met by the text after the review; the outcomes under the plan are those of Section 1.

Table 5. Statements of version 5 and the cases of the third complete run.

| Statement of version 5 | Cases | What they show |
|---|---|---|
| The core: the declaration is the law of the computer | Guarantee 43, Completeness 152, Law 91 | met |
| A declaration is a text that a person designated | the test declaration of every case | a premise of the cases |
| Consequence 1: by default the system itself permits nothing past the declaration | Completeness 152, Law 91 | met |
| Consequence 2: the declaration can be trusted | Understanding 153, Guarantee 43, Completeness 152 | met against the reference installation |
| Consequences 3 and 4: the same result on another computer; remove a line and apply | Reproducibility 3; Removal 5 | 2 met and 1 cannot be written; 5 met |
| In force: the law is the declaration applied last with a report of success | Guarantee 43, with nine power cuts and one interrupted installation; ten recorded requests, after which the earlier state stayed in force | met |
| What the declaration is about: what is installed, settings, data | Completeness 152, Guarantee 43; fifteen attempts with built-in tools; ordinary work with documents, a script and a game | met; radio on real hardware not observed |
| “Written”: what a line names, and what the system obtains or builds from it | Guarantee 43; the shared dependency of Removal; building a program from lines; Reproducibility 2 | met |
| “By default”: a property under any declaration | Law 91, with Completeness after each attempt | met for the declarations and programs tried |
| Breaking: installing or configuring what the declaration is silent about only by force | Law 91, with tools run as superuser; two candidates for breaking | met; no successful breaking is established |
| Question 2: an installer run through `sudo` | Law 91; ten recorded requests | met; in both directions: Section 3.6 |
| Question 3: one’s own script and recorded Python | five attempts through interpreters | met (R1, R4, R5) |
| Question 4: a typed command; one’s own recorded program that executes a file | the command shell; three commands that download and execute without saving | decided by the review (R6, R10) and, for R4, by us; no case performs the route of R10 |
| Question 5: a program in a container | four attempts with containers | met |
| Questions 6–8: a website and a guest system; a theme and a home page; a process and an open port | work in a browser; five attempts with an alias, a hook, autostart and SSH; three cases of Removal and two attempts with a recorded player | met; no case with a guest system, with a theme or a home page, or attributing a listening port |

Eight statements were not tested on ConfOS and rest on reasoning: that there are no degrees; that many files form
one description; that what a line leaves open is neither shown nor promised; that “by default” means as long as no line opens it, and question 1; that a system with a path open until it is prohibited lacks the property; that breaking does not refute the
definition; and question 9. Two sentences of “Words” say how a word is used and are mapped in the full table: which declaration is
meant, and what it is silent about. No verdict of the third run would differ under version 5.

### 6.2. The differences from version 4

Version 5 is a rewording of version 4, not a new hypothesis. It has one core sentence, and everything else follows
from it. Guarantee is the core itself; Completeness and Law are consequence 1; Understanding is consequence 2;
Reproducibility is consequence 3; Removal is consequence 4. The sentences of version 4 that decided particular
cases are found in “Words” and in “Frequently asked questions”; the seven concepts of [4], Section 8.1, and the four
questions asked in order of Section 8.2 are no longer separate parts of the text.

There are three differences in content, and none makes a requirement stricter.

1. The sentence “an installer does not install a program past the declaration but adds it to the declaration” is
   gone. A tool of the system either records the line or refuses. ConfOS did the stricter thing: it recorded.
2. A file with code that a person wrote or downloaded is that person’s material, which the system does not run by
   default. In version 4 it was a program that must be recorded [4, Section 8.2, the second question]. The runs
   were already judged in the new way: such files were refused (R1).
3. “Everything … recorded” and “shows” are replaced by “what it is silent about is neither installed nor
   configured”. On ConfOS 0.55 the two coincide, because it has no line that opens anything.

One statement is new relative to version 4: the answer about a line that a person writes into his or her own
declaration (question 1, with the meaning of “by default”). The line itself is not new to the series: version 1
allowed a bypass “through a line in the declaration itself that permits it” [1, Section 5.2], version 2 treated
such a line as a separate notion with a frame of its own [2, Sections 6.3 and 7.1, problem O12], and version 3
left such lines to the design of a system [3, Section 2.6]. The answer of version 5 is that such a line needs no
separate notion in the definition: it is simply a line like any other. This answer is reasoning from the core, not a result of Part I: ConfOS 0.55
has no such line. It is to be checked on the reference implementation (Section 7). The fact about `nix-env` on
which question 1 relies was established in [4], Sections 4.4 and 6.2.

### 6.3. What we conclude

The statement that was the hypothesis—a system that meets the definition can be built, and ordinary work is
possible in it—is confirmed by construction.

That such a system can be built is shown by one working example. ConfOS was built from the
text as its specification and checked by a party that did not build it, with programs of its own. In the last
complete run every part was met by the text in every row performed, nine of the eleven actions of ordinary work
were performed, and the search found no way past the declaration. The three facts of Section 4.2 stand next to this result.

The definition itself is not proven by this, and cannot be: it is a choice of the meaning of a word
[4, Section 6.4]. What is established is that the choice is not empty: a system of this kind exists.

## 7. The plan

The next step is a reference implementation of version 5: ConfOS without Debian. It has a base of its own, a small
frozen set of packages built from source. With it come a manual by which a person builds the system by hand, an
archive of the sources, and the site confos.org. It is checked by rules fixed in advance.

1. **One kind of line that opens a folder.** Three cases check it: in the folder, a person’s own script runs;
   outside it, the script is refused; the line is visible in the declaration.
2. **A hard rule for the base.** A program enters the base only if without it the system cannot boot, apply a
   declaration, build its own packages or pass the checks.
3. **The condition “done”, written in advance.** The system builds itself from source; one clean complete run is
   made in a virtual machine and on real hardware; the manual is written; a build by hand on a real laptop has
   succeeded. After that the implementation is frozen.
4. **“The same result”** means what the line names—the source and the recipe—and not identical bytes.

## Conclusion

Under the plan fixed in [5], a reference implementation was built from the text of version 4. In the last complete run no row fails, and the search found no way past the
declaration. By the letter of the plan no part receives 0 and none receives 1.

We conclude that a declarative operating system in the sense of the definition can be built and that ordinary work
is possible in it. What remains is a reference implementation with a base of its own, checked on real hardware by
rules fixed in advance, and attempts by others to break it.

## References

1. Yakymenko, A. (2026). Configuration as Law: A hypothesis on what a declarative operating system is. Preprint,
   18 November 2026; hypothesis, version 1. https://yakyman.com/configuration-as-law-v1.pdf
2. Yakymenko, A. (2026). Testing the “Configuration as Law” Hypothesis: Results of the First Cycle and a Second
   Version. Preprint, 20 November 2026. https://yakyman.com/configuration-as-law-v2.pdf
3. Yakymenko, A. (2026). Testing the “Configuration as Law” Hypothesis, Version 3: Hypothesis, Checks, and Failure
   Conditions Fixed Before the Checks. Preregistration, 21 November 2026.
   https://yakyman.com/configuration-as-law-v3.pdf
4. Yakymenko, A. (2026). The “Configuration as Law” Hypothesis: Results of the Checks of Version 3, and Version 4.
   Preprint, 22 November 2026. https://yakyman.com/configuration-as-law-v4.pdf
5. Yakymenko, A. (2026). The “Configuration as Law” Hypothesis: Results of the Checks of Version 4, and a New Plan
   for Checking It. Preprint, 23 November 2026. https://yakyman.com/configuration-as-law-v5.pdf
6. Records of the checks. https://github.com/Yakyman/configuration-as-law
7. Willroth, E. C., Atherton, O. E. (2024). Best Laid Plans: A Guide to Reporting Preregistration Deviations.
   Advances in Methods and Practices in Psychological Science, 7(1). https://doi.org/10.1177/25152459231213802

## Records

The inputs of the three complete runs are in the repository of records [6]: commits `425609f9`,
`9e99accd` and `39533ee3`.

- The source of the implementation, with the list of the choices that the text leaves to a system.
  configuration-as-law/confos
- The cases and the checking programs. configuration-as-law/confos-check
- The cases beyond the plan. configuration-as-law/confos-check-extra

Published with this paper in the same repository:

- The list of the complete runs. configuration-as-law/records-confos/RUNS.md
- The summary of each run and of the cases beyond the plan. configuration-as-law/records-confos/RUN-1.md;
  configuration-as-law/records-confos/RUN-2.md; configuration-as-law/records-confos/RUN-3.md;
  configuration-as-law/records-confos/RUN-3-EXTRA.md
- The decisions of the review. configuration-as-law/records-confos/REVIEW.md
- The full table of Section 6.1. configuration-as-law/records-confos/TABLE.md
