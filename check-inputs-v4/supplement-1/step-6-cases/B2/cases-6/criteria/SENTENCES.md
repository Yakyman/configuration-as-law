# Numbered sentences of Sections 8.1–8.3 of TEXT.md

Each line: sentence ID, then the sentence exactly as published. Cite sentences by ID.

### 8.1. Concepts

- **S8.1-1** **Declaration**—a text recording what the computer should be like: what is installed on it and how it is configured.
- **S8.1-2** The computer is brought into conformity with this text, rather than the text being compiled from the computer.
- **S8.1-3** The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.

- **S8.1-4** **Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.
- **S8.1-5** A general-purpose program with a built-in installer counts as an installer in that part of its functionality.

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.1-7** **Built-in tool**—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.
- **S8.1-8** General-purpose programs—an editor, file copying, link creation, the command shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.

- **S8.1-9** **In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.
- **S8.1-10** A setting is in force if it has its value.
- **S8.1-11** A service is in force if it is enabled; an account, if it exists.
- **S8.1-12** The required state of a recorded object is stated by its line.

- **S8.1-13** **Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.
- **S8.1-14** The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].

- **S8.1-15** **Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.
- **S8.1-16** Breaking is a violation on the person’s part rather than a property of the system, and it refutes no property.

### 8.2. What is recorded

- **S8.2-1** Everything that is installed and every setting must be recorded.
- **S8.2-2** The rest need not be recorded.

- **S8.2-3** The rule applies to objects that are on the computer.
- **S8.2-4** A command that a person typed himself or herself is that person’s action, not an object.
- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

#### 1.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

#### 2.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?
- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

#### 3.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?
- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.
- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.

#### 4.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

#### Which line records an object.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-18** A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.

- **S8.2-19** What need not be recorded may also be recorded in the declaration.

#### Clarifications.

- **S8.2-20** A file containing code that cannot be executed on this computer is not a program.

- **S8.2-21** Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.

- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

### 8.3. Properties

- **S8.3-1** The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.
- **S8.3-2** They admit no degrees: a system either has all three properties or it does not.
- **S8.3-3** The numbers are kept from earlier versions.

- **S8.3-4** **P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.

- **S8.3-5** **P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

- **S8.3-6** **P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.
- **S8.3-7** Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.
- **S8.3-8** What is installed and settings can be changed past the declaration only by breaking.
