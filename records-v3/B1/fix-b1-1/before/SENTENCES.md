# Numbered sentences of Sections 2 and 3 of TEXT.md (version 3, published 21 November 2026)

Each line: sentence ID, then the sentence exactly as published. Cite sentences by ID.


## 2. The hypothesis, version 3


### 2.1. Concepts

- **S2.1-1** **Declaration**—a collection of files that a person has designated as the primary description of the computer.
- **S2.1-2** There may be many files; together they form one description and one source of truth about the system.
- **S2.1-3** **In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.
- **S2.1-4** For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.
- **S2.1-5** **Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.
- **S2.1-6** **Built-in tool**—a program of the system whose purpose includes changing what must be recorded: installing programs, managing accounts and rights, enabling services, changing access rules and network settings.
- **S2.1-7** **Breaking**—a change to what must be recorded, made past the declaration outside the built-in tools through the power of superuser privileges obtained by any means—in a full superuser session or through sudo: by writing directly to files, deleting, or disabling system mechanisms.
- **S2.1-8** Breaking is a violation on the person’s part rather than a property of the system, and it refutes no property.

### 2.2. What must be recorded

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-8** Consequences of this rule that we fix explicitly:
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.

### 2.3. Properties

- **S2.3-1** The properties concern the computer after a completed application of the declaration, provided there was no breaking.
- **S2.3-2** They admit no degrees: a system either has all three properties or it does not.
- **S2.3-3** The numbers P1, P2, and P4 are kept from versions 1 and 2 so that the versions can be compared.
- **S2.3-4** **P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.
- **S2.3-5** **P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.
- **S2.3-6** **P4. Law.** The system provides no path for changing, past the declaration, anything that must be recorded.
- **S2.3-7** The built-in tools, including those executed with superuser privileges, change it only through the declaration: an installer does not install a program past the declaration but adds it to the declaration.

### 2.4. Consequences

- **S2.4-1** **Understanding.** If there was no breaking, what is in force on the computer can be read from the declaration alone, without inspecting the computer.
- **S2.4-2** **Reproducibility.** The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous.
- **S2.4-3** Differences explained by hardware are excluded.
- **S2.4-4** **Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is in force unless the remaining lines cover it: the program is stopped and cannot be started, the service does not run and is not enabled, the rule is not in force.

### 2.5. What is not part of the definition

- **S2.5-1** How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.
- **S2.5-2** Such a system may resolve them in its own way.
- **S2.5-3** Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.

### 2.6. What changed relative to version 2

- **S2.6-1** Instead of a list of parts of the system, the rule of Section 2.2 with the removal test.
- **S2.6-2** Problems O10 (the boundary of locked-in code) and O11 (the boundary of rules and hardware) of version 2 are closed by this rule.
- **S2.6-3** Saved Wi-Fi networks must be recorded; in version 2, they were not part of the system.
- **S2.6-4** The exceptions that version 2 allowed are removed from the definition; problem O12 goes into system design.
- **S2.6-5** Problems O13 (built-in versus general-purpose tools), O14 (completed application), and O15 (unambiguity of a line) are closed by the indicators of Section 3.
- **S2.6-6** When an edit takes effect and the protection of secrets are assigned to system design.

## 3. Observable indicators

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.
- **S3-3** **Declaration in force and completed application.** The declaration in force is the declaration of the last application that the system has reported as successful; that report completes the application.
- **S3-4** If the system reports an application as failed, or gives no report within one hour, the previous declaration stays in force.
- **S3-5** The properties are checked against the declaration in force, including after an immediate power cut right after the success report and a new boot; a state that then differs from the declaration reported as applied is a failure of P2.
- **S3-6** **Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.
- **S3-7** General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.
- **S3-8** If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.
- **S3-9** **Unambiguous line.** A line that installs something is unambiguous when it states the version and the source so that the content to be installed is uniquely determined, for example by a checksum.
- **S3-10** A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default.
