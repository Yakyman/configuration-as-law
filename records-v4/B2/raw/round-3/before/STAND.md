STAND: partial

Round 2, recorded 2026-11-23 UTC. The testbed has an ordinary Bash command shell, inherited native execution/mapping policy, declaration-writing configuration and editor-installer frontends, and ordered object coverage with finite installer provenance. **2 CLOSED / 86 NOT CLOSED after the rebuilt full run and [independent review](../../round-2/REVIEW-FINAL.md).** Historical version 3 closures do not transfer into version 4. Overall hypothesis outcome: `?`.

Round 2 completed at 14:38:29 UTC after two independent scratch builds and the complete fresh-machine suite. All nine Round 2 variants remain **NOT CLOSED**: three concrete new boundary failures are retained, and finite supported examples do not establish general coverage. The [Round 2 evidence map](../../round-2/COVERAGE.md) records each owner. The [Round 1 report](../../../BUILD-1.md) remains the historical source of the two closures, preserved by the new run.

## Implementation and evidence boundary

The complete recipe is in [build/](../../../build); the retained server image is `VMs/cal-1123/stand/base/stand.qcow2`, relative to the server account's initial directory. Historical Round 1 build evidence is under `raw/round-1/`; completed Round 2 evidence, offline audit and independent review are under `raw/round-2/`. Heavy work runs in disposable server guests under the shared slot locks. See the final build report, SELFTEST and HOWTO for exact identities, commands and cleanup.

The ordinary login runs `/usr/bin/bash` through `stand-shell`, with free commands, quoting, arguments, pipelines, redirections and runtime functions. Documents remain writable without mandatory declaration lines. An exact recorded personal Bash script accepts ordinary arguments. The old tab-separated `stand-session` launcher remains an explicit compatibility tool, not the login interface. Old refusal evidence is not free-shell evidence.

The policy reuses AppArmor, exact declared native paths/mappings, Unix ownership and existing authorization. Shell descendants inherit the domain. Saved native copies and native mapping attempts are tested separately from interpreted input. The shell can still evaluate saved unrecorded script/module/serialized inputs: these are actual boundary failures, not new exemptions or definition-only impossibility claims. A genuine HTTP response is executed from a pipe without saving it; the observed runtime process disappears after reboot. That finite case does not prove every possible effect of unsaved execution.

Application holds the existing exclusive writer lock, closes new shell admission and pauses existing shell-domain tasks before realizing changes. The kernel cgroup v2 freezer pauses tasks without job-control stop signals. Original and temporary child cgroups are journaled before migration and restored after application. Only a durable successful application or verified recovery resumes them; pending recovery also blocks new entry after supervisor loss. A heartbeat/concurrent-entry self-test checks the barrier. This integration change makes no closure claim for the later round's general lifecycle families. The current migration implementation supports normal cgroups, refuses threaded source groups, and checks process identity around the numeric cgroup API. Those checks do not make PID lookup/migration atomic; this remains a stated concurrency limit.

Public typed account/group, service/timer/socket, rule and saved radio-profile tools add/remove exact rows through the common broker under both ordinary Bash and actual root execution. Exact package reinstall/downgrade aliases use the same application path. `v4-editor` edits documents and exposes documented package-install/package-remove functionality using that broker. Direct root general editing remains permitted breaking. In contrast, the canonical native root account tool still bypasses the declaration; it is a built-in-tool failure, not breaking.

## Reading choices and limits

S8.2-4 says: “A command that a person typed himself or herself is that person’s action, not an object.” The implementation does not log commands as declaration lines. S8.1-5 says: “A general-purpose program with a built-in installer counts as an installer in that part of its functionality.” The editor's installer therefore applies a declaration even as root, while its general document operation keeps the caller's identity. S8.3-7 says: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.” This includes canonical backends; calling their bypass breaking would add an exemption the text does not contain.

The stricter engineering reading used here keeps coverage attached to saved executable input after a read, pipe, source, import or custom dispatch; an interpreter's line alone cannot cover arbitrary saved input. It permits ordinary typed instructions and material writes and adds no mandatory line for transient memory. This is an attempted boundary, with failures retained, not an author decision resolving an ambiguity. No textual gap or new hypothesis rule is claimed. Unsupported finite tool syntax is an implementation limit, not a requirement imposed on ordinary work by the paper.

