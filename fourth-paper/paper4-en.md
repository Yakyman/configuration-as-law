# The “Configuration as Law” Hypothesis: Results of the Checks of Version 3, and Version 4

Arthur Yakymenko

Preprint · 22 November 2026 · Part II fixes version 4 of the hypothesis and the failure conditions of its checks before these
checks begin; after publication, they do not change

## Abstract

In the third paper [3], we fixed version 3 of the “Configuration as Law” hypothesis—a definition of a declarative
operating system through three properties—and four checks with failure conditions. This paper consists of two
parts. In Part I, we report the outcomes of the checks strictly under the fixed conditions. The check of the rule
“what must be recorded” on clean installations of Fedora Workstation, openSUSE Tumbleweed, Linux Mint and Flatcar Container Linux
yielded outcome 0: among 16,524 objects, five kinds of objects were found for which the text does not allow deciding whether
they must be recorded; all five concern the removal test. The assessment of existing systems yielded outcome 1: NixOS and
GNU Guix System could be assessed against each property, and they have none of the three properties. The checks of the properties
on a testbed and of reproducibility were not conducted: the testbed was partly built and was not accepted. In Part II, formulated
after the results, we explain why we regard only a description of the computer that can be trusted as a declaration,
and set out version 4. In it, the rule with the removal test is replaced by a direct definition: everything that is installed
and all settings are recorded; records that programs keep themselves as they run, and material created by
a person, need not be recorded. We fix the plan for checking version 4 and the failure conditions.

Keywords: declarative configuration, configuration management, operating systems, check conditions fixed in advance,
reproducibility.

## 1. Introduction

We investigate the question: what is a declarative operating system, and what properties must it have?

In the first paper [1], we proposed version 1 of the hypothesis and, before the checks began, fixed five checks and their
failure conditions. In the second paper [2], we reported the outcomes—the census of objects yielded 0, the other checks yielded ?—and,
separately, as formulated after the results, set out version 2. In the third paper [3], we changed the definitions
of version 2 before its checks, producing version 3, and fixed four checks and their failure conditions.

Under the rule adopted in the second paper, definitions changed after the results became known form a new version
of the hypothesis, which is tested on machines and objects that earlier checks have not seen. This paper therefore
has the same structure as the second. Part I reports the outcomes of the checks of version 3 under the conditions fixed in
[3], without new rules or thresholds. Part II is formulated after the results, is not supported by the results of Part I,
and contains version 4 together with a plan for checking it.

Table 1. Versions of the hypothesis and their checks.

| Version | Where set out | What determined what must be recorded | What was checked | Outcome |
|---|---|---|---|---|
| 1 | [1] | everything that runs on the computer; the rest is data or produced by programs | five checks [2] | census 0; the others ? |
| 2 | [2], Part II | a list of parts of the system | not checked: replaced by version 3 before the checks | — |
| 3 | [3] | whatever the computer’s behaviour depends on—what it does and what can be done on it; the removal test | four checks, this paper, Part I | check 1—0; check 4—1; checks 2 and 3 not conducted |
| 4 | this paper, Part II | what is installed and settings | plan in Section 9 | — |

## 2. What was checked

### 2.1. The hypothesis, version 3

The full text of version 3 is given in [3], Sections 2 and 3. There, a declaration is defined as a collection of files that
a person has designated as the primary description of the computer. What must be recorded was determined by the rule: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded. The test is
removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the
object must be recorded.” Objects that need not be recorded were content, cache, records of the past and settings that are in force only inside one
program. There are three properties. P1, Completeness: everything that must be recorded and is in force on the computer is recorded. P2,
Guarantee: everything recorded is in force as its line requires. P4, Law: the system provides no
path for changing, past the declaration, anything that must be recorded.

### 2.2. Four checks and their failure conditions

The conditions are quoted verbatim from [3], Section 4.

Check 1, what must be recorded. “On any machine, an object is found for which the text of Sections 2.2 and 3 does not allow
deciding whether it must be recorded, or allows deciding both ways; or the two classifications decided differently
and the adjudication finds no sentence of the text that resolves the dispute.”

Check 2, the properties on a testbed. “At least one channel installs, launches, or changes something that must be
recorded although it is not recorded, and this is not breaking (P1, P4); a built-in tool, including with superuser
privileges, changes such a thing past the declaration (P4); after a completed application, at least one line is not
fulfilled (P2); after application of a declaration without a line, something the line contributed and the remaining
lines do not cover is in force (Removal, P1).” A separate condition concerned suitability for ordinary work.

Check 3, reproducibility. “What is in force under the lines of the declaration differs between the two machines, and the
difference is not explained by hardware.”

Check 4, existing systems. “A case yields 1 when both assessments reach the same decision, “has” or “does not have”, with
sufficient information, or when they differ and the adjudication resolves the dispute by a sentence of the text; ?
when the information is insufficient; 0 when the information is sufficient but the text of
the hypothesis does not allow deciding whether the system has the property, or when the two assessments differ and
the adjudication finds no sentence of the text that resolves the dispute.”

### 2.3. General rules

The outcome of a check is 1, 0 or ?. It combines its cases: 0 if any case yields 0; otherwise ? if any case
yields ?; otherwise 1. An object for which the definitions do not allow deciding whether it must be recorded yields 0. The two
classifications are independent; their disagreement is considered by a separate adjudication that took part in neither
of them. A failure of the testbed yields 0 only if a written argument shows that it follows from the definitions alone.
The machines and objects of checks 1–3 did not take part in the first cycle [3, Section 4.1].

