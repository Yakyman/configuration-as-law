# Design input after FX-B1-2

Recorded 2026-11-22 UTC. The complete P1/P2/P4/Removal existence outcome remains **?**. This is a candidate design input, not a ready configuration or a completed Check 2. Current verdicts are in CHANNELS.md; original notes and raw evidence are historical inputs. The fix does not build the missing broker or a cooperating own-rights interpreter.

## Exact available version pins and evidence limits

The original probe used **Debian 13.8 amd64**, released 2026-11-21, with the explicitly selected **trixie-backports kernel package `7.3.4-1~bpo13+1`, image `linux-image-7.3.4+deb13-amd64`**, and **systemd `257.13-1~deb13u1`**. These versions were checked in primary release/package pages and subsequently booted in the disposable P01 VM. The kernel requires backports `linux-base 4.17~bpo13+1`; select the backports dependency set explicitly. Actual package versions and required kernel configuration options are saved in `raw/vm-versions-output.txt`. Debian stable's default kernel is instead `6.12.117-1` / `6.12.117+deb13-amd64`; do not silently attribute the newer API to that default. Upstream latest stable at source access was 7.3.5 (2026-11-17), distinct from the available Debian backport. [Evidence: `raw/ordinary-sources.md` V1–V6; `raw/install-sources.md` E27–29.]

The execution-check API and locked `SECBIT_EXEC_RESTRICT_FILE` / `SECBIT_EXEC_DENY_INTERACTIVE` are present in versioned **Linux 6.14** documentation and the `inc` source example, with `set-exec` also verified in source package 7.3.4-1, and documented again for **Linux 7.3**. Linux 6.12 already documents `cgroup.kill`; systemd 257 documents control-group stopping and the mature memory-execution restriction facilities. These establish supported upstream primitives at the selected newer kernel version, not an enabled or correct boot policy. [Evidence: `raw/c7-sources.md` E1–5,E16–19; `raw/c7-pinned-source-checks.json`; `raw/mechanics-sources.md` E5,E6.]

Before the actual testbed's first observation, the builder must pin package checksums, kernel build configuration and boot LSM selection, source versions of all cooperating evaluators, policy and the concrete declaration/ordinary commands as Section 4.1 requires. Required configuration includes dm-verity, enforcing SELinux (or one equivalently complete mandatory policy), seccomp filters, cgroup v2, and the execution-check ABI. The package pages alone do not establish these runtime choices. No claim is made that a distribution ships the needed interpreter/editor patches. The limited Linux 6.14 sample demonstrates the API, not adoption for the own-rights interpreter class; CPython verified-open/audit facilities are integration points, not a complete sandbox. Production Bash/Python/glibc adoption across all input paths is unestablished (`raw/c7-sources.md`). P01 specifically establishes that Debian Python 3.13.5, package `3.13.5-2+deb13u5`, executes `-c` code as uid 65534 with both securebits and locks (`0xf00`) retained across exec. Setting the bits alone does not close that route for this binary (`raw/python-securebits-output.txt`). The other input paths were not probed.

## Minimum control responsibilities, with evidence boundaries

