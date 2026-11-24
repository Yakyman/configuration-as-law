# The “Configuration as Law” Hypothesis: Results of the Checks of Version 4, and a New Plan for Checking It

Arthur Yakymenko

Preprint · 23 November 2026 · Part II fixes the plan for checking version 4 on a reference implementation before that
check begins; after publication, the plan does not change

## Abstract

In the fourth paper [4], we fixed version 4 of the “Configuration as Law” hypothesis—a definition of a declarative
operating system through three properties—and four checks with failure conditions. This paper consists of two parts.
In Part I, we report the outcomes strictly under the fixed conditions. The check of the rule “what is recorded” on
clean installations of AlmaLinux, Void Linux, openSUSE MicroOS and Talos Linux yielded outcome 0: among 16,375
objects, three kinds of objects were confirmed for which the text decides both ways or does not decide. Work beyond
the plan and a supplement of eight steps confirmed further gaps of the text and showed that one of the stated
consequences does not follow from the properties. The assessment of NixOS and GNU Guix System yielded outcome 1: both
could be assessed, and they have none of the three properties. The checks of the properties on a testbed and of
reproducibility were again not conducted: the testbed was not accepted. We list every departure from the plan.
Part II is formulated after the results. In it, we note that the check which has yielded 0 in all three cycles
answers whether the wording decides every object of an inventory, and that the question whether a system meeting the
definition can be built, which has been part of the plan since the first paper, has not been answered. We leave the text
of version 4 unchanged, withdraw the first check from the plan, and fix a new plan: a reference implementation built
from the text of the hypothesis as its specification, with an outcome for each property and each consequence.

Keywords: declarative configuration, configuration management, operating systems, check conditions fixed in advance,
reference implementation.

## 1. Introduction

We investigate the question: what is a declarative operating system, and what properties must it have?

In the first paper [1], we proposed version 1 of the hypothesis and fixed five checks. In the second [2], we reported
their outcomes—the census of objects yielded 0, the other checks yielded ?—and set out version 2. In the third [3], we
changed the definitions before any check, producing version 3, and fixed four checks. In the fourth [4], we reported
the outcomes for version 3—check 1 yielded 0, check 4 yielded 1, checks 2 and 3 were not conducted—and set out
version 4 with a plan for checking it.

This paper has the same two parts as the second and the fourth. Part I reports the outcomes of the checks of version 4
under the conditions fixed in [4], without new rules or thresholds. Part II is formulated after the results. It
differs from the earlier second parts in one respect: it does not contain a new version of the hypothesis. The
definitions of version 4 are not changed. What changes is the plan by which the hypothesis is checked.

Table 1. Versions of the hypothesis and their checks.

| Version | Where set out | What was checked | Outcome |
|---|---|---|---|
| 1 | [1] | five checks [2] | census 0; the others ? |
| 2 | [2], Part II | not checked: replaced by version 3 before the checks | — |
| 3 | [3] | four checks [4] | check 1—0; check 4—1; checks 2 and 3 not conducted |
| 4 | [4], Part II | four checks, this paper, Part I | check 1—0; check 4—1; checks 2 and 3 not conducted |
| 4 | unchanged | plan in Section 9 of this paper | — |

## 2. What was checked

### 2.1. The hypothesis, version 4

The full text of version 4 is given in [4], Section 8. A declaration is a text recording what the computer should be
like: what is installed on it and how it is configured; the computer is brought into conformity with this text,
rather than the text being compiled from the computer. Everything that is installed and every setting must be
recorded; the rest need not be. What an object is, is determined by four questions asked in order: whether it is an
installed package or part of one that remains as received; whether it is code that the computer executes or can
execute; whether it is a value chosen by a person that the computer as a whole obeys; otherwise it is a program
record or a person’s material. There are three properties. P1, Completeness: everything that is installed and every
setting, when in force on the computer, are recorded. P2, Guarantee: everything recorded is in force as its line
requires. P4, Law: the system provides no ordinary path for changing what is installed and settings past the
declaration. Three consequences are stated: Understanding, Reproducibility and Removal.

### 2.2. Four checks and their failure conditions

The conditions are quoted verbatim from [4], Section 9, and, where that section refers to it, from [3], Section 4.

Check 1, what is recorded. “On any machine, an object is found for which the text of Sections 8.1 and 8.2 does not
allow deciding what it is and whether it must be recorded, or allows deciding both ways; or the two classifications
decided differently and the adjudication finds no sentence of the text that resolves the dispute.”

Check 2, the properties on a testbed. “At least one channel installs, launches, or changes something that must be
recorded although it is not recorded, and this is not breaking (P1, P4); a built-in tool, including with superuser
privileges, changes such a thing past the declaration (P4); after a completed application, at least one line is not
fulfilled (P2); after application of a declaration without a line, something the line contributed and the remaining
lines do not cover is in force (Removal, P1).” A separate condition concerns ordinary work: “An ordinary action from
the list above cannot be performed through the declaration and its built-in tools.” Under [4], Section 9.3, the
testbed has a command shell, and a command typed by a person is not a channel; a channel is anything that such a
command tries to leave behind.

Check 3, reproducibility. “What is in force under the lines of the declaration differs between the two machines, and
the difference is not explained by hardware.”

Check 4, existing systems. “A case yields 1 when both assessments reach the same decision, “has” or “does not have”,
with sufficient information, or when they differ and the adjudication resolves the dispute by a sentence of the text;
? when the information is insufficient; 0 when the information is sufficient but the text of the hypothesis does not
allow deciding whether the system has the property, or when the two assessments differ and the adjudication finds no
sentence of the text that resolves the dispute.”

### 2.3. General rules, the order of the checks and the supplement

The general rules of [3], Section 4.1, apply. The outcome of a check is 1, 0 or ?; it combines its cases: 0 if any
case yields 0; otherwise ? if any case yields ?; otherwise 1. The two classifications are independent, and their
disagreement is considered by a separate adjudication. A failure of the testbed yields 0 only if a written argument
shows that it follows from the definitions alone; otherwise it is a defect of the testbed, and the case yields ?. Each
case is attempted once. The concrete inputs are committed to the repository of records [5] before the first
observation.

Two further texts were published in the repository before the observations they govern. The order of the checks
(committed on 23 November 2026 at 05:35 UTC) states that the outcome of each check is determined by the conditions of
[4] alone; it adds a procedure that assigns every gap found one of two weights, “gap in the wording” or “gap in the
idea”, eight cases with a decision known in advance on which this procedure must first be tried, and three
investigations beyond the plan. Supplement 1 (23 November 2026) adds eight steps, each with its inputs and expected
result recorded before its first observation, except the files named in Section 5. Neither text changes the four
checks or their failure conditions.
Supplement 1 states: “a confirmed gap means that version 4 did not withstand the checks, and a correction will be a
new version.”

# Part I. Results of the checks of version 4

## 3. How the checks were conducted

The checks ran on 23 November 2026 (UTC) under the text of [4], published before they began. The order of the checks
was committed to the repository of records at 05:35 UTC; the inputs of checks 1 and 4 and of the investigations
beyond the plan—the release numbers, the installation recipes, the commands for ordinary actions, the program that
compiles the inventory—at 11:10 UTC, with a correction of one checksum entry at 11:14 UTC, before the first
observation. Supplement 1 and the inputs of its steps were committed between 13:12 and 18:45 UTC, each before the
work on the step concerned, except the files named in Section 5. Before the first observation, the instruments were rehearsed on disposable copies of the
systems; what these rehearsals exposed is recorded in the file of disclosures published with the inputs. The failure
conditions did not change after publication; no new classification rules or agreement thresholds were introduced.
The departures from the plan are listed in Section 5.

The systems of check 1 were AlmaLinux 10.3, Void Linux (installation image 20250202), Gentoo (stage 3 of
22 November 2026), openSUSE MicroOS (snapshot 20261121) and Talos Linux 1.14.6. The systems of check 4 were
NixOS 26.05 and GNU Guix System 1.5.0.

## 4. Outcomes of the checks

### 4.1. Check 1: what is recorded. Outcome 0

Inventories were obtained on four of the five machines. The Gentoo machine failed to start in its single prescribed
attempt; no action and no collection ran on it, and it yields ?. On Talos Linux the second level of the inventory was
obtained only in part, and 43 rows remain with an unknown fact; no counterexample was confirmed on it, and it yields ?.
On MicroOS the second level was also partial: the active subvolume that holds the configuration directory was not
traversed.

