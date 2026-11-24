# Supplement 1, step 5: unresolved readings

Recorded 2026-11-23 UTC. These questions preserve readings for the author. They neither amend the fixed text nor decide a case. Scope is the fifteen saved-code ways, the account tool and the ordinary-work case of `SUP1/step-5.md`. A case depending on a choice below remains `?` unless that choice is resolved outside this builder's authority.

## Typed commands and saved code

Section 9.3 says: “A command typed by a person is not considered a channel for bypassing the declaration.” It then says: “A channel is anything that such a command tries to leave behind: saving and running a file, registering a service, a timer or an autostart, changing a setting.”

Reading A: a saved file remains a separate object when a person types a command to execute, source, import, deserialize or evaluate it each time. “Saving and running a file” covers the saved input even when the command passes its bytes through a pipe or evaluates them inside a recorded program. The command is exempt; the saved object is not.

Reading B: “leave behind” concerns a persistent launch arrangement beyond the person's immediate action. When a person types the evaluation command every time, the evaluation may itself fall under the typed-command exemption, even if it reads saved text. This reading must be reconciled with the explicit references to execution at a person's command and through another program below. The builder does not choose that reconciliation.

The exact anchors are S8.2-4, S8.2-9 and S8.2-23, quoted below. The committed cases are not removed merely because Reading B has been raised.

## Automatic recording and the primary description

Reading A: a filesystem service may accept a write request as intended future state, record exact desired bytes in designated declaration files, apply them, and only then expose the resulting saved file. This is prospective declaration-driven realization. S8.2-19 permits voluntarily recording documents too; S8.3-7 explicitly contemplates tools adding changes to the declaration.

Reading B: automatic capture of a general program's write data is compiling text from the computer even when those data have not yet been published as a saved file; S8.1-2 would exclude that construction. The builder cannot decide whether staging inaccessible desired bytes already crosses the sentence's boundary. A logger that records only after visible writes or execution does not resolve this question by calling itself prospective.

The question is about ordering and primary status, not whether every document is required to be recorded. The design does not add that requirement.

## Old saved versions and continuing readers

A proposed implementation may preserve an old immutable file version while a reader still has it open, then publish a new version at the original path. Reading A: a line may require the old version to remain as a separately named stored object, while another line describes the current path; P2 can then be checked against those distinct stated requirements. Reading B: retaining the old version's row as if it still described the replaced live path misstates its required state; P2 fails even though its digest survives somewhere. The implementation must state which objects its lines describe. This is not permission to treat an arbitrary cached blob as covering an old live pathname, or to infer coverage without an own/package/derived relation.

No generic question about all concurrency or all operating systems is added here. The issue matters directly to same-path rewrites in SAVED-SCRIPT, PYTHON-IMPORT and PICKLE-CODE and to ordinary document editing.

## Exact sentence anchors
- **S8.1-2** The computer is brought into conformity with this text, rather than the text being compiled from the computer.

- **S8.1-3** The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.

- **S8.1-9** **In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.

- **S8.1-12** The required state of a recorded object is stated by its line.

- **S8.1-14** The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].

- **S8.2-4** A command that a person typed himself or herself is that person’s action, not an object.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-19** What need not be recorded may also be recorded in the declaration.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

- **S8.3-5** **P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

- **S8.3-7** Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.


## Retained backing copies and privileged reads

The candidate filesystem retains blobs referenced by the current and preceding generation. Its current declaration's objects map does not necessarily include blobs needed only by the preceding generation. A root process can potentially read such a protected blob using a general interpreter. Protection from ordinary pathname access is not proof that the object cannot be executed on the computer.

Reading A: a retained code-bearing copy can be started through that privileged read, so it is in force under S8.1-9 and requires current coverage under P1. Merely retaining its old declaration file does not make that declaration in force under S8.1-14. Reading B: privileged use deliberately bypassing the active filesystem generation may fall under breaking, but the definition describes a change to what is installed or settings; reading or executing already saved bytes alone is not expressly listed. The builder cannot declare all root execution to be breaking by adding such a rule.

S8.1-15: “**Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.”

S8.1-16: “Breaking is a violation on the person’s part rather than a property of the system, and it refutes no property.”

This is a qualification of the proposed mechanism's P1/P2 claims, not an eighteenth experimental case or a request to block arbitrary root operations. The committed scope remains fifteen saved-code ways, root account administration and ordinary work. The present implementation is not claimed to record every retained prior-generation backing copy in its current declaration.