# Part I. Results of the checks of version 3

## 3. How the checks were conducted

The checks ran on 21–22 November 2026 under the text of [3], published before they began. The inputs to the checks—the release
numbers, the commands for ordinary actions, the programs for compiling the inventory—were committed to the repository of records [4] before the first
observation. The failure conditions did not change after publication; no new classification rules or agreement thresholds
were introduced.

There was one departure from the text of [3] in how facts were established. Section 3 of that text provided that,
in a disputed case, the object would be removed on a disposable copy of the machine, and what stopped working would be recorded. In check 1,
objects were not removed: the consequences of removal were established by reasoning from the inventory and documentation. This departure
does not affect the failure conditions or the rules for combining outcomes, but the facts about the objects were obtained less directly
than had been promised.

Before the checks, as required by Section 5 of [3], the wording of Section 2.2 was tried on 5,200 objects from the first
cycle in two independent classifications. Decisions matched in 80.21% of cases. Adjudication of disagreements confirmed two
gaps in the text: a system service setting fits both “a setting inside one program” and the rule about the
computer’s behaviour; a compiled copy of code that a program recreates itself fits both “cache” and
“code executed with the program’s rights”. The wording was not changed after this trial, and the checks were conducted under
the unchanged text of version 3.

## 4. Outcomes of the checks

### 4.1. Check 1: what must be recorded. Outcome 0

Inventories were obtained on four of the five machines: Fedora Workstation 45, openSUSE Tumbleweed 20261120, Linux Mint 22.3 and
Flatcar Container Linux 4757.2.3. On Talos Linux 1.14.6, the collection program was stopped before it wrote
the table of objects; there is no inventory, and this machine yields ?. The ordinary actions before the inventory on the desktop systems were
completed in full: 15 on Fedora, 15 on Tumbleweed, 17 on Mint.

Table 2. Check 1 by machine.

| Machine | Objects | Matching decisions | Share | Cohen’s kappa | Sent for adjudication | Outcome |
|---|---:|---:|---:|---:|---:|:---:|
| Fedora Workstation | 5,887 | 5,444 | 92.47% | 0.550 | 455 | 0 |
| openSUSE Tumbleweed | 6,779 | 6,542 | 96.50% | 0.781 | 490 | 0 |
| Linux Mint | 2,031 | 1,816 | 89.41% | 0.448 | 250 | 0 |
| Flatcar Container Linux | 1,827 | 1,223 | 66.94% | 0.301 | 648 | 0 |
| Talos Linux | — | — | — | — | — | ? |
| Total | 16,524 | 15,025 | 90.93% | 0.556 | 1,843 | 0 |

Of the 1,843 objects sent for adjudication, the adjudication marked 888 as resolved by the text: 295 must be recorded, 593
need not be. What 31 objects do remained unknown. For 924 objects, the adjudication found no sentence
of the text that resolves the dispute. A separate check of these records confirmed five kinds of gaps out of the eight named
by the adjudication; one argument was rejected by the text, and two were based on incorrect facts.

The same check reconsidered random samples. Of 40 decisions marked by the adjudication as resolved, it supported
10; it assigned 20 to gaps, seven to questions outside the definition, and three to unknown facts. Of 60 objects for
which the two classifications matched, it supported 57 and assigned three to gaps. The figure 888 therefore counts the adjudication’s
labels, rather than being a confirmed count of objects that the text resolves.

The five confirmed kinds of gaps follow. Row counts are taken from the check record; some are disputed by the review, as discussed below.

1. **Shared content or capability.** A font, translation or theme shared by many programs. Their removal
   can be described as the loss of particular images and texts, or as the loss of the capability to display them. The text
   draws no boundary between content and capability. According to the check record: 303 rows.
2. **Lookup tables.** Terminal descriptions, character tables. Removal can be described as the loss of particular
   answers, or as the loss of the ability to perform such a lookup. According to the check record: 131 rows.
3. **Packages containing only dependencies.** Removing such a package changes nothing now, but changes what
   the package manager will install or retain at the next operation. The text does not say whether such a later
   consequence is part of the removal test. According to the check record: 319 rows.
4. **Support for absent hardware and other execution environments.** Firmware for a device that is absent; boot
   files for another hypervisor. If the environment stays the same, removing them changes nothing; if the environment changes,
   it does. The text does not say which environment is used in the comparison. According to the check record: 255 rows.
5. **Objects that the system recreates.** After removal, the object is restored from another object. The text
   does not say whether restoration is part of the comparison or how long to wait for it. According to the check record: 20 rows.

The check record assigns 1,028 rows to the five kinds. An independent review disputes the inclusion of 371 of them—eight
Tumbleweed rows, 252 Fedora rows and 111 Mint rows: the installation scripts of these packages were not examined, and a package
with a script might turn out to require recording under the rule about code. The remaining 657 rows are undisputed. In each
of the five kinds, there is at least one row for which the facts have been fully established, so neither outcome 0 nor the number of kinds depends
on this dispute. All five gaps concern the removal test: the rule does not say exactly what should be compared with what
after removal.

