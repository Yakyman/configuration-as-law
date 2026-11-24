# Version 4 carry-forward difference record

Recorded 2026-11-23 UTC. Builder analysis only; no new mechanism is built here.

Historical authority: (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), (not published: record outside this collection), and (not published: record outside this collection). The review accepts the last bounded build scope, not the entire testbed: **78 historical CLOSED, 10 historical NOT CLOSED, STAND: partial**.

Target authority: [TEXT](../TEXT.md), Sections 8, 9.1, 9.3, 9.4 and Appendix A.4.1/A.4.3/A.4.4, with exact [sentence IDs](../SENTENCES.md). The table preserves historical dispositions; **none of the 88 is validated against version 4 by this carry-forward analysis**. “No” in criterion change means the core object-level criterion remains, not that old shellless evidence remains sufficient. “Yes” means a concrete classification, coverage, authority or ordinary-work criterion changes. All rows require subsequent v4 evidence/review; the unchanged round-0 test is an attribution baseline only.

The ten historical open rows are C1.1, C1.3, C6.5, C10.3, C10.4, M1.02, M2.02, M3.02, M5.01 and M5.02. Their historical reasons are preserved in [the machine-readable map](v4-variant-map.json). Existing format limitations are implementation choices; they are not universal impossibility arguments. An implementation failure remains `?` unless a separately reviewed definition-only argument establishes `0` (Appendix A.4.1). No such argument is made here.

## Mechanism dispositions

“Removed” and “must change” describe the version 4 target for later rounds; round 0 retains all carried bytes. References in the final column identify the mechanism in the previous STAND, including its type table and variant evidence, rather than unseen external records.