1. **Native primitives and conditional file controls.** Immutable code, execution/mapping authorization, native memory restrictions and revocation remain documented subcontrols. D supplies file-open denial only for processes that enter or inherit its domain; a mandatory component covering every interpreter launch is not evidenced. If imposed on the whole session, its document/project-data read denial also reaches the shell and descendant editors. D does not sanitize stdin, argv/environment, inherited descriptors or socket/IPC instruction streams, including custom dispatch in C7.24. F/I cooperation and selective mandatory placement remain UNKNOWN. No complete positive C7 integration is established. [Sources: raw/c7-sources.md E1–12; fix-b1-2/evidence-audit.md.]
2. **Declaration mutation authority — candidate, UNKNOWN.** Package, service, network, account, firewall and container managers, including privileged and direct backend/API paths, would need a common declaration-only mutation path. General mandatory denials and documented manager APIs do not evidence this broker. Rows depending on it are listed below; installation, updating, Wi-Fi and Bluetooth through it remain proposed workflows. Code admission also does not authorize runtime ports: S2.2-15 and C7.25 apply. Landlock TCP binding restriction is a bounded subcontrol, not a complete listener policy. [Sources: raw/install-sources.md; raw/mechanics-sources.md; fix-b1-1/evidence-addendum.md.]
3. **Application lifecycle.** Inert staging, durable file/boot selection, bounded removal and finite comparison have documented primitives. Whole-state success, immediate-power-cut recovery and failure/one-hour recovery remain M1.02/M2.02/M3.02 UNKNOWN. Revoking an old file name alone is insufficient; terminate holders, revoke permissions and withdraw activation edges before success. The bounded M4.03 withdrawal does not establish declaration-only creation/modification of those edges. [Sources: raw/mechanics-sources.md E1–12.]

These are candidate responsibilities, not a proven minimal implementation. All channel verdicts now follow their full R requirement; none is certified closed merely from its subcontrol. Whole-state lifecycle and runtime-port obligations remain applicable. The eight CLOSABLE mechanics rows retain their explicitly narrower requirements. Browser code genuinely confined to the program's interface retains the explicit exemption; its independent helper programs still require recording. Host interpreters do not inherit that exemption. No author rule or changed failure condition is supplied to resolve a hole.

## What this design cannot certify closed

This list is generated from precisely the non-CLOSABLE channel/mechanic rows. No NOT-CLOSABLE or CLOSABLE-ONLY-BY-REMOVAL result is established.

