# Saved code readers — 2026-11-24 UTC

Current published release42: native mpv/libmpv Lua/JavaScript and discovery guards
passed in41; pdb/gyp/curl guards and native apt/dpkg/cron store denials passed in42.
Exact originals, native positives, removal and outside-inventory evidence are in
STATE.md, MPV-041-DOCUMENTATION.md and records/readers-0.42.log. Release43 work
adds native ed; its canonical gates are pending. OpenSSH saved configuration,
separately installed embedded libraries and document macros remain unclaimed.

The release-by-release prototype observations below are historical. Their older
“open”/“pending” labels describe the named release, not the current implementation.

Release39 integrates the exact Flatpak Bash/sh and Python/libpython
overrides and original-object alias denials; canonical two-boot/removal checks
passed. Native mpv Lua remains OPEN. See flatpak-readers-component-draft.md and
the exact packaged manifest/provenance; unknown runtime versions are unclaimed.

Standalone Flatpak-runtime prototypes now pass bounded guest checks: static
Bash nine direct refusals plus recorded/source/startup/typed/data controls;
Python3.14 twenty-one direct refusals plus seven positive controls. Evidence:
records/flatpak-bash-0.34.log and records/flatpak-python-0.34.log. These are declared
standalone programs, not replacements for the original runtime readers. Original
readers remain open. ABI/optional-module/provenance and OSTree-object exposure
limits are listed in flatpak-reader-integration-draft.md; no integration claim.

Target: REVIEW.md R1 direct routes; S8.2-9 and S8.3-6. No outcome0 is claimed.
Release29 adds optional dash/mawk/gawk/GNU sed/make checks to the native
Bash/Python/Perl/BusyBox component. Direct routes, restart, removal, smoke,
updates, pip/npm and browser/document/compiler checks passed. Release evidence,
game checks and source/inventory verification are recorded in STATE.md.
Release30 adds native Node/libnode, including snapshot/environment/policy readers.
Native route/restart/removal, smoke, updates, language, ordinary and game checks
passed. Candidate31 adds Git readers; candidate32 adds Neovim AppImage readers.
Their native tests passed; release verification is tracked in STATE.md.

