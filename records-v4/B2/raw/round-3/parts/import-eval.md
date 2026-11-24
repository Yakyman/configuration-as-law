# Saved imports, evaluation and dispatch: build input assessment

Recorded 2026-11-23 UTC. Builder component analysis, not an acceptance review or a machine observation. No new probe was run. Scope: PYTHON-IMPORT, PICKLE-CODE, DIRECT-READ-EXEC, JIT-SAVED-INPUT, DISPATCHER-SAVED. Exact original expected-command records are copied without editing into `import-eval-commands.json` alongside this file, with source paths and line numbers. No replacement invocation may silently stand in for one of them.

## Original fixtures and positive counterparts

| Way | Fixture and original evidence | Same-code permitted action |
|---|---|---|
| PYTHON-IMPORT | `loose_module.py` bytes `print("IMPORTED_UNRECORDED")\n`; shell.jsonl lines 31–32 | Cover these exact bytes, keep current-directory import resolution, execute `python3 -B -c 'import loose_module'`; if repeating the full original compound command, its preceding identical write must work too. |
| PICKLE-CODE | `serialized` bytes `cbuiltins\nprint\n(S'PICKLE_EXECUTED'\ntR.`; shell.jsonl lines 33–34 | Cover these exact bytes, allow the original `pickle.load(open("serialized","rb"))` route. The original single typed command first writes the file; predeclaring an immutable file must not turn that write into a false positive failure. |
| DIRECT-READ-EXEC | `saved.py` bytes `print("READ_EXEC_RAN")\n`; direct.jsonl lines 32–33; fixture source `B2/raw/round-1/final-2-supplement-inputs/v4-direct-selftest.py` | Cover exact source bytes and execute the same `python3 -B -c 'exec(open("saved.py").read())'` command from its fixture directory. |
| JIT-SAVED-INPUT | `machine.bytes` six bytes hexadecimal `b8 2a 00 00 00 c3`; SHA-256 `11db5348e275fb704be582e8005ee7d604f7f17b154d6cc644d240eef29d456a`; extra.jsonl lines 35–36 | Cover exact saved bytes; same ctypes/mmap sequence must still print `JIT_SAVED_INPUT_EXECUTED 42`. Denying all executable anonymous mappings fails this positive counterpart. |
| DISPATCHER-SAVED | `instructions.ops` bytes `PRINT DISPATCHER_SAVED_EXECUTED\n`; SHA-256 `08a7984a7805319b3b105b98c2da1d9efdfdf841c166266b74b8a803923be3ef`; extra.jsonl lines 49–50 | Keep the exact recorded dispatcher, cover exact instruction file, and invoke its original `--file` path. Changing the dispatcher into a new policy-aware wrapper does not preserve the same recorded program. |

The original extra fixture directory is `/tmp/v4-extra-7z89hz2f`; retain it for the literal original commands. The dispatcher prerequisite is installed in the original source lines 259–279, and its exact row is in extra.jsonl's DISPATCHER-INSTALL expected event. The recorded dispatcher uses a Python shebang, chooses argv text or `pathlib.Path(...).read_text()`, splits the text and handles PRINT directly. It never calls eval or exec on the saved instructions. Its source bytes are part of that recorded row.

The round-1 result for all five is actual marker output with no declaration change. The aggregate logs and unchanged-report observations are execution evidence, not an impossibility argument.

## Distinct existing-mechanism limitations

1. Native execution and executable-file mapping admission is already implemented, not hypothetical: (not published: record outside selected evidence) grants exact `ix` paths but also `/** r`. Each of these five attempts reads saved bytes inside an already admitted program. For imports, pickle, direct evaluation and the dispatcher there need not be a new executable-file mapping at the semantic execution point. JIT copies ordinary read bytes into anonymous executable memory. Round-1 records establish failure of that native boundary for all five.
2. General file-read restriction can refuse unrecorded reads, but restricting every ordinary process to immutable declared input would also stop reading a newly edited ordinary document. Selectively restricting only known interpreter binaries misses a recorded custom dispatcher or another evaluator. The original dispatcher is a concrete counterexample to a rule limited to Python eval/import APIs. This is a design rejection from its inputs and required work, not a claim of a second performed VM trial. No additional variant of this restriction should be tried without naming a genuinely different general mechanism.

A separate JIT option, denial of `PROT_EXEC` anonymous mappings or writable/executable memory, lacks the saved-input provenance needed to distinguish the negative fixture from its identical recorded positive. It fails the requested paired case by construction. Python-level audit hooks are insufficient as a general enforcement mechanism and leave the custom dispatcher route untouched; they would also need to retain ctypes for the required positive JIT case.