- **C1.1 — UNKNOWN:** Repository install, upgrade, downgrade, reinstall and remove through CLI.
- **C1.2 — UNKNOWN:** Direct low-level manager or library/API/GUI frontend bypassing CLI wrapper.
- **C1.3 — UNKNOWN:** Alternate root, alternate database, package extraction into writable directory.
- **C1.4 — UNKNOWN:** Maintainer scripts, triggers, hooks and post-install service activation.
- **C1.5 — UNKNOWN:** Hook disable/config override, backend flag or environment bypass.
- **C1.6 — UNKNOWN:** Old generations, package cache copies, rollback paths after removal.
- **C2.1 — UNKNOWN:** pip system, --user, virtualenv, --target/--prefix installs.
- **C2.2 — UNKNOWN:** npm local, global, prefix/workspace installs and executable links.
- **C2.3 — UNKNOWN:** Local archives, VCS URLs and package indexes selected by flags.
- **C2.4 — UNKNOWN:** Editable pip installs, npm links, mutable source and dependency replacement.
- **C2.5 — UNKNOWN:** Build backend, lifecycle script, npm run/start/test and dependency hook execution.
- **C2.6 — UNKNOWN:** Native extensions and admitted module/.pth inputs; custom evaluator behavior in C7.08.
- **C3.1 — UNKNOWN:** Flatpak system install/update and graphical or D-Bus frontend.
- **C3.2 — UNKNOWN:** Flatpak --user install, extra installation roots/remotes, local bundles.
- **C3.3 — UNKNOWN:** Flatpak runtime/extension updates, override permissions, alternate commands and development mode.
- **C3.4 — UNKNOWN:** AppImage directly executed and self-mounted via FUSE.
- **C3.5 — UNKNOWN:** AppImage extracted/mounted externally, AppDir launch or self-update.
- **C4.1 — UNKNOWN:** Download a native executable and chmod/run it.
- **C4.2 — UNKNOWN:** Download and extract archive, including nested archives and renamed files.
- **C4.3 — UNKNOWN:** Download by browser, curl, copier, sync client or application self-updater.
- **C4.4 — UNKNOWN:** Downloaded script or library passed to existing interpreter/loader.
- **C4.5 — UNKNOWN:** Stream download directly into interpreter or process substitution.
- **C5.1 — UNKNOWN:** Compile/link native program in home, then execute output.
- **C5.2 — UNKNOWN:** Build-system commands, configure probes, generators and test binaries.
- **C5.3 — UNKNOWN:** Install target copying to user prefix, changing PATH or creating symlinks.
- **C5.4 — UNKNOWN:** Rebuild/replace an already recorded binary or library in place.
- **C5.5 — UNKNOWN:** Compilers embedding plugins or build processes loading generated code.
- **C6.1 — UNKNOWN:** Persistent user units and drop-ins, aliases, template instances and symlinks.
- **C6.2 — UNKNOWN:** Direct manager API/CLI start, enable, reload, set-property or link.
- **C6.3 — UNKNOWN:** Transient service/scope/timer/path/socket created through systemd-run or D-Bus.
- **C6.4 — UNKNOWN:** User cron entries, @reboot and crontab replacement.
- **C6.5 — UNKNOWN:** Generated units, user environment generators and cron command text loading more code.
- **C6.6 — UNKNOWN:** Removed unit reactivated by socket, timer, dependency, lingering manager or surviving child.
- **C7.01 — UNKNOWN:** Script file passed as interpreter argument.
- **C7.02 — UNKNOWN:** Executable shebang script.
- **C7.03 — UNKNOWN:** Code supplied as -c or -e argument.
- **C7.04 — UNKNOWN:** Code piped into stdin, FIFO, socket, here-document or process substitution.
- **C7.05 — UNKNOWN:** Code from regular file redirected to stdin or /proc/self/fd/N.
- **C7.06 — UNKNOWN:** Interactive REPL with language statements.
- **C7.07 — UNKNOWN:** Recorded script sources another file.
- **C7.08 — UNKNOWN:** exec(open(file).read()), eval of read data, custom import loader.
- **C7.09 — UNKNOWN:** Ordinary import, zipimport and non-regenerable bytecode; module path injection.
- **C7.10 — UNKNOWN:** Embedded interpreter in editor, awk, make, debugger or database program.
- **C7.11 — UNKNOWN:** Helper process launch: find -exec, editor shell escape, make recipe child.
- **C7.12 — UNKNOWN:** Git hook program in writable project.
- **C7.13 — UNKNOWN:** Direct dynamic loader invocation.
- **C7.14 — UNKNOWN:** LD_PRELOAD, LD_AUDIT, dlopen/FFI and alternate library path.
- **C7.15 — UNKNOWN:** Native executable memfd, fexecve/execveat of memory file.
- **C7.16 — UNKNOWN:** Anonymous machine code, JIT, writable/executable aliases.
- **C7.17 — UNKNOWN:** Shell command line, including invocation of a declared program.
- **C7.18 — TEXT-OPEN:** Regenerable executable bytecode/JIT cache with same-rights execution.
- **C7.19 — UNKNOWN:** Browser web code and JIT confined inside recorded renderer/helper programs.
- **C7.20 — UNKNOWN:** Code-bearing serialized input (pickle, macro-bearing document).
- **C7.21 — TEXT-OPEN:** WASI module with a preopened host directory and partial runtime rights.
- **C7.22 — UNKNOWN:** Debugger/interpreter writing another process memory or injecting code.
- **C7.23 — UNKNOWN:** binfmt_misc handlers and user-mode foreign-binary interpreters.
- **C7.24 — UNKNOWN:** Recorded custom dispatcher: file-open route and non-file instruction input without eval/import.
- **C7.25 — UNKNOWN:** Runtime-selected TCP listening port (also C2/C3/C5/C9.2).
- **C8.01 — UNKNOWN:** Shell startup profiles and rc files.
- **C8.02 — UNKNOWN:** Environment-selected startup code, BASH_ENV/ENV/PYTHONSTARTUP.
- **C8.03 — UNKNOWN:** Environment-imported shell functions and command substitutions.
- **C8.04 — UNKNOWN:** Editor executable configuration, plugins, modelines executing code.
- **C8.05 — UNKNOWN:** Project-local executable settings: Git !alias, external filter, build recipe.
- **C8.06 — UNKNOWN:** Runtime own-rights code definitions: shell functions, aliases, editor commands.
- **C8.07 — UNKNOWN:** Browser extension executing with browser-equivalent rights.
- **C8.08 — UNKNOWN:** Settings only read as values, such as theme or home page.
- **C9.1 — UNKNOWN:** Rootful image pull/run, mutable tags and manager API.
- **C9.2 — UNKNOWN:** Rootless containers, user namespaces, alternative OCI runtime invocation.
- **C9.3 — UNKNOWN:** Bind-mounted executable/script, writable overlay, exec into container and package install inside.
- **C9.4 — UNKNOWN:** Image build RUN/hooks, import/load archive and commit modified container.
- **C9.5 — UNKNOWN:** Privileged/host-namespace/device/runtime-hook options.
- **C9.6 — UNKNOWN:** Removed image/container restarted through old name, daemon state, API or retained layers.
- **C10.1 — UNKNOWN:** Documented privileged package/service/account/network/firewall administration.
- **C10.2 — UNKNOWN:** Built-in privileged tool changes guards, permissions, mounts or execution policy.
- **C10.3 — UNKNOWN:** Retained arbitrary privileged hooks and multi-resource live side effects.
- **C10.4 — TEXT-OPEN:** Root editor with documented package installer.
- **M1.02 — UNKNOWN:** All C1–C10: complete live activation and success report across all objects.
- **M2.02 — UNKNOWN:** All C1–C10: add/change/remove power cut with complete runtime/device replay.
- **M3.02 — UNKNOWN:** All C1–C10: partial activation failure, stalled worker, or no report at one hour.
- **M5.02 — UNKNOWN:** All C1–C10: unrestricted algorithmic requirements and semantic effects.

