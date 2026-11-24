# Saved-file execution group: design and source audit

2026-11-23 UTC. Builder analysis only. No machine probe was run, no refusal was demonstrated, and no shared recipe was edited for this part. The six prior observations remain failures until the integrated rebuilt image establishes otherwise. Read: (not published: orchestration or scratch), `TEXT.md` Sections 8, 9.1, 9.3, A.4.1 and A.4.3, `SENTENCES.md`, `SUP1/step-5.md`, `B2/BUILD-1.md`, `B2/BUILD-2.md`, and the recipe/source files cited below.

## Exact inputs

Commands below are the JSON-decoded `command` values, not suggested substitutes. The first pair runs from the ordinary account's working directory. The direct supplement runs from its `v4-direct` subdirectory. See `B2/build/v4-shell-selftest.py:63` and `B2/raw/round-1/final-2-supplement-inputs/v4-direct-selftest.py:115`.

| Way | Original command | Marker | Original evidence |
|---|---|---|---|
| SAVED-SCRIPT | `printf 'printf SAVED_CODE_RAN\n' > saved.txt; bash saved.txt` | `SAVED_CODE_RAN` | `B2/raw/round-1/final-2/shell.jsonl:23`–24 |
| SAVED-PIPE | `cat saved.txt \| bash` (the backslash in this table is Markdown escaping only) | `SAVED_CODE_RAN` | same, lines 25–26 |
| DIRECT-REDIRECT-STDIN | `bash < saved.sh` | `SAVED_DIRECT_RAN` | `B2/raw/round-1/final-2/supplement/direct.jsonl:27`–28 |
| DIRECT-PROC-FD | `exec 3<saved.sh; bash /proc/self/fd/3` | `SAVED_DIRECT_RAN` | same, lines 29–30 |
| DIRECT-AWK-FILE | `awk -f saved.awk` | `AWK_FILE_RAN` | same, lines 35–36 |
| DIRECT-SCRIPT-HELPER | `find . -maxdepth 0 -exec bash saved.sh ';'` | `SAVED_DIRECT_RAN` | same, lines 37–38 |

Exact fixture bytes (Python byte-literal notation; `\n` represents one LF):

- `saved.txt`: `b'printf SAVED_CODE_RAN\n'`, 22 bytes, SHA-256 `17415ceff55ee272ac1df03cebd32d979e47bc8727836ab76f55a56c8521009d`. Created by the original SAVED-SCRIPT command; inherited by SAVED-PIPE.
- `saved.sh`: `b'#!/usr/bin/bash\nprintf SAVED_DIRECT_RAN\n'`, 40 bytes, mode 0755, SHA-256 `43d50a29262f6b0a31a30fc85806697adb289ad85bd98591fcce61ab7fc5bb2a`.
- `saved.awk`: `b'BEGIN { print "AWK_FILE_RAN" }\n'`, 31 bytes, mode 0644, SHA-256 `c6d3872bf43cbf05e2c48b2f496dcea1f5d36ccc7af58d0f125ed45441dc5889`.

The latter hashes and lengths also occur in the original direct log's fixture rows. All six original results report exit 0 and the marker. Direct supplement results explicitly report unchanged declaration/report. `find` exit status alone is insufficient: observe the marker and execution diagnostic.

For the permitted partner, record these exact code bytes, then use the same dispatch command with the same working-directory resolution. For SAVED-SCRIPT, retain the original write-and-run command as well: a policy that makes the recorded path immutable can fail the write even when a subsequent Bash process still prints the expected marker. Inspect stderr and the writing operation, not merely the final shell status. Exact code coverage must survive or transactionally follow that same-byte truncation/rewrite.

## Existing mechanisms and limits

The existing recipe admits recorded native execution and mappings but explicitly does not classify pipe text (`B2/build/shell.c`, opening comment). Its original raw results already establish that this mechanism does not close these six ways. Do not repeat that test merely to rediscover its result.

An inherited read allowlist would stop a direct script open and the producer's read of saved pipe input. However, denying all unrecorded document reads prevents ordinary creation/editing/readback unless such documents first become recorded. A profile for Bash alone also misses `cat saved.txt | bash`: the consumer sees a pipe, not the file. Denying pipes or all redirected shell input breaks the original permitted action. This is a design limit, not a second measured mechanism failure.