Primary documentation consulted before any proposed probe:

- Kernel seccomp documentation, https://docs.kernel.org/userspace-api/seccomp_filter.html : “BPF programs may not dereference pointers”; seccomp observes syscall numbers/arguments, not a later interpretation of already read strings. The same document explicitly separates logical behavior/information-flow policy from syscall filtering. This is why a syscall filter alone cannot recognize the dispatcher instruction semantics.
- Python audit hook documentation, https://docs.python.org/3/library/sys.html#sys.addaudithook : “They are not suitable for implementing a ‘sandbox’.” Its documented native-hook requirements and arbitrary-memory caveat rule out presenting a Python callback as complete containment while retaining unrestricted ctypes.
- Python pickle documentation, https://docs.python.org/3/library/pickle.html : “The `pickle` module is not secure. Only unpickle data you trust.” Its documented code-execution behavior confirms that a serialization filename does not establish inert material.

These online documents establish general interface limitations, not a measurement of the guest's version or policy.

## Concrete alternate-system mechanism for every open way

Mechanism, not a definition-only impossibility argument: a transactional managed filesystem records write intents before publication. Interpose on persistent object creation/replacement/truncation and metadata changes in the ordinary namespace, stage the requested exact bytes in an inaccessible version store, and submit a declaration transaction stating the next immutable file version and path mapping. Commit/apply/report that declaration and publish the corresponding filesystem view through one atomic generation switch. A reader obtains a version tied to the committed generation, never unrecorded staged bytes. An initial import/eval/read/pickle/dispatcher operation therefore receives only recorded saved bytes; JIT's later anonymous copy remains derived from the already covered saved input. Existing recorded bytes pass the identical path unchanged. This records ordinary material too, an implementation choice permitted by S8.2-19, not a new requirement to classify documents as programs.

For the inline write cases the filesystem operation is the requested change, and the declaration transaction precedes the visible change. Identical writes to an already recorded version can be acknowledged without changing that version. Changed bytes use a new declaration generation. Ordinary pipelines and typed commands continue; editing, browser saves and package transactions enter the same filesystem publication gate. Runtime pipes and network input need not be saved or independently declared; installed programs and built-in configuration changes still require their own original coverage/tool transactions. Root direct changes outside tools remain possible breaking.

This is concrete about object, moment and actor, but not implemented or proved here. It requires atomic view/declaration/report publication, failure recovery, mediation of all writes including mmap/direct I/O and aliases, preservation of permissions and Unix operation semantics, and handling old readers across generation changes. For removal it must revoke old execution authority and running descendants when required, rather than treating a stale open version as permanently covered. The current prototype's cgroup freezer is not automatically a solution: a filesystem request blocked in kernel I/O may prevent the freezer acknowledgement, and freezing the transaction client can deadlock the service. These are implementation obligations, not proof that the definitions contradict one another.

Strongest objection: declaration capture could merely inventory an already existing file, violating S8.1-2. The proposed mechanism avoids that specific objection only if it treats uncommitted writes as inaccessible intent and makes the declaration the source of the published object. A post-read log or post-write census does not meet that ordering. A second objection is P2 at the atomic generation boundary and continued access through old mappings; claiming all three properties needs a proof of those invariants, not five passing markers. Consequently this prospective mechanism prevents a warranted universal impossibility conclusion but does not close an image case.

## Exact textual anchors and unresolved readings

- S8.1-2: “The computer is brought into conformity with this text, rather than the text being compiled from the computer.”
- S8.1-9: “An installed object is in force if it is on the computer; a program, if it runs or can be started.”
- S8.1-14: “The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].”
- S8.2-4: “A command that a person typed himself or herself is that person’s action, not an object.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-19: “What need not be recorded may also be recorded in the declaration.”
- S8.3-4: “**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.”
- S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”

Question to preserve in QUESTIONS-5: Does “saving and running a file” in Section 9.3 cover a saved instruction file every time a person types an otherwise exempt command to read/evaluate it, or does the exemption for the person's command extend to that evaluation when no autonomous future launcher is left? The first reading treats all five saved objects as the channel independently of the typed invocation; the second can exempt an operation because it is explicitly typed each time. Neither reading is adopted here to erase committed cases.

Question to preserve: Does transactional optional recording of every persistent write intent count as the declaration being primary when bytes are staged privately before publication, or does S8.1-2 exclude that automatic recording even before the object can be used? The text permits automatic tool recording and optional material recording, but it supplies no author decision about this exact construction. Both readings and the publication-order distinction must remain visible.

No definition-only argument that *every* system must fail any of these five ways has been established. For every one left open, the deliverable choice here is **mechanism**.
