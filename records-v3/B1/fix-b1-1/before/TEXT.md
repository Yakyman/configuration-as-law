# Testing the “Configuration as Law” Hypothesis, Version 3: Hypothesis, Checks, and Failure Conditions Fixed Before the Checks

<USER> <USER>

Preregistration · 21 November 2026 · published before the checks begin; after publication, the hypothesis and the
failure conditions do not change

## 1. The question and the place of this text

Research question: what is a declarative operating system, and what properties must it have?

In the first paper [1], we proposed version 1 of the “Configuration as Law” hypothesis and, before any check was run,
fixed five checks and their failure conditions. In the second paper [2], we reported the outcomes of these checks—the
census yielded 0, the other checks yielded ?—and, separately and as formulated after the results, set out version 2,
which has not been tested.

Version 3 changes the definitions of version 2 before any of its checks (Section 2.6). Under the rule of the second
paper, definitions changed after the results became known form a new version of the hypothesis, which is tested on
machines and objects that earlier checks have not seen. Therefore version 3 is tested, and version 2 is not tested
separately.

This text fixes the hypothesis, the checks, and the failure conditions before the checks begin. After publication, it
does not change. Anything formulated after the results will be presented separately and marked as formulated after the
results.

## 2. The hypothesis, version 3

### 2.1. Concepts

- **Declaration**—a collection of files that a person has designated as the primary description of the computer.
  There may be many files; together they form one description and one source of truth about the system.
- **In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service
  is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that
  uses it, firmware or a boot order is set on the device. For a recorded object, its line states the required state;
  whether a recorded program is running at a given moment does not matter unless its line requires it.
- **Application of the declaration**—an action of the system that brings the computer into conformity with the
  declaration.
- **Built-in tool**—a program of the system whose purpose includes changing what must be recorded: installing
  programs, managing accounts and rights, enabling services, changing access rules and network settings.
- **Breaking**—a change to what must be recorded, made past the declaration outside the built-in tools through the
  power of superuser privileges obtained by any means—in a full superuser session or through sudo: by writing directly
  to files, deleting, or disabling system mechanisms. Breaking is a violation on the person’s part rather than a
  property of the system, and it refutes no property.

### 2.2. What must be recorded

Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded. The test is
removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the
object must be recorded.

The following need not be recorded:
- content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the
  same, and only the content itself is unavailable;
- cache: after it is removed, the computer does the same, only more slowly;
- records of the past—logs, history;
- settings that are in force only inside one program, for example the home page, theme, and extensions of a web
  browser.

Consequences of this rule that we fix explicitly:
- a program that runs on the computer must be recorded regardless of how it was installed—including an application
  package (Flatpak), a program in the home directory, and a program in a container;
- code that another program executes must be recorded if the program runs it with the program’s own rights, so that
  the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files,
  an editor configuration written in the editor’s programming language. Code that the program confines to its own
  interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself
  must be. This exemption covers only code that runs inside the executing program; a program that runs as its own
  process on the computer, including in a container, is a program and must be recorded. A file that a program executes
  as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the
  same;
- accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for
  connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- the boot order and device firmware must be recorded where the system is able to change them.

### 2.3. Properties

The properties concern the computer after a completed application of the declaration, provided there was no breaking.
They admit no degrees: a system either has all three properties or it does not. The numbers P1, P2, and P4 are kept
from versions 1 and 2 so that the versions can be compared.

**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.

**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

**P4. Law.** The system provides no path for changing, past the declaration, anything that must be recorded. The
built-in tools, including those executed with superuser privileges, change it only through the declaration: an
installer does not install a program past the declaration but adds it to the declaration.

### 2.4. Consequences

- **Understanding.** If there was no breaking, what is in force on the computer can be read from the declaration
  alone, without inspecting the computer.
- **Reproducibility.** The same declaration on another computer yields exactly the result described in it, provided
  the description is unambiguous. Differences explained by hardware are excluded.
- **Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is
  in force unless the remaining lines cover it: the program is stopped and cannot be started, the service does not run
  and is not enabled, the rule is not in force.

