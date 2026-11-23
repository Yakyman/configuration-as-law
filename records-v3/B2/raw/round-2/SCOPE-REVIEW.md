# Round 2 scope closure review

Evidence reviewed: [integration-05-live.jsonl](integration-05-live.jsonl), [self-test recipe](../../build/round2-selftest.py), [native probes](../../build/round2-probe.c), [launcher](../../build/session.c), [policy generator](../../build/codeboundary.py), B1/CHANNELS.md, BUILD-1.md and the prior STAND disposition. The integration log contains 118 passing result rows, two passing content assertions and a passing summary. It is not rebuilt-image evidence.

Recommendation updated after partial rebuilt-2 evidence: **all 45 scope variants are candidates for CLOSED only after the complete rebuilt-image suite and managed-service integration pass.** With the existing 10 closed variants preserved by regression, that would yield 55 closed in total of 88. These numbers are conditional, not a build result. No file outside this review was changed for this assessment.

Closure means the supplied system blocks the full input route under its finite admitted interfaces, including refusing unsupported launches. It does not promise unrestricted stock application compatibility. Native/interpreted execution, writable-memory protection, source closure, removal and service inheritance must be considered together; a launcher rejection alone does not prove an arbitrary already-running interpreter safe. The admitted malicious scripts and native probes supply that additional evidence here. Out-of-scope transaction/device shortcomings are not repeated as objections to these code-boundary rows.