| Carried mechanism | V4 disposition | Required interpretation or work | Sentence/section basis | Previous STAND location |
|---|---|---|---|---|
| Pinned image, complete recipe, archive checksums, lab slot locks, disposable overlays and independent builds | kept | Build/reproducibility scaffolding remains; carry recipe unchanged for round 0, not a copied finished image as a rebuild. | S8.1-2; Sections 9.4 and A.4.4 | Image and implementation |
| Finite stand.py translator and actual-state readers | must change | Retain transaction core; extend covered installed-object/setting semantics and supported declaration-writing interfaces; factory capture alone remains insufficient for P1. | S8.2-1, S8.2-7, S8.2-8, S8.3-4, S8.3-7 | Image and implementation |
| Factory package/base manifest, recognized code and shell-startup inventory | must change | Record packages including no-code/no-file packages and defaults with provenance; distinguish unchanged package contents, changed settings and records/material. Do not infer completeness from signatures. | S8.2-6, S8.2-7, S8.2-8, S8.2-15, S8.2-16, S8.2-17 | Image and implementation |
| Historical file-trust attempt and supplementary noexec mounts | kept | Historical evidence and supplementary control only; neither closes interpreter input or establishes the required shell. No active restoration of a superseded failed approach. | S8.2-9, S8.3-6; Section 9.3 | Image and implementation |
| Shellless run/broker-only ordinary login and refusal of expansions, pipelines, functions and PTYs | removed | Remove as the v4 ordinary interface and closure argument; a real command shell and ordinary typed commands are mandatory. Keep unchanged in round 0 solely as the baseline. | S8.2-4; Section 9.3 | Image and implementation, first boundary bullet |
| Fixed script/interpreter hashes, null stdin, fixed argv/environment and closed inherited FDs | must change | Hashes/coverage may remain for stored scripts, but universal null-input/refusal cannot substitute for shell work or the unsaved-download reboot case. Retest declared own-script use. | S8.2-4, S8.2-9; Section 9.3 | Image and implementation, first boundary bullet |
| Declared AppArmor execution/mapping policy, ELF admission and mount/namespace restrictions | kept | Retain as a bounded stored-code control; revalidate inheritance and entrypoints after shell introduction. Restrictive artifact admission remains design, not definition. | S8.2-9, S8.3-4, S8.3-6; Section 8.5 | Image and implementation, second boundary bullet |
| Immutable input root, recorded aliases, privilege drop, Landlock and no_new_privs | must change | May retain sealed mode for appropriate recorded programs; it cannot be the sole ordinary shell interface. Separate material reading from stored executable activation and preserve required ordinary work. | S8.2-4, S8.2-15, S8.2-23; Section 9.3 | Image and implementation, third boundary bullet |
| Seccomp executable-memory/injection/ABI controls and inherited confinement | kept | Controls may remain design choices. Runtime-only memory state follows its creating program/setting; saved payloads and access settings require separate assessment. Revalidate free commands and the unsaved-execution/reboot case. | S8.2-4, S8.2-5, S8.2-9, S8.2-14; Section 9.3 | Image and implementation, fourth boundary bullet |
| Universal socket/IPC/listener denial as runtime-port closure | must change | An open port or runtime relationship follows its creating program/setting. Access/network settings in force remain required; no separate port line is mandated. Socket refusal cannot replace the unsaved-download case. | S8.2-5, S8.2-13; Section 9.3 | Image and implementation, fourth boundary bullet |
| Fixed data tools, literal writer, restricted editor and passive text browser | must change | Retain document/browser positive workflows but expose useful ordinary commands in the shell; distinguish values-only preferences from launch/access settings and package defaults. | S8.2-4, S8.2-14, S8.2-15, S8.2-17; Section 9.3 | Image and implementation, fifth boundary bullet |
| Manager-owned service setup, permanent identity/capability drop and exact kernel-profile verification | kept | Recorded service requirements and effective readback remain useful; do not require blocking direct external-root breaking. | S8.1-11, S8.1-12, S8.1-15, S8.1-16, S8.3-5 | Image and implementation, sixth boundary bullet |
| Code/job quiescence, domain revocation, policy replacement and exact loaded-policy comparison | kept | Preserve live-holder revocation, old launch withdrawal and candidate restart; check additional shell-exposed holders and remaining package/source contributions. | S8.2-16, S8.3-5; Section 8.4 Removal | Image and implementation, seventh boundary bullet |
| Restricted ordinary sudo, private backends, daemon/API authorization and declaration broker | must change | Retain authority boundaries as design, but test supported built-in tools under actual superuser rights: they must write/apply, not rely solely on caller denial. A root editor installer is included in its installer part. | S8.1-5, S8.1-7, S8.1-8, S8.3-7 | Image and implementation; channel table C1/C6/C10 |
| External operator access and direct privileged mutation of system mechanisms | kept | Keep breaking possible and separately reported; direct root file mutation outside built-in tools is not a channel that must be blocked and refutes no property. | S8.1-15, S8.1-16, S8.3-1 | Image and implementation, setup paragraph |
| Immutable pip/npm lock/archive reconstruction and native-wheel entry | must change | Retain exact content/dependency reconstruction; cover whole installed packages/defaults and make supported installer calls declaration-writing under both authorities through the shell. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | Channel mechanisms added in round 4 |
| Flatpak/OSTree and AppImage/SquashFS import, scratch parser confinement and removed native helper | must change | Retain pinned parsing and inactive preparation; reassess installed-package contents and native frontend mutation under superuser rights. General-purpose built-in installer parts cannot bypass recording. | S8.1-5, S8.2-7, S8.2-8, S8.3-7 | Channel mechanisms added in round 4 |
| OCI exact image/configuration rows, immutable root and single-entry container confinement | must change | Retain immutable execution mechanism; establish whole installed-image coverage and own-process code classification, including removal of installed non-code contributions. | S8.1-9, S8.2-7, S8.2-8, S8.2-22; Section 8.4 Removal | Channel mechanisms added in round 4 |
| Trusted repository/base transaction catalog and captured package state | must change | Retain exact captured transactions; positively exercise all admitted install/update/remove operations and package/default coverage, including root invocation. Unsupported transactions can remain explicit limits. | S8.1-6, S8.2-7, S8.2-8, S8.2-17, S8.3-7 | Channel mechanisms added in round 4 |
| Inert download import and recorded C-source compiler with separately imported output | must change | Retain as an allowed workflow, but separate output-line requirement is not definitional: a system-derived output may be covered by its generating line. Add the unsaved execution/reboot case. | S8.2-16; Section 9.3 | Channel mechanisms added in round 4 |
| User-job/scheduled-command and saved Wi-Fi/prepared Bluetooth frontends | must change | Registration remains a setting channel and tools must write/apply it. Saved/prepared profiles do not prove actual connection/pairing; hardware ordinary work remains required. | S8.2-13, S8.3-5, S8.3-7; Appendix A.4.3 | Channel mechanisms added in round 4 |
| Static parser/compiler profiles recorded and verified against actual enforcing kernel bytes | kept | Exact policy readback remains a P2 mechanism; revalidate any changed policy after future work. | S8.1-12, S8.3-5 | Channel mechanisms added in round 4 |
| JSONL designated declaration, checked base manifest, inline payloads, generation digest and conflict rejection | kept | A finite explicit declaration is permitted. Keep complete example and exact required values; do not present the finite schema as a restriction imposed by the hypothesis. | S8.1-1, S8.1-3, S8.1-12; Section 8.5 | Declaration and defaults |
| Base/program/code schema and exact file requirements | must change | Internal type names may remain, but cover installed objects regardless of executable content; package/derived-source lines can cover objects without distinct lines. | S8.2-7, S8.2-8, S8.2-16 | Declaration and defaults, type table |
| Account, privilege, login-key and password-login exact requirements | kept | Existing explicit settings/readback remain valid; distinguish local login authorization from private credentials for other machines. Schema limitations remain explicit. | S8.2-13, S8.2-15, S8.3-5 | Declaration and defaults, type table |
| Service/timer/socket units, masked user managers, protected schedulers and explicit default rules | must change | Keep declared job mechanism while making configuration tools write/apply; defaults from a package are covered by its package line, runtime sockets/relationships are not separate required objects. | S8.2-5, S8.2-13, S8.2-17, S8.3-7 | Declaration and defaults, type table |
| Firewall rules, backend DAC, mount flags and fixed boot default | must change | Rights/network/filesystem/boot settings in force must be covered; runtime mount observations follow their creating object. Package defaults need provenance, and explicit required values still must verify. | S8.2-5, S8.2-13, S8.2-17, S8.3-5 | Declaration and defaults, type table |
| Standalone port row as mandatory object type | removed | Remove mandatory independent-port rationale, not necessarily optional recorded observations; optional rows are allowed but then P2 requires their stated state. | S8.2-5, S8.2-19, S8.3-5 | Declaration and defaults, port row |
| Wi-Fi/Bluetooth exact profile schema and frozen boot firmware observation | kept | Keep finite readback with explicit hardware/firmware limits; these observations do not establish real radio work or unknowable external state. | S8.1-12, S8.2-13, S8.3-5; Appendix A.4.3 | Declaration and defaults, type table |
| Application lock, supervised worker, journal, inverse reconciliation and watchdog recovery | kept | Retain transaction mechanisms and unresolved multi-resource recovery limits. The carried one-hour setting is engineering policy, not a newly inferred v4 property. | S8.1-13, S8.1-14, S8.3-1, S8.3-5 | Application, comparison and removal |
| Durable success report, sync ordering, boot replay and PAM/session readiness gate | kept | Last successful report remains authoritative; repeat required three cuts per add/change/remove in later validation. | S8.1-14, S8.3-5; Appendix A.4.3 | Application, comparison and removal |
| Per-line stand-verify and actual-value stand-compare | kept | Retain exact state comparisons and independent installations; expand readers with revised object requirements rather than exclude differing rows. External-list reproduction exclusion must remain explicit if used. | S8.1-12, S8.3-5; Sections 8.4, 9.4 and A.4.4 | Application, comparison and removal |
| Independent stand-inventory census and explicit unknown output | must change | Apply four questions in order using installed-package membership, unchanged/changed provenance, execution capability and settings purpose; do not count runtime objects separately or material as unrecorded solely because unclaimed. Unknown facts stay FACT_UNKNOWN. | S8.2-3, S8.2-5, S8.2-6, S8.2-7, S8.2-15, S8.2-16, S8.2-17 | Application, comparison and removal |
| Ordered socket/timer/service removal, duplicate contribution ownership and atomic rule regeneration | must change | Preserve mechanics while extending residual coverage to all installed objects/defaults and derived-source claims; inert retained installed contents are not automatically removed. | S8.1-9, S8.2-16, S8.2-17; Section 8.4 Removal | Application, comparison and removal |
| Historical assertions, combined declaration and independent rebuilt-image comparison | kept | Run unchanged for round 0 as attribution baseline; their success does not validate v4 shell behavior, whole-object coverage or complete ordinary work. | S8.3-2; Sections 9.1, 9.3, 9.4 and A.4.1 | Observed scope and remaining work |