Table 2. Check 1 by machine.

| Machine | Objects | In force | Stored | Matching decisions | Share | Cohen’s kappa | Outcome |
|---|---:|---:|---:|---:|---:|---:|:---:|
| AlmaLinux | 6,293 | 4,605 | 1,688 | 5,065 | 80.49% | 0.747 | 0 |
| Void Linux | 3,282 | 1,214 | 2,068 | 1,701 | 51.83% | 0.473 | 0 |
| Gentoo | — | — | — | — | — | — | ? |
| openSUSE MicroOS | 6,522 | 1,452 | 5,070 | 1,683 | 25.80% | 0.182 | 0 |
| Talos Linux | 278 | 225 | 53 | 228 | 82.01% | 0.552 | ? |
| Total | 16,375 | 7,496 | 8,879 | 8,677 | 52.99% | 0.459 | 0 |

The two classifications gave a valid decision for every object. They gave the same decision for 8,677 objects of
16,375. The remaining 7,698 objects and ten objects with a matching mixed decision, 7,708 in all, went to
adjudication. The adjudication marked 5,994 rows as resolved by the text, 350 as depending on an unknown fact, and
1,364 as gaps, grouped in five kinds.

The outcome follows from two clauses of the failure condition.

Under the second clause, 1,362 of the rows marked as gaps are rows on which the two classifications differ and the
adjudication found no resolving sentence: 179 on AlmaLinux, 1,126 on Void Linux and 57 on MicroOS. These rows are of
two sorts. In 1,267 of them, one classification answered that a fact was unknown and the other gave a decision. In
95—59 on AlmaLinux, 21 on Void Linux and 15 on MicroOS—both classifications gave a decision and the decisions differ.
Under the plan, all 1,362 rows meet the second clause. The verification, whose task contained a step outside the
plan (Section 5), found that 1,068 of them belong to a kind that depends on a fact the inventory does not hold, and
213 to a kind that it rejected by the text; 73 of the remaining 81 rows, present on each of the three machines, are
confirmed members of the three kinds below.

Under the first clause, a separate verification of the five kinds confirmed three, rejected one by the text, and
left one, with 1,068 rows, depending on a fact that the inventory does not hold. The three confirmed kinds follow;
together they cover 111 distinct rows, or 113 if two downloaded copies of the browser extension are counted, as the
last review holds they should be.

1. **A list that the system generated from installed packages**—the loader cache, the lists of kernel module
   dependencies, the database of file types. The fourth question of Section 8.2 calls a cache written by a program a
   program record, which need not be recorded; the rule on lines in the same section names “a generated list” among
   what is installed and is recorded by the line from which the system built it. The text does not say which
   sentence prevails. 100 rows: 38 on AlmaLinux, 28 on Void Linux, 34 on MicroOS.
2. **A stored archive whose contents are executed**—the initial boot archive. The computer unpacks it and executes
   what it contains. The text does not say whether the stored archive is itself code that the computer executes, in
   which case it is a program and is recorded, or data from which code is taken, in which case it is a program
   record. Nine rows: four on AlmaLinux, four on Void Linux, one on MicroOS.
3. **An installed package whose code runs only inside its program**—a browser extension installed in a profile. The
   first question makes it an installed object, which must be recorded; the clarification about code that runs inside
   a recorded program and cannot itself launch programs or change what is installed and settings says that such code
   need not be recorded. Two rows: one on AlmaLinux, one on Void Linux.

Limits of this result. First, the facts that the decisions depend on are missing for 2,007 identified rows: for 937
rows, the adjudication or both classifications recorded an unknown fact, and the verification added 1,070 rows,
chiefly files left by an earlier kernel version on Void Linux, whose package origin and unchanged state are not
established. Second, for 220 rows of the original gaps, the verification did not complete a decision row by row.
Third, the last review of the result disagrees with the report on three points that do not change any outcome: two
downloaded copies of the browser extension were excluded from the second kind on a reading the review does not
accept; rows of one inactive system generation on MicroOS were decided by two different standards; and the
reasons stated in the table of machines were not updated for the first and third kinds. Fourth, step 2 of the
supplement decided the first and the third kind anew with all the facts it could collect, and did not confirm them:
both families yielded ? there, because deciding facts were still missing (Section 4.6). Fifth, the task of the
verification contained a step that the published plan does not have; this is listed in Section 5.

### 4.2. Check 2: the properties on a testbed. Not conducted

The testbed of the second cycle had been built for the strict reading of version 3 and had no unrestricted command
shell [4, Section 4.2]. For version 4, it was rebuilt with an ordinary command shell and with built-in tools that record
changes in the declaration. The 78 closures of ways of bypassing the declaration reported in [4] were kept as a
historical record and not carried over: all 88 ways were marked as not validated for version 4. Two rounds of
construction followed. After them, two of the 88 ways were closed, and the testbed was not accepted. Check 2 did not
begin and has no outcome.

Parts of the testbed were used, as bounded images, in steps 5, 6 and 8 of the supplement (Section 4.6). Those steps
are not check 2, and their outcomes are not its outcome.

### 4.3. Check 3: reproducibility. Not conducted

Check 3 requires an accepted testbed. It did not begin and has no outcome.

### 4.4. Check 4: existing systems. Outcome 1

NixOS and GNU Guix System were assessed against each property twice, independently. In all six cases, both
assessments reached the same decision with sufficient information: the system does not have the property. The review
agrees. Under the condition of the check, the conclusion “does not have” is a successful assessment, so each case
yields 1.

Table 3. Check 4.

| System | Property | Decision of both assessments | Decisive fact |
|---|---|---|---|
| NixOS | P1 | does not have | The option `users.mutableUsers` is enabled by default; the manual describes creating accounts with the ordinary `useradd` command. Such an account is in force without a line. |
| NixOS | P2 | does not have | After a successful application, an account-management command removed a recorded group membership of an account; the declaration stayed the same. |
| NixOS | P4 | does not have | The account-management commands are a documented ordinary path that changes accounts past the declaration. |
| Guix System | P1 | does not have | The manual describes accounts created with `useradd`, which are lost at the next reconfiguration or reboot; until then they are in force without a line. |
| Guix System | P2 | does not have | After application, an account-management command removed a recorded group membership. |
| Guix System | P4 | does not have | The same commands change accounts past the system declaration. |

The decisive facts for P1 and P4 come from documentation and release sources; for P2 they were also obtained on
clean installations of both systems. The facts about accounts sufficed in each case; the arguments about package
installation into user profiles, which were decisive in [4], were not needed.

### 4.5. Work beyond the plan

This work was announced in the order of the checks and does not contribute to the outcome of any check.

- **Contradictions within the text.** The reading of the sentences of Sections 8.1–8.3 against one another produced
  no case of its own. Its verification found and confirmed one collision: for an installed browser extension, the
  sentence that everything installed must be recorded and the clarification that code running inside a recorded
  program need not be recorded both apply literally and prescribe opposite duties, and no sentence says which
  prevails. This is the third kind of Section 4.1, found here by reasoning. Of the planned comparisons, 340 pairings
  with Section 8.3 were not carried out.
- **Ways of installing and configuring.** For each of the 88 ways examined in [4], it was decided from the text of
  version 4 what the way leaves behind and what that is. For 53 ways the text decides; for eight it decides both
  ways; for 27 a fact is unknown; for none does it fail to decide. The review agrees.
- **Lived-in machines.** Three disposable machines were prepared as a developer’s workstation, a gaming computer with
  a game store, and a server with containers. Of 39,382 objects, 24,249 were compared after grouping; the two
  classifications matched on 3,007 (12.40%; Cohen’s kappa 0.115). Four kinds of gaps were confirmed: the history of a
  fetched repository, which fits both branches of the fourth question; values that a program generated and that the
  computer obeys, such as firewall rules written by a container engine, while the third question speaks of a value
  chosen by a person; files of values whose entries include commands that are executed, such as a schedule file; and
  container images, for which the text does not say whether the tool that obtains them is an installer. The
  adjudication had named seven kinds; the verification confirmed these four, rejected two—among them the own files
  of a client program that installs and updates itself, with most of the rows marked as gaps—and split one. The last
  review of this result disagrees with the report on the extent of the fourth kind, on two citations and on one line
  reference.
