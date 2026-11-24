# Supplement 1, step 5: mechanisms for ways left open

Recorded 2026-11-23 UTC. This is a builder design record. It supplies concrete prospective mechanisms for all fifteen ways so that any way left open by the final image has a named alternative. It does **not** assert that the image closes any case, that the prospective system has been implemented, or that an impossibility argument has been established. Final observed status and evidence belong to `BUILD-3.md`; acceptance belongs to the second party and separate review.

The chosen deliverable for every saved-code way is **mechanism**. No definition-only argument that every system having P1, P2 and P4 must fail the permitted action or ordinary work is established. Failed prototype mechanisms do not entail such a conclusion. Questions depending on the author's reading are preserved in `QUESTIONS-5.md`.

## Evidence and mechanisms already considered

The first round's native executable/file-mapping admission failed all fifteen saved-input attempts. The exact commands and output are in `raw/round-1/final-2/shell.jsonl`, `supplement/direct.jsonl` and `supplement/extra.jsonl`, as named by `SUP1/step-5.md`. `build/shell_boundary.py:generate` permits ordinary reads and admits recorded native execution; evaluation of read data is not a native execution permission check.

The independent component source assessments are `raw/round-3/parts/saved-inputs.md`, `source-startup.md`, `import-eval.md` and `accounts.md`. They distinguish historical measured failures from source/documentation rejection of candidate mechanisms. A blanket read allowlist blocks ordinary document reads; a permission-event read recorder needs stable version identity and cannot alone mediate mmap writes; denial of executable anonymous memory blocks the same recorded JIT positive action; interpreter-specific hooks omit arbitrary dispatch. These are distinct mechanism limitations. They are not fabricated records of two new machine trials. No further variants of those same mechanisms are proposed as closure by themselves.

## One general alternate-system mechanism

The object boundary is a managed persistent filesystem, backed by inaccessible immutable versions and a declaration generation. It uses an existing filesystem mediation interface, such as FUSE, rather than inspecting command strings or filenames for code. The filesystem service acts on an intended mutation before publishing it. It voluntarily records all persistent regular-file versions in the mediated namespace, including material, so it need not decide whether an arbitrary byte string is code.

1. A create, write, truncate, rename, unlink or metadata request is received by the filesystem service. Requested data are inaccessible staging input. No executable or readable unrecorded file version is published, even briefly.
2. The service constructs exact desired declaration rows for content, path mapping and metadata. Required-state descriptions distinguish immutable stored versions from current path entries. The designated declaration is the input to the resulting filesystem realization, not a census of already visible changed files.
3. One recoverable transaction commits the declaration generation, matching filesystem namespace and successful-application identity. Publication must be one atomic boundary shared by readers and declaration queries; separate renames of unrelated state files are insufficient without an additional visibility barrier. Recovery exposes only a consistent committed generation before ordinary use resumes.
4. Reads and mappings resolve a committed version. A pipe producer, interpreter, startup reader, editor, importer, deserializer and custom dispatcher all see already covered saved bytes. Execution does not require a new code-classification decision. Network and typed instructions that remain runtime-only are handled under the existing runtime rules; the mechanism does not invent a separate declaration requirement for each pipe buffer.
5. Subsequent writes are new intended versions and run through the same transaction. Exact same-byte rewrites remain possible. This preserves the original compound commands that first write and then execute, and lets ordinary document creation/editing continue. Installed package and built-in configuration operations retain their own required coverage and transaction paths.
6. An old version readable through a descriptor or mapping remains explicitly covered under a distinct, accurate stored-version requirement while it is available. Its obsolete path requirement is removed or updated. On removal of its last covering line, the system revokes remaining execution/reader authority as required and removes its contribution; a permanently exposed undeclared old blob is not an acceptable cache exception.

A practical implementation must mediate aliases, preexisting descriptors, writable mmap, asynchronous/direct I/O and alternative writable mounts, or constrain them in a way that still permits these exact seventeen cases. Simply choosing `direct_io` or taking a lock is not proof of those properties. The scope here is the committed finite cases, not every application workload.

## Per-way mechanism and preserved action

