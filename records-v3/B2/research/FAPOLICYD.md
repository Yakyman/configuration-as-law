# Selected partial implementation: file-access enforcement

Recorded 2026-11-22 UTC. This supplements DESIGN-NOTE.md for the builder-selected fresh Linux VM, finite JSONL declaration broker, declaration-generated fapolicyd trust database, managed systemd services, and actual account/network/firewall backends. IPE is an alternative discussed in the design note, not a claim about the selected prototype. No probe has run in this research task.

## Primary source ledger consulted before development observations

| ID | Source and short exact quotation | Consequence for this prototype |
|---|---|---|
| F1 | [Rules manual](https://raw.githubusercontent.com/linux-application-whitelisting/fapolicyd/main/doc/fapolicyd.rules.5): “the first rule to match being used” | Check ordered effective rules. Permitted trusted execution followed by deny execution is a bounded native-entry policy. Subject executable and object trust are distinct fields. |
| F2 | [Configuration manual](https://raw.githubusercontent.com/linux-application-whitelisting/fapolicyd/main/doc/fapolicyd.conf.5): “Selecting this option will calculate a SHA256 hash by cryptographic means.” | Explicit `integrity=sha256`, `trust=file`, `permissive=0`. Build trust only from the current declaration's exact manifests. Database contents and effective configuration must be read back after reload. Defaults do not establish this. |
| F3 | [Upstream README](https://raw.githubusercontent.com/linux-application-whitelisting/fapolicyd/main/README.md): “No bypass of security by executing programs via ld.so.” | This is a stock policy goal, not proof for custom rules. Gate untrusted ELF/shared-object opens as well as direct execution. Source describes fanotify execution-permission support as a runtime prerequisite. |
| F4 | [Stock shell rule](https://raw.githubusercontent.com/linux-application-whitelisting/fapolicyd/main/rules.d/72-shell.rules): `allow perm=any all : ftype=text/x-shellscript` | Do not include this unconditional shell allowance. It does not require declaration trust. |
| F5 | [Stock language rule](https://raw.githubusercontent.com/linux-application-whitelisting/fapolicyd/main/rules.d/70-trusted-lang.rules): `deny_audit perm=any all : ftype=%languages` | Preceded by a trusted-language allow, it demonstrates a MIME-class rule. It does not cover every plain-text instruction stream or custom dispatcher. |

URLs track upstream main, so these are mechanism references, not exact binary/version evidence. Record the actual installed version and consult its shipped manual before depending on options absent in older releases. Do not copy repository navigation or raw document headers into publishable task records.

F2 additionally documents filesystem watch selection and filesystem marks. Default watches are ext4, xfs and tmpfs. `allow_filesystem_mark=1` extends observation beneath bind/overlay mounts; default is 0 and kernel support matters. Do not leave required executable trees outside observation. Avoid ignored mounts. These are policy coverage obligations, not proof containers are closed.

## Narrow mechanism and limits

Use current-declaration file digests to populate trust. Deny untrusted executable entry and untrusted ELF/library opens. For known interpreter executables, deny opens of untrusted candidate code; document which executables and input routes are covered. MIME recognition alone misses scripts presented as text or instructions consumed by a recorded custom dispatcher. A deny of *all* untrusted file opens by an interpreter is stronger for file input but denies documents and project data too; argv/stdin/IPC are still outside it.

Do not grant unrestricted interpreter data reads merely to let the broker read JSONL unless the broker is isolated from arbitrary code execution. A rule that trusts every process whose executable is the broker's Python interpreter also trusts other executions of that interpreter. Executable path matching is not script identity. A general exception for root would also exempt root built-in tools, contrary to S2.3-7. These are implementation gaps if no independent boundary is present.

`MemoryDenyWriteExecute` on managed systemd services constrains those services, not every login process. File-access admission does not cover anonymous native memory execution or all already-open/mapped objects. Native-entry success cannot establish C7.16/C7.22, full Removal, or C1–C10 full-R closure. Changing trust must quiesce holders and establish effective new policy before success; a daemon restart may create an enforcement interval that needs analysis.

Root frontend interception can provide useful refusal/translation paths, but stock backends retained for the broker can still be invoked directly unless an additional boundary denies those paths. The same applies to fapolicyd administration and service-manager APIs. Treat direct-backend and policy-disabling built-in commands as NOT CLOSED where unsupported, not as root breaking. General-purpose privileged direct file edits retain the text's breaking exclusion.

## Source-first development questions and proposed expectations

These are planning entries only, not observations or authorization to repeat existing B1 probes. The builder must enter exact commands, unique development inputs and timestamp before any unanswered integration probe. Documentation answers primitive behavior; observations should address only the composed prototype.

| Item | Unanswered integration question | Expected observation to record before running | Required evidence |
|---|---|---|---|
| File admission | Does the custom effective policy and explicit trust DB permit one declared development executable and deny its undeclared copy on this VM? | Declared file succeeds; copied unknown path is refused with a matching rule. | Version/configuration, effective rules, trust entries, stdout/status and daemon decision. |
| Loader entry | Does custom ELF-open ordering cover a direct-loader invocation of a development executable outside trust? | No development payload executes; open refusal identifies custom rule. | Exact loader path, artifact checksum, exit status and denial. Distinct from direct exec question. |
| Interpreter data boundary | Does the selected subject rule deny an untrusted development script file without preventing the selected document editor from reading plain documents? | File script refused; document edit succeeds. | Exact real interpreter identity, trust status, file type, refusal and resulting document. No inference to stdin/argv. |
| Broker admission | Does adding a finite program line make the declared exact artifact usable only after a successful apply? | Apply reports success after trust reload/readback; verify matches bytes and modes. | Before/after declaration hash, observed trust/policy, payload launch result and verify row. |
| Removal | Does removing that line terminate its managed process and deny its former file and retained copy? | Process absent; launch denied; remaining shared contributions still work. | Process/control-group readback and actual execution denials, plus residual dependency map. Interpretive copies remain separate. |
| Root refusal | Does each provided frontend refuse or translate the tested root invocation? | Refusal or successful declaration transaction. | Full argv, effective uid, old/new declaration, actual system state. Direct stock backend remains a documented gap unless separately closed. |
| Failure | Does a deliberately invalid finite declaration leave prior state and declaration untouched? | Failure report; old verify rows pass. | Invalid candidate, previous hash, status and actual-state verification. This only demonstrates the exercised phase, not arbitrary partial activation recovery. |
| Durability | Does the exact reported add/change/remove survive an immediate VM power cut? | Selected declaration hash and every line's effective state survive boot. | Success marker timing, host cut invocation, boot identity, current declaration and verification. Do not substitute graceful shutdown. |
| Reproducibility | Do two independent clean images with identical finite declaration produce equal required fields? | Per-line compare values match. | Independent creation records, same declaration digest, both complete snapshots and diff. |

Do not empirically rerun stock interpreter securebit behavior: B1 already measured that question, and it is not the selected policy. Non-file own-rights inputs and arbitrary custom dispatch may be retained as known open routes without trying to turn a new file-open success into their closure. Radio paths should create backend-readable state and report not tested on hardware.