### 2.5. What is not part of the definition

How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the
transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect
the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of
declarativeness. Such a system may resolve them in its own way. Nor is the form of the declaration part of the
definition: it may be a list or an algorithm that computes what is recorded.

### 2.6. What changed relative to version 2

- Instead of a list of parts of the system, the rule of Section 2.2 with the removal test. Problems O10 (the boundary
  of locked-in code) and O11 (the boundary of rules and hardware) of version 2 are closed by this rule.
- Saved Wi-Fi networks must be recorded; in version 2, they were not part of the system.
- The exceptions that version 2 allowed are removed from the definition; problem O12 goes into system design.
- Problems O13 (built-in versus general-purpose tools), O14 (completed application), and O15 (unambiguity of a line)
  are closed by the indicators of Section 3.
- When an edit takes effect and the protection of secrets are assigned to system design.

## 3. Observable indicators

- **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what
  the object does, established by documentation, by observation, or by removal: in a disputed case, the object is
  removed on a disposable copy of the machine, and what stopped working is recorded. If what the object does remains
  unknown, the case yields ?.
- **Declaration in force and completed application.** The declaration in force is the declaration of the last
  application that the system has reported as successful; that report completes the application. If the system
  reports an application as failed, or gives no report within one hour, the previous declaration stays in force. The
  properties are checked against the declaration in force, including after an immediate power cut right after the
  success report and a new boot; a state that then differs from the declaration reported as applied is a failure of
  P2.
- **Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must
  be recorded: a package manager, including package managers of programming languages and of application packages;
  account and rights management; the service manager; network and firewall configuration. General-purpose programs—an
  editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser
  privileges, what must be recorded is breaking. If a program’s documentation does not state its purpose, the case
  yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a
  counterexample to the definitions and yields 0.
- **Unambiguous line.** A line that installs something is unambiguous when it states the version and the source so
  that the content to be installed is uniquely determined, for example by a checksum. A line for an account, a service
  or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a
  documented default.

## 4. Checks

### 4.1. General rules

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

### 4.2. Check 1: what must be recorded

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

### 4.3. Check 2: the properties on a testbed

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

### 4.4. Check 3: reproducibility

**Procedure.** The same declaration, all of whose lines are unambiguous, is applied to two independent clean
installations of the check 2 testbed on different virtual machines. What is in force under each line is compared:
every value the line states and, in addition, for a program, the checksums and permissions of its installed files;
for a service, whether it is enabled and the checksum of its unit file; for an account, its name, numeric identifier,
groups, shell, and home directory; for a rule, its effective text as reported by the system.

**Failure condition.** What is in force under the lines of the declaration differs between the two machines, and the
difference is not explained by hardware. A difference counts as explained by hardware only if it concerns drivers,
firmware, or device files of hardware that is present on one machine and absent on the other.

### 4.5. Check 4: existing systems

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

## 5. Order of work

- Before the checks, the wording of Section 2.2 is tried on objects from the first cycle: two independent
  classifications of the same objects under the new text. This is a trial of the wording, not a check of the
  hypothesis; its records are published together with the outcomes. If the trial leads to a change of the wording,
  the changed text is published before the checks as a new version of the hypothesis.
- Before the checks, this text is published on the author’s website, in the Internet Archive as a dated snapshot, and
  in the repository of check records as a commit with the hash of the file.
- Not checked: whether a system with these properties can serve for everyday work with all of one’s programs over a
  long time. Only such a system itself can show this.

## References

1. <USER>, A. (2026). Configuration as Law: A hypothesis on what a declarative operating system is. Preprint,
   18 November 2026; hypothesis, version 1. https://yakyman.com/configuration-as-law-v1.pdf
2. <USER>, A. (2026). Testing the “Configuration as Law” Hypothesis: Results of the First Cycle and a Second
   Version. Preprint, 20 November 2026. https://yakyman.com/configuration-as-law-v2.pdf
3. Records of the first-cycle checks. https://github.com/Yakyman/configuration-as-law