- **Weighting of gaps.** Of the eight cases with a decision known in advance, two received a different decision. For
  the compiled copy of code, one party found no gap under version 3 and gave no answer about the meaning, and the
  procedure returned “gap in the idea” where “gap in the wording” was expected. For the browser extension, one party
  found a gap where the order of the checks expected none; check 1 then confirmed a gap for objects of this kind,
  its third kind. Under the order of the checks, weighting then does not begin. Weights were nevertheless computed
  for the gaps of check 1 and of the lived-in machines, contrary to the order; they are published as such and are
  not used in this paper.

### 4.6. The supplement: eight steps

Table 4. Outcomes of the steps of Supplement 1.

| Step | What was done | Outcome | Expected result recorded in advance | Last review |
|---|---|---|---|---|
| 1 | By reasoning, two states of a computer under one declaration were sought in which the three properties hold | Understanding 0; Reproducibility ?; Removal ? | met in part: the pair was found for accounts that the declaration requests, not for values that nobody requested | agrees |
| 2 | Fifteen families of disagreements decided anew with all available facts; a sample of 600 agreements | six families 0, nine ?; in the sample, 582 agreements established, 16 undetermined, two do not follow from the text | met in part: of six families expected to yield two decisions or none, two did and four yielded ?; the family expected to yield one decision yielded ? | agrees |
| 3 | What must hold at each moment of an update; a list taken from a server when there is no network | ? and ? | not met | disagrees on one listing; outcomes kept |
| 4 | The facts missing after check 1; a new inventory of Gentoo | AlmaLinux ?; Void Linux 0; Gentoo 0; MicroOS ?; Talos Linux 0 | two of three clauses met | agrees |
| 5 | One image on which seventeen cases were performed: fifteen ways of running saved code, an account tool run as superuser, ordinary work | one case 1; sixteen ? | neither of two met | agrees |
| 6 | Reproducibility and removal on a rebuilt image of the same design | four cases 1; one ? | met | agrees |
| 7 | The procedure of weighting tried on ten cases with a known answer | 0 for the procedure | two of four met | agrees |
| 8 | Four longer histories: updates, development, a game, loss of network | ? in all four | one of three met | disagrees on the limits stated; outcomes kept |

Step 1. A pair of states was constructed. A declaration has three lines: a base line that fixes a rule of
allocation—the least unused of two permitted numeric identifiers at the moment an account is created—and two lines
that each install a package and request an account. On one computer the first package is installed first, on the
other the second. Both computers satisfy the three properties under the same declaration, and the identifiers of the
two accounts are exchanged. The declaration does not show which identifier an account has. Understanding, as worded
in [4], Section 8.4, therefore does not follow from the three properties. For Reproducibility, the result depends on
what “unambiguous” means for a line that leaves a value to the installation; for Removal, on whether an account that
a package created, and that nobody chose separately, must disappear with the line of the package. Both remain ?.

Step 2. Six families yield 0: a stored archive whose contents are executed; the history of a repository fetched at a
person’s command; container images and containers; package contents held in an installer’s own store, such as the
sources that a language tool downloads; code that an installed program copies or generates as it runs, such as a copy
of a file supplied with a package or links created at start; and files of values whose entries include commands that
are run. The two agreements of the sample that do not follow from the text concern a second name that an
installation created for a file of a package: the text does not say whether “obtained as part of a package” follows
the content of a file or its name and place. Several results of this step run against results reported above, on
the same objects. The family of generated lists and the family of browser extensions, confirmed as gaps in check 1,
yield ? here: no pair of decisions was established, because deciding facts were missing. The same holds for the
family of values that a program generated, confirmed as a gap on the lived-in machines. Within the family of
containers, the four container images received one decision each, whereas the lived-in machines confirmed container
images as a gap; the 0 of the family comes from one stored container, which is a program under one sentence and a
set of service values under another. The family of package contents in an installer’s store yields 0 on rows for
which the verification of the lived-in machines had found the premise of the gap factually wrong. And the family of
code that a program copies or generates yields 0 on rows that are examples of a kind which that verification
rejected.

Step 4. The Gentoo inventory was obtained: 32,775 objects. The two classifications matched on 5,074 of the 34,708
objects of the step (14.62%). Two kinds of gaps were found in 37 rows. One is container images, as on the lived-in
machines. The other is a stored archive of code that nothing executes as it is—a downloaded or cached archive of
sources or of a package, a downloaded copy of a browser extension, a layer of a container image. It is related to the
second kind of Section 4.1 but is not the same: there the contents of the archive are executed, and the verification
of check 1 excluded downloaded copies, which is the point its last review disputes. Whether this kind is new was not
established; the last review notes that an object of this kind was present in an inventory of check 1. The rows of
AlmaLinux were not delivered to the classifications (Section 5), and that machine yields ?.

Step 5. All seventeen cases ran. The ordinary work—ordinary commands in the command shell, one’s own recorded
script, installing and running a package, use of the network, a text browser, editing a document—succeeded in one
session and yields 1; the page was fetched over a network configured when the image started, and no network was
joined in the session. None of the fifteen ways of running saved code was refused. On this image, a
service writes every file saved under five designated directories—the home directory, two directories for temporary
files, the shared-memory directory and the configuration directory—into a text designated as part of the
declaration, before the file can be read; in every case the saved code was therefore covered by such a text before
it ran. The first version of each such text was made by importing the directory as it already was. Whether a file
can be saved outside these directories was not established; on the image of steps 6 and 8, files written elsewhere
by the package installer were not recorded. Whether a text that the system writes from what is saved is a
declaration in the sense of [4], Section 8.1, was left to the author, and the sixteen cases yield ?.

Step 6. The same declaration applied to two independent clean installations left no difference in any value stated by
a line that can be read back from inside the machine. Two packages installed in opposite orders, with the account
identifiers stated in the declaration, gave the same accounts on both machines. After the lines of a program, a
service and a rule were removed and the declaration applied, the former process did not exist, the service was
unknown to the service manager, the rule was absent, and the executable could not be started from its path. A shared
package stayed while its second owner remained recorded and was gone when that owner was removed. The case in which
the identifiers are not stated could not be expressed: the declaration format of the image requires them. These four
cases yield 1, and the fifth yields ?. Two limits apply: a line that fixes the boot order and a requirement stated in
prose cannot be verified from inside a machine, and after the removal the copy of the executable that the image keeps
for execution was checked only by the image’s own verifier.

Step 7. On ten cases whose answer is given in [4], Section 8.6, two parties answered separately whether the object
must be in the declaration. They gave the same answer in eight cases; in six, that shared answer equalled the known
one under the comparison rule of the step. Each party separately equalled the known answer in seven cases. In two of
the cases in which the shared answer was counted as different from the known one, both parties named coverage by the
line of the package that supplied the object, where the table of Section 8.6 names a line of the object’s own or its
status as a dependency of a recorded package. A third party, shown ten known answers and ten opposite ones without
labels, accepted two of the known answers and rejected all ten opposite ones. Under the rule of the step, the
procedure of weighting yields 0. This outcome does not depend on the comparison rule: in two cases the two parties
gave different answers, and one such case alone counts against the procedure. The step ran under one of two readings of which
procedure the supplement means, and its second half, a trial on cases known to be wrong, was not attempted
(Section 5).

Step 8. In the first history, an update performed with the tool of the image was applied and, after a restart, no
line was found unfulfilled among the comparisons made. A second update was then performed with the system package
installer run directly as superuser: the package changed past the declaration, was in force unrecorded, and the line
of the package was unfulfilled until the next restart, after which the image restored the recorded version. That the
second update did not last beyond the restart is recorded as a question about ordinary work, and several files that
this history left behind remain undecided for want of a fact. In the development history, all eighteen actions were completed and no observation against the properties was found; what
the comparisons covered was not established. In the game history, fifteen packages were installed past the
declaration by the same direct use of the installer, one line of the declaration was then unfulfilled for two files
that the installer had rewritten, and the game could not be installed because its launcher failed. In the network
history, an installation interrupted by a loss of network failed; one line of the declaration, for a network port,
was unfulfilled after the last completed application; and after the network returned no new session could be opened,
so the history could not be continued. The inputs of the step say that this installation need not fail merely
because the network is down; whether its failure counts against ordinary work depends on a reading that the record
leaves open. No written argument shows that any system with the three properties would fail these histories; under
the general rules, these are defects of the testbed, and all four histories yield ?. The last review of the record
holds that the comparison of lines with the state of the machine was less complete than the record says.

## 5. Departures from the plan

