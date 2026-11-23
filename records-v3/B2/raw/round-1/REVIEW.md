# Independent review — BC1 round 1

REVIEW: ACCEPTED AS A BOUNDED BUILDER RESULT ONLY.

Recorded 2026-11-22 UTC. Role: review. Scope: C1.1–C1.6, C6.1–C6.6, C10.1–C10.3 and M1.01–M1.02. This review does not accept the whole testbed, does not perform Check 2 or Check 3, and gives no hypothesis outcome.

## Review basis

The review read (not published: outside selected checks and direct evidence); the required sections of `../../../TEXT.md` and `../../../SENTENCES.md`; (not published: orchestration and working notes); the scoped rows of `../../../B1/CHANNELS.md`; the final `../../build/stand.py`, `../../build/guard.py`, `../../build/install-guard.py`, `../../build/noexec.py`, `../../build/capture.py`, `../../build/lab.py`, `../../build/build.py` and round drivers; and the final `../../STAND.md`, `../../BUILD-1.md`, `../../SELFTEST.md` and `../../HOWTO.md`.

The saved final evidence is:

- `rebuilt/summary.json`: suite exit 0, rebuilt image SHA-256 `66c7c055c23a27bcec2f34145a2262ee174fe22e4c7869a6c0b4221aff562062`, no retained disposable VM.
- `rebuilt/round1.jsonl`: 160 assertions, zero failures, with commands, caller context, complete combined output and exit status; the final summary row reports success.
- `rebuilt/original-console.log`: every original D01–D10 phase and cleanup exits 0.
- `rebuilt/original/D10-summary.log` and (not published: over 20 MB: raw trace, snapshot, index or operational log): byte-identical declarations, compare exit 0, 495 full-value rows and no unequal row.
- `rebuilt/original/D07.log`: add, change and remove each boot into the exact reported generation and complete post-boot readback.
- `rebuilt/policy-state.log`: the exact sudo grant, protected backend list, bus policy, masks, inactive schedulers and representative DAC modes.
- `recipe-manifest.json`: the installed source files equal the recorded recipe files.
- `cleanup.json`: no disposable VM, source image or temporary seed remains; the retained base is read-only.

These records support observations of the rebuilt image. They do not turn finite tests into proof of an unrestricted mechanism.

## Findings

No unresolved correctness or security defect was found inside the ten claimed closures under the stated authority boundary: the supplied ordinary account and only the named sudo grants recorded in the declaration. The host-held root operator credential is external laboratory authority. Deliberate changes made through that external root access are outside this result as breaking; the review does not treat ordinary sudo as external authority.

Ten full scoped rows are accepted:

| Rows | Review grounds |
|---|---|
| C1.2, C1.4, C1.5 | Original package executables, helpers, modules and native libraries are unreadable to the ordinary caller; generic sudo does not grant them; supported frontends either apply an exact line or refuse. Alternate direct, copy, library, hook, option and environment routes in the supplied system are denied. Hooks are removed from the supported admission schema rather than trusted as optional enforcement. |
| C6.1, C6.2, C6.3, C6.4 | The supplied user manager and scheduler backends are unavailable, writable user definitions are not consumed, system-manager methods are denied by sender policy, and declared `User=stand` services/timers retain a mediated scheduling path. Direct, D-Bus, transient, cron, at, spool, unit, drop-in, template, alias and generator cases have matching saved refusals. |
| C10.1, C10.2 | Under the stated system-granted authority, package/account/service/network/Bluetooth/firewall mutations either enter through declared tools or lack executable, D-Bus, sudo or kernel authority. Generic root shell, mount/policy tools, environment launchers and authority-bearing declaration inputs refuse. This is not hostile-root containment. |
| M1.01 | Preparation is frozen and validated without a success report. Success follows activation and readback of every candidate line. Invalid preparation leaves the previous generation selected, and the injected live readback mismatch emits failure without success and restores the tested previous state. General live atomicity remains M1.02. |

Seven scoped rows remain NOT CLOSED, correctly preventing acceptance of the whole testbed:

| Row | Required limit |
|---|---|
| C1.1 | No declaration-mediated repository or base-system update exists. Pinned fixture update is not system updating. |
| C1.3 | Backend extraction is denied and native copies are bounded by noexec, but generic extraction followed by interpreted or other executable-memory input remains open. |
| C1.6 | Cache and generation directories are private and retained native copies are denied, but previously copied interpreted bytes can still be supplied to a recorded interpreter. |
| C6.5 | Unit admission validates directives and the executable, but not arbitrary caller-controlled code or configuration selected by that executable's arguments or later inputs. |
| C6.6 | The managed fixture uses a controlled cgroup and its tested timer/service contribution is removed, but every activation edge, surviving process and retained code holder is not enumerated. |
| C10.3 | Arbitrary privileged hooks are refused, but one successful service rollback does not establish restoration of arbitrary cross-resource account, daemon, network or device effects. |
| M1.02 | Shared nonblocking exclusion and finite readback are established. Complete activation, rollback and success semantics for every object and hardware-backed device state are not. |

The initial integration evidence is properly retained. It exposed two comparison calls that bypassed application exclusion, an imprecise SONAME library assertion, and nondeterministic tmpfs sizes in the two-instance comparison. The final source makes every compare path take the transaction lock, drops UID, GID and supplementary groups before reading caller snapshots, uses the absolute protected library path, fixes tmpfs sizes and records the authority DAC as a declaration line. The final rebuilt suite, rather than the earlier integration image, supplies the acceptance evidence.

## Disposition

`../../BUILD-1.md` and the scoped rows of `../../STAND.md` now match the source and evidence: 10 of the 17 BC1 rows are CLOSED and the seven rows above remain NOT CLOSED. The documentation identifies implementation limits as testbed limits and makes no definition-only impossibility argument. The result is accepted for this bounded round. `STAND: partial` remains required, and no whole-testbed, ordinary-work, reproducibility-check or hypothesis verdict follows from this review.