Limits of this result. First, on Fedora, Tumbleweed and Mint, the collection program’s filesystem query
failed, and stored objects outside packages on these machines were not included in the inventory; the Mint inventory contains only
accounts, groups and packages. Such objects appear only in the Flatcar inventory, in 852 rows. Outcome 0 does not depend
on this, but the check did not see the hardest part for the rule—files in the home directory and changed settings of a desktop
system. Second, the row counts by kind given above are taken from the check record before
accounting for the review’s objection and sum to 1,028; taking the objection into account, they overstate the count by at most 371, and full
coverage of each kind has not been established. Third, one of the early checks of the records of check 1 read the adjudication’s
working folder, which it should not have read under the rules; this departure is recorded, and the subsequent check did not
use that folder.

### 4.2. Check 2: the properties on a testbed. Not conducted

The testbed—a Linux prototype in a virtual machine—was being built during the checks and was not accepted. It is assembled from
existing components (a service manager, kernel access control mechanisms) and several small programs: one
applies the declaration, and the others prevent execution of what is not recorded. Of the 88 ways of bypassing the declaration listed during
preparation, 78 have been closed; an independent review confirmed all 78 closures, and ten ways remain open.
The testbed nevertheless remains partial: a full inventory for property P1 and recovery from failures in general
have not been demonstrated. No attempt to bypass the completed testbed has been carried through. Check 2 has not begun and has no outcome.

The testbed was built for a strict reading of the rule about code, under which code typed
by a person at the command line must also be recorded. It therefore has no unrestricted command shell: the person selects a recorded
program from a list.

### 4.3. Check 3: reproducibility. Not conducted

Check 3 requires an accepted testbed from check 2. It has not begun and has no outcome.

### 4.4. Check 4: existing systems. Outcome 1

NixOS 26.05 and GNU Guix System 1.5.0 were assessed against each property twice, independently. In all six cases, both
assessments reached the same decision with sufficient information: the systems do not have the property. The independent review
agrees with the outcome. Under the condition of the check, the conclusion “does not have” is a successful assessment, so each case yields 1.

Table 3. Check 4.

| System | Property | Decision of both assessments | Decisive fact |
|---|---|---|---|
| NixOS | P1 | does not have | The `users.mutableUsers` option is enabled by default; an account can be created with the `useradd` command, and it is in force without being recorded [10]. |
| NixOS | P2 | does not have | After a successful application, the `usermod` command changed the primary group of a recorded account; the declaration stayed the same, and the discrepancy persisted. |
| NixOS | P4 | does not have | The `nix-env` command installs programs into the user’s profile independently of the declaration [8]; the account management command changes what is recorded past the declaration. |
| Guix System | P1 | does not have | The manual describes creating accounts using commands outside the declaration; such accounts are in force until the next application or reboot [11]. |
| Guix System | P2 | does not have | According to the manual, recorded properties of an account can be changed by a command after application [11]. |
| Guix System | P4 | does not have | The package manager works with user profiles past the system declaration; the same applies to accounts [11]. |

For NixOS, the decisive facts were obtained experimentally on a clean installation. For Guix System, they come from documentation: the experiment
with application of the declaration on this system failed and was not included in the assessment.

Three of the six cases depend on how the period during which the properties hold is read: “at any moment after a completed
application” or “at the moment of completion of the application”. Both assessments and the review adopted the first reading; the text of version 3
allows it but does not state it explicitly.

### 4.5. Work beyond the fixed plan

This work was not part of the plan in [3] and does not contribute to the outcome.

- Reading the text of version 3 for contradictions yielded seven cases in which the definitions admit two readings; all
  seven were confirmed by a separate check. Among them: a browser setting by which it opens a file in another
  program; an editor that installs executable extensions itself with superuser privileges; an account
  from an external directory, not created on the computer; a login key whose every use requires
  a person’s confirmation.
- An inventory of a machine prepared as a lived-in machine, with objects outside packages: 21,278 rows reduced to 5,212 objects.
  Decisions matched in 73.94% of cases; three gaps were confirmed in 142 rows. Two of them—a program’s history and
  a record that a service was enabled in the past—fit both “records of the past” and the rule about the computer’s behaviour.
- An analysis, from documentation, of 88 ways of bypassing the declaration. Eight were claimed to be closable; the review
  did not accept some of these claims. For three, the answer depends on the reading of the text: a recreated compiled
  copy of code; code to which the executing program has granted access to one directory on the computer; an editor with an
  extension installer. For 77, the documentation is insufficient. No way that no system could close was found.
  A separate question was recorded: whether a line of the declaration may compute what is recorded from a list outside the declaration.

## 5. Summary and limits of the conclusion

Table 4. Outcomes of the checks of version 3.

| Check | Outcome |
|---|:---:|
| 1. What must be recorded | 0 |
| 2. The properties on a testbed | not conducted |
| 3. Reproducibility | not conducted |
| 4. Existing systems | 1 |

Version 3 did not withstand the check: its rule does not make it possible to decide, for every object of a real computer, whether
it must be recorded. The confirmed gaps occur in two places in one section. The removal test does not
say what to compare with what. The list of what need not be recorded conflicts with the rule itself when an object fits
both.

Nothing in these results establishes whether a system with the three properties can be built: checks 2 and 3 were not
conducted. Outcome 1 of check 4 means that the definitions suffice to assess existing systems, not that
the hypothesis is true.

# Part II. Formulated after the results