Table 5 follows the form recommended for reporting deviations from a fixed plan [7]: what was planned, what was done,
why, and what it means for reading the results.

Table 5. Departures from the plan.

| What was fixed | What was done | Why | Effect on the results |
|---|---|---|---|
| Each of the five systems of check 1 is inventoried | Gentoo did not start in its single attempt; no inventory | The cause was not established in the record of the attempt | Gentoo yields ? in check 1. A new inventory was taken in step 4 under a new name; it does not replace the attempt |
| The outcome of check 1 follows from the two classifications and the adjudication | The task of the verification added a step that tried to refute the kinds of gaps | Our error in writing the task | The review identified the step. The outcome is reported from the adjudication, as the plan requires, and is 0 with or without that step |
| The inputs are committed before the first observation | One checksum entry of the inputs was wrong | Our error | Corrected by a public commit before the first observation |
| The eight cases of the order of the checks have known decisions under its own procedure; if one receives a different decision, weighting does not begin | Two received a different decision; weights were computed all the same | The cases were not tried on the procedure before publication; for the browser extension, check 1 contradicts the expected decision, and step 2 did not confirm the gap (Section 7.4) | The weighting was done contrary to the order. No weight is used |
| Supplement 1 and the inputs of its steps are fixed before the work | There were nine reviews of nine texts before publication: the inputs of steps 1 and 3 were reviewed together and those of step 2 twice; all nine disagreed; the corrected texts were published without a review that agreed | The work on the steps was not held back for a further review | The published inputs carry corrections that no review confirmed |
| Rules of the supplement: gaps in the wording and gaps in the idea are reported in two separate lists | Steps 1 and 3 made the two lists, without the weighting of the order of the checks; steps 2 and 4–8 put no gap into either list | After the cases with a known decision failed, the inputs of step 2 left to the author whether the lists are made; the inputs of steps 4, 5, 6 and 8 put no gap into either list until the author answers, and the inputs of step 7 put none into a list | No gap of this paper carries a weight |
| Step 7: the procedure is tried on cases known to be right and on cases known to be wrong | The half with cases known to be wrong was not attempted; the step ran under one of two readings of which procedure is meant | The published text names no such cases | The outcome of step 7 holds for that reading only |
| Step 5: the image is validated by its builder before the cases | The builder’s validation ended with an error in one carried-over test | A kind of file that the image cannot create | The cases were performed on this image all the same |
| Step 6: inputs recorded before the first observation | Of 181 files fixed by checksum, 89 were published before the attempts; 92, including the programs that performed the cases, were not | The publication was not compared with the list of fixed files | The texts of the cases, the comparison queries and the declarations were public in advance; the programs were not |
| Step 8: the same | Of 198 files fixed by checksum, 41 were published before the attempts | The same | The same |
| Step 4: the rows of all five machines are delivered to both classifications | 5,711 rows of AlmaLinux were not delivered: the copying program stopped at a field longer than its limit | A defect of the program, not tried beforehand on the full AlmaLinux inventory; the published rule of the hand-over said that a failed copy is not repaired | AlmaLinux yields ? in step 4 |
| Step 4: the classifications do not see earlier decisions | The list of documents prepared for them named three files with the earlier explanations of which fact was missing for each object; the files were removed from the list before the inventories were taken | Our error in preparing the hand-over; the last review of the instrument identified it | The removal was not reviewed, so the instrument of collection stands as not accepted after four reviews. The outcomes of step 4 were accepted by their own review |
| Step 4: both parties answer what each gap means | For the 37 rows of gaps, the answers of one party are absent for all rows and of the other for 24 | The tasks asked only the party that had named a gap | The gaps of step 4 are reported without these answers |
| The fixed ordinary actions are performed on every machine | One download failed on the gaming machine and was not repeated; in step 4 the installation of a browser extension failed on Gentoo | Not established | Objects that these actions would have left are absent from those inventories |
| Contradictions: every pair of sentences of Sections 8.1–8.3 | 340 pairings with Section 8.3 were not made | The task omitted them | The search for contradictions does not cover Section 8.3 |
| In the working list of the checks, not in a published text: the testbed is tried by a party that did not build it | Both starts of this work were stopped at once, and it was not continued | The means chosen for this work did not accept it: both starts were stopped by that means before any attempt on the testbed. The cause lies in the means and not in the testbed. It was not worked around, no other means was tried, and steps 5 and 6 of the supplement took the place of this work | No attempt to bypass the testbed was carried through |
| Reports are accepted by a separate review | The last reviews of check 1, of the lived-in machines, of step 3 and of step 8 disagree with the reports | The points of disagreement were not corrected before this paper | The reviews keep every outcome. The points are named in Sections 4.1, 4.5, 4.6 and 6 |

## 6. Summary and limits of the conclusion

Table 6. Outcomes of the checks of version 4.

| Check | Outcome |
|---|:---:|
| 1. What is recorded | 0 |
| 2. The properties on a testbed | not conducted |
| 3. Reproducibility | not conducted |
| 4. Existing systems | 1 |

Version 4 did not withstand check 1. Table 7 lists the gaps of the text that the records report on objects of the
inventories and on the 88 ways, with the result of step 1 on Understanding, by the place of the text concerned, and
says where each was confirmed and where it was not. The gaps in the wording that steps 1 and 3 list from reasoning
about the text follow the table.

Table 7. Gaps of the text of version 4 reported on objects and on the 88 ways, and the result of step 1 on
Understanding.

| Place in [4], Section 8 | What the text does not decide | Where found, and where not confirmed |
|---|---|---|
| The fourth question against the rule on lines | Whether a list that the system generated from installed packages is a program record or is installed | check 1; not confirmed in step 2 |
| The second question | Whether a stored archive is itself code when its contents are executed, or when it only holds code | check 1; steps 2 and 4 |
| The rule that everything installed must be recorded, against the clarification about code inside a recorded program | Whether an installed browser extension must be recorded | check 1; the search for contradictions; not confirmed in step 2 |
| The fourth question | Whether the history of a repository fetched at a person’s command is a program record or material | lived-in machines; step 2 |
| The third question | Whether a value that a program generated and the computer obeys is a setting | lived-in machines; not confirmed in step 2 |
| The clarification about files executed as code | Whether a file of values whose entries include commands is code | lived-in machines; step 2 |
| The definition of an installer | Whether a tool that obtains and removes container images is an installer | lived-in machines; step 4; in step 2 the four images received one decision each |
| The clarification about a program in a container against the third question | Whether a stored container is a program or a set of service values | step 2 |
| The first question | Whether “obtained as part of a package” follows the content of a file or its name and place | step 2 |
| The first, second and fourth questions | What package contents held in an installer’s own store are, and what the code is that an installed program copies or generates as it runs | step 2, on rows for which the verification of the lived-in machines had rejected the kind or found its premise wrong |
| The clarification about a value obeyed only by a program that a person runs for himself or herself | Whether a browser’s home page “launches something” | the 88 ways; not confirmed in step 2 |
| The definitions of a built-in tool and of general-purpose programs | Whether a compiler or a build tool is a built-in tool or a general-purpose program | the 88 ways; not confirmed in step 2 |
| The second question against the fourth, with the clarification about files executed as code | Whether a saved history is values that are read or statements that can be executed | the 88 ways; not confirmed in step 2 |
| Section 8.4 | Understanding does not follow from the three properties | step 1 |

Steps 1 and 3 reasoned from the text and made their own lists of gaps in the wording; none of these was observed on
an object. Step 1 lists four. Reproducibility does not decide between one clear requirement and one possible result,
or between meeting the described requirement and equality of everything the lines cover. The words “such a package”
in the first question leave a question about old remnants that are not code. The permission to record what need not
be recorded, read with Section 8.5, leaves open the scope intended for material that is recorded voluntarily. And
the classification of an account that was generated without being requested depends on the reading. Step 3 lists
three: the permission for a line to name a source, against the requirement that a line state the state it requires
(marked there as a candidate only); what counts as the report of a successful application (marked as depending on
the reading; the last review of step 3 holds that, like the third, it is a candidate only, unless Section 8.5
covers it); and whether the properties refer to the last declaration applied successfully or to the present
contents of its files (a candidate only, unless Section 8.5 covers it).

Questions that the records leave to the author, and that Part I does not decide, are published with the records.
The chief of them: whether a text that the system writes from what is saved is a declaration (step 5); what
“unambiguous” means for a line that leaves a value to the installation (steps 1 and 6); and to which declaration the
properties refer while an update is being applied (step 3).

