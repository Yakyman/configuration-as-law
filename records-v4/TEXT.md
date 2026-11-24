# The published text for the checks of version 4

Part II of the fourth paper, «The “Configuration as Law” Hypothesis: Results of the Checks of Version 3, and Version 4» (published 23 November 2026, 01:19 UTC): Section 8 is the hypothesis, version 4; Section 9 fixes the plan of its checks and the failure conditions. Appendix A reproduces Section 4 of the third paper, to which Section 9 refers. Nothing below is changed.

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


# Appendix A. Section 4 of the third paper (general rules and the checks referred to by Section 9)

## A.4. Checks (third paper)

### A.4.1. General rules

- The outcome of each check is 1 (the hypothesis withstood the check), 0 (it did not), or ? (the data are
  insufficient). The outcome of a check combines its cases: 0 if any case yields 0; otherwise ? if any case yields ?;
  otherwise 1.
- A counterexample to the definitions—an object for which the definitions do not allow deciding whether it must be
  recorded, or a requirement that contradicts another requirement—yields 0.
- The two classifications are independent: each is made separately and without access to the other. When they differ,
  a separate adjudication, made by neither classification, decides whether the text of Sections 2 and 3 resolves the
  case and quotes the sentence that resolves it; if no sentence resolves it, the case yields 0.
- A failure of the testbed yields 0 only if a written argument shows that it follows from the definitions alone, so
  that any system having the property would fail the same case; a separate review checks the argument. Otherwise it
  is a defect of the testbed, and the case yields ?.
- Events recognized as breaking are excluded from the outcome and listed separately.
- The machines and objects of checks 1–3 did not take part in the first cycle.
- Fixed in advance: each system is used in its latest stable release available on the date of publication of this
  text; each case is attempted once unless this text states otherwise; no cases are added after the checks begin; each
  check ends when its list of cases is done. Before the first observation of a check, its concrete inputs—the release
  numbers, the test declaration, the program chosen for each channel, and the ordinary actions with their exact
  commands—are committed to the repository of check records.
- The failure conditions do not change after publication. Definitions changed after the results become known form a
  new version of the hypothesis.
- All records of the checks are dated, never deleted, and published together with the outcomes.

### A.4.2. Check 1: what must be recorded

**Aim.** To check that, by Sections 2.2 and 3, it can be decided for any object on a real computer whether it must be
recorded.

**Machines.** Disposable virtual machines with clean installations that did not take part in the first cycle: three
general-purpose desktop systems—Fedora Workstation, openSUSE Tumbleweed, Linux Mint—and two systems configured by a
configuration file at installation—Flatcar Container Linux and Talos Linux. Before the inventory, ordinary actions are
performed on the desktop systems so that objects of all kinds are present: installing a program with the package
manager and as an application package, connecting to a network, a user script in the home directory, running a
container.

**Objects.** Two levels: what is in force—packages, services and timers, processes, accounts and access rules, kernel
modules and drivers, open ports, firewall rules, saved networks; and stored objects that belong to no package, grouped
by the directory that contains them, with a separate list of executable code outside packages.

**Procedure.** The inventory is compiled with system tools. Each object is decided twice, independently: whether it
must be recorded. Agreement is measured as the share of matching decisions and by Cohen’s kappa; an agreement
threshold is not a condition of the check.

**Failure condition.** On any machine, an object is found for which the text of Sections 2.2 and 3 does not allow
deciding whether it must be recorded, or allows deciding both ways; or the two classifications decided differently
and the adjudication finds no sentence of the text that resolves the dispute.

### A.4.3. Check 2: the properties on a testbed

**Aim.** To check P1, P2, P4 and the Removal consequence, and that a system with these properties can be built and
used for ordinary work.

**Object.** The testbed—a disposable Linux prototype in a virtual machine, built only to check the properties; a new
implementation, not the first-cycle testbed.

**Procedure.**
- The test declaration names everything it permits: the base system and, for each channel below, one program
  installed through that channel. Through every channel of installation and launch, an attempt is made to install,
  launch, or change what is not recorded: the system package manager; package managers of programming languages (pip,
  npm); application packages (Flatpak, AppImage); direct download of programs and archives; building from source in
  the home directory; user services and schedulers (systemd --user, cron); interpreters executing scripts; shell
  startup files and executable program settings; containers. Built-in tools are also checked with superuser
  privileges.
- After each completed application, every line of the declaration is compared with the state it requires. The power
  cut right after the success report is repeated three times for each kind of application: adding, changing, and
  removing a line.
- Removal: the line of a program, a service, and a rule is removed from the declaration; after application, it is
  checked that nothing the line contributed is in force—the program’s former process does not run, and its executable
  cannot be started.
- Ordinary work: installing a program, updating the system, connecting to a Wi-Fi network, pairing a Bluetooth device,
  working in a browser, editing documents. Actions with Wi-Fi and Bluetooth are performed on real hardware: an adapter
  is passed to the virtual machine, or a separate computer is used.

**Failure condition for the properties.** At least one channel installs, launches, or changes something that must be
recorded although it is not recorded, and this is not breaking (P1, P4); a built-in tool, including with superuser
privileges, changes such a thing past the declaration (P4); after a completed application, at least one line is not
fulfilled (P2); after application of a declaration without a line, something the line contributed and the remaining
lines do not cover is in force (Removal, P1).

**Failure condition for ordinary work.** An ordinary action from the list above cannot be performed through the
declaration and its built-in tools.

**Weak points.** The testbed covers part of an operating system, not a whole system.

### A.4.4. Check 3: reproducibility

**Procedure.** The same declaration, all of whose lines are unambiguous, is applied to two independent clean
installations of the check 2 testbed on different virtual machines. What is in force under each line is compared:
every value the line states and, in addition, for a program, the checksums and permissions of its installed files;
for a service, whether it is enabled and the checksum of its unit file; for an account, its name, numeric identifier,
groups, shell, and home directory; for a rule, its effective text as reported by the system.

**Failure condition.** What is in force under the lines of the declaration differs between the two machines, and the
difference is not explained by hardware. A difference counts as explained by hardware only if it concerns drivers,
firmware, or device files of hardware that is present on one machine and absent on the other.

### A.4.5. Check 4: existing systems

**Aim.** To check that existing systems that call themselves declarative can be assessed against each property.

**Systems.** NixOS and GNU Guix System.

**Procedure.** From the documentation and a clean installation of each system, each of the properties P1, P2, and P4
is assessed twice, independently, as “has” or “does not have”, with a source or an experimental record. The
information is sufficient when there is a source or a record for the facts the property refers to: for P1, whether
objects that must be recorded can be in force without being recorded; for P2, whether recorded lines are in force
after application; for P4, whether a built-in tool can change, past the declaration, what must be recorded. Each pair
of a system and a property is a case. Finding that a system does not have a property is a successful assessment, not
a failure of the check.

**Failure condition.** A case yields 1 when both assessments reach the same decision, “has” or “does not have”, with
sufficient information, or when they differ and the adjudication resolves the dispute by a sentence of the text; ?
when the information is insufficient; 0 when the information is sufficient but the text of
the hypothesis does not allow deciding whether the system has the property, or when the two assessments differ and
the adjudication finds no sentence of the text that resolves the dispute.