| Way | What the service records before publication; what checks or uses it | Permitted action preserved |
|---|---|---|
| SAVED-SCRIPT | Exact saved.txt version at the original write; Bash reads committed version | Same write-and-Bash command and same code |
| SAVED-PIPE | Exact saved.txt version; cat reads committed bytes before feeding pipe | Same cat-to-Bash pipeline |
| SAVED-SOURCE | Exact saved.txt version; current shell reads committed version | Same source command |
| STARTUP-ENV | Exact saved.txt version selected through BASH_ENV | Same child shell and environment selection |
| PYTHON-IMPORT | Exact loose_module.py version at creation/rewrite; import reads it | Same code, current-directory lookup and import command |
| PICKLE-CODE | Exact serialized version at its write, before pickle.load reads it | Same byte stream, write/read/deserialization sequence |
| DIRECT-REDIRECT-STDIN | Exact saved.sh version; redirection opens committed version | Same Bash stdin redirection |
| DIRECT-PROC-FD | Exact saved.sh version pinned by open descriptor | Same descriptor and /proc/self/fd command |
| DIRECT-READ-EXEC | Exact saved.py version; open/read receives committed bytes | Same typed exec(open(...).read()) |
| DIRECT-AWK-FILE | Exact saved.awk version; AWK reads committed version | Same awk -f command |
| DIRECT-SCRIPT-HELPER | Exact saved.sh version; helper's child reads committed bytes | Same find -exec Bash route |
| RC-STARTUP | Exact startup.rc version; startup reader receives committed bytes | Same explicit rcfile/interactive command |
| EDITOR-SAVED-COMMANDS | Exact commands.ed version; redirected command reader receives it | Same editor command and shell escape |
| JIT-SAVED-INPUT | Exact six-byte machine.bytes version before Python reads it | Same ctypes/mmap machine-code call, including executable anonymous memory |
| DISPATCHER-SAVED | Exact instructions.ops version; unchanged recorded dispatcher reads it | Same custom instruction parser and --file command |

These mechanisms allow the attempt to execute only after recording its saved input. They do not claim literal refusal when the recorded-output alternative succeeds. The test report must distinguish those outcomes. The positive counterpart additionally checks that the same already recorded code runs by the same way.

Ordinary free shell commands, pipelines and redirections remain available because the mediation point is the resulting persistent object. Documents and browser saves can be optional declaration objects without being classified as installed programs. Package installation and account changes still need declaration-writing tools. Network access and page rendering do not require shell syntax restrictions.

## Definition-based constraints, not an impossibility proof

The sentence quotes below are exact copies from `SENTENCES.md`. Their implications for the proposed mechanism are:

- S8.1-9 together with S8.2-9 and P1 means coverage cannot wait until the first observed execution if the newly saved object can already be started. Prepublication write mediation addresses that timing; first-read logging alone does not establish it.
- S8.1-2 and S8.1-3 require a designated primary description. The write request is intended future state; staging cannot itself become ordinary exposed state before recording. Treating an arbitrary log as the declaration is insufficient.
- S8.1-12, S8.1-14 and P2 make exact line semantics and successful-generation identity important. A digest in a file, without actual required state or application, is not enough. Optional document lines incur P2 too.
- S8.2-16 requires a real own/package/derived covering relation; the interpreter's line is not automatically the saved input's line. Old blobs need explicit surviving coverage if available for execution. Current-path and old-version requirements must not contradict each other.
- S8.2-19 permits the voluntary material-recording choice; it does not classify all material as mandatory installed objects, prohibit unrecorded material in other systems, or license blocking ordinary work.
- S8.3-7 requires the account tool to record changes even as root. General filesystem code mediation alone is not a substitute for that account transaction.

- **S8.1-2** The computer is brought into conformity with this text, rather than the text being compiled from the computer.

- **S8.1-3** The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.

- **S8.1-9** **In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.

- **S8.1-12** The required state of a recorded object is stated by its line.

- **S8.1-14** The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-19** What need not be recorded may also be recorded in the declaration.

- **S8.3-1** The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.

- **S8.3-4** **P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.

- **S8.3-5** **P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

- **S8.3-6** **P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.

- **S8.3-7** Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.

- **S8.3-8** What is installed and settings can be changed past the declaration only by breaking.

## Strongest objections and limits