## All 88 variants

Historical closure is copied from the final previous STAND, not from B1's proposed-mechanism verdict. The criterion column is a v4 requirement comparison, not a new closure verdict. Every row is currently **NOT VALIDATED for v4**. The round number is a planning assignment coordinated with [ROUNDS](ROUNDS.md); final combined validation covers all rows.

| ID | Variant | Previous-night end | V4 changes criterion? | Concrete implication | Basis | Planned round |
|---|---|---|---|---|---|---|
| C1.1 | Repository install, upgrade, downgrade, reinstall and remove through CLI | NOT CLOSED | Yes | Supported installer operations must positively write and apply declaration changes under ordinary and full superuser invocation; refusal of unavailable options alone is insufficient. Package/dependency contents include non-code installed objects. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-16, S8.3-7 | 1 |
| C1.2 | Direct low-level manager or library/API/GUI frontend bypassing CLI wrapper | CLOSED | Yes | Supported installer operations must positively write and apply declaration changes under ordinary and full superuser invocation; refusal of unavailable options alone is insufficient. Package/dependency contents include non-code installed objects. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-16, S8.3-7 | 1 |
| C1.3 | Alternate root, alternate database, package extraction into writable directory | NOT CLOSED | Yes | Distinguish an installer-created installed package in an alternate root/database from inert downloaded material. Nonstartability alone does not establish that installed package contents are absent; inspect provenance and interpreter activation. | S8.1-6, S8.1-9, S8.2-6, S8.2-7, S8.2-8, S8.2-15 | 2 |
| C1.4 | Maintainer scripts, triggers, hooks and post-install service activation | CLOSED | Yes | Supported installer operations must positively write and apply declaration changes under ordinary and full superuser invocation; refusal of unavailable options alone is insufficient. Package/dependency contents include non-code installed objects. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-16, S8.3-7 | 1 |
| C1.5 | Hook disable/config override, backend flag or environment bypass | CLOSED | Yes | Supported installer operations must positively write and apply declaration changes under ordinary and full superuser invocation; refusal of unavailable options alone is insufficient. Package/dependency contents include non-code installed objects. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-16, S8.3-7 | 1 |
| C1.6 | Old generations, package cache copies, rollback paths after removal | CLOSED | Yes | Remove all uncovered installed package contributions, including non-code objects; a retained archive must be established as material rather than assumed exempt merely because launch is denied. | S8.1-9, S8.2-7, S8.2-8, S8.2-15, S8.2-16; Section 8.4 Removal | 3 |
| C2.1 | pip system, --user, virtualenv, --target/--prefix installs | CLOSED | Yes | Recheck positive package installation through shell-accessible built-in frontends at both authorities; record the whole installed package/dependency closure, including non-code contents and installation defaults. Mutable links/hooks remain subject to resulting object coverage. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | 1 |
| C2.2 | npm local, global, prefix/workspace installs and executable links | CLOSED | Yes | Recheck positive package installation through shell-accessible built-in frontends at both authorities; record the whole installed package/dependency closure, including non-code contents and installation defaults. Mutable links/hooks remain subject to resulting object coverage. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | 1 |
| C2.3 | Local archives, VCS URLs and package indexes selected by flags | CLOSED | Yes | Recheck positive package installation through shell-accessible built-in frontends at both authorities; record the whole installed package/dependency closure, including non-code contents and installation defaults. Mutable links/hooks remain subject to resulting object coverage. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | 1 |
| C2.4 | Editable pip installs, npm links, mutable source and dependency replacement | CLOSED | Yes | Recheck positive package installation through shell-accessible built-in frontends at both authorities; record the whole installed package/dependency closure, including non-code contents and installation defaults. Mutable links/hooks remain subject to resulting object coverage. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | 1 |
| C2.5 | Build backend, lifecycle script, npm run/start/test and dependency hook execution | CLOSED | Yes | Recheck positive package installation through shell-accessible built-in frontends at both authorities; record the whole installed package/dependency closure, including non-code contents and installation defaults. Mutable links/hooks remain subject to resulting object coverage. | S8.1-4, S8.2-7, S8.2-8, S8.2-16, S8.2-17, S8.3-7 | 1 |
| C2.6 | Native extensions and admitted module/.pth inputs; custom evaluator behavior in C7.08 | CLOSED | Yes | Determine package or derived-source coverage before demanding a separate native/module/cache line; preserve recorded native-extension execution and prevent uncovered code activation. | S8.2-6, S8.2-7, S8.2-9, S8.2-16 | 1 |
| C3.1 | Flatpak system install/update and graphical or D-Bus frontend | CLOSED | Yes | Application installer operations, including privileged calls and permission changes, must write/apply the declaration; record app/runtime packages and defaults, not just executable entries. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-17, S8.3-7 | 1 |
| C3.2 | Flatpak --user install, extra installation roots/remotes, local bundles | CLOSED | Yes | Application installer operations, including privileged calls and permission changes, must write/apply the declaration; record app/runtime packages and defaults, not just executable entries. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-17, S8.3-7 | 1 |
| C3.3 | Flatpak runtime/extension updates, override permissions, alternate commands and development mode | CLOSED | Yes | Application installer operations, including privileged calls and permission changes, must write/apply the declaration; record app/runtime packages and defaults, not just executable entries. | S8.1-4, S8.1-7, S8.2-7, S8.2-8, S8.2-17, S8.3-7 | 1 |
| C3.4 | AppImage directly executed and self-mounted via FUSE | CLOSED | Yes | Separate downloaded inert material from an installed application package and its retained contents; shell commands are not violations, while saved executable or updater-produced installed state requires coverage. | S8.1-6, S8.2-4, S8.2-7, S8.2-15, S8.3-7; Section 9.3 | 1 |
| C3.5 | AppImage extracted/mounted externally, AppDir launch or self-update | CLOSED | Yes | Separate downloaded inert material from an installed application package and its retained contents; shell commands are not violations, while saved executable or updater-produced installed state requires coverage. | S8.1-6, S8.2-4, S8.2-7, S8.2-15, S8.3-7; Section 9.3 | 1 |
| C4.1 | Download a native executable and chmod/run it | CLOSED | No | Saving then executing unrecorded file code remains the boundary. Repeat native/extracted/renamed file cases from a working command shell rather than count command-parser refusal. | S8.2-9, S8.2-10, S8.3-4, S8.3-6; Section 9.3 | 1 |
| C4.2 | Download and extract archive, including nested archives and renamed files | CLOSED | No | Saving then executing unrecorded file code remains the boundary. Repeat native/extracted/renamed file cases from a working command shell rather than count command-parser refusal. | S8.2-9, S8.2-10, S8.3-4, S8.3-6; Section 9.3 | 1 |
| C4.3 | Download by browser, curl, copier, sync client or application self-updater | CLOSED | Yes | A download can remain material; code activated from a saved file must be covered. A general program with an installer is declaration-writing in that part, including self-update when its documented role qualifies. | S8.1-5, S8.1-8, S8.2-15, S8.3-7; Section 9.3 | 1 |
| C4.4 | Downloaded script or library passed to existing interpreter/loader | CLOSED | No | A saved script/library executed through another program still requires coverage; permit ordinary shell use and the declared own-script positive case while testing the saved-file route. | S8.2-9, S8.2-10, S8.2-23; Section 9.3 | 1 |
| C4.5 | Stream download directly into interpreter or process substitution | CLOSED | Yes | Execute the separate unsaved download case and reboot; inspect that nothing executed is in force afterward, including saved files, jobs, autostarts and settings. Null stdin or refusal of all free commands is not this case. | S8.2-4, S8.2-5; Section 9.3 | 1 |
| C5.1 | Compile/link native program in home, then execute output | CLOSED | Yes | A system-built result may be covered by the recorded source/build line; do not require a distinct output line as a definition. Verify exact coverage before generated output or plugins can execute. | S8.2-9, S8.2-16; Section 9.3 | 1 |
| C5.2 | Build-system commands, configure probes, generators and test binaries | CLOSED | Yes | A system-built result may be covered by the recorded source/build line; do not require a distinct output line as a definition. Verify exact coverage before generated output or plugins can execute. | S8.2-9, S8.2-16; Section 9.3 | 1 |
| C5.3 | Install target copying to user prefix, changing PATH or creating symlinks | CLOSED | Yes | A typed install command is an action; classify its saved files, links and settings. When documented installation functionality is built-in, it must record/apply the change at both authorities. | S8.1-5, S8.1-8, S8.2-4, S8.3-7; Section 9.3 | 1 |
| C5.4 | Rebuild/replace an already recorded binary or library in place | CLOSED | No | Ordinary replacement of required recorded bytes still needs declaration application; direct superuser file mutation outside built-in tools is separately breaking. | S8.1-15, S8.1-16, S8.3-5, S8.3-6 | 1 |
| C5.5 | Compilers embedding plugins or build processes loading generated code | CLOSED | Yes | A system-built result may be covered by the recorded source/build line; do not require a distinct output line as a definition. Verify exact coverage before generated output or plugins can execute. | S8.2-9, S8.2-16; Section 9.3 | 1 |
| C6.1 | Persistent user units and drop-ins, aliases, template instances and symlinks | CLOSED | Yes | Registration or modification of jobs/settings is the channel, not command text. Demonstrate supported service/scheduler frontend writes and applies the declaration under ordinary and full superuser invocation. | S8.1-7, S8.2-4, S8.2-13, S8.3-7; Section 9.3 | 1 |
| C6.2 | Direct manager API/CLI start, enable, reload, set-property or link | CLOSED | Yes | Registration or modification of jobs/settings is the channel, not command text. Demonstrate supported service/scheduler frontend writes and applies the declaration under ordinary and full superuser invocation. | S8.1-7, S8.2-4, S8.2-13, S8.3-7; Section 9.3 | 1 |
| C6.3 | Transient service/scope/timer/path/socket created through systemd-run or D-Bus | CLOSED | Yes | Separate transient runtime processes/relationships from the program or setting creating them; service/timer registration remains a setting channel and built-in mutations require declaration writes. | S8.2-5, S8.2-13, S8.3-7; Section 9.3 | 1 |
| C6.4 | User cron entries, @reboot and crontab replacement | CLOSED | Yes | Registration or modification of jobs/settings is the channel, not command text. Demonstrate supported service/scheduler frontend writes and applies the declaration under ordinary and full superuser invocation. | S8.1-7, S8.2-4, S8.2-13, S8.3-7; Section 9.3 | 1 |
| C6.5 | Generated units, user environment generators and cron command text loading more code | NOT CLOSED | Yes | Stored executable generator/cron text and effective settings need coverage; system-generated outputs may follow a recorded generating line. A typed command is not the same as a saved cron command. | S8.2-4, S8.2-13, S8.2-16, S8.2-23; Section 9.3 | 2 |
| C6.6 | Removed unit reactivated by socket, timer, dependency, lingering manager or surviving child | CLOSED | No | Removed units must not reactivate uncovered services or code; continue cgroup/descendant and timer/socket tests under the new shell. Runtime activation edges follow their creating object. | S8.1-11, S8.2-5; Section 8.4 Removal | 3 |
| C7.01 | Script file passed as interpreter argument | CLOSED | No | Saved executable script requires coverage and the user must run a recorded own script from the shell; shellless fixed-protocol execution does not meet that ordinary-work condition. | S8.2-9, S8.2-10; Section 9.3 | 1 |
| C7.02 | Executable shebang script | CLOSED | No | Saved executable script requires coverage and the user must run a recorded own script from the shell; shellless fixed-protocol execution does not meet that ordinary-work condition. | S8.2-9, S8.2-10; Section 9.3 | 1 |
| C7.03 | Code supplied as -c or -e argument | CLOSED | Yes | Personally typed commands are actions, not declaration objects or bypass channels. Positive ordinary shell commands are required; assess the files, jobs and settings they leave. The old blanket command/PTY refusal is not closure. | S8.2-4; Section 9.3 | 1 |
| C7.04 | Code piped into stdin, FIFO, socket, here-document or process substitution | CLOSED | Yes | Distinguish typed here-document/pipeline commands, saved code delivered through a stream, and the unsaved download case. Judge resulting objects, with reboot absence for downloaded executed unsaved code. | S8.2-4, S8.2-5, S8.2-9; Section 9.3 | 1 |
| C7.05 | Code from regular file redirected to stdin or /proc/self/fd/N | CLOSED | No | Stored executable source/module code remains subject to coverage regardless of redirection, source, eval or import; repeat through working shell paths, including declared own-script execution. | S8.2-9, S8.2-10, S8.2-23; Section 9.3 | 1 |
| C7.06 | Interactive REPL with language statements | CLOSED | Yes | Personally typed commands are actions, not declaration objects or bypass channels. Positive ordinary shell commands are required; assess the files, jobs and settings they leave. The old blanket command/PTY refusal is not closure. | S8.2-4; Section 9.3 | 1 |
| C7.07 | Recorded script sources another file | CLOSED | No | Stored executable source/module code remains subject to coverage regardless of redirection, source, eval or import; repeat through working shell paths, including declared own-script execution. | S8.2-9, S8.2-10, S8.2-23; Section 9.3 | 1 |
| C7.08 | exec(open(file).read()), eval of read data, custom import loader | CLOSED | No | Stored executable source/module code remains subject to coverage regardless of redirection, source, eval or import; repeat through working shell paths, including declared own-script execution. | S8.2-9, S8.2-10, S8.2-23; Section 9.3 | 1 |
| C7.09 | Ordinary import, zipimport and non-regenerable bytecode; module path injection | CLOSED | No | Stored executable source/module code remains subject to coverage regardless of redirection, source, eval or import; repeat through working shell paths, including declared own-script execution. | S8.2-9, S8.2-10, S8.2-23; Section 9.3 | 1 |
| C7.10 | Embedded interpreter in editor, awk, make, debugger or database program | CLOSED | Yes | Distinguish typed actions from stored executable settings/code and distinguish embedded installer functionality. Removing all evaluator interfaces cannot stand in for positive ordinary shell work. | S8.1-5, S8.1-8, S8.2-4, S8.2-23; Section 9.3 | 1 |
| C7.11 | Helper process launch: find -exec, editor shell escape, make recipe child | CLOSED | Yes | A helper launch requested by a typed command is not itself a channel; launched stored program code and any setting in force still need coverage. Saved make recipes/editor code must be assessed as objects. | S8.2-4, S8.2-9, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C7.12 | Git hook program in writable project | CLOSED | No | Uncovered executable objects and injected code remain subject to the recorded-code boundary. Revalidate the specific hook/loader/mapping/injection route after ordinary shell admission; a typed command alone is not the failing object. | S8.2-4, S8.2-9, S8.3-4, S8.3-6; Section 9.3 | 1 |
| C7.13 | Direct dynamic loader invocation | CLOSED | No | Uncovered executable objects and injected code remain subject to the recorded-code boundary. Revalidate the specific hook/loader/mapping/injection route after ordinary shell admission; a typed command alone is not the failing object. | S8.2-4, S8.2-9, S8.3-4, S8.3-6; Section 9.3 | 1 |
| C7.14 | LD_PRELOAD, LD_AUDIT, dlopen/FFI and alternate library path | CLOSED | No | Uncovered executable objects and injected code remain subject to the recorded-code boundary. Revalidate the specific hook/loader/mapping/injection route after ordinary shell admission; a typed command alone is not the failing object. | S8.2-4, S8.2-9, S8.3-4, S8.3-6; Section 9.3 | 1 |
| C7.15 | Native executable memfd, fexecve/execveat of memory file | CLOSED | Yes | Runtime-only memory state follows its creating program or setting, not a separate memory-byte line. Assess any saved source/payload and access setting separately; personally typed actions are not objects. Exercise the unsaved-execution/reboot condition when that case applies. | S8.2-4, S8.2-5, S8.2-9, S8.2-10, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C7.16 | Anonymous machine code, JIT, writable/executable aliases | CLOSED | Yes | Runtime-only memory state follows its creating program or setting, not a separate memory-byte line. Assess any saved source/payload and access setting separately; personally typed actions are not objects. Exercise the unsaved-execution/reboot condition when that case applies. | S8.2-4, S8.2-5, S8.2-9, S8.2-10, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C7.17 | Shell command line, including invocation of a declared program | CLOSED | Yes | Personally typed commands are actions, not declaration objects or bypass channels. Positive ordinary shell commands are required; assess the files, jobs and settings they leave. The old blanket command/PTY refusal is not closure. | S8.2-4; Section 9.3 | 1 |
| C7.18 | Regenerable executable bytecode/JIT cache with same-rights execution | CLOSED | Yes | Apply ordered package/code questions before program-record classification; executable cache derived by the system from a recorded source can be covered by that source line. No blanket cache exemption or mandatory separate line is inferred. | S8.2-6, S8.2-7, S8.2-9, S8.2-15, S8.2-16 | 2 |
| C7.19 | Browser web code and JIT confined inside recorded renderer/helper programs | CLOSED | Yes | The exemption is inability of internal code to launch programs or change installed objects/settings, subject to question order. Passive browsing may remain an implementation choice; JavaScript removal is not the definition. | S8.2-6, S8.2-21 | 2 |
| C7.20 | Code-bearing serialized input (pickle, macro-bearing document) | CLOSED | No | Stored serialized inputs executed as code remain code; literal document values need no code line unless an earlier package or setting question applies. Verify the actual consumer behavior. | S8.2-6, S8.2-9, S8.2-15, S8.2-23 | 1 |
| C7.21 | WASI module with a preopened host directory and partial runtime rights | CLOSED | Yes | Use the new capability condition: can the module itself launch programs or change installed objects/settings? A preopened directory alone does not answer that; missing rights facts are FACT_UNKNOWN. Preserve question order. | S8.2-6, S8.2-21 | 2 |
| C7.22 | Debugger/interpreter writing another process memory or injecting code | CLOSED | Yes | Runtime-only memory state follows its creating program or setting, not a separate memory-byte line. Assess any saved source/payload and access setting separately; personally typed actions are not objects. Exercise the unsaved-execution/reboot condition when that case applies. | S8.2-4, S8.2-5, S8.2-9, S8.2-10, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C7.23 | binfmt_misc handlers and user-mode foreign-binary interpreters | CLOSED | Yes | Establish whether the installed handlers can execute the foreign code on this computer; unsupported code is not automatically a program. Handler registration is a setting and built-in changes record/apply. | S8.2-9, S8.2-13, S8.2-20, S8.3-7 | 1 |
| C7.24 | Recorded custom dispatcher: file-open route and non-file instruction input without eval/import | CLOSED | Yes | Differentiate personally typed commands from a stored instruction object; assess code-execution capability and the internal-code exception literally. Immutable-input isolation may remain, but cannot eliminate the required shell. | S8.2-4, S8.2-9, S8.2-21, S8.2-23; Section 9.3 | 1 |
| C7.25 | Runtime-selected TCP listening port (also C2/C3/C5/C9.2) | CLOSED | Yes | An open port is not a separate required object; it follows its creating program or setting. Remove the inference that every selected runtime port requires its own line; inspect network/access settings in force. | S8.2-5, S8.2-13 | 2 |
| C8.01 | Shell startup profiles and rc files | CLOSED | No | Saved executable startup objects remain covered or unable to execute. Test actual shell startup and environment selection; shellless login ignoring all files is no longer adequate evidence. | S8.2-9, S8.2-23; Section 9.3 | 1 |
| C8.02 | Environment-selected startup code, BASH_ENV/ENV/PYTHONSTARTUP | CLOSED | No | Saved executable startup objects remain covered or unable to execute. Test actual shell startup and environment selection; shellless login ignoring all files is no longer adequate evidence. | S8.2-9, S8.2-23; Section 9.3 | 1 |
| C8.03 | Environment-imported shell functions and command substitutions | CLOSED | Yes | Personally typed functions, substitutions or commands are actions; saved startup/executable configuration remains an object. Judge the effects left behind and launch-granting saved settings, not blanket refusal of shell syntax. | S8.2-4, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C8.04 | Editor executable configuration, plugins, modelines executing code | CLOSED | Yes | Stored executable settings remain code; values that launch or grant access are settings. Embedded installer functionality must write/apply declaration changes even under root. | S8.1-5, S8.2-14, S8.2-23, S8.3-7 | 1 |
| C8.05 | Project-local executable settings: Git !alias, external filter, build recipe | CLOSED | Yes | Stored executable settings remain code; values that launch or grant access are settings. Embedded installer functionality must write/apply declaration changes even under root. | S8.1-5, S8.2-14, S8.2-23, S8.3-7 | 1 |
| C8.06 | Runtime own-rights code definitions: shell functions, aliases, editor commands | CLOSED | Yes | Personally typed functions, substitutions or commands are actions; saved startup/executable configuration remains an object. Judge the effects left behind and launch-granting saved settings, not blanket refusal of shell syntax. | S8.2-4, S8.2-14, S8.2-23; Section 9.3 | 1 |
| C8.07 | Browser extension executing with browser-equivalent rights | CLOSED | Yes | An installed extension is covered by the package question before any confinement exception; its built-in installer writes/applies declaration changes. Do not inherit the old rights-only rationale. | S8.1-5, S8.2-6, S8.2-7, S8.2-8, S8.2-21, S8.3-7 | 1 |
| C8.08 | Settings only read as values, such as theme or home page | CLOSED | Yes | Check package/default provenance first. Personal values-only preferences that neither launch nor grant access are program records; system-wide or launch/access values are settings. | S8.2-6, S8.2-7, S8.2-11, S8.2-14, S8.2-17 | 2 |
| C9.1 | Rootful image pull/run, mutable tags and manager API | CLOSED | Yes | Record installed image/package contents, own-process container programs and settings, not only an executable entry. Supported container installer/configuration calls write/apply at both authorities; runtime namespaces are not separate objects. | S8.2-5, S8.2-7, S8.2-8, S8.2-22, S8.3-7 | 1 |
| C9.2 | Rootless containers, user namespaces, alternative OCI runtime invocation | CLOSED | Yes | Record installed image/package contents, own-process container programs and settings, not only an executable entry. Supported container installer/configuration calls write/apply at both authorities; runtime namespaces are not separate objects. | S8.2-5, S8.2-7, S8.2-8, S8.2-22, S8.3-7 | 1 |
| C9.3 | Bind-mounted executable/script, writable overlay, exec into container and package install inside | CLOSED | Yes | Record installed image/package contents, own-process container programs and settings, not only an executable entry. Supported container installer/configuration calls write/apply at both authorities; runtime namespaces are not separate objects. | S8.2-5, S8.2-7, S8.2-8, S8.2-22, S8.3-7 | 1 |
| C9.4 | Image build RUN/hooks, import/load archive and commit modified container | CLOSED | Yes | Record installed image/package contents, own-process container programs and settings, not only an executable entry. Supported container installer/configuration calls write/apply at both authorities; runtime namespaces are not separate objects. | S8.2-5, S8.2-7, S8.2-8, S8.2-22, S8.3-7 | 1 |
| C9.5 | Privileged/host-namespace/device/runtime-hook options | CLOSED | Yes | Record installed image/package contents, own-process container programs and settings, not only an executable entry. Supported container installer/configuration calls write/apply at both authorities; runtime namespaces are not separate objects. | S8.2-5, S8.2-7, S8.2-8, S8.2-22, S8.3-7 | 1 |
| C9.6 | Removed image/container restarted through old name, daemon state, API or retained layers | CLOSED | Yes | Removal must account for remaining installed image/package content as well as live descendants and executable authority; establish whether retained archive bytes are material before calling them exempt. | S8.1-9, S8.2-7, S8.2-15, S8.2-22; Section 8.4 Removal | 3 |
| C10.1 | Documented privileged package/service/account/network/firewall administration | CLOSED | Yes | Test actual superuser invocations of built-in tools: changing guards/rights through those tools must record/apply. A limited sudo grant or inaccessible backend alone is insufficient. Direct root mutation outside them is breaking and is not required to be blocked. | S8.1-7, S8.1-8, S8.1-15, S8.1-16, S8.3-7 | 1 |
| C10.2 | Built-in privileged tool changes guards, permissions, mounts or execution policy | CLOSED | Yes | Test actual superuser invocations of built-in tools: changing guards/rights through those tools must record/apply. A limited sudo grant or inaccessible backend alone is insufficient. Direct root mutation outside them is breaking and is not required to be blocked. | S8.1-7, S8.1-8, S8.1-15, S8.1-16, S8.3-7 | 1 |
| C10.3 | Retained arbitrary privileged hooks and multi-resource live side effects | NOT CLOSED | Yes | Effects of supported installation hooks still belong to built-in transactions, including root; distinguish direct superuser bypass outside the built-in tools. Multi-resource/device readback and restoration remain unproved. | S8.1-15, S8.1-16, S8.3-4, S8.3-5, S8.3-7 | 3 |
| C10.4 | Root editor with documented package installer | NOT CLOSED | Yes | The embedded installer part is explicitly an installer, even in a general-purpose editor. Demonstrate its declaration-writing behavior under root; direct root editing outside that part is breaking. The old role ambiguity is not carried as a decision. | S8.1-5, S8.1-8, S8.1-15, S8.3-7 | 1 |
| M1.01 | All C1–C10: successful inactive preparation versus actual application report | CLOSED | No | Keep last-success declaration and complete required-state readback/replay. Revalidate over the expanded v4 object set and shell/frontend surfaces; historical finite evidence does not close unobserved device effects. | S8.1-13, S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M1.02 | All C1–C10: complete live activation and success report across all objects | NOT CLOSED | No | Keep last-success declaration and complete required-state readback/replay. Revalidate over the expanded v4 object set and shell/frontend surfaces; historical finite evidence does not close unobserved device effects. | S8.1-13, S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M2.01 | All C1–C10: durable exact file generation and boot selection after report | CLOSED | No | Keep last-success declaration and complete required-state readback/replay. Revalidate over the expanded v4 object set and shell/frontend surfaces; historical finite evidence does not close unobserved device effects. | S8.1-13, S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M2.02 | All C1–C10: add/change/remove power cut with complete runtime/device replay | NOT CLOSED | No | Keep last-success declaration and complete required-state readback/replay. Revalidate over the expanded v4 object set and shell/frontend surfaces; historical finite evidence does not close unobserved device effects. | S8.1-13, S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M3.01 | All C1–C10: explicit failure or timeout while only inert preparation changed | CLOSED | No | Keep last-success declaration and complete required-state readback/replay. Revalidate over the expanded v4 object set and shell/frontend surfaces; historical finite evidence does not close unobserved device effects. | S8.1-13, S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M3.02 | All C1–C10: partial activation failure, stalled worker, or no report at one hour | NOT CLOSED | Yes | Recovery remains a carried engineering obligation. The explicit one-hour deadline is historical implementation/test policy, not a v4 sentence; evaluate P1/P2 against the last successful declaration and do not invent a deadline rule. | S8.1-14, S8.3-1, S8.3-4, S8.3-5; Appendix A.4.3 | 3 |
| M4.01 | All C1–C10: running code, descendants, open FDs and mapped/injected copies | CLOSED | No | Continue revoking uncovered programs, holders, activators and effective rules; runtime processes/edges are evidence about creating programs/settings rather than separately required objects. | S8.1-9, S8.1-11, S8.2-5; Section 8.4 Removal | 3 |
| M4.02 | All C1–C10: executable aliases, copied cache/store/image content, old generations | CLOSED | Yes | Track full installed package/default/derived contributions and residual source/package coverage. Inertness alone is insufficient for an installed object; sharing is allowed when remaining lines actually cover it. | S8.1-9, S8.2-7, S8.2-16, S8.2-17; Section 8.4 Removal | 3 |
| M4.03 | All C1–C10: service activators, timers, restart policy and effective rules | CLOSED | No | Continue revoking uncovered programs, holders, activators and effective rules; runtime processes/edges are evidence about creating programs/settings rather than separately required objects. | S8.1-9, S8.1-11, S8.2-5; Section 8.4 Removal | 3 |
| M4.04 | All C1–C10: contributions shared with remaining declaration lines | CLOSED | Yes | Track full installed package/default/derived contributions and residual source/package coverage. Inertness alone is insufficient for an installed object; sharing is allowed when remaining lines actually cover it. | S8.1-9, S8.2-7, S8.2-16, S8.2-17; Section 8.4 Removal | 3 |
| M5.01 | All C1–C10: finite typed lines, exact content, permissions and documented defaults | NOT CLOSED | Yes | Inventory packages with and without code/files, unchanged package defaults, changed settings, code and provenance before assigning coverage. Classify records/material separately and runtime observations through their creating objects; missing provenance is FACT_UNKNOWN. | S8.2-1, S8.2-5, S8.2-6, S8.2-7, S8.2-8, S8.2-15, S8.2-16, S8.2-17 | 2 |
| M5.02 | All C1–C10: unrestricted algorithmic requirements and semantic effects | NOT CLOSED | Yes | External list sources are explicitly recordable and exempted from the corresponding reproducibility claim. Unrestricted semantic validation is still unimplemented; finite JSON is a design choice, not a new admissibility law or a claimed universal impossibility. | S8.2-18; Sections 8.4 and 8.5 | 2 |

