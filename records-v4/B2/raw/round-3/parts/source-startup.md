# Source, startup and editor saved input: builder design notes

Recorded 2026-11-23 UTC. Scope: SAVED-SOURCE, STARTUP-ENV, RC-STARTUP,
EDITOR-SAVED-COMMANDS. These are source/documentation findings, not new machine
observations, closure claims, or independent acceptance. No VM was started.

## Frozen commands and fixtures

All commands run through the ordinary `stand-shell -c` interface. Its initial
working directory and HOME agree; `B2/build/shell.c` fixes both. Do not replace
these commands with a purpose-built wrapper or change the startup options.

| Way | Exact command from round 1 | Exact saved bytes, expressed as a Python bytes literal | Observed round-1 marker |
|---|---|---|---|
| SAVED-SOURCE | `source saved.txt` | `b'printf SAVED_CODE_RAN\n'` | `SAVED_CODE_RAN` |
| STARTUP-ENV | `BASH_ENV="$HOME/saved.txt" bash -c :` | `b'printf SAVED_CODE_RAN\n'` | `SAVED_CODE_RAN` |
| RC-STARTUP | `cd /tmp/v4-extra-7z89hz2f && bash --rcfile /tmp/v4-extra-7z89hz2f/startup.rc -i -c :` | `b'printf "SAVED_RC_EXECUTED\\n"\n'` | `SAVED_RC_EXECUTED` |
| EDITOR-SAVED-COMMANDS | `cd /tmp/v4-extra-7z89hz2f && ed -s < /tmp/v4-extra-7z89hz2f/commands.ed` | `b'!printf "SAVED_EDITOR_COMMAND_EXECUTED\\n"\nq\n'` | `SAVED_EDITOR_COMMAND_EXECUTED` |

Evidence: `B2/raw/round-1/final-2/shell.jsonl` records SAVED-SOURCE and
STARTUP-ENV; their saved.txt preparation is the immediately preceding SAVED-SCRIPT
command, implemented in `B2/build/v4-shell-selftest.py`. The two supplemental
commands and SHA-256 hashes are in
`B2/raw/round-1/final-2/supplement/extra.jsonl`. Their fixture bytes and ownership
are in `B2/raw/round-1/final-2-supplement-inputs/v4-extra-selftest.py`.
The supplemental directory has mode 0700 and uid/gid 1000; both files have mode
0600 and uid/gid 1000. startup.rc has 29 bytes and SHA-256
`a829afcc91f6bf36347cde073a527ce259b35e1b74d7f4b2ac997445294ea28e`;
commands.ed has 44 bytes and SHA-256
`83f83d4ddda12cb3ec60bdc2cef97c112835dd31900571ad4fc819a6ecb09174`.
The positive action must retain the same command and exact source bytes after
those source objects have a covering declaration line; a recorded interpreter
alone is not a covering line for these independently created sources.

## Documented mechanisms before any probe