[fanotify documentation](https://man7.org/linux/man-pages/man7/fanotify.7.html) says permission events require a decision before access. FAN_ACCESS_PERM can hold a read, whereas ordinary modification notifications happen too late to provide a write transaction. It expressly says: “does not report file accesses and modifications that may occur because of mmap(2), msync(2), and munmap(2).” Whole-mount monitoring avoids the documented recursive-directory marking race; inherited writable descriptors and concurrent changes still require separate protection.

[fs-verity documentation](https://docs.kernel.org/filesystems/fsverity.html) says: “After this, the file is made readonly”. Thus fs-verity can stabilize recorded bytes, including mapped reads, but cannot itself preserve same-path ordinary edits or the original SAVED-SCRIPT write. Immutable snapshots may be part of a versioned design; blindly sealing every read document is not sufficient.

These are two distinct mechanism families to evaluate, not a record that two build probes have failed. No impossibility argument follows from their limitations.

## Prospective recording mechanism

The strongest general design identified here is a declaration-first transactional writable filesystem, using the existing FUSE kernel interface with a recorded filesystem service. This is a concrete design, not implemented evidence. [Kernel FUSE documentation](https://docs.kernel.org/filesystems/fuse/fuse.html) describes it as: “A filesystem in which data and metadata are provided by an ordinary userspace process.”

1. Ordinary writable persistent files live on the mediated filesystem. Its backing content store is unavailable to ordinary processes. Recorded native applications and unchanged package files remain in the existing protected system store.
2. A write/truncate/create/rename/unlink request reaches the filesystem service before a new persistent version is made visible. The service prepares immutable content and metadata for the resulting version, then prepares corresponding exact declaration rows. It need not guess whether bytes are code: material may be recorded too.
3. The common application transaction durably commits those rows and the namespace/version pointer as one recoverable generation. Read visibility changes only to the committed generation; acknowledgment of the original operation follows a successful application report. Recovery finishes or rolls back the same transaction before admitting ordinary sessions.
4. All readers, including `cat`, Bash, AWK, a helper's descendant, and a reader through an inherited descriptor or `/proc/self/fd`, receive bytes of a committed version. No special recognition of command names, suffixes, marker strings or interpreter flags is needed.
5. Later ordinary edits create another version through the same path, rather than failing because the earlier read recorded the document. Deletion updates declaration requirements and namespace consistently. Existing open descriptors require an explicit version-retention rule and covering rows until their version is no longer readable/executable.
6. Cached writable mappings must not expose changed bytes ahead of declaration application. Disable unsupported writable-mmap modes or implement write mediation with correct page-cache visibility. A claim about all ordinary work requires showing that chosen editor/browser operations still work; a claim of universal coverage needs considerably more than these finite fixtures.

With this design each original marker may print, but its saved code is already recorded. That meets the step's recorded-output alternative; it should be reported as recorded rather than a refused execution. Prospective automatic recording only at first read is weaker: the saved object may already be capable of execution before the read, and its bytes may change after the gate inspects it. First-read recording can still be a bounded prototype only if these limitations are explicitly left open.

## Definition support and strongest objections

- S8.2-19: “What need not be recorded may also be recorded in the declaration.” This permits recording document bytes without declaring that all documents must be recorded.
- S8.1-2: “The computer is brought into conformity with this text, rather than the text being compiled from the computer.” This is the strongest objection to a read-time filesystem inventory. The prospective design writes the next desired generation before publishing that generation; an after-the-fact logger fails this requirement.
- S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.” Recording a hash then allowing later unmediated writes does not satisfy this. Versioned writes and namespace updates are essential.
- S8.1-9: “**In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.” This motivates prepublication write mediation rather than relying solely on first execution.
- S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.” A filesystem service implementing the declared transition is a candidate mechanism; this does not excuse an unmediated root built-in account tool.
- S8.2-4: “A command that a person typed himself or herself is that person’s action, not an object.” The design need not record the typed command; it records the saved object that command produces.

Open author question, not resolved here: does “saving and running a file” in Section 9.3 cover a saved file consumed as instructions through `cat file | bash` or redirected stdin every time a person types the command, or only a saved object with an independently usable launch path? Record both readings in `B2/QUESTIONS-5.md`; neither the failed existing mechanism nor the prospective design authorizes choosing one.

Outcome of this analysis: `?`. It supplies a mechanism design for all six ways and exact historical inputs, not a definition-only impossibility argument and not a tested closure.