## Exact sentence ledger

These are all 47 exact sentences from [SENTENCES](../SENTENCES.md), in their original order. They also supply the quotations for sentence-ID references in STAND and ROUNDS. Section references outside 8.1–8.3 have no sentence IDs in that file and are quoted separately below; no identifiers are invented.

- **S8.1-1** **Declaration**—a text recording what the computer should be like: what is installed on it and how it is configured.

- **S8.1-2** The computer is brought into conformity with this text, rather than the text being compiled from the computer.

- **S8.1-3** The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.

- **S8.1-4** **Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.

- **S8.1-5** A general-purpose program with a built-in installer counts as an installer in that part of its functionality.

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.1-7** **Built-in tool**—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.

- **S8.1-8** General-purpose programs—an editor, file copying, link creation, the command shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.

- **S8.1-9** **In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.

- **S8.1-10** A setting is in force if it has its value.

- **S8.1-11** A service is in force if it is enabled; an account, if it exists.

- **S8.1-12** The required state of a recorded object is stated by its line.

- **S8.1-13** **Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.

- **S8.1-14** The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].

- **S8.1-15** **Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.

- **S8.1-16** Breaking is a violation on the person’s part rather than a property of the system, and it refutes no property.

- **S8.2-1** Everything that is installed and every setting must be recorded.