Nothing in these results establishes whether a system with the three properties can be built: checks 2 and 3 were not
conducted, for the second cycle in succession. Outcome 1 of check 4 means that the definitions suffice to assess the
two existing systems against the properties, not that the hypothesis is true.

# Part II. Formulated after the results

This part was formulated after the results of Part I became known, and those results do not support it. It changes
no outcome of Part I. It contains no new version of the hypothesis: the text of version 4 stays as published in [4],
with the gaps of Table 7 in it. It contains an account of what check 1 answers, made after its outcome was known, and
a new plan.

## 7. What check 1 answers and what it does not

### 7.1. Two questions

The research question asks for a definition. We take as a premise that a definition of a kind of system is of use
only if such a system can exist. We have not claimed that it can: in [4] we wrote that nothing in the results
establishes whether a system with the three properties can be built (Section 5) and that we do not claim it
(Section 6.5). The question has nevertheless been part of the plan from the start. The first paper named three
conditions for what counts as an answer: that the properties allow any object on a real computer to be assigned to
a class, that a system with these properties can be built and used in everyday work, and that existing systems can
be assessed against each property [1]. The third paper gave check 2 the aim of checking “that a system with these
properties can be built and used for ordinary work” [3, Section 4.3].

Check 1 addresses the first of these conditions. It takes computers that were not built under the definition, lists
what is on them, and asks whether the words of the definition assign every item to exactly one kind. Its outcome
describes the wording.

### 7.2. Three cycles of the same check

Table 8. The check of what must be recorded, in three cycles.

| Cycle | Text | Objects compared | Matching decisions | Outcome |
|---|---|---:|---|:---:|
| 1 [2, Section 4.1] | version 1 | 398 on three clean systems; 178 on a fourth | 63.32%; 80.34% | 0 |
| 2 [4, Section 4.1] | version 3 | 16,524 | 90.93% | 0 |
| 3, this paper | version 4 | 16,375 | 52.99% | 0 |

The first cycle also compared 695 rows of two personal machines, whose records are not published, and three further
samples [2, Section 4.1]; they are not shown.

In each cycle the check found places where the text does not decide, and each new text was written to resolve the
places found before. In the third cycle, 1,362 rows met the second clause of the failure condition, and three kinds
with 111 rows were confirmed under the first. One of these kinds is not new: [4], Section 8.6, gave an answer for the
browser extension, and the text still decides it both ways. The check has done what it was fixed to do. Its findings
concern the wording; for two of its three kinds, step 2 could not exclude that deciding facts were missing.

### 7.3. What the agreement figure contains

After the results, we examined the rows on which the two classifications differ. The computation is published with
the records.

In check 1, 7,698 rows differ. In 7,307 of them, the first classification answered that a fact needed for the
decision was unknown, and the second gave a decision; in 1,117 of these, the decision of the second was that the
text decides both ways. In 24 rows the roles are reversed. In 367 rows, both gave a decision and the decisions
differ. The adjudication decided the 7,307 rows as follows: 5,692 are resolved by a sentence of the text, 1,267 are
gaps, and 348 depend on an unknown fact. Of the 1,267 rows marked as gaps, 1,068 belong to the kind that the
verification later found to depend on an unknown fact, and 152 to the kind it rejected. Most of the low agreement of
check 1 therefore comes from one classification declining to decide objects that the adjudication found the text and
the available facts to decide. Among the 8,457 objects for which both classifications gave a decision other than
“unknown”, the decisions match for 8,090, or 95.66%.

On the lived-in machines, 21,105 of the 21,242 differing rows are of the same sort, and in 14,918 of them the
decision of the second classification was that the text decides both ways. The adjudication marked 16,529 of the
21,105 rows as gaps, 2,431 as resolved and 2,145 as depending on an unknown fact. The verification then rejected the
kind to which 14,856 of these gap rows belong—the own files of a client program that installs and updates itself, on
the gaming machine—and did not confirm the kind of a further 1,335. In step 4, there are 29,372 rows in which one
classification answered “unknown” and the other decided, and the adjudication left 29,155 of them depending on an
unknown fact; there the facts are missing, chiefly for the tree of package recipes on Gentoo.

In all three tables, then, most of the rows on which the classifications differ are rows where one of them gave no
decision. In check 1 and on the lived-in machines, most of the gaps first marked on such rows were not confirmed
afterwards. The share of matching decisions says little about how the text decides, and we draw no conclusion from
it. The gaps found on rows of the inventories are among those of Table 7: few kinds, on few rows. Six of the fifteen families yielded 0 in step 2 with all
the facts it could collect; for the generated lists, the browser extension and the values generated by a program,
step 2 could not exclude that facts were missing.

### 7.4. The controls of the procedure

Two controls were fixed in advance for the way of deciding in which two parties answer separately what must be in
the declaration: the eight cases of the order of the checks, and the ten cases of step 7. Checks of this sort are
known as outcome-neutral checks or positive controls; they are meant to “confirm that the study is sufficiently well
designed to be capable of answering the research questions”, and when one fails, “the study may still be informative
in showing that a procedure does not perform as intended” [6].

Both controls failed, for reasons of two kinds.

Some failures are failures of the procedure. In the first control, for the compiled copy of code under version 3,
one party found no gap and gave no answer about the meaning, and the procedure returned a weight other than the
expected one. In
step 7, the two parties gave different answers in two of the ten cases, and one such case alone gives 0 under the
rule of the step.

Other failures come from the expected answers. In the first control, for the browser extension, a party found a gap
where we had expected none; check 1 confirmed a gap for objects of this kind, although step 2, with the facts it
could collect, did not. In step 7, the known answers were our own reasoning in [4], Section 8.6, which that section calls
reasoning and not a check; in two of the four cases counted against the procedure, both parties named the line of
the package that supplied the object, which the rule on lines of [4], Section 8.2, allows.

The controls were fixed for the weighting of gaps, and step 7 ran under one of two readings of which procedure is
meant. They show that this way of deciding did not pass the controls set for it, and that some of our expected
answers were unsound. Whether the first of these results bears on check 1, which also relies on two separate
decisions, we leave open. The withdrawal of check 1 below does not rest on it.

### 7.5. What we conclude

The outcome of check 1 stands as recorded: under the conditions fixed in [4], version 4 did not withstand it. The
gaps of Table 7 are properties of the wording, with the reservation stated there for those that step 2 did not
confirm. They will be corrected in a new version.

Check 1 does not address whether a system meeting the definition can be built. The checks that address that
question yielded ? in the first cycle and were not conducted in the second and the third, while the wording was
checked in all three. We change this order. We withdraw from the plan the classification of inventories of systems
that were not built under the definition; this is a decision about the plan, made after the results, and it does
not rest on a claim that the check was unsound.

This changes the first of the three conditions that the first paper named for an answer [1]. We no longer ask that
the properties assign any object on any real computer to a class. The new plan asks less, and only of the objects
of one system built under the definition: every object of the reference implementation that must be recorded, or
for which the text decides both ways or does not decide whether it must be recorded, must be recorded
(Section 9.3). An object that the text assigns to two classes, or to none, passes when it is recorded. An outcome of
1 under the new plan would therefore not show that the text assigns every object to one class.

## 8. What has not been checked

In three cycles, the checks that address whether such a system can be built have not produced an outcome of 1 or 0.
In the first cycle, the four checks on testbeds yielded ? [2, Section 5.1]. In the second and the third, the checks
of the properties and of reproducibility did not begin, because the testbed was not accepted (Sections 4.2 and 4.3;
[4], Section 4.2).

In both of the last cycles, the testbed was built, as its records state, on an existing general-purpose
distribution and was restricted way by way, against a list of 88 ways of bypassing the declaration prepared in
advance [4, Section 4.2]. Step 8 shows a way that this left open in the third cycle: the system’s own package
installer, run directly as superuser, changed what was installed.

The steps of the supplement that performed cases gave the only observations of this kind in the third cycle. They
are not outcomes of checks 2 and 3. In step 6, the cases of reproducibility and removal yielded 1 within the limits
stated. In step 5, ordinary work in one session yielded 1, and none of the fifteen ways of running saved code was
refused. In step 8, all four histories yielded ?; lines were unfulfilled in three of them, the game could not be
installed, and an installation failed while the network was down (Section 4.6).

