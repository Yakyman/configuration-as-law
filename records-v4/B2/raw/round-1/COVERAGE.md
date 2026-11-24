# Round 1 coverage and supplemental observations

Recorded 2026-11-23 UTC. Exactly 65 owning-round-1 variants are listed.
The complete rebuilt-image, carried, supplemental and combined validation is
finished. [Independent final review](REVIEW-FINAL.md) closes only C5.4 and C10.4.
All other Round 1 variants remain NOT CLOSED; the complete 88-row table is in
[STAND.md](../../STAND.md). Overall hypothesis outcome: `?`.

## Source and execution distinctions

- **S**: `build/v4-shell-selftest.py`. Tests invoke actual ordinary Bash through
  `stand-shell -c`. `requirement=False` on saved-code probes means a failed
  boundary can coexist with a successful implemented-check exit; it does not
  turn the boundary failure into a pass. `UNSAVED-AFTER-REBOOT` requires the
  driver's separate post-reboot invocation.
- **T**: `build/v4-tools-selftest.py`. `ordinary-` IDs invoke quoted public tools
  as Bash commands; `root-` IDs invoke the public tool directly with actual root
  identity. Exact changed declaration rows, application report and per-line
  readback are checked. `root-native-account-bypass` instead invokes the native
  canonical administrative executable; its separate `boundary_result` records
  a built-in-tool failure without failing the implemented-check exit.
- **G**: `build/v4-gate-selftest.py`. An actual Bash heartbeat loop is paused
  during declaration realization. This concurrency regression test supports
  shell integration; it does not close untested object admission routes.
- **L/A/Y/W**: `build/language-selftest.py`, `build/app-selftest.py`,
  `build/system-selftest.py`, `build/round4-selftest.py`, respectively, when run
  via `build/v4-suite-adapter.py`. Broker requests become actual Bash commands.
  Existing `run` requests remain explicit `stand-session` commands *inside*
  Bash: their execution and refusal evidence belongs to the sealed launcher,
  not to unrestricted Bash interpreter inputs. Root subprocesses are unchanged.
  Parent suite success is not an assertion that all 65 v4 boundaries hold.

Test IDs identify assertions; a source citation alone does not imply success.
S/T/G observations are summarized in the completed-component ledger below;
L/A/Y/W completed with 301 passing assertions in [carried evidence](final-2/carried-suite); their interface distinctions above still apply. D/E entries
state actual final-2 supplemental observations. Where a test is only related, that limitation is explicit. No old
runtime-only refusal is reused as proof that v4 requires separate memory records.
Radio profile tests are saved/prepared settings only. This map does not assess
any variant owned by another round.

## Completed final-2 components

- (not published: direct evidence at least 2 MB): 85 `result` passes and one distinct
  `boundary_result:false`, `root-native-account-bypass`. Final declaration IDs
  are restored and all 553 final readback rows pass. The
  [tools review](REVIEW-FINAL2-TOOLS.md) accepts bounded C5.4/C10.4 evidence
  conditionally on the remaining full-suite/peer checks; [final review](REVIEW-FINAL.md)
  subsequently accepted both after those checks completed.
- [gate.jsonl](final-2/gate.jsonl): nine passes, including
  `APPLY-SHELL-GATE`, both `NESTED-BROKER-CALLER` lifecycle assertions,
  both `NESTED-EDITOR-CALLER` lifecycle assertions, and final restoration.
  The heartbeat stays fixed across 456 frozen samples; callers resume into
  their original cgroups and private freezer children/journal disappear.
  [Component review](REVIEW-FINAL2-COMPONENTS.md) records the finite acceptance
  and remaining general race/topology limits.
- [shell.jsonl](final-2/shell.jsonl) passes its implementation checks while
  retaining six saved-input failures: `SAVED-SCRIPT`, `SAVED-PIPE`,
  `SAVED-SOURCE`, `STARTUP-ENV`, `PYTHON-IMPORT`, `PICKLE-CODE`.
  [shell-reboot.jsonl](final-2/shell-reboot.jsonl) confirms the tested unsaved
  process is absent after reboot and the declaration report is unchanged.