- **S8.2-2** The rest need not be recorded.

- **S8.2-3** The rule applies to objects that are on the computer.

- **S8.2-4** A command that a person typed himself or herself is that person’s action, not an object.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-18** A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.

- **S8.2-19** What need not be recorded may also be recorded in the declaration.

- **S8.2-20** A file containing code that cannot be executed on this computer is not a program.

- **S8.2-21** Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.

- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

- **S8.3-1** The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.

- **S8.3-2** They admit no degrees: a system either has all three properties or it does not.

- **S8.3-3** The numbers are kept from earlier versions.

- **S8.3-4** **P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.

- **S8.3-5** **P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.

- **S8.3-6** **P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.

- **S8.3-7** Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.

- **S8.3-8** What is installed and settings can be changed past the declaration only by breaking.

### Additional exact passages

Section 9.3:

> The testbed has a command shell. A command typed by a person is not considered a channel for bypassing the declaration. A channel is
> anything that such a command tries to leave behind: saving and running a file, registering a service, a timer or an
> autostart, changing a setting. A separate case: a command downloads and executes code without saving it; after
> a reboot, nothing that was executed must be in force.

> The list of ordinary work is extended to include running ordinary commands and one’s own script, recorded in the declaration,
> in the command shell.

Section 8.4:

> **Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is
> in force unless it is recorded in the remaining lines.