Step 5 left two questions to the author: whether a text that the system itself writes from every file saved under
the designated directories is a declaration, and the same for the account rows that the system derives from what
the account tool wrote. For each, two readings were recorded. Under the first, the text is written before the
file exists for any reader, so the computer is brought into conformity with a text written first, as [4],
Section 8.1, requires. Under the second, a text that follows whatever programs save is compiled from the computer,
which the same sentence excludes; for the account rows, [4], Section 8.3, is then met only by a tool that writes the
declaration as part of its own operation. Under either reading, the first version of each such text on the image was made
by importing the directory as it already was. The text of version 4 says that the tools for installation and
configuration record changes in the declaration [4, Section 8.3]; Section 8.1 says that the declaration consists of
files that a person has designated as the primary description of the computer, and Section 8.5 leaves to the system
how it adds to the declaration what a program that itself downloads other programs has installed. The text does not
say whether a line may be written by the system from what programs, including a built-in tool, save, and so does
not choose between the readings. We do not choose here either: a choice would change the definition, and a changed
definition is a new version [3, Section 4.1]. The question is carried to the new version, and the plan of
Section 9 gives ? to a case that is met only under one of the two readings, as a defect of the implementation
(Section 9.4).

## 9. The plan: a reference implementation

This section is fixed before the check it describes begins and does not change after publication.

### 9.1. What is checked

Whether a system with the three properties of version 4 can be built and used for ordinary work, and whether the
three consequences hold on it. The text of the hypothesis is Section 8 of [4], unchanged.

### 9.2. The object

A reference implementation: a small operating system in a virtual machine, built from existing components, with the
text of Section 8 of [4] as its specification. We call it ConfOS.

The third paper fixed the object of check 2 as “a disposable Linux prototype in a virtual machine, built only to
check the properties” [3, Section 4.3]. ConfOS differs from it in four respects. It is kept and published: its source
is placed in the repository of records [5] under the licence that the repository applies to code, so that anyone can
build it and repeat the cases. It is accepted by the cases of this plan and not by a list of ways of bypassing. It
is repaired and tried again when a case fails. And the party that builds it does not write the cases.

The mechanisms by which it meets the specification are not fixed here: by [4], Section 8.5, they are not part of the
definition. Every choice that the text leaves to a system and that the implementation makes is listed with it.

ConfOS is not meant for everyday use. The ordinary actions of Section 9.3 must nevertheless be possible on it.

### 9.3. The parts and their cases

There are six parts: the three properties and the three consequences. The cases are those fixed in [3], Sections 4.3
and 4.4, with the differences of [4], Section 9.3, with the additions of step 6 of the supplement, and with the four
histories of step 8. The conditions are those quoted in Section 2.2, with the additions named in the table and in
Section 9.6. The definition of a difference explained by hardware is kept as in [3], Section 4.4. What “unambiguous”
means for a line that leaves a value to the installation is a question left to the author (Section 6); a case whose
outcome depends on it yields ?.

Table 9. Parts, cases and what counts against.

| Part | Cases | Counts against |
|---|---|---|
| P1, Completeness | After the ordinary work and after every attempt of the cases of P4, an inventory of the whole machine is taken at both levels of [3], Section 4.2, by a program that is not part of the implementation and does not use its records; every object is decided as stated below | An installed object or a setting is in force and no line records it, and this is not breaking |
| P2, Guarantee | After each completed application, every line is compared with the state it requires. A power cut right after the report of success, three times for each kind of application: adding, changing and removing a line. An installation interrupted by a loss of network | At least one line is not fulfilled |
| P4, Law | Through every channel of [3], Section 4.3, an attempt is made to install, launch or change what is not recorded; the built-in tools, including the system’s own package installer, are also tried directly with superuser privileges. The command shell is present. A command that downloads and executes code without saving it: after a restart, nothing that was executed may be in force | A channel installs, launches or changes such a thing although it is not recorded, and this is not breaking; a built-in tool changes it past the declaration |
| Removal | The lines of a program, a service and a rule are removed and the declaration applied; a shared object with two owners, whose lines are removed one after the other | Something the line contributed, and the remaining lines do not cover, is in force |
| Reproducibility | The same declaration, all of whose lines are unambiguous, is applied to two independent clean installations; the same with two packages installed in opposite orders | What is in force under the lines differs between the two machines, and the difference is not explained by hardware. A line that takes a list from outside the declaration is excepted: for it, reproducibility is not claimed [4, Section 8.4] |
| Understanding | From the declaration alone, without access to the machine, a published program derives what must be installed and the value of every setting; the result is compared with the inventory of the machine. The derivation may read, besides the declaration, only the packages that its lines name, in the release that its line names or, where the line names none and the package is a component, in the release committed under Section 9.5; for any other package, the derivation reads nothing beyond the declaration; it may not read anything produced by the implementation on a machine. Each object of the inventory is compared with what the derivation gives for the line that records it under [4], Section 8.2. The comparison is made with every inventory taken under P1 | An installed object or a value of a setting on the machine differs from what was derived from the declaration. For a line that takes a list from outside the declaration, it suffices that the declaration shows which source determines the list [4, Section 8.4] |

Ordinary work is a condition of the whole check. Its list is that of [3], Section 4.3—installing a program, updating
the system, connecting to a Wi-Fi network and pairing a Bluetooth device on real hardware, working in a browser,
editing documents—with running ordinary commands and one’s own recorded script in the command shell [4,
Section 9.3], and with the histories of step 8: two updates with a restart after each; fetching, building, changing
and rebuilding a small program; installing and starting a game through a launcher that downloads it; and an
installation during which the network is lost and then restored. It counts against the hypothesis when an ordinary
action cannot be performed through the declaration and its built-in tools.

How objects are decided. The inventory does not come from the implementation’s own records. The implementation may
name the line from which it built an object; this is accepted only if the checksum of the object equals the one that
follows from that line. Every other object is decided under [4], Section 8.2, by the party that performs the runs,
which quotes the sentence it relies on; a separate review checks each decision. If the review finds that the text
does not decide whether the object must be recorded, the object is treated, in that run and every later run, as one
that the text decides both ways (below); if the review does not accept a decision for another reason, the object
counts against the part. The two independent classifications and the adjudication of [3] are not used. Where the
text decides both ways whether an object must be recorded, as for kinds of Table 7, an implementation that records
the object meets the requirement under both readings, because what need not be recorded may also be recorded
[4, Section 8.2]; the case yields ? only if it is met under one reading and not under the other. The same holds for the two readings that Section 8 leaves open: a case that is met only because the
system wrote a line from what a program saved—every file saved in a directory, or the files that a program or a
built-in tool wrote—rather than because the built-in tool [4, Section 8.1] that made the change recorded it in the
declaration as part of its own operation, yields ?. A general-purpose program, outside a part of it that is a
built-in installer, is not such a tool, including when code placed in its process writes the line for it. A line
written by code written for the implementation counts as written by a program written for the implementation, also
when that code is placed in, loaded by or patched into a program that is not written for it. For this rule only, a
program counts as such a tool only where [4], Section 8.1, decides that it is one without relying on documentation
written
for the implementation; a program written for the implementation therefore does not count as such a tool. This
condition belongs to the plan and is not a reading of [4], under which a program’s documentation decides whoever
wrote it. Where the text does not decide, or decides both ways, whether a program is a built-in tool or a
general-purpose program, as the 88 ways found for a compiler or a build tool (Table 7), a case that is met because
that program recorded the change yields ?. For each case that is met because a program recorded the change in the
declaration as part of its own operation, the review checks which program recorded the change and whether it is
such a tool; if the review does not confirm that it is, the case yields ?. This rule applies whatever mechanism writes
such lines, including a mechanism that [4], Section 8.5, leaves to the system. An installer that is such a tool and
adds to the declaration, as part of its own operation, what it installs [4, Section 8.3] is not covered by this
rule.

The consequences. Step 1 shows that Understanding does not follow from the three properties as they are worded. The
plan therefore does not check whether the consequences follow from the properties. It checks whether they hold on
one implementation. An outcome 1 for a consequence says nothing against step 1: an implementation may meet a
consequence by requiring more of a declaration than the text does, as the image of step 6 did when it required every
account identifier to be stated. Each such requirement is listed with the implementation.

### 9.4. Outcomes

Each part receives one outcome. Outcome 1 is assigned from one complete run, the last; an outcome ? is assigned from
that run, unless it was made final earlier as stated below. In every complete run, every case of every part is
performed, on fresh installations of one published version of the implementation.