This part was formulated after the results of Part I became known. Those results do not support it:
they were obtained for version 3, whereas version 4 has not yet been checked. It will be checked under the plan in Section 9 on machines and objects
that earlier checks have not seen.

## 6. Why it must be possible to trust the declaration

### 6.1. What is expected of a declaration

Declarative configuration is commonly defined through desired state: a person describes what the result should be, and
the tool derives the actions. Anderson and Couch call a configuration declarative when it specifies a “desired final
state” [5]; we examined this definition and its boundaries in the first paper [1, Sections 2.1–2.3]. Two things are expected
of a system built on a declaration: the text can tell us what is on the computer, and the same
text can produce a second identical computer.

### 6.2. Desired state gives only a lower bound

A description of desired state answers the question of what will be on the computer. It does not answer the question of what
is on the computer. If a program or an account can be added past the description, then a person who reads the description
knows only part: what is recorded is present, but the text does not show what is present beyond it. Neither
of the two expectations is then met: the text cannot tell us what is on the computer, and a second computer built
from the same text differs from the first.

This is not a rare case but documented behaviour. The NixOS manual describes two ways of managing packages,
declarative and “ad hoc”, and says of the second: “It's the only choice for non-root users” [8]. The Kubernetes
documentation lists among the advantages of declarative object management that changes made directly to
live objects are retained, “even if they are not merged back into the configuration files” [12]. We observed the same experimentally twice. In the census of the first
cycle, on a clean installation of Guix System, an ordinary user installed and ran a program without changing the declaration
files [2, Section 7.5]. In check 4 of this paper, on NixOS, a recorded account was changed with an ordinary
command, the declaration stayed the same, and the discrepancy persisted (Section 4.4).

### 6.3. This distinction is known

The distinction between an incomplete and a complete description was introduced by Traugott and Brown [6]; we presented it in the first paper [1,
Section 2.2] and related the properties of the hypothesis to it in the second [2, Section 7.5]. Under convergence, machines
approach the description, but the description itself is “characteristically an incomplete description of machine state”. Under
congruence, machines are maintained “in complete compliance with a fully descriptive baseline”. The authors of
NixOS place their system in the second regime with a qualification: “Disregarding mutable state, NixOS has a congruent
model” [9].

Here, this distinction serves as an argument. The requirement for a complete description is not our invention: it was named in 2002, and
the system most often called declarative places itself in the congruence regime. The authors of
NixOS draw the boundary themselves: mutable state, in which they include the accounts file, in their words, “is not
dealt with in the functional model at all” [9]. The account change in check 4 therefore does not
refute their claim: it lies beyond the boundary they declared. Our disagreement with them concerns where the boundary lies.
We include accounts and installed programs in what the declaration must cover; according to the NixOS
manual and the experiment in check 4, the description of these is incomplete and is not the only description.

### 6.4. Our position

We call an operating system declarative when its declaration is both a prescription and a complete list:
everything recorded is present on the computer, and nothing beyond what is recorded is installed or configured on it.
This is a choice of the meaning of a word, and we present it as a choice. The basis for the choice is Section 6.2: only with this meaning
does the declaration provide what is expected of it.

Completeness is limited here to what is installed and settings. Program records and a person’s material, as defined
in Section 8.2, need not be recorded. These two kinds are what remains after the questions about code and settings:
objects that no one executes and that the computer does not obey. The declaration is written before the computer runs,
whereas they appear as it runs. A script written by a person, and history that a program executes as code,
do not belong to them: they are programs. The author of Nix draws the same boundary: a service consists of programs, static
settings and mutable state, and the first two are managed, whereas the third is not [7, p. 15].

### 6.5. What we do not claim

We do not claim that desired-state systems are useless: they solve the problem of deployment. We do not claim
that the question of mutable state is resolved: it is not part of the definition. Nor do we claim that a system with the three
properties can be built: that is the subject of checks 2 and 3.

## 7. What changed and why

The rule of version 3 decided an object’s status by a question about consequences: what will stop working if the object is removed.
Part I showed that this question requires five clarifications absent from the text: whether loss means the loss of
content or the loss of a capability; whether consequences that arise later should count; whether to compare on the same machine
or on any machine; whether to wait for restoration; and which takes precedence, the rule or the list of what need not be recorded. Each clarification
can be added, but this makes the rule longer rather than more precise.

Version 4 abandons the question about consequences. It asks what the object is: whether it was installed as part of a package;
whether it is executed; whether a person decided on it as an instruction to the computer; whether a program recorded it itself or a
person created it. The questions are asked in this order, and the first affirmative answer decides.

The four kinds of objects in this formulation are ours. They are derived from two sources. In the first paper, we cited
standards for file placement as a division of state by purpose [1, Section 2.3]; here we use a different part
of the Filesystem Hierarchy Standard—the division of files by whether they change without administrator intervention:
“"Static" files include binaries, libraries, documentation files and other files that do not change without
system administrator intervention. "Variable" files are files that are not static” [13]. The author of Nix divides a service
into programs, static settings and mutable state [7]. What is installed and settings constitute the static part of both
divisions; program records are mutable state. We distinguish the fourth kind, what a person creates: the standard
mentions files in home directories only as shareable between machines and does not distinguish them from other variable files,
while the division of a service into three parts says nothing about user files.