**Primary-description objection.** Automatic ingestion of write data may be challenged as compiling the declaration from the computer. The defense is strictly prospective ordering: record desired bytes, apply, then publish. Whether private staging itself defeats that reading is preserved in QUESTIONS-5, not decided by renaming a log. No successful final readback repairs already exposed unrecorded execution.

**Continuous P1/P2 objection.** A mutable filesystem and a separate declaration/report store can diverge between writes. The proposed atomic shared generation is an implementation obligation, not a demonstrated feature of the image. Freezing ordinary shell processes alone does not prove consistency for root readers, cached pages, filesystem service threads or kernel access. A blocked filesystem request can also prevent freezer acknowledgement or deadlock its own transaction. Exactly which actors share the visibility boundary must be shown.

**Old-version objection.** An immutable blob's existence does not make the original replaced path satisfy its old line. Conversely deleting the old covering line while a descriptor can still supply executable bytes may violate P1. Distinct accurately stated version and namespace requirements, coverage retention and eventual revocation are needed. Copying file requirements blindly into each generation cannot prove them.

**Ordinary-work objection.** Making every recorded file immutable at its ordinary path breaks same-path writes and editing; it also breaks original self-writing import/pickle commands. Versioned mutation must remain transparent to those exact commands. Denying mmap, pipes, interpreters or document reads cannot be counted as a closure if the corresponding permitted action or ordinary session fails.

**Account objection.** A post-hook sees an already existing account and can leave an uncovered interval. A pre-hook that creates the account may make the original native operation fail as duplicate. A general alternative is a shared account-database transaction API: preserve native argument processing, collect intended passwd/group/shadow changes privately, generate declaration rows before live database publication, then atomically switch their shared generation and success identity. All account readers and tools must follow that generation. Direct privileged edits outside built-in tools remain breaking. This is a concrete mechanism for the sixteenth case, not an argv-specific patch or a universal proof.

None of these objections is converted into an argument that no possible system can satisfy the definitions. They identify what an actual implementation must establish. A failed image case without a separately reviewed definitions-only impossibility argument retains outcome `?` under the committed step.

## Retained backing copies: explicit implementation weakness

The current candidate stores immutable blobs for both the active and preceding generation. A blob needed only by the preceding generation is not necessarily present in the active declaration's objects map. A retained historical declaration is not automatically the declaration in force: S8.1-14 above binds that status to the last successful application. The source implementation must not be described as recording every retained backing copy in the current declaration.

A protected directory can prevent the ordinary account from reading a copy while root can still read it into a general interpreter. That is relevant to S8.1-9's “can be started” condition. No text supplied here makes every privileged read or execution breaking. S8.1-15 defines breaking as a change to what is installed or settings through privileged power outside built-in tools; whether the read/execution alone qualifies is preserved with both readings in QUESTIONS-5. No new blanket root execution prohibition is proposed, and no extra experimental case is added.

A concrete stronger mechanism would keep explicit own-line requirements for every retained backing version in the active declaration, distinguishing each content-addressed stored object from the live path requirement. The filesystem would publish those retained-object rows together with the active namespace and application identity, keep ordinary admission tied to the live namespace, and transactionally delete or retire a backing object and its coverage only when no reader, recovery obligation or remaining contribution needs it. It must not claim that a hash retained somewhere makes a replaced live pathname satisfy its obsolete line. This alternative also requires a coherent deletion boundary: first dropping coverage while leaving an executable copy readable can violate P1; first deleting a still-required stored object can violate P2. An atomic object/declaration view, or another concretely demonstrated compatible transition, remains an obligation of that stronger system.

This stronger retained-copy mechanism is prospective. The tested finite sixteen-way boundary, even if successful, does not establish whole-system P1/P2 for backing stores, privileged arbitrary interpreters or all generation transitions. The ordinary-work case supplies its own bounded result.

## Required report-header wording

The task fixes a header containing the word “refused”. Keep that literal wording
and count actual denials there. Successful automatic recording is the other
explicitly allowed outcome of the committed step; report its count separately
instead of calling a successful command a refusal. Per-way rows must say
“recorded before use” where markers executed with coverage. The final message
must identify the mechanism or argument supplied for each way that was not
literally refused. For this image all fifteen have a mechanism above. A way whose
timing/coverage is not established must not count as successful automatic
recording merely because a final hash appears in a declaration.