## Round 2 object coverage: implementation and limits

The v4 entry is `stand-inventory --v4`. [inventory.py](../../../build/inventory.py) snapshots the filesystem, native installed-package database, accounts, groups, enabled system units, one native setting and runtime observations before loading the declaration or enumerating its claims. Native enumeration includes all installed package identities, including packages without executable files; it does not establish why a package was installed. Finite dependency registrations are observed separately in the stand installer ledger. [object_rules.py](../../../build/object_rules.py) then applies the questions in order. S8.2-6 says: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.” Unknown earlier facts prevent a later convenient classification; a path, signature, dependency name or interpreter line supplies no missing semantic fact.

The separate installation ledger `/var/lib/stand/objects.json`, written during activation, records this installer's exact package artifacts, defaults, dependency identities and derivation edges. [recorded_objects.py](../../../build/recorded_objects.py) reads actual state independently of the current declaration and matches surviving origins to current exact requirements. Coverage names the owning line and `own`, `package` or `derived` relation; file bytes, mode, owner/group and symlink target must match. An enabled generated unit keeps its own setting line and an exact source edge. Supported derivations are byte copying and the finite Python bytecode procedure; unsupported algorithms are refused, not implemented by that refusal.

Native package identity and installed status are observed through `dpkg-query`; the native file list establishes membership only. A captured factory file is not proof that it remains as originally received: local changes may predate capture, and native metadata does not establish every original permission or symlink target. Native receipt therefore remains `FACT_UNKNOWN`. This installer's exact registered artifacts supply only its finite receipt coverage. Removing a current owning line cannot manufacture a remaining claim from stale provenance; native package disappearance also removes its membership basis. The [final object evidence](../../round-2/final-1/objects.jsonl) and five exported censuses test these mechanisms and retain their failures; they do not establish complete census or prevention.

The conservative engineering interpretation demands positive facts for each applicable earlier question and for the containment clarification; missing facts remain `FACT_UNKNOWN` and never count as covered. S8.2-17 says: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.” The ledger distinguishes a package default from a subsequently chosen setting; the finite added native chosen-value reader is `kernel.printk`. Generic semantic setting discovery is not implemented. After earlier questions fail, a personal program's values-only configuration that neither launches anything nor grants access is a program record under S8.2-14, even if a person wrote it. Material and program records need no additional line. This reading does not prohibit ordinary document work or create a rule requiring all writable files to be declared.

Processes, ports and mounts are diagnostic observations, not separate mandatory declaration objects. A process executable can be linked by its actual hash to a recorded creator; missing listener or mount creator provenance stays explicitly unknown. A socket holder alone would not prove its creator. Optional runtime requirements retained in the finite declaration remain subject to their stated readback requirements. No absence of a browser/WASI runtime, or pure rule fixture with assumed capabilities, proves containment on a real machine. The [fixed rule fixtures](../../../build/v4-rules-selftest.py) exercise decisions from stated facts; machine evidence must establish those facts separately.

The legacy inventory remains available for carried diagnostics and historical tests. Its old statuses do not replace the v4 criterion. The final rebuild, full machine suite, exact [evidence map](../../round-2/COVERAGE.md) and [saved-evidence audit](../../round-2/audit-final-1.json) are complete; none of the nine owning variants meets the closure criterion.

## Declaration format and complete example

The designated declaration in the guest is a directory selected by `/var/lib/stand/current`: `machine.jsonl` contains one JSON object per line, with unique `id` and a supported `type`. File requirements are inline or refer to a checked manifest in the same directory; the referring line states its digest. The factory uses `base-files.json`, while the complete combined example embeds the complete captured base-file requirements inline. A generation hash covers sorted filenames and exact bytes. `/var/lib/stand/last-success.json` identifies the last application reported successful. This format is a prototype choice, not a restriction added to §8.5.

The current complete replayable exports are in (not published: record outside selected evidence) and (not published: record outside selected evidence); their provenance records exact source exports and hashes. Earlier Round 0 and Round 1 examples remain unchanged as historical evidence. Additional channel rows alone are not a complete declaration. The factory has 553 rows (434 package rows and 31,261 base-file requirements); the combined declaration has 578 rows, adding six exact object/unit rows to the carried assembly. All combined rows verified before and after reboot on both independently rebuilt images and compared equal. Exact identities are in SELFTEST.

