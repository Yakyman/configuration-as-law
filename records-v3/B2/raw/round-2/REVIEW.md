# Round 2 independent design review

Status: design review; implementation and fresh-image results not yet supplied. Review used a separate task context. Independent acceptance by a separately configured implementation is not established. No VM probes were run by review.

## Sources and mechanisms

- [Kernel Landlock documentation](https://docs.kernel.org/userspace-api/landlock.html): “A set of rules is aggregated in a ruleset, which can then restrict the thread enforcing it, and its future children.” Use per-file declaration-derived read/execute closure for interpreter children. Fail closed if the guest ABI lacks a required right; do not copy the example's compatibility downgrade into an enforcement guarantee. Landlock applies to file opens, so inherited descriptors and non-file inputs require separate controls.
- [Kernel no_new_privs documentation](https://docs.kernel.org/userspace-api/no_new_privs.html): “the setuid and setgid bits will no longer change the uid or gid”. Set this only after separating the privileged broker path from interpreter children. Putting it on the ordinary launcher before invoking sudo prevents the current broker from working. A privileged fixed launcher or a root-owned broker socket can instead perform the authorized transition before confinement.
- [Kernel seccomp documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html): “System call filtering isn’t a sandbox.” Combine syscall filtering with filesystem access policy. Restrict to the native architecture, rejecting alternate ABI syscall numbers as well. Deny memfd_create, ptrace, process_vm_writev, executable anonymous mmap, executable mprotect/pkey_mprotect, executable shmat and personality changes; deny namespace/mount and socket creation for the strict interpreter child. Proc-memory access needs filesystem denial as well.
- [systemd execution documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#MemoryDenyWriteExecute=): “the protection can be circumvented, if the service can write to a filesystem, which is not mounted with noexec”. It also identifies memfd creation and alternate ABIs as escape routes. MemoryDenyWriteExecute by itself is insufficient; executable read-only mappings backed by caller-writable files must also be prevented. This has a documented cost for JIT engines and trampolines.

## Required shape

1. A native shellless login launcher accepts a finite action identifier and separately parsed value fields. It never sends input through a shell. Explicitly document the accepted text grammar. SSH command execution, TTY login, forced commands, SFTP and existing sessions must not provide a second interpreter route.
2. Admission records the interpreter, script and exact transitive read closure. Hash the actual immutable objects, then launch with a fixed executable, fixed arguments and environment, an immutable working directory, stdin from /dev/null, and all inherited descriptors closed except controlled output. Prevent opening mutable data, /proc/*/fd, /proc/*/mem, devices, FIFOs and sockets in the interpreter. Output descriptors must not be bidirectional input channels. This intentionally means own-rights scripts cannot read arbitrary user documents; passive document tools need a separate restricted domain.
3. Every available interpreter needs mandatory entry, including shells, awk, Perl, Python, make, debuggers, database evaluators, editor commands and user-mode foreign runtimes. Naming several known executables is not an inventory proof. A small finite launch allowlist is easier to establish than a blacklist, but each allowed native program needs review for embedded evaluators or helpers.
4. Keep the broker available from the shellless interface. Test install/update through that actual interface, including privileged invocation, rather than only calling the broker from the external operator shell. External superuser breaking remains outside the ordinary domain.
5. Readable native binaries and libraries can be copied, opened by loaders or mapped; declaration membership must authorize the actual code object. Do not infer closure from extension/MIME detection or a deny-exec rule alone. Record all writable mount paths and explain coverage of newly mounted filesystems.
6. A recorded source file may itself contain a literal eval string, which is covered by the source line. It must not acquire additional instructions from mutable file data, argv, stdin, environment, sockets or inherited descriptors. A runner that merely verifies the top-level script hash is insufficient.
7. Removal must revoke running interpreter descendants, already open files and executable mappings. An old process retaining access after a successful apply leaves M4.01 open even if a fresh launch is denied. Old-generation aliases require membership checks independent of previous trust.

## Literal self-test checklist

Tests should attempt each actual route, verify nonzero refusal or ignored input, and verify the unrecorded marker never appears. A generic launcher rejection can prove a removed entry point, but not an interpreter's read-closure enforcement; the latter needs an admitted malicious script executing inside the real runner.

| Rows | Distinct attempts required |
|---|---|
| C4.1–5, C5.1–5 | downloaded/renamed/nested-extracted ELF and script; copied compiler output; symlink/PATH alias; overwrite recorded file; generated plugin/build helper |
| C7.01–06 | interpreter file argument; executable shebang; -c/-e; pipe, FIFO and socket input; redirected regular-file stdin and inherited /proc/self/fd; interactive REPL |
| C7.07–09 | admitted source script; admitted exec(open())/eval script; mutable import directory, zipimport, bytecode and custom import loader |
| C7.10–12 | each embedded evaluator actually present; find -exec/helper escape; writable Git hook and configured interpreter hook |
| C7.13–16 | direct loader; LD_PRELOAD, LD_AUDIT, dlopen and alternate library path; memfd/fexecve/execveat; anonymous RWX and RW→RX; writable/executable aliases |
| C7.17, C8.01–06 | typed shell command; shell rc/profile; BASH_ENV, ENV, PYTHONSTARTUP; exported shell function; executable editor configuration/modeline; Git !alias/filter/build recipe; runtime function/alias/editor-command definition |
| C7.18–25 | mutable generated cache, confined browser positive, active serialized payload, partial-rights runtime, ptrace/process_vm_writev/proc-memory, binfmt and explicit foreign runtime, custom file/stream dispatcher, runtime listener |
| C8.07–08 | privileged extension admission/refusal; positive value-only preference change |
| M4.01–02 | remove while child or mapping survives; attempt copied/old-generation/alias launch after removal |

Positive required: an admitted script under its recorded interpreter runs after declaration application. Test the same positive after rebuilding from scratch, alongside all negative rows. Browser and passive document editing must remain usable; refusing every program is not a successful ordinary-work boundary.

## Initial code inspection

Inspected `../../build/guard.py`, `install-guard.py`, `policy.py`, and `install.sh`. The existing policy has declaration-derived execute trust and selective MIME-based open denial; it does not establish the interpreted-code read closure. The existing sudo broker requires privilege gain, so launcher-wide no_new_privs would regress access. Existing service policy accepts managed executable launch without independently showing that an executable containing an interpreter cannot receive code arguments or mutable inputs. These findings concern this implementation, not every possible system.

## Concrete implementation static review

Reviewed `session.c`, `codeboundary.py`, `install-code-boundary.py` and integration changes in `stand.py`, `guard.py`, `capture.py`. This is static review, not acceptance of runtime behavior. Findings were sent to the builder before tests.

### Required corrections

- **Service transaction deadlock/refusal:** `stand.py:transaction()` holds the exclusive application lock during `activate()`. `activate()` starts managed services before returning. Every `stand-session --service` tries the same shared nonblocking lock. Consequently the intended service launch is refused while the transaction is active. A trusted handoff is required; simply bypassing the lock for the publicly selectable service mode creates a race.
- **Revocation race:** `codeboundary.revoke()` enumerates `/proc` once and kills matching processes; it subsequently waits only for those captured PIDs. A process can fork a child during enumeration. The child can survive a reported successful revocation. Repeated whole-domain enumeration until empty, with the application lock excluding new launches, or kernel cgroup freezing/termination and verified emptiness, is needed. A failure to drain must fail application.
- **Service argument array overflow:** `session.c` fills `args[80]` from all `|`-separated declared service arguments without a bound. `guard.unit()` constrains argument characters but not the number of arguments. A declaration can therefore overflow the launcher's stack. Reject excessive input lengths/counts during validation and check the C bound before every append.
- **Launcher lock permission:** generated AppArmor launcher policy grants read but no `k` permission on the application lock. Kernel file-lock mediation can therefore deny the shared `flock`. Add the narrow lock permission and verify real ordinary launch.

### Inspected controls

- Seccomp architecture handling rejects non-x86-64 and x32 syscall numbers. The mmap branch's jumps deny executable anonymous maps and simultaneous write/execute; the mprotect branch denies executable protection changes. The inspected branch offsets are internally consistent. This does not replace a native syscall self-test.
- Sealed execution supplies null stdin, a fresh environment, immutable working directory, pipe-only output, and closes descriptors before exec. Landlock restricts read opens to recorded immutable members, while AppArmor mediates executable maps and the sole executable. This addresses copied-interpreter entry provided all paths enter the runner and its profile transition succeeds.
- Hash checks cover the executable and top-level script. Remaining mapping/read members rely on immutable ownership and declaration application, so transaction and revocation correctness are essential. A shared lock is released after confinement acknowledgement but before exec: revocation must reliably see and terminate that already-confined child before changing its files.
- Services have declaration-derived fixed argument tables and generated launcher overrides. This closes the earlier conceptual direct-service bypass only after the transaction-lock conflict is corrected and service restart tests pass.
- Writable startup files are not consumed by the native launcher. Interpreter caller arguments are refused. Data tools retain caller arguments but options beginning with `-` are refused and fixed options are supplied. Actual editor/browser behavior still requires positive tests; static checks do not demonstrate ordinary-work preservation.
- Removing entrypoints without changing code files does not trigger the current `changed`-file revocation. Whether this removes required startability while a process remains depends on the declaration semantics; do not claim entrypoint-removal revocation from the file-change test alone.

AppArmor permission reference: [upstream application confinement guide](https://apparmor.dev/getting-started/confine-your-application/) shows `operation="file_lock"` with `requested_mask="k"`. [Upstream profile manual](https://apparmor.dev/man/apparmor.d/) states: “the task receiving the signal must have a receive permission for the sending process' profile.” The launcher/workload profiles currently grant same-profile and unconfined signal peers, but no cross-profile child-to-launcher SIGCHLD allowance. Check normal child collection and termination behavior rather than broadening signal authority indiscriminately.