| Reader | Direct input routes | Current evidence/status |
|---|---|---|
| Bash | script file, stdin, source/dot, BASH_ENV, rcfile, fd aliases, redirected parser input | Patched prototype closes32 tested routes in home/tmp/shm, including root; declared script runs as file/stdin/source. records/bash-code-routes.log. Native26 remains open. |
| CPython | script/stdin, -m, source/bytecode imports, zipimport, runpy, .pth, startup | Patched prototype closes38 tested routes, with recorded/typed/data controls; records/python-code-routes.log. First sourceless.pyc bypass preserved and repaired. Native26 open. |
| Perl | script/stdin, require/do, modules, startup options | Patched prototype closes33 tested routes plus recorded/typed/data/native-module controls; records/perl-code-routes.log. Native26 with Perl installed remains open. |
| BusyBox ash/sh | script/stdin, source/dot, startup | Candidate28 passes native aliases and restart with39 total BusyBox refusals plus recorded/typed/data controls. records/native-reader-routes-0.28.log. |
| dash, other package shells | script/stdin, dot, startup | Candidate29 native dash/awk/sed passes69 refusal routes and recorded/typed/data controls before/after restart, plus optional removal. records/native-optional-readers-0.29.log. Other package shells remain open. |
| BusyBox awk; GNU awk; mawk | -f program, included program files | Native29 file/fd routes passed before/after restart; optional removal and gawk exact arithmetic/native extension controls passed. records/native-optional-readers-0.29.log. |
| BusyBox sed; GNU sed | -f program (including command execution where supported) | Native29 file/fd routes passed before/after restart with recorded/data controls; optional removal restores the base BusyBox alias. records/native-optional-readers-0.29.log. |
| GNU make | -f/default makefile, includes, startup environment | Candidate29 native make passes30 refusals and recorded/typed/pipe controls before/after restart, plus removal; records/native-optional-readers-0.29.log. Fixed inherited temp cleanup after first run deleted a fixture. Checked stdin uses sealed anonymous memory. Not mediated in28. |
| Node.js | script, CommonJS/ES module imports, preload, stdin, package.json resolver settings, snapshot builder/config/blob, dotenv, policy | Repaired native30 passes79 direct-route refusals before/after restart and removal;24 additional snapshot/environment/policy refusals, recorded snapshot loading after restart and other recorded/typed/data controls passed. records/native-node-0.30.log and node-snapshots-0.30.log. Not included in29. |
| Git | hooks, executable aliases and configurable external commands | Native28 alternate/local/include aliases executed, including sudo and after restart; records/git-readers-0.28.log. Candidate31 native routes, helper aliases, recorded alias/hook/repository controls, restart and removal passed; records/native-git-0.31.log. Release verification remains pending. |
| Embedded Python/Perl libraries | Native API script/import readers | Standalone executable patches do not replace separately installed libpython/libperl packages. Embedded routes need independent tests and library integration. |
| Neovim/Vim/BusyBox vi | startup scripts, source, embedded language/plugin readers | Original recorded Neovim0.10.4 AppImage executes all27 tested direct inputs; records/nvim-readers-0.29.log. Candidate32 passes45 refusals through the launcher/internal binary and after restart, recorded/typed/data/document controls and shared/final-owner removal; records/native-nvim-0.32.log. Vim/BusyBox vi remain untested. |
| LibreOffice | document macros and executable configuration | Needs direct-route inspection and ordinary-document controls. |
| Flatpak/OCI payload interpreters | Same readers inside recorded application/runtime/image | Recorded Flatpak on30 executes all9 tested shell/Python/mpv-Lua routes in home/tmp/shm; recorded controls pass. App context is unconfined and shm executable. records/flatpak-reader-routes-0.30.log. OCI still needs direct-route evidence. |
| LinuxGSM | shell launcher and downloaded shell functions | Recorded immutable launcher install/run/update/removal passed with patched native shell on28; records/game-0.28.log. |
| ELF loader/native exec | direct path, loader argument, native shared-object load | Existing noexec/AppArmor refuses tested home-native and loader routes; code19 evidence. |

Prototype mechanism: checks the already-open descriptor. A regular code input must
belong to an executable read-only mount. It need not have an executable mode bit:
package libraries and declared0644 source files are legitimate code. The kernel
reported `unconfined` boot/apply context is exempt; no environment-variable switch
disables checks in a session. Pipes/terminals remain usable. Data reads are unchanged.
This depends on current session mount confinement and needs namespace/runtime tests.

Documentation read before implementation:

- https://docs.kernel.org/userspace-api/check_exec.html — interpreters must cooperate;
  upgrading the kernel alone is not enforcement. The prototype uses current6.12
  descriptor/mount checks, not AT_EXECVE_CHECK. No backports kernel was installed.
- https://docs.python.org/3.13/c-api/file.html — native code-open API/hook.
- https://docs.python.org/3.13/library/io.html#io.open_code — distinct code-file opener.

`cat F | bash` is a data route under REVIEW R4: a typed command hands data to the
interpreter. Record its effects separately; do not close typed/piped commands.

Development33 evidence retained in34: native BusyBox vi saved .exrc refusals and
recorded option-value, typed option-value, ordinary save, root, restart and removal
controls pass (records/native-vi-0.33.log). Startup shell-command SIGSEGV is also
present upstream; records/vi-startup-baseline.log records both binaries.
Flatpak processes now enter confos-flatpak(enforce); recorded Python/Lua and mpv
controls pass, but all9 original shell/Python/mpv-Lua direct routes remain open
(records/flatpak-confined-0.33.log). Confinement alone does not mediate code reads.