| Type/field | Required state and schema limits |
|---|---|
| `base`, `program`, `code` | `id`, `version`, `source`, exact `files` or checked `files_manifest`; regular-file SHA-256, numeric mode, uid/gid, or symlink target. Managed bytes include `content_b64`; checksum mismatch refuses before activation. Ordinary managed paths are under `/opt/stand/pkgs/`; only the trusted base-update catalog can replace its exact root paths. Factory package rows are internally named `type: program`, including packages with no executable content; the label is not a v4 classification. |
| `package_identity`, `package_dependencies`, `default_settings` | Exact finite `stand` package registrations and dependency identities; `default_settings` names received package file paths. Native identities use `dpkg` name/version/architecture/status, independently read. Native file receipt remains unknown without delivery evidence. |
| `derivations`, `derived_from` | Exact source/output relation for `copy` or target-interpreter `python-bytecode`; generated unit content uses a named source line and copy algorithm. Settings still need own rows except proven package defaults. |
| `setting` | Finite native reader `sysctl`, name `kernel.printk`, four canonical single-digit values. Apply writes the kernel interface; observe reads it. Unsupported names/algorithms refuse. Removal keeps residual provenance and does not infer a restore value. |
| `entrypoints` | Explicit file and optional interpreter paths; sealed launch policy fixes hashes and inputs; ordinary Bash uses the explicitly recorded script/interpreter and accepts arguments. An interpreter line alone does not cover arbitrary stored input code. |
| `account` | Name, numeric uid/gid, sorted groups, shell, home and GECOS; managed uid 1100–60000; numeric-ID replacement refuses. Password content is not in this tuple. |
| `group` | Independent managed group name, numeric GID 1100–60000, and empty `members`; conflicting account/group ownership refuses. Account primary groups retain their existing account coverage. |
| `service`, `timer`, `socket` | Unit name, enabled-state string, unit SHA-256, optional required active state; managed unit text inline, `stand-*` names and a finite safe directive grammar. Shared identical claims are supported; conflicting ones refuse. User jobs use protected system units whose workload drops to the ordinary identity. |
| `rule` | Exact supported backend requirement: nftables expression/chain, mount flags, backend ownership/modes or code-boundary policy. Managed rules accept only `tcp`/`udp dport PORT accept/drop`. |
| `privilege`, `login-key`, `password-login` | Exact file text/path/ownership/mode for recorded privilege and login-key state; password login supports only `allowed:false`, checked against effective SSH settings. Keys here are synthetic laboratory public login authorizations. Private access keys are not published. |
| `port` | Protocol, numeric port, local endpoint and listening requirement. This is a carried observation type; v4 does not require a separate line for the runtime port itself. Optional recorded requirements still incur P2. |
| `wifi`, `bluetooth` | Exact saved/connected Wi-Fi profile or prepared/paired Bluetooth state. Current examples use saved open Wi-Fi and prepared, unpaired Bluetooth. These are not evidence of actual connection/pairing on hardware. |
| `boot` | Fixed VM disk boot, `guest_can_change:false`; no general firmware reader or changer is supplied. |

For example, this complete additional rule line has no omitted fields:

```json
{"id":"dev-rule","type":"rule","managed":true,"expression":"tcp dport 17777 drop"}
```

Its implementation defaults are nftables family `inet`, table `stand`, chain `input`, filter type, input hook, priority 0 and accept policy; the ID is the rule comment. It must be included in a complete candidate declaration, not applied as a one-line replacement for the machine. Unsupported firewall expressions refuse. Other firewall tables are not thereby proved absent. Exact schema/default behavior is in [stand.py](../../../build/stand.py) and [guard.py](../../../build/guard.py); the finite Round 2 package-default provenance mechanism, completed validation and limits are described above.

## Variant table

