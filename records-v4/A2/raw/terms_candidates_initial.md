# Terms sweep: candidates and attempted refutations

Beyond the published plan. These are candidates for independent review, not accepted cards or outcomes of the published checks. TERMS.tsv contains 55 term-boundary rows. Source passages are stored once in TERM_SOURCES.md; each table entry carries the corresponding URL.

## 1. A mixed file has no specified unit of classification

Type: TERM. Concrete object: an SQLite database storing SQL triggers in its schema table and ordinary table records. Sources: SQLITE and TRIGGER in TERM_SOURCES.md. The documented file format places trigger SQL in sqlite_schema.sql alongside the same database's ordinary tables.

- S8.2-3: “The rule applies to objects that are on the computer.”
- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-23: “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

Why it fails: The text does not specify whether the object supplied to the four questions is the database file, the stored trigger definition, or a data record. Classifying the executable schema as a separate object can require recording only it, whereas classifying the containing executable document can require recording the file. The question order starts after that object choice and cannot choose it. This is a difference in recorded extent, not merely terminology.

Strongest objection: S8.2-23 says how an executed file counts. An SQLite engine reads the database as a structured file and extracts SQL; the sentence does not identify whether indirect execution of contents makes the whole file code or identify subfile objects. Additional risk to this candidate: S8.2-21 can separately exempt restricted trigger code; this must be resolved in the sandbox card before using that example as a final mandatory-recording witness. A mixed SSH configuration with Match exec and ordinary client values is a second primary-documented boundary (SSH source); the shell command is executed while the rest are read as values.

Declaration difference: whole mixed file recorded versus just executable/launching entries recorded and ordinary data omitted.

Other objects: SSH Match exec files; executable document containers; database schemas mixed with ordinary records. Do not accept examples without their own primary evidence.

## 2. A recorded tool may or may not cover everything it produces

Type: TERM. Concrete object: a Python bytecode cache produced from a personal source file by py_compile. Source: PY in TERM_SOURCES.md. It is a compiled file generated from the specified source by an installed tool.

- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

Why it fails: A line for the compiler is a cause of the compiled output, but so is the line for the source if any. The text does not define the relation from a line needed to count as built from it. Reading that relation as program provenance covers arbitrary outputs of a recorded compiler; reading it as declared output/input provenance does not. Q2 says the output is code under either reading and does not choose its recording line.

Strongest objection: The examples in S8.2-16 point to compiled copies and declared package dependencies. These suggest a narrower relation but do not say that tool provenance is insufficient; adding a restriction would supply the missing criterion. S8.6's unnumbered history example says a history file was not built from what is recorded, which supports a narrow intention but supplies no general boundary for generated code.

Declaration difference: compiler/package line alone covers bytecode versus source or output requires an additional line.

Other objects: outputs of compilers, code generators, project build tools. Merge with any card already addressing the breadth of S8.2-16.

## 3. Root in a user namespace leaves the breaking exemption open

Type: TERM. Concrete object: an ordinary rootless container whose root identity has full privileges within its user namespace but no host privilege. Source: USERNS in TERM_SOURCES.md. Additional primary source: https://docs.podman.io/en/stable/markdown/podman-create.1.html documents rootless-container mapping to the invoking user's identity.

- S8.1-15: “**Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.”
- S8.3-1: “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.”
- S8.2-22: “A program that runs as its own process on the computer, including in a container, is a program.”

Why it fails: Local full privilege and host unprivileged status coexist. The definition does not specify which privilege domain makes a direct modification breaking. Consequently it leaves open whether properties continue to apply after a namespace-local privileged modification. Q2 and S8.2-22 make container code subject to recording without deciding this exemption.

Strongest objection: The words through the power of superuser privileges can naturally mean privileges over the particular changed object, which would count namespace-local administrative power. Nothing expressly chooses that domain over the computer-wide domain invoked elsewhere. Qualification: a concrete final witness must actually require namespace-local privilege; merely writing a file that the host user already owns does not prove use of that power, and must not be used to claim a conflict.

Declaration difference: properties remain required after modification versus the modification excludes the run as breaking; this is an open property predicate rather than a name dispute.

Other objects: rootless containers and nested user namespaces. Do not infer a general contradiction from ordinary systems lacking enforcement.

## 4. Service enablement has an implementation meaning and a broader meaning

Type: TERM candidate, weak. Concrete object: a systemd static service. Source: SYSTEMCTL in TERM_SOURCES.md expressly says static is not enabled and has no enablement provisions.

- S8.1-11: “A service is in force if it is enabled; an account, if it exists.”
- S8.1-12: “The required state of a recorded object is stated by its line.”
- S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”

Why it may fail: The term enabled could refer to explicit installation enablement or to being eligible for dependency/socket activation; the text does not select a mapping. The question order classifies a service but does not define its in-force predicate. A requirement about its configured active state could therefore yield different P2 checks.

Strongest objection, sufficient to reject unless further evidence changes it: Literal implementation enablement gives a clear answer: static is not enabled. The text did not promise to use a broader eligibility meaning, and a line can state the required service state under S8.1-12. Keep as a boundary examination, not an accepted card on this evidence.

## Rejected and merged boundaries

- Runtime DHCP addresses: S8.2-5 assigns runtime objects to their creating policy; automatic address selection is not necessarily a person-chosen value. A persistent lease file is a record absent additional facts. No new card.
- Personal program settings versus whole-computer settings: the explicit service-parameter list S8.2-13 and launch/access extension S8.2-14 often decide the example. Database session values have not supplied a surviving contrary declaration.
- Sandbox rights and indirect effects: Q2 process credentials versus language capability, and S8.2-21's itself, belong with the sandbox exemption collision. Avoid multiplying that same gap under PAC files and triggers.
- Modified packaged executable: lack of remains-as-received in S8.2-16 is relevant to recording coverage, and may belong in the provenance/Understanding analysis. A pure Q1-versus-Q2 label change is not a card.
- Generated program records with human authorship: two Q4 branches overlap but both permit omission; put in NAMES.tsv.
- General-purpose editor containing installer: S8.1-5 and S8.1-8 expressly settle the functionality boundary. A shell subprocess invoked by a maintainer script raises attribution wording, but the installer-function exception is the strongest deciding sentence; no independent surviving card established.
- Ordinary path: S8.3-8 is stronger and supplies all changes except breaking; do not claim ordinary as a separate unbounded exemption.
- Declaration edit timing, preventing unrecorded execution, and record/material storage: explicitly outside definition in 8.5, not gaps.
