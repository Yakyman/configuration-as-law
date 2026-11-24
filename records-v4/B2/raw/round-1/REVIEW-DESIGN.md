# Round 1 design review

Recorded 2026-11-23T08:25:30Z. Scope: source review only; no probe was run.

## Finding

The proposed round is feasible only as a bounded partial implementation. A real shell can retain the existing executable/mapping and persistent-setting barriers, and the declaration brokers can provide positive built-in-tool mutations. The present mechanisms cannot, however, distinguish typed code from saved code after an ordinary process has copied saved bytes into an argument, pipe, FIFO, or custom evaluator. Any design that installs a stock shell over the present policy and claims the full interpreter/custom-dispatcher rows is unsound.

This distinction follows directly from S8.2-4, S8.2-9--10, S8.2-23 and Section 9.3. The command text is an action, while a saved file executed as code is a program. The boundary must therefore follow the origin and later semantic use of bytes; path-only execution checks are insufficient.

## Reusable mechanisms

1. Keep a persistent `stand-shell` AppArmor domain for the login shell and its ordinary descendants. Generate exact `ix`/`m` authority from the recorded immutable closure, preserve `no_new_privs`, identity/capability dropping and the application lock, and allow document trees to be written. The loaded-policy comparison in `build/codeverify.py` and the immutable code root in `build/codeboundary.py` are useful evidence mechanisms. `fapolicyd` can remain defence in depth, but `build/policy.py` explicitly records `reload_acknowledged:false` and says that database equality is not an atomic execution barrier; it cannot be the sole admission proof.

2. Retain the sealed runner for declared scripts, services, applications and containers. Its hash checks, immutable input root, Landlock read closure, seccomp restrictions and generated service profiles already provide a stronger domain than free shell work needs. A recorded personal script should be entered from the shell through this common declared launch path, with its exact bytes and interpreter in the declaration.

3. Keep persistent settings behind protected stores and manager APIs. The backend DAC, system-bus policy, scheduler masking and finite declaration validation in `build/install-guard.py`, `build/guard.py` and `build/stand.py` are suitable foundations. A shell startup must use a protected fixed configuration and a scrubbed environment; writable startup files must not become effective. Ordinary runtime aliases, functions and command text may exist in the running shell, but persistence, autostart, service enablement and access grants must cross the declaration transaction.

4. Make the unsaved download-and-execute case a positive ephemeral path. Execute it in a separate domain with network input and transient executable memory, no persistent writable mount, no manager/control APIs and no authority to create effective jobs or settings. Its scratch state must be tmpfs-only. A pre-execution refusal cannot close the Section 9.3 case. The same treatment is appropriate for supplied memfd/JIT/runtime-injection cases when their bytes are runtime-only under S8.2-5; saved inputs and settings remain subject to their own boundaries.

## Fundamental saved-code gap

AppArmor execute/map rules, `noexec`, file MIME checks and immutable recorded roots can block direct execution, mapping, shebang launch and many ordinary loader paths. They do not close examples such as `cat saved | sh`, `python -c "$(cat saved)"`, an inherited descriptor, or a recorded custom evaluator that reads a nominal data file and executes its bytes. Once bytes have been laundered through an allowed process or pipe, the stock kernel interfaces used here carry no origin label to the semantic code sink.

An honest full solution needs one of these general mechanisms:

- a provenance-aware shell/execution broker that tracks literal typed text, expansions, substitutions, files and descriptors, and admits code sinks only from allowed origins; or
- mandatory information-flow labels propagated through files, pipes, descriptors and process memory, enforced at every declared evaluator/code sink.

A practical bounded design may instead register every code-consuming executable and place it in a profile that cannot read mutable storage or receive data from document-capable processes. The shell must broker code-bearing pipelines and argument expansion, because inherited pipes otherwise defeat the split. Disabling `source`/`eval` alone is insufficient. Until such mediation exists, keep at least the saved-script/interpreter, redirected-input, source/import/custom-loader, serialized-code and embedded-evaluator rows open. This is a testbed defect (`?`), not a definition-only failure.

## Positive built-in tools

The current public names already enter `build/stand.py`, and successful supported operations call `candidate_edit()` and `apply()` before returning. That is the correct transaction shape: mutate the designated primary declaration, apply it, identify the successful generation, read back the required state, and use the same path for removal.

The current root boundary is incomplete. Mode `0700` on native package, service, account, network and firewall backends blocks the ordinary identity but does not stop direct root execution. Such an invocation is still inside a built-in tool under S8.1-7 and S8.3-7; it cannot be relabelled as breaking. Relocate native backends to private paths, replace every documented public entry/API with a declaration frontend, and attach a mandatory deny profile to direct backend execution. The broker alone should receive an explicit AppArmor transition to narrowly profiled backend children. Direct root file editing or disabling this enforcement remains separately recorded breaking under S8.1-15--16.

For C10.4, use a real general-purpose editor with a documented integrated package manager. An editor package subsystem such as `package.el` is a concrete fit. Its install/update/remove entry points should call the same declaration broker; the raw editor binary and any bypass mode must be confined so that its package subsystem cannot publish directly. Evidence must exercise the editor's documented installer function as both the ordinary identity and actual root, while ordinary editing remains available. A separate wrapper that merely refuses the editor installer is not positive evidence.

## Evidence needed for closure

Design inspection closes no variant. Before each run, freeze exact commands, artifacts, expected declaration diffs and concrete object/effect readbacks. Evidence can honestly close bounded direct-exec/map rows, protected startup/setting/job rows and brokered installer/tool rows only when every specified direct, helper, inherited and API route has the same observed result. For each positive built-in tool, save the primary-declaration diff, successful generation identity, exact required-state readback, and the corresponding removal result under ordinary and root execution.

For the free shell, record quoting, arguments, a pipeline, redirection, document/browser work and a declared personal script. For unrecorded saved native code, services/autostarts and settings, observe the actual absence of executable/effective state rather than an exit status. For the ephemeral case, prove execution occurred, prove no payload was saved, reboot, and inventory processes, executable objects, jobs and settings for residue. Rows involving saved-byte laundering must remain NOT CLOSED until provenance reaches the semantic code sink; success on a finite list of filename extensions cannot close them.