- **1.** In that run every case of the part is performed, no case of the part yields ?, and nothing counts against
  the part; the ordinary work succeeds in the same run; the run is performed by a party that did not build the
  implementation, from the published materials; and the search of Section 9.5, made on the same version, has found
  nothing.
- **0.** A written argument shows that a requirement of the part cannot be met by any system, because it contradicts
  another requirement of the hypothesis or the condition of ordinary work; a separate review accepts the argument.
- **?.** No decision. There are four reasons, and the reason is named: the text of the hypothesis does not decide
  a case, or the case is met under one of its readings only (the case, the readings and the choice made in the
  implementation are recorded for a new version); a case is met only through a program that does not count as a
  built-in tool under Section 9.3; a case cannot be observed (for example a line that cannot be verified from inside
  the machine and was not verified from outside it); or the work ended before the conditions for 1 were met. A part
  of which one case yields ? yields ?.

Within a part, 0 prevails; otherwise ? prevails, including a ? made final in an earlier run; otherwise the part
receives 1 if the conditions above hold. A case whose ? is final is still performed in every complete run.

A case that the implementation fails is a defect of the implementation, whatever mechanism is at fault, including a
mechanism that [4], Section 8.5, leaves to the system. It counts against the part until it is repaired, and after a
repair a new complete run is made. The party that performs the run may instead find that the text does not decide
the case; it then quotes the sentence of [4] it relies on, and a separate review checks the finding. Such a case
yields ? if the review accepts the finding. If the review holds that the text decides the case, the case is decided
as the review holds: if it fails, it counts against the part until it is repaired; otherwise it is met. Where the
finding concerns whether an object must be recorded, or a case to which Section 9.3 gives ? because it is met under
one reading only or only through a program that does not count as a built-in tool, Section 9.3 applies instead. Any
other ? given under this
paragraph because the text does not decide is final for the part under the present text; the runs continue. A case
that yields ? under Section 9.3, because it is met under one reading only or only through a program that does not
count as a built-in tool, is a defect of the implementation for the end of the work under this section; in the run
in which it is observed, it yields ? and does not count against the part.

The work under this plan ends when a complete run leaves no defect and the search that follows it (Section 9.5)
finds nothing, and at the latest with the eighth complete run. After the eighth complete run the search is made
whether or not that run left a defect. Every part that then receives neither 1 nor 0 yields ?, for the reason that
the work ended; the part and the case that prevented 1 are named, with the number of runs and repairs.

The outcomes combine as before: 0 if any part yields 0; otherwise ? if any part yields ?; otherwise 1.

### 9.5. Procedure

- The parties are separated by what they can see and do. The party that writes the cases and performs the runs takes
  no part in building the implementation and receives it only as published source and as a built image. The builder
  may read the cases. The review reads the records of both and takes part in neither.
- The cases, the programs that take the inventory and compare the machine with the declaration, and the program
  that derives the state from the declaration are written by that party, from the text of the hypothesis and this
  section. It may take the published cases of steps 6 and 8 as a starting point and use the same programs and
  packages.
- The exact commands of the cases, the declarations, the programs named above, the program chosen for each channel
  and the releases of the components of the implementation are committed to the repository of records before the
  first complete run. Components are taken in their latest stable release on the day of that commit.
- Runs made while the implementation is being built are not observations of the check. Each of them, and each repair,
  is recorded and published with the outcomes.
- After a complete run that leaves no defect, and in any case after the eighth complete run, the party that performs
  the runs searches, on the same version, for a way to change what is installed or settings past the declaration by
  an ordinary path. The search covers every channel of [3], Section 4.3, with at least three attempts for each
  channel that differ from the fixed cases. The attempts are not committed in advance; each is recorded as it is
  made. Each success becomes a new case, committed before the next complete run, and the implementation returns to
  repair. An outcome of 1 is assigned only after a search that finds nothing. Cases are only added in this way,
  never removed or weakened.
- Events recognized as breaking are excluded from the outcome and listed separately, as in [3]. Each event
  recognized as breaking is checked by the review; if the review does not accept the recognition, the event counts
  against the part, and a success of the search becomes a new case.
- All records are dated, never deleted, and published with the outcomes.

### 9.6. What changes relative to the fixed plan

The plan of [4], Section 9, and the general rules of [3], Section 4.1, were fixed before the checks. One of those
rules is that the failure conditions do not change after publication. It was kept for the checks reported in Part I:
their outcomes are given under the conditions as published. We change the plan here, after the results of Part I
and before any observation under the new plan, and we list every change. Items 1, 6, 7 and 14 replace or remove
conditions under which the earlier plan gave 0.

1. Check 1 is withdrawn, and the first of the three conditions of [1] for an answer is no longer checked in full:
   for the objects of one system built under the definition, the plan asks only that each be recorded where the
   text requires it, decides both ways or does not decide whether it must be recorded (Sections 7.5 and 9.3). The
   two independent classifications and the adjudication are no longer
   used; objects of the implementation receive one decision, under review. Where the review does not accept a
   decision for a reason other than that the text does not decide, the object counts against the part; where the
   review finds that the text does not decide whether an object must be recorded, the object is treated as one that
   the text decides both ways, and the case is met only if the object is recorded; where the review accepts any
   other finding that the text does not decide a case, other than a case to which Section 9.3 gives ?, the case
   yields ?, and this ? is final for the part under the present text. Under [3], a difference that no sentence resolved yielded 0.
2. Checks 2 and 3 become one check with six parts. Their failure conditions are kept, and two are added: for P1,
   besides the condition on channels, any installed object or setting in force that the inventory finds and no line
   records; and the condition for Understanding.
3. The object is kept, published, repaired and accepted by cases, and the party that builds it does not write the
   cases (Section 9.2); under [3] it was disposable.
4. A case may be repeated after a repair. Under [3], each case was attempted once, and a defect of the testbed ended
   the case with ?.
5. A check no longer ends when its list of cases is done: it ends when a complete run leaves no defect and the
   search that follows it finds nothing, or with the eighth complete run and its search, and the outcomes are
   assigned from the last run.
6. A case that the text does not decide, or that is met under one of its readings only, yields ? and goes to a new
   version; for the question whether an object must be recorded, item 1 applies. Under [3], an object that the
   definitions do not allow deciding yielded 0. A case whose outcome depends on the meaning of “unambiguous” also
   yields ?.
7. Outcome 0 is kept for what no system can meet, and it requires in every case a written argument accepted by a
   separate review. Under [3], a requirement that contradicts another requirement yielded 0 without this condition.
8. Outcome 1 requires that the run be performed by a party that did not build the implementation, and that the search
   of Section 9.5 find nothing.
9. The consequences are checked on the implementation and are not taken to follow from the properties; Understanding
   receives a case of its own.
10. Cases may be added after the check begins, by the search of Section 9.5, and the attempts of that search are not
    committed in advance.
11. The cases of Removal and Reproducibility are extended by those of step 6, and the list of ordinary work and the
    cases of P2 and P4 by the histories of step 8.
12. The new cases may start from the published cases of steps 6 and 8 and use the same programs and packages, and
    the implementation, although built anew, is built from existing components, which may include those of the image
    of the third cycle. The rule that objects and machines took part in no earlier cycle is therefore not kept.
13. The rule on the latest stable release is applied to the components of the implementation, on the day the inputs
    are committed; [3] fixed the date of its own publication.
14. Check 4 is not repeated. The cases of Section 9.3 can later be performed on existing systems; this is beyond the
    plan and will be reported separately.
15. Each event recognized as breaking is checked by the review, and an event whose recognition the review does not
    accept counts against the part (Section 9.5); under [3], events recognized as breaking were excluded without
    review.
16. For the rule of Section 9.3 on cases met because a program recorded a change, a program counts as a built-in
    tool only where [4], Section 8.1, decides that it is one without relying on documentation written for the
    implementation; [4] relies on the program’s documentation, whoever wrote it. For every other purpose of the
    plan, including the cases and the conditions of P4, breaking and ordinary work, a built-in tool is as defined in
    [4], Section 8.1.

## 10. Discussion and limitations

The new plan can establish less than it may seem. Outcome 1 for every part would show that one small system has the
properties and the consequences on the cases of the plan. It would not show that the definition is the right one,
that the wording is free of gaps, or that a system for everyday use can be built in the same way.