As in version 2, the boundary is not drawn by storage location [2, Section 7.5]: a script in the home directory that
is executed is a program, whereas a document is material, wherever it is located.

Version 4 returns to two open problems of the second paper [2, Section 9], which version 3 considered closed
by the rule with the removal test. Problem O10, the boundary of locked-in code, is resolved by the indicator in Section 8.2: code
is locked in if it cannot itself launch programs or change what is installed and the computer’s settings. Problem O11,
the boundary of rules and program records, is resolved by the third and fourth questions of the same section: a person decides on
a setting, whereas a program makes a record itself.

At the same time, three places where the text of version 3 admitted two readings have been clarified (Sections 4.2 and 4.5). The rule applies to
objects that are on the computer; a command typed by a person is called that person’s action. A line of the declaration
is allowed to take a list from outside it, provided that the source is named in the declaration. A person’s private key and password
are assigned to what a person creates.

## 8. The “Configuration as Law” hypothesis, version 4

### 8.1. Concepts

- **Declaration**—a text recording what the computer should be like: what is installed on it and how it
  is configured. The computer is brought into conformity with this text, rather than the text being compiled from the computer. The declaration consists of
  files that a person has designated as the primary description of the computer; there may be many files, and together they form one
  description.
- **Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing
  programs: the system package manager, package managers of programming languages and of application packages. A general-purpose
  program with a built-in installer counts as an installer in that part of its functionality.
- **Package**—what an installer installs and removes as a whole; in a system that is installed and updated
  as an image, the image is a package.
- **Built-in tool**—a program of the system whose purpose, according to its documentation, includes changing
  what is installed and settings: an installer, account and rights management, the service manager, network and
  access rule configuration. General-purpose programs—an editor, file copying, link creation, the command
  shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.
- **In force.** An installed object is in force if it is on the computer; a program, if it runs or can
  be started. A setting is in force if it has its value. A service is in force if it is enabled; an account,
  if it exists. The required state of a recorded object is stated by its line.
- **Application of the declaration**—an action of the system that brings the computer into conformity with the declaration. The declaration
  in force is the declaration of the last application that the system reported as successful [3, Section 3].
- **Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside
  the built-in tools: by writing directly to files, deleting, or disabling system mechanisms. Breaking is a violation on the
  person’s part rather than a property of the system, and it refutes no property.

### 8.2. What is recorded

Everything that is installed and every setting must be recorded. The rest need not be recorded.

The rule applies to objects that are on the computer. A command that a person typed himself or herself is that person’s
action, not an object. What exists only while the computer runs—a process, an open port, a mount
point, a relationship between services—is not considered a separate object: it belongs to the program or setting
that creates it, and the decision follows that for the program or setting.

What an object is is determined by four questions asked in order; the first affirmative answer decides, and
the clarifications do not change this order.

1. Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as
   received? Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup
   tables, firmware, default setting values, a package containing only dependencies.
2. Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another
   program with that program’s rights? Then it is a **program**, whoever wrote it and wherever it came from; a program
   belongs to what is installed.
3. Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program
   that a person runs for himself or herself? Then it is a **setting**, however it was entered and whatever file
   stores it. Settings are services and their parameters, the network, including saved networks, devices and filesystems,
   time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
   A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something
   or grants access; otherwise it is a record of that program.
4. Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working
   state; if a person created or brought the object, it is **material**—documents, photographs, projects,
   downloaded files, private keys and passwords for logging in to other machines.

Which line records an object.

- What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line
  from which the system itself built or obtained it—a compiled copy, a generated list, a package
  installed as a dependency of a recorded package.
- A setting is recorded by a line of its own; a default value obtained with a package or created during its
  installation is covered by the line of the package.
- A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded
  is the source named in the line.
- What need not be recorded may also be recorded in the declaration.

Clarifications.

- A file containing code that cannot be executed on this computer is not a program.
- Code that runs inside a recorded program and cannot itself launch programs or change what is installed
  and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.
- A program that runs as its own process on the computer, including in a container, is a program.
- A file that a program executes as code counts as code even when it contains setting values; a file
  that a program only reads as values does not count as code.

### 8.3. Properties

The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.
They admit no degrees: a system either has all three properties or it does not. The numbers are kept from earlier versions.

**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.

**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration. Its
tools for installation and configuration record changes in the declaration even when they run with superuser
privileges: an installer does not install a program past the declaration but adds it to the declaration. What is installed
and settings can be changed past the declaration only by breaking.

### 8.4. Consequences

- **Understanding.** The declaration alone, without inspecting the computer, shows what is installed on it and how it is configured.
  For a line that takes a list from outside the declaration, the declaration shows which source determines the list.
- **Reproducibility.** The same declaration on another computer yields exactly the result described in it,
  provided the description is unambiguous. For a line that takes a list from outside the declaration, reproducibility is not claimed.
  Differences explained by hardware are excluded.
- **Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is
  in force unless it is recorded in the remaining lines.

### 8.5. What is not part of the definition

How to store, transfer and remove program records and material. By what mechanism the system prevents execution
of what is not recorded, and how it adds to the declaration what has been installed by a program that itself downloads other
programs. User authority, generations and rollback, protection of the declaration itself and secrets, when an edit
takes effect. The form of the declaration: it may be a list or an algorithm.

### 8.6. How version 4 addresses the gaps of Part I

This is our reasoning, not a check; the check is described in Section 9.