| Scope variants | Recommendation after prerequisites | Mechanism and integration-05 evidence |
|---|---|---|
| C4.1, C4.2, C4.3 | CLOSED | Exact launch membership plus executable-map policy independent of download/extraction path or suffix. NATIVE-downloaded, NATIVE-nested-extracted.renamed, NATIVE-build-output and NATIVE-KERNEL. The path fixtures test the resulting artifacts, not each transport client. |
| C4.4 | CLOSED | Interpreter inputs require sealed recorded entrypoints; mutable imports/reads unavailable. FILE-*, SOURCE, EXEC-OPEN, IMPORT, LOADER. |
| C4.5 | CLOSED | No free interpreter stdin or shell expansion. PIPE-*, SEALED-PIPE, SEALED-FIFO, SEALED-SOCKET, PROCESS-SUBSTITUTION. |
| C5.1 | CLOSED | Output inert until recorded; ADMIT and POSITIVE show the declared route. NATIVE-build-output refuses. Compiler fixture creation is external operator work, not ordinary compiler access. |
| C5.2 | CLOSED | Generic configure/build/generator/recipe interfaces removed; sealed admitted programs cannot launch unrecorded output. COMPILER-CONFIGURE, COMPILER-GENERATOR, MAKE-RECIPE, NATIVE-build-output. |
| C5.3 | CLOSED | Prefix/PATH/symlink spelling grants no launch authority. NATIVE-prefix-bin-app, NATIVE-SYMLINK. |
| C5.4 | CLOSED | Recorded files and input snapshot immutable to ordinary sessions; changes require application. OVERWRITE, VERIFY, existing update regression prerequisite. |
| C5.5 | CLOSED | Unrecorded plugin input cannot enter compiler/runtime closure. COMPILER-PLUGIN, CUSTOM-LOADER, NATIVE-KERNEL/DLOPEN. |
| C7.01 | CLOSED | Fixed script/interpreter pair and checksums; no generic interpreter file launch. FILE-*, POSITIVE, malformed entrypoint refusal and unchanged-generation checks. |
| C7.02 | CLOSED | Shebang does not confer launch authority. SHEBANG. |
| C7.03 | CLOSED | Fixed argv for sealed entries; generic -c/-e launch removed. INTERPRETER-*, SEALED-ARGS. |
| C7.04 | CLOSED | Sealed stdin is null; inherited descriptors closed; sockets/IPC unavailable. PIPE-*, SEALED-PIPE/FIFO/SOCKET, HEREDOC, PROCESS-SUBSTITUTION, native IPC denials. |
| C7.05 | CLOSED | No inherited input/readable mutable descriptor route. REDIRECT-*, PROC-FD, SEALED-REDIRECT. |
| C7.06 | CLOSED | General REPL unavailable, including terminal input. INTERACTIVE-*, REPL-PTY. |
| C7.07 | CLOSED | Admitted shell cannot source mutable files. SOURCE plus SHELL-STARTUP positive. |
| C7.08 | CLOSED | Immutable input snapshot prevents data-to-code read from mutable files. EXEC-OPEN, EVAL-OPEN, CUSTOM-LOADER. |
| C7.09 | CLOSED | Mutable import roots/archive/bytecode absent from input view. IMPORT, ZIPIMPORT, BYTECODE. |
| C7.10 | CLOSED | Installed general embedded interpreters excluded from ordinary launch; document writer consumes only literal bytes. INTERPRETER-awk/mawk/vi/vim, EDITOR-ESCAPE/GLOBAL/SOURCE/DEFINITION, EDITOR-CONTENT. |
| C7.11 | CLOSED | Child executable policy allows only the entry binary; helper shell unavailable. INTERPRETER-find, MAKE-RECIPE, NATIVE-KERNEL/HELPER. |
| C7.12 | CLOSED | Git hook interfaces removed; direct/interpreter hook routes refuse. GIT-HOOK, HOOK-DIRECT, HOOK-INTERPRETER. Git absence is a removal cost, not evidence of a functioning Git hook subsystem. |
| C7.13 | CLOSED | Loader is not an ordinary entrypoint; executable mappings remain declaration-derived. LOADER, NATIVE-KERNEL/FILE_EXEC_MAP. |
| C7.14 | CLOSED | Fixed environment and declaration-derived maps/immutable input closure. PRELOAD, NATIVE-KERNEL/DLOPEN. |
| C7.15 | CLOSED | memfd creation denied; descriptor/path execution cannot bypass membership. NATIVE-KERNEL/MEMFD/FEXECVE/EXECVEAT. |
| C7.16 | CLOSED | Native ELF admission and inherited syscall filter deny executable stacks, RWX segments, anonymous executable maps, protection changes and writable aliases. ADMISSION-EXECSTACK/WX-ELF, native WX/ANON_RX/MPROTECT_RX/WRITABLE_ALIAS. |
| C7.17 | CLOSED | Structured launcher does not interpret free command text. TYPED, FUNCTION, ALIAS, SUBSTITUTION. |
| C7.18 | CLOSED under stricter implementation reading | Unrecorded bytecode/cache cannot be read as code; generated executable memory unavailable. BYTECODE and native memory denials. This implementation choice does not settle the B1 textual ambiguity. |
| C7.19 | CLOSED by restricting capability | Recorded text browser displays pages without webpage JavaScript/JIT. BROWSER succeeds without the embedded execution marker. No executing renderer/JIT sandbox is claimed. |
| C7.20 | CLOSED | Serialized active content cannot reach sealed evaluator; ordinary writer treats document bytes literally. PICKLE, EDITOR-MODELINE-CONTENT. |
| C7.21 | CLOSED under stricter implementation reading, by removal | Partial-rights WASI runtime interface unavailable. WASI-PREOPEN refuses. No resolution of the textual boundary between interface-confined and own-rights code is inferred. |
| C7.22 | CLOSED | Syscall denial and inaccessible proc-memory route. Native PTRACE, PROCESS_VM and PROC_MEM denials. |
| C7.23 | CLOSED | Foreign ELF admission refuses; no ordinary foreign runtime/binfmt registration interface. ADMISSION-FOREIGN-ELF, BINFMT-REGISTER; exact launch inventory. |
| C7.24 | CLOSED within supplied interfaces | Sealed program has no mutable file, metadata, directory, argv, stdin or IPC instruction source. DISPATCH, METADATA-DISPATCH, DIRECTORY-DISPATCH, EXISTENCE-ORACLE, SEALED-ARGS/PIPE, native IPC denials. No universal semantic classification theorem is claimed. |
| C7.25 | CLOSED by refusal | bind/listen denied in ordinary workloads; sealed sockets additionally denied and inherited sockets not passed. Native LISTENER denial plus common syscall filter. No arbitrary listener service support is claimed. |
| C8.01 | CLOSED | Native login ignores startup scripts; interpreter settings fixed; login authority protected. SHELL-STARTUP, LOGIN-KEY-CP/WRITER/ED and LOGIN-KEY-UNCHANGED. |
| C8.02 | CLOSED | Fixed environment and sealed read closure. ENVIRONMENT, SHELL-STARTUP. |
| C8.03 | CLOSED | No imported function/environment command path. ENVIRONMENT, SHELL-STARTUP, SUBSTITUTION. |
| C8.04 | CLOSED | Programmable editor launch removed; plain document bytes not evaluated. INTERPRETER-vi/vim, EDITOR-MODELINE-CONTENT. |
| C8.05 | CLOSED by removal of general project interfaces | GIT-ALIAS, GIT-FILTER, MAKE-RECIPE explicitly refuse; sealed programs cannot acquire mutable project settings. |
| C8.06 | CLOSED | Free functions/aliases/editor commands refuse; writer has one fixed destination value and literal stdin. FUNCTION, ALIAS, EDITOR-GLOBAL/SOURCE/DEFINITION, WRITER-OPERAND/EXTRA-OPTION/NO-TARGET, EDITOR-CONTENT. |
| C8.07 | CLOSED by removal, conditional on full rebuilt suite | Partial rebuilt-2 evidence adds browser inventory (w3m present; chromium/chromium-browser/firefox absent) and BROWSER-EXTENSION-REQUEST: `chromium --load-extension=... about:blank` refuses at exact launch membership. BROWSER still displays content. This closes the previously missing extension-route evidence through removal of extension-capable interfaces, not through implementing a functioning privileged-extension admission system. |
| C8.08 | CLOSED for supported values-only selection | HOME-PREFERENCE-ONE/TWO select different displayed pages without code admission; modeline-looking document bytes remain literal. These prove a permitted page-selection value, not persistent preferences or arbitrary GUI theme support. |
| M4.01 | CLOSED conditional on managed-service integration | Repeated workload-domain revocation plus launch exclusion drains processes/descendants before mutation. REMOVE-HOLDER verifies both retained parent and child disappear; removal readback succeeds. Service lifecycle regression remains essential because service setup is a separate root-owned entry. |
| M4.02 | CLOSED | Removal withdraws launch membership, exact snapshot names and obsolete kernel profiles; copied code remains inert. REMOVE-PROFILES, REMOVED-SCRIPT/NATIVE/COPY, VERIFY. |