The gaps of Table 7 remain in the text. We do not correct them here, because a correction would be a new version,
and because we expect the implementation to meet more places where the text is silent. They will be corrected
together. They do not by themselves prevent an outcome of 1: where the text decides both ways, or does not decide,
whether an object must be recorded, an implementation can record it and so meet both readings. Where a case is met
under one reading only, or the text does not decide a case for another reason, the part yields ?. One such case is
already known: the plan cannot give 1 for a case that is met only because the system wrote a line from what a
program saved, as the image of step 5 did for saved files and for the account tool. An implementation in which a
program that counts as a built-in tool under Section 9.3, which excludes programs written for the implementation,
and that makes a change records it in the declaration as part of its own operation is not affected; nor is one in
which a person writes the line before the change is made.

A plan in which a failing case is repaired and repeated cannot end with 0 through failure alone. This is deliberate:
a failed attempt to build something does not show that it cannot be built. The cost is that 0 now requires an
argument, and an argument can be wrong; it is reviewed separately for that reason.

The builder may read the cases, and an implementation can be fitted to them. The search for other ways after a
complete run is meant to expose this; it is bounded, and it can miss what a longer search would find. In the third
cycle, the work of trying the testbed by a party that did not build it was not performed at all (Section 5). Under
this plan the search is a condition of outcome 1: if it is not performed, no part receives 1.

The implementation and its cases come from the same author. The separation of the party that builds from the party
that writes the cases and performs the runs reduces this, and publication of the source and the cases allows anyone
to repeat the run; it does not remove it.

Section 7 was written after the outcome of check 1 was known, by the author of the hypothesis that the check had
failed. The reader should weigh it accordingly. The figures it gives can be recomputed from the published tables.

The definition says nothing about whether a system that meets it is convenient to use.

## 11. Conclusion

Under the conditions fixed in advance, version 4 did not withstand the check of what is recorded: three kinds of
objects were confirmed for which the text decides both ways or does not decide, and the work beyond the plan and the
supplement confirmed further gaps and showed that Understanding does not follow from the three properties as worded.
NixOS and GNU Guix System were assessed and have none of the three properties. Whether a system with the three
properties can be built was not checked in the third cycle.

We leave the text of version 4 unchanged, with its gaps recorded, and change the order of the work. The
classification of inventories of existing systems is withdrawn from the plan: it answers a question about the
wording. Of that question the new plan keeps one part: for every object of one system built under the definition,
that it is recorded wherever the text requires it, decides both ways or does not decide whether it must be. We fix
one check: a reference implementation, ConfOS, built from the text of the hypothesis as its specification, with an outcome of
1, 0 or ? for each property and each consequence. The gaps of the wording will be corrected in a new version,
together with what the implementation meets.

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
5. Records of the checks. https://github.com/Yakyman/configuration-as-law
6. Henderson, E. L., Chambers, C. D. (2022). Ten simple rules for writing a Registered Report. PLoS Computational
   Biology, 18(10), e1010571. https://doi.org/10.1371/journal.pcbi.1010571
7. Willroth, E. C., Atherton, O. E. (2024). Best Laid Plans: A Guide to Reporting Preregistration Deviations.
   Advances in Methods and Practices in Psychological Science, 7(1). https://doi.org/10.1177/25152459231213802

## Records of the third-cycle checks

The records are dated 23 November 2026 and are published in the repository of records [5]. Paths are given from the
root of the repository.

- The order of the checks, Supplement 1, the inputs and the disclosures, committed before the observations they
  govern. configuration-as-law/check-inputs-v4/PROTOCOL.md; configuration-as-law/check-inputs-v4/SUPPLEMENT-1.md;
  configuration-as-law/check-inputs-v4/inputs-check-1.md; configuration-as-law/check-inputs-v4/inputs-check-4.md;
  configuration-as-law/check-inputs-v4/releases.tsv; configuration-as-law/check-inputs-v4/DISCLOSURES.md;
  configuration-as-law/check-inputs-v4/supplement-1
- The text of version 4 and the numbering of its sentences used in the checks. configuration-as-law/records-v4/TEXT.md;
  configuration-as-law/records-v4/SENTENCES.md
- Check 1: outcome, comparison of the two classifications, adjudication, verification of the kinds of gaps, reviews,
  and the record of the Gentoo attempt. configuration-as-law/records-v4/D1/RESULT.md;
  configuration-as-law/records-v4/D1/compare/STATS.md; configuration-as-law/records-v4/D1/compare/joined.tsv;
  configuration-as-law/records-v4/D1/adjudication/rows.tsv; configuration-as-law/records-v4/D1/adjudication/HOLES.md;
  configuration-as-law/records-v4/D1/fix-d1-h-2; configuration-as-law/records-v4/D1/REVIEW-D1-H-3.md;
  configuration-as-law/records-v4/D1/in/raw/gentoo/NOT-RUN.md
- Testbed: description, records of the rounds of construction and the review. configuration-as-law/records-v4/B2/STAND.md;
  configuration-as-law/records-v4/B2/BUILD-1.md; configuration-as-law/records-v4/B2/BUILD-2.md;
  configuration-as-law/records-v4/B2/BUILD-3.md; configuration-as-law/records-v4/B2/BUILD-4.md;
  configuration-as-law/records-v4/B2/ROUNDS.md; configuration-as-law/records-v4/B2/REVIEW.md
- Check 4: outcome, the two assessments and the review. configuration-as-law/records-v4/D4/RESULT.md;
  configuration-as-law/records-v4/D4/REVIEW.md; configuration-as-law/records-v4/D4/c1/ASSESS.md;
  configuration-as-law/records-v4/D4/c2/ASSESS.md
- Beyond the plan: contradictions within the text; the 88 ways; the lived-in machines; the weighting and its cases
  with a known decision. configuration-as-law/records-v4/A2/CARDS.md; configuration-as-law/records-v4/A2/VERIFY.md;
  configuration-as-law/records-v4/A2/REVIEW.md; configuration-as-law/records-v4/B1/RESULT.md;
  configuration-as-law/records-v4/B1/REVIEW-B1-2.md; configuration-as-law/records-v4/A3/RESULT.md;
  configuration-as-law/records-v4/A3/compare/STATS.md; configuration-as-law/records-v4/A3/compare/joined.tsv;
  configuration-as-law/records-v4/A3/adjudication/rows.tsv; configuration-as-law/records-v4/A3/REVIEW-A3-H-3.md;
  configuration-as-law/records-v4/W0/RESULT.md; configuration-as-law/records-v4/W1/RESULT.md;
  configuration-as-law/records-v4/W2/RESULT.md
- Supplement 1: the reviews of the supplement and of the inputs of its steps.
  configuration-as-law/records-v4/SUP1
- Supplement 1, steps 1–4: arguments, results and reviews. configuration-as-law/records-v4/S1/ARGUMENT.md;
  configuration-as-law/records-v4/S1/REVIEW-S1-A-2.md; configuration-as-law/records-v4/S2/RESULT.md;
  configuration-as-law/records-v4/S2/REVIEW-S2-R-2.md; configuration-as-law/records-v4/S3/ARGUMENT.md;
  configuration-as-law/records-v4/S3/REVIEW-S3-A-3.md; configuration-as-law/records-v4/D1b/RESULT.md;
  configuration-as-law/records-v4/D1b/compare/STATS.md; configuration-as-law/records-v4/D1b/compare/joined.tsv;
  configuration-as-law/records-v4/D1b/adjudication/rows.tsv; configuration-as-law/records-v4/D1b/adjudication/HOLES.md;
  configuration-as-law/records-v4/D1b/REVIEW.md; configuration-as-law/records-v4/S4/REVIEW-S4-P-4.md
- Supplement 1, steps 5–8: records of the cases, questions and reviews. configuration-as-law/records-v4/S5/RECORD.md;
  configuration-as-law/records-v4/S5/QUESTIONS.md; configuration-as-law/records-v4/S5/REVIEW.md;
  configuration-as-law/records-v4/S6/RECORD.md; configuration-as-law/records-v4/S6/REVIEW.md;
  configuration-as-law/records-v4/S7/RESULT.md; configuration-as-law/records-v4/S7/REVIEW.md;
  configuration-as-law/records-v4/S8/RECORD.md; configuration-as-law/records-v4/S8/REVIEW-S8-O-2.md
- The computations of Section 7.3. configuration-as-law/analysis/agreement_breakdown.py;
  configuration-as-law/analysis/disagreement_adjudication.py