| Gap in Part I | How it is resolved in version 4 |
|---|---|
| Shared content or capability (fonts, translations, themes) | A package or part of one: an installed object; recorded by a line of its own or obtained as a dependency of a recorded package. |
| Lookup tables | The same. |
| Packages containing only dependencies | A package is an installed object, whether it contains files or not. |
| Support for absent hardware | Obtained as part of a package or image: an installed object. |
| Objects that the system recreates | Exist only while the computer runs or are built by the system from what is recorded. |
| A system service setting | A value chosen by a person that the computer as a whole obeys: a setting. |
| A compiled copy of code | A program that the system built from what is recorded; it is covered by the line of the original package. |
| A program’s history that the program executes as code | It is executed, so it is a program; it was not built from what is recorded, so it needs a line of its own. |
| A record that a service was enabled in the past | Recorded by a program as it ran: a program record. |
| A browser extension | An installer built into the browser installs and removes it as a whole: an installed object, recorded. |

## 9. Plan for checking version 4 and failure conditions

This section is fixed before the checks begin and does not change after publication.

### 9.1. General rules

The general rules of Section 4.1 of [3] apply: the three possible outcomes and the procedure for combining them; the independence of the two
classifications and separate adjudication of disagreements; the rule about failure of the testbed; committing inputs to the repository before
the first observation; the prohibition on changing conditions after publication. The objects of checks 1–3 took part in neither the first nor
the second cycle; nor did the machines, except for one specified in Section 9.2.

### 9.2. Check 1: what is recorded

**Aim.** To check that, by Sections 8.1 and 8.2, it can be decided for any object on a real computer what it
is and whether it must be recorded.

**Machines.** Disposable virtual machines with clean installations. Three general-purpose systems that did not take part in
earlier cycles: AlmaLinux, Void Linux, which has no systemd, and Gentoo, which builds programs from source
code; and two systems with an immutable base: openSUSE MicroOS and Talos Linux. Talos Linux was on the list for the second
cycle, but no inventory was obtained from it (Section 4.1), so earlier checks have not seen its objects. Before
the inventory, ordinary actions are performed on the general-purpose systems: installing
a program with the package manager and as an application package; installing a program in the home directory with a programming language
package manager; installing a browser extension; changing a setting of a program that a person runs for himself or herself; enabling
a user service; connecting to a network; a user script in the home directory; running a container.

**Objects.** Two levels, as in [3]: objects in force and stored objects that belong to no package, with
a separate list of executable code outside packages. A machine on which the second-level inventory has not been obtained cannot
yield 1: its outcome is 0 if an object meeting the failure condition below is found on it, and ? otherwise.
The inventory additionally records facts on which the decision depends (Section 9.6): for each package, whether it was installed
explicitly or as a dependency; for each file obtained with a package, whether it has been changed since installation.

**Procedure.** Each object is decided twice, independently: an installed object, a program, a setting, a program record,
material or what exists only while the computer runs; whether the object must be recorded and by which line.

**Failure condition.** On any machine, an object is found for which the text of Sections 8.1 and 8.2 does not allow deciding
what it is and whether it must be recorded, or allows deciding both ways; or the two classifications decided
differently and the adjudication finds no sentence of the text that resolves the dispute.

### 9.3. Check 2: the properties on a testbed

The aim, object, channels, procedure and failure conditions are as in Section 4.3 of [3], with the following differences.

- The testbed has a command shell. A command typed by a person is not considered a channel for bypassing the declaration. A channel is
  anything that such a command tries to leave behind: saving and running a file, registering a service, a timer or an
  autostart, changing a setting. A separate case: a command downloads and executes code without saving it; after
  a reboot, nothing that was executed must be in force.
- The list of ordinary work is extended to include running ordinary commands and one’s own script, recorded in the declaration,
  in the command shell.

### 9.4. Check 3: reproducibility

As in Section 4.4 of [3].

### 9.5. Check 4: existing systems

As in Section 4.5 of [3]: NixOS and GNU Guix System are assessed against each property of version 4.

### 9.6. Order of work

Before publication, the wording of Section 8.2 was tried on objects that earlier checks had already seen: on 4,937
objects sent for adjudication in check 1, in the trial on first-cycle objects and in the inventory of the lived-in machine, and on
fifteen separately described cases. The classification was made independently of the author of the wording, under instructions
that prohibited reading earlier decisions. This is a trial of the wording, not a check of the hypothesis: the text was revised using
the same objects, and its outcome says nothing about new machines. The records are published together with the outcomes.

The first draft of Section 8.2 did not withstand the trial. For 58 objects, the text did not allow deciding; for 542, it allowed
deciding both ways. There were three reasons. The clarification “a file that cannot be executed is material” was worded without
qualification and conflicted with the definitions of a setting and a program record: this accounted for all 542 cases. Programs were
named as requiring recording, but the package as a unit of installation was absent from the text, so a font or a lookup table
installed as a separate package turned out to be material, while 30 packages without files were not defined at all. Finally,
the text said nothing about objects that exist only while the computer runs: relationships between services, mount points,
process groups, references to absent services and communication endpoints; there were 28 such objects.