- The [Bash reference manual](https://www.gnu.org/software/bash/manual/bash.html)
  describes the dot/source operation: “Read and execute commands from the filename
  argument in the current shell”.
- [Bash startup documentation](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files)
  says “The `--rcfile file` option causes Bash to use `file` instead of (not published: record outside this collection).”
  It also documents BASH_ENV selecting a file for noninteractive startup.
- The [ed manual](https://www.gnu.org/software/ed/manual/ed_manual.html) describes
  `!command`: “Shell escape command. Executes command via sh.” This case consumes
  redirected command input; it does not require an executable plugin API.
- The [kernel man-pages documentation](https://www.kernel.org/pub/linux/docs/man-pages/book/man-pages-6.11.pdf)
  states: “The fanotify API does not report file accesses and modifications that
  may occur because of mmap(2), msync(2), and munmap(2).”
- [fanotify permission events](https://man7.org/linux/man-pages/man7/fanotify.7.html)
  let a monitor decide access before allowing the waiting operation. The API
  supplies an opened object descriptor; it does not label its contents code.

The existing `B2/build/shell_boundary.py` profile grants `/** r,` while restricting
native exec/map permissions. Source, startup and editor input use ordinary reads;
these mechanisms therefore explain the retained failures without another probe.
The launcher's --noprofile/--norc options affect its initial shell only; the
explicit child startup commands are documented separately.

## General candidates and their limits

1. A declaration-generated read allowlist for the interpreter/editor would reject
   the unrecorded source reads and admit protected recorded source paths. Used as
   a blanket denial of ordinary writable files, it also rejects ordinary document
   input and free shell redirection. The shared source/data read operation cannot
   establish this case by itself. This is a documented design objection, not a
   new tested failed mechanism.
2. A permission-event gate can record the exact prospective admitted source version
   and apply that declaration before releasing its read. This avoids needing a
   semantic code detector if it optionally records all admitted regular files.
   It needs write exclusion and version identity, not a pathname/hash check alone.
   An already opened writer can change the inode after its hash is checked; mmap
   updates are outside the documented event coverage. Future edits/removals must
   also update requirements or P2 fails. A retrospective close/read log is not
   declaration application. These are engineering requirements, not proof that
   fanotify alone supplies them.

A concrete alternate mechanism for all four ways is a transaction-backed writable
filesystem: the filesystem intercepts create/write/truncate/rename/unlink before
exposing their result, stages exact desired regular-file bytes as a declaration
update, applies that update to an immutable version and only then publishes the
version for reads. Read descriptors pin a declared version. Concurrent writers
serialize through the same transaction; shared writable mappings must participate
through mediated page writes or be replaced with a compatible mediated mapping
implementation. Package and configuration tools use the same transaction boundary.
The person designates the declaration store; it is not inferred from an inventory.
The source commands then read the published source versions unchanged. Ed can
create/edit documents through the filesystem, and ordinary commands/pipelines do
not need syntax filtering. Documents may be optional records, without asserting
that they are installed programs. This is a proposed mechanism, not an implemented
or universally verified system. A deployment must demonstrate its interception
coverage, atomic application semantics and ordinary-work compatibility.

## Textual support and strongest objection

S8.2-19: “What need not be recorded may also be recorded in the declaration.”
This permits optional document rows; it does not make documents mandatory programs.

S8.1-2: “The computer is brought into conformity with this text, rather than the
text being compiled from the computer.” The prospective write transaction treats
requested bytes as declaration input before realization. Merely hashing and
recording already executed bytes would not satisfy that direction.

S8.1-14: “The declaration in force is the declaration of the last application that
the system reported as successful [3, Section 3].” A log entry by itself is not
proof the new declaration is in force.

S8.3-4: “**P1. Completeness.** Everything that is installed and every setting,
when in force on the computer, are recorded.”

S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on
the computer as its line requires.” Exact optional document rows therefore need
synchronized edits/removals too.

Strongest objection: the proposed filesystem must reconcile old successful
requirements, new successful requirements and actual visible bytes at the
transition, including failure and concurrency; merely announcing a transaction
cannot prove the Section 8 guarantees. It must also avoid a permanently retained
old version becoming an uncovered object. This is an unresolved implementation
obligation, not an impossibility argument from the definitions.

## Readings to preserve for the author

Section 9.3 says: “A channel is anything that such a command tries to leave behind:
saving and running a file, registering a service, a timer or an autostart, changing
a setting.”

S8.2-4: “A command that a person typed himself or herself is that person’s action,
not an object.”

S8.2-9: “Is the object code that the computer executes or can execute: on its own,
at a person’s command, or through another program with that program’s rights?”

S8.2-23: “A file that a program executes as code counts as code even when it
contains setting values; a file that a program only reads as values does not count
as code.”

Reading A: a saved source/startup/editor file remains an object executed as code,
even when its consumption is requested by a fresh typed command each time; Section
9.3's saving/running language includes these forms.

Reading B: Section 9.3's leave-behind wording distinguishes a persistent installed
launch arrangement from a person repeatedly typing an evaluation command; the
person's immediate evaluation could be the exempt action. Whether that reading
can coexist with S8.2-9 and S8.2-23 is an author question, not a license to classify
these cases as closed. No choice between the readings is made here.