## Supplemental evidence and detector history

- **D**: [final-2/supplement/direct.jsonl](final-2/supplement/direct.jsonl),
  17 actual ordinary-shell assertions: 12 passes and five genuine saved-code
  failures with unchanged declaration/report: `DIRECT-REDIRECT-STDIN`,
  `DIRECT-PROC-FD`, `DIRECT-READ-EXEC`, `DIRECT-AWK-FILE`,
  `DIRECT-SCRIPT-HELPER`.
- **E**: [final-2/supplement/extra.jsonl](final-2/supplement/extra.jsonl),
  with four genuine saved-code failures: `RC-STARTUP`,
  `EDITOR-SAVED-COMMANDS`, `JIT-SAVED-INPUT`, `DISPATCHER-SAVED`.
  `SAVED-FFI` is correctly recorded as `ATTEMPT_REFUSED`: mapping failed,
  stdout is empty, and no exact effect marker was observed. Runtime-only
  observations and the six unavailable/untested records remain separate.
- Final-2 executed source bytes are in
  [final-2-supplement-inputs/](final-2-supplement-inputs), with
  [frozen source hashes](final-2-supplement-source-sha256.json) matching the
  [controller input hashes](final-2/supplement/input-sha256.json).
- Both [before-reboot verification](final-2/supplement/before-reboot-verify.jsonl)
  and [after-reboot verification](final-2/supplement/after-reboot-verify.jsonl)
  contain the same 553 `OK` rows and are byte-identical. Successful report
  bytes are unchanged according to [reboot.json](final-2/supplement/reboot.json).
  The [controller summary](final-2/supplement/summary.json) records completed
  steps and destruction with no remaining owned VM. This proves finite
  readback/reboot continuity, not that saved-code failures disappeared.
- [Supplement review](REVIEW-FINAL2-SUPPLEMENT.md) confirms these final-2
  observations and their bounded interpretation.

The [offline marker audit](supplement-marker-audit.json) is retained **for
final-1**. Its original substring detector falsely labelled `SAVED-FFI` because
Python echoed the print expression in a traceback; all four other failure
labels were exact execution effects. That audit repeated no guest command.
The corrected detector was subsequently frozen and executed during the
mandatory whole rebuilt-image final-2 validation after the general freezer
mechanism changed. Final-2 was not a repeat performed solely to repair the
detector. Historical payloads remain in `supplement-inputs/`; they must not be
confused with the final-2 frozen payload directory above.

All these observations retain their route-specific limits. Only C5.4 and C10.4
are CLOSED after full-suite consistency checks and final independent review.

## Per-variant mapping