C8.07 evidence update: [rebuilt-2-live.jsonl](rebuilt-2-live.jsonl), browser inventory and BROWSER-EXTENSION-REQUEST at 2026-11-22T07:46:49Z, provide the concrete removal evidence missing in integration-05. BROWSER-OPTIONS remains a helper-configuration test, not an extension test. The full rebuilt suite was still ongoing when this update was written; no final aggregate pass or digest is asserted.


## Separate static review of policy verification and service lifecycle

Reviewed current `../../build/codeverify.py` and `stand.py` independently from their implementation work. No code changes or extra experiments were made.

- `verify_kernel_policy` compiles the generated policy afresh, requires every expected profile once and enforcing, groups kernel-exported load blobs by device/inode, rejects unexpected profiles sharing a selected transaction, and consumes the entire fresh compilation using each exported blob exactly once. A missing blob, altered bytes, suffix/prefix mismatch, ambiguous match or changed kernel revision fails verification. The caller separately checks the exact active `stand-run-*` name set. These controls are materially stronger than checking profile names alone. Static inspection found no acceptance bypass in the comparison logic. Parser execution has no explicit timeout; that is an operational liveness limitation, not evidence that changed policy could be accepted.
- The service observer reads MainPID status and requires all four UIDs/GIDs to be 1000, NoNewPrivs=1, zero inherited/effective/permitted/ambient capabilities, and the exact enforcing service profile. The generated drop-in text must also match. MainPID is the fixed output relay, so these observed values prove that process's privilege boundary. The workload child's chroot, Landlock and seccomp depend additionally on the recorded launcher implementation and service tests; do not describe the MainPID status read as directly measuring every descendant's confinement.
- Lifecycle handling now stops all old managed timers before services whenever code or job definitions change; this closes the earlier unchanged-timer reactivation window. Code changes drain workload profiles before file mutation. Policy/snapshot refresh is followed by another drain when the boundary changed, before requested units are restarted. The lock excludes ordinary launches through this interval; the service setup path separately requires root identity and its manager-owned cgroup/profile. This is a coherent correction to the earlier service-lock and revocation concerns.
- Service start/readback is still an observation at a particular time, not proof of eternal service availability. Final acceptance requires the ongoing live service lifecycle tests and whole-suite regression result. No new static blocking defect was found in these reviewed changes.
