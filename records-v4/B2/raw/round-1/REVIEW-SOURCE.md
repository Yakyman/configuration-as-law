# Round 1 independent source review

Recorded 2026-11-23T08:50:48Z. This review covers the frozen sources identified by `final-source-sha256.json`. The reviewed key-file hashes match that record. Runtime evidence is not accepted in this note.

## Disposition

The implementation is source-ready for a final bounded run. No remaining source-level blocker was found for the two proposed closure candidates, C5.4 and C10.4. All other Round 1 variants must remain open unless the later evidence review identifies a separately complete exact-variant case. The overall testbed remains partial and the hypothesis outcome remains `?`.

The real shell does not solve saved-byte provenance. The six deliberate saved-input probes are correctly marked as property requirements while excluded from implemented-check success. A successful suite exit must not convert those failed requirements into passes. Direct privileged native built-in tools also remain an explicit P4 failure; their effects cannot be classified as breaking merely because the caller is root.

## Shell and application boundary

`build/shell.c` enters ordinary Bash with a fixed environment and startup suppression after checking boot readiness, the nonblocking application lock and pending recovery. `build/shell_boundary.py` gives shell descendants exact recorded native execute/map authority under one inherited AppArmor profile while retaining material writes and the whitelisted declaration broker.

The application race found during review was corrected. `shell_boundary.pause()` records stable process identities before stopping every running `stand-shell` task, repeats until the profile has no running task, and preserves tasks that were stopped before the transaction. The broker has already transitioned out of that profile. Candidate realization, policy replacement, readback and the durable report therefore occur while existing shell tasks cannot execute. New shell entry is denied by the exclusive lock and by `pending.json` after supervisor loss.

Finalization now writes readiness and resumes recorded shell identities before removing pending state. Recovery and the watchdog handle both pending transactions and a paused-shell journal left without pending state. PID start-time validation prevents resuming a reused PID. This is sufficient for the Round 1 before-report execution boundary. It does not establish removal of code-derived state already held inside a process; the affected live-removal variants remain owned by Round 3.

The final gate evidence must show all of the following in one run: a nonempty paused identity set, every recorded identity stopped, an unchanged heartbeat throughout more than a momentary sample, refusal of a new shell entry while pending, a durable success report matching stdout, resumed heartbeat only after the report, absence of the pause journal, and concrete fixture removal.

## C5.4 candidate

The decisive assertion is T `recorded-native-overwrite`, not the related personal-script refusal. It installs the recorded native worker, attempts replacement from actual ordinary Bash, and requires a nonzero copy result together with exact SHA-256, mode, uid, gid, covering declaration row and successful-declaration identity unchanged. If the final log contains all those values and the later complete readback/restoration succeeds, C5.4 is supported for this bounded variant.

## C10.4 candidate

`build/v4-editor.py` is a supplied general-purpose document editor under the literal definition: its recorded documentation and interface provide document read, replacement and append operations, plus documented package install and remove operations. The installer part delegates to the common declaration transaction rather than merely refusing installation. Document operations preserve the caller identity.

The final evidence must show actual document byte changes and exact reads, then positive installer add/run/remove under ordinary Bash and direct root execution. Each installation must include the exact declaration diff, durable successful-generation identity and required-state readback; removal must show both line and object absence. The changed-hash fixture must fail without changing declaration or state. Direct root document editing is outside the installer part and is correctly recorded separately as breaking. Any direct root native administrative tool bypass remains a built-in-tool failure, not breaking.

This supports only the supplied editor's documented installer functionality. It does not establish a universal boundary for other editors or general-purpose programs.

## Final evidence limits

`build/v4-suite-adapter.py` preserves old suite sources and expectations while replacing compatible ordinary broker requests with public frontend commands parsed by real Bash. It leaves sealed launch requests explicit inside Bash and logs the actual command, so sealed-launch results cannot be presented as free-shell saved-input evidence.

The final report must retain the coverage draft's distinctions: positive finite frontends do not close native privileged backends, selected namespace/container refusals do not close every runtime path, and path-based native admission does not close saved scripts, imports, serialized code or custom evaluators. Failed requirement rows and unavailable paths remain visible. No testbed defect reviewed here supplies a definition-only argument for outcome `0`.
