# Gaps in the 88-row classification

This is the separate, unweighted investigation required by PROTOCOL.md Section 5. Eight rows are TWO_WAYS in three kinds of gap; there are no NOT_DECIDED rows. This is the FX-B1-1 revision. Missing tool/artifact facts are listed in the table as FACT_UNKNOWN and are not textual gaps.

## Home-page navigation and launching something

S8.2-14 does not say whether opening the chosen home page is launching something: for C8.08 the same stored URL is either a setting under S8.2-14 requiring its own line under S8.2-17, or a program record under S8.2-14 that need not be recorded under S8.2-2.

The documented objects are a chosen theme value and a home-page URL in the browser profile preferences. The homepage is opened on browser start, a new window, or the Home button, as documented in [home-page behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page); [preference storage](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0) documents the stored values. Short primary excerpts are in [SOURCES.md](SOURCES.md).

Both values fail Q1 (not unchanged package contents) and Q2 (read as values, not executed as code). The theme is a program record under S8.2-14 under both readings. For the URL, the broad reading includes page opening in launching something; the narrow reading means launching an executable/program and treats page display as ordinary work within the already-running browser. No sentence selects between these meanings.

The declarations differ by the required home-page setting line. Under the broad reading, changing that URL must follow the declaration and P4 disallows an ordinary bypass; under the narrow reading, the URL need not be recorded and this preference change is outside P4's installed-object/setting requirement. Voluntary recording remains permitted by S8.2-19. The result concerns the requirement, not the mechanism by which it is enforced.

S8.2-6: «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»

S8.2-14: «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

S8.2-17: «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»

S8.2-2: «The rest need not be recorded.»

S8.3-6: «P4. Law. The system provides no ordinary path for changing what is installed and settings past the declaration.»

S8.3-8: «What is installed and settings can be changed past the declaration only by breaking.»

## Compiler and build-tool purpose versus general-purpose work

Variants: C5.1, C5.2, C5.3, C5.4, C5.5.

What the text lacks: S8.1-7 and S8.1-8 do not settle whether executable-producing build functionality is a built-in installation/configuration tool by way of S8.2-10, or general-purpose build/copy work.

The source facts are compilation/linking and executable output (SOURCES.md E083, E093), generated installation rules and a documented install command (E085, E094), and plugin loading (E084). No missing compiler output fact is used to resolve the route.

Reading A applies S8.1-7 because these documented operations create or replace programs, which S8.2-10 places among what is installed. Reading B understands the documented build purpose as general-purpose processing, with copying/link creation expressly excluded by S8.1-8. The generic route definition does not explicitly name compilation or choose between those readings. For C5.3, the documented install target is evidence for reading A, while reading B applies the copy/link exclusion to that output operation; no removing-programs purpose establishes the installer exception in S8.1-4 and S8.1-8. This is recorded as a dispute, not settled by adopting either interpretation. Separately invoked shell/editor/copy/link operations retain their explicit general-purpose classification. C5.4's separately privileged direct bypass remains the breaking branch when the conditions of S8.1-15 hold.

The output declaration requirement is the same under both readings: unchanged packaged objects stop at Q1; other executable output stops at Q2 and requires S8.2-16 coverage. The system behaviour differs: reading A requires the acting build tool itself to record its changes under S8.3-7; reading B does not establish that tool-specific duty. Under both, P4 still forbids an ordinary path changing an installed program past the declaration. This is not permission to leave a general-purpose tool's executable output unrecorded, and it prescribes no enforcement mechanism.

## Saved history: values read versus executable statements

Variants: C7.06 object b (.python_history), C7.17 object c (HISTFILE).

What the text lacks: S8.2-23 does not delimit a file read as history values from saved language statements that S8.2-9 treats as code executable at a person's command; S8.2-6 preserves the order but does not decide that boundary.

E005 and E105 in SOURCES.md document saving and reading the entries as history. Reading A applies the second clause of S8.2-23 to that history-file operation: Q1 no, Q2 no, Q3 no, Q4 program record under S8.2-15, requiring no line under S8.2-2. Reading B applies the capability wording of S8.2-9 to the retained language statements: Q1 no, Q2 yes, program under S8.2-10, without reaching Q4. It reads S8.2-23's values-only exclusion as inapplicable to code that can be executed at command. No observation of another invocation is added; no assertion is made that every possible history file is a valid complete script. The competing readings concern the described retained statements and the scope of the values-only exclusion, so requesting unspecified syntax did not resolve them.

The declarations differ by a required program line or actual derivation coverage under S8.2-16 versus no required history line. Under reading B, P1/P4 require the retained program to be recorded and disallow ordinary unrecorded program changes. Under reading A, writing that history record adds no such obligation. Personally typed commands remain actions under S8.2-4 in both readings, and runtime state follows S8.2-5. This records the two readings without selecting one or changing the questions' order.

## Additional exact text cited by the revised gap analysis

S8.1-4: «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»

S8.1-7: «Built-in tool—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.»

S8.1-8: «General-purpose programs—an editor, file copying, link creation, the command shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.»

S8.2-4: «A command that a person typed himself or herself is that person’s action, not an object.»

S8.2-9: «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»

S8.2-10: «Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.»

S8.2-15: «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»

S8.2-16: «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»

S8.2-23: «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»

S8.3-4: «P1. Completeness. Everything that is installed and every setting, when in force on the computer, are recorded.»

S8.3-7: «Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.»