Q2 is an additional **author question / requirement hole**, outside the channel-row count: Understanding as a claimed consequence versus an admissibility filter, and concrete-object knowledge versus knowing a symbolic rule, are both left open. The previous categorical exclusion of this question is withdrawn. Declaration form alone is a design choice under S2.5-3; the question concerns its interaction with S2.4-1. See CHANNELS Q2 for the conditional construction and consequences of both choices.

## Ordinary work: requirements and unresolved feasibility

Q3 in CHANNELS gives schematic declaration fields and documented backend interfaces for all six required ordinary actions, plus programming and pip/npm. Those workflows are proposals where broker/interpreter integration is UNKNOWN. No required action is proved impossible, and none of those unknown integrations is certified by listing a backend API. After entry into D, scripts and dependency/build code lose new opens of unrecorded user-document and project-data files. Whole-session inheritance also denies these reads to descendant editors, so document editing is not preserved by that blanket arrangement. Selective mandatory entry is unestablished. Scripts still receive bytes through stdin, argv/environment, inherited descriptors and socket/IPC input; forwarding those bytes to admitted own-rights dispatchers retains the conditional failure. Safe mediation is unestablished. A recorded VM remains a distinct expressly exempt guest route, not proof of unrestricted host programming.

C8.07 is required own-rights extension code with UNKNOWN closure, not an extension/settings hole. C10.4 is restored as TEXT-OPEN. C7.18 and C7.21 remain TEXT-OPEN. The review-confirmed definitional holes invoke Section 4.1's 0 rule separately from the unresolved system-existence question. No universal engineering NOT-CLOSABLE conclusion is established.

No fix-round VM or new experiment was needed. The original P01 source-first justification was incomplete because the exact distribution source package and patches were not consulted; its negative binary observation remains evidence. Corrected procedural and timestamp accounts are in fix-b1-1/PROBE-DISPOSITION.md and fix-b1-1/python-securebits-plan-corrected.md. Round 2 preserves prior outputs and hashes all existing inputs in fix-b1-2/input-manifest.json; only report consistency checks were rerun, into fix-b1-2/validation.json. The current disposition is FIX-B1-2.md; separate review is recorded in fix-b1-2/REVIEW.md.
