# B2 code review

Recorded 2026-11-22 UTC. Scope: static inspection of the named B2 build files and research records. No VM, probe, or integration run was performed. Python AST parsing and shell syntax parsing passed. This review does not require a whole-system P4 proof: the documented native-root backend and non-file interpreter routes remain explicitly partial. The findings below concern behaviour that this finite implementation claims to apply, verify, remove, report successful, or compare.

## Blocking findings

1. **`stand-compare --snapshot` cannot take a snapshot.**

   - Source: `B2/build/stand.py:379` is reached for every two-argument `stand-compare` invocation before the snapshot branch at `B2/build/stand.py:384`. Thus `stand-compare --snapshot FILE` calls `compare("--snapshot", "FILE")`, which attempts to read `--snapshot` as JSON. Both snapshot calls in `B2/build/selftest.py:27` and `B2/build/selftest.py:31` therefore fail before Check 3 data are produced.
   - Effect: the declared two-machine comparison cannot run.
   - Fix: dispatch `--snapshot` first and validate that it has exactly one output argument; dispatch the two-input comparison only otherwise. Add a direct syntax-level invocation test or a self-test assertion that both snapshot files exist and are JSON arrays.

2. **A `port` line is observation only; application and removal never control the listener.**

   - Source: `B2/build/stand.py:160-162` only compares the result of `ss`. `activate()` has no `port` case in either removal (`:229-235`) or addition/change (`:236-261`), while the firewall table created at `:263-267` does not create or close a listening socket.
   - Effect: a declaration can report success while a required open port is absent, or a removed port remains listening. This violates the stated P2 and Removal checks for the supported `port` type. It also cannot make a firewall rule evidence that a port is not open.
   - Fix: either reject standalone port lines and represent each supported listener as a managed service/socket whose lifecycle is applied and removed, or implement a finite listener backend with an explicit owner, start/stop operation, and readback. Validate protocol and port fields rather than hard-coding TCP in `observe()`.

3. **The schema permits removal of unmanaged contributions, but the removal path deliberately retains them.**

   - Source: file ownership is restricted to `managed` base/program/code rows at `B2/build/stand.py:191-192`; old account, privilege, login-key, Wi-Fi, and Bluetooth rows are skipped when not managed at `:229-235`; old services are only stopped/unlinked when managed at `:219-223`. `candidate_edit()` nevertheless permits removal of any line ID at `:354-362`.
   - Effect: removing an accepted declaration line can report success while its files, account, service, key, privilege, or network state remains in force. The factory declaration itself contains unmanaged accounts, services, keys, and privilege lines (`B2/build/capture.py:28-40`), so this is reachable through the provided edit interface.
   - Fix: reject removal or modification of every unmanaged line before staging, or give each accepted line an explicit reversible owner and implement its removal. Do not let a successful application remove the declaration record while retaining its contribution.

4. **The success report is issued after a trust-database check that explicitly does not establish enforcement convergence.**

   - Source: `B2/build/policy.py:163-185` returns `reload_acknowledged=False`; `B2/research/policy.md:56-60` states that persisted database equality does not establish the synchronous enforcement boundary. Nevertheless `B2/build/stand.py:269-271` accepts that return as activation success and `:309-318` verifies and emits `SUCCESS`.
   - Effect: after add, change, or removal, the reported-success point can precede the only proposed execution gate's effective decision boundary. The implementation therefore cannot claim that launch authority is present or revoked at reported success, including after a power cut and replay.
   - Fix: keep this backend partial and refuse to emit successful application for a declaration whose correctness depends on it, or add and verify a real synchronous boundary with an evidence-backed readback of an actual allow/deny decision. Database polling, a delay, and service liveness are insufficient according to the component's own research record.

5. **The first failed application can leave live changes with no prior declaration restored.**

   - Source: `B2/build/stand.py:307-318` begins live activation before a current declaration exists. If that activation fails, the `else` at `:329` only prints `FAILED initial application`; it neither rolls back the changes nor records a recoverable prior state. The install path invokes this first application at `B2/build/install.sh:29`.
   - Effect: a partially created account, file, service, rule, or profile can survive a failed first application although no successful declaration is in force. A later boot has no selected declaration to replay.
   - Fix: establish and durably select a verified factory generation before any mutable activation, or make initial activation fully staged and reversible. On every failed return, verify the selected prior generation's actual state before reporting failure.

6. **Factory capture does not create declaration lines for several required effective-state classes.**

   - Source: `B2/build/capture.py:7-20` walks selected filesystem trees but explicitly excludes saved network profiles at `:9`; `:28-44` adds accounts, selected system services, two SSH-related lines, and boot only. There is no capture of effective firewall tables, saved network entries, Bluetooth pairings, user services, or cron/scheduler entries.
   - Effect: the factory declaration can be successfully applied and verified while in-force objects required by the task are absent from its lines. A filesystem hash is not a readback of an effective firewall rule, saved connection, pairing, or user scheduler state.
   - Fix: either construct the fresh image so each unsupported class is absent and verify that absence before freezing, or add finite capture and verification for each class. In particular, inventory effective firewall rules separately from files and create saved-network lines instead of excluding their backend directory.

## Major gaps that must constrain claims

7. **The provided wrappers do not mediate the retained backend executables.**

   - Source: `B2/build/install.sh:5-6` installs same-name links only in `/usr/local/bin`; `B2/build/stand.py:10-16` itself calls absolute backend paths. The development self-test acknowledges that direct original backend paths remain at `B2/build/selftest.py:47-51`.
   - Effect: refusal through the wrapper is not closure of the package, account, service, network, firewall, scheduler, or container built-in tool. This is a known partial P4 boundary, including invocation with elevated privileges; it must be reported as NOT CLOSED rather than treated as breaking.
   - Fix: retain the explicit limitation in all results, and do not describe wrapper refusal as mediation of the named backend. A closure claim needs a mandatory mutation boundary for the backend APIs, or the backend must be removed from the admitted system.

8. **The policy rule allows any trusted base executable, including unrestricted interpreters and their non-file inputs.**

   - Source: `B2/build/policy.py:14` allows execution for every trusted file. The factory base manifest is populated from broad system trees (`B2/build/capture.py:13-20`). `B2/research/policy.md:43-47` correctly identifies arguments, standard input, generated memory, alternate MIME types, and browser code as uncontrolled.
   - Effect: this must not be presented as a closure of own-rights interpreter routes or as full removal of retained script bytes. It is an explicit partial-P4 limitation, not a reason to reject the finite prototype itself.
   - Fix: state the limit per variant and keep any successful claim bounded to measured native file-entry cases.

## Review disposition

Do not mark application/verification/removal, immediate-power-cut recovery, or reproducibility ready until findings 1-6 are resolved and rechecked independently. Findings 7-8 may remain documented open routes in a partial P4 result; they must not be upgraded to closure by wrapper or file-trust evidence.