Previous is historical version 3 evidence only. Current rows become CLOSED only after a concrete mechanism, failed bypass attempt and separate evidence review. C5.4 and C10.4 meet those conditions; the other 86 remain NOT CLOSED. Round 1 owns 65 rows. This Round 2 update addresses only C1.3, C6.5, C7.18, C7.19, C7.21, C7.25, C8.08, M5.01 and M5.02; their final validation is complete without new closure. Other rows retain their existing status and evidence. See the [Round 1 per-variant evidence map](../../round-1/COVERAGE.md) for its attempts and the [Round 2 map](../../round-2/COVERAGE.md) for this round.

| ID | Variant | Previous | Current | Owning round | Evidence |
|---|---|---|---|---|---|
| C1.1 | Repository install, upgrade, downgrade, reinstall and remove through CLI | NOT CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C1.2 | Direct low-level manager or library/API/GUI frontend bypassing CLI wrapper | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C1.3 | Alternate root, alternate database, package extraction into writable directory | NOT CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): exact registered-artifact provenance; actual alternate-root/database native installation and extracted code both bypass declaration coverage |
| C1.4 | Maintainer scripts, triggers, hooks and post-install service activation | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C1.5 | Hook disable/config override, backend flag or environment bypass | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C1.6 | Old generations, package cache copies, rollback paths after removal | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| C2.1 | pip system, --user, virtualenv, --target/--prefix installs | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C2.2 | npm local, global, prefix/workspace installs and executable links | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C2.3 | Local archives, VCS URLs and package indexes selected by flags | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C2.4 | Editable pip installs, npm links, mutable source and dependency replacement | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C2.5 | Build backend, lifecycle script, npm run/start/test and dependency hook execution | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C2.6 | Native extensions and admitted module/.pth inputs; custom evaluator behavior in C7.08 | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C3.1 | Flatpak system install/update and graphical or D-Bus frontend | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C3.2 | Flatpak --user install, extra installation roots/remotes, local bundles | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C3.3 | Flatpak runtime/extension updates, override permissions, alternate commands and development mode | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C3.4 | AppImage directly executed and self-mounted via FUSE | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C3.5 | AppImage extracted/mounted externally, AppDir launch or self-update | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C4.1 | Download a native executable and chmod/run it | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C4.2 | Download and extract archive, including nested archives and renamed files | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C4.3 | Download by browser, curl, copier, sync client or application self-updater | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C4.4 | Downloaded script or library passed to existing interpreter/loader | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C4.5 | Stream download directly into interpreter or process substitution | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C5.1 | Compile/link native program in home, then execute output | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C5.2 | Build-system commands, configure probes, generators and test binaries | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C5.3 | Install target copying to user prefix, changing PATH or creating symlinks | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C5.4 | Rebuild/replace an already recorded binary or library in place | CLOSED | CLOSED | 1 | Per-variant evidence map |
| C5.5 | Compilers embedding plugins or build processes loading generated code | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C6.1 | Persistent user units and drop-ins, aliases, template instances and symlinks | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C6.2 | Direct manager API/CLI start, enable, reload, set-property or link | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C6.3 | Transient service/scope/timer/path/socket created through systemd-run or D-Bus | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C6.4 | User cron entries, @reboot and crontab replacement | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C6.5 | Generated units, user environment generators and cron command text loading more code | NOT CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): exact copied-unit source edge and own setting line pass readback; supplied manager refusal does not establish general generator or cron-loaded-code coverage |
| C6.6 | Removed unit reactivated by socket, timer, dependency, lingering manager or surviving child | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| C7.01 | Script file passed as interpreter argument | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.02 | Executable shebang script | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.03 | Code supplied as -c or -e argument | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.04 | Code piped into stdin, FIFO, socket, here-document or process substitution | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.05 | Code from regular file redirected to stdin or /proc/self/fd/N | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.06 | Interactive REPL with language statements | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.07 | Recorded script sources another file | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.08 | exec(open(file).read()), eval of read data, custom import loader | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.09 | Ordinary import, zipimport and non-regenerable bytecode; module path injection | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.10 | Embedded interpreter in editor, awk, make, debugger or database program | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.11 | Helper process launch: find -exec, editor shell escape, make recipe child | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.12 | Git hook program in writable project | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.13 | Direct dynamic loader invocation | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.14 | LD_PRELOAD, LD_AUDIT, dlopen/FFI and alternate library path | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.15 | Native executable memfd, fexecve/execveat of memory file | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.16 | Anonymous machine code, JIT, writable/executable aliases | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.17 | Shell command line, including invocation of a declared program | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.18 | Regenerable executable bytecode/JIT cache with same-rights execution | CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): recorded source-bound Python bytecode executes and false derivation refuses; actual unrecorded bytecode also executes |
| C7.19 | Browser web code and JIT confined inside recorded renderer/helper programs | CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): ordered containment rules require actual capabilities; executable browser renderer/helper containment is UNTESTED |
| C7.20 | Code-bearing serialized input (pickle, macro-bearing document) | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.21 | WASI module with a preopened host directory and partial runtime rights | CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): partial rights do not establish containment; actual WASI capabilities are UNTESTED |
| C7.22 | Debugger/interpreter writing another process memory or injecting code | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.23 | binfmt_misc handlers and user-mode foreign-binary interpreters | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.24 | Recorded custom dispatcher: file-open route and non-file instruction input without eval/import | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C7.25 | Runtime-selected TCP listening port (also C2/C3/C5/C9.2) | CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): actual runtime listener is diagnostic with no separate mandatory port line; creator provenance remains unknown |
| C8.01 | Shell startup profiles and rc files | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.02 | Environment-selected startup code, BASH_ENV/ENV/PYTHONSTARTUP | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.03 | Environment-imported shell functions and command substitutions | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.04 | Editor executable configuration, plugins, modelines executing code | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.05 | Project-local executable settings: Git !alias, external filter, build recipe | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.06 | Runtime own-rights code definitions: shell functions, aliases, editor commands | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.07 | Browser extension executing with browser-equivalent rights | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C8.08 | Settings only read as values, such as theme or home page | CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): recorded bytecode consumes received default, personal values/document work passes and chosen system setting reads back; general semantic readers incomplete |
| C9.1 | Rootful image pull/run, mutable tags and manager API | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C9.2 | Rootless containers, user namespaces, alternative OCI runtime invocation | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C9.3 | Bind-mounted executable/script, writable overlay, exec into container and package install inside | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C9.4 | Image build RUN/hooks, import/load archive and commit modified container | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C9.5 | Privileged/host-namespace/device/runtime-hook options | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C9.6 | Removed image/container restarted through old name, daemon state, API or retained layers | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| C10.1 | Documented privileged package/service/account/network/firewall administration | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C10.2 | Built-in privileged tool changes guards, permissions, mounts or execution policy | CLOSED | NOT CLOSED | 1 | Per-variant evidence map |
| C10.3 | Retained arbitrary privileged hooks and multi-resource live side effects | NOT CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| C10.4 | Root editor with documented package installer | NOT CLOSED | CLOSED | 1 | Per-variant evidence map |
| M1.01 | All C1–C10: successful inactive preparation versus actual application report | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M1.02 | All C1–C10: complete live activation and success report across all objects | NOT CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M2.01 | All C1–C10: durable exact file generation and boot selection after report | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M2.02 | All C1–C10: add/change/remove power cut with complete runtime/device replay | NOT CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M3.01 | All C1–C10: explicit failure or timeout while only inert preparation changed | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M3.02 | All C1–C10: partial activation failure, stalled worker, or no report at one hour | NOT CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M4.01 | All C1–C10: running code, descendants, open FDs and mapped/injected copies | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M4.02 | All C1–C10: executable aliases, copied cache/store/image content, old generations | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M4.03 | All C1–C10: service activators, timers, restart policy and effective rules | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M4.04 | All C1–C10: contributions shared with remaining declaration lines | CLOSED | NOT CLOSED | 3 | Not assessed in this round |
| M5.01 | All C1–C10: finite typed lines, exact content, permissions and documented defaults | NOT CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): exact own/package/derived matching and removal sensitivity pass; independent census remains incomplete with native receipts and unobserved semantics FACT_UNKNOWN |
| M5.02 | All C1–C10: unrestricted algorithmic requirements and semantic effects | NOT CLOSED | NOT CLOSED | 2 | [Round 2 coverage](../../round-2/COVERAGE.md): finite JSON rows and copy/bytecode algorithms pass; actual unrestricted-algorithm request explicitly refuses and remains unsupported |