| Variant | Exact test IDs / relevant evidence | Current limit or review condition |
|---|---|---|
| C1.1 — Repository install, upgrade, downgrade, reinstall and remove through CLI | T: ordinary-apt-install, ordinary-apt-reinstall, ordinary-apt-downgrade, ordinary-apt-remove; root-apt-install, root-apt-reinstall, root-apt-downgrade, root-apt-remove; same apt-get IDs. Y: SYSTEM-REPOSITORY-INSTALL, SYSTEM-BASE-UPDATE, SYSTEM-NEW-VERIFY, SYSTEM-UPDATE-REMOVE. | Exact artifact/catalog selection is positive; native low-level privileged mutation is not mediated. Aliases alone do not prove all repository operations. |
| C1.2 — Direct low-level manager or library/API/GUI frontend bypassing CLI wrapper | Y: SYSTEM-BYPASS-0, SYSTEM-SUDO-BYPASS-0. T: root-native-account-bypass (related architectural witness, not a package test). | Wrapper refusal does not exercise direct package libraries/GUI/helper methods as actual root. Native package backend channel remains untested here. |
| C1.4 — Maintainer scripts, triggers, hooks and post-install service activation | Y: SYSTEM-BYPASS-2, SYSTEM-SUDO-BYPASS-2, SYSTEM-BASE-UPDATE. | Rejects an explicit pre-invoke option; captured update is a positive exact transaction. Arbitrary maintainer-script/trigger post-install activation through other native interfaces is not exercised. |
| C1.5 — Hook disable/config override, backend flag or environment bypass | Y: SYSTEM-BYPASS-2, SYSTEM-SUDO-BYPASS-2, SYSTEM-CATALOG-TAMPER. | Finite wrapper validation is covered; backend flags and environment on native privileged entry are not a complete negative test. |
| C2.1 — pip system, --user, virtualenv, --target/--prefix installs | L: LANG-pip-INSTALL, LANG-pip-ROOT-INSTALL, LANG-pip-BYPASS-0, LANG-pip-BYPASS-1, LANG-pip-BYPASS-2, LANG-pip-VIRTUALENV. | Positive pinned broker install; virtualenv refusal is a sealed-launch check. Real Bash interpreter/venv routes are not exhaustively checked. |
| C2.2 — npm local, global, prefix/workspace installs and executable links | L: LANG-npm-INSTALL, LANG-npm-ROOT-INSTALL, LANG-npm-BYPASS-0, LANG-npm-BYPASS-1, LANG-npm-BYPASS-2, LANG-npm-BYPASS-3. | Pinned broker positives and flag refusals do not cover all free-shell package/module/link paths. |
| C2.3 — Local archives, VCS URLs and package indexes selected by flags | L: LANG-pip-BAD-HASH, LANG-npm-BAD-HASH, LANG-pip-MISSING-DEPENDENCY, LANG-npm-MISSING-DEPENDENCY; LANG-pip-BYPASS-4, LANG-pip-BYPASS-5; LANG-npm-BYPASS-8, LANG-npm-BYPASS-9, LANG-npm-BYPASS-10. | Pinned archive/hash checks are meaningful, but refusing frontend URLs does not close alternate importer or native API paths. |
| C2.4 — Editable pip installs, npm links, mutable source and dependency replacement | L: LANG-pip-BYPASS-3, LANG-npm-BYPASS-3, LANG-pip-IMMUTABLE-WRITE, LANG-npm-IMMUTABLE-WRITE, LANG-pip-COPIED-LAUNCH, LANG-npm-COPIED-LAUNCH. S: SAVED-SCRIPT, PYTHON-IMPORT. | Copied-launch refusal remains sealed; Bash exposes saved-source execution/import paths that that refusal cannot close. |
| C2.5 — Build backend, lifecycle script, npm run/start/test and dependency hook execution | L: LANG-pip-SOURCE-BACKEND, LANG-pip-SOURCE-NOT-EXECUTED, LANG-npm-HOOK-ARTIFACT, LANG-npm-HOOK-NOT-EXECUTED; LANG-npm-BYPASS-4, LANG-npm-BYPASS-5, LANG-npm-BYPASS-6. | Finite importer avoids running hooks; free-shell evaluation of saved build/lifecycle code remains outside the demonstrated boundary. |
| C2.6 — Native extensions and admitted module/.pth inputs; custom evaluator behavior in C7.08 | L: LANG-NATIVE-WHEEL-INSTALL, LANG-NATIVE-WHEEL-IMPORT, LANG-pip-HOOK-ARTIFACT, LANG-pip-MUTABLE-NATIVE-REFUSED. S: PYTHON-IMPORT. | Native-wheel/import checks use the sealed runner; ordinary Bash Python import explicitly tests the unresolved saved-module boundary. |
| C3.1 — Flatpak system install/update and graphical or D-Bus frontend | A: flatpak-INSTALL-ordinary, flatpak-INSTALL-root, flatpak-VERIFY-root, flatpak-SYSTEM-ordinary, flatpak-UPDATE-root, FLATPAK-ABSOLUTE-ROOT, FLATPAK-DBUS-HELPER. | Positive exact import and selected refusal paths; GUI and all helper/API mutation behavior are not demonstrated as closed. |
| C3.2 — Flatpak --user install, extra installation roots/remotes, local bundles | A: flatpak-USER-ordinary, flatpak-ROOT-ordinary, flatpak-REMOTE-ordinary, flatpak-BUNDLE-ordinary (and root counterparts). | Refusal of finite frontend options is real Bash broker evidence, but does not census objects left by every alternate installation method. |
| C3.3 — Flatpak runtime/extension updates, override permissions, alternate commands and development mode | A: flatpak-RUNTIME-ordinary, flatpak-OVERRIDE-ordinary, flatpak-ALT-COMMAND-ordinary, flatpak-DEVEL-ordinary (and root counterparts); flatpak-TOOL-RUN-root. | Declared app sandbox is tested; alternate saved inputs through ordinary-shell paths are not completely checked. |
| C3.4 — AppImage directly executed and self-mounted via FUSE | A: appimage-INSTALL-ordinary, appimage-INSTALL-root, APPIMAGE-DOWNLOADED, APPIMAGE-FUSE, appimage-POSITIVE. | Downloaded/FUSE execution refusals still use the sealed runner; a direct Bash launch/mount of the actual fixture is not the same observation. |
| C3.5 — AppImage extracted/mounted externally, AppDir launch or self-update | A: APPIMAGE-EXTRACTED, APPIMAGE-SELF-UPDATE, appimage-SELF-UPDATE-ordinary, appimage-SELF-UPDATE-root. | Extracted entry and self-update argument tests are sealed or finite wrappers; arbitrary extracted scripts under Bash remain uncovered. |
| C4.1 — Download a native executable and chmod/run it | S: NATIVE-COPY. W: DOWNLOAD, DOWNLOAD-INERT, DOWNLOAD-IMPORT, DOWNLOAD-RUN. D: DIRECT-HTTP-SAVE, DIRECT-HTTP-NATIVE. | Observed HTTP download completed, then actual Bash native launch was permission-denied with declaration/report unchanged. This is one concrete native download route; interpreter alternatives remain open.
| C4.2 — Download and extract archive, including nested archives and renamed files | S: NATIVE-COPY. A: APPIMAGE-EXTRACTED. D: DIRECT-NESTED-EXTRACT, DIRECT-NESTED-ARCHIVE. | Observed nested archive extraction completed; actual Bash execution of renamed payload was permission-denied, with declaration/report unchanged. One nested-native fixture does not cover arbitrary script/library archive outputs.
| C4.3 — Download by browser, curl, copier, sync client or application self-updater | S: BROWSER. W: DOWNLOAD, DOWNLOAD-INERT. D: DIRECT-HTTP-SAVE, DIRECT-HTTP-NATIVE. | Observed HTTP download and denied direct native launch. Ordinary browser material work remains separate; browser/sync/self-updater script and package output families are not all covered.
| C4.4 — Downloaded script or library passed to existing interpreter/loader | S: NATIVE-LOADER, SAVED-SCRIPT. | Native mapping refusal is separate from the tested unresolved saved-script interpreter route. |
| C4.5 — Stream download directly into interpreter or process substitution | S: UNSAVED-EXECUTE, UNSAVED-AFTER-REBOOT. | Genuine pipe execution/reboot witness is scoped to one runtime-only payload; process substitution and payloads attempting saved code/settings are not fully covered. |
| C5.1 — Compile/link native program in home, then execute output | W: SOURCE-RECORD, SOURCE-BUILD, BUILD-INERT, BUILD-IMPORT, BUILD-RUN. D: DIRECT-COMPILE, DIRECT-COMPILED-RUN. | Observed ordinary compiler output creation and denied actual Bash execution, with declaration/report unchanged. This finite native output test does not close interpreter-generated code routes.
| C5.2 — Build-system commands, configure probes, generators and test binaries | W: SOURCE-BUILD, UNRECORDED-BUILD. D: DIRECT-COMPILE, DIRECT-COMPILED-RUN. | Observed direct compiler output denied at execution. Configure probes, generators and the broader build-system family are not all exercised; make is absent according to E MAKE-SAVED-RECIPE.
| C5.3 — Install target copying to user prefix, changing PATH or creating symlinks | S: NATIVE-COPY. W: MUTABLE-OUTPUT-OVERWRITE. D: DIRECT-PREFIX-SETUP, DIRECT-PREFIX-PATH. | Observed user-prefix installation and symlink setup, then denied PATH-selected symlink execution, with declaration/report unchanged. Interpreter reading of copied scripts remains a separate open route.
| C5.4 — Rebuild/replace an already recorded binary or library in place | T: recorded-native-overwrite. S: RECORDED-REPLACE, PERSONAL-COVERAGE. W: MUTABLE-OUTPUT-OVERWRITE. L: LANG-pip-IMMUTABLE-WRITE, LANG-npm-IMMUTABLE-WRITE. | CLOSED: final-2 T recorded-native-overwrite passed. Ordinary replacement was denied and exact SHA-256, mode 0755, UID/GID 0, complete covering row and successful report remained unchanged. Final review accepts this bounded recorded-native-file mechanism after full-suite/peer consistency; it does not close other saved-input or process-race variants. |
| C5.5 — Compilers embedding plugins or build processes loading generated code | W: SOURCE-BUILD. L: LANG-pip-SOURCE-BACKEND, LANG-pip-SOURCE-NOT-EXECUTED. D: DIRECT-PLUGIN-BUILD, DIRECT-COMPILER-PLUGIN. | Observed plugin compilation and compiler refusal with failed-to-map-segment diagnostic. Finite native plugin mapping is tested; generated saved instructions evaluated as text remain outside that result.
| C6.1 — Persistent user units and drop-ins, aliases, template instances and symlinks | S: USER-SERVICE, USER-SERVICE-STATE. T: ordinary-service, root-service, ordinary-socket-add, root-socket-add. | Exact declared jobs work and one user enable request fails; all drop-in/template/alias/link paths and native privileged manager mutations remain unchecked. |
| C6.2 — Direct manager API/CLI start, enable, reload, set-property or link | S: USER-SERVICE, USER-SERVICE-STATE. T: ordinary-service, root-service. | Public typed manager works; canonical native root manager and direct bus method effects are not blocked by the adapter or exhaustively tested. |
| C6.3 — Transient service/scope/timer/path/socket created through systemd-run or D-Bus | S: TRANSIENT-JOB. T: ordinary-systemd-run-add, root-systemd-run-add, ordinary-systemd-run-remove, root-systemd-run-remove. | Supported declared timer positive; refusal of one transient command is not all scope/path/socket/direct bus registrations. |
| C6.4 — User cron entries, @reboot and crontab replacement | S: CRON-JOB. T: ordinary-crontab-add, root-crontab-add, ordinary-at-add, root-at-add. W: SCHEDULE-COMMAND, SCHEDULE-EXECUTED. | Declared timer/schedule execution works; broader crontab replacement and privileged native scheduler interfaces are not fully established. |
| C7.01 — Script file passed as interpreter argument | S: PERSONAL-INSTALL, PERSONAL-RUN, PERSONAL-COVERAGE, SAVED-SCRIPT. | Exact personal script works, while saved unrecorded interpreter-file execution is the explicit unresolved boundary. |
| C7.02 — Executable shebang script | S: PERSONAL-RUN, PERSONAL-COVERAGE. D: DIRECT-SHEBANG. | Observed actual Bash launch of the saved unrecorded shebang file was permission-denied, with declaration/report unchanged. Explicit interpreter input remains a demonstrated bypass in other rows; no broad shebang-family closure claimed.
| C7.03 — Code supplied as -c or -e argument | S: FREE-COMMANDS, PYTHON-IMPORT. | Typed code is allowed as required; resulting saved instruction inputs/settings still need their boundary, which the import case exposes. |
| C7.04 — Code piped into stdin, FIFO, socket, here-document or process substitution | S: SAVED-PIPE, UNSAVED-EXECUTE, UNSAVED-AFTER-REBOOT. | Unsaved pipe execution is distinguished from saved-file pipe execution; the latter remains an unresolved path. FIFO/socket/here-document cases are not each exercised. |
| C7.05 — Code from regular file redirected to stdin or /proc/self/fd/N | S: SAVED-PIPE, SAVED-SCRIPT. D: DIRECT-REDIRECT-STDIN, DIRECT-PROC-FD. | Both actual Bash routes executed SAVED_DIRECT_RAN from saved unrecorded code, with declaration/report unchanged. Concrete boundary failure; inherited descriptor variants are not thereby universally tested.
| C7.06 — Interactive REPL with language statements | E: REPL-TYPED. | Observed interactive Python stdin printed REPL_TYPED_EXECUTED with unchanged declaration/report. This is allowed typed runtime work, not proof that all saved inputs or persistent REPL effects are covered.
| C7.07 — Recorded script sources another file | S: SAVED-SOURCE. | Direct Bash source exposes saved-file evaluation; source from inside a recorded personal script is not separately exercised. |
| C7.08 — exec(open(file).read()), eval of read data, custom import loader | S: SAVED-SCRIPT, PYTHON-IMPORT. D: DIRECT-READ-EXEC. | Observed exec of read saved text printed READ_EXEC_RAN with unchanged declaration/report. Concrete boundary failure; every custom loader/evaluator is not individually tested.
| C7.09 — Ordinary import, zipimport and non-regenerable bytecode; module path injection | S: PYTHON-IMPORT. L: LANG-NATIVE-WHEEL-IMPORT. | Ordinary import route tests unresolved saved module access; zipimport, bytecode and path-injection variants lack individual Bash tests. |
| C7.10 — Embedded interpreter in editor, awk, make, debugger or database program | S: DOCUMENT-EDIT. W: DOCUMENT-EDIT, EDITOR-SHELL-REFUSED, EDITOR-COMMAND-READ-REFUSED. D: DIRECT-AWK-FILE. E: EDITOR-SAVED-COMMANDS. | Observed saved awk instructions and saved ed command input executed their exact effect markers, with unchanged declaration/report. Two concrete embedded-interpreter boundary failures; debugger/database families remain untested.
| C7.11 — Helper process launch: find -exec, editor shell escape, make recipe child | S: NATIVE-HELPER. W: EDITOR-SHELL-REFUSED. D: DIRECT-SCRIPT-HELPER. | Observed a helper launched an interpreter consuming saved script bytes and printed SAVED_DIRECT_RAN, with unchanged declaration/report. Native helper denial does not close this saved-script helper route.
| C7.12 — Git hook program in writable project | E: GIT-HOOK (availability). | Git is absent from the supplied image; actual hook execution is UNTESTED. No package was installed and absence is not closure.
| C7.13 — Direct dynamic loader invocation | S: NATIVE-LOADER. | Direct loader mapping of one unrecorded native file is tested; full loader/library input paths are not established by a single fixture. |
| C7.14 — LD_PRELOAD, LD_AUDIT, dlopen/FFI and alternate library path | L: LANG-pip-MUTABLE-NATIVE-REFUSED. E: LIBRARY-FIXTURE-COMPILE, SAVED-LD-PRELOAD, SAVED-LD-AUDIT, SAVED-FFI; final-1 offline supplement-marker-audit.json retained separately. | Real test library compiled. Preload and audit mapping were denied (loader continued after ignoring them); FFI mapping was also denied. The rebuilt-image exact-line detector reports FFI denial correctly. The earlier final-1 false label and its offline correction remain preserved. Three finite mapping routes do not cover all alternate-library paths.
| C7.15 — Native executable memfd, fexecve/execveat of memory file | E: MEMFD-RUNTIME, MEMFD-SAVED-INPUT. | Both executions were denied with EACCES, with declaration/report unchanged. Saved-input laundering did not execute in this fixture. Runtime-only refusal is an implementation restriction, not a successful v4 memory-record requirement; fexecve/execveat alternatives are not all tested.
| C7.16 — Anonymous machine code, JIT, writable/executable aliases | E: JIT-RUNTIME, JIT-SAVED-INPUT. | Typed anonymous code executed and returned 42 without a new line, as runtime work. Saved uncovered machine bytes also executed and returned 42 with unchanged declaration/report: concrete saved-input boundary failure. Writable/executable alias families are not universally covered.
| C7.17 — Shell command line, including invocation of a declared program | S: SHELL-PROFILE, FREE-COMMANDS, MATERIAL-NO-LINE, PERSONAL-RUN. G: APPLY-SHELL-GATE. | Final-2 ordinary Bash and all nine cgroup-gate assertions pass, including retained broker/editor callers. Commands still execute uncovered saved code, so the overall resulting-state boundary remains open. |
| C7.20 — Code-bearing serialized input (pickle, macro-bearing document) | S: PICKLE-CODE. | Saved serialized code execution has an explicit unresolved-boundary test; macro-bearing documents are not separately exercised. |
| C7.22 — Debugger/interpreter writing another process memory or injecting code | E: PROCESS-MEMORY-RUNTIME. | Same-user parent-to-child process_vm_writev returned -1/EPERM; child retained its original executable result 7, with declaration/report unchanged. Runtime-only restriction is not a mandatory-record success; saved-payload injection and debugger variants remain untested.
| C7.23 — binfmt_misc handlers and user-mode foreign-binary interpreters | E: BINFMT-REGISTER, BINFMT-EFFECT, FOREIGN-INTERPRETER (availability). | Actual ordinary registration write was denied; exact test handler entry remained absent. Foreign-runtime execution is UNTESTED because no prepared payload or demonstrated invocation was supplied; the recorded `/usr/bin/qemu-*-static` scan returned an empty list. No general foreign-interpreter closure.
| C7.24 — Recorded custom dispatcher: file-open route and non-file instruction input without eval/import | S: SAVED-PIPE. E: DISPATCHER-INSTALL, DISPATCHER-TYPED, DISPATCHER-SAVED, DISPATCHER-REMOVE. | Exact recorded manual dispatcher installed and removed successfully. Typed instruction executed as ordinary action; saved uncovered instruction also executed DISPATCHER_SAVED_EXECUTED with unchanged declaration/report, without eval/import. Concrete boundary failure.
| C8.01 — Shell startup profiles and rc files | S: SAVED-SOURCE. E: RC-STARTUP. | Actual Bash --rcfile startup executed SAVED_RC_EXECUTED from saved uncovered text, with unchanged declaration/report. Concrete boundary failure; every login/profile entry is not individually exercised.
| C8.02 — Environment-selected startup code, BASH_ENV/ENV/PYTHONSTARTUP | S: STARTUP-ENV. | Actual BASH_ENV saved startup execution is tested as unresolved; ENV and PYTHONSTARTUP paths lack dedicated tests. |
| C8.03 — Environment-imported shell functions and command substitutions | S: FREE-COMMANDS. E: EXPORTED-FUNCTION-SUBSTITUTION. | Observed typed function exported through environment and consumed in command substitution, printing FUNCTION_FROM_ENV with unchanged declaration/report. This is allowed typed work; stored startup/function-source routes remain governed by their separate unresolved boundary.
| C8.04 — Editor executable configuration, plugins, modelines executing code | S: DOCUMENT-EDIT. W: EDITOR-SHELL-REFUSED. E: EDITOR-SAVED-COMMANDS, EDITOR-PLUGIN-MODELINE (availability). | Saved ed commands executed an exact marker with unchanged declaration/report. This is a saved-command input witness, not proof of a plugin/modeline test. No supported plugin/modeline facility was supplied for ed; that part remains UNTESTED.
| C8.05 — Project-local executable settings: Git !alias, external filter, build recipe | E: GIT-LOCAL-ALIAS-FILTER, MAKE-SAVED-RECIPE (availability). | Git and make are absent from the supplied image. Their executable alias/filter/recipe integration is UNTESTED; absence does not close the family.
| C8.06 — Runtime own-rights code definitions: shell functions, aliases, editor commands | S: FREE-COMMANDS, DOCUMENT-EDIT. D: DIRECT-RUNTIME-ALIAS. | Observed typed runtime shell alias printed RUNTIME_ALIAS_OK with unchanged declaration/report. Alongside functions/editor work, this establishes a finite allowed ordinary action; lasting saved settings are not thereby covered.
| C8.07 — Browser extension executing with browser-equivalent rights | S: BROWSER. E: BROWSER-EXTENSION (availability). | w3m is present, but no browser-equivalent extension facility or fixture was demonstrated. Documented local CGI is not substituted for an extension; this family remains UNTESTED.
| C9.1 — Rootful image pull/run, mutable tags and manager API | A: oci-INSTALL-ordinary, oci-INSTALL-root, oci-PULL-TAG-ordinary, oci-RUN-TAG-root, oci-API-root. | Exact imported image positive and public-manager refusals are tested; general rootful manager APIs/native runtime paths are not fully demonstrated. |
| C9.2 — Rootless containers, user namespaces, alternative OCI runtime invocation | S: USER-NAMESPACE, OCI-ALTERNATE. A: oci-ROOTLESS-ordinary, OCI-ALTERNATIVE-runc, OCI-ALTERNATIVE-crun, OCI-ALTERNATIVE-bwrap. | Actual Bash namespace request plus wrapper checks; alternative runtime attempts remain sealed/unavailable distinctions, not all direct Bash runtime behavior. |
| C9.3 — Bind-mounted executable/script, writable overlay, exec into container and package install inside | S: OCI-WRITABLE-OVERLAY. A: oci-BIND-ordinary, oci-OVERLAY-root, oci-EXEC-root, oci-PACKAGE-INSTALL-root, OCI-ROOT-CONTENT, OCI-HOLDER-START. | Sealed immutable container demonstrates bounded behavior; mutable input/script/native alternatives are not completely exercised from the free shell. |
| C9.4 — Image build RUN/hooks, import/load archive and commit modified container | S: OCI-WRITABLE-OVERLAY. A: oci-BUILD-RUN-ordinary, oci-LOAD-root, oci-IMPORT-root, oci-COMMIT-root. | Finite manager rejections do not establish every build/hook/import path and saved instruction boundary. |
| C9.5 — Privileged/host-namespace/device/runtime-hook options | S: USER-NAMESPACE, OCI-ALTERNATE. A: oci-PRIVILEGED-root, oci-HOST-NS-root, oci-DEVICE-root, oci-HOOK-root. | Selected privilege/namespace flags are rejected; native alternative runtime/root API coverage is incomplete. |
| C10.1 — Documented privileged package/service/account/network/firewall administration | T: ordinary-useradd, root-useradd, ordinary-usermod, root-usermod, root-nft-add, root-nmcli-add, root-bluetoothctl-add, root-native-account-bypass. S: RAW-SETTINGS. | Final-2 typed-tool positives pass. Native root useradd actually created an uncovered account with unchanged declaration/report; this is the separate failed boundary result, explicitly not breaking. Cleanup passed but does not cure the bypass. |
| C10.2 — Built-in privileged tool changes guards, permissions, mounts or execution policy | S: RAW-SETTINGS. T: ordinary-groupadd, root-groupadd, root-native-account-bypass. | Account/group positive adapters and ordinary DAC denial do not cover documented native root guard/permission/mount/policy mutations. Related account witness is not an exact guard mutation test. |
| C10.4 — Root editor with documented package installer | T: ordinary-editor-write, ordinary-editor-append, ordinary-editor-read, ordinary-editor-install, ordinary-editor-remove, ordinary-editor-hash-refusal; root counterparts; root-editor-breaking. | CLOSED: final-2 ordinary and actual-root document edit, exact package install/run/remove and bad-hash refusal all passed; the nested editor caller also resumed with its original cgroup restored. Root general editing remains separately breaking. Final review accepts this bounded supplied-editor mechanism after full-suite/peer consistency; arbitrary foreign embedded installers remain outside this claim. |