> **Reproducibility.** The same declaration on another computer yields exactly the result described in it,
> provided the description is unambiguous. For a line that takes a list from outside the declaration, reproducibility is not claimed.
> Differences explained by hardware are excluded.

Section 8.5:

> The form of the declaration: it may be a list or an algorithm.

Appendix A.4.1:

> A failure of the testbed yields 0 only if a written argument shows that it follows from the definitions alone, so
> that any system having the property would fail the same case; a separate review checks the argument. Otherwise it
> is a defect of the testbed, and the case yields ?.

Appendix A.4.3:

> Built-in tools are also checked with superuser
> privileges.

> Ordinary work: installing a program, updating the system, connecting to a Wi-Fi network, pairing a Bluetooth device,
> working in a browser, editing documents. Actions with Wi-Fi and Bluetooth are performed on real hardware: an adapter
> is passed to the virtual machine, or a separate computer is used.

> After each completed application, every line of the declaration is compared with the state it requires. The power
> cut right after the success report is repeated three times for each kind of application: adding, changing, and
> removing a line.

Appendix A.4.4:

> **Procedure.** The same declaration, all of whose lines are unambiguous, is applied to two independent clean
> installations of the check 2 testbed on different virtual machines.

## Limits and unresolved facts

For C7.21, a preopened host directory does not establish all runtime rights; the exact executable capabilities and effects must be known before applying S8.2-21. For package archives retained after removal, establish whether they remain installed objects or are merely downloaded material; do not infer provenance from a path, name or denied launch. The rule order in S8.2-6 applies before the internal-code clarification. These are missing-fact boundaries, not invented gaps.

C10.4 now has an explicit functionality distinction in S8.1-5 and S8.1-8. C7.18 now has explicit ordered classification and derived-source coverage. This report does not carry the previous text-open labels as conclusions about version 4, nor infer broader answers than the cited sentences give. M5.02 remains an implementation and validation limit; permitting algorithmic declarations does not require this prototype to implement an unrestricted language, and finite successful readers do not establish unrestricted semantics.

The preserved one-hour recovery deadline comes from the prior testbed and its earlier requirements. Sections 8–9 and the incorporated Appendix A.4.3 do not prescribe that duration. It may remain a documented engineering/self-test bound; it must not be used as an additional hypothesis failure condition.