The second draft—the text of Section 8 of this paper—corrects all three places: the clarification about a non-executable file
is restricted to code, the question about a package became the first question, and a rule about objects that exist only while the computer runs was added. On the same
objects, it yielded no object for which the text fails to decide or decides both ways. For 3,320 objects out of
4,934, the decision depends on a fact missing from the inventories of earlier checks. Most often, provenance is unknown:
whether a package was installed explicitly or as a dependency (1,172 objects); whether an object was obtained with a package and has not been changed since
installation (1,610); whether a setting value was set during installation or changed later (291). For the remaining 247 objects,
something else is unknown: content and purpose (114), the composition of a group of objects (101), executability and rights (29),
lifetime (3). Three objects out of 4,937 were missing from the output of the second classification. During the check of the second
classification, one inventory file was read that no row referred to; after that, 122 decisions
that it could have affected were left unknown. The plan in Section 9.2 requires the inventory to record the first two
facts; the others remain a limitation, and an object with an unknown fact yields ?.

Not checked: whether a system with these properties can serve for everyday work with all of one’s
programs over a long time. Only such a system itself can show this.

## 10. Discussion and limitations

Version 4 was formulated after the results, and its agreement with the gaps of Part I (Section 8.6) proves nothing:
it was written to address them. Only a check on objects it has not seen can provide proof.

Check 1 in the second cycle did not see stored objects outside packages on the desktop systems. That is precisely where
the cases difficult for version 4 are found: a program in the home directory; a setting of a program that a person runs for himself or herself, where the setting launches something;
a setting recorded by a program according to a person’s choice. The plan in Section 9.2 requires an inventory of this level and lists
actions that create such objects.

The boundary of “code inside a program” in version 4 is drawn using one indicator: whether the code can itself launch programs and
change what is installed and the computer’s settings. This is established from the host program’s documentation and from
exactly what it has access to in the case at hand: the same executing program may give the code access to a directory of documents or
a directory of settings. If any of this is not established, the case yields ?.

The questions of version 4 rely on an object’s provenance: whether it was obtained with a package and is unchanged, whether a person chose the value,
whether a program recorded the object. On an ordinary system, some of these facts cannot be recovered from the state of the disk;
the trial in Section 9.6 showed that without them the decision remains unknown for most
objects. In the check, such objects yield ?, not 0, and their share is reported together with the outcome.

Under version 4, a browser extension is an installed object and must be recorded: an installer built into the browser
installs and removes it as a whole. Version 3 classified extensions as settings inside one program.

The definition says nothing about whether a system that meets it is convenient to use.

## 11. Conclusion

Version 3 of the hypothesis did not withstand the first check: the rule that decided an object’s status by a question about the consequences of its
removal does not define what to compare. The assessment of NixOS and GNU Guix System against the three properties succeeded, and these systems have
none of the properties. Whether a system with the three properties can be built remains unchecked.

Version 4 defines directly what is to be recorded: everything that is installed and all settings. We fix the plan for checking it and
the failure conditions and will check it on machines that earlier checks have not seen.

## References

1. Yakymenko, A. (2026). Configuration as Law: A hypothesis on what a declarative operating system is. Preprint,
   18 November 2026; hypothesis, version 1. https://yakyman.com/configuration-as-law-v1.pdf
2. Yakymenko, A. (2026). Testing the “Configuration as Law” Hypothesis: Results of the First Cycle and a Second Version.
   Preprint, 20 November 2026. https://yakyman.com/configuration-as-law-v2.pdf
3. Yakymenko, A. (2026). Testing the “Configuration as Law” Hypothesis, Version 3: Hypothesis, Checks, and Failure Conditions Fixed Before the Checks.
   Preregistration, 21 November 2026.
   https://yakyman.com/configuration-as-law-v3.pdf
4. Records of the checks. https://github.com/Yakyman/configuration-as-law
5. Anderson, P., Couch, A. (2004). What Is This Thing Called System Configuration? Talk, LISA 2004.
   https://usenix.org/legacy/publications/library/proceedings/lisa04/tech/talks/couch.pdf
6. Traugott, S., Brown, L. (2002). Why Order Matters: Turing Equivalence in Automated Systems Administration.
   LISA 2002. https://www.usenix.org/legacy/events/lisa02/tech/full_papers/traugott/traugott_html/index.html
7. Dolstra, E. (2006). The Purely Functional Software Deployment Model. Dissertation, Utrecht University,
   p. 15. https://edolstra.github.io/pubs/phd-thesis.pdf
8. NixOS Manual, section Package Management. Accessed 22.11.2026.
   https://nixos.org/manual/nixos/stable/
9. Dolstra, E., Löh, A., Pierron, N. (2010). NixOS: A Purely Functional Linux Distribution. Journal of Functional
   Programming. https://www.cs.tufts.edu/~nr/cs257/archive/andres-loeh/nix-os-jfp.pdf
10. NixOS, nixos/modules/config/users-groups.nix, option users.mutableUsers.
    https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/config/users-groups.nix
11. GNU Guix Reference Manual 1.5.0, sections User Accounts and Invoking guix package.
    https://guix.gnu.org/manual/1.5.0/en/html_node/User-Accounts.html;
    https://guix.gnu.org/manual/1.5.0/en/html_node/Invoking-guix-package.html
12. Kubernetes documentation. Kubernetes Object Management.
    https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/
13. Filesystem Hierarchy Standard, version 3.0 (2015), chapter 2.
    https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch02.html

## Records of the second-cycle checks

The records are dated 22 November 2026 and are published in the repository of records [4]. Paths are given from the root of the
repository.

- The text of version 3 and the numbering of its sentences used in the checks; matches the published text
  [3]. configuration-as-law/records-v3/TEXT.md; configuration-as-law/records-v3/SENTENCES.md
- Release numbers and inputs to the checks, committed before the first observation. Published before the checks:
  configuration-as-law/check-inputs-v3
- Trial of the wording on first-cycle objects: comparison of the two classifications, confirmed gaps and
  a check of the outcome. configuration-as-law/records-v3/A1/RESULT.md; configuration-as-law/records-v3/A1/compare/STATS.md;
  configuration-as-law/records-v3/A1/REVIEW-A1-H-3.md
- Check 1: outcome, comparison of the two classifications by machine, adjudication of disagreements, established rows for the five kinds of
  gaps and the review. configuration-as-law/records-v3/D1/RESULT.md; configuration-as-law/records-v3/D1/compare/STATS.md;
  configuration-as-law/records-v3/D1/adjudication/rows.tsv; configuration-as-law/records-v3/D1/adjudication/HOLES.md;
  configuration-as-law/records-v3/D1/fix-d1-h-2/confirmed-rows.tsv; configuration-as-law/records-v3/D1/REVIEW-D1-H-3.md
- Check 1: inventories of four machines, a record of the completeness of collection and a record of collection being stopped on Talos Linux.
  configuration-as-law/records-v3/D1/in/READY.md; configuration-as-law/records-v3/D1/in/part-fedora.tsv; configuration-as-law/records-v3/D1/in/part-tumbleweed.tsv;
  configuration-as-law/records-v3/D1/in/part-mint.tsv; configuration-as-law/records-v3/D1/in/part-flatcar.tsv;
  configuration-as-law/records-v3/D1/in/control/talos/termination.json
- Testbed: description, records of four rounds of construction and acceptance records. configuration-as-law/records-v3/B2/STAND.md;
  configuration-as-law/records-v3/B2/BUILD-1.md; configuration-as-law/records-v3/B2/BUILD-2.md; configuration-as-law/records-v3/B2/BUILD-3.md; configuration-as-law/records-v3/B2/BUILD-4.md;
  configuration-as-law/records-v3/B2/raw/round-4/REVIEW-4.md
- Check 4: outcome, two independent assessments of NixOS and GNU Guix System with experimental records and excerpts from
  documentation, review. configuration-as-law/records-v3/D4/RESULT.md; configuration-as-law/records-v3/D4/REVIEW.md;
  configuration-as-law/records-v3/D4/c1/ASSESS.md; configuration-as-law/records-v3/D4/c1/cases.tsv; configuration-as-law/records-v3/D4/c2/ASSESS.md;
  configuration-as-law/records-v3/D4/c2/cases.tsv
- Reading the text of version 3 for contradictions: seven cases and their check. configuration-as-law/records-v3/A2/CARDS.md;
  configuration-as-law/records-v3/A2/VERIFY.md
- Inventory of the lived-in machine: reduction of rows, comparison of the two classifications, confirmed gaps and review.
  configuration-as-law/records-v3/A3R/RESULT.md; configuration-as-law/records-v3/A3R/compare/STATS.md; configuration-as-law/records-v3/A3R/in/REDUCTION.md;
  configuration-as-law/records-v3/A3R/REVIEW-A3R-H-3.md
- Analysis, from documentation, of 88 ways of bypassing the declaration, and its review. configuration-as-law/records-v3/B1/CHANNELS.md;
  configuration-as-law/records-v3/B1/REVIEW-B1-3.md
- Trial of the wording of version 4 on previously seen objects: the texts of the two drafts, instructions, input tables,
  decisions for each object and for the fifteen cases, lists of unresolved cases and unknown facts.
  configuration-as-law/trial-v4/round-1/PAGE.md; configuration-as-law/trial-v4/round-1/TASK.md; configuration-as-law/trial-v4/round-1/CASES.md; configuration-as-law/trial-v4/round-1/in/rows-d1.tsv; configuration-as-law/trial-v4/round-1/in/rows-a1.tsv;
  configuration-as-law/trial-v4/round-1/in/rows-a3r.tsv; configuration-as-law/trial-v4/round-1/out/rows-d1.tsv; configuration-as-law/trial-v4/round-1/out/rows-a1.tsv; configuration-as-law/trial-v4/round-1/out/rows-a3r.tsv;
  configuration-as-law/trial-v4/round-1/out/SUMMARY.md; configuration-as-law/trial-v4/round-1/out/HOLES.md; configuration-as-law/trial-v4/round-1/out/CASES-ANSWERS.md; configuration-as-law/trial-v4/round-2/PAGE.md;
  configuration-as-law/trial-v4/round-2/TASK.md; configuration-as-law/trial-v4/round-2/out/rows-d1.tsv; configuration-as-law/trial-v4/round-2/out/rows-a1.tsv; configuration-as-law/trial-v4/round-2/out/rows-a3r.tsv;
  configuration-as-law/trial-v4/round-2/out/SUMMARY.md; configuration-as-law/trial-v4/round-2/out/HOLES.md; configuration-as-law/trial-v4/round-2/out/UNKNOWN.md;
  configuration-as-law/trial-v4/round-2/out/CASES-ANSWERS.md; configuration-as-law/trial-v4/round-2/out/REVIEW.md
